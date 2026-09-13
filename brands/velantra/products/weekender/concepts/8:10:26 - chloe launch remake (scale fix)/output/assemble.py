#!/usr/bin/env python3
"""DC-02 assembly. Usage:
  python3 assemble.py kenburns <s2_keyframe_pick.png>   # build s2_kenburns.mp4 (8s push-in) + VO
  python3 assemble.py s3                                # mux VO onto s3_broll_trim.mp4
  python3 assemble.py final                             # caption S1, stitch 1-5, export final
All VO patches gain-matched to S1 native audio when s1 exists.
"""
import os, subprocess, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
FF = ["ffmpeg", "-v", "error", "-y"]

def run(cmd):
    print(" ".join(str(c) for c in cmd)[:160])
    subprocess.run([str(c) for c in cmd], check=True)

def kenburns(pick):
    # 8s slow push-in 1.0 -> 1.12, 720x1280@24, then lay vo_s2 over it
    z = "min(zoom+0.0006,1.12)"
    run(FF + ["-loop", "1", "-i", pick, "-filter_complex",
        f"[0:v]scale=1440:2560,zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=192:s=1440x2560:fps=24,scale=720:1280[v]",
        "-map", "[v]", "-t", "8", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
        ROOT / "s2_kenburns_silent.mp4"])
    run(FF + ["-i", ROOT / "s2_kenburns_silent.mp4", "-i", ROOT / "vo_s2_take1.mp3",
        "-filter_complex", "[1:a]adelay=250|250,apad[a]",
        "-map", "0:v", "-map", "[a]", "-t", "8",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", ROOT / "seg_02.mp4"])
    print("seg_02.mp4 built")

def s3():
    run(FF + ["-i", ROOT / "s3_broll_trim.mp4", "-i", ROOT / "vo_s3_take1.mp3",
        "-filter_complex", "[1:a]adelay=300|300,apad[a]",
        "-map", "0:v", "-map", "[a]", "-t", "7",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", ROOT / "seg_03.mp4"])
    print("seg_03.mp4 built")

def final():
    # 1) caption overlay on S1 (first 3.5s fade)
    s1 = ROOT / "seg_01.mp4"
    if not s1.exists():
        sys.exit("seg_01.mp4 missing (Seedance not fired yet)")
    run(FF + ["-i", s1, "-i", ROOT / "caption_weekender.png",
        "-filter_complex",
        "[1:v]format=rgba,fade=t=out:st=3:d=0.5:alpha=1[cap];[0:v][cap]overlay=(W-w)/2:H*0.86:enable='lte(t,3.5)'[v]",
        "-map", "[v]", "-map", "0:a", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "copy", ROOT / "seg_01_cap.mp4"])
    # 2) S5: mux clone VO over the silent chain clip
    s5src = ROOT / "s5" / "seg_01.mp4"
    if s5src.exists():
        run(FF + ["-i", s5src, "-i", ROOT / "vo_s5_take1.mp3",
            "-filter_complex", "[0:a]volume=0.35[amb];[1:a]adelay=250|250[vo];[amb][vo]amix=inputs=2:duration=first:dropout_transition=0[a]",
            "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
            ROOT / "seg_05.mp4"])
    # 3) stitch
    order = ["seg_01_cap.mp4", "seg_02.mp4", "seg_03.mp4", "seg_04.mp4", "seg_05.mp4"]
    missing = [f for f in order if not (ROOT / f).exists()]
    if missing:
        sys.exit("missing segments: %s" % missing)
    norm = []
    for i, f in enumerate(order):
        n = ROOT / ("n_%d.mp4" % i)
        run(FF + ["-i", ROOT / f, "-vf", "scale=720:1280,fps=24,setsar=1",
            "-af", "aresample=48000,aformat=channel_layouts=stereo",
            "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", n])
        norm.append(n)
    concat = ROOT / "concat.txt"
    concat.write_text("".join("file '%s'\n" % n for n in norm))
    run(FF + ["-f", "concat", "-safe", "0", "-i", concat, "-c", "copy",
        ROOT / "VEL-WEEKENDER-CHLOE-DC-02-final.mp4"])
    print("FINAL: VEL-WEEKENDER-CHLOE-DC-02-final.mp4")

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "kenburns":
        kenburns(sys.argv[2])
    elif cmd == "s3":
        s3()
    elif cmd == "final":
        final()
    else:
        sys.exit(__doc__)
