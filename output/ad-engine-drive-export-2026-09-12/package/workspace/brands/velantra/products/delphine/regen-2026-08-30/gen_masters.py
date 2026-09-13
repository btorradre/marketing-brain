#!/usr/bin/env python3
"""THE DELPHINE — product-image REGENERATION, master gate.

Why this run exists: the live gallery and the DEL-FALL-VO ads render a bag that
does not match the physical product. Diagnosed 2026-08-30 by pulling both live
Meta ads and reading them against the real photography:

  AD 120246141298260449  Trybe creator, real bag on camera, Army Green
  AD 120246105046880449  DEL-FALL-VO-05, our generated bag

Eight defects, all measured off `real-product/AG-01-front-1x1.png` (the
supplier's dimensioned front elevation, the only authoritative front we have):

  1. BASE. The real base is CONCAVE -- it arcs upward between the two corner
     caps. Every generated frame draws a flat straight bottom edge.
  2. CANVAS. Real canvas is a coarse diagonal twill with the weave plainly
     readable. Ours renders a smooth textureless felt panel.
  3. LEATHER. Real leather is burnished cognac with orange warmth and real
     sheen, light pooling on the flap. Ours is flat matte dark brown.
  4. GOLD PLATES. Real plates are LARGE, hang LOW on the canvas, ~20% of canvas
     height. Ours draws them small and tucked up under the band.
  5. HANDLES. Real handles arch ~38% of body height above the top edge. Ours
     are stubby, ~20-25%.
  6. SIDES. Real side gussets are LEATHER, flaring at the top corners. Ours
     wraps canvas around the sides.
  7. SHOULDER STRAP. The real bag has a detachable crossbody strap on gold snap
     hooks plus a roller buckle on each side gusset -- worn crossbody on camera
     in the creator ad. Not one generated frame has ever shown it. PRODUCT-TRUTH
     called it "unconfirmed" and banned it from prompts; that is now disproved.
  8. ARMY GREEN. Real AG is a dark army-drab olive. Ours renders mid sage.

NOT changed: the 40/60 leather-to-canvas ratio measured 42/58 on the dimensioned
front, so the existing law is correct and stays.

This script renders ONLY the three front-on masters. Per
feedback_one_approved_master_is_the_only_product_seed the master is approved
before anything is derived from it -- this product has been rejected four times
for deriving a set off an unapproved master.
"""
import json, os, time, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
VAULT = "/Users/brooksorradre2/Documents/marketing brain"
SEEDS = os.path.join(ROOT, "seeds")
OUT = os.path.join(ROOT, "masters")
API = "https://api.kie.ai/api/v1"
UPLOAD = "https://kieai.redpandaai.co/api/file-stream-upload"

KEY = None
with open(os.path.join(VAULT, ".env")) as f:
    for line in f:
        if line.startswith("KIE_API_KEY="):
            KEY = line.split("=", 1)[1].strip()
assert KEY, "KIE_API_KEY not found"
H = {"Authorization": f"Bearer {KEY}"}

# --- COLORWAYS ---------------------------------------------------------------
# Canvas and leather stated separately because the recolour path is
# single-variable. AG leather is the SAME cognac as LC -- only the canvas moves.

LC = dict(key="LC", name="Light Chocolate",
          canvas="natural cream ivory canvas",
          leather="burnished cognac leather, a warm mid brown with a clear orange red warmth in it")
DC = dict(key="DC", name="Dark Chocolate",
          canvas="natural cream ivory canvas",
          leather="very dark espresso brown leather, nearly black where it turns into shadow")
AG = dict(key="AG", name="Army Green",
          canvas="dark army drab olive green canvas, a deep muted military olive that is almost brown "
                 "in shadow and never a bright sage, never a grey green and never a light olive",
          leather="burnished cognac leather, a warm mid brown with a clear orange red warmth in it")

# --- IDENTITY. Rewritten 2026-08-30 from the dimensioned front elevation. ------
# Ordered top of the bag downward so the model builds it in the right sequence.


def identity(cw):
    return (
        f"THE BAG, built from the top down. It is a small structured top handle handbag that is wider than "
        f"it is tall, flaring outward at its top corners and drawing in slightly toward the base. "
        f"TOP: two tall rolled {cw['leather']} handles, each a single continuous unbroken smooth leather "
        f"tube, arching high above the top edge, rising by roughly a third of the height of the bag body, "
        f"set close together near the centre. "
        f"UPPER SECTION, the top two fifths of the body: one piece of {cw['leather']} shaped as a flap "
        f"whose top edge is DOMED, sweeping across in a shallow arch that is highest at the centre, with a "
        f"line of decorative stitching following that top edge and one small gold rivet at each of its "
        f"upper outer corners. In the middle of this flap sits one upright oval gold plate with one short "
        f"gold turning bar across it. A slim upright gold post stands proud of the leather on the left and "
        f"another on the right, out toward the flap's side tabs. A small leather clochette tag hangs on a "
        f"long leather tab at the centre front. "
        f"LOWER SECTION, the bottom three fifths of the body: a large panel of {cw['canvas']} whose "
        f"COARSE DIAGONAL TWILL WEAVE is plainly visible as fine ribbing running across the fabric. "
        f"Two {cw['leather']} belt straps come down onto this canvas from the flap above, one on the left "
        f"and one on the right, and each ends in a LARGE flat gold plate with a long oblong slot through "
        f"it. These two gold plates are big and they hang LOW, well down onto the canvas panel, each about "
        f"a fifth as tall as the canvas panel itself, tilted slightly inward toward each other. "
        f"BASE: the bottom edge of the bag is CONCAVE, curving gently UPWARD in the middle so the bag's "
        f"silhouette dips like a shallow smile between its two bottom corners, and it is never a flat "
        f"straight horizontal line. A large rounded {cw['leather']} corner cap wraps each bottom corner "
        f"and sweeps up the side edge. Small gold metal feet sit under the base. "
        f"SIDES: the side gussets are {cw['leather']}, not canvas, flaring out as leather wings at the top "
        f"corners, and a leather side strap runs out to a small gold roller buckle on each side gusset. "
        f"Every fitting is warm brass gold. There is no logo, no lettering, no monogram and no embossed "
        f"text anywhere on the bag."
    )


# SMALL-SCALE BLOCK. Validated 2026-08-14, still the single most important line.
SCALE = (
    "The bag is SMALL. It is a compact everyday handbag measuring 25 cm wide, 22 cm tall and 14 cm deep, "
    "about 10 by 8.7 by 5.5 inches. It is a handbag and it is never a travel bag, never a weekender, never "
    "a duffel and never a large tote. The gold fittings stay full size so they read LARGE against the small "
    "front panel."
)

# The strap. New on 2026-08-30 and the single biggest miss in the old library:
# the real bag ships a detachable crossbody strap and it is worn crossbody in
# the creator ad. Kept OFF the bag in the front master so the master reads as a
# clean packshot, but the side buckles it clips to must be present.
STRAP_OFF = (
    "In this frame the long detachable shoulder strap is not fitted to the bag, but the small gold roller "
    "buckle on each side gusset that it clips to is present and clearly visible."
)

MATERIAL = (
    "MATERIALS. The leather is real full grain leather with a burnished finish: it has a genuine sheen, "
    "light pooling brightly across the middle of the flap and deepening toward its edges, with visible "
    "natural grain and slight tonal variation the way burnished leather really behaves. It is never flat, "
    "never matte, never plastic and never suede. Every leather surface on the bag is the same single "
    "shade and the same single finish, on the flap, the handles, the corner caps, the side gussets and "
    "the straps alike. The canvas is a heavy woven cotton twill whose individual threads and diagonal "
    "weave are clearly readable at this size, never a smooth flat untextured panel and never felt."
)

STYLE = (
    "Warm off white seamless studio sweep in colour #F5F2EC, the floor curving up into the back wall with "
    "no visible corner or edge. Soft diffused daylight from the upper left, one soft contact shadow under "
    "the bag, a warm quiet low contrast grade. Photorealistic product photograph shot on a full frame "
    "camera with a 100mm macro lens at f8, the whole bag sharp. The bag stands upright on its own feet, "
    "square to the camera, filling most of the frame. No person, no hands, no props and no other objects "
    "anywhere in the frame. Absolutely no text, no words, no letters, no captions, no watermarks, no "
    "measurements and no logos anywhere in the image."
)

ANTI_CGI = (
    "The reference image supplies the bag's geometry, construction, hardware and materials ONLY, and never "
    "its lighting, its background or its rendering style. This is a real photograph taken with a real "
    "camera, not a computer rendering. It must not look like a 3D model, a CGI product visualisation, "
    "Octane, Blender, Cinema 4D or any game engine. The leather shows real grain and slight uneven creasing "
    "where it folds, the canvas shows real woven fibre texture, the gold hardware shows real specular "
    "highlights with tiny imperfections, and the bag casts one real soft contact shadow. The bag is very "
    "slightly asymmetric the way a handmade bag is, never perfectly mirrored left to right."
)


def prompt(cw):
    return (
        f"A single {cw['name']} handbag photographed straight on from the front. "
        f"{identity(cw)} {SCALE} {STRAP_OFF} {MATERIAL} "
        f"The bag matches the bag in the reference image exactly in construction, proportion, hardware and "
        f"colour. {STYLE} {ANTI_CGI}"
    )


# Seeds: each colorway is anchored on its OWN real photograph. The AG front is
# the supplier's dimensioned elevation with the printed measurements cropped off.
SPEC = {
    "LC": (LC, ["LC-front-clean.png"]),
    "DC": (DC, ["DC-34.png"]),
    "AG": (AG, ["AG-front-clean.png"]),
}
ROLLS = 2   # two rolls per colorway, picked on a contact sheet


def api(url, payload=None, headers=None):
    # urllib has no cert bundle on this machine; curl uses the system trust store.
    cmd = ["curl", "-s", "--max-time", "120", url]
    for k, v in (headers or {}).items():
        cmd += ["-H", f"{k}: {v}"]
    if payload is not None:
        cmd += ["-H", "Content-Type: application/json", "-d", json.dumps(payload)]
    for attempt in range(4):
        out = subprocess.run(cmd, capture_output=True, text=True)
        try:
            return json.loads(out.stdout, strict=False)
        except Exception as e:
            if attempt == 3:
                raise RuntimeError(f"{url} -> {(out.stdout or out.stderr)[:300]}") from e
            time.sleep(3 * (attempt + 1))


def upload(path):
    name = os.path.basename(path).replace(" ", "_")
    last = ""
    for attempt in range(4):
        if attempt:
            time.sleep(15 * attempt)
        out = subprocess.run(
            ["curl", "-s", "-X", "POST", UPLOAD,
             "-H", f"Authorization: Bearer {KEY}",
             "-F", f"file=@{path}",
             "-F", "uploadPath=delphine-regen-0830",
             "-F", f"fileName={int(time.time())}-{name}"],
            capture_output=True, text=True)
        try:
            d = json.loads(out.stdout, strict=False)
            url = (d.get("data") or {}).get("downloadUrl")
            if url:
                print(f"uploaded {name}", flush=True)
                return url
            last = out.stdout
        except Exception:
            last = out.stdout or out.stderr
    raise RuntimeError(f"upload failed for {name}: {last[:300]}")


def submit(cw, refs):
    payload = {"model": "gpt-image-2-image-to-image",
               "input": {"prompt": prompt(cw), "input_urls": refs,
                         "aspect_ratio": "1:1", "resolution": "2K"}}
    d = api(f"{API}/jobs/createTask", payload, H)
    if d.get("code") != 200:
        payload["input"]["resolution"] = "1K"
        d = api(f"{API}/jobs/createTask", payload, H)
    assert d.get("code") == 200, f"createTask failed: {d}"
    return d["data"]["taskId"]


def main():
    os.makedirs(OUT, exist_ok=True)
    cache = {}
    pending = {}
    for key, (cw, seeds) in SPEC.items():
        for s in seeds:
            if s not in cache:
                cache[s] = upload(os.path.join(SEEDS, s))
        for r in range(1, ROLLS + 1):
            tag = f"{key}-master-r{r}"
            if os.path.exists(os.path.join(OUT, f"{tag}.png")):
                print(f"{tag}: exists, skip", flush=True)
                continue
            pending[tag] = submit(cw, [cache[s] for s in seeds])
            print(f"{tag}: task {pending[tag]}", flush=True)

    deadline = time.time() + 2400
    while pending and time.time() < deadline:
        time.sleep(15)
        for tag, tid in list(pending.items()):
            d = api(f"{API}/jobs/recordInfo?taskId={tid}", None, H)
            data = d.get("data") or {}
            st = data.get("state")
            if st == "success":
                res = json.loads(data.get("resultJson") or "{}")
                urls = res.get("resultUrls") or []
                if urls:
                    dest = os.path.join(OUT, f"{tag}.png")
                    subprocess.run(["curl", "-s", "-L", "--max-time", "300", "-o", dest, urls[0]])
                    print(f"{tag}: SAVED {os.path.getsize(dest)//1024}kb", flush=True)
                pending.pop(tag)
            elif st == "fail":
                print(f"{tag}: FAILED {str(data.get('failMsg'))[:160]}", flush=True)
                pending.pop(tag)
    if pending:
        print("timed out:", list(pending), flush=True)


if __name__ == "__main__":
    main()
