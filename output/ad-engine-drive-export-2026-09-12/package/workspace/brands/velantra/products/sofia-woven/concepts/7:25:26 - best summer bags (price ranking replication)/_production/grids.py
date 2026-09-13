#!/usr/bin/env python3
"""VEL-SOFIA-BEST-01 — composite grids.

  grids.py            rebuild ../assets/cards/hook-grid-5up.jpg and cta-grid-8colorway.jpg

HOOK GRID LAW: the grid must show exactly as many bags as the VO claims to rank.
The script says "I ranked all five," so the hook grid holds FIVE — the four named
competitors plus the Sofia. A four-cell grid under a five-bag script is a
congruence break the viewer feels in the first two seconds even if they cannot
name it. If the lineup ever changes, this file changes with it.

The Sofia sits in an ordinary cell, unlabelled and un-emphasised. It is on screen
from second zero and is not revealed as #1 until ~61s — the answer hiding in
plain sight. Do NOT move it to the wide cell; that telegraphs the ending.
"""
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.normpath(os.path.join(HERE, "..", "assets"))
COMP = os.path.join(ASSETS, "competitors")
SOFIA = os.path.join(ASSETS, "sofia")
CARDS = os.path.join(ASSETS, "cards")
W, H = 1080, 1920

# 2 + 2 + 1, every cell an identical 540x640 portrait. The fifth is CENTRED on the
# bottom row rather than stretched full-width: these are all tall product shots on
# white, and a 1080x640 letterbox crop decapitates them (tried it — Saint Laurent
# lost both the strap tops and the base). Matching cells also make the five read as
# one set rather than four-plus-a-banner.
HOOK_CELLS = [
    (os.path.join(COMP, "prada-crochet-front.jpg"),                0,    0, 540, 640),
    (os.path.join(COMP, "loewe-basket-690-front.jpg"),           540,    0, 540, 640),
    (os.path.join(COMP, "cultgaia-ark-198-front.jpg"),             0,  640, 540, 640),
    (os.path.join(SOFIA, "BEST-K01-sofia-hero.png"),             540,  640, 540, 640),
    (os.path.join(COMP, "saintlaurent-panier-medium-2700-A.jpg"), 270, 1280, 540, 640),
]

CTA_ORDER = ["caramel", "cream", "light-chocolate", "caban-black",
             "sky-blue", "lightning-orange", "lady-pink", "sunny-yellow"]


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
    cols, rows = 2, 4
    cw, ch = W // cols, H // rows
    grid = Image.new("RGB", (W, H), (231, 227, 219))     # oat-greige seamless
    for i, slug in enumerate(CTA_ORDER):
        p = os.path.join(SOFIA, "colorways", f"{slug}.jpg")
        grid.paste(cover(p, cw, ch), ((i % cols) * cw, (i // cols) * ch))
    dest = os.path.join(CARDS, "cta-grid-8colorway.jpg")
    grid.save(dest, quality=93)
    print(f"  cta-grid-8colorway.jpg  {grid.size}  ({len(CTA_ORDER)} colorways)")
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
    old = os.path.join(CARDS, "hook-grid-4up.jpg")
    if os.path.exists(old):
        os.remove(old)
        print("  removed stale hook-grid-4up.jpg")
