#!/usr/bin/env python3
"""Animate approved keyframes with Google Omni (Interactions API via curl, per house reference).
  python3 omni_animate.py run [CLIP-ID ...]     # animate picks in state/picks.json (or given ids)
  python3 omni_animate.py status
picks.json: {"COL-001": {"kf": "keyframes/COL-001/v1.png", "motion": "..."}}"""
import base64, json, os, subprocess, sys, time, tempfile
from PIL import Image
from common import *
from manifest import CLIPS as MANIFEST
KEY = ENV["GEMINI_API_KEY"]; BASE = "https://generativelanguage.googleapis.com/v1beta/interactions"
PICKS = os.path.join(STATE, "picks.json"); ST = os.path.join(STATE, "omni.json")
LOCK = (" The bag keeps exactly its shape, proportions and every detail from the image for the entire clip: "
        "same two top handles, same slim leather belt with its two free ends and small round gold disc caps, "
        "same two vertical felt straps, open top, nothing appears or disappears on the bag. No on-screen text, "
        "no captions, no graphics. Handheld iPhone footage, natural light, slight hand shake, realistic focus. "
        "No people speaking, natural ambient sound only. Vertical 9:16.")

def curl_json(url, payload=None):
    args = ["curl", "-s", "--max-time", "180", url, "-H", "Content-Type: application/json"]
    if payload is not None:
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(payload, f); p = f.name
        args += ["-X", "POST", "--data-binary", f"@{p}"]
    out = subprocess.run(args, capture_output=True, text=True).stdout
    if payload is not None: os.unlink(p)
    return json.loads(out) if out.strip() else {}

def to_720(kf):
    im = Image.open(kf).convert("RGB"); w, h = im.size
    tw, th = 720, 1280
    s = max(tw / w, th / h); im = im.resize((round(w * s), round(h * s)), Image.LANCZOS)
    w, h = im.size; l = (w - tw) // 2; t = (h - th) // 2
    im = im.crop((l, t, l + tw, t + th)); buf = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
    im.save(buf.name, "JPEG", quality=92); return buf.name

def submit(kf, motion):
    jpg = to_720(kf); b64 = base64.b64encode(open(jpg, "rb").read()).decode(); os.unlink(jpg)
    d = curl_json(f"{BASE}?key={KEY}", {"model": "models/gemini-omni-1.1-flash",
        "input": [{"type": "image", "data": b64, "mime_type": "image/jpeg"}, {"type": "text", "text": motion}],
        "background": True, "generation_config": {"video_config": {}}})
    if "id" not in d: raise RuntimeError(json.dumps(d)[:300])
    return d["id"]

def poll(iid, timeout_s=900):
    t0 = time.time()
    while time.time() - t0 < timeout_s:
        d = curl_json(f"{BASE}/{iid}?key={KEY}")
        st = d.get("status")
        if st == "completed":
            for step in d.get("steps", []):
                for c in step.get("content", []):
                    if c.get("type") == "video" and c.get("data"): return base64.b64decode(c["data"])
            raise RuntimeError("completed, no video part")
        if st in ("failed", "cancelled", "error"): raise RuntimeError(f"{st}: {json.dumps(d)[:300]}")
        time.sleep(12)
    raise TimeoutError(iid)

def animate(cid, pick, state):
    out = os.path.join(CLIPS, f"{cid}.mp4")
    if os.path.exists(out) and os.path.getsize(out) > 100_000: return out, "cached"
    kf = os.path.join(ROOT, pick["kf"]); motion = pick["motion"] + LOCK
    last = None
    for attempt in range(4):
        try:
            iid = submit(kf, motion); state[cid] = {"iid": iid, "kf": pick["kf"]}; save(ST, state)
            data = poll(iid); open(out, "wb").write(data)
            if os.path.getsize(out) < 100_000: raise RuntimeError("tiny clip")
            state[cid]["done"] = True; save(ST, state); return out, iid
        except Exception as e:
            last = e; time.sleep(15 + 15 * attempt)
    raise RuntimeError(f"{cid}: {last}")

def cmd_run(ids, workers=4):
    import queue, threading
    picks = load(PICKS, {}); state = load(ST, {}); lock = threading.Lock(); q = queue.Queue()
    for cid, p in picks.items():
        if ids and cid not in ids: continue
        out = os.path.join(CLIPS, f"{cid}.mp4")
        if os.path.exists(out) and os.path.getsize(out) > 100_000: continue
        q.put((cid, p))
    print(f"queue {q.qsize()}", flush=True)
    def worker(w):
        time.sleep(w * 5)
        while True:
            try: cid, p = q.get_nowait()
            except queue.Empty: return
            try:
                with lock: st = dict(state)
                out, iid = animate(cid, p, st)
                with lock: state.update(st); save(ST, state)
                print(cid, "ok", flush=True)
            except Exception as e: print(cid, "FAIL", e, flush=True)
    th = [threading.Thread(target=worker, args=(i,), daemon=True) for i in range(workers)]
    [t.start() for t in th]; [t.join() for t in th]

if __name__ == "__main__":
    c = sys.argv[1] if len(sys.argv) > 1 else "status"
    if c == "run": cmd_run(sys.argv[2:])
    else:
        picks = load(PICKS, {}); done = [f for f in os.listdir(CLIPS) if f.endswith(".mp4")]
        print(f"picks {len(picks)}, clips {len(done)}")
