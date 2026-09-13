#!/usr/bin/env python3
"""Measure the type geometry of each Vestirsi reference so compose.py can land 1:1.

Row scan: text rows are rows carrying many pixels that deviate strongly from
their own row median (which tracks the photographic background). Runs of such
rows are grouped into blocks; per block we report the cap-top / baseline as a
fraction of frame height, the ink x-extents, and the background luminance
behind the glyphs (the legibility target compose.py has to reproduce).
"""
import os, sys
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REFS = os.path.join(ROOT, "refs")

def blocks(path, dev=26, minpx=14, gap=9):
    im = Image.open(path).convert("L")
    a = np.asarray(im, dtype=float)
    H, W = a.shape
    med = np.median(a, axis=1, keepdims=True)
    d = a - med
    hot = np.abs(d) > dev
    rows = hot.sum(axis=1)
    on = rows >= minpx
    out, run = [], None
    for y in range(H):
        if on[y] and run is None:
            run = y
        elif not on[y] and run is not None:
            if y - run >= 3:
                out.append((run, y))
            run = None
    if run is not None:
        out.append((run, H))
    merged = []
    for y0, y1 in out:
        if merged and y0 - merged[-1][1] <= gap:
            merged[-1][1] = y1
        else:
            merged.append([y0, y1])
    res = []
    for y0, y1 in merged:
        if y1 - y0 < 8:
            continue
        sub = hot[y0:y1]
        cols = np.where(sub.sum(axis=0) > 0)[0]
        if len(cols) == 0:
            continue
        x0, x1 = int(cols.min()), int(cols.max()) + 1
        sign = float(np.sign(d[y0:y1][hot[y0:y1]].mean()))
        bg = float(np.median(a[y0:y1, max(0, x0 - 40):min(W, x1 + 40)]))
        res.append(dict(y0=y0, y1=y1, h=y1 - y0, cappct=y0 / H, botpct=y1 / H,
                        x0=x0, x1=x1, w=x1 - x0, cx=(x0 + x1) / 2,
                        ink="light" if sign > 0 else "dark", bg=bg))
    return res, W, H

for f in sorted(os.listdir(REFS)):
    if f.startswith("_") or not f.lower().endswith((".png", ".jpg")):
        continue
    res, W, H = blocks(os.path.join(REFS, f))
    print(f"\n=== {f}  ({W}x{H}) ===")
    for b in res:
        print(f"  y {b['y0']:4d}-{b['y1']:4d}  h={b['h']:3d}  cap={b['cappct']*100:6.2f}%  "
              f"x {b['x0']:4d}-{b['x1']:4d}  w={b['w']:4d}  cx={b['cx']:6.1f} "
              f"(centre off {b['cx']-W/2:+6.1f})  ink={b['ink']}  bgL={b['bg']:5.1f}")
