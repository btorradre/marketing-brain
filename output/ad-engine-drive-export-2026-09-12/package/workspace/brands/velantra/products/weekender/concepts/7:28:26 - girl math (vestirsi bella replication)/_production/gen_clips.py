"""Step 2 — Google Omni motion from the approved GPT Image 2 keyframes (Gemini Interactions API)."""
import base64, json, os, pathlib, subprocess, sys, time

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from scenes import SCENES

KEY = os.environ["GEMINI_API_KEY"]
BASE = "https://generativelanguage.googleapis.com/v1beta/interactions"
KF = HERE / "keyframes"
OUT = HERE / "clips"; OUT.mkdir(exist_ok=True)
TMP = HERE / ".tmp"; TMP.mkdir(exist_ok=True)


def sh(args, **kw):
    return subprocess.run(args, capture_output=True, text=True, **kw).stdout


def small_jpeg(png):
    """Downscale the keyframe so the inline part stays light."""
    dst = TMP / (png.stem + "_720.jpg")
    if not dst.exists():
        subprocess.run(["ffmpeg", "-v", "error", "-i", str(png), "-vf", "scale=720:1280",
                        "-q:v", "3", "-y", str(dst)], check=True)
    return dst


def launch(img, prompt):
    body = {
        "model": "models/gemini-omni-flash-preview",
        "input": [
            {"type": "image", "data": base64.b64encode(img.read_bytes()).decode(),
             "mime_type": "image/jpeg"},
            {"type": "text", "text": prompt},
        ],
        "background": True,
        "generation_config": {"video_config": {}},
    }
    f = TMP / "req.json"
    f.write_text(json.dumps(body))
    r = sh(["curl", "-s", "-X", "POST", f"{BASE}?key={KEY}",
            "-H", "Content-Type: application/json", "-d", f"@{f}"])
    d = json.loads(r, strict=False)
    if "error" in d:
        raise RuntimeError(d["error"].get("message", "")[:300])
    return d.get("id") or d["name"].split("/")[-1]


def collect(iid, dst, timeout=900):
    t0 = time.time()
    while time.time() - t0 < timeout:
        raw = sh(["curl", "-s", f"{BASE}/{iid}?key={KEY}"])
        d = json.loads(raw, strict=False)
        st = d.get("status")
        if st == "completed":
            for step in d.get("steps", []):
                for c in step.get("content", []):
                    if c.get("type") == "video":
                        dst.write_bytes(base64.b64decode(c["data"]))
                        return True
            raise RuntimeError("completed but no video part")
        if st in ("failed", "cancelled"):
            raise RuntimeError(f"{st}: {json.dumps(d)[:300]}")
        time.sleep(10)
    raise TimeoutError(iid)


def main():
    only = sys.argv[1:] or [s["id"] for s in SCENES]
    jobs = {}
    for s in SCENES:
        if s["id"] not in only:
            continue
        dst = OUT / f"CLIP-{s['id']}.mp4"
        if dst.exists():
            print(f"[{s['id']}] exists, skip"); continue
        img = small_jpeg(KF / f"KF-{s['id']}.png")
        for attempt in range(3):
            try:
                jobs[s["id"]] = launch(img, s["motion"])
                print(f"[{s['id']}] {s['name']} -> {jobs[s['id']]}")
                break
            except Exception as e:
                print(f"[{s['id']}] launch attempt {attempt+1} failed: {e}")
                time.sleep(8)

    for sid, iid in jobs.items():
        dst = OUT / f"CLIP-{sid}.mp4"
        try:
            collect(iid, dst)
            print(f"[{sid}] saved {dst.name} ({dst.stat().st_size//1024}kb)")
        except Exception as e:
            print(f"[{sid}] ERROR {e}")


if __name__ == "__main__":
    main()
