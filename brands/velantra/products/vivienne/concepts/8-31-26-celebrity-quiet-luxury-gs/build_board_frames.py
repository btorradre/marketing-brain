#!/usr/bin/env python3
"""Board frames for VEL-VIV-CELEB-GS-01, one per cut, pulled at the exact in-point."""
import json, subprocess
from pathlib import Path

HERE  = Path(__file__).resolve().parent
VIV   = HERE.parent.parent
BROLL = VIV / "broll/final"
GS    = VIV / "concepts/8-31-26-greenscreen-everything/board-frames"
OUT   = HERE / "board-frames"; OUT.mkdir(exist_ok=True)

# cut, in, out, source, source in-point, PiP side, spoken fragment
CUTS = [
 ("c01",  0.00,  2.20, "HOOK-A",     None, "L", "Okay, so if you love that Katie Holmes,"),
 ("c02",  2.20,  3.80, "HOOK-B",     None, "L", "Sofia Richie clean girl energy,"),
 ("c03",  3.80,  6.40, "O8",          1.2, "L", "always in a Birkin shape bag, never a logo,"),
 ("c04",  6.40,  9.70, "O9",          1.5, "R", "quiet luxury written all over it, you already know the problem."),
 ("c05",  9.70, 11.70, "HOOK-B-late",None, "R", "Every bag that gives you that look"),
 ("c06", 11.70, 13.40, "O1",          0.5, "L", "starts around ten thousand dollars."),
 ("c07", 13.40, 15.50, "O2",          2.0, "L", "So I hunted down the affordable version."),
 ("c08", 15.50, 17.60, "O12",         1.0, "R", "It's called the Vivienne by Velantra."),
 ("c09", 17.60, 19.80, "O3",          1.5, "R", "Same silhouette, no logo, actually accessible."),
 ("c10", 19.80, 22.20, "O4",          0.8, "L", "It's vegetable tanned leather all the way through,"),
 ("c11", 22.20, 24.30, "O5",          1.0, "L", "with an aged brass belted turn lock,"),
 ("c12", 24.30, 25.50, "O11",         0.5, "L", "braided leather trim,"),
 ("c13", 25.50, 27.50, "GAP-02",     None, "L", "and zero branding anywhere on it."),
 ("c14", 27.50, 30.40, "O4",          5.5, "R", "It's soft, so instead of sitting stiff on your arm"),
 ("c15", 30.40, 32.20, "O10",         0.0, "R", "like most bags in this shape,"),
 ("c16", 32.20, 35.00, "O9",          6.0, "R", "it slouches and molds to you as you carry it."),
 ("c17", 35.00, 38.30, "O7",          1.0, "L", "And right now they've actually just opened pre orders on it."),
 ("c18", 38.30, 46.50, "PDP-SCROLL", None, "L", "Twenty five percent off, one forty nine instead of one ninety nine, and the first run ships in October. I've left the link below."),
]

if __name__ == "__main__":
    for cid, tin, tout, src, sin, side, line in CUTS:
        if src.startswith("HOOK") or src.startswith("GAP"):
            continue                      # stills / not yet generated
        if src == "PDP-SCROLL":
            dst = OUT / f"{cid}-PDP-SCROLL.jpg"
            subprocess.run(["cp", str(GS / "c14-PDP-SCROLL.jpg"), str(dst)], check=True)
            continue
        dst = OUT / f"{cid}-{src}.jpg"
        subprocess.run(["ffmpeg","-v","error","-ss",str(sin),"-i",str(BROLL/f"{src}.mp4"),
                        "-frames:v","1","-q:v","2",str(dst),"-y"], check=True)
    json.dump([{"cut":c,"in":i,"out":o,"src":s,"src_in":si,"pip":p,"line":l}
               for c,i,o,s,si,p,l in CUTS], open(HERE/"beat-map.json","w"), indent=1)
    print("board frames:", len(list(OUT.glob('*.jpg'))))
