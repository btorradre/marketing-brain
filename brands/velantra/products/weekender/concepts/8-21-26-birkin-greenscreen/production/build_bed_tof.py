#!/usr/bin/env python3
"""Build the 63.4s cold-TOF b-roll bed (19 beats).

Same sources and same laws as the long cut. Four lines were trimmed, which drops
two beats: the open-and-packed structure shot and the packed-beside-the-roller
shot. Every remaining claim keeps its own demo frame.

Main frame stays bag-and-hands only for the whole runtime; b12 is the one carry
shot containing a face and is punched in and pushed down to cut the head.
"""
import json, os, subprocess, sys

ROOT = "/Users/brooksorradre2/Documents/marketing brain"
CON = os.path.join(ROOT, "brands/velantra/products/weekender/concepts/8-21-26-birkin-greenscreen")
BROLL = os.path.join(ROOT, "brands/velantra/products/weekender/broll")
PDP = os.path.join(CON, "production/pdp")
OUT = os.path.join(CON, "production/beats_tof")
STILLS = os.path.join(CON, "production/stills")
os.makedirs(OUT, exist_ok=True)

W, H, FPS = 1080, 1920, 25
T = json.load(open("/tmp/tof_T.json"))

PLAN = [
    ("b01", "broll", "onroute-S5",    0.5, None),
    ("b02", "broll", "lc-travel-S12", 0.5, None),
    ("b03", "broll", "lc-travel-S17", 0.5, None),
    ("b04", "broll", "lc-travel-S11", 0.5, None),
    ("b05", "broll", "lc-travel-S03", 0.5, None),
    ("b06", "broll", "lc-travel-S04", 0.5, None),
    ("b07", "broll", "lc-travel-S09", 0.5, None),   # MECHANISM
    ("b08", "broll", "onroute-S2",    0.3, None),   # laptop going in
    ("b09", "broll", "onroute-S3",    0.3, None),   # caramel interior
    ("b10", "broll", "lc-travel-S08", 3.0, None),   # fold-back flap
    ("b11", "still", "overhead-bin",  0.0, None),
    ("b12", "broll", "lc-travel-S02", 1.0, "scale=1512:2688,crop=1080:1920:216:660"),
    ("b13", "broll", "onroute-S4",    0.5, None),   # macro hardware
    ("b14", "broll", "lc-travel-S05", 0.5, None),   # macro leather, no logo
    ("b15", "pdp",   "tof_swatches",  0.0, None),
    ("b16", "pdp",   "tof_price",     0.0, None),
    ("b17", "broll", "lc-travel-S12", 5.0, None),
    ("b18", "pdp",   "tof_scroll",    0.0, None),
    ("b19", "pdp",   "tof_cart",      0.0, None),
]

BASE = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}"
PDP_SRC = os.path.join(PDP, "pdp_1080.png")
# (name, y-start, y-end) windows on the 1080x6912 page capture
PDP_PANS = {
    "tof_swatches": (900, 965),
    "tof_price":    (800, 880),
    "tof_scroll":   (800, 1300),
    "tof_cart":     (1210, 1250),
}


def run(cmd, label):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"FAIL {label}: {r.stderr[-500:]}", file=sys.stderr)
    return r.returncode == 0


# rebuild the PDP pans at the TOF durations
for i, (beat, kind, src, _, _) in enumerate(PLAN):
    if kind != "pdp":
        continue
    dur = round(T[i + 1] - T[i], 3)
    y0, y1 = PDP_PANS[src]
    run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-loop", "1", "-i", PDP_SRC,
         "-t", str(dur), "-r", str(FPS),
         "-vf", f"crop=1080:1920:0:'{y0}+({y1}-{y0})*t/{dur}',format=yuv420p",
         "-an", os.path.join(PDP, src + ".mp4")], src)

made = []
for i, (beat, kind, src, ss, extra) in enumerate(PLAN):
    dur = round(T[i + 1] - T[i], 3)
    dst = os.path.join(OUT, f"{beat}.mp4")
    if kind == "broll":
        vf = (extra or BASE) + f",fps={FPS},format=yuv420p"
        ok = run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-ss", str(ss),
                  "-i", os.path.join(BROLL, src + ".mp4"), "-t", str(dur),
                  "-vf", vf, "-an", dst], beat)
    elif kind == "pdp":
        ok = run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error",
                  "-i", os.path.join(PDP, src + ".mp4"), "-t", str(dur),
                  "-vf", f"{BASE},fps={FPS},format=yuv420p", "-an", dst], beat)
    else:
        vf = (f"scale={int(W*1.16)}:{int(H*1.16)}:force_original_aspect_ratio=increase,"
              f"crop={W}:{H}:'(iw-{W})/2+(t/{dur})*40':'(ih-{H})/2',fps={FPS},format=yuv420p")
        ok = run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-loop", "1",
                  "-i", os.path.join(STILLS, src + ".png"), "-t", str(dur),
                  "-vf", vf, "-an", dst], beat)
    if ok:
        made.append(beat)
        print(f"{beat}: {dur:5.2f}s  <- {src}")

print(f"\nbuilt {len(made)}/{len(PLAN)}")
