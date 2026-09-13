#!/usr/bin/env python3
"""Column-split R4's type band (left wordmark vs right tagline/kicker) and
resolve R5's merged body/attribution rows."""
import numpy as np
from PIL import Image, ImageFilter
import os
REFS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "refs")

def hotmask(path, sat=14, hi=228, lift=22):
    rgb = Image.open(path).convert("RGB")
    a = np.asarray(rgb, float); L = np.asarray(rgb.convert("L"), float)
    bg = np.asarray(rgb.convert("L").filter(ImageFilter.GaussianBlur(24)), float)
    s = a.max(axis=2) - a.min(axis=2)
    return (L > hi) & (s < sat) & ((L - bg) > lift), L

print("=== R4 column split, y 820-960 ===")
hot, L = hotmask(os.path.join(REFS, "R4-vDTMIC.png"))
sub = hot[820:960]
cols = sub.sum(axis=0)
runs, run = [], None
for x in range(len(cols)):
    if cols[x] > 0 and run is None: run = x
    elif cols[x] == 0 and run is not None:
        if x - run > 2: runs.append([run, x])
        run = None
merged = []
for x0, x1 in runs:
    if merged and x0 - merged[-1][1] <= 30: merged[-1][1] = x1
    else: merged.append([x0, x1])
for x0, x1 in merged:
    if x1 - x0 < 20: continue
    blk = hot[820:960, x0:x1]
    rows = np.where(blk.sum(axis=1) > 0)[0]
    # split this column group into its own row runs
    on = blk.sum(axis=1) >= 3
    rr, r = [], None
    for y in range(len(on)):
        if on[y] and r is None: r = y
        elif not on[y] and r is not None:
            if y - r >= 4: rr.append((r, y))
            r = None
    if r is not None: rr.append((r, len(on)))
    print(f" x {x0:4d}-{x1:4d} w={x1-x0:4d}")
    for r0, r1 in rr:
        seg = hot[820+r0:820+r1, x0:x1]
        c = np.where(seg.sum(axis=0) > 0)[0]
        ax0, ax1 = x0+int(c.min()), x0+int(c.max())+1
        print(f"    y {820+r0:4d}-{820+r1:4d} h={r1-r0:3d} cap={(820+r0)/1920*100:6.2f}%  "
              f"x {ax0:4d}-{ax1:4d} w={ax1-ax0:4d}  right_edge={ax1}")

print("\n=== R5 rows, y 400-580 (fine) ===")
hot, L = hotmask(os.path.join(REFS, "R5-V7icXf.jpg"), sat=30, hi=200, lift=18)
on = hot[400:580].sum(axis=1) >= 5
rr, r = [], None
for y in range(len(on)):
    if on[y] and r is None: r = y
    elif not on[y] and r is not None:
        if y - r >= 4: rr.append((r, y)); 
        r = None
if r is not None: rr.append((r, len(on)))
for r0, r1 in rr:
    seg = hot[400+r0:400+r1]
    c = np.where(seg.sum(axis=0) > 0)[0]
    print(f"  y {400+r0:4d}-{400+r1:4d} h={r1-r0:3d} cap={(400+r0)/1920*100:6.2f}%  "
          f"x {int(c.min()):4d}-{int(c.max())+1:4d} w={int(c.max())+1-int(c.min()):4d} "
          f"cx={(int(c.min())+int(c.max())+1)/2:6.1f}")
