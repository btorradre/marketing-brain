#!/usr/bin/env python3
"""STT read-back gate. Checks the Vel-vs-Vol onset and 'Colette'. Usage: stt_gate.py <mp3...>"""
import json, os, re, subprocess, sys
VAULT = os.path.expanduser("~/Documents/marketing brain")
ENV = {}
for line in open(os.path.join(VAULT, ".env")):
    line = line.strip()
    if "=" in line and not line.startswith("#"):
        k, v = line.split("=", 1); ENV[k] = v.strip().strip('"').strip("'")
KEY = ENV["ELEVENLABS_API_KEY"]

for f in sys.argv[1:]:
    out = subprocess.run(["curl", "-s", "--max-time", "300",
        "https://api.elevenlabs.io/v1/speech-to-text",
        "-H", f"xi-api-key: {KEY}",
        "-F", f"file=@{f}", "-F", "model_id=scribe_v1"],
        capture_output=True, text=True)
    d = json.loads(out.stdout)
    txt = d.get("text", "")
    name = os.path.basename(f)
    # Vel onset is the only real signal; the a/e vowel is STT jitter.
    brand = re.findall(r"\b[VvWw][aeoi][a-z]*(?:tra|tre|nte?ra|lantra|lentra)\b", txt, re.I)
    bad_onset = [b for b in brand if b.lower().startswith(("vo", "wo", "va"))]
    colette = re.findall(r"\bcol[ae]tte?\b", txt, re.I)
    print(f"--- {name}")
    print(f"    brand heard: {brand or 'NONE FOUND'}   bad onset: {bad_onset or 'none'}")
    print(f"    colette heard: {colette or 'NONE FOUND'}")
    print(f"    GATE: {'FAIL' if bad_onset or not colette else 'PASS'}")
    open(f.replace('.mp3', '-stt.txt'), 'w').write(txt)
    print(f"    {txt}")
