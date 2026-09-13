#!/usr/bin/env python3
"""VEL-WEEKENDER-MENSBADGE-01 — lay the GRAMS(28) overlay system onto the QA-passed plates.

Layout measured off the swipe (606x604) and rescaled to a 1080x1350 4:5 feed cut:

  wordmark      VELANTRA, white, letterspaced, small, top left      x=64  y=58
  product line  THE WEEKENDER · BLACK                                x=64  y=112
  status line   PRE-ORDER · SHIPS MID SEPTEMBER                      x=64  under it
  badge row     4 white line icons + two-line caps labels            y=1120 / 1206

Type and icons are composited here, never generated. "Weekender" is a known text-render
failure on every engine we use, and the badge row has to be pixel-consistent across the
three ads or it stops reading as one campaign.

EVERY BADGE IS A LIVE CLAIM, verified against velantrafashion.com on 2026-08-11:
  Full-Grain Leather   PDP MATERIAL block: "Full-Grain Leather"; Black is the all-leather
                       colorway, so the "+ Woven Canvas" half is correctly dropped here
  No Logos Anywhere    product truth, confirmed against the physical bag (no stamp inside
                       or out) and a stated purchase requirement in the men's VOC
  Two-Year Warranty    site trust bar: "Two-Year Warranty, free replacement on every bag"
  Free U.S. Shipping   PDP trust line: "Free U.S. shipping" ($159.99 clears the $75 floor)

The swipe's own badges did NOT port: "Premium Italian Leather" is an origin claim (banned)
and "100K+ Happy Customers" is a number we cannot substantiate.

The status line is not decoration. Black is a pre-order with nothing delivered, so the ad
states the ship date the same way the PDP has to.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLATES = os.path.join(ROOT, "plates")
FINAL = os.path.join(ROOT, "final")

SANS = "/System/Library/Fonts/HelveticaNeue.ttc"
MEDIUM, LIGHT, REGULAR = 10, 7, 0

W, H = 1080, 1350
MARGIN = 64

WORDMARK = "VELANTRA"
PRODUCT = "THE WEEKENDER · BLACK"
STATUS = "PRE-ORDER · SHIPS MID SEPTEMBER"

BADGES = [
    ("hide", ("FULL-GRAIN", "LEATHER")),
    ("tag", ("NO LOGOS", "ANYWHERE")),
    ("shield", ("TWO-YEAR", "WARRANTY")),
    ("globe", ("FREE U.S.", "SHIPPING")),
]

MARK_CAP, PROD_CAP, STAT_CAP, LABEL_CAP = 15, 26, 13, 15
MARK_TRACK, PROD_TRACK, STAT_TRACK, LABEL_TRACK = 4.2, 3.4, 2.6, 1.9

ICON_BOX = 76          # icon bounding box, px
ICON_CY = 1154         # icon centre line
LABEL_TOP = 1220       # first label line top
LABEL_GAP = 10         # gap between the two label lines
SS = 4                 # icon supersample

# The badge strip must sit on tone dark enough for white type. Plates are prompted with a
# darker bottom fifth, but overcast daylight varies, so the scrim is ADAPTIVE: it is
# strengthened until the measured mean luminance under the strip clears the gate.
LUMA_GATE = 84         # of 255
SCRIP_TOP = 0.60       # gradient starts at this fraction of height


def fit_cap(index, target_cap, probe="H"):
    """Font whose cap height is exactly target_cap px."""
    lo, hi = 4, target_cap * 4
    best = None
    while lo <= hi:
        mid = (lo + hi) // 2
        f = ImageFont.truetype(SANS, mid, index=index)
        box = f.getbbox(probe)
        cap = box[3] - box[1]
        if cap == target_cap:
            return f
        if cap < target_cap:
            best = f
            lo = mid + 1
        else:
            hi = mid - 1
    return best or ImageFont.truetype(SANS, target_cap, index=index)


def tracked_width(draw, text, font, track):
    return sum(draw.textlength(c, font=font) + track for c in text) - track


def draw_tracked(draw, xy, text, font, track, fill=(255, 255, 255, 255), anchor="ls"):
    """Letterspaced text. anchor 'ls' = left baseline, 'ms' = centred on baseline."""
    x, y = xy
    if anchor == "ms":
        x -= tracked_width(draw, text, font, track) / 2
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill, anchor="ls")
        x += draw.textlength(ch, font=font) + track


# ---------------------------------------------------------------- line icons
# Drawn at SS scale and downsampled: Pillow has no antialiased stroke, so this is the only
# way to get the swipe's fine hairline weight without it going ragged.

def _bez(p0, p1, p2, n=40):
    out = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        out.append((u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0],
                    u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1]))
    return out


def _rrect_path(x0, y0, x1, y1, r, per_corner=14):
    """Rounded-rect as a closed polyline, so it can be dashed."""
    pts = []
    corners = [(x1 - r, y0 + r, -math.pi / 2, 0), (x1 - r, y1 - r, 0, math.pi / 2),
               (x0 + r, y1 - r, math.pi / 2, math.pi), (x0 + r, y0 + r, math.pi, 1.5 * math.pi)]
    for cx, cy, a0, a1 in corners:
        for i in range(per_corner + 1):
            a = a0 + (a1 - a0) * i / per_corner
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    pts.append(pts[0])
    return pts


def _hide(d, s, w):
    """Leather swatch: a cut panel with a saddle-stitch line running inside its edge.

    The swipe's own icon is a pelt outline; a pelt at 76px reads as an ink blot. A stitched
    swatch says leather AND says made object, which is the claim the label carries.
    """
    pad = s * 0.16
    d.line(_rrect_path(pad, pad * 1.25, s - pad, s - pad * 1.25, s * 0.10),
           fill=255, width=w, joint="curve")
    inner = _rrect_path(pad + s * 0.085, pad * 1.25 + s * 0.075,
                        s - pad - s * 0.085, s - pad * 1.25 - s * 0.075, s * 0.07, per_corner=10)
    # Resample at uniform arc length first: the raw path is dense at the corners and has
    # two-point straight sides, so dashing it by segment index stitches only the corners.
    step = s * 0.011
    walk, carry = [], 0.0
    for (x0, y0), (x1, y1) in zip(inner, inner[1:]):
        seg = math.hypot(x1 - x0, y1 - y0)
        t = carry
        while t < seg:
            walk.append((x0 + (x1 - x0) * t / seg, y0 + (y1 - y0) * t / seg))
            t += step
        carry = t - seg
    for i in range(0, len(walk) - 1, 2):            # dash-gap-dash = saddle stitching
        d.line([walk[i], walk[i + 1]], fill=255, width=max(1, int(w * 0.9)))


def _tag(d, s, w):
    """Blank luggage tag: no mark on it, which is the claim."""
    pad = s * 0.20
    x0, y0, x1, y1 = pad, pad * 1.15, s - pad, s - pad * 1.15
    cut = s * 0.20
    pts = [(x0 + cut, y0), (x1, y0), (x1, y1), (x0 + cut, y1), (x0, (y0 + y1) / 2)]
    d.line(pts + [pts[0]], fill=255, width=w, joint="curve")
    r = s * 0.035
    hx, hy = x0 + cut * 0.85, (y0 + y1) / 2
    d.ellipse([hx - r, hy - r, hx + r, hy + r], outline=255, width=w)


def _shield(d, s, w):
    """Shield + check. Two-year free replacement."""
    cx = s / 2
    top, bot = s * 0.16, s * 0.88
    half = s * 0.29
    shoulder = top + (bot - top) * 0.45
    right = _bez((cx + half, shoulder), (cx + half, bot - (bot - top) * 0.06), (cx, bot))
    left = _bez((cx, bot), (cx - half, bot - (bot - top) * 0.06), (cx - half, shoulder))
    pts = [(cx - half, top), (cx + half, top), (cx + half, shoulder)] + right + left
    d.line(pts + [(cx - half, top)], fill=255, width=w, joint="curve")
    d.line([(cx - s * 0.115, s * 0.47), (cx - s * 0.025, s * 0.565), (cx + s * 0.145, s * 0.355)],
           fill=255, width=int(w * 1.2), joint="curve")


def _globe(d, s, w):
    """Globe with meridian + latitudes, and two speed streaks. Free U.S. shipping."""
    cx, cy, r = s * 0.58, s / 2, s * 0.30
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=255, width=w)
    d.ellipse([cx - r * 0.46, cy - r, cx + r * 0.46, cy + r], outline=255, width=w)
    d.line([(cx - r, cy), (cx + r, cy)], fill=255, width=w)
    for sign in (-1, 1):
        pts = []
        for i in range(41):
            t = -1 + 2 * i / 40
            x = cx + r * 0.985 * t
            y = cy + sign * r * 0.50 * math.cos(t * math.pi / 2)
            pts.append((x, y))
        d.line(pts, fill=255, width=w, joint="curve")
    for yf, lf in ((0.33, 0.13), (0.50, 0.19), (0.67, 0.13)):
        y = s * yf
        d.line([(s * 0.02, y), (s * (0.02 + lf), y)], fill=255, width=w)


ICONS = {"hide": _hide, "tag": _tag, "shield": _shield, "globe": _globe}


def icon(kind, box=ICON_BOX, weight=2.0):
    s = box * SS
    layer = Image.new("L", (s, s), 0)
    ICONS[kind](ImageDraw.Draw(layer), s, max(1, int(weight * SS)))
    layer = layer.resize((box, box), Image.LANCZOS)
    out = Image.new("RGBA", (box, box), (255, 255, 255, 0))
    out.putalpha(layer)
    return out


# ---------------------------------------------------------------- scrim
def band_luma(img, y0, y1):
    band = img.convert("L").crop((0, y0, img.width, y1))
    px = list(band.getdata())
    return sum(px) / len(px)


def apply_scrim(img, strength):
    grad = Image.new("L", (1, H), 0)
    for y in range(H):
        t = (y / H - SCRIP_TOP) / (1 - SCRIP_TOP)
        grad.putpixel((0, y), 0 if t <= 0 else int(255 * strength * (t ** 1.6)))
    grad = grad.resize((W, H))
    black = Image.new("RGB", (W, H), (0, 0, 0))
    return Image.composite(black, img, grad)


def fit_45(plate_path):
    """3:4 plate -> 4:5 canvas. Trim height, keep the full width and the whole bag."""
    im = Image.open(plate_path).convert("RGB")
    im = im.resize((W, int(W * im.height / im.width)), Image.LANCZOS)
    if im.height > H:
        # take from the TOP band, which the prompt reserved as empty background
        top = int((im.height - H) * 0.62)
        im = im.crop((0, top, W, top + H))
    else:
        im = im.resize((W, H), Image.LANCZOS)
    return im


def compose(plate_path, out_path):
    img = fit_45(plate_path)

    strength = 0.0
    for s in (0.0, 0.25, 0.4, 0.55, 0.7, 0.85):
        test = apply_scrim(img, s) if s else img
        if band_luma(test, ICON_CY - 60, LABEL_TOP + 60) <= LUMA_GATE:
            strength = s
            break
        strength = s
    img = apply_scrim(img, strength) if strength else img
    luma = band_luma(img, ICON_CY - 60, LABEL_TOP + 60)

    img = img.convert("RGBA")
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    f_mark = fit_cap(MEDIUM, MARK_CAP)
    f_prod = fit_cap(MEDIUM, PROD_CAP)
    f_stat = fit_cap(LIGHT, STAT_CAP)
    f_label = fit_cap(MEDIUM, LABEL_CAP)

    draw_tracked(d, (MARGIN, 74), WORDMARK, f_mark, MARK_TRACK)
    draw_tracked(d, (MARGIN, 146), PRODUCT, f_prod, PROD_TRACK)
    draw_tracked(d, (MARGIN, 186), STATUS, f_stat, STAT_TRACK, fill=(255, 255, 255, 205))

    span0, span1 = 0.055, 0.945
    step = (span1 - span0) / 4
    for i, (kind, lines) in enumerate(BADGES):
        cx = W * (span0 + step * (i + 0.5))
        ic = icon(kind)
        layer.alpha_composite(ic, (int(cx - ICON_BOX / 2), int(ICON_CY - ICON_BOX / 2)))
        y = LABEL_TOP + LABEL_CAP
        for line in lines:
            draw_tracked(d, (cx, y), line, f_label, LABEL_TRACK, anchor="ms")
            y += LABEL_CAP + LABEL_GAP

    out = Image.alpha_composite(img, layer).convert("RGB")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    out.save(out_path, quality=95, subsampling=0)
    return strength, luma


if __name__ == "__main__":
    import sys
    jobs = sys.argv[1:]
    if not jobs:
        jobs = sorted(f[:-4] for f in os.listdir(PLATES) if f.endswith(".png"))
    for name in jobs:
        src = os.path.join(PLATES, name + ".png")
        dst = os.path.join(FINAL, "4x5", "VEL-WKND-BLK-MENS-%s-4x5.jpg" % name)
        s, l = compose(src, dst)
        print("%-16s scrim=%.2f  badge-band luma=%.0f/255  ->  %s"
              % (name, s, l, os.path.basename(dst)))
