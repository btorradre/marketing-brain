#!/usr/bin/env python3
"""Round 2: percentage-reduction edits for the two scenes round 1 could not shrink."""
import json, os, time, urllib.request, subprocess, pathlib

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "fixes2"
OUT.mkdir(exist_ok=True)
KEY = None
for line in open("/Users/brooksorradre2/Documents/marketing brain/.env"):
    if line.startswith("KIE_API_KEY="):
        KEY = line.split("=", 1)[1].strip()

HERO_LC = "https://cdn.shopify.com/s/files/1/0627/4092/2433/files/hero1.webp?v=1783703263"

IDENTITY_LC = "a structured two tone weekend bag, wider than tall, rich cognac brown leather upper flap section and two rolled cognac leather top handles over a cream ivory woven canvas body, a small gold oval turn lock on the front, two flat gold clasp plates with cognac leather belt straps threaded through them, a small cognac leather key bell tied to the handle base, cognac leather corner patches at the bottom, visible stitching, gold hardware, no logos anywhere on the bag"

HARDEN = "The bag stays an exact copy of the bag in the second attached image in silhouette, proportions, materials and details. The two rolled top handles are smooth simple leather tubes with no wrapping and no braiding. BOTH clasp plates are the SAME warm brass gold, no silver, no chrome, no white metal on any hardware. The canvas keeps the exact same smooth woven texture and cream ivory colour as in the first attached image, never pebbled, never grainy."

FOOTER = " Everything else in the picture stays EXACTLY as it is in the first attached image: the same woman, same pose, same clothing, same background, same lighting, same colour grade, same crop, same photographic style. No text, no lettering, no logos anywhere."

JOBS = [
    {
        "name": "fix2-05-lc-on-arm",
        "base": "https://cdn.shopify.com/s/files/1/0627/4092/2433/files/weekender-lc-on-arm.png?v=1783800547",
        "prompt": ("Edit the first attached image. ONE change only: make the bag TWENTY FIVE PERCENT SMALLER in the frame. "
                   "The bag currently fills almost the whole width of the picture, which is wrong. After the edit the bag is a large travel bag, "
                   "18 inches wide, hanging from her forearm, and clearly more of the courtyard, her hips and her legs are visible around it. "
                   "Its width never exceeds the length of her forearm from elbow to knuckles. "
                   + IDENTITY_LC + ". " + HARDEN + FOOTER),
    },
    {
        "name": "fix2-09-lc-modelcarry",
        "base": "https://cdn.shopify.com/s/files/1/0627/4092/2433/files/img6.webp?v=1783703262",
        "prompt": ("Edit the first attached image. ONE change only: make the bag FIFTEEN PERCENT SMALLER in the frame. "
                   "After the edit the bag is a large travel bag, 18 inches wide, held by both rolled handles in her right hand at her side, "
                   "and its width is slightly NARROWER than the span of her shoulders, never wider. The top of the leather flap sits at her hip "
                   "and the bottom of the bag ends just above her knee. "
                   + IDENTITY_LC + ". " + HARDEN + FOOTER),
    },
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
                        "prompt": job["prompt"], "input_urls": [job["base"], HERO_LC],
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
