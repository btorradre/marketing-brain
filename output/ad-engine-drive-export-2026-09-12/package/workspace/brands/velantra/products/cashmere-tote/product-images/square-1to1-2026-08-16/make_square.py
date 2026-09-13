"""Reframe Colette studio shots to 1:1 with the bag FILLING the frame.

v1 of this padded the sides out to the full portrait height, which dropped the bag from
83.5% to 55.7% of frame width. That shrank the bag (against the never-shrink-a-bag rule)
and broke the colour swatch, because the theme builds swatches with
`image_url: width:80, height:80, crop:'center'` — on a portrait source that zooms into
the bag, but on an already-square source there is nothing left to crop, so the swatch
showed the whole airy frame.

So: size the square to the BAG, not to the source height. Crop away empty backdrop
vertically, pad horizontally only as far as needed, and never resample product pixels.
Normalising on bag HEIGHT also makes the bag read at a consistent size across the gallery.
"""
from PIL import Image
import numpy as np
import glob, os

SRC, OUT = "fullres", "square"
os.makedirs(OUT, exist_ok=True)

FILL_H = 0.86   # bag height as a share of the square
MAX_FILL_W = 0.90  # never let the bag get wider than this share
EDGE = 24
SHADOW_SAFE = 0.60

for path in sorted(glob.glob(f"{SRC}/*.png")):
    name = os.path.basename(path)
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(np.float64)
    h, w, _ = a.shape

    top = int(h * SHADOW_SAFE)
    strip = np.concatenate([a[:top, :EDGE, :].reshape(-1, 3),
                            a[:top, -EDGE:, :].reshape(-1, 3)])
    bg = np.median(strip, axis=0)
    noise = float(np.mean([a[:top, :EDGE, :].std(axis=1).mean(),
                           a[:top, -EDGE:, :].std(axis=1).mean()]))

    # bag bounds (include the contact shadow so we never clip it)
    dev = np.abs(a - bg).max(axis=2)
    cols = np.where((dev > 28).sum(axis=0) > h * 0.01)[0]
    rows = np.where((dev > 28).sum(axis=1) > w * 0.01)[0]
    x0, x1, y0, y1 = int(cols.min()), int(cols.max()), int(rows.min()), int(rows.max())
    bw, bh = x1 - x0 + 1, y1 - y0 + 1

    S = int(round(max(bh / FILL_H, bw / MAX_FILL_W)))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    left, top_ = cx - S // 2, cy - S // 2   # window in source coords (may fall outside)

    canvas = np.empty((S, S, 3), dtype=np.float64)
    canvas[:, :, :] = bg

    src_x0, src_x1 = max(0, left), min(w, left + S)
    src_y0, src_y1 = max(0, top_), min(h, top_ + S)
    dst_x0, dst_y0 = src_x0 - left, src_y0 - top_
    canvas[dst_y0:dst_y0 + (src_y1 - src_y0),
           dst_x0:dst_x0 + (src_x1 - src_x0), :] = a[src_y0:src_y1, src_x0:src_x1, :]

    # feather the pasted edges into the fill wherever we padded, so no hard step shows
    def feather_edge(axis_len, start, end, horizontal):
        F = 40
        for i in range(F):
            t = (i + 0.5) / F
            if horizontal:
                if start > 0:
                    c = start + i
                    canvas[:, c, :] = canvas[:, c, :] * t + bg * (1 - t)
                if end < S:
                    c = end - 1 - i
                    canvas[:, c, :] = canvas[:, c, :] * t + bg * (1 - t)
            else:
                if start > 0:
                    r = start + i
                    canvas[r, :, :] = canvas[r, :, :] * t + bg * (1 - t)
                if end < S:
                    r = end - 1 - i
                    canvas[r, :, :] = canvas[r, :, :] * t + bg * (1 - t)

    feather_edge(S, dst_x0, dst_x0 + (src_x1 - src_x0), True)
    feather_edge(S, dst_y0, dst_y0 + (src_y1 - src_y0), False)

    # grain only where we filled
    rng = np.random.default_rng(4242)
    mask = np.ones((S, S, 1))
    mask[dst_y0:dst_y0 + (src_y1 - src_y0), dst_x0:dst_x0 + (src_x1 - src_x0), :] = 0.0
    canvas += rng.normal(0.0, max(noise, 0.4), (S, S, 3)) * mask

    Image.fromarray(np.clip(canvas, 0, 255).astype(np.uint8)).save(f"{OUT}/{name}", "PNG", optimize=True)
    print(f"{name}: {w}x{h} -> {S}x{S} | bag {bw}x{bh} | fills {bw/S*100:.1f}% W / {bh/S*100:.1f}% H "
          f"(was {bw/w*100:.1f}% W in portrait)")
