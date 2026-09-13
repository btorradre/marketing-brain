#!/usr/bin/env python3
"""VEL-FOUNDER-TOF-01 B-roll generator.
Phase 1 (default): GPT Image 2 keyframes via kie.ai -> assets/broll/keyframes/
Phase 2 (--animate B00,B03,...): Kling 3.0 i2v on QA-passed keyframes -> assets/broll/clips/
Resumable: state in _production/state.json (task ids, upload cache). Meter credits via /chat/credit.
"""
import json, os, sys, time, subprocess, ssl, urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
CAMP = os.path.dirname(BASE)
VAULT = "/Users/brooksorradre2/Documents/marketing brain"
OUT_KF = os.path.join(CAMP, "assets", "broll", "keyframes")
OUT_CL = os.path.join(CAMP, "assets", "broll", "clips")
STATE_F = os.path.join(BASE, "state.json")
os.makedirs(OUT_KF, exist_ok=True); os.makedirs(OUT_CL, exist_ok=True)

# SSL fix (house law)
try:
    import certifi; os.environ.setdefault("SSL_CERT_FILE", certifi.where())
except Exception: pass

KEY = None
with open(os.path.join(VAULT, ".env")) as f:
    for line in f:
        if line.startswith("KIE_API_KEY="): KEY = line.strip().split("=", 1)[1]
assert KEY, "KIE_API_KEY not found"
API = "https://api.kie.ai/api/v1"
UPLOAD = "https://kieai.redpandaai.co/api/file-stream-upload"

def http(method, url, payload=None):
    import requests
    h = {"Authorization": f"Bearer {KEY}"}
    if payload is not None:
        h["Content-Type"] = "application/json"
        r = requests.post(url, headers=h, json=payload, timeout=90)
    else:
        r = requests.get(url, headers=h, timeout=60)
    return json.loads(r.text, strict=False)

def credit():
    try: return http("GET", f"{API}/chat/credit").get("data", {}).get("credits")
    except Exception: return None

def state_load():
    if os.path.exists(STATE_F):
        with open(STATE_F) as f: return json.load(f)
    return {"uploads": {}, "tasks": {}, "kling": {}}

def state_save(st):
    with open(STATE_F, "w") as f: json.dump(st, f, indent=1)

def upload(path, st):
    if path in st["uploads"]: return st["uploads"][path]
    import requests
    for attempt in range(4):
        try:
            with open(path, "rb") as f:
                r = requests.post(UPLOAD, headers={"Authorization": f"Bearer {KEY}"},
                                  files={"file": (os.path.basename(path).replace(" ", "_"), f)},
                                  data={"uploadPath": "founder-tof"}, timeout=120)
            d = r.json()
            if d.get("code") == 200 and d["data"].get("downloadUrl"):
                st["uploads"][path] = d["data"]["downloadUrl"]; state_save(st)
                print(f"  uploaded {os.path.basename(path)}", flush=True)
                return st["uploads"][path]
        except Exception as e:
            print(f"  upload retry {attempt+1}: {e}", flush=True)
        time.sleep(5)
    sys.exit(f"upload failed: {path}")

def poll(task_id, max_wait=900):
    start = time.time()
    while time.time() - start < max_wait:
        try:
            d = http("GET", f"{API}/jobs/recordInfo?taskId={task_id}")
            stt = d.get("data", {}).get("state")
            if stt == "success":
                rj = json.loads(d["data"].get("resultJson", "{}"), strict=False)
                return rj.get("resultUrls", [None])[0]
            if stt == "fail":
                print(f"  FAIL: {d['data'].get('failMsg')}", flush=True); return None
        except Exception as e:
            print(f"  poll err {e}", flush=True)
        time.sleep(15)
    return None

def download(url, path):
    subprocess.run(["curl", "-s", "-A", "Mozilla/5.0", "-o", path, url], check=True)
    return os.path.getsize(path) > 10000

# ---------- verbatim product-truth blocks ----------
STYLE = ("natural editorial realism with a shot on iPhone feel, warm coastal daylight, soft shadows, "
         "shallow depth of field, true to life color with gentle warmth, no text anywhere in frame, no logos anywhere in frame")

ID_STRAW = ("a structured hand woven straw tote in warm sandy caramel, tightly woven straw body with braided cross stitch trim along the edges, "
    "a smooth taupe leather flap folded over the top of the bag from the back: the flap is ONE single seamless piece of leather, its front lower edge cut into the "
    "silhouette of a wide center panel with 2 squared outer tabs, the leather fully continuous and unbroken between and above these shapes, with exactly 2 narrow slots "
    "through which the handles pass, two rolled taupe leather top handles, two taupe leather belt straps crossed on the front, white contrast stitching on all leather edges, "
    "no metal hardware, no logos. The leather flap, tabs and belt straps exist ONLY on the FRONT face of the bag, the back face is plain woven straw, no duplicated front detailing on any other face.")

FLAP_STRAW = ("Flap and opening construction: the taupe leather flap is ONE single seamless sheet of leather attached along the top rear edge of the tote and folded all the way "
    "forward over the front, lying completely flat. Its front lower edge is cut into the shape of a wide center panel and 2 squared outer tabs, but these are shapes cut into the SAME "
    "single sheet, never separate pieces. The leather is continuous and unbroken between the shapes and across the entire top of the bag, including between the two handle slots. "
    "The only openings anywhere in the flap are the 2 narrow handle slots. No gap, no seam, no split, no opening exists anywhere else in the flap, and nothing behind or inside the bag "
    "is ever visible through the flap. The flap never splits into pieces, never lifts, never stands up, always folded all the way over. When the tote is carrying things, the woven mouth "
    "opens BEHIND the flap: the croissant, baguette or flowers lean out of the open mouth at the back of the bag, behind the leather flap, never through the flap. The 2 taupe leather belt "
    "straps lie crossed in an X over the front below the flap with rounded ends and white contrast stitching, exactly as on the closed reference bag, never threaded through the flap and "
    "never wrapped around the contents. No metal hardware anywhere on the bag.")

FLAP_PIN_VIDEO = ("The leather flap stays ONE single seamless sheet folded all the way over, lying completely flat the entire clip: no gap, seam, or split ever opens anywhere in it, "
    "nothing behind it ever shows through it, and its cut edge shapes never separate into pieces.")

ID_WEEK = ("a structured two tone weekend bag, wider than tall, rich cognac brown leather upper flap section and two rolled cognac leather top handles over a cream ivory woven canvas body, "
    "a small gold oval turn lock on the front, two flat gold clasp plates with cognac leather belt straps threaded through them, a small cognac leather key bell tied to the handle base, "
    "cognac leather corner patches at the bottom, visible stitching, gold hardware, no logos anywhere on the bag, natural cream cotton canvas interior lining with a cognac leather slip pocket on the back wall")

ANTIDRIFT = ("the bag in frame is an exact copy of the bag in the reference image in silhouette, proportions, materials and details, "
    "the two rolled top handles are smooth simple leather tubes with no wrapping, no braiding and no woven texture")

EXACT = "the bag in frame is an exact copy of the bag in the reference image in silhouette, proportions, materials, hardware and details, nothing added and nothing removed"

R = lambda *p: os.path.join(VAULT, *p)
REF_STRAW_CARAMEL = R("brands/velantra/products/straw-birkin/product-images/straw birkin/caramel 1.png")
REF_STRAW_BLUE    = R("brands/velantra/products/straw-birkin/product-images/straw birkin/blue 1.png")
REF_STRAW_BLACK   = R("brands/velantra/products/straw-birkin/product-images/straw birkin/black-colorway/black-tote-1.jpeg")
REF_BOAT          = R("brands/velantra/products/boat-tote/product-images/boat tote/01.jpg")
REF_WEEK          = R("brands/velantra/products/weekender/product-images/product images/light chocolate 1.webp")
REF_MARGOT        = R("brands/velantra/products/meridian/product-references/meridian/coffee brown 2.webp")
SCAM = R("brands/velantra/_shared/creative/coastal-brand-films-2026-07/VEL-SCAM-FILM-02/assets/keyframes")
REF_T = os.path.join(SCAM, "S07-916.png"); REF_M = os.path.join(SCAM, "S08-916.png"); REF_S = os.path.join(SCAM, "S09-916.png")

GALLERY_MOTION = ("She holds her look into the lens, blinking naturally as wind moves a strand of hair. Subtle handheld jitter, eye focus drift, "
                  "fabric ripples in the breeze, 35mm film grain. " + FLAP_PIN_VIDEO)

MARGOT_PIN = ("The leather tote from the fourth reference image is an exact copy of that reference: FLAT strap handles, never rolled or tubular, "
    "the handle straps end cleanly at the belt line with plain clean leather below them and no stitched tab ends, slim silver keeper bars where the belts "
    "pass through the side loops, two silver clasp plates meeting at the center front with only a single short tail from the right belt, "
    "no crossed X belts on this bag and no long rounded tails.")

SHOTS = [
 dict(id="B00", model="gpt-image-2-text-to-image", refs=[],
      prompt=f"{STYLE} + inside a beautiful minimalist boutique with pale wooden shelves, a woman seen from behind and to the side lifting a structured fictional logo free leather handbag from a shelf, a small blank paper price tag hanging from its handle on a thin string, warm quiet light, her face turned away from camera, the tag completely blank on both sides",
      kling="Slow dolly push as the woman turns the small blank tag over with two fingers, pauses, then sets the bag gently back on the shelf and lets her hand fall. Subtle handheld jitter, soft focus drift, 35mm film grain; the tag stays completely blank and no readable text ever appears.",
      dur="5", mode="std"),
 dict(id="B01", model="gpt-image-2-text-to-image", refs=[],
      prompt=f"{STYLE} + a folded generic broadsheet newspaper lying on a pale oak kitchen table beside a white ceramic cup of coffee, soft morning window light, the paper angled away from camera so no headline or masthead is readable, all newsprint soft and completely out of focus, no readable text anywhere",
      kling="Very slow push toward the folded newspaper as steam rises and curls from the coffee cup. Dust motes float in the window light, subtle handheld jitter, 35mm film grain; all newsprint stays soft and unreadable.",
      dur="5", mode="std"),
 dict(id="B02", model="gpt-image-2-text-to-image", refs=[],
      prompt=f"{STYLE} + an orderly spread of unbranded material samples on a natural linen surface, smooth leather swatches in tan and cognac, squares of tightly woven straw, spools of white thread, one leather swatch set slightly apart from the rest, bright neutral daylight from one side, no hands, no tools, no logos",
      kling="Gentle handheld drift across the samples as the sunlight shifts subtly. A fabric edge lifts slightly in a draft, soft focus breathing, 35mm film grain.",
      dur="5", mode="std"),
 dict(id="B03", model="gpt-image-2-image-to-image", refs=[REF_STRAW_CARAMEL, REF_T],
      prompt=f"{STYLE} + portrait of the woman from the second reference image, in her 40s, standing on a weathered wooden dock, she looks directly into the lens, expression level and knowing, not smiling yet, crisp warm daylight. She holds the straw tote from the FIRST reference image on her forearm by its two short rolled top handles. The bag is an EXACT copy of the bag in the first reference image in silhouette, construction, colors and details: it has NO shoulder strap of any kind, only two short rolled leather top handles. {ID_STRAW} {FLAP_STRAW}",
      kling=GALLERY_MOTION, dur="5", mode="pro"),
 dict(id="B04", model="gpt-image-2-image-to-image", refs=[REF_STRAW_BLUE, REF_M],
      prompt=f"{STYLE} + portrait of the woman from the second reference image standing under a market awning, direct level look into the lens, warm daylight. The straw tote from the FIRST reference image hangs naturally at her side from her forearm by its two rolled top handles, the bag seen at a slight natural angle. The bag is an EXACT copy of the bag in the first reference image in silhouette, construction and EVERY color, sky blue colorway, never taupe, never greige. The front of the bag carries EXACTLY 2 leather belt straps and nothing else: each strap emerges from under the flap, they cross once in a single symmetric centered X, and each ends in one rounded tip lying flat on the straw, one tip pointing down left and one pointing down right. There is no horizontal band, no strap running behind or past the flap tabs, no stitched splice joints, no strap touching the sides or corners of the bag. {FLAP_STRAW.replace('taupe leather flap', 'leather flap colored exactly as the reference bag').replace('2 taupe leather belt straps', '2 leather belt straps colored exactly as the reference bag')}",
      kling=GALLERY_MOTION, dur="5", mode="pro"),
 dict(id="B05", model="gpt-image-2-image-to-image", refs=[REF_STRAW_BLACK, REF_S],
      prompt=f"{STYLE} + portrait of the woman from the second reference image seated at a patio table, tightest crop, she almost smiles into the lens, warm daylight. The straw tote from the FIRST reference image stands on the table beside her. The bag is an EXACT copy of the bag in the first reference image: this is the caban black colorway, meaning the woven straw BODY stays NATURAL TAN straw exactly as the reference, and ONLY the leather elements are black: black leather flap, black rolled handles, black crossed belt straps, black trim. The bag body is NEVER black straw, never an all black bag. Both rolled handles arc cleanly above the top of the bag and pass through their 2 slots in the flap, no handle ever lies over the front face of the flap or crosses below its bottom edge. The 2 black belt straps lie crossed in ONE symmetric centered X on the front below the flap. {FLAP_STRAW.replace('taupe leather flap', 'black leather flap').replace('2 taupe leather belt straps', '2 black leather belt straps')}",
      kling=GALLERY_MOTION + " The bag on the table stays perfectly still and completely unchanged the entire clip, its straps never move, and no metal, no buckle, and no new hardware of any kind ever appears anywhere on the bag.", dur="5", mode="pro"),
 dict(id="B06", model="gpt-image-2-image-to-image", refs=[REF_BOAT, R("brands/velantra/products/boat-tote/product-images/boat tote/02.jpg")],
      prompt=f"{STYLE} + a woman walking along a harbor boardwalk in morning light seen from her side in profile, carrying the canvas boat tote from the reference images by its handles in her near hand, the bag seen from its SIDE and three quarter rear angle so its side gusset and handles face the camera and its front turn lock panel faces AWAY from camera and is completely hidden from view, no lock hardware visible anywhere, sailboat masts soft behind her, {EXACT}. She carries nothing else, no other bag anywhere in the frame",
      kling="Handheld follow as she walks at an easy unhurried pace, the tote swinging gently at her side. Hair and fabric move in the breeze, subtle rolling shutter wobble, 35mm film grain; the bag keeps its exact shape with no added hardware.",
      dur="5", mode="pro"),
 dict(id="B07", model="gpt-image-2-image-to-image", refs=[REF_STRAW_CARAMEL],
      prompt=f"{STYLE} + a woman carrying {ID_STRAW} at a sunlit farmers market, carried by its handles at her side, flap lying completely flat, relaxed grip, stalls soft behind her. {FLAP_STRAW}",
      kling="Static tripod as she walks past the stalls at an easy pace, the bag swinging gently at her side as one rigid piece. Fabric of her clothing moves in the breeze, subtle handheld jitter, 35mm film grain. " + FLAP_PIN_VIDEO + " The 2 crossed belt straps stay flat against the front of the bag the entire clip, they never lift, never unwrap, never dangle, and never separate from the bag.",
      dur="5", mode="pro"),
 dict(id="B08", model="gpt-image-2-image-to-image", refs=[REF_WEEK],
      prompt=f"{STYLE} + a woman stepping out of a boutique hotel doorway carrying {ID_WEEK}, the bag CLOSED, morning light, cobblestones soft behind her, {ANTIDRIFT}. The weekend bag is the ONLY bag in the entire frame: she carries no other bag, no purse, no shoulder bag, nothing over her shoulder",
      kling="Static camera as she steps out of the doorway and walks past at an unhurried pace, the bag held steady at her side. Natural light flicker, subtle film grain; the bag stays closed, its flap one single piece, and no zipper ever appears.",
      dur="5", mode="pro"),
 dict(id="B09", model="gpt-image-2-image-to-image", refs=[REF_MARGOT],
      prompt=f"{STYLE} + a woman with the leather tote from the reference image over her shoulder holding a coffee, city sidewalk in the morning, {EXACT}",
      kling="Handheld follow as she walks a few unhurried steps and takes a small sip of coffee. Hair moves in the breeze, subtle rolling shutter wobble, 35mm film grain; the bag keeps its exact shape with no added hardware.",
      dur="5", mode="pro"),
 dict(id="B10", model="gpt-image-2-image-to-image", refs=[REF_BOAT, REF_STRAW_CARAMEL, REF_WEEK, REF_MARGOT],
      prompt=f"{STYLE} + the product family arranged together on a sunlit linen covered table by a bright window: the canvas boat tote, the caramel straw tote with its leather flap lying completely flat, the cream and cognac weekend bag closed, and the leather tote, all standing structured side by side, each bag an exact copy of its reference image, nothing added and nothing removed. The weekend bag's hardware is GOLD only, never silver and never chrome: the small gold oval turn lock on the front, two flat gold clasp plates with the cognac belt straps threaded through them and clearly visible on the front, gold keeper posts, the belt straps never tucked under the flap and never dead ending. {MARGOT_PIN} {FLAP_STRAW}",
      kling=None, dur=None, mode=None),  # audited-still Ken Burns in post
]

PACKSHOT = ("clean studio product photography, ONE single bag centered on an even seamless background in warm oat greige color hex E7E3DB, soft even light, "
            "only a soft contact shadow under the bag, the bag front facing and an exact copy of the bag in the reference image in silhouette, proportions, "
            "materials, hardware and details, nothing added and nothing removed, no text, no logos, no other objects. ")

MARGOT_PIN_SINGLE = MARGOT_PIN.replace("fourth reference image", "reference image")

SHOTS += [
 dict(id="B11A", model="gpt-image-2-image-to-image", refs=[REF_BOAT],
      prompt=PACKSHOT + "The turn lock closure is copied EXACTLY from the reference: gold rectangular plate with an EMPTY vertical slot, upright gold T toggle, and the navy canvas belt tab with pointed gold end cap crossing the plate as a separate piece, never fused, never melted.",
      kling=None, dur=None, mode=None),
 dict(id="B11B", model="gpt-image-2-image-to-image", refs=[REF_STRAW_CARAMEL],
      prompt=PACKSHOT + FLAP_STRAW,
      kling=None, dur=None, mode=None),
 dict(id="B11C", model="gpt-image-2-image-to-image", refs=[REF_WEEK],
      prompt=PACKSHOT + "The bag is CLOSED. Hardware is GOLD only, never silver: small gold oval turn lock, two flat gold clasp plates with cognac belt straps threaded through them, gold keeper posts. No zipper anywhere. The ENTIRE bag including every strap, buckle and handle sits fully inside the frame with generous empty background margin on ALL four sides, the bag occupying only the central 65 percent of the frame width, nothing ever touching or approaching the frame edges. " + ANTIDRIFT + ".",
      kling=None, dur=None, mode=None),
 dict(id="B11D", model="gpt-image-2-image-to-image", refs=[REF_MARGOT],
      prompt=PACKSHOT + MARGOT_PIN_SINGLE,
      kling=None, dur=None, mode=None),
]

def gen_keyframes(only=None):
    st = state_load()
    c0 = credit(); print(f"credits before: {c0}", flush=True)
    for s in SHOTS:
        if only and s["id"] not in only: continue
        out = os.path.join(OUT_KF, f"{s['id']}.png")
        if os.path.exists(out): print(f"{s['id']}: exists, skip", flush=True); continue
        print(f"=== {s['id']} keyframe", flush=True)
        inp = {"prompt": s["prompt"], "aspect_ratio": "2:3", "resolution": "2K"}
        if s["refs"]:
            inp["input_urls"] = [upload(p, st) for p in s["refs"]]
        tkey = f"kf_{s['id']}"
        task = st["tasks"].get(tkey)
        if not task:
            d = http("POST", f"{API}/jobs/createTask", {"model": s["model"], "input": inp})
            if d.get("code") != 200:
                # retry once with 9:16 in case 2:3 rejected, then flag
                inp["aspect_ratio"] = "9:16"
                d = http("POST", f"{API}/jobs/createTask", {"model": s["model"], "input": inp})
            if d.get("code") != 200:
                print(f"{s['id']}: createTask rejected: {d}", flush=True); continue
            task = d["data"]["taskId"]; st["tasks"][tkey] = task; state_save(st)
        url = poll(task)
        if url and download(url, out):
            print(f"{s['id']}: saved {out}", flush=True)
        else:
            st["tasks"].pop(tkey, None); state_save(st)
            print(f"{s['id']}: FAILED (task cleared for retry)", flush=True)
    c1 = credit(); print(f"credits after: {c1} (delta {c0 - c1 if c0 and c1 else '?'})", flush=True)

def animate(ids):
    st = state_load()
    c0 = credit(); print(f"credits before: {c0}", flush=True)
    for s in SHOTS:
        if s["id"] not in ids or not s.get("kling"): continue
        kf = os.path.join(OUT_KF, f"{s['id']}.png")
        out = os.path.join(OUT_CL, f"{s['id']}.mp4")
        if not os.path.exists(kf): print(f"{s['id']}: no keyframe", flush=True); continue
        if os.path.exists(out): print(f"{s['id']}: clip exists", flush=True); continue
        print(f"=== {s['id']} kling", flush=True)
        img = upload(kf, st)
        tkey = f"kl_{s['id']}"
        task = st["kling"].get(tkey)
        if not task:
            payload = {"model": "kling-3.0/video", "input": {
                "prompt": s["kling"], "image_urls": [img], "sound": False,
                "duration": s["dur"], "aspect_ratio": "9:16", "mode": s["mode"], "multi_shots": False}}
            d = http("POST", f"{API}/jobs/createTask", payload)
            if d.get("code") != 200: print(f"{s['id']}: rejected: {d}", flush=True); continue
            task = d["data"]["taskId"]; st["kling"][tkey] = task; state_save(st)
        url = poll(task, max_wait=1200)
        if url and download(url, out):
            print(f"{s['id']}: saved {out}", flush=True)
        else:
            st["kling"].pop(tkey, None); state_save(st)
            print(f"{s['id']}: kling FAILED (cleared)", flush=True)
        time.sleep(5)
    c1 = credit(); print(f"credits after: {c1} (delta {c0 - c1 if c0 and c1 else '?'})", flush=True)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--animate":
        animate(sys.argv[2].split(","))
    elif len(sys.argv) > 1 and sys.argv[1] == "--only":
        gen_keyframes(only=sys.argv[2].split(","))
    else:
        gen_keyframes()
