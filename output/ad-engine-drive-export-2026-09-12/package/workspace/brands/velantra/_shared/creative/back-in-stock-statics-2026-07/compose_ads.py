#!/usr/bin/env python3
"""BACK IN STOCK statics — overlay the typography system onto the QA-passed plates.

Typography is composited here (never generated) so it is pixel-identical across all
10 ads and spelling can never drift.

Layout is measured 1:1 off the Vestirsi reference at 1080x1920:
  headline  "Back In Stock"   Didone serif, white, cap-height 49px, top y=299, centered
  subhead   "<The X in Y>"    light sans, white, top y=380, centered
  wordmark  VELANTRA          white, centered (see SIZES for the y offset)
"""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
PLATES = os.path.join(ROOT, "plates")
FINAL = os.path.join(ROOT, "final")
LOGO = os.path.join(ROOT, "velantra_logo.png")

SERIF = "/System/Library/Fonts/Supplemental/Didot.ttc"      # index 0 = Didot Regular
SANS = "/System/Library/Fonts/HelveticaNeue.ttc"            # index 7 = Light

HEAD_CAP, SUB_CAP, MARK_H = 49, 19, 30
HEAD_TRACK, SUB_TRACK = 3.0, 1.6   # letterspacing px

# Two placements. Type SIZE is constant across both (same 1080 canvas width);
# only the vertical rhythm changes. 9:16 y-positions are measured off the swipe.
# The swipe puts its wordmark at y=1521, but GPT Image 2 does not land the bag at
# an identical scale on every plate — the deepest (Lightning Orange) runs to
# y~1575, which would put white type on straw. One uniform y=1610 clears all ten
# and keeps the whole set typographically identical, which matters more for a
# campaign pack than matching the swipe to the pixel.
SIZES = {
    "9x16": dict(w=1080, h=1920, head=299, sub=380, mark=1610),
    # 4:5 feed cut. A centre-crop of a 9:16 plate zooms so far that the headline
    # hits the handles and the wordmark lands on the bag, so instead we keep the
    # plate's full composition (fit to height) and widen the draped backdrop by
    # stretching its edge columns outward. The fabric is soft and out of focus at
    # the edges, so the extension is seamless. Type follows at the same ratio.
    "4x5": dict(w=1080, h=1350, head=210, sub=267, mark=1132),
}

HEADLINE = "Back In Stock"

SUBHEADS = {
    "sofia-caramel":            "The Sofia in Caramel",
    "sofia-sky-blue":           "The Sofia in Sky Blue",
    "sofia-lightning-orange":   "The Sofia in Lightning Orange",
    "sofia-light-chocolate":    "The Sofia in Light Chocolate",
    "sofia-lady-pink":          "The Sofia in Lady Pink",
    "sofia-cream":              "The Sofia in Cream",
    "sofia-sunny-yellow":       "The Sofia in Sunny Yellow",
    "sofia-caban-black":        "The Sofia in Caban Black",
    "eleanor-light-chocolate":  "The Eleanor in Light Chocolate",
    "eleanor-army-green":       "The Eleanor in Army Green",
}


def fit_cap(path, index, target_cap, probe="H"):
    """Return the font size whose cap height matches target_cap px."""
    size = target_cap * 2
    for _ in range(40):
        f = ImageFont.truetype(path, size, index=index)
        box = f.getbbox(probe)
        cap = box[3] - box[1]
        if cap == target_cap:
            return f, size
        size += 1 if cap < target_cap else -1
        size = max(6, size)
    return ImageFont.truetype(path, size, index=index), size


def tracked(draw, text, font, track):
    """Width of text with per-character tracking applied."""
    w = sum(draw.textlength(c, font=font) for c in text)
    return w + track * (len(text) - 1)


def draw_tracked(draw, text, font, track, center_x, top_y, fill=(255, 255, 255)):
    """Draw letterspaced text centered on center_x with its cap top at top_y."""
    total = tracked(draw, text, font, track)
    x = center_x - total / 2
    # align by the cap-top of the string rather than the font ascender
    off = font.getbbox(text)[1]
    for c in text:
        draw.text((x, top_y - off), c, font=font, fill=fill)
        x += draw.textlength(c, font=font) + track


def white_logo(path, height):
    """Load the black VELANTRA wordmark and return it as a white RGBA overlay."""
    im = Image.open(path).convert("RGBA")
    px = im.split()
    alpha = px[3]
    # if the file is opaque, derive the mask from darkness of the glyphs
    if alpha.getextrema()[0] == 255:
        gray = im.convert("L")
        alpha = gray.point(lambda v: 255 - v)
    # trim to the inked bounding box so height is the true glyph height
    mask = alpha.point(lambda v: 255 if v > 25 else 0)
    bbox = mask.getbbox()
    alpha = alpha.crop(bbox)
    out = Image.new("RGBA", alpha.size, (255, 255, 255, 0))
    out.putalpha(alpha)
    w = max(1, round(alpha.width * height / alpha.height))
    return out.resize((w, height), Image.LANCZOS)


def frame(src, spec):
    """Fit the plate to the target canvas, widening the backdrop when needed.

    The plate is 9:16. For a wider canvas we scale it to full height and extend
    the draped fabric sideways by stretching the outermost column strip, rather
    than cropping in (which would wreck the measured type/product spacing).
    """
    img = Image.open(src).convert("RGB")
    w, h = spec["w"], spec["h"]
    scaled_w = round(img.width * h / img.height)
    if scaled_w >= w:                                   # native ratio or wider
        return img.resize((w, h), Image.LANCZOS)

    body = img.resize((scaled_w, h), Image.LANCZOS)
    x0 = (w - scaled_w) // 2

    # Backdrop: fan out the plate's outermost columns, which are pure draped
    # fabric. Stretching the whole plate instead would smear the bag's bright
    # straw into the margins and read as a light leak.
    ramp = 70
    canvas = Image.new("RGB", (w, h))
    strip = 20
    lw, rw = x0 + ramp, w - (x0 + scaled_w) + ramp
    left = body.crop((0, 0, strip, h)).resize((lw, h), Image.LANCZOS)
    right = body.crop((scaled_w - strip, 0, scaled_w, h)).resize((rw, h), Image.LANCZOS)
    canvas.paste(left.filter(ImageFilter.GaussianBlur(12)), (0, 0))
    canvas.paste(right.filter(ImageFilter.GaussianBlur(12)), (w - rw, 0))

    # Feather the plate into that fill so there is no hard vertical seam.
    mask = Image.new("L", (scaled_w, h), 255)
    md = ImageDraw.Draw(mask)
    for i in range(ramp):
        v = round(255 * i / ramp)
        md.line([(i, 0), (i, h)], fill=v)
        md.line([(scaled_w - 1 - i, 0), (scaled_w - 1 - i, h)], fill=v)
    canvas.paste(body, (x0, 0), mask)
    return canvas


def main():
    head_font, hs = fit_cap(SERIF, 0, HEAD_CAP)
    sub_font, ss = fit_cap(SANS, 7, SUB_CAP)
    mark = white_logo(LOGO, MARK_H)
    print(f"headline Didot {hs}px | subhead HelveticaNeue Light {ss}px | mark {mark.size}")

    total = 0
    for ratio, spec in SIZES.items():
        outdir = os.path.join(FINAL, ratio)
        os.makedirs(outdir, exist_ok=True)
        for slug, sub in SUBHEADS.items():
            src = os.path.join(PLATES, f"{slug}.png")
            if not os.path.exists(src):
                print(f"SKIP {slug}: no plate")
                continue
            img = frame(src, spec)
            d = ImageDraw.Draw(img)
            cx = spec["w"] // 2
            draw_tracked(d, HEADLINE, head_font, HEAD_TRACK, cx, spec["head"])
            draw_tracked(d, sub, sub_font, SUB_TRACK, cx, spec["sub"])
            img.paste(mark, (cx - mark.width // 2, spec["mark"]), mark)
            img.save(os.path.join(outdir, f"VEL-BACKINSTOCK-{slug}-{ratio}.jpg"),
                     quality=94, subsampling=0)
            total += 1
        print(f"{ratio}: {len(SUBHEADS)} ads -> final/{ratio}/")
    print(f"\n{total} files written to {FINAL}")


if __name__ == "__main__":
    main()
