#!/usr/bin/env python3
"""White-type detector for the busy reference photographs.

The plain row-deviation scan drowns in the photograph itself on the on-body
references. White ad type has a signature the photograph does not: pixels very
near 255 that sit well ABOVE a heavily blurred version of the same frame (the
local background). Thresholding on that lift isolates the glyphs.
"""
import os, sys
import numpy as np
from PIL import Image, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REFS = os.path.join(ROOT, "refs")

def white_blocks(path, lift=30, hi=205, minpx=8, gap=12):
    im = Image.open(path).convert("L")
    a = np.asarray(im, dtype=float)
    bg = np.asarray(im.filter(ImageFilter.GaussianBlur(28)), dtype=float)
    hot = (a > hi) & ((a - bg) > lift)
    H, W = a.shape
    rows = hot.sum(axis=1)
    on = rows >= minpx
    runs, run = [], None
    for y in range(H):
        if on[y] and run is None: run = y
        elif not on[y] and run is not None:
            runs.append([run, y]); run = None
    if run is not None: runs.append([run, H])
    merged = []
    for y0, y1 in runs:
        if merged and y0 - merged[-1][1] <= gap: merged[-1][1] = y1
        else: merged.append([y0, y1])
    out = []
    for y0, y1 in merged:
        if y1 - y0 < 7: continue
        sub = hot[y0:y1]
        cols = np.where(sub.sum(axis=0) > 0)[0]
        if len(cols) < 12: continue
        x0, x1 = int(cols.min()), int(cols.max()) + 1
        # background luminance behind the glyphs: median of NON-hot pixels in the box
        box = a[y0:y1, x0:x1]; m = ~hot[y0:y1, x0:x1]
        bgl = float(np.median(box[m])) if m.any() else 0.0
        out.append(dict(y0=y0, y1=y1, h=y1-y0, cap=y0/H, x0=x0, x1=x1, w=x1-x0,
                        cx=(x0+x1)/2, bg=bgl, n=int(hot[y0:y1].sum())))
    return out, W, H

for f in sorted(os.listdir(REFS)):
    if f.startswith("_") or not f.lower().endswith((".png",".jpg")): continue
    res, W, H = white_blocks(os.path.join(REFS, f))
    print(f"\n=== {f} ({W}x{H}) ===")
    for b in res:
        print(f"  y {b['y0']:4d}-{b['y1']:4d} h={b['h']:3d} cap={b['cap']*100:6.2f}%  "
              f"x {b['x0']:4d}-{b['x1']:4d} w={b['w']:4d} cx={b['cx']:6.1f} "
              f"(off {b['cx']-W/2:+7.1f}) bgL={b['bg']:5.1f} px={b['n']}")
