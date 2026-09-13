#!/usr/bin/env python3
"""VEL-SOFIA-EDIT-01 assembly — speech-island trim, hard-cut concat, PIL captions.

  assemble.py islands            report speech islands per clip (QA read)
  assemble.py trim               write trimmed clips to assets/clips/_trimmed
  assemble.py captions           render one transparent caption PNG per clip
  assemble.py stitch             concat trimmed clips -> assets/VEL-SOFIA-EDIT-01-final.mp4
  assemble.py stitch --captions  same, with captions burned in

Why speech islands: Seedance appends hallucinated stray words at clip ends
("Regood", "Short.") even when the prompt forbids extra speech. A trailing
island under ~0.45s is dropped. A silence that ENDS is a mid-line pause, never
the end of the line — treating it as the end truncates the tail clause.

Why PIL for captions: this machine's ffmpeg has NO drawtext and NO libass.
"""
import json, os, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import blocks as B

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.normpath(os.path.join(HERE, "..", "assets"))
CLIPS = os.path.join(ASSETS, "clips")
TRIMMED = os.path.join(CLIPS, "_trimmed")
CAPS = os.path.join(ASSETS, "overlays")
FINAL = os.path.join(ASSETS, "VEL-SOFIA-EDIT-01-final.mp4")
W, H = 720, 1280
MIN_ISLAND = 0.45          # trailing islands shorter than this are hallucinated tails
NOISE_DB = "-32dB"


def clip_path(sid):
    return os.path.join(CLIPS, f"{sid}.mp4")


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "default=nw=1:nk=1", path], capture_output=True, text=True)
    return float(out.stdout.strip())


def islands(path):
    """Return [(start, end)] of speech, via silencedetect inversion."""
    out = subprocess.run(
        ["ffmpeg", "-i", path, "-af", f"silencedetect=noise={NOISE_DB}:d=0.28", "-f", "null", "-"],
        capture_output=True, text=True).stderr
    sil = []
    start = None
    for line in out.splitlines():
        if "silence_start" in line:
            start = float(line.split("silence_start:")[1].split()[0])
        elif "silence_end" in line:
            end = float(line.split("silence_end:")[1].split()[0])
            sil.append((start if start is not None else 0.0, end))
            start = None
    if start is not None:
        sil.append((start, duration(path)))
    total = duration(path)
    spans, cur = [], 0.0
    for a, b in sil:
        if a - cur > 0.05:
            spans.append((cur, a))
        cur = b
    if total - cur > 0.05:
        spans.append((cur, total))
    return spans, total


def speech_window(path):
    """Start/end of real speech: first island start, last island end after dropping
    a short trailing island (hallucinated word)."""
    spans, total = islands(path)
    if not spans:
        return 0.0, total
    keep = list(spans)
    while len(keep) > 1 and (keep[-1][1] - keep[-1][0]) < MIN_ISLAND:
        keep.pop()
    return max(0.0, keep[0][0] - 0.10), min(total, keep[-1][1] + 0.18)


def cmd_islands():
    for sid, *_ in B.SHOTS:
        p = clip_path(sid)
        if not os.path.exists(p):
            print(f"{sid}: MISSING")
            continue
        spans, total = islands(p)
        a, b = speech_window(p)
        pretty = " ".join(f"[{x:.2f}-{y:.2f}]" for x, y in spans)
        print(f"{sid}: total={total:.2f} keep={a:.2f}-{b:.2f} ({b-a:.2f}s) islands={pretty}")


def cmd_trim():
    os.makedirs(TRIMMED, exist_ok=True)
    for sid, *_ in B.SHOTS:
        p = clip_path(sid)
        if not os.path.exists(p):
            print(f"{sid}: MISSING, skipping")
            continue
        a, b = speech_window(p)
        dest = os.path.join(TRIMMED, f"{sid}.mp4")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", p, "-ss", f"{a:.3f}", "-to", f"{b:.3f}",
                        "-vf", f"scale={W}:{H}", "-r", "30",
                        "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
                        "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2", dest],
                       check=True)
        print(f"{sid} -> {b-a:.2f}s")


def cmd_captions():
    """One transparent PNG per clip. White, sentence case, thin sans, centred
    lower-third, no box — matches the reference exactly."""
    from PIL import Image, ImageDraw, ImageFont
    os.makedirs(CAPS, exist_ok=True)
    face = None
    for cand in ["/System/Library/Fonts/Supplemental/HelveticaNeue.ttc",
                 "/System/Library/Fonts/Helvetica.ttc",
                 "/Library/Fonts/Arial.ttf"]:
        if os.path.exists(cand):
            face = cand
            break
    assert face, "no usable font found"
    font = ImageFont.truetype(face, 40)
    for shot in B.SHOTS:
        sid, line = shot[0], shot[6]
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        words, lines, cur = line.split(), [], ""
        for w in words:
            t = (cur + " " + w).strip()
            if d.textlength(t, font=font) > W - 76 and cur:
                lines.append(cur)
                cur = w
            else:
                cur = t
        lines.append(cur)
        y = int(H * 0.815) - (len(lines) - 1) * 26
        for ln in lines:
            x = (W - d.textlength(ln, font=font)) / 2
            for ox, oy in ((-2, 0), (2, 0), (0, -2), (0, 2)):
                d.text((x + ox, y + oy), ln, font=font, fill=(0, 0, 0, 90))
            d.text((x, y), ln, font=font, fill=(255, 255, 255, 255))
            y += 52
        img.save(os.path.join(CAPS, f"{sid}.png"))
    print(f"{len(B.SHOTS)} caption PNGs -> {CAPS}")


def cmd_stitch(with_caps):
    src = TRIMMED if os.path.isdir(TRIMMED) else CLIPS
    have = [s[0] for s in B.SHOTS if os.path.exists(os.path.join(src, f"{s[0]}.mp4"))]
    missing = [s[0] for s in B.SHOTS if s[0] not in have]
    if missing:
        print(f"WARNING: missing {missing} — stitching {len(have)} clips only")
    stage = os.path.join(src, "_captioned") if with_caps else src
    if with_caps:
        os.makedirs(stage, exist_ok=True)
        for sid in have:
            subprocess.run(["ffmpeg", "-y", "-v", "error",
                            "-i", os.path.join(src, f"{sid}.mp4"),
                            "-i", os.path.join(CAPS, f"{sid}.png"),
                            "-filter_complex", "[0:v][1:v]overlay=0:0",
                            "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
                            "-c:a", "copy", os.path.join(stage, f"{sid}.mp4")], check=True)
    lst = os.path.join(HERE, "concat.txt")
    with open(lst, "w") as f:
        for sid in have:
            f.write(f"file '{os.path.join(stage, sid + '.mp4')}'\n")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst,
                    "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "160k", FINAL], check=True)
    print(f"FINAL {duration(FINAL):.2f}s -> {FINAL}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "islands"
    {"islands": cmd_islands, "trim": cmd_trim, "captions": cmd_captions,
     "stitch": lambda: cmd_stitch("--captions" in sys.argv)}.get(cmd, lambda: print(__doc__))()
