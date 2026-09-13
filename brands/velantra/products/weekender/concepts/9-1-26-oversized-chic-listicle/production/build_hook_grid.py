#!/usr/bin/env python3
"""Rebuild the b01 hook grid (mirrors reference beat 1: 2x2 stills, title on the seam).

usage: build_hook_grid.py <top-left panel image>
The other three panels are fixed (DC on roller / trench + silver roller / AG on forearm).
"""
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

WK = "/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/weekender"
C = os.path.join(WK, "concepts/9-1-26-oversized-chic-listicle")
OUT = os.path.join(C, "board-frames/b01.jpg")

tl = sys.argv[1]
panels = [tl,
          os.path.join(WK, "broll/dc-B13-onluggage.mp4"),
          os.path.join(WK, "images/onroute-S1_v1.png"),
          os.path.join(WK, "product-images/weekender-ag-on-arm.png")]


def fit(im, w, h):
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)))
    l = (im.width - w) // 2; t = (im.height - h) // 2
    return im.crop((l, t, l + w, t + h))


tiles = []
for i, p in enumerate(panels):
    if p.endswith(".mp4"):
        tmp = os.path.join(C, "production", f"_p{i}.jpg")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "2", "-i", p, "-frames:v", "1", tmp])
        im = Image.open(tmp)
    else:
        im = Image.open(p)
    tiles.append(fit(im.convert("RGB"), 540, 960))

grid = Image.new("RGB", (1080, 1920))
for im, xy in zip(tiles, [(0, 0), (540, 0), (0, 960), (540, 960)]):
    grid.paste(im, xy)


def font(sz):
    for f in ["/System/Library/Fonts/HelveticaNeue.ttc", "/System/Library/Fonts/Helvetica.ttc"]:
        try:
            return ImageFont.truetype(f, sz, index=1)
        except Exception:
            pass
    return ImageFont.load_default()


d = ImageDraw.Draw(grid)
y = 880
for txt, f in [("The Oversized Travel Bag", font(62)), ("That's Actually Chic", font(62)),
               ("& Worth Traveling With", font(34))]:
    bb = d.textbbox((0, 0), txt, font=f); w = bb[2] - bb[0]; x = (1080 - w) // 2
    for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (2, 2), (-2, 2), (2, -2)]:
        d.text((x + dx, y + dy), txt, font=f, fill=(0, 0, 0))
    d.text((x, y), txt, font=f, fill="white")
    y += bb[3] - bb[1] + 22

grid.save(OUT, quality=92)
print("wrote", OUT)
