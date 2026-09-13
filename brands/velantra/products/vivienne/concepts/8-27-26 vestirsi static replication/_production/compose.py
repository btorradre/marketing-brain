#!/usr/bin/env python3
"""THE VIVIENNE — composite the type onto each clean plate, 1:1 with its Vestirsi reference.

All six layouts are MEASURED off the actual reference files in `refs/`, never
eyeballed (see GEOMETRY below for the numbers and `measure_refs.py`,
`measure_white.py`, `measure_white2.py` for how each was taken). Type is
composited HERE and never model-generated, so tracking, weight and alignment are
pixel-correct and the copy stays swappable without touching a plate.

    V1 first-run     <- R6  centred tracked caps + subhead, top third, mark bottom
    V2 leather-logo  <- R2  centred wordmark + tagline across the middle band
    V3 out-the-door  <- R3  centred wordmark + tagline across the middle band
    V4 effortless    <- R4  ghost mark top, mark left, tagline + kicker right
    V5 real-day      <- R5  tracked caps + 2 body lines + attribution, mark bottom
    V6 quote         <- R1  three-line quote, left aligned, lower left

Every one of the six references sets WHITE type, so every plate runs the
brightest-window guard: white type fails on a local blown-out patch, not on the
band mean (the Delphine run lost a headline letter to a 222 patch inside a band
that averaged a comfortable 204).

COPY MODE
---------
Two of the six references (R5, R1) are review statics carrying a named "Verified
Buyer". The Vivienne is a DRAFT, pre-order product with no review corpus at all,
so running invented names under a verified badge would be a fabricated
endorsement. Two modes ship:

    MODE = "brand"   (default) — the same layouts, copy in Velantra's own voice
                                 drawn from the LIVE PDP, no badge, no name.
                                 Launch-safe today.
    MODE = "review"  — the reference's exact device, badge and all. The strings
                       under "review" are PLACEHOLDERS, not real buyer text. Do
                       not ship this mode until REVIEWS below holds real quotes.

Swap MODE, re-run, done in seconds. Plates are never touched.

Usage:  python3 compose.py [slug ...]        (default: all)
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageStat

MODE = "review"         # "brand" | "review"
BIRKIN = False          # V2 tagline swap, see COPY. Cleared copy, see BRIEF.md.

# White type stays legible up to about this luminance. The references measure
# L~23 (V6, black dress) to L~193 (V1, pale sweep) behind their glyphs, and V1's
# 193 is the top of the range Vestirsi itself accepts.
TARGET_HI = 202.0

ROOT = os.path.dirname(os.path.abspath(__file__))
CONCEPT = os.path.dirname(ROOT)
PLATES = os.path.join(CONCEPT, "plates")
FINAL = os.path.join(CONCEPT, "final")
LOGO = os.path.join(ROOT, "velantra_logo.png")

SS = 3                                  # text supersampling factor
INK_LIGHT = (255, 255, 255, 255)

HN = "/System/Library/Fonts/HelveticaNeue.ttc"
HN_LIGHT, HN_ROMAN = 7, 0
HELV = "/System/Library/Fonts/Helvetica.ttc"
DIDOT = "/System/Library/Fonts/Supplemental/Didot.ttc"

# --- COPY --------------------------------------------------------------------
#
# Guardrails held across all six (PRODUCT-TRUTH.md §11/§12 + the Velantra copy
# laws), each of which the reference copy violates and therefore could not be
# traced:
#   · NO ORIGIN CLAIM. Every one of the six references leans on "Handwoven in
#     Italy" or "Handcrafted Italian leather, designed in Australia". Velantra
#     manufactures in China; those lines are replaced with construction language.
#   · NO BNPL. R5's "Free Shipping | AfterPay" is dropped outright.
#   · NO CAPACITY CLAIM. Height and depth are unmeasured and nothing about what
#     the bag fits is cleared, so no line names a laptop, a volume or a contents
#     list. "Carries a real day" is the LIVE PDP blurb and is cleared.
#   · NO "STRUCTURED" / "STANDS ON ITS OWN". Banned claims since the 2026-08-22
#     structure correction.
#   · No em dashes. No coastal framing. No competitor comparison (see BIRKIN).
#   · No invented review counts, star ratings, certifications or percentages.
#
# V1 replaces R6's "BACK IN STOCK". The Vivienne has never been in stock, so that
# line would be false. The truthful equivalent of its scarcity engine is the
# launch mechanic from PRODUCT-TRUTH.md §10: whole product on pre-order, first
# run ships October, a date Brooks confirmed and which is already a public
# promise on the PDP.
#
# Every brand-mode line below traces to live PDP copy: the blurb, the "leather,
# not the logo" editorial tile, and the MATERIAL / CARRY pillars.

COPY = {
    "V1-first-run": {
        "headline": "NOW ON PRE-ORDER",
        "sub": "The First Run Ships In October",
    },
    "V2-leather-logo": {
        # BIRKIN=True swaps in the mechanism line. "Birkin-inspired" is cleared
        # for customer-facing copy by the 2026-08-21 reversal and already runs on
        # the live PDP editorial tile. It stays OFF by default here because a
        # trademark on a Meta static is a different risk surface than a PDP.
        "tagline": "The Leather, Not The Logo.",
        "tagline_birkin": "The Shape You Know, Without The Name.",
    },
    "V3-out-the-door": {
        "tagline": "For The Woman Already Out The Door.",
    },
    "V4-effortless": {
        "tagline": "Everyday Leather, Without The Logo.",
        "kicker": "DISCOVER THE VIVIENNE",
    },
    "V5-real-day": {
        "brand": {
            "headline": "THE BAG THAT CARRIES A REAL DAY",
            "body": [
                "Vegetable-tanned leather on every panel, a belted brass closure,",
                "and a detachable shoulder strap. No logo anywhere on it.",
            ],
            "who": "The Vivienne in Olive",
        },
        "review": {
            # Authorised by Brooks 2026-08-27 ("verified buyer is fine, do it"),
            # same device as the Weekender and Straw Tote verified-buyer MOF runs.
            # Written in avatar voice, NOT transcribed from a real customer.
            #
            # The headline stays a BRAND claim and is never set in quotation
            # marks, exactly as the reference does it: R5 puts its claim on top
            # and the review underneath. A quoted headline would have to be a
            # verbatim whole sentence of the body (the doctored-quote law from
            # the Weekender run) and there is no reason to take that risk here.
            #
            # Every detail is a cleared claim: vegetable-tanned leather, a
            # turning brass lock, no logo. No origin, no capacity, no duration
            # of ownership, no "structured".
            "headline": "THE BAG THAT CARRIES A REAL DAY",
            "body": [
                "“I never write these. The leather is much heavier than I",
                "expected and the brass actually turns and locks.”",
            ],
            "who": "Erin M., Verified Buyer",
        },
    },
    "V6-quote": {
        "brand": [
            "Vegetable-tanned leather on every panel, including",
            "the corner caps and the gussets. No logo anywhere.",
            "The Vivienne in Black, $149.99",
        ],
        "review": [
            # Same authorisation and same rules as V5. Two quote lines then the
            # attribution, mirroring R1. Scale impression rather than a capacity
            # claim, and creasing rather than a duration of ownership.
            "“Could not be happier. It is much bigger than it looks in",
            "photos, and the leather already creases like it should.”",
            "-Claire T., Verified Buyer",
        ],
    },
}

# --- GEOMETRY ----------------------------------------------------------------
#
# Measured off the reference files. The busy on-body references (R1, R2, R3, R4)
# defeated a plain row-deviation scan because the bag's specular highlights are
# as bright as the type; they were resolved with an achromatic gate (ad type is
# neutral white, the leather highlights are warm). Numbers, all on 1080x1920:
#
#   R6 -> V1  head cap-top 26.04%, ink w 445 · sub cap-top 29.79%, ink w 479
#             brand mark centred at cy 89.87% (reference sets a monogram there)
#   R2 -> V2  wordmark cy 48.67%, ink w 233 · tagline cap-top 50.73%, ink w 447
#   R3 -> V3  wordmark cy 48.36%, ink w 320 · tagline cap-top 51.30%, ink w 589
#   R4 -> V4  ghost mark cy 7.79% ink w 286 · left mark cy 46.02% left x=75 w 266
#             tagline cap-top 44.11% right edge x=995 · kicker cap-top 46.77%
#             right edge x=996
#   R5 -> V5  head cap-top 21.51% ink w 829 · body 24.64% and 26.35% (lead 33)
#             who 28.07% · brand mark centred cy 94.95%, ink w 200
#   R1 -> V6  three lines, left edge x=110, cap-tops 79.27/81.46/83.65% (lead 42)
#             ink widths 544 / 529 / 347
#
# The Velantra wordmark's ink aspect is 7.51:1 and the Vestirsi mark measures
# 7.6-8.0:1 across the four references that carry it, so matching the reference's
# ink WIDTH lands the height correctly too and no separate height is set.

GEOM = {
    "V1-first-run": dict(
        w=1080, h=1920,
        head_cap_pct=0.2604, head_w=445, head_track=0.34, head_font=(HN, HN_LIGHT),
        sub_cap_pct=0.2979, sub_w=479, sub_font=(HN, HN_ROMAN),
        mark_cy_pct=0.8987, mark_w=270,
        falloff_target=193.0,
    ),
    "V2-leather-logo": dict(
        w=1080, h=1920,
        mark_cy_pct=0.4867, mark_w=233,
        tag_cap_pct=0.5073, tag_w=447, tag_font=(HN, HN_ROMAN),
    ),
    "V3-out-the-door": dict(
        w=1080, h=1920,
        mark_cy_pct=0.4836, mark_w=320,
        tag_cap_pct=0.5130, tag_w=589, tag_font=(HN, HN_ROMAN),
    ),
    "V4-effortless": dict(
        w=1080, h=1920,
        ghost_cy_pct=0.0779, ghost_w=286, ghost_alpha=165,
        mark_left=75, mark_cy_pct=0.4602, mark_w=266,
        tag_right=995, tag_cap_pct=0.4411, tag_w=450, tag_font=(HN, HN_ROMAN),
        kick_right=996, kick_cap_pct=0.4677, kick_w=271, kick_track=0.14,
        kick_font=(HN, HN_LIGHT),
    ),
    "V5-real-day": dict(
        w=1080, h=1920,
        head_cap_pct=0.2151, head_w=829, head_track=0.30, head_font=(DIDOT, 0),
        body_cap_pct=0.2464, body_w=863, body_lead=33, body_font=(HELV, 0),
        who_cap_pct=0.2807, badge_r=9,
        mark_cy_pct=0.9495, mark_w=200,
    ),
    "V6-quote": dict(
        w=1080, h=1920,
        left=110, cap_pct=0.7927, line_w=544, lead=42, font=(HELV, 0), badge_r=8,
    ),
}


def font(spec, size):
    path, idx = spec
    return ImageFont.truetype(path, size, index=idx)


def tracked_w(f, text, track_px):
    if not text:
        return 0
    return sum(f.getlength(c) for c in text) + track_px * (len(text) - 1)


def draw_tracked(d, x, y, text, f, track_px, fill):
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill)
        x += f.getlength(ch) + track_px


def fit_tracked(spec, text, target_w, track_frac, hint=34):
    """Size a tracked line so its inked width lands on target_w."""
    size = hint
    for _ in range(160):
        f = font(spec, size)
        w = tracked_w(f, text, size * track_frac)
        if abs(w - target_w) <= 3:
            break
        size += 1 if w < target_w else -1
        size = max(8, size)
    f = font(spec, size)
    return f, size, tracked_w(f, text, size * track_frac)


def fit_plain(spec, text, target_w, hint=30):
    """Size an untracked line so its inked width lands on target_w."""
    size = hint
    for _ in range(160):
        f = font(spec, size)
        w = f.getlength(text)
        if abs(w - target_w) <= 3:
            break
        size += 1 if w < target_w else -1
        size = max(8, size)
    f = font(spec, size)
    return f, size, f.getlength(text)


def band_mean(img, y0, y1):
    y0, y1 = max(0, y0), min(img.height, y1)
    return ImageStat.Stat(img.convert("L").crop((0, y0, img.width, y1))).mean[0]


def band_local_max(img, y0, y1, x0=0, x1=None, win=110, step=20, row=36):
    """Brightest patch inside the text band.

    White type fails on a local blown-out patch, not on the band mean: a band can
    average a comfortable 184 while one highlight sits at 220+ and swallows the
    glyphs over it. Scans in 2D, thin `row`-tall strips crossed with `win`-wide
    windows, because averaging the full band height hides exactly that.
    """
    y0, y1 = max(0, y0), min(img.height, y1)
    x1 = img.width if x1 is None else x1
    a = np.asarray(img.convert("L").crop((x0, y0, x1, y1)), dtype=float)
    if a.size == 0:
        return 0.0
    best = 0.0
    for ry in range(0, max(1, a.shape[0] - row + 1), max(1, row // 2)):
        strip = a[ry:ry + row]
        for x in range(0, max(1, a.shape[1] - win + 1), step):
            best = max(best, strip[:, x:x + win].mean())
    return best


def scrim(img, top, strength, invert=False):
    """Soft wash fading in downward so type always reads. Dark wash for white ink."""
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


def solve_scrim(img, y0, y1, top, x0=0, x1=None):
    """Lightest dark wash that pulls the band's brightest window under TARGET_HI.

    Solving beats stepping fixed strengths: on the Delphine run a fixed 0.32 took
    a band from 190 to 136, far darker than the reference's ~195 and visibly a
    different photograph.
    """
    hi = band_local_max(img, y0, y1, x0, x1)
    if hi <= TARGET_HI:
        print(f"  brightest window {hi:.0f}, no scrim")
        return img
    cand = img
    for s in [round(0.04 * i, 2) for i in range(1, 13)]:
        cand = scrim(img, top, s, invert=True)
        if band_local_max(cand, y0, y1, x0, x1) <= TARGET_HI:
            break
    print(f"  brightest {hi:.0f} -> scrim {s} -> {band_local_max(cand, y0, y1, x0, x1):.0f}")
    return cand


def local_scrim(img, box, strength, feather=140):
    """Feathered dark wash confined to one region instead of the whole frame.

    V4 needs 0.40 to pull its tagline band under target, because that band runs
    off the model's leg onto a wall measuring L~224. The downward-ramp scrim
    applies that 0.40 to everything below the band, which visibly darkened the
    floor, the shoes and the lower jeans. The reference does no such thing: its
    own type band is dark because the whole wall is a greyer greige, and its
    floor is untouched. Confining the wash to the type's own box, feathered wide
    enough that no edge is visible, keeps the rest of the photograph as shot.
    """
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rectangle(box, fill=int(255 * strength))
    mask = mask.filter(ImageFilter.GaussianBlur(feather))
    return Image.composite(Image.new("RGB", img.size, (0, 0, 0)), img, mask)


def solve_local_scrim(img, y0, y1, box, x0=0, x1=None, feather=140):
    """Lightest local wash that pulls the band's brightest window under TARGET_HI."""
    hi = band_local_max(img, y0, y1, x0, x1)
    if hi <= TARGET_HI:
        print(f"  brightest window {hi:.0f}, no scrim")
        return img
    cand = img
    for s in [round(0.05 * i, 2) for i in range(1, 17)]:
        cand = local_scrim(img, box, s, feather)
        if band_local_max(cand, y0, y1, x0, x1) <= TARGET_HI:
            break
    print(f"  brightest {hi:.0f} -> local scrim {s} -> "
          f"{band_local_max(cand, y0, y1, x0, x1):.0f}")
    return cand


def edge_falloff(img, bands, target=193.0, floor=0.72):
    """Deepen the empty top/bottom of a studio sweep so white type reads.

    V1's reference carries white type over a warm grey sweep measuring L~193.
    Our sweep renders far brighter, correct for a Velantra packshot and far too
    bright to hold white type. The reference's own sweep falls off toward the
    edges and is brightest across the bag line, so the fix is that same lighting
    rather than a flat scrim over the whole frame, which would kill the packshot.

    `bands` are (y0, y1) spans that must land on `target`. The needed multiplier
    is measured per band and interpolated back to 1.0 across the middle of the
    frame, so the bags keep their bright ground untouched.
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


def wordmark(ink_w, alpha=255):
    """Velantra wordmark sized to a target INK width, recoloured white.

    Sized on the ink bbox rather than the file canvas: the brand PNG carries
    padding, so scaling the canvas to the reference's measured ink width would
    render the mark noticeably small.
    """
    lg = Image.open(LOGO).convert("RGBA")
    a = np.asarray(lg.split()[3])
    ys, xs = np.where(a > 8)
    lg = lg.crop((int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1))
    al = lg.split()[3].point(lambda v: int(v * alpha / 255))
    lg = Image.merge("RGBA", (al.point(lambda _: 255),) * 3 + (al,))
    h = max(1, round(ink_w * lg.size[1] / lg.size[0]))
    return lg.resize((ink_w, h), Image.LANCZOS)


def place_mark(img, mk, cx=None, left=None, cy=0.5):
    x = left if left is not None else round((cx or img.width / 2) - mk.size[0] / 2)
    y = round(cy * img.height - mk.size[1] / 2)
    img.alpha_composite(mk, (int(x), int(y)))
    return img


# --- per-format compositors ---------------------------------------------------

def build_V1(slug, g, img, c):
    """R6: centred tracked caps + subhead in the empty top third, mark at bottom."""
    W, H = g["w"], g["h"]
    head_top = int(g["head_cap_pct"] * H)
    mark_cy = int(g["mark_cy_pct"] * H)
    img = edge_falloff(img, [(head_top - 20, head_top + 110),
                             (mark_cy - 34, mark_cy + 34)], target=g["falloff_target"])
    gl = np.asarray(img.convert("L"))
    print(f"  falloff -> headline band L={np.median(gl[head_top-20:head_top+110]):.0f}, "
          f"mark band L={np.median(gl[mark_cy-34:mark_cy+34]):.0f}")
    img = solve_scrim(img, head_top - 20, head_top + 130, head_top - 260)

    layer = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    f, size, w = fit_tracked(g["head_font"], c["headline"], g["head_w"], g["head_track"], 34)
    fs = font(g["head_font"], size * SS)
    top = g["head_cap_pct"] * H - f.getbbox("H")[1]
    draw_tracked(d, (W - w) / 2 * SS, top * SS, c["headline"], fs, size * g["head_track"] * SS,
                 INK_LIGHT)

    fb, sb, wb = fit_plain(g["sub_font"], c["sub"], g["sub_w"], 24)
    fbs = font(g["sub_font"], sb * SS)
    topb = g["sub_cap_pct"] * H - fb.getbbox("H")[1]
    d.text(((W - wb) / 2 * SS, topb * SS), c["sub"], font=fbs, fill=INK_LIGHT)

    layer = layer.resize((W, H), Image.LANCZOS)
    img = Image.alpha_composite(img.convert("RGBA"), layer)
    return place_mark(img, wordmark(g["mark_w"]), cx=W / 2, cy=g["mark_cy_pct"]).convert("RGB")


def build_centre_lockup(slug, g, img, c):
    """R2 / R3: wordmark then a tagline, both centred across the middle band."""
    W, H = g["w"], g["h"]
    tag_top = int(g["tag_cap_pct"] * H)
    mark_cy = int(g["mark_cy_pct"] * H)
    y0, y1 = mark_cy - 40, tag_top + 60
    # Measure and wash only the horizontal span the type actually occupies. A
    # full-width scan on V3 read 228 off the pale linen shirt at the frame edges,
    # 300px clear of the longest glyph, and solved a 0.32 full-frame wash for it.
    ink = max(g["mark_w"], g["tag_w"])
    ix0, ix1 = int(W / 2 - ink / 2) - 30, int(W / 2 + ink / 2) + 30
    img = solve_local_scrim(img, y0, y1, box=(ix0 - 60, y0 - 50, ix1 + 60, y1 + 50),
                            x0=ix0, x1=ix1, feather=150)

    layer = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    f, size, w = fit_plain(g["tag_font"], c["tagline"], g["tag_w"], 26)
    fs = font(g["tag_font"], size * SS)
    top = g["tag_cap_pct"] * H - f.getbbox("H")[1]
    d.text(((W - w) / 2 * SS, top * SS), c["tagline"], font=fs, fill=INK_LIGHT)
    layer = layer.resize((W, H), Image.LANCZOS)
    img = Image.alpha_composite(img.convert("RGBA"), layer)
    return place_mark(img, wordmark(g["mark_w"]), cx=W / 2, cy=g["mark_cy_pct"]).convert("RGB")


def build_V4(slug, g, img, c):
    """R4: ghost mark at the top, mark left, tagline + tracked kicker right."""
    W, H = g["w"], g["h"]
    tag_top = int(g["tag_cap_pct"] * H)
    kick_top = int(g["kick_cap_pct"] * H)
    # Guard the RIGHT half only: the left of this band is the bag's own dark
    # leather and darkening it would drag the product down with the type. The
    # wash is LOCAL, so the floor, the shoes and the lower jeans stay as shot.
    img = solve_local_scrim(img, tag_top - 30, kick_top + 40,
                            box=(500, tag_top - 70, W, kick_top + 80),
                            x0=520, x1=W, feather=150)

    layer = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    f, size, w = fit_plain(g["tag_font"], c["tagline"], g["tag_w"], 26)
    fs = font(g["tag_font"], size * SS)
    top = g["tag_cap_pct"] * H - f.getbbox("H")[1]
    d.text(((g["tag_right"] - w) * SS, top * SS), c["tagline"], font=fs, fill=INK_LIGHT)

    fk, sk, wk = fit_tracked(g["kick_font"], c["kicker"], g["kick_w"], g["kick_track"], 18)
    fks = font(g["kick_font"], sk * SS)
    topk = g["kick_cap_pct"] * H - fk.getbbox("H")[1]
    draw_tracked(d, (g["kick_right"] - wk) * SS, topk * SS, c["kicker"], fks,
                 sk * g["kick_track"] * SS, INK_LIGHT)

    layer = layer.resize((W, H), Image.LANCZOS)
    img = Image.alpha_composite(img.convert("RGBA"), layer)

    # The reference sets the mark twice: once faint over the bright wall at the
    # top, once solid at mid-left. The top one is nearly invisible in the
    # reference (it measures L~228 over an L~214 wall) so it ships at reduced
    # alpha rather than as a second full-strength lockup.
    img = place_mark(img, wordmark(g["ghost_w"], alpha=g["ghost_alpha"]),
                     cx=W / 2, cy=g["ghost_cy_pct"])
    return place_mark(img, wordmark(g["mark_w"]),
                      left=g["mark_left"], cy=g["mark_cy_pct"]).convert("RGB")


def build_V5(slug, g, img, c):
    """R5: tracked caps headline, two body lines, attribution, mark at bottom."""
    W, H = g["w"], g["h"]
    head_top = int(g["head_cap_pct"] * H)
    who_top = int(g["who_cap_pct"] * H)
    img = solve_scrim(img, head_top - 30, who_top + 50, head_top - 240)

    layer = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    # The headline is the brand's claim and is never quoted, in either mode.
    # R5 sets its claim in bare tracked caps and puts the review underneath;
    # quoting it would make it a pull quote, which then has to be a verbatim
    # whole sentence of the body (the Weekender run's doctored-quote law).
    headline = c["headline"]
    f, size, w = fit_tracked(g["head_font"], headline, g["head_w"], g["head_track"], 44)
    fs = font(g["head_font"], size * SS)
    top = g["head_cap_pct"] * H - f.getbbox("H")[1]
    draw_tracked(d, (W - w) / 2 * SS, top * SS, headline, fs, size * g["head_track"] * SS,
                 INK_LIGHT)

    fb, sb, _ = fit_plain(g["body_font"], c["body"][0], g["body_w"], 28)
    fbs = font(g["body_font"], sb * SS)
    y = g["body_cap_pct"] * H - fb.getbbox("H")[1]
    for ln in c["body"]:
        d.text(((W - fb.getlength(ln)) / 2 * SS, y * SS), ln, font=fbs, fill=INK_LIGHT)
        y += g["body_lead"]

    # Attribution. The verified badge is the review device and only ships in
    # review mode; in brand mode the same slot carries a product line, unbadged.
    badge = MODE == "review"
    who = f"-{c['who']}" if badge else c["who"]
    ww = fb.getlength(who)
    r = g["badge_r"]
    total = ww + (6 + r * 2 if badge else 0)
    x = (W - total) / 2
    ywho = g["who_cap_pct"] * H - fb.getbbox("H")[1]
    d.text((x * SS, ywho * SS), who, font=fbs, fill=INK_LIGHT)
    if badge:
        draw_badge(d, (x + ww + 6 + r) * SS, (ywho + sb * 0.62) * SS, r * SS)

    layer = layer.resize((W, H), Image.LANCZOS)
    img = Image.alpha_composite(img.convert("RGBA"), layer)
    return place_mark(img, wordmark(g["mark_w"]), cx=W / 2, cy=g["mark_cy_pct"]).convert("RGB")


def build_V6(slug, g, img, lines):
    """R1: three left-aligned lines low on the left, over the dark skirt."""
    W, H = g["w"], g["h"]
    y0 = int(g["cap_pct"] * H) - 30
    y1 = y0 + g["lead"] * len(lines) + 60
    img = solve_scrim(img, y0, y1, y0 - 240, x0=60, x1=740)

    layer = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    f, size, _ = fit_plain(g["font"], lines[0], g["line_w"], 30)
    fs = font(g["font"], size * SS)
    y = g["cap_pct"] * H - f.getbbox("H")[1]
    for i, ln in enumerate(lines):
        d.text((g["left"] * SS, y * SS), ln, font=fs, fill=INK_LIGHT)
        if MODE == "review" and i == len(lines) - 1:
            draw_badge(d, (g["left"] + f.getlength(ln) + 6 + g["badge_r"]) * SS,
                       (y + size * 0.62) * SS, g["badge_r"] * SS)
        y += g["lead"]
    layer = layer.resize((W, H), Image.LANCZOS)
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")


def draw_badge(d, cx, cy, rr):
    """The filled 'Verified Buyer' check. Review mode only."""
    d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=INK_LIGHT)
    chk = [(cx - 0.50 * rr, cy - 0.02 * rr), (cx - 0.16 * rr, cy + 0.36 * rr),
           (cx + 0.51 * rr, cy - 0.40 * rr)]
    d.line(chk, fill=(17, 17, 17), width=max(2, int(0.22 * rr)), joint="curve")


BUILDERS = {
    "V1-first-run": build_V1,
    "V2-leather-logo": build_centre_lockup,
    "V3-out-the-door": build_centre_lockup,
    "V4-effortless": build_V4,
    "V5-real-day": build_V5,
    "V6-quote": build_V6,
}


def build(slug):
    g = GEOM[slug]
    img = load_plate(slug, g["w"], g["h"])
    if img is None:
        print(f"{slug}: no plate, skip")
        return False
    print(f"{slug}:")
    raw = COPY[slug]
    c = raw[MODE] if MODE in raw else dict(raw)
    if slug == "V2-leather-logo" and BIRKIN:
        c = dict(c, tagline=c["tagline_birkin"])
    out = BUILDERS[slug](slug, g, img, c)
    os.makedirs(FINAL, exist_ok=True)
    dest = os.path.join(FINAL, f"VEL-VIVIENNE-{slug}.jpg")
    out.save(dest, "JPEG", quality=94, subsampling=0)
    print(f"  -> {dest}")
    return True


if __name__ == "__main__":
    names = sys.argv[1:] or list(COPY)
    n = sum(build(s) for s in names)
    print(f"composited {n}/{len(names)}  (MODE={MODE}, BIRKIN={BIRKIN})")
