#!/usr/bin/env python3
"""Generate the full 8-slot BLACK Weekender gallery from the Light Chocolate gallery bases.
Black is ALL BLACK LEATHER (the canvas body becomes leather too) with a caramel leather interior."""
import json, time, urllib.request, subprocess, pathlib

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "black" / "gen"
OUT.mkdir(parents=True, exist_ok=True)
KEY = None
for line in open("/Users/brooksorradre2/Documents/marketing brain/.env"):
    if line.startswith("KIE_API_KEY="):
        KEY = line.split("=", 1)[1].strip()

REF_FRONT = "https://tempfile.redpandaai.co/kieai/706342/images/velantra/black-ref-front.png"
REF_INTERIOR = "https://tempfile.redpandaai.co/kieai/706342/images/velantra/black-ref-interior.png"

CORE = (
    "Use the first attached image as the exact picture to edit. Change ONLY the bag, so that it becomes the all black leather "
    "version of the same bag shown in the second attached image. "
    "The second attached image is the real black bag and is the authority on its colour and material. "
    "CRITICAL MATERIAL CHANGE: the black bag has NO canvas anywhere. The panel that is cream ivory canvas on the bag in the first "
    "image must become smooth black leather in your result, the same black leather as the rest of the bag, so the finished bag is "
    "one single uniform black leather all over, with only a fine horizontal seam line where the upper section meets the lower body. "
    "The flap section, the two rolled top handles, the belt straps, the side belts, the key bell and the corner reinforcements are "
    "all that same smooth black leather. "
    "ALL HARDWARE STAYS WARM BRASS GOLD exactly as in the first image: the oval turn lock, both flat clasp plates, the strap pegs "
    "and the side buckles. No silver, no chrome, no white metal. "
    "The bag keeps EXACTLY the same shape, proportions, construction, stitching, hardware placement, size in the frame and position "
    "in the frame as in the first attached image. Do not resize the bag, do not move it, do not restyle it. "
)

SCENE = (
    "Everything else in the picture stays EXACTLY as it is in the first attached image: the same scene, the same people, the same "
    "pose and clothing, the same props, the same background, the same lighting, the same colour grade, the same crop and the same "
    "photographic style. No text, no lettering, no logos anywhere in the frame."
)

INTERIOR_NOTE = (
    "This shot shows the inside of the bag. The interior lining is smooth CARAMEL TAN leather with a caramel leather slip pocket, "
    "exactly as in the second attached image, against the black leather exterior. The inner face of the folded flap is black leather. "
)

JOBS = [
    {"name": "blk-01-front",        "base": "https://cdn.shopify.com/s/files/1/0627/4092/2433/files/hero1.webp?v=1783703263", "ref": REF_FRONT},
    {"name": "blk-02-onluggage",    "base": "https://cdn.shopify.com/s/files/1/0627/4092/2433/files/weekender-lc-on-luggage.png?v=1786293350", "ref": REF_FRONT},
    {"name": "blk-03-packed",       "base": "https://cdn.shopify.com/s/files/1/0627/4092/2433/files/img3.webp?v=1783703262", "ref": REF_INTERIOR, "interior": True},
    {"name": "blk-04-onarm",        "base": "https://cdn.shopify.com/s/files/1/0627/4092/2433/files/weekender-lc-on-arm.png?v=1786293357", "ref": REF_FRONT},
    {"name": "blk-05-threequarter", "base": "https://cdn.shopify.com/s/files/1/0627/4092/2433/files/img2.webp?v=1783703262", "ref": REF_FRONT},
    {"name": "blk-06-interior",     "base": "https://cdn.shopify.com/s/files/1/0627/4092/2433/files/img4.webp?v=1783703262", "ref": REF_INTERIOR, "interior": True},
    {"name": "blk-07-hardware",     "base": "https://cdn.shopify.com/s/files/1/0627/4092/2433/files/img5.webp?v=1783703263", "ref": REF_FRONT},
    {"name": "blk-08-modelcarry",   "base": "https://cdn.shopify.com/s/files/1/0627/4092/2433/files/img6.jpg?v=1786293364", "ref": REF_FRONT},
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
    prompt = CORE + (INTERIOR_NOTE if job.get("interior") else "") + SCENE
    for v in (1, 2, 3):
        key = f"{job['name']}-v{v}"
        if (OUT / (key + ".png")).exists():
            continue
        tid = log.get(key)
        if not tid:
            for attempt in range(6):
                try:
                    r = api("jobs/createTask", {"model": "gpt-image-2-image-to-image", "input": {
                        "prompt": prompt, "input_urls": [job["base"], job["ref"]],
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
        for _ in range(150):
            try:
                r = api(f"jobs/recordInfo?taskId={tid}")
                st = r.get("data", {}).get("state")
                if st == "success":
                    url = json.loads(r["data"]["resultJson"], strict=False).get("resultUrls", [None])[0]
                    break
                if st == "fail":
                    print(f"[{key}] FAILED: {r['data'].get('failMsg')}", flush=True)
                    log.pop(key, None); tasklog.write_text(json.dumps(log, indent=1))
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
