#!/usr/bin/env python3
"""Composite 5 catalyst/native static ads (1:1) in the HealthLine style:
circular mechanism inset top-left + publisher bar + heavy headline with a
yellow highlight phrase. Base photos + mechanism circles are in ./src."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "src")
OUT = BASE

S = 1080
YELLOW = (255, 197, 26)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_BLACK = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

# Each ad: base photo, mechanism circle, publisher, and headline lines.
# Each line is a list of (text, is_highlight) segments.
ADS = [
    {
        "out": "ad1_celery-compound.jpg", "base": "base1.png", "circle": "circle_motility.png",
        "pub": "GUT HEALTH BLOG",
        "lines": [
            [("A NEW CELERY COMPOUND RESTORES", False)],
            [("STOMACH MOTILITY AND CAN", False)],
            [("END GLP-1 CONSTIPATION", True), (" IN 6 WEEKS", False)],
        ],
    },
    {
        "out": "ad2_wrong-organ.jpg", "base": "base3.png", "circle": "circle_stomach_colon.png",
        "pub": "GUT HEALTH BLOG",
        "lines": [
            [("NEARLY 3 IN 4 GLP-1 USERS ARE", False)],
            [("CONSTIPATED BECAUSE LAXATIVES", False)],
            [("TARGET THE WRONG ORGAN", True)],
        ],
    },
    {
        "out": "ad3_stomach-not-colon.jpg", "base": "base2.png", "circle": "circle_stomach_colon.png",
        "pub": "GUT HEALTH BLOG",
        "lines": [
            [("YOUR GLP-1 DIDN'T SLOW YOUR COLON", False)],
            [("IT SLOWED YOUR STOMACH, AND THAT'S", False)],
            [("WHY YOU'RE BACKED UP", True)],
        ],
    },
    {
        "out": "ad4_regular-again.jpg", "base": "base4.png", "circle": "circle_motility.png",
        "pub": "GUT HEALTH BLOG",
        "lines": [
            [("A GUT DOCTOR'S NEW PROTOCOL GETS", False)],
            [("OZEMPIC USERS ", False), ("REGULAR AGAIN", True)],
            [("IN AS LITTLE AS 6 WEEKS", False)],
        ],
    },
    {
        "out": "ad5_fiber-backfire.jpg", "base": "base5.png", "circle": "circle_backed_up.png",
        "pub": "GUT HEALTH BLOG",
        "lines": [
            [("THE REAL REASON MORE FIBER", False)],
            [("MAKES GLP-1 BLOATING", False)],
            [("WORSE, NOT BETTER", True)],
        ],
    },
]

def fill_square(img, size):
    return ImageOps.fit(img.convert("RGB"), (size, size), Image.LANCZOS, centering=(0.5, 0.42))

def circle_crop(img, d):
    im = ImageOps.fit(img.convert("RGB"), (d, d), Image.LANCZOS, centering=(0.5, 0.5))
    mask = Image.new("L", (d, d), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, d, d), fill=255)
    out = Image.new("RGBA", (d, d), (0, 0, 0, 0))
    out.paste(im, (0, 0), mask)
    return out

def line_width(draw, segs, font):
    return sum(draw.textlength(t, font=font) for t, _ in segs)

def fit_font(draw, lines, max_w, start=64, min_s=30):
    s = start
    while s > min_s:
        f = ImageFont.truetype(FONT_BLACK, s)
        if all(line_width(draw, ln, f) <= max_w for ln in lines):
            return f
        s -= 2
    return ImageFont.truetype(FONT_BLACK, min_s)

def build(ad):
    base = fill_square(Image.open(os.path.join(SRC, ad["base"])), S)
    canvas = base.copy()
    draw = ImageDraw.Draw(canvas)

    # ---- bottom black bar ----
    bar_h = 300
    bar_top = S - bar_h
    # subtle feather scrim above bar
    scrim = Image.new("RGBA", (S, 120), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scrim)
    for i in range(120):
        sd.line([(0, i), (S, i)], fill=(0, 0, 0, int(255 * (i / 120) ** 2 * 0.9)))
    canvas.paste(Image.new("RGB", (S, bar_h), BLACK), (0, bar_top))
    canvas.paste(scrim, (0, bar_top - 120), scrim)
    draw = ImageDraw.Draw(canvas)

    # ---- publisher row ----
    pub = ad["pub"]
    pf = ImageFont.truetype(FONT_BOLD, 24)
    pw = draw.textlength(pub, font=pf)
    dot_r = 9
    gap = 14
    total = dot_r * 2 + gap + pw
    py = bar_top + 34
    cx = S / 2
    left = cx - total / 2
    # small green logo dot
    draw.ellipse((left, py, left + dot_r * 2, py + dot_r * 2), fill=(46, 157, 79))
    tx = left + dot_r * 2 + gap
    draw.text((tx, py - 4), pub, font=pf, fill=WHITE)
    # divider lines flanking the publisher
    ly = py + dot_r
    draw.line([(60, ly), (left - 22, ly)], fill=(120, 120, 120), width=2)
    draw.line([(tx + pw + 22, ly), (S - 60, ly)], fill=(120, 120, 120), width=2)

    # ---- headline ----
    max_w = S - 100
    font = fit_font(draw, ad["lines"], max_w, start=68, min_s=30)
    asc, desc = font.getmetrics()
    lh = int((asc + desc) * 1.06)
    block_h = lh * len(ad["lines"])
    region_top = bar_top + 86
    region_bot = S - 28
    y = region_top + ((region_bot - region_top) - block_h) // 2
    for ln in ad["lines"]:
        w = line_width(draw, ln, font)
        x = (S - w) / 2
        for text, hi in ln:
            draw.text((x, y), text, font=font, fill=(YELLOW if hi else WHITE))
            x += draw.textlength(text, font=font)
        y += lh

    # ---- circular mechanism inset (top-left) ----
    d = 340
    margin = 28
    ring = 9
    circ = circle_crop(Image.open(os.path.join(SRC, ad["circle"])), d)
    # white ring + soft shadow
    ring_img = Image.new("RGBA", (d + ring * 2, d + ring * 2), (0, 0, 0, 0))
    rd = ImageDraw.Draw(ring_img)
    rd.ellipse((0, 0, d + ring * 2, d + ring * 2), fill=(255, 255, 255, 255))
    shadow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    sd2 = ImageDraw.Draw(shadow)
    sd2.ellipse((margin - 4, margin - 2, margin + d + ring * 2 + 6, margin + d + ring * 2 + 8),
                fill=(0, 0, 0, 90))
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    canvas.paste(shadow, (0, 0), shadow)
    canvas.paste(ring_img, (margin, margin), ring_img)
    canvas.paste(circ, (margin + ring, margin + ring), circ)

    path = os.path.join(OUT, ad["out"])
    canvas.save(path, "JPEG", quality=90)
    return path

if __name__ == "__main__":
    for ad in ADS:
        p = build(ad)
        print("wrote", os.path.basename(p))
