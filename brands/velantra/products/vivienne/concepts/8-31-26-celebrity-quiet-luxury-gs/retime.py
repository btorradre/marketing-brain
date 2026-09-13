#!/usr/bin/env python3
"""Re-time the 18-cut bed off the REAL ElevenLabs alignment. Cut boundaries are word
boundaries: a cut ends when its last spoken word ends, the next begins there."""
import json, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
VOD  = Path("/Users/brooksorradre2/Documents/marketing brain/_engine/mcp/ad-engine/data/vo/job_f97a185c38d2")

# cut, source, source in-point, PiP side, spoken fragment (display spelling)
CUTS = [
 ("c01","HOOK-A",  None,"L","Okay, so if you love that Katie Holmes,"),
 ("c02","HOOK-B",  None,"L","Sofia Richie energy,"),
 ("c03","O8",       1.2,"L","always in a Birkin shape bag, never a logo,"),
 ("c04","O9",       1.5,"R","quiet luxury written all over it, you already know the problem."),
 # the price line used to be two cuts: a SECOND pass of the Sofia still carrying a burned
 # $10,000+ card, then O1. Brooks killed both - the still was a visible reuse and the card
 # looked cheap. The whole line now plays over one continuous cut of our bag on the counter,
 # and the number still lands on screen in the normal word-synced caption style.
 ("c05","O1",       0.5,"L","Every bag that gives you that look starts around ten thousand dollars."),
 ("c06","O2",       2.0,"L","So I hunted down the affordable version."),
 ("c07","O12",      1.0,"R","It's called the Vivienne by Velantra."),
 ("c08","O3",       1.5,"R","Same silhouette, no logo, actually accessible."),
 ("c09","O4",       0.8,"L","It's vegetable tanned leather all the way through,"),
 ("c10","O5",       1.0,"L","with an aged brass belted turn lock,"),
 ("c11","O11",      0.5,"L","braided leather trim,"),
 ("c12","O2",       5.5,"L","and zero branding anywhere on it."),
 ("c13","O8",       6.5,"R","It's soft, so instead of sitting stiff on your arm"),
 ("c14","O10",      0.0,"R","like most bags in this shape,"),
 ("c15","O9",       6.0,"R","it slouches and molds to you as you carry it."),
 ("c16","O7",       1.0,"L","And right now they've actually just opened pre orders on it."),
 ("c17","PDP-SCROLL",None,"L","Twenty five percent off, one forty nine instead of one ninety nine, "
                              "and the first run ships in October. I've left the link below."),
]
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
    for wd in out:                                  # phonetic -> display
        for k, v in RESPELL.items(): wd["w"] = wd["w"].replace(k, v)
    return out

def norm(s): return re.sub(r"[^a-z0-9]", "", s.lower())

if __name__ == "__main__":
    W = words()
    i, beats = 0, []
    for cid, src, sin, pip, line in CUTS:
        n = len(line.split())
        span = W[i:i+n]
        got, want = norm(" ".join(x["w"] for x in span)), norm(line)
        assert got == want, f"{cid} misaligned\n  want {want}\n  got  {got}"
        beats.append({"cut": cid, "in": round(beats[-1]["out"], 3) if beats else 0.0,
                      "out": round(span[-1]["e"], 3), "src": src, "src_in": sin,
                      "pip": pip, "line": line})
        i += n
    beats[0]["in"] = 0.0
    beats[-1]["out"] = round(W[-1]["e"] + 0.45, 3)          # small tail after the last word
    json.dump(beats, open(HERE / "beat-map-final.json", "w"), indent=1)
    for b in beats:
        print(f"  {b['cut']}  {b['in']:6.2f} -> {b['out']:6.2f}  {b['out']-b['in']:5.2f}s  {b['src']:<12} {b['line'][:48]}")
    print(f"\nTOTAL {beats[-1]['out']:.2f}s  avg cut {beats[-1]['out']/len(beats):.2f}s  words matched {i}/{len(W)}")
