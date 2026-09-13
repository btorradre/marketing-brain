#!/usr/bin/env python3
"""Captions + real beat timings for VEL-SOFIA-ONEBAG-01.

Drives everything off the ElevenLabs word alignment rather than the estimated
timings in the script brief, so cuts land on the words they were written for.

Writes, per voice:
  assets/vo/VEL-SOFIA-ONEBAG-VO-<v>.srt      caption cards, 4-8 words
  assets/vo/VEL-SOFIA-ONEBAG-EDL-<v>.json    per-shot in/out points
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
VO = os.path.normpath(os.path.join(HERE, "..", "assets", "vo"))
MANIFEST = json.load(open(os.path.join(HERE, "manifest.json")))

MAX_WORDS = 7
MIN_WORDS = 3


def norm(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


def ts(t):
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:06.3f}".replace(".", ",")


def cards(words):
    """Sentence-safe caption cards.

    A card never straddles a sentence boundary — the swipe's captions read as clean
    phrase chunks, and merging "...effortless. Mine is the Sofia..." onto one card
    reads as a transcription error. Within a sentence, prefer to break after a comma.
    """
    sentences, cur = [], []
    for w in words:
        cur.append(w)
        if w["word"].rstrip().endswith((".", "?", "!")):
            sentences.append(cur)
            cur = []
    if cur:
        sentences.append(cur)

    out = []
    for sent in sentences:
        i = 0
        while i < len(sent):
            remaining = len(sent) - i
            take = min(MAX_WORDS, remaining)
            # avoid orphaning 1-2 words onto a final card
            if remaining - take and remaining - take < MIN_WORDS:
                take = remaining - MIN_WORDS if remaining - MIN_WORDS >= MIN_WORDS else remaining
            # prefer a comma break inside the window
            for j in range(i + take - 1, i + MIN_WORDS - 1, -1):
                if sent[j]["word"].rstrip().endswith(","):
                    take = j - i + 1
                    break
            out.append(sent[i:i + take])
            i += take
    return out


def caption_text(card):
    """Natural casing from the script, terminal punctuation stripped, commas kept."""
    txt = " ".join(w["word"] for w in card).strip()
    return txt.rstrip(".!?").strip()


def write_srt(cards_, path):
    lines = []
    for i, card in enumerate(cards_, 1):
        lines += [str(i), f"{ts(card[0]['start'])} --> {ts(card[-1]['end'])}",
                  caption_text(card), ""]
    open(path, "w").write("\n".join(lines))
    return len(cards_)


def build_edl(words, total):
    """Locate each shot's VO line inside the word stream -> real in/out points."""
    stream = [norm(w["word"]) for w in words]
    edl, cursor = [], 0
    for shot in MANIFEST["shots"]:
        toks = [norm(t) for t in shot["vo"].split() if norm(t)]
        # find this line's first token at or after the cursor
        start_i = None
        for i in range(cursor, len(stream) - len(toks) + 1):
            if stream[i:i + len(toks)] == toks:
                start_i = i
                break
        if start_i is None:            # fall back to first-token match
            for i in range(cursor, len(stream)):
                if stream[i] == toks[0]:
                    start_i = i
                    break
        end_i = min(start_i + len(toks) - 1, len(stream) - 1)
        edl.append({"id": shot["id"], "kind": shot["kind"],
                    "in": round(words[start_i]["start"], 3),
                    "out": round(words[end_i]["end"], 3),
                    "vo": shot["vo"]})
        cursor = end_i + 1
    # butt-joint the cuts: each shot runs until the next one starts
    for i in range(len(edl) - 1):
        edl[i]["out"] = edl[i + 1]["in"]
    edl[0]["in"] = 0.0
    edl[-1]["out"] = round(total + 0.6, 3)      # small tail after the last word
    for e in edl:
        e["dur"] = round(e["out"] - e["in"], 3)
    return edl


def run(vkey):
    """Captions only. The v2 beat map includes talking-head-only beats that the shot
    manifest doesn't model, and assembly is not ours to do — the beat map in the script
    doc is the source of truth for what lands where."""
    data = json.load(open(os.path.join(VO, f"VEL-SOFIA-ONEBAG-VO-{vkey}.words.json")))
    words, total = data["words"], data["duration"]
    n = write_srt(cards(words), os.path.join(VO, f"VEL-SOFIA-ONEBAG-VO-{vkey}.srt"))
    print(f"{vkey} ({data['voice']}): VO {total:.2f}s, {n} caption cards")


if __name__ == "__main__":
    for vk in (sys.argv[1:] or ["w30", "w40"]):
        run(vk)
