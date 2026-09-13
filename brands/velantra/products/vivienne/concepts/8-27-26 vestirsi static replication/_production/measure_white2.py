#!/usr/bin/env python3
"""Second-pass white-type detector for the three on-body references.

R2/R3/R4 defeated the luminance-lift scan: the bag's specular highlights are
bright enough to pass it. Ad type has one property the leather highlights do
not — it is ACHROMATIC. Gating on low saturation as well as high luminance and
a lift over the local background isolates the glyphs cleanly.
"""
import os, sys
import numpy as np
from PIL import Image, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REFS = os.path.join(ROOT, "refs")

def scan(path, y0=0, y1=None, sat=14, hi=228, lift=22, minpx=8, gap=10):
    rgb = Image.open(path).convert("RGB")
    a = np.asarray(rgb, dtype=float)
    L = np.asarray(rgb.convert("L"), dtype=float)
    bg = np.asarray(rgb.convert("L").filter(ImageFilter.GaussianBlur(24)), dtype=float)
    s = a.max(axis=2) - a.min(axis=2)
    hot = (L > hi) & (s < sat) & ((L - bg) > lift)
    H, W = L.shape
    y1 = y1 or H
    mask = np.zeros_like(hot); mask[y0:y1] = hot[y0:y1]; hot = mask
    rows = hot.sum(axis=1); on = rows >= minpx
    runs, run = [], None
    for y in range(H):
        if on[y] and run is None: run = y
        elif not on[y] and run is not None: runs.append([run, y]); run = None
    if run is not None: runs.append([run, H])
    merged = []
    for r0, r1 in runs:
        if merged and r0 - merged[-1][1] <= gap: merged[-1][1] = r1
        else: merged.append([r0, r1])
    out = []
    for r0, r1 in merged:
        if r1 - r0 < 7: continue
        cols = np.where(hot[r0:r1].sum(axis=0) > 0)[0]
        if len(cols) < 12: continue
        x0, x1 = int(cols.min()), int(cols.max()) + 1
        box, m = L[r0:r1, x0:x1], ~hot[r0:r1, x0:x1]
        out.append((r0, r1, x0, x1, float(np.median(box[m])) if m.any() else 0.0,
                    int(hot[r0:r1].sum())))
    return out, W, H

TARGETS = {
    "R2-SdX8SZ.png": (780, 1120),
    "R3-lh5lTB.png": (800, 1120),
    "R4-vDTMIC.png": (100, 1000),
}
for f, (y0, y1) in TARGETS.items():
    res, W, H = scan(os.path.join(REFS, f), y0, y1)
    print(f"\n=== {f}  window y{y0}-{y1} ===")
    for r0, r1, x0, x1, bgl, n in res:
        print(f"  y {r0:4d}-{r1:4d} h={r1-r0:3d} cap={r0/H*100:6.2f}%  x {x0:4d}-{x1:4d} "
              f"w={x1-x0:4d} cx={(x0+x1)/2:6.1f} (off {(x0+x1)/2-W/2:+7.1f}) bgL={bgl:5.1f} px={n}")
