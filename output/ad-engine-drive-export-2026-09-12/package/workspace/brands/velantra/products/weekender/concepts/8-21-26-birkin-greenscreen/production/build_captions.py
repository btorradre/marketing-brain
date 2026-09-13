#!/usr/bin/env python3
"""Caption cards for VEL-WEEKENDER-GS-BIRKIN-01, cut on Scribe word timestamps.

Cards cap at 4 words AND flush at any word ending in terminal punctuation, so a
sentence never splits across cards. Each card is clamped to the next card's
start so overlapping ranges cannot stack two cards into garble.
"""
import json, os

STT = "/tmp/stt_take2.json"
CON = ("/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/"
       "weekender/concepts/8-21-26-birkin-greenscreen")
OUT = os.path.join(CON, "production/captions.ass")

MAXW = 4
words = [w for w in json.load(open(STT))["words"] if w.get("type") == "word"]

cards, cur = [], []
for w in words:
    cur.append(w)
    flush = len(cur) >= MAXW or w["text"].rstrip()[-1:] in ".?!"
    if flush:
        cards.append(cur)
        cur = []
if cur:
    cards.append(cur)

rows = []
for i, c in enumerate(cards):
    start = c[0]["start"]
    end = c[-1]["end"] + 0.12
    if i + 1 < len(cards):
        end = min(end, cards[i + 1][0]["start"] - 0.02)
    if end <= start:
        end = start + 0.15
    text = " ".join(w["text"].strip() for w in c)
    rows.append((start, end, text))


def ts(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


# MarginV places the card at roughly 77% down a 1920-tall frame, matching the
# reference ad's caption line.
header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Arial,74,&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,7,0,2,70,70,410,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

with open(OUT, "w", encoding="utf-8") as f:
    f.write(header)
    for s, e, t in rows:
        f.write(f"Dialogue: 0,{ts(s)},{ts(e)},Cap,,0,0,0,,{t}\n")

print(f"{len(rows)} caption cards -> {OUT}")
print("first 6:")
for s, e, t in rows[:6]:
    print(f"  {s:6.2f}-{e:6.2f}  {t}")
print("...")
for s, e, t in rows[-3:]:
    print(f"  {s:6.2f}-{e:6.2f}  {t}")
