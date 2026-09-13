#!/usr/bin/env python3
"""Assemble VEL-STRAWTOTE-GOESWITH-VO-01.

Cut points are derived from the chosen VO take's Whisper word timings, so every
shot change lands on the intended word. Each Kling clip is 6s; we always take
from the HEAD of the clip (i2v drift grows late), trimmed to its beat length.

Usage:
  assemble.py            # builds clean cut, captioned cut, and captions.srt
"""
import json, os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
CLIPS = os.path.join(ROOT, "assets", "clips")
WORK = os.path.join(ROOT, "assets", "_work")
VO = os.path.join(ROOT, "vo", "eden-clone-v3", "voiceover.mp3")
VO_LUFS = -14.0          # broadcast-ish target so the read sits forward
W, H = 720, 1280

# shot -> (in, out) on the finished timeline, from the v3 take's Whisper word timings
TIMELINE = [
    ("S01",  0.00,  1.30), ("S02",  1.30,  2.62),
    ("S03",  2.62,  3.74), ("S04",  3.74,  4.85),
    ("S05",  4.85,  5.84), ("S06",  5.84,  6.84), ("S07",  6.84,  7.83),
    ("S08",  7.83,  9.76),
    ("S09",  9.76, 10.90), ("S10", 10.90, 12.05), ("S11", 12.05, 13.20),
    ("S12", 13.20, 14.80), ("S13", 14.80, 16.35),
    ("S14", 16.35, 17.35), ("S15", 17.35, 18.32), ("S16", 18.32, 19.60),
]

# on-screen text mirrors the VO word for word, cut into reading chunks
CAPTIONS = [
    (0.00,  2.62, "From beach mornings to market runs,"),
    (2.62,  4.85, "lunch on the water to dinner in town,"),
    (4.85,  6.18, "it goes with everything"),
    (6.18,  7.83, "without feeling overthought."),
    (7.83,  9.76, "Meet the Velantra Straw Tote."),
    (9.76, 11.14, "It's hand woven,"),
    (11.14, 13.20, "with a structured body and leather detailing,"),
    (13.20, 14.70, "so it holds its shape,"),
    (14.70, 16.35, "and a whole day of stuff."),
    (16.35, 18.32, "It's the one you'll keep reaching for,"),
    (18.32, 19.60, "all summer long."),
]


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(" ".join(cmd[:6]) + "\n" + r.stderr[-1500:])
    return r


def srt_ts(t):
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s - int(s)) * 1000)):03d}"


FONT_TTC = "/System/Library/Fonts/Avenir Next.ttc"
FONT_IDX = 10          # Avenir Next Ultra Light
FONT_PX = 30
CAP_Y = 350            # baseline band, upper third — matches the reference ad
LINE_GAP = 8


def render_caption_png(text, dst):
    """Transparent 720x1280 PNG holding one centred caption, wrapped to fit."""
    from PIL import Image, ImageDraw, ImageFont
    font = ImageFont.truetype(FONT_TTC, FONT_PX, index=FONT_IDX)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    max_w = W - 120

    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)

    y = CAP_Y
    for line in lines:
        tw = d.textlength(line, font=font)
        d.text(((W - tw) / 2, y), line, font=font, fill=(255, 255, 255, 242))
        y += FONT_PX + LINE_GAP
    img.save(dst)


def build_captioned(src, dst):
    pngs = []
    for i, (a, b, txt) in enumerate(CAPTIONS):
        p = os.path.join(WORK, f"cap_{i:02d}.png")
        render_caption_png(txt, p)
        pngs.append((p, a, b))

    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", src]
    for p, _, _ in pngs:
        cmd += ["-i", p]
    chain, last = [], "0:v"
    for i, (_, a, b) in enumerate(pngs):
        out = f"v{i}"
        chain.append(f"[{last}][{i + 1}:v]overlay=0:0:enable='between(t,{a},{b})'[{out}]")
        last = out
    cmd += ["-filter_complex", ";".join(chain),
            "-map", f"[{last}]", "-map", "0:a:0",
            "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p",
            "-c:a", "copy", dst]
    run(cmd)


def main():
    os.makedirs(WORK, exist_ok=True)
    missing = [s for s, _, _ in TIMELINE if not os.path.exists(os.path.join(CLIPS, f"{s}.mp4"))]
    if missing:
        raise SystemExit(f"missing clips: {missing}")

    parts = []
    for sid, t_in, t_out in TIMELINE:
        dur = round(t_out - t_in, 3)
        dst = os.path.join(WORK, f"{sid}_cut.mp4")
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(CLIPS, f"{sid}.mp4"),
             "-t", str(dur),
             "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps=30,setsar=1",
             "-an", "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p", dst])
        parts.append(dst)

    listfile = os.path.join(WORK, "concat.txt")
    with open(listfile, "w") as f:
        for p in parts:
            f.write(f"file '{p}'\n")

    silent = os.path.join(WORK, "video_silent.mp4")
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", listfile,
         "-c", "copy", silent])

    # loudness-normalise the VO so the read sits forward and consistent
    vo_norm = os.path.join(WORK, "vo_norm.wav")
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", VO,
         "-af", f"loudnorm=I={VO_LUFS}:TP=-1.5:LRA=11", "-ar", "48000", vo_norm])

    clean = os.path.join(ROOT, "VELANTRA-GOESWITH-VO-V1-clean.mp4")
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-i", vo_norm,
         "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy",
         "-c:a", "aac", "-b:a", "192k", clean])

    srt = os.path.join(ROOT, "captions.srt")
    with open(srt, "w") as f:
        for i, (a, b, txt) in enumerate(CAPTIONS, 1):
            f.write(f"{i}\n{srt_ts(a)} --> {srt_ts(b)}\n{txt}\n\n")

    # Thin white centred caption in the upper third, no box — matches the reference ad.
    # This ffmpeg build has no libass (no subtitles/ass/drawtext filters), so captions
    # are rendered to transparent PNGs with PIL and composited with `overlay`.
    capped = os.path.join(ROOT, "VELANTRA-GOESWITH-VO-V1-captioned.mp4")
    build_captioned(clean, capped)

    for p in (clean, capped):
        d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                            "-of", "csv=p=0", p], capture_output=True, text=True).stdout.strip()
        print(f"{os.path.basename(p)}  {d}s")
    print(f"captions.srt  {len(CAPTIONS)} cues")


if __name__ == "__main__":
    main()
