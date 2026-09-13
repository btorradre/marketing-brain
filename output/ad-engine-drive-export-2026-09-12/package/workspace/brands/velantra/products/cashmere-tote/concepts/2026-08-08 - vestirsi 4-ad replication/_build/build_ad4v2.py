#!/usr/bin/env python3
"""Assemble VEL-COL-THANKME-02: creator-led fit-check reel, Omni shots + the AD4 VO."""
import pathlib, subprocess, sys

HERE = pathlib.Path(__file__).parent
CONCEPT = HERE.parent
C = HERE / "ad4v2/clips"
WORK = HERE / "ad4v2/cut"; WORK.mkdir(parents=True, exist_ok=True)
VO = HERE / "vo/cand-A.mp3"
OUTDIR = CONCEPT / "output"; OUTDIR.mkdir(exist_ok=True)
W, H, FPS = 720, 1280, 30
# Omni already rendered to the ref-4 recipe, so this is a light unifying pass only
GRADE = "eq=contrast=0.97:saturation=0.93,curves=all='0/0.03 0.5/0.5 1/0.99'"

sys.path.insert(0, str(HERE))
from build_ad4 import caption_cards, render_card, render_offer

EDL = [
    (0.00,  2.74, C/"s01.mp4",              0.5),
    (2.74,  4.60, C/"s02.mp4",              0.5),
    (4.60,  6.54, C/"s03.mp4",              0.5),
    (6.54,  7.79, C/"s04.mp4",              0.5),
    (7.79, 10.00, None,                     0.5),   # s05: Omni if it landed, else keyframe push-in
    (10.00,12.19, C/"s06.mp4",              0.5),
    (12.19,14.90, C/"s07.mp4",              0.4),
    (14.90,17.95, C/"s08.mp4",              0.5),
    (17.95,20.60, C/"s09.mp4",              0.1),
    (20.60,23.23, C/"s10.mp4",              0.5),
    (23.23,25.28, C/"s11.mp4",              0.5),
    (25.28,27.07, C/"s12-kenburns.mp4",     0.0),   # Omni grew a 2nd disc, keyframe push-in
    (27.07,29.24, C/"s13.mp4",              0.5),
    (29.24,30.88, HERE/"ad4/duo-colorways.mp4", 0.0),
    (30.88,35.17, C/"s15.mp4",              0.5),
    (35.17,37.68, C/"s16.mp4",              0.3),
]


def resolve(src, idx):
    if src is not None:
        return src
    omni = C / "s05.mp4"
    return omni if omni.exists() else C / "s05-kenburns.mp4"


def main():
    parts = []
    for i, (a, b, src, tin) in enumerate(EDL):
        src = resolve(src, i)
        if src is None or not src.exists():
            sys.exit(f"missing {src}")
        if src.name == "s05-kenburns.mp4":
            tin = 0.0
        dur = round(b - a, 3)
        dst = WORK / f"c{i:02d}.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(tin), "-t", str(dur),
                        "-i", str(src), "-an",
                        "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,"
                               f"crop={W}:{H},fps={FPS},{GRADE}",
                        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                        "-pix_fmt", "yuv420p", str(dst)], check=True)
        parts.append(dst)
        print(f"  {i:02d} {dur:5.2f}s  {src.name}")

    lst = WORK / "concat.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in parts))
    silent = WORK / "silent.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
                    "-i", str(lst), "-c", "copy", str(silent)], check=True)

    cards = caption_cards()
    cdir = WORK / "cards"; cdir.mkdir(exist_ok=True)
    inputs, filt, cur = [], [], "0:v"
    for i, (text, s, e) in enumerate(cards):
        png = cdir / f"c{i:02d}.png"
        _, ch = render_card(text, png)
        inputs += ["-i", str(png)]
        nxt = f"v{i}"
        filt.append(f"[{cur}][{i+2}:v]overlay=x=0:y={H-330-ch}:"
                    f"enable='between(t,{s:.3f},{e:.3f})'[{nxt}]")
        cur = nxt
    opng = cdir / "offer.png"; render_offer(opng)
    inputs += ["-i", str(opng)]
    filt.append(f"[{cur}][{len(cards)+2}:v]overlay=x=0:y={H-620}:"
                f"enable='between(t,31.60,35.10)'[vout]")

    final = OUTDIR / "VEL-COL-THANKME-02.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(silent), "-i", str(VO)] + inputs +
                   ["-filter_complex", ";".join(filt), "-map", "[vout]", "-map", "1:a",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-shortest", str(final)], check=True)
    d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(final)], capture_output=True, text=True).stdout.strip()
    print(f"\nFINAL {final}  {d}s")


if __name__ == "__main__":
    main()
