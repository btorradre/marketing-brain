#!/usr/bin/env python3
"""DC-02 S2 keyframe: closed cream Weekender + Blair, scale-anchored. 3 variants, kie GPT Image 2 i2i."""
import json, os, subprocess, time, urllib.request, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
VAULT = "/Users/brooksorradre2/Documents/marketing brain"
REFS = pathlib.Path(VAULT) / "brands/velantra/products/weekender/product-references/real-product-2026-08-08"
BLAIR = os.path.join(VAULT, "brands/velantra/_shared/ugc-creators/Blair/blair-ref.png")

KEY = None
for line in open(os.path.join(VAULT, ".env")):
    if line.startswith("KIE_API_KEY="):
        KEY = line.split("=", 1)[1].strip()
assert KEY
KIE_API = "https://api.kie.ai/api/v1"
KIE_UPLOAD = "https://kieai.redpandaai.co/api/file-stream-upload"

PREAMBLE = (
    "Use the first attached photo ONLY as the reference for the bag's shape, proportions, materials, colours, "
    "stitching and hardware, and the second attached photo ONLY as the reference for the woman's identity, face "
    "and hair. Do NOT copy either photo's lighting, background, framing or polished look. Create a new photograph. "
)

SCENE = (
    "Create a photograph from a phone on a tripod at table height: a large closed two tone weekend bag stands on "
    "a light oak table with its front face square to the lens, and a woman stands at the right edge of frame "
    "turned toward the bag in profile with an easy admiring smile, her right hand resting flat on the table "
    "beside the bag, never touching the bag, her left hand tucked at her waist. She is 42 years old with "
    "voluminous golden blonde hair in soft waves, light natural makeup, natural skin texture with visible pores, "
    "a few flyaway hairs, small gold huggie hoop earrings, wearing an oat cream linen shirt jacket with dark "
    "buttons over a crisp white button down shirt. Soft warm daylight from a tall window on the left, warm beige "
    "plaster wall softly out of focus behind. Nothing else on the table. "
)

SCALE = (
    "SCALE IS CRITICAL. This is a LARGE TRAVEL BAG, 18 inches wide by 14.5 inches tall by 7 inches deep, big "
    "enough to pack two to three days of clothes. It is NOT a handbag, NOT a purse, NOT a medium tote. Roughly "
    "the size of a carry-on duffel. Render it noticeably oversized rather than too small. The bag fills most of "
    "the frame's width and dominates the tabletop; the woman's hand resting flat on the table beside it looks "
    "small, spanning less than a third of the bag's width. "
)

IDENTITY = (
    "The bag: a structured two tone weekend bag, wider than tall, rich cognac brown leather upper flap section "
    "and two rolled cognac leather top handles over a cream ivory woven canvas body, a small gold oval turn lock "
    "on the front, two flat gold clasp plates with cognac leather belt straps threaded through them, a small "
    "cognac leather key bell tied to the handle base, cognac leather corner patches at the bottom, a small gold "
    "eyelet high on each side face, visible stitching, gold hardware, no logos anywhere on the bag. "
)

HARDWARE = (
    "Front closure hardware, exactly as on the reference photo: at the front center of the leather band stands a "
    "small gold turn post with a round knurled mushroom shaped head. The flap's center tab carries a polished gold "
    "oval plate with a shaped keyhole cutout in its middle, and when the flap is down this tab rests over the post "
    "so the gold post head shows through the cutout. To the left and right, two flat vertical gold staples stand "
    "on the leather band; when the flap is down its two small oval slots sit over these staples so the staples "
    "poke through. The two cognac leather belt straps come over the top from the back of the bag, and each strap "
    "tip carries a flat gold rounded rectangular end plate with an oblong slot and small dome rivets, which hooks "
    "over its staple. Each staple is TWO PARALLEL FLAT GOLD BARS side by side, never one solid blade and never a "
    "buckle. The knurled mushroom post appears ONCE, at the front centre of the band; never render both a post "
    "through the plate and a second post below the flap edge. The oval plate itself is FLAT and flush against the "
    "leather with a smooth polished face and an EMPTY cross shaped keyhole cutout punched through it, flanked by "
    "two TINY PLAIN SMOOTH DOME RIVETS sitting almost flush: no barrel, no cylinder, no knurled drum, no turning "
    "bar or toggle standing proud of the plate face, and the rivets are never slotted screws. The handles pass "
    "through keyhole shaped cutouts in the flap with stitched edges. All hardware is the same warm brass gold, "
    "both sides identical, no silver, no chrome. BOTH clasp plates are the SAME warm brass gold, the RIGHT plate "
    "identical in color to the LEFT plate. "
)

FOOTER = (
    "CRITICAL RENDERING INSTRUCTION. This is a real photograph casually taken on an iPhone 15 Pro by an ordinary "
    "person, handheld, in one second, with no lighting equipment, no tripod and no styling. It is NOT a 3D "
    "render, NOT CGI, NOT a product visualisation, NOT Blender or Octane or Unreal or Keyshot, NOT ray traced, "
    "NOT a commercial or catalogue product photograph, NOT an advertisement, NOT retouched, NOT airbrushed, NOT "
    "studio lit. If it looks polished or computer generated it is wrong. Photographic evidence that must be "
    "present: visible digital sensor noise and grain through the shadows and midtones, highlights slightly blown "
    "out where the light source hits, mild chromatic aberration on high contrast edges, faint JPEG compression "
    "artefacts, focus that is slightly imperfect so nothing is tack sharp, a trace of handheld motion blur, and "
    "framing that is a little crooked and off centre the way a real snapshot is. Real light only: one dominant "
    "available light source, mixed colour temperature across the frame, uneven exposure, and real shadows "
    "falling off naturally with visible ambient bounce. Real surfaces: the leather is creased, faintly scuffed, "
    "unevenly grained and dulled where it has been handled, never a uniform polished finish; the canvas shows "
    "individual woven fibres, slubs and small wrinkles; ordinary dust, lint and fingerprints are present. No "
    "on-screen text, lettering, signage or graphics anywhere. Vertical 9:16."
)

PROMPT = " ".join([PREAMBLE, SCENE, SCALE, IDENTITY, HARDWARE, FOOTER])

state_path = ROOT / "_s2_state.json"
state = json.loads(state_path.read_text()) if state_path.exists() else {"uploads": {}, "tasks": {}}
def save(): state_path.write_text(json.dumps(state, indent=1))

def api(path, payload=None):
    req = urllib.request.Request(KIE_API + "/" + path,
        headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"})
    if payload is not None:
        req.data = json.dumps(payload).encode()
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.loads(r.read().decode(), strict=False)

def upload(path):
    if path in state["uploads"]:
        return state["uploads"][path]
    for attempt in range(4):
        out = subprocess.run(["curl", "-s", "-X", "POST", KIE_UPLOAD,
             "-H", "Authorization: Bearer " + KEY, "-F", "file=@" + path,
             "-F", "uploadPath=images/velantra-dc02",
             "-F", "fileName=%d-%s" % (int(time.time()), os.path.basename(path).replace(" ", "_"))],
            capture_output=True, text=True)
        try:
            url = json.loads(out.stdout).get("data", {}).get("downloadUrl")
        except ValueError:
            url = None
        if url:
            state["uploads"][path] = url; save()
            print("[upload]", os.path.basename(path), flush=True)
            return url
        time.sleep(5)
    raise SystemExit("upload failed: " + path)

urls = [upload(str(REFS / "LC-closed-front-unfastened.jpg")), upload(BLAIR)]

for v in (1, 2, 3):
    key = "s2v%d" % v
    tid = state["tasks"].get(key)
    if not tid:
        for attempt in range(6):
            try:
                r = api("jobs/createTask", {"model": "gpt-image-2-image-to-image", "input": {
                    "prompt": PROMPT, "input_urls": urls, "aspect_ratio": "9:16", "resolution": "2K"}})
                tid = r.get("data", {}).get("taskId")
                if tid:
                    state["tasks"][key] = tid; save()
                    print("[%s] task %s" % (key, tid), flush=True)
                    break
                print("[%s] no taskId: %s" % (key, str(r)[:200]), flush=True)
            except Exception as e:
                print("[%s] create attempt %d: %s" % (key, attempt, e), flush=True)
            time.sleep(8)
    if not tid:
        continue
    for _ in range(120):
        try:
            r = api("jobs/recordInfo?taskId=" + tid)
            st = r.get("data", {}).get("state")
            if st == "success":
                u = json.loads(r["data"]["resultJson"], strict=False).get("resultUrls", [None])[0]
                dest = ROOT / ("s2_keyframe_v%d.png" % v)
                subprocess.run(["curl", "-sf", "-A", "Mozilla/5.0", "-o", str(dest), u], check=True, timeout=240)
                print("[%s] saved %d bytes" % (key, dest.stat().st_size), flush=True)
                break
            if st == "fail":
                print("[%s] FAILED: %s" % (key, r["data"].get("failMsg")), flush=True)
                state["tasks"].pop(key, None); save()
                break
        except Exception as e:
            print("[%s] poll err: %s" % (key, e), flush=True)
        time.sleep(10)
print("done")
