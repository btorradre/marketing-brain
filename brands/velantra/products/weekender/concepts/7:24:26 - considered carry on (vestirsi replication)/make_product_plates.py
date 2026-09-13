#!/usr/bin/env python3
"""Build the two lower-panel product plates from the CANONICAL reference photos.

These were originally to be generated (gen_plates.py), but the references are
already exactly what the lower panel needs: the real product, front-on, at eye
level, both colorways. Using them directly removes all generation risk — there is
no construction to QA, because these ARE the reference.

Matting: the refs sit on a near-white studio sweep. A border flood fill is not
enough — the gaps under the handle arch and between the side cinch straps and the
body are enclosed background and stay white. And a plain brightness threshold eats
the cream canvas, which is nearly as bright as the sweep.

The separator that actually works is NEUTRALITY, measured off the refs:
    studio sweep  (253,251,249) / (245,245,245)  -> channel spread <= 4
    cream canvas  (237,220,198) / (216,194,172)  -> channel spread 39-44
So background = bright AND neutral, which catches enclosed regions with no
connectivity needed. Small neutral specks (white contrast stitching, specular hits
on the gold hardware) are then filled back in by dropping background components
below MIN_BG_AREA, so the stitching cannot punch holes through the bag.

The original drop shadow is neutral and bright, so it is matted out with the sweep;
a clean soft contact shadow is drawn back in on the greige, as on the swipe.
"""
import os
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

REFS = ("/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/"
        "weekender/product-images/product images")
OUT = "plates"
FILL = (215, 207, 200)          # #D7CFC8, sampled off the swipe
CANVAS = 1600

# Neutrality (SPREAD) is what protects the canvas, not brightness — so the
# brightness floor can sit low enough to absorb the soft studio shadow without
# endangering the bag. At 236 a ragged strip of that shadow survived under the bag
# and composited onto the greige as a bright fringe.
BRIGHT = 212
SPREAD = 15                     # sweep is neutral (<=4); canvas is warm (39-44)
MIN_BG_AREA = 500               # below this, a "background" blob is stitching/specular
MIN_FG_FRAC = 0.03              # drop foreground blobs under 3% of the bag: shadow residue

SRC = {"plate-light-chocolate": "light chocolate 1.webp",
       "plate-army-green": "green 1.webp"}


def matte(img):
    """Return an alpha channel isolating the bag from the studio sweep."""
    a = np.asarray(img).astype(np.int16)
    bright = a.max(axis=2) >= BRIGHT
    neutral = (a.max(axis=2) - a.min(axis=2)) <= SPREAD
    bg = bright & neutral

    # Drop tiny "background" specks so white stitching / gold specular stay opaque.
    lbl, n = ndimage.label(bg)
    if n:
        sizes = ndimage.sum(bg, lbl, range(1, n + 1))
        small = np.isin(lbl, 1 + np.flatnonzero(sizes < MIN_BG_AREA))
        bg = bg & ~small

    # Keep only substantial foreground blobs. Any shadow residue that survives the
    # brightness/neutrality test is a thin detached strip and gets dropped here.
    fg = ~bg
    lbl, n = ndimage.label(fg)
    if n:
        sizes = ndimage.sum(fg, lbl, range(1, n + 1))
        keep = 1 + np.flatnonzero(sizes >= MIN_FG_FRAC * sizes.max())
        fg = np.isin(lbl, keep)

    alpha = Image.fromarray(np.where(fg, 255, 0).astype(np.uint8), "L")
    return alpha.filter(ImageFilter.GaussianBlur(0.7))


def main():
    os.makedirs(OUT, exist_ok=True)
    for slug, fname in SRC.items():
        img = Image.open(os.path.join(REFS, fname)).convert("RGB")
        img.thumbnail((1400, 1400), Image.LANCZOS)

        alpha = matte(img)
        box = alpha.point(lambda v: 255 if v > 40 else 0).getbbox()
        cut = img.crop(box)
        cut.putalpha(alpha.crop(box))

        # scale so the bag fills a consistent share of the plate across colorways
        target_w = int(CANVAS * 0.74)
        cut = cut.resize((target_w, round(cut.height * target_w / cut.width)), Image.LANCZOS)

        plate = Image.new("RGB", (CANVAS, CANVAS), FILL)
        cx, cy = (CANVAS - cut.width) // 2, (CANVAS - cut.height) // 2

        # soft contact shadow, replacing the ref's matted-out studio shadow
        sh = Image.new("L", (CANVAS, CANVAS), 0)
        band = Image.new("L", (int(cut.width * 0.80), int(cut.height * 0.06)), 80)
        sh.paste(band, ((CANVAS - band.width) // 2, cy + cut.height - band.height // 2))
        sh = sh.filter(ImageFilter.GaussianBlur(24))
        plate = Image.composite(Image.new("RGB", (CANVAS, CANVAS), (170, 162, 154)), plate, sh)

        plate.paste(cut, (cx, cy), cut)
        plate.save(os.path.join(OUT, f"{slug}.png"))

        holes = np.asarray(alpha.crop(box)) < 128
        print(f"{slug}: {fname} -> cut {cut.size}, {100*holes.mean():.1f}% matted out")


if __name__ == "__main__":
    main()
