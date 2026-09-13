#!/usr/bin/env python3
"""VEL-WEEKENDER-OVERSIZED-01 v2 bed: every bag shot is real motion footage.

Order of resort per house law: Brooks's real filmed clips first, then approved
library b-roll, then a generated motion clip, never a still. Beat boundaries
come from the ElevenLabs character alignment of the locked take.
"""
import json, os, re, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = "/Users/brooksorradre2/Documents/marketing brain"
WK = os.path.join(ROOT, "brands/velantra/products/weekender")
CON = os.path.join(WK, "concepts/9-1-26-oversized-chic-listicle")
GS = os.path.join(WK, "concepts/8-21-26-birkin-greenscreen")
REAL = os.path.join(WK, "actual product assets")
BR = os.path.join(WK, "broll")
VOJOB = os.path.join(ROOT, "_engine/mcp/ad-engine/data/vo/job_5de3cd0ca756")
OUT = os.path.join(CON, "production/beats"); os.makedirs(OUT, exist_ok=True)
W, H, FPS = 1080, 1920, 25

# ---- words from the character alignment --------------------------------
al = json.load(open(os.path.join(VOJOB, "alignment.json")))
if "alignment" in al:
    al = al["alignment"]
chars, st, en = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
words, cur, cs, ce = [], "", None, None
for c, s, e in zip(chars, st, en):
    if c.isspace():
        if cur:
            words.append({"text": cur, "start": cs, "end": ce}); cur = ""
        continue
    if not cur:
        cs = s
    cur += c; ce = e
if cur:
    words.append({"text": cur, "start": cs, "end": ce})
json.dump({"words": words}, open(os.path.join(CON, "production/words.json"), "w"), indent=1)
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                            os.path.join(VOJOB, "voiceover.mp3")], capture_output=True, text=True).stdout.strip())


def norm(t):
    return re.sub(r"[^a-z0-9']", "", t.lower())


def find(phrase, after=0):
    toks = [norm(t) for t in phrase.split()]
    for i in range(after, len(words) - len(toks) + 1):
        if all(norm(words[i + k]["text"]) == toks[k] for k in range(len(toks))):
            return i
    raise SystemExit(f"beat phrase not found: {phrase}")


STARTS = [("b01", "Okay, I found"), ("b02", "This is the"), ("b03", "It's a Birkin-inspired"),
          ("b04", "full-grain leather"), ("b05", "It's eighteen inches"), ("b06", "and it still"),
          ("b07", "The inside is"), ("b08", "I've carried it"), ("b09", "It sits on"),
          ("b10", "it slides straight"), ("b11", "and I haven't"), ("b12", "I get asked"),
          ("b13", "It comes in"), ("b14", "And if you"), ("b15", "They're running a"), ("b16", "I left the")]
T, idx = [], 0
for b, ph in STARTS:
    idx = find(ph, idx); T.append(round(words[idx]["start"], 3))
T[0] = 0.0; T.append(round(dur, 3))

# ---- sources: (beat, kind, source, in-point) ----------------------------
# kind: clip = library/real footage, pdp = screen capture, grid = 2x2 live tiles + title
GRID_TILES = [(os.path.join(BR, "lc-travel-S10.mp4"), 1.0),       # TL woman walking, bag + silver roller
              (os.path.join(BR, "dc-B13-onluggage.mp4"), 1.0),    # TR dark chocolate on green roller
              (os.path.join(BR, "onroute-S1.mp4"), 1.0),          # BL trench + aluminium roller
              (os.path.join(BR, "NB-08-doorway-pickup.mp4"), 0.5)]   # BR black held up in the doorway
PLAN = [
    ("b01", "grid", None, 0),
    ("b02", "clip", os.path.join(BR, "lc-travel-S09.mp4"), 1.0),                 # bag on the roller handle
    ("b03", "clip", os.path.join(BR, "NB-04-carry-hallway.mp4"), 2.0),           # walking carry, silhouette
    ("b04", "clip", os.path.join(REAL, "IMG_4052.MOV"), 3.0),                    # REAL: hand turning the lock
    ("b05", "clip", os.path.join(BR, "onroute-S2.mp4"), 1.0),                    # laptop going in
    ("b06", "clip", os.path.join(BR, "onroute-S4.mp4"), 1.0),                    # open packed, holds shape
    ("b07", "clip", os.path.join(REAL, "IMG_4051.MOV"), 3.5),                    # REAL: flap folds back, caramel inside
    ("b08", "clip", os.path.join(BR, "onroute-S1.mp4"), 1.0),                    # trench, bag in hand, roller
    ("b09", "clip", os.path.join(BR, "askme-ELEANOR-S09.mp4"), 1.0),                 # bag on the carry-on
    ("b10", "clip", os.path.join(CON, "production/gen/overhead-bin.mp4"), 0.0),  # generated motion, bag static in bin
    ("b11", "clip", os.path.join(BR, "NB-09-airport-bench.mp4"), 1.0),               # at the gate beside the carry-on
    ("b12", "clip", os.path.join(BR, "lc-travel-S05.mp4"), 1.0),                 # leather macro, no logo
    ("b13", "pdp", os.path.join(GS, "production/pdp/b17_swatches.mp4"), 0),
    ("b14", "clip", os.path.join(BR, "NB-12-stairs-descend.mp4"), 3.0),          # black carried
    ("b15", "pdp", os.path.join(GS, "production/pdp/b18_price.mp4"), 0),
    ("b16", "pdp", os.path.join(GS, "production/pdp/b21_cart.mp4"), 0),
]
BASE = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}"


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print("FFMPEG FAIL", cmd[-1], r.stderr[-600:], file=sys.stderr)
    return r.returncode == 0


def title_png(path):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)

    def font(sz):
        for f in ["/System/Library/Fonts/HelveticaNeue.ttc", "/System/Library/Fonts/Helvetica.ttc"]:
            try:
                return ImageFont.truetype(f, sz, index=1)
            except Exception:
                pass
        return ImageFont.load_default()
    y = 880
    for txt, f in [("The Oversized Travel Bag", font(62)), ("That's Actually Chic", font(62)),
                   ("& Worth Traveling With", font(34))]:
        bb = d.textbbox((0, 0), txt, font=f); w = bb[2] - bb[0]; x = (W - w) // 2
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (2, 2), (-2, 2), (2, -2)]:
            d.text((x + dx, y + dy), txt, font=f, fill=(0, 0, 0, 255))
        d.text((x, y), txt, font=f, fill=(255, 255, 255, 255)); y += bb[3] - bb[1] + 22
    im.save(path)


def build_grid(dst, d):
    title = os.path.join(CON, "production/_grid_title.png"); title_png(title)
    ins = []
    for src, ss in GRID_TILES:
        ins += ["-stream_loop", "2", "-ss", str(ss), "-t", str(d), "-i", src]
    ins += ["-i", title]
    tile = "scale=540:960:force_original_aspect_ratio=increase,crop=540:960,fps=25,setsar=1"
    fc = ";".join(f"[{i}:v]{tile}[t{i}]" for i in range(4))
    fc += ";[t0][t1][t2][t3]xstack=inputs=4:layout=0_0|540_0|0_960|540_960[g];[g][4:v]overlay=0:0,format=yuv420p[v]"
    return run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error"] + ins +
               ["-filter_complex", fc, "-map", "[v]", "-t", str(d), "-an", dst])


for i, (b, kind, src, ss) in enumerate(PLAN):
    d = round(T[i + 1] - T[i], 3)
    dst = os.path.join(OUT, f"{b}.mp4")
    if kind == "grid":
        ok = build_grid(dst, d); src = "grid(4 live tiles)"
    else:
        if not os.path.exists(src):
            raise SystemExit(f"missing {src}")
        ok = run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-stream_loop", "2", "-ss", str(ss),
                  "-i", src, "-t", str(d), "-vf", f"{BASE},fps={FPS},format=yuv420p", "-an", dst])
    print(f"{b}: {T[i]:6.2f} -> {T[i+1]:6.2f} ({d:5.2f}s) {'ok' if ok else 'FAIL'} <- {os.path.basename(str(src))}")

lst = os.path.join(CON, "production/_concat.txt")
with open(lst, "w") as f:
    for b, *_ in PLAN:
        f.write(f"file '{os.path.join(OUT, b + '.mp4')}'\n")
bed = os.path.join(CON, "production/bed.mp4")
ok = run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
          "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), bed])
json.dump({"T": T, "duration": dur}, open(os.path.join(CON, "production/beat_times.json"), "w"), indent=1)
print("bed:", bed, ok)
