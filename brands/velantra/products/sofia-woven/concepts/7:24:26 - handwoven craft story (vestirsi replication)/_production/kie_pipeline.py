#!/usr/bin/env python3
"""VEL-STRAW-WOVEN-CRAFT-01 asset pipeline.
GPT Image 2 i2i keyframes -> Kling 3.0 i2v clips, all via kie.ai.

Usage:
  kie_pipeline.py upload
  kie_pipeline.py images [A B ...]      # default: all shots
  kie_pipeline.py poll-images
  kie_pipeline.py videos [A ...]        # needs poll-images done for those shots
  kie_pipeline.py poll-videos
  kie_pipeline.py prompts [A ...]       # print assembled prompts, no API calls
  kie_pipeline.py status
"""
import json, os, ssl, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = json.load(open(os.path.join(HERE, "manifest.json")))
STATE_PATH = os.path.join(HERE, "state.json")
KEY = None
API = "https://api.kie.ai/api/v1/jobs"
UPLOAD_URL = "https://kieai.redpandaai.co/api/file-stream-upload"
IMG_MODEL = "gpt-image-2-image-to-image"
VID_MODEL = "kling-3.0/video"

BANNED = ["made in italy", "italian", "italy", "made in usa", "made in the usa",
          "european", "made in europe", "birkin", "hermes", "hermès"]


def ctx():
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


def load_key():
    global KEY
    env = "/Users/brooksorradre2/Documents/marketing brain/.env"
    for line in open(env):
        if line.startswith("KIE_API_KEY="):
            KEY = line.strip().split("=", 1)[1]
    assert KEY, "KIE_API_KEY not found"


def claims_check(text, label):
    low = text.lower()
    for b in BANNED:
        if b in low:
            raise RuntimeError(f"BANNED CLAIM '{b}' in {label}")


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
    import subprocess
    last = ""
    for attempt in range(4):
        if attempt:
            time.sleep(10 * attempt)
        out = subprocess.run(
            ["curl", "-s", "-X", "POST", UPLOAD_URL,
             "-H", f"Authorization: Bearer {KEY}",
             "-F", f"file=@{path}",
             "-F", "uploadPath=velantra-woven-craft",
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
    lock = MANIFEST["product_lock"] + " " + MANIFEST["flap_closed_pin"] \
        if shot["subject"] == "product" else MANIFEST["material_lock"]
    p = " ".join([shot["keyframe_prompt"], lock, MANIFEST["style_line"]])
    claims_check(p, f"{shot['id']} image")
    return p


def build_video_prompt(shot):
    parts = [shot["motion_prompt"]]
    if shot["subject"] == "product":
        parts.append(MANIFEST["kling_flap_pin"])
    parts.append(MANIFEST["motion_footer"])
    parts.append(MANIFEST["imperfections"])
    p = " ".join(parts)
    claims_check(p, f"{shot['id']} video")
    return p


def shots_by_id(ids):
    if not ids:
        return MANIFEST["shots"]
    return [s for s in MANIFEST["shots"] if s["id"] in ids]


def cmd_prompts(ids):
    for shot in shots_by_id(ids):
        print(f"===== {shot['id']} (cuts {shot['cuts']}, {shot['time']}) subject={shot['subject']} =====")
        print("-- IMAGE --\n" + build_image_prompt(shot))
        print("-- VIDEO --\n" + build_video_prompt(shot) + "\n")


def cmd_images(ids):
    st = state()
    ups = st["uploads"]
    assert ups, "run upload first"
    for shot in shots_by_id(ids):
        payload = {"model": IMG_MODEL, "input": {
            "prompt": build_image_prompt(shot),
            "input_urls": [ups[r] for r in shot["refs"]],
            "aspect_ratio": MANIFEST["aspect_ratio"],
            "resolution": MANIFEST["image_resolution"]}}
        r = api("/createTask", payload)
        if r.get("code") != 200:
            print(f"{shot['id']} CREATE FAIL: {r}")
            continue
        st["images"][shot["id"]] = {"taskId": r["data"]["taskId"], "state": "created"}
        print(f"{shot['id']} image task {r['data']['taskId']}")
        save(st)


def download(url, dest):
    import subprocess
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
    deadline = time.time() + 40 * 60
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
                    dest = os.path.join(HERE, "..", "plates", out_dir, f"{sid}{ext}")
                    download(rec["resultUrl"], dest)
                    print(f"{sid} DONE ({d.get('creditsConsumed')}cr) -> {os.path.normpath(dest)}")
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
    for shot in shots_by_id(ids):
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
        st["videos"][shot["id"]] = {"taskId": r["data"]["taskId"], "state": "created"}
        print(f"{shot['id']} video task {r['data']['taskId']}")
        save(st)


def cmd_status():
    st = state()
    print(f"credits: {credits()}")
    for kind in ("images", "videos"):
        print(f"== {kind} ==")
        for sid, rec in sorted(st[kind].items()):
            print(f" {sid}: {rec.get('state')} cr={rec.get('credits')} fail={rec.get('failMsg', '')}")


if __name__ == "__main__":
    load_key()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    args = sys.argv[2:]
    if cmd == "upload":
        cmd_upload()
    elif cmd == "images":
        cmd_images(args)
    elif cmd == "poll-images":
        poll("images", "keyframes", ".png")
    elif cmd == "videos":
        cmd_videos(args)
    elif cmd == "poll-videos":
        poll("videos", "clips", ".mp4")
    elif cmd == "prompts":
        cmd_prompts(args)
    elif cmd == "status":
        cmd_status()
    else:
        print(__doc__)
