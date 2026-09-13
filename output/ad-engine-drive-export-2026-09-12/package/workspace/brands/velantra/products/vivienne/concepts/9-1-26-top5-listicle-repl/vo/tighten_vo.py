#!/usr/bin/env python3
"""Remove dead space from the Woman Over 40 VO and remap the word alignment onto the tighter read.

Only long pauses are compressed. Gaps under KEEP_UNDER are speech rhythm (plosives, breaths)
and are left alone -- squeezing those is what makes a read sound clipped. Head and tail are
trimmed hard. This is NOT atempo: no sample is time-stretched, silence is simply shortened.
"""
import json, subprocess, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
VO   = Path("/Users/brooksorradre2/Documents/marketing brain/_engine/mcp/ad-engine/data/vo/job_71b8bf93dfe9")
SRC  = VO / "voiceover.mp3"

KEEP_UNDER = 0.22   # gaps shorter than this are natural rhythm, untouched
TARGET     = 0.15   # anything longer is compressed to this
EDGE       = 0.04   # leading / trailing silence kept

def silences():
    out = subprocess.run(["ffmpeg","-hide_banner","-i",str(SRC),
        "-af","silencedetect=noise=-35dB:d=0.08","-f","null","-"],
        capture_output=True, text=True).stderr
    st = [float(m) for m in re.findall(r"silence_start: ([\d.]+)", out)]
    en = [float(m) for m in re.findall(r"silence_end: ([\d.]+)", out)]
    return list(zip(st, en))

def dur(p):
    return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
        "-of","csv=p=0",str(p)], capture_output=True, text=True).stdout.strip())

def main():
    total = dur(SRC)
    # merge overlapping/adjacent detections
    sil, raw = [], sorted(silences())
    for s, e in raw:
        if sil and s <= sil[-1][1] + 0.01:
            sil[-1][1] = max(sil[-1][1], e)
        else:
            sil.append([s, e])

    # decide the kept span of each silence
    plan = []            # (sil_start, sil_end, kept_len)
    for s, e in sil:
        length = e - s
        if s <= 0.02:                      # leading
            keep = min(length, EDGE)
        elif e >= total - 0.02:            # trailing
            keep = min(length, EDGE)
        elif length <= KEEP_UNDER:
            keep = length
        else:
            keep = TARGET
        plan.append((s, e, keep))

    # build the kept-segment list, and an old->new time map
    segs, mapping, cursor, new_t = [], [], 0.0, 0.0
    for s, e, keep in plan:
        if s > cursor:
            segs.append((cursor, s))
            mapping.append((cursor, s, new_t))
            new_t += s - cursor
        if keep > 0.001:
            segs.append((s, s + keep))
            mapping.append((s, e, new_t))   # whole silence collapses onto this point
            new_t += keep
        else:
            mapping.append((s, e, new_t))
        cursor = e
    if cursor < total:
        segs.append((cursor, total))
        mapping.append((cursor, total, new_t))
        new_t += total - cursor

    # render: one filter_complex, no re-timing of any sample
    parts, streams = [], []
    for i, (a, b) in enumerate(segs):
        parts.append(f"[0:a]atrim=start={a:.4f}:end={b:.4f},asetpts=PTS-STARTPTS[a{i}]")
        streams.append(f"[a{i}]")
    fc = ";".join(parts) + ";" + "".join(streams) + f"concat=n={len(segs)}:v=0:a=1[out]"
    out = HERE / "VO-tight.mp3"
    subprocess.run(["ffmpeg","-y","-v","error","-i",str(SRC),"-filter_complex",fc,
                    "-map","[out]","-c:a","libmp3lame","-b:a","192k",str(out)], check=True)

    def remap(t):
        for a, b, nt in mapping:
            if a <= t <= b:
                if b - a < 1e-6: return nt
                # inside a kept speech run, scale linearly; inside a silence, clamp to its start
                seg_new_len = next((k for (s,e,k) in plan if abs(s-a)<1e-6 and abs(e-b)<1e-6), None)
                if seg_new_len is None:
                    return nt + (t - a)
                return nt + min(t - a, seg_new_len)
        return mapping[-1][2]

    # rebuild words on the new timebase
    al = json.load(open(VO / "alignment.json"))
    ch, st, en = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
    words, cur, cs = [], "", None
    for c, s, e in zip(ch, st, en):
        if c.isspace():
            if cur: words.append({"w": cur, "s": cs, "e": pe}); cur, cs = "", None
        else:
            if not cur: cs = s
            cur += c; pe = e
    if cur: words.append({"w": cur, "s": cs, "e": pe})
    for w in words:
        w["s"], w["e"] = round(remap(w["s"]), 3), round(remap(w["e"]), 3)
    json.dump(words, open(HERE / "words-tight.json", "w"), indent=1)

    segsum = sum(b - a for a, b in segs)
    print(f"source {total:.2f}s -> tight {dur(out):.2f}s (planned {segsum:.2f}s), removed {total-segsum:.2f}s")
    print(f"{len(sil)} silences, {sum(1 for s,e,k in plan if e-s-k > 0.01)} compressed")
    # sentence table on the new timebase
    seg, c = [], []
    for w in words:
        c.append(w)
        if w["w"].rstrip().endswith((".", "?", "!")): seg.append(c); c = []
    if c: seg.append(c)
    for s in seg:
        print(f'  {s[0]["s"]:6.2f} -> {s[-1]["e"]:6.2f}  ' + " ".join(x["w"] for x in s))

main()
