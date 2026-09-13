#!/usr/bin/env python3
"""Delphine fall TOF — B-roll library v3. REGENERATE EVERY STILL, iPhone-real.

WHY THIS EXISTS
---------------
2026-08-16, Brooks on the v1/v2 library: "all the B-roll clips look very AI-generated.
They have that 3D model kind of look. I want you to go regenerate them for me so every
shot looks like it's actually shot on an iPhone. It was filmed for a B-roll library,
getting ready to post on TikTok."

Confirmed on inspection. LC-B04-standsquare and LC-B09-bench are textbook CGI: dead-
centre framing, uniform polished leather with no creasing or scuffs, immaculate
surfaces, tack-sharp everywhere, no sensor noise, an over-warm even grade and no blown
highlights. They read as product visualisations, not photographs.

This is the GLOBAL LAW in feedback_no_3d_render_look: a 3D-model-looking frame is a
hard regenerate, never a ship-it-anyway. That memory also names the two causes, and
BOTH are fixed here:

  1. The old negative was weak. "No studio lighting" never tells a model not to make
     CGI. The footer below names what to REFUSE (render engines by name, ray tracing,
     catalogue photography, retouching) and what photographic EVIDENCE must be present
     (sensor noise, blown highlights, chromatic aberration, JPEG artefacts, imperfect
     focus, handheld blur, crooked framing, creased leather, dust, fingerprints).
  2. THE i2i REFERENCE IS THE REAL CULPRIT. The real-product files are clean supplier
     packshots on grey and i2i inherits their rendering aesthetic wholesale. Every
     prompt therefore OPENS by stating the attachment supplies geometry and materials
     ONLY -- never its lighting, background, clean edges or product-photo look.

Also carried: THREE VARIANTS PER SCENE, then pick (same memory, standing rule). Never
ship a first roll. Rejects stay on disk beside the pick so the choice is auditable.

Product truth is anchored on the REAL 25 cm photography in `products/delphine/
real-product/`, never the 46 cm Eleanor stills (PRODUCT-TRUTH.md 2b).

Transport is curl, not urllib: this machine has no cert bundle for urllib and every
call to api.kie.ai dies on CERTIFICATE_VERIFY_FAILED
(project_delphine_vestirsi_statics).

Idempotent: skips any variant whose PNG already exists.
"""
import json, os, subprocess, time

ROOT = os.path.dirname(os.path.abspath(__file__))
VAULT = "/Users/brooksorradre2/Documents/marketing brain"
REAL = os.path.join(VAULT, "brands/velantra/products/delphine/real-product")
OUT = os.path.join(ROOT, "v3", "raw")
API = "https://api.kie.ai/api/v1"
UPLOAD = "https://kieai.redpandaai.co/api/file-stream-upload"
VARIANTS = 3
ATTEMPTS = 5

KEY = None
with open(os.path.join(VAULT, ".env")) as f:
    for line in f:
        if line.startswith("KIE_API_KEY="):
            KEY = line.split("=", 1)[1].strip()
assert KEY, "KIE_API_KEY not found"
H = {"Authorization": f"Bearer {KEY}"}


# --- THE REFERENCE-ANCHORING PREAMBLE ----------------------------------------
# Verbatim from the velantra-weekender skill's VERBATIM PHOTOREAL BLOCK. This is
# cause #2 above and it goes at the TOP of every prompt, before anything else.

PREAMBLE = (
    "Use the attached photo ONLY as the reference for the bag's shape, proportions, materials, "
    "colours, stitching and hardware. Do NOT copy its lighting, its plain background, its clean "
    "edges or its polished studio product-photo look. That attachment is a catalogue image and the "
    "picture you produce must not resemble one. Create the following completely new photograph."
)

# --- THE ANTI-CGI FOOTER ------------------------------------------------------
# Verbatim from the same block. This REPLACES the retired wording entirely; the old
# "raw unedited iPhone photo, available light only, no studio lighting" line failed
# silently and is banned.

FOOTER = (
    "CRITICAL RENDERING INSTRUCTION. This is a real photograph casually taken on an iPhone 15 Pro "
    "by an ordinary person, handheld, in one second, with no lighting equipment, no tripod and no "
    "styling. It is NOT a 3D render, NOT CGI, NOT a product visualisation, NOT Blender or Octane or "
    "Unreal or Keyshot, NOT ray traced, NOT a commercial or catalogue product photograph, NOT an "
    "advertisement, NOT retouched, NOT airbrushed, NOT studio lit. If it looks polished or computer "
    "generated it is wrong. Photographic evidence that must be present: visible digital sensor noise "
    "and grain through the shadows and midtones, highlights slightly blown out where the light "
    "source hits, mild chromatic aberration on high contrast edges, faint JPEG compression "
    "artefacts, focus that is slightly imperfect so nothing is tack sharp, a trace of handheld "
    "motion blur, and framing that is a little crooked and off centre the way a real snapshot is. "
    "Real light only: one dominant available light source, mixed colour temperature across the "
    "frame, uneven exposure, and real shadows falling off naturally with visible ambient bounce. "
    "Real surfaces: the leather is creased, faintly scuffed, unevenly grained and dulled where it "
    "has been handled, never a uniform polished finish; the canvas shows individual woven fibres, "
    "slubs and small wrinkles; ordinary dust, lint and fingerprints are present. The setting is a "
    "real lived-in place with ordinary clutter, not a set. No on-screen text, lettering, signage or "
    "graphics anywhere. Vertical 9:16."
)

# --- OPTICS / "GOUACHE AND BLUR" -------------------------------------------------
# 2026-08-16, Brooks, after v3 round 1 STILL read as 3D: "There should be a slight
# gouache and blur to the image... You still look native, like it was shot on an iPhone."
#
# Diagnosed on LC-B04: the frame was uniformly, unnaturally sharp from the foreground
# table scratches all the way to the people down the street, with cranked micro-contrast
# on every surface and no haze anywhere. That edge-to-edge crispness IS the render tell —
# it is the one thing a real phone photo never does. The anti-CGI footer alone does not
# fix it because "photorealistic" pushes the model toward MORE detail, not less.
OPTICS = (
    "OPTICS, and this matters as much as anything else. Shot at a wide aperture on a phone: only a "
    "shallow slice of the subject is genuinely in focus, and everything in front of and behind that "
    "plane falls away into soft natural blur, with the background thrown well out of focus into "
    "soft undefined shapes. The corners and edges of the frame are visibly softer than the centre. "
    "There is a faint veiling haze over the picture and a gentle bloom around the bright areas, so "
    "highlights glow a little and bleed into whatever is next to them instead of stopping at a hard "
    "edge. Overall micro-contrast is LOW and slightly milky: fine surface detail is muted and soft "
    "rather than crisply resolved, the blacks are lifted and a touch hazy, and the whole image has a "
    "gentle diffused quality as though there were a little haze in the air. Nothing is crisply sharp "
    "from edge to edge. It must not look HDR, must not be uniformly sharp across the whole frame, "
    "and must not have crunchy over-resolved micro-detail. If every part of the picture is equally "
    "sharp, it is wrong."
)

# Perfect bilateral symmetry is the single strongest render tell, so it is named.
ASYMMETRY = (
    "The bag is very slightly asymmetric the way a real handmade bag is, never perfectly mirrored "
    "left to right, and it sits at a slightly casual angle rather than squared to the camera."
)


# --- LOCKED PRODUCT TRUTH (PRODUCT-TRUTH.md 2b, the REAL 25 cm spec) ----------

LC = dict(canvas="cream ivory canvas", leather="warm chestnut brown")
DC = dict(canvas="cream ivory canvas", leather="very dark espresso brown, nearly black in shadow")
AG = dict(canvas="deep muted olive green canvas", leather="warm chestnut brown")


def identity(cw):
    return (
        f"The bag is a small structured top handle handbag, nearly square from the front and "
        f"noticeably deep front to back. Its upper section is {cw['leather']} leather with visible "
        f"natural grain, shaped as a domed arched flap folded down flat over the front, sitting over "
        f"a lower body of {cw['canvas']}. Two short rolled leather top handles rise from the leather "
        f"band. A small gold turn lock sits at the front centre of the flap. Two leather belt straps "
        f"run roughly horizontally across the front, angling slightly down toward the centre, each "
        f"passing through a flat gold plate with an oblong slot and continuing outward to a small "
        f"gold roller buckle on each side gusset. A small leather clochette tag hangs on a long "
        f"leather tab at the front centre. Leather corner patches finish the bottom, and small gold "
        f"feet sit along the bottom edge. Visible stitching throughout, warm brass gold hardware, "
        f"and no logos, no lettering and no embossing anywhere on the bag."
    )


# SMALL-SCALE BLOCK. Validated 2026-08-14, the single most important instruction on
# this product: dimensions bluntly, name it a handbag, rule out larger silhouettes by
# name, give the two visible consequences.
SCALE = (
    "The bag is SMALL. It is a compact everyday handbag measuring 25 cm wide, 22 cm tall and 14 cm "
    "deep, about 10 by 8.7 by 5.5 inches. It is a handbag and it is never a travel bag, never a "
    "weekender, never a duffel and never a large tote. Two visible consequences that must both "
    "show: the rolled top handles arch only about three inches above the top edge of the bag, and "
    "the gold fittings stay full size so they read LARGE against the small front panel."
)

# MANDATORY DETAIL CORRECTIONS. Four defects that appear on essentially every first
# roll of this silhouette. Phrased POSITIVELY per the moderation law.
DETAILS = (
    "Four details must be rendered correctly. First, each belt strap is a continuous piece of "
    "leather that visibly runs from the gold plate outward across the canvas to its side buckle, so "
    "the gold plates always sit ON a leather strap. Second, the leather band carries exactly one "
    "gold turn lock and that is the only round gold fitting on the front. Third, each side tab along "
    "the lower edge of the flap carries its own small vertical oval slot. Fourth, every leather "
    "surface on the bag is the same grained leather, on the flap, the band, the handles, the corner "
    "patches and the straps alike."
)

# CLOSURE-INTERACTION LAW: hands never work the flap or the belt straps.
CLOSED = (
    "The bag is fully closed exactly as in the reference image: the one piece leather flap is folded "
    "down flat over the front with its domed arched top edge clearly readable, both belt straps are "
    "fastened outward to the gold roller buckle on each side gusset, and the gold turn lock sits "
    "closed at the front centre. No hand touches the flap, the turn lock or the belt straps. The bag "
    "is carried by its two short rolled top handles only: it has no shoulder strap, no crossbody "
    "strap and no long strap of any kind anywhere in the frame."
)

HANDS = (
    "Any visible hand is rendered cleanly and naturally, with five well formed fingers, each finger "
    "clearly separated and correctly proportioned, in a relaxed everyday grip."
)

# 2026-08-16, Brooks: "only product focused footage please. no other random bags or anything."
# A second bag in frame splits attention and can read as a competitor product -- the same reason
# the two-bags shot was retired from the first library. This goes in EVERY prompt.
NO_OTHER_BAGS = (
    "This handbag is the ONLY bag anywhere in the photograph. There is no second handbag, no tote, "
    "no straw or woven basket bag, no shopper, no backpack, no rucksack, no luggage, no suitcase, "
    "no holdall and no shoulder bag of any kind visible anywhere in the frame, not in the "
    "foreground and not in the background."
)


# --- THE 12 SHOTS -------------------------------------------------------------
#
# Every scene is written as something a real person would actually film on their phone
# for a TikTok B-roll library: a real room with its own clutter, one window as the only
# light, framing a bit off. The reference image is named per shot -- and per the LAW
# from the 8/15 QA round, the OPEN-state photo is the PRIMARY reference for the one
# open-bag shot (B03). Describing an open bag while referencing the closed hero
# produces a both-states-at-once hybrid.

SHOTS = {
    "B01-closet": (["LC-01.png"], CLOSED,
        "A woman's hand lifts the handbag off a shelf inside an ordinary open wardrobe. The shelf "
        "around it has real life on it: a folded jumper with a sleeve hanging over the edge, a "
        "stack of two shoeboxes, and a rolled scarf pushed to the back. Light comes only from a bedroom window off to the "
        "left, so the inside of the wardrobe falls into soft shadow and the edge of the bag catches "
        "the brighter light. Shot from chest height, slightly off centre, the phone held in one hand."),

    "B02-flatlay": (["LC-01.png"], CLOSED,
        "Overhead phone snapshot looking straight down at a rumpled linen bedspread with the duvet "
        "creased and not smoothed out. The handbag sits at the bottom of the frame and a few things "
        "are scattered above it, not arranged: a small folded wallet, two or three loose cards, a "
        "set of keys on a ring and a lip balm. There are NO sunglasses and NO phone anywhere in the "
        "picture. Her other hand rests in the corner of the frame. "
        "Daylight from one window on the left, her own shadow falling faintly across the bed."),

    "B03-loadin": (["ref-interior.jpg", "LC-01.png"], HANDS +
        " Because the flap is folded all the way BACK, the front of the bag shows NO flap: no "
        "scalloped tabs and no oval keyhole plate, only the shallow leather band with the turn lock "
        "and one gold plate either side. No hand touches the flap or the belt straps at any point.",
        "Close phone shot of the bag sitting open on a kitchen counter, its mouth standing open, "
        "while a hand lowers a small folded wallet down into it. The counter has ordinary things on "
        "it just out of focus behind: a mug, a set of keys, a folded tea towel. One window light from "
        "the side, the near edge of the counter slightly blown out."),

    "B04-standsquare": (["LC-01.png"], CLOSED,
        "The handbag set down on a small outdoor cafe table, standing on its own on its gold feet. "
        "The table is real and used: a couple of water rings, a crumpled paper napkin, a half "
        "finished espresso pushed to one side. Shot from a seated person's eye level, the phone held "
        "casually so the horizon tilts a few degrees and the bag sits off centre, with the pavement "
        "and passing street behind thrown out of focus. Low afternoon sun from behind and to the "
        "left, so the top edge of the bag is rimmed bright and slightly blown out."),

    "B05-walking": (["LC-01.png"], CLOSED + " " + HANDS,
        "Filmed from the side, following a woman as she walks along a city pavement in a camel coat, "
        "the handbag hanging from one hand at her side. She is cropped from mid thigh to shoulder "
        "with her head out of the top of the frame. Autumn leaves on the wet pavement. The phone is "
        "held in one hand while walking, so the frame moves a little and there is a trace of motion "
        "blur in her coat and the background. Overcast daylight, flat and cool."),

    "B06-elbow": (["LC-01.png"], CLOSED,
        "Close phone shot of the handbag carried in the crook of a woman's elbow, over the sleeve of "
        "a camel wool coat, cropped so only her forearm and the bag are in frame. Behind her a real "
        "street with parked cars and railings, out of focus. Late afternoon side light, the coat "
        "sleeve slightly overexposed where the sun hits it."),

    "B07-buckle": (["LC-04.png", "LC-03.png"], CLOSED,
        "Very close phone macro of the small gold roller buckle on the side gusset of the bag, with "
        "the leather belt strap running into it. The focus falls just slightly behind the buckle the "
        "way a phone macro does, so the buckle edge is only nearly sharp. Real grain in the leather, "
        "a faint fingerprint on the gold. Warm low sun raking across from the left. Framing is tight "
        "and a little crooked, and the top edge of the flap is cropped out of frame entirely."),

    "B08-feet": (["LC-03.png", "LC-01.png"], CLOSED,
        "Low phone shot down at the bottom edge of the bag where it rests on a worn stone step, "
        "showing the small gold feet and the leather corner patches lifting the canvas just clear of "
        "the stone. A dry leaf and some grit beside it. The stone is chipped and stained. Framing is "
        "tight and low so the top edge of the flap is cropped out of frame entirely. Soft daylight "
        "from one side."),

    "B09-bench": (["LC-01.png", "LC-03.png"], CLOSED,
        "The handbag sitting at a three quarter angle on the weathered slats of a park bench, shot "
        "from standing height looking down at it, off centre and a little crooked. The bench timber "
        "is grey, splintered and marked, with fallen leaves caught between the slats and one leaf "
        "resting against the bag. Late golden light coming through trees behind, dappled and uneven "
        "across the seat, part of the frame in shade."),

    "B10-wall": (["LC-01.png"], CLOSED + " " + HANDS,
        "A woman holds the handbag up in one hand at about hip height against a plain warm painted "
        "interior wall, so its size reads against her body. She is cropped from the shoulders down. "
        "The wall is a real wall with a scuff, a faint mark and an uneven paint finish. Light from a "
        "window camera-left throws her soft shadow onto the wall behind. Phone held slightly low and "
        "tilted."),

    "B11-carseat": (["LC-01.png"], CLOSED,
        "The handbag standing upright on the passenger seat of a parked car, shot from the driver's "
        "seat with the phone held at chest height and angled down. The seat fabric is creased with a "
        "seatbelt buckle lying beside it and a receipt in the door pocket. Daylight through the "
        "windscreen, dappled as if parked under a tree, the windscreen side of the frame much "
        "brighter than the footwell."),

    "B12-doorway": (["LC-01.png"], CLOSED + " " + HANDS,
        "A woman stepping out through an apartment doorway with her coat on, the handbag riding on "
        "her forearm while both hands are full with a set of keys and a phone. Cropped at the "
        "shoulders. The hallway behind her is dim and real, with a coat hook and shoes by the wall, "
        "while bright daylight comes through the open door and blows out one side of the frame."),
}

# Colorway coverage. LC is authored first and is the master; DC and AG are produced as
# single-variable recolours in a second pass (recolour_v3.py) so composition stays
# pixel-identical across colorways -- the established Delphine workflow.
COLORWAY = LC


def build_prompt(shot):
    refs, extra, scene = SHOTS[shot]
    return "\n\n".join([
        PREAMBLE,
        scene,
        identity(COLORWAY),
        SCALE,
        extra,
        NO_OTHER_BAGS,
        DETAILS,
        ASYMMETRY,
        OPTICS,
        FOOTER,
    ])


def api(url, payload=None, headers=None):
    """curl, not urllib -- this machine has no cert bundle for urllib and every
    api.kie.ai call dies on CERTIFICATE_VERIFY_FAILED."""
    cmd = ["curl", "-s", "--max-time", "120", url]
    for k, v in (headers or {}).items():
        cmd += ["-H", f"{k}: {v}"]
    if payload is not None:
        cmd += ["-H", "Content-Type: application/json", "-d", json.dumps(payload)]
    out = subprocess.run(cmd, capture_output=True, text=True).stdout
    try:
        return json.loads(out)
    except Exception:
        return {"code": -1, "raw": out[:400]}


def fetch(url, dest):
    subprocess.run(["curl", "-s", "-L", "--max-time", "300", "-o", dest, url], check=True)
    return os.path.getsize(dest)


def upload(path):
    out = subprocess.run(
        ["curl", "-s", "-X", "POST", UPLOAD,
         "-H", f"Authorization: Bearer {KEY}",
         "-F", f"file=@{path}",
         "-F", "uploadPath=images/delphine-broll-v3"],
        capture_output=True, text=True).stdout
    d = json.loads(out)
    assert d.get("success") or d.get("code") == 200, f"upload failed {path}: {out[:300]}"
    return (d.get("data") or {}).get("downloadUrl") or d["data"]["fileUrl"]


def submit(shot, ref_urls):
    payload = {"model": "gpt-image-2-image-to-image",
               "input": {"prompt": build_prompt(shot),
                         "input_urls": ref_urls,
                         "aspect_ratio": "9:16",
                         "resolution": "2K"}}
    d = api(f"{API}/jobs/createTask", payload, H)
    if d.get("code") != 200:
        payload["input"]["resolution"] = "1K"
        d = api(f"{API}/jobs/createTask", payload, H)
    if d.get("code") != 200:
        return None
    return d["data"]["taskId"]


def main():
    os.makedirs(OUT, exist_ok=True)

    jobs = []   # (name, shot)
    for shot in SHOTS:
        for v in range(1, VARIANTS + 1):
            name = f"LC-{shot}-v{v}"
            if os.path.exists(os.path.join(OUT, f"{name}.png")):
                print(f"{name}: exists, skip", flush=True)
            else:
                jobs.append((name, shot))
    if not jobs:
        print("all variants present", flush=True)
        return

    cache = {}
    for shot in {s for _, s in jobs}:
        for r in SHOTS[shot][0]:
            if r not in cache:
                cache[r] = upload(os.path.join(REAL, r))
                print(f"uploaded {r}", flush=True)

    tries = {name: 0 for name, _ in jobs}
    pending = {}
    for name, shot in jobs:
        tries[name] += 1
        tid = submit(shot, [cache[r] for r in SHOTS[shot][0]])
        if tid:
            pending[name] = (tid, shot)
            print(f"{name}: task {tid}", flush=True)
        else:
            print(f"{name}: submit rejected", flush=True)
        time.sleep(2)

    deadline = time.time() + 3600
    while pending and time.time() < deadline:
        time.sleep(15)
        for name, (tid, shot) in list(pending.items()):
            d = api(f"{API}/jobs/recordInfo?taskId={tid}", None, H)
            st = (d.get("data") or {}).get("state")
            if st == "success":
                rj = json.loads(d["data"]["resultJson"], strict=False)
                size = fetch(rj["resultUrls"][0], os.path.join(OUT, f"{name}.png"))
                print(f"{name}: DONE ({size // 1024} KB)", flush=True)
                del pending[name]
            elif st == "fail":
                print(f"{name}: attempt {tries[name]} failed: "
                      f"{(d.get('data') or {}).get('failMsg')}", flush=True)
                del pending[name]
                if tries[name] < ATTEMPTS:
                    tries[name] += 1
                    tid2 = submit(shot, [cache[r] for r in SHOTS[shot][0]])
                    if tid2:
                        pending[name] = (tid2, shot)
                        print(f"{name}: retry task {tid2} (attempt {tries[name]})", flush=True)
                else:
                    print(f"{name}: GIVING UP", flush=True)

    if pending:
        print(f"TIMEOUT still pending: {list(pending)}", flush=True)
    done = len([f for f in os.listdir(OUT) if f.endswith(".png")])
    print(f"complete: {done} variants on disk", flush=True)


if __name__ == "__main__":
    main()
