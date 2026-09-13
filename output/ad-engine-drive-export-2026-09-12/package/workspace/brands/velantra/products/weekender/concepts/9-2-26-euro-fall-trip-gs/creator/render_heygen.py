#!/usr/bin/env python3
"""HeyGen Avatar V render for the Euro-fall-trip concept (product from the path). Reuses a photo-avatar look when
one exists for this creator (state.json LOOK), otherwise creates it from the green still. Drives with VO take A.
Same API truths as 8/31: /v3/assets multipart, poll the look to completed, POST /v3/videos with avatar_id+engine avatar_v."""
import os, sys, json, time, ssl, certifi, urllib.request, urllib.error, subprocess
from pathlib import Path
from PIL import Image
HERE = Path(__file__).resolve().parent; ROOT = HERE.parent; PRODUCT = str(ROOT).split("/products/")[1].split("/")[0]
VO = ROOT / "vo" / "VO-woman-over-40-A.mp3"; OUT = HERE / "renders"; OUT.mkdir(exist_ok=True)
CFG = {"vivienne": ("C2", "C2-helen-52-navy-chignon-green.png", "17cbf7839c5bbbbb6abd8417059e802a"),
       "margot":   ("C1", "C1v2-eleanor-48-cream-silk-green.png", "bdbdde455696cb94f91dda6df385abdb"),
       "weekender":("C3", "C3v2-claire-45-camel-cardigan-green.png", None)}
NAME, STILL, LOOK = CFG[PRODUCT]
ctx = ssl.create_default_context(cafile=certifi.where())
KEY = [l.split("=",1)[1].strip().strip('"') for l in open("/Users/brooksorradre2/Documents/marketing brain/.env") if l.startswith("HEYGEN_API_KEY=")][0]
H = {"X-Api-Key": KEY}
def upload(path):
    out = subprocess.run(["curl","-sS","-X","POST","https://api.heygen.com/v3/assets","-H",f"X-Api-Key: {KEY}","-F",f"file=@{path}"],capture_output=True,text=True).stdout
    return json.loads(out)["data"]["asset_id"]
def upload_image(png):
    jpg = HERE / f".{Path(png).stem}.jpg"; Image.open(png).convert("RGB").save(jpg,"JPEG",quality=94); a = upload(jpg); jpg.unlink(); return a
def post(url, payload):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={**H,"Content-Type":"application/json"}, method="POST")
    return json.loads(urllib.request.urlopen(req, timeout=300, context=ctx).read())
def get(url): return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=120, context=ctx).read())
sp = OUT / "_state.json"; state = json.load(open(sp)) if sp.exists() else {}
def save(): json.dump(state, open(sp,"w"), indent=1)
if "audio_asset_id" not in state: state["audio_asset_id"] = upload(VO); save()
print("audio", state["audio_asset_id"], flush=True)
s = state.setdefault(NAME, {})
if LOOK and not s.get("look_id"): s["look_id"] = LOOK; save()
if not s.get("look_id"):
    s["image_asset_id"] = upload_image(HERE / STILL); save()
    d = post("https://api.heygen.com/v3/avatars", {"type":"photo","name":f"eurofall-{PRODUCT}-{NAME}","file":{"type":"asset_id","asset_id":s["image_asset_id"]}})["data"]
    s["look_id"] = d["avatar_item"]["id"]; s["engines"] = d["avatar_item"].get("supported_api_engines"); save(); print(NAME, "look", s["look_id"], s["engines"], flush=True)
for _ in range(60):
    st = get(f"https://api.heygen.com/v3/avatars/{s['look_id']}")["data"].get("status")
    if st == "completed": break
    print(NAME, "avatar", st, flush=True); time.sleep(10)
if not s.get("video_id"):
    payload = {"type":"avatar","avatar_id":s["look_id"],"audio_asset_id":state["audio_asset_id"],"engine":{"type":"avatar_v"},"resolution":"1080p","aspect_ratio":"auto"}
    s["submit_payload"] = payload
    for attempt in range(4):
        try:
            r = post("https://api.heygen.com/v3/videos", payload); s["video_id"] = r["data"]["video_id"]; save(); print(NAME, "video", s["video_id"], flush=True); break
        except urllib.error.HTTPError as e:
            print(NAME, "submit err", e.code, e.read().decode()[:300], flush=True)
            if attempt < 3: time.sleep(20); continue
            raise
out = OUT / f"{NAME}-heygen-green.mp4"
while not out.exists():
    d = get(f"https://api.heygen.com/v3/videos/{s['video_id']}")["data"]; st = d.get("status")
    if st in ("completed","success"):
        url = d.get("video_url") or d.get("url"); subprocess.run(["curl","-sL","-A","Mozilla/5.0","-o",str(out),url], check=True); print(NAME, "DONE", out, flush=True); break
    if st in ("failed","error"): print(NAME, "FAILED", str(d.get("error"))[:300], flush=True); sys.exit(1)
    print(NAME, st, flush=True); time.sleep(20)
