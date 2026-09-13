#!/usr/bin/env python3
"""THE CONSIDERED CARRY-ON statics — assemble the two-panel ad and overlay the type.

Layout measured 1:1 off the Vestirsi swipe at 1080x1920
(_production/SWIPE-vestirsi-vera-bowler.png):

  panel split    y=1122                      (top 58.4% / bottom 41.6%)
  bottom fill    #D7CFC8                     (sampled off the swipe)
  headline       all-caps HN Light, white, cap-height 21px, +2.5 track, left x=89, cap-top y=982
  subline        HN Light, white, cap-height 15px, +0.6 track, left x=89, cap-top y=1030
  wordmark       VELANTRA, white, h=20px, right-aligned to x=991, top y=982
  product left   center x=320, width 360, bottom-aligned to y=1663
  product right  center x=760, width 360, bottom-aligned to y=1663

Typography is composited HERE, never model-generated: that keeps it pixel-identical
across the set and is the standing workaround for "Weekender" being unrenderable by
the generation engines.

Run gen_plates.py + make_product_plates.py first, then the frame-QA pass, then this.
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
PLATES = os.path.join(ROOT, "plates")
FINAL = os.path.join(ROOT, "final")
LOGO = os.path.join(ROOT, "_production", "velantra_logo.png")

SANS = "/System/Library/Fonts/HelveticaNeue.ttc"
HEAD_IDX = 7   # Light
SUB_IDX = 7    # Light

# Measured off the swipe, then corrected against a render.
#
# Swipe headline "FROM AIRPORT LOUNGE TO APERITIVO" (32 chars): 554px wide, cap
# height 21, 'F' ink width 14. Helvetica Neue is wider than the swipe's grotesque
# ('F' is 16 at Light, 15 at UltraLight), so no HN weight matches both width and
# stroke. UltraLight matched the width best and was the first choice, but it
# renders with a sub-pixel stem and the dry-run headline was still washing out
# over photography. Stroke weight is what carries legibility, so Light wins: its
# 2px stem matches what the swipe's headline actually looks like.
#
# Tracking is then a free choice rather than a fit, since our strings differ from
# the swipe's. +2.5 reproduces the letterspaced look Light would otherwise lose
# (a pure width-fit to 554 would need only +0.3 and would not read as tracked).
#
# Subline "Travelling with @rosalieburns" (29 chars): 279px at cap 15, which Light
# hits exactly at +0.6. Same weight as the headline; the hierarchy is carried by
# size and tracking, as in the swipe.
HEAD_CAP, SUB_CAP, MARK_H = 21, 15, 20
HEAD_TRACK, SUB_TRACK = 2.5, 0.6
BOTTOM_FILL = (215, 207, 200)                     # #D7CFC8
MARGIN = 89                                       # left type margin, mirrored on the right

# Two placements. Type SIZE is constant across both (identical 1080 canvas width);
# only the vertical rhythm changes — same convention as the Back In Stock pack.
# The 4:5 is a RECOMPOSE, not a crop: a centre-crop would push the headline into the
# suitcase and shove the product panel off-canvas. The panel split holds its 58.4%
# ratio and the bottom-panel composition scales uniformly by 0.7031 about the
# panel's horizontal centre, which is why the two product centres move inward.
#
# `anchor` is where the top-panel crop sits vertically in the source plate (1.0 =
# flush bottom). The 9:16 panel is 1080x1122, near-square like the plate, so it
# loses only 42px of width and the anchor is irrelevant. The 4:5 panel is 1080x789
# — properly landscape — so a square plate loses 291px of height, and a flush-bottom
# crop decapitates the bag's handles. 0.58 keeps the bag whole and still leaves the
# floor the type sits on.
# Product geometry is REBALANCED from the swipe rather than copied. The Vera Bowler
# is taller than wide (long shoulder straps standing up, 308x397); the Eleanor is
# the opposite (short rolled top handles, ~310x280, aspect 1.08-1.13). Dropping the
# Eleanor into the swipe's slots left ~400px of dead greige under the bags. Widening
# to 360 and lifting the top to 1330 restores the swipe's *proportions* — airy, two
# bags, generous margins — for a silhouette it was never measured on.
#   9:16  outer margin 140 | bag 360 | gap 80 | bag 360 | outer 140  = 1080
#
# `prod_baseline` bottom-aligns the two bags on a shared line rather than
# top-aligning them. Light Chocolate and Army Green have slightly different aspects
# (1.13 vs 1.08), so a common top edge would leave their bottoms ragged; the swipe
# stands both bags on the same implied surface.
SIZES = {
    "9x16": dict(w=1080, h=1920, split=1122, head=982, sub=1030, mark=982,
                 prod_baseline=1663, prod_w=360, prod_cx=(320, 760), anchor=1.0),
    "4x5":  dict(w=1080, h=1350, split=789, head=690, sub=724, mark=690,
                 prod_baseline=1169, prod_w=253, prod_cx=(385, 695), anchor=0.58),
}

# slug -> (top plate, headline, subline)
ADS = {
    "01-friday-flight": ("top-01-departure-lc",
                         "FROM THE FRIDAY FLIGHT TO DINNER",
                         "The Eleanor Weekender in Light Chocolate"),
    "02-three-days":    ("top-02-arrival-ag",
                         "THREE DAYS IN ONE BAG",
                         "The Eleanor Weekender in Army Green"),
    "03-rides-carryon": ("top-03-corridor-lc",
                         "IT RIDES ON YOUR CARRY ON",
                         "The Eleanor Weekender · one generous size"),
}

# Lower panel is identical on all three: both colorways, left to right.
PRODUCT_PLATES = ("plate-light-chocolate", "plate-army-green")


def fit_cap(path, index, target_cap, probe="H"):
    """Return the font whose cap height matches target_cap px."""
    size = target_cap * 2
    for _ in range(60):
        f = ImageFont.truetype(path, size, index=index)
        box = f.getbbox(probe)
        cap = box[3] - box[1]
        if cap == target_cap:
            return f, size
        size += 1 if cap < target_cap else -1
        size = max(6, size)
    return ImageFont.truetype(path, size, index=index), size


def tracked(draw, text, font, track):
    w = sum(draw.textlength(c, font=font) for c in text)
    return w + track * (len(text) - 1)


def draw_tracked(draw, text, font, track, left_x, top_y, fill=(255, 255, 255)):
    """Draw letterspaced text left-aligned at left_x with its cap top at top_y."""
    off = font.getbbox(text)[1]
    x = left_x
    for c in text:
        draw.text((x, top_y - off), c, font=font, fill=fill)
        x += draw.textlength(c, font=font) + track


def white_logo(path, height):
    """Load the black VELANTRA wordmark and return it as a white RGBA overlay."""
    im = Image.open(path).convert("RGBA")
    alpha = im.split()[3]
    if alpha.getextrema()[0] == 255:                  # opaque file: mask from glyph darkness
        alpha = im.convert("L").point(lambda v: 255 - v)
    bbox = alpha.point(lambda v: 255 if v > 25 else 0).getbbox()
    alpha = alpha.crop(bbox)
    out = Image.new("RGBA", alpha.size, (255, 255, 255, 0))
    out.putalpha(alpha)
    w = max(1, round(alpha.width * height / alpha.height))
    return out.resize((w, height), Image.LANCZOS)


TYPE_TARGET_LUM = 96        # luminance the type block's bright end must sit at or below
TYPE_PCTL = 0.80            # measure the bright end, not the mean (see scrim())
SCRIM_MIN, SCRIM_MAX = 0.18, 0.74


def scrim(panel, head_y, sub_y, margin, start=0.46):
    """Darken the bottom of the top panel behind the type block, adaptively.

    The swipe puts white light-weight type over uniformly mid-dark concrete and gets
    away with it. Our scenes are brighter (sunlit stone, pale departure hall) and a
    fixed scrim left the headline effectively invisible in the first dry-run. So the
    strength is measured, not guessed: sample the luminance the type actually lands
    on, then solve for the alpha that brings it to TYPE_TARGET_LUM.

    That keeps legibility independent of whatever the generator returns and avoids
    over-darkening a plate that is already dark. Top panel only, never the product
    panel below.

    Measured at the bright END of the band (TYPE_PCTL), not the mean: the headline
    crosses both the dark suitcase and pale sunlit floor, and a mean of 113 hid a
    floor sitting near 190 — white type only fails against the bright part.
    """
    w, h = panel.size
    y0 = int(h * start)
    band = panel.crop((margin, max(0, head_y - 8), w - margin, min(h, sub_y + 26)))

    hist = band.convert("L").histogram()
    cutoff = TYPE_PCTL * sum(hist)
    run = 0
    lum = 255
    for v, n in enumerate(hist):
        run += n
        if run >= cutoff:
            lum = v
            break

    peak = 0.0 if lum <= TYPE_TARGET_LUM else 1 - TYPE_TARGET_LUM / lum
    peak = min(SCRIM_MAX, max(SCRIM_MIN, peak))

    # The ramp must reach `peak` by the top of the headline and hold to the bottom,
    # so solve the eased curve for the alpha at that row rather than at the edge.
    t_head = (head_y - y0) / max(1, h - 1 - y0)
    scale = peak / max(1e-6, t_head * t_head)

    grad = Image.new("L", (1, h), 0)
    px = grad.load()
    for y in range(y0, h):
        t = (y - y0) / max(1, h - 1 - y0)
        px[0, y] = int(255 * min(SCRIM_MAX, scale * t * t))   # eased: no visible onset line
    out = Image.composite(Image.new("RGB", (w, h), (0, 0, 0)), panel, grad.resize((w, h)))
    print(f"    scrim: type-block p80 luminance {lum:.0f} -> peak alpha {peak:.2f}")
    return out


def top_panel(src, w, h, anchor=1.0):
    """Cover-fit the square editorial plate into the top panel box.

    `anchor` places the crop vertically: 1.0 is flush bottom, 0.5 centred. The 9:16
    panel is near-square so nothing meaningful is lost either way; the 4:5 panel is
    landscape and needs a raised anchor to keep the bag's handles in frame.
    """
    img = Image.open(src).convert("RGB")
    scale = max(w / img.width, h / img.height)
    sw, sh = round(img.width * scale), round(img.height * scale)
    img = img.resize((sw, sh), Image.LANCZOS)
    x0 = (sw - w) // 2
    y0 = round((sh - h) * anchor)
    return img.crop((x0, y0, x0 + w, y0 + h))


def cutout(src, target_w, fill=BOTTOM_FILL, tol=30):
    """Trim a product plate to its inked bounding box and scale to target_w.

    The plate is generated on a flat #D7CFC8 field, so the bag is isolated by
    distance from that fill rather than by a matte. Returned RGB, to be pasted
    onto the identical fill — no alpha needed, and no halo.
    """
    img = Image.open(src).convert("RGB")
    px = img.load()
    W, Hh = img.size
    step = 2
    xs, ys = [], []
    for y in range(0, Hh, step):
        for x in range(0, W, step):
            p = px[x, y]
            if abs(p[0] - fill[0]) + abs(p[1] - fill[1]) + abs(p[2] - fill[2]) > tol:
                xs.append(x)
                ys.append(y)
    if not xs:
        raise RuntimeError(f"{os.path.basename(src)}: could not isolate the bag from the backdrop")
    pad = 4
    box = (max(0, min(xs) - pad), max(0, min(ys) - pad),
           min(W, max(xs) + pad), min(Hh, max(ys) + pad))
    crop = img.crop(box)
    h = round(crop.height * target_w / crop.width)
    return crop.resize((target_w, h), Image.LANCZOS)


def main():
    head_font, hs = fit_cap(SANS, HEAD_IDX, HEAD_CAP)
    sub_font, ss = fit_cap(SANS, SUB_IDX, SUB_CAP)
    mark = white_logo(LOGO, MARK_H)
    print(f"headline HN Light {hs}px | subline HN Light {ss}px | mark {mark.size}")

    missing = [p for p in PRODUCT_PLATES if not os.path.exists(os.path.join(PLATES, f"{p}.png"))]
    if missing:
        print(f"ABORT: missing product plates {missing} — run gen_plates.py")
        return

    total = 0
    for ratio, spec in SIZES.items():
        outdir = os.path.join(FINAL, ratio)
        os.makedirs(outdir, exist_ok=True)

        bags = [cutout(os.path.join(PLATES, f"{p}.png"), spec["prod_w"]) for p in PRODUCT_PLATES]

        for slug, (plate, headline, subline) in ADS.items():
            src = os.path.join(PLATES, f"{plate}.png")
            if not os.path.exists(src):
                print(f"SKIP {slug}: no plate {plate}.png")
                continue

            print(f"  {slug} {ratio}")
            canvas = Image.new("RGB", (spec["w"], spec["h"]), BOTTOM_FILL)
            panel = top_panel(src, spec["w"], spec["split"], spec["anchor"])
            canvas.paste(scrim(panel, spec["head"], spec["sub"], MARGIN), (0, 0))

            for bag, cx in zip(bags, spec["prod_cx"]):
                canvas.paste(bag, (cx - bag.width // 2, spec["prod_baseline"] - bag.height))

            d = ImageDraw.Draw(canvas)
            draw_tracked(d, headline, head_font, HEAD_TRACK, MARGIN, spec["head"])
            draw_tracked(d, subline, sub_font, SUB_TRACK, MARGIN, spec["sub"])
            canvas.paste(mark, (spec["w"] - MARGIN - mark.width, spec["mark"]), mark)

            out = os.path.join(outdir, f"VEL-CARRYON-{slug}-{ratio}.jpg")
            canvas.save(out, quality=94, subsampling=0)
            total += 1
        print(f"{ratio}: -> final/{ratio}/")

    print(f"\n{total} files written to {FINAL}")


if __name__ == "__main__":
    main()
