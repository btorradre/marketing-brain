#!/usr/bin/env python3
"""Boatkin VO run: generate 13 b-roll keyframes via kie.ai GPT Image 2 i2i.

Uploads canonical refs (temp), fires createTask per shot with the verbatim
identity + flap mechanism blocks, polls, downloads results to keyframes/.
Idempotent: skips shots whose output PNG already exists (delete to regen).
"""
import json, os, sys, time, urllib.request, urllib.error, mimetypes

ROOT = os.path.dirname(os.path.abspath(__file__))
VAULT = "/Users/brooksorradre2/Documents/marketing brain"
REF_DIR = os.path.join(VAULT, "brands/velantra/products/straw-birkin/product-images/straw birkin")
OUT = os.path.join(ROOT, "keyframes")
API = "https://api.kie.ai/api/v1"
UPLOAD = "https://kieai.redpandaai.co/api/file-stream-upload"

# .env
KEY = None
with open(os.path.join(VAULT, ".env")) as f:
    for line in f:
        if line.startswith("KIE_API_KEY="):
            KEY = line.split("=", 1)[1].strip()
assert KEY, "KIE_API_KEY not found"
H = {"Authorization": f"Bearer {KEY}"}

IDENTITY = "a structured hand woven straw tote in warm sandy caramel, tightly woven straw body with braided cross stitch trim along the edges, a smooth taupe leather flap folded over the top of the bag from the back: the flap is ONE single seamless piece of leather, its front lower edge cut into the silhouette of a wide center panel with 2 squared outer tabs, the leather fully continuous and unbroken between and above these shapes, with exactly 2 narrow slots through which the handles pass, two rolled taupe leather top handles, two taupe leather belt straps crossed on the front, white contrast stitching on all leather edges, no metal hardware, no logos. The leather flap, tabs and belt straps exist ONLY on the FRONT face of the bag, the back face is plain woven straw, no duplicated front detailing on any other face."

FLAP = "Flap and opening construction: the taupe leather flap is ONE single seamless sheet of leather attached along the top rear edge of the tote and folded all the way forward over the front, lying completely flat. Its front lower edge is cut into the shape of a wide center panel and 2 squared outer tabs, but these are shapes cut into the SAME single sheet, never separate pieces. The leather is continuous and unbroken between the shapes and across the entire top of the bag, including between the two handle slots. The only openings anywhere in the flap are the 2 narrow handle slots. No gap, no seam, no split, no opening exists anywhere else in the flap, and nothing behind or inside the bag is ever visible through the flap. The flap never splits into pieces, never lifts, never stands up, always folded all the way over. When the tote is carrying things, the woven mouth opens BEHIND the flap: the croissant, baguette or flowers lean out of the open mouth at the back of the bag, behind the leather flap, never through the flap. The 2 taupe leather belt straps lie crossed in an X over the front below the flap with rounded ends and white contrast stitching, exactly as on the closed reference bag, never threaded through the flap and never wrapped around the contents. No metal hardware anywhere on the bag."

STYLE = "Photorealistic editorial lifestyle photography, shot on a full frame camera with a 50mm lens, soft natural coastal light, warm neutral palette, vertical 9 by 16 composition, no on screen text, no captions, no logos, no visible human faces."
MATCH = "The bag is the exact bag shown in the first reference image, matching its construction, proportions, weave pattern, straw color and leather color exactly."

SHOTS = [
    ("K01-hero-studio", "A product photograph of the bag standing on a warm beige plaster pedestal against a soft beige studio wall, gentle morning sunlight casting a long soft shadow across the wall, minimal styling.", ["caramel 1.png"], True),
    ("K02-dock-walk", "A woman seen from behind in a flowing white linen dress walking away down a weathered grey wooden dock in a New England harbor town, carrying the bag in her right hand at her side, moored sailboats and a calm harbor in the soft background.", ["caramel 1.png"], True),
    ("K03-shingle-wall", "A close crop of a woman's hand and forearm holding the bag by both top handles at her side against a weathered grey cedar shingle wall, the edge of a white linen dress visible, no face in frame.", ["caramel 1.png"], True),
    ("K04-weaving-macro", "An extreme macro photograph of an artisan's hands weaving tight rows of warm sandy caramel seagrass straw on the partially finished woven body of the bag, natural fiber texture filling the frame, warm workshop daylight.", ["caramel 1.png"], False),
    ("K05-leather-macro", "An extreme macro photograph of a woman's fingertips resting on the smooth taupe leather flap edge of the bag, white contrast stitching in sharp focus, tightly woven caramel straw texture below, shallow depth of field.", ["caramel 1.png"], True),
    ("K06-porch-chair", "The bag sitting on a weathered white wooden porch chair beside a small table holding a white ceramic coffee cup and tortoiseshell sunglasses, white hydrangeas and a blurred blue ocean horizon behind the porch railing.", ["caramel 1.png"], True),
    ("K07-contents", "The bag sitting on a natural linen bench cushion with a fresh baguette and a small bunch of white wildflowers leaning out of the open woven mouth at the back of the bag, behind the leather flap, soft window light.", ["caramel 1.png", "straw birkin opened.png"], True),
    ("K08-beach-path", "A woman seen from behind cropped at the shoulders wearing a cream flowing dress, carrying the bag through golden beach grass on a sandy dune path, soft ocean light ahead of her.", ["caramel 1.png"], True),
    ("K09-dock-post", "The bag sitting on top of a thick weathered wooden dock post, a New England harbor with moored boats and a grey shingle cottage softly blurred behind it, late afternoon light.", ["caramel 1.png"], True),
    ("K10-ferry-deck", "The bag resting on a glossy white bench on the open deck of a passenger ferry, a coiled navy rope nearby, sunlight sparkling on the water beyond the white railing.", ["caramel 1.png"], True),
    ("K11-cafe-table", "The bag on a rattan bistro chair beside a small marble cafe table holding an iced latte and a woven straw sun hat, dappled morning shade on a coastal village street.", ["caramel 1.png"], True),
    ("K12-colorway-duo", "Two of the bags side by side on a clean white floating shelf against a white wall, the first in warm sandy caramel and the second in the soft sky blue colorway exactly as shown in the second reference image, identical construction, soft even daylight.", ["caramel 1.png", "blue 1.png"], True),
    ("K13-caramel-close", "A three quarter close up of the front of the bag in golden hour light standing on a linen covered table, rolled handles upright, leather flap and crossed belt straps in sharp focus.", ["caramel 1.png"], True),
]


def api(url, payload=None, headers=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers={**(headers or {}), **({"Content-Type": "application/json"} if data else {})})
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
            time.sleep(20 * attempt)
        out = subprocess.run(
            ["curl", "-s", "-X", "POST", UPLOAD,
             "-H", f"Authorization: Bearer {KEY}",
             "-F", f"file=@{path}",
             "-F", "uploadPath=boatkin-vo",
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
        print(f"  upload retry for {name}: {last[:150]}", flush=True)
    raise RuntimeError(f"upload failed for {name}: {last[:300]}")


def main():
    os.makedirs(OUT, exist_ok=True)
    ref_urls = {}
    for _, _, refs, _ in SHOTS:
        for rf in refs:
            if rf not in ref_urls:
                ref_urls[rf] = upload(os.path.join(REF_DIR, rf))

    tasks = {}
    for sid, scene, refs, flap in SHOTS:
        out_path = os.path.join(OUT, f"{sid}.png")
        if os.path.exists(out_path):
            print(f"{sid}: exists, skip", flush=True)
            continue
        prompt = f"{scene} The bag: {IDENTITY} {FLAP if flap else ''} {MATCH} {STYLE}"
        payload = {"model": "gpt-image-2-image-to-image",
                   "input": {"prompt": prompt,
                             "input_urls": [ref_urls[r] for r in refs],
                             "aspect_ratio": "9:16",
                             "resolution": "1K"}}
        d = api(f"{API}/jobs/createTask", payload, H)
        if d.get("code") != 200:
            # fallback aspect if 9:16 rejected
            payload["input"]["aspect_ratio"] = "2:3"
            d = api(f"{API}/jobs/createTask", payload, H)
        assert d.get("code") == 200, f"{sid} createTask failed: {d}"
        tasks[sid] = d["data"]["taskId"]
        print(f"{sid}: task {tasks[sid]}", flush=True)

    pending = dict(tasks)
    deadline = time.time() + 1500
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
        print(f"TIMEOUT still pending: {list(pending)}", flush=True)
    done = [s for s, _, _, _ in SHOTS if os.path.exists(os.path.join(OUT, f"{s}.png"))]
    print(f"complete: {len(done)}/13 -> {sorted(done)}", flush=True)


if __name__ == "__main__":
    main()
