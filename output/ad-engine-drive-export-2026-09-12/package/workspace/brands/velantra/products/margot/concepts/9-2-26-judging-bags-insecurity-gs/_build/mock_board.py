#!/usr/bin/env python3
"""Board mocks for VEL-MER-JUDGE-01: 9:16 plate + persistent title + score card + creator PiP window (bottom-left, plain grey wall,
mirrors the reference's rectangular selfie window). Writes board-frames/*.jpg and beat-map.json from the VO alignment."""
import json, os, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(R)
W, H = 1080, 1920
TITLE = "judging girls based on their bags with little to no explanation"
F_T = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 46)
F_S = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 60)
CREATOR = os.environ.get("CREATOR", "C3v2-claire-45-camel-cardigan-green")
A = json.load(open("vo/VO-woman-over-40-A.alignment.json"))
chars, cs, ce = A["characters"], A["character_start_times_seconds"], A["character_end_times_seconds"]
words = []; cur = ""; st = None; pe = None
for ch, s, e in zip(chars, cs, ce):
    if ch.isspace():
        if cur: words.append((cur, st, pe)); cur = ""
    else:
        if not cur: st = s
        cur += ch; pe = e
if cur: words.append((cur, st, pe))
VO_END = ce[-1]
def t_of(phrase, nth=1):
    toks = phrase.split(); k = 0
    for i in range(len(words) - len(toks) + 1):
        if [w.strip(".,?!") for w, _, _ in words[i:i+len(toks)]] == [t.strip(".,?!") for t in toks]:
            k += 1
            if k == nth: return round(words[i][1], 2)
    raise SystemExit("anchor missing: " + phrase)
BEATS = [
 ("B01", t_of("Eight out"),      "plates/J1-birkin-p086.jpg",              "8/10",  "Eight out of ten. She has taste. She also waited two years for it, and everyone at the table knows exactly what it cost.", "judgment 1 (hook)", "Real street-style still: torso, brown Birkin in hand. Title card top, score centred, creator window bottom-left."),
 ("B02", t_of("Seven. Gorgeous"),"plates/J2-lv-lv007.jpg",                 "7/10",  "Seven. Gorgeous bag. It introduces her before she opens her mouth.", "judgment 2", "Real still: monogram Neverfull on a cafe table, sunglasses, coffee. Same overlay set."),
 ("B03", t_of("Seven. Timeless"),"plates/J3-chanel-chanel026.jpg",         "7/10",  "Seven. Timeless, truly. Three other women at brunch brought the same one.", "judgment 3", "Real still: white shirt, coffee, black quilted flap on the shoulder."),
 ("B04", t_of("Eight. No"),      "plates/J4-bv-bv045.jpg",                 "8/10",  "Eight. No logo, so she knows what she's doing. She also knows exactly how delicate that weave is.", "judgment 4", "Real still: denim, grey woven Jodie held low at the hip."),
 ("B05", t_of("Ten. Same"),      "board-frames/B02-MAR002-crook-coffee.jpg","10/10", "Ten. Same taste, nobody can place the brand, and she paid what the bag is actually worth.", "verdict reveal", "OUR bag in the reference's own composition: white shirt, black Meridian at torso height, coffee. Title still up, 10/10 centred. Creator window jumps bottom-RIGHT for this one beat (mirrors ref beat 4)."),
 ("B06", t_of("This is"),        "board-frames/B03-PDP-brown-hero.jpg",     None,    "This is the Meridian from Velantra.", "product intro", "Title and score drop. Brown three-quarter hero, clean hold on the name. Creator back bottom-left."),
 ("B07a", t_of("It's a"),        "board-frames/B10-PDP-brown-onmodel.jpg",  None,    "It's a Birkin-inspired shape in grained leather,", "attribute: shape + leather", "On-model brown, the silhouette read whole."),
 ("B07b", t_of("with the two"),  "board-frames/B04b-MAR077-macro-turnlock.jpg", None, "with the two belt straps and a silver turn-lock,", "attribute: hardware", "Macro of the turn-lock and belt buckle. Hardware is silver, never brass."),
 ("B07c", t_of("no logo"),       "board-frames/B09-MAR007-coffee-balance.jpg", None, "no logo anywhere on it, and it holds its shape packed full.", "attribute: no logo, structure", "Coffee brown carried full at her side, front face clean."),
 ("B08a", t_of("I've carried"),  "board-frames/B02b-MAR013-friday-street.jpg", None, "I've carried mine every single day since spring,", "proof (lived)", "Cognac carried past the flower stand."),
 ("B08b", t_of("and I get"),     "board-frames/B11c-MAR009-crosswalk-front.jpg", None, "and I get asked where it's from about once a week.", "proof (lived)", "Brown at the crosswalk, full and soft."),
 ("B09a", t_of("Your laptop"),   "board-frames/B11b-MAR061-pack-laptop.jpg", None,  "Your laptop drops straight in, plus a planner and a water bottle,", "capacity demo", "Laptop sliding into the main compartment. Demonstrate, never describe."),
 ("B09b", t_of("and there's"),   "board-frames/B11-MAR053-open-overhead.jpg", None, "and there's a zip pocket down the middle so your keys never end up under your laptop.", "capacity demo: the zip", "Open top overhead, centre zip visible, packed."),
 ("B10", t_of("It comes"),       "board-frames/B13-COLORWAY-6up.jpg",       None,    "It comes in six colors.", "variants", "Six-up PDP colorway card."),
 ("B11", t_of("They're running"),"board-frames/B14-PDP-scroll-start.jpg",   None,    "They're running a sale on it right now, and the colors do sell out. I left the link below.", "offer + CTA", "Live PDP screen recording, continuous: $149.99 struck to $124.99, six swatches, Add to Cart. Holds to the last frame."),
]
def fill(src):
    im = Image.open(src).convert("RGB"); w, h = im.size; s = max(W / w, H / h)
    im = im.resize((round(w * s), round(h * s)), Image.LANCZOS); w2, h2 = im.size
    return im.crop(((w2 - W) // 2, (h2 - H) // 2, (w2 - W) // 2 + W, (h2 - H) // 2 + H))
def shadow_text(dr, xy, txt, font, fill="white"):
    x, y = xy
    dr.text((x + 2, y + 2), txt, font=font, fill=(0, 0, 0, 170)); dr.text((x, y), txt, font=font, fill=fill)
def wrap(txt, font, maxw):
    out, line = [], ""
    for w in txt.split():
        t = (line + " " + w).strip()
        if font.getlength(t) > maxw and line: out.append(line); line = w
        else: line = t
    if line: out.append(line)
    return out
# creator window: key the green plate onto a flat grey wall, crop to a 5:6 window
def creator_window(path, ww=300, wh=360):
    im = Image.open(path).convert("RGB"); a = np.asarray(im).astype(int); r, g, b = a[..., 0], a[..., 1], a[..., 2]
    green = (g > 120) & (g > r + 40) & (g > b + 40)
    mask = Image.fromarray(((~green) * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
    wall = Image.new("RGB", im.size, (128, 128, 126)); comp = Image.composite(im, wall, mask)
    ys, xs = np.where(np.asarray(mask) > 128); top = ys.min(); cx = int(np.median(xs[ys < top + 0.12 * (ys.max() - top)]))
    head_w = int(np.ptp(xs[ys < top + 0.12 * (ys.max() - top)]))
    # head ~ 40% of window width, head top ~ 12% down the window
    s = (0.40 * ww) / head_w; cw, chh = int(ww / s), int(wh / s)
    box = (max(0, cx - cw // 2), max(0, top - int(0.12 * chh)), 0, 0); box = (box[0], box[1], min(im.width, box[0] + cw), min(im.height, box[1] + chh))
    return comp.crop(box).resize((ww, wh), Image.LANCZOS)
PIP = creator_window(f"creator/{CREATOR}.png"); PIP.save("_build/pip-window.png")
os.makedirs("board-frames", exist_ok=True); beatmap = []
for i, (bid, t, src, score, line, emotion, visual) in enumerate(BEATS):
    t_end = BEATS[i + 1][1] if i + 1 < len(BEATS) else round(VO_END + 0.4, 2)
    base = fill(src).convert("RGBA"); ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dr = ImageDraw.Draw(ov)
    if score:
        y = 150
        for ln in wrap(TITLE, F_T, 560): shadow_text(dr, ((W - F_T.getlength(ln)) / 2, y), ln, F_T); y += 56
        shadow_text(dr, ((W - F_S.getlength(score)) / 2, 1190), score, F_S)
    base = Image.alpha_composite(base, ov)
    px = W - 20 - PIP.width if bid == "B05" else 20
    base.paste(PIP, (px, 1720 - PIP.height))
    out = f"board-frames/{bid}-mock.jpg"; base.convert("RGB").save(out, quality=92)
    beatmap.append({"beat": bid, "in": t, "out": t_end, "src": src, "mock": out, "score": score, "line": line, "emotion": emotion, "visual": visual})
json.dump(beatmap, open("beat-map.json", "w"), indent=1)
for b in beatmap: print(b["beat"], b["in"], b["out"], b["src"].split("/")[-1])
# QA sheet
ims = [Image.open(b["mock"]).resize((216, 384)) for b in beatmap]; cols = 8; rows = (len(ims) + cols - 1) // cols
sh = Image.new("RGB", (cols * 220, rows * 390), "white")
for i, im in enumerate(ims): sh.paste(im, ((i % cols) * 220, (i // cols) * 390))
sh.save("_build/board-frames-sheet.jpg", quality=82); print("sheet", sh.size)
