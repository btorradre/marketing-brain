#!/usr/bin/env python3
"""VERIFIED BUYER — Weekender: composite the review-quote block onto each clean plate.

1:1 with the Vestirsi review static: full bleed 9:16 photo, wide-tracked all-caps
serif pull quote in the lower third, small sans review body under it, attribution
line with a verified badge. No box, no card — type sits directly on the photo.

Copy lives in QUOTES below. Swap the text there and re-run; plates are untouched.

Usage:  python3 overlay.py [variation ...]      (default: all)
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
# who      = attribution, rendered after an em dash with a verified badge
#
# One documented ICP objection per variation. Register A (peer excitement) in the
# pull quote, Register B (material, specific, skeptical) in the body.
QUOTES = {
    # ---- LIGHT CHOCOLATE (cream ivory canvas) ----
    "light-chocolate-a": {                      # capacity: does a weekend actually fit
        "headline": "FOUR DAYS FIT WITH ROOM LEFT.",
        "body": [
            "I packed out of habit and expected to be sitting on it to",
            "get it closed. Two pairs of shoes, a dress, a sweater, my",
            "toiletry bag. Four days fit with room left.",
        ],
        "who": "Katherine B., Verified Buyer",
    },
    "light-chocolate-b": {                      # durability at the stress points
        "headline": "NOTHING PULLS ON THE CANVAS.",
        "body": [
            "The handles are set into the leather that runs across the",
            "whole top, not stitched onto the fabric. Nothing pulls on",
            "the canvas. That is the part that always goes first.",
        ],
        "who": "Diane R., Verified Buyer",
    },
    "light-chocolate-c": {                      # airline practicality
        "headline": "IT WENT IN THE OVERHEAD BIN PACKED.",
        "body": [
            "No turning it sideways, no conversation with the gate",
            "agent. It went in the overhead bin packed. That was the",
            "entire reason I bought it and it does it every time.",
        ],
        "who": "Lauren P., Verified Buyer",
    },
    "light-chocolate-d": {                      # cream canvas will get dirty
        "headline": "THE CREAM CANVAS HAS HELD UP.",
        "body": [
            "This was the one thing I hesitated on. Airport floors, the",
            "back of a car, hotel luggage racks. The cream canvas has",
            "held up. It still looks the way it did in the photos.",
        ],
        "who": "Susannah T., Verified Buyer",
    },
    # ---- ARMY GREEN (deep army green twill) ----
    "army-green-a": {                           # a travel bag I would use twice a year
        "headline": "I STOPPED SAVING IT FOR TRIPS.",
        "body": [
            "I bought it for flights. I stopped saving it for trips. It does",
            "the school run, the gym and two days a week at the office,",
            "and the green goes with everything I own.",
        ],
        "who": "Nicole S., Verified Buyer",
    },
    "army-green-b": {                           # weight / impracticality
        "headline": "IT IS NOT HEAVY WHEN IT IS FULL.",
        "body": [
            "Packed for two nights it still sits easy on my arm through a",
            "whole terminal. The body of it is canvas, so you carry what",
            "you put in it. It is not heavy when it is full.",
        ],
        "who": "Priya M., Verified Buyer",
    },
    "army-green-c": {                           # cannot see or touch it before buying
        "headline": "THE HARDWARE IS WHAT SURPRISED ME.",
        "body": [
            "I ordered it without seeing it in person. The hardware is",
            "what surprised me. The turn lock is solid and weighted and",
            "the clasp plates have not scratched.",
        ],
        "who": "Margaret H., Verified Buyer",
    },
    "army-green-d": {                           # unfinished interiors / peeling lining
        "headline": "THE INSIDE IS FINISHED PROPERLY.",
        "body": [
            "I check the inside of a bag first. Full cotton lining, a real",
            "leather pocket on the back wall, no raw edges, nothing",
            "shedding onto my clothes. The inside is finished properly.",
        ],
        "who": "Erin D., Verified Buyer",
    },
}

# --- LAYOUT (measured off the reference static) ------------------------------
HEAD_Y = 1228          # cap-top of the pull quote
HEAD_MAX_W = 990       # tracked line must fit inside this
HEAD_TRACK = 0.20      # letterspacing as a fraction of font size
HEAD_GAP = 24          # space between the pull quote and the review body
BODY_SIZE = 30
BODY_LEAD = 38
WHO_GAP = 6            # extra space above the attribution line
BADGE_R = 9


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

    A full-width mean hides local darkness: a plate can average 206 across the band
    while an open doorway or a dark railing at one end drops local text contrast far
    below legible, and no scrim gets applied because the mean looks fine. Scrim
    decisions read this, not just the mean.
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


def build(variation):
    src = os.path.join(PLATES, f"{variation}.png")
    if not os.path.exists(src):
        print(f"{variation}: no plate, skip")
        return False
    q = QUOTES[variation]

    img = Image.open(src).convert("RGB")
    # cover-fit to 1080x1920
    s = max(W / img.width, H / img.height)
    img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    img = img.crop(((img.width - W) // 2, (img.height - H) // 2,
                    (img.width - W) // 2 + W, (img.height - H) // 2 + H))

    # The reference sets black type straight onto a bright studio floor with no
    # scrim. Only lift the band when the plate cannot carry it — judged on the
    # DARKEST window in the band as well as its mean, so a local dark patch behind
    # a few glyphs cannot hide inside a healthy average.
    y0, y1 = HEAD_Y - 40, H - 60
    mean, lo = band_mean(img, y0, y1), band_local_min(img, y0, y1)
    if mean >= 198 and lo >= 185:
        strength = 0.0
    elif mean >= 168 and lo >= 150:
        strength = 0.30
    else:
        strength = 0.62
    if strength:
        img = scrim(img, HEAD_Y - 200, strength)
        mean, lo = band_mean(img, y0, y1), band_local_min(img, y0, y1)
    dark = mean < 140
    ink = INK_LIGHT if dark else INK
    print(f"{variation}: band mean {mean:.0f}, darkest window {lo:.0f}, "
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
    draw_tracked(d, (W - tw) / 2 * SS, HEAD_Y * SS, line, fs, size * HEAD_TRACK * SS, ink)

    # review body
    fb = font(HELV, BODY_SIZE)
    fbs = font(HELV, BODY_SIZE * SS)
    y = HEAD_Y + size + HEAD_GAP
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
    out = os.path.join(FINAL, f"VEL-ELEANOR-MOF-REVIEW-{variation}.jpg")
    img.save(out, "JPEG", quality=94, subsampling=0)
    print(f"{variation}: {out}")
    return True


if __name__ == "__main__":
    names = sys.argv[1:] or list(QUOTES)
    n = sum(build(c) for c in names)
    print(f"composited {n}/{len(names)}")
