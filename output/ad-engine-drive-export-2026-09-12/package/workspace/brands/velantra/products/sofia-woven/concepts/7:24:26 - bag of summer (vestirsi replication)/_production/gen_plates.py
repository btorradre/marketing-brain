#!/usr/bin/env python3
"""THE BAG OF SUMMER — 8 colorway static plates via kie.ai GPT Image 2 i2i.

Replicates the Vestirsi "THE BAG OF THE SEASON" editorial still-life composition
for the Velantra Straw Tote, one plate per live colorway. Plates are generated
CLEAN (no text) — headline + wordmark are composited locally in overlay.py so
typography and logo are pixel-correct.

Each colorway is anchored on its own live PDP "Hand-held front" hero image so the
leather color is exact. Verbatim identity + flap mechanism blocks in every prompt.
Idempotent: skips colorways whose plate PNG already exists (delete to regen).
"""
import json, os, time, urllib.request, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
VAULT = "/Users/brooksorradre2/Documents/marketing brain"
REF_DIR = os.path.join(ROOT, "refs")
OUT = os.path.join(os.path.dirname(ROOT), "plates")
API = "https://api.kie.ai/api/v1"
UPLOAD = "https://kieai.redpandaai.co/api/file-stream-upload"

KEY = None
with open(os.path.join(VAULT, ".env")) as f:
    for line in f:
        if line.startswith("KIE_API_KEY="):
            KEY = line.split("=", 1)[1].strip()
assert KEY, "KIE_API_KEY not found"
H = {"Authorization": f"Bearer {KEY}"}

# --- LOCKED PRODUCT TRUTH (velantra-straw-tote skill, verbatim; leather color resolved) ---

def identity(leather):
    return (
        f"a structured hand woven straw tote in warm sandy caramel, tightly woven straw body with "
        f"braided cross stitch trim along the edges, a smooth {leather} flap folded over the top of the "
        f"bag from the back: the flap is ONE single seamless piece of leather, its front lower edge cut "
        f"into the silhouette of a wide center panel with 2 squared outer tabs, the leather fully "
        f"continuous and unbroken between and above these shapes, with exactly 2 narrow slots through "
        f"which the handles pass, two rolled {leather} top handles, two {leather} belt straps crossed on "
        f"the front, white contrast stitching on all leather edges, no metal hardware, no logos. The "
        f"leather flap, tabs and belt straps exist ONLY on the FRONT face of the bag, the back face is "
        f"plain woven straw, no duplicated front detailing on any other face."
    )


def flap(leather):
    return (
        f"Flap and opening construction: the {leather} flap is ONE single seamless sheet of leather "
        f"attached along the top rear edge of the tote and folded all the way forward over the front, "
        f"lying completely flat. Its front lower edge is cut into the shape of a wide center panel and 2 "
        f"squared outer tabs, but these are shapes cut into the SAME single sheet, never separate pieces. "
        f"The leather is continuous and unbroken between the shapes and across the entire top of the bag, "
        f"including between the two handle slots. The only openings anywhere in the flap are the 2 narrow "
        f"handle slots. No gap, no seam, no split, no opening exists anywhere else in the flap, and "
        f"nothing behind or inside the bag is ever visible through the flap. The flap never splits into "
        f"pieces, never lifts, never stands up, always folded all the way over. The 2 {leather} belt "
        f"straps lie crossed in an X over the front below the flap with rounded ends and white contrast "
        f"stitching, exactly as on the closed reference bag, never threaded through the flap and never "
        f"wrapped around the contents. No metal hardware anywhere on the bag. "
        f"Belt strap geometry: there are exactly 2 separate {leather} belt straps of equal width on the "
        f"front of the bag below the flap, each ending in a rounded tip with white contrast stitching. "
        f"Reproduce their exact arrangement from the reference image for this colorway and do not "
        f"restyle it: some colorways are photographed with the two straps crossed in a symmetric X, "
        f"others with one strap running level and the second angling down across it. Never more than 2 "
        f"straps, never threaded through the flap, never wrapped around anything."
    )


# --- LOCKED COMPOSITION (Vestirsi skeleton, summer mood) ---

def scene(backdrop):
    return (
        f"A luxury editorial still life product photograph. The background is a seamless studio backdrop "
        f"in two tones. The entire upper half of the frame, from the very top edge all the way down to "
        f"just above the middle of the frame, is one smooth flat continuous wall of {backdrop} spanning "
        f"the full width of the frame from the left edge to the right edge, with absolutely no other "
        f"color, object, shadow or surface intruding into it anywhere. Only below that, in the lower "
        f"half of the frame, does a warm bone cream surface sweep in a soft organic arc from the lower "
        f"left up toward the right, the two tones meeting in one gentle curve just below the midpoint "
        f"of the frame. The tote sits upright on the bone cream surface slightly right "
        f"of center, angled about thirty degrees toward the camera so the leather flap and the two "
        f"crossed belt straps face the viewer, both rolled top handles standing upright, casting a soft "
        f"warm shadow to the left. In the lower left foreground, resting on the same bone cream surface "
        f"in front of and to the left of the tote, sits a small summer still life cluster: a shallow "
        f"round woven straw tray holding a clear plastic takeaway cup of iced coffee with a domed lid and "
        f"condensation beading on the sides, a pair of folded tortoiseshell sunglasses leaning against "
        f"the cup, and a small white tube of sunscreen lying flat beside them. Bright warm summer "
        f"sunlight rakes in from the upper right, crisp edged, casting clean defined shadows. The top "
        f"third of the frame is completely empty backdrop with nothing in it."
    )


MATCH = (
    "The tote is the exact bag shown in the first reference image, matching its construction, "
    "proportions, weave pattern, straw color and leather color exactly. The woven straw body is warm "
    "natural sandy tan, only the leather is colored."
)

STYLE = (
    "Photorealistic high end fashion advertising still life, shot on a full frame camera with an 85mm "
    "lens at f8, sharp focus throughout, warm summer color grade, vertical 9 by 16 composition. "
    "Absolutely no text, no words, no letters, no captions, no watermarks, no logos anywhere in the "
    "image. No people, no hands, no faces. The tote is empty and closed, no food, no bread, no flowers, "
    "nothing inside or leaning out of the bag."
)

# colorway -> (ref file, leather wording, backdrop wording)
COLORWAYS = [
    ("caramel",          "caramel.png",          "warm caramel tan leather",     "deep toasted caramel brown"),
    ("light-chocolate",  "light-chocolate.png",  "medium chocolate brown leather", "rich dark chocolate brown"),
    ("caban-black",      "caban-black.jpg",      "black leather",                "deep charcoal near black"),
    ("cream",            "cream.png",            "soft ivory cream leather",     "warm mid tone sand taupe"),
    ("lightning-orange", "lightning-orange.png", "bright vermillion orange leather", "deep burnt terracotta orange"),
    ("sky-blue",         "sky-blue.png",         "bright azure sky blue leather", "deep azure blue"),
    ("sunny-yellow",     "sunny-yellow.png",     "golden mustard yellow leather", "deep amber ochre"),
    ("lady-pink",        "lady-pink.png",        "dusty rose pink leather",      "deep dusty rose"),
]


def api(url, payload=None, headers=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data,
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
    name = os.path.basename(path).replace(" ", "_")
    last = ""
    for attempt in range(4):
        if attempt:
            time.sleep(20 * attempt)
        out = subprocess.run(
            ["curl", "-s", "-X", "POST", UPLOAD,
             "-H", f"Authorization: Bearer {KEY}",
             "-F", f"file=@{path}",
             "-F", "uploadPath=bag-of-summer",
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
    todo = [c for c in COLORWAYS if not os.path.exists(os.path.join(OUT, f"{c[0]}.png"))]
    for name, _, _, _ in COLORWAYS:
        if not any(t[0] == name for t in todo):
            print(f"{name}: exists, skip", flush=True)
    if not todo:
        print("all plates present", flush=True)
        return

    tasks = {}
    for name, ref, leather, backdrop in todo:
        ref_url = upload(os.path.join(REF_DIR, ref))
        prompt = f"{scene(backdrop)} The bag: {identity(leather)} {flap(leather)} {MATCH} {STYLE}"
        payload = {"model": "gpt-image-2-image-to-image",
                   "input": {"prompt": prompt,
                             "input_urls": [ref_url],
                             "aspect_ratio": "9:16",
                             "resolution": "2K"}}
        d = api(f"{API}/jobs/createTask", payload, H)
        if d.get("code") != 200:
            payload["input"]["resolution"] = "1K"
            d = api(f"{API}/jobs/createTask", payload, H)
        assert d.get("code") == 200, f"{name} createTask failed: {d}"
        tasks[name] = d["data"]["taskId"]
        print(f"{name}: task {tasks[name]}", flush=True)

    pending = dict(tasks)
    deadline = time.time() + 1800
    while pending and time.time() < deadline:
        time.sleep(15)
        for name, tid in list(pending.items()):
            d = api(f"{API}/jobs/recordInfo?taskId={tid}", None, H)
            st = (d.get("data") or {}).get("state")
            if st == "success":
                rj = json.loads(d["data"]["resultJson"], strict=False)
                url = rj["resultUrls"][0]
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=300) as r:
                    blob = r.read()
                with open(os.path.join(OUT, f"{name}.png"), "wb") as f:
                    f.write(blob)
                print(f"{name}: DONE ({len(blob)//1024} KB)", flush=True)
                del pending[name]
            elif st == "fail":
                print(f"{name}: FAILED {(d.get('data') or {}).get('failMsg')}", flush=True)
                del pending[name]
    if pending:
        print(f"TIMEOUT still pending: {list(pending)}", flush=True)
    done = [c[0] for c in COLORWAYS if os.path.exists(os.path.join(OUT, f"{c[0]}.png"))]
    print(f"complete: {len(done)}/8 -> {sorted(done)}", flush=True)


if __name__ == "__main__":
    main()
