#!/usr/bin/env python3
"""
seedance-brief-runner — executes a compiled segment manifest (segments.json)
through Higgsfield's Seedance 2.0 CLI: casting call, voice-anchor lock,
last-frame chaining, product keyframe overrides, stitch, resume, single-segment regen.

Commands:
  cast        Generate N takes of segment 1 (casting call for the voice anchor)
  set-anchor  Promote a casting take to segment 1 (locks voice anchor + seed chain)
  run         Generate segments (chains 2..N by default; --from / --only supported)
  stitch      Concat all segments into final.mp4
  status      Show what exists / what's missing

Usage:
  python3 run_brief.py cast       --manifest segments.json [--takes 3]
  python3 run_brief.py set-anchor --manifest segments.json --take 2
  python3 run_brief.py run        --manifest segments.json [--from 2] [--only 5]
  python3 run_brief.py stitch     --manifest segments.json
  python3 run_brief.py status     --manifest segments.json

Requires: higgsfield CLI (authed), ffmpeg/ffprobe, curl. Python stdlib only.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys

BANNED_DIALOGUE = ["...", "…", "—", "--"]  # ellipses + em-dash render as dead air
CR_PER_SECOND = 2.75  # ~22 credits per 8s observed


def die(msg, code=1):
    print(f"[runner] ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def log(msg):
    print(f"[runner] {msg}", file=sys.stderr)


def load_manifest(path):
    if not os.path.isfile(path):
        die(f"manifest not found: {path}")
    with open(path) as f:
        try:
            m = json.load(f)
        except json.JSONDecodeError as e:
            die(f"manifest is not valid JSON: {e}")
    for key in ("output_dir", "avatar_keyframe", "segments"):
        if key not in m:
            die(f"manifest missing '{key}'")
    if not os.path.isfile(m["avatar_keyframe"]):
        die(f"avatar keyframe not found: {m['avatar_keyframe']}")
    if "prompt_template" not in m and not all(s.get("prompt") for s in m["segments"]):
        die("manifest needs 'prompt_template' or a full 'prompt' on every segment")
    for img in m.get("reference_images", []):
        if not os.path.isfile(img):
            die(f"reference image not found: {img}")
    for s in m["segments"]:
        for key in ("index", "duration", "dialogue"):
            if key not in s:
                die(f"segment missing '{key}': {s}")
        # house style: no ellipses / em dashes anywhere the model reads
        for text, label in ((s["dialogue"], "dialogue"), (s.get("prompt", ""), "prompt")):
            for bad in BANNED_DIALOGUE:
                if bad in text:
                    die(f"segment {s['index']} {label} contains banned '{bad}' "
                        f"(ellipses/em-dashes: dead-air pauses + house style). Fix the manifest.")
        si = s.get("start_image")
        if si and not os.path.isfile(si):
            die(f"segment {s['index']} start_image not found: {si}")
        ac = s.get("audio_chunk")
        if ac and not os.path.isfile(ac):
            die(f"segment {s['index']} audio_chunk not found: {ac}")
        for img in s.get("images", []):
            if not os.path.isfile(img):
                die(f"segment {s['index']} image not found: {img}")
    m["segments"].sort(key=lambda s: s["index"])
    idxs = [s["index"] for s in m["segments"]]
    if idxs != list(range(1, len(idxs) + 1)):
        die(f"segment indexes must be 1..N contiguous, got {idxs}")
    os.makedirs(m["output_dir"], exist_ok=True)
    return m


def build_prompt(m, seg, include_voice_line):
    # UGC-Director mode: segment carries its own full dense timestamped prompt
    # (compiled per _engine/standalone-skills/UGC DIRECTOR.md). Used verbatim.
    if seg.get("prompt"):
        p = seg["prompt"]
        if include_voice_line and m.get("voice_line") and "<VOICE_LINE>" in p:
            p = p.replace("<VOICE_LINE>", m["voice_line"].strip())
        return p
    # Legacy template mode
    p = m["prompt_template"]
    p = p.replace("<DEVIATION>", seg.get("deviation", "").strip() or "natural")
    p = p.replace("<DIALOGUE>", seg["dialogue"].replace('"', '\\"'))
    p = p.replace("<CUE>", seg.get("cue", "").strip() or "natural gestures")
    p = p.replace("<DURATION>", str(seg["duration"]))
    extra = seg.get("extra_prompt", "").strip()
    p = p.replace("<EXTRA>", (" " + extra) if extra else "")
    if include_voice_line and m.get("voice_line"):
        p = f"{p} {m['voice_line'].strip()}"
    return p


def seg_dir(m, i):
    return os.path.join(m["output_dir"], f"seg_{i}")


def anchor_wav(m):
    return os.path.join(seg_dir(m, 1), "segment_audio.wav")


def generate_one(m, seg, seed_image, out_dir, audio=None):
    os.makedirs(out_dir, exist_ok=True)
    prompt = build_prompt(m, seg, include_voice_line=(seg["index"] == 1))
    args = [
        "higgsfield", "generate", "create", "seedance_2_0",
        "--prompt", prompt,
        "--start-image", seed_image,
        "--aspect_ratio", m.get("aspect_ratio", "9:16"),
        "--duration", str(seg["duration"]),
        "--resolution", m.get("resolution", "720p"),
        "--mode", m.get("mode", "std"),
        "--wait", "--wait-timeout", "25m", "--json",
    ]
    # NOTE: the CLI maps every image to start_image for seedance_2_0 (max one) —
    # @Image multi-references are a web-UI feature. Identity/product lock = the start frame.
    if m.get("reference_images") or seg.get("images"):
        log(f"seg {seg['index']}: ignoring reference_images/images — CLI seedance accepts "
            f"only one start image; encode identity/product in the start frame instead.")
    if audio:
        args += ["--audio", audio]
    log(f"seg {seg['index']}: generating ({seg['duration']}s, "
        f"audio={'anchor' if audio else 'native'}) ...")
    with open(os.path.join(out_dir, "seg_job.json"), "w") as f:
        r = subprocess.run(args, stdout=f, stderr=subprocess.PIPE, text=True)
    if r.returncode != 0:
        err = r.stderr[-2000:]
        hint = ""
        low = err.lower()
        if "401" in low or "unauthorized" in low or "session" in low or "auth" in low:
            hint = ("\n[runner] HINT: looks like an expired Higgsfield session — run "
                    "'higgsfield auth login', then re-run this command (done segments skip).")
        elif "ssl" in low or "certificate" in low:
            hint = ("\n[runner] HINT: SSL error — export "
                    "SSL_CERT_FILE=$(python3 -m certifi) and re-run.")
        die(f"seg {seg['index']} higgsfield call failed:\n{err}{hint}")
    with open(os.path.join(out_dir, "seg_job.json")) as f:
        job = json.load(f)
    node = job[0] if isinstance(job, list) else job
    url = node.get("result_url") or (node.get("results") or [{}])[0].get("result_url")
    if not url:
        die(f"seg {seg['index']}: no result_url in seg_job.json — inspect {out_dir}/seg_job.json")
    mp4 = os.path.join(out_dir, "seg.mp4")
    r = subprocess.run(["curl", "-sSL", "--fail", "-o", mp4, url])
    if r.returncode != 0:
        die(f"seg {seg['index']}: download failed")
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-sseof", "-0.25", "-i", mp4, "-vframes", "1", "-q:v", "2",
                    os.path.join(out_dir, "segment_lastframe.png")], check=True)
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-i", mp4, "-vn", "-ac", "1", "-ar", "48000", "-c:a", "pcm_s16le",
                    os.path.join(out_dir, "segment_audio.wav")], check=True)
    log(f"seg {seg['index']}: saved {mp4}")
    return mp4


def seed_for(m, seg):
    """Seed image for a segment: explicit override, else previous segment's last frame,
    else the avatar keyframe for segment 1."""
    if seg.get("start_image"):
        return seg["start_image"]
    if seg["index"] == 1:
        return m["avatar_keyframe"]
    prev = os.path.join(seg_dir(m, seg["index"] - 1), "segment_lastframe.png")
    if not os.path.isfile(prev):
        die(f"seg {seg['index']}: previous last frame missing ({prev}). "
            f"Run earlier segments first (or use --from/--only correctly).")
    return prev


def audio_for(m, seg):
    """Audio input: per-segment ElevenLabs chunk if present, else the seg-1 anchor
    (segments 2..N), else none (segment 1 establishes the voice)."""
    if seg.get("audio_chunk"):
        return seg["audio_chunk"]
    if seg["index"] == 1:
        return None
    a = anchor_wav(m)
    if not os.path.isfile(a):
        die("voice anchor missing — run 'cast' then 'set-anchor' (or generate seg 1) first.")
    return a


def cmd_cast(m, takes):
    seg1 = m["segments"][0]
    est = int(takes * seg1["duration"] * CR_PER_SECOND)
    log(f"casting call: {takes} takes of segment 1 (~{est} credits)")
    for t in range(1, takes + 1):
        out = os.path.join(m["output_dir"], "cast", f"take_{t}")
        if os.path.isfile(os.path.join(out, "seg.mp4")):
            log(f"take {t}: exists, skipping")
            continue
        generate_one(m, seg1, m["avatar_keyframe"], out, audio=None)
    print("\nCasting takes ready — LISTEN to each and pick the most alive delivery")
    print("(expressive pitch movement, energy held to the final word, no teleprompter):")
    for t in range(1, takes + 1):
        print(f"  take {t}: {os.path.join(m['output_dir'], 'cast', f'take_{t}', 'seg.mp4')}")
    print(f"\nThen: python3 run_brief.py set-anchor --manifest <manifest> --take <n>")


def cmd_set_anchor(m, take):
    src = os.path.join(m["output_dir"], "cast", f"take_{take}")
    if not os.path.isfile(os.path.join(src, "seg.mp4")):
        die(f"take {take} not found at {src}")
    dst = seg_dir(m, 1)
    if os.path.isdir(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    log(f"segment 1 = casting take {take}. Voice anchor locked: {anchor_wav(m)}")
    log("next: python3 run_brief.py run --manifest <manifest> --from 2")


def cmd_run(m, start_from, only):
    segs = m["segments"]
    if only is not None:
        targets = [s for s in segs if s["index"] == only]
        if not targets:
            die(f"--only {only}: no such segment")
        if only < len(segs):
            log(f"WARNING: regenerating seg {only} changes its last frame — segments "
                f"{only + 1}..{len(segs)} were seeded from the old one. Re-run them "
                f"(--from {only + 1}) if the visual seam matters.")
    else:
        targets = [s for s in segs if s["index"] >= start_from]
    total_s = sum(s["duration"] for s in targets)
    log(f"generating {len(targets)} segment(s), ~{total_s}s of video, "
        f"~{int(total_s * CR_PER_SECOND)} credits")
    for seg in targets:
        out = seg_dir(m, seg["index"])
        if only is None and os.path.isfile(os.path.join(out, "seg.mp4")):
            log(f"seg {seg['index']}: exists, skipping (use --only {seg['index']} to redo)")
            continue
        generate_one(m, seg, seed_for(m, seg), out, audio=audio_for(m, seg))
    cmd_status(m)


def cmd_stitch(m):
    parts = []
    for s in m["segments"]:
        mp4 = os.path.join(seg_dir(m, s["index"]), "seg.mp4")
        if not os.path.isfile(mp4):
            die(f"seg {s['index']} missing — finish 'run' first")
        parts.append(mp4)
    lst = os.path.join(m["output_dir"], "concat.txt")
    with open(lst, "w") as f:
        for p in parts:
            f.write(f"file '{p}'\n")
    final = os.path.join(m["output_dir"], "final.mp4")
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-f", "concat", "-safe", "0", "-i", lst,
                    "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                    "-c:a", "aac", "-b:a", "192k",
                    "-pix_fmt", "yuv420p", "-movflags", "+faststart", final], check=True)
    dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", final], capture_output=True, text=True)
    log(f"final: {final} ({float(dur.stdout.strip()):.1f}s)")
    print(final)


def cmd_status(m):
    print(f"\n{m.get('concept_id', '(no id)')} — {m['output_dir']}")
    cast_dir = os.path.join(m["output_dir"], "cast")
    if os.path.isdir(cast_dir):
        takes = sorted(d for d in os.listdir(cast_dir) if d.startswith("take_"))
        print(f"  casting takes: {', '.join(takes) if takes else 'none'}")
    for s in m["segments"]:
        mp4 = os.path.join(seg_dir(m, s["index"]), "seg.mp4")
        mark = "DONE " if os.path.isfile(mp4) else "  -  "
        extras = []
        if s.get("start_image"):
            extras.append("seed-override")
        if s.get("audio_chunk"):
            extras.append("11labs-audio")
        print(f"  [{mark}] seg {s['index']:>2} ({s['duration']}s) "
              f"{(' [' + ','.join(extras) + ']') if extras else ''}")
    final = os.path.join(m["output_dir"], "final.mp4")
    print(f"  final.mp4: {'DONE' if os.path.isfile(final) else 'not stitched'}\n")


def main():
    ap = argparse.ArgumentParser(description="Seedance segment-brief runner")
    ap.add_argument("command", choices=["cast", "set-anchor", "run", "stitch", "status"])
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--takes", type=int, default=3)
    ap.add_argument("--take", type=int)
    ap.add_argument("--from", dest="start_from", type=int, default=1)
    ap.add_argument("--only", type=int)
    args = ap.parse_args()

    for tool in ("higgsfield", "ffmpeg", "ffprobe", "curl"):
        if shutil.which(tool) is None:
            die(f"'{tool}' not on PATH")

    m = load_manifest(args.manifest)
    if args.command == "cast":
        cmd_cast(m, args.takes)
    elif args.command == "set-anchor":
        if args.take is None:
            die("set-anchor requires --take N")
        cmd_set_anchor(m, args.take)
    elif args.command == "run":
        cmd_run(m, args.start_from, args.only)
    elif args.command == "stitch":
        cmd_stitch(m)
    elif args.command == "status":
        cmd_status(m)


if __name__ == "__main__":
    main()
