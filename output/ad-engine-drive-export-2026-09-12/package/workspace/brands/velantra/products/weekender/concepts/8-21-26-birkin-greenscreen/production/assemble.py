#!/usr/bin/env python3
"""Assemble VEL-WEEKENDER-GS-BIRKIN-01: bed + keyed creator PiP + captions + VO.

Per-creator source handling:
  whitney - native green screen from HeyGen, keyed with chromakey. Her garment is
            cream linen, so despill stays low (0.5 renders cream visibly pink).
  brooks  - shot in a car, matted by fal BEN2 to a transparent webm.
  anna    - shot in a hallway, matted by fal BEN2 to a transparent webm.

PiP is 32% of frame width, bottom-left anchored, per the sizing law: the b-roll
is the ad, the creator is a corner presence.
"""
import os, shutil, subprocess, sys

CON = ("/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/"
       "weekender/concepts/8-21-26-birkin-greenscreen")
ENG = "/Users/brooksorradre2/Documents/marketing brain/_engine/mcp/ad-engine/data/vo"

# VARIANT=tof builds the 63.4s cold cut: four lines trimmed, 19 beats instead of
# 21, its own VO and caption track, and the avatars re-lipsynced to that VO
# (splicing the long take would break the one-take audio law and show as a jump).
VARIANT = os.environ.get("VARIANT", "long")
if VARIANT == "tof":
    BEATS = os.path.join(CON, "production/beats_tof")
    CAPS = os.path.join(CON, "production/captions_tof.webm")
    VO = os.path.join(ENG, "job_19f191dbc5ad/voiceover.mp3")
    NBEATS, SUFFIX, AVSUF = 19, "-TOF", "_tof"
else:
    BEATS = os.path.join(CON, "production/beats")
    CAPS = os.path.join(CON, "production/captions.webm")
    VO = os.path.join(ENG, "job_31089bb431af/voiceover.mp3")
    NBEATS, SUFFIX, AVSUF = 21, "", ""

AV = os.path.join(CON, "production/avatars")
OUT = os.path.join(CON, "production/out")
os.makedirs(OUT, exist_ok=True)

W, H = 1080, 1920
PIP_W = int(W * 0.32)          # ~345px, matching the reference ad's corner presence
ORDER = [f"b{i:02d}" for i in range(1, NBEATS + 1)]

# name -> (source file, key filter chain, pre-crop applied before PiP scaling)
#
# whitney renders on a native green screen. Her green is 0x0AA442, NOT the
# 0x007A28 from the DC/BLK builds, so it was swept fresh: alpha is stable
# 0.06-0.14 with the cliff at 0.18. Despill stays low because her cream linen
# shirt goes visibly pink at 0.5.
#
# anna and brooks had no green screen (hallway / car) and were matted by fal,
# which returns the subject on BLACK rather than with an alpha channel. Keying
# that black has to stay very tight: anna's dark brown hair starts keying out
# above similarity 0.01, and by 0.28 her hair and eyes are gone.
SRC = {
    "long": {"whitney": "whitney.mp4",
             "anna": "anna_matte.webm",
             "brooks": "brooks_matte.webm"},
    "tof":  {"whitney": "whitney_tof.mp4",
             "anna": "anna_tof_matte.mp4",
             "brooks": "brooks_tof_matte.mp4"},
}

CREATORS = {
    "whitney": (None,
                "chromakey=0x0AA442:0.10:0.02,despill=type=green:mix=0.15",
                None),
    "anna":    (None,
                "colorkey=0x000000:0.01:0.02",
                None),
    # brooks was shot in a car and BEN2 only darkened the interior rather than
    # removing it, leaving ghosted roof/window structure. She is blonde in a pale
    # sweater, so unlike anna she tolerates an aggressive black key: at 0.20 the
    # leftover car is 99.7% gone with only edge-level loss on her.
    "brooks":  (None,
                "colorkey=0x000000:0.20:0.05",
                "crop=iw*0.56:ih*0.62:iw*0.14:ih*0.36"),
}


def run(cmd, label):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"FAIL {label}:\n{r.stderr[-1200:]}", file=sys.stderr)
        return False
    return True


def build_bed():
    bed = os.path.join(CON, f"production/bed{SUFFIX or ''}.mp4")
    lst = os.path.join(CON, f"production/_concat{SUFFIX or ''}.txt")
    missing = [b for b in ORDER if not os.path.exists(os.path.join(BEATS, b + ".mp4"))]
    if missing:
        print("cannot build bed, missing beats:", missing); return None
    with open(lst, "w") as f:
        for b in ORDER:
            f.write(f"file '{os.path.join(BEATS, b + '.mp4')}'\n")
    ok = run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-f", "concat",
              "-safe", "0", "-i", lst, "-c:v", "libx264", "-crf", "18",
              "-pix_fmt", "yuv420p", "-r", "25", bed], "bed")
    return bed if ok else None


def build_one(name, bed):
    _, keychain, precrop = CREATORS[name]
    src = SRC[VARIANT][name]
    srcpath = os.path.join(AV, src)
    if not os.path.exists(srcpath):
        print(f"skip {name}: no {src}"); return None
    dst = os.path.join(OUT, f"VEL-WEEKENDER-GS-BIRKIN-01{SUFFIX}-{name}.mp4")

    chain = [keychain]
    if precrop:
        chain.append(precrop)
    chain.append(f"scale={PIP_W}:-2")
    cf = (f"[1:v]format=rgba,{','.join(chain)}[pip];"
          f"[0:v][pip]overlay=0:H-h:format=auto[v0];"
          f"[v0][2:v]overlay=0:0:format=auto[v]")

    # VP9 alpha must be force-decoded or ffmpeg silently drops the alpha plane
    # and the layer renders as an opaque box.
    # the fal mattes carry a .webm name but are actually h264 mp4, so probe
    # rather than trusting the extension
    import subprocess as _sp
    _pf = _sp.run(["ffprobe","-v","error","-select_streams","v:0",
                   "-show_entries","stream=codec_name","-of","csv=p=0",srcpath],
                  capture_output=True,text=True).stdout.strip()
    dec = ["-c:v","libvpx-vp9"] if _pf.startswith("vp9") else []
    cmd = (["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-i", bed]
           + dec + ["-i", srcpath,
                    "-c:v", "libvpx-vp9", "-i", CAPS,
                    "-i", VO,
                    "-filter_complex", cf, "-map", "[v]", "-map", "3:a",
                    "-c:v", "libx264", "-crf", "19", "-preset", "medium",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", dst])
    if run(cmd, name):
        d = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                            "format=duration", "-of", "csv=p=0", dst],
                           capture_output=True, text=True).stdout.strip()
        print(f"  {name}: {dst}  ({float(d):.2f}s, {os.path.getsize(dst)/1e6:.1f}MB)")
        return dst
    return None


if __name__ == "__main__":
    bed = build_bed()
    if not bed:
        sys.exit(1)
    print("bed built")
    targets = sys.argv[1:] or list(CREATORS)
    for n in targets:
        build_one(n, bed)
