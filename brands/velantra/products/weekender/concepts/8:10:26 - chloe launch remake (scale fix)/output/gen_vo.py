#!/usr/bin/env python3
"""DC-02 VO takes from the velantra-blair-chloe-dc clone + word-level STT gate."""
import json, os, ssl, sys, time, urllib.request

import certifi
CTX = ssl.create_default_context(cafile=certifi.where())

ROOT = os.path.dirname(os.path.abspath(__file__))
ENV = "/Users/brooksorradre2/Documents/marketing brain/.env"

def env(name, path=ENV):
    for line in open(path):
        if line.strip().startswith(name + "="):
            return line.strip().split("=", 1)[1]
    return None

EL_KEY = env("ELEVENLABS_API_KEY")
OPENAI_KEY = env("OPENAI_API_KEY", os.path.expanduser("~/.config/watch/.env"))
VOICE = "oltTSSZ5bHj6XqJOWp5b"  # velantra-blair-chloe-dc

LINES = {
    "s1": ("Introducing the Velantra Weekender, our first ever travel bag, and it might be the most beautiful thing we have ever made. Let me show you.", 3),
    "s2": ("It holds three days of clothes, slides right into the overhead bin, and keeps its shape, packed full or empty.", 2),
    "s3": ("Everything for the weekend goes in one bag, and the flap folds all the way back while you pack it.", 2),
    "s4": ("It still carries like a handbag, even packed for three days.", 2),
    "s5": ("The Weekender is on the site now, and this first run will not last long.", 3),
}

def tts(text, out):
    body = json.dumps({
        "text": text,
        "model_id": "eleven_v3",
        "voice_settings": {"stability": 0.0, "similarity_boost": 0.85},
    }).encode()
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}?output_format=mp3_44100_128",
        data=body, method="POST")
    req.add_header("xi-api-key", EL_KEY)
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=120, context=CTX) as r:
        open(out, "wb").write(r.read())

def stt_words(path):
    import subprocess
    r = subprocess.run([
        "curl", "-s", "--cacert", certifi.where(),
        "https://api.openai.com/v1/audio/transcriptions",
        "-H", f"Authorization: Bearer {OPENAI_KEY}",
        "-F", f"file=@{path}", "-F", "model=whisper-1",
        "-F", "response_format=verbose_json",
        "-F", "timestamp_granularities[]=word",
    ], capture_output=True, text=True)
    return json.loads(r.stdout)

results = {}
for seg, (text, n) in LINES.items():
    results[seg] = []
    for i in range(1, n + 1):
        out = os.path.join(ROOT, f"vo_{seg}_take{i}.mp3")
        if not os.path.exists(out):
            for attempt in range(3):
                try:
                    tts(text, out)
                    break
                except Exception as e:
                    print(f"{seg} take{i} tts retry {attempt+1}: {e}", file=sys.stderr)
                    time.sleep(5)
        j = stt_words(out)
        words = [w["word"] for w in j.get("words", [])]
        results[seg].append({"take": i, "file": os.path.basename(out),
                             "text": j.get("text", ""), "words": words})
        print(f"{seg} take{i}: {j.get('text','')[:120]}")

json.dump(results, open(os.path.join(ROOT, "vo_stt_results.json"), "w"), indent=1)
print("done")
