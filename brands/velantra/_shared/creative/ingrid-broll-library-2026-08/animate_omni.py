#!/usr/bin/env python3
"""Animate picked keyframes via Google Omni (gemini-omni-flash-preview, Interactions API).

Commands:
  python3 animate_omni.py probe SCENE-ID [variant]   # animate one keyframe now
  python3 animate_omni.py run                        # animate all picks in state/picks.json
  python3 animate_omni.py status
Picks file format: {"COL-001-...": "v2", ...}
"""
import base64, json, os, sys, time, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from pipeline import ENV, SCENES, scene_by_id, motion_prompt, load, save

GEMINI_KEY = ENV["GEMINI_API_KEY"]
BASE = "https://generativelanguage.googleapis.com/v1beta/interactions"
CLIPS = os.path.join(HERE, "clips")
STATE_DIR = os.path.join(HERE, "state")
os.makedirs(CLIPS, exist_ok=True)
STATE_FILE = os.path.join(STATE_DIR, "omni.json")
PICKS_FILE = os.path.join(STATE_DIR, "picks.json")


def api(url, payload=None, timeout=120):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        return json.loads(urllib.request.urlopen(req, timeout=timeout).read())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")[:500]
        raise RuntimeError(f"HTTP {e.code}: {body}")


def submit(image_path, motion):
    b64 = base64.b64encode(open(image_path, "rb").read()).decode()
    payload = {
        "model": "models/gemini-omni-flash-preview",
        "input": [
            {"type": "image", "data": b64, "mime_type": "image/png"},
            {"type": "text", "text": motion},
        ],
        "background": True,
        "generation_config": {"video_config": {}},
    }
    d = api(f"{BASE}?key={GEMINI_KEY}", payload)
    if "id" not in d:
        raise RuntimeError(f"no id in response: {json.dumps(d)[:300]}")
    return d["id"]


def poll(iid, timeout_s=900):
    t0 = time.time()
    while time.time() - t0 < timeout_s:
        d = api(f"{BASE}/{iid}?key={GEMINI_KEY}")
        st = d.get("status")
        if st == "completed":
            for step in d.get("steps", []):
                for c in step.get("content", []):
                    if c.get("type") == "video" and c.get("data"):
                        return base64.b64decode(c["data"])
            raise RuntimeError("completed but no video part found")
        if st in ("failed", "cancelled", "error"):
            raise RuntimeError(f"interaction {st}: {json.dumps(d)[:400]}")
        time.sleep(12)
    raise TimeoutError(iid)


def animate(sid, variant, state):
    s = scene_by_id(sid)
    kf = os.path.join(HERE, "keyframes", s[0], f"{variant}.png")
    if not os.path.exists(kf):
        raise FileNotFoundError(kf)
    out = os.path.join(CLIPS, f"{s[0]}.mp4")
    if os.path.exists(out) and os.path.getsize(out) > 100_000:
        return out, "cached"
    motion = motion_prompt(s)
    ent = state.get(s[0], {})
    last_err = None
    for attempt in range(5):
        try:
            iid = ent.get("iid")
            if not iid:
                iid = submit(kf, motion)
                ent["iid"] = iid
                state[s[0]] = ent
                save(STATE_FILE, state)
            data = poll(iid)
            open(out, "wb").write(data)
            if os.path.getsize(out) < 100_000:
                raise RuntimeError("clip too small")
            ent["done"] = True
            state[s[0]] = ent
            save(STATE_FILE, state)
            return out, iid
        except Exception as e:
            last_err = e
            ent["iid"] = None  # dead interaction, resubmit
            state[s[0]] = ent
            save(STATE_FILE, state)
            time.sleep(15 + attempt * 15)
    raise RuntimeError(f"{s[0]}: {last_err}")


def cmd_probe(sid, variant="v1"):
    state = load(STATE_FILE, {})
    out, iid = animate(sid, variant, state)
    print("OK", out, iid)


def cmd_run(workers=4):
    import queue, threading
    state = load(STATE_FILE, {})
    picks = load(PICKS_FILE, {})
    lock = threading.Lock()
    q = queue.Queue()
    for s in SCENES:
        sid = s[0]
        if sid not in picks:
            continue
        out = os.path.join(CLIPS, f"{sid}.mp4")
        if os.path.exists(out) and os.path.getsize(out) > 100_000:
            continue
        q.put((sid, picks[sid]))
    total = q.qsize()
    print(f"queue: {total} clips, {workers} workers", flush=True)
    counters = {"done": 0, "fail": 0}

    def worker(wid):
        time.sleep(wid * 5)
        while True:
            try:
                sid, variant = q.get_nowait()
            except queue.Empty:
                return
            try:
                with lock:
                    st = dict(state)
                out, iid = animate(sid, variant, st)
                with lock:
                    state.update(st)
                    counters["done"] += 1
                    save(STATE_FILE, state)
                    n = counters["done"] + counters["fail"]
                print(f"[{n}/{total}] {sid} ok", flush=True)
            except Exception as e:
                with lock:
                    counters["fail"] += 1
                print(f"{sid} FAIL {e}", flush=True)
            q.task_done()

    threads = [threading.Thread(target=worker, args=(i,), daemon=True) for i in range(workers)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"done: {counters['done']} clips, {counters['fail']} failed")


def cmd_status():
    picks = load(PICKS_FILE, {})
    clips = [f for f in os.listdir(CLIPS) if f.endswith(".mp4")] if os.path.exists(CLIPS) else []
    print(f"picks: {len(picks)}, clips done: {len(clips)}/{len(picks) or 200}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "probe":
        cmd_probe(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "v1")
    elif cmd == "run":
        cmd_run()
    else:
        cmd_status()
