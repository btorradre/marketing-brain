"""Casting pass for VEL-WEEKENDER-HAALAND-01: three male TikTok-native creators on chroma green.

Text-to-image (no Pinterest ref supplied this run), GPT Image 2 on kie, 2:3 @1K, 3 variants each.
The fix vs MENSID-01 (which read robotic): propped-phone TikTok framing instead of a flat
centred passport shot, one hand up mid-gesture so Avatar V has something to move, lips parted
mid-word, head off-centre and tilted, window light from one side, imperfection cues.

  python3 gen_casting.py            # all three, 3 variants
  python3 gen_casting.py C1 C3
"""
import json, os, ssl, subprocess, sys, time, urllib.request, certifi

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "casting"); STATE = os.path.join(HERE, "state_casting.json")
VAULT = "/Users/brooksorradre2/Documents/marketing brain"
CTX = ssl.create_default_context(cafile=certifi.where())
MODEL = "gpt-image-2-text-to-image"; RATIO = "2:3"; RES = "1K"; VARIANTS = 3

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

CREATORS = [
    {"id": "C1", "who": "a white man of 29 with short dark blond hair under a plain navy cap worn backwards, "
                        "a few days of light stubble, a straight nose and an easy open face, medium athletic build",
     "wardrobe": "a plain heather grey hoodie with the hood down"},
    {"id": "C2", "who": "a white man of 32 with short dark brown hair pushed back off his forehead, a neat short "
                        "beard, strong jaw, faint lines at the eyes, broad shoulders",
     "wardrobe": "a plain washed light blue crew neck tee"},  # black tee pulled 6/6 rolls off the green
    {"id": "C3", "who": "a white man of 27 with light brown loosely curly hair falling over his forehead, clean "
                        "shaven, a slightly crooked friendly smile line, lean build",
     "wardrobe": "a plain white tee under an unbuttoned cream overshirt"},
]

FRAME = ("Vertical 2:3 frame that looks like a paused moment from a real iPhone video recorded for TikTok. "
         "The phone is propped up at roughly eye level in front of him; he is clearly not holding it. "
         "Framed from the mid chest up, his head a little off centre and tilted a few degrees, one shoulder "
         "slightly closer to the camera, leaning in toward the phone. His right hand is raised loosely to "
         "collarbone height mid gesture, fingers relaxed, well clear of his mouth and chin; his other arm rests "
         "below the bottom edge of the frame. He looks straight into the lens with his lips parted mid word, "
         "eyebrows slightly up, like he is halfway through telling a friend something he just figured out.")
GREEN = ("BACKGROUND, MANDATORY: every pixel behind him, edge to edge and top to bottom, is a bright saturated "
         "pure chroma key green screen, the flat solid green of a studio green screen backdrop, evenly lit, "
         "no gradient, no vignette, no dark corners, no blur, no room, no wall, no window, no props, nothing "
         "else in the frame behind him. The green does not spill onto his skin, hair or clothing.")
LIGHT = ("The light on him is ordinary window daylight coming from one side, leaving the far side of his face "
         "a little darker, imperfect white balance, slightly uneven exposure across his face.")
RAW = ("Real front camera phone footage look, not a render: natural skin with visible pores, mild redness, "
       "a few flyaway hairs, slight phone camera softness, mild front camera sharpening on the edges, light "
       "digital grain, subtle compression, never tack sharp, never airbrushed, never studio lit, no beauty "
       "filter. It looks like a real guy recording a TikTok, not an advertisement.")
NEG = ("No text, captions, logos, watermarks or overlays. No visible phone, selfie stick or extended selfie "
       "arm. No sunglasses, no headphones, no hands covering the mouth. No ring light reflections, no studio "
       "or cinematic lighting, no plastic skin, no HDR, no extra or distorted fingers. Not a 3D render, not CGI.")

def build_prompt(c):
    return (f"{FRAME} He is {c['who']}, wearing {c['wardrobe']}. {GREEN} {LIGHT} {RAW} {NEG}")

def api(url, payload=None, timeout=180):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=H, method="POST" if data else "GET")
    return json.loads(urllib.request.urlopen(req, timeout=timeout, context=CTX).read().decode(), strict=False)

def create(prompt):
    d = api("https://api.kie.ai/api/v1/jobs/createTask", {"model": MODEL,
        "input": {"prompt": prompt, "aspect_ratio": RATIO, "resolution": RES}})
    if d.get("code") != 200: raise RuntimeError(f"createTask {d.get('code')}: {str(d)[:200]}")
    return d["data"]["taskId"]

def poll(tid, timeout_s=900):
    t0 = time.time()
    while time.time() - t0 < timeout_s:
        d = api(f"https://api.kie.ai/api/v1/jobs/recordInfo?taskId={tid}"); data = d.get("data") or {}
        if data.get("state") == "success":
            return json.loads(data["resultJson"], strict=False)["resultUrls"][0], data.get("creditsConsumed")
        if data.get("state") == "fail": raise RuntimeError("task fail: " + str(data.get("failMsg"))[:200])
        time.sleep(8)
    raise TimeoutError(tid)

def gen_one(c, v, state):
    d = os.path.join(OUT, c["id"]); os.makedirs(d, exist_ok=True); dest = os.path.join(d, f"v{v}.png")
    if os.path.exists(dest) and os.path.getsize(dest) > 50000: return dest, "cached"
    prompt = build_prompt(c); ekey = f"{c['id']}.v{v}"; ent = state.get(ekey, {}); last = None
    for attempt in range(6):
        try:
            tid = ent.get("tid") or create(prompt); ent["tid"] = tid; state[ekey] = ent; save(STATE, state)
            url, cost = poll(tid)
            subprocess.run(["curl", "-sS", "-A", "Mozilla/5.0", "-o", dest, url], check=True, timeout=300)
            ent.update(done=True, cost=cost); state[ekey] = ent; save(STATE, state); return dest, cost
        except Exception as e:
            last = e; ent["tid"] = None; state[ekey] = ent; save(STATE, state)
            print(f"    {ekey} attempt {attempt+1} failed: {str(e)[:140]}", flush=True); time.sleep(10 + attempt * 10)
    raise RuntimeError(f"{ekey}: {last}")

if __name__ == "__main__":
    only = sys.argv[1:] or None
    state = load(STATE, {}); spent = 0
    open(os.path.join(HERE, "casting_prompts.txt"), "w").write("\n\n".join(f"{c['id']}:\n{build_prompt(c)}" for c in CREATORS))
    for c in CREATORS:
        if only and c["id"] not in only: continue
        for v in range(1, VARIANTS + 1):
            try:
                dest, cost = gen_one(c, v, state); spent += cost if isinstance(cost, (int, float)) else 0
                print(f"{c['id']} v{v} ok ({cost})", flush=True)
            except Exception as e:
                print(f"{c['id']} v{v} FAIL {str(e)[:160]}", flush=True)
    print("credits spent:", spent)
