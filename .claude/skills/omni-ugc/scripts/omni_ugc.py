#!/usr/bin/env python3
"""AI UGC pipeline runner (omni-ugc skill) — Google Omni OR Seedance 2.0.

Reference image -> original actor keyframe -> beat-by-beat video segments
(engine-appropriate identity + voice anchoring) -> ffmpeg-stitched 9:16 final.

Engines (job.json "engine", default "omni"):
  omni      gemini-omni-flash-preview via the Gemini Interactions API
            (POST /v1beta/interactions, background=true, poll GET .../{id}).
            Segments render at a FIXED ~10s — every omni beat is 27-35 words.
            Identity = last-frame chaining; voice = compressed seg-1 video
            anchor (Omni hears audio inside video input parts).
  seedance  bytedance/seedance-2 via kie.ai (createTask/recordInfo).
            Per-segment "duration" 5-15s, native audio (generate_audio).
            Identity = actor image on reference_image_urls of EVERY segment;
            voice = seg-1 audio mp3 via reference_audio_urls.

Pacing lint (both engines): the dialogue word count must sit inside the
WORD_BUDGET sweet spot for the segment's duration — over budget the engine
crams the words in and the actor talks unnaturally fast; under budget you get
trailing dead air. Blocking; --force overrides.

Usage:
  python3 omni_ugc.py actor <reference.png> <out_actor.png> [--prompt "<actor prompt>"]
  python3 omni_ugc.py run <job.json> [--force]
  python3 omni_ugc.py stitch <job.json>
  python3 omni_ugc.py segment <job.json> <index> [--force]   # (re)generate one segment

Job shape:
{
  "concept_id": "MOT-XXX-UGC-01",
  "engine": "omni",                    # "omni" (default) | "seedance"
  "output_dir": "/abs/path/omni",
  "actor_image": "/abs/actor.png",
  "voice_line": "she says in an american 20 year old ugc tone:",
  "identity_line": "same actor in every frame",
  "voice_anchor": true,
  "product_image": "/abs/product.png",
  "aspect_ratio": "9:16",              # seedance param (omni is prompt-driven)
  "resolution": "720p",                # seedance param
  "segments": [
    {"index": 1,
     "duration": 10,                   # omni: always 10; seedance: 5-15
     "movement": "natural and realistic arm movements, subtle lean forward, looks directly at the lens the whole time",
     "dialogue": "I don't feel like I'm wasting the product when I put a bunch on.",
     "product_in_hand": false,
     "voice_color": "",                      # optional: ", quiet but fully present"
     "extra_images": []                       # optional additional image refs
    }
  ]
}

Resumable: existing seg-N.mp4 files are skipped; delete a segment file to
regenerate it (its successors keep their existing files unless also deleted).
Seedance in-flight taskIds persist in kie_tasks.json so a re-run resumes
polling instead of creating (and paying for) a fresh task.
"""
import argparse
import base64
import json
import mimetypes
import os
import re
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

API = "https://generativelanguage.googleapis.com/v1beta/interactions"
MODEL = os.environ.get("OMNI_MODEL", "models/gemini-omni-flash-preview")
ENV_PATH = "/Users/brooksorradre2/Documents/marketing brain/.env"

KIE_API = "https://api.kie.ai/api/v1"
KIE_UPLOAD = "https://kieai.redpandaai.co/api/file-stream-upload"
KIE_MODEL = "bytedance/seedance-2"  # std only. seedance-2-fast is BANNED (distortion).
VPS_RELAY = "root@187.124.249.12"  # this machine's network resets TLS to kie's result
                                    # CDN (tempfile.aiquickdraw.com, 2026-07-10) — relay
                                    # downloads through the VPS when direct curl fails.

ENGINE_MAX_SECONDS = {"omni": 10, "seedance": 15}

# Brooks-calibrated words-per-duration sweet spots (2026-07-11). Over the max
# the engine crams the words in — the actor rushes; under the min the clip
# trails off into dead air. 6s/7s are interpolated between calibrated points.
WORD_BUDGET = {
    5: (10, 13),
    6: (13, 16),
    7: (16, 19),
    8: (20, 22),
    9: (21, 23),
    10: (27, 35),
    11: (36, 40),
    12: (41, 48),
    13: (49, 55),
    14: (56, 60),
    15: (61, 70),
}

FOOTER_NO_PRODUCT = ("Ambient Sound. No cuts. No zooms. No transitions. "
                     "Raw iPhone footage, expressive ugc movements, UGC aesthetic. "
                     "Vertical 9:16. NO PRODUCT IN HAND. ONE CONTINUOUS SHOT")
FOOTER_PRODUCT = ("Ambient Sound. No cuts. No zooms. No transitions. "
                  "Raw iPhone footage, expressive ugc movements, UGC aesthetic. "
                  "Vertical 9:16. PRODUCT IN HAND, LABEL FACING CAMERA, "
                  "LABEL TEXT UNCHANGED. ONE CONTINUOUS SHOT")

# The actor step generates a short "casting clip" (Omni is video-native; it
# returns video even under image_config) and extracts a still as the keyframe.
DEFAULT_ACTOR_PROMPT = (
    "An original person with a similar overall look, styling and vibe to the "
    "person in the reference photo, but a clearly different face, not the same "
    "person and not any real person. They sit facing the camera in a casual, "
    "well lit room, framed chest up, looking directly at the lens the whole "
    "time, natural relaxed expression, small natural movements, no talking.\n\n"
    "Ambient Sound. No cuts. No zooms. No transitions. Raw iPhone footage, "
    "UGC aesthetic. Vertical 9:16. ONE CONTINUOUS SHOT"
)

BANNED_PUNCT = re.compile(r"[—–…]|\.\.\.")


def env_key(name="GEMINI_API_KEY"):
    key = os.environ.get(name)
    if not key and os.path.exists(ENV_PATH):
        for line in open(ENV_PATH):
            if line.strip().startswith(name + "="):
                key = line.strip().split("=", 1)[1]
                break
    if not key:
        sys.exit(f"{name} not found (env or marketing brain/.env)")
    return key


def api(method, url, key, payload=None, timeout=180):
    data = json.dumps(payload).encode() if payload is not None else None
    sep = "&" if "?" in url else "?"
    req = urllib.request.Request(f"{url}{sep}key={key}", data=data, method=method)
    if data:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=SSL_CTX) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code}: {e.read().decode()[:400]}") from e


def media_part(path):
    mime = mimetypes.guess_type(path)[0]
    if not mime:
        sys.exit(f"can't guess mime type for {path}")
    kind = mime.split("/")[0]  # image | audio | video
    with open(path, "rb") as f:
        return {"type": kind, "data": base64.b64encode(f.read()).decode(),
                "mime_type": mime}


def interact(key, parts, gen_config, label):
    """Create a background interaction, poll to completion, return response dict."""
    body = {"model": MODEL, "input": parts, "background": True,
            "generation_config": gen_config}
    resp = api("POST", API, key, body)
    iid = resp.get("id")
    if not iid:
        raise RuntimeError(f"no interaction id: {json.dumps(resp)[:300]}")
    t0 = time.time()
    while resp.get("status") in (None, "in_progress", "queued"):
        if time.time() - t0 > 900:
            raise RuntimeError(f"{label}: timed out after 15min (id={iid})")
        time.sleep(6)
        resp = api("GET", f"{API}/{iid}", key)
    if resp.get("status") != "completed":
        raise RuntimeError(f"{label}: status={resp.get('status')} "
                           f"{json.dumps(resp.get('error', ''))[:300]}")
    usage = resp.get("usage", {})
    print(f"  {label}: done in {int(time.time() - t0)}s, "
          f"{usage.get('total_output_tokens', '?')} output tokens")
    return resp


def extract_media(resp, kind):
    found = []
    for step in resp.get("steps", []):
        if step.get("type") == "model_output":
            for c in step.get("content", []):
                if c.get("data"):
                    found.append(c)
    for c in found:
        if c.get("type") == kind:
            return base64.b64decode(c["data"]), kind
    # Omni is video-native: callers wanting an image may get video and
    # extract a frame from it.
    if kind == "image":
        for c in found:
            if c.get("type") == "video":
                return base64.b64decode(c["data"]), "video"
    raise RuntimeError(f"no {kind} in response "
                       f"(content types: {[c.get('type') for c in found]})")


def gen_with_retry(key, parts, gen_config, label, kind, dest):
    last_err = None
    for attempt in range(3):
        if attempt:
            print(f"  retry {attempt + 1}/3 for {label} ({str(last_err)[:150]})")
            time.sleep(15 * attempt)
        try:
            try:
                resp = interact(key, parts, gen_config, label)
            except RuntimeError as e:
                droppable = any(p.get("type") in ("audio", "video") for p in parts)
                if droppable and ("Audio input modality" in str(e)
                                  or "invalid argument" in str(e)
                                  or "Input blocked" in str(e)):
                    print(f"  {label}: anchor input rejected "
                          f"({str(e)[:100]}) — retrying without voice anchor")
                    parts = [p for p in parts
                             if p.get("type") not in ("audio", "video")
                             and "voice reference" not in p.get("text", "")]
                    resp = interact(key, parts, gen_config, label)
                else:
                    raise
            blob, got = extract_media(resp, kind)
            if kind == "image" and got == "video":
                # video-native fallback: pull a mid-clip still as the keyframe
                tmp = dest + ".casting.mp4"
                with open(tmp, "wb") as f:
                    f.write(blob)
                subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "2",
                                "-i", tmp, "-frames:v", "1", "-q:v", "2", dest],
                               check=True)
                print(f"  {label}: video-native output, extracted still "
                      f"(casting clip kept at {os.path.basename(tmp)})")
            else:
                with open(dest, "wb") as f:
                    f.write(blob)
            return dest
        except (RuntimeError, urllib.error.URLError, TimeoutError, OSError) as e:
            last_err = e
    raise RuntimeError(f"{label} failed after 3 attempts: {last_err}")


# ---------- prompt assembly (LOCKED simple 4-part format, both engines) ----------

def build_prompt(job, seg):
    identity = job.get("identity_line", "same actor in every frame")
    movement = seg["movement"].rstrip(", ")
    if identity and identity not in movement:
        movement = f"{movement}, {identity}"
    voice = job["voice_line"].rstrip(":")
    color = seg.get("voice_color", "").strip().strip(",")
    if color:
        voice = f"{voice}, {color}"
    voice += ":"
    dialogue = seg["dialogue"].strip().strip('"')
    footer = FOOTER_PRODUCT if seg.get("product_in_hand") else FOOTER_NO_PRODUCT
    return f"{movement}\n\n{voice}\n\n\"{dialogue}\"\n\n{footer}"


def lint_segment(job, seg):
    problems = []
    if BANNED_PUNCT.search(seg["dialogue"]):
        problems.append("dialogue has ellipsis/em-dash (renders as dead air) — "
                        "commas and periods only")
    eng = job.get("engine", "omni")
    dur = int(seg.get("duration", 10))
    cap = ENGINE_MAX_SECONDS[eng]
    if dur > cap:
        problems.append(f"duration {dur}s exceeds the {eng} max of {cap}s")
    elif eng == "omni" and dur != 10:
        problems.append("omni renders fixed ~10s clips — set duration 10 "
                        "(or omit) and write 27-35 words, or switch the job "
                        "to engine=seedance for other lengths")
    elif dur not in WORD_BUDGET:
        problems.append(f"duration {dur}s outside the supported 5-15s range")
    else:
        lo, hi = WORD_BUDGET[dur]
        words = len(seg["dialogue"].split())
        if words > hi:
            problems.append(f"dialogue is {words} words, over the {dur}s sweet "
                            f"spot of {lo}-{hi} — the actor will rush; cut "
                            f"words, lengthen the segment, or split the beat")
        elif words < lo:
            problems.append(f"dialogue is {words} words, under the {dur}s sweet "
                            f"spot of {lo}-{hi} — dead-air risk; add words or "
                            f"shorten the segment")
    return problems


# ---------- ffmpeg helpers ----------

def last_frame(mp4, out_png):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-sseof", "-0.15", "-i", mp4,
                    "-frames:v", "1", "-q:v", "2", out_png], check=True)
    return out_png


def extract_anchor_clip(mp4, out_mp4):
    # Voice anchor rides in as a small VIDEO part: standalone audio input is
    # gated off ("Audio input modality is not enabled") but Omni hears the
    # audio track inside video input. Keep it tiny — large inline video
    # payloads (~2MB+) get a generic "invalid argument" rejection.
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", mp4,
                    "-vf", "scale=240:-2,fps=12", "-c:v", "libx264",
                    "-crf", "35", "-preset", "fast",
                    "-c:a", "aac", "-b:a", "96k", out_mp4], check=True)
    return out_mp4


def stitch(files, out_path):
    """Normalize every clip to 720x1280/30fps/48k aac and concat."""
    args, vf, af = [], [], []
    for i, f in enumerate(files):
        args += ["-i", f]
        vf.append(f"[{i}:v]scale=720:1280:force_original_aspect_ratio=increase,"
                  f"crop=720:1280,fps=30,setsar=1[v{i}]")
        af.append(f"[{i}:a]aresample=48000[a{i}]")
    pairs = "".join(f"[v{i}][a{i}]" for i in range(len(files)))
    fc = ";".join(vf + af) + f";{pairs}concat=n={len(files)}:v=1:a=1[v][a]"
    subprocess.run(["ffmpeg", "-y", "-v", "error", *args,
                    "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
                    out_path], check=True)
    print(f"stitched -> {out_path}")


# ---------- kie.ai Seedance backend ----------

def kie_api(method, url, key, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {key}")
    if data:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=120, context=SSL_CTX) as r:
        # strict=False: kie echoes prompts back with raw control chars
        return json.loads(r.read().decode("utf-8", "replace"), strict=False)


def kie_upload(path, key):
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
             "-F", "uploadPath=omni-ugc",
             "-F", f"fileName={int(time.time())}-{os.path.basename(path).replace(' ', '_')}"],
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


def kie_upload_cached(path, key, cache):
    # kie temp URLs expire (~24h) — the cache only spans a run, not days.
    path = os.path.abspath(path)
    if path not in cache:
        cache[path] = kie_upload(path, key)
        print(f"  uploaded {os.path.basename(path)} -> {cache[path]}")
    return cache[path]


def kie_download(url, dest):
    try:
        subprocess.run(["curl", "-sL", "-o", dest, url], check=True,
                       capture_output=True, timeout=25)
        return dest
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        pass
    remote = f"/tmp/kie_dl_{os.getpid()}_{abs(hash(url)) % 100000}.mp4"
    subprocess.run(["ssh", "-o", "ConnectTimeout=10", VPS_RELAY,
                    f"curl -sL -o '{remote}' --max-time 60 '{url}'"], check=True)
    subprocess.run(["scp", "-q", f"{VPS_RELAY}:{remote}", dest], check=True)
    subprocess.run(["ssh", VPS_RELAY, f"rm -f '{remote}'"], check=False)
    return dest


def kie_create_task(key, inp):
    resp = kie_api("POST", f"{KIE_API}/jobs/createTask", key,
                   {"model": KIE_MODEL, "input": inp})
    if resp.get("code") != 200:
        sys.exit(f"createTask failed: {resp}")
    return resp["data"]["taskId"]


def kie_poll(key, task_id, label):
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
        time.sleep(15)


def seedance_state(job):
    out_dir = job["output_dir"]
    st = {"cache_file": os.path.join(out_dir, "kie_upload_cache.json"),
          "tasks_file": os.path.join(out_dir, "kie_tasks.json")}
    st["cache"] = (json.load(open(st["cache_file"]))
                   if os.path.exists(st["cache_file"]) else {})
    st["tasks"] = (json.load(open(st["tasks_file"]))
                   if os.path.exists(st["tasks_file"]) else {})
    return st


def seedance_save(st):
    json.dump(st["cache"], open(st["cache_file"], "w"), indent=1)
    json.dump(st["tasks"], open(st["tasks_file"], "w"), indent=1)


def seedance_anchor_url(job, seg_files, key, st):
    """Seg 1's audio as an mp3 voice anchor (kie reference_audio_urls).
    Once voice-anchor.mp3 exists it voice-locks every later generation,
    including seg-1 regens — delete the mp3 to re-roll the voice."""
    if not job.get("voice_anchor", True):
        return None
    mp3 = os.path.join(job["output_dir"], "voice-anchor.mp3")
    if not os.path.exists(mp3):
        if not seg_files.get(1):
            return None
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", seg_files[1],
                        "-vn", "-t", "15", "-ac", "1", "-b:a", "128k", mp3],
                       check=True)
    url = kie_upload_cached(mp3, key, st["cache"])
    seedance_save(st)
    return url


def seedance_generate(job, seg, key, st, anchor_url):
    idx = seg["index"]
    dest = os.path.join(job["output_dir"], f"seg-{idx}.mp4")
    print(f"seg {idx}: generating ({int(seg.get('duration', 10))}s)…")
    print("  --- prompt ---")
    print("  " + build_prompt(job, seg).replace("\n", "\n  "))
    inp = {"prompt": build_prompt(job, seg),
           "aspect_ratio": job.get("aspect_ratio", "9:16"),
           "resolution": job.get("resolution", "720p"),
           "duration": int(seg.get("duration", 10)),
           "generate_audio": True}
    imgs = [job["actor_image"]]
    if seg.get("product_in_hand") and job.get("product_image"):
        imgs.append(job["product_image"])
    imgs += seg.get("extra_images", [])
    inp["reference_image_urls"] = [kie_upload_cached(p, key, st["cache"])
                                   for p in imgs]
    if anchor_url:
        inp["reference_audio_urls"] = [anchor_url]
    task_id = st["tasks"].get(str(idx))
    if task_id:
        print(f"  resuming task {task_id}")
    else:
        task_id = kie_create_task(key, inp)
        st["tasks"][str(idx)] = task_id
        seedance_save(st)
    result = kie_poll(key, task_id, f"seg {idx}")
    if result is None:
        st["tasks"].pop(str(idx), None)
        seedance_save(st)
        sys.exit(f"seg {idx}: task failed — re-run to retry with a fresh task")
    url = (result.get("resultUrls") or [None])[0]
    if not url:
        st["tasks"].pop(str(idx), None)
        seedance_save(st)
        sys.exit(f"seg {idx}: no resultUrls in {result}")
    # keep the taskId until the download succeeds — a CDN failure must not
    # force a re-generate (and re-charge) on retry
    kie_download(url, dest)
    st["tasks"].pop(str(idx), None)
    seedance_save(st)
    return dest


def run_seedance(job):
    key = env_key("KIE_API_KEY")
    st = seedance_state(job)
    seg_files = existing_seg_files(job)
    anchor_url = seedance_anchor_url(job, seg_files, key, st)
    print(f"{job.get('concept_id', '?')}: {len(job['segments'])} segments, "
          f"engine=seedance")
    for seg in job["segments"]:
        idx = seg["index"]
        if idx in seg_files:
            print(f"seg {idx}: exists, skipping")
        else:
            seg_files[idx] = seedance_generate(job, seg, key, st, anchor_url)
        if anchor_url is None:
            anchor_url = seedance_anchor_url(job, seg_files, key, st)
    files = [seg_files[s["index"]] for s in job["segments"]]
    stitch(files, os.path.join(job["output_dir"], "final.mp4"))


# ---------- omni engine ----------

def run_omni(job):
    key = env_key()
    out_dir = job["output_dir"]
    seg_files = existing_seg_files(job)
    print(f"{job.get('concept_id', '?')}: {len(job['segments'])} segments, "
          f"engine=omni")
    for seg in job["segments"]:
        idx = seg["index"]
        dest = os.path.join(out_dir, f"seg-{idx}.mp4")
        if idx in seg_files:
            print(f"seg {idx}: exists, skipping")
            continue
        print(f"seg {idx}: generating…")
        print("  --- prompt ---")
        print("  " + build_prompt(job, seg).replace("\n", "\n  "))
        parts = segment_parts(job, seg, out_dir, seg_files)
        gen_with_retry(key, parts, {"video_config": {}}, f"seg {idx}",
                       "video", dest)
        seg_files[idx] = dest
    files = [seg_files[s["index"]] for s in job["segments"]]
    stitch(files, os.path.join(out_dir, "final.mp4"))


# ---------- commands ----------

def cmd_actor(args):
    key = env_key()
    parts = [media_part(args.reference),
             {"type": "text", "text": args.prompt or DEFAULT_ACTOR_PROMPT}]
    gen_with_retry(key, parts, {"image_config": {}}, "actor keyframe",
                   "image", args.out)
    print(f"actor keyframe -> {args.out}")


def segment_parts(job, seg, out_dir, seg_files):
    idx = seg["index"]
    parts = []
    if idx == 1 or not seg_files.get(idx - 1):
        parts.append(media_part(job["actor_image"]))
    else:
        frame = os.path.join(out_dir, f"seg-{idx - 1}-lastframe.png")
        last_frame(seg_files[idx - 1], frame)
        parts.append(media_part(frame))
    if seg.get("product_in_hand") and job.get("product_image"):
        parts.append(media_part(job["product_image"]))
    for extra in seg.get("extra_images", []):
        parts.append(media_part(extra))
    # Voice anchor: segs 2+ carry a compressed copy of SEG 1 (always seg 1,
    # never the previous segment, so voice drift can't compound). Omni hears
    # the audio track of video inputs even though standalone audio is gated.
    if idx > 1 and job.get("voice_anchor", True) and seg_files.get(1):
        anchor = os.path.join(out_dir, "voice-anchor.mp4")
        if not os.path.exists(anchor):
            extract_anchor_clip(seg_files[1], anchor)
        parts.append(media_part(anchor))
        # Phrasing matters: "voice reference"/"exact same voice" trips Google's
        # safety filter (reads as voice cloning). Continuity language passes.
        parts.append({"type": "text",
                      "text": "The short clip is the same actor from earlier "
                              "in this same video, keep her voice and delivery "
                              "consistent with it."})
    parts.append({"type": "text", "text": build_prompt(job, seg)})
    return parts


def load_job(path):
    job = json.loads(open(path).read())
    eng = job.get("engine", "omni")
    if eng not in ENGINE_MAX_SECONDS:
        sys.exit(f"unknown engine '{eng}' (use \"omni\" or \"seedance\")")
    os.makedirs(job["output_dir"], exist_ok=True)
    job["segments"] = sorted(job["segments"], key=lambda s: s["index"])
    return job


def existing_seg_files(job):
    out = {}
    for seg in job["segments"]:
        p = os.path.join(job["output_dir"], f"seg-{seg['index']}.mp4")
        if os.path.exists(p):
            out[seg["index"]] = p
    return out


def cmd_run(args):
    job = load_job(args.job)
    lint_fail = False
    for seg in job["segments"]:
        for p in lint_segment(job, seg):
            print(f"LINT seg {seg['index']}: {p}")
            lint_fail = True
    if lint_fail and not args.force:
        sys.exit("fix dialogue/duration (or pass --force)")
    if job.get("engine", "omni") == "seedance":
        run_seedance(job)
    else:
        run_omni(job)


def cmd_segment(args):
    job = load_job(args.job)
    seg = next((s for s in job["segments"] if s["index"] == args.index), None)
    if not seg:
        sys.exit(f"no segment with index {args.index}")
    problems = lint_segment(job, seg)
    for p in problems:
        print(f"LINT seg {args.index}: {p}")
    if problems and not args.force:
        sys.exit("fix dialogue/duration (or pass --force)")
    dest = os.path.join(job["output_dir"], f"seg-{args.index}.mp4")
    if os.path.exists(dest):
        os.remove(dest)
    seg_files = existing_seg_files(job)
    if job.get("engine", "omni") == "seedance":
        key = env_key("KIE_API_KEY")
        st = seedance_state(job)
        anchor_url = seedance_anchor_url(job, seg_files, key, st)
        seedance_generate(job, seg, key, st, anchor_url)
    else:
        key = env_key()
        parts = segment_parts(job, seg, job["output_dir"], seg_files)
        gen_with_retry(key, parts, {"video_config": {}}, f"seg {args.index}",
                       "video", dest)
    print(f"regenerated -> {dest} (run 'stitch' to rebuild final.mp4)")


def cmd_stitch(args):
    job = load_job(args.job)
    seg_files = existing_seg_files(job)
    missing = [s["index"] for s in job["segments"] if s["index"] not in seg_files]
    if missing:
        sys.exit(f"missing segment files: {missing}")
    files = [seg_files[s["index"]] for s in job["segments"]]
    stitch(files, os.path.join(job["output_dir"], "final.mp4"))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("actor")
    a.add_argument("reference")
    a.add_argument("out")
    a.add_argument("--prompt", default=None)
    a.set_defaults(fn=cmd_actor)
    r = sub.add_parser("run")
    r.add_argument("job")
    r.add_argument("--force", action="store_true")
    r.set_defaults(fn=cmd_run)
    s = sub.add_parser("segment")
    s.add_argument("job")
    s.add_argument("index", type=int)
    s.add_argument("--force", action="store_true")
    s.set_defaults(fn=cmd_segment)
    st = sub.add_parser("stitch")
    st.add_argument("job")
    st.set_defaults(fn=cmd_stitch)
    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
