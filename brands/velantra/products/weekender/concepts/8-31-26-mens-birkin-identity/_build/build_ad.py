"""Composite VEL-WEEKENDER-MENSID-01: one shared VO, 13 beats timed off the ElevenLabs alignment,
keyed HeyGen creator PiP, word-synced caption cards, real PDP recording on the close.
  python3 build_ad.py M1 [M2 M3]
Stills are HARD CUTS (no zoom). Motion beats swap to Omni clips after the kie top-up.
"""
import json, os, re, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = os.path.join(ROOT, "_build", "tmp"); os.makedirs(T, exist_ok=True)
VO = os.path.join(ROOT, "voice", "VO-teva-take1.mp3")
ALIGN = json.load(open(os.path.join(ROOT, "voice", "VO-teva-take1.alignment.json")))
W, H, FPS = 1080, 1920, 30
PIP_W = 389  # 36% of frame width
CAP_Y = 1010  # caption band centre (above the creator's head)
FONT = "/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf"
GREENS = {"M1": "0x35BB39", "M2": "0x159B20", "M3": "0x48D54B"}

BEATS = [  # (anchor phrase in the script, asset, kind)
    ("Everybody's seen him", "f01/F01-haaland-plate-1080x1920.jpg", "still"),
    ("This is the Eleanor", "keyframes/K02/v2.png", "still"),
    ("It's a Birkin", "keyframes/K03/v1.png", "still"),
    ("so it holds three days", "keyframes/K04/v1.png", "still"),
    ("Smooth leather over canvas", "keyframes/K05/v4.png", "still"),
    ("and no logo anywhere", "keyframes/K06/v3.png", "still"),
    ("The whole inside is caramel", "keyframes/K07/v1.png", "still"),
    ("For scale", "keyframes/K08/v2.png", "still"),
    ("It sits on top of my carry", "keyframes/K09/v1.png", "still"),
    ("it slides straight into the overhead", "keyframes/K10/v1.png", "still"),
    ("and my laptop and charger", "keyframes/K11/v1.png", "still"),
    ("It comes in four colors", "keyframes/K12/v6.png", "still"),
    ("They're running a sale", "f13/F13-pdp-scroll-1080x1920.mp4", "video"),
]

# ---- words + times from the character alignment
chars, cs, ce = ALIGN["characters"], ALIGN["character_start_times_seconds"], ALIGN["character_end_times_seconds"]
text = "".join(chars)
words = []
for m in re.finditer(r"\S+", text):
    words.append({"w": m.group(), "s": cs[m.start()], "e": ce[m.end() - 1], "i": m.start()})
VO_END = ce[-1]
def t_of(phrase):
    i = text.find(phrase)
    if i < 0:  # tolerate the TTS brand respelling / curly quotes
        i = text.lower().find(phrase.lower())
    assert i >= 0, f"anchor not found: {phrase}"
    return cs[i]
starts = [t_of(p) for p, _, _ in BEATS]
starts[0] = 0.0
ends = starts[1:] + [VO_END + 0.4]
print("beats:", [(round(s, 2), os.path.basename(a)) for s, (_, a, _) in zip(starts, BEATS)])
PIP_RIGHT_FROM = starts[9]   # creator jumps to bottom-right at the overhead-bin beat (~3/4)

# ---- background track: hard cuts
segs = []
for n, ((_, asset, kind), s, e) in enumerate(zip(BEATS, starts, ends)):
    d = max(e - s, 0.2); out = os.path.join(T, f"seg{n:02d}.mp4")
    if not os.path.exists(out):
        if kind == "still":
            cmd = ["ffmpeg", "-v", "error", "-y", "-loop", "1", "-t", f"{d:.3f}", "-i", os.path.join(ROOT, asset),
                   "-vf", f"scale={W}:{H}:flags=lanczos,format=yuv420p", "-r", str(FPS), "-c:v", "libx264", "-crf", "17", "-an", out]
        else:
            pdp_start = max(0.0, 18.9 - d)
            cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{pdp_start:.3f}", "-t", f"{d:.3f}", "-i", os.path.join(ROOT, asset),
                   "-vf", f"scale={W}:{H},format=yuv420p", "-r", str(FPS), "-c:v", "libx264", "-crf", "17", "-an", out]
        subprocess.run(cmd, check=True)
    segs.append(out)
with open(os.path.join(T, "concat.txt"), "w") as f:
    for s in segs: f.write(f"file '{s}'\n")
BG = os.path.join(T, "bg.mp4")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(T, "concat.txt"), "-c", "copy", BG], check=True)

# ---- caption cards: 3-6 words, break on punctuation, sentence case, no terminal punctuation
def display(w):
    w = re.sub(r"Vell[- ]?Ahn[- ]?Trah|Vel Lantra|Velentra", "Velantra", w, flags=re.I)
    return w
CHUNKS = [
 "Everybody's seen him with these bags", "This is the Eleanor Weekender from Velantra",
 "and it's about a hundred and sixty dollars", "It's a Birkin-inspired shape", "scaled up to travel size",
 "so it holds three days of clothes", "and still keeps its shape packed full", "Smooth leather over canvas",
 "solid brass hardware, contrast stitching", "and no logo anywhere on it", "The whole inside is caramel leather",
 "with a wide slip pocket", "For scale, I'm six foot four", "It's eighteen inches wide", "and it still looks big on me",
 "It sits on top of my carry-on", "through the whole terminal", "it slides straight into the overhead bin",
 "and my laptop and charger live in that slip pocket", "I haven't checked a bag in two months", "It comes in four colors",
 "They're running a sale right now", "and when they do, the colors always sell out", "I left the link below"]
cards, wi = [], 0
for ch in CHUNKS:
    n = len(ch.split()); grp = words[wi:wi+n]; wi += n
    cards.append((ch, grp))
assert wi == len(words), f"chunk/word mismatch: {wi} vs {len(words)}"
font = ImageFont.truetype(FONT, 62)
def render_card(txt, idx):
    txt = txt.strip().rstrip(".,;:!?"); txt = txt[0].upper() + txt[1:]
    # wrap to <= 900px, max 2 lines
    lines, line = [], ""
    for tok in txt.split():
        trial = (line + " " + tok).strip()
        if font.getlength(trial) > 900 and line:
            lines.append(line); line = tok
        else:
            line = trial
    if line: lines.append(line)
    img = Image.new("RGBA", (W, 220), (0, 0, 0, 0)); dr = ImageDraw.Draw(img)
    y = 110 - (len(lines) * 74) / 2
    for ln in lines:
        x = (W - font.getlength(ln)) / 2
        dr.text((x, y), ln, font=font, fill="white", stroke_width=6, stroke_fill=(20, 20, 20, 255)); y += 74
    p = os.path.join(T, f"cap{idx:03d}.png"); img.save(p); return p
cap_files = []
for i, (txt, ws) in enumerate(cards):
    s = ws[0]["s"]; e = ws[-1]["e"]
    nxt = cards[i + 1][1][0]["s"] if i + 1 < len(cards) else VO_END + 0.4
    e = min(e + 0.12, nxt - 0.02)  # clamp to next card (MENSGS lesson: overlapping cards garble)
    cy = 230 if s < starts[1] else (180 if s >= starts[12] else CAP_Y)
    cap_files.append((render_card(txt, i), s, e, cy))
print("caption cards:", len(cap_files))

# ---- VO loudness
VO_N = os.path.join(T, "vo_-14.m4a")
if not os.path.exists(VO_N):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", VO, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11,volume=1.6dB", "-c:a", "aac", "-b:a", "192k", VO_N], check=True)

def build(m):
    render = os.path.join(ROOT, "avatars", "renders", f"{m}-heygen-green.mp4")
    out = os.path.join(ROOT, "final", f"VEL-WEEKENDER-MENSID-01-{m}.mp4")
    inputs = ["-i", BG, "-i", render]
    for p, _, _, _ in cap_files: inputs += ["-loop", "1", "-i", p]
    x_expr = f"if(lt(t,{starts[1]:.3f}),(W-w)/2,if(lt(t,{PIP_RIGHT_FROM:.3f}),30,W-w-30))"
    fc = [f"[1:v]chromakey={GREENS[m]}:0.08:0.03,despill=type=green:mix=0.15,scale={PIP_W}:-2[pip]",
          f"[0:v][pip]overlay=x='{x_expr}':y=H-h:eof_action=pass[v0]"]
    last = "v0"
    for k, (_, s, e, cy) in enumerate(cap_files):
        fc.append(f"[{last}][{k+2}:v]overlay=0:{cy-110}:enable='between(t,{s:.3f},{e:.3f})'[v{k+1}]"); last = f"v{k+1}"
    cmd = ["ffmpeg", "-v", "error", "-y"] + inputs + ["-i", VO_N, "-filter_complex", ";".join(fc),
           "-map", f"[{last}]", "-map", f"{len(cap_files)+2}:a", "-t", f"{VO_END+0.4:.3f}",
           "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True); print("built", out)

for m in (sys.argv[1:] or ["M1", "M2", "M3"]): build(m)
