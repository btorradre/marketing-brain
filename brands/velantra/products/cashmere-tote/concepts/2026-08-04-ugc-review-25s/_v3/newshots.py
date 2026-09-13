#!/usr/bin/env python3
"""Two new Colette b-roll shots for the REVIEW-03 recut, built on the exact
prompt machinery that produced the 200-clip library (same product truth, same
photoreal footer), but writing into this concept folder instead of library state.

  python3 newshots.py prompt COL-091
  python3 newshots.py keys            # GPT Image 2 i2i, 3 variants per shot
  python3 newshots.py animate COL-091 v2
"""
import base64, json, os, subprocess, sys, time

# framework python has no cert chain of its own; urllib -> api.kie.ai dies without this
try:
    import certifi
    os.environ.setdefault("SSL_CERT_FILE", certifi.where())
except ImportError:
    pass

VAULT = os.path.expanduser("~/Documents/marketing brain")
LIB = os.path.join(VAULT, "brands/velantra/_shared/creative/broll-library-2026-08")
sys.path.insert(0, LIB)
import pipeline as P

HERE = os.path.dirname(os.path.abspath(__file__))
KF = os.path.join(HERE, "keyframes")
CLIPS = os.path.join(HERE, "clips")
STATE = os.path.join(HERE, "state")
for d in (KF, CLIPS, STATE):
    os.makedirs(d, exist_ok=True)

# scene tuple = (id, product, colorway, category, open_bag, scene, motion)
SCENES = [
    ("COL-091-pan-full-bag", "colette", "caramel", "hero", False,
     "A photo of the bag standing on a pale wooden bench under a window in a lived in room, "
     "shot straight on from across the room so the ENTIRE bag is inside the frame from the tips "
     "of both handles down to the base with clear empty space above and below it, nothing "
     "cropped off at any edge. Soft late afternoon window light rakes across the felt from the "
     "left. The full width of the bag reads clearly, a folded newspaper and a set of keys sit on "
     "the bench beside it.",
     "One continuous unbroken shot. The camera glides slowly and steadily sideways, travelling "
     "from the left end of the bag across to the right end and continuing, a smooth lateral "
     "handheld move with a gentle natural sway, as if someone is walking slowly past it with a "
     "phone. The whole bag stays fully inside the frame for the entire move and is never cropped. "
     "Nothing in the scene moves, the bag stays exactly where it is on the bench, and every "
     "detail of the bag stays exactly as in the image."),

    # r1 and r2 both grew an Apple logo on the silver lid and a snap tab on the inner rim.
    # 092b removes both attractors at the keyframe: laptop is matte charcoal and turned edge on,
    # and the bare rim is stated in the scene, not only in the motion.
    ("COL-092b-pack-continuous-three", "colette", "caramel", "pack", True,
     "A photo taken from just above and slightly to one side of the bag, which stands wide open "
     "on a bed made with white linen. A woman's hands have just entered the top of the frame "
     "holding a closed matte charcoal grey 13 inch laptop TURNED EDGE ON, so only its thin dark "
     "side edge faces the camera and no face of the lid is visible at all, lowering it down into "
     "the open mouth of the bag. The laptop is a plain dark slab with no logo, no symbol and no "
     "lettering on any surface. The top rim of the bag is a plain bare felt edge, completely "
     "empty all the way round, with no tab, no button, no snap and no fastening of any kind on it "
     "or on the inside wall. Waiting on the linen beside the bag and fully in frame are a plain "
     "steel water bottle lying on its side and a folded cream cable knit sweater. Her arms are "
     "bare to the elbow, no face and no head anywhere in the frame, soft morning light from a "
     "window to the left.",
     "ONE CONTINUOUS UNBROKEN SHOT with no cuts and no jumps. Her hands lower the laptop the rest "
     "of the way into the bag and settle it flat against the back wall, then without pausing her "
     "hands pick up the steel water bottle from the linen and slide it down into the bag beside "
     "the laptop, then without pausing her hands pick up the folded cream sweater from the linen "
     "and press it down into the bag on top of the other two. She works BRISKLY: all three items "
     "are fully inside the bag within the first five seconds, and after that her hands simply "
     "withdraw out of the frame and nothing else happens. The bag never overflows and still "
     "stands upright. The camera holds one steady position the whole time with a gentle handheld "
     "sway and never cuts away. "
     "THE BAG IS A FIXED OBJECT. It stays exactly where it is on the bed. It never rotates, never "
     "turns toward or away from the camera, never becomes rounder, deeper or more oval, and keeps "
     "the same flat wide rectangular front face it has in the first frame for every single frame. "
     "The two vertical felt straps, the horizontal caramel leather belt threaded through them and "
     "the two small round gold disc caps at the belt ends stay in exactly the same places and the "
     "same shapes throughout and are visible in every frame. "
     "NEVER: the top rim of the bag stays a plain bare open felt edge for the entire clip. No tab, "
     "no loop, no strap, no button, no snap, no magnet, no clasp, no buckle and no closure of any "
     "kind ever appears on the rim, on the inside wall or anywhere else on the bag. No new "
     "hardware appears at any point. No logo, lettering, engraving or marking appears on the bag "
     "or on the gold caps. The laptop stays a plain matte charcoal grey slab and NO logo, NO "
     "fruit symbol, NO badge and NO lettering ever appears on any face of it. No second bag and "
     "no other person enters the frame."),
]

BASE = "https://generativelanguage.googleapis.com/v1beta/interactions"


def scene(sid):
    return next(s for s in SCENES if s[0].startswith(sid))


def cmd_keys(variants=3):
    uploads = P.load(P.UPLOADS_FILE, {})
    st = P.load(os.path.join(STATE, "keyframes.json"), {})
    for s in SCENES:
        d = os.path.join(KF, s[0])
        os.makedirs(d, exist_ok=True)
        prompt = P.build_prompt(s)
        input_urls = [P.get_upload(p, uploads) for p in P.refs_for(s)]
        for v in range(1, variants + 1):
            out = os.path.join(d, f"v{v}.png")
            if os.path.exists(out) and os.path.getsize(out) > 10000:
                print(f"{s[0]} v{v} cached")
                continue
            for attempt in range(5):
                try:
                    tid = P.kie_create("gpt-image-2-image-to-image",
                                       {"prompt": prompt, "input_urls": input_urls,
                                        "aspect_ratio": "9:16", "resolution": "1K"})
                    urls = P.kie_poll(tid)
                    if not urls or not P.download(urls[0], out):
                        raise RuntimeError("no usable result")
                    st.setdefault(s[0], {})[f"v{v}"] = {"ok": True, "task": tid}
                    P.save(os.path.join(STATE, "keyframes.json"), st)
                    print(f"{s[0]} v{v} ok  {tid}", flush=True)
                    break
                except Exception as e:
                    print(f"{s[0]} v{v} retry {attempt}: {str(e)[:160]}", flush=True)
                    time.sleep(10 + attempt * 10)
            else:
                print(f"{s[0]} v{v} FAILED", flush=True)


def _api(url, payload=None, timeout=180):
    import tempfile
    args = ["curl", "-s", "--max-time", str(timeout), url]
    tmp = None
    if payload is not None:
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
            json.dump(payload, fh)
            tmp = fh.name
        args += ["-H", "Content-Type: application/json", "--data-binary", f"@{tmp}"]
    try:
        out = subprocess.run(args, capture_output=True, text=True)
    finally:
        if tmp:
            os.unlink(tmp)
    try:
        return json.loads(out.stdout)
    except ValueError:
        raise RuntimeError((out.stdout or out.stderr)[:300])


def cmd_animate(sid, variant, tag=""):
    s = scene(sid)
    key = os.environ.get("GEMINI_API_KEY") or P.ENV["GEMINI_API_KEY"]
    kf = os.path.join(KF, s[0], f"{variant}.png")
    out = os.path.join(CLIPS, f"{s[0]}{tag}.mp4")
    if os.path.exists(out) and os.path.getsize(out) > 100_000:
        print("cached", out)
        return out
    motion = P.motion_prompt(s)
    payload = {"model": "models/gemini-omni-flash-preview",
               "input": [{"type": "image", "data": base64.b64encode(open(kf, "rb").read()).decode(),
                          "mime_type": "image/png"},
                         {"type": "text", "text": motion}],
               "background": True,
               "generation_config": {"video_config": {}}}
    last = None
    for attempt in range(5):
        try:
            d = _api(f"{BASE}?key={key}", payload)
            if "id" not in d:
                raise RuntimeError(json.dumps(d)[:300])
            iid = d["id"]
            t0 = time.time()
            while time.time() - t0 < 900:
                r = _api(f"{BASE}/{iid}?key={key}")
                stt = r.get("status")
                if stt == "completed":
                    for step in r.get("steps", []):
                        for c in step.get("content", []):
                            if c.get("type") == "video" and c.get("data"):
                                open(out, "wb").write(base64.b64decode(c["data"]))
                                print("OK", out, f"{os.path.getsize(out)//1024}KB")
                                return out
                    raise RuntimeError("completed, no video part")
                if stt in ("failed", "cancelled", "error"):
                    raise RuntimeError(f"{stt}: {json.dumps(r)[:300]}")
                time.sleep(12)
            raise TimeoutError(iid)
        except Exception as e:
            last = e
            print(f"retry {attempt}: {str(e)[:200]}", flush=True)
            time.sleep(15 + attempt * 15)
    raise RuntimeError(f"{s[0]}: {last}")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "prompt":
        s = scene(sys.argv[2])
        print(P.build_prompt(s))
        print("\n--- MOTION ---\n" + P.motion_prompt(s))
    elif cmd == "keys":
        cmd_keys()
    elif cmd == "animate":
        cmd_animate(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else "")
