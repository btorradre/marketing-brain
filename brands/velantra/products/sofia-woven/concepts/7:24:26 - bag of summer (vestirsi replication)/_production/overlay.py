#!/usr/bin/env python3
"""Composite the Velantra wordmark + THE BAG OF SUMMER headline onto each plate.

Text is overlaid locally (never generated) so the logo and typography are
pixel-correct on all 8 colorways. Geometry is measured off the Vestirsi
reference: wordmark centered at 13.8% height, headline centered at 21%,
headline spanning ~60% of frame width in wide-tracked light caps.

Output: final/VEL-BAGOFSUMMER-<colorway>.jpg at 1080x1920.
"""
import os, glob
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
CONCEPT = os.path.dirname(ROOT)
PLATES = os.path.join(CONCEPT, "plates")
FINAL = os.path.join(CONCEPT, "final")
LOGO = os.path.join(ROOT, "velantra_logo.png")

W, H = 1080, 1920
HEADLINE = "THE BAG OF SUMMER"
FONT_PATH = "/System/Library/Fonts/HelveticaNeue.ttc"
FONT_INDEX = 7          # Light
FONT_SIZE = 46
TRACKING = 13.0         # px added between glyphs
TARGET_W = 660          # headline target width in px
HEADLINE_CY = int(H * 0.212)
LOGO_W = 300
LOGO_CY = int(H * 0.138)


def tracked_width(font, text, tracking):
    w = 0.0
    for ch in text:
        w += font.getlength(ch) + tracking
    return w - tracking


def draw_tracked(draw, xy, text, font, tracking, fill):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill, anchor="ls")
        x += font.getlength(ch) + tracking


def main():
    os.makedirs(FINAL, exist_ok=True)

    logo = Image.open(LOGO).convert("RGBA")
    # brand wordmark ships black on transparent -> recolor to white, keep alpha
    r, g, b, a = logo.split()
    logo = Image.merge("RGBA", (a.point(lambda _: 255),) * 3 + (a,))
    logo = logo.resize((LOGO_W, max(1, round(LOGO_W * logo.size[1] / logo.size[0]))), Image.LANCZOS)

    # size the headline so it spans TARGET_W with tracking
    size, tracking = FONT_SIZE, TRACKING
    font = ImageFont.truetype(FONT_PATH, size, index=FONT_INDEX)
    tracking = (TARGET_W - sum(font.getlength(c) for c in HEADLINE)) / (len(HEADLINE) - 1)

    for p in sorted(glob.glob(os.path.join(PLATES, "*.png"))):
        name = os.path.splitext(os.path.basename(p))[0]
        im = Image.open(p).convert("RGB").resize((W, H), Image.LANCZOS)
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))

        lx = (W - logo.size[0]) // 2
        ly = LOGO_CY - logo.size[1] // 2
        layer.alpha_composite(logo, (lx, ly))

        d = ImageDraw.Draw(layer)
        tw = tracked_width(font, HEADLINE, tracking)
        ascent, descent = font.getmetrics()
        cap = ascent * 0.72
        draw_tracked(d, ((W - tw) / 2, HEADLINE_CY + cap / 2), HEADLINE, font, tracking, (255, 255, 255, 255))

        out = Image.alpha_composite(im.convert("RGBA"), layer).convert("RGB")
        dest = os.path.join(FINAL, f"VEL-BAGOFSUMMER-{name}.jpg")
        out.save(dest, "JPEG", quality=94, subsampling=0)
        print(f"{name}: {dest}", flush=True)


if __name__ == "__main__":
    main()
