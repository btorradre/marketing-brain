#!/usr/bin/env python3
"""Universal scene-aware ad replication runner — kie.ai backend.

ANY reference ad in -> per-scene stills -> per-scene clips -> assembled video.
Format-agnostic: POV, UGC, talking-head, product demo, claymation, cinematic.
Brand-agnostic. Engine-selectable (Seedance 2.0 / Kling 3.0).

THE ARCHITECTURE (why this exists):
  A reference ad is almost never one continuous shot. A 9s TikTok routinely
  carries 6-9 cuts. Pipelines that generate ONE keyframe and animate it produce
  a single drifting clip that does not match the reference.

  This runner is KEYFRAME-FIRST and BATCH-AUTHORED:
    scan   -> detect the reference's real cut boundaries, cut a frame + clip
              per scene, write scenes.json
    image  -> generate ONE still PER SCENE, each i2i from THAT scene's own
              reference frame + the SAME shared reference images
    animate-> animate each still INDEPENDENTLY
    finish -> trim each clip to its scene's target length, concat, mux

  NO CHAINING. No clip is ever seeded from another clip's last frame. Chaining
  makes every generation inherit the previous one's errors, which is how a
  bag's belts multiplied into a lattice over successive segments. Independent
  stills conditioned on shared references cannot compound.

  Two wins fall out: every still is auditable BEFORE any video credit is spent,
  and each generated clip is ONE CONTINUOUS SHOT with the cuts living in the
  edit (which is why the ugc footers say "no cuts").

  Continuity becomes the prompt-writer's job: wardrobe, setting, lighting and
  time of day must be restated in EVERY scene's prompt, since nothing is
  inherited. That is the trade for zero compounding drift.

Subcommands (all resumable — delete an output file to regenerate it):
  fetch    <url-or-path> <out_dir>   yt-dlp download (or copy/curl), metadata
                                     -> reference.mp4, music.json, first_frame,
                                     original_audio.m4a
  scan     <out_dir>                 ffmpeg scene-change detection -> per-scene
                                     reference frame + clip + scenes.json
  image    <job.json>                GPT Image 2 i2i, one still PER SCENE
  animate  <job.json>                Seedance/Kling i2v per scene, independent
  finish   <job.json>                trim -> concat -> overlay -> mux

Job shape (job.json):
{
  "concept_id": "VEL-XXX-01",
  "output_dir": "/abs/path",
  "reference_video": "/abs/reference.mp4",
  "shared_references": ["/abs/product.png", "/abs/creator.png"],
        # uploaded ONCE, appended to every scene's image refs. This is what
        # holds identity across scenes in place of chaining.
  "aspect_ratio": "9:16",
  "resolution": "720p",
  "image_aspect_ratio": "2:3",   # kie GPT Image 2 has no 9:16 — we crop after
  "image_resolution": "2K",      # drop to "1K" for long prompts (see NOTES)
  "engine": "seedance",          # default engine: "seedance" | "kling"
  "footer_preset": "none",       # "none"|"clean"|"ugc"|"ugc_text" or set "footer"
  "footer": null,                # explicit footer string, overrides the preset
  "max_seconds": null,           # cap on TOTAL assembled duration (null = none)
  "upload_path": "scene-replicator",
  "overlay_text": null,          # optional global text burned in at finish
  "scenes": [
    {
      "index": 1,
      "reference_frame": "/abs/scenes/001/reference.jpg",  # from scan
      "reference_clip":  "/abs/scenes/001/reference.mp4",  # from scan
      "target_seconds": 2.4,     # what it occupies in the FINAL edit
      "gen_seconds": 4,          # what we ask the engine for (floor 4)
      "image_prompt": "<THIS scene's composition + our subject + style block>",
      "motion_prompt": "<camera verbs for THIS scene only>",
      "mode": "first_frame",     # "first_frame" | "motion_transfer" | "reference"
      "engine": null,            # per-scene override
      "generate_audio": true,
      "extra_references": [],    # scene-only refs on top of shared_references
      "bake_text": null          # text that MUST appear verbatim in image_prompt
    }
  ]
}

NOTES (hard-won, do not relearn):
  - kie GPT Image 2 hard-fails (400, at EXECUTION not createTask) on a ~5k-char
    prompt combined with 2K resolution. Same prompt at 1K passes. Long
    multi-subject prompts: set "image_resolution": "1K".
  - Seedance pre-authorizes ~130cr/sec (~3x the ~41cr/sec actual) and holds it
    PER TASK, so the balance wall is the LARGEST single scene, not the sum.
  - seedance-2-fast is BANNED (distortion). std only.
  - Kling's recordInfo under-reports credits badly; meter with /chat/credit.
  - This machine's TLS resets against kie's result CDN — downloads relay
    through the VPS automatically.
"""
import argparse
import json
import math
import os
import re
import shutil
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.request

try:  # macOS python.org builds lack system CAs — use certifi
    import certifi
    SSL_CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CTX = ssl.create_default_context()

VAULT = "/Users/brooksorradre2/Documents/marketing brain"
ENV_PATH = os.path.join(VAULT, ".env")
KIE_API = "https://api.kie.ai/api/v1"
KIE_UPLOAD = "https://kieai.redpandaai.co/api/file-stream-upload"
KIE_IMG_MODEL = "gpt-image-2-image-to-image"
VPS_RELAY = "root@187.124.249.12"

ENGINES = {
    # seedance-2-fast is BANNED (distortion). std only.
    "seedance": "bytedance/seedance-2",
    "kling": "kling-3.0/video",
}

MIN_GEN_SECONDS = 4    # kie floor — 3s is rejected outright
MAX_GEN_SECONDS = 15   # kie ceiling

SCENE_THRESHOLD = 0.25   # tuned for TikTok's soft cuts (0.3 misses them)
MIN_SCENE_GAP = 0.35     # drop flash frames / flicker
MAX_SCENES = 40

# Footers are OPT-IN. This runner takes ANY ad, so imposing an iPhone/UGC
# aesthetic by default would be wrong for cinematic, animated or studio formats.
FOOTERS = {
    "none": "",
    "clean": "No cuts. No transitions. ONE CONTINUOUS SHOT.",
    "ugc": ("Ambient sound only, no speech, no voiceover. No cuts. No zooms. "
            "No transitions. Raw handheld iPhone footage, subtle natural hand "
            "shake, UGC aesthetic. No on-screen text of any kind. "
            "ONE CONTINUOUS SHOT"),
    "ugc_text": ("Ambient sound only, no speech, no voiceover. No cuts. No "
                 "zooms. No transitions. Raw handheld iPhone footage, subtle "
                 "natural hand shake, UGC aesthetic. The on-screen text caption "
                 "stays pixel-perfect fixed, sharp, legible and unchanged for "
                 "the entire clip. ONE CONTINUOUS SHOT"),
}


def env_key(name="KIE_API_KEY"):
    key = os.environ.get(name)
    if not key and os.path.exists(ENV_PATH):
        for line in open(ENV_PATH):
            if line.strip().startswith(name + "="):
                key = line.strip().split("=", 1)[1]
                break
    if not key:
        sys.exit(f"{name} not found (env or {ENV_PATH})")
    return key


# ---------- kie.ai plumbing (proven: omni-ugc -> pov-trend-factory -> here) ----------

def kie_api(method, url, key, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {key}")
    if data:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=120, context=SSL_CTX) as r:
        # strict=False: kie echoes prompts back with raw control chars
        return json.loads(r.read().decode("utf-8", "replace"), strict=False)


def kie_upload(path, key, upload_path):
    # kie's R2 storage throws transient 500s — retry with backoff
    last = ""
    for attempt in range(4):
        if attempt:
            wait = 30 * attempt
            print(f"  upload retry {attempt + 1}/4 for "
                  f"{os.path.basename(path)} in {wait}s ({last[:120]})")
            time.sleep(wait)
        out = subprocess.run(
            ["curl", "-s", "-X", "POST", KIE_UPLOAD,
             "-H", f"Authorization: Bearer {key}",
             "-F", f"file=@{path}",
             "-F", f"uploadPath={upload_path}",
             "-F", f"fileName={int(time.time())}-"
                   f"{os.path.basename(path).replace(' ', '_')}"],
            capture_output=True, text=True)
        try:
            resp = json.loads(out.stdout)
        except ValueError:
            last = out.stdout or out.stderr
            continue
        if resp.get("data", {}).get("downloadUrl"):
            return resp["data"]["downloadUrl"]
        last = out.stdout
    sys.exit(f"upload failed for {path} after 4 attempts: {last[:300]}")


def upload_cached(path, key, st):
    # kie temp URLs expire (~24h) — the cache only spans a run, not days.
    path = os.path.abspath(path)
    if path not in st["cache"]:
        st["cache"][path] = kie_upload(path, key, st["upload_path"])
        save_state(st)
        print(f"  uploaded {os.path.basename(path)}")
    return st["cache"][path]


def kie_download(url, dest):
    try:
        subprocess.run(["curl", "-sL", "-o", dest, url], check=True,
                       capture_output=True, timeout=60)
        if os.path.getsize(dest) > 0:
            return dest
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError):
        pass
    remote = f"/tmp/kie_dl_{os.getpid()}_{abs(hash(url)) % 100000}"
    subprocess.run(["ssh", "-o", "ConnectTimeout=10", VPS_RELAY,
                    f"curl -sL -o '{remote}' --max-time 90 '{url}'"], check=True)
    subprocess.run(["scp", "-q", f"{VPS_RELAY}:{remote}", dest], check=True)
    subprocess.run(["ssh", VPS_RELAY, f"rm -f '{remote}'"], check=False)
    return dest


def kie_create_task(key, model, inp):
    resp = kie_api("POST", f"{KIE_API}/jobs/createTask", key,
                   {"model": model, "input": inp})
    if resp.get("code") != 200:
        sys.exit(f"createTask failed: {resp}")
    return resp["data"]["taskId"]


def kie_poll(key, task_id, label, interval=12):
    while True:
        resp = kie_api("GET", f"{KIE_API}/jobs/recordInfo?taskId={task_id}", key)
        d = resp.get("data", {})
        state = d.get("state")
        if state == "success":
            result = json.loads(d.get("resultJson") or "{}", strict=False)
            print(f"  {label}: success ({d.get('creditsConsumed')} credits, "
                  f"{round((d.get('costTime') or 0) / 1000)}s)")
            return result
        if state == "fail":
            print(f"  {label} FAILED: {d.get('failCode')} {d.get('failMsg')} "
                  f"(failed tasks are not charged)")
            return None
        time.sleep(interval)


def kie_balance(key):
    try:
        return kie_api("GET", f"{KIE_API}/chat/credit", key).get("data")
    except (urllib.error.URLError, OSError, ValueError):
        return None


def run_task(st, key, task_key, model, inp, dest, label, interval=12,
             fatal=True):
    """createTask with resume: an in-flight taskId is polled instead of
    re-created (and re-charged). fatal=False returns None instead of exiting,
    so one bad scene does not throw away the whole batch."""
    task_id = st["tasks"].get(task_key)
    if task_id:
        print(f"  resuming task {task_id}")
    else:
        task_id = kie_create_task(key, model, inp)
        st["tasks"][task_key] = task_id
        save_state(st)
    result = kie_poll(key, task_id, label, interval)
    if result is None:
        st["tasks"].pop(task_key, None)
        save_state(st)
        if fatal:
            sys.exit(f"{label}: task failed — re-run to retry with a fresh task")
        return None
    url = (result.get("resultUrls") or [None])[0]
    if not url:
        st["tasks"].pop(task_key, None)
        save_state(st)
        if fatal:
            sys.exit(f"{label}: no resultUrls in {result}")
        return None
    kie_download(url, dest)
    st["tasks"].pop(task_key, None)
    save_state(st)
    return dest


# ---------- state / job ----------

def load_state(out_dir, upload_path="scene-replicator"):
    st = {"cache_file": os.path.join(out_dir, "kie_upload_cache.json"),
          "tasks_file": os.path.join(out_dir, "kie_tasks.json"),
          "upload_path": upload_path}
    st["cache"] = (json.load(open(st["cache_file"]))
                   if os.path.exists(st["cache_file"]) else {})
    st["tasks"] = (json.load(open(st["tasks_file"]))
                   if os.path.exists(st["tasks_file"]) else {})
    return st


def save_state(st):
    json.dump(st["cache"], open(st["cache_file"], "w"), indent=1)
    json.dump(st["tasks"], open(st["tasks_file"], "w"), indent=1)


def scene_dir(job, idx):
    d = os.path.join(job["output_dir"], "scenes", f"{idx:03d}")
    os.makedirs(d, exist_ok=True)
    return d


def footer_for(job):
    if job.get("footer") is not None:
        return job["footer"]
    preset = job.get("footer_preset", "none")
    if preset not in FOOTERS:
        sys.exit(f"unknown footer_preset {preset!r} "
                 f"(choose from {sorted(FOOTERS)} or set \"footer\")")
    return FOOTERS[preset]


def load_job(path):
    job = json.loads(open(path).read())
    for req in ("output_dir", "scenes"):
        if not job.get(req):
            sys.exit(f"job.json is missing required key {req!r}")
    os.makedirs(job["output_dir"], exist_ok=True)

    eng = job.get("engine", "seedance")
    if eng not in ENGINES:
        sys.exit(f"unknown engine {eng!r} (choose from {sorted(ENGINES)})")

    cap = job.get("max_seconds")
    total = 0.0
    for i, s in enumerate(job["scenes"], start=1):
        s.setdefault("index", i)
        s["target_seconds"] = float(s.get("target_seconds")
                                    or s.get("gen_seconds") or MIN_GEN_SECONDS)
        # Generate with headroom: the engine rejects <4s, and a clip trimmed
        # down reads cleaner than one generated at exactly the cut length.
        gen = int(s.get("gen_seconds") or math.ceil(s["target_seconds"]))
        s["gen_seconds"] = max(MIN_GEN_SECONDS, min(MAX_GEN_SECONDS, gen))
        if s["target_seconds"] > s["gen_seconds"]:
            sys.exit(f"scene {s['index']}: target_seconds "
                     f"({s['target_seconds']}) exceeds gen_seconds "
                     f"({s['gen_seconds']}) — cannot trim up")
        for req in ("image_prompt", "motion_prompt"):
            if not s.get(req):
                sys.exit(f"scene {s['index']}: {req} is required")
        s.setdefault("mode", "first_frame")
        if s["mode"] not in ("first_frame", "motion_transfer", "reference"):
            sys.exit(f"scene {s['index']}: mode must be first_frame, "
                     f"motion_transfer or reference")
        se = s.get("engine") or eng
        if se not in ENGINES:
            sys.exit(f"scene {s['index']}: unknown engine {se!r}")
        # A baked-text scene must actually carry the text in its prompt.
        bake = (s.get("bake_text") or "").strip()
        if bake and bake not in s["image_prompt"]:
            sys.exit(f"scene {s['index']}: bake_text is set but image_prompt "
                     f"does not contain it verbatim")
        total += s["target_seconds"]

    if cap and total > float(cap) + 0.05:
        sys.exit(f"assembled duration {total:.1f}s breaks the {cap}s cap — "
                 f"trim target_seconds, drop a scene, or raise max_seconds")
    job["_total_seconds"] = total
    return job


# ---------- ffmpeg helpers ----------

def probe_duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", path], capture_output=True, text=True)
    try:
        return float(out.stdout.strip())
    except ValueError:
        return None


def crop_916(src, dest):
    """Center-crop a wider-than-9:16 still to exact 9:16."""
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src,
                    "-vf", "crop='min(iw,floor(ih*9/16/2)*2)':ih",
                    "-frames:v", "1", "-update", "1", dest], check=True)
    return dest


# ---------- fetch ----------

def cmd_fetch(args):
    out_dir = os.path.abspath(args.out_dir)
    os.makedirs(out_dir, exist_ok=True)
    ref = os.path.join(out_dir, "reference.mp4")
    info = {}
    if not os.path.exists(ref):
        if os.path.exists(args.url):
            shutil.copy(args.url, ref)
        else:
            got = subprocess.run(
                ["yt-dlp", "--no-playlist", "--write-info-json",
                 "--merge-output-format", "mp4",
                 "-o", os.path.join(out_dir, "reference.%(ext)s"), args.url],
                capture_output=True, text=True)
            if got.returncode != 0 or not os.path.exists(ref):
                subprocess.run(["curl", "-sL", "-o", ref, args.url], check=True)
                if not os.path.exists(ref) or os.path.getsize(ref) < 10000:
                    sys.exit(f"could not fetch video: {got.stderr[-400:]}")
    info_path = os.path.join(out_dir, "reference.info.json")
    if os.path.exists(info_path):
        info = json.load(open(info_path))
    music = {"track": info.get("track"), "artist": info.get("artist"),
             "title": info.get("title"), "uploader": info.get("uploader"),
             "source_url": args.url}
    json.dump(music, open(os.path.join(out_dir, "music.json"), "w"), indent=1)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", ref, "-frames:v", "1",
                    "-q:v", "2", os.path.join(out_dir, "first_frame.jpg")],
                   check=True)
    audio = os.path.join(out_dir, "original_audio.m4a")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", ref, "-vn",
                    "-c:a", "aac", "-b:a", "192k", audio], check=False)
    print(json.dumps({
        "reference": ref,
        "first_frame": os.path.join(out_dir, "first_frame.jpg"),
        "original_audio": audio if os.path.exists(audio) else None,
        "duration_seconds": probe_duration(ref),
        "music": music,
        "next": "run `scan` to detect the reference's cut boundaries"},
        indent=2))


# ---------- scan ----------

def detect_cuts(video, threshold):
    out = subprocess.run(
        ["ffmpeg", "-i", video, "-filter:v",
         f"select='gt(scene,{threshold})',showinfo", "-vsync", "vfr",
         "-f", "null", "-"], capture_output=True, text=True)
    return sorted(set(float(m) for m in
                      re.findall(r"pts_time:([0-9.]+)", out.stderr)))


def cmd_scan(args):
    out_dir = os.path.abspath(args.out_dir)
    ref = args.video or os.path.join(out_dir, "reference.mp4")
    if not os.path.exists(ref):
        sys.exit(f"{ref} missing — run `fetch` first or pass --video")
    duration = probe_duration(ref) or 0.0
    if duration <= 0:
        sys.exit("could not probe reference duration")

    cuts = detect_cuts(ref, args.threshold)
    bounds = [0.0] + [t for t in cuts if 0.0 < t < duration] + [duration]

    merged = [bounds[0]]
    for t in bounds[1:]:
        if t - merged[-1] >= args.min_gap:
            merged.append(t)
    if merged[-1] < duration - 1e-3:
        merged[-1] = duration

    # No detectable hard cuts (one long take, or a cross-dissolve edit): slice
    # on a fixed interval so the shot is still authored as distinct beats.
    if len(merged) <= 2 and duration > args.interval * 1.5:
        n = max(2, int(round(duration / args.interval)))
        merged = [duration * i / n for i in range(n + 1)]
        print(f"no hard cuts detected — falling back to {n} x "
              f"~{duration / n:.1f}s interval beats")

    # Subdivide over-long spans. Two things produce one: a MISSED cut (the
    # scene filter under-scores low-contrast transitions and dissolves), and a
    # genuinely long take. Both want splitting — one long clip is exactly
    # where a generated shot drifts.
    if args.max_scene > 0:
        split = [merged[0]]
        for i in range(len(merged) - 1):
            start, end = merged[i], merged[i + 1]
            span = end - start
            if span > args.max_scene:
                n = int(math.ceil(span / args.max_scene))
                print(f"  span {start:.2f}-{end:.2f}s ({span:.2f}s) exceeds "
                      f"--max-scene {args.max_scene}s — splitting into {n} beats")
                for k in range(1, n):
                    split.append(start + span * k / n)
            split.append(end)
        merged = split

    scenes, root = [], os.path.join(out_dir, "scenes")
    os.makedirs(root, exist_ok=True)
    for i in range(len(merged) - 1):
        if len(scenes) >= MAX_SCENES:
            print(f"capped at {MAX_SCENES} scenes — remaining cuts ignored")
            break
        start, end = merged[i], merged[i + 1]
        dur = end - start
        idx = len(scenes) + 1
        d = os.path.join(root, f"{idx:03d}")
        os.makedirs(d, exist_ok=True)
        frame = os.path.join(d, "reference.jpg")
        clip = os.path.join(d, "reference.mp4")
        # Sample just inside the cut — the boundary frame is often a blend.
        at = start + min(0.25, dur * 0.25)
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(at),
                        "-i", ref, "-frames:v", "1", "-q:v", "2", frame],
                       check=True)
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(start),
                        "-i", ref, "-t", str(round(dur, 3)),
                        "-c:v", "libx264", "-crf", "20", "-an", clip],
                       check=False)
        scenes.append({
            "index": idx, "start": round(start, 3), "end": round(end, 3),
            "duration": round(dur, 3), "reference_frame": frame,
            "reference_clip": clip if os.path.exists(clip) else None,
            "target_seconds": round(dur, 2),
            "gen_seconds": max(MIN_GEN_SECONDS, math.ceil(dur)),
        })

    path = os.path.join(out_dir, "scenes.json")
    json.dump({"reference": ref, "duration_seconds": round(duration, 3),
               "threshold": args.threshold, "scene_count": len(scenes),
               "scenes": scenes}, open(path, "w"), indent=1)

    print(f"\n{len(scenes)} scenes over {duration:.1f}s -> {path}")
    print(f"{'#':>3}  {'in':>6} {'out':>6} {'dur':>5}   reference frame")
    for s in scenes:
        print(f"{s['index']:>3}  {s['start']:>6.2f} {s['end']:>6.2f} "
              f"{s['duration']:>5.2f}   "
              f"{os.path.relpath(s['reference_frame'], out_dir)}")
    print("\nNext: VIEW every reference frame, then author one image_prompt + "
          "motion_prompt per scene into job.json.")


# ---------- image: one still PER SCENE ----------

def cmd_image(args):
    job = load_job(args.job)
    key = env_key()
    st = load_state(job["output_dir"],
                    job.get("upload_path", "scene-replicator"))

    for s in job["scenes"]:
        if not s.get("reference_frame") or not os.path.exists(s["reference_frame"]):
            sys.exit(f"scene {s['index']}: reference_frame missing "
                     f"({s.get('reference_frame')}) — run `scan` first")

    # Shared refs are uploaded ONCE and appended to every scene. This is what
    # holds identity across scenes in place of chaining.
    shared = [upload_cached(p, key, st)
              for p in job.get("shared_references", [])]

    made = skipped = 0
    for s in job["scenes"]:
        d = scene_dir(job, s["index"])
        keyframe = os.path.join(d, "keyframe.png")
        if os.path.exists(keyframe):
            print(f"scene {s['index']}: keyframe exists, skipping")
            skipped += 1
        else:
            urls = ([upload_cached(s["reference_frame"], key, st)] + shared +
                    [upload_cached(p, key, st)
                     for p in s.get("extra_references", [])])
            print(f"scene {s['index']}: generating keyframe "
                  f"({len(urls)} refs)…")
            got = run_task(st, key, f"image-{s['index']:03d}", KIE_IMG_MODEL,
                           {"prompt": s["image_prompt"], "input_urls": urls,
                            "aspect_ratio": job.get("image_aspect_ratio", "2:3"),
                            "resolution": job.get("image_resolution", "2K")},
                           keyframe, f"scene {s['index']} keyframe", fatal=False)
            if not got:
                print(f"scene {s['index']}: FAILED — re-run `image` to retry "
                      f"just this scene")
                continue
            made += 1
        crop_916(keyframe, os.path.join(d, "animate-source.png"))

    print(f"\nkeyframes: {made} generated, {skipped} reused")
    print("QA GATE — view EVERY scenes/NNN/keyframe.png before `animate`. "
          "Batch-authoring makes every still auditable for free; a bad still "
          "animated is a wasted video credit. Check product fidelity, "
          "continuity across scenes (wardrobe/setting/light), any baked text "
          "character by character, and that nothing reads as a 3D render.")


# ---------- animate: per scene, INDEPENDENT ----------

def build_video_input(job, s, st, key, footer):
    """Engine-specific payload. Seedance and Kling take different shapes."""
    engine = s.get("engine") or job.get("engine", "seedance")
    d = scene_dir(job, s["index"])
    source = os.path.join(d, "animate-source.png")
    prompt = s["motion_prompt"]
    if footer:
        prompt = f"{prompt}\n\n{footer}"

    if engine == "kling":
        inp = {"prompt": prompt,
               "image_urls": [upload_cached(source, key, st)],
               "duration": str(s["gen_seconds"]),
               "mode": job.get("kling_mode", "std"),
               "sound": bool(s.get("generate_audio", True)),
               # kie schema change (2026-08): required boolean; True splits the
               # clip into Kling-authored sub-shots, we always want ONE shot
               "multi_shots": False}
        return engine, inp

    # seedance
    inp = {"aspect_ratio": job.get("aspect_ratio", "9:16"),
           "resolution": job.get("resolution", "720p"),
           "duration": s["gen_seconds"],
           "generate_audio": bool(s.get("generate_audio", True))}
    mode = s.get("mode", "first_frame")
    if mode == "motion_transfer" and s.get("reference_clip"):
        # Multimodal reference mode. Stronger motion copy, but it can drift
        # baked text. Mutually exclusive with first_frame_url per kie docs.
        inp["prompt"] = ("@Image1 is the exact opening frame and look of the "
                         "shot. Replicate the camera motion, pacing and energy "
                         f"of @Video1 precisely.\n\n{prompt}")
        inp["reference_image_urls"] = [upload_cached(source, key, st)]
        inp["reference_video_urls"] = [upload_cached(s["reference_clip"],
                                                     key, st)]
    elif mode == "reference":
        # Pure multi-reference mode: the still plus shared refs as @ImageN.
        # first_frame_url is NOT allowed alongside these.
        refs = [upload_cached(source, key, st)]
        refs += [upload_cached(p, key, st)
                 for p in job.get("shared_references", [])][:8]
        inp["prompt"] = prompt
        inp["reference_image_urls"] = refs
    else:
        inp["prompt"] = prompt
        inp["first_frame_url"] = upload_cached(source, key, st)
    return engine, inp


def cmd_animate(args):
    job = load_job(args.job)
    key = env_key()
    st = load_state(job["output_dir"],
                    job.get("upload_path", "scene-replicator"))
    footer = footer_for(job)

    pending = []
    for s in job["scenes"]:
        d = scene_dir(job, s["index"])
        if os.path.exists(os.path.join(d, "raw-clip.mp4")):
            continue
        if not os.path.exists(os.path.join(d, "animate-source.png")):
            sys.exit(f"scene {s['index']}: animate-source.png missing — "
                     f"run `image` first")
        pending.append(s)

    if not pending:
        print("all scene clips exist (delete a scenes/NNN/raw-clip.mp4 to "
              "regenerate it)")
        return

    gen_total = sum(s["gen_seconds"] for s in pending)
    biggest = max(s["gen_seconds"] for s in pending)
    bal = kie_balance(key)
    if isinstance(bal, (int, float)):
        # The pre-auth hold is PER TASK, so the wall is the largest single
        # scene, not the sum.
        need = 130 * biggest
        print(f"kie balance: {bal} credits · {len(pending)} scenes / "
              f"{gen_total}s (~{41 * gen_total} actual on seedance, "
              f"~{need} pre-auth hold on the largest task)")
        if bal < need:
            sys.exit(f"balance {bal} < ~{need} pre-auth for a {biggest}s "
                     f"task — top up first")

    failed = []
    for s in pending:
        d = scene_dir(job, s["index"])
        dest = os.path.join(d, "raw-clip.mp4")
        engine, inp = build_video_input(job, s, st, key, footer)
        print(f"\nscene {s['index']}: {s['gen_seconds']}s on {engine} "
              f"({s.get('mode')} mode, trims to {s['target_seconds']}s)…")
        print("  --- prompt ---")
        print("  " + inp["prompt"].replace("\n", "\n  "))
        got = run_task(st, key, f"animate-{s['index']:03d}", ENGINES[engine],
                       inp, dest, f"scene {s['index']} clip", interval=15,
                       fatal=False)
        if not got:
            failed.append(s["index"])

    if failed:
        print(f"\nscenes FAILED: {failed} — re-run `animate` to retry only those")
        sys.exit(1)
    print(f"\nall {len(pending)} scene clips generated")


# ---------- finish ----------

def render_text_overlay(text, width, height, dest):
    from PIL import Image, ImageDraw, ImageFont
    font = None
    for path in ("/System/Library/Fonts/Helvetica.ttc",
                 "/System/Library/Fonts/HelveticaNeue.ttc",
                 "/Library/Fonts/Arial.ttf"):
        if os.path.exists(path):
            font = ImageFont.truetype(path, size=max(28, width // 11), index=1)
            break
    if font is None:
        sys.exit("no usable system font for the overlay")
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    max_w = int(width * 0.86)
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textbbox((0, 0), trial, font=font)[2] <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    stroke = max(2, font.size // 12)
    line_h = int(font.size * 1.25)
    y = int(height * 0.13)
    for line in lines:
        w = draw.textbbox((0, 0), line, font=font, stroke_width=stroke)[2]
        draw.text(((width - w) // 2, y), line, font=font,
                  fill=(255, 255, 255, 255), stroke_width=stroke,
                  stroke_fill=(0, 0, 0, 230))
        y += line_h
    img.save(dest)
    return dest


def cmd_finish(args):
    job = load_job(args.job)
    out_dir = job["output_dir"]

    trimmed = []
    for s in job["scenes"]:
        d = scene_dir(job, s["index"])
        raw = os.path.join(d, "raw-clip.mp4")
        if not os.path.exists(raw):
            sys.exit(f"scene {s['index']}: raw-clip.mp4 missing — run animate")
        cut = os.path.join(d, "trimmed.mp4")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", raw,
                        "-t", str(s["target_seconds"]),
                        "-c:v", "libx264", "-crf", "18", "-preset", "medium",
                        "-c:a", "aac", "-b:a", "192k", cut], check=True)
        trimmed.append(cut)
        print(f"scene {s['index']}: trimmed to {s['target_seconds']}s")

    # Concat via the concat FILTER, never the demuxer — the demuxer silently
    # desyncs when clips differ in encode params, which independently
    # generated scenes always do.
    assembled = os.path.join(out_dir, "assembled.mp4")
    if len(trimmed) == 1:
        shutil.copy(trimmed[0], assembled)
    else:
        cmd = ["ffmpeg", "-y", "-v", "error"]
        for t in trimmed:
            cmd += ["-i", t]
        n = len(trimmed)
        # generate_audio:false clips carry NO audio stream — concat video-only
        # unless every clip has audio (the filter demands uniform inputs)
        def _has_audio(path):
            out = subprocess.run(
                ["ffprobe", "-v", "error", "-select_streams", "a",
                 "-show_entries", "stream=index", "-of", "csv=p=0", path],
                capture_output=True, text=True)
            return bool(out.stdout.strip())
        if all(_has_audio(t) for t in trimmed):
            streams = "".join(f"[{i}:v][{i}:a]" for i in range(n))
            cmd += ["-filter_complex", f"{streams}concat=n={n}:v=1:a=1[v][a]",
                    "-map", "[v]", "-map", "[a]",
                    "-c:v", "libx264", "-crf", "18", "-preset", "medium",
                    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
                    assembled]
        else:
            streams = "".join(f"[{i}:v]" for i in range(n))
            cmd += ["-filter_complex", f"{streams}concat=n={n}:v=1:a=0[v]",
                    "-map", "[v]",
                    "-c:v", "libx264", "-crf", "18", "-preset", "medium",
                    "-movflags", "+faststart", assembled]
        subprocess.run(cmd, check=True)
    print(f"concat: {len(trimmed)} scenes -> assembled.mp4 "
          f"({probe_duration(assembled):.1f}s)")

    final = os.path.join(out_dir, "final.mp4")
    if job.get("overlay_text"):
        probe = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height", "-of", "csv=p=0",
             assembled], capture_output=True, text=True)
        w, h = (int(x) for x in probe.stdout.strip().split(","))
        overlay = render_text_overlay(job["overlay_text"], w, h,
                                      os.path.join(out_dir, "text-overlay.png"))
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", assembled,
                        "-i", overlay,
                        "-filter_complex", "[0:v][1:v]overlay=0:0",
                        "-c:v", "libx264", "-crf", "18", "-preset", "medium",
                        "-c:a", "copy", "-movflags", "+faststart", final],
                       check=True)
    else:
        shutil.copy(assembled, final)
    print(f"final -> {final} ({probe_duration(final):.1f}s)")

    ref_audio = os.path.join(out_dir, "original_audio.m4a")
    if os.path.exists(ref_audio) and job.get("mux_reference_audio", True):
        refsound = os.path.join(out_dir, "final-refsound.mp4")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", final,
                        "-i", ref_audio, "-map", "0:v", "-map", "1:a",
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                        "-shortest", "-movflags", "+faststart", refsound],
                       check=True)
        print(f"ref-sound mux -> {refsound}")
    music = os.path.join(out_dir, "music.json")
    if os.path.exists(music):
        print("reference sound: " + json.dumps(json.load(open(music))))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("fetch")
    f.add_argument("url")
    f.add_argument("out_dir")
    f.set_defaults(fn=cmd_fetch)
    sc = sub.add_parser("scan")
    sc.add_argument("out_dir")
    sc.add_argument("--video", default=None,
                    help="explicit reference path (default <out_dir>/reference.mp4)")
    sc.add_argument("--threshold", type=float, default=SCENE_THRESHOLD)
    sc.add_argument("--min-gap", type=float, default=MIN_SCENE_GAP,
                    dest="min_gap")
    sc.add_argument("--interval", type=float, default=2.0,
                    help="fallback beat length when no hard cuts are found")
    sc.add_argument("--max-scene", type=float, default=4.0, dest="max_scene",
                    help="split any scene longer than this (0 disables)")
    sc.set_defaults(fn=cmd_scan)
    for name, fn in (("image", cmd_image), ("animate", cmd_animate),
                     ("finish", cmd_finish)):
        q = sub.add_parser(name)
        q.add_argument("job")
        q.set_defaults(fn=fn)
    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
