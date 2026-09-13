#!/usr/bin/env python3
"""Slice the middle VO (the b-roll stretch) out of a full-script v3 take.

Usage: slice_mid.py <stem>          # reads <stem>.mp3 + <stem>-words.json
Writes <stem>-mid.mp3 and <stem>-mid-words.json (re-zeroed to the slice).

Middle = "It's Loro Piana inspired ... a sweater all fit."
The A1 Seedance segment covers everything before it, A3 everything after.
"""
import json, os, subprocess, sys

FIRST = "It's"      # first word of the middle (the one following "Velantra.")
LAST = "fit."       # last word of the middle
PAD_HEAD = 0.10     # breath in front of the first word
PAD_TAIL = 0.28     # let the last word decay


def find_span(words):
    # first "It's" that comes after the word ending in "Velantra."
    anchor = next(i for i, w in enumerate(words) if w["w"].rstrip(".,").lower() == "velantra")
    i0 = next(i for i in range(anchor + 1, len(words)) if words[i]["w"] == FIRST)
    i1 = next(i for i in range(i0, len(words)) if words[i]["w"] == LAST)
    return i0, i1


def main(stem):
    words = json.load(open(stem + "-words.json"))
    i0, i1 = find_span(words)
    prev_end = words[i0 - 1]["e"]
    start = max(prev_end + 0.02, words[i0]["s"] - PAD_HEAD)
    end = words[i1]["e"] + PAD_TAIL
    out = stem + "-mid.mp3"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", stem + ".mp3",
                    "-ss", f"{start:.3f}", "-to", f"{end:.3f}",
                    "-c:a", "libmp3lame", "-b:a", "192k", out], check=True)
    mid = [{"w": w["w"], "s": round(w["s"] - start, 3), "e": round(w["e"] - start, 3)}
           for w in words[i0:i1 + 1]]
    json.dump(mid, open(stem + "-mid-words.json", "w"), indent=1)
    print(f"{os.path.basename(out)}  {start:.2f}->{end:.2f}  ({end - start:.2f}s, {len(mid)} words)")


if __name__ == "__main__":
    main(sys.argv[1])
