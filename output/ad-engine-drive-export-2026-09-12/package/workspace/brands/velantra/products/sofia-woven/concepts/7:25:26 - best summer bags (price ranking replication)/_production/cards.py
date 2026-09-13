#!/usr/bin/env python3
"""VEL-SOFIA-BEST-01 — on-screen type cards as transparent 1080x1920 PNGs.

ffmpeg here has NO drawtext and NO libass, so every caption ships as a PNG
overlay. Style is matched to the reference reel: heavy white sans, thick black
stroke, tight leading, centered.

  cards.py            render every card into ../assets/cards/
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "assets", "cards"))
W, H = 1080, 1920
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

# name, lines, y-anchor as fraction of height, size, stroke
CARDS = [
    ("hook-a",     ["THE BEST SUMMER BAGS", "ON THE INTERNET"],  0.335, 88,  10),
    ("hook-b",     ["AT EVERY PRICE POINT"],                       0.665, 88,  10),

    ("rank-5",     ["#5", "SAINT LAURENT PANIER", "$2,700"],        0.20, 88,  10),
    ("rank-4",     ["#4", "PRADA CROCHET TOTE", "$2,050"],          0.20, 88,  10),
    ("rank-3",     ["#3", "LOEWE BASKET BAG", "$690"],              0.20, 88,  10),
    ("rank-2",     ["#2", "CULT GAIA ARK", "$198"],                 0.20, 88,  10),
    ("rank-1",     ["#1", "THE SOFIA", "$119.99"],                  0.20, 96,  11),

    ("cta",        ["COMMENT", '"SOFIA"'],                          0.42, 110, 12),
]


SAFE_W = int(W * 0.90)          # never let type touch the frame edge


def fit_size(d, lines, size, stroke):
    """Shrink until the widest line clears the safe area. Stroke counts."""
    while size > 20:
        f = ImageFont.truetype(FONT, size)
        widest = max(d.textbbox((0, 0), ln, font=f, stroke_width=stroke)[2]
                     - d.textbbox((0, 0), ln, font=f, stroke_width=stroke)[0]
                     for ln in lines)
        if widest <= SAFE_W:
            return size
        size -= 2
    return size


def render(name, lines, anchor, size, stroke):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    size = fit_size(d, lines, size, stroke)
    f = ImageFont.truetype(FONT, size)
    lh = int(size * 1.16)
    total = lh * len(lines)
    y = int(H * anchor) - total // 2
    for line in lines:
        bbox = d.textbbox((0, 0), line, font=f, stroke_width=stroke)
        x = (W - (bbox[2] - bbox[0])) // 2 - bbox[0]
        d.text((x, y), line, font=f, fill=(255, 255, 255, 255),
               stroke_width=stroke, stroke_fill=(0, 0, 0, 255))
        y += lh
    dest = os.path.join(OUT, f"card-{name}.png")
    img.save(dest)
    print(f"  {os.path.basename(dest)}")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    print(f"rendering {len(CARDS)} cards -> {OUT}")
    for c in CARDS:
        render(*c)
