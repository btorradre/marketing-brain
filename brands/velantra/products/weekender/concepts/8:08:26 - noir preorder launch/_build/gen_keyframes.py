#!/usr/bin/env python3
"""NOIR b-roll keyframes: kie GPT Image 2 i2i off the QA-passed NOIR picks. 3 variants/scene."""
import json, os, subprocess, sys, time, urllib.request, pathlib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from noir_blocks import (IDENTITY, HARDWARE, MECHANISM, SCALE, PREAMBLE, HARDEN, FOOTER_9x16)

OUT = HERE.parent / "broll-keyframes"
OUT.mkdir(exist_ok=True)
VAULT = "/Users/brooksorradre2/Documents/marketing brain"
PICKS = pathlib.Path(VAULT) / "brands/velantra/products/weekender/concepts/8:08:26 - all black leather concept/picks"

KEY = None
for line in open(os.path.join(VAULT, ".env")):
    if line.startswith("KIE_API_KEY="):
        KEY = line.split("=", 1)[1].strip()
assert KEY

KIE_API = "https://api.kie.ai/api/v1"
KIE_UPLOAD = "https://kieai.redpandaai.co/api/file-stream-upload"

CLOSED = str(PICKS / "NOIR-01-hero-front-closed.png")
THREEQ = str(PICKS / "NOIR-02-three-quarter.png")
MACRO = str(PICKS / "NOIR-03-hardware-macro.png")
OPEN = str(PICKS / "NOIR-04-open-caramel-interior.png")
CARRY = str(PICKS / "NOIR-05-carry-scale.png")

# state: kind "omni" = animated by Google Omni; "kenburns" = macro, push-in only (macro-mutation law)
SCENES = [
    dict(id="NB-01-entryway-floor", kind="omni", refs=[CLOSED],
         scene="Create a photograph of the all black bag standing on the floor of a real apartment entryway, just "
               "inside the front door, with a wool coat hanging on a hook above it and a pair of boots beside it. "
               "Morning light comes through the door glass from the left.",
         motion="Slow steady push in toward the bag on the entryway floor. Nothing else in the scene moves. The bag "
                "stays completely still and does not change shape.",
         extra=[HARDWARE]),
    dict(id="NB-02-bed-open-packed", kind="omni", refs=[OPEN],
         scene="Create a photograph of the all black bag sitting open on an unmade linen bed, shot from the front "
               "and slightly above so the open mouth and the caramel tan leather interior are clearly visible. A "
               "folded knit sweater and a rolled pair of jeans sit inside. Soft window light from the right.",
         motion="Very slow push in toward the open mouth of the bag so the caramel interior fills more of the frame. "
                "The bag does not move and its construction does not change.",
         extra=[MECHANISM]),
    dict(id="NB-03-hotel-rack", kind="omni", refs=[CLOSED, THREEQ],
         scene="Create a photograph of the all black bag resting closed on a wooden hotel luggage rack at the foot "
               "of a made bed, shot from a low three quarter angle. Warm lamp light from the right, curtains behind.",
         motion="Slow drift of the camera to the right around the bag, keeping the bag centred. The bag itself stays "
                "perfectly still and its hardware does not change shape.",
         extra=[HARDWARE]),
    dict(id="NB-04-carry-hallway", kind="omni", refs=[CARRY],
         scene="Create a candid photograph of a woman in her early thirties in a black wool coat and jeans walking "
               "along an apartment hallway, carrying the all black bag by both rolled top handles in one hand at "
               "her side. Her face is cropped out at the top of frame. The bag reaches from her hip toward her knee.",
         motion="She walks slowly forward along the hallway, the bag swinging gently at her side. Handheld camera "
                "follows at the same pace. Her hand stays on the handles and never touches the front hardware.",
         extra=[]),
    dict(id="NB-05-car-seat", kind="omni", refs=[CLOSED],
         scene="Create a photograph of the all black bag sitting on the passenger seat of a car, shot from the "
               "driver's side. Late afternoon sun comes through the window and falls across the leather. Seatbelt "
               "and door trim visible.",
         motion="The camera holds nearly still with a faint handheld drift while the light shifts slowly across the "
                "leather as the car moves. The bag stays completely still.",
         extra=[HARDWARE]),
    dict(id="NB-06-kitchen-counter", kind="omni", refs=[CLOSED, THREEQ],
         scene="Create a photograph of the all black bag set down on a kitchen counter beside a half full mug of "
               "coffee and a set of keys, in a real lived in kitchen. Morning light from a window behind.",
         motion="Slow push in past the mug toward the bag. The bag stays still and does not change shape.",
         extra=[HARDWARE]),
    dict(id="NB-07-packing-hands", kind="omni", refs=[OPEN],
         scene="Create a photograph of a woman's hands lowering a folded cream knit sweater into the open all black "
               "bag, which sits open on a bed. The caramel tan leather interior is clearly visible around the "
               "sweater. Her face is not in frame. Soft daylight.",
         motion="Her hands lower the folded sweater down into the open bag and let go, then withdraw from frame. The "
                "bag itself does not move and its construction does not change. Her hands never touch the front "
                "hardware, the flap or the belt straps.",
         extra=[MECHANISM]),
    dict(id="NB-08-doorway-pickup", kind="omni", refs=[CLOSED, CARRY],
         scene="Create a photograph of a woman's hand reaching down and closing around both rolled top handles of "
               "the all black bag where it stands on the floor by an open front door. Only her forearm and hand are "
               "in frame. Daylight from the doorway.",
         motion="Her hand closes on the two rolled handles and lifts the bag smoothly straight up out of frame. Her "
                "hand only ever touches the rolled handles, never the flap, never the belt straps and never the "
                "gold hardware. The bag keeps its exact shape as it lifts.",
         extra=[]),
    dict(id="NB-09-airport-bench", kind="omni", refs=[CLOSED, THREEQ],
         scene="Create a photograph of the all black bag sitting on a bench in an airport departure area beside a "
               "woman's legs in jeans and black boots. Big windows and grey daylight behind, other travellers "
               "blurred in the distance.",
         motion="The camera holds with a faint handheld sway while blurred travellers pass in the far background. "
                "The bag stays completely still.",
         extra=[]),
    dict(id="NB-10-closet-shelf", kind="omni", refs=[CLOSED],
         scene="Create a photograph of the all black bag sitting on a closet shelf beside neat stacks of folded "
               "clothes, with hanging garments below. Warm closet light from one side.",
         motion="Very slow push in toward the bag on the shelf. Nothing in the scene moves.",
         extra=[HARDWARE]),
    dict(id="NB-11-nightstand-lamp", kind="omni", refs=[CLOSED, THREEQ],
         scene="Create a photograph of the all black bag standing on the floor beside a bed and a nightstand in the "
               "evening, lit only by a warm bedside lamp. The gold hardware catches the lamp light against the "
               "black leather.",
         motion="Slow push in toward the bag in the lamp light. Nothing moves and the hardware does not change shape.",
         extra=[HARDWARE]),
    dict(id="NB-12-stairs-descend", kind="omni", refs=[CARRY],
         scene="Create a candid photograph from below of a woman in a black coat carrying the all black bag by its "
               "handles as she comes down a set of apartment stairs. Her face is cropped out at the top of frame. "
               "Daylight from a landing window.",
         motion="She walks down the stairs toward the camera, the bag held at her side. Handheld camera holds "
                "position. Her hand stays on the handles.",
         extra=[]),
    # ---- macro: Ken Burns only, never handed to an i2v engine (macro-mutation law) ----
    dict(id="NB-13-macro-turnlock", kind="kenburns", refs=[MACRO, CLOSED],
         scene="Create a tight macro photograph of the front closure hardware on the all black bag, shot close and "
               "slightly from above with shallow depth of field so the gold catches a hard specular highlight "
               "against the black leather. The black leather grain, pores and tonal topstitching fill the frame.",
         motion=None, extra=[HARDWARE]),
    dict(id="NB-14-macro-interior", kind="kenburns", refs=[OPEN],
         scene="Create a macro photograph looking down into the open all black bag at the caramel tan leather "
               "interior lining and the wide matching caramel slip pocket on the interior wall, with the black "
               "leather mouth of the bag framing the top of the shot. Soft daylight falling into the bag.",
         motion=None, extra=[MECHANISM]),
    dict(id="NB-15-macro-gusset-eyelet", kind="kenburns", refs=[THREEQ, CLOSED],
         scene="Create a macro photograph of the side face of the all black bag, showing the small gold eyelet high "
               "near the gusset edge, the deep side gusset and the tonal black topstitching running down the seam. "
               "Raking side light picks out the leather grain.",
         motion=None, extra=[]),
]


def api(path, payload=None):
    req = urllib.request.Request(KIE_API + "/" + path,
                                 headers={"Authorization": "Bearer " + KEY,
                                          "Content-Type": "application/json"})
    if payload is not None:
        req.data = json.dumps(payload).encode()
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.loads(r.read().decode(), strict=False)


state_path = OUT / "_state.json"
state = json.loads(state_path.read_text()) if state_path.exists() else {"uploads": {}, "tasks": {}}
save = lambda: state_path.write_text(json.dumps(state, indent=1))


def upload(path):
    if path in state["uploads"]:
        return state["uploads"][path]
    for _ in range(4):
        out = subprocess.run(
            ["curl", "-s", "-X", "POST", KIE_UPLOAD, "-H", "Authorization: Bearer " + KEY,
             "-F", "file=@" + path, "-F", "uploadPath=images/velantra-weekender-noir-broll",
             "-F", "fileName=%d-%s" % (int(time.time()), os.path.basename(path).replace(" ", "_"))],
            capture_output=True, text=True)
        try:
            url = json.loads(out.stdout).get("data", {}).get("downloadUrl")
        except ValueError:
            url = None
        if url:
            state["uploads"][path] = url
            save()
            print("[upload] " + os.path.basename(path), flush=True)
            return url
        time.sleep(6)
    raise SystemExit("upload failed: " + path)


def build_prompt(s):
    return " ".join(p.strip() for p in
                    [PREAMBLE, s["scene"], SCALE, IDENTITY] + s["extra"] + [HARDEN, FOOTER_9x16])


def create(key, prompt, urls):
    if key in state["tasks"]:
        return state["tasks"][key]
    for attempt in range(6):
        try:
            r = api("jobs/createTask", {"model": "gpt-image-2-image-to-image", "input": {
                "prompt": prompt, "input_urls": urls, "aspect_ratio": "9:16", "resolution": "2K"}})
            tid = r.get("data", {}).get("taskId")
            if tid:
                state["tasks"][key] = tid
                save()
                print("[%s] task %s" % (key, tid), flush=True)
                return tid
            print("[%s] no taskId: %s" % (key, str(r)[:160]), flush=True)
        except Exception as e:
            print("[%s] create %d: %s" % (key, attempt, e), flush=True)
        time.sleep(8)
    return None


def poll(key, tid):
    for _ in range(150):
        try:
            r = api("jobs/recordInfo?taskId=" + tid)
            st = r.get("data", {}).get("state")
            if st == "success":
                return json.loads(r["data"]["resultJson"], strict=False).get("resultUrls", [None])[0]
            if st == "fail":
                print("[%s] FAILED %s" % (key, r["data"].get("failMsg")), flush=True)
                state["tasks"].pop(key, None)
                save()
                return None
        except Exception as e:
            print("[%s] poll: %s" % (key, e), flush=True)
        time.sleep(10)
    return None


if __name__ == "__main__":
    for s in SCENES:
        d = OUT / s["id"]
        d.mkdir(exist_ok=True)
        urls = [upload(p) for p in s["refs"]]
        prompt = build_prompt(s)
        (d / "prompt.txt").write_text(prompt)
        if s["motion"]:
            (d / "motion.txt").write_text(s["motion"])
        for v in (1, 2, 3):
            key = "%s-v%d" % (s["id"], v)
            if (d / ("v%d.png" % v)).exists():
                continue
            tid = create(key, prompt, urls)
            if not tid:
                continue
            u = poll(key, tid)
            if u:
                subprocess.run(["curl", "-sf", "-A", "Mozilla/5.0", "-o", str(d / ("v%d.png" % v)), u],
                               timeout=240)
                print("[%s] saved" % key, flush=True)
    print("DONE", flush=True)
