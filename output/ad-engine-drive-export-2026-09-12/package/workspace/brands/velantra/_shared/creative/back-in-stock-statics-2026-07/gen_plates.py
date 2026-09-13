#!/usr/bin/env python3
"""BACK IN STOCK statics — generate 10 clean product plates via kie.ai GPT Image 2 i2i.

1:1 replication of the Vestirsi "Back In Stock" static: bag centered on a deep
chocolate-brown draped fabric backdrop, generous clean fabric top and bottom for
the post-overlay typography.

8 plates = The Sofia Woven Tote (every live colorway)
2 plates = The Eleanor Weekender (light chocolate, army green)

Text is NEVER generated here — it is overlaid in post (compose_ads.py) so the
typography is pixel-identical across all 10 and spelling can never drift.

Idempotent: skips plates whose PNG already exists (delete to regenerate).
"""
import json, os, time, urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
VAULT = "/Users/brooksorradre2/Documents/marketing brain"
TOTE_REFS = os.path.join(VAULT, "brands/velantra/videos/VEL-STRAWTOTE-POV-PACK-01/_product-refs")
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

# ---------------------------------------------------------------- scene (shared)
SCENE = (
    "A vertical studio product photograph. The background is one continuous piece of deep "
    "chocolate brown matte cotton fabric hung and draped as a backdrop, filling the entire frame, "
    "with soft natural vertical folds and gentle creases reading as subtle shadow gradients, "
    "slightly darker toward the edges and corners. The bag stands upright, perfectly centered "
    "left to right, photographed straight on from the front at eye level, its two top handles "
    "standing upright above it. The bag sits in the MIDDLE band of the frame only: the entire top "
    "quarter of the image and the entire bottom quarter of the image are clean empty draped fabric "
    "with nothing in them. Soft diffused studio light from the front, a soft dark contact shadow "
    "pooling directly beneath the bag. Warm neutral color grade, shallow depth of field on the "
    "backdrop folds, crisp focus on the bag."
)
NEG = (
    "There is absolutely no text, no lettering, no words, no captions, no watermark, no logo and no "
    "graphics anywhere in the image. No hands, no people, no body parts, no mannequin, no props, "
    "no furniture, no other bags."
)
MATCH = (
    "The bag in the image is an exact copy of the bag in the first reference image in silhouette, "
    "proportions, construction, materials and details, and every color on the bag matches the first "
    "reference image exactly."
)

# ---------------------------------------------------- Sofia Woven Tote (verbatim skill blocks)
TOTE_IDENTITY = (
    "a structured hand woven straw tote in {straw}, tightly woven straw body with braided cross "
    "stitch trim along the edges, a smooth {leather} leather flap folded over the top of the bag "
    "from the back: the flap is ONE single seamless piece of leather, its front lower edge cut into "
    "the silhouette of a wide center panel with 2 squared outer tabs, the leather fully continuous "
    "and unbroken between and above these shapes, with exactly 2 narrow slots through which the "
    "handles pass, two rolled {leather} leather top handles, two {leather} leather belt straps "
    "crossed on the front, white contrast stitching on all leather edges, no metal hardware, no "
    "logos. The leather flap, tabs and belt straps exist ONLY on the FRONT face of the bag, the back "
    "face is plain woven straw, no duplicated front detailing on any other face."
)

TOTE_FLAP = (
    "Flap and opening construction: the {leather} leather flap is ONE single seamless sheet of "
    "leather attached along the top rear edge of the tote and folded all the way forward over the "
    "front, lying completely flat. Its front lower edge is cut into the shape of a wide center panel "
    "and 2 squared outer tabs, but these are shapes cut into the SAME single sheet, never separate "
    "pieces. The leather is continuous and unbroken between the shapes and across the entire top of "
    "the bag, including between the two handle slots. The only openings anywhere in the flap are the "
    "2 narrow handle slots. No gap, no seam, no split, no opening exists anywhere else in the flap, "
    "and nothing behind or inside the bag is ever visible through the flap. The flap never splits "
    "into pieces, never lifts, never stands up, always folded all the way over. The 2 {leather} "
    "leather belt straps lie crossed in an X over the front below the flap with rounded ends and "
    "white contrast stitching, exactly as on the closed reference bag. No metal hardware anywhere "
    "on the bag."
)

# straw body is natural tan on every colorway; only the leather elements change
TOTE_COLORS = {
    "caramel":          ("warm natural sandy tan straw", "warm caramel tan"),
    "sky-blue":         ("warm natural sandy tan straw", "bright sky blue"),
    "lightning-orange": ("warm natural sandy tan straw", "vivid bright orange"),
    "light-chocolate":  ("warm natural sandy tan straw", "medium chocolate brown"),
    "lady-pink":        ("warm natural sandy tan straw", "soft rose pink"),
    "cream":            ("warm natural sandy tan straw", "cream ivory white"),
    "sunny-yellow":     ("warm natural sandy tan straw", "golden sunny yellow"),
    "caban-black":      ("warm natural sandy tan straw", "deep true black"),
}

# ---------------------------------------------------- Eleanor Weekender (verbatim skill block)
WK_IDENTITY = (
    "a structured two tone weekend bag, wider than tall, rich cognac brown leather upper flap "
    "section and two rolled cognac leather top handles over a {canvas} body, a small gold oval turn "
    "lock on the front, two flat gold clasp plates with cognac leather belt straps threaded through "
    "them, a small cognac leather key bell tied to the handle base, cognac leather corner patches at "
    "the bottom, visible stitching, gold hardware, no logos anywhere on the bag, natural cream cotton "
    "canvas interior lining with a cognac leather slip pocket on the back wall"
)
WK_HARDEN = (
    "The bag in frame is an exact copy of the bag in the first reference image in silhouette, "
    "proportions, materials and details, the two rolled top handles are smooth simple leather tubes "
    "with no wrapping, no braiding and no woven texture. The bag is fully closed with its flap down "
    "over the front. The bag has no zipper anywhere and no embossed text or lettering anywhere on it. "
    # skill: GPT i2i drops a handle on attempt 1 — pin both explicitly
    "BOTH handles are clearly visible standing upright above the bag as two separate parallel rolled "
    "leather tubes: the front handle rises from the front leather band and the rear handle rises from "
    "the back leather band directly behind it, with visible space between the two arcs. Never omit "
    "the rear handle. "
    # skill: i2i invented floral tooling on the flap
    "All of the cognac leather is plain smooth grain leather: no embossed pattern, no floral, paisley "
    "or damask tooling, no decorative stamping anywhere on the leather. The canvas is plain woven "
    "canvas with no pattern woven or printed into it."
)
WK_COLORS = {
    "light-chocolate": ("cream ivory woven canvas", "light chocolate 1.webp"),
    "army-green":      ("deep army green twill canvas", "green 1.webp"),
}


def build_jobs():
    jobs = []
    for slug, (straw, leather) in TOTE_COLORS.items():
        ident = TOTE_IDENTITY.format(straw=straw, leather=leather)
        flap = TOTE_FLAP.format(leather=leather)
        prompt = f"{SCENE} The bag: {ident} {flap} {MATCH} {NEG}"
        ref = None
        for ext in ("png", "jpg", "jpeg", "webp"):
            p = os.path.join(TOTE_REFS, slug, f"ref-1.{ext}")
            if os.path.exists(p):
                ref = p
                break
        assert ref, f"no ref for {slug}"
        jobs.append((f"sofia-{slug}", prompt, [ref]))

    for slug, (canvas, fname) in WK_COLORS.items():
        ident = WK_IDENTITY.format(canvas=canvas)
        prompt = f"{SCENE} The bag: {ident} {WK_HARDEN} {MATCH} {NEG}"
        jobs.append((f"eleanor-{slug}", prompt, [os.path.join(WK_REFS, fname)]))
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
             "-F", "uploadPath=back-in-stock",
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
    jobs = [j for j in build_jobs() if not os.path.exists(os.path.join(OUT, f"{j[0]}.png"))]
    if not jobs:
        print("all plates exist, nothing to do")
        return

    cache = {}
    for _, _, refs in jobs:
        for r in refs:
            if r not in cache:
                cache[r] = upload(r)

    tasks = {}
    for sid, prompt, refs in jobs:
        payload = {"model": "gpt-image-2-image-to-image",
                   "input": {"prompt": prompt,
                             "input_urls": [cache[r] for r in refs],
                             "aspect_ratio": "9:16",
                             "resolution": "2K"}}
        d = api(f"{API}/jobs/createTask", payload, H)
        if d.get("code") != 200:
            payload["input"]["resolution"] = "1K"
            d = api(f"{API}/jobs/createTask", payload, H)
        if d.get("code") != 200:
            payload["input"]["aspect_ratio"] = "2:3"
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
    print(f"plates on disk: {len(have)}/10 -> {have}", flush=True)


if __name__ == "__main__":
    main()
