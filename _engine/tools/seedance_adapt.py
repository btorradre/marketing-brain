#!/usr/bin/env python3
"""
Reference video -> Seedance 2.5 prompt scaffold.

Implements the replication intake in _engine/sops/Seedance-Prompt-System.md.

The split that makes this reliable: ffmpeg finds the cuts (deterministic, frame
accurate), Gemini describes what is inside them (it is good at description and
bad at timestamps). Asking a model "when are the cuts" produces confident wrong
numbers; handing it the real cut list and asking "what happens between 4.2 and
7.8" produces something you can fire.

    # 1. extract the reference half of the module stack
    python3 seedance_adapt.py analyze <url|path> --out runs/myref

    # 2. emit a fireable scaffold, retimed to the length you actually want
    python3 seedance_adapt.py scaffold runs/myref/reference.json \
        --target 25 --profile P2 --out runs/myref/prompt.txt

    # 3. fill the TODO blocks with OUR cast/product/voice/dialogue, then
    python3 seedance_prompt_lint.py runs/myref/prompt.txt --duration 25 --profile P2

Requires: ffmpeg, yt-dlp (for URLs), GEMINI_API_KEY in marketing brain/.env
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
MODEL_CHAIN = ["gemini-3.1-pro-preview", "gemini-3-pro-preview", "gemini-2.5-pro"]

WPS_TARGET = 2.8
ENGINE_MAX_SECONDS = 30
ENGINE_MIN_SECONDS = 4
MIN_BEAT_SECONDS = 0.8   # research: merge anything under ~1s into its neighbour

CUT_HEADERS = {
    "hard cut": "SHOT {n}. HARD CUT.",
    "jump cut": "SHOT {n}. JUMP CUT.",
    "match cut": "SHOT {n}. MATCH CUT.",
    "continuous": "SHOT {n}. CONTINUOUS.",
}


def load_env():
    env = REPO / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


# ---------------------------------------------------------------- acquisition

def acquire(src, outdir):
    outdir.mkdir(parents=True, exist_ok=True)
    dest = outdir / "reference.mp4"
    if dest.exists():
        print(f"  reusing {dest}")
        return dest
    if re.match(r"^https?://", src):
        if not shutil.which("yt-dlp"):
            sys.exit("yt-dlp not installed and the source is a URL")
        print(f"  downloading {src}")
        r = run(["yt-dlp", "-f", "mp4/best", "-o", str(dest), "--no-playlist", src])
        if not dest.exists():
            # some hosts serve a direct file yt-dlp declines
            r2 = run(["curl", "-sL", "-A", "Mozilla/5.0", "-o", str(dest), src])
            if not dest.exists() or dest.stat().st_size < 10000:
                sys.exit(f"download failed:\n{r.stderr[-800:]}\n{r2.stderr[-400:]}")
    else:
        p = Path(src).expanduser()
        if not p.exists():
            sys.exit(f"not found: {p}")
        shutil.copy(p, dest)
    return dest


def probe_duration(path):
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", str(path)])
    return round(float(r.stdout.strip()), 2)


# ------------------------------------------------------------ cut detection

def detect_cuts(path, threshold):
    """Frame-accurate hard-cut timestamps via ffmpeg scene score.

    Use metadata=print, NOT showinfo. showinfo logs at INFO level, so pairing it
    with `-v error` silently prints nothing and every video looks like a single
    continuous take. That false negative cost a whole round of wrong conclusions.
    """
    r = run(["ffmpeg", "-v", "error", "-i", str(path),
             "-vf", f"select='gt(scene,{threshold})',metadata=print:file=-",
             "-an", "-f", "null", "-"])
    times = [float(m) for m in re.findall(r"pts_time:([0-9.]+)", r.stdout)]
    # collapse near-duplicates (a cut can score twice on adjacent frames)
    out = []
    for t in sorted(times):
        if not out or t - out[-1] > 0.35:
            out.append(round(t, 2))
    return out


def auto_cuts(path, duration, threshold=None):
    """Walk the threshold down until cuts appear, so we don't miss soft cuts.

    A fast-cut ad often has a rapid opening montage and a slower back half. The
    first threshold that returns ANY cut will find the hard opening cuts and miss
    the softer ones later, so keep walking down and take the richest reading that
    still looks like an edit rather than camera motion.
    """
    if threshold is not None:
        return [c for c in detect_cuts(path, threshold) if 0.3 < c < duration - 0.3], threshold
    best, best_th = [], 0.4
    for th in (0.4, 0.3, 0.2, 0.12):
        cuts = [c for c in detect_cuts(path, th) if 0.3 < c < duration - 0.3]
        if len(cuts) > len(best):
            best, best_th = cuts, th
        # stop before cuts get so dense they are obviously motion, not edits
        if len(cuts) > duration / 0.6:
            break
    return best, best_th


def build_windows(cuts, duration, min_beat=MIN_BEAT_SECONDS):
    bounds = [0.0] + cuts + [duration]
    wins = []
    for i in range(len(bounds) - 1):
        s, e = bounds[i], bounds[i + 1]
        if e - s >= min_beat or not wins:
            wins.append([round(s, 2), round(e, 2)])
        else:
            wins[-1][1] = round(e, 2)  # absorb a flash-frame into the previous beat
    return wins


# ------------------------------------------------------------------- gemini

SCHEMA_INSTRUCTION = """You are extracting the REFERENCE half of a video ad so it can be
rebuilt with a different person, different wardrobe, different room, and a different product.

I have already detected the cuts with frame-accurate tooling. The beat windows below are
GROUND TRUTH. Do not invent, merge, split, or renumber them. Describe what happens inside
each one.

BEAT WINDOWS (seconds):
{windows}

Return ONLY JSON matching this shape:

{{
  "runtime": <float, total seconds>,
  "look": "<capture medium, lens character, lighting direction and quality, colour grade. One or two sentences.>",
  "sound": "<music, room tone, SFX. One sentence.>",
  "words_per_second": <float, total spoken words / runtime>,
  "format_note": "<aspect ratio and anything structural about how it is shot>",
  "beats": [
    {{
      "index": <int, 1-based, matching the windows above in order>,
      "start": <float>,
      "end": <float>,
      "cut_type": "<how the PREVIOUS beat ends into this one. One of: open (first beat only), hard cut, jump cut, match cut, continuous>",
      "frame": "<shot size and camera position, plus any camera move. Name at most one move.>",
      "action": "<the physical action, concrete verbs tied to a body part. No abstractions.>",
      "dialogue": "<verbatim transcript for this window, or empty string if silent>",
      "word_count": <int>,
      "on_screen_text": "<verbatim burned-in text, or empty string>",
      "role": "<what this beat does for the ad: hook, problem, mechanism, proof, product reveal, cta, or broll>"
    }}
  ]
}}

RULES:
- "jump cut" means the framing/setup is essentially the same and time skips. "hard cut"
  means the framing or location genuinely changes. "match cut" means composition is held
  while contents change. Choose carefully, it drives how the rebuild is prompted.
- Do NOT describe the person, their face, their clothes, the room decor, or the product.
  All of those are being replaced. Describing them pollutes the rebuild.
- Do describe SHOT SIZE, CAMERA POSITION, and PHYSICAL ACTION precisely, because those are
  what gets replicated.
- Transcribe dialogue verbatim including filler words. Empty string if nobody speaks.
"""


def gemini_analyze(video, windows, duration):
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        sys.exit("pip install google-genai")

    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        sys.exit("GEMINI_API_KEY not set")
    client = genai.Client(api_key=key)

    size = video.stat().st_size
    part = None

    # Reference ads are short. Under the inline-request ceiling, sending bytes
    # directly avoids the Files API entirely, which is the step that flakes.
    if size < 18_000_000:
        print(f"  sending inline ({size/1e6:.1f}MB)")
        part = types.Part.from_bytes(data=video.read_bytes(), mime_type="video/mp4")
    else:
        for attempt in range(1, 4):
            try:
                print(f"  uploading to Gemini ({size/1e6:.1f}MB, attempt {attempt})")
                up = client.files.upload(file=str(video))
                while up.state == "PROCESSING":
                    time.sleep(2)
                    up = client.files.get(name=up.name)
                if up.state != "ACTIVE":
                    raise RuntimeError(f"upload state {up.state}")
                part = types.Part.from_uri(file_uri=up.uri, mime_type="video/mp4")
                break
            except Exception as e:  # noqa: BLE001
                print(f"    upload failed: {str(e)[:160]}")
                if attempt == 3:
                    sys.exit("gemini upload failed 3x; check network and retry")
                time.sleep(4 * attempt)

    win_txt = "\n".join(
        f"  beat {i+1}: [{s:.2f} - {e:.2f}]  ({e-s:.2f}s)" for i, (s, e) in enumerate(windows)
    )
    prompt = SCHEMA_INSTRUCTION.format(windows=win_txt)

    last = None
    for model in MODEL_CHAIN:
        try:
            print(f"  analyzing with {model}")
            resp = client.models.generate_content(
                model=model,
                contents=[part, prompt],
                config=types.GenerateContentConfig(
                    temperature=0.1,
                    response_mime_type="application/json",
                ),
            )
            txt = resp.text
            if "```" in txt:
                txt = re.sub(r"^.*?```(?:json)?\n", "", txt, flags=re.S)
                txt = txt.rsplit("```", 1)[0]
            return json.loads(txt)
        except Exception as e:  # noqa: BLE001
            last = e
            print(f"    {model} failed: {str(e)[:200]}")
    sys.exit(f"all gemini models failed: {last}")


# ------------------------------------------------------------------ retiming

def retime(beats, target):
    """Scale reference beat windows to the runtime we actually intend to generate.

    The article's warning is real: if the timeline is written for one length and
    generated at another, the model compresses and the delivery desyncs. So we
    rescale explicitly and round to whole seconds that still sum to the target.
    """
    src_total = beats[-1]["end"] - beats[0]["start"]
    scale = target / src_total
    raw = [(b["end"] - b["start"]) * scale for b in beats]

    secs = [max(1, int(round(x))) for x in raw]
    # fix rounding drift so the sum is exactly the target
    while sum(secs) != target:
        if sum(secs) < target:
            secs[max(range(len(secs)), key=lambda i: raw[i] - secs[i])] += 1
        else:
            cand = [i for i in range(len(secs)) if secs[i] > 1]
            secs[max(cand, key=lambda i: secs[i] - raw[i])] -= 1

    t = 0
    out = []
    for b, d in zip(beats, secs):
        nb = dict(b)
        nb["new_start"], nb["new_end"], nb["new_dur"] = t, t + d, d
        nb["word_budget"] = int(d * WPS_TARGET)
        t += d
        out.append(nb)
    return out


def mmss(s):
    return f"{int(s)//60:02d}:{int(s)%60:02d}"


# ----------------------------------------------------------------- scaffold

def scaffold(ref, target, profile, brand):
    beats = retime(ref["beats"], target)
    real_cuts = sum(1 for b in beats[1:] if b.get("cut_type") in
                    {"hard cut", "jump cut", "match cut"})

    b = brand or {}
    def slot(key, fallback):
        return b.get(key) or fallback

    L = []
    L.append(f"FORMAT: One continuous {target}-second vertical 9:16 video, real-time pacing")
    L.append(f"throughout. Contains exactly {real_cuts} cuts, at the timestamps marked in the")
    L.append("timeline below. No other cuts.")
    L.append("")
    L.append("CAST: " + slot("cast", "<<TODO: pointer to @Image1 + only what the ref cannot carry>>"))
    L.append("")
    L.append("WARDROBE (identical in every beat unless a PHASE OVERRIDE says otherwise): "
             + slot("wardrobe", "<<TODO: garment, colour, fit, jewellery>>"))
    L.append("")
    L.append("SET: " + slot("set", "<<TODO: our room. State what is NOT in it.>>"))
    L.append("")
    L.append("PRODUCT: " + slot("product", "<<TODO: @Image2 pointer + product skill mechanism block VERBATIM>>"))
    L.append("")
    L.append("LOOK: " + slot("look", ref.get("look", "")).strip())
    L.append("")
    L.append("VOICE: " + slot("voice", "<<TODO: our avatar's register>>"))
    L.append("")
    L.append("SOUND: " + slot("sound", ref.get("sound", "Ambient room tone only. No music.")).strip())
    L.append("")
    L.append("TIMELINE")
    L.append("")

    for i, bt in enumerate(beats):
        n = i + 1
        if i == 0:
            head = "SHOT 1. OPEN."
        else:
            head = CUT_HEADERS.get(bt.get("cut_type", "hard cut"),
                                   "SHOT {n}. HARD CUT.").format(n=n)
        L.append(f"[{mmss(bt['new_start'])}–{mmss(bt['new_end'])}]  {head}")
        L.append(f"  FRAME: {bt.get('frame','').strip()}")
        L.append(f"  ACTION: {bt.get('action','').strip()}")
        if bt.get("dialogue", "").strip():
            L.append(f"  DIALOGUE: <<TODO {bt['word_budget']} words max, role={bt.get('role','')}>>")
            L.append(f"  # reference said: \"{bt['dialogue'].strip()}\"")
        else:
            L.append("  DIALOGUE: (none, natural breath)")
        if bt.get("on_screen_text", "").strip():
            L.append(f"  # reference had burned-in text here: \"{bt['on_screen_text'].strip()}\""
                     " -> burn ours in post, not in the generation")
        L.append("")

    L.append("CONTINUITY: " + slot("continuity",
        "The same person in every beat. Identical face, hair colour, hair length, skin tone "
        "and eye colour from the first frame to the last. Same wardrobe and same jewellery in "
        "every beat except where a PHASE OVERRIDE states otherwise. Same room, same light "
        "direction, same time of day. One voice throughout, one person in one recording "
        "session, no shift in pitch or accent at any cut."))
    L.append("")
    L.append("TEXT: No on-screen text, no captions, no subtitles, no watermarks, no rendered logos.")
    L.append("")
    L.append("NEGATIVES: no slow motion, no speed ramps, no cinematic color grading, no 3D render "
             "or CGI look, no plastic skin, no extra fingers, no warped hands, no morphing between "
             "cuts, no extra people entering frame, no invented props or furniture.")
    return "\n".join(L), beats, real_cuts


# --------------------------------------------------------------------- main

def cmd_analyze(a):
    out = Path(a.out)
    video = acquire(a.source, out)
    dur = probe_duration(video)
    cuts, th = auto_cuts(video, dur, a.threshold)
    windows = build_windows(cuts, dur, a.min_beat)
    print(f"  {dur}s, {len(cuts)} cuts detected (threshold {th}), {len(windows)} beats")
    if not cuts:
        print("  NOTE: no cuts found. Reference is a single continuous take.")

    ref = gemini_analyze(video, windows, dur)
    ref["_detected"] = {"duration": dur, "cuts": cuts, "threshold": th,
                        "windows": windows, "source": a.source}
    # trust ffmpeg over the model for timing
    for i, bt in enumerate(ref.get("beats", [])):
        if i < len(windows):
            bt["start"], bt["end"] = windows[i]
    p = out / "reference.json"
    p.write_text(json.dumps(ref, indent=2))
    print(f"  wrote {p}")
    wps = ref.get("words_per_second")
    if wps:
        print(f"  reference pacing: {wps} w/s (we generate at {WPS_TARGET})")
    return 0


def cmd_scaffold(a):
    ref = json.loads(Path(a.reference).read_text())
    target = a.target or int(round(ref["_detected"]["duration"]))
    target = max(ENGINE_MIN_SECONDS, min(ENGINE_MAX_SECONDS, target))
    brand = json.loads(Path(a.brand).read_text()) if a.brand else None

    text, beats, cuts = scaffold(ref, target, a.profile, brand)
    outp = Path(a.out) if a.out else Path(a.reference).with_name("prompt.txt")
    outp.write_text(text)

    src = ref["_detected"]["duration"]
    print(f"  reference {src}s -> generating {target}s (scale {target/src:.2f}x)")
    print(f"  {len(beats)} beats, {cuts} cuts, one cut per {target/max(cuts,1):.1f}s")
    print(f"  wrote {outp}")
    todo = text.count("<<TODO")
    if todo:
        print(f"  {todo} TODO slots to fill before this is fireable")
    print(f"  then: python3 seedance_prompt_lint.py {outp} --duration {target}"
          + (f" --profile {a.profile}" if a.profile else ""))
    return 0


def main():
    sys.stdout.reconfigure(line_buffering=True)  # progress is useless if it buffers
    load_env()
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    an = sub.add_parser("analyze", help="reference video -> reference.json")
    an.add_argument("source", help="URL or local path")
    an.add_argument("--out", required=True, help="output directory")
    an.add_argument("--threshold", type=float, help="force ffmpeg scene threshold")
    an.add_argument("--min-beat", type=float, default=MIN_BEAT_SECONDS,
                    dest="min_beat", help="merge beats shorter than this")
    an.set_defaults(fn=cmd_analyze)

    sc = sub.add_parser("scaffold", help="reference.json -> prompt scaffold")
    sc.add_argument("reference")
    sc.add_argument("--target", type=int, help=f"runtime to generate, {ENGINE_MIN_SECONDS}-{ENGINE_MAX_SECONDS}")
    sc.add_argument("--profile", help="P1..P8")
    sc.add_argument("--brand", help="JSON with cast/wardrobe/set/product/voice/look overrides")
    sc.add_argument("--out")
    sc.set_defaults(fn=cmd_scaffold)

    a = ap.parse_args()
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
