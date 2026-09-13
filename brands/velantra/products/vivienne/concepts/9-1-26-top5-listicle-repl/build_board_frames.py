#!/usr/bin/env python3
"""VEL-VIV-BIRKIN-COUCH-01 (v3, was TOP5-01): beat map on the tightened VO timebase + one board frame per cut,
rendered the way the reference does it (Didot rank cards on the talking head, small serif
phrase captions on b-roll). Competitor beats use the reference's own frames as PLACEHOLDERS
with a SOURCE ribbon: the editor sources licensed/brand-site footage; nothing third-party ships."""
import json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = Path(__file__).resolve().parent
OUT  = HERE / "board-frames"; OUT.mkdir(exist_ok=True)
REF  = HERE / "reference" / "frames"
BF   = HERE / "board-frames"
W, H = 1080, 1920
DIDOT = "/System/Library/Fonts/Supplemental/Didot.ttc"
def font(sz, idx=0): return ImageFont.truetype(DIDOT, sz, index=idx)

CREATOR = HERE / "creator" / "C-blue-shirt.png"     # board default; A-knit-gesture.png is the alt

def creator_plate():
    im = Image.open(CREATOR).convert("RGB")
    s = H / im.height; im = im.resize((int(im.width*s), H), Image.LANCZOS)
    l = (im.width - W)//2; return im.crop((l, 0, l+W, H))

def fit(path):
    im = Image.open(path).convert("RGB")
    s = max(W/im.width, H/im.height); im = im.resize((int(im.width*s), int(im.height*s)), Image.LANCZOS)
    l=(im.width-W)//2; t=(im.height-H)//2; return im.crop((l,t,l+W,t+H))

def shadow_text(img, xy, text, f, fill=(255,255,255), anchor="mm"):
    # soft dark shadow like the reference's serif overlays
    sh = Image.new("RGBA", img.size, (0,0,0,0)); d = ImageDraw.Draw(sh)
    d.text((xy[0]+3, xy[1]+4), text, font=f, fill=(0,0,0,170), anchor=anchor)
    sh = sh.filter(ImageFilter.GaussianBlur(6)); img.alpha_composite(sh)
    ImageDraw.Draw(img).text(xy, text, font=f, fill=fill, anchor=anchor)

def rank_card(img, n, name, sub, y=980):
    """n° + big numeral, brand line(s), small country line. Mirrors the reference's card."""
    if n:
        shadow_text(img, (W//2 - 120, y-60), "n°", font(70))
        shadow_text(img, (W//2 + 30, y-70), str(n), font(190))
        y += 110
    for line in name.split("\n"):
        shadow_text(img, (W//2, y), line, font(120)); y += 125
    if sub: shadow_text(img, (W//2, y+5), sub, font(56))

def caption(img, text, y=1200):
    shadow_text(img, (W//2, y), text, font(58))

def ribbon(img, text):
    d = ImageDraw.Draw(img); d.rectangle((0, 40, W, 130), fill=(180, 30, 30, 235))
    d.text((W//2, 85), text, font=ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 34), fill="white", anchor="mm")

def split_hook(top_path, bottom_plate):
    img = Image.new("RGB", (W, H))
    top = fit(top_path).crop((0, 0, W, H//2))               # top half of a 9:16 source
    bot = bottom_plate.crop((0, 140, W, 140 + H//2))         # creator's head + mic band
    img.paste(top, (0,0)); img.paste(bot, (0, H//2)); return img

# ---- the cut list on the TIGHT timebase (vo/words-tight.json) ----
# id, in, out, source, kind, overlay, spoken
CUTS = [
 ("c01", 0.00,  1.94, "ref-01-0.6s", "split", ("cap","the Birkin"), "The Birkin is your dream bag,"),
 ("c02", 1.94,  2.98, "ref-02-3.0s", "split", ("cap","and that's the problem"), "and that's the problem."),
 ("c03", 2.98,  4.58, "TH", "th", ("cap","you can't just walk in and buy one"), "You can't just walk in and buy one,"),
 ("c04", 4.58,  7.90, "TH", "th", ("cap","most of what you pay is the name"), "and when they finally let you, most of what you pay is the name."),
 ("c05", 7.90, 10.51, "TH", "th", ("card", None, "The perfect\none", "if it's the shape you love"), "But if it's the shape you love, I found the perfect one."),
 ("c06",10.51, 12.34, "O8", "ours", ("card", None, "The Vivienne\nVelantra", ""), "This is the Vivienne from Velantra."),
 ("c07",12.34, 13.40, "O2", "ours", ("cap","same silhouette"), "Same silhouette,"),
 ("c08",13.40, 14.74, "O5", "ours", ("cap","a belted brass turn lock"), "a belted brass turn lock,"),
 ("c09",14.74, 16.94, "O4", "ours", ("cap","vegetable-tanned leather"), "vegetable-tanned leather all the way through,"),
 ("c10",16.94, 18.00, "O11", "ours", ("cap","braided leather trim"), "braided leather trim,"),
 ("c11",18.00, 19.67, "O12", "ours", ("cap","no logo anywhere"), "and no logo anywhere."),
 ("c12",19.67, 21.40, "O10", "ours", ("cap","it's soft"), "It's soft, so it slouches"),
 ("c13",21.40, 23.97, "O9", "ours", ("cap","molds to you"), "and molds to you instead of sitting stiff on your arm,"),
 ("c14",23.97, 25.69, "COLORWAY-4up", "ours", ("cap","four colors"), "and it comes in four colors."),
 ("c15",25.69, 33.15, "PDP-scroll-placeholder", "pdp", ("cap","25% off on pre-order"), "It's twenty five percent off on pre-order right now, one forty nine instead of one ninety nine, and the first run ships in October. I left the link below."),
]

if __name__ == "__main__":
    plate = creator_plate()
    for cid, tin, tout, src, kind, ov, line in CUTS:
        if kind == "split":
            base = split_hook(REF / f"{src}.jpg", plate)
        elif kind == "th":
            base = plate.copy()
        elif kind == "src":
            base = fit(HERE/"reference"/"competitors"/"row-soft-margaux-10-walnut.jpg") if src == "row" else fit(REF / f"{src}.jpg")
        elif kind in ("ours", "pdp"):
            p = BF / f"{src}.png" if (BF / f"{src}.png").exists() else BF / f"{src}.jpg"
            base = fit(p)
        img = base.convert("RGBA")
        if ov[0] == "cap": caption(img, ov[1])
        else: rank_card(img, ov[1], ov[2], ov[3])
        if kind == "split": ribbon(img, "TOP HALF = PLACEHOLDER. Editor sources street footage of a Birkin being carried")
        if kind == "src": ribbon(img, "PLACEHOLDER (reference frame). Editor sources brand-site / licensed footage of this bag")
        if kind == "pdp": ribbon(img, "PLACEHOLDER. Live PDP screen recording captured the day the ad ships")
        img.convert("RGB").save(OUT / f"{cid}.jpg", quality=90)
    json.dump([{"cut":c,"in":i,"out":o,"src":s,"kind":k,"overlay":list(ov) if isinstance(ov,tuple) else ov,"line":l}
               for c,i,o,s,k,ov,l in CUTS], open(HERE/"beat-map.json","w"), indent=1)
    # QA storyboard
    fs=[OUT/f"{c[0]}.jpg" for c in CUTS]; ims=[Image.open(f).resize((216,384)) for f in fs]
    cols=8; rows=(len(ims)+cols-1)//cols; sheet=Image.new("RGB",(cols*216,rows*384),"black")
    for i,im in enumerate(ims): sheet.paste(im,((i%cols)*216,(i//cols)*384))
    sheet.save(HERE/"_qa-storyboard.jpg", quality=85)
    print(len(CUTS), "cuts; avg", round(sum(o-i for _,i,o,*_ in CUTS)/len(CUTS),2), "s")
