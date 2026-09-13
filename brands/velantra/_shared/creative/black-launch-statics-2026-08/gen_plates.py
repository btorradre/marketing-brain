#!/usr/bin/env python3
"""BLACK PRE-ORDER LAUNCH statics — generate the product plate via kie.ai GPT Image 2 i2i.

Fork of dark-chocolate-launch-statics-2026-08/gen_plates.py, which was itself a fork of
back-in-stock-statics-2026-07 (Vestirsi "Back In Stock" swipe). Same composition: bag
centered on a draped fabric backdrop with clean empty fabric in the top and bottom
quarters for the post-overlay typography.

Two things are different here and both come from the same fact: **Black is the darkest
colorway we have, and it is all leather with no canvas anywhere.**

1. The backdrop is squeezed between two hard constraints. It has to be clearly LIGHTER
   than pure black leather or the bag dissolves into it (the DC run's one real risk,
   maximised here), and it has to stay deep enough that WHITE typography sits legibly
   over it in the top and bottom quarters. That lands on a warm medium brown, a couple
   of stops lighter than the DC drape, plus a rim light on the flap top and handles.
2. The composition reference (the approved DC plate) has a cream canvas body. Black does
   not. Leftover canvas is the documented signature failure on every Black i2i we have
   run, so the canvas is negated explicitly rather than left to the first reference to
   settle.

Text is NEVER generated here — it is overlaid in post (compose_ads.py) so spelling can
never drift ("Weekender" is a known text-render failure across engines).

3 variants per the standing three-variants-then-pick rule. Idempotent: skips variants
whose PNG already exists (delete to regenerate).
"""
import json, os, time, urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
VAULT = "/Users/brooksorradre2/Documents/marketing brain"
# Ground truth for black colour and material: the real iPhone photograph of the physical
# bag, per the black-colorway supreme-reference law.
REAL = os.path.join(VAULT, "brands/velantra/products/weekender/product-images/black/"
                           "original-iphone-photos/black-01.png")
# Composition/backdrop/lighting only. The DC plate rather than the July light-chocolate
# one, because it already solved this layout for a dark bag.
COMP = os.path.join(VAULT, "brands/velantra/_shared/creative/"
                           "dark-chocolate-launch-statics-2026-08/plates/"
                           "eleanor-dark-chocolate-v2.png")
OUT = os.path.join(ROOT, "plates")
API = "https://api.kie.ai/api/v1"
UPLOAD = "https://kieai.redpandaai.co/api/file-stream-upload"
VARIANTS = 3

KEY = None
with open(os.path.join(VAULT, ".env")) as f:
    for line in f:
        if line.startswith("KIE_API_KEY="):
            KEY = line.split("=", 1)[1].strip()
assert KEY, "KIE_API_KEY not found"
H = {"Authorization": f"Bearer {KEY}"}

# ---------------------------------------------------------------- scene
SCENE = (
    "A vertical studio product photograph. The background is one continuous piece of warm medium "
    "brown matte cotton fabric hung and draped as a backdrop, filling the entire frame, with soft "
    "natural vertical folds and gentle creases reading as subtle shadow gradients, slightly darker "
    "toward the edges and corners. The backdrop brown is a warm mid tone, about the tone of milk "
    "chocolate or toasted caramel: clearly and obviously MUCH LIGHTER than the pure black leather of "
    "the bag, so the black bag reads as a clean separated silhouette against it and never blends into "
    "it, while still being deep enough in tone to sit under white text. The bag stands upright, "
    "perfectly centered left to right, photographed straight on from the front at eye level, its two "
    "top handles standing upright above it. The bag sits in the MIDDLE band of the frame only: the "
    "entire top quarter of the image and the entire bottom quarter of the image are clean empty "
    "draped fabric with nothing in them. Soft diffused studio light from the front plus a distinct "
    "soft rim of light along the top edge of the flap and along the top of both handles so the black "
    "leather separates cleanly from the brown backdrop, and a soft dark contact shadow pooling "
    "directly beneath the bag. Warm neutral color grade, shallow depth of field on the backdrop "
    "folds, crisp focus on the bag."
)

REFS = (
    "There are two reference images. Use the FIRST reference image as the truth for the bag itself: "
    "its silhouette, proportions, construction, hardware, stitching, materials and every one of its "
    "colors. Use the SECOND reference image ONLY as the guide for the composition, the framing, the "
    "size of the bag in frame, the draped fabric backdrop and the lighting. Ignore the bag materials "
    "and colors in the second reference image completely: that bag has a cream ivory woven canvas "
    "body and dark brown leather, and BOTH are WRONG for this bag. The bag you produce has no canvas "
    "on it anywhere and no brown on it anywhere. Every exterior surface of it is smooth black leather, "
    "exactly as in the FIRST reference image."
)

# velantra-weekender identity block, resolved to the all-leather Black colorway
IDENTITY = (
    "The bag: a structured single tone weekend bag, wider than tall, made entirely of smooth black "
    "leather over its whole exterior, with a black leather upper flap section and two rolled black "
    "leather top handles above a black leather body, a fine horizontal seam where the upper section "
    "meets the body being the only division on it, a small gold oval turn lock on the front, two flat "
    "gold clasp plates with black leather belt straps threaded through them, a small black leather key "
    "bell tied to the handle base, black leather corner patches at the bottom, a small gold eyelet "
    "high on each side face, visible stitching, warm brass gold hardware, no logos anywhere on the bag."
)

# The documented signature failure on every Black i2i: the model recolours a canvas panel
# instead of replacing it, leaving a visible weave, a grey-versus-black material split, or
# a small unconverted wedge at a side gusset. Stated positively AND negatively.
NO_CANVAS = (
    "This bag has NO canvas on it at all. There is no woven fabric panel, no crosshatch weave, no "
    "textile texture and no cream, ivory, beige, grey or off white area anywhere on its exterior. The "
    "body of the bag below the flap is the same smooth black leather as the flap above it, one single "
    "uniform black leather all over, including both side gussets and both bottom corners."
)

# closure hardware block, condensed for a full-bag front-on shot
HARDWARE = (
    "Front closure, exactly as on the first reference image: the flap is down over the front, its "
    "center tab carrying a polished gold oval plate resting over a small gold turn post on the "
    "leather band, and two flat vertical gold staples standing to its left and right. The two leather "
    "belt straps come over the top from the back and hang unfastened down the sides with their flat "
    "gold end plates visible. TWO flat gold clasp plates, one on the left and one on the right, BOTH "
    "fully visible and symmetric, the RIGHT plate identical in shape, size and warm brass gold color "
    "to the LEFT plate. No silver, no chrome, no white metal on any hardware."
)

HARDEN = (
    "The bag in frame is an exact copy of the bag in the first reference image in silhouette, "
    "proportions, materials and details. The two rolled top handles are smooth simple leather tubes "
    "with no wrapping, no braiding and no woven texture. The bag is fully closed with its flap down "
    "over the front. The bag has no zipper anywhere and no embossed text or lettering anywhere on it. "
    "BOTH handles are clearly visible standing upright above the bag as two separate parallel rolled "
    "leather tubes: the front handle rises from the front leather band and the rear handle rises from "
    "the back leather band directly behind it, with visible space between the two arcs. Never omit "
    "the rear handle. All of the leather is plain smooth grain leather: no embossed pattern, no "
    "floral, paisley or damask tooling, no decorative stamping anywhere on the leather."
)

# GLOBAL LAW: nothing may read as a 3D render. This is a studio still, so the iPhone
# snapshot footer does not apply — the anti-CGI pressure goes on the SURFACES instead.
# Black leather is the easiest surface in the whole line to render as plastic, so this
# block carries more weight here than it did on Dark Chocolate.
MATERIAL = (
    "This is a real photograph of a real physical bag, not a 3D render, not CGI, not a computer "
    "generated product visualisation. The black leather is real leather: unevenly grained with a "
    "visible natural pebbled grain, softly creased where it folds, faintly scuffed and gently dulled "
    "where it has been handled, with soft broad highlights that fall off gradually rather than sharp "
    "specular hotspots. It is a soft matte to satin black, never patent, never high gloss, never a "
    "uniform polished plastic finish, and never a flat featureless black shape. The fabric backdrop "
    "shows real cotton texture and real fold shadows."
)

NEG = (
    "There is absolutely no text, no lettering, no words, no captions, no watermark, no logo and no "
    "graphics anywhere in the image. No hands, no people, no body parts, no mannequin, no props, "
    "no furniture, no other bags."
)

PROMPT = f"{SCENE} {REFS} {IDENTITY} {NO_CANVAS} {HARDWARE} {HARDEN} {MATERIAL} {NEG}"


def api(url, payload=None, headers=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(
        url, data=data,
        headers={**(headers or {}), **({"Content-Type": "application/json"} if data else {})})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read().decode(), strict=False)
        except Exception as e:
            if attempt == 3:
                raise
            print(f"  retry {attempt+1}: {e}", flush=True)
            time.sleep(3 * (attempt + 1))


def upload(path):
    import subprocess
    name = os.path.basename(path).replace(" ", "_")
    last = ""
    for attempt in range(4):
        if attempt:
            time.sleep(15 * attempt)
        out = subprocess.run(
            ["curl", "-s", "-X", "POST", UPLOAD,
             "-H", f"Authorization: Bearer {KEY}",
             "-F", f"file=@{path}",
             "-F", "uploadPath=black-launch-statics",
             "-F", f"fileName={int(time.time()*1000)}-{name}"],
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
        print(f"  upload retry {name}: {last[:150]}", flush=True)
    raise RuntimeError(f"upload failed {path}")


def main():
    os.makedirs(OUT, exist_ok=True)
    want = [f"eleanor-black-v{i}" for i in range(1, VARIANTS + 1)]
    todo = [s for s in want if not os.path.exists(os.path.join(OUT, f"{s}.png"))]
    if not todo:
        print("all variants exist, nothing to do")
        return

    urls = [upload(REAL), upload(COMP)]

    # kie returns "Internal Error" on a large fraction of calls and batching makes it
    # worse — fire sequentially with a retry loop, per the skill.
    tasks = {}
    for sid in todo:
        payload = {"model": "gpt-image-2-image-to-image",
                   "input": {"prompt": PROMPT,
                             "input_urls": urls,
                             "aspect_ratio": "9:16",
                             "resolution": "2K"}}
        d = None
        for attempt in range(6):
            d = api(f"{API}/jobs/createTask", payload, H)
            if d.get("code") == 200:
                break
            print(f"  {sid} createTask attempt {attempt+1}: {d}", flush=True)
            time.sleep(10)
        assert d and d.get("code") == 200, f"{sid} createTask failed: {d}"
        tasks[sid] = d["data"]["taskId"]
        print(f"{sid}: task {tasks[sid]}", flush=True)
        time.sleep(4)

    pending = dict(tasks)
    deadline = time.time() + 1800
    while pending and time.time() < deadline:
        time.sleep(15)
        for sid, tid in list(pending.items()):
            d = api(f"{API}/jobs/recordInfo?taskId={tid}", None, H)
            st = (d.get("data") or {}).get("state")
            if st == "success":
                rj = json.loads(d["data"]["resultJson"], strict=False)
                url = rj["resultUrls"][0]
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=300) as r:
                    blob = r.read()
                with open(os.path.join(OUT, f"{sid}.png"), "wb") as f:
                    f.write(blob)
                print(f"{sid}: DONE ({len(blob)//1024} KB)", flush=True)
                del pending[sid]
            elif st == "fail":
                print(f"{sid}: FAILED {d['data'].get('failMsg')}", flush=True)
                del pending[sid]
    if pending:
        print(f"TIMEOUT pending: {list(pending)}", flush=True)
    have = sorted(f[:-4] for f in os.listdir(OUT) if f.endswith(".png"))
    print(f"plates on disk: {len(have)} -> {have}", flush=True)


if __name__ == "__main__":
    main()
