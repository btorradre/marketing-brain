#!/usr/bin/env python3
"""Assemble the Vellatini-replication 'details pack' ads.

Structure is a 1:1 port of TrendTrack vellatini-Uzptt3:
  A arrival 0.00-3.30 | B settle 3.30-7.20 | C pack block 7.20-14.80 | D depart 14.80-20.00

Act C is seven locked GPT Image 2 stills, hard cut, ~1.086s each — never animated
(Weekender open-bag law + Omni Colette strap/belt mutation).
Every segment gets the mandatory degrade pass; no vignette.
Master is delivered SILENT: trending audio is selected in-platform at upload.
"""
import os
import subprocess
import sys

W = "/private/tmp/claude-503/-Users-brooksorradre2-Documents-marketing-brain/b16ffd58-65c2-46a4-81f8-4d8d6f55cdd7/scratchpad/vellatini-uzptt3"
PROD = "/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products"
SEG = f"{W}/build/seg"
os.makedirs(SEG, exist_ok=True)

# raw iPhone finishing layer — flat and slightly lifted, never graded
DEGRADE = (
    "unsharp=5:5:-0.3,noise=alls=8:allf=t+u,rgbashift=rh=1:bv=1:edge=smear,"
    "eq=contrast=0.98:saturation=0.95:brightness=0.012:gamma=1.03"
)
FIT = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30"

PACK_N = 7
PACK_DUR = 7.60 / PACK_N  # 1.0857s


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("FAILED:", " ".join(cmd[:12]), file=sys.stderr)
        print(r.stderr[-1500:], file=sys.stderr)
        sys.exit(1)


def clip(src, start, dur, out):
    """Trim a library clip to length, fit 1080x1920, degrade."""
    run(["ffmpeg", "-v", "error", "-ss", str(start), "-t", str(dur), "-i", src,
         "-vf", f"{FIT},{DEGRADE}", "-an",
         "-c:v", "libx264", "-crf", "23", "-preset", "medium", "-pix_fmt", "yuv420p",
         out, "-y"])


def still(src, dur, out, zoom_to=1.025):
    """Hold a pack still with a very slight push-in, then degrade.

    Every still starts at the same scale so the seven hard cuts read as one
    locked camera rather than as drifting framing.
    """
    frames = max(2, int(round(dur * 30)))
    zp = (zoom_to - 1.0) / frames
    vf = (
        f"scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,"
        f"zoompan=z='min(1+{zp:.6f}*on,{zoom_to})':d={frames}:x='iw/2-(iw/zoom/2)':"
        f"y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30,setsar=1,{DEGRADE}"
    )
    run(["ffmpeg", "-v", "error", "-loop", "1", "-i", src, "-t", str(dur),
         "-vf", vf, "-an",
         "-c:v", "libx264", "-crf", "23", "-preset", "medium", "-pix_fmt", "yuv420p",
         out, "-y"])


def mix_audio(vo, bed, vo_end, total, out):
    """VO in front, bed ducked underneath it, bed up once the VO finishes.

    Mirrors the reference: the voice front-loads the argument alone, then the
    track takes over for the demonstration. One continuous VO take, never
    stitched per line.
    """
    duck, ramp = 0.17, 1.20
    bed_vol = (f"volume='if(lt(t,{vo_end}),{duck},"
               f"{duck}+{1-duck:.2f}*min(1,(t-{vo_end})/{ramp}))':eval=frame")
    run(["ffmpeg", "-v", "error", "-i", bed, "-i", vo,
         "-filter_complex",
         f"[0:a]atrim=0:{total},asetpts=N/SR/TB,{bed_vol}[b];"
         f"[1:a]adelay=0|0,apad=whole_dur={total},atrim=0:{total},asetpts=N/SR/TB,volume=1.0[v];"
         f"[b][v]amix=inputs=2:duration=first:normalize=0[m];"
         f"[m]loudnorm=I=-14:TP=-1.5:LRA=11[a]",
         "-map", "[a]", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", out, "-y"])


def assemble(tag, edl, packs, caps, out, audio=None):
    """edl: list of (name, src, start, dur). packs: 7 still paths.
    caps: list of (png, t_in, t_out). audio: (vo, bed, vo_end) or None."""
    parts = []
    for i, (name, src, start, dur) in enumerate(edl):
        p = f"{SEG}/{tag}_{i:02d}_{name}.mp4"
        if src == "PACK":
            still(packs[int(name[-1]) - 1], dur, p)
        else:
            clip(src, start, dur, p)
        parts.append(p)
        print("  seg", name, f"{dur:.3f}s")

    lst = f"{W}/build/{tag}_concat.txt"
    with open(lst, "w") as f:
        for p in parts:
            f.write(f"file '{p}'\n")
    joined = f"{W}/build/{tag}_joined.mp4"
    run(["ffmpeg", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst,
         "-c", "copy", joined, "-y"])

    # burn the overlay text windows
    inputs = ["-i", joined]
    for png, _, _ in caps:
        inputs += ["-i", png]
    fc, cur = [], "[0:v]"
    for i, (_, tin, tout) in enumerate(caps):
        nxt = f"[v{i}]"
        fc.append(f"{cur}[{i+1}:v]overlay=0:0:enable='between(t,{tin},{tout})'{nxt}")
        cur = nxt
    silent = f"{W}/build/{tag}_captioned.mp4"
    run(["ffmpeg", "-v", "error"] + inputs + [
        "-filter_complex", ";".join(fc), "-map", cur,
        "-c:v", "libx264", "-crf", "20", "-preset", "slow", "-pix_fmt", "yuv420p",
        "-movflags", "+faststart", "-an", silent, "-y"])

    if not audio:
        os.replace(silent, out)
        print("BUILT (silent)", out)
        return

    vo, bed, vo_end = audio
    total = float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", silent], capture_output=True, text=True).stdout.strip())
    track = f"{W}/build/{tag}_audio.m4a"
    mix_audio(vo, bed, vo_end, total, track)
    run(["ffmpeg", "-v", "error", "-i", silent, "-i", track,
         "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "copy",
         "-shortest", "-movflags", "+faststart", out, "-y"])
    print("BUILT", out)


# ---------------------------------------------------------------- Weekender
WK = f"{PROD}/weekender/broll"
wk_edl = [
    ("A1", f"{WK}/lc-travel-S13.mp4", 2.0, 1.10),   # walks in carrying the bag
    ("A2", f"{WK}/lc-travel-S02.mp4", 3.0, 1.10),   # carrying it through the room
    ("A3", f"{WK}/lc-travel-S11.mp4", 1.0, 1.10),   # sets it on the bed
    ("B1", f"{WK}/lc-travel-S06.mp4", 2.0, 1.30),   # hand resting on it
    ("B2", f"{WK}/lc-travel-S05.mp4", 2.0, 1.30),   # macro, the details beat
    ("B3", f"{WK}/lc-travel-S07.mp4", 2.0, 1.30),   # she looks at it, still closed
    ("PACK1", "PACK", 0, PACK_DUR), ("PACK2", "PACK", 0, PACK_DUR),
    ("PACK3", "PACK", 0, PACK_DUR), ("PACK4", "PACK", 0, PACK_DUR),
    ("PACK5", "PACK", 0, PACK_DUR), ("PACK6", "PACK", 0, PACK_DUR),
    ("PACK7", "PACK", 0, PACK_DUR),
    ("D1", f"{WK}/lc-travel-S08.mp4", 0.5, 1.30),   # packed, open on the bed
    ("D2", f"{WK}/lc-travel-S09.mp4", 2.0, 1.30),   # closed, on the carry-on
    ("D3", f"{WK}/lc-travel-S10.mp4", 2.0, 1.30),   # her, bag and carry-on
    ("D4", f"{WK}/lc-travel-S16.mp4", 2.0, 1.30),   # out the door
]
wk_packs = [f"{W}/gen/wk_C{i}.png" for i in range(1, 8)]
# caption windows are driven off the picked VO take's real word timings
# (take2: L1 0.08-2.82, L2 3.80-5.36), mirroring the reference where the text
# appears with the spoken line and then lingers.
wk_caps = [(f"{W}/cap_wk_l1.png", 0.0, 3.48), (f"{W}/cap_wk_l2.png", 3.90, 21.0)]
wk_audio = (f"{W}/vo/wk_take2.mp3", f"{W}/music/wk_bed_a.mp3", 5.36)

# ------------------------------------------------------------------ Colette
CL = f"{PROD}/cashmere-tote/broll/library-2026-08/clips"
col_edl = [
    ("A1", f"{CL}/VEL-COL-003-street-coffee-run.mp4", 0.8, 1.10),
    ("A2", f"{CL}/VEL-COL-015-street-phone-check.mp4", 2.0, 1.10),
    ("A3", f"{CL}/VEL-COL-019-cafe-bistro-chair.mp4", 1.0, 1.10),
    ("B1", f"{CL}/VEL-COL-025-cafe-communal-table.mp4", 2.0, 1.30),
    ("B2", f"{CL}/VEL-COL-020-cafe-table-beside-latte.mp4", 2.0, 1.30),
    ("B3", f"{CL}/VEL-COL-076-macro-gold-disc.mp4", 2.0, 1.30),   # lands under "the details"
    ("PACK1", "PACK", 0, PACK_DUR), ("PACK2", "PACK", 0, PACK_DUR),
    ("PACK3", "PACK", 0, PACK_DUR), ("PACK4", "PACK", 0, PACK_DUR),
    ("PACK5", "PACK", 0, PACK_DUR), ("PACK6", "PACK", 0, PACK_DUR),
    ("PACK7", "PACK", 0, PACK_DUR),
    ("D1", f"{CL}/VEL-COL-052-open-overhead-cafe.mp4", 0.5, 1.30),    # packed, the payoff
    ("D2", f"{CL}/VEL-COL-081-macro-hand-on-handle.mp4", 2.0, 1.30),  # the lift
    ("D3", f"{CL}/VEL-COL-026-cafe-checkout-set-down.mp4", 2.0, 1.30),
    ("D4", f"{CL}/VEL-COL-010-street-bakery-door.mp4", 2.0, 1.30),
]
col_packs = [f"{W}/gen/col_C{i}.png" for i in range(1, 8)]
# take1 word timings: L1 0.12-3.82, L2 4.80-6.68
col_caps = [
    (f"{W}/cap_col_l1.png", 0.0, 4.48),
    (f"{W}/cap_col_l2.png", 4.92, 21.0),
    (f"{W}/cap_col_preorder.png", 17.40, 21.0),
]
col_audio = (f"{W}/vo/col_take1.mp3", f"{W}/music/col_bed_a.mp3", 6.68)

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "both"
    if which in ("both", "wk"):
        print("Weekender:")
        assemble("wk", wk_edl, wk_packs, wk_caps,
                 f"{PROD}/weekender/video/VEL-WEEKENDER-DETAILSPACK-01-three-days-one-bag.mp4",
                 audio=wk_audio)
    if which in ("both", "col"):
        print("Colette:")
        assemble("col", col_edl, col_packs, col_caps,
                 f"{PROD}/cashmere-tote/video/VEL-COLETTE-DETAILSPACK-01-the-details.mp4",
                 audio=col_audio)
