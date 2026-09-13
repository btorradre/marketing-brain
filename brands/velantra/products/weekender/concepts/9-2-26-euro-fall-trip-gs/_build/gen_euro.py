#!/usr/bin/env python3
"""EURO keyframes for the Euro-fall-trip greenscreen concepts (Vivienne / Weekender / Meridian).

Pixel-seed i2i on kie GPT Image 2 (the Zede-validated recipe): the real street-style pin is the
scene seed (woman, outfit, street, light, grain all kept), the real product photo is the second
input, and the prompt changes ONLY the bag. 2:3 @ 1K = 6 credits per frame, 2 variants per shot.

  python3 gen_euro.py            # every shot for this concept's product (detected from the path)
  python3 gen_euro.py EURO-P1    # one shot
"""
import json, os, ssl, subprocess, sys, time, urllib.request, certifi, concurrent.futures as cf

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
PRODUCT = ROOT.split("/products/")[1].split("/")[0]            # vivienne | weekender | margot
OUT = os.path.join(ROOT, "keyframes"); SEEDS = os.path.join(OUT, "seeds"); SRC = os.path.join(ROOT, "plates", "euro-src")
STATE = os.path.join(HERE, "state_euro.json"); UPCACHE = os.path.join(HERE, "kie_uploads.json")
VAULT = "/Users/brooksorradre2/Documents/marketing brain"
CTX = ssl.create_default_context(cafile=certifi.where())
MODEL = "gpt-image-2-image-to-image"; RATIO = "2:3"; RES = "1K"; VARIANTS = 2

def env(k):
    for line in open(os.path.join(VAULT, ".env")):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            a, b = line.split("=", 1)
            if a.strip() == k: return b.strip().strip('"').strip("'")
    raise KeyError(k)
KEY = env("KIE_API_KEY"); H = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}
load = lambda p, d: json.load(open(p)) if os.path.exists(p) else d
save = lambda p, o: json.dump(o, open(p, "w"), indent=2)

PREAMBLE = ("Two photos are attached. The FIRST photo is the scene and it is the ground truth for everything except the bag: "
    "keep the woman, her face, hair, outfit, shoes, pose, the street, the buildings, the weather, the light, the colour "
    "grade, the camera angle, the framing and the phone-camera grain exactly as they are. Change ONLY the bag. Remove "
    "whatever bag or tote she is carrying in the first photo, and any strap that belongs to it, and put the bag from the "
    "SECOND photo in its place. The SECOND photo is used only as the reference for the bag's shape, proportions, "
    "materials, colours, stitching and hardware; do not copy its lighting, its background or its product-photo look. "
    "The bag must sit in her hand or on her body naturally, with correct perspective, correct scale against her body, "
    "and shadows and light that match the first photo. ")

PHOTOREAL = ("CRITICAL RENDERING INSTRUCTION. This is a real photograph casually taken on an iPhone 15 Pro by an ordinary "
    "person, handheld, in one second, with no lighting equipment, no tripod and no styling. It is NOT a 3D render, NOT CGI, "
    "NOT a product visualisation, NOT Blender or Octane or Unreal or Keyshot, NOT ray traced, NOT a commercial or catalogue "
    "product photograph, NOT an advertisement, NOT retouched, NOT airbrushed, NOT studio lit. If it looks polished or "
    "computer generated it is wrong. Photographic evidence that must be present: visible digital sensor noise and grain "
    "through the shadows and midtones, highlights slightly blown out where the light source hits, mild chromatic aberration "
    "on high contrast edges, faint JPEG compression artefacts, focus that is slightly imperfect so nothing is tack sharp, a "
    "trace of handheld motion blur, and framing that is a little crooked and off centre the way a real snapshot is. Real "
    "light only: one dominant available light source, mixed colour temperature across the frame, uneven exposure, and real "
    "shadows falling off naturally with visible ambient bounce. Real surfaces: the leather is creased, faintly scuffed, "
    "unevenly grained and dulled where it has been handled, never a uniform polished finish; ordinary dust, lint and "
    "fingerprints are present. No on-screen text, lettering, signage, logos or graphics anywhere on the bag. Vertical frame.")

HW_GOLD = ("Front closure hardware: at the front centre of the leather band stands a small gold turn post with a round knurled "
    "mushroom shaped head. The flap's centre tab carries a polished gold OVAL plate with a shaped keyhole cutout in its "
    "middle, and when the flap is down this tab rests over the post so the gold post head shows through the cutout. To the "
    "left and right, two flat vertical gold staples stand on the band, each TWO PARALLEL FLAT GOLD BARS side by side, never "
    "one solid blade and never a buckle; when the flap is down its two small oval slots sit over these staples so the "
    "staples poke through. The two leather belt straps come over the top from the back of the bag, each strap tip carrying "
    "a flat gold rounded rectangular end plate with an oblong slot and small dome rivets, hooked over its staple. The "
    "knurled post appears ONCE. The oval plate is FLAT and flush with an EMPTY keyhole cutout, no barrel, no cylinder, no "
    "toggle standing proud. The handles pass through keyhole shaped cutouts in the flap with stitched edges; the cutouts "
    "show only the bag's own dark leather behind them, never the background. All hardware is the same warm brass gold, no "
    "silver, no chrome. No logos, no stamped lettering, no plaques anywhere on the bag. ")

PRODUCTS = {
 "vivienne": {
   "seed": "SEED-chocolate-front.png",
   "identity": ("The bag is a LARGE, SOFT, SLOUCHY all-leather top handle bag in dark chocolate leather with contrast cognac "
     "leather flap edge, belt straps, rolled handles and corner caps (two-tone: chocolate body, cognac trim), trapezoid "
     "outline that bows and slumps under its own weight, a one-piece leather flap folded over the top, a belted closure, two "
     "short rolled top handles, reinforced curved corner caps, rolled piping down the side seams, braided whip-stitched trim "
     "along the top edge of the band, and a small leather key bell tied at a handle base. The body leather is soft with "
     "visible natural pore and pebble grain and a MATTE to SATIN sheen, creased where it slumps; never lacquered, never "
     "mirror bright, never rigid or boxy. " + HW_GOLD +
     "SCALE: carried in the hand it hangs to mid-thigh and is about as wide as her torso; worn on the shoulder strap it "
     "reaches from just under her armpit to below her hip. Her hand spans only a small fraction of its width. Never render "
     "it small. The two short top handles are hand or crook-of-elbow carry only and never reach a shoulder. "),
   "shots": {
     "EURO-P1": ("p014", "She carries the bag by its two rolled top handles in the hand that held her small bag, the bag hanging at her side to mid-thigh, the coffee stays in her other hand. Paris street in autumn leaves, trench coat, exactly as the first photo. "),
     "EURO-P2": ("p012", "She carries the bag by its two rolled top handles in her left hand at her side, flap down, straps fastened, the cafe terrace and awning behind her exactly as in the first photo. "),
     "EURO-M1": ("p053", "She carries the bag by its two rolled top handles in her hand at her side, hanging to mid-thigh, flap down and belted; leather jacket, white shirt, grey trousers, the stone street exactly as the first photo. "),
     "EURO-M2": ("p059", "The bag sits on the wooden bench right beside her hip, flap down, straps fastened, its soft body slumping a little and bowing at the front, handles standing up loosely; her coffee, her pose and the cafe behind stay exactly as in the first photo. "),
     "EURO-L1": ("p017", "The bag is worn CROSSBODY on its long detachable leather shoulder strap clipped to the brass rings at its sides, the strap running diagonally across her chest from her right shoulder, the bag resting at her left hip, flap down; grey knit, pleated skirt, the street exactly as the first photo. "),
     "EURO-L2": ("p073", "She carries the bag by its two rolled top handles in one hand at her side, hanging to mid-thigh, flap down and belted; the red double-decker bus, plaid skirt and grey knit exactly as the first photo. "),
   }},
 "weekender": {
   "seed": "SEED-LC-closed-front.jpg",
   "identity": ("The bag is a structured two tone weekend bag, wider than tall, rich cognac brown leather upper flap section and "
     "two rolled cognac leather top handles over a cream ivory woven canvas body, a small gold oval turn lock on the front, "
     "two flat gold clasp plates with cognac leather belt straps threaded through them, a small cognac leather key bell tied "
     "to the handle base, cognac leather corner patches at the bottom, a small gold eyelet high on each side face, visible "
     "stitching, gold hardware, no logos anywhere on the bag. The bag in frame is an exact copy of the bag in the second "
     "photo in silhouette, proportions, materials and details; the two rolled top handles are smooth simple leather tubes "
     "with no wrapping, no braiding and no woven texture. Flap down and fastened. " + HW_GOLD +
     "SCALE IS CRITICAL. This is a LARGE TRAVEL BAG, 18 inches wide by 14.5 inches tall by 7 inches deep, big enough to pack "
     "two to three days of clothes. It is NOT a handbag, NOT a purse, NOT a medium tote. Roughly the size of a carry-on "
     "duffel. Render it noticeably oversized rather than too small. Hand or forearm carry only: the short rolled handles "
     "never reach a shoulder and there is NO shoulder strap. It keeps its full boxy shape with no slump. No zipper anywhere. "),
   "shots": {
     "EURO-P1": ("p006", "The weekend bag sits on top of the rolling suitcase right beside her, flap down and fastened, its base flat, replacing the black bag; it is clearly wider than her torso and as tall as her head-to-shoulder height, filling a large part of the frame. Trench coat, jeans, the suitcase and the street exactly as the first photo. "),
     "EURO-P2": ("q016", "She carries the weekend bag by its two rolled handles in her hand at her side, replacing the small black bag, reaching from her hip toward her knee and as wide as her shoulders; trench coat, cream trousers, the Paris crosswalk and Haussmann buildings exactly as the first photo. "),
     "EURO-M1": ("p033", "She carries the weekend bag over her forearm with both rolled handles in the crook of her elbow, the bag hanging at her hip and reaching toward her knee, as wide as her shoulders; leather jacket, grey trousers and the hotel doorway exactly as the first photo. "),
     "EURO-L1": ("q070", "She carries the weekend bag by its two rolled handles in her left hand at her side, reaching from her hip toward her knee and as wide as her shoulders; the coffee stays in her right hand. Brown leather jacket, white top, jeans, the red double-decker bus and red phone box behind her exactly as the first photo. "),
   }},
 "margot": {
   "seed": "SEED-brown-1.webp",
   "identity": ("The bag is a structured warm brown pebbled-leather tote that is clearly WIDER THAN IT IS TALL, with a flat base "
     "and squared-off sides. The top of the bag is OPEN and you can see down into it. There is NO large flap covering the "
     "front face. Exactly two FLAT leather strap handles standing upright, flat straps and not rounded tubes. One small "
     "silver turn-lock plate mounted on a short tab at the top centre of the front face. Exactly two leather belt straps "
     "running HORIZONTALLY across the front face, each passing through a silver buckle near the left and right edges. Small "
     "silver feet on the base. Single colour leather throughout, no canvas, no two-tone panels, and no logos, monograms or "
     "lettering anywhere. DO NOT give the bag a large front flap. DO NOT make it taller than it is wide. DO NOT make the "
     "handles rounded tubes. DO NOT close over the open top. All hardware is polished silver, never gold, never brass. "
     "SCALE: about 37 cm wide, the width of her torso, hanging to mid-thigh when carried in the hand. "),
   "shots": {
     "EURO-P1": ("p007", "She carries the tote by its two flat handles in her hand at her side, replacing the white tote, the coffee stays in her other hand; trench coat, striped top, the bookshop street exactly as the first photo. "),
     "EURO-P2": ("p002", "She carries the tote by its two flat handles in her gloved hand at her side, replacing the small bag; beret, trench coat, the cafe terrace behind her exactly as the first photo. "),
     "EURO-M1": ("p060", "She carries the tote by its two flat handles in her hand at her side, replacing the black bag; black leather jacket, the yellow tram behind her exactly as the first photo. "),
     "EURO-L1": ("p071", "The tote is worn CROSSBODY on its removable adjustable leather strap clipped by silver swivel snap hooks to the rings at its sides, the strap running diagonally across her chest, the tote resting at her hip with its open top facing up; cream knit, plaid mini skirt, tall boots and the street exactly as the first photo. "),
   }},
}

def api(url, payload=None, timeout=180):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=H, method="POST" if data else "GET")
    return json.loads(urllib.request.urlopen(req, timeout=timeout, context=CTX).read().decode(), strict=False)

def upload(path):
    cache = load(UPCACHE, {}); k = os.path.basename(path)
    if k in cache and time.time() - cache[k]["t"] < 60000: return cache[k]["url"]
    out = subprocess.run(["curl", "-s", "-X", "POST", "https://kieai.redpandaai.co/api/file-stream-upload",
        "-H", f"Authorization: Bearer {KEY}", "-F", f"file=@{path}", "-F", f"uploadPath=images/velantra-eurofall-{PRODUCT}"],
        capture_output=True, text=True, timeout=180)
    url = (json.loads(out.stdout, strict=False).get("data") or {}).get("downloadUrl")
    if not url: raise RuntimeError("upload failed: " + out.stdout[:200])
    cache[k] = {"url": url, "t": time.time()}; save(UPCACHE, cache); return url

def create(prompt, urls):
    d = api("https://api.kie.ai/api/v1/jobs/createTask", {"model": MODEL, "input": {"prompt": prompt, "input_urls": urls, "aspect_ratio": RATIO, "resolution": RES}})
    if d.get("code") != 200: raise RuntimeError(f"createTask {d.get('code')}: {str(d)[:200]}")
    return d["data"]["taskId"]

def poll(tid, timeout_s=900):
    t0 = time.time()
    while time.time() - t0 < timeout_s:
        d = api(f"https://api.kie.ai/api/v1/jobs/recordInfo?taskId={tid}"); data = d.get("data") or {}
        if data.get("state") == "success": return json.loads(data["resultJson"], strict=False)["resultUrls"][0], data.get("creditsConsumed")
        if data.get("state") == "fail": raise RuntimeError("task fail: " + str(data.get("failMsg"))[:200])
        time.sleep(8)
    raise TimeoutError(tid)

def gen_one(shot, v, prompt, urls):
    dest = os.path.join(OUT, f"{shot}-v{v}.png")
    if os.path.exists(dest) and os.path.getsize(dest) > 50000: return dest, "cached"
    ekey = f"{shot}.v{v}"; last = None
    for attempt in range(5):
        try:
            state = load(STATE, {}); ent = state.get(ekey, {})
            tid = ent.get("tid") or create(prompt, urls); ent["tid"] = tid; state[ekey] = ent; save(STATE, state)
            url, cost = poll(tid)
            subprocess.run(["curl", "-sS", "-A", "Mozilla/5.0", "-o", dest, url], check=True, timeout=300)
            state = load(STATE, {}); state[ekey] = {**ent, "done": True, "cost": cost, "url": url}; save(STATE, state); return dest, cost
        except Exception as e:
            last = e; state = load(STATE, {}); state[ekey] = {"tid": None}; save(STATE, state)
            print(f"    {ekey} attempt {attempt+1} failed: {str(e)[:140]}", flush=True); time.sleep(10 + attempt * 10)
    raise RuntimeError(f"{ekey}: {last}")

if __name__ == "__main__":
    P = PRODUCTS[PRODUCT]; only = sys.argv[1:] or None; os.makedirs(OUT, exist_ok=True)
    seed_url = upload(os.path.join(SEEDS, P["seed"]))
    jobs = []; prompts = {}
    for shot, (pin, scene) in P["shots"].items():
        if only and shot not in only: continue
        scene_url = upload(os.path.join(SRC, f"{pin}.jpg"))
        prompt = PREAMBLE + P["identity"] + scene + PHOTOREAL; prompts[shot] = prompt
        for v in range(1, VARIANTS + 1): jobs.append((shot, v, prompt, [scene_url, seed_url]))
    open(os.path.join(HERE, "euro_prompts.txt"), "w").write("\n\n".join(f"{k}:\n{v}" for k, v in prompts.items()))
    spent = 0
    with cf.ThreadPoolExecutor(6) as ex:
        futs = {ex.submit(gen_one, *j): j for j in jobs}
        for f in cf.as_completed(futs):
            shot, v = futs[f][0], futs[f][1]
            try:
                dest, cost = f.result(); spent += cost if isinstance(cost, (int, float)) else 0; print(f"{PRODUCT} {shot} v{v} ok ({cost})", flush=True)
            except Exception as e: print(f"{PRODUCT} {shot} v{v} FAIL {str(e)[:160]}", flush=True)
    print("credits spent:", spent)
