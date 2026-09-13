#!/usr/bin/env python3
"""VERIFIED BUYER — composite the review-quote block onto each clean plate.

1:1 with the Vestirsi review static: full bleed 9:16 photo, wide-tracked all-caps
serif pull quote in the lower third, small sans review body under it, attribution
line with a verified badge. No box, no card — type sits directly on the photo.

Copy lives in QUOTES below. Swap the text there and re-run; plates are untouched.

Usage:  python3 overlay.py [colorway ...]      (default: all)
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageStat

ROOT = os.path.dirname(os.path.abspath(__file__))
PLATES = os.path.join(os.path.dirname(ROOT), "plates")
FINAL = os.path.join(os.path.dirname(ROOT), "final")

W, H = 1080, 1920
SS = 3                          # text supersampling factor
INK = (17, 17, 17, 255)
INK_LIGHT = (255, 255, 255, 255)

DIDOT = "/System/Library/Fonts/Supplemental/Didot.ttc"
HELV = "/System/Library/Fonts/Helvetica.ttc"

# --- COPY -------------------------------------------------------------------
# headline = the pull quote (all caps, wide tracking, in quotation marks)
# body     = the review, wrapped exactly as written (one list item per line)
# who      = attribution; rendered after a plain hyphen and followed by a verified
#            badge, exactly as the reference static sets it ("-Erin, Verified Buyer")
# Each headline must be a COMPLETE literal sentence of its own review body, not a
# clause with the comma swapped for a period — quoting "Market in the morning,
# dinner that night, and it has never..." as "MARKET IN THE MORNING, DINNER THAT
# NIGHT." is a doctored quote. `check_quotes.py` enforces sentence-level equality.
# Curly typographic marks throughout, no straight apostrophes. Attribution uses a
# plain hyphen, exactly as the reference sets it.
QUOTES = {
    "caramel": {
        "headline": "THREE PEOPLE ASKED ME WHERE IT WAS FROM.",
        "body": [
            "I took it to Nantucket for a long weekend and ended up",
            "carrying it every single day. Three people asked me where",
            "it was from. I have never had a bag do that.",
        ],
        "who": "Caroline W., Verified Buyer",
        "dy": 20,
    },
    "light-chocolate": {
        "headline": "IT STILL STANDS UP ON ITS OWN.",
        "body": [
            "Farmers market, the beach, two dinners out, and it holds its",
            "shape exactly the way it did the day it arrived. I set it down",
            "after a full day. It still stands up on its own.",
        ],
        "who": "Anne M., Verified Buyer",
    },
    "caban-black": {
        "headline": "MARKET IN THE MORNING, DINNER THAT NIGHT.",
        "body": [
            "The black leather is what sold me. Market in the morning,",
            "dinner that night. It has never once looked out of place at",
            "either one.",
        ],
        "who": "Whitney L., Verified Buyer",
    },
    "cream": {
        "headline": "IT SWALLOWS MY ENTIRE DAY.",
        "body": [
            "Laptop, water bottle, sunscreen, a paperback, and my",
            "daughter’s swim goggles. It swallows my entire day. Nothing",
            "looks stuffed and the handles have not stretched an inch.",
        ],
        "who": "Meredith K., Verified Buyer",
        "dy": 40,
    },
    "lightning-orange": {
        "headline": "THERE IS NO LOGO ON IT ANYWHERE.",
        "body": [
            "There is no logo on it anywhere. It still gets stopped more",
            "than anything else I own, and the color does all of the",
            "talking for me.",
        ],
        "who": "Juliet R., Verified Buyer",
    },
    "sky-blue": {
        "headline": "IT IS NICER IN PERSON THAN IN THE PHOTOS.",
        "body": [
            "I ordered it without seeing it first and expected to be a little",
            "let down. It is nicer in person than in the photos. The",
            "stitching and the leather are better than they look online.",
        ],
        "who": "Elise H., Verified Buyer",
    },
}

# --- LAYOUT (measured off the reference static) ------------------------------
HEAD_Y = 1228          # cap-top of the pull quote
HEAD_MAX_W = 950       # tracked line must fit inside this (keeps 60px+ safe margins)
HEAD_TRACK = 0.20      # letterspacing as a fraction of font size
HEAD_GAP = 24          # space between the pull quote and the review body
BODY_SIZE = 30
BODY_LEAD = 38
WHO_GAP = 6            # extra space above the attribution line
BADGE_R = 9

# Per-ad downward nudge of the whole type block, via an optional "dy" in QUOTES.
# Needed because the type must clear whatever hangs into the lower third and the
# clearance is a property of each pose, not of the layout. Measured, not guessed:
# cream's fingertips bottomed out at y1233 against an ink top of y1236 (3px — the
# headline read as growing out of her hand) and caramel's at y1210 (23px).
# Tried and rejected as automation: a row-gradient detector cannot separate a
# fingertip from a dress fold, and skin-tone detection fires on the warm plaster
# and linen that fills most of these backgrounds. An explicit measured offset per
# ad is honest and reviewable; a heuristic that silently misses is not.


def font(path, size, index=0):
    return ImageFont.truetype(path, size, index=index)


def tracked_width(draw, text, f, track_px):
    w = 0
    for ch in text:
        w += draw.textlength(ch, font=f) + track_px
    return w - track_px if text else 0


def draw_tracked(draw, x, y, text, f, track_px, fill):
    for ch in text:
        draw.text((x, y), ch, font=f, fill=fill)
        x += draw.textlength(ch, font=f) + track_px


def band_mean(img, y0, y1):
    return ImageStat.Stat(img.convert("L").crop((0, y0, img.width, y1))).mean[0]


def band_local_min(img, y0, y1, win=110, step=30):
    """Darkest window inside the text band.

    A full-width mean hides local darkness: one plate averaged 206 across the band
    while an open doorway on the left dropped local text contrast to 3.4:1, and no
    scrim was applied because the mean looked fine. Scrim decisions read this, not
    just the mean.
    """
    band = img.convert("L").crop((0, y0, img.width, y1))
    worst = 255.0
    for x in range(0, max(1, band.width - win + 1), step):
        m = ImageStat.Stat(band.crop((x, 0, x + win, band.height))).mean[0]
        worst = min(worst, m)
    return worst


def scrim(img, top, strength):
    """Soft white wash fading in downward, so dark type always reads."""
    grad = Image.new("L", (1, img.height), 0)
    px = grad.load()
    for y in range(img.height):
        if y <= top:
            px[0, y] = 0
        else:
            t = (y - top) / max(1, img.height - top)
            px[0, y] = int(255 * strength * min(1.0, t * 1.6))
    mask = grad.resize((img.width, img.height))
    return Image.composite(Image.new("RGB", img.size, (255, 255, 255)), img, mask)


def build(colorway):
    src = os.path.join(PLATES, f"{colorway}.png")
    if not os.path.exists(src):
        print(f"{colorway}: no plate, skip")
        return False
    q = QUOTES[colorway]

    img = Image.open(src).convert("RGB")
    # cover-fit to 1080x1920
    s = max(W / img.width, H / img.height)
    img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    img = img.crop(((img.width - W) // 2, (img.height - H) // 2,
                    (img.width - W) // 2 + W, (img.height - H) // 2 + H))

    head_y = HEAD_Y + q.get("dy", 0)

    # The reference sets black type straight onto a bright studio floor with no
    # scrim. Only lift the band when the plate cannot carry it — judged on the
    # DARKEST window in the band as well as its mean, so a local dark patch behind
    # a few glyphs cannot hide inside a healthy average.
    y0, y1 = head_y - 40, H - 60
    mean, lo = band_mean(img, y0, y1), band_local_min(img, y0, y1)
    if mean >= 198 and lo >= 185:
        strength = 0.0
    elif mean >= 168 and lo >= 150:
        strength = 0.30
    else:
        strength = 0.62
    if strength:
        img = scrim(img, head_y - 200, strength)
        mean, lo = band_mean(img, y0, y1), band_local_min(img, y0, y1)
    dark = mean < 140
    ink = INK_LIGHT if dark else INK
    print(f"{colorway}: band mean {mean:.0f}, darkest window {lo:.0f}, "
          f"scrim {strength}, ink {'light' if dark else 'dark'}")

    # Type is drawn on a transparent layer at SS times scale and downsampled, so
    # Didot's hairline crossbars survive instead of dropping out ("THERE"->"TIIERE").
    layer = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    counter = ImageDraw.Draw(Image.new("L", (1, 1)))

    # pull quote: auto-fit the tracked, quoted line to HEAD_MAX_W
    line = f'“{q["headline"]}”'
    size = 62
    while size > 26:
        f = font(DIDOT, size)
        if tracked_width(counter, line, f, size * HEAD_TRACK) <= HEAD_MAX_W:
            break
        size -= 1
    f = font(DIDOT, size)
    tw = tracked_width(counter, line, f, size * HEAD_TRACK)
    fs = font(DIDOT, size * SS)
    draw_tracked(d, (W - tw) / 2 * SS, head_y * SS, line, fs, size * HEAD_TRACK * SS, ink)

    # review body
    fb = font(HELV, BODY_SIZE)
    fbs = font(HELV, BODY_SIZE * SS)
    y = head_y + size + HEAD_GAP
    for i, ln in enumerate(q["body"]):
        text = ln
        if i == 0:
            text = "“" + text
        if i == len(q["body"]) - 1:
            text = text + "”"
        d.text(((W - counter.textlength(text, font=fb)) / 2 * SS, y * SS), text, font=fbs, fill=ink)
        y += BODY_LEAD

    # attribution + verified badge
    y += WHO_GAP
    who = f"-{q['who']}"
    ww = counter.textlength(who, font=fb)
    x = (W - (ww + 6 + BADGE_R * 2)) / 2
    d.text((x * SS, y * SS), who, font=fbs, fill=ink)
    cx, cy = (x + ww + 6 + BADGE_R) * SS, (y + BODY_SIZE * 0.62) * SS
    r = BADGE_R * SS
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=ink)
    chk = [(cx - 0.50 * r, cy - 0.02 * r), (cx - 0.16 * r, cy + 0.36 * r), (cx + 0.51 * r, cy - 0.40 * r)]
    d.line(chk, fill=(255, 255, 255) if not dark else INK, width=max(2, int(0.22 * r)), joint="curve")

    layer = layer.resize((W, H), Image.LANCZOS)
    img = Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")

    os.makedirs(FINAL, exist_ok=True)
    out = os.path.join(FINAL, f"VEL-STRAW-MOF-REVIEW-{colorway}.jpg")
    img.save(out, "JPEG", quality=94, subsampling=0)
    print(f"{colorway}: {out}")
    return True


if __name__ == "__main__":
    names = sys.argv[1:] or list(QUOTES)
    n = sum(build(c) for c in names)
    print(f"composited {n}/{len(names)}")
