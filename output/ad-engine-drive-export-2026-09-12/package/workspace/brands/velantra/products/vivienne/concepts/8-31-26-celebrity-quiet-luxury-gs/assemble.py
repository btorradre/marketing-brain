#!/usr/bin/env python3
"""Assemble VEL-VIV-CELEB-GS-01: bed + keyed creator PiP + captions + VO.

One shared VO drives all three creators, so bed, captions and every timing are
identical and ONLY the creator changes - a clean creator-only A/B/C.

PiP is 32% of frame width, bottom-anchored, and alternates side per cut off the
beat map. Captions overlay LAST so type always sits above the creator.
"""
import json, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROD = HERE / "production"
REN  = HERE / "creator-renders"
OUT  = PROD / "out"; OUT.mkdir(parents=True, exist_ok=True)
VO   = Path("/Users/brooksorradre2/Documents/marketing brain/_engine/mcp/ad-engine/data/vo/job_f97a185c38d2/voiceover.mp3")
W, H, FPS = 1080, 1920, 24
GEO = json.load(open(HERE / "pip-geometry.json"))   # per-creator, solved in pip_geometry.py

def ranges(beats, side):
    """ffmpeg enable expression: '+' is OR. Half-frame pad so no cut shows a gap."""
    r = [b for b in beats if b["pip"] == side]
    if not r: return "0"
    return "+".join(f"between(t,{b['in']:.3f},{b['out']+0.021:.3f})" for b in r)

def build(name, beats):
    src = REN / f"{name}-alpha.webm"
    if not src.exists(): print(f"skip {name}: not keyed yet"); return None
    dst = OUT / f"VEL-VIV-CELEB-GS-01-{name}.mp4"
    swL, shL, xL, yL = GEO[name]["L"]
    _,   _,   xR, yR = GEO[name]["R"]
    # x and y are NEGATIVE / past the edge on purpose: the frame has to CUT her, or she
    # reads as a sticker pasted into the corner instead of a person standing in the shot.
    fc = (f"[1:v]scale={swL}:{shL},format=rgba,split=2[pl][pr];"
          f"[0:v][pl]overlay={xL}:{yL}:format=auto:enable='{ranges(beats,'L')}'[v1];"
          f"[v1][pr]overlay={xR}:{yR}:format=auto:enable='{ranges(beats,'R')}'[v2];"
          f"[v2][2:v]overlay=0:0:format=auto[v];"
          f"[3:a]loudnorm=I=-14:TP=-1.5:LRA=11[a]")
    cmd = ["ffmpeg","-nostdin","-y","-v","error",
           "-i",str(PROD/"bed.mp4"),
           "-c:v","libvpx-vp9","-i",str(src),          # VP9 alpha MUST be force-decoded
           "-c:v","libvpx-vp9","-i",str(PROD/"captions.webm"),
           "-i",str(VO),
           "-filter_complex",fc,"-map","[v]","-map","[a]",
           "-c:v","libx264","-crf","19","-preset","medium","-pix_fmt","yuv420p",
           "-r",str(FPS),"-c:a","aac","-b:a","192k","-shortest",str(dst)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: print(f"FAIL {name}:\n{r.stderr[-1500:]}"); return None
    d = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",
                        str(dst)],capture_output=True,text=True).stdout.strip()
    print(f"  {name}: {float(d):.2f}s  {dst.stat().st_size/1e6:.1f}MB  "
          f"PiP {swL}x{shL} cut {abs(min(xL,0))}px side / {yL+shL-H}px bottom  -> {dst.name}")
    return dst

if __name__ == "__main__":
    beats = json.load(open(HERE / "beat-map-final.json"))
    for n in (sys.argv[1:] or ["A-diane", "B-bridget", "C-marguerite"]):
        build(n, beats)
