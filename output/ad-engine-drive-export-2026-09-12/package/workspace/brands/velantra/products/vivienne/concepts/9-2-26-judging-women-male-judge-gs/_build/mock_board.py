#!/usr/bin/env python3
"""Board mocks for VEL-VIV-JUDGE-01 v3: GREENSCREEN cut-out judge over full-bleed stills per the 8/31 edge-cut law
(head 0.20 W, head top ~1260, body past the bottom and left edges), persistent title on the shame beats, no scores.
Writes board-frames/*-mock.jpg + beat-map.json off the chosen VO take."""
import json, os, sys, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(R)
W, H = 1080, 1920
TITLE = "judging women based on their bags with little to no explanation"
F_T = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 46)
TAKE = os.environ.get("TAKE", "D"); CREATOR = os.environ.get("CREATOR", "G1-charcoal-green")
HEAD_W_FRAC, HEAD_TOP_Y, BOTTOM_BLEED, SIDE_BLEED = 0.20, 1260, 60, 70
A = json.load(open(f"vo/VO-gringo-{TAKE}.alignment.json"))
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
    toks = [t.strip(".,?!") for t in phrase.split()]; k = 0
    for i in range(len(words) - len(toks) + 1):
        if [w.strip(".,?!") for w, _, _ in words[i:i+len(toks)]] == toks:
            k += 1
            if k == nth: return round(words[i][1], 2)
    raise SystemExit("anchor missing: " + phrase)
BEATS = [
 ("B01", t_of("Ladies I"),      "plates/C1-cheap-puffer-sl056.jpg", True,  "left",  "Ladies, I can tell when your bag was cheap. So can every man in the room, and so can every woman at the table.", "hook: the shame", "Real still, a woman from behind at a cafe counter with a cheap quilted puffer bag. Title card top. Judge keyed bottom-left, cut by the frame."),
 ("B02", t_of("You put"),       "plates/C2-cheap-houndstooth-sl055.jpg", True, "left", "You put the outfit together, you did the hair, and then you walked in carrying something that told everyone you cut a corner.", "agitate: she cut a corner", "Real still, the outfit is right and the bag is a cheap houndstooth hobo."),
 ("B03", t_of("A cheap"),       "plates/C2alt-cheap-red-hobo-sl000.jpg", True, "left", "A cheap bag tells people you didn't think you were worth the good one.", "the wound", "Real still, red hobo on a sunset street, sunglasses."),
 ("B04", t_of("The women"),     "board-frames/B07-ed-bench.jpg", False, "right", "The women who get treated differently are carrying real leather, real hardware, a bag that looks like money.", "the expensive-bag need (curiosity opens: how do I afford that)", "Vivienne editorial bench still, the bag that looks like money. Title card is OFF from here. Judge jumps bottom-right for this beat."),
 ("B05", t_of("And before"),    "board-frames/B10-lifestyle-cognac-carried.jpg", False, "left", "And before you say it, no, you don't have to spend all that money anymore.", "the reversal", "Cognac carried full on the street. Title drops here."),
 ("B06", t_of("This is"),       "board-frames/B03-front-hero.jpg", False, "left", "This is the Vivienne from Velantra.", "product intro (the mantra)", "Chocolate front hero, clean hold on the name. Captions start."),
 ("B07a", t_of("It's soft"),    "board-frames/B04-O4-fingers-press.jpg", False, "left", "It's soft vegetable tanned leather", "attribute: leather", "Fingers press the leather, it gives."),
 ("B07b", t_of("with aged"),    "board-frames/B04b-O5-brass-lock.jpg", False, "left", "with aged brass hardware,", "attribute: hardware", "Brass lock macro. Brass, never silver."),
 ("B07c", t_of("a shoulder"),   "board-frames/B02-O9-on-the-hip.jpg", False, "left", "a shoulder strap you can take off,", "attribute: strap", "On the hip on the shoulder strap, hallway."),
 ("B07d", t_of("and there's"),  "board-frames/B06-O2-clean-front-no-logo.jpg", False, "left", "and there's no logo anywhere on it, so nobody can tell what you paid.", "attribute: no logo = the insecurity resolved", "Clean front, nothing on it."),
 ("B08a", t_of("It looks"),     "board-frames/B09-three-quarter.jpg", False, "left", "It looks like the bag the woman with the corner office carries,", "desire", "Chocolate three-quarter."),
 ("B08b", t_of("and it holds"), "board-frames/B05-O10-desk-notebook.jpg", False, "left", "and it holds her whole day, planner, water bottle, everything, without looking like luggage.", "capacity (cleared claims only)", "Desk, notebook, mug. No laptop claim on this bag."),
 ("B09", t_of("It comes"),      "board-frames/B12-COLORWAY-4up.jpg", False, "left", "It comes in four colors.", "variants", "Four-up colorway card."),
 ("B10", t_of("They're running"), "board-frames/B13-PDP-scroll-start.jpg", False, "left", "They're running a pre-order sale on it right now, it ships in October, and the colors do sell out.", "offer, ship date stated", "Live PDP scroll: $199.99 struck to $149.99, four swatches, Expected to ship October."),
 ("B11", t_of("I left"),        "board-frames/B14-PDP-scroll-end.jpg", False, "left", "I left the link below. Stop walking in with the cheap one.", "CTA + the last jab", "PDP settles on the pre-order line, holds to the last frame."),
]
def fill(src):
    im = Image.open(src).convert("RGB"); w, h = im.size; s = max(W / w, H / h)
    im = im.resize((round(w * s), round(h * s)), Image.LANCZOS); w2, h2 = im.size
    return im.crop(((w2 - W) // 2, (h2 - H) // 2, (w2 - W) // 2 + W, (h2 - H) // 2 + H))
def shadow_text(dr, xy, txt, font):
    x, y = xy; dr.text((x + 2, y + 2), txt, font=font, fill=(0, 0, 0, 170)); dr.text((x, y), txt, font=font, fill="white")
def wrap(txt, font, maxw):
    out, line = [], ""
    for w in txt.split():
        t = (line + " " + w).strip()
        if font.getlength(t) > maxw and line: out.append(line); line = w
        else: line = t
    if line: out.append(line)
    return out
def key_plate(path):
    im = Image.open(path).convert("RGB"); a = np.asarray(im).astype(int); r, g, b = a[..., 0], a[..., 1], a[..., 2]
    green = (g > 110) & (g > r + 35) & (g > b + 35)
    mask = Image.fromarray(((~green) * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.0))
    # despill: pull green channel down toward the mean of r,b on the kept pixels
    a2 = a.copy(); spill = a2[..., 1] > (a2[..., 0] + a2[..., 2]) / 2 + 8
    a2[..., 1][spill] = ((a2[..., 0] + a2[..., 2]) / 2 + 8)[spill]
    rgba = Image.fromarray(a2.astype(np.uint8)).convert("RGBA"); rgba.putalpha(mask)
    m = np.asarray(mask) > 128; ys, xs = np.where(m); top = ys.min(); band = m[top:top + int(0.11 * (ys.max() - top))]
    hx = np.where(band.any(0))[0]; return rgba, {"head_top": int(top), "head_w": int(hx.max() - hx.min()), "head_cx": int((hx.max() + hx.min()) // 2), "w": im.width, "h": im.height}
PLATE, M = key_plate(f"creator/{CREATOR}.png")
s = (HEAD_W_FRAC * W) / M["head_w"]; sw, sh_ = int(round(M["w"] * s)), int(round(M["h"] * s))
SC = PLATE.resize((sw, sh_), Image.LANCZOS)
y = HEAD_TOP_Y - int(M["head_top"] * s)                      # head top lands at HEAD_TOP_Y
y = max(y, H + BOTTOM_BLEED - sh_)                             # never float: body must run past the bottom edge
xL = -SIDE_BLEED + 0; xL = min(xL, int(0.20 * W - M["head_cx"] * s))   # head centre near 0.20 W, body past the left edge
xR = W + SIDE_BLEED - sw; xR = max(xR, int(0.80 * W - M["head_cx"] * s))
geo = {"scale": round(s, 3), "plate": [sw, sh_], "y": y, "xL": xL, "xR": xR, "head_top_y": HEAD_TOP_Y, **M}
json.dump(geo, open("_build/pip-geometry.json", "w"), indent=1); print("geometry", geo)
beatmap = []
for i, (bid, t, src, title_on, pos, line, emotion, visual) in enumerate(BEATS):
    t_end = BEATS[i + 1][1] if i + 1 < len(BEATS) else round(VO_END + 0.4, 2)
    base = fill(src).convert("RGBA"); ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dr = ImageDraw.Draw(ov)
    if title_on:
        yy = 150
        for ln in wrap(TITLE, F_T, 560): shadow_text(dr, ((W - F_T.getlength(ln)) / 2, yy), ln, F_T); yy += 56
    base = Image.alpha_composite(base, ov)
    base.alpha_composite(SC, (xR if pos == "right" else xL, y))
    out = f"board-frames/{bid}-mock.jpg"; base.convert("RGB").save(out, quality=92)
    beatmap.append({"beat": bid, "in": t, "out": t_end, "src": src, "mock": out, "title": title_on, "creator": pos, "line": line, "emotion": emotion, "visual": visual})
json.dump(beatmap, open("beat-map.json", "w"), indent=1)
for b in beatmap: print(b["beat"], b["in"], b["out"], b["src"].split("/")[-1])
ims = [Image.open(b["mock"]).resize((216, 384)) for b in beatmap]; cols = 8; rows = (len(ims) + cols - 1) // cols
sh = Image.new("RGB", (cols * 220, rows * 390), "white")
for i, im in enumerate(ims): sh.paste(im, ((i % cols) * 220, (i // cols) * 390))
sh.save("_build/board-frames-sheet.jpg", quality=82); print("sheet", sh.size, "VO_END", round(VO_END, 2), "take", TAKE)
