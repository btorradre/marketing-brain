#!/usr/bin/env python3
"""VEL-MARGOT-BEST-01 — composite grids.

  grids.py            rebuild ../assets/cards/hook-grid-5up.jpg and cta-grid-6colorway.jpg

HOOK GRID LAW (Brooks, 2026-07-26, inherited from the Sofia BEST build): the grid
must show exactly as many bags as the VO claims to rank. The script says "I ranked
all five," so the hook grid holds FIVE — the four named competitors plus the
Margot. If the lineup ever changes, this file changes with it.

The Margot sits in an ordinary cell, unlabelled and un-emphasised. It is on screen
from second zero and is not revealed as #1 until ~60s — the answer hiding in
plain sight. Do NOT move it to the centred fifth slot; that telegraphs the ending.
The Row takes the centred slot: it is the first bag the VO names and the strongest
silhouette on white.
"""
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.normpath(os.path.join(HERE, "..", "assets"))
COMP = os.path.join(ASSETS, "competitors")
MARGOT = os.path.join(ASSETS, "margot")
CARDS = os.path.join(ASSETS, "cards")
W, H = 1080, 1920

# 2 + 2 + 1, every cell an identical 540x640 portrait, fifth centred bottom row.
HOOK_CELLS = [
    (os.path.join(COMP, "polene-cyme-620-front.png"),        0,    0, 540, 640),
    (os.path.join(COMP, "longchamp-lepliage-180-0.png"),   540,    0, 540, 640),
    (os.path.join(COMP, "cuyana-system-358-hero-clean.jpg"),       0,  640, 540, 640),
    (os.path.join(MARGOT, "WORK-K01-margot-hero.png"),     540,  640, 540, 640),
    (os.path.join(COMP, "therow-marlo-4300-front.jpg"),    270, 1280, 540, 640),
]

# Live Margot colorways, pulled from the Shopify CDN (velantra-meridian-tote).
CTA_ORDER = ["brown", "black", "coffee-brown", "cream", "taupe", "burgundy"]


def cover(path, cw, ch):
    """Scale to cover the cell, then centre-crop. Never distorts the bag."""
    im = Image.open(path).convert("RGB")
    s = max(cw / im.width, ch / im.height)
    im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS)
    l, t = (im.width - cw) // 2, (im.height - ch) // 2
    return im.crop((l, t, l + cw, t + ch))


def hook_grid():
    grid = Image.new("RGB", (W, H), (240, 238, 234))
    for path, x, y, cw, ch in HOOK_CELLS:
        grid.paste(cover(path, cw, ch), (x, y))
    dest = os.path.join(CARDS, "hook-grid-5up.jpg")
    grid.save(dest, quality=93)
    print(f"  hook-grid-5up.jpg  {grid.size}  ({len(HOOK_CELLS)} bags)")
    return grid


def cta_grid():
    cols, rows = 2, 3
    cw, ch = W // cols, H // rows
    grid = Image.new("RGB", (W, H), (231, 227, 219))     # oat-greige seamless
    for i, slug in enumerate(CTA_ORDER):
        p = os.path.join(MARGOT, "colorways", f"{slug}.jpg")
        grid.paste(cover(p, cw, ch), ((i % cols) * cw, (i // cols) * ch))
    dest = os.path.join(CARDS, "cta-grid-6colorway.jpg")
    grid.save(dest, quality=93)
    print(f"  cta-grid-6colorway.jpg  {grid.size}  ({len(CTA_ORDER)} colorways)")
    return grid


def preview(base, card_names, out):
    img = base.convert("RGBA")
    for n in card_names:
        img = Image.alpha_composite(img, Image.open(os.path.join(CARDS, n)).convert("RGBA"))
    img.convert("RGB").save(os.path.join(ASSETS, out), quality=92)
    print(f"  {out}")


if __name__ == "__main__":
    os.makedirs(CARDS, exist_ok=True)
    print("building grids ->", CARDS)
    hg = hook_grid()
    cg = cta_grid()
    preview(hg, ["card-hook-a.png", "card-hook-b.png"], "_preview-hook.jpg")
    preview(cg, ["card-cta.png"], "_preview-cta.jpg")
