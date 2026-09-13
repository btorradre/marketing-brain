#!/usr/bin/env python3
"""Delphine B-roll v3 — DC and AG colorways as SINGLE-VARIABLE recolours of the LC picks.

The established Delphine workflow (PRODUCT-TRUTH.md 4, and the route the Eleanor's dark
chocolate gallery took): author every shot in Light Chocolate, then change exactly one
variable to produce the other colorways. Composition, cast, wardrobe, setting, light and
framing stay pixel-identical across the three colorways, which is what a B-roll library
wants and costs a fraction of re-authoring.

Two things this script must not lose, both learned the hard way:

  * The recolour has to state that ALL leather is ONE shade and ONE finish, or the flap
    drifts lighter/greyer than the handles. Caught on Army Green during the gallery build.
  * The frame being edited is already a real photograph. The prompt therefore preserves
    the photographic character explicitly -- grain, blown highlights, imperfect focus,
    creasing, dust -- because a recolour pass will happily "clean up" the very artefacts
    that took the v3 regeneration to earn (feedback_no_3d_render_look).

Coverage matches the existing library: 8 shots per secondary colorway.
AG has no interior photograph, so there is no AG load-in shot. Same reason B03 stays
LC-only: inventing a lining colour is not allowed.
"""
import json, os, subprocess, time

ROOT = os.path.dirname(os.path.abspath(__file__))
VAULT = "/Users/brooksorradre2/Documents/marketing brain"
PICKS = os.path.join(ROOT, "v3", "picks")
API = "https://api.kie.ai/api/v1"
UPLOAD = "https://kieai.redpandaai.co/api/file-stream-upload"
ATTEMPTS = 5

KEY = None
with open(os.path.join(VAULT, ".env")) as f:
    for line in f:
        if line.startswith("KIE_API_KEY="):
            KEY = line.split("=", 1)[1].strip()
assert KEY, "KIE_API_KEY not found"
H = {"Authorization": f"Bearer {KEY}"}

SHOTS = ["B01-closet", "B02-flatlay", "B04-standsquare", "B05-walking",
         "B06-elbow", "B09-bench", "B10-wall", "B12-doorway"]

PRESERVE = (
    "Change NOTHING else in the photograph. The framing, the crop, the camera angle, the "
    "composition, the person, her pose, her hands, her clothing, the background, every object "
    "in the scene and the exact direction, colour and intensity of the light all stay exactly as "
    "they are, pixel for pixel. This is a real photograph taken on a phone and it must still look "
    "like one afterwards: keep the existing film grain and digital sensor noise, keep the blown "
    "out highlights where the light hits, keep the slightly imperfect focus and any handheld "
    "motion blur, keep the creasing and scuffing in the leather, keep the woven fibre texture in "
    "the canvas, and keep the dust, lint and fingerprints. Do not sharpen it, do not clean it up, "
    "do not brighten it, do not retouch it and do not make it look like a catalogue product "
    "photograph. No text, lettering or graphics anywhere."
)

RECOLOUR = {
    "DC": ("Change ONLY the colour of the bag's LEATHER. Every leather part of the handbag becomes "
           "a very dark espresso chocolate brown that reads nearly black in shadow: the domed flap, "
           "the leather band, both rolled top handles, both belt straps, the corner patches and the "
           "hanging clochette tag. All of that leather is ONE single shade and ONE single finish, "
           "with no part of it lighter, greyer or warmer than the rest. The lower canvas body stays "
           "exactly the cream ivory it already is, and all the gold hardware stays exactly the warm "
           "brass gold it already is. " + PRESERVE),

    "AG": ("Change ONLY the colour of the bag's CANVAS. The lower canvas body of the handbag becomes "
           "a deep muted olive green that reads almost solid. Every leather part of the bag stays "
           "exactly the warm chestnut brown it already is -- the domed flap, the leather band, both "
           "rolled top handles, both belt straps, the corner patches and the clochette tag are ONE "
           "single shade and ONE single finish, unchanged. All the gold hardware stays exactly the "
           "warm brass gold it already is. " + PRESERVE),
}


def api(url, payload=None, headers=None):
    cmd = ["curl", "-s", "--max-time", "120", url]
    for k, v in (headers or {}).items():
        cmd += ["-H", f"{k}: {v}"]
    if payload is not None:
        cmd += ["-H", "Content-Type: application/json", "-d", json.dumps(payload)]
    out = subprocess.run(cmd, capture_output=True, text=True).stdout
    try:
        return json.loads(out)
    except Exception:
        return {"code": -1, "raw": out[:400]}


def fetch(url, dest):
    subprocess.run(["curl", "-s", "-L", "--max-time", "300", "-o", dest, url], check=True)
    return os.path.getsize(dest)


def upload(path):
    out = subprocess.run(
        ["curl", "-s", "-X", "POST", UPLOAD,
         "-H", f"Authorization: Bearer {KEY}",
         "-F", f"file=@{path}",
         "-F", "uploadPath=images/delphine-broll-v3-recolour"],
        capture_output=True, text=True).stdout
    d = json.loads(out)
    assert d.get("success") or d.get("code") == 200, f"upload failed {path}: {out[:300]}"
    return (d.get("data") or {}).get("downloadUrl") or d["data"]["fileUrl"]


def submit(url, cw):
    payload = {"model": "gpt-image-2-image-to-image",
               "input": {"prompt": RECOLOUR[cw], "input_urls": [url],
                         "aspect_ratio": "9:16", "resolution": "2K"}}
    d = api(f"{API}/jobs/createTask", payload, H)
    if d.get("code") != 200:
        payload["input"]["resolution"] = "1K"
        d = api(f"{API}/jobs/createTask", payload, H)
    return d["data"]["taskId"] if d.get("code") == 200 else None


def main():
    jobs = [(cw, s) for cw in ("DC", "AG") for s in SHOTS
            if not os.path.exists(os.path.join(PICKS, f"{cw}-{s}.png"))]
    if not jobs:
        print("all recolours present")
        return

    cache = {}
    for _, s in jobs:
        if s not in cache:
            cache[s] = upload(os.path.join(PICKS, f"LC-{s}.png"))
            print(f"uploaded LC-{s}", flush=True)

    tries, pending = {}, {}
    for cw, s in jobs:
        name = f"{cw}-{s}"
        tries[name] = 1
        tid = submit(cache[s], cw)
        if tid:
            pending[name] = (tid, cw, s)
            print(f"{name}: task {tid}", flush=True)
        time.sleep(2)

    deadline = time.time() + 3600
    while pending and time.time() < deadline:
        time.sleep(15)
        for name, (tid, cw, s) in list(pending.items()):
            d = api(f"{API}/jobs/recordInfo?taskId={tid}", None, H)
            st = (d.get("data") or {}).get("state")
            if st == "success":
                rj = json.loads(d["data"]["resultJson"], strict=False)
                size = fetch(rj["resultUrls"][0], os.path.join(PICKS, f"{name}.png"))
                print(f"{name}: DONE ({size // 1024} KB)", flush=True)
                del pending[name]
            elif st == "fail":
                print(f"{name}: failed: {(d.get('data') or {}).get('failMsg')}", flush=True)
                del pending[name]
                if tries[name] < ATTEMPTS:
                    tries[name] += 1
                    tid2 = submit(cache[s], cw)
                    if tid2:
                        pending[name] = (tid2, cw, s)
                        print(f"{name}: retry (attempt {tries[name]})", flush=True)

    if pending:
        print(f"TIMEOUT still pending: {list(pending)}", flush=True)
    print(f"picks dir now holds {len(os.listdir(PICKS))} files", flush=True)


if __name__ == "__main__":
    main()
