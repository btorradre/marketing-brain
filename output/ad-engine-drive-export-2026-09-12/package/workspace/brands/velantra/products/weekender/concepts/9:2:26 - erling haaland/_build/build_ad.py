"""Composite VEL-WEEKENDER-HAALAND-01 (Nuamore celebrity-greenscreen mirror).

One shared VO, beats cut on the ElevenLabs character alignment, Haaland plates + our product
frames as HARD CUTS (the reference holds its paparazzi stills static), a keyed HeyGen creator
bottom-left CUT BY THE FRAME EDGE (sized on his head, never on the plate), small two-line captions
across his chest like the reference, live PDP recording under the close.

  python3 build_ad.py bed              # background + captions + VO only (board preview)
  python3 build_ad.py C1 [C2 C3]       # full cut per creator (needs casting/renders/<C>-heygen-green.mp4)
  VOICE=mens-kerim python3 build_ad.py C1
"""
import json, os, re, subprocess, sys, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = os.path.join(ROOT, "_build", "tmp"); os.makedirs(T, exist_ok=True)
VOICE = os.environ.get("VOICE", "mens-chill")
VO = os.path.join(ROOT, "voice", f"VO-{VOICE}.mp3")
ALIGN = json.load(open(os.path.join(ROOT, "voice", f"VO-{VOICE}.alignment.json")))
W, H, FPS = 1080, 1920, 30
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
CAP_SIZE = 46            # reference captions are small
CAP_Y = 1620             # caption band centre, across the creator's chest like the reference (1500 crossed his mouth)
# house PiP geometry (feedback_greenscreen_pip_edge_cut): head ~0.20 W, head centre 0.16 W in from the edge,
# body runs 60px past the bottom edge so the frame cuts him
HEAD_W_FRAC, HEAD_CX_FRAC, BOTTOM_BLEED = 0.20, 0.16, 60

BEATS = [  # (anchor phrase in the spoken script, asset relative to ROOT)
    ("Okay so", "plates/P1-lounge-jet.jpg"),
    ("Airport", "plates/P2-tarmac-orange.jpg"),
    ("Training", "plates/P3-training-black.jpg"),
    ("Off duty", "plates/P4-garden-khaki.jpg"),
    ("Same shape", "plates/P5-trophy-room.jpg"),
    ("And I'm like", "plates/P1-lounge-jet-tight.jpg"),
    ("Turns out", "product-broll/B7-gate-held-up.png"),
    ("And honestly", "product-broll/B1-fullbody-hotel-scale.png"),
    ("It's structured", "product-broll/R1-real-closed-LC.jpg"),
    ("it doesn't collapse", "product-broll/B3-hotel-on-carryon-handle.png"),
    ("and it looks like", "product-broll/B4-macro-hardware-hand.png"),
    ("Italian leather", "product-broll/R2-real-hand-scale.jpg"),
    ("Fits a full weekend", "product-broll/B5-open-packed-bed.png"),
    ("Holds its shape", "product-broll/B6-overhead-bin.png"),
    ("or in the back", "product-broll/B8-cab/pick.png"),
    ("Right now", "product-broll/B9-real-screenrec-1080x1920.mp4"),
]
# Brooks 9/02: the close is his REAL iPhone screen recording (PDP -> add to cart -> cart drawer -> checkout),
# 6.3s usable before the control centre appears. It plays from 0 and is slowed to fill the beat.
PDP_BUYBOX_T = 18.9   # only used for the old headless PDP capture (B9-pdp-scroll.mp4)

# ---- words + times from the character alignment
chars, cs, ce = ALIGN["characters"], ALIGN["character_start_times_seconds"], ALIGN["character_end_times_seconds"]
text = "".join(chars)
words = [{"w": m.group(), "s": cs[m.start()], "e": ce[m.end() - 1]} for m in re.finditer(r"\S+", text)
         if not re.fullmatch(r"\[[^\]]+\]", m.group())]   # drop v3 audio tags like [casual] from the word list
VO_END = ce[-1]
def t_of(phrase):
    i = text.find(phrase)
    if i < 0: i = text.lower().find(phrase.lower())
    assert i >= 0, f"anchor not found: {phrase}"
    return cs[i]
starts = [t_of(p) for p, _ in BEATS]; starts[0] = 0.0
ends = starts[1:] + [VO_END + 0.5]
print("beats:", [(round(s, 2), os.path.basename(a)) for s, (_, a) in zip(starts, BEATS)])

# tight second crop of the lounge plate for the "And I'm like" return (reference re-uses Hailey)
tight = os.path.join(ROOT, "plates", "P1-lounge-jet-tight.jpg")
if not os.path.exists(tight):
    im = Image.open(os.path.join(ROOT, "plates", "P1-lounge-jet.jpg"))
    im.crop((60, 380, 60 + 900, 380 + 1600)).resize((W, H), Image.LANCZOS).save(tight, quality=92)

def fill_9x16(src, dst):
    """scale to cover 1080x1920 then centre-crop (never stretch)"""
    im = Image.open(src).convert("RGB"); w, h = im.size; s = max(W / w, H / h)
    im = im.resize((round(w * s), round(h * s)), Image.LANCZOS); w2, h2 = im.size
    im.crop(((w2 - W) // 2, (h2 - H) // 2, (w2 - W) // 2 + W, (h2 - H) // 2 + H)).save(dst, quality=94)

# ---- background track: hard cuts
segs = []
for n, ((_, asset), s, e) in enumerate(zip(BEATS, starts, ends)):
    d = max(e - s, 0.2); out = os.path.join(T, f"{VOICE}-seg{n:02d}.mp4"); src = os.path.join(ROOT, asset)
    if not os.path.exists(out):
        if "screenrec" in asset:
            src_d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src],
                                         capture_output=True, text=True).stdout.strip())
            factor = max(d / src_d, 1.0)   # slow the recording (never speed it) so it ends on the checkout frame
            cmd = ["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", f"setpts={factor:.4f}*PTS,scale={W}:{H},format=yuv420p",
                   "-t", f"{d:.3f}", "-r", str(FPS), "-c:v", "libx264", "-crf", "17", "-an", out]
        elif asset.endswith(".mp4"):
            pdp_start = max(0.0, PDP_BUYBOX_T - d)
            cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{pdp_start:.3f}", "-t", f"{d:.3f}", "-i", src,
                   "-vf", f"scale={W}:{H},format=yuv420p", "-r", str(FPS), "-c:v", "libx264", "-crf", "17", "-an", out]
        else:
            still = os.path.join(T, f"fill{n:02d}.jpg"); fill_9x16(src, still)
            cmd = ["ffmpeg", "-v", "error", "-y", "-loop", "1", "-t", f"{d:.3f}", "-i", still,
                   "-vf", "format=yuv420p", "-r", str(FPS), "-c:v", "libx264", "-crf", "17", "-an", out]
        subprocess.run(cmd, check=True)
    segs.append(out)
with open(os.path.join(T, f"{VOICE}-concat.txt"), "w") as f:
    for s in segs: f.write(f"file '{s}'\n")
BG = os.path.join(T, f"{VOICE}-bg.mp4")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(T, f"{VOICE}-concat.txt"), "-c", "copy", BG], check=True)

# ---- caption cards: reference style = small, white, soft dark stroke, 1-2 lines, sentence fragments
CHUNKS = ["Okay so, I kept seeing Haaland", "carry this bag everywhere", "Airport.", "Training.", "Off duty.",
          "Same shape, every time", "And I'm like, why is one of", "the best footballers in the world",
          "carrying a Birkin?", "Turns out the answer's pretty obvious", "It's the Velantra Weekender",
          "And honestly, I get it now", "It's structured, it doesn't collapse", "and it looks like it costs",
          "three times what it does", "Italian leather.", "Fits a full weekend.", "Holds its shape whether",
          "you're on a flight", "or in the back of a cab", "Right now it's sold out", "almost everywhere,",
          "and this is the first batch", "I've actually seen available", "I've left the link below"]
cards, wi = [], 0
for ch in CHUNKS:
    n = len(ch.split()); grp = words[wi:wi + n]; wi += n; cards.append((ch, grp))
assert wi == len(words), f"chunk/word mismatch: {wi} vs {len(words)}"
font = ImageFont.truetype(FONT, CAP_SIZE)
def render_card(txt, idx):
    txt = re.sub(r"Vell[- ]?Ahn[- ]?Trah|Vel Lantra|Velentra", "Velantra", txt.strip(), flags=re.I)
    lines, line = [], ""
    for tok in txt.split():
        trial = (line + " " + tok).strip()
        if font.getlength(trial) > 620 and line: lines.append(line); line = tok
        else: line = trial
    if line: lines.append(line)
    img = Image.new("RGBA", (W, 160), (0, 0, 0, 0)); dr = ImageDraw.Draw(img); lh = CAP_SIZE + 10
    y = 80 - (len(lines) * lh) / 2
    for ln in lines:
        x = (W - font.getlength(ln)) / 2
        dr.text((x + 2, y + 2), ln, font=font, fill=(0, 0, 0, 140))
        dr.text((x, y), ln, font=font, fill="white", stroke_width=3, stroke_fill=(25, 25, 25, 230)); y += lh
    p = os.path.join(T, f"cap{idx:03d}.png"); img.save(p); return p
cap_files = []
for i, (txt, ws) in enumerate(cards):
    s = ws[0]["s"]; e = ws[-1]["e"]
    nxt = cards[i + 1][1][0]["s"] if i + 1 < len(cards) else VO_END + 0.5
    e = min(e + 0.15, nxt - 0.02)
    cap_files.append((render_card(txt, i), s, e))

VO_N = os.path.join(T, f"{VOICE}-vo_-14.m4a")
if not os.path.exists(VO_N):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", VO, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11,volume=1.6dB", "-c:a", "aac", "-b:a", "192k", VO_N], check=True)

# ---- creator PiP geometry, measured off the keyed plate's own alpha
def sample_green(render):
    p = os.path.join(T, "g.png")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "1", "-i", render, "-frames:v", "1", p], check=True)
    a = np.asarray(Image.open(p).convert("RGB")); corner = np.concatenate([a[:60, :60].reshape(-1, 3), a[:60, -60:].reshape(-1, 3)])
    r, g, b = np.median(corner, 0).astype(int); return f"0x{r:02X}{g:02X}{b:02X}"
def measure(render, green, times=(3, 15, 27)):
    out = []
    for t in times:
        p = os.path.join(T, f"k{t}.png")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", render, "-frames:v", "1",
                        "-vf", f"chromakey={green}:0.08:0.03,format=rgba", p], check=True)
        a = np.asarray(Image.open(p).convert("RGBA"))[:, :, 3] > 128
        ys, xs = np.where(a); top = int(ys.min()); band = a[top:top + int(0.11 * (int(ys.max()) - top))]
        hx = np.where(band.any(0))[0]; out.append((top, int(hx.min()), int(hx.max())))
    top = int(np.mean([o[0] for o in out])); hl = int(np.mean([o[1] for o in out])); hr = int(np.mean([o[2] for o in out]))
    return {"plate_w": a.shape[1], "plate_h": a.shape[0], "head_top": top, "head_w": hr - hl, "head_cx": (hl + hr) // 2}
def solve(m):
    s = (HEAD_W_FRAC * W) / m["head_w"]; sw, sh = int(round(m["plate_w"] * s)), int(round(m["plate_h"] * s))
    y = H + BOTTOM_BLEED - sh; x = int(round(HEAD_CX_FRAC * W - m["head_cx"] * s))
    return sw, sh, x, y, m["head_top"] * s + y

def build(creator):
    out = os.path.join(ROOT, "final", f"VEL-WEEKENDER-HAALAND-01-{creator}-{VOICE}.mp4")
    inputs = ["-i", BG]; fc = []; last = "0:v"; base = 1
    if creator != "bed":
        render = os.path.join(ROOT, "casting", "renders", f"{creator}-heygen-green.mp4")
        green = sample_green(render); m = measure(render, green); sw, sh, x, y, head_top = solve(m)
        print(f"{creator}: green {green}, head_w {m['head_w']} -> scaled {sw}x{sh} at x={x} y={y}, head top y={head_top:.0f}")
        inputs += ["-i", render]; base = 2
        fc.append(f"[1:v]chromakey={green}:0.08:0.03,despill=type=green:mix=0.15,scale={sw}:{sh}[pip]")
        fc.append(f"[0:v][pip]overlay=x={x}:y={y}:eof_action=pass[v0]"); last = "v0"
    for p, _, _ in cap_files: inputs += ["-loop", "1", "-i", p]
    for k, (_, s, e) in enumerate(cap_files):
        fc.append(f"[{last}][{k+base}:v]overlay=0:{CAP_Y-80}:enable='between(t,{s:.3f},{e:.3f})'[c{k}]"); last = f"c{k}"
    cmd = ["ffmpeg", "-v", "error", "-y"] + inputs + ["-i", VO_N, "-filter_complex", ";".join(fc),
           "-map", f"[{last}]", "-map", f"{len(cap_files)+base}:a", "-t", f"{VO_END+0.5:.3f}",
           "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True); print("built", out)

for c in (sys.argv[1:] or ["bed"]): build(c)
