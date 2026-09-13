#!/usr/bin/env python3
"""VEL-MARGOT-BEST-01 — Margot keyframe generation via GPT Image 2 i2i on kie.ai.

  margot_images.py prompts        print assembled prompts, no API calls
  margot_images.py images [K01..] submit i2i jobs (~10 cr each)
  margot_images.py poll           poll + download into ../assets/margot/

Resume-safe: `images` skips anything already downloaded.

Style law for this concept (inherited from VEL-SOFIA-BEST-01): every Margot
frame must read as BRAND CAMPAIGN photography, matching the polish of the
competitor PDP stills it is cut against (The Row, Polene, Cuyana, Longchamp).
If the Margot looks like scrappy UGC next to The Row's studio lighting, the
comparison is lost visually before the VO ever lands.

Seeded from the LIVE burgundy PDP hero on the Shopify CDN — no upload needed.
"""
import json, os, ssl, subprocess, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "assets", "margot"))
STATE_PATH = os.path.join(HERE, "state.json")
API = "https://api.kie.ai/api/v1/jobs"
IMG_MODEL = "gpt-image-2-image-to-image"
MARGOT_HERO = ("https://cdn.shopify.com/s/files/1/0627/4092/2433/files/"
               "margot-burgundy-hero.jpg?v=1784826552")
KEY = None

# ---------------------------------------------------------------- locked blocks
IDENTITY = (
    "the exact Velantra Margot leather tote from the reference image, every colour and detail matching the "
    "reference exactly: a softly structured open top tote in deep burgundy wine leather with a fine embossed "
    "swirling grain texture across every panel, never plain smooth leather and never a classic round pebble "
    "grain. The body is clearly wider than it is tall, the top edge wider than the base with a gentle inward "
    "taper, soft folded accordion gussets on each side. Two slim flat burgundy leather top handles. A single "
    "horizontal burgundy leather belt strap runs across the upper front through one small polished silver "
    "rectangular keeper at each side, its two strap ends angling down toward the centre in a shallow open V, "
    "each end finished with a polished silver slotted clasp plate, both loose ends hanging free and NOT "
    "fastened. Centred on the front panel above the V sits one small square polished silver turn lock plate "
    "with a small vertical toggle. Four small silver feet under the base. The top is open with no flap and no "
    "top zipper. The bag has ONLY the two flat top handles, no shoulder strap and no crossbody strap of any "
    "kind, never add one. No logos, no text anywhere on the bag.")

COLOUR = (
    "Colour lock: the leather is deep burgundy wine exactly as the reference image, never brown, never black, "
    "never bright red, and the fine embossed swirling grain stays visible. ALL hardware is polished silver, "
    "never gold, never brass. EXACTLY 1 horizontal belt strap, EXACTLY 2 silver slotted clasp plate ends "
    "hanging in an open V, EXACTLY 1 small square silver turn lock plate. The bag holds its structured shape "
    "and never slumps.")

NEVER = (
    "Never: no gold or brass hardware. No logos, no brand names, no text, no lettering anywhere. No shoulder "
    "strap added. No flap added over the top. No second belt strap, no extra clasp plates or turn locks. The "
    "bag never slumps or collapses. No people's faces anywhere in frame.")

STYLE = (
    "Luxury brand campaign photography, editorial product still, shot on medium format, soft directional "
    "daylight, shallow depth of field, warm neutral palette, clean and quiet styling, high polish. Vertical "
    "9:16.")

# ---------------------------------------------------------------- frames
FRAMES = [
    ("WORK-K01-margot-hero",
     "The bag stands upright and perfectly composed on a warm honed limestone surface against a softly lit "
     "warm plaster wall, front face square to camera, belt strap and turn lock clearly visible, generous "
     "negative space above."),
    ("WORK-K02-margot-macro-grain",
     "Extreme macro close up of the bag's front panel: the grain is a fine DENSE swirling embossed pattern "
     "of tiny curved ridges and swirls exactly as in the reference image, never round pebble bumps, filling "
     "the frame with raking soft light across it, the edge of the belt strap and one silver keeper entering "
     "frame at the side, tack sharp."),
    ("WORK-K03-margot-macro-lock",
     "Tight macro of the front centre of the bag: the small square polished silver turn lock plate with its "
     "vertical toggle, and below it the two silver slotted clasp plate strap ends hanging in their shallow "
     "open V, the embossed grain readable around them, tack sharp."),
    ("WORK-K04-margot-laptop",
     "Top down three quarter view into the open top of the bag standing on a desk: a slim closed silver "
     "laptop and a hardcover planner sit upright inside the soft tan interior, the bag holding its structured "
     "shape perfectly around them, handles parted to the sides, nothing poking above the top edge except the "
     "laptop's top centimetres."),
    ("WORK-K05-margot-desk",
     "The bag stands on a pale oak desk beside a closed laptop and a small ceramic cup in a bright minimal "
     "home office, a camel blazer draped over the chair back behind it, morning light from a window at the "
     "side, the bag's front face with belt and turn lock toward camera. Every piece of hardware is polished "
     "mirror finish silver METAL with realistic metallic reflections, never white, never matte, never "
     "plastic, and the two slotted clasp plates hang in a shallow open V below the square turn lock."),
    ("WORK-K06-margot-carried",
     "The bag carried at a woman's side by both flat top handles, her hand gripping both handles together, "
     "cropped from shoulder to knee so no face is in frame, ivory silk shirt and tailored charcoal trousers, "
     "walking past a warm plaster wall, the bag's front face toward camera."),
    ("WORK-K07-margot-three-quarter",
     "The bag standing on the honed limestone surface turned to a three quarter angle showing the front face "
     "and one soft accordion side gusset, the trapezoid silhouette and depth clearly readable, soft daylight, "
     "generous negative space."),
]


def ctx():
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


def load_key():
    global KEY
    for line in open("/Users/brooksorradre2/Documents/marketing brain/.env"):
        if line.startswith("KIE_API_KEY="):
            KEY = line.strip().split("=", 1)[1]
    assert KEY, "KIE_API_KEY not found"


def state():
    return json.load(open(STATE_PATH)) if os.path.exists(STATE_PATH) else {"images": {}}


def save(st):
    json.dump(st, open(STATE_PATH, "w"), indent=1)


def api(path, payload=None):
    data = json.dumps(payload).encode() if payload else None
    req = urllib.request.Request(API + path, data=data, headers={
        "Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, context=ctx(), timeout=120) as r:
        return json.loads(r.read().decode(), strict=False)


def download(url, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    out = subprocess.run(["curl", "-sL", "--fail", "-A", "Mozilla/5.0", "-o", dest, url],
                         capture_output=True, text=True)
    if out.returncode != 0 or not os.path.getsize(dest):
        raise RuntimeError(f"download failed for {url}")


def prompt_for(blocking):
    return " ".join([blocking, f"The bag is {IDENTITY}", COLOUR, STYLE, NEVER])


def cmd_prompts():
    for name, blocking in FRAMES:
        print(f"===== {name} =====\n{prompt_for(blocking)}\n")


def cmd_images(ids):
    st = state()
    for name, blocking in FRAMES:
        if ids and not any(x in name for x in ids):
            continue
        if os.path.exists(os.path.join(OUT, f"{name}.png")):
            print(f"{name}: already downloaded, skipping")
            continue
        payload = {"model": IMG_MODEL, "input": {
            "prompt": prompt_for(blocking),
            "input_urls": [MARGOT_HERO],
            "aspect_ratio": "9:16",
            "resolution": "2K"}}
        r = api("/createTask", payload)
        if r.get("code") != 200:
            print(f"{name} CREATE FAIL: {r}")
            continue
        st["images"][name] = {"taskId": r["data"]["taskId"], "state": "created"}
        print(f"{name} task {r['data']['taskId']}")
        save(st)
        time.sleep(4)


def cmd_poll():
    st = state()
    pending = {k: v for k, v in st["images"].items() if v.get("state") not in ("success", "fail")}
    deadline = time.time() + 30 * 60
    while pending and time.time() < deadline:
        for name in list(pending):
            rec = st["images"][name]
            try:
                r = api(f"/recordInfo?taskId={rec['taskId']}")
            except Exception as e:
                print(f"{name} poll error {e}")
                continue
            d = r.get("data") or {}
            rec["state"] = d.get("state")
            if d.get("state") == "success":
                res = json.loads(d.get("resultJson") or "{}", strict=False)
                urls = res.get("resultUrls") or []
                rec["resultUrl"] = urls[0] if urls else None
                if rec["resultUrl"]:
                    dest = os.path.join(OUT, f"{name}.png")
                    download(rec["resultUrl"], dest)
                    print(f"{name} DONE -> {dest}")
                pending.pop(name)
            elif d.get("state") == "fail":
                rec["failMsg"] = d.get("failMsg")
                print(f"{name} FAIL: {d.get('failMsg')}")
                pending.pop(name)
            save(st)
        if pending:
            time.sleep(15)


if __name__ == "__main__":
    load_key()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "prompts"
    {"prompts": cmd_prompts,
     "images": lambda: cmd_images(sys.argv[2:]),
     "poll": cmd_poll}.get(cmd, cmd_prompts)()
