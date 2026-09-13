#!/usr/bin/env python3
"""eleven_v3 Creative TTS with word timestamps. Usage: tts.py <voice_id> <hook A|B|C> <out-stem>"""
import base64, json, os, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from script_text import full

VAULT = os.path.expanduser("~/Documents/marketing brain")
ENV = {}
for line in open(os.path.join(VAULT, ".env")):
    line = line.strip()
    if "=" in line and not line.startswith("#"):
        k, v = line.split("=", 1)
        ENV[k] = v.strip().strip('"').strip("'")
KEY = ENV["ELEVENLABS_API_KEY"]
MODEL = os.environ.get("EL_MODEL", "eleven_v3")


def words_from_alignment(al):
    chars, starts, ends = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
    words, cur, s, prev_e = [], "", None, 0
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


def synth(voice, text, stem):
    # Creative preset: stability 0.0, similarity 0.85, speaker boost on.
    sim = float(os.environ.get("EL_SIM", "0.85"))
    payload = {"text": text, "model_id": MODEL,
               "voice_settings": {"stability": 0.0, "similarity_boost": sim, "use_speaker_boost": True}}
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
        json.dump(payload, fh); p = fh.name
    try:
        out = subprocess.run(
            ["curl", "-s", "--max-time", "300",
             f"https://api.elevenlabs.io/v1/text-to-speech/{voice}/with-timestamps?output_format=mp3_44100_192",
             "-H", f"xi-api-key: {KEY}", "-H", "Content-Type: application/json",
             "--data-binary", f"@{p}", "--retry", "3", "--retry-all-errors"],
            capture_output=True, text=True)
    finally:
        os.unlink(p)
    if not out.stdout.strip():
        raise RuntimeError(f"EMPTY response (curl rc={out.returncode}) stderr={out.stderr[:300]}")
    d = json.loads(out.stdout)
    if "audio_base64" not in d:
        raise RuntimeError("EL error: " + json.dumps(d)[:600])
    open(stem + ".mp3", "wb").write(base64.b64decode(d["audio_base64"]))
    words = words_from_alignment(d.get("normalized_alignment") or d["alignment"])
    json.dump(words, open(stem + "-words.json", "w"), indent=1)
    return words


if __name__ == "__main__":
    voice, hook, stem = sys.argv[1], sys.argv[2], sys.argv[3]
    w = synth(voice, full(hook), stem)
    dur = w[-1]["e"]
    print(f"OK {os.path.basename(stem):<34} {len(w)} words  {dur:5.2f}s  {len(w)/dur*60:3.0f} wpm  [{MODEL} sim={os.environ.get('EL_SIM','0.85')}]")
