"""One new still for VEL-WEEKENDER-HAALAND-01: the Light Chocolate Weekender on the back seat of a cab,
the same man's hand resting on the handle. Covers the "or in the back of a cab" beat. GPT Image 2 i2i on kie,
anchored on the real closed-bag still + the MENSID creator anchor (same blazer / watch). 3 variants @1K.
"""
import json, os, ssl, subprocess, sys, time, urllib.request, certifi
MENSLC = ("/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/weekender/concepts/"
          "8:8:26 - mens carry lc (wool oak replication)/VEL-WEEKENDER-MENSLC-01/_build")
sys.path.insert(0, MENSLC)
from blocks import PREAMBLE, IDENTITY, ANTI_DRIFT, CLOSURE, HARDWARE_LAW, SCALE, PHOTOREAL  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "product-broll", "B8-cab"); os.makedirs(OUT, exist_ok=True)
STATE = os.path.join(HERE, "state_cab.json"); UPCACHE = os.path.join(HERE, "upload_cache_cab.json")
VAULT = "/Users/brooksorradre2/Documents/marketing brain"
REFDIR = os.path.join(VAULT, "brands/velantra/products/weekender/product-references/real-product-2026-08-08")
REFS = [os.path.join(REFDIR, "LC-closed-front-unfastened.jpg"),
        os.path.join(VAULT, "brands/velantra/products/weekender/concepts/8-31-26-mens-birkin-identity/_build/creator-ref.png")]
CTX = ssl.create_default_context(cafile=certifi.where())
MODEL = "gpt-image-2-image-to-image"; RATIO = "2:3"; RES = "1K"; VARIANTS = 3

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

SCENE = (
    "The setting is the back seat of an ordinary city taxi or rideshare car in daylight: grey or black "
    "textured fabric or leather rear seat, a seat belt buckle beside the bag, the driver's headrest and "
    "part of the front seat visible ahead, city buildings and traffic passing soft and out of focus through "
    "the side window, daylight coming through that window and falling unevenly across the bag. The closed "
    "light chocolate weekend bag sits upright on the seat cushion next to the man, flap down, straps hanging "
    "near its side edges, its base flat on the seat, keeping its full boxy shape with no slump. Only the "
    "man's hand and forearm are in frame, resting loosely on top of the rolled handles: a large hand, fair "
    "skin with natural texture, a plain steel watch on the left wrist, the black sleeve of an oversized "
    "blazer and a white tee cuff at the edge of frame, the man in the second reference photo. No face. The "
    "bag is the main subject and fills most of the lower two thirds of the frame, clearly as wide as the "
    "seat cushion it sits on. Shot from the seat beside it at about the bag's own height, slightly from "
    "above, handheld phone, a little crooked. No readable text anywhere in the frame, no taxi meter "
    "lettering, no signage, no plates."
)

def build_prompt():
    return " ".join([PREAMBLE, IDENTITY, ANTI_DRIFT, CLOSURE, HARDWARE_LAW, SCALE, SCENE, PHOTOREAL])

def api(url, payload=None, timeout=180):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=H, method="POST" if data else "GET")
    return json.loads(urllib.request.urlopen(req, timeout=timeout, context=CTX).read().decode(), strict=False)

def upload(path):
    cache = load(UPCACHE, {}); k = os.path.basename(path)
    if k in cache and time.time() - cache[k]["t"] < 60000: return cache[k]["url"]
    out = subprocess.run(["curl", "-s", "-X", "POST", "https://kieai.redpandaai.co/api/file-stream-upload",
        "-H", f"Authorization: Bearer {KEY}", "-F", f"file=@{path}", "-F", "uploadPath=images/velantra-haaland"],
        capture_output=True, text=True, timeout=180)
    url = (json.loads(out.stdout, strict=False).get("data") or {}).get("downloadUrl")
    if not url: raise RuntimeError("upload failed: " + out.stdout[:200])
    cache[k] = {"url": url, "t": time.time()}; save(UPCACHE, cache); return url

def create(prompt, urls):
    d = api("https://api.kie.ai/api/v1/jobs/createTask", {"model": MODEL,
        "input": {"prompt": prompt, "input_urls": urls, "aspect_ratio": RATIO, "resolution": RES}})
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

if __name__ == "__main__":
    prompt = build_prompt(); open(os.path.join(HERE, "cab_prompt.txt"), "w").write(prompt)
    if "irkin" in prompt or "erm" + "es" in prompt.lower(): raise SystemExit("claims-grep: banned word in prompt")
    urls = [upload(p) for p in REFS]; state = load(STATE, {}); spent = 0
    for v in range(1, VARIANTS + 1):
        dest = os.path.join(OUT, f"v{v}.png")
        if os.path.exists(dest) and os.path.getsize(dest) > 50000: print(f"v{v} cached"); continue
        ekey = f"cab.v{v}"; ent = state.get(ekey, {}); ok = False
        for attempt in range(6):
            try:
                tid = ent.get("tid") or create(prompt, urls); ent["tid"] = tid; state[ekey] = ent; save(STATE, state)
                url, cost = poll(tid)
                subprocess.run(["curl", "-sS", "-A", "Mozilla/5.0", "-o", dest, url], check=True, timeout=300)
                ent.update(done=True, cost=cost); state[ekey] = ent; save(STATE, state)
                spent += cost if isinstance(cost, (int, float)) else 0; print(f"v{v} ok ({cost})", flush=True); ok = True; break
            except Exception as e:
                ent["tid"] = None; state[ekey] = ent; save(STATE, state)
                print(f"  v{v} attempt {attempt+1} failed: {str(e)[:140]}", flush=True); time.sleep(10 + attempt * 10)
        if not ok: print(f"v{v} FAIL")
    print("credits spent:", spent)
