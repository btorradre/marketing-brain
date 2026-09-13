#!/usr/bin/env python3
"""ElevenLabs v3 TTS with character-level timestamps -> mp3 + words.json.

Usage: tts_v3.py <out-stem> <stability> <similarity> [speed] [< text on stdin]

stability for v3 must be exactly 0.0 (Creative), 0.5 (Natural) or 1.0 (Robust).
"""
import base64, json, os, subprocess, sys, tempfile

VAULT = os.path.expanduser("~/Documents/marketing brain")
ENV = {}
for line in open(os.path.join(VAULT, ".env")):
    line = line.strip()
    if "=" in line and not line.startswith("#"):
        k, v = line.split("=", 1)
        ENV[k] = v.strip().strip('"').strip("'")
KEY = ENV["ELEVENLABS_API_KEY"]
VOICE = os.environ.get("EL_VOICE", "5VJqyR650KC1jubNlVCG")
MODEL = "eleven_v3"


def words_from_alignment(text, al):
    """Collapse ElevenLabs character alignment into word spans."""
    chars = al["characters"]
    starts = al["character_start_times_seconds"]
    ends = al["character_end_times_seconds"]
    words, cur, s = [], "", None
    for ch, cs, ce in zip(chars, starts, ends):
        if ch.isspace():
            if cur:
                words.append({"w": cur, "s": round(s, 3), "e": round(prev_e, 3)})
                cur, s = "", None
        else:
            if not cur:
                s = cs
            cur += ch
            prev_e = ce
    if cur:
        words.append({"w": cur, "s": round(s, 3), "e": round(prev_e, 3)})
    return words


def synth(text, stem, stability, similarity, speed=None):
    vs = {"stability": stability, "similarity_boost": similarity, "use_speaker_boost": True}
    if speed is not None:
        vs["speed"] = speed
    payload = {"text": text, "model_id": MODEL, "voice_settings": vs}
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
        json.dump(payload, fh)
        p = fh.name
    try:
        out = subprocess.run(
            ["curl", "-s", "--max-time", "300",
             f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps"
             "?output_format=mp3_44100_192",
             "-H", f"xi-api-key: {KEY}", "-H", "Content-Type: application/json",
             "--data-binary", f"@{p}"],
            capture_output=True, text=True)
    finally:
        os.unlink(p)
    d = json.loads(out.stdout)
    if "audio_base64" not in d:
        raise RuntimeError("EL error: " + json.dumps(d)[:600])
    open(stem + ".mp3", "wb").write(base64.b64decode(d["audio_base64"]))
    al = d.get("normalized_alignment") or d.get("alignment")
    words = words_from_alignment(text, al)
    json.dump(words, open(stem + "-words.json", "w"), indent=1)
    return stem + ".mp3", words


if __name__ == "__main__":
    stem = sys.argv[1]
    stab = float(sys.argv[2])
    sim = float(sys.argv[3])
    spd = float(sys.argv[4]) if len(sys.argv) > 4 else None
    txt = sys.stdin.read().strip()
    f, w = synth(txt, stem, stab, sim, spd)
    print("OK", f, f"{len(w)} words, {w[-1]['e']:.2f}s")
