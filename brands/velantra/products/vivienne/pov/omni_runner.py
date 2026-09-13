#!/usr/bin/env python3
"""Omni i2v runner for the VIV-POV set. Keyframe -> 10s clip, curl transport."""
import base64, json, os, subprocess, sys, time, tempfile

ROOT = os.path.dirname(os.path.abspath(__file__))
ENV = "/Users/brooksorradre2/Documents/marketing brain/.env"
KEY = None
for line in open(ENV):
    line = line.strip()
    if line.startswith("GEMINI_API_KEY"):
        KEY = line.split("=", 1)[1].strip().strip('"').strip("'")
assert KEY, "no GEMINI_API_KEY"

API = "https://generativelanguage.googleapis.com/v1beta/interactions"
MODEL = "models/gemini-omni-flash-preview"


def curl_json(url, payload=None):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        if payload is not None:
            json.dump(payload, f)
        p = f.name
    cmd = ["curl", "-s", "-X", "GET" if payload is None else "POST", url]
    if payload is not None:
        cmd += ["-H", "Content-Type: application/json", "--data-binary", "@" + p]
    out = subprocess.run(cmd, capture_output=True, text=True).stdout
    os.unlink(p)
    try:
        return json.loads(out)
    except Exception:
        return {"error": {"message": out[:500]}}


def to_jpeg(png, dest, w=720, h=1280):
    subprocess.run(["ffmpeg", "-v", "error", "-i", png, "-vf",
                    f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}",
                    "-q:v", "2", dest, "-y"], check=True)
    return dest


def launch(keyframe_png, prompt):
    jpg = to_jpeg(keyframe_png, os.path.join(tempfile.gettempdir(),
                  os.path.basename(keyframe_png) + ".jpg"))
    b64 = base64.b64encode(open(jpg, "rb").read()).decode()
    payload = {"model": MODEL,
               "input": [{"type": "image", "data": b64, "mime_type": "image/jpeg"},
                         {"type": "text", "text": prompt}],
               "background": True,
               "generation_config": {"video_config": {}}}
    d = curl_json(f"{API}?key={KEY}", payload)
    return d.get("id"), d


def poll(job_id, timeout=600):
    t0 = time.time()
    while time.time() - t0 < timeout:
        d = curl_json(f"{API}/{job_id}?key={KEY}")
        st = d.get("status")
        if st == "completed":
            for step in d.get("steps", []):
                for c in step.get("content", []):
                    if c.get("type") == "video":
                        return c.get("data"), d
            return None, d
        if st in ("failed", "cancelled"):
            return None, d
        time.sleep(10)
    return None, {"error": {"message": "timeout"}}


if __name__ == "__main__":
    jobs = json.load(open(sys.argv[1]))
    outdir = os.path.join(ROOT, "clips")
    os.makedirs(outdir, exist_ok=True)
    handles = {}
    for j in jobs:
        dest = os.path.join(outdir, j["id"] + ".mp4")
        if os.path.exists(dest):
            print(f"[skip] {j['id']} exists"); continue
        hid, raw = launch(os.path.join(ROOT, "frames", j["frame"]), j["prompt"])
        if not hid:
            print(f"[FAIL-LAUNCH] {j['id']}: {json.dumps(raw)[:300]}"); continue
        handles[j["id"]] = hid
        print(f"[launched] {j['id']} -> {hid}")
    json.dump(handles, open(os.path.join(ROOT, "omni_handles.json"), "w"), indent=1)
    for jid, hid in handles.items():
        b64, raw = poll(hid)
        dest = os.path.join(outdir, jid + ".mp4")
        if b64:
            open(dest, "wb").write(base64.b64decode(b64))
            print(f"[done] {jid} -> {dest}")
        else:
            print(f"[FAIL] {jid}: {json.dumps(raw)[:300]}")
