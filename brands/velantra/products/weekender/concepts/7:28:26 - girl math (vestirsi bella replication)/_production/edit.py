"""Step 4 — assemble the cut.

Timeline slots are anchored to real word times from the ElevenLabs alignment, so the same
slot map works for all three hook versions even though each VO take is its own generation.
"""
import json, pathlib, re, subprocess, sys

HERE = pathlib.Path(__file__).parent
ROOT = pathlib.Path.home() / "Documents/marketing brain/brands/velantra/products/weekender"
LIB = ROOT / "broll"
CLIPS = HERE / "clips"
VO = HERE / "vo"
BUILD = HERE / ".build"; BUILD.mkdir(exist_ok=True)
FINAL = HERE.parent / "final"; FINAL.mkdir(exist_ok=True)

W, H, FPS = 1080, 1920, 30
FONT = "/System/Library/Fonts/HelveticaNeue.ttc"

# slot -> (source file, in-point). Order is the brief's Section 4.
# Cut points favour the early-to-mid stretch of every generated clip (SOP 2.4).
# Every slot is now generated. The 2026-07-10/11 library clips read as 3D renders, which is
# the fault this whole cut was rebuilt to fix, so reusing five of them beside eleven
# photographic ones would look worse than either alone.
SLOTS = [
    ("gen:CLIP-G.mp4", 0.20),   # 1  airport gate seating
    ("gen:CLIP-A.mp4", 0.20),   # 2  restaurant chair, evening
    ("gen:CLIP-H.mp4", 0.20),   # 3  kitchen counter, the naming beat
    ("gen:CLIP-B.mp4", 0.20),   # 4  overhead bin
    ("gen:CLIP-C.mp4", 0.20),   # 5  gate clutter, wide
    # C's tilt runs past the three-bag read by ~7s, so slot 6 is pulled forward off 4.4s.
    ("gen:CLIP-C.mp4", 3.40),   # 6  gate clutter, tighter
    ("gen:CLIP-I.mp4", 0.20),   # 7  packed at the foot of the bed
    ("gen:CLIP-K.mp4", 0.20),   # 8  open packed bag, mechanism-critical
    ("gen:CLIP-D.mp4", 0.20),   # 9  leather seam macro
    ("gen:CLIP-J.mp4", 0.20),   # 10 luggage rack, holds its shape
    ("gen:CLIP-E1.mp4", 0.20),  # 11 terminal walk
    ("gen:CLIP-E2.mp4", 0.20),  # 12 restaurant entrance
    ("gen:CLIP-F.mp4", 0.20),   # 13 front door
]

# Slot boundaries, as the first words of the line that slot carries. Slot 1 starts at 0.0
# and slot 2 opens at the hook's midpoint (the hook differs per version, so it is computed).
ANCHORS = [
    None, "HOOK_MID",
    "this is the eleanor", "it holds three days", "i used to travel",
    "plus a personal item", "now i just take", "three days of clothes",
    "the leather is full", "and the frame holds", "ive walked an airport",
    "then carried it straight", "i bought it for one weekend",
]


def norm(s):
    return re.sub(r"[^a-z0-9 ]", "", s.lower())


def find(words, phrase):
    toks = phrase.split()
    flat = [norm(w["w"]) for w in words]
    for i in range(len(flat) - len(toks) + 1):
        if flat[i:i + len(toks)] == toks:
            return words[i]["start"]
    raise KeyError(phrase)


def sh(args):
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(" ".join(map(str, args))[:200] + "\n" + r.stderr[-900:])
    return r.stdout


def probe(p):
    return float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                     "-of", "csv=p=0", str(p)]).strip())


def src(tag):
    kind, name = tag.split(":", 1)
    return (LIB if kind == "lib" else CLIPS) / name


# ---------- captions ----------

def cards(words, bounds):
    """Group words into <=7-word cards that never straddle a slot boundary."""
    out, cur = [], []
    edges = set()
    for b in bounds[1:]:
        # index of the first word at or after each slot start
        for i, w in enumerate(words):
            if w["start"] >= b - 1e-6:
                edges.add(i); break

    MAXW = 7

    def emit(group):
        """Split a sentence into balanced chunks so a trailing word is never orphaned.
        Greedy 6-then-remainder stranded 'Velantra.' alone on its own card."""
        if not group:
            return
        n = max(1, -(-len(group) // MAXW))          # chunks needed
        size = -(-len(group) // n)                   # balanced chunk size
        for i in range(0, len(group), size):
            chunk = group[i:i + size]
            out.append({"text": " ".join(w["w"] for w in chunk),
                        "start": chunk[0]["start"], "end": chunk[-1]["end"]})

    for i, w in enumerate(words):
        if i in edges:
            emit(cur); cur = []
        cur.append(w)
        if w["w"].endswith((".", "?", "!")):
            emit(cur); cur = []
    emit(cur)
    return out


def render_cards(cs, outdir):
    """One transparent PNG per card. The swipe uses bare white with no outline, but our
    footage runs much brighter (marble, cream canvas, white bedding) and bare white
    disappeared on it. A soft dark halo under the glyphs buys legibility without reading
    as an outline on the darker frames."""
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    outdir.mkdir(exist_ok=True)
    font = ImageFont.truetype(FONT, 50, index=0)
    for i, c in enumerate(cs):
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        words, lines, cur = c["text"].split(), [], ""
        for w in words:
            t = (cur + " " + w).strip()
            if d.textlength(t, font=font) > W * 0.78 and cur:
                lines.append(cur); cur = w
            else:
                cur = t
        lines.append(cur)
        lh = 62
        y0 = int(H * 0.72) - (len(lines) - 1) * lh // 2

        halo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        hd = ImageDraw.Draw(halo)
        y = y0
        for ln in lines:
            x = (W - d.textlength(ln, font=font)) / 2
            hd.text((x, y + 2), ln, font=font, fill=(0, 0, 0, 190))
            y += lh
        halo = halo.filter(ImageFilter.GaussianBlur(7))
        img = Image.alpha_composite(img, halo)

        d = ImageDraw.Draw(img)
        y = y0
        for ln in lines:
            x = (W - d.textlength(ln, font=font)) / 2
            d.text((x, y), ln, font=font, fill=(255, 255, 255, 242))
            y += lh
        img.save(outdir / f"c{i:03d}.png")
    return [outdir / f"c{i:03d}.png" for i in range(len(cs))]


# ---------- build ----------

def build(ver):
    words = json.loads((VO / f"vo-{ver}.words.json").read_text())
    audio = VO / f"vo-{ver}.mp3"
    total = probe(audio)

    body = find(words, "this is the eleanor")
    bounds = []
    for a in ANCHORS:
        if a is None:
            bounds.append(0.0)
        elif a == "HOOK_MID":
            bounds.append(round(body * 0.55, 3))
        else:
            bounds.append(round(find(words, a), 3))
    bounds.append(total)

    work = BUILD / ver
    work.mkdir(exist_ok=True)
    parts = []
    for i, (tag, tin) in enumerate(SLOTS):
        dur = bounds[i + 1] - bounds[i]
        s = src(tag)
        avail = probe(s) - tin
        if dur > avail:  # never stretch: hold the last frame instead
            print(f"  slot {i+1}: need {dur:.2f}s, have {avail:.2f}s -> freeze tail")
        p = work / f"s{i:02d}.mp4"
        sh(["ffmpeg", "-v", "error", "-ss", str(tin), "-t", f"{dur:.3f}", "-i", str(s),
            "-vf", f"scale={W}:{H}:flags=lanczos,fps={FPS},tpad=stop_mode=clone:stop_duration=3,"
                   f"trim=duration={dur:.3f},setpts=PTS-STARTPTS",
            "-an", "-c:v", "libx264", "-crf", "16", "-preset", "medium",
            "-pix_fmt", "yuv420p", "-y", str(p)])
        parts.append(p)

    lst = work / "parts.txt"
    lst.write_text("".join(f"file '{p.resolve()}'\n" for p in parts))
    base = work / "base.mp4"
    sh(["ffmpeg", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
        "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p",
        "-r", str(FPS), "-y", str(base)])

    cs = cards(words, bounds)
    pngs = render_cards(cs, work / "cards")

    # Each card is overlaid with its own enable window. The concat-demuxer route drifted
    # ~1s late by the end of the reel, which floated captions onto the wrong shots.
    ins, chain, prev = [], [], "0:v"
    for i, (c, p) in enumerate(zip(cs, pngs)):
        ins += ["-i", str(p)]
        # Hold the card past its last word, but never into the next card: words run almost
        # continuously, so an unclamped tail double-exposes two cards on top of each other.
        nxt = cs[i + 1]["start"] - 0.04 if i + 1 < len(cs) else total
        end = min(c["end"] + 0.18, nxt, total)
        lbl = f"v{i}"
        chain.append(f"[{prev}][{i+1}:v]overlay=0:0:format=auto:"
                     f"enable='between(t,{c['start']:.3f},{end:.3f})'[{lbl}]")
        prev = lbl

    dst = FINAL / f"eleanor-girl-math-{ver}.mp4"
    sh(["ffmpeg", "-v", "error", "-i", str(base)] + ins + ["-i", str(audio),
        "-filter_complex", ";".join(chain),
        "-map", f"[{prev}]", "-map", f"{len(pngs)+1}:a",
        "-c:v", "libx264", "-b:v", "18M", "-maxrate", "20M", "-bufsize", "36M",
        "-preset", "slow", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-t", f"{total:.3f}", "-movflags", "+faststart", "-y", str(dst)])
    print(f"{dst.name}  {probe(dst):.1f}s  {dst.stat().st_size//1024//1024}MB  "
          f"{len(cs)} caption cards")
    return bounds


if __name__ == "__main__":
    for ver in (sys.argv[1:] or ["v1", "hookb", "hookc"]):
        print(f"--- {ver} ---")
        b = build(ver)
        print("   slot starts:", [f"{x:.1f}" for x in b])
