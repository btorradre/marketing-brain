#!/usr/bin/env python3
"""Build the 79.2s b-roll bed for VEL-WEEKENDER-GS-BIRKIN-01.

Main frame is bag-and-hands only for the whole runtime: the b-roll model's face
must never appear, or it competes with the keyed presenter (one-creator lock).
b14 is the one carry/walk shot that contains a face, so it is punched in and
offset to sit below the chin.
"""
import json, os, subprocess, sys

ROOT = "/Users/brooksorradre2/Documents/marketing brain"
CON = os.path.join(ROOT, "brands/velantra/products/weekender/concepts/8-21-26-birkin-greenscreen")
BROLL = os.path.join(ROOT, "brands/velantra/products/weekender/broll")
PDP = os.path.join(CON, "production/pdp")
OUT = os.path.join(CON, "production/beats")
os.makedirs(OUT, exist_ok=True)

W, H, FPS = 1080, 1920, 25

# beat: (start, end) from the VO alignment of take 2
T = [0.00, 2.92, 5.64, 9.68, 13.40, 16.43, 19.01, 22.32, 27.68, 31.34, 36.44,
     40.60, 44.77, 50.44, 55.91, 58.25, 60.77, 62.28, 65.07, 71.81, 77.68, 79.201]

# (beat, kind, source, in-point, extra filter)
PLAN = [
    ("b01", "broll", "onroute-S5",    0.5, None),
    ("b02", "broll", "lc-travel-S12", 0.5, None),
    ("b03", "broll", "lc-travel-S17", 0.5, None),
    ("b04", "broll", "lc-travel-S11", 0.5, None),
    ("b05", "broll", "lc-travel-S03", 0.5, None),
    ("b06", "broll", "lc-travel-S04", 0.5, None),
    ("b07", "broll", "lc-travel-S09", 0.5, None),   # MECHANISM: bag on the carry-on
    ("b08", "broll", "onroute-S2",    0.3, None),   # laptop going in
    ("b09", "broll", "lc-travel-S08", 0.3, None),   # open + packed
    ("b10", "broll", "onroute-S3",    0.3, None),   # hands packing, caramel interior
    ("b11", "broll", "lc-travel-S08", 5.0, None),   # flap folded back (later moment)
    ("b12", "broll", "onroute-S5",    5.0, None),
    ("b13", "still", "overhead-bin",  0.0, None),   # the one new generation
    # b14 carries a face: punch in and push down so the head is out of frame
    ("b14", "broll", "lc-travel-S02", 1.0, "scale=1512:2688,crop=1080:1920:216:660"),
    ("b15", "broll", "onroute-S4",    0.5, None),   # macro hardware
    ("b16", "broll", "lc-travel-S05", 0.5, None),   # macro leather, no logo
    ("b17", "pdp",   "b17_swatches",  0.0, None),
    ("b18", "pdp",   "b18_price",     0.0, None),
    ("b19", "broll", "lc-travel-S12", 5.0, None),
    ("b20", "pdp",   "b20_scroll",    0.0, None),
    ("b21", "pdp",   "b21_cart",      0.0, None),
]

BASE = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}"


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("FFMPEG FAIL:", " ".join(cmd[:12]), file=sys.stderr)
        print(r.stderr[-700:], file=sys.stderr)
    return r.returncode == 0


made, missing = [], []
for i, (beat, kind, src, ss, extra) in enumerate(PLAN):
    dur = round(T[i + 1] - T[i], 3)
    dst = os.path.join(OUT, f"{beat}.mp4")

    if kind == "broll":
        srcpath = os.path.join(BROLL, src + ".mp4")
        vf = (extra or BASE) + f",fps={FPS},format=yuv420p"
        ok = run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error",
                  "-ss", str(ss), "-i", srcpath, "-t", str(dur),
                  "-vf", vf, "-an", dst])
    elif kind == "pdp":
        srcpath = os.path.join(PDP, src + ".mp4")
        ok = run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error",
                  "-i", srcpath, "-t", str(dur),
                  "-vf", f"{BASE},fps={FPS},format=yuv420p", "-an", dst])
    else:  # still with a slow push-in
        stills = os.path.join(CON, "production/stills", src + ".png")
        if not os.path.exists(stills):
            missing.append(beat)
            print(f"{beat}: MISSING still {stills}")
            continue
        vf = (f"scale={int(W*1.16)}:{int(H*1.16)}:force_original_aspect_ratio=increase,"
              f"crop={W}:{H}:'(iw-{W})/2+(t/{dur})*40':'(ih-{H})/2'"
              f",fps={FPS},format=yuv420p")
        ok = run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error",
                  "-loop", "1", "-i", stills, "-t", str(dur), "-vf", vf, "-an", dst])

    if kind != "still" or beat not in missing:
        if ok:
            made.append(beat)
            print(f"{beat}: {dur:5.2f}s  <- {src}")

print(f"\nbuilt {len(made)}/{len(PLAN)}; missing={missing}")
json.dump({"T": T, "plan": [p[0] for p in PLAN], "missing": missing},
          open(os.path.join(OUT, "_manifest.json"), "w"), indent=1)
