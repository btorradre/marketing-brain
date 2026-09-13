#!/usr/bin/env python3
"""Colette pre-order statics — text-free plates via kie.ai GPT Image 2 i2i.

6 Vestirsi-swipe concepts, fall mood, anchored on the approved v3 canonicals
(real-photo-anchor law). Text is NEVER generated — compose_ads.py overlays it.

Idempotent: skips plates whose PNG already exists (delete to regenerate).
"""
import json, os, time, urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
VAULT = "/Users/brooksorradre2/Documents/marketing brain"
PREF = os.path.join(VAULT, "brands/velantra/products/cashmere-tote/product-references")
PIMG = os.path.join(VAULT, "brands/velantra/products/cashmere-tote/product-images/system-oat-greige")
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

CARAMEL = os.path.join(PREF, "colette-canonical-caramel-v3.png")
ESPRESSO = os.path.join(PIMG, "colette-v3-espresso-hero.png")

# ---------------------------------------------------------------- identity
IDENT = (
    "The bag is a large structured tote in pale oatmeal greige brushed wool felt. The wool "
    "surface is a soft matte melange brushed felt exactly like a brushed wool coat: smooth, "
    "NOT knitted, no knit ribs, no visible yarn loops, no chunky weave. Two long rolled top "
    "handles: the lower half of each handle is wrapped in the same oatmeal wool, the upper "
    "arc is smooth {trim} leather. Vertical oatmeal wool straps run down the faces of the "
    "bag. A thin half-inch smooth {trim} leather belt is threaded horizontally through wool "
    "loops around the upper body of the bag; the two free ends of the belt curve outward and "
    "downward away from the bag, and each belt end is capped with a small round polished "
    "gold disc. No other metal hardware, no logos, no zippers, no embossing, tone-on-tone "
    "stitching only."
)
CAR = IDENT.format(trim="warm caramel cognac tan")
ESP = IDENT.format(trim="deep espresso dark brown")

MATCH = (
    "The bag in the image is an exact copy of the bag in the first reference image in "
    "silhouette, proportions, construction, materials and details, and every color on the "
    "bag matches the first reference image exactly."
)
NEG = (
    "There is absolutely no text, no lettering, no words, no captions, no watermark, no "
    "logo and no graphics anywhere in the image, and no readable text on any object. "
)
REAL = (
    "This is a real photograph shot on a full-frame camera with natural photographic "
    "lighting, true fabric imperfections and subtle film grain. It must never look like a "
    "3D render, CGI, illustration or product visualization."
)
NOPPL = "No hands, no people, no body parts, no mannequin, no furniture, no other bags. "
HANDLES = (
    "BOTH rolled top handles are clearly visible standing upright above the bag as two "
    "separate parallel arcs with visible space between them; never omit the rear handle. "
)

# ---------------------------------------------------------------- scenes
A_DUO = (
    "A vertical studio product photograph for a luxury handbag campaign, autumn mood. The "
    "background is a seamless warm deep greige taupe studio backdrop with a soft vignette, "
    "lit like late afternoon window light, warm and soft. TWO large wool totes of identical "
    "design stand upright on the seamless floor, staggered: one slightly forward and left, "
    "the other just behind it to the right, partially overlapped, both photographed straight "
    "on at eye level. The forward bag is an exact copy of the bag in the FIRST reference "
    "image with warm caramel cognac tan leather trim. The rear bag is an exact copy of the "
    "bag in the SECOND reference image with deep espresso dark brown leather trim. The two "
    "bags differ ONLY in leather trim color; both wool bodies are the same pale oatmeal. "
    + HANDLES +
    "The bags sit in the lower two thirds of the frame; the entire top third is clean empty "
    "backdrop with nothing in it. Soft contact shadows pool beneath the bags. Warm neutral "
    "autumn color grade, crisp focus on both bags. "
)
B_MODEL = (
    "A vertical editorial fashion photograph, camera directly behind the subject: a woman "
    "seen from the back, soft dark honey hair falling past her shoulders, wearing an "
    "oversized camel wool coat over cream knitwear and straight-leg trousers, standing in a "
    "bright warm studio against a pale warm ivory-grey seamless backdrop, soft autumn window "
    "light. Her head is turned very slightly so only a sliver of cheek shows, face not "
    "visible. A large oatmeal wool tote hangs from her right shoulder on its long rolled "
    "handles, resting against her hip, its front face with the thin caramel leather belt "
    "turned fully toward the camera. Her arm hangs relaxed beside it. The woman and bag "
    "fill the central band of the frame with generous clean headroom above her head. "
    "Natural realistic skin, subtle film grain, softly diffused focus, nothing tack sharp. "
    "Warm quiet-luxury editorial grade. "
)
C_DARK = (
    "A vertical moody studio product photograph. The entire background and floor are one "
    "continuous deep dark chocolate espresso brown seamless backdrop, softly lit by one warm "
    "low spotlight from the upper front that creates a gentle pool of light around the bag "
    "and falls off to near-black in the corners. The pale oatmeal wool tote stands upright, "
    "turned at a slight three-quarter angle, its brushed wool glowing warmly against the "
    "dark ground, caramel leather belt catching the light. " + HANDLES + NOPPL +
    "The bag sits in the lower sixty percent of the frame; the entire top forty percent is "
    "clean dark backdrop with nothing in it. Rich warm autumn grade, crisp focus on the bag. "
)
D_LIFE = (
    "A vertical editorial street-style crop photographed indoors by a large window: a woman "
    "cropped from chin to mid-thigh, no face visible, wearing a plush textured taupe brown "
    "teddy wool coat over dark straight trousers, arms loosely crossed in front of her. A "
    "large oatmeal wool tote with deep espresso dark brown leather trim hangs from her "
    "shoulder beside her arm, its front face with the thin espresso leather belt turned "
    "toward the camera. Softly blurred warm neutral interior background, soft autumn light, "
    "natural realistic skin on her hands, subtle film grain, softly diffused focus. The "
    "woman stands center-right; the lower left area of the frame stays visually calm. "
)
E_INSIDE = (
    "A vertical studio still life on a warm rosy taupe-brown seamless backdrop and matching "
    "surface, moody warm light. The pale oatmeal wool tote stands upright photographed from "
    "a slightly elevated three-quarter angle so its open top is visible. Inside the open "
    "top, neatly visible: the top edge of a plain dark hardcover book, a folded cream "
    "chunky-knit sweater peeking over the rim, a pair of dark brown oval sunglasses resting "
    "on the sweater, and a small plain white unbranded cosmetic tube. Every object is "
    "completely unbranded with no readable text anywhere. The handles rest naturally, both "
    "visible. " + NOPPL +
    "The bag and contents sit in the lower two thirds of the frame; the entire top third is "
    "clean empty backdrop. Soft contact shadow, warm autumn grade, crisp focus. "
)
F_FLAT = (
    "A vertical top-down flat lay photographed from directly above. The entire surface is a "
    "deep chocolate brown soft wool blanket with gentle natural folds filling the whole "
    "frame. The pale oatmeal wool tote lies flat on the blanket in the lower two thirds of "
    "the frame, its opening pointing toward the top of the frame, its caramel leather belt "
    "and gold disc caps visible on its front face. Spilling slightly from the open top: a "
    "pair of dark oval sunglasses, a plain dark hardcover book, and the cuff of a folded "
    "cream chunky-knit sweater, all completely unbranded with no readable text. " + NOPPL +
    "The entire top quarter of the frame is clean empty blanket with nothing in it. Soft "
    "even warm light, natural shadows in the blanket folds, warm autumn grade. "
)

JOBS = [
    ("a-duo-916",    A_DUO + NOPPL + NEG + REAL,            [CARAMEL, ESPRESSO], "9:16"),
    ("a-duo-45",     A_DUO + NOPPL + NEG + REAL,            [CARAMEL, ESPRESSO], "4:5"),
    ("b-model-916",  B_MODEL + CAR + " " + MATCH + " " + NEG + REAL, [CARAMEL], "9:16"),
    ("b-model-45",   B_MODEL + CAR + " " + MATCH + " " + NEG + REAL, [CARAMEL], "4:5"),
    ("c-dark-916",   C_DARK + CAR + " " + MATCH + " " + NEG + REAL,  [CARAMEL], "9:16"),
    ("c-dark-45",    C_DARK + CAR + " " + MATCH + " " + NEG + REAL,  [CARAMEL], "4:5"),
    ("d-life-45",    D_LIFE + ESP + " " + MATCH + " " + NEG + REAL,  [ESPRESSO], "4:5"),
    ("e-inside-916", E_INSIDE + CAR + " " + MATCH + " " + NEG + REAL, [CARAMEL], "9:16"),
    ("e-inside-45",  E_INSIDE + CAR + " " + MATCH + " " + NEG + REAL, [CARAMEL], "4:5"),
    ("f-flat-916",   F_FLAT + CAR + " " + MATCH + " " + NEG + REAL,  [CARAMEL], "9:16"),
    ("f-flat-45",    F_FLAT + CAR + " " + MATCH + " " + NEG + REAL,  [CARAMEL], "4:5"),
]


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
             "-F", "uploadPath=colette-preorder",
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
    jobs = [j for j in JOBS if not os.path.exists(os.path.join(OUT, f"{j[0]}.png"))]
    if not jobs:
        print("all plates exist, nothing to do")
        return

    cache = {}
    for _, _, refs, _ in jobs:
        for r in refs:
            if r not in cache:
                cache[r] = upload(r)

    tasks = {}
    for sid, prompt, refs, ratio in jobs:
        payload = {"model": "gpt-image-2-image-to-image",
                   "input": {"prompt": prompt,
                             "input_urls": [cache[r] for r in refs],
                             "aspect_ratio": ratio,
                             "resolution": "2K"}}
        d = api(f"{API}/jobs/createTask", payload, H)
        if d.get("code") != 200:
            payload["input"]["resolution"] = "1K"
            d = api(f"{API}/jobs/createTask", payload, H)
        if d.get("code") != 200:
            payload["input"]["aspect_ratio"] = "2:3" if ratio == "9:16" else "4:5"
            d = api(f"{API}/jobs/createTask", payload, H)
        assert d.get("code") == 200, f"{sid} createTask failed: {d}"
        tasks[sid] = d["data"]["taskId"]
        print(f"{sid}: task {tasks[sid]}", flush=True)

    pending = dict(tasks)
    deadline = time.time() + 2400
    while pending and time.time() < deadline:
        time.sleep(15)
        for sid, tid in list(pending.items()):
            try:
                d = api(f"{API}/jobs/recordInfo?taskId={tid}", None, H)
            except Exception as e:
                print(f"{sid}: poll error {e}, will retry", flush=True)
                continue
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
        print(f"TIMEOUT pending: {json.dumps(pending)}", flush=True)
    have = sorted(f[:-4] for f in os.listdir(OUT) if f.endswith(".png"))
    print(f"plates on disk: {len(have)}/{len(JOBS)} -> {have}", flush=True)


if __name__ == "__main__":
    main()
