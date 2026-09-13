#!/usr/bin/env python3
"""
Chunk a continuous spoken VSL script into N text chunks of ~target_seconds
each, splitting at sentence boundaries (. ? !) preferring the strongest
boundary closest to the target word count.

No audio is rendered — Seedance generates audio per segment natively.

Output: chunks_manifest.json with each chunk's index, text, word count,
estimated_seconds, and the recommended Seedance --duration (clamped 4-10s).
"""
import argparse, json, pathlib, sys, re

WORDS_PER_SEC = 4.2  # conversational rant cadence

def split_sentences(text):
    """Split into sentence-ish units, keeping terminal punctuation."""
    # Split on . ? ! followed by whitespace, retain the punctuation.
    parts = re.split(r'(?<=[.!?])\s+', text.strip())
    return [p.strip() for p in parts if p.strip()]

def chunk(script_text, target_seconds, min_seconds, max_seconds):
    target_words = int(target_seconds * WORDS_PER_SEC)
    min_words = int(min_seconds * WORDS_PER_SEC)
    max_words = int(max_seconds * WORDS_PER_SEC)

    sentences = split_sentences(script_text)
    chunks = []
    current = []
    cur_wc = 0

    def flush():
        nonlocal current, cur_wc
        if not current: return
        text = " ".join(current).strip()
        wc = len(text.split())
        est_sec = wc / WORDS_PER_SEC
        seedance_dur = max(4, min(10, int(round(est_sec))))
        chunks.append({
            "index": len(chunks) + 1,
            "text": text,
            "word_count": wc,
            "estimated_seconds": round(est_sec, 2),
            "seedance_duration": seedance_dur,
        })
        current = []
        cur_wc = 0

    for sent in sentences:
        swc = len(sent.split())
        # If this single sentence exceeds max_words, hard-split at commas as fallback
        if swc > max_words:
            # Split at commas
            comma_parts = [p.strip() for p in re.split(r',\s+', sent) if p.strip()]
            running = []; running_wc = 0
            for cp in comma_parts:
                cwc = len(cp.split())
                if running_wc + cwc > max_words and running:
                    # flush running
                    if cur_wc + running_wc >= min_words:
                        current.append(", ".join(running))
                        cur_wc += running_wc
                        flush()
                    else:
                        current.append(", ".join(running))
                        cur_wc += running_wc
                    running = [cp]; running_wc = cwc
                else:
                    running.append(cp); running_wc += cwc
            if running:
                joined = ", ".join(running)
                # Also restore terminal punct on the last
                if not joined.endswith((".", "!", "?")):
                    joined += "."
                current.append(joined)
                cur_wc += running_wc
            continue

        # Normal case: would adding this sentence keep us within max?
        if cur_wc + swc <= max_words:
            current.append(sent)
            cur_wc += swc
            # If we're already near target, flush at next punctuation
            if cur_wc >= target_words:
                flush()
        else:
            # Adding this would overflow — flush current first if it has anything,
            # then start a new chunk with this sentence.
            if cur_wc >= min_words:
                flush()
                current = [sent]; cur_wc = swc
            else:
                # Current too short to flush, just append and let it overflow slightly
                current.append(sent); cur_wc += swc
                flush()

    flush()
    return chunks

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--script", required=True, help="path to .txt or literal string")
    p.add_argument("--target-seconds", type=float, default=8.0)
    p.add_argument("--min-seconds", type=float, default=5.0)
    p.add_argument("--max-seconds", type=float, default=10.0)
    p.add_argument("--output", required=True, help="output chunks_manifest.json path")
    a = p.parse_args()
    text = pathlib.Path(a.script).read_text() if pathlib.Path(a.script).exists() else a.script
    chunks = chunk(text, a.target_seconds, a.min_seconds, a.max_seconds)
    pathlib.Path(a.output).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.output).write_text(json.dumps({
        "source_script_words": len(text.split()),
        "source_estimated_seconds": round(len(text.split())/WORDS_PER_SEC, 2),
        "chunks_count": len(chunks),
        "chunks": chunks,
    }, indent=2))
    print(f"[chunk] {len(chunks)} chunks from {len(text.split())} words", file=sys.stderr)
    for c in chunks:
        print(f"  chunk_{c['index']:03d} {c['word_count']}w/{c['estimated_seconds']:.1f}s ({c['seedance_duration']}s rounded): \"{c['text'][:70]}...\"", file=sys.stderr)

if __name__ == "__main__":
    main()
