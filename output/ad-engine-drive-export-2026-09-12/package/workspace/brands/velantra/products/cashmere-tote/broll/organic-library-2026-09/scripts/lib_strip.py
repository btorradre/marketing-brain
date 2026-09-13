#!/usr/bin/env python3
"""lib_strip.py ID [ID...] -> probes/lib_<first>.jpg : 8 evenly spaced frames of the TRIMMED library file, one row per clip."""
import os, subprocess, sys
from PIL import Image, ImageDraw
from common import *
files = load(os.path.join(STATE, "library_files.json"), {})
rows = []
for cid in sys.argv[1:]:
    p = os.path.join(ROOT, "BROLL_LIBRARY", files[cid])
    d = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p],capture_output=True,text=True).stdout.strip() or 0)
    tiles = []
    for i in range(8):
        t = max(0.05, d * (i + 0.5) / 8); out = f"/tmp/lib_{cid}_{i}.jpg"
        subprocess.run(["ffmpeg","-y","-loglevel","error","-ss",f"{t:.2f}","-i",p,"-frames:v","1","-vf","scale=180:320",out])
        if os.path.exists(out): tiles.append(Image.open(out).convert("RGB"))
    row = Image.new("RGB", (180*8, 320), "black")
    for i, im in enumerate(tiles): row.paste(im, (i*180, 0))
    ImageDraw.Draw(row).text((6,6), f"{cid} {d:.1f}s", fill="yellow"); rows.append(row)
sheet = Image.new("RGB", (1440, 320*len(rows)), "black")
for i, r in enumerate(rows): sheet.paste(r, (0, i*320))
out = os.path.join(ROOT, "probes", f"lib_{sys.argv[1]}.jpg"); sheet.save(out, quality=85); print(out)
