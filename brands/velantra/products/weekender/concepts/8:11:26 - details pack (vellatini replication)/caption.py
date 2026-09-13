#!/usr/bin/env python3
"""Render the reference ad's overlay-text style as a transparent 1080x1920 PNG.

Didot Italic, white, soft drop shadow, centred, small, high in frame — matched to
TrendTrack vellatini-Uzptt3.

The reference sits its text over a mid-tone cafe interior, so plain white reads.
Our beats are bright white bedrooms and marble, which washed the text out on the
first build, so a soft gradient scrim is baked behind it. The scrim is subtle
enough to stay invisible as a graphic element and only does the contrast work.
"""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONT = "/System/Library/Fonts/Supplemental/Didot.ttc"
W, H = 1080, 1920


def scrim(img, from_top=True, depth=0.30, strength=110):
    """Bake a soft linear darkening gradient at the top or bottom edge."""
    grad = Image.new("L", (1, H), 0)
    px = grad.load()
    span = int(H * depth)
    for y in range(span):
        a = int(strength * (1 - y / span) ** 1.6)
        px[0, y if from_top else H - 1 - y] = a
    grad = grad.resize((W, H))
    black = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    black.putalpha(grad)
    return Image.alpha_composite(black, img)


def render(lines, out, size=64, top_frac=0.075, line_gap=1.30, bottom=False):
    font = ImageFont.truetype(FONT, size, index=1)  # 1 = Italic
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dsh, d = ImageDraw.Draw(sh), ImageDraw.Draw(img)

    lh = int(size * line_gap)
    y0 = int(H * top_frac)

    y = y0
    for ln in lines:
        bb = d.textbbox((0, 0), ln, font=font)
        x = (W - (bb[2] - bb[0])) // 2 - bb[0]
        dsh.text((x + 2, y + 3), ln, font=font, fill=(0, 0, 0, 205))
        y += lh
    sh = sh.filter(ImageFilter.GaussianBlur(7))

    img = Image.alpha_composite(sh, img)
    d = ImageDraw.Draw(img)
    y = y0
    for ln in lines:
        bb = d.textbbox((0, 0), ln, font=font)
        x = (W - (bb[2] - bb[0])) // 2 - bb[0]
        d.text((x, y), ln, font=font, fill=(255, 255, 255, 255))
        y += lh

    depth = 0.16 if bottom else 0.30
    img = scrim(img, from_top=not bottom, depth=depth,
                strength=95 if bottom else 115)
    img.save(out)
    print("wrote", out)


if __name__ == "__main__":
    out, size, top = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
    bottom = top > 0.5
    render(sys.argv[4:], out, size=size, top_frac=top, bottom=bottom)
