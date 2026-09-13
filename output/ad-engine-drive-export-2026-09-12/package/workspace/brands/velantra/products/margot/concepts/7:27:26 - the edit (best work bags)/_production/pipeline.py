#!/usr/bin/env python3
"""VEL-MARGOT-EDIT-01 pipeline — kie.ai. Clone of the VEL-SOFIA-EDIT-02 runner.

  pipeline.py prompts [K00 S01 ...]   print assembled prompts, no API calls
  pipeline.py images  [K00 ...]       GPT Image 2 keyframes (~10 cr each)
                                      margot frames i2i-seed from the live
                                      burgundy PDP hero, others t2i from Camille
  pipeline.py poll-images
  pipeline.py videos  [S01 ...]       Seedance 2.0 std i2v, native audio (~69 cr/s)
  pipeline.py poll-videos
  pipeline.py status

Resume loop: `images`/`videos` skip anything already downloaded, so re-running
after an auto-top-up queues the next affordable batch. Seedance pre-authorises
~130 cr x duration, so a 6s clip needs ~780 cr free even though it charges ~414.
"""
import json, os, ssl, subprocess, sys, time, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import blocks as B

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.normpath(os.path.join(HERE, "..", "assets"))
STATE_PATH = os.path.join(HERE, "state.json")
API = "https://api.kie.ai/api/v1/jobs"
UPLOAD_URL = "https://kieai.redpandaai.co/api/file-stream-upload"
IMG_MODEL = "gpt-image-2-image-to-image"
VID_MODEL = "bytedance/seedance-2"          # std only. seedance-2-fast is BANNED.
CAMILLE = ("/Users/brooksorradre2/Documents/marketing brain/brands/velantra/_shared/"
           "ugc-creators/Camille/camille-ref.png")
KEY = None


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
    """kie file upload 403s via urllib — curl -F is the working path."""
    last = ""
    for attempt in range(4):
        if attempt:
            time.sleep(10 * attempt)
        out = subprocess.run(
            ["curl", "-s", "-X", "POST", UPLOAD_URL,
             "-H", f"Authorization: Bearer {KEY}",
             "-F", f"file=@{path}",
             "-F", "uploadPath=velantra-margot-edit1",
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


def camille_url():
    st = state()
    if not st["uploads"].get("camille"):
        st["uploads"]["camille"] = upload_file(CAMILLE)
        save(st)
        print(f"uploaded camille ref: {st['uploads']['camille']}")
    return st["uploads"]["camille"]


def download(url, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    out = subprocess.run(["curl", "-sL", "--fail", "-A", "Mozilla/5.0", "-o", dest, url],
                         capture_output=True, text=True)
    if out.returncode != 0 or not os.path.getsize(dest):
        raise RuntimeError(f"download failed ({out.returncode}) for {url}")


def pick(items, ids, idx=0):
    return [i for i in items if not ids or any(x in i[idx] for x in ids)]


def cmd_prompts(ids):
    for name, cw, blocking in pick(B.KEYFRAMES, ids):
        print(f"===== IMAGE {name} ({cw}) =====\n{B.image_prompt(cw, blocking)}\n")
    for shot in pick(B.SHOTS, ids):
        print(f"===== VIDEO {shot[0]} ({shot[1]}s, key={shot[2]}, {shot[3]}) =====\n{B.video_prompt(*shot)}\n")


def cmd_images(ids):
    st = state()
    cam = camille_url()
    for name, bag, blocking in pick(B.KEYFRAMES, ids):
        if os.path.exists(os.path.join(ASSETS, "keyframes", f"{name}.png")):
            print(f"{name}: already downloaded, skipping")
            continue
        # Margot frames get the live burgundy PDP hero as the second reference.
        urls = [cam, B.MARGOT_HERO] if name in B.MARGOT_KEYS else [cam]
        payload = {"model": IMG_MODEL, "input": {
            "prompt": B.image_prompt(bag, blocking),
            "input_urls": urls,
            "aspect_ratio": "9:16",
            "resolution": "2K"}}
        r = api("/createTask", payload)
        if r.get("code") != 200:
            print(f"{name} CREATE FAIL: {r}")
            continue
        st["images"][name] = {"taskId": r["data"]["taskId"], "state": "created"}
        print(f"{name} image task {r['data']['taskId']}")
        save(st)
        time.sleep(4)          # createTask rate-limits: pace submits ~4s apart


def cmd_videos(ids):
    st = state()
    for shot in pick(B.SHOTS, ids):
        sid, dur, keyframe = shot[0], shot[1], shot[2]
        if os.path.exists(os.path.join(ASSETS, "clips", f"{sid}.mp4")):
            print(f"{sid}: already downloaded, skipping")
            continue
        img = st["images"].get(keyframe, {})
        frame_url = img.get("resultUrl")
        if not frame_url:
            local = os.path.join(ASSETS, "keyframes", f"{keyframe}.png")
            if os.path.exists(local):                      # regenerated/replaced frames
                key = f"kf::{keyframe}"
                if not st["uploads"].get(key):
                    st["uploads"][key] = upload_file(local)
                    save(st)
                frame_url = st["uploads"][key]
            else:
                print(f"{sid}: keyframe {keyframe} not ready, skipping")
                continue
        bal = credits()
        if bal < 130 * dur:
            print(f"{sid}: balance {bal} < {130 * dur} pre-auth, stopping. Re-run after top-up.")
            return
        # NOTE: reference_audio_urls and first_frame_url are mutually exclusive (HTTP 422).
        # Voice consistency comes from the identical tone line in every prompt.
        payload = {"model": VID_MODEL, "input": {
            "prompt": B.video_prompt(*shot),
            "first_frame_url": frame_url,
            "aspect_ratio": "9:16",
            "resolution": "720p",
            "duration": dur,
            "generate_audio": True}}
        r = api("/createTask", payload)
        if r.get("code") != 200:
            print(f"{sid} CREATE FAIL: {r}")
            if "insufficient" in json.dumps(r).lower():
                return
            continue
        st["videos"][sid] = {"taskId": r["data"]["taskId"], "state": "created"}
        print(f"{sid} video task {r['data']['taskId']} ({dur}s)")
        save(st)
        time.sleep(4)


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


def cmd_status():
    st = state()
    print(f"credits: {credits()}")
    for kind in ("images", "videos"):
        print(f"== {kind} ==")
        for sid, rec in sorted(st[kind].items()):
            print(f"  {sid}: {rec.get('state')} {rec.get('failMsg', '')}")


if __name__ == "__main__":
    load_key()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    args = sys.argv[2:]
    {"prompts": lambda: cmd_prompts(args),
     "images": lambda: cmd_images(args),
     "poll-images": lambda: poll("images", "keyframes", ".png"),
     "videos": lambda: cmd_videos(args),
     "poll-videos": lambda: poll("videos", "clips", ".mp4"),
     "status": cmd_status}.get(cmd, lambda: print(__doc__))()
