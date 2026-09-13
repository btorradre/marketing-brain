#!/usr/bin/env python3
"""Regenerate 4 Weekender PDP images at true scale via kie GPT Image 2 i2i. 3 variants each."""
import json, os, sys, time, urllib.request, subprocess, pathlib

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "fixes"
OUT.mkdir(exist_ok=True)
KEY = None
for line in open("/Users/brooksorradre2/Documents/marketing brain/.env"):
    if line.startswith("KIE_API_KEY="):
        KEY = line.split("=", 1)[1].strip()
assert KEY

HERO_LC = "https://cdn.shopify.com/s/files/1/0627/4092/2433/files/hero1.webp?v=1783703263"
HERO_AG = "https://cdn.shopify.com/s/files/1/0627/4092/2433/files/green1_86cf21f0-ff84-4f5a-8009-cb98c6a259f2.webp?v=1783703262"

IDENTITY_LC = "a structured two tone weekend bag, wider than tall, rich cognac brown leather upper flap section and two rolled cognac leather top handles over a cream ivory woven canvas body, a small gold oval turn lock on the front, two flat gold clasp plates with cognac leather belt straps threaded through them, a small cognac leather key bell tied to the handle base, cognac leather corner patches at the bottom, visible stitching, gold hardware, no logos anywhere on the bag, natural cream cotton canvas interior lining with a cognac leather slip pocket on the back wall"
IDENTITY_AG = IDENTITY_LC.replace("cream ivory woven canvas body", "deep army green twill canvas body")

HARDEN = "The bag in frame is an exact copy of the bag in the second attached image in silhouette, proportions, materials and details. The two rolled top handles are smooth simple leather tubes with no wrapping, no braiding and no woven texture. BOTH clasp plates are the SAME warm brass gold, the right plate identical in colour to the left plate, no silver, no chrome, no white metal on any hardware."

def scale_block(anchor):
    return ("SCALE IS CRITICAL. The bag is a LARGE TRAVEL BAG, exactly 18 inches wide by 14.5 inches tall by 7 inches deep, "
            "big enough to pack two to three days of clothes. It is not a handbag and not a purse, and it is also never larger "
            "than these true dimensions. " + anchor)

def preamble(subject):
    return ("Use the first attached image as the exact scene to recreate: same " + subject + ", same background, same lighting, "
            "same camera angle, same photographic style, same colour grade, same crop. Use the second attached image only as the "
            "reference for the bag's construction, materials, colours and hardware. Recreate the scene with ONE change only: "
            "the rendered size of the bag. ")

FOOTER = " The finished picture must be indistinguishable in style, colour grade and lighting from the first attached image. No text, no lettering, no logos, no graphics anywhere in the frame."

JOBS = [
    {
        "name": "fix-02-lc-on-luggage",
        "base": "https://cdn.shopify.com/s/files/1/0627/4092/2433/files/weekender-lc-on-luggage.png?v=1783800546",
        "ref": HERO_LC,
        "prompt": preamble("hotel corridor, same rolling carry-on suitcase")
            + scale_block("The bag sits on top of the rolling carry-on suitcase. The suitcase shell is 14 inches wide and 22 inches tall. "
                          "The bag is WIDER than the suitcase: its body overhangs the suitcase shell by roughly two inches on each side. "
                          "The bag body including its leather flap stands two thirds as tall as the suitcase shell, clearly bigger than it reads in the first attached image. "
                          "The trolley handle rises behind the bag.")
            + " " + IDENTITY_LC + ". " + HARDEN + FOOTER,
    },
    {
        "name": "fix-05-lc-on-arm",
        "base": "https://cdn.shopify.com/s/files/1/0627/4092/2433/files/weekender-lc-on-arm.png?v=1783800547",
        "ref": HERO_LC,
        "prompt": preamble("woman, same pose, same clothing")
            + scale_block("The bag hangs from her forearm. Its width equals the length of her forearm from elbow to knuckles, 18 inches, never wider. "
                          "The bag body from the top of the leather flap to the bottom edge is 14.5 inches tall, reaching from her waist to the top of her thigh. "
                          "It reads slightly smaller than in the first attached image, at its true 18 inch width.")
            + " " + IDENTITY_LC + ". " + HARDEN + FOOTER,
    },
    {
        "name": "fix-09-lc-modelcarry",
        "base": "https://cdn.shopify.com/s/files/1/0627/4092/2433/files/img6.webp?v=1783703262",
        "ref": HERO_LC,
        "prompt": preamble("woman, same pose, same clothing")
            + scale_block("She holds the bag by both rolled handles in one hand at her side, in front of her legs. "
                          "The bag's 18 inch width is slightly narrower than the span of her shoulders, never wider than her shoulder span. "
                          "With her arm relaxed the top of the leather flap sits at her hip and the bottom of the bag reaches just above her knee. "
                          "It reads slightly narrower than in the first attached image.")
            + " " + IDENTITY_LC + ". " + HARDEN + FOOTER,
    },
    {
        "name": "fix-13-ag-on-arm",
        "base": "https://cdn.shopify.com/s/files/1/0627/4092/2433/files/weekender-ag-on-arm.png?v=1783800550",
        "ref": HERO_AG,
        "prompt": preamble("woman, same pose, same clothing")
            + scale_block("The bag hangs from her forearm. Its width equals the length of her forearm from elbow to knuckles, 18 inches, never wider. "
                          "The bag body from the top of the leather flap to the bottom edge is 14.5 inches tall, reaching from her waist to the top of her thigh. "
                          "It reads slightly smaller than in the first attached image, at its true 18 inch width.")
            + " " + IDENTITY_AG + ". " + HARDEN + FOOTER,
    },
]

def api(path, payload=None):
    url = "https://api.kie.ai/api/v1/" + path
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"})
    if payload is not None:
        req.data = json.dumps(payload).encode()
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode(), strict=False)

tasklog = OUT / "taskids.json"
log = json.loads(tasklog.read_text()) if tasklog.exists() else {}

def create(job, v):
    key = f"{job['name']}-v{v}"
    if key in log:
        return log[key]
    for attempt in range(6):
        try:
            r = api("jobs/createTask", {"model": "gpt-image-2-image-to-image", "input": {
                "prompt": job["prompt"],
                "input_urls": [job["base"], job["ref"]],
                "aspect_ratio": "1:1",
                "resolution": "2K",
            }})
            tid = r.get("data", {}).get("taskId")
            if tid:
                log[key] = tid
                tasklog.write_text(json.dumps(log, indent=1))
                print(f"[{key}] task {tid}", flush=True)
                return tid
            print(f"[{key}] no taskId: {r}", flush=True)
        except Exception as e:
            print(f"[{key}] createTask attempt {attempt}: {e}", flush=True)
        time.sleep(8)
    return None

def poll(key, tid):
    for _ in range(120):
        try:
            r = api(f"jobs/recordInfo?taskId={tid}")
            st = r.get("data", {}).get("state")
            if st == "success":
                res = json.loads(r["data"]["resultJson"], strict=False)
                return res.get("resultUrls", [None])[0]
            if st == "fail":
                print(f"[{key}] FAILED: {r['data'].get('failMsg')}", flush=True)
                return None
        except Exception as e:
            print(f"[{key}] poll err: {e}", flush=True)
        time.sleep(10)
    return None

def download(key, url):
    dest = OUT / (key + ".png")
    try:
        subprocess.run(["curl", "-sf", "-A", "Mozilla/5.0", "-o", str(dest), url], check=True, timeout=180)
        print(f"[{key}] saved {dest.name} ({dest.stat().st_size} bytes)", flush=True)
        return True
    except Exception as e:
        print(f"[{key}] download failed: {e} url={url}", flush=True)
        (OUT / (key + ".url.txt")).write_text(url)
        return False

for job in JOBS:
    for v in (1, 2, 3):
        key = f"{job['name']}-v{v}"
        if (OUT / (key + ".png")).exists():
            print(f"[{key}] exists, skip", flush=True)
            continue
        tid = create(job, v)
        if not tid:
            continue
        url = poll(key, tid)
        if url:
            download(key, url)

print("DONE", flush=True)
