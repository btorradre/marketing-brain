#!/usr/bin/env python3
"""Animate the Vivienne organic b-roll keyframes via Google Omni (Interactions API).

Transport is curl: urllib fails SSL_CERTIFICATE_VERIFY_FAILED against
generativelanguage.googleapis.com on this machine (see reference_omni_interactions_api).

  python3 animate_omni.py run          # animate everything not yet done
  python3 animate_omni.py run O4 O5    # animate specific shots (re-roll)
  python3 animate_omni.py status
"""
import base64, json, os, subprocess, sys, tempfile, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
VAULT = Path("/Users/brooksorradre2/Documents/marketing brain")
SRC = HERE / "organic"
CLIPS = HERE / "clips"; CLIPS.mkdir(exist_ok=True)
STATE = HERE / "omni_state.json"
BASE = "https://generativelanguage.googleapis.com/v1beta/interactions"

def env():
    d = {}
    for line in (VAULT / ".env").read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1); d[k.strip()] = v.strip().strip('"').strip("'")
    return d
KEY = env()["GEMINI_API_KEY"]

# Construction lock pasted into every motion prompt. The bag must not re-synthesize.
LOCK = ("The bag itself does not change in any way: its shape, its soft slumped body, its matte "
        "grain leather, its colour, its contrasting cognac belt straps, its gold oval plate with "
        "the empty keyhole cutout, its knurled brass post, its two flat gold staples, its braided "
        "trim, its leather key bell and its corner caps all stay exactly as they are in the still. "
        "The flap stays CLOSED for the entire clip and the bag is never opened. No hardware is "
        "added, removed or reshaped. The cutouts in the flap stay dark and occluded and never "
        "become see-through. No lettering, engraving, stamp, logo or text ever appears on any "
        "metal or leather surface. ")
REAL = ("Keep it looking like the same real phone snapshot in motion: same grain, same ordinary "
        "light, same imperfect focus, same crooked framing. Do not clean it up, do not relight it, "
        "do not make it cinematic or advertorial. Vertical 9:16.")

MOTION = {
"O1":  "A locked-off phone shot, barely moving. The camera drifts a few centimetres closer over ten seconds with a small handheld wobble. Steam rises faintly from the coffee. Nothing else in the frame moves. ",
"O2":  "A hand closes around both rolled top handles and lifts the bag up off the bench, the soft body sagging and folding as it takes its own weight, then the bag swings slightly and steadies. The camera follows the lift a little, handheld. ",
"O3":  "A locked-off shot from the driver's seat. The car is stationary. Light shifts very slightly across the bag as if a cloud passes. The bag settles a fraction into the seat. Almost nothing moves. ",
"O4":  "Fingers press down into the soft leather of the bag, the leather visibly dimpling and creasing under the fingertips, then the hand lifts away and the leather slowly relaxes back. The camera stays overhead and still with a small handheld drift. ",
"O5":  "THE CAMERA DOES NOT MOVE AT ALL. It is locked off on a tripod at exactly the framing of the still, and it never pushes in, never pulls back, never reframes and never changes focal length. The ONLY movement in the entire clip is the thumb and forefinger rotating the gold oval plate a few degrees and then withdrawing. The plate rotates in place: it does not change shape, size, thickness or position, and its keyhole cutout stays an open dark hole throughout and never fills in. ",
"O6":  "A locked-off POV looking down. Her boots shift slightly as she settles her weight. The bag stays where it is on the floor. Faint daylight flicker from the window. Almost nothing moves. ",
"O7":  "Following her from behind as she walks out through the door, the bag swinging at her side with each stride, her arm moving naturally. The camera walks with her, handheld and bouncing slightly. ",
"O8":  "A locked-off shot. The camera drifts a few centimetres closer over ten seconds with a small handheld wobble. The bag settles a fraction into the soft bedding. Nothing else moves. ",
"O9":  "Following her from behind at hip height down the hallway, the bag swaying against her hip on its shoulder strap with each stride. The camera walks with her, handheld and bouncing slightly. ",
"O10": "THE CAMERA DOES NOT MOVE AT ALL. It is locked off at exactly the framing of the still and never pushes in, pulls back or reframes. The ONLY movement is her hand releasing the two top handles and withdrawing from frame, the handles tipping slightly sideways as she lets go. The bag stays in exactly the same place and keeps exactly the same shape and proportions. ",
"O11": "THE CAMERA DOES NOT MOVE AT ALL. It is locked off overhead at exactly the framing of the still and never pushes in, pulls back or reframes. NOTHING in the frame moves except an almost imperceptible handheld breathing of one or two pixels. The braided trim is stitched flat into the edge of the leather and stays part of it: it never lifts, never detaches, never becomes a separate cord, rope or strap lying on top of the bag. ",
"O12": "THE CAMERA DOES NOT MOVE AT ALL. It is locked off at exactly the framing of the still and never pushes in, pulls back or reframes. The bag stays hanging in exactly the same position on the chair back and the chair does not move. The ONLY change across the clip is a faint flicker in the lamp light. ",
}

def curl_json(url, payload=None, timeout=180):
    cmd = ["curl", "-sS", "-m", str(timeout), url]
    tmp = None
    if payload is not None:
        tmp = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
        json.dump(payload, tmp); tmp.close()
        cmd += ["-X", "POST", "-H", "Content-Type: application/json", "--data-binary", f"@{tmp.name}"]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError(f"curl failed: {r.stderr[-300:]}")
        return json.loads(r.stdout)
    finally:
        if tmp: os.unlink(tmp.name)

def to_jpeg_720(png_path):
    """Omni wants a 720x1280 JPEG image part."""
    from PIL import Image
    im = Image.open(png_path).convert("RGB").resize((720, 1280), Image.LANCZOS)
    out = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
    im.save(out.name, "JPEG", quality=92)
    return out.name

def submit(img_path, motion):
    jpg = to_jpeg_720(img_path)
    b64 = base64.b64encode(Path(jpg).read_bytes()).decode()
    os.unlink(jpg)
    payload = {
        "model": "models/gemini-omni-flash-preview",
        "input": [
            {"type": "image", "data": b64, "mime_type": "image/jpeg"},
            {"type": "text", "text": motion},
        ],
        "background": True,
        "generation_config": {"video_config": {}},
    }
    d = curl_json(f"{BASE}?key={KEY}", payload)
    if "id" not in d:
        raise RuntimeError(f"no id: {json.dumps(d)[:300]}")
    return d["id"]

def poll(iid, timeout_s=900):
    t0 = time.time()
    while time.time() - t0 < timeout_s:
        d = curl_json(f"{BASE}/{iid}?key={KEY}")
        st = d.get("status")
        if st == "completed":
            for step in d.get("steps", []):
                for c in step.get("content", []):
                    if c.get("type") == "video" and c.get("data"):
                        return base64.b64decode(c["data"])
            raise RuntimeError("completed, no video part")
        if st in ("failed", "cancelled", "error"):
            raise RuntimeError(f"{st}: {json.dumps(d)[:300]}")
        time.sleep(12)
    raise TimeoutError(iid)

def main():
    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    args = sys.argv[1:]
    if args and args[0] == "status":
        for k in sorted(MOTION):
            p = CLIPS / f"{k}.mp4"
            print(f"  {k}: {'OK ' + str(round(p.stat().st_size/1e6,1)) + 'MB' if p.exists() else state.get(k,'pending')}")
        return
    only = [a for a in args[1:]] if args and args[0] == "run" else []
    todo = only or sorted(MOTION)
    for sid in todo:
        out = CLIPS / f"{sid}.mp4"
        if out.exists() and sid not in only:
            print(f"  {sid}: already done, skip"); continue
        src = SRC / next(p.name for p in SRC.glob(f"{sid}-*.png"))
        motion = MOTION[sid] + LOCK + REAL
        try:
            print(f"  {sid}: submitting...", flush=True)
            iid = submit(src, motion)
            data = poll(iid)
            out.write_bytes(data)
            state[sid] = "ok"
            print(f"  {sid}: OK {round(len(data)/1e6,1)}MB", flush=True)
        except Exception as e:
            state[sid] = f"ERROR {e}"
            print(f"  {sid}: FAIL {str(e)[:180]}", flush=True)
        STATE.write_text(json.dumps(state, indent=1))

if __name__ == "__main__":
    main()
