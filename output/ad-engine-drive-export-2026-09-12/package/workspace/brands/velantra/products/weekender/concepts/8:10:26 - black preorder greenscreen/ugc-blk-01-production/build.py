#!/usr/bin/env python3
"""UGC-BLK-01 "The One I Won't Be Careful With" — composite build.

Fork of the DC-04 v2 recipe: all-b-roll base, hard cut from cream-canvas problem
footage to the all-black payoff, keyed creator PiP bottom-left, one continuous VO,
Pillow caption cards burned from word-level STT.
"""
import json, os, subprocess, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BROLL = os.path.abspath(os.path.join(HERE, "../../../broll"))
WORK = os.path.join(HERE, "_work")
os.makedirs(WORK, exist_ok=True)

W, H, FPS = 1080, 1920, 30

def run(args):
    subprocess.run(args, check=True, capture_output=True)

# beat = (start, end, source, in-point). source is a filename in broll/ or a local file.
BEATS = [
    # --- cream canvas: the problem -------------------------------------------
    (0.00,  2.42, "dc-B01-bench.mp4",                              0.0),
    (2.42,  6.20, "Velantra_Weekender_bag_travel_202607101152 (1).mp4", 0.3),
    (6.20,  9.55, "dc-B10-styled.mp4",                             0.0),
    (9.55, 11.30, "dc-B08-canvas.mp4",                             0.0),
    (11.30,14.75, "Velantra_Weekender_in_car_trunk_202607101153.mp4", 0.3),
    (14.75,16.20, "dc-B14-car.mp4",                                0.0),
    (16.20,18.42, "dc-B03-door.mp4",                               0.0),
    # --- hard cut to black: the fix ------------------------------------------
    (18.42,20.00, "NB-01-entryway-floor.mp4",                      0.0),
    (20.00,22.30, "NB-03-hotel-rack.mp4",                          0.0),
    (22.30,25.70, "NB-15-macro-gusset-eyelet.mp4",                 0.0),
    (25.70,28.30, "NB-04-carry-hallway.mp4",                       0.0),
    (28.30,30.10, "NB-13-macro-turnlock.mp4",                      0.0),
    (30.10,32.50, "NB-14-macro-interior.mp4",                      0.0),
    (32.50,36.90, "NB-02-bed-open-packed.mp4",                     0.0),
    (36.90,38.80, "NB-07-packing-hands.mp4",                       0.0),
    (38.80,40.50, "NB-09-airport-bench.mp4",                       0.0),
    # --- offer ---------------------------------------------------------------
    (40.50,47.70, "@pdp_scroll.mp4",                               0.0),
    # --- close ---------------------------------------------------------------
    (47.70,50.20, "NB-08-doorway-pickup.mp4",                      0.0),
    (50.20,53.30, "NB-12-stairs-descend.mp4",                      0.0),
]

def src_path(name):
    return os.path.join(HERE, name[1:]) if name.startswith("@") else os.path.join(BROLL, name)

def cut_beats():
    paths = []
    for i, (a, b, name, ss) in enumerate(BEATS):
        out = os.path.join(WORK, f"beat_{i:02d}.mp4")
        dur = round(b - a, 3)
        run(["ffmpeg", "-y", "-v", "error", "-ss", str(ss), "-i", src_path(name),
             "-t", str(dur), "-an",
             "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},format=yuv420p",
             "-c:v", "libx264", "-crf", "17", "-preset", "medium", out])
        paths.append(out)
    lst = os.path.join(WORK, "concat.txt")
    with open(lst, "w") as f:
        for p in paths:
            f.write(f"file '{p}'\n")
    base = os.path.join(WORK, "base.mp4")
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst,
         "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p", base])
    return base

def key_avatar():
    """Green -> VP9 alpha webm. Decode side MUST force libvpx-vp9 or alpha is dropped."""
    out = os.path.join(WORK, "avatar_keyed.webm")
    run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(HERE, "avatar_green_blk.mp4"), "-an",
         # No despill: mix=0.5 crushes green on her neutral sweater and it renders pink.
         # Measured fringe with the key alone is 0.16% of subject pixels, which is nothing.
         "-vf", (f"format=yuva420p,chromakey=0x007A28:0.11:0.02,fps={FPS},format=yuva420p"),
         "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "6M", "-auto-alt-ref", "0", out])
    return out

def caption_cards():
    """4-word cards on word-level STT boundaries. White Helvetica Bold + black stroke."""
    from PIL import Image, ImageDraw, ImageFont
    words = [w for w in json.load(open(os.path.join(HERE, "vo_final.words.json")))["words"]
             if w.get("type") == "word"]
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 62)
    cdir = os.path.join(WORK, "caps")
    shutil.rmtree(cdir, ignore_errors=True)
    os.makedirs(cdir)
    # Group up to 4 words, but never carry a card across a sentence boundary.
    groups, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) == 4 or w["text"].rstrip().endswith((".", "!", "?")):
            groups.append(cur); cur = []
    if cur:
        groups.append(cur)

    cards = []
    for i, grp in enumerate(groups):
        text = " ".join(w["text"] for w in grp)
        img = Image.new("RGBA", (W, 200), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        bb = d.textbbox((0, 0), text, font=font, stroke_width=6)
        d.text(((W - (bb[2] - bb[0])) / 2 - bb[0], (200 - (bb[3] - bb[1])) / 2 - bb[1]),
               text, font=font, fill=(255, 255, 255, 255),
               stroke_width=6, stroke_fill=(0, 0, 0, 235))
        p = os.path.join(cdir, f"c{i:03d}.png")
        img.save(p)
        cards.append((grp[0]["start"], grp[-1]["end"] + 0.06, p))
    return cards

def composite(base, keyed, cards):
    inputs = ["-i", base, "-c:v", "libvpx-vp9", "-i", keyed, "-i", os.path.join(HERE, "vo_final.mp3")]
    for _, _, p in cards:
        inputs += ["-i", p]

    # creator PiP: 44% of frame width, flush to the bottom-left corner
    pw = int(W * 0.44)
    fc = [f"[1:v]scale={pw}:-1[av]",
          f"[0:v][av]overlay=x=0:y=H-h:format=auto[v0]"]
    prev = "v0"
    for n, (s, e, _) in enumerate(cards):
        idx = 3 + n
        nxt = f"v{n+1}"
        fc.append(f"[{prev}][{idx}:v]overlay=x=(W-w)/2:y=812:"
                  f"enable='between(t,{s:.3f},{e:.3f})'[{nxt}]")
        prev = nxt
    out = os.path.join(HERE, "VEL-WEEKENDER-UGC-BLK-01-wont-be-careful.mp4")
    run(["ffmpeg", "-y", "-v", "error"] + inputs +
        ["-filter_complex", ";".join(fc), "-map", f"[{prev}]", "-map", "2:a",
         "-c:v", "libx264", "-crf", "18", "-preset", "slow", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", "-shortest", out])
    return out

if __name__ == "__main__":
    stage = sys.argv[1] if len(sys.argv) > 1 else "all"
    base = os.path.join(WORK, "base.mp4")
    keyed = os.path.join(WORK, "avatar_keyed.webm")
    if stage in ("all", "beats"):
        base = cut_beats(); print("base ok")
    if stage in ("all", "key"):
        keyed = key_avatar(); print("key ok")
    if stage in ("all", "comp"):
        print(composite(base, keyed, caption_cards()))
