#!/usr/bin/env python3
"""The Delphine — B-roll library animator. Stills in `stills/`, clips out to `clips/`.

Usage:
    python3 animate.py launch          # fire every still that has no clip yet
    python3 animate.py launch B04 B09  # fire only matching shots
    python3 animate.py poll            # download whatever has finished
    python3 animate.py qa              # first-frame vs last-frame drift check

Engine is Google Omni, billed to the Gemini key, NOT Higgsfield credits.

═══════════════════════════════════════════════════════════════════════════════
TWO LAWS THIS FILE EXISTS TO ENFORCE. Do not "improve" the prompts past them.
═══════════════════════════════════════════════════════════════════════════════

1. THE CAMERA ALWAYS MOVES, AT A CONSTANT DISTANCE.
   Static b-roll is a failure in its own right — a shot that reveals nothing new gives the
   viewer no reason to stay. Every shot carries an arc, an orbit or a lateral slide that
   shows a NEW angle of the bag as it goes.

2. NEVER A PUSH-IN, DOLLY-IN OR ZOOM.
   This is the ONLY banned move, and the reason is specific: every push-in in the first
   build inflated the bag. B11 opened as a handbag and ended a weekender. On a product
   whose whole claim is "it is small", that silently destroys the pitch. An arc at a fixed
   radius has none of that risk because the distance never changes — which is exactly why
   banning ALL movement (the previous version of this file) was an over-correction.

QA IS ON THE MOTION, NOT THE STILL. The stills passed contact-sheet review last time and
the defect was only visible in the animation. `qa` extracts first and last frames so
drift is measurable rather than eyeballed.
"""
import base64, json, pathlib, subprocess, sys, time

HERE = pathlib.Path(__file__).parent
STILLS = HERE / "stills"
CLIPS = HERE / "clips"
STATE = HERE / "_prompts" / "animate_state.json"
CLIPS.mkdir(exist_ok=True)
STATE.parent.mkdir(exist_ok=True)

ENV = pathlib.Path("/Users/brooksorradre2/Documents/marketing brain/.env")
KEY = [l.split("=", 1)[1].strip().strip('"').strip("'")
       for l in ENV.read_text().splitlines() if l.startswith("GEMINI_API_KEY=")][0]
BASE = "https://generativelanguage.googleapis.com/v1beta/interactions"

ANTI_ZOOM = (
    " CONSTANT DISTANCE. The camera may move, but it never gets closer to or further from the bag "
    "and the focal length never changes. There is NO push-in, NO dolly-in, NO zoom and NO move "
    "toward or away from the subject. The bag occupies exactly the same fraction of the frame at "
    "the last frame as it does at the first — it never grows, never gets closer and never fills "
    "more of the frame. All camera movement is SIDEWAYS or AROUND the subject at a fixed radius. "
    "Measure it this way: the bag is the same NUMBER OF PIXELS wide in the final frame as in the "
    "first frame. If an orbit or a drift would bring the camera even slightly nearer, pull the path "
    "outward to compensate so the distance is held exactly constant. Revealing a new angle must come "
    "from travelling AROUND the bag, never from approaching it."
)

# 2026-08-16, Brooks: "all of the B-roll is too monotone... there's no movement at all. The point
# is to show new visuals to keep the viewer engaged... regenerate it so the camera is moving
# throughout, showing off different product angles."
#
# He is right and this was my error. After the first library inflated the bag on every push-in I
# banned ALL camera movement, but the defect was the bag GROWING, not the camera moving. An arc or
# an orbit at a fixed radius reveals the side gusset, the depth and the hardware while the bag's
# size on screen never changes. Static B-roll is its own failure: a shot that does not move gives
# the viewer nothing new and they scroll.
MOVE_EXEMPT = {"B03-loadin"}

MOVE = (
    " The camera is HANDHELD and moving for the entire clip, never locked off and never still: a "
    "slow continuous move with the small natural wobble and breathing of a hand, plus a live "
    "parallax shift so nearer and further things slide past each other at different rates and new "
    "angles of the bag are revealed as it goes."
)

ANTI_MUTATE = (
    " The handbag's construction must not change: the leather flap keeps the exact shape and "
    "position it has in the first frame and never lifts, folds, rises, splits or moves; the two "
    "belt straps stay put and never merge; no new buckle, clasp, ring, zip, stud, logo or metal "
    "fitting ever appears; the gold fittings keep their exact shape and position. The bag's "
    "colours do not shift. No text or captions appear. Vertical 9:16."
)

# Keep the photographic character the v3 stills earned. Omni will otherwise smooth a
# real-looking frame into a clean render across the clip.
KEEP_REAL = (
    " This is real phone footage. Keep the existing grain, the slightly imperfect focus and the "
    "available-light look of the first frame all the way through. Do not brighten it, do not "
    "sharpen it, do not stabilise it into something glossy and do not make it look like a "
    "commercial."
)

# Every shot carries a constant-radius camera move so the library is never static.
SHOTS = {
    "B01-closet":
        "Animate this exact frame. Her hand lifts the handbag straight up off the shelf a few "
        "inches and holds it there. The shelf, the basket behind and the folded knitwear stay still. The camera arcs slowly to the LEFT around the bag at a fixed distance as her hand lifts it, so the front turns away and the deep side gusset comes into view.",
    "B02-flatlay":
        "Animate this exact frame. Her hand slides a few inches across "
        "the linen and comes to rest. The bag and every laid-out item stay exactly where they are. The camera slides slowly and steadily SIDEWAYS across the flat lay from left to right, staying at exactly the same height above the bed the whole way.",
    "B03-loadin":
        "Animate this exact frame. Her hand lowers the folded wallet the last inch down into the "
        "already-open mouth of the bag until it settles inside, then the hand withdraws out of the "
        "top of frame. The bag does not move at all. The flap stays folded back exactly as it is "
        "and NEVER rises, closes or changes angle. CAMERA LOCKED OFF. The camera does not move at all: no travel, no arc, no sway, no drift, no zoom. THIS SHOT IS THE ONE EXCEPTION to the moving-camera rule in this file, and the reason is specific: the open bag is the most fragile frame in the library and every camera move made the model redraw it, inventing a shoulder strap, a reshaped lid and a stamped logo plate. Only the hand moves. The bag keeps EXACTLY the construction it has in the first frame: no shoulder strap, no crossbody strap and no long strap of any kind ever appears on it, the flap stays folded back and never lifts or reshapes, and no new hardware appears.",
    "B04-standsquare":
        "Animate this exact frame. The bag stays put on the cafe table. Motion "
        "is a few autumn leaves drifting past in the blurred background, a passer-by crossing far "
        "behind, and a slight shift of warm light across the canvas. The camera SLIDES steadily sideways across the scene on a straight line, parallel to the table edge, never curving toward the bag and never approaching it. The angle on the bag changes through parallax alone as the camera passes.",
    "B05-walking":
        "Animate this exact frame. She continues walking at a steady pace and the camera PANS "
        "sideways to follow her, holding her at the same distance and the same size in frame "
        "throughout, the way someone filming while walking alongside would. The bag hangs from her "
        "hand and sways only slightly. No tripod, camera, crew or filming equipment ever appears in "
        "the shot. The camera tracks alongside her at walking pace, holding her at exactly the same distance and the same size in frame, the way someone filming while walking beside her would. No tripod, camera, crew or filming equipment ever appears.",
    "B06-elbow":
        "Animate this exact frame. She shifts her weight very slightly and the bag settles on her "
        "forearm. The coat sleeve shifts with her. The camera drifts slowly BACKWARD ALONG her side at a fixed distance from the bag, so the angle on it rotates from the front round toward the side gusset without ever getting closer.",
    "B07-buckle":
        "Animate this exact frame. The bag itself stays put; warm light shifts "
        "very slightly across the leather grain and the gold buckle. The camera slides slowly SIDEWAYS along the side gusset at macro distance, travelling across the leather strap and over the gold roller buckle, the focus riding along with it.",
    "B08-feet":
        "Animate this exact frame. The bag itself stays put. A dry leaf "
        "stirring slightly in a breath of wind. The bag does not move and the framing never widens. The camera slides slowly SIDEWAYS along the bottom edge at a fixed low height, passing one gold foot after another and along the leather corner patch.",
    "B09-bench":
        "Animate this exact frame. The bag stays put on the bench slats. Golden-hour "
        "light flickers gently through the trees behind and one leaf drifts down. The camera ORBITS slowly around the bag along the bench at a fixed radius, moving from the three-quarter front round toward the side so the depth of the bag and its gold side buckle come into view.",
    "B10-wall":
        "Animate this exact frame. She shifts her stance slightly and the bag sways a fraction at "
        "her side. Her sleeve shifts with her. The camera SLIDES steadily sideways on a straight line parallel to the wall, never curving toward her and never approaching. She turns the bag a little in her hand so its front rotates and the deep side face comes into view; the reveal comes from HER movement, not from the camera closing in.",
    "B11-carseat":
        "Animate this exact frame. The bag stays upright on the passenger seat and does "
        "not tip or slump. Dappled light moves across the canvas as if the car "
        "were parked under trees. The camera arcs slowly across the passenger seat at a fixed radius, revealing the side of the bag and the gold feet as the angle changes.",
    "B12-doorway":
        "Animate this exact frame. She takes one small step forward through the doorway, hands "
        "still full, the bag riding on her forearm. The camera follows her handheld through the doorway, keeping the same distance from the bag as she steps, so the angle on it swings round as she turns.",
}


def load_state():
    return json.loads(STATE.read_text()) if STATE.exists() else {}


def save_state(s):
    STATE.write_text(json.dumps(s, indent=1))


def curl_json(url, payload=None):
    if payload is not None:
        p = HERE / "_prompts" / ".payload.json"
        p.write_text(json.dumps(payload))
        cmd = ["curl", "-s", "-X", "POST", url, "-H", "Content-Type: application/json",
               "--data-binary", f"@{p}"]
    else:
        cmd = ["curl", "-s", url]
    out = subprocess.run(cmd, capture_output=True, text=True, timeout=300).stdout
    try:
        return json.loads(out)
    except Exception:
        return {"_raw": out[:400]}


def launch(only=None):
    state = load_state()
    for still in sorted(STILLS.glob("*.png")):
        key = still.stem                      # e.g. LC-B04-standsquare
        shot = key.split("-", 1)[1]           # e.g. B04-standsquare
        if only and not any(o in key for o in only):
            continue
        if shot not in SHOTS:
            print(f"no motion defined for {shot}, skipping {key}")
            continue
        if key in state or (CLIPS / f"{key}.mp4").exists():
            continue
        move = "" if shot in MOVE_EXEMPT else MOVE
        text = SHOTS[shot] + move + ANTI_ZOOM + ANTI_MUTATE + KEEP_REAL
        payload = {
            "model": "models/gemini-omni-flash-preview",
            "input": [
                {"type": "image", "data": base64.b64encode(still.read_bytes()).decode(),
                 "mime_type": "image/png"},
                {"type": "text", "text": text},
            ],
            "background": True,
            "generation_config": {"video_config": {}},
        }
        d = curl_json(f"{BASE}?key={KEY}", payload)
        if "id" in d:
            state[key] = d["id"]
            print(f"launched {key}", flush=True)
        else:
            print(f"FAILED  {key}: {json.dumps(d)[:200]}", flush=True)
        save_state(state)
        time.sleep(1)


def poll():
    state = load_state()
    done = pending = 0
    for key, iid in state.items():
        out = CLIPS / f"{key}.mp4"
        if out.exists() and out.stat().st_size > 100_000:
            done += 1
            continue
        d = curl_json(f"{BASE}/{iid}?key={KEY}")
        st = d.get("status")
        if st == "completed":
            vid = None
            for step in d.get("steps", []):
                for c in step.get("content", []):
                    if c.get("type") == "video":
                        vid = c.get("data")
            if vid:
                out.write_bytes(base64.b64decode(vid))
                print(f"landed {key} ({out.stat().st_size // 1024} KB)", flush=True)
                done += 1
            else:
                print(f"completed but no video: {key}")
        elif st in ("failed", "error"):
            print(f"FAILED {key}: {json.dumps(d)[:200]}")
        else:
            pending += 1
    print(f"{done} landed, {pending} pending")
    return pending


def qa():
    """First frame vs last frame, side by side, so scale drift is MEASURED not eyeballed.

    This is the check that a stills-only pass cannot do. Any clip whose bag is visibly
    larger on the right half is a reject and gets re-animated."""
    outdir = HERE / "_prompts" / "qa"
    outdir.mkdir(exist_ok=True)
    for clip in sorted(CLIPS.glob("*.mp4")):
        a, b = outdir / f"{clip.stem}_first.jpg", outdir / f"{clip.stem}_last.jpg"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(clip),
                        "-vf", "select=eq(n\\,0),scale=380:-1", "-vframes", "1", str(a)])
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-sseof", "-0.3", "-i", str(clip),
                        "-vf", "scale=380:-1", "-vframes", "1", str(b)])
    print(f"first/last frames in {outdir}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "poll"
    {"launch": lambda: launch(only=sys.argv[2:] or None),
     "poll": poll, "qa": qa}[cmd]()
