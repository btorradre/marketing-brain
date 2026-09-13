#!/usr/bin/env python3
"""Stage 3 — animate every picked still via Google Omni (Interactions API).

  python3 animate_omni.py probe S03
  python3 animate_omni.py run
  python3 animate_omni.py status

Macro scenes (S09/S10/S11) get exactly ONE roll. Omni re-synthesizes hardware at
high magnification and is 0/5 on re-rolls, so a drifted macro goes to Ken Burns
instead of another spin (feedback_omni_macro_mutation).
"""
import base64, json, os, ssl, sys, time, urllib.request, urllib.error
import certifi

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from scenes import SCENES, scene_by_id

VAULT = "/Users/brooksorradre2/Documents/marketing brain"
PICKS = os.path.join(HERE, "picks.json")
CLIPS = os.path.join(ROOT, "clips")
KEYFRAMES = os.path.join(ROOT, "keyframes")
STATE = os.path.join(HERE, "state_omni.json")
os.makedirs(CLIPS, exist_ok=True)

CTX = ssl.create_default_context(cafile=certifi.where())
BASE = "https://generativelanguage.googleapis.com/v1beta/interactions"


def env(k):
    for line in open(os.path.join(VAULT, ".env")):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            a, b = line.split("=", 1)
            if a.strip() == k:
                return b.strip().strip('"').strip("'")
    raise KeyError(k)


KEY = env("GEMINI_OMNI_API_KEY")


def load(p, d):
    return json.load(open(p)) if os.path.exists(p) else d


def save(p, o):
    json.dump(o, open(p, "w"), indent=2)


def api(url, payload=None, timeout=180):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        return json.loads(urllib.request.urlopen(req, timeout=timeout, context=CTX).read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code}: {e.read().decode('utf-8','replace')[:400]}")


def motion_prompt(s):
    """Motion only. The still already carries construction; do not re-describe it."""
    return (
        f"{s['motion']}\n\n"
        "Animate the attached photograph directly. Keep the bag, the room, the light and the "
        "framing exactly as they are in the photograph. Do not redesign, restyle or re-light "
        "anything. The bag's construction must not change at any point: the leather and canvas "
        "split stays exactly where it is, the handles stay smooth simple leather tubes, the "
        "hardware keeps its exact shape and stays warm brass gold on both sides, and no zipper, "
        "logo, engraving, lettering or brand stamp appears anywhere at any moment. "
        "Real handheld phone footage, natural available light, subtle grain, no camera shake "
        "beyond a slight handheld drift. No text or graphics on screen."
    )


def submit(image_path, motion):
    b64 = base64.b64encode(open(image_path, "rb").read()).decode()
    d = api(f"{BASE}?key={KEY}", {
        "model": "models/gemini-omni-flash-preview",
        "input": [
            {"type": "image", "data": b64, "mime_type": "image/png"},
            {"type": "text", "text": motion},
        ],
        "background": True,
        "generation_config": {"video_config": {}},
    })
    if "id" not in d:
        raise RuntimeError(f"no id: {json.dumps(d)[:300]}")
    return d["id"]


def poll(iid, timeout_s=1200):
    t0 = time.time()
    while time.time() - t0 < timeout_s:
        d = api(f"{BASE}/{iid}?key={KEY}")
        st = d.get("status")
        if st == "completed":
            for step in d.get("steps", []):
                for c in step.get("content", []):
                    if c.get("type") == "video" and c.get("data"):
                        return base64.b64decode(c["data"])
            raise RuntimeError("completed but no video part")
        if st in ("failed", "cancelled", "error"):
            raise RuntimeError(f"{st}: {json.dumps(d)[:400]}")
        time.sleep(12)
    raise TimeoutError(iid)


def animate(sid, state):
    s = scene_by_id(sid)
    picks = load(PICKS, {})
    variant = picks.get(sid)
    if not variant:
        raise RuntimeError(f"{sid}: no pick recorded in picks.json")
    kf = os.path.join(KEYFRAMES, sid, f"{variant}.png")
    if not os.path.exists(kf):
        raise FileNotFoundError(kf)
    out = os.path.join(CLIPS, f"{sid}.mp4")
    if os.path.exists(out) and os.path.getsize(out) > 100_000:
        return out, "cached"
    # macros get one shot only
    attempts = 1 if s["macro"] else 4
    ent = state.get(sid, {})
    last = None
    for a in range(attempts):
        try:
            iid = ent.get("iid") or submit(kf, motion_prompt(s))
            ent["iid"] = iid
            state[sid] = ent
            save(STATE, state)
            data = poll(iid)
            open(out, "wb").write(data)
            if os.path.getsize(out) < 100_000:
                raise RuntimeError("clip too small")
            ent.update(done=True, variant=variant)
            state[sid] = ent
            save(STATE, state)
            return out, iid
        except Exception as e:
            last = e
            ent["iid"] = None
            state[sid] = ent
            save(STATE, state)
            print(f"    {sid} attempt {a+1} failed: {str(e)[:160]}")
            time.sleep(15 + a * 15)
    raise RuntimeError(f"{sid}: {last}")


def cmd_run(only=None):
    state = load(STATE, {})
    picks = load(PICKS, {})
    todo = [s["id"] for s in SCENES if s["id"] in picks and (not only or s["id"] in only)]
    print(f"{len(todo)} clips to animate", flush=True)
    for i, sid in enumerate(todo, 1):
        try:
            out, iid = animate(sid, state)
            print(f"[{i}/{len(todo)}] {sid} ok", flush=True)
        except Exception as e:
            print(f"[{i}/{len(todo)}] {sid} FAIL {str(e)[:200]}", flush=True)
        time.sleep(4)


def cmd_status():
    picks = load(PICKS, {})
    done = [f[:-4] for f in os.listdir(CLIPS) if f.endswith(".mp4")] if os.path.isdir(CLIPS) else []
    print(f"picks {len(picks)}/{len(SCENES)}, clips {len(done)}/{len(picks) or len(SCENES)}")
    missing = [s["id"] for s in SCENES if s["id"] not in done]
    if missing:
        print("missing:", " ".join(missing))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "probe":
        st = load(STATE, {})
        print("OK", *animate(sys.argv[2], st))
    elif cmd == "run":
        cmd_run(sys.argv[2:] or None)
    else:
        cmd_status()
