#!/usr/bin/env python3
"""Attempt-3 fallback: animate failing keyframes with Kling 3.0 on kie.ai
(engine change per blocking-escalation law). Usage: kling_fallback.py K02 K05
"""
import json, os, subprocess, sys, time, urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
VAULT = "/Users/brooksorradre2/Documents/marketing brain"
API = "https://api.kie.ai/api/v1"
UPLOAD = "https://kieai.redpandaai.co/api/file-stream-upload"

KEY = None
with open(os.path.join(VAULT, ".env")) as f:
    for line in f:
        if line.startswith("KIE_API_KEY="):
            KEY = line.split("=", 1)[1].strip()
assert KEY

PIN = ("The leather flap stays ONE single seamless sheet folded all the way over, lying completely flat the "
       "entire clip: no gap, seam, or split ever opens anywhere in it, nothing behind it ever shows through it, "
       "and its cut edge shapes never separate into pieces. The bag keeps its exact construction, straw weave "
       "texture and colors identical every frame.")

PROMPTS = {
    "K02": "Nearly still cinemagraph, locked camera. The woman stands motionless on the dock holding the bag at her side, only her hair and dress hem sway gently in the harbor breeze, soft water glitter behind. The bag hangs completely still and rigid. " + PIN,
    "K05": "Nearly still macro cinemagraph, locked camera, no focus change. The fingertips rest motionless on the leather flap edge, only a soft light shimmer moves across the scene. The leather and straw keep their exact texture and color every frame. " + PIN,
    "K08": "Nearly still cinemagraph, locked camera. The woman stands motionless on the dune path holding the bag, only the beach grass and her dress hem sway gently in the breeze. The bag hangs completely still and rigid. " + PIN,
    "K09": "Nearly still cinemagraph, locked camera. The bag sits completely still on the dock post, only the water glitters and boats bob very gently in the blurred background. " + PIN,
}
KEYFRAME = {"K02": "K02-dock-walk.png", "K05": "K05-leather-macro.png",
            "K08": "K08-beach-path.png", "K09": "K09-dock-post.png"}


def api(url, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers={
        "Authorization": f"Bearer {KEY}",
        **({"Content-Type": "application/json"} if data else {})})
    for a in range(4):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read().decode(), strict=False)
        except Exception as e:
            if a == 3:
                raise
            time.sleep(5 * (a + 1))


def upload(path):
    out = subprocess.run(["curl", "-s", "-X", "POST", UPLOAD,
                          "-H", f"Authorization: Bearer {KEY}",
                          "-F", f"file=@{path}",
                          "-F", "uploadPath=boatkin-vo",
                          "-F", f"fileName={int(time.time())}-{os.path.basename(path).replace(' ', '_')}"],
                         capture_output=True, text=True)
    d = json.loads(out.stdout, strict=False)
    return d["data"]["downloadUrl"]


def main(targets):
    tasks = {}
    for k in targets:
        url = upload(os.path.join(ROOT, "keyframes", KEYFRAME[k]))
        payload = {"model": "kling-3.0/video",
                   "input": {"prompt": PROMPTS[k], "image_urls": [url],
                             "duration": "6", "mode": "std", "sound": False,
                             "multi_shots": False}}
        d = api(f"{API}/jobs/createTask", payload)
        assert d.get("code") == 200, f"{k}: {d}"
        tasks[k] = d["data"]["taskId"]
        print(f"{k}: kling task {tasks[k]}", flush=True)
    deadline = time.time() + 1800
    while tasks and time.time() < deadline:
        time.sleep(20)
        for k, tid in list(tasks.items()):
            d = api(f"{API}/jobs/recordInfo?taskId={tid}")
            st = (d.get("data") or {}).get("state")
            if st == "success":
                rj = json.loads(d["data"]["resultJson"], strict=False)
                url = rj["resultUrls"][0]
                out = os.path.join(ROOT, "clips", f"{k}.mp4")
                subprocess.run(["curl", "-s", "-A", "Mozilla/5.0", "-o", out, url], check=True)
                print(f"{k}: DONE {os.path.getsize(out)//1024} KB", flush=True)
                del tasks[k]
            elif st == "fail":
                print(f"{k}: KLING FAILED {d['data'].get('failMsg')}", flush=True)
                del tasks[k]
    if tasks:
        print(f"TIMEOUT: {list(tasks)}", flush=True)


if __name__ == "__main__":
    main(sys.argv[1:] or ["K02", "K05"])
