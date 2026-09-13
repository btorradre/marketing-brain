#!/usr/bin/env python3
"""Assemble the Euro-fall-trip greenscreen ad (product from the path). Port of OLDMONEY-GRID-01's build_ad.py with the
reference's grammar: hard-cut stills off beat-map.json, live PDP recording spanning the close, creator KEYED off the HeyGen
green plate (house greenscreen: head 0.20 W, body cut by the bottom and side edges, bottom-left then bottom-right at the London chapter),
word-synced captions centred above her head.

  python3 build_ad.py bed        # no creator
  python3 build_ad.py C2         # needs creator/renders/C2-heygen-green.mp4
  KEY_SIM=0.12 KEY_BLEND=0.05 DESPILL=0.15 python3 build_ad.py C2
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); PRODUCT = ROOT.split("/products/")[1].split("/")[0]
CID = {"vivienne": "VEL-VIV-EUROFALL-01", "weekender": "VEL-WEEKENDER-EUROFALL-01", "margot": "VEL-MER-EUROFALL-01"}[PRODUCT]
PDP = {"vivienne": "PDP-scroll-viv-0902.mp4", "weekender": "PDP-scroll-wk-0902.mp4", "margot": "PDP-scroll-mer-0902.mp4"}[PRODUCT]
T = os.path.join(ROOT, "_build", "tmp"); os.makedirs(T, exist_ok=True); os.makedirs(os.path.join(ROOT, "final"), exist_ok=True)
VO = os.path.join(ROOT, "vo", "VO-woman-over-40-A.mp3"); ALIGN = json.load(open(os.path.join(ROOT, "vo", "VO-woman-over-40-A.alignment.json")))
BEATS = json.load(open(os.path.join(ROOT, "beat-map.json")))
W, H, FPS = 1080, 1920, 30
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"; CAP_SIZE, CAP_Y_BOTTOM = 54, 1180
HEAD_W_FRAC, BOTTOM_BLEED, SIDE_BLEED = 0.20, 60, 70   # house greenscreen geometry: size on the HEAD, body runs past the bottom and the near side edge
PIP_W, PIP_H, PIP_R, MARGIN = 372, 500, 30, 44
RESPELL = {"Vivian": "Vivienne", "Vehlantra": "Velantra"}
KEY_SIM, KEY_BLEND, DESPILL = float(os.environ.get("KEY_SIM", "0.12")), float(os.environ.get("KEY_BLEND", "0.05")), float(os.environ.get("DESPILL", "0.15"))

chars, cs, ce = ALIGN["characters"], ALIGN["character_start_times_seconds"], ALIGN["character_end_times_seconds"]
text = "".join(chars); VO_END = ce[-1]; END = VO_END + 0.4

# ---- bed: hard cuts; PDP recording spans from the pdp beat to the end
segs = []; n = 0
while n < len(BEATS):
    b = BEATS[n]; s = b["in"]
    if b["kind"] == "pdp":
        d = END - s; out = os.path.join(T, f"seg{n:02d}.mp4"); src = os.path.join(ROOT, "_build", PDP)
        if not os.path.exists(out):
            src_d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src], capture_output=True, text=True).stdout.strip())
            factor = max(d / src_d, 1.0)   # slow to fill, never speed up; trim if longer
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", f"setpts={factor:.4f}*PTS,scale={W}:{H},format=yuv420p", "-t", f"{d:.3f}", "-r", str(FPS), "-c:v", "libx264", "-crf", "17", "-an", out], check=True)
        segs.append(out); break
    e = b["out"]; d = max(e - s, 0.2); out = os.path.join(T, f"seg{n:02d}.mp4")
    if not os.path.exists(out):
        im = Image.open(os.path.join(ROOT, "board-frames", b["frame"])).convert("RGB"); w, h = im.size; sc = max(W / w, H / h)
        im = im.resize((round(w * sc), round(h * sc)), Image.LANCZOS); w2, h2 = im.size
        still = os.path.join(T, f"fill{n:02d}.jpg"); im.crop(((w2 - W) // 2, (h2 - H) // 2, (w2 - W) // 2 + W, (h2 - H) // 2 + H)).save(still, quality=94)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-t", f"{d:.3f}", "-i", still, "-vf", "format=yuv420p", "-r", str(FPS), "-c:v", "libx264", "-crf", "17", "-an", out], check=True)
    segs.append(out); n += 1
with open(os.path.join(T, "concat.txt"), "w") as f:
    for s_ in segs: f.write(f"file '{s_}'\n")
BG = os.path.join(T, "bg.mp4"); subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(T, "concat.txt"), "-c", "copy", BG], check=True)
PDP_FROM = next(b["in"] for b in BEATS if b["kind"] == "pdp")

# ---- captions: word-synced cards, bottom-centre like the reference, scrim over the PDP page
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
cards = []; buf = []
def flush():
    global buf
    if buf: cards.append((" ".join(w for w, _, _ in buf), buf[0][1], buf[-1][2])); buf = []
for wd in words:
    buf.append(wd); dur = buf[-1][2] - buf[0][1]
    if wd[0].endswith((".", "?", "!")) or (wd[0].endswith(",") and len(buf) >= 4) or len(buf) >= 6 or dur >= 2.9: flush()
flush()
merged = []
for c in cards:
    if merged and len(c[0].split()) <= 2 and not merged[-1][0].endswith((".", "?", "!")) and (c[2] - merged[-1][1]) <= 3.4:
        pt, ps, _ = merged[-1]; merged[-1] = (pt + " " + c[0], ps, c[2])
    else: merged.append(c)
cards = merged; font = ImageFont.truetype(FONT, CAP_SIZE)
def wrap(txt, maxw=940):
    out, line = [], ""
    for w in txt.split():
        t = (line + " " + w).strip()
        if font.getlength(t) > maxw and line: out.append(line); line = w
        else: line = t
    if line: out.append(line)
    return out[:2] if len(out) <= 2 else [" ".join(out[:-1]), out[-1]]
overlays = []
for i, (txt, s, e) in enumerate(cards):
    lines = wrap(txt); lh = CAP_SIZE + 14
    img = Image.new("RGBA", (W, lh * len(lines) + 30), (0, 0, 0, 0)); dr = ImageDraw.Draw(img); y = 15
    if s >= PDP_FROM - 0.2:
        mw = int(max(font.getlength(ln) for ln in lines)) + 80
        scrim = Image.new("RGBA", img.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(scrim)
        sd.rounded_rectangle(((W - mw) // 2, 4, (W + mw) // 2, img.height - 4), radius=22, fill=(0, 0, 0, 150))
        img = Image.alpha_composite(img, scrim.filter(ImageFilter.GaussianBlur(6))); dr = ImageDraw.Draw(img)
    for ln in lines:
        x = (W - font.getlength(ln)) / 2
        dr.text((x + 3, y + 3), ln, font=font, fill=(0, 0, 0, 140))
        dr.text((x, y), ln, font=font, fill="white", stroke_width=3, stroke_fill=(20, 20, 20, 230)); y += lh
    p = os.path.join(T, f"cap{i:02d}.png"); img.save(p)
    nxt = cards[i + 1][1] if i + 1 < len(cards) else VO_END + 1
    overlays.append((p, CAP_Y_BOTTOM - img.height, s, min(e + 0.12, nxt - 0.02)))
json.dump([{"text": t, "in": round(s, 2), "out": round(e, 2)} for t, s, e in cards], open(os.path.join(ROOT, "_build", "caption-cards.json"), "w"), indent=1)

VO_N = os.path.join(T, "vo_-14.m4a")
if not os.path.exists(VO_N):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", VO, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11,volume=1.4dB,alimiter=limit=0.84:attack=5:release=60:level=false", "-c:a", "aac", "-b:a", "192k", VO_N], check=True)

# ---- keyed creator (house greenscreen): bottom-LEFT cut by the bottom and left edges, jumps to bottom-RIGHT at the London chapter (~3/4)
def chapter_start(prefix):
    return next(b["in"] for b in BEATS if b["line"].lower().startswith(prefix))
sched = [(0.0, "left"), (chapter_start("london"), "right")]

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
def solve(m, side):
    s = (HEAD_W_FRAC * W) / m["head_w"]; sw, sh = int(round(m["plate_w"] * s)), int(round(m["plate_h"] * s))
    y = H + BOTTOM_BLEED - sh; head_top = m["head_top"] * s + y
    # plate edge past the near frame edge by SIDE_BLEED; the head lands wherever the plate framing puts it
    x = -SIDE_BLEED if side == "left" else W + SIDE_BLEED - sw
    return sw, sh, x, y, head_top

def build(creator):
    out = os.path.join(ROOT, "final", f"{CID}-{creator}-A.mp4")
    inputs = ["-i", BG]; fc = []; last = "0:v"; base = 1
    if creator != "bed":
        render = os.path.join(ROOT, "creator", "renders", f"{creator}-heygen-green.mp4"); green = sample_green(render); m = measure(render, green)
        inputs += ["-i", render]; base = 2; geo = {}
        fc.append(f"[1:v]chromakey={green}:{KEY_SIM}:{KEY_BLEND},despill=type=green:mix={DESPILL},format=rgba[cre]"); fc.append(f"[cre]split={len(sched)}" + "".join(f"[p{k}]" for k in range(len(sched))))
        for k, (t0, side) in enumerate(sched):
            sw, sh, x, y, head_top = solve(m, side); geo[side] = {"scale": [sw, sh], "x": x, "y": y, "head_top_y": round(head_top)}
            t1 = sched[k + 1][0] if k + 1 < len(sched) else END + 1
            fc.append(f"[p{k}]scale={sw}:{sh}[q{k}]"); fc.append(f"[{last}][q{k}]overlay=x={x}:y={y}:enable='between(t,{t0:.3f},{t1:.3f})':eof_action=pass[v{k}]"); last = f"v{k}"
        print(f"{creator}: green {green}, head_w {m['head_w']}px on the plate, geometry {geo}")
        json.dump({"green": green, **m, "geometry": geo, "schedule": sched, "key": [KEY_SIM, KEY_BLEND, DESPILL]}, open(os.path.join(ROOT, "_build", f"pip-{creator}.json"), "w"), indent=1)
    for p, _, _, _ in overlays: inputs += ["-loop", "1", "-i", p]
    for k, (_, oy, s, e) in enumerate(overlays):
        fc.append(f"[{last}][{k+base}:v]overlay=0:{oy}:enable='between(t,{s:.3f},{e:.3f})'[c{k}]"); last = f"c{k}"
    cmd = ["ffmpeg", "-v", "error", "-y"] + inputs + ["-i", VO_N, "-filter_complex", ";".join(fc), "-map", f"[{last}]", "-map", f"{len(overlays)+base}:a",
           "-t", f"{END:.3f}", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True); print("built", out)

for c in (sys.argv[1:] or ["bed"]): build(c)
