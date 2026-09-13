#!/usr/bin/env python3
"""Render the three creators on HeyGen Avatar V, all driven by the same tightened VO.

Three things this API does that cost real time, all handled here:
  1. /v3/assets is MULTIPART (curl -F). A raw-body POST 400s.
  2. A photo avatar lands `status: processing` with image_width/height 0. Submitting a video
     against it fails "missing image dimensions" -- POLL /v3/avatars/{id} until completed.
  3. The video POST returns data.video_id, not data.id.
"""
import os, json, time, ssl, certifi, urllib.request, urllib.error, subprocess
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
CRE  = HERE.parent / "creators"
VO   = HERE.parent / "vo" / "VO-tight.mp3"
ctx  = ssl.create_default_context(cafile=certifi.where())
KEY  = subprocess.run(["bash","-lc",'set -a; source "/Users/brooksorradre2/Documents/marketing brain/.env"; set +a; echo -n "$HEYGEN_API_KEY"'],capture_output=True,text=True).stdout.strip()
H    = {"X-Api-Key": KEY}
CREATORS = ["A-diane", "B-bridget", "C-marguerite"]

def upload(path):
    out = subprocess.run(["curl","-sS","-X","POST","https://api.heygen.com/v3/assets",
        "-H", f"X-Api-Key: {KEY}", "-F", f"file=@{path}"], capture_output=True, text=True).stdout
    return json.loads(out)["data"]["asset_id"]

def upload_image(png):
    """HeyGen wants a normal-sized JPEG; the 2K PNGs are 4MB."""
    jpg = HERE / f".{Path(png).stem}.jpg"
    Image.open(png).convert("RGB").resize((1080,1626), Image.LANCZOS).save(jpg,"JPEG",quality=94)
    a = upload(jpg); jpg.unlink()
    return a

def post(url, payload):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(),
        headers={**H, "Content-Type":"application/json"}, method="POST")
    return json.loads(urllib.request.urlopen(req, timeout=300, context=ctx).read())

def get(url):
    return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=120, context=ctx).read())

state_p = HERE / "_state.json"
state = json.load(open(state_p)) if state_p.exists() else {}
def save(): json.dump(state, open(state_p,"w"), indent=1)

if __name__ == "__main__":
    if "audio_asset_id" not in state:
        state["audio_asset_id"] = upload(VO); save()
    print("audio:", state["audio_asset_id"])

    for name in CREATORS:
        s = state.setdefault(name, {})
        if "image_asset_id" not in s:
            s["image_asset_id"] = upload_image(CRE / f"{name}-green.png"); save()
        if not s.get("look_id"):
            d = post("https://api.heygen.com/v3/avatars",
                     {"type":"photo","name":f"vivienne-gs-{name}",
                      "file":{"type":"asset_id","asset_id":s["image_asset_id"]}})["data"]
            s["look_id"] = d["avatar_item"]["id"]; s["group_id"] = d["avatar_group"]["id"]
            s["engines"] = d["avatar_item"].get("supported_api_engines"); save()
            print(name, "look", s["look_id"], s["engines"])
        # 2. wait for the photo avatar to finish processing
        for _ in range(60):
            st = get(f"https://api.heygen.com/v3/avatars/{s['look_id']}")["data"].get("status")
            if st == "completed": break
            print(name, "avatar", st); time.sleep(10)
        if not s.get("video_id"):
            for attempt in range(4):
                try:
                    r = post("https://api.heygen.com/v3/videos",
                             {"type":"avatar","avatar_id":s["look_id"],
                              "audio_asset_id":state["audio_asset_id"],
                              "engine":{"type":"avatar_v"},
                              "resolution":"1080p","aspect_ratio":"auto"})
                    s["video_id"] = r["data"]["video_id"]; save()   # 3. video_id, not id
                    print(name, "video", s["video_id"]); break
                except urllib.error.HTTPError as e:
                    body = e.read().decode(); print(name, "submit err", e.code, body[:220])
                    if attempt < 3: time.sleep(20); continue
                    raise

    pending = [n for n in CREATORS if not (HERE / f"{n}-green.mp4").exists()]
    while pending:
        for name in list(pending):
            d = get(f"https://api.heygen.com/v3/videos/{state[name]['video_id']}")["data"]
            st = d.get("status")
            if st in ("completed","success"):
                url = d.get("video_url") or d.get("url")
                out = HERE / f"{name}-green.mp4"
                subprocess.run(["curl","-sL","-A","Mozilla/5.0","-o",str(out),url], check=True)
                print(name, "DONE"); pending.remove(name)
            elif st in ("failed","error"):
                print(name, "FAILED", str(d.get("error"))[:200]); pending.remove(name)
            else:
                print(name, st)
        if pending: time.sleep(20)
    print("all done")
