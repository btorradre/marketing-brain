#!/usr/bin/env python3
"""VEL-STRAW-WOVEN-CRAFT-01 edit builder.

Cuts the 6s Kling clips to the real VO word timings, burns progressive
word-by-word captions, muxes the single-track VO, appends the end card.

Usage: build_edit.py [voice]      # voice = amaya | lily | cecily (default amaya)
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
CLIPS = os.path.join(ROOT, "plates", "clips")
WORK = os.path.join(HERE, "edit")
FINAL = os.path.join(ROOT, "final")
LOGO = "/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/straw-birkin/concepts/7:24:26 - bag of summer (vestirsi replication)/_production/velantra_logo.png"

W, H, FPS = 720, 1280, 24
FONT_FILE = "/System/Library/Fonts/HelveticaNeue.ttc"
FONT_INDEX = 10          # Helvetica Neue Medium
FONTSIZE = 44
MARGIN_L = int(W * 0.10)
CAP_Y = int(H * 0.50)
ENDCARD = 0.6

VOICE = sys.argv[1] if len(sys.argv) > 1 else "amaya"


def run(args, cwd=None):
    r = subprocess.run(args, capture_output=True, text=True, cwd=cwd)
    if r.returncode != 0:
        raise RuntimeError(f"{args[0]} failed:\n{r.stderr[-1500:]}")
    return r


def words_from_alignment(path):
    a = json.load(open(path))
    chars, st, en = a["characters"], a["character_start_times_seconds"], a["character_end_times_seconds"]
    out, cur, s, prev = [], "", None, 0.0
    for c, t0, t1 in zip(chars, st, en):
        if c == " ":
            if cur:
                out.append({"w": cur, "s": s, "e": prev})
                cur, s = "", None
            continue
        if not cur:
            s = t0
        cur += c
        prev = t1
    if cur:
        out.append({"w": cur, "s": s, "e": prev})
    return out


def split_sentences(words):
    sents, cur = [], []
    for w in words:
        cur.append(w)
        if w["w"].endswith("."):
            sents.append(cur)
            cur = []
    if cur:
        sents.append(cur)
    return sents


def main():
    os.makedirs(WORK, exist_ok=True)
    os.makedirs(FINAL, exist_ok=True)
    align = os.path.join(HERE, "vo", f"FINAL_{VOICE}_align.json")
    vo_mp3 = os.path.join(HERE, "vo", f"FINAL_{VOICE}.mp3")
    words = words_from_alignment(align)
    sents = split_sentences(words)
    vo_end = words[-1]["e"]

    # locate the "damp," / "so" boundary inside sentence 2
    s2 = sents[1]
    bidx = next(i for i, w in enumerate(s2) if w["w"].lower().startswith("so"))
    b = s2[bidx]["s"]

    # timeline spans: (start, end, [(clip, src_in), ...])
    spans = [
        (0.0,            sents[1][0]["s"], [("A", 0.6), ("B", 0.8)]),
        (sents[1][0]["s"], b,              [("C", 0.5), ("D", 0.4), ("D", 3.2)]),
        (b,              sents[2][0]["s"], [("E", 0.5), ("F", 0.8), ("G", 0.6)]),
        (sents[2][0]["s"], sents[3][0]["s"], [("H", 0.6), ("I", 0.7)]),
        (sents[3][0]["s"], sents[4][0]["s"], [("J", 0.6), ("K", 0.8), ("L", 0.8)]),
        (sents[4][0]["s"], sents[5][0]["s"], [("M", 0.4), ("M", 3.9)]),
        (sents[5][0]["s"], vo_end + 0.45,   [("N", 0.5), ("N", 2.8), ("N", 4.6)]),
    ]

    # ---- cut every segment -------------------------------------------------
    cuts, n = [], 0
    for s0, s1, items in spans:
        dur = (s1 - s0) / len(items)
        for clip, src_in in items:
            n += 1
            src = os.path.join(CLIPS, f"{clip}.mp4")
            if not os.path.exists(src):
                raise SystemExit(f"missing clip {clip}.mp4 -- generate it first")
            dst = os.path.join(WORK, f"cut{n:02d}.mp4")
            run(["ffmpeg", "-y", "-v", "error", "-ss", f"{src_in:.3f}", "-i", src,
                 "-t", f"{dur:.3f}", "-an",
                 "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}",
                 "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", dst])
            cuts.append((dst, s0, dur, clip))
            s0 += dur
    print(f"cut {len(cuts)} segments, video body {cuts[-1][1] + cuts[-1][2]:.2f}s")

    # ---- concat ------------------------------------------------------------
    lst = os.path.join(WORK, "concat.txt")
    open(lst, "w").write("".join(f"file '{c[0]}'\n" for c in cuts))
    body = os.path.join(WORK, "body.mp4")
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst,
         "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", body])

    # ---- progressive word captions (PNG sequence) --------------------------
    # this ffmpeg has no libass/libfreetype, so the caption layer is rendered
    # with PIL and composited as a transparent image sequence.
    from PIL import Image, ImageDraw, ImageFont

    font = ImageFont.truetype(FONT_FILE, FONTSIZE, index=FONT_INDEX)

    def wrap(text, maxch=26):
        parts, line, out = text.split(), "", []
        for p in parts:
            if len(line) + len(p) + 1 > maxch and line:
                out.append(line)
                line = p
            else:
                line = (line + " " + p).strip()
        out.append(line)
        return out[-2:]          # never more than 2 lines

    ev = []
    for sent in sents:
        for i, w in enumerate(sent):
            acc = " ".join(x["w"] for x in sent[:i + 1])
            start = w["s"]
            end = sent[i + 1]["s"] if i + 1 < len(sent) else w["e"] + 0.42
            ev.append((start, end, acc))

    capdir = os.path.join(WORK, "caps")
    os.makedirs(capdir, exist_ok=True)
    for f in os.listdir(capdir):
        os.remove(os.path.join(capdir, f))

    blank = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cache = {}

    def render(text):
        if text in cache:
            return cache[text]
        img = blank.copy()
        d = ImageDraw.Draw(img)
        lines = wrap(text)
        lh = int(FONTSIZE * 1.32)
        y = CAP_Y - (len(lines) - 1) * lh // 2
        for ln in lines:
            d.text((MARGIN_L, y), ln, font=font, fill=(255, 255, 255, 255), anchor="lm")
            y += lh
        cache[text] = img
        return img

    body_dur = cuts[-1][1] + cuts[-1][2]
    nframes = int(round(body_dur * FPS))
    for fi in range(nframes):
        t = fi / FPS
        txt = next((e[2] for e in ev if e[0] <= t < e[1]), None)
        img = render(txt) if txt else blank
        img.save(os.path.join(capdir, f"c{fi:05d}.png"))
    print(f"rendered {nframes} caption frames ({len(cache)} unique states)")

    capped = os.path.join(WORK, "capped.mp4")
    run(["ffmpeg", "-y", "-v", "error", "-i", body,
         "-framerate", str(FPS), "-i", os.path.join(capdir, "c%05d.png"),
         "-filter_complex", "[0:v][1:v]overlay=0:0:format=auto,format=yuv420p[v]",
         "-map", "[v]", "-c:v", "libx264", "-preset", "medium", "-crf", "17", capped])

    # ---- end card ----------------------------------------------------------
    # the source wordmark is pure black on transparent; recolor to white so it
    # is visible on the black card, preserving the original alpha.
    lg = Image.open(LOGO).convert("RGBA")
    a = lg.getchannel("A")
    white = Image.new("RGBA", lg.size, (255, 255, 255, 0))
    white.putalpha(a)
    logo_w = os.path.join(WORK, "logo_white.png")
    white.save(logo_w)

    card = os.path.join(WORK, "card.mp4")
    run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi",
         "-i", f"color=c=black:s={W}x{H}:d={ENDCARD}:r={FPS}",
         "-i", logo_w,
         "-filter_complex",
         f"[1:v]scale={int(W*0.42)}:-1[lg];[0:v][lg]overlay=(W-w)/2:(H-h)/2,format=yuv420p[v]",
         "-map", "[v]", "-c:v", "libx264", "-preset", "medium", "-crf", "17", card])

    lst2 = os.path.join(WORK, "concat2.txt")
    open(lst2, "w").write(f"file '{capped}'\nfile '{card}'\n")
    silent = os.path.join(WORK, "silent.mp4")
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst2,
         "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", silent])

    # ---- mux VO ------------------------------------------------------------
    out = os.path.join(FINAL, f"VEL-STRAW-WOVEN-CRAFT-01_{VOICE}.mp4")
    run(["ffmpeg", "-y", "-v", "error", "-i", silent, "-i", vo_mp3,
         "-filter_complex", "[1:a]adelay=0|0,apad[a]",
         "-map", "0:v", "-map", "[a]", "-shortest",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", out])

    d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", out], capture_output=True, text=True).stdout.strip()
    print(f"FINAL -> {out}  ({float(d):.2f}s)")


if __name__ == "__main__":
    main()
