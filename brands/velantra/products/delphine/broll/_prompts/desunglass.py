#!/usr/bin/env python3
"""Remove the sunglasses from the Delphine flatlay stills WITHOUT touching the bag.

A generative i2i pass was tried first and redrew the bag as an all-leather product with no
canvas — a product-truth failure — so this is deterministic instead.

The flatlay is crowded (wallet, keys, lip balm, bag, hand, trousers), so there is no single
clean rectangle the size of the sunglasses to copy from. Instead a small clean linen SWATCH is
mirror-tiled to fill the target box, exposure-matched to the ring of pixels around the target,
then blended through a feathered mask. The target box is deliberately padded well past the
sunglasses so their tips sit inside the fully-opaque core of the mask, not the soft edge.
"""
import sys, pathlib
from PIL import Image, ImageFilter
import numpy as np

LIB = pathlib.Path("/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/delphine/broll")
BAK = LIB / "_variants"

# name -> (target box to erase, clean linen swatch box)
JOBS = {
    "LC-B02-flatlay": ((618, 560, 1116, 1058), (800, 80, 1148, 428)),
    "DC-B02-flatlay": ((618, 560, 1116, 1058), (800, 80, 1148, 428)),
    # AG still is 1520x2688; coords scaled by 1520/1152 = 1.3194
    "AG-B02-flatlay": ((815, 739, 1472, 1396), (1055, 105, 1515, 565)),
}

FEATHER = 34


def mirror_tile(swatch, w, h):
    """Fill w x h by mirror-tiling swatch, so tile seams never show as hard lines."""
    sh, sw = swatch.shape[:2]
    ny, nx = -(-h // sh) + 1, -(-w // sw) + 1
    rows = []
    for j in range(ny):
        cols = []
        for i in range(nx):
            t = swatch
            if i % 2:
                t = t[:, ::-1]
            if j % 2:
                t = t[::-1, :]
            cols.append(t)
        rows.append(np.concatenate(cols, axis=1))
    return np.concatenate(rows, axis=0)[:h, :w]


def ring_mean(arr, box, pad=30):
    x0, y0, x1, y1 = box
    h, w = arr.shape[:2]
    ox0, oy0 = max(0, x0 - pad), max(0, y0 - pad)
    ox1, oy1 = min(w, x1 + pad), min(h, y1 + pad)
    outer = arr[oy0:oy1, ox0:ox1].reshape(-1, 3)
    inner = arr[y0:y1, x0:x1].reshape(-1, 3)
    if len(outer) <= len(inner):
        return outer.mean(axis=0)
    return (outer.sum(axis=0) - inner.sum(axis=0)) / (len(outer) - len(inner))


def patch(name):
    tgt, sw_box = JOBS[name]
    bak = BAK / f"{name}-WITH-SUNGLASSES-orig.png"
    src_path = LIB / "stills" / f"{name}.png"

    # always work from the pristine original so re-runs are idempotent
    base = Image.open(bak if bak.exists() else src_path).convert("RGB")
    if not bak.exists():
        base.save(bak)

    arr = np.asarray(base).astype(np.float32)
    tw, th = tgt[2] - tgt[0], tgt[3] - tgt[1]

    swatch = np.asarray(base.crop(sw_box)).astype(np.float32)
    donor = mirror_tile(swatch, tw, th)
    donor = np.clip(donor + (ring_mean(arr, tgt) - ring_mean(arr, sw_box)), 0, 255)

    m = Image.new("L", (tw, th), 0)
    m.paste(255, (FEATHER, FEATHER, tw - FEATHER, th - FEATHER))
    m = m.filter(ImageFilter.GaussianBlur(FEATHER * 0.5))
    a = (np.asarray(m).astype(np.float32) / 255.0)[..., None]

    region = arr[tgt[1]:tgt[3], tgt[0]:tgt[2]]
    arr[tgt[1]:tgt[3], tgt[0]:tgt[2]] = donor * a + region * (1 - a)

    Image.fromarray(arr.astype(np.uint8)).save(src_path)
    print(f"patched {name} target={tgt}")


for n in (sys.argv[1:] or list(JOBS)):
    patch(n)
