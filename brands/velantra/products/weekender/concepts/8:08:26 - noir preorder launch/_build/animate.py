#!/usr/bin/env python3
"""Animate the NOIR b-roll picks.

  omni      — 12 scenes via Google Omni (gemini-omni-flash-preview, Interactions API)
  kenburns  — 3 macro scenes as ffmpeg push-ins (macro-mutation law: never hand a macro to i2v)

Resumable: an existing clips/<id>.mp4 is skipped.
"""
import base64, json, os, pathlib, subprocess, sys, time, urllib.request, urllib.error

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
KF = ROOT / "broll-keyframes"
CLIPS = ROOT / "clips"
CLIPS.mkdir(exist_ok=True)
VAULT = "/Users/brooksorradre2/Documents/marketing brain"

ENV = {}
for line in open(os.path.join(VAULT, ".env")):
    line = line.strip()
    if "=" in line and not line.startswith("#"):
        k, v = line.split("=", 1)
        ENV[k] = v.strip().strip('"').strip("'")
GEMINI_KEY = ENV["GEMINI_API_KEY"]
BASE = "https://generativelanguage.googleapis.com/v1beta/interactions"

PICKS = json.loads((KF / "picks.json").read_text())
KENBURNS = ["NB-13-macro-turnlock", "NB-14-macro-interior", "NB-15-macro-gusset-eyelet"]

# Global negatives. The bag's failure modes under motion are known and specific.
FOOTER = (" The bag must not change shape, construction, colour or hardware at any point. "
          "Both gold clasp plates stay the same size and the same warm gold, neither vanishes and "
          "neither elongates. The two rolled handles stay intact and never stretch into a strap. "
          "No zipper ever appears. No lettering or engraving appears on any metal. No text or "
          "graphics on screen. Natural ambient sound only, no speech, no music. One continuous "
          "shot, no cuts, no transitions. Vertical 9:16.")


def api(url, payload=None, timeout=180):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        return json.loads(urllib.request.urlopen(req, timeout=timeout).read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code}: {e.read().decode('utf-8','replace')[:400]}")


def submit(image_path, motion):
    b64 = base64.b64encode(open(image_path, "rb").read()).decode()
    payload = {"model": "models/gemini-omni-flash-preview",
               "input": [{"type": "image", "data": b64, "mime_type": "image/png"},
                         {"type": "text", "text": motion + FOOTER}],
               "background": True,
               "generation_config": {"video_config": {}}}
    d = api(f"{BASE}?key={GEMINI_KEY}", payload)
    if "id" not in d:
        raise RuntimeError(f"no id: {json.dumps(d)[:300]}")
    return d["id"]


def poll(iid, timeout_s=1200):
    t0 = time.time()
    while time.time() - t0 < timeout_s:
        d = api(f"{BASE}/{iid}?key={GEMINI_KEY}")
        st = d.get("status")
        if st == "completed":
            for step in d.get("steps", []):
                for c in step.get("content", []):
                    if c.get("type") == "video" and c.get("data"):
                        return base64.b64decode(c["data"])
            raise RuntimeError("completed but no video part")
        if st in ("failed", "cancelled", "error"):
            raise RuntimeError(f"{st}: {json.dumps(d)[:300]}")
        time.sleep(12)
    raise TimeoutError(iid)


def run_omni():
    todo = [s for s in PICKS if s not in KENBURNS]
    for i, sid in enumerate(todo, 1):
        out = CLIPS / f"{sid}.mp4"
        if out.exists():
            print(f"[{sid}] exists, skip", flush=True)
            continue
        kf = KF / sid / f"{PICKS[sid]}.png"
        motion = (KF / sid / "motion.txt").read_text().strip()
        for attempt in range(3):
            try:
                iid = submit(str(kf), motion)
                print(f"[{sid}] ({i}/{len(todo)}) submitted {iid}", flush=True)
                out.write_bytes(poll(iid))
                print(f"[{sid}] saved {out.stat().st_size} bytes", flush=True)
                break
            except Exception as e:
                print(f"[{sid}] attempt {attempt}: {e}", flush=True)
                time.sleep(20)


def run_kenburns():
    for sid in KENBURNS:
        out = CLIPS / f"{sid}.mp4"
        if out.exists():
            print(f"[{sid}] exists, skip", flush=True)
            continue
        v = PICKS.get(sid, "v1")
        kf = KF / sid / f"{v}.png"
        if not kf.exists():
            kf = KF / sid / "v1.png"
        # upscale first so zoompan moves subpixel-smooth, then a slow 1.00 -> 1.11 push over 10s
        vf = ("scale=3240:5760:flags=lanczos,"
              "zoompan=z='1+0.00037*on':x='iw/2-(iw/zoom/2)':y='ih/2.15-(ih/zoom/2)':"
              "d=300:s=720x1280:fps=30,format=yuv420p")
        r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", str(kf),
                            "-vf", vf, "-t", "10", "-r", "30", "-c:v", "libx264",
                            "-preset", "medium", "-crf", "20", str(out)])
        ok = r.returncode == 0 and out.exists() and out.stat().st_size > 100_000
        print(f"[{sid}] {'ok' if ok else 'FAIL'}", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    if cmd in ("kenburns", "all"):
        run_kenburns()
    if cmd in ("omni", "all"):
        run_omni()
    print("DONE", flush=True)
