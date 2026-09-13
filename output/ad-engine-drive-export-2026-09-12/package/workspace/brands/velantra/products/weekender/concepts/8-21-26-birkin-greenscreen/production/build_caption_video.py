#!/usr/bin/env python3
"""Render the caption track as a single VP9 alpha video.

This ffmpeg build has neither libass nor drawtext, so cards are drawn with
Pillow and concatenated (card / transparent gap) into one full-length RGBA
overlay, which the assembler composites in a single pass.

Cards cap at 4 words AND flush at terminal punctuation so a sentence never
splits, and each card is clamped to the next card's start so two cards can
never stack into garble.
"""
import json, os, subprocess, sys

CON = ("/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/"
       "weekender/concepts/8-21-26-birkin-greenscreen")
# CLI: build_caption_video.py [stt_json] [duration] [out_basename]
STT_PATH = sys.argv[1] if len(sys.argv) > 1 else "/tmp/stt_take2.json"
DUR_ARG = float(sys.argv[2]) if len(sys.argv) > 2 else 79.201
TAG = sys.argv[3] if len(sys.argv) > 3 else "captions"
WORK = os.path.join(CON, "production/" + TAG)
os.makedirs(WORK, exist_ok=True)
OUTV = os.path.join(CON, f"production/{TAG}.webm")

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
SIZE = 76
STROKE = 7
BASELINE_Y = int(H * 0.775)      # matches the reference ad's caption line
MAXW_PX = int(W * 0.86)
DUR = DUR_ARG

font = ImageFont.truetype(FONT, SIZE)

# Scribe hears the brand correctly but spells it by ear, so the raw transcript
# would burn a misspelled brand into the ad. Correct it before drawing.
RESPELL = {"velentra": "Velantra", "valentra": "Velantra", "volantra": "Velantra"}


def fix(tok):
    bare = tok.strip(".,!?").lower()
    if bare in RESPELL:
        return tok.lower().replace(bare, RESPELL[bare])
    return tok


words = [w for w in json.load(open(STT_PATH))["words"]
         if w.get("type") == "word"]
for w in words:
    w["text"] = fix(w["text"])

cards, cur = [], []
for w in words:
    cur.append(w)
    if len(cur) >= 4 or w["text"].rstrip()[-1:] in ".?!":
        cards.append(cur); cur = []
if cur:
    cards.append(cur)

rows = []
for i, c in enumerate(cards):
    s = c[0]["start"]
    e = c[-1]["end"] + 0.12
    if i + 1 < len(cards):
        e = min(e, cards[i + 1][0]["start"] - 0.02)
    if e <= s:
        e = s + 0.15
    rows.append((s, e, " ".join(x["text"].strip() for x in c)))


def wrap(txt):
    lines, cur_l = [], ""
    for word in txt.split():
        t = (cur_l + " " + word).strip()
        if font.getbbox(t)[2] - font.getbbox(t)[0] > MAXW_PX and cur_l:
            lines.append(cur_l); cur_l = word
        else:
            cur_l = t
    if cur_l:
        lines.append(cur_l)
    return lines


blank = os.path.join(WORK, "_blank.png")
Image.new("RGBA", (W, H), (0, 0, 0, 0)).save(blank)

paths = []
for i, (s, e, txt) in enumerate(rows):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    lines = wrap(txt)
    lh = SIZE + 14
    y = BASELINE_Y - (len(lines) - 1) * lh
    for ln in lines:
        bb = d.textbbox((0, 0), ln, font=font, stroke_width=STROKE)
        d.text(((W - (bb[2] - bb[0])) / 2 - bb[0], y), ln, font=font,
               fill=(255, 255, 255, 255), stroke_width=STROKE,
               stroke_fill=(0, 0, 0, 255))
        y += lh
    p = os.path.join(WORK, f"c{i:03d}.png")
    im.save(p)
    paths.append(p)

# concat list alternating transparent gaps and cards
seq, t = [], 0.0
for (s, e, _), p in zip(rows, paths):
    if s > t + 0.001:
        seq.append((blank, s - t))
    seq.append((p, e - s))
    t = e
if t < DUR:
    seq.append((blank, DUR - t))

lst = os.path.join(WORK, "_concat.txt")
with open(lst, "w") as f:
    for p, d_ in seq:
        f.write(f"file '{p}'\nduration {max(d_, 0.04):.3f}\n")
    f.write(f"file '{seq[-1][0]}'\n")

cmd = ["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-f", "concat",
       "-safe", "0", "-i", lst, "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p",
       "-b:v", "0", "-crf", "30", "-r", "25", "-t", str(DUR), OUTV]
r = subprocess.run(cmd, capture_output=True, text=True)
print("cards:", len(rows), "| segments:", len(seq))
if r.returncode:
    print("FAIL\n", r.stderr[-1200:])
else:
    print("wrote", OUTV, f"{os.path.getsize(OUTV)/1e6:.1f}MB")
