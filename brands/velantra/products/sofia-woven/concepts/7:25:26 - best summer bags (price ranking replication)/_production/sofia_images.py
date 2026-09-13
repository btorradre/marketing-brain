#!/usr/bin/env python3
"""VEL-SOFIA-BEST-01 — Sofia keyframe generation via GPT Image 2 i2i on kie.ai.

  sofia_images.py prompts        print assembled prompts, no API calls
  sofia_images.py images [K01..] submit i2i jobs (~10 cr each)
  sofia_images.py poll           poll + download into ../assets/sofia/

Resume-safe: `images` skips anything already downloaded.

Style law for this concept: every Sofia frame must read as BRAND CAMPAIGN
photography, matching the polish of the competitor PDP stills it is cut against.
If the Sofia looks like scrappy UGC next to Prada's studio lighting, the
comparison is lost visually before the VO ever lands.
"""
import json, os, ssl, subprocess, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "assets", "sofia"))
STATE_PATH = os.path.join(HERE, "state.json")
API = "https://api.kie.ai/api/v1/jobs"
UPLOAD_URL = "https://kieai.redpandaai.co/api/file-stream-upload"
IMG_MODEL = "gpt-image-2-image-to-image"
CARAMEL = ("/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/"
           "straw-birkin/product-images/straw birkin/caramel 1.png")
KEY = None

# ---------------------------------------------------------------- locked blocks
IDENTITY = (
    "a structured hand woven straw tote in warm sandy caramel, tightly woven straw body with "
    "braided cross stitch trim along the edges, a smooth taupe leather flap folded over the top "
    "of the bag from the back: the flap is ONE single seamless piece of leather, its front lower "
    "edge cut into the silhouette of a wide center panel with 2 squared outer tabs, the leather "
    "fully continuous and unbroken between and above these shapes, with exactly 2 narrow slots "
    "through which the handles pass, two rolled taupe leather top handles, two taupe leather belt "
    "straps crossed on the front, white contrast stitching on all leather edges, no metal hardware, "
    "no logos. The leather flap, tabs and belt straps exist ONLY on the FRONT face of the bag, the "
    "back face is plain woven straw, no duplicated front detailing on any other face."
)

FLAP = (
    "Flap and opening construction: the taupe leather flap is ONE single seamless sheet of leather "
    "attached along the top rear edge of the tote and folded all the way forward over the front, "
    "lying completely flat and fully closed. Its front lower edge is cut into the shape of a wide "
    "center panel and 2 squared outer tabs, but these are shapes cut into the SAME single sheet, "
    "never separate pieces. The leather is continuous and unbroken between the shapes and across "
    "the entire top of the bag, including between the two handle slots. The only openings anywhere "
    "in the flap are the 2 narrow handle slots. No gap, no seam, no split, no opening exists "
    "anywhere else in the flap, and nothing behind or inside the bag is ever visible through the "
    "flap. The flap never splits into pieces, never lifts, never stands up, always folded all the "
    "way over. The bag is completely empty and closed, no objects in or near it, and no hand "
    "touches or works the flap or the belt straps."
)

PROPORTION = (
    "Bag proportions stay exactly as in the reference image: the body is wider than it is tall, "
    "width to height about 1.18 to 1, widest at the base with a gentle inward taper and soft straw "
    "side wings. Never stretch it taller or pinch the shoulders. The bag has ONLY the two rolled "
    "top handles, it has no shoulder strap and no crossbody strap of any kind, never add one."
)

COLOUR = (
    "Colour lock: every colour matches the first reference image exactly. The straw body is warm "
    "sandy caramel natural straw, the leather is taupe, never grey, never washed out. Strap lock: "
    "EXACTLY 2 belt straps on the front crossed in a symmetric X, never a lattice, never a third strap."
)

FOOTER = (
    "Shot as premium brand campaign photography on a full frame camera, editorial product lighting, "
    "clean and expensive looking, shallow depth of field, natural summer daylight, crisp focus on "
    "the bag. Vertical 9:16 composition. No text, no logos, no watermarks, no people's faces in frame."
)

# name, scene
KEYFRAMES = [
    ("BEST-K01-sofia-hero",
     "The tote stands upright and perfectly centered on a smooth sunlit off white plaster surface "
     "against a soft neutral cream backdrop, shot straight on at bag height, the whole bag fully in "
     "frame with generous clean space above and below it. Soft directional daylight from the right "
     "rakes across the weave and picks out its texture, gentle natural shadow pooling to the left."),

    ("BEST-K02-sofia-macro-weave",
     "Extreme close macro filling the frame with the tightly woven caramel straw body and the "
     "braided cross stitch trim running along the top edge, every individual straw strand sharp and "
     "dense, the taupe leather flap edge entering the top of frame. Warm raking daylight across the "
     "texture, background completely out of focus."),

    ("BEST-K03-sofia-macro-stitch",
     "Extreme close macro on the taupe leather flap edge and one crossed belt strap, filling the "
     "frame, the white contrast stitching running crisply along the leather edges in sharp focus, "
     "the woven straw visible softly behind it. No metal hardware anywhere in frame."),

    ("BEST-K04-sofia-carried",
     "A woman carries the tote by both rolled top handles at her side as she walks, framed from the "
     "shoulders down so no face is visible, wearing a simple cream linen summer dress, warm "
     "Mediterranean daylight, a soft out of focus pale stone wall behind her. The bag hangs closed "
     "and upright and is the sharpest thing in frame."),

    # --- "it fits everything" — the ONLY carrying frame. Uses CARRY block, not the closed pin.
    ("BEST-K05-sofia-fits-everything",
     "The tote stands upright on a sunlit pale wooden table, packed for a summer day: a rolled "
     "striped towel, a straw sun hat brim, a paperback and a pair of tortoiseshell sunglasses lean "
     "out of the open woven mouth at the BACK of the bag, behind the leather flap. Shot straight on "
     "at bag height, warm late afternoon daylight from the right.",
     "carry"),

    ("BEST-K06-sofia-goes-with-everything",
     "The tote rests on a pale linen upholstered chair beside a folded cream linen blazer and a pair "
     "of tan leather sandals, styled like an outfit laid out for the day, shot from slightly above at "
     "a three quarter angle. Soft diffused window daylight, calm neutral palette, the bag closed and "
     "upright and clearly the hero of the frame."),

    ("BEST-K07-sofia-three-quarter",
     "The tote sits on a sunlit pale plaster ledge photographed from a three quarter front angle so "
     "both the front face and one woven side wing are visible, showing the structure and depth of "
     "the bag. Soft directional daylight from the left, clean neutral cream backdrop, gentle shadow."),
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


# Carrying variant of the flap block. Generators poke contents THROUGH the flap or split it into
# floating tabs — this is the exact failure the skill's flap law exists to prevent. Never use the
# closed-and-empty pin on a frame with contents, and never use this one on a frame without.
FLAP_CARRY = (
    "Flap and opening construction: the taupe leather flap is ONE single seamless sheet of leather "
    "attached along the top rear edge of the tote and folded all the way forward over the front, "
    "lying completely flat. Its front lower edge is cut into the shape of a wide center panel and 2 "
    "squared outer tabs, but these are shapes cut into the SAME single sheet, never separate pieces. "
    "The leather is continuous and unbroken between the shapes and across the entire top of the bag, "
    "including between the two handle slots. The only openings anywhere in the flap are the 2 narrow "
    "handle slots. No gap, no seam, no split, no opening exists anywhere else in the flap. The flap "
    "never splits into pieces, never lifts, never stands up, always folded all the way over. The "
    "woven mouth of the tote opens BEHIND the flap: every item leans out of that open mouth at the "
    "BACK of the bag, behind the leather flap, and nothing ever passes through, between or over the "
    "flap. Nothing inside the bag is ever visible through the flap. The 2 taupe leather belt straps "
    "lie crossed in an X over the front below the flap, never threaded through the flap and never "
    "wrapped around the contents. No metal hardware anywhere on the bag."
)


def prompt_for(scene, mode="closed"):
    flap = FLAP_CARRY if mode == "carry" else FLAP
    return f"{scene}\n\nThe bag is {IDENTITY}\n\n{flap}\n\n{PROPORTION}\n\n{COLOUR}\n\n{FOOTER}"


def credits():
    req = urllib.request.Request("https://api.kie.ai/api/v1/chat/credit",
                                 headers={"Authorization": f"Bearer {KEY}"})
    with urllib.request.urlopen(req, context=ctx(), timeout=60) as r:
        return json.loads(r.read().decode(), strict=False).get("data")


def state():
    return json.load(open(STATE_PATH)) if os.path.exists(STATE_PATH) else {"uploads": {}, "images": {}}


def save(st):
    json.dump(st, open(STATE_PATH, "w"), indent=1)


def api(path, payload=None):
    data = json.dumps(payload).encode() if payload else None
    req = urllib.request.Request(API + path, data=data, headers={
        "Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, context=ctx(), timeout=120) as r:
        return json.loads(r.read().decode(), strict=False)


def upload_file(path):
    """kie file upload 403s via urllib — curl -F is the working path."""
    last = ""
    for attempt in range(4):
        if attempt:
            time.sleep(10 * attempt)
        out = subprocess.run(
            ["curl", "-s", "-X", "POST", UPLOAD_URL,
             "-H", f"Authorization: Bearer {KEY}",
             "-F", f"file=@{path}",
             "-F", "uploadPath=velantra-sofia-worst",
             "-F", f"fileName={int(time.time())}-caramel-ref.png"],
            capture_output=True, text=True)
        try:
            resp = json.loads(out.stdout)
        except ValueError:
            last = out.stdout or out.stderr
            continue
        if resp.get("data", {}).get("downloadUrl"):
            return resp["data"]["downloadUrl"]
        last = out.stdout
    raise RuntimeError(f"upload failed: {last[:300]}")


def ref_url():
    st = state()
    if not st["uploads"].get("caramel"):
        st["uploads"]["caramel"] = upload_file(CARAMEL)
        save(st)
        print(f"uploaded caramel ref: {st['uploads']['caramel']}")
    return st["uploads"]["caramel"]


def cmd_prompts(ids):
    for kf in KEYFRAMES:
        name, scene, mode = (kf + ("closed",))[:3]
        if ids and not any(i in name for i in ids):
            continue
        print(f"===== {name} ({mode}) =====\n{prompt_for(scene, mode)}\n")


def cmd_images(ids):
    st = state()
    ref = ref_url()
    print(f"credits: {credits()}")
    for kf in KEYFRAMES:
        name, scene, mode = (kf + ("closed",))[:3]
        if ids and not any(i in name for i in ids):
            continue
        if os.path.exists(os.path.join(OUT, f"{name}.png")):
            print(f"{name}: already downloaded, skipping")
            continue
        payload = {"model": IMG_MODEL, "input": {
            "prompt": prompt_for(scene, mode),
            "input_urls": [ref],
            "aspect_ratio": "9:16",
            "resolution": "2K"}}
        r = api("/createTask", payload)
        if r.get("code") != 200:
            print(f"{name} CREATE FAIL: {r}")
            continue
        st["images"][name] = {"taskId": r["data"]["taskId"], "state": "created"}
        print(f"{name} -> task {r['data']['taskId']}")
        save(st)
        time.sleep(4)          # createTask rate-limits: pace submits ~4s apart


def cmd_poll():
    st = state()
    pending = {k: v for k, v in st["images"].items() if v.get("state") != "success"}
    if not pending:
        print("nothing pending")
        return
    os.makedirs(OUT, exist_ok=True)
    deadline = time.time() + 25 * 60
    while pending and time.time() < deadline:
        for name in list(pending):
            rec = st["images"][name]
            try:
                d = (api(f"/recordInfo?taskId={rec['taskId']}").get("data") or {})
            except Exception as e:
                print(f"{name} poll error {e}")
                continue
            rec["state"] = d.get("state")
            if d.get("state") == "success":
                res = json.loads(d.get("resultJson") or "{}", strict=False)
                urls = res.get("resultUrls") or []
                if urls:
                    rec["resultUrl"] = urls[0]
                    dest = os.path.join(OUT, f"{name}.png")
                    subprocess.run(["curl", "-sL", "--fail", "-o", dest, urls[0]], check=False)
                    print(f"{name}: downloaded -> {dest}")
                pending.pop(name, None)
            elif d.get("state") == "fail":
                print(f"{name}: FAILED {d.get('failMsg')}")
                pending.pop(name, None)
            save(st)
        if pending:
            time.sleep(15)
    save(st)


if __name__ == "__main__":
    load_key()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    ids = sys.argv[2:]
    if cmd == "prompts":
        cmd_prompts(ids)
    elif cmd == "images":
        cmd_images(ids)
    elif cmd == "poll":
        cmd_poll()
    else:
        print(f"credits: {credits()}")
        print(json.dumps(state().get("images", {}), indent=1))
