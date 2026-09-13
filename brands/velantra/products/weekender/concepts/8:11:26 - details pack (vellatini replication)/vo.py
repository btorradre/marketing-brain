#!/usr/bin/env python3
"""Generate the front-loaded VO for the details-pack ads.

The reference speaks its two lines once, at the top, in a single unbroken take
(0.20-4.54s), then hands off to the music. So each ad gets ONE continuous
take covering both lines, never one render per line.

Three takes per ad; each is transcribed word-level so the pick is made on what
was actually said and so the caption timings can be driven off the real audio.
"""
import json
import os
import subprocess
import sys

W = "/private/tmp/claude-503/-Users-brooksorradre2-Documents-marketing-brain/b16ffd58-65c2-46a4-81f8-4d8d6f55cdd7/scratchpad/vellatini-uzptt3"
VO = f"{W}/vo"
os.makedirs(VO, exist_ok=True)
KEY = os.environ["ELEVENLABS_API_KEY"]

ADS = {
    "wk": {
        "voice": "hGQkZQUA5RiOXIw7P9iO",   # Kiora — travel/weekend register
        "text": "Nothing changes how you pack faster than the right bag.\n\nThree days. One bag.",
    },
    "col": {
        "voice": "T720RsqorTx4ZZWohrNN",   # Katie — fall everyday register
        "text": "Nothing pulls an outfit together faster than the right bag.\n\nThe difference is in the details.",
    },
}

MODELS = ["eleven_v3", "eleven_multilingual_v2"]


def tts(voice, text, out, model):
    payload = {
        "text": text,
        "model_id": model,
        "voice_settings": {"stability": 0.0, "similarity_boost": 0.85,
                           "style": 0.0, "use_speaker_boost": True},
    }
    r = subprocess.run([
        "curl", "-s", "-w", "%{http_code}", "-o", out,
        "-X", "POST", f"https://api.elevenlabs.io/v1/text-to-speech/{voice}?output_format=mp3_44100_128",
        "-H", f"xi-api-key: {KEY}", "-H", "Content-Type: application/json",
        "-d", json.dumps(payload)], capture_output=True, text=True)
    return r.stdout.strip()


def stt(path):
    r = subprocess.run([
        "curl", "-s", "-X", "POST", "https://api.elevenlabs.io/v1/speech-to-text",
        "-H", f"xi-api-key: {KEY}", "-F", f"file=@{path}",
        "-F", "model_id=scribe_v1", "-F", "timestamps_granularity=word"],
        capture_output=True, text=True)
    try:
        return json.loads(r.stdout)
    except Exception:
        return {"text": "PARSE_ERROR", "words": []}


def main():
    model = None
    for m in MODELS:
        code = tts(ADS["wk"]["voice"], "Test.", f"{VO}/_probe.mp3", m)
        if code == "200" and os.path.getsize(f"{VO}/_probe.mp3") > 2000:
            model = m
            break
        print(f"  model {m} unavailable (HTTP {code})")
    if not model:
        sys.exit("no usable TTS model")
    print(f"model = {model}\n")

    for tag, cfg in ADS.items():
        for i in (1, 2, 3):
            p = f"{VO}/{tag}_take{i}.mp3"
            code = tts(cfg["voice"], cfg["text"], p, model)
            if code != "200":
                print(f"{tag} take{i}: HTTP {code}")
                continue
            dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                  "format=duration", "-of", "csv=p=0", p],
                                 capture_output=True, text=True).stdout.strip()
            d = stt(p)
            words = [w for w in d.get("words", []) if w.get("type") == "word"]
            said = " ".join(w["text"] for w in words)
            print(f"{tag} take{i}  {float(dur):5.2f}s  {said}")
            json.dump(d, open(f"{VO}/{tag}_take{i}.json", "w"))


if __name__ == "__main__":
    main()
