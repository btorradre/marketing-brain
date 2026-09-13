#!/usr/bin/env python3
"""Per-clip QA strip: start/mid/end frames side by side -> clipqa/<id>.jpg"""
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageOps
HERE = os.path.dirname(os.path.abspath(__file__))
CLIPS, OUT = os.path.join(HERE, "clips"), os.path.join(HERE, "clipqa")
os.makedirs(OUT, exist_ok=True)
w, h = 300, 533
made = 0
for f in sorted(os.listdir(CLIPS)):
    if not f.endswith(".mp4"):
        continue
    sid = f[:-4]
    out = os.path.join(OUT, sid + ".jpg")
    src = os.path.join(CLIPS, f)
    if os.path.exists(out) and os.path.getmtime(out) > os.path.getmtime(src):
        continue
    frames = []
    okall = True
    for i, t in enumerate(("0.4", "5", "9.4")):
        fp = f"/tmp/cqa-{i}.jpg"
        r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", t, "-i", src,
                            "-frames:v", "1", fp], capture_output=True)
        if r.returncode != 0 or not os.path.exists(fp):
            okall = False
            break
        frames.append(Image.open(fp).convert("RGB"))
        os.remove(fp)
    if not okall:
        continue
    sheet = Image.new("RGB", (w * 3, h + 24), (18, 18, 18))
    dr = ImageDraw.Draw(sheet)
    for i, (im, lab) in enumerate(zip(frames, ("start", "mid", "end"))):
        sheet.paste(ImageOps.fit(im, (w, h)), (i * w, 24))
        dr.text((i * w + 8, 5), lab, fill=(255, 255, 80))
    sheet.save(out, quality=80)
    made += 1
print("clip strips made", made)
