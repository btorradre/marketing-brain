#!/usr/bin/env python3
"""clip_strip.py ID [ID...] -> probes/strip_<first>.jpg : frames at 0.5s / 3s / 6s / 9.5s of each clip, one row per clip."""
import os, subprocess, sys
from PIL import Image, ImageDraw
from common import *
rows = []
for cid in sys.argv[1:]:
    p = os.path.join(CLIPS, f"{cid}.mp4")
    if not os.path.exists(p): continue
    tiles = []
    for t in (0.5, 3.0, 6.0, 9.5):
        out = f"/tmp/strip_{cid}_{t}.jpg"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(t), "-i", p, "-frames:v", "1", "-vf", "scale=270:480", out])
        if os.path.exists(out): tiles.append(Image.open(out).convert("RGB"))
    row = Image.new("RGB", (270 * 4, 480), "black")
    for i, im in enumerate(tiles): row.paste(im, (i * 270, 0))
    ImageDraw.Draw(row).text((6, 6), cid, fill="yellow"); rows.append(row)
sheet = Image.new("RGB", (1080, 480 * len(rows)), "black")
for i, r in enumerate(rows): sheet.paste(r, (0, i * 480))
out = os.path.join(ROOT, "probes", f"strip_{sys.argv[1]}.jpg"); sheet.save(out, quality=82); print(out)
