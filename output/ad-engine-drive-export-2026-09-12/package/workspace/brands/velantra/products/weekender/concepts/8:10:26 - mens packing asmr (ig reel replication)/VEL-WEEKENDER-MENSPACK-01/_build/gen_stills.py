#!/usr/bin/env python3
"""Stage 1 — generate every scene still with GPT Image 2 i2i on kie.ai.

Three variants per scene (standing rule: never ship the first roll).
Sequential with a retry loop; kie throws "Internal Error" on a chunk of calls
regardless of pacing and batching makes it worse.

  python3 gen_stills.py probe S03        # one variant, prints cost
  python3 gen_stills.py run [S01 S02..]  # 3 variants for every scene (resumable)
  python3 gen_stills.py status
"""
import base64, json, os, ssl, subprocess, sys, time, urllib.request, urllib.error
import certifi

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from scenes import SCENES, REFS, build_prompt, scene_by_id

VAULT = "/Users/brooksorradre2/Documents/marketing brain"
REFDIR = os.path.join(VAULT, "brands/velantra/products/weekender/product-references/real-product-2026-08-08")
CREATOR = os.path.join(VAULT, "brands/velantra/products/weekender/concepts/"
                       "8:07:26 - mens angle replication/VEL-WEEKENDER-MENS-01/creator-ref.jpg")
KEYFRAMES = os.path.join(ROOT, "keyframes")
STATE = os.path.join(HERE, "state_stills.json")
UPCACHE = os.path.join(HERE, "upload_cache.json")

CTX = ssl.create_default_context(cafile=certifi.where())
MODEL = "gpt-image-2-image-to-image"
RATIO = os.environ.get("GI2_RATIO", "9:16")
RES = "2K"
# VSTART lets a corrected-prompt pass write v4..v6 alongside the originals so the
# rejects stay on disk and the pick is auditable across both passes.
VSTART = int(os.environ.get("VSTART", "1"))
VARIANTS = int(os.environ.get("VARIANTS", "3"))


def env(k):
    for line in open(os.path.join(VAULT, ".env")):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            a, b = line.split("=", 1)
            if a.strip() == k:
                return b.strip().strip('"').strip("'")
    raise KeyError(k)


KEY = env("KIE_API_KEY")
H = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}


def load(p, d):
    return json.load(open(p)) if os.path.exists(p) else d


def save(p, o):
    json.dump(o, open(p, "w"), indent=2)


def api(url, payload=None, timeout=180):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=H, method="POST" if data else "GET")
    raw = urllib.request.urlopen(req, timeout=timeout, context=CTX).read().decode()
    return json.loads(raw, strict=False)


def ref_path(key):
    return CREATOR if key == "creator" else os.path.join(REFDIR, REFS[key])


def upload(key):
    """Upload a local reference to kie temp storage. Cached per run."""
    cache = load(UPCACHE, {})
    if key in cache and time.time() - cache[key]["t"] < 60000:
        return cache[key]["url"]
    path = ref_path(key)
    out = subprocess.run([
        "curl", "-s", "-X", "POST", "https://kieai.redpandaai.co/api/file-stream-upload",
        "-H", f"Authorization: Bearer {KEY}",
        "-F", f"file=@{path}",
        "-F", "uploadPath=images/velantra-weekender-menspack",
    ], capture_output=True, text=True, timeout=180)
    d = json.loads(out.stdout, strict=False)
    url = (d.get("data") or {}).get("downloadUrl")
    if not url:
        raise RuntimeError(f"upload failed for {key}: {out.stdout[:300]}")
    cache[key] = {"url": url, "t": time.time()}
    save(UPCACHE, cache)
    print(f"    uploaded {key}")
    return url


def create(prompt, urls):
    d = api("https://api.kie.ai/api/v1/jobs/createTask", {
        "model": MODEL,
        "input": {"prompt": prompt, "input_urls": urls,
                  "aspect_ratio": RATIO, "resolution": RES},
    })
    if d.get("code") != 200:
        raise RuntimeError(f"createTask {d.get('code')}: {str(d)[:300]}")
    return d["data"]["taskId"]


def poll(tid, timeout_s=900):
    t0 = time.time()
    while time.time() - t0 < timeout_s:
        d = api(f"https://api.kie.ai/api/v1/jobs/recordInfo?taskId={tid}")
        data = d.get("data") or {}
        st = data.get("state")
        if st == "success":
            rj = json.loads(data["resultJson"], strict=False)
            return rj["resultUrls"][0], data.get("creditsConsumed")
        if st == "fail":
            raise RuntimeError(f"task fail: {data.get('failMsg') or str(data)[:300]}")
        time.sleep(8)
    raise TimeoutError(tid)


def download(url, dest):
    r = subprocess.run(["curl", "-sS", "-A", "Mozilla/5.0", "-o", dest, url],
                       capture_output=True, text=True, timeout=300)
    if os.path.exists(dest) and os.path.getsize(dest) > 50_000:
        return True
    # CDN filter fallback documented in reference_kie_api
    raise RuntimeError(f"download failed ({r.stderr[:200]}) for {url}")


def gen_one(s, v, state):
    sid = s["id"]
    outdir = os.path.join(KEYFRAMES, sid)
    os.makedirs(outdir, exist_ok=True)
    dest = os.path.join(outdir, f"v{v}.png")
    if os.path.exists(dest) and os.path.getsize(dest) > 50_000:
        return dest, "cached"
    prompt = build_prompt(s)
    urls = [upload(k) for k in s["refs"]]
    ekey = f"{sid}.v{v}"
    ent = state.get(ekey, {})
    last = None
    for attempt in range(6):
        try:
            tid = ent.get("tid")
            if not tid:
                tid = create(prompt, urls)
                ent["tid"] = tid
                state[ekey] = ent
                save(STATE, state)
            url, cost = poll(tid)
            download(url, dest)
            ent.update(done=True, cost=cost)
            state[ekey] = ent
            save(STATE, state)
            return dest, cost
        except Exception as e:
            last = e
            ent["tid"] = None
            state[ekey] = ent
            save(STATE, state)
            print(f"    {ekey} attempt {attempt+1} failed: {str(e)[:140]}")
            time.sleep(10 + attempt * 10)
    raise RuntimeError(f"{ekey}: {last}")


def cmd_probe(sid):
    state = load(STATE, {})
    s = scene_by_id(sid)
    print(f"probe {sid} at {RATIO}/{RES}")
    dest, cost = gen_one(s, 1, state)
    print("OK", dest, "cost:", cost)


def cmd_run(only=None):
    state = load(STATE, {})
    todo = [s for s in SCENES if not only or s["id"] in only]
    vrange = range(VSTART, VSTART + VARIANTS)
    total = len(todo) * VARIANTS
    n = 0
    spent = 0
    for s in todo:
        for v in vrange:
            n += 1
            try:
                dest, cost = gen_one(s, v, state)
                if isinstance(cost, (int, float)):
                    spent += cost
                print(f"[{n}/{total}] {s['id']} v{v} ok ({cost})", flush=True)
            except Exception as e:
                print(f"[{n}/{total}] {s['id']} v{v} FAIL {str(e)[:200]}", flush=True)
            time.sleep(3)
    print(f"done. credits spent this pass: {spent}")


def cmd_status():
    rows = []
    for s in SCENES:
        d = os.path.join(KEYFRAMES, s["id"])
        got = len([f for f in os.listdir(d) if f.endswith(".png")]) if os.path.isdir(d) else 0
        rows.append(f"{s['id']} {got}/{VARIANTS}")
    print("  ".join(rows))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "probe":
        cmd_probe(sys.argv[2])
    elif cmd == "run":
        cmd_run(sys.argv[2:] or None)
    else:
        cmd_status()
