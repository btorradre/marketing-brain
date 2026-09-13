#!/usr/bin/env python3
"""DARK CHOCOLATE LAUNCH statics — overlay the typography onto the QA-passed plate.

Fork of back-in-stock-statics-2026-07/compose_ads.py. Same measured layout (taken
1:1 off the Vestirsi reference at 1080x1920), same fonts, same wordmark treatment —
only the copy changes, because the swipe's announcement slot now carries a color
launch instead of a restock.

  headline  Didone serif, white, cap-height 49px, top y=299, centered
  subhead   light sans, white, top y=380, centered
  wordmark  VELANTRA, white, centered at y=1610

Type is composited here, never generated: "Weekender" is a known text-render
failure across every engine we use.

3 headline treatments x 2 ratios = 6 ads off the one plate.
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

# The swipe's headline ("Back In Stock") sits at ~43% of the canvas width. A color
# launch needs more words, and at cap 49 "Now In Dark Chocolate" runs to 73% — it
# reads shouty next to the restraint of the original. Cap the optical width instead
# of the character count so short headlines keep the measured cap height and only
# long ones scale down.
HEAD_MAX_FRAC = 0.62

# The subhead is NOT given a fixed y. Type size is constant across both ratios (same
# 1080 canvas width) while the y-positions scale, so a scaled subhead y collapses the
# gap — at 4:5 the July numbers leave 8px between the headline baseline and the
# subhead cap. Derive it instead: 32px under whatever cap the headline actually got,
# which reproduces the swipe's measured 299/380 exactly at 9:16.
SUB_GAP = 32

SIZES = {
    "9x16": dict(w=1080, h=1920, head=299, mark=1610),
    # 4:5 feed cut: keep the plate's full composition (fit to height) and widen the
    # draped backdrop outward rather than centre-cropping, which would zoom the
    # headline into the handles.
    "4x5": dict(w=1080, h=1350, head=210, mark=1132),
}

PLATE = "eleanor-dark-chocolate"

# The swipe's structure: big serif = the news, small sans = which product it is.
ADS = {
    "now-in": ("Now In Dark Chocolate", "The Eleanor Weekender"),
    "new-color": ("New Color", "The Eleanor Weekender in Dark Chocolate"),
    "just-launched": ("Just Launched", "The Eleanor Weekender in Dark Chocolate"),
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
    head_font, hs = fit_cap(SERIF, 0, HEAD_CAP)
    sub_font, ss = fit_cap(SANS, 7, SUB_CAP)
    mark = white_logo(LOGO, MARK_H)
    print(f"headline Didot {hs}px | subhead HelveticaNeue Light {ss}px | mark {mark.size}")

    src = os.path.join(PLATES, f"{PLATE}.png")
    assert os.path.exists(src), f"no plate at {src}"

    # Per-headline font: shrink only what overruns HEAD_MAX_FRAC of the canvas.
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    heads = {}
    for slug, (head, _) in ADS.items():
        f, cap = head_font, HEAD_CAP
        while tracked(probe, head, f, HEAD_TRACK) > 1080 * HEAD_MAX_FRAC and cap > 24:
            cap -= 1
            f, _px = fit_cap(SERIF, 0, cap)
        heads[slug] = (f, cap)
        print(f"  {slug}: headline cap {cap}px, "
              f"width {tracked(probe, head, f, HEAD_TRACK):.0f}px")

    total = 0
    for ratio, spec in SIZES.items():
        outdir = os.path.join(FINAL, ratio)
        os.makedirs(outdir, exist_ok=True)
        for slug, (head, sub) in ADS.items():
            img = frame(src, spec)
            d = ImageDraw.Draw(img)
            cx = spec["w"] // 2
            head_f, head_cap = heads[slug]
            draw_tracked(d, head, head_f, HEAD_TRACK, cx, spec["head"])
            draw_tracked(d, sub, sub_font, SUB_TRACK, cx,
                         spec["head"] + head_cap + SUB_GAP)
            img.paste(mark, (cx - mark.width // 2, spec["mark"]), mark)
            img.save(os.path.join(outdir, f"VEL-WKND-DARKCHOC-{slug}-{ratio}.jpg"),
                     quality=94, subsampling=0)
            total += 1
        print(f"{ratio}: {len(ADS)} ads -> final/{ratio}/")
    print(f"\n{total} files written to {FINAL}")


if __name__ == "__main__":
    main()
