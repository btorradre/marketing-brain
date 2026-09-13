#!/usr/bin/env python3
"""Composite the audited single-bag packshots (B11A-D) into the end-card base.
Normalizes each tile's near-uniform studio background to exact #E7E3DB via
per-channel scaling (uniform transform, no masking), then lays the four bags
in a centered row on a 1080x1920 canvas. No text baked in (wordmark comped in edit).
Output: assets/broll/keyframes/B11.png (end-card base) +
        assets/broll/keyframes/B11-row.png (row strip for the family-beat Ken Burns alt).
"""
import os
from PIL import Image
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
KF = os.path.join(os.path.dirname(BASE), "assets", "broll", "keyframes")
TARGET = np.array([231.0, 227.0, 219.0])  # E7E3DB

def load_normalized(name):
    im = Image.open(os.path.join(KF, name)).convert("RGB")
    a = np.asarray(im).astype(np.float64)
    border = np.concatenate([
        a[:12].reshape(-1, 3), a[-12:].reshape(-1, 3),
        a[:, :12].reshape(-1, 3), a[:, -12:].reshape(-1, 3)])
    bg = np.median(border, axis=0)
    scale = TARGET / np.clip(bg, 1, None)
    out = np.clip(a * scale, 0, 255).astype(np.uint8)
    print(f"{name}: bg {bg.round(1)} -> scaled {tuple(scale.round(3))}")
    return Image.fromarray(out)

tiles = [load_normalized(f"B11{c}.png") for c in "ABCD"]

def crop_to_bag(im, pad=40):
    a = np.asarray(im).astype(np.int32)
    diff = np.abs(a - TARGET).sum(axis=2)
    mask = diff > 24
    ys, xs = np.where(mask)
    if len(xs) == 0: return im
    x0, x1 = max(xs.min() - pad, 0), min(xs.max() + pad, im.width)
    y0, y1 = max(ys.min() - pad, 0), min(ys.max() + pad, im.height)
    return im.crop((x0, y0, x1, y1))

tiles = [crop_to_bag(t) for t in tiles]

# real-world relative heights: boat tote, straw tote, Weekender (largest), Margot
REL = [0.78, 0.72, 1.00, 0.62]
BASE_H = 620
resized = []
for t, r in zip(tiles, REL):
    h = int(BASE_H * r)
    w = int(t.width * h / t.height)
    resized.append(t.resize((w, h), Image.LANCZOS))

GAP = 36
row_h = max(t.height for t in resized)
row_w = sum(t.width for t in resized) + GAP * 3
row = Image.new("RGB", (row_w, row_h), tuple(TARGET.astype(int)))
x = 0
for t in resized:
    row.paste(t, (x, row_h - t.height)); x += t.width + GAP  # bottom-aligned: common floor line
row.save(os.path.join(KF, "B11-row.png"))

# 9:16 end-card base
card = Image.new("RGB", (1080, 1920), tuple(TARGET.astype(int)))
scale = min(1.0, (1080 - 80) / row.width)
rw, rh = int(row.width * scale), int(row.height * scale)
rr = row.resize((rw, rh), Image.LANCZOS)
card.paste(rr, ((1080 - rw) // 2, (1920 - rh) // 2 + 80))
card.save(os.path.join(KF, "B11.png"))
print("saved B11.png (end-card base) + B11-row.png")
