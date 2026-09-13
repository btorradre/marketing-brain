"""Generate the three greenscreen talking-head avatar keyframes for MENSID-01.

Each avatar = ONE Pinterest reference (Brooks-directed look, men 35-45) -> GPT Image 2 i2i:
same man, chest-up selfie framing, flat chroma green backdrop, iPhone imperfection cues.
The picked frame becomes the HeyGen photo avatar (Avatar V) AND the identity anchor for reuse.

  python3 gen_avatars.py run            # all avatars, VARIANTS each (default 2)
  python3 gen_avatars.py run M1 M3
"""
import json, os, ssl, subprocess, sys, time, urllib.request, certifi

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "avatars"); REFS = os.path.join(OUT, "pinterest-refs")
STATE = os.path.join(HERE, "state_avatars.json"); UPCACHE = os.path.join(HERE, "upload_cache_avatars.json")
VAULT = "/Users/brooksorradre2/Documents/marketing brain"
CTX = ssl.create_default_context(cafile=certifi.where())
MODEL = "gpt-image-2-image-to-image"; RATIO = "2:3"; RES = os.environ.get("GI2_RES", "1K")
VARIANTS = int(os.environ.get("VARIANTS", "2")); VSTART = int(os.environ.get("VSTART", "1"))

def env(k):
    for line in open(os.path.join(VAULT, ".env")):
        line=line.strip()
        if line and not line.startswith("#") and "=" in line:
            a,b=line.split("=",1)
            if a.strip()==k: return b.strip().strip('"').strip("'")
    raise KeyError(k)
KEY = env("KIE_API_KEY"); H = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}
load = lambda p,d: json.load(open(p)) if os.path.exists(p) else d
save = lambda p,o: json.dump(o, open(p,"w"), indent=2)

# AVATARS: filled after the Pinterest pick. ref = filename inside avatars/pinterest-refs/
AVATARS = json.load(open(os.path.join(HERE, "avatars.json"))) if os.path.exists(os.path.join(HERE, "avatars.json")) else []

GREEN = ("The entire background is a flat, evenly lit, solid chroma key green screen, pure uniform green "
         "with no folds, no gradient, no shadows, no props and nothing else in frame behind him.")
FRAMING = ("Chest-up selfie framing like a phone held at arm's length slightly below eye level, his head and "
           "shoulders filling the frame, one arm angled out of the bottom corner toward the camera, looking "
           "straight into the lens mid-sentence with his mouth slightly open as if talking, relaxed and natural.")
IMPERFECT = ("Real iPhone front-camera photo, not a render: natural skin texture with visible pores and fine lines, "
             "a few flyaway hairs, slight phone camera softness, mild sensor noise, never tack sharp, never airbrushed, "
             "never studio lit. Real light only: one soft indoor light source on his face with natural falloff.")
NEG = "No text, no watermark, no logo, no second person, no hands covering the face, no sunglasses."

def build_prompt(a):
    return ("Use the attached photo ONLY as the reference for this man's identity: his face, age, skin, hair, "
            "facial hair, build and general style. Recreate the SAME man, clearly recognisable as him, "
            f"{a['age']} years old, {a['look']}, wearing {a['wardrobe']}. "
            + FRAMING + " " + GREEN + " " + IMPERFECT + " " + NEG + " Vertical portrait.")

def api(url, payload=None, timeout=180):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=H, method="POST" if data else "GET")
    return json.loads(urllib.request.urlopen(req, timeout=timeout, context=CTX).read().decode(), strict=False)

def upload(path):
    cache = load(UPCACHE, {}); k = os.path.basename(path)
    if k in cache and time.time()-cache[k]["t"] < 60000: return cache[k]["url"]
    out = subprocess.run(["curl","-s","-X","POST","https://kieai.redpandaai.co/api/file-stream-upload",
        "-H",f"Authorization: Bearer {KEY}","-F",f"file=@{path}","-F","uploadPath=images/velantra-mensid-avatars"],
        capture_output=True, text=True, timeout=180)
    url = (json.loads(out.stdout, strict=False).get("data") or {}).get("downloadUrl")
    if not url: raise RuntimeError("upload failed: "+out.stdout[:200])
    cache[k] = {"url":url,"t":time.time()}; save(UPCACHE, cache); return url

def create(prompt, urls):
    d = api("https://api.kie.ai/api/v1/jobs/createTask", {"model": MODEL,
        "input": {"prompt": prompt, "input_urls": urls, "aspect_ratio": RATIO, "resolution": RES}})
    if d.get("code") != 200: raise RuntimeError(f"createTask {d.get('code')}: {str(d)[:200]}")
    return d["data"]["taskId"]

def poll(tid, timeout_s=900):
    t0=time.time()
    while time.time()-t0 < timeout_s:
        d = api(f"https://api.kie.ai/api/v1/jobs/recordInfo?taskId={tid}"); data = d.get("data") or {}
        if data.get("state")=="success":
            return json.loads(data["resultJson"], strict=False)["resultUrls"][0], data.get("creditsConsumed")
        if data.get("state")=="fail": raise RuntimeError("task fail: "+str(data.get("failMsg"))[:200])
        time.sleep(8)
    raise TimeoutError(tid)

def gen_one(a, v, state):
    d = os.path.join(OUT, a["id"]); os.makedirs(d, exist_ok=True); dest = os.path.join(d, f"v{v}.png")
    if os.path.exists(dest) and os.path.getsize(dest) > 50000: return dest, "cached"
    prompt = build_prompt(a); urls = [upload(os.path.join(REFS, a["ref"]))]
    ekey=f"{a['id']}.v{v}"; ent=state.get(ekey,{}); last=None
    for attempt in range(5):
        try:
            tid = ent.get("tid") or create(prompt, urls); ent["tid"]=tid; state[ekey]=ent; save(STATE,state)
            url, cost = poll(tid)
            subprocess.run(["curl","-sS","-A","Mozilla/5.0","-o",dest,url], check=True, timeout=300)
            ent.update(done=True, cost=cost); state[ekey]=ent; save(STATE,state); return dest, cost
        except Exception as e:
            last=e; ent["tid"]=None; state[ekey]=ent; save(STATE,state)
            print(f"    {ekey} attempt {attempt+1} failed: {str(e)[:140]}", flush=True); time.sleep(10+attempt*10)
    raise RuntimeError(f"{ekey}: {last}")

if __name__ == "__main__":
    only = sys.argv[2:] if len(sys.argv) > 2 else None
    state = load(STATE, {}); spent = 0
    for a in AVATARS:
        if only and a["id"] not in only: continue
        for v in range(VSTART, VSTART+VARIANTS):
            try:
                dest, cost = gen_one(a, v, state); spent += cost if isinstance(cost,(int,float)) else 0
                print(f"{a['id']} v{v} ok ({cost})", flush=True)
            except Exception as e:
                print(f"{a['id']} v{v} FAIL {str(e)[:160]}", flush=True)
    print("credits spent:", spent)
