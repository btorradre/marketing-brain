#!/usr/bin/env python3
"""Regenerate 3 Dark Chocolate gallery images from the ORIGINAL LC bases (validated recolor recipe)."""
import json, time, urllib.request, subprocess, pathlib

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "dc" / "gen"
OUT.mkdir(exist_ok=True)
KEY = None
for line in open("/Users/brooksorradre2/Documents/marketing brain/.env"):
    if line.startswith("KIE_API_KEY="):
        KEY = line.split("=", 1)[1].strip()

DC_REAL = "https://tempfile.redpandaai.co/kieai/706342/images/velantra/weekender-dc-real.png"

PROMPT = ("Use the first attached image as the exact picture to edit. ONE change only: recolor every piece of leather on the bag, "
          "the flap section, the two rolled top handles, the belt straps, the side belts, the key bell, the corner patches and the trim, "
          "to the very dark espresso chocolate brown leather of the bag in the second attached image, matching its exact shade and finish. "
          "The canvas body stays exactly the same cream ivory colour and texture. All hardware stays warm brass gold: the oval turn lock, "
          "both clasp plates, the strap pegs and the buckles, no silver, no chrome. Everything else stays EXACTLY as in the first attached "
          "image: the same scene, same people, same pose, same suitcase if present, same background, same lighting, same colour grade, "
          "same crop, same photographic style, and most importantly the bag stays EXACTLY the same size and position in the frame as in "
          "the first attached image. No text, no lettering, no logos anywhere.")

JOBS = [
    {"name": "dc-02-onluggage", "base": "https://cdn.shopify.com/s/files/1/0627/4092/2433/files/weekender-lc-on-luggage.png?v=1786293350"},
    {"name": "dc-04-onarm",     "base": "https://cdn.shopify.com/s/files/1/0627/4092/2433/files/weekender-lc-on-arm.png?v=1786293357"},
    {"name": "dc-08-modelcarry","base": "https://cdn.shopify.com/s/files/1/0627/4092/2433/files/img6.jpg?v=1786293364"},
]

def api(path, payload=None):
    req = urllib.request.Request("https://api.kie.ai/api/v1/" + path,
                                 headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"})
    if payload is not None:
        req.data = json.dumps(payload).encode()
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode(), strict=False)

tasklog = OUT / "taskids.json"
log = json.loads(tasklog.read_text()) if tasklog.exists() else {}

for job in JOBS:
    for v in (1, 2, 3):
        key = f"{job['name']}-v{v}"
        if (OUT / (key + ".png")).exists():
            continue
        tid = log.get(key)
        if not tid:
            for attempt in range(6):
                try:
                    r = api("jobs/createTask", {"model": "gpt-image-2-image-to-image", "input": {
                        "prompt": PROMPT, "input_urls": [job["base"], DC_REAL],
                        "aspect_ratio": "1:1", "resolution": "2K"}})
                    tid = r.get("data", {}).get("taskId")
                    if tid:
                        log[key] = tid
                        tasklog.write_text(json.dumps(log, indent=1))
                        print(f"[{key}] task {tid}", flush=True)
                        break
                    print(f"[{key}] no taskId: {r}", flush=True)
                except Exception as e:
                    print(f"[{key}] create attempt {attempt}: {e}", flush=True)
                time.sleep(8)
        if not tid:
            continue
        url = None
        for _ in range(120):
            try:
                r = api(f"jobs/recordInfo?taskId={tid}")
                st = r.get("data", {}).get("state")
                if st == "success":
                    url = json.loads(r["data"]["resultJson"], strict=False).get("resultUrls", [None])[0]
                    break
                if st == "fail":
                    print(f"[{key}] FAILED: {r['data'].get('failMsg')}", flush=True)
                    break
            except Exception:
                pass
            time.sleep(10)
        if url:
            dest = OUT / (key + ".png")
            try:
                subprocess.run(["curl", "-sf", "-A", "Mozilla/5.0", "-o", str(dest), url], check=True, timeout=180)
                print(f"[{key}] saved ({dest.stat().st_size} bytes)", flush=True)
            except Exception as e:
                print(f"[{key}] download failed: {e} url={url}", flush=True)
                (OUT / (key + ".url.txt")).write_text(url)

print("DONE", flush=True)
