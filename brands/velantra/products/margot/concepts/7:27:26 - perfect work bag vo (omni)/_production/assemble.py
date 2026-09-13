#!/usr/bin/env python3
"""VEL-MARGOT-PERFECT-VO-01 — assemble final cut.
Beats timed to vo/main-v3/voiceover.mp3 (28.2s master). Clips 720x1280@24 -> 1080x1920@24.
Stills 1152x2048 -> Ken Burns. Captions PIL (no drawtext/libass in this ffmpeg).
"""
import os, subprocess, sys

CD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(os.path.dirname(CD), "7:27:26 - tof ugc perfect work bag", "assets")
BROLL = os.path.join(ASSETS, "broll")
STILLS = os.path.join(ASSETS, "stills")
VO = os.path.join(CD, "vo", "main-v3", "voiceover.mp3")
WORK = os.path.join(CD, "_production", "work")
os.makedirs(WORK, exist_ok=True)
FPS = 24
W, H = 1080, 1920

def run(args):
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("FFMPEG FAIL: " + " ".join(args)[:200] + "\n" + r.stderr[-1500:])

# beat: (name, kind, source, dur, opts)
# kind clip: opts = (src_start, crop) where crop=None or (factor, xfrac, yfrac)
# kind still: opts = (z_from, z_to)  zoompan linear
BEATS = [
    ("b01", "clip", f"{BROLL}/scene03-office-walk/scene03-office-walk-var1.mp4", 3.10, (0.40, (0.74, 0.65, 0.24))),
    ("b02", "still", f"{STILLS}/slot02-burgundy-hero-v2.png", 1.90, (1.00, 1.10)),
    ("b03", "clip", f"{BROLL}/scene05-leather-macro/scene05-leather-macro-var1.mp4", 3.40, (0.40, None)),
    ("b04", "clip", f"{BROLL}/scene08-turnlock/scene08-turnlock-var1.mp4", 3.05, (0.40, None)),
    ("b05", "still", f"{STILLS}/slot06-burgundy-straighton-v2.png", 1.70, (1.00, 1.09)),
    ("b06", "clip", f"{BROLL}/scene07-laptop-in/scene07-laptop-in-var1.mp4", 2.40, (0.30, None)),
    ("b07", "still", f"{STILLS}/slot04-burgundy-onmodel-office-v1.png", 2.35, (1.08, 1.00)),
    ("b08", "still", f"{STILLS}/slot10-burgundy-closeup-v2.png", 3.85, (1.00, 1.12)),
    ("b09", "clip", f"{BROLL}/scene11-walking/scene11-walking-var1.mp4", 2.80, (0.50, (0.74, 0.35, 0.22))),
    ("b10", "still", f"{STILLS}/slot02-burgundy-hero-v2.png", 3.65, (1.12, 1.00)),
]

ENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS), "-an"]

def render_beats():
    total = 0.0
    for name, kind, src, dur, opts in BEATS:
        out = os.path.join(WORK, name + ".mp4")
        total += dur
        if os.path.exists(out):
            continue
        if kind == "clip":
            start, crop = opts
            vf = []
            if crop:
                f, xf, yf = crop
                vf.append(f"crop=w=iw*{f}:h=ih*{f}:x=(iw-iw*{f})*{xf}:y=ih*{yf}")
            vf.append(f"scale={W}:{H}:flags=lanczos")
            run(["ffmpeg", "-y", "-v", "error", "-ss", str(start), "-i", src,
                 "-t", str(dur), "-vf", ",".join(vf)] + ENC + [out])
        else:
            z0, z1 = opts
            n = int(round(dur * FPS))
            # upscale for zoom headroom, then zoompan; jitter-free x/y centering
            zexpr = f"{z0}+({z1}-{z0})*on/{max(n-1,1)}"
            vf = (f"scale=2160:3840:flags=lanczos,"
                  f"zoompan=z='{zexpr}':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d={n}:s={W}x{H}:fps={FPS}")
            run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", src,
                 "-t", str(dur), "-vf", vf, "-frames:v", str(n)] + ENC + [out])
        print(f"{name} rendered ({dur}s)")
    print(f"video total {total:.2f}s")

def concat():
    lst = os.path.join(WORK, "concat.txt")
    with open(lst, "w") as f:
        for name, *_ in [(b[0],) for b in BEATS]:
            f.write(f"file '{WORK}/{name}.mp4'\n")
    out = os.path.join(WORK, "master-video.mp4")
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst,
         "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS), "-an", out])
    print("concat done")
    return out

CARDS = [
    ("okay I think I found", 0.00, 1.15),
    ("the perfect work bag", 1.15, 3.10),
    ("and it almost feels illegal", 3.15, 4.95),
    ("structured leather with\na fine embossed grain", 5.05, 8.35),
    ("a belt strap and\na silver turn lock", 8.45, 11.40),
    ("it stands up on its own", 11.50, 13.20),
    ("it fits your laptop\nand your planner", 13.25, 15.55),
    ("and it goes with everything", 15.65, 16.60),
    ("you wear to work", 16.60, 17.90),
    ("would you believe me\nif I told you", 17.95, 19.55),
    ("it's under a hundred dollars", 19.65, 22.30),
    ("this is the Velantra Margot", 22.35, 24.60),
    ("comment MARGOT and\nI will send it", 24.70, 26.55),
    ("straight to your DMs", 26.60, 28.20),
]

def make_caption_pngs():
    from PIL import Image, ImageDraw, ImageFont
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf", 62)
    paths = []
    for i, (text, *_ ) in enumerate(CARDS):
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        lines = text.split("\n")
        line_h = 76
        y0 = int(H * 0.78) - (len(lines) * line_h) // 2
        for j, line in enumerate(lines):
            w = d.textlength(line, font=font)
            x = (W - w) // 2
            y = y0 + j * line_h
            d.text((x, y), line, font=font, fill="white", stroke_width=5, stroke_fill="black")
        p = os.path.join(WORK, f"cap{i:02d}.png")
        img.save(p)
        paths.append(p)
    print(f"{len(paths)} caption cards rendered")
    return paths

def burn_and_mux(master):
    caps = make_caption_pngs()
    inputs = ["-i", master]
    for p in caps:
        inputs += ["-i", p]
    chains, last = [], "0:v"
    for i, (text, t0, t1) in enumerate(CARDS):
        nxt = f"v{i}"
        chains.append(f"[{last}][{i+1}:v]overlay=0:0:enable='between(t,{t0},{t1})'[{nxt}]")
        last = nxt
    fc = ";".join(chains)
    withcaps = os.path.join(WORK, "master-captions.mp4")
    run(["ffmpeg", "-y", "-v", "error"] + inputs + ["-filter_complex", fc, "-map", f"[{last}]",
         "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-an", withcaps])
    print("captions burned")
    for src, out in [(withcaps, "VEL-MARGOT-PERFECT-VO-01-final.mp4"),
                     (master, "VEL-MARGOT-PERFECT-VO-01-final-nocaptions.mp4")]:
        run(["ffmpeg", "-y", "-v", "error", "-i", src, "-i", VO,
             "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-map", "0:v", "-map", "1:a",
             "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest",
             os.path.join(CD, out)])
        print("delivered " + out)

if __name__ == "__main__":
    render_beats()
    m = concat()
    burn_and_mux(m)
    print("DONE")
