#!/usr/bin/env python3
"""Assemble the three Vivienne VO ads: b-roll + word-synced burned captions + VO.

9:16 1080x1920, locked 24fps CFR, one encode pass. VO normalised to -14 LUFS.
Generated b-roll audio is muted (the clips are already audio-stripped).
ffmpeg on this machine has NO drawtext, so caption cards are rendered with Pillow.
"""
import json, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
VAULT = Path("/Users/brooksorradre2/Documents/marketing brain")
BROLL = VAULT / "brands/velantra/products/vivienne/broll/final"
VOD = VAULT / "_engine/mcp/ad-engine/data/vo"
OUT = HERE / "ads"; OUT.mkdir(exist_ok=True)
W, H, FPS = 1080, 1920, 24
FONT = "/System/Library/Fonts/Helvetica.ttc"

ADS = {
 "VEL-VIVIENNE-WORK-01": {
   "vo": HERE / "vo/WORK-punched.mp3",
   "align": VOD / "job_df9f4f73598b/alignment.json",
   "sub": {"This is the Vivienne from Vel-LAN-truh.": "This is the Vivienne from Velantra."},
   "seq": ["O1","O2","O5","O11","O4","O3","O8","O7"],
 },
 "VEL-VIVIENNE-EVERYTHING-01": {
   "vo": VOD / "job_5d38343a5748/voiceover.mp3",
   "align": VOD / "job_5d38343a5748/alignment.json",
   "sub": {"Viv-ee-EN": "Vivienne", "Vel-LAN-truh": "Velantra"},
   "seq": ["O1","O8","O4","O11","O10","O6","O3","O7"],
 },
 "VEL-VIVIENNE-FALL-01": {
   "vo": VOD / "job_1947349f91fd/voiceover.mp3",
   "align": VOD / "job_1947349f91fd/alignment.json",
   "sub": {"Viv-ee-EN": "Vivienne", "Vel-LAN-truh": "Velantra"},
   "seq": ["O12","O2","O4","O11","O5","O6","O9","O1"],
 },
}


MACROS = {"O4","O5","O11"}   # tight crops: no whole bag visible

def check_seq(name, seq):
    """Slots 1 and 2 carry the HOOK and the mandatory brand intro. Both must show the
    whole bag, so a macro there is a hard error (Brooks caught O11 in slot 2, 2026-08-24)."""
    bad = [s for s in seq[:2] if s in MACROS]
    if bad:
        raise SystemExit(f"{name}: macro {bad} in an opening slot. "
                         "Slots 1-2 must show the whole bag.")

def dur(p):
    return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
        "-of","csv=p=0",str(p)],capture_output=True,text=True).stdout.strip())

def words_from_alignment(path, sub):
    """Character alignment -> word list with start/end. Phonetic spellings mapped back."""
    a = json.load(open(path))
    chars, st, en = a["characters"], a["character_start_times_seconds"], a["character_end_times_seconds"]
    words, cur, cs = [], "", None
    for c, s, e in zip(chars, st, en):
        if c.isspace():
            if cur: words.append({"w": cur, "s": cs, "e": prev_e}); cur, cs = "", None
        else:
            if not cur: cs = s
            cur += c; prev_e = e
    if cur: words.append({"w": cur, "s": cs, "e": prev_e})
    # map phonetic tokens back to display spelling
    for wd in words:
        for k, v in sub.items():
            if k in wd["w"]: wd["w"] = wd["w"].replace(k, v)
        for tok, rep in [("Viv-ee-EN","Vivienne"),("Vel-LAN-truh","Velantra"),
                         ("Vel-LAN-truh.","Velantra."),("Viv-ee-EN,","Vivienne,")]:
            wd["w"] = wd["w"].replace(tok, rep)
    return words

def cards(words, max_words=7):
    """Group words into caption cards that break on SENSE, not on a word counter.

    Segment at punctuation first; only split a segment if it is too long, and then
    split as evenly as possible so no card is left a 1-2 word orphan.
    """
    segs, cur = [], []
    for wd in words:
        cur.append(wd)
        if wd["w"].rstrip().endswith((".", ",", "!", "?", ";", ":")):
            segs.append(cur); cur = []
    if cur: segs.append(cur)

    out = []
    for seg in segs:
        if len(seg) <= max_words:
            chunks = [seg]
        else:
            n = -(-len(seg) // max_words)          # how many cards this segment needs
            size = -(-len(seg) // n)               # even split, no orphan tail
            chunks = [seg[i:i+size] for i in range(0, len(seg), size)]
        for ch in chunks:
            out.append({"text": " ".join(x["w"] for x in ch).strip(),
                        "s": ch[0]["s"], "e": ch[-1]["e"]})

    # merge any 1-2 word card into its neighbour so nothing reads as a fragment
    merged = []
    for c in out:
        if merged and len(c["text"].split()) <= 2:
            merged[-1]["text"] += " " + c["text"]; merged[-1]["e"] = c["e"]
        else:
            merged.append(c)
    for c in merged:
        c["text"] = c["text"].rstrip(".,;:")        # house style: no terminal punctuation
    return merged

def render_card(text, path):
    """White bold rounded sans, thin dark outline, sentence case, 1-2 lines, centred."""
    fs = 62
    f = ImageFont.truetype(FONT, fs, index=1)   # Helvetica Bold
    im = Image.new("RGBA", (W, 300), (0,0,0,0)); d = ImageDraw.Draw(im)
    # wrap to <=2 lines
    ws = text.split(); lines, cur = [], ""
    for w in ws:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) > W - 160 and cur:
            lines.append(cur); cur = w
        else: cur = t
    lines.append(cur)
    lines = lines[:2]
    y = 20
    for ln in lines:
        tw = d.textlength(ln, font=f); x = (W - tw) / 2
        for dx in (-3,-2,0,2,3):
            for dy in (-3,-2,0,2,3):
                d.text((x+dx, y+dy), ln, font=f, fill=(20,14,10,235))
        d.text((x, y), ln, font=f, fill=(255,255,255,255))
        y += fs + 14
    im.crop((0,0,W,min(300, y+20))).save(path)
    return path

def build(name, cfg):
    vo = cfg["vo"]; vd = dur(vo)
    tmp = Path(tempfile.mkdtemp())

    # 1. b-roll bed: each clip contributes up to 4s, playlist repeats until VO is covered
    segs, t = [], 0.0
    i = 0
    while t < vd + 1:
        sid = cfg["seq"][i % len(cfg["seq"])]
        src = BROLL / f"{sid}.mp4"
        take = min(4.0, dur(src))
        seg = tmp / f"s{i:02d}.mp4"
        subprocess.run(["ffmpeg","-v","error","-t",str(take),"-i",str(src),
            "-vf",f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}",
            "-c:v","libx264","-crf","18","-preset","veryfast","-pix_fmt","yuv420p","-an",
            str(seg),"-y"],check=True)
        segs.append(seg); t += take; i += 1
    lst = tmp/"list.txt"; lst.write_text("".join(f"file '{s.resolve()}'\n" for s in segs))
    bed = tmp/"bed.mp4"
    subprocess.run(["ffmpeg","-v","error","-f","concat","-safe","0","-i",str(lst),
        "-t",str(vd),"-c:v","libx264","-crf","18","-preset","veryfast","-pix_fmt","yuv420p",
        "-r",str(FPS),str(bed),"-y"],check=True)

    # 2. caption cards
    cs = cards(words_from_alignment(cfg["align"], cfg["sub"]))
    pngs = []
    for n, c in enumerate(cs):
        p = tmp/f"c{n:03d}.png"; render_card(c["text"], p); pngs.append((p, c))

    # 3. overlay + VO, single encode
    cmd = ["ffmpeg","-v","error","-i",str(bed)]
    for p,_ in pngs: cmd += ["-i",str(p)]
    cmd += ["-i",str(vo)]
    fc, cur = [], "0:v"
    for n,(p,c) in enumerate(pngs):
        out = f"v{n}"
        fc.append(f"[{cur}][{n+1}:v]overlay=x=(W-w)/2:y=H-h-300:"
                  f"enable='between(t,{c['s']:.3f},{c['e']:.3f})'[{out}]")
        cur = out
    fc.append(f"[{len(pngs)+1}:a]loudnorm=I=-14:TP=-1.5:LRA=11[a]")
    cmd += ["-filter_complex",";".join(fc),"-map",f"[{cur}]","-map","[a]",
            "-c:v","libx264","-crf","19","-preset","medium","-pix_fmt","yuv420p",
            "-r",str(FPS),"-c:a","aac","-b:a","192k","-shortest",
            str(OUT/f"{name}.mp4"),"-y"]
    subprocess.run(cmd,check=True)
    return OUT/f"{name}.mp4", vd, len(cs)

if __name__ == "__main__":
    for name,cfg in ADS.items():
        check_seq(name, cfg["seq"])
        p,vd,nc = build(name,cfg)
        print(f"  {name}: {dur(p):.1f}s  ({nc} caption cards)  -> {p.name}")
