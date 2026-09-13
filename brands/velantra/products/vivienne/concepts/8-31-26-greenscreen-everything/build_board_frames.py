#!/usr/bin/env python3
"""Extract one board frame per cut of VEL-VIVIENNE-GS-EVERYTHING-01, at the exact in-point."""
import json, subprocess
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
BROLL = Path("/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/vivienne/broll/final")
COLORS = Path("/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/vivienne/product-images/colors")
OUT = HERE / "board-frames"; OUT.mkdir(exist_ok=True)

# cut, in, out, source, source in-point, PiP side, spoken fragment
CUTS = [
 ("c01", 0.00,  1.55, "O1",  0.5, "L", "If you want one bag"),
 ("c02", 1.55,  3.12, "O8",  1.2, "L", "that holds everything, I found it."),
 ("c03", 3.12,  5.28, "O12", 1.0, "R", "This is the Vivienne from Velantra."),
 ("c04", 5.28,  7.10, "O3",  1.5, "L", "Fifteen inches across,"),
 ("c05", 7.10,  9.00, "O4",  0.8, "L", "soft vegetable-tanned leather,"),
 ("c06", 9.00, 10.60, "O11", 0.5, "L", "reinforced corners,"),
 ("c07",10.60, 11.90, "GAP-01", None, "L", "brass feet,"),
 ("c08",11.90, 13.01, "O2",  2.0, "L", "and no logo anywhere."),
 ("c09",13.01, 15.10, "O10", 0.0, "R", "It's a soft bag, so it takes the shape"),
 ("c10",15.10, 17.36, "O9",  1.5, "R", "of whatever you put in it instead of fighting you."),
 ("c11",17.36, 19.60, "O1",  6.0, "L", "A folder, a water bottle,"),
 ("c12",19.60, 21.97, "O8",  6.5, "L", "a sweater and your wallet, all at once."),
 ("c13",21.97, 23.71, "COLORWAY", None, "R", "It comes in four colors."),
 ("c14",23.71, 28.96, "PDP-SCROLL", None, "L", "It's twenty five percent off right now, and the first run ships in October. I left the link below."),
]

def colorway_card():
    """Four-up card: the real per-colorway front renders, no recolours."""
    names = ["Chocolate", "Cognac", "Black", "Olive"]
    W, H = 1080, 1920
    card = Image.new("RGB", (W, H), (238, 234, 227))
    cw, ch = W // 2, H // 2
    for i, n in enumerate(names):
        im = Image.open(COLORS / n / "front.png").convert("RGB")
        s = max(cw / im.width, ch / im.height)
        im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
        l = (im.width - cw) // 2; t = (im.height - ch) // 2
        card.paste(im.crop((l, t, l + cw, t + ch)), ((i % 2) * cw, (i // 2) * ch))
    p = OUT / "COLORWAY-4up.png"; card.save(p); return p

if __name__ == "__main__":
    colorway_card()
    for cid, tin, tout, src, sin, side, line in CUTS:
        dst = OUT / f"{cid}-{src}.jpg"
        if src.startswith(("GAP", "PDP", "COLOR")):
            continue
        subprocess.run(["ffmpeg","-v","error","-ss",str(sin),"-i",str(BROLL/f"{src}.mp4"),
                        "-frames:v","1","-q:v","2",str(dst),"-y"], check=True)
    json.dump([{"cut":c,"in":i,"out":o,"src":s,"src_in":si,"pip":p,"line":l}
               for c,i,o,s,si,p,l in CUTS], open(HERE/"beat-map.json","w"), indent=1)
    print("frames:", len(list(OUT.glob('*.jpg'))), "+ colorway + GAP-01")
