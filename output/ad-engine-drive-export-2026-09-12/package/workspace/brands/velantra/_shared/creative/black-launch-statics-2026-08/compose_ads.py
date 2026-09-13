#!/usr/bin/env python3
"""BLACK PRE-ORDER LAUNCH statics — overlay the typography onto the QA-passed plate.

Fork of dark-chocolate-launch-statics-2026-08/compose_ads.py. Same measured layout
(taken 1:1 off the Vestirsi "Back In Stock" reference at 1080x1920), same fonts, same
wordmark treatment.

  headline  Didone serif, white, cap-height 49px, top y=299, centered
  subhead   light sans, white, top y=380, centered
  wordmark  VELANTRA, white, centered at y=1610

Type is composited here, never generated: "Weekender" is a known text-render failure
across every engine we use.

3 headline treatments x 2 ratios = 6 ads off the one plate.

What changed vs the DC pack, and why:

1. **The subhead now carries the ship date, so it needs its own width guard.** Black is
   a pre-order with nothing delivered, and a pre-order asset has to state when it ships.
   That pushes the subhead from "The Eleanor Weekender in Dark Chocolate" (39 chars) to
   60, which overruns the swipe's restrained line. SUB_MAX_FRAC shrinks only the lines
   that overrun, the same way HEAD_MAX_FRAC already did for headlines.
2. **"Now In Black" is gone.** The DC pack's lead treatment was "Now In Dark Chocolate",
   which was true: it was in stock that morning. "Now In Black" would read as available
   and it is not. Replaced with "Introducing Black", which announces without promising
   stock.
3. **"Just Launched" swapped for "All Leather."** Black is not a recolor of the other
   three, it replaces the canvas body with leather, and that is the only headline in the
   set that says something the picture cannot say on its own.
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

# The swipe's headline ("Back In Stock") sits at ~43% of the canvas width. Cap the
# optical width so short headlines keep the measured cap height and only long ones
# scale down.
HEAD_MAX_FRAC = 0.62

# New here. The swipe's subhead runs to ~55% of canvas width. A pre-order subhead has to
# name the product AND the ship date, so it needs the same treatment the headline got.
SUB_MAX_FRAC = 0.74

# The subhead is NOT given a fixed y. Type size is constant across both ratios (same
# 1080 canvas width) while the y-positions scale, so a scaled subhead y collapses the
# gap. Derive it: 32px under whatever cap the headline actually got, which reproduces
# the swipe's measured 299/380 exactly at 9:16.
SUB_GAP = 32

SIZES = {
    "9x16": dict(w=1080, h=1920, head=299, mark=1610),
    # 4:5 feed cut: keep the plate's full composition (fit to height) and widen the
    # draped backdrop outward rather than centre-cropping, which would zoom the
    # headline into the handles.
    "4x5": dict(w=1080, h=1350, head=210, mark=1132),
}

PLATE = "eleanor-black"

SUB_PREORDER = "The Eleanor Weekender in Black. Pre-Order, Ships Mid September"

# The swipe's structure: big serif = the news, small sans = which product it is.
ADS = {
    "introducing": ("Introducing Black",
                    "The Eleanor Weekender. Pre-Order, Ships Mid September"),
    "new-color": ("New Color", SUB_PREORDER),
    "all-leather": ("All Leather", SUB_PREORDER),
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
    w = sum(draw.textlength(c, font=font) for c in text)
    return w + track * (len(text) - 1)


def fit_width(probe, text, path, index, cap, track, max_frac, floor=10):
    """Shrink the cap height until the tracked line fits max_frac of the canvas."""
    f, _px = fit_cap(path, index, cap)
    while tracked(probe, text, f, track) > 1080 * max_frac and cap > floor:
        cap -= 1
        f, _px = fit_cap(path, index, cap)
    return f, cap


def draw_tracked(draw, text, font, track, center_x, top_y, fill=(255, 255, 255)):
    """Draw letterspaced text centered on center_x with its cap top at top_y."""
    total = tracked(draw, text, font, track)
    x = center_x - total / 2
    off = font.getbbox(text)[1]
    for c in text:
        draw.text((x, top_y - off), c, font=font, fill=fill)
        x += draw.textlength(c, font=font) + track


def white_logo(path, height):
    """Load the black VELANTRA wordmark and return it as a white RGBA overlay."""
    im = Image.open(path).convert("RGBA")
    alpha = im.split()[3]
    if alpha.getextrema()[0] == 255:
        alpha = im.convert("L").point(lambda v: 255 - v)
    mask = alpha.point(lambda v: 255 if v > 25 else 0)
    alpha = alpha.crop(mask.getbbox())
    out = Image.new("RGBA", alpha.size, (255, 255, 255, 0))
    out.putalpha(alpha)
    w = max(1, round(alpha.width * height / alpha.height))
    return out.resize((w, height), Image.LANCZOS)


def frame(src, spec):
    """Fit the plate to the canvas, widening the draped backdrop when needed."""
    img = Image.open(src).convert("RGB")
    w, h = spec["w"], spec["h"]
    scaled_w = round(img.width * h / img.height)
    if scaled_w >= w:
        return img.resize((w, h), Image.LANCZOS)

    body = img.resize((scaled_w, h), Image.LANCZOS)
    x0 = (w - scaled_w) // 2
    ramp, strip = 70, 20
    canvas = Image.new("RGB", (w, h))
    lw, rw = x0 + ramp, w - (x0 + scaled_w) + ramp
    left = body.crop((0, 0, strip, h)).resize((lw, h), Image.LANCZOS)
    right = body.crop((scaled_w - strip, 0, scaled_w, h)).resize((rw, h), Image.LANCZOS)
    canvas.paste(left.filter(ImageFilter.GaussianBlur(12)), (0, 0))
    canvas.paste(right.filter(ImageFilter.GaussianBlur(12)), (w - rw, 0))

    mask = Image.new("L", (scaled_w, h), 255)
    md = ImageDraw.Draw(mask)
    for i in range(ramp):
        v = round(255 * i / ramp)
        md.line([(i, 0), (i, h)], fill=v)
        md.line([(scaled_w - 1 - i, 0), (scaled_w - 1 - i, h)], fill=v)
    canvas.paste(body, (x0, 0), mask)
    return canvas


def main():
    mark = white_logo(LOGO, MARK_H)
    src = os.path.join(PLATES, f"{PLATE}.png")
    assert os.path.exists(src), f"no plate at {src}"

    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    typeset = {}
    for slug, (head, sub) in ADS.items():
        hf, hcap = fit_width(probe, head, SERIF, 0, HEAD_CAP, HEAD_TRACK, HEAD_MAX_FRAC, 24)
        sf, scap = fit_width(probe, sub, SANS, 7, SUB_CAP, SUB_TRACK, SUB_MAX_FRAC, 12)
        typeset[slug] = (hf, hcap, sf, scap)
        print(f"  {slug}: headline cap {hcap}px "
              f"({tracked(probe, head, hf, HEAD_TRACK) / 1080:.0%} wide) | "
              f"subhead cap {scap}px "
              f"({tracked(probe, sub, sf, SUB_TRACK) / 1080:.0%} wide)")

    total = 0
    for ratio, spec in SIZES.items():
        outdir = os.path.join(FINAL, ratio)
        os.makedirs(outdir, exist_ok=True)
        for slug, (head, sub) in ADS.items():
            img = frame(src, spec)
            d = ImageDraw.Draw(img)
            cx = spec["w"] // 2
            hf, hcap, sf, _scap = typeset[slug]
            draw_tracked(d, head, hf, HEAD_TRACK, cx, spec["head"])
            draw_tracked(d, sub, sf, SUB_TRACK, cx, spec["head"] + hcap + SUB_GAP)
            img.paste(mark, (cx - mark.width // 2, spec["mark"]), mark)
            img.save(os.path.join(outdir, f"VEL-WKND-BLACK-{slug}-{ratio}.jpg"),
                     quality=94, subsampling=0)
            total += 1
        print(f"{ratio}: {len(ADS)} ads -> final/{ratio}/")
    print(f"\n{total} files written to {FINAL}")


if __name__ == "__main__":
    main()
