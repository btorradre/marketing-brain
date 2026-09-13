#!/usr/bin/env python3
"""
pick_take.py — score candidate takes of one segment and pick the anchor-worthy one.

Long-form chains fail in a specific, compounding way: the open is up-tempo, the back half
decays to monotone, and because every segment seeds off the last one, a faded take poisons
everything downstream. The skill's rule is to QA each clip's LAST sentence for energy fade
and regenerate before chaining. This scores that mechanically so 21 segments do not need 21
human judgement calls.

    python3 pick_take.py seg-03-takeA.mp4 seg-03-takeB.mp4 [--json out.json]

Scoring, all from the audio track:
  disqualify  silent, or speech too short to contain the line
  fade        RMS of the last second of speech vs the clip's speech mean (higher is better)
  coverage    speech duration vs container (too little = dropped words or dead air)
  dynamics    stdev of frame RMS across speech (flat = monotone, the thing we are avoiding)
"""
import argparse
import json
import pathlib
import re
import subprocess
import sys

RMS_RE = re.compile(r"lavfi\.astats\.Overall\.RMS_level=(-?[\d.]+|-inf)")


def run(cmd: list[str]) -> str:
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.stdout + p.stderr


def duration(path: pathlib.Path) -> float:
    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
               "-of", "default=nw=1:nk=1", str(path)]).strip()
    try:
        return float(out.splitlines()[0])
    except (ValueError, IndexError):
        return 0.0


def rms_track(path: pathlib.Path, window: float = 0.1) -> list[float]:
    """Per-window RMS in dB across the whole file. -inf becomes a floor value."""
    # astats only SETS the metadata; ametadata=mode=print is what emits it.
    af = (f"asetnsamples=n={int(48000 * window)},"
          "astats=metadata=1:reset=1,"
          "ametadata=mode=print:key=lavfi.astats.Overall.RMS_level:file=-")
    out = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
               "-af", af, "-f", "null", "-"])
    vals = []
    for m in RMS_RE.finditer(out):
        raw = m.group(1)
        vals.append(-90.0 if raw == "-inf" else float(raw))
    return vals


def speech_span(rms: list[float], floor: float = -45.0) -> tuple[int, int]:
    live = [i for i, v in enumerate(rms) if v > floor]
    return (live[0], live[-1]) if live else (0, -1)


def mean(xs: list[float]) -> float:
    return sum(xs) / len(xs) if xs else 0.0


def stdev(xs: list[float]) -> float:
    if len(xs) < 2:
        return 0.0
    m = mean(xs)
    return (sum((x - m) ** 2 for x in xs) / (len(xs) - 1)) ** 0.5


def score(path: pathlib.Path, window: float = 0.1) -> dict:
    dur = duration(path)
    rms = rms_track(path, window)
    lo, hi = speech_span(rms)
    if hi <= lo:
        return {"file": path.name, "duration": round(dur, 2), "disqualified": "no speech detected",
                "total": -1.0}

    speech = rms[lo:hi + 1]
    speech_seconds = len(speech) * window
    tail_frames = max(1, int(1.0 / window))
    tail = speech[-tail_frames:]

    # Fade: tail loudness relative to the speech mean. ~0 dB means energy held.
    fade_db = mean(tail) - mean(speech)
    dynamics = stdev(speech)
    coverage = speech_seconds / dur if dur else 0.0

    disq = None
    if speech_seconds < 1.0:
        disq = "speech shorter than one second"

    # Normalise each axis to 0-1, then weight. Fade is weighted hardest because a faded
    # take contaminates every downstream segment through the chain.
    fade_n = max(0.0, min(1.0, (fade_db + 12.0) / 12.0))     # -12dB fade -> 0, no fade -> 1
    dyn_n = max(0.0, min(1.0, dynamics / 12.0))              # 12dB spread reads as expressive
    cov_n = max(0.0, min(1.0, coverage / 0.85))

    # Audio-only base score. When the intended line is known, main() re-weights this
    # with word accuracy, which outranks every delivery metric.
    total = -1.0 if disq else round(0.5 * fade_n + 0.3 * dyn_n + 0.2 * cov_n, 4)
    return {
        "file": path.name,
        "duration": round(dur, 2),
        "speech_seconds": round(speech_seconds, 2),
        "coverage": round(coverage, 3),
        "tail_fade_db": round(fade_db, 2),
        "dynamics_db": round(dynamics, 2),
        "disqualified": disq,
        "total": total,
    }


NUM_WORDS = {
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
    "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen",
    "eighteen", "nineteen", "twenty", "thirty", "forty", "fifty", "sixty", "seventy",
    "eighty", "ninety", "hundred", "thousand",
}


def normalise(text: str) -> list[str]:
    """
    Words only, numbers dropped.

    Speech-to-text renders spoken numbers however it likes: "twenty twenty three" comes
    back as "23". Comparing those token-for-token reports a misread that never happened,
    and it does so deterministically, so retrying can never clear it. Numbers are excluded
    from the similarity score and verified separately by locked-term presence instead.
    """
    toks = re.sub(r"[^a-z0-9 ]", " ", text.lower()).split()
    return [t for t in toks if t not in NUM_WORDS and not t.isdigit()]


def transcribe(path: pathlib.Path, api_key: str) -> str:
    """Scribe the take so the words spoken can be checked against the words written."""
    import ssl
    import urllib.request
    try:
        import certifi
        ctx = ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        ctx = ssl.create_default_context()

    wav = path.with_suffix(".scribe.mp3")
    subprocess.run(["ffmpeg", "-y", "-i", str(path), "-vn", "-ac", "1", "-ar", "16000",
                    "-b:a", "48k", str(wav)], capture_output=True)
    boundary = "----picktake"
    body = bytearray()
    body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"model_id\"\r\n\r\nscribe_v1\r\n".encode()
    body += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; "
             f"filename=\"a.mp3\"\r\nContent-Type: audio/mpeg\r\n\r\n").encode()
    body += wav.read_bytes() + f"\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request(
        "https://api.elevenlabs.io/v1/speech-to-text", data=bytes(body),
        headers={"xi-api-key": api_key,
                 "Content-Type": f"multipart/form-data; boundary={boundary}"})
    try:
        with urllib.request.urlopen(req, timeout=300, context=ctx) as resp:
            return json.loads(resp.read()).get("text", "")
    except Exception:
        return ""
    finally:
        wav.unlink(missing_ok=True)


def word_accuracy(spoken: str, intended: str) -> float:
    """
    Ratio of the intended line actually present, in order. 1.0 is a clean read.

    Heard tokens are first snapped to a near-identical intended token. Speech-to-text
    guesses at spelling for anything it has not seen — an invented brand name comes back
    as "Motili" for "Motilli" — and comparing those literally reports a misread that never
    happened, deterministically, so retrying can never clear it. The 0.85 floor is tight
    enough that a genuinely different word does not get snapped and still fails.
    """
    import difflib
    a, b = normalise(spoken), normalise(intended)
    if not b:
        return 1.0
    vocab = set(b)
    snapped = []
    for tok in a:
        if tok in vocab:
            snapped.append(tok)
            continue
        near = difflib.get_close_matches(tok, vocab, n=1, cutoff=0.85)
        snapped.append(near[0] if near else tok)
    return difflib.SequenceMatcher(None, snapped, b).ratio()


def load_key() -> str:
    env = pathlib.Path(__file__).resolve().parents[2] / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            if line.startswith("ELEVENLABS_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("takes", nargs="+")
    ap.add_argument("--json")
    ap.add_argument("--script", help="intended dialogue; enables transcript verification")
    ap.add_argument("--accuracy-floor", type=float, default=0.90,
                    help="below this the take misread the line and is disqualified")
    ap.add_argument("--fade-floor", type=float, default=-6.0,
                    help="tail_fade_db below this is flagged as a faded take")
    args = ap.parse_args()

    results = [score(pathlib.Path(t)) for t in args.takes]

    # Energy scoring is deaf to a mangled or dropped word, which is a hard reject that
    # no amount of good delivery redeems. Transcribe and compare when the line is known.
    if args.script:
        key = load_key()
        for r, t in zip(results, args.takes):
            heard = transcribe(pathlib.Path(t), key) if key else ""
            r["accuracy"] = round(word_accuracy(heard, args.script), 3) if heard else None
            r["heard"] = heard
            if r["accuracy"] is None or r["total"] < 0:
                continue
            if r["accuracy"] < args.accuracy_floor:
                r["disqualified"] = f"misread the line (accuracy {r['accuracy']})"
                r["total"] = -1.0
                continue
            # A single fumbled word in a 30-word beat only costs ~0.02 of ratio, so a
            # flat floor never catches it. Stretch the top of the range instead: 0.97
            # maps to 0 and a clean read maps to 1, then let accuracy outweigh delivery.
            # A correct line read adequately beats a mangled line read beautifully.
            acc_n = max(0.0, min(1.0, (r["accuracy"] - 0.97) / 0.03))
            r["total"] = round(0.55 * acc_n + 0.45 * r["total"], 4)

    for r in results:
        flag = ""
        if r.get("disqualified"):
            flag = f"  DISQUALIFIED: {r['disqualified']}"
        elif r["tail_fade_db"] < args.fade_floor:
            flag = f"  FADED TAIL ({r['tail_fade_db']}dB) — regenerate rather than chain"
        acc = f"  acc {r['accuracy']}" if r.get("accuracy") is not None else ""
        print(f"{r['file']:<26} score {r['total']:>6}  fade {r.get('tail_fade_db', 0):>6}dB  "
              f"dyn {r.get('dynamics_db', 0):>5}dB  cov {r.get('coverage', 0):>5}{acc}{flag}")

    live = [r for r in results if r["total"] >= 0]
    if not live:
        print("\nNo usable take. Regenerate this segment.", file=sys.stderr)
        sys.exit(2)

    win = max(live, key=lambda r: r["total"])
    spread = win["total"] - min(r["total"] for r in live)
    print(f"\nPICK: {win['file']}" + ("   (close call, worth an eyeball)" if spread < 0.05 else ""))

    if args.json:
        pathlib.Path(args.json).write_text(json.dumps(
            {"picked": win["file"], "spread": round(spread, 4), "takes": results}, indent=2))


if __name__ == "__main__":
    main()
