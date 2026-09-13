#!/usr/bin/env python3
"""THE CONSIDERED CARRY-ON statics — generate 5 plates via kie.ai GPT Image 2 i2i.

Replication of the Vestirsi "Vera Large Bowler" two-panel static for The Eleanor
Weekender. Two panel types:

  3 x TOP PANEL     editorial lifestyle, bag stacked on a rolling carry-on with the
                    telescoping handle extended (the stack IS the mechanism demo)
  2 x PRODUCT PLATE single bag, front-on, flat #D7CFC8 greige, for the lower panel

Text is NEVER generated here — it is overlaid in post (compose_ads.py) so the
typography is pixel-identical across the set and "Weekender" can never misspell.

The bag is CLOSED in all five plates, so the open-bag mechanism block does not
apply. What DOES apply, from the velantra-weekender skill + the Back In Stock
post-mortem, is in WK_HARDEN below: pin both handles, ban decorative tooling.

Reference is the CLOSED hero only. `light chocolate 4.webp` is deliberately not
wired in — it is the open-interior ref and the documented source of the phantom
front-flap reconstruction.

Idempotent: skips plates whose PNG already exists (delete to regenerate).
"""
import json, os, time, urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
VAULT = "/Users/brooksorradre2/Documents/marketing brain"
WK_REFS = os.path.join(VAULT, "brands/velantra/products/weekender/product-images/product images")
OUT = os.path.join(ROOT, "plates")
API = "https://api.kie.ai/api/v1"
UPLOAD = "https://kieai.redpandaai.co/api/file-stream-upload"

KEY = None
with open(os.path.join(VAULT, ".env")) as f:
    for line in f:
        if line.startswith("KIE_API_KEY="):
            KEY = line.split("=", 1)[1].strip()
assert KEY, "KIE_API_KEY not found"
H = {"Authorization": f"Bearer {KEY}"}

# ------------------------------------------------ verbatim identity block (velantra-weekender skill)
WK_IDENTITY = (
    "a structured two tone weekend bag, wider than tall, rich cognac brown leather upper flap "
    "section and two rolled cognac leather top handles over a {canvas} body, a small gold oval turn "
    "lock on the front, two flat gold clasp plates with cognac leather belt straps threaded through "
    "them, a small cognac leather key bell tied to the handle base, cognac leather corner patches at "
    "the bottom, visible stitching, gold hardware, no logos anywhere on the bag, natural cream cotton "
    "canvas interior lining with a cognac leather slip pocket on the back wall"
)

# Anti-drift hardening. MANDATORY here: the bag is small in frame in the top panels.
# The both-handles pin and the no-tooling ban are the two failures GPT i2i actually
# committed on this bag in the Back In Stock run.
WK_HARDEN = (
    "The bag in frame is an exact copy of the bag in the first reference image in silhouette, "
    "proportions, materials and details, the two rolled top handles are smooth simple leather tubes "
    "with no wrapping, no braiding and no woven texture. The bag is fully closed with its flap folded "
    "down flat over the front. The bag has no zipper anywhere, no zipper track, no zipper teeth and "
    "no zipper pull, and no embossed text or lettering anywhere on it. "
    "BOTH handles are clearly visible standing upright above the bag as two separate parallel rolled "
    "leather tubes: the front handle rises from the front leather band and the rear handle rises from "
    "the back leather band directly behind it, with visible space between the two arcs. Never omit "
    "the rear handle. "
    "All of the cognac leather is plain smooth grain leather: no embossed pattern, no floral, paisley "
    "or damask tooling, no decorative stamping anywhere on the leather. The canvas is plain woven "
    "canvas with no pattern woven or printed into it. "
    "The turn lock, the clasp plates and the belt straps exist ONLY on the front face of the bag, "
    "with no front detailing duplicated onto any side or back face."
)

MATCH = (
    "The bag in the image is an exact copy of the bag in the first reference image in silhouette, "
    "proportions, construction, materials and details, and every color on the bag matches the first "
    "reference image exactly."
)

NEG_COMMON = (
    "There is absolutely no text, no lettering, no words, no captions, no watermark, no logo and no "
    "graphics anywhere in the image. No other bags."
)

WK_COLORS = {
    "light-chocolate": ("cream ivory woven canvas", "light chocolate 1.webp"),
    "army-green":      ("deep army green twill canvas", "green 1.webp"),
}

# ------------------------------------------------------------------ top panel scenes
# The stack is non-negotiable: bag squarely on the flat top of the case, telescoping
# handle rising just behind it. That composition is the silent product demo and the
# whole reason this swipe works. A clean quiet lower-left area is reserved for type.
STACK = (
    "A dark charcoal grey hard shell rolling carry on suitcase stands upright with its telescoping "
    "metal handle fully extended straight up. The bag rests on top of the suitcase, sitting squarely "
    "and level on the flat top of the case, with the extended luggage handle rising just behind it "
    "and its two rolled leather handles standing upright above it. The bag is the visual hero of the "
    "photograph, large in frame, photographed from the front at a very slight angle, positioned in "
    "the right half of the frame."
)

MODEL = (
    "A woman stands in the left third of the frame, cropped so that only her body from the ribcage "
    "down is visible and her face, head, neck and shoulders are entirely outside the top of the "
    "frame. She wears head to toe warm oatmeal linen: an oversized open long line linen shirt jacket "
    "over matching high waisted wide leg linen trousers, with one hand resting inside her trouser "
    "pocket. Her hands never touch the bag."
)

TYPE_SPACE = (
    "The lower left area of the frame is a clean quiet expanse of floor and soft blurred background "
    "with nothing in it, reserved and uncluttered."
)

TOP_SCENES = {
    "top-01-departure-lc": ("light-chocolate", (
        "A vertical editorial fashion photograph in soft cool natural daylight. "
        + MODEL + " " + STACK + " "
        "They stand on a smooth pale polished concrete floor in a modern airport departure hall, the "
        "background softly blurred far out of focus into muted grey, warm beige and pale glass tones "
        "with soft daylight from tall windows. Shallow depth of field with crisp focus held on the "
        "bag, quiet restrained editorial color grade, warm neutral palette, no harsh shadows. "
        + TYPE_SPACE)),

    "top-02-arrival-ag": ("army-green", (
        "A vertical editorial fashion photograph in warm late afternoon daylight. "
        + MODEL + " " + STACK + " "
        "They stand on the warm pale stone floor of a quiet sunlit hotel corridor, the background "
        "softly blurred out of focus into pale plaster walls and long cream linen curtains, with warm "
        "sunlight falling across the stone floor in soft diagonal bands. Shallow depth of field with "
        "crisp focus held on the bag, quiet restrained editorial color grade, warm neutral palette. "
        + TYPE_SPACE)),

    "top-03-corridor-lc": ("light-chocolate", (
        "A vertical editorial product photograph in warm late afternoon daylight, with no people "
        "anywhere in the image. " + STACK + " "
        "The suitcase stands on the warm pale stone floor of a quiet sunlit hotel corridor, the "
        "background softly blurred out of focus into pale plaster walls, a tall cream linen curtain "
        "and a distant console table, with warm sunlight falling across the stone floor in soft "
        "diagonal bands. Shallow depth of field with crisp focus held on the bag, quiet restrained "
        "editorial color grade, warm neutral palette. " + TYPE_SPACE +
        " No people, no hands, no body parts, no mannequin.")),
}

# ---------------------------------------------------------------- product plate scene
PLATE_SCENE = (
    "A square studio product photograph. The background is one completely flat, smooth, seamless "
    "warm greige backdrop of the exact color hex D7CFC8, perfectly even edge to edge with no folds, "
    "no texture, no gradient, no vignette and no visible horizon line. The bag stands upright, "
    "perfectly centered left to right, photographed straight on from the front at eye level, its two "
    "rolled top handles standing upright above it in two clean parallel arcs. Soft even diffused "
    "studio light from the front, with only a very soft subtle contact shadow directly beneath the "
    "bag. The bag sits in the middle of the frame with generous clean empty background all around it "
    "on every side. Crisp focus throughout, warm neutral color grade. "
    "No hands, no people, no body parts, no mannequin, no props, no furniture, no suitcase."
)


def build_jobs():
    jobs = []
    for sid, (colorway, scene) in TOP_SCENES.items():
        canvas, fname = WK_COLORS[colorway]
        ident = WK_IDENTITY.format(canvas=canvas)
        prompt = f"{scene} The bag: {ident} {WK_HARDEN} {MATCH} {NEG_COMMON}"
        jobs.append((sid, prompt, [os.path.join(WK_REFS, fname)], "1:1"))

    for colorway, (canvas, fname) in WK_COLORS.items():
        ident = WK_IDENTITY.format(canvas=canvas)
        prompt = f"{PLATE_SCENE} The bag: {ident} {WK_HARDEN} {MATCH} {NEG_COMMON}"
        jobs.append((f"plate-{colorway}", prompt, [os.path.join(WK_REFS, fname)], "1:1"))
    return jobs


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
             "-F", "uploadPath=carryon-statics",
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
    all_jobs = build_jobs()
    jobs = [j for j in all_jobs if not os.path.exists(os.path.join(OUT, f"{j[0]}.png"))]
    if not jobs:
        print("all plates exist, nothing to do")
        return

    cache = {}
    for _, _, refs, _ in jobs:
        for r in refs:
            if r not in cache:
                cache[r] = upload(r)

    tasks = {}
    for sid, prompt, refs, ar in jobs:
        payload = {"model": "gpt-image-2-image-to-image",
                   "input": {"prompt": prompt,
                             "input_urls": [cache[r] for r in refs],
                             "aspect_ratio": ar,
                             "resolution": "2K"}}
        d = api(f"{API}/jobs/createTask", payload, H)
        if d.get("code") != 200:
            payload["input"]["resolution"] = "1K"
            d = api(f"{API}/jobs/createTask", payload, H)
        assert d.get("code") == 200, f"{sid} createTask failed: {d}"
        tasks[sid] = d["data"]["taskId"]
        print(f"{sid}: task {tasks[sid]}", flush=True)

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
    print(f"plates on disk: {len(have)}/{len(all_jobs)} -> {have}", flush=True)
    print("\nNEXT: run the mandatory frame-QA subagent pass on every plate "
          "BEFORE compose_ads.py (see brief section 6).", flush=True)


if __name__ == "__main__":
    main()
