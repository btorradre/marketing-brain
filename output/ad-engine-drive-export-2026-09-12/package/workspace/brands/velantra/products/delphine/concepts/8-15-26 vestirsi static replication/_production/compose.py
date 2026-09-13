#!/usr/bin/env python3
"""THE DELPHINE — composite the type onto each clean plate, 1:1 with its Vestirsi reference.

All five layouts are measured off the actual reference files in `refs/` (see
GEOMETRY below for the numbers and how they were taken). Type is composited HERE
and never model-generated, so tracking, weight and alignment are pixel-correct and
the copy stays swappable without touching a plate.

    D1 new-arrival      <- V1  centered caps + subhead, top third, wordmark bottom
    D2 everyday-size    <- V2  left-aligned block in the left negative space, dark
    D3 effortless       <- V3  wordmark left / tagline + kicker right, 4:5, white
    D4 on-the-fence     <- V4  centered tracked caps + body + attribution, dark
    D5 everyday-staple  <- V5  centered tracked caps + body + attribution, white

COPY MODE
---------
Three of the five references are review statics carrying a named "Verified Buyer".
The Delphine has no review corpus yet, so running invented names under a verified
badge would be a fabricated endorsement. Two modes ship:

    MODE = "brand"   (default) — the same layouts, copy in Velantra's own voice,
                                 no badge, no attributed name. Launch-safe today.
    MODE = "review"  — the reference's exact device, badge and all. Only switch
                       this on once REVIEWS below holds real buyer text.

Swap MODE, re-run, done in seconds. Plates are never touched.

Usage:  python3 compose.py [slug ...]        (default: all)
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageStat

MODE = "brand"          # "brand" | "review"

# White type stays legible up to about this luminance; the V5 reference measures
# ~192-196 behind its glyphs. Used as the solve target for the light-ink scrim.
TARGET_HI = 202.0

ROOT = os.path.dirname(os.path.abspath(__file__))
CONCEPT = os.path.dirname(ROOT)
PLATES = os.path.join(CONCEPT, "plates")
FINAL = os.path.join(CONCEPT, "final")
LOGO = os.path.join(ROOT, "velantra_logo.png")

SS = 3                                  # text supersampling factor
INK_DARK = (17, 17, 17, 255)
INK_LIGHT = (255, 255, 255, 255)

HN = "/System/Library/Fonts/HelveticaNeue.ttc"
HN_LIGHT, HN_ROMAN = 7, 0
HELV = "/System/Library/Fonts/Helvetica.ttc"
DIDOT = "/System/Library/Fonts/Supplemental/Didot.ttc"

# --- COPY --------------------------------------------------------------------
#
# Guardrails held across all five (research/icp-branding + the Velantra copy laws):
#   · no competitor comparison, named or generic
#   · no origin claim of any kind — the reference's "Handwoven in Italy" has no
#     Velantra equivalent and is replaced with construction language
#   · no "Birkin" / "Hermes" anywhere, including internal positioning lines
#   · no designer-inflation grievance register, no "scam", no priced-out language
#   · lineage claim only: "the Eleanor, built at everyday size", never "the
#     Eleanor in a smaller size" and never a size variant of that product
#   · the factory-error origin of this stock is never referenced, ever
#
# D1 replaces the reference's "BACK IN STOCK". The Delphine has never been in
# stock, so that line would be false. The truthful equivalent of its scarcity
# engine is the launch mechanic from PRODUCT-TRUTH.md: one production run.

COPY = {
    "D1-new-arrival": {
        "headline": "JUST ARRIVED",
        "sub": "The Eleanor, Built At Everyday Size",
    },
    "D2-everyday-size": {
        "brand": [
            "Everything that makes the Eleanor work,",
            "built at the size you actually carry.",
            "The Delphine. 25cm.",
        ],
        "review": [
            '"I have the Eleanor and I wanted it smaller.',
            'This is exactly that. Same leather, same weight',
            'to it." -Caroline W., Verified Buyer',
        ],
    },
    "D3-effortless": {
        "headline": "The Everyday Size, Finally.",
        "kicker": "MEET THE DELPHINE",
    },
    "D4-on-the-fence": {
        "brand": {
            "headline": "SMALL BAG. FULL BUILD.",
            "body": [
                "Phone, wallet, keys, sunglasses, and it closes without a",
                "fight. The same grained leather, the same brass turn lock",
                "and the same belted straps that are on the Eleanor.",
            ],
            "who": "The Delphine  ·  25 x 22 x 14 cm",
        },
        "review": {
            "headline": "IT IS SMALL AND IT STILL HOLDS EVERYTHING.",
            "body": [
                "Phone, wallet, keys, sunglasses, and it closes without a",
                "fight. The hardware is the part that surprised me. It is",
                "the same weight as the big one.",
            ],
            "who": "Erin D., Verified Buyer",
        },
    },
    "D5-everyday-staple": {
        "brand": {
            "headline": "THE EVERYDAY STAPLE",
            "body": [
                "One production run. Three colorways. The bag you reach for",
                "without thinking about it.",
            ],
            "who": "The Delphine in Light Chocolate",
        },
        "review": {
            "headline": "THE EVERYDAY STAPLE",
            "body": [
                '"I bought it for weekends. Now it is the one I reach for',
                'every single morning."',
            ],
            "who": "Jennifer C., Verified Buyer",
        },
    },
}

# --- GEOMETRY ----------------------------------------------------------------
#
# Measured off the reference files by scanning for rows that deviate from their
# own per-row background, then reading the ink extents of each run. Percentages
# are of frame height/width so they carry across the 9:16 and 4:5 canvases.
#
#   V1  headline cap-top 26.04%, ink width 444px centered · sub cap-top 29.74%,
#       ink width 478px · brand mark centered, cap-top 89.06%, 36px tall
#   V2  block left edge x=85 (7.87%), first cap-top 27.40%, 3 lines, ~41px lead
#   V3  right-aligned tagline ink ends x=1039, cap-top 42.96% (4:5 canvas)
#   V4  quote block spans x=59..1011, headline cap-top 59.90%
#   V5  headline cap-top 74.27%, ink width 543 · body 77.55% · who 79.48%

GEOM = {
    "D1-new-arrival": dict(
        w=1080, h=1920, ink="light",
        head_cap_pct=0.2604, head_w=444, head_track=0.34, head_font=(HN, HN_LIGHT),
        sub_cap_pct=0.2974, sub_w=478, sub_font=(HN, HN_ROMAN),
        mark_cy_pct=0.9010, mark_h=36,
    ),
    "D2-everyday-size": dict(
        w=1080, h=1920, ink="dark",
        left=85, cap_pct=0.2740, size=34, lead=41, font=(HELV, 0),
    ),
    "D3-effortless": dict(
        w=1080, h=1350, ink="light",
        head_right=1039, head_cap_pct=0.4296, head_size=34, head_font=(HN, HN_ROMAN),
        kick_gap=26, kick_size=20, kick_track=0.10, kick_font=(HN, HN_LIGHT),
        mark_left=84, mark_cy_pct=0.4940, mark_h=26,
    ),
    "D4-on-the-fence": dict(
        w=1080, h=1920, ink="dark",
        head_cap_pct=0.5990, head_max_w=952, head_track=0.20, head_font=(DIDOT, 0),
        head_gap=26, body_size=30, body_lead=38, who_gap=8, badge_r=9,
        body_font=(HELV, 0),
    ),
    "D5-everyday-staple": dict(
        w=1080, h=1920, ink="light",
        head_cap_pct=0.7427, head_max_w=560, head_track=0.34, head_font=(HN, HN_LIGHT),
        head_gap=30, body_size=28, body_lead=37, who_gap=6, badge_r=9,
        body_font=(HN, HN_ROMAN),
    ),
}


def font(spec, size):
    path, idx = spec
    return ImageFont.truetype(path, size, index=idx)


def fit_cap(spec, target_cap, probe="H"):
    """Font whose cap height measures target_cap px."""
    size = max(8, target_cap * 2)
    for _ in range(80):
        f = font(spec, size)
        box = f.getbbox(probe)
        cap = box[3] - box[1]
        if cap == target_cap:
            return f, size
        size += 1 if cap < target_cap else -1
        size = max(6, size)
    return font(spec, size), size


def tracked_w(f, text, track_px):
    if not text:
        return 0
    return sum(f.getlength(c) for c in text) + track_px * (len(text) - 1)


def draw_tracked(d, x, y, text, f, track_px, fill):
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill)
        x += f.getlength(ch) + track_px


def fit_tracked(spec, text, target_w, track_frac, cap_hint=34):
    """Size a tracked line so its inked width lands on target_w."""
    size = cap_hint
    for _ in range(120):
        f = font(spec, size)
        w = tracked_w(f, text, size * track_frac)
        if abs(w - target_w) <= 3:
            break
        size += 1 if w < target_w else -1
        size = max(8, size)
    f = font(spec, size)
    return f, size, tracked_w(f, text, size * track_frac)


def band_mean(img, y0, y1):
    y0, y1 = max(0, y0), min(img.height, y1)
    return ImageStat.Stat(img.convert("L").crop((0, y0, img.width, y1))).mean[0]


def band_local_min(img, y0, y1, win=110, step=30):
    """Darkest window inside the text band.

    A full-width mean hides local darkness: a plate can average 206 across the
    band while one dark patch at one end drops contrast under a few glyphs below
    legible, and no scrim gets applied because the mean looks fine.
    """
    y0, y1 = max(0, y0), min(img.height, y1)
    band = img.convert("L").crop((0, y0, img.width, y1))
    worst = 255.0
    for x in range(0, max(1, band.width - win + 1), step):
        worst = min(worst, ImageStat.Stat(band.crop((x, 0, x + win, band.height))).mean[0])
    return worst


def band_local_max(img, y0, y1, win=110, step=20, row=36):
    """Brightest patch inside the text band — the mirror of band_local_min.

    White type has the opposite failure from dark type: a band can average a
    comfortable 184 while one blown-out patch (sand, sky, a highlight on fabric)
    sits at 220+ and swallows the glyphs over it.

    This scans in 2D — thin `row`-tall strips crossed with `win`-wide windows —
    rather than averaging the full band height. D5 lost the last letter of its
    headline to a 222 patch that a full-height band average reported as 204,
    because the darker body rows underneath pulled the number down.
    """
    y0, y1 = max(0, y0), min(img.height, y1)
    a = np.asarray(img.convert("L").crop((0, y0, img.width, y1)), dtype=float)
    if a.size == 0:
        return 0.0
    best = 0.0
    for ry in range(0, max(1, a.shape[0] - row + 1), row // 2):
        strip = a[ry:ry + row]
        for x in range(0, max(1, a.shape[1] - win + 1), step):
            best = max(best, strip[:, x:x + win].mean())
    return best


def scrim(img, top, strength, invert=False):
    """Soft wash fading in downward so type always reads. White for dark ink."""
    grad = Image.new("L", (1, img.height), 0)
    px = grad.load()
    for y in range(img.height):
        if y <= top:
            px[0, y] = 0
        else:
            t = (y - top) / max(1, img.height - top)
            px[0, y] = int(255 * strength * min(1.0, t * 1.6))
    mask = grad.resize((img.width, img.height))
    wash = (0, 0, 0) if invert else (255, 255, 255)
    return Image.composite(Image.new("RGB", img.size, wash), img, mask)


def edge_falloff(img, bands, target=195.0, floor=0.72):
    """Deepen the empty top/bottom of a studio sweep so white type reads.

    D1's reference carries white type over a warm grey sweep that measures
    L~195 behind the glyphs. Our plate renders the same sweep at L~240-249 —
    correct for a Velantra packshot, far too bright to hold white type, which is
    why a straight composite washed out. The reference's own sweep falls off
    toward the top and bottom edges and is brightest across the bag line, so the
    fix is that same lighting rather than a flat scrim over the whole frame.

    `bands` are (y0, y1) spans in pixels that must land on `target`. The needed
    multiplier is measured per band and interpolated back to 1.0 across the
    middle of the frame, so the bags keep their bright ground untouched.
    """
    g = np.asarray(img.convert("L"), dtype=float)
    H = img.height
    pts = [(0.0, 1.0)]
    for y0, y1 in bands:
        med = float(np.median(g[max(0, y0):min(H, y1)]))
        k = min(1.0, max(floor, target / med)) if med > 0 else 1.0
        pts.append(((y0 + y1) / 2 / H, k))
    pts.append((1.0, 1.0))
    pts.sort()

    # anchor 1.0 midway between the outermost band and the frame centre so the
    # ramp is gradual and never crosses the product
    ys = [p[0] for p in pts if p[1] < 1.0]
    if not ys:
        return img
    if min(ys) < 0.5:
        pts.append((min(min(ys) + 0.22, 0.5), 1.0))
    if max(ys) > 0.5:
        pts.append((max(max(ys) - 0.22, 0.5), 1.0))
    pts = sorted(set(pts))

    ramp = np.interp(np.arange(H) / max(1, H - 1),
                     [p[0] for p in pts], [p[1] for p in pts])
    a = np.asarray(img.convert("RGB"), dtype=float) * ramp[:, None, None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")


def load_plate(slug, w, h):
    src = os.path.join(PLATES, f"{slug}.png")
    if not os.path.exists(src):
        return None
    img = Image.open(src).convert("RGB")
    s = max(w / img.width, h / img.height)
    img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    x, y = (img.width - w) // 2, (img.height - h) // 2
    return img.crop((x, y, x + w, y + h))


def wordmark(height, ink):
    """Velantra wordmark, recoloured from the black-on-transparent brand file."""
    lg = Image.open(LOGO).convert("RGBA")
    a = lg.split()[3]
    v = 255 if ink == "light" else 17
    lg = Image.merge("RGBA", (a.point(lambda _: v),) * 3 + (a,))
    w = max(1, round(height * lg.size[0] / lg.size[1]))
    return lg.resize((w, height), Image.LANCZOS)


# --- per-format compositors ---------------------------------------------------

def build_D1(slug, g, img, c):
    W, H = g["w"], g["h"]
    head_top = int(g["head_cap_pct"] * H)
    mark_cy = int(g["mark_cy_pct"] * H)
    img = edge_falloff(img, [(head_top - 20, head_top + 110),
                             (mark_cy - 34, mark_cy + 34)])
    print(f"  falloff -> headline band L={np.median(np.asarray(img.convert('L'))[head_top-20:head_top+110]):.0f}, "
          f"mark band L={np.median(np.asarray(img.convert('L'))[mark_cy-34:mark_cy+34]):.0f}")
    layer = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    ink = INK_LIGHT

    f, size, w = fit_tracked(g["head_font"], c["headline"], g["head_w"], g["head_track"], 34)
    fs = font(g["head_font"], size * SS)
    top = g["head_cap_pct"] * H - f.getbbox("H")[1]
    draw_tracked(d, (W - w) / 2 * SS, top * SS, c["headline"], fs, size * g["head_track"] * SS, ink)

    fb, sb = fit_cap(g["sub_font"], 23)
    while fb.getlength(c["sub"]) > g["sub_w"] + 30 and sb > 10:
        sb -= 1
        fb = font(g["sub_font"], sb)
    fbs = font(g["sub_font"], sb * SS)
    topb = g["sub_cap_pct"] * H - fb.getbbox("H")[1]
    d.text(((W - fb.getlength(c["sub"])) / 2 * SS, topb * SS), c["sub"], font=fbs, fill=ink)

    layer = layer.resize((W, H), Image.LANCZOS)
    img = Image.alpha_composite(img.convert("RGBA"), layer)

    mk = wordmark(g["mark_h"], "light")
    img.alpha_composite(mk, ((W - mk.size[0]) // 2, round(g["mark_cy_pct"] * H - mk.size[1] / 2)))
    return img.convert("RGB")


def build_D2(slug, g, img, lines):
    W, H = g["w"], g["h"]
    y0 = int(g["cap_pct"] * H) - 30
    y1 = y0 + g["lead"] * len(lines) + 60
    mean, lo = band_mean(img, y0, y1), band_local_min(img, y0, y1)
    if mean < 198 or lo < 178:
        img = scrim(img, y0 - 160, 0.40 if lo >= 140 else 0.62)
        mean = band_mean(img, y0, y1)
    ink = INK_LIGHT if mean < 140 else INK_DARK
    print(f"  band mean {mean:.0f}, darkest {lo:.0f}, ink {'light' if mean < 140 else 'dark'}")

    layer = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    f = font(g["font"], g["size"])
    fs = font(g["font"], g["size"] * SS)
    y = g["cap_pct"] * H - f.getbbox("H")[1]
    for ln in lines:
        d.text((g["left"] * SS, y * SS), ln, font=fs, fill=ink)
        y += g["lead"]
    layer = layer.resize((W, H), Image.LANCZOS)
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")


def build_D3(slug, g, img, c):
    W, H = g["w"], g["h"]
    layer = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    ink = INK_LIGHT

    fh = font(g["head_font"], g["head_size"])
    fhs = font(g["head_font"], g["head_size"] * SS)
    hw = fh.getlength(c["headline"])
    top = g["head_cap_pct"] * H - fh.getbbox("H")[1]
    d.text(((g["head_right"] - hw) * SS, top * SS), c["headline"], font=fhs, fill=ink)

    fk = font(g["kick_font"], g["kick_size"])
    fks = font(g["kick_font"], g["kick_size"] * SS)
    tk = g["kick_size"] * g["kick_track"]
    kw = tracked_w(fk, c["kicker"], tk)
    ky = top + g["head_size"] + g["kick_gap"]
    draw_tracked(d, (g["head_right"] - kw) * SS, ky * SS, c["kicker"], fks, tk * SS, ink)

    layer = layer.resize((W, H), Image.LANCZOS)
    img = Image.alpha_composite(img.convert("RGBA"), layer)

    mk = wordmark(g["mark_h"], "light")
    img.alpha_composite(mk, (g["mark_left"], round(g["mark_cy_pct"] * H - mk.size[1] / 2)))
    return img.convert("RGB")


def build_quote(slug, g, img, c):
    """D4 / D5: centered tracked-caps pull quote, body, attribution (+ badge)."""
    W, H = g["w"], g["h"]
    head_y = g["head_cap_pct"] * H
    y0, y1 = int(head_y) - 40, H - 50
    mean, lo = band_mean(img, y0, y1), band_local_min(img, y0, y1)
    want_light = g["ink"] == "light"

    if want_light:
        # White type: judged on the BRIGHTEST window, not the mean. The reference
        # holds white type over a band measuring ~195; anything much above that
        # starts eating glyphs, and a comfortable mean hides a blown-out patch at
        # one end of the line.
        hi = band_local_max(img, y0, y1)
        if hi > TARGET_HI:
            # Solve for the lightest scrim that clears the target rather than
            # stepping through fixed strengths: a fixed 0.32 took this band from
            # 190 to 136, far darker than the reference's ~195 and visibly a
            # different photograph.
            for s in [round(0.04 * i, 2) for i in range(1, 11)]:
                cand = scrim(img, int(head_y) - 220, s, invert=True)
                if band_local_max(cand, y0, y1) <= TARGET_HI:
                    img = cand
                    break
            else:
                img = cand
            mean, lo, hi = (band_mean(img, y0, y1), band_local_min(img, y0, y1),
                            band_local_max(img, y0, y1))
            print(f"  scrim {s} -> brightest {hi:.0f}")
        else:
            print(f"  brightest window {hi:.0f}, no scrim")
        ink = INK_LIGHT
    else:
        if mean >= 198 and lo >= 185:
            strength = 0.0
        elif mean >= 168 and lo >= 150:
            strength = 0.30
        else:
            strength = 0.62
        if strength:
            img = scrim(img, int(head_y) - 200, strength)
            mean, lo = band_mean(img, y0, y1), band_local_min(img, y0, y1)
        ink = INK_LIGHT if mean < 140 else INK_DARK
    print(f"  band mean {mean:.0f}, darkest {lo:.0f}, ink {'light' if ink == INK_LIGHT else 'dark'}")

    layer = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    headline = c["headline"]
    if MODE == "review":
        headline = f'“{headline}”'
    f, size, tw = fit_tracked(g["head_font"], headline, g["head_max_w"], g["head_track"], 46)
    fs = font(g["head_font"], size * SS)
    top = head_y - f.getbbox("H")[1]
    draw_tracked(d, (W - tw) / 2 * SS, top * SS, headline, fs, size * g["head_track"] * SS, ink)

    fb = font(g["body_font"], g["body_size"])
    fbs = font(g["body_font"], g["body_size"] * SS)
    y = head_y + size + g["head_gap"]
    for ln in c["body"]:
        d.text(((W - fb.getlength(ln)) / 2 * SS, y * SS), ln, font=fbs, fill=ink)
        y += g["body_lead"]

    # Attribution. The verified badge is the review device and only ships in
    # review mode; in brand mode the same slot carries a product line, unbadged.
    y += g["who_gap"]
    who = c["who"]
    badge = MODE == "review"
    who = f"-{who}" if badge else who
    ww = fb.getlength(who)
    r = g["badge_r"]
    total = ww + (6 + r * 2 if badge else 0)
    x = (W - total) / 2
    d.text((x * SS, y * SS), who, font=fbs, fill=ink)
    if badge:
        cx, cy = (x + ww + 6 + r) * SS, (y + g["body_size"] * 0.62) * SS
        rr = r * SS
        d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=ink)
        chk = [(cx - 0.50 * rr, cy - 0.02 * rr), (cx - 0.16 * rr, cy + 0.36 * rr),
               (cx + 0.51 * rr, cy - 0.40 * rr)]
        d.line(chk, fill=(17, 17, 17) if ink == INK_LIGHT else (255, 255, 255),
               width=max(2, int(0.22 * rr)), joint="curve")

    layer = layer.resize((W, H), Image.LANCZOS)
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")


BUILDERS = {
    "D1-new-arrival": build_D1,
    "D2-everyday-size": build_D2,
    "D3-effortless": build_D3,
    "D4-on-the-fence": build_quote,
    "D5-everyday-staple": build_quote,
}


def build(slug):
    g = GEOM[slug]
    img = load_plate(slug, g["w"], g["h"])
    if img is None:
        print(f"{slug}: no plate, skip")
        return False
    print(f"{slug}:")
    raw = COPY[slug]
    c = raw[MODE] if MODE in raw else raw
    out = BUILDERS[slug](slug, g, img, c)
    os.makedirs(FINAL, exist_ok=True)
    dest = os.path.join(FINAL, f"VEL-DELPHINE-{slug}.jpg")
    out.save(dest, "JPEG", quality=94, subsampling=0)
    print(f"  -> {dest}")
    return True


if __name__ == "__main__":
    names = sys.argv[1:] or list(COPY)
    n = sum(build(s) for s in names)
    print(f"composited {n}/{len(names)}  (MODE={MODE})")
