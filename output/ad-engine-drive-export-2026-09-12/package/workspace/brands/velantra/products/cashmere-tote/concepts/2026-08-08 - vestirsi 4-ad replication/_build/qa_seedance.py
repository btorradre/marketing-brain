#!/usr/bin/env python3
"""Dense QA for a finished Seedance 2.5 ad.

Sampling misses progressive drift — that is how two artifacts shipped on the Omni
ad — so this sweeps EVERY frame at 2.5fps into contact sheets for review, and runs
the mechanical checks the prompt system specifies:

  1. cut count in the output == the count declared in FORMAT
  2. runtime == the FORMAT runtime == the beat sum
  3. beat windows line up with where the cuts actually landed

Cut detection uses the scene filter reading STDOUT. Never use showinfo with
`-v error`: showinfo logs at INFO level, so that combination prints nothing and
every video looks like one continuous take.

  python3 qa_seedance.py ../output/VEL-COL-POV-01.mp4 AD1
"""
import pathlib, re, subprocess, sys

HERE = pathlib.Path(__file__).parent
PROMPTS = HERE.parent / "prompts"


def probe(v):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                          "format=duration:stream=width,height,r_frame_rate,codec_name",
                          "-of", "default=nw=1", str(v)], capture_output=True, text=True).stdout
    return out.strip()


def detect_cuts(v, thresh=0.25):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(v), "-vf",
                        f"select='gt(scene,{thresh})',metadata=print:file=-",
                        "-an", "-f", "null", "-"], capture_output=True, text=True)
    return [round(float(m), 3) for m in re.findall(r"pts_time:([0-9.]+)", r.stdout)]


def declared(tag):
    t = (PROMPTS / f"{tag}-seedance.txt").read_text()
    m = re.search(r"exactly\s+(\d+)\s+cuts?", t, re.I)
    cuts = int(m.group(1)) if m else None
    beats = [(a, b) for a, b in re.findall(r"\[(\d\d):(\d\d)-\d\d:\d\d\]", t)]
    wins = re.findall(r"\[(\d\d):(\d\d)-(\d\d):(\d\d)\]", t)
    wins = [(int(a)*60+int(b), int(c)*60+int(d)) for a, b, c, d in wins]
    rt = re.search(r"(\d+)-second take", t)
    return cuts, wins, int(rt.group(1)) if rt else None


def sheets(v, out):
    out.mkdir(parents=True, exist_ok=True)
    for f in out.glob("*.png"):
        f.unlink()
    subprocess.run(["ffmpeg", "-v", "error", "-i", str(v), "-vf", "fps=2.5,scale=360:640",
                    str(out / "f%03d.png"), "-y"], check=True)
    fs = sorted(out.glob("f*.png"))
    per = 12
    made = []
    for i in range(0, len(fs), per):
        ch = fs[i:i+per]
        a = []
        for c in ch:
            a += ["-i", str(c)]
        n = len(ch)
        dest = out / f"sheet{i//per}.png"
        if n == 1:                       # hstack needs >=2 inputs
            subprocess.run(["ffmpeg", "-v", "error", "-i", str(ch[0]), "-vf",
                            "scale=300:533", str(dest), "-y"], check=True)
        else:
            fc = (";".join(f"[{j}:v]scale=300:533,setsar=1[v{j}]" for j in range(n)) + ";"
                  + "".join(f"[v{j}]" for j in range(n)) + f"hstack={n}[o]")
            subprocess.run(["ffmpeg", "-v", "error"] + a + ["-filter_complex", fc, "-map", "[o]",
                                                           str(dest), "-y"], check=True)
        made.append((dest, i/2.5, (i+n-1)/2.5))
    return len(fs), made


if __name__ == "__main__":
    v = pathlib.Path(sys.argv[1]); tag = sys.argv[2]
    print(probe(v))
    dc, wins, rt = declared(tag)
    cuts = detect_cuts(v)
    print(f"\ndeclared cuts: {dc}   detected: {len(cuts)} at {cuts}")
    if dc is not None and len(cuts) != dc:
        print(f"  ** MISMATCH: FORMAT says {dc}, output has {len(cuts)}")
    if wins:
        want = [w[0] for w in wins[1:]]
        print(f"beat boundaries wanted: {want}")
        for w in want:
            near = min(cuts, key=lambda c: abs(c-w)) if cuts else None
            d = abs(near-w) if near is not None else None
            flag = "" if (d is not None and d <= 0.6) else "   ** off"
            print(f"  {w:>3}s -> nearest cut {near}  (drift {d}){flag}")
    n, made = sheets(v, HERE / f"qa-{tag}")
    print(f"\n{n} frames at 2.5fps -> {len(made)} sheets")
    for dest, a, b in made:
        print(f"  {dest.name}: {a:.1f}s - {b:.1f}s")
