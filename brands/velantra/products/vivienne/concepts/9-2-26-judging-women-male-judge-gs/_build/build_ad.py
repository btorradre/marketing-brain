#!/usr/bin/env python3
"""Composite VEL-VIV-JUDGE-01 (greenscreen male judge, cheap-bag shame -> reversal -> This is the Vivienne).

Hard-cut stills -> live PDP scroll, judge keyed BOTTOM-LEFT and cut by the bottom + left edges (bottom-right on B04),
title card on B01-B04, one VO (gringo take D), caption cards from B06 off the alignment, centred, above the head.
Ported from the 9/02 grid build_ad.py.

  python3 build_ad.py bed          # no creator
  python3 build_ad.py G1           # needs creator/renders/G1-heygen-green.mp4
  KEY_SIM=0.12 KEY_BLEND=0.05 python3 build_ad.py G1
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = os.path.join(ROOT, "_build", "tmp"); os.makedirs(T, exist_ok=True)
TAKE = os.environ.get("TAKE", "J")
VO = os.path.join(ROOT, "vo", f"VO-gringo-{TAKE}.mp3")
ALIGN = json.load(open(os.path.join(ROOT, "vo", f"VO-gringo-{TAKE}.alignment.json")))
BEATS = json.load(open(os.path.join(ROOT, "beat-map.json")))
W, H, FPS = 1080, 1920, 30
ARIAL = "/System/Library/Fonts/Supplemental/Arial.ttf"; ARIAL_B = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
TITLE = "judging women based on their bags with little to no explanation"
CAP_SIZE, CAP_Y_BOTTOM = 52, 1180                 # caption block bottom edge sits above the head top (1260)
HEAD_W_FRAC, HEAD_TOP_Y, BOTTOM_BLEED, SIDE_BLEED = 0.20, 1260, 60, 70
RESPELL = {"Vivian": "Vivienne", "Vehlantra": "Velantra", "Volantra": "Velantra", "Vell-Ahn-Trah": "Velantra"}
KEY_SIM, KEY_BLEND = float(os.environ.get("KEY_SIM", "0.10")), float(os.environ.get("KEY_BLEND", "0.03"))
DESPILL = float(os.environ.get("DESPILL", "0.15"))

chars, cs, ce = ALIGN["characters"], ALIGN["character_start_times_seconds"], ALIGN["character_end_times_seconds"]
VO_END = ce[-1]
CAP_FROM = next(b["in"] for b in BEATS if b["beat"] == "B06")     # captions from the product intro
SRC = {}
for b in BEATS:
    if b["beat"] == "B10": SRC[b["beat"]] = "pdp/PDP-scroll.mp4"
    elif b["beat"] == "B11": SRC[b["beat"]] = None                  # PDP recording spans B10+B11
    else: SRC[b["beat"]] = b["src"]
TITLE_UNTIL = max(b["out"] for b in BEATS if b.get("title"))
RIGHT_BEATS = [(b["in"], b["out"]) for b in BEATS if b.get("creator") == "right"]

def fill_9x16(src, dst):
    im = Image.open(src).convert("RGB"); w, h = im.size; s = max(W / w, H / h)
    im = im.resize((round(w * s), round(h * s)), Image.LANCZOS); w2, h2 = im.size
    im.crop(((w2 - W) // 2, (h2 - H) // 2, (w2 - W) // 2 + W, (h2 - H) // 2 + H)).save(dst, quality=94)

# ---- background bed: hard cuts, the PDP recording spans B10..end
segs = []; n = 0
while n < len(BEATS):
    b = BEATS[n]; asset = SRC[b["beat"]]; s = b["in"]; m = n + 1
    while m < len(BEATS) and SRC[BEATS[m]["beat"]] is None: m += 1
    e = BEATS[m - 1]["out"] if m - 1 < len(BEATS) - 1 else VO_END + 0.4
    d = max(e - s, 0.2); out = os.path.join(T, f"seg{n:02d}.mp4"); src = os.path.join(ROOT, asset)
    if not os.path.exists(out):
        if asset.endswith(".mp4"):
            src_d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src], capture_output=True, text=True).stdout.strip())
            factor = max(d / src_d, 1.0)
            cmd = ["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", f"setpts={factor:.4f}*PTS,scale={W}:{H},format=yuv420p", "-t", f"{d:.3f}", "-r", str(FPS), "-c:v", "libx264", "-crf", "17", "-an", out]
        else:
            still = os.path.join(T, f"fill-{n:02d}.jpg"); fill_9x16(src, still)
            cmd = ["ffmpeg", "-v", "error", "-y", "-loop", "1", "-t", f"{d:.3f}", "-i", still, "-vf", "format=yuv420p", "-r", str(FPS), "-c:v", "libx264", "-crf", "17", "-an", out]
        subprocess.run(cmd, check=True)
    segs.append(out); n = m
with open(os.path.join(T, "concat.txt"), "w") as f:
    for s_ in segs: f.write(f"file '{s_}'\n")
BG = os.path.join(T, "bg.mp4")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(T, "concat.txt"), "-c", "copy", BG], check=True)

# ---- title card (B01..B04), mirrors the reference: white Arial, three centred lines from y=150
def wrap(txt, font, maxw):
    out, line = [], ""
    for w in txt.split():
        t = (line + " " + w).strip()
        if font.getlength(t) > maxw and line: out.append(line); line = w
        else: line = t
    if line: out.append(line)
    return out
f_t = ImageFont.truetype(ARIAL, 46); lines = wrap(TITLE, f_t, 560)
timg = Image.new("RGBA", (W, 60 * len(lines) + 20), (0, 0, 0, 0)); td = ImageDraw.Draw(timg); yy = 6
for ln in lines:
    x = (W - f_t.getlength(ln)) / 2
    td.text((x + 2, yy + 2), ln, font=f_t, fill=(0, 0, 0, 170)); td.text((x, yy), ln, font=f_t, fill="white"); yy += 56
TITLE_PNG = os.path.join(T, "title.png"); timg.save(TITLE_PNG)

# ---- caption cards: sentence -> phrase -> card, <=2.9s, word-synced off the alignment, from CAP_FROM on
words = []; cur = ""; st = None; pe = None
for ch, s, e in zip(chars, cs, ce):
    if ch.isspace():
        if cur: words.append([cur, st, pe]); cur = ""
    else:
        if not cur: st = s
        cur += ch; pe = e
if cur: words.append([cur, st, pe])
for wd in words:
    core = wd[0].strip(".,?!"); tail = wd[0][len(core):]
    if core in RESPELL: wd[0] = RESPELL[core] + tail
words = [w for w in words if w[1] >= CAP_FROM - 0.05]
cards = []; buf = []
def flush():
    global buf
    if buf: cards.append((" ".join(w for w, _, _ in buf), buf[0][1], buf[-1][2])); buf = []
for wd in words:
    buf.append(wd); dur = buf[-1][2] - buf[0][1]
    ends_sentence = wd[0].endswith((".", "?", "!")); ends_phrase = wd[0].endswith(",")
    if ends_sentence or (ends_phrase and len(buf) >= 4) or len(buf) >= 6 or dur >= 2.9: flush()
flush()
merged = []
for c in cards:
    if merged and len(c[0].split()) <= 2 and not merged[-1][0].endswith((".", "?", "!")) and (c[2] - merged[-1][1]) <= 3.4:
        pt, ps, _ = merged[-1]; merged[-1] = (pt + " " + c[0], ps, c[2])
    else: merged.append(c)
cards = merged
font = ImageFont.truetype(ARIAL_B, CAP_SIZE)
def wrap2(txt, maxw=940):
    out = wrap(txt, font, maxw)
    return out[:2] if len(out) <= 2 else [" ".join(out[:-1]), out[-1]]
SCRIM_FROM = next(b["in"] for b in BEATS if b["beat"] == "B10")
overlays = []
for i, (txt, s, e) in enumerate(cards):
    lns = wrap2(txt); lh = CAP_SIZE + 14
    img = Image.new("RGBA", (W, lh * len(lns) + 30), (0, 0, 0, 0)); dr = ImageDraw.Draw(img); y = 15
    if s >= SCRIM_FROM:
        mw = int(max(font.getlength(ln) for ln in lns)) + 80
        scrim = Image.new("RGBA", img.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(scrim)
        sd.rounded_rectangle(((W - mw) // 2, 4, (W + mw) // 2, img.height - 4), radius=22, fill=(0, 0, 0, 150))
        img = Image.alpha_composite(img, scrim.filter(ImageFilter.GaussianBlur(6))); dr = ImageDraw.Draw(img)
    for ln in lns:
        x = (W - font.getlength(ln)) / 2
        dr.text((x + 3, y + 3), ln, font=font, fill=(0, 0, 0, 140))
        dr.text((x, y), ln, font=font, fill="white", stroke_width=3, stroke_fill=(20, 20, 20, 230)); y += lh
    p = os.path.join(T, f"cap{i:02d}.png"); img.save(p)
    nxt = cards[i + 1][1] if i + 1 < len(cards) else VO_END + 1
    overlays.append((p, CAP_Y_BOTTOM - img.height, s, min(e + 0.12, nxt - 0.02)))
json.dump([{"text": t, "in": round(s, 2), "out": round(e, 2)} for t, s, e in cards], open(os.path.join(ROOT, "_build", "caption-cards.json"), "w"), indent=1)

VO_N = os.path.join(T, "vo_-14.m4a")
if not os.path.exists(VO_N):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", VO, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11,volume=0.8dB", "-c:a", "aac", "-b:a", "192k", VO_N], check=True)

def sample_green(render):
    p = os.path.join(T, "g.png"); subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "1", "-i", render, "-frames:v", "1", p], check=True)
    a = np.asarray(Image.open(p).convert("RGB")); corner = np.concatenate([a[:60, :60].reshape(-1, 3), a[:60, -60:].reshape(-1, 3)])
    r, g, b = np.median(corner, 0).astype(int); return f"0x{r:02X}{g:02X}{b:02X}"
def measure(render, green, times=(3, 20, 40)):
    out = []
    for t in times:
        p = os.path.join(T, f"k{t}.png")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", render, "-frames:v", "1", "-vf", f"chromakey={green}:0.08:0.03,format=rgba", p], check=True)
        a = np.asarray(Image.open(p).convert("RGBA"))[:, :, 3] > 128
        ys, xs = np.where(a); top = int(ys.min()); band = a[top:top + int(0.11 * (int(ys.max()) - top))]
        hx = np.where(band.any(0))[0]; out.append((top, int(hx.min()), int(hx.max())))
    top = int(np.mean([o[0] for o in out])); hl = int(np.mean([o[1] for o in out])); hr = int(np.mean([o[2] for o in out]))
    return {"plate_w": a.shape[1], "plate_h": a.shape[0], "head_top": top, "head_w": hr - hl, "head_cx": (hl + hr) // 2}
def solve(m):
    s = (HEAD_W_FRAC * W) / m["head_w"]; sw, sh = int(round(m["plate_w"] * s)), int(round(m["plate_h"] * s))
    y = HEAD_TOP_Y - int(m["head_top"] * s); y = max(y, H + BOTTOM_BLEED - sh)          # body always past the bottom edge
    xL = min(-SIDE_BLEED, int(0.20 * W - m["head_cx"] * s)); xR = max(W + SIDE_BLEED - sw, int(0.80 * W - m["head_cx"] * s))
    return sw, sh, xL, xR, y, m["head_top"] * s + y

def build(creator):
    out = os.path.join(ROOT, "final", f"VEL-VIV-JUDGE-01-{creator}-{TAKE}.mp4")
    inputs = ["-i", BG]; fc = []; last = "0:v"; base = 1
    if creator != "bed":
        render = os.path.join(ROOT, "creator", "renders", f"{creator}-heygen-green-{TAKE}.mp4")
        green = sample_green(render); m = measure(render, green); sw, sh, xL, xR, y, head_top = solve(m)
        print(f"{creator}: green {green}, head_w {m['head_w']} -> {sw}x{sh} at xL={xL} xR={xR} y={y}, head top y={head_top:.0f}")
        json.dump({"green": green, **m, "scale_w": sw, "scale_h": sh, "xL": xL, "xR": xR, "y": y, "head_top_y": head_top}, open(os.path.join(ROOT, "_build", f"pip-{creator}.json"), "w"), indent=1)
        inputs += ["-i", render]; base = 2
        xexpr = "+".join([f"if(between(t,{a:.3f},{b:.3f}),{xR - xL},0)" for a, b in RIGHT_BEATS]) or "0"
        fc.append(f"[1:v]chromakey={green}:{KEY_SIM}:{KEY_BLEND},despill=type=green:mix={DESPILL},scale={sw}:{sh}[pip]")
        fc.append(f"[0:v][pip]overlay=x='{xL}+({xexpr})':y={y}:eof_action=pass[v0]"); last = "v0"
    inputs += ["-loop", "1", "-i", TITLE_PNG]
    fc.append(f"[{last}][{base}:v]overlay=0:150:enable='between(t,0,{TITLE_UNTIL:.3f})'[vt]"); last = "vt"; base += 1
    for p, _, _, _ in overlays: inputs += ["-loop", "1", "-i", p]
    for k, (_, oy, s, e) in enumerate(overlays):
        fc.append(f"[{last}][{k+base}:v]overlay=0:{oy}:enable='between(t,{s:.3f},{e:.3f})'[c{k}]"); last = f"c{k}"
    cmd = ["ffmpeg", "-v", "error", "-y"] + inputs + ["-i", VO_N, "-filter_complex", ";".join(fc), "-map", f"[{last}]", "-map", f"{len(overlays)+base}:a",
           "-t", f"{VO_END+0.4:.3f}", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True); print("built", out)

for c in (sys.argv[1:] or ["bed"]): build(c)
