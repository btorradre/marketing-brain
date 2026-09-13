#!/usr/bin/env python3
"""Finish a rendered Seedance 2.5 ad: burned house-style captions, plus the
per-ad overlays (AD1's POV card, AD3's optional offer end card).

Seedance renders its own dialogue, so caption timing cannot come from a TTS
alignment the way the Omni ad's did. Instead the known dialogue (read straight
out of the prompt file's DIALOGUE lines) is force-aligned against the rendered
audio via ElevenLabs /v1/forced-alignment, which returns real per-word times.
Never estimate these — cards drift and land on the wrong shot.

  python3 finish_seedance.py ../output/VEL-COL-POV-01.mp4 AD1
  python3 finish_seedance.py ../output/VEL-COL-SPEC-01.mp4 AD3 --offer
"""
import json, os, pathlib, re, subprocess, sys

HERE = pathlib.Path(__file__).parent
CONCEPT = HERE.parent
PROMPTS = CONCEPT / "prompts"
OUT = CONCEPT / "output"
ROOT = pathlib.Path("/Users/brooksorradre2/Documents/marketing brain")
for l in (ROOT / ".env").read_text().splitlines():
    if "=" in l and not l.strip().startswith("#"):
        k, v = l.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
EL = os.environ["ELEVENLABS_API_KEY"]

sys.path.insert(0, str(HERE))
from build_ad4 import render_card          # same house style as the Omni ad

W, H = 720, 1280
POV_TEXT = "POV: YOU FOUND THE PERFECT FALL BAG"


def dialogue(tag):
    """Every spoken word in beat order, skipping beats marked silent."""
    t = (PROMPTS / f"{tag}-seedance.txt").read_text()
    lines = re.findall(r'DIALOGUE:\s*"([^"]+)"', t)
    return " ".join(lines)


def align(clip, text):
    wav = HERE / "_align.mp3"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(clip), "-vn",
                    "-ac", "1", "-ar", "16000", str(wav)], check=True)
    r = subprocess.run(["curl", "-s", "--max-time", "600",
                        "https://api.elevenlabs.io/v1/forced-alignment",
                        "-H", f"xi-api-key: {EL}", "-F", f"file=@{wav}",
                        "-F", f"text={text}"], capture_output=True, text=True)
    d = json.loads(r.stdout)
    if "words" not in d:
        sys.exit(f"alignment failed: {json.dumps(d)[:300]}")
    return [w for w in d["words"] if w.get("text", "").strip()]


def cards(words, total):
    """Clause-first grouping, <=7 words, tails clamped so two never stack."""
    GLUE = {"a", "an", "the", "and", "or", "of", "with", "for", "to", "in",
            "on", "it", "that", "so", "is"}
    groups, buf = [], []
    for w in words:
        buf.append(w)
        if w["text"].rstrip().endswith((",", ".")):
            groups.append(buf); buf = []
        elif len(buf) >= 7:
            # back off to the last boundary that is not after a function word,
            # so a card never ends on "the" / "a" / "and"
            cut = len(buf)
            for j in range(len(buf) - 1, 2, -1):
                if buf[j-1]["text"].strip(",.").lower() not in GLUE:
                    cut = j; break
            groups.append(buf[:cut]); buf = buf[cut:]
    if buf:
        groups.append(buf)
    # merge a 1-2 word opener forward so it does not flash
    if len(groups) > 1 and len(groups[0]) <= 2 and len(groups[0]) + len(groups[1]) <= 8:
        groups[1] = groups[0] + groups[1]; groups.pop(0)
    PROPER = {"Colette", "Velantra", "Loro", "Piana", "Girls", "Caramel", "Okay"}
    out = []
    for i, g in enumerate(groups):
        # house style strips punctuation, so a mid-card sentence break would otherwise
        # leave an orphan capital ("Okay This is..."). Lowercase across the seam.
        toks, drop_cap = [], False
        for x in g:
            w = x["text"]
            ends = w.rstrip().endswith((".", "!", "?"))
            w = w.replace(",", "").replace(".", "").replace("!", "").replace("?", "")
            if drop_cap and w and w[0].isupper() and w not in PROPER and not w.startswith("I"):
                w = w[0].lower() + w[1:]
            drop_cap = ends
            toks.append(w)
        txt = " ".join(toks).strip()
        first = txt.split()[0] if txt else ""
        if txt and txt[0].isupper() and first not in PROPER and not first.startswith("I"):
            txt = txt[0].lower() + txt[1:]
        nxt = groups[i+1][0]["start"] if i + 1 < len(groups) else total + 1
        out.append((txt, g[0]["start"], min(g[-1]["end"] + 0.18, nxt - 0.04, total)))
    return out


def main():
    clip = pathlib.Path(sys.argv[1]); tag = sys.argv[2]
    offer = "--offer" in sys.argv
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                "format=duration", "-of", "csv=p=0", str(clip)],
                               capture_output=True, text=True).stdout.strip())
    cs = cards(align(clip, dialogue(tag)), dur)
    cdir = HERE / f"cards-{tag}"; cdir.mkdir(exist_ok=True)
    inputs, filt, cur = [], [], "0:v"
    n = 0
    for i, (txt, s, e) in enumerate(cs):
        png = cdir / f"c{i:02d}.png"
        _, ch = render_card(txt, png)
        inputs += ["-i", str(png)]; n += 1
        filt.append(f"[{cur}][{n}:v]overlay=x=0:y={H-330-ch}:"
                    f"enable='between(t,{s:.3f},{e:.3f})'[v{i}]")
        cur = f"v{i}"
        print(f"  {s:5.2f}-{e:5.2f}  {txt}")
    if tag == "AD1":                      # the reference's POV card, first 3s
        png = cdir / "pov.png"
        _, ch = render_card(POV_TEXT, png, size=40, maxw=560)
        inputs += ["-i", str(png)]; n += 1
        filt.append(f"[{cur}][{n}:v]overlay=x=0:y={(H-ch)//2 - 120}:"
                    f"enable='between(t,0.15,3.0)'[pov]")
        cur = "pov"
    filt.append(f"[{cur}]null[vout]")
    dest = OUT / (clip.stem + ("-OFFER" if offer else "") + "-final.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(clip)] + inputs +
                   ["-filter_complex", ";".join(filt), "-map", "[vout]", "-map", "0:a",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "19",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", str(dest)],
                   check=True)
    print(f"\nFINAL {dest}")


if __name__ == "__main__":
    main()
