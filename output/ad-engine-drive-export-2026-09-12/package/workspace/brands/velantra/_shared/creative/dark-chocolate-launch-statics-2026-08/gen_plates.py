#!/usr/bin/env python3
"""DARK CHOCOLATE LAUNCH statics — generate the product plate via kie.ai GPT Image 2 i2i.

1:1 fork of back-in-stock-statics-2026-07/gen_plates.py (Vestirsi "Back In Stock"
swipe): bag centered on a deep chocolate-brown draped fabric backdrop, clean empty
fabric in the top and bottom quarters for the post-overlay typography.

Difference from the July run: the announcement is a COLOR LAUNCH, and the colorway
is Dark Chocolate, so the plate is anchored on the REAL product photograph
(XX-DARK-still-closed-front.jpg) rather than a catalogue webp, per the
velantra-weekender real-product ground-truth law (2026-08-08). The approved July
Eleanor plate is wired as a second reference for composition/backdrop/lighting ONLY.

Text is NEVER generated here — it is overlaid in post (compose_ads.py) so spelling
can never drift ("Weekender" is a known text-render failure across engines).

3 variants per the standing three-variants-then-pick rule. Idempotent: skips
variants whose PNG already exists (delete to regenerate).
"""
import json, os, time, urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
VAULT = "/Users/brooksorradre2/Documents/marketing brain"
REAL = os.path.join(VAULT, "brands/velantra/products/weekender/product-references/"
                           "real-product-2026-08-08/XX-DARK-still-closed-front.jpg")
COMP = os.path.join(VAULT, "brands/velantra/_shared/creative/back-in-stock-statics-2026-07/"
                           "plates/eleanor-light-chocolate.png")
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
# Backdrop brown is pinned LIGHTER than the bag's espresso leather: on the swipe the
# bag was pale straw against dark brown, here the bag's whole upper half is nearly as
# dark as the drape and would otherwise dissolve into it.
SCENE = (
    "A vertical studio product photograph. The background is one continuous piece of warm "
    "medium chocolate brown matte cotton fabric hung and draped as a backdrop, filling the entire "
    "frame, with soft natural vertical folds and gentle creases reading as subtle shadow gradients, "
    "slightly darker toward the edges and corners. This backdrop brown is clearly LIGHTER and warmer "
    "than the very dark espresso leather of the bag, so the bag reads as a clean separated silhouette "
    "against it and never blends into it. The bag stands upright, perfectly centered left to right, "
    "photographed straight on from the front at eye level, its two top handles standing upright above "
    "it. The bag sits in the MIDDLE band of the frame only: the entire top quarter of the image and "
    "the entire bottom quarter of the image are clean empty draped fabric with nothing in them. Soft "
    "diffused studio light from the front plus a soft rim of light along the top edge of the flap and "
    "along both handles so the dark leather separates from the dark backdrop, and a soft dark contact "
    "shadow pooling directly beneath the bag. Warm neutral color grade, shallow depth of field on the "
    "backdrop folds, crisp focus on the bag."
)

REFS = (
    "There are two reference images. Use the FIRST reference image as the truth for the bag itself: "
    "its silhouette, proportions, construction, hardware, stitching, materials and every one of its "
    "colors. Use the SECOND reference image ONLY as the guide for the composition, the framing, the "
    "size of the bag in frame, the draped fabric backdrop and the lighting. Ignore the bag colors in "
    "the second reference image completely: its leather is a light reddish cognac and that is WRONG "
    "for this bag. Every piece of leather on the bag you produce is the very dark espresso chocolate "
    "brown of the FIRST reference image."
)

# velantra-weekender verbatim identity block, dark chocolate bracket resolved
IDENTITY = (
    "The bag: a structured two tone weekend bag, wider than tall, very dark espresso chocolate brown "
    "leather upper flap section and two rolled dark espresso chocolate leather top handles over a "
    "cream ivory woven canvas body, a small gold oval turn lock on the front, two flat gold clasp "
    "plates with dark espresso chocolate leather belt straps threaded through them, a small dark "
    "espresso chocolate leather key bell tied to the handle base, dark espresso chocolate leather "
    "corner patches at the bottom, a small gold eyelet high on each side face, visible stitching, "
    "gold hardware, no logos anywhere on the bag."
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
    "floral, paisley or damask tooling, no decorative stamping anywhere on the leather. The canvas is "
    "plain woven canvas with no pattern woven or printed into it."
)

# GLOBAL LAW: nothing may read as a 3D render. This is a studio still, so the iPhone
# snapshot footer does not apply — the anti-CGI pressure goes on the SURFACES instead.
MATERIAL = (
    "This is a real photograph of a real physical bag, not a 3D render, not CGI, not a computer "
    "generated product visualisation. The espresso leather is real leather: unevenly grained, softly "
    "creased where it folds, faintly scuffed and mottled with natural pull up variation, dulled where "
    "it has been handled, never a uniform polished plastic finish and never high gloss. The cream "
    "canvas shows individual woven fibres, a fine two tone pin dot weave, slubs and small wrinkles. "
    "The fabric backdrop shows real cotton texture and real fold shadows."
)

NEG = (
    "There is absolutely no text, no lettering, no words, no captions, no watermark, no logo and no "
    "graphics anywhere in the image. No hands, no people, no body parts, no mannequin, no props, "
    "no furniture, no other bags."
)

PROMPT = f"{SCENE} {REFS} {IDENTITY} {HARDWARE} {HARDEN} {MATERIAL} {NEG}"


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
             "-F", "uploadPath=dc-launch-statics",
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
    want = [f"eleanor-dark-chocolate-v{i}" for i in range(1, VARIANTS + 1)]
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
