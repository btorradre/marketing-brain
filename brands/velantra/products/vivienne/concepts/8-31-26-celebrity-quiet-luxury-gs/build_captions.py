#!/usr/bin/env python3
"""Word-synced burned caption track -> one alpha VP9 webm the three assemblies share.

Cards break on SENSE (punctuation) first, then split evenly so nothing is orphaned.
Phonetic TTS spellings are mapped back before a card is ever drawn.
"""
import json, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = Path(__file__).resolve().parent
VOD  = Path("/Users/brooksorradre2/Documents/marketing brain/_engine/mcp/ad-engine/data/vo/job_f97a185c38d2")
PROD = HERE / "production"; PROD.mkdir(exist_ok=True)
W, H, FPS, DUR = 1080, 1920, 24, 58.84
CARD_Y = 1120      # the creator is now edge-cut and much larger: her head top sits at ~1276-1346
FONT = "/System/Library/Fonts/Helvetica.ttc"
RESPELL = {"Vivian": "Vivienne", "Vehlantra": "Velantra"}   # plain TTS spellings: hyphens made v3 pause

def words():
    a = json.load(open(VOD / "alignment.json"))
    ch, st, en = a["characters"], a["character_start_times_seconds"], a["character_end_times_seconds"]
    out, cur, cs, pe = [], "", None, 0.0
    for c, s, e in zip(ch, st, en):
        if c.isspace():
            if cur: out.append({"w": cur, "s": cs, "e": pe}); cur, cs = "", None
        else:
            if not cur: cs = s
            cur += c; pe = e
    if cur: out.append({"w": cur, "s": cs, "e": pe})
    for wd in out:
        for k, v in RESPELL.items(): wd["w"] = wd["w"].replace(k, v)
    return out

def cards(ws, max_words=6, max_dur=2.9):
    """Sentence -> phrase -> card. Three rules, learned from the first pass:

      1. A card NEVER crosses a sentence end. The naive 'merge any short card into its
         neighbour' rule glued 'It's called the Vivienne by Velantra.' onto 'Same silhouette,
         no logo, actually accessible' and produced one 8-second card spanning two cuts.
      2. A card never runs longer than max_dur, however few words it holds.
      3. Phrases merge forward only inside their own sentence, and only while BOTH the word
         count and the duration still fit.
    """
    sents, cur = [], []
    for wd in ws:
        cur.append(wd)
        if wd["w"].rstrip().endswith((".", "!", "?")): sents.append(cur); cur = []
    if cur: sents.append(cur)

    out = []
    for sent in sents:
        phrases, cur = [], []
        for wd in sent:
            cur.append(wd)
            if wd["w"].rstrip().endswith((",", ";", ":")): phrases.append(cur); cur = []
        if cur: phrases.append(cur)

        # split any phrase that is too long or too slow, as evenly as possible
        split = []
        for ph in phrases:
            n = max(-(-len(ph) // max_words),
                    -(-int((ph[-1]["e"] - ph[0]["s"]) / max_dur * 100) // 100) or 1)
            n = max(n, 1)
            if n == 1: split.append(ph); continue
            size = -(-len(ph) // n)
            split += [ph[i:i+size] for i in range(0, len(ph), size)]

        # merge forward, inside this sentence only
        merged = []
        for ph in split:
            if merged:
                cand = merged[-1] + ph
                if len(cand) <= max_words and cand[-1]["e"] - cand[0]["s"] <= max_dur:
                    merged[-1] = cand; continue
            merged.append(ph)
        # a leftover one-word tail is pulled back rather than left as an orphan
        if len(merged) > 1 and len(merged[-1]) == 1 and \
           merged[-1][-1]["e"] - merged[-2][0]["s"] <= max_dur + 0.6:
            merged[-2] += merged.pop()

        for ch in merged:
            out.append({"text": " ".join(x["w"] for x in ch).strip(),
                        "s": ch[0]["s"], "e": ch[-1]["e"]})
    for c in out: c["text"] = c["text"].rstrip(".,;:")
    return out


def render_card(text, path):
    """White bold sans over a feathered LOCAL scrim.

    The scrim is measured on the type's own ink extents per line, never washed over the
    whole frame. Without it the cards sit unreadable over the white PDP screen recording
    that closes the ad.
    """
    fs, pad = 62, 26
    f = ImageFont.truetype(FONT, fs, index=1)
    im = Image.new("RGBA", (W, 300), (0,0,0,0)); d = ImageDraw.Draw(im)
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) > W - 160 and cur: lines.append(cur); cur = w
        else: cur = t
    lines.append(cur); lines = lines[:2]

    # 1. scrim: one feathered box per line, sized to that line's ink
    scrim = Image.new("L", (W, 300), 0); sd = ImageDraw.Draw(scrim)
    y = 20
    for ln in lines:
        tw = d.textlength(ln, font=f); x = (W - tw) / 2
        sd.rounded_rectangle([x - pad, y - 10, x + tw + pad, y + fs + 14], radius=18, fill=150)
        y += fs + 14
    scrim = scrim.filter(ImageFilter.GaussianBlur(16))
    im = Image.merge("RGBA", (*[Image.new("L", (W,300), c) for c in (14, 10, 7)], scrim))

    # 2. type on top, thin dark outline for the edges the scrim does not cover
    d = ImageDraw.Draw(im)
    y = 20
    for ln in lines:
        tw = d.textlength(ln, font=f); x = (W - tw) / 2
        for dx in (-3,-2,0,2,3):
            for dy in (-3,-2,0,2,3):
                d.text((x+dx, y+dy), ln, font=f, fill=(20,14,10,235))
        d.text((x, y), ln, font=f, fill=(255,255,255,255))
        y += fs + 14
    im.crop((0,0,W,min(300, y+20))).save(path)

if __name__ == "__main__":
    cs = cards(words())
    tmp = Path(tempfile.mkdtemp()); pngs = []
    print(f"{len(cs)} caption cards -- AUDIT EVERY LINE:")
    for n, c in enumerate(cs):
        p = tmp / f"c{n:03d}.png"; render_card(c["text"], p); pngs.append(p)
        print(f"  {c['s']:6.2f}-{c['e']:6.2f}  {c['text']}")
    cmd = ["ffmpeg","-v","error","-y","-f","lavfi","-i",
           f"color=c=black@0.0:s={W}x{H}:r={FPS}:d={DUR},format=rgba"]
    for p in pngs: cmd += ["-i", str(p)]
    fc, cur = [], "0:v"
    for n, (p, c) in enumerate(zip(pngs, cs)):
        o = f"v{n}"
        fc.append(f"[{cur}][{n+1}:v]overlay=x=(W-w)/2:y={CARD_Y}:"
                  f"enable='between(t,{c['s']:.3f},{c['e']:.3f})'[{o}]")
        cur = o
    out = PROD / "captions.webm"
    cmd += ["-filter_complex",";".join(fc),"-map",f"[{cur}]",
            "-c:v","libvpx-vp9","-pix_fmt","yuva420p","-b:v","0","-crf","28","-row-mt","1",
            "-an",str(out)]
    subprocess.run(cmd, check=True)
    print("\ncaptions:", out)
