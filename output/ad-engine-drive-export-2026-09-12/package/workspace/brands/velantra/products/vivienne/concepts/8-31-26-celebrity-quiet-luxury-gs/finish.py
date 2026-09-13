#!/usr/bin/env python3
"""Drive the rest of the run: download B/C when HeyGen finishes, key each plate,
assemble each ad. Serialised on purpose - VP9 alpha encoding is CPU bound and three
at once thrashes."""
import json, subprocess, time, sys, os
from pathlib import Path

HERE = Path(__file__).resolve().parent
REN  = HERE / "creator-renders"
KEY  = subprocess.run(["bash","-lc",'set -a; source "/Users/brooksorradre2/Documents/marketing brain/.env"; set +a; echo -n "$HEYGEN_API_KEY"'],capture_output=True,text=True).stdout.strip()
STATE = json.load(open(REN / "_state.json"))
ORDER = ["A-diane", "B-bridget", "C-marguerite"]

def log(*a): print(*a, flush=True)

def dur(p):
    r = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(p)],
                       capture_output=True, text=True).stdout.strip()
    try: return float(r)
    except ValueError: return 0.0

def fetch(name):
    out = REN / f"{name}-green.mp4"
    if out.exists() and dur(out) > 50: return True
    vid = STATE[name]["video_id"]
    while True:
        d = json.loads(subprocess.run(["curl","-sS","-H",f"X-Api-Key: {KEY}",
            f"https://api.heygen.com/v3/videos/{vid}"], capture_output=True, text=True).stdout)["data"]
        st = d.get("status")
        if st in ("completed","success"):
            url = d.get("video_url") or d.get("url")
            subprocess.run(["curl","-sL","-A","Mozilla/5.0","-o",str(out),url], check=True)
            log(f"{name}: downloaded {dur(out):.2f}s"); return True
        if st in ("failed","error"):
            log(f"{name}: HEYGEN FAILED {str(d.get('error'))[:200]}"); return False
        log(f"{name}: heygen {st}"); time.sleep(20)

if __name__ == "__main__":
    for name in ORDER:
        if not fetch(name): continue
        alpha = REN / f"{name}-alpha.webm"
        if dur(alpha) < 50:
            log(f"{name}: keying...")
            subprocess.run([sys.executable, str(REN/"matte.py"), name], check=True)
        log(f"{name}: alpha {dur(alpha):.2f}s -- assembling")
        subprocess.run([sys.executable, str(HERE/"assemble.py"), name], check=True)
    log("ALL DONE")
