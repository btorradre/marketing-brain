#!/usr/bin/env python3
"""kie.ai Seedance 2.0 runner for the velantra-ugc skill.

Replaces the Higgsfield CLI (2026-07-07). Executes a segment manifest:
uploads local reference images, creates one bytedance/seedance-2 task per
segment, polls, downloads, optionally voice-anchors segments 2+ to segment 1's
audio, and stitches final.mp4. Resumable: finished segment files are skipped.

Usage:
  python3 kie_seedance.py upload <file>
  python3 kie_seedance.py run <manifest.json>
  python3 kie_seedance.py status <taskId>

Manifest shape:
{
  "concept_id": "VEL-STRATO-UGC-01",
  "output_dir": "/abs/path/output",
  "aspect_ratio": "9:16",
  "resolution": "720p",
  "mode": "ref",                      # "ref" (reference_image_urls, default) | "chain" (first_frame from prev lastFrameUrl)
  "voice_anchor": true,               # ref mode only: seg 1 audio becomes reference_audio for segs 2+
  "reference_images": ["/abs/creator-ref.png", "/abs/product-ref.png"],   # @Image1, @Image2 ... order
  "segments": [
    {"index": 1, "duration": 15, "prompt": "<full dense prompt>", "dialogue": "<spoken line only>",
     "images": ["/abs/override.png"],   # optional: replaces manifest reference_images for this segment
     "first_frame": "/abs/keyframe.png" # optional: chain-mode start frame override
    }
  ]
}
"""
import json
import os
import re
import ssl
import subprocess
import sys
import time
import urllib.request

try:  # macOS python.org builds lack system CAs — use certifi
    import certifi
    SSL_CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CTX = ssl.create_default_context()

API = "https://api.kie.ai/api/v1"
UPLOAD_API = "https://kieai.redpandaai.co/api/file-stream-upload"
MODEL = "bytedance/seedance-2"  # std only. seedance-2-fast is BANNED (distortion).

BANNED_CLAIMS = re.compile(
    r"\b(italian|italy|french|france|european|europe|american|america|usa|made in|imported from|hermes|hermès|birkin)\b",
    re.IGNORECASE,
)
BANNED_PUNCT = re.compile(r"[—–…]|\.\.\.")


def env_key():
    key = os.environ.get("KIE_API_KEY")
    if not key:
        env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "..", ".env")
        candidates = [os.path.normpath(env_path),
                      "/Users/brooksorradre2/Documents/marketing brain/.env"]
        for p in candidates:
            if os.path.exists(p):
                for line in open(p):
                    if line.strip().startswith("KIE_API_KEY="):
                        key = line.strip().split("=", 1)[1]
                        break
            if key:
                break
    if not key:
        sys.exit("KIE_API_KEY not found (env or marketing brain/.env)")
    return key


def api(method, url, key, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {key}")
    if data:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=120, context=SSL_CTX) as r:
        # strict=False: kie echoes prompts back with raw control chars in param/resultJson
        return json.loads(r.read().decode("utf-8", "replace"), strict=False)


def upload(path, key):
    # kie's R2 storage throws transient 500s — retry with backoff before giving up
    last = ""
    for attempt in range(4):
        if attempt:
            wait = 30 * attempt
            print(f"  upload retry {attempt + 1}/4 for {os.path.basename(path)} in {wait}s ({last[:120]})")
            time.sleep(wait)
        out = subprocess.run(
            ["curl", "-s", "-X", "POST", UPLOAD_API,
             "-H", f"Authorization: Bearer {key}",
             "-F", f"file=@{path}",
             "-F", "uploadPath=velantra-ugc",
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


def upload_cached(path, key, cache):
    # kie temp files expire (~24h) — cache per run only.
    path = os.path.abspath(path)
    if path not in cache:
        cache[path] = upload(path, key)
        print(f"  uploaded {os.path.basename(path)} -> {cache[path]}")
    return cache[path]


def validate(seg, allow=()):
    for field in ("prompt", "dialogue"):
        text = seg.get(field, "")
        if BANNED_PUNCT.search(text):
            sys.exit(f"seg {seg['index']}: em dash/ellipsis in {field} (house style hard fail)")
    # manifest "claims_allow" lists words Brooks explicitly approved for this concept
    hits = [h for h in BANNED_CLAIMS.findall(seg.get("dialogue", "")) if h.lower() not in allow]
    if hits:
        sys.exit(f"seg {seg['index']}: BANNED CLAIM in dialogue: {hits} (origin/Birkin/Hermes rule)")


def create_task(key, inp):
    resp = api("POST", f"{API}/jobs/createTask", key, {"model": MODEL, "input": inp})
    if resp.get("code") != 200:
        sys.exit(f"createTask failed: {resp}")
    return resp["data"]["taskId"]


def poll(key, task_id, label=""):
    while True:
        resp = api("GET", f"{API}/jobs/recordInfo?taskId={task_id}", key)
        d = resp.get("data", {})
        state = d.get("state")
        if state == "success":
            result = json.loads(d.get("resultJson") or "{}", strict=False)
            print(f"  {label} success ({d.get('creditsConsumed')} credits, {round((d.get('costTime') or 0)/1000)}s)")
            return result
        if state == "fail":
            print(f"  {label} FAILED: {d.get('failCode')} {d.get('failMsg')} (failed tasks are not charged)")
            return None
        time.sleep(15)


VPS_RELAY = "root@187.124.249.12"  # this machine's network resets TLS connections to kie's result CDN
                                     # (tempfile.aiquickdraw.com) — 2026-07-10 diagnosis. Relay through the
                                     # VPS instead of downloading directly until that's fixed locally.


def download(url, dest):
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


def extract_voice_anchor(seg1_mp4, out_dir, key, cache):
    wav = os.path.join(out_dir, "voice_anchor.mp3")
    if not os.path.exists(wav):
        subprocess.run(["ffmpeg", "-y", "-i", seg1_mp4, "-vn", "-t", "15",
                        "-ac", "1", "-b:a", "128k", wav],
                       check=True, capture_output=True)
    return upload_cached(wav, key, cache)


def stitch(files, out_path):
    lst = out_path + ".list.txt"
    with open(lst, "w") as f:
        for p in files:
            f.write(f"file '{p}'\n")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst,
                    "-c:v", "libx264", "-crf", "18", "-preset", "medium",
                    "-c:a", "aac", "-b:a", "192k", out_path],
                   check=True, capture_output=True)
    os.remove(lst)
    return out_path


def run(manifest_path):
    key = env_key()
    m = json.load(open(manifest_path))
    out_dir = m["output_dir"]
    os.makedirs(out_dir, exist_ok=True)
    cache_file = os.path.join(out_dir, "upload_cache.json")
    cache = json.load(open(cache_file)) if os.path.exists(cache_file) else {}
    tasks_file = os.path.join(out_dir, "tasks.json")  # seg index -> in-flight taskId (resume without re-charging)
    tasks = json.load(open(tasks_file)) if os.path.exists(tasks_file) else {}
    mode = m.get("mode", "ref")
    segs = sorted(m["segments"], key=lambda s: s["index"])
    seg_files, anchor_url, prev_last_frame = [], None, None
    # Regen case: an anchor from a prior run voice-locks ALL segments, including seg 1
    anchor_path = os.path.join(out_dir, "voice_anchor.mp3")
    if mode == "ref" and m.get("voice_anchor") and os.path.exists(anchor_path):
        anchor_url = upload_cached(anchor_path, key, cache)

    allow = {w.lower() for w in m.get("claims_allow", [])}
    for seg in segs:
        validate(seg, allow)
    print(f"{m['concept_id']}: {len(segs)} segments, mode={mode}")

    for seg in segs:
        i = seg["index"]
        dest = os.path.join(out_dir, f"seg_{i:02d}.mp4")
        if os.path.exists(dest) and os.path.getsize(dest) > 100_000:
            print(f"seg {i}: exists, skipping")
            seg_files.append(dest)
            if mode == "ref" and m.get("voice_anchor") and i == 1 and anchor_url is None:
                anchor_url = extract_voice_anchor(dest, out_dir, key, cache)
            continue

        inp = {
            "prompt": seg["prompt"],
            "aspect_ratio": m.get("aspect_ratio", "9:16"),
            "resolution": m.get("resolution", "720p"),
            "duration": seg["duration"],
            "generate_audio": True,
        }
        if mode == "ref":
            imgs = seg.get("images") or m.get("reference_images", [])
            inp["reference_image_urls"] = [upload_cached(p, key, cache) for p in imgs]
            if anchor_url:
                inp["reference_audio_urls"] = [anchor_url]
        else:  # chain
            ff = seg.get("first_frame")
            if ff:
                inp["first_frame_url"] = upload_cached(ff, key, cache)
            elif prev_last_frame:
                inp["first_frame_url"] = prev_last_frame

        task_id = tasks.get(str(i))
        if task_id:
            print(f"seg {i}: resuming task {task_id}")
        else:
            print(f"seg {i}: creating task ({seg['duration']}s)")
            task_id = create_task(key, inp)
            tasks[str(i)] = task_id
            json.dump(tasks, open(tasks_file, "w"), indent=1)
            json.dump(cache, open(cache_file, "w"), indent=1)
        result = poll(key, task_id, f"seg {i}")
        if result is None:
            tasks.pop(str(i), None)
            json.dump(tasks, open(tasks_file, "w"), indent=1)
            sys.exit(f"seg {i}: task failed — re-run the same command to retry with a fresh task")
        url = (result.get("resultUrls") or [None])[0]
        if not url:
            tasks.pop(str(i), None)
            json.dump(tasks, open(tasks_file, "w"), indent=1)
            sys.exit(f"seg {i}: no resultUrls in {result}")
        results_file = os.path.join(out_dir, "results.json")
        results = json.load(open(results_file)) if os.path.exists(results_file) else {}
        results[str(i)] = url
        json.dump(results, open(results_file, "w"), indent=1)
        # keep task_id in tasks.json until download actually succeeds — a download failure
        # (e.g. network block on the result CDN) must not force a re-generate on retry.
        download(url, dest)
        tasks.pop(str(i), None)
        json.dump(tasks, open(tasks_file, "w"), indent=1)
        seg_files.append(dest)
        prev_last_frame = result.get("lastFrameUrl")
        if mode == "ref" and m.get("voice_anchor") and i == 1:
            anchor_url = extract_voice_anchor(dest, out_dir, key, cache)
        json.dump(cache, open(cache_file, "w"), indent=1)

    final = os.path.join(out_dir, "final.mp4")
    if len(seg_files) > 1:
        stitch(seg_files, final)
    else:
        subprocess.run(["cp", seg_files[0], final], check=True)
    print(f"DONE -> {final}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "upload":
        print(upload(sys.argv[2], env_key()))
    elif cmd == "run":
        run(sys.argv[2])
    elif cmd == "status":
        print(json.dumps(api("GET", f"{API}/jobs/recordInfo?taskId={sys.argv[2]}", env_key()), indent=1))
    else:
        sys.exit(__doc__)
