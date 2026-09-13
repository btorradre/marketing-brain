"""Composite VEL-WEEKENDER-INVEST-01 (Poke "10/10 male purchases" listicle mirror).

Mirrors the reference: a 2x2 photo GRID hook with a big centred title, then one still per beat
with a short lower-third LABEL (not word-synced captions), hard cuts, creator keyed over the
middle-bottom of the frame and cut by the bottom edge. One VO (gringo clone).

  python3 build_ad.py bed                 # no creator (board preview)
  python3 build_ad.py C1                  # needs casting/renders/C1-heygen-green.mp4 (this concept's own render)
  VOICE=gringo-B GRID=GRID-B-product python3 build_ad.py C1
"""
import json, os, re, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = os.path.join(ROOT, "_build", "tmp"); os.makedirs(T, exist_ok=True)
VOICE = os.environ.get("VOICE", "gringo-A"); GRID = os.environ.get("GRID", "GRID-A-travel")
VO = os.path.join(ROOT, "voice", f"VO-{VOICE}.mp3")
ALIGN = json.load(open(os.path.join(ROOT, "voice", f"VO-{VOICE}.alignment.json")))
W, H, FPS = 1080, 1920, 30
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
LABEL_SIZE, LABEL_Y = 50, 1640          # lower-third label like the reference, across the creator's chest
TITLE_SIZE, TITLE_Y = 78, 640           # hook title, centred, like "10/10 Male Purchases"
HEAD_W_FRAC, HEAD_CX_FRAC, BOTTOM_BLEED = 0.20, 0.50, 60   # creator CENTRED like the reference, cut by the bottom edge

# (anchor phrase, asset, label) — label None = keep previous
BEATS = [
    ("The one purchase", f"plates/{GRID}.jpg", "TITLE"),
    ("A weekend bag", "product-broll/R1-real-closed-LC.jpg", "a weekend bag that holds its shape"),
    ("This is the", "product-broll/B7-gate-held-up.png", "the Velantra Weekender"),
    ("Full grain", "product-broll/B4-macro-hardware-hand.png", "full grain leather over woven canvas"),
    ("no logo", "product-broll/R2-real-hand-scale.jpg", "no logo on it"),
    ("and it stands up", "product-broll/B3-hotel-on-carryon-handle.png", "stands up on its own"),
    ("packed or empty", "product-broll/R3-real-open-interior.jpg", "packed or empty"),
    ("I've dragged", "product-broll/B2-terminal-on-carryon.png", "three airports, still looks new"),
    ("Three days", "product-broll/B5-open-packed-bed.png", "three days of clothes"),
    ("laptop in", "product-broll/B10-laptop-slip-pocket.png", "laptop in the slip pocket"),
    ("straight into", "product-broll/B6-overhead-bin.png", "straight into the overhead bin"),
    ("Four colors", "product-broll/B9-real-screenrec-1080x1920.mp4", "four colors, on sale now"),
    ("I left the link", None, "link below"),
]
TITLE_LINES = ["The one purchase", "every guy should make"]

chars, cs, ce = ALIGN["characters"], ALIGN["character_start_times_seconds"], ALIGN["character_end_times_seconds"]
text = "".join(chars); VO_END = ce[-1]
def t_of(phrase):
    i = text.find(phrase)
    if i < 0: i = text.lower().find(phrase.lower())
    assert i >= 0, f"anchor not found: {phrase}"
    return cs[i]
starts = [t_of(p) for p, _, _ in BEATS]; starts[0] = 0.0
ends = starts[1:] + [VO_END + 0.5]
print("beats:", [(round(s, 2), os.path.basename(a) if a else "-") for s, (_, a, _) in zip(starts, BEATS)])

def fill_9x16(src, dst):
    im = Image.open(src).convert("RGB"); w, h = im.size; s = max(W / w, H / h)
    im = im.resize((round(w * s), round(h * s)), Image.LANCZOS); w2, h2 = im.size
    im.crop(((w2 - W) // 2, (h2 - H) // 2, (w2 - W) // 2 + W, (h2 - H) // 2 + H)).save(dst, quality=94)

# ---- background: hard cuts; the screen recording spans its beat plus every following beat with asset None
segs = []; n = 0
while n < len(BEATS):
    _, asset, _ = BEATS[n]; s = starts[n]; m = n + 1
    while m < len(BEATS) and BEATS[m][1] is None: m += 1
    e = ends[m - 1]; d = max(e - s, 0.2); out = os.path.join(T, f"{VOICE}-{GRID}-seg{n:02d}.mp4"); src = os.path.join(ROOT, asset)
    if not os.path.exists(out):
        if asset.endswith(".mp4"):
            src_d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src], capture_output=True, text=True).stdout.strip())
            factor = max(d / src_d, 1.0)
            cmd = ["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", f"setpts={factor:.4f}*PTS,scale={W}:{H},format=yuv420p", "-t", f"{d:.3f}", "-r", str(FPS), "-c:v", "libx264", "-crf", "17", "-an", out]
        else:
            still = os.path.join(T, f"fill-{GRID}-{n:02d}.jpg"); fill_9x16(src, still)
            cmd = ["ffmpeg", "-v", "error", "-y", "-loop", "1", "-t", f"{d:.3f}", "-i", still, "-vf", "format=yuv420p", "-r", str(FPS), "-c:v", "libx264", "-crf", "17", "-an", out]
        subprocess.run(cmd, check=True)
    segs.append(out); n = m
with open(os.path.join(T, f"{VOICE}-concat.txt"), "w") as f:
    for s in segs: f.write(f"file '{s}'\n")
BG = os.path.join(T, f"{VOICE}-{GRID}-bg.mp4")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(T, f"{VOICE}-concat.txt"), "-c", "copy", BG], check=True)

# ---- text layers: hook title + per-beat labels (reference style: white sans, soft shadow, centred)
def render_text(lines, size, idx, tag):
    font = ImageFont.truetype(FONT, size); lh = size + 12
    img = Image.new("RGBA", (W, lh * len(lines) + 40), (0, 0, 0, 0)); dr = ImageDraw.Draw(img); y = 20
    for ln in lines:
        x = (W - font.getlength(ln)) / 2
        dr.text((x + 3, y + 3), ln, font=font, fill=(0, 0, 0, 150))
        dr.text((x, y), ln, font=font, fill="white", stroke_width=3, stroke_fill=(20, 20, 20, 220)); y += lh
    p = os.path.join(T, f"{tag}{idx:02d}.png"); img.save(p); return p, img.height
overlays = []   # (png, y, start, end)
for i, ((_, _, label), s, e) in enumerate(zip(BEATS, starts, ends)):
    if label == "TITLE":
        p, h = render_text(TITLE_LINES, TITLE_SIZE, i, "title"); overlays.append((p, TITLE_Y - h // 2, s, e - 0.02))
    elif label:
        p, h = render_text([label], LABEL_SIZE, i, "label"); overlays.append((p, LABEL_Y - h // 2, s, e - 0.02))

VO_N = os.path.join(T, f"{VOICE}-vo_-14.m4a")
if not os.path.exists(VO_N):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", VO, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11,volume=1.1dB", "-c:a", "aac", "-b:a", "192k", VO_N], check=True)

def sample_green(render):
    p = os.path.join(T, "g.png"); subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "1", "-i", render, "-frames:v", "1", p], check=True)
    a = np.asarray(Image.open(p).convert("RGB")); corner = np.concatenate([a[:60, :60].reshape(-1, 3), a[:60, -60:].reshape(-1, 3)])
    r, g, b = np.median(corner, 0).astype(int); return f"0x{r:02X}{g:02X}{b:02X}"
def measure(render, green, times=(3, 14, 26)):
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
    return sw, sh, int(round(HEAD_CX_FRAC * W - m["head_cx"] * s)), H + BOTTOM_BLEED - sh, m["head_top"] * s + H + BOTTOM_BLEED - sh

def build(creator):
    out = os.path.join(ROOT, "final", f"VEL-WEEKENDER-INVEST-01-{creator}-{VOICE}-{GRID.split('-')[1]}.mp4")
    inputs = ["-i", BG]; fc = []; last = "0:v"; base = 1
    if creator != "bed":
        render = os.path.join(ROOT, "casting", "renders", f"{creator}-heygen-green.mp4")
        green = sample_green(render); m = measure(render, green); sw, sh, x, y, head_top = solve(m)
        print(f"{creator}: green {green}, head_w {m['head_w']} -> {sw}x{sh} at x={x} y={y}, head top y={head_top:.0f}")
        inputs += ["-i", render]; base = 2
        fc.append(f"[1:v]chromakey={green}:0.08:0.03,despill=type=green:mix=0.15,scale={sw}:{sh}[pip]")
        fc.append(f"[0:v][pip]overlay=x={x}:y={y}:eof_action=pass[v0]"); last = "v0"
    for p, _, _, _ in overlays: inputs += ["-loop", "1", "-i", p]
    for k, (_, oy, s, e) in enumerate(overlays):
        fc.append(f"[{last}][{k+base}:v]overlay=0:{oy}:enable='between(t,{s:.3f},{e:.3f})'[c{k}]"); last = f"c{k}"
    cmd = ["ffmpeg", "-v", "error", "-y"] + inputs + ["-i", VO_N, "-filter_complex", ";".join(fc), "-map", f"[{last}]", "-map", f"{len(overlays)+base}:a",
           "-t", f"{VO_END+0.5:.3f}", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True); print("built", out)

for c in (sys.argv[1:] or ["bed"]): build(c)
