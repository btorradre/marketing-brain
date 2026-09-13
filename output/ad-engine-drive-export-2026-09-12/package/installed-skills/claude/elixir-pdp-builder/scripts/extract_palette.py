#!/usr/bin/env python3
"""
extract_palette.py  —  Universal brand-palette extractor for the Elixir PDP builder.

Reads ALL product images in a folder, finds the brand's primary color + accent + a light
neutral, then derives the FIXED set of style roles every template/recolor consumes.
The roles are identical for every brand; only the values change.

Usage:  python extract_palette.py "product images/" [--out palette.json]
Deps:   pillow   (pip install pillow)
"""
import sys, os, json, glob, colorsys, argparse
from collections import Counter
from PIL import Image

IMG_EXTS = ('.png', '.jpg', '.jpeg', '.webp', '.bmp')

def load_pixels(folder, max_side=120):
    px = []
    files = [f for f in glob.glob(os.path.join(folder, '*')) if f.lower().endswith(IMG_EXTS)]
    for f in files:
        try:
            im = Image.open(f).convert('RGB')
        except Exception:
            continue
        im.thumbnail((max_side, max_side))
        px.extend(im.getdata())
    if not px:
        raise SystemExit('No readable images in: ' + folder)
    return px

def hls(rgb):  # returns (h 0-1, l 0-1, s 0-1)
    r, g, b = [c/255 for c in rgb]
    return colorsys.rgb_to_hls(r, g, b)

def to_hex(rgb):
    return '#%02x%02x%02x' % tuple(max(0, min(255, int(round(c)))) for c in rgb)

def adjust(rgb, dl=0.0, ds=0.0):
    """Shift lightness/saturation of an RGB by deltas (clamped)."""
    h, l, s = hls(rgb)
    l = max(0.0, min(1.0, l + dl)); s = max(0.0, min(1.0, s + ds))
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return (r*255, g*255, b*255)

def hue_deg(rgb):
    return hls(rgb)[0]*360

def dominant(pixels, lmin, lmax, smin, exclude_hue=None, hue_gap=28, topk=1):
    """Most frequent color in an HLS band, weighted by saturation; optionally far from a hue."""
    buckets = Counter()
    for p in pixels:
        h, l, s = hls(p)
        if not (lmin <= l <= lmax) or s < smin:
            continue
        if exclude_hue is not None:
            d = abs((h*360) - exclude_hue) % 360
            d = min(d, 360-d)
            if d < hue_gap:
                continue
        key = (round(p[0]/16)*16, round(p[1]/16)*16, round(p[2]/16)*16)
        buckets[key] += s  # weight by saturation
    if not buckets:
        return None
    ranked = [c for c, _ in buckets.most_common(topk)]
    return ranked[0] if topk == 1 else ranked

def extract(folder):
    px = load_pixels(folder)

    # BRAND: dominant saturated mid/dark color (the label/brand color)
    brand = dominant(px, lmin=0.12, lmax=0.62, smin=0.28) \
         or dominant(px, lmin=0.10, lmax=0.70, smin=0.18) \
         or (138, 39, 24)

    # ACCENT (gold-ish secondary): saturated color a different hue from brand,
    # preferring warm/light (gold) tones.
    accent = dominant(px, lmin=0.40, lmax=0.80, smin=0.25, exclude_hue=hue_deg(brand)) \
          or dominant(px, lmin=0.30, lmax=0.85, smin=0.18, exclude_hue=hue_deg(brand))
    if accent is None:
        # derive a warm gold from brand: rotate toward yellow, lighten
        h, l, s = hls(brand)
        gh = (h + 0.10) % 1.0
        r, g, b = colorsys.hls_to_rgb(0.12 if abs(gh-0.12) > 0.25 else gh, 0.55, 0.55)
        accent = (r*255, g*255, b*255)

    # CREAM / light warm neutral background
    cream = dominant(px, lmin=0.82, lmax=0.985, smin=0.04) or (247, 238, 222)
    # ensure cream is warm + very light
    ch, cl, cs = hls(cream)
    cream = tuple(c*255 for c in colorsys.hls_to_rgb(ch, max(0.92, cl), min(0.18, cs) if cs else 0.10))

    # INK: dark text — desaturated dark of the brand hue
    bh = hls(brand)[0]
    ink = tuple(c*255 for c in colorsys.hls_to_rgb(bh, 0.16, 0.30))

    roles = {
        'BRAND':      to_hex(brand),
        'BRAND_DEEP': to_hex(adjust(brand, dl=-0.06)),
        'BRAND_DARK': to_hex(adjust(brand, dl=-0.12)),
        'DARK':       to_hex(adjust(brand, dl=-0.30, ds=-0.05)),   # near-black brand-tinted (page/header bg)
        'MAROON':     to_hex(adjust(brand, dl=-0.24, ds=-0.02)),   # dark panel bg for custom sections
        'GOLD':       to_hex(accent),
        'GOLD_LT':    to_hex(adjust(accent, dl=+0.10)),
        'GOLD_DK':    to_hex(adjust(accent, dl=-0.12)),
        'CREAM':      to_hex(cream),
        'PAPER':      to_hex(adjust(cream, dl=+0.02)),
        'OFF':        to_hex(adjust(cream, dl=+0.035)),
        'INK':        to_hex(ink),
        'MUTED':      to_hex(adjust(ink, dl=+0.28, ds=-0.05)),
        'LIGHT':      to_hex(adjust(cream, dl=-0.02)),             # cream text on dark sections
        'LINE':       to_hex(adjust(cream, dl=-0.07, ds=+0.05)),   # hairline/border on cream
        'GREEN':      '#5b7c3a',                                   # fixed positive ("FREE") accent
        'WHITE':      '#ffffff',
    }
    return roles

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('folder')
    ap.add_argument('--out', default=None)
    a = ap.parse_args()
    pal = extract(a.folder)
    out = json.dumps(pal, indent=2)
    if a.out:
        open(a.out, 'w').write(out)
        print('wrote', a.out)
    print(out)
