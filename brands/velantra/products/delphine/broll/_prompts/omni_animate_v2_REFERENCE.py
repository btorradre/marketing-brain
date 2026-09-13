#!/usr/bin/env python3
"""Delphine fall TOF — animate QA'd B-roll stills with Google Omni.

v2, 2026-08-15. THE LAW THIS VERSION EXISTS FOR:

  NEVER ask Omni for a push-in, dolly, zoom or "camera drifts toward" on a product shot.
  Every single push-in in v1 made the bag GROW across the clip — B11 started a small handbag
  and ended a weekender, B10/B04/B02/B09/B12 all inflated, B08 pulled out far enough to reveal
  the flap it was supposed to crop out. On a product whose entire claim is "it is small", a
  push-in silently destroys the mechanism.

  Camera is LOCKED OFF. Motion comes from the SUBJECT (a hand, her stride, leaves, light).
  Every prompt carries the ANTI_ZOOM clause below.
"""
import base64, json, pathlib, subprocess, sys, time

HERE = pathlib.Path(__file__).parent
PICKS = HERE / "picks"
CLIPS = HERE / "clips"
STATE = HERE / "omni_state_v2.json"
SCRATCH = pathlib.Path("/private/tmp/claude-503/-Users-brooksorradre2-Documents-marketing-brain/a99c500d-ccf1-4f2c-bb5f-934d9c973026/scratchpad")
CLIPS.mkdir(exist_ok=True)

ENV = pathlib.Path("/Users/brooksorradre2/Documents/marketing brain/.env")
KEY = [l.split("=", 1)[1].strip().strip('"').strip("'")
       for l in ENV.read_text().splitlines() if l.startswith("GEMINI_API_KEY=")][0]
BASE = "https://generativelanguage.googleapis.com/v1beta/interactions"

ANTI_ZOOM = (
    "CAMERA IS COMPLETELY LOCKED OFF on a tripod. There is NO push-in, NO dolly, NO zoom, NO "
    "camera move toward or away from the subject, and NO change of focal length. The framing at "
    "the last frame is IDENTICAL to the framing at the first frame. The handbag must occupy "
    "exactly the same fraction of the frame at the end as it does at the start — it must never "
    "grow, never get closer, never fill more of the frame. If nothing else moves, the shot is "
    "simply held still."
)

ANTI_MUTATE = (
    "The handbag's construction must not change: the leather flap keeps the exact shape and "
    "position it has in the first frame and never lifts, folds, rises, splits or moves; the two "
    "belt straps stay put and never merge; no new buckle, clasp, ring, zip, stud, logo or metal "
    "fitting ever appears; the gold fittings keep their exact shape and position. "
    "No text or captions appear. Vertical 9:16."
)

# Motion is SUBJECT-ONLY. No camera moves anywhere in this file.
SHOTS = {
    "B01-closet":      "Animate this exact frame. Her hand lifts the handbag straight up off the shelf a few inches and holds it there. The shelf, the straw tote behind and the folded knitwear stay still. ",
    "B02-flatlay":     "Animate this exact frame. Nothing moves except her hand, which slides a few inches across the linen and comes to rest. The bag and every laid-out item stay exactly where they are. ",
    "B03-loadin":      "Animate this exact frame. Her right hand lowers the tortoiseshell sunglasses case the last inch down into the already-open mouth of the bag until it settles inside, then the hand withdraws out of the top of frame. The bag does not move at all. The flap stays folded back exactly as it is and NEVER rises, closes or changes angle. ",
    "B04-standsquare": "Animate this exact frame. The bag sits completely still on the marble table. The only motion is a few autumn leaves drifting past in the blurred background and a slight shift of warm light across the canvas. The espresso cup stays exactly where it is. ",
    "B05-walking":     "Animate this exact frame. She continues walking at a steady pace and the camera holds its position, so she travels across the frame. The bag hangs from her hand and sways only slightly. ",
    "B06-elbow":       "Animate this exact frame. She shifts her weight very slightly and the bag settles on her forearm. Almost nothing else moves. ",
    "B07-buckle":      "Animate this exact frame. Absolutely still macro. The only change is warm light shifting very slightly across the leather grain and the gold buckle. ",
    "B08-feet":        "Animate this exact frame. Absolutely still low macro. The only motion is the dry leaf stirring slightly in a breath of wind. The bag does not move and the framing never widens. ",
    "B09-bench":       "Animate this exact frame. The bag stays perfectly still on the bench slats. Golden-hour light flickers gently through the trees behind and one leaf drifts down. ",
    "B10-wall":        "Animate this exact frame. She shifts her stance slightly and the bag sways a fraction at her side. Nothing else moves. ",
    "B11-carseat":     "Animate this exact frame. The bag sits still and upright on the passenger seat and does not tip or slump. The only motion is dappled light moving across the canvas as if the car were parked under trees. ",
    "B12-doorway":     "Animate this exact frame. She takes one small step forward through the doorway, hands still full, the bag riding on her forearm. ",
    "B13-strawhook":   "Animate this exact frame. The straw tote hangs still on its hook. Light shifts gently through the window behind it and one leaf falls outside. No text or captions appear. Vertical 9:16. " + ANTI_ZOOM,
}


def load_state():
    return json.loads(STATE.read_text()) if STATE.exists() else {}


def save_state(s):
    STATE.write_text(json.dumps(s, indent=1))


def curl_json(url, payload=None):
    p = SCRATCH / "omni_payload.json"
    if payload is not None:
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
    for name, motion in SHOTS.items():
        if only and name not in only:
            continue
        for cw in ("LC", "DC", "AG"):
            key = f"{cw}-{name}"
            still = PICKS / f"{key}.png"
            if not still.exists() or key in state:
                continue
            text = motion + ANTI_ZOOM + " " + ANTI_MUTATE
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
                print(f"launched {key}")
            else:
                print(f"FAILED  {key}: {json.dumps(d)[:200]}")
            save_state(state)
            time.sleep(1)


def poll():
    state = load_state()
    done = pending = 0
    for key, iid in state.items():
        out = CLIPS / f"{key}.mp4"
        if out.exists() and out.stat().st_size > 100_000 and key in load_state():
            pass
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
                done += 1
            else:
                print(f"completed, no video: {key}")
        elif st in ("failed", "error"):
            print(f"FAILED {key}: {json.dumps(d)[:200]}")
        else:
            pending += 1
    print(f"{done} landed, {pending} pending")
    return pending


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "poll"
    if cmd == "launch":
        launch(only=sys.argv[2:] or None)
    else:
        poll()
