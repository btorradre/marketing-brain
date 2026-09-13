#!/usr/bin/env python3
"""
chunk_vo_beats.py — split a continuous VO script into engine-legal beats.

Omni renders a fixed ~10s per segment and the omni-ugc runner lints hard in both
directions: over budget the actor crams the words and talks unnaturally fast, under
budget you get trailing dead air. So beats have to land inside the window, and the
split has to prefer sentence boundaries, then clause boundaries, and never mid-phrase.

    python3 chunk_vo_beats.py script.txt --min 27 --max 35 [--json out.json]
"""
import argparse
import json
import pathlib
import re
import sys

# Spoken-form substitutions. The engine reads the dialogue literally, so numerals and
# hyphenated product names have to arrive already in the form we want said out loud.
SPOKEN = [
    (r"\bGLP-1\b", "GLP one"),
    (r"\b2023\b", "twenty twenty three"),
]


def wc(s: str) -> int:
    return len(s.split())


def sentences(text: str) -> list[str]:
    """Split on terminal punctuation, keeping the punctuation attached."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p.strip() for p in parts if p.strip()]


def clause_split(unit: str, limit: int) -> list[str]:
    """Break an oversized sentence at commas, accumulating up to the limit."""
    pieces = re.split(r"(?<=,)\s+", unit)
    out, cur = [], ""
    for piece in pieces:
        cand = f"{cur} {piece}".strip()
        if wc(cand) <= limit or not cur:
            cur = cand
        else:
            out.append(cur)
            cur = piece
    if cur:
        out.append(cur)
    return out


def chunk_sentence_safe(text: str, lo: int, hi: int) -> list[str]:
    """
    Pack whole sentences, never splitting one across beats.

    Each beat is generated as its OWN performance: the model is told to stop and hold
    silence after the final word, so it delivers terminal falling intonation wherever a
    beat ends. Split a sentence across two beats and you get "...needs more push every"
    [full stop] "time." — which sounds exactly like a dropped word no matter how clean
    the audio is. Prosody, not gaps, and no amount of trimming repairs it.

    An underrun beat is the acceptable failure here: Omni's container is a fixed ~10s, so
    a short beat just leaves trailing silence, and silence is trimmable. A crammed or
    severed beat is not. When a single sentence exceeds the ceiling it splits at a comma,
    which at least lands the break where a speaker would already pause.
    """
    for pat, rep in SPOKEN:
        text = re.sub(pat, rep, text)

    units: list[str] = []
    for sent in sentences(text):
        units.extend(clause_split(sent, hi) if wc(sent) > hi else [sent])

    beats: list[str] = []
    cur = ""
    for unit in units:
        cand = f"{cur} {unit}".strip()
        if not cur or wc(cand) <= hi:
            cur = cand
        else:
            beats.append(cur)
            cur = unit
    if cur:
        beats.append(cur)
    return beats


def chunk(text: str, lo: int, hi: int) -> list[str]:
    """
    Word-level packing. Retained for engines fed one continuous pre-rendered VO, where
    the audio really is a single take being sliced and a mid-sentence cut is inaudible.
    Do NOT use it when each beat is separately generated — see chunk_sentence_safe.
    """
    for pat, rep in SPOKEN:
        text = re.sub(pat, rep, text)

    # Tokenise, tagging how good a cut AFTER each word would be.
    words: list[str] = []
    strength: list[int] = []
    for sent in sentences(text):
        toks = sent.split()
        for j, tok in enumerate(toks):
            words.append(tok)
            if j == len(toks) - 1:
                strength.append(3)            # sentence end
            elif tok.endswith(","):
                strength.append(2)            # clause end
            else:
                strength.append(1)            # bare word gap

    beats: list[str] = []
    i, n = 0, len(words)
    while i < n:
        remaining = n - i
        if remaining <= hi:
            # Tail: take it all if legal, else cut so both halves stay in range.
            if remaining >= lo or not beats:
                beats.append(" ".join(words[i:]))
                break
            cut = remaining - lo
            beats.append(" ".join(words[i:i + cut])) if cut >= lo else None
            i += cut if cut >= lo else 0
            beats.append(" ".join(words[i:]))
            break
        window = range(i + lo - 1, min(i + hi, n))
        best = max(window, key=lambda k: (strength[k], k))
        beats.append(" ".join(words[i:best + 1]))
        i = best + 1

    # If the tail underran, pull words back from its predecessor.
    if len(beats) > 1 and wc(beats[-1]) < lo:
        need = lo - wc(beats[-1])
        prev = beats[-2].split()
        if len(prev) - need >= lo:
            beats[-2] = " ".join(prev[:-need])
            beats[-1] = " ".join(prev[-need:] + beats[-1].split())
    return beats


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("--min", type=int, default=27)
    ap.add_argument("--max", type=int, default=35)
    ap.add_argument("--json")
    ap.add_argument("--allow-split-sentences", action="store_true",
                    help="word-level packing; only for a single pre-rendered VO being sliced")
    args = ap.parse_args()

    text = pathlib.Path(args.script).read_text()
    beats = (chunk(text, args.min, args.max) if args.allow_split_sentences
             else chunk_sentence_safe(text, args.min, args.max))

    bad = 0
    for i, b in enumerate(beats, 1):
        n = wc(b)
        ok = args.min <= n <= args.max
        bad += 0 if ok else 1
        print(f"[{i:02d}] {n:>2}w {'ok ' if ok else 'OUT'} {b}")

    total = sum(wc(b) for b in beats)
    print(f"\n{len(beats)} beats, {total} words, ~{len(beats) * 10}s at Omni's fixed 10s/segment")
    if bad:
        print(f"WARNING: {bad} beat(s) outside {args.min}-{args.max} — fix before running", file=sys.stderr)

    if args.json:
        pathlib.Path(args.json).write_text(json.dumps(
            [{"index": i, "words": wc(b), "dialogue": b} for i, b in enumerate(beats, 1)], indent=2))
        print(f"-> {args.json}")


if __name__ == "__main__":
    main()
