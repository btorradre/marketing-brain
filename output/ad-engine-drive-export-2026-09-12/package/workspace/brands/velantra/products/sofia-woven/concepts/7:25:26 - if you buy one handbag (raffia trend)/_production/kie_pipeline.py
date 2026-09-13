#!/usr/bin/env python3
"""VEL-SOFIA-ONEBAG-01 asset pipeline (kie.ai).

S01-S05 -> stills only.  S06-S09 -> keyframe then Kling 3.0 i2v b-roll.

Usage:
  kie_pipeline.py upload
  kie_pipeline.py images [S01 ...]      # default: all shots
  kie_pipeline.py poll-images
  kie_pipeline.py videos [S06 ...]      # default: all kind=broll shots
  kie_pipeline.py poll-videos
  kie_pipeline.py prompts [S01 ...]
  kie_pipeline.py status
"""
import json, os, ssl, subprocess, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = json.load(open(os.path.join(HERE, "manifest.json")))
STATE_PATH = os.path.join(HERE, "state.json")
ASSETS = os.path.normpath(os.path.join(HERE, "..", "assets"))
KEY = None
API = "https://api.kie.ai/api/v1/jobs"
UPLOAD_URL = "https://kieai.redpandaai.co/api/file-stream-upload"
IMG_MODEL = "gpt-image-2-image-to-image"
VID_MODEL = "kling-3.0/video"


def ctx():
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


def load_key():
    global KEY
    for line in open("/Users/brooksorradre2/Documents/marketing brain/.env"):
        if line.startswith("KIE_API_KEY="):
            KEY = line.strip().split("=", 1)[1]
    assert KEY, "KIE_API_KEY not found"


def credits():
    req = urllib.request.Request("https://api.kie.ai/api/v1/chat/credit",
                                 headers={"Authorization": f"Bearer {KEY}"})
    with urllib.request.urlopen(req, context=ctx(), timeout=60) as r:
        return json.loads(r.read().decode(), strict=False).get("data")


def state():
    return json.load(open(STATE_PATH)) if os.path.exists(STATE_PATH) else {"uploads": {}, "images": {}, "videos": {}}


def save(st):
    json.dump(st, open(STATE_PATH, "w"), indent=1)


def api(path, payload=None):
    data = json.dumps(payload).encode() if payload else None
    req = urllib.request.Request(API + path, data=data, headers={
        "Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, context=ctx(), timeout=120) as r:
        return json.loads(r.read().decode(), strict=False)


def upload_file(path):
    last = ""
    for attempt in range(4):
        if attempt:
            time.sleep(10 * attempt)
        out = subprocess.run(
            ["curl", "-s", "-X", "POST", UPLOAD_URL,
             "-H", f"Authorization: Bearer {KEY}",
             "-F", f"file=@{path}",
             "-F", "uploadPath=velantra-onebag",
             "-F", f"fileName={int(time.time())}-{os.path.basename(path).replace(' ', '_')}"],
            capture_output=True, text=True)
        try:
            resp = json.loads(out.stdout)
        except ValueError:
            last = out.stdout or out.stderr
            continue
        if resp.get("data", {}).get("downloadUrl"):
            return resp["data"]["downloadUrl"]
        last = out.stdout
    raise RuntimeError(f"upload failed for {path}: {last[:300]}")


def cmd_upload():
    st = state()
    for name, path in MANIFEST["refs"].items():
        url = upload_file(path)
        st["uploads"][name] = url
        print(f"uploaded {name}: {url}")
    save(st)


def build_image_prompt(shot):
    return " ".join([shot["keyframe_prompt"], MANIFEST["product_lock"],
                     MANIFEST["flap_closed_pin"], MANIFEST["style_line"]])


def build_video_prompt(shot):
    return " ".join([shot["motion_prompt"], MANIFEST["kling_flap_pin"], MANIFEST["imperfections"]])


def shots_by_id(ids, kind=None):
    out = MANIFEST["shots"]
    if kind:
        out = [s for s in out if s["kind"] == kind]
    if ids:
        out = [s for s in out if s["id"] in ids]
    return out


def cmd_prompts(ids):
    for shot in shots_by_id(ids):
        print(f"===== {shot['id']} ({shot['time']}, {shot['kind']}, {shot['dur']}s) =====")
        print("-- IMAGE --\n" + build_image_prompt(shot))
        if shot["kind"] == "broll":
            print("-- VIDEO --\n" + build_video_prompt(shot))
        print()


def cmd_images(ids):
    st = state()
    ups = st["uploads"]
    assert ups, "run upload first"
    for shot in shots_by_id(ids):
        res = MANIFEST["image_resolution_still"] if shot["kind"] == "still" else MANIFEST["image_resolution_broll"]
        payload = {"model": IMG_MODEL, "input": {
            "prompt": build_image_prompt(shot),
            "input_urls": [ups["caramel"]],
            "aspect_ratio": MANIFEST["aspect_ratio"],
            "resolution": res}}
        r = api("/createTask", payload)
        if r.get("code") != 200:
            print(f"{shot['id']} CREATE FAIL: {r}")
            continue
        st["images"][shot["id"]] = {"taskId": r["data"]["taskId"], "state": "created"}
        print(f"{shot['id']} image task {r['data']['taskId']} ({res})")
        save(st)


def download(url, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    out = subprocess.run(["curl", "-sL", "--fail", "-A", "Mozilla/5.0", "-o", dest, url],
                         capture_output=True, text=True)
    if out.returncode != 0 or not os.path.getsize(dest):
        raise RuntimeError(f"download failed ({out.returncode}) for {url}")


def poll(kind, out_dir, ext):
    st = state()
    pending = {k: v for k, v in st[kind].items() if v.get("state") not in ("success", "fail")}
    if not pending:
        print("nothing pending")
        return
    deadline = time.time() + 45 * 60
    while pending and time.time() < deadline:
        for sid in list(pending):
            rec = st[kind][sid]
            try:
                r = api(f"/recordInfo?taskId={rec['taskId']}")
            except Exception as e:
                print(f"{sid} poll error {e}")
                continue
            d = r.get("data") or {}
            rec["state"] = d.get("state")
            if d.get("state") == "success":
                res = json.loads(d.get("resultJson") or "{}", strict=False)
                urls = res.get("resultUrls") or []
                rec["resultUrl"] = urls[0] if urls else None
                rec["credits"] = d.get("creditsConsumed")
                if rec["resultUrl"]:
                    dest = os.path.join(ASSETS, out_dir, f"{sid}{ext}")
                    download(rec["resultUrl"], dest)
                    print(f"{sid} DONE -> {dest}")
                del pending[sid]
            elif d.get("state") == "fail":
                rec["failMsg"] = d.get("failMsg")
                print(f"{sid} FAIL: {d.get('failMsg')}")
                del pending[sid]
            save(st)
        if pending:
            time.sleep(15)
    for sid in pending:
        print(f"{sid} still {st[kind][sid].get('state')} at timeout")


def cmd_videos(ids):
    st = state()
    before = credits()
    for shot in shots_by_id(ids, kind="broll"):
        img = st["images"].get(shot["id"], {})
        if not img.get("resultUrl"):
            print(f"{shot['id']}: no keyframe yet, skipping")
            continue
        payload = {"model": VID_MODEL, "input": {
            "prompt": build_video_prompt(shot),
            "image_urls": [img["resultUrl"]],
            "duration": str(shot["dur"]),
            "mode": MANIFEST["kling_mode"],
            "sound": False,
            "multi_shots": False}}
        r = api("/createTask", payload)
        if r.get("code") != 200:
            print(f"{shot['id']} CREATE FAIL: {r}")
            continue
        st["videos"][shot["id"]] = {"taskId": r["data"]["taskId"], "state": "created", "dur": shot["dur"]}
        print(f"{shot['id']} video task {r['data']['taskId']} ({shot['dur']}s)")
        save(st)
    st = state()
    st.setdefault("meter", {})["videos_before"] = before
    save(st)


def cmd_status():
    st = state()
    print(f"credits: {credits()}")
    for kind in ("images", "videos"):
        print(f"== {kind} ==")
        for sid, rec in sorted(st[kind].items()):
            print(f" {sid}: {rec.get('state')} {rec.get('failMsg', '')}")


if __name__ == "__main__":
    load_key()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    args = sys.argv[2:]
    {"upload": lambda: cmd_upload(),
     "images": lambda: cmd_images(args),
     "poll-images": lambda: poll("images", "keyframes", ".png"),
     "videos": lambda: cmd_videos(args),
     "poll-videos": lambda: poll("videos", "clips", ".mp4"),
     "prompts": lambda: cmd_prompts(args),
     "status": lambda: cmd_status()}.get(cmd, lambda: print(__doc__))()
