#!/usr/bin/env python3
"""HeyGen Avatar V render for VEL-VIV-OLDMONEY-GRID-01. usage: render_heygen.py C2 [C1 C3]
Same three API truths as the 8/31 build: /v3/assets is multipart, poll the photo avatar to
`completed` before submitting, the video POST returns data.video_id."""
import os, sys, json, time, ssl, certifi, urllib.request, urllib.error, subprocess
from pathlib import Path
from PIL import Image
HERE = Path(__file__).resolve().parent; CRE = HERE.parent; VO = HERE.parent.parent / "vo" / "VO-woman-over-40-A.mp3"
ctx = ssl.create_default_context(cafile=certifi.where())
KEY = [l.split("=",1)[1].strip().strip('"') for l in open("/Users/brooksorradre2/Documents/marketing brain/.env") if l.startswith("HEYGEN_API_KEY=")][0]
H = {"X-Api-Key": KEY}
STILLS = {"C1": "C1v2-eleanor-48-cream-silk-green.png", "C2": "C2-helen-52-navy-chignon-green.png", "C3": "C3v2-claire-45-camel-cardigan-green.png"}
def upload(path):
    out = subprocess.run(["curl","-sS","-X","POST","https://api.heygen.com/v3/assets","-H",f"X-Api-Key: {KEY}","-F",f"file=@{path}"],capture_output=True,text=True).stdout
    return json.loads(out)["data"]["asset_id"]
def upload_image(png):
    jpg = HERE / f".{Path(png).stem}.jpg"; Image.open(png).convert("RGB").save(jpg,"JPEG",quality=94); a = upload(jpg); jpg.unlink(); return a
def post(url, payload):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={**H,"Content-Type":"application/json"}, method="POST")
    return json.loads(urllib.request.urlopen(req, timeout=300, context=ctx).read())
def get(url): return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=120, context=ctx).read())
sp = HERE / "_state.json"; state = json.load(open(sp)) if sp.exists() else {}
def save(): json.dump(state, open(sp,"w"), indent=1)
names = sys.argv[1:] or ["C2"]
if "audio_asset_id" not in state: state["audio_asset_id"] = upload(VO); save()
print("audio", state["audio_asset_id"], flush=True)
for n in names:
    s = state.setdefault(n, {})
    if "image_asset_id" not in s: s["image_asset_id"] = upload_image(CRE / STILLS[n]); save()
    if not s.get("look_id"):
        d = post("https://api.heygen.com/v3/avatars", {"type":"photo","name":f"mer-oldmoney-{n}","file":{"type":"asset_id","asset_id":s["image_asset_id"]}})["data"]
        s["look_id"] = d["avatar_item"]["id"]; s["group_id"] = d["avatar_group"]["id"]; s["engines"] = d["avatar_item"].get("supported_api_engines"); save()
        print(n, "look", s["look_id"], s["engines"], flush=True)
    for _ in range(60):
        st = get(f"https://api.heygen.com/v3/avatars/{s['look_id']}")["data"].get("status")
        if st == "completed": break
        print(n, "avatar", st, flush=True); time.sleep(10)
    if not s.get("video_id"):
        payload = {"type":"avatar","avatar_id":s["look_id"],"audio_asset_id":state["audio_asset_id"],"engine":{"type":"avatar_v"},"resolution":"1080p","aspect_ratio":"auto"}
        s["submit_payload"] = payload
        for attempt in range(4):
            try:
                r = post("https://api.heygen.com/v3/videos", payload); s["video_id"] = r["data"]["video_id"]; save(); print(n, "video", s["video_id"], flush=True); break
            except urllib.error.HTTPError as e:
                body = e.read().decode(); print(n, "submit err", e.code, body[:300], flush=True)
                if attempt < 3: time.sleep(20); continue
                raise
pending = [n for n in names if not (HERE / f"{n}-heygen-green.mp4").exists()]
while pending:
    for n in list(pending):
        d = get(f"https://api.heygen.com/v3/videos/{state[n]['video_id']}")["data"]; st = d.get("status")
        if st in ("completed","success"):
            url = d.get("video_url") or d.get("url"); out = HERE / f"{n}-heygen-green.mp4"
            subprocess.run(["curl","-sL","-A","Mozilla/5.0","-o",str(out),url], check=True); print(n, "DONE", flush=True); pending.remove(n)
        elif st in ("failed","error"): print(n, "FAILED", str(d.get("error"))[:300], flush=True); pending.remove(n)
        else: print(n, st, flush=True)
    if pending: time.sleep(20)
print("all done")
