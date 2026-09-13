#!/usr/bin/env python3
"""Assemble VEL-COL-THANKME-01 from the existing Colette b-roll library + the AD4 VO.

Every clip is muted (Omni bakes ambient in, it fights the VO), trimmed from the
early-to-mid stretch (late frames drift), graded to the ref-4 look
(low contrast, desaturated, lifted blacks), then the single continuous VO is laid
over the whole assembly.
"""
import json, pathlib, subprocess, sys

HERE = pathlib.Path(__file__).parent
CONCEPT = HERE.parent
PROD = pathlib.Path("/Users/brooksorradre2/Documents/marketing brain"
                    "/brands/velantra/products/cashmere-tote")
LIB = PROD / "broll/library-2026-08/clips"
V3 = PROD / "concepts/2026-08-04-ugc-review-25s/_v3/clips"
WORK = HERE / "ad4"; WORK.mkdir(exist_ok=True)
VO = HERE / "vo/cand-A.mp3"
OUTDIR = CONCEPT / "output"; OUTDIR.mkdir(exist_ok=True)

W, H, FPS = 720, 1280, 30
GRADE = "eq=contrast=0.93:saturation=0.86,curves=all='0/0.055 0.5/0.5 1/0.97'"

# (start, end) in the finished cut, source clip, in-point inside that clip
EDL = [
    (0.00,  2.74, LIB/"VEL-COL-018-street-crisp-morning.mp4",   1.2),
    (2.74,  3.70, LIB/"VEL-COL-016-street-school-pickup.mp4",   1.5),
    (3.70,  6.54, LIB/"VEL-COL-003-street-coffee-run.mp4",      1.0),
    (6.54,  7.79, LIB/"VEL-COL-004-street-walking-side.mp4",    1.5),
    (7.79, 10.00, V3 /"COL-091-pan-full-bag.mp4",               0.8),
    (10.00,12.19, LIB/"VEL-COL-075-macro-felt-fibre.mp4",       1.0),
    (12.19,14.90, LIB/"VEL-COL-085-macro-side-gusset.mp4",      1.0),
    (14.90,17.95, LIB/"VEL-COL-088-setdown-park-bench.mp4",     0.8),
    (17.95,23.23, V3 /"COL-092-pack-continuous-three-r2.mp4",   0.6),
    (23.23,25.28, LIB/"VEL-COL-077-macro-handle-wrap.mp4",      1.0),
    (25.28,27.07, LIB/"VEL-COL-076-macro-gold-disc.mp4",        1.0),
    (27.07,29.24, LIB/"VEL-COL-083-macro-corner-base.mp4",      1.0),
    (29.24,31.50, HERE/"ad4/duo-colorways.mp4",                   0.0),
    (31.50,35.17, LIB/"VEL-COL-020-cafe-table-beside-latte.mp4",1.0),
    (35.17,37.68, LIB/"VEL-COL-004-street-walking-side.mp4",    5.0),
]


def caption_cards():
    """Cards from the VO's real character alignment. <=6 words, break on sentence punctuation,
    tail clamped to the next card so two cards never stack (see burned-caption-overlays)."""
    d = json.loads((HERE/"vo/cand-A-words.json").read_text())
    ch, st, en = d["characters"], d["character_start_times_seconds"], d["character_end_times_seconds"]
    words, cur, s0 = [], "", None
    for c, a, b in zip(ch, st, en):
        if s0 is None and c.strip():
            s0 = a
        cur += c
        if c == " " and cur.strip():
            words.append((cur.strip(), s0, b)); cur, s0 = "", None
    if cur.strip():
        words.append((cur.strip(), s0, en[-1]))
    # group on clause boundaries first, then split anything over 8 words at a point
    # that is not immediately after a function word, so cards never break mid-phrase
    GLUE = {"a","an","the","and","or","of","with","for","to","in","on","it","that","so","is"}
    clauses, buf = [], []
    for w in words:
        buf.append(w)
        if w[0].rstrip().endswith((",", ".")):
            clauses.append(buf); buf = []
    if buf:
        clauses.append(buf)
    groups = []
    for cl in clauses:
        if len(cl) <= 8:
            if groups and len(groups[-1]) + len(cl) <= 7 and len(cl) <= 3:
                groups[-1].extend(cl)       # absorb trailing stubs
            else:
                groups.append(cl)
            continue
        # long clause: cut as close to the middle as possible on a non-glue boundary
        best, mid = None, len(cl) // 2
        NUM = {"thirteen","twenty","one","two","three","pre-order"}
        for j in range(2, len(cl) - 1):
            if cl[j][0].strip(",.").lower() in GLUE:
                continue
            if cl[j-1][0].strip(",.").lower() in NUM:   # never split "thirteen | inch"
                continue
            if best is None or abs(j - mid) < abs(best - mid):
                best = j
        best = best or mid
        groups.append(cl[:best]); groups.append(cl[best:])
    # a 1-2 word opening clause reads as a flash card, merge it forward
    if len(groups) > 1 and len(groups[0]) <= 2 and len(groups[0]) + len(groups[1]) <= 8:
        groups[1] = groups[0] + groups[1]; groups.pop(0)
    total = en[-1]
    cards = []
    for i, g in enumerate(groups):
        # house style: no periods or commas, sentence case starting lowercase
        text = " ".join(w[0] for w in g)
        text = text.replace(",", "").replace(".", "").strip()
        if text and text[0].isupper() and text.split()[0] not in ("Colette", "Velantra", "Loro", "Girls", "Caramel"):
            text = text[0].lower() + text[1:]
        nxt = groups[i+1][0][1] if i + 1 < len(groups) else total + 1
        end = min(g[-1][2] + 0.18, nxt - 0.04, total)
        cards.append((text, g[0][1], end))
    return cards


def render_card(text, path, size=46, maxw=620):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    font = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", size, index=2)
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if font.getbbox(trial)[2] > maxw and cur:
            lines.append(cur); cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    lines = lines[:2]
    lh = int(size * 1.28)
    img = Image.new("RGBA", (W, lh * len(lines) + 40), (0, 0, 0, 0))
    halo = Image.new("RGBA", img.size, (0, 0, 0, 0))
    dh, dt = ImageDraw.Draw(halo), ImageDraw.Draw(img)
    for i, ln in enumerate(lines):
        bb = font.getbbox(ln)
        x = (W - (bb[2] - bb[0])) // 2 - bb[0]
        y = 20 + i * lh
        dh.text((x, y), ln, font=font, fill=(0, 0, 0, 190))
    halo = halo.filter(ImageFilter.GaussianBlur(7))
    img = Image.alpha_composite(halo, img)
    dt = ImageDraw.Draw(img)
    for i, ln in enumerate(lines):
        bb = font.getbbox(ln)
        x = (W - (bb[2] - bb[0])) // 2 - bb[0]
        dt.text((x, 20 + i * lh), ln, font=font, fill=(255, 255, 255, 255))
    img.save(path)
    return img.size


def render_offer(path):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    f1 = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 62, index=2)
    f2 = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 32, index=2)
    img = Image.new("RGBA", (W, 150), (0, 0, 0, 0))
    halo = Image.new("RGBA", img.size, (0, 0, 0, 0))
    dh = ImageDraw.Draw(halo)
    rows = [("$119.99 PRE-ORDER", f1, 10), ("$149.99 WHEN IT SHIPS", f2, 92)]
    for txt, f, y in rows:
        bb = f.getbbox(txt)
        dh.text(((W - (bb[2]-bb[0]))//2 - bb[0], y), txt, font=f, fill=(0, 0, 0, 200))
    halo = halo.filter(ImageFilter.GaussianBlur(8))
    img = Image.alpha_composite(halo, img)
    d = ImageDraw.Draw(img)
    for txt, f, y in rows:
        bb = f.getbbox(txt)
        d.text(((W - (bb[2]-bb[0]))//2 - bb[0], y), txt, font=f, fill=(255, 255, 255, 255))
    img.save(path)
    return img.size


def main():
    parts = []
    for i, (a, b, src, tin) in enumerate(EDL):
        dur = round(b - a, 3)
        if not src.exists():
            sys.exit(f"missing {src}")
        dst = WORK / f"seg{i:02d}.mp4"
        subprocess.run([
            "ffmpeg", "-v", "error", "-y", "-ss", str(tin), "-t", str(dur), "-i", str(src),
            "-an", "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,"
                          f"crop={W}:{H},fps={FPS},{GRADE}",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
            str(dst)], check=True)
        parts.append(dst)
        print(f"  seg{i:02d} {dur:5.2f}s  {src.name}")

    lst = WORK / "concat.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in parts))
    silent = WORK / "silent.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
                    "-i", str(lst), "-c", "copy", str(silent)], check=True)

    # captions + offer card: Pillow PNGs composited with one enable-gated overlay each
    cards = caption_cards()
    cdir = WORK / "cards"; cdir.mkdir(exist_ok=True)
    inputs, filt, cur = [], [], "0:v"
    for i, (text, s, e) in enumerate(cards):
        png = cdir / f"c{i:02d}.png"
        _, ch = render_card(text, png)
        inputs += ["-i", str(png)]
        y = H - 330 - ch
        nxt = f"v{i}"
        filt.append(f"[{cur}][{i+2}:v]overlay=x=0:y={y}:enable='between(t,{s:.3f},{e:.3f})'[{nxt}]")
        cur = nxt
        print(f"  card {i:02d} {s:6.2f}-{e:6.2f}  {text}")
    opng = cdir / "offer.png"
    _, oh = render_offer(opng)
    inputs += ["-i", str(opng)]
    idx = len(cards) + 2
    filt.append(f"[{cur}][{idx}:v]overlay=x=0:y={H-620}:enable='between(t,31.60,35.10)'[vout]")

    final = OUTDIR / "VEL-COL-THANKME-01.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y",
                    "-i", str(silent), "-i", str(VO)] + inputs +
                   ["-filter_complex", ";".join(filt),
                    "-map", "[vout]", "-map", "1:a",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-shortest", str(final)], check=True)

    d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(final)], capture_output=True, text=True).stdout.strip()
    print(f"\nFINAL {final}  {d}s")


if __name__ == "__main__":
    main()
