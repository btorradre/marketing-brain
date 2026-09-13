#!/usr/bin/env python3
"""Caption track for VEL-WEEKENDER-OVERSIZED-01 as one VP9 alpha video.

Mirrors the reference: white bold with a black outline, centred mid-frame
(~50% of height, above the creator plate whose top sits at 57%). Cards cap at
5 words and flush at terminal punctuation. Word times come from the ElevenLabs
alignment of the locked take (production/words.json), so the brand is spelled
from the script, never by ear.
"""
import json, os, subprocess
from PIL import Image, ImageDraw, ImageFont

CON = ("/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/"
       "weekender/concepts/9-1-26-oversized-chic-listicle")
WORK = os.path.join(CON, "production/captions"); os.makedirs(WORK, exist_ok=True)
OUTV = os.path.join(CON, "production/captions.webm")
W, H = 1080, 1920
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
SIZE, STROKE = 64, 6
CENTER_Y = int(H * 0.50)
MAXW_PX = int(W * 0.80)
MAXW = 5
font = ImageFont.truetype(FONT, SIZE)

words = json.load(open(os.path.join(CON, "production/words.json")))["words"]
# the TTS feed respells the brand for pronunciation; captions show the real spelling
for w in words:
    w["text"] = w["text"].replace("Vell-Ahn-Trah", "Velantra").replace("vell-ahn-trah", "Velantra")
BT = json.load(open(os.path.join(CON, "production/beat_times.json")))
DUR = BT["duration"]
# the hook grid carries its own title (as in the reference), so no caption cards over beat 1
words = [w for w in words if w["start"] >= BT["T"][1] - 0.05]

cards, cur = [], []
for w in words:
    cur.append(w)
    if len(cur) >= MAXW or w["text"][-1:] in ".?!":
        cards.append(cur); cur = []
if cur:
    cards.append(cur)
rows = []
for i, c in enumerate(cards):
    s, e = c[0]["start"], c[-1]["end"] + 0.15
    if i + 1 < len(cards):
        e = min(e, cards[i + 1][0]["start"] - 0.02)
    rows.append((s, max(e, s + 0.15), " ".join(x["text"] for x in c)))


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
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    lines = wrap(txt); lh = SIZE + 12
    y = CENTER_Y - (len(lines) * lh) // 2
    for ln in lines:
        bb = d.textbbox((0, 0), ln, font=font, stroke_width=STROKE)
        d.text(((W - (bb[2] - bb[0])) / 2 - bb[0], y), ln, font=font, fill=(255, 255, 255, 255),
               stroke_width=STROKE, stroke_fill=(0, 0, 0, 255))
        y += lh
    p = os.path.join(WORK, f"c{i:03d}.png"); im.save(p); paths.append(p)

seq, t = [], 0.0
for (s, e, _), p in zip(rows, paths):
    if s > t + 0.001:
        seq.append((blank, s - t))
    seq.append((p, e - s)); t = e
if t < DUR:
    seq.append((blank, DUR - t))
lst = os.path.join(WORK, "_concat.txt")
with open(lst, "w") as f:
    for p, d_ in seq:
        f.write(f"file '{p}'\nduration {max(d_, 0.04):.3f}\n")
    f.write(f"file '{seq[-1][0]}'\n")
r = subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                    "-i", lst, "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "0", "-crf", "30",
                    "-r", "25", "-t", str(DUR), OUTV], capture_output=True, text=True)
print("cards:", len(rows), "| wrote" if not r.returncode else r.stderr[-800:], OUTV)
for s, e, txt in rows:
    print(f"{s:6.2f}-{e:6.2f}  {txt}")
