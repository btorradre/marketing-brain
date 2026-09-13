#!/usr/bin/env python3
"""Derive frame-accurate beat boundaries from the ElevenLabs word alignment."""
import json, sys

# Beat = (label, the word that STARTS it, occurrence index)
BEATS = [
    ("HOOK",     0),
    ("INTRO",    "This"),
    ("STACK_1",  "It's"),      # brushed wool + handles
    ("STACK_2",  "and"),       # a belted front
    ("STACK_3",  "it's"),      # cut to stand upright
    ("STACK_4",  "and"),       # no logo anywhere
    ("PROOF",    "I"),
    ("CAP_1",    "My"),
    ("CAP_2",    "a"),         # a water bottle
    ("CAP_3",    "and"),       # and a sweater
    ("VARIANTS", "It"),
    ("OFFER",    "They're"),
    ("CTA",      "I"),
]

def build(path):
    W = json.load(open(path))
    txt = [w["w"].strip(".,").lower() for w in W]
    # anchor on distinctive words, scanning forward so repeats resolve in order
    anchors = ["this", "it's", "and", "it's", "and", "i", "my", "a", "and", "it", "they're", "i"]
    # more robust: anchor on unique-enough phrases
    marks = {}
    def find(seq, start):
        for i in range(start, len(txt) - len(seq) + 1):
            if txt[i:i+len(seq)] == seq:
                return i
        return None
    order = [
        ("INTRO",    ["this", "is", "the", "colette"]),
        ("STACK_1",  ["it's", "brushed", "wool"]),
        ("STACK_2",  ["and", "a", "belted", "front"]),
        ("STACK_3",  ["it's", "cut", "to", "stand"]),
        ("STACK_4",  ["and", "there's", "no", "logo"]),
        ("PROOF",    ["i", "filled", "it"]),
        ("CAP_1",    ["my", "laptop"]),
        ("CAP_2",    ["a", "water", "bottle"]),
        ("CAP_3",    ["and", "a", "sweater"]),
        ("VARIANTS", ["it", "comes", "in", "caramel"]),
        ("OFFER",    ["they're", "running"]),
        ("CTA",      ["i", "left", "the", "link"]),
    ]
    pos, cur = {}, 0
    for name, seq in order:
        i = find(seq, cur)
        if i is None:
            raise SystemExit(f"anchor not found: {name} {seq}")
        pos[name] = i; cur = i + 1
    rows, names = [], ["HOOK"] + [n for n, _ in order]
    starts = [0] + [pos[n] for n, _ in order]
    for k, name in enumerate(names):
        s = W[starts[k]]["s"]
        e = W[starts[k+1]]["s"] if k + 1 < len(names) else W[-1]["e"]
        line = " ".join(w["w"] for w in W[starts[k]: (starts[k+1] if k+1 < len(names) else len(W))])
        rows.append((name, round(s, 2), round(e, 2), round(e - s, 2), line))
    return rows, W[-1]["e"]

if __name__ == "__main__":
    for p in sys.argv[1:]:
        rows, total = build(p)
        print(f"\n=== {p}  total {total:.2f}s ===")
        for n, s, e, d, line in rows:
            print(f"{n:<9} {s:>6.2f} -> {e:>6.2f}  ({d:>5.2f}s)  {line}")
