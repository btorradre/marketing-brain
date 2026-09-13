#!/usr/bin/env python3
"""Build one labeled 3-variant strip per scene for the QA pass: keyframes/<id>/strip.jpg"""
import os, sys
from PIL import Image, ImageDraw, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
KF = os.path.join(HERE, "keyframes")
w, h = 360, 640
made = skipped = 0
prefix = sys.argv[1] if len(sys.argv) > 1 else ""
for sid in sorted(os.listdir(KF)):
    if not sid.startswith(prefix):
        continue
    d = os.path.join(KF, sid)
    if not os.path.isdir(d):
        continue
    vs = [os.path.join(d, f"v{i}.png") for i in (1, 2, 3)]
    have = [p for p in vs if os.path.exists(p) and os.path.getsize(p) > 10000]
    if len(have) < 2:
        skipped += 1
        continue
    out = os.path.join(d, "strip.jpg")
    if os.path.exists(out) and os.path.getmtime(out) > max(os.path.getmtime(p) for p in have):
        continue
    sheet = Image.new("RGB", (w * len(have), h + 28), (18, 18, 18))
    dr = ImageDraw.Draw(sheet)
    for i, p in enumerate(have):
        im = ImageOps.fit(Image.open(p).convert("RGB"), (w, h))
        sheet.paste(im, (i * w, 28))
        dr.text((i * w + 8, 6), os.path.basename(p).replace(".png", ""), fill=(255, 255, 80))
    sheet.save(out, quality=80)
    made += 1
print(f"strips made {made}, skipped(incomplete) {skipped}")
