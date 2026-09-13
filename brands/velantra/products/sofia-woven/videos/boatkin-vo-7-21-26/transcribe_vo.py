#!/usr/bin/env python3
"""Word-level timings for all 15 VO tracks via OpenAI Whisper (verbose_json).
Writes vo/<AD>.words.json: [{"w": word, "s": start, "e": end}, ...]
Key comes from ~/.config/watch/.env (OPENAI_API_KEY).
"""
import json, os, glob, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
VO = os.path.join(ROOT, "vo")

key = None
for envp in (os.path.expanduser("~/.config/watch/.env"),):
    if os.path.exists(envp):
        for line in open(envp):
            line = line.strip()
            if line.startswith("OPENAI_API_KEY=") and len(line.split("=", 1)[1]) > 10:
                key = line.split("=", 1)[1].strip().strip('"')
assert key, "no OPENAI_API_KEY"

FIX = {"boat kin": "boatkin", "botkin": "boatkin", "boatkins": "boatkin",
       "sea grass": "seagrass", "seagrasses": "seagrass"}

for d in sorted(glob.glob(os.path.join(VO, "S*-v*"))):
    ad = os.path.basename(d)
    outp = os.path.join(VO, f"{ad}.words.json")
    if os.path.exists(outp):
        print(f"{ad}: exists, skip", flush=True)
        continue
    mp3 = sorted(glob.glob(os.path.join(d, "*.mp3")))[0]
    r = subprocess.run([
        "curl", "-s", "https://api.openai.com/v1/audio/transcriptions",
        "-H", f"Authorization: Bearer {key}",
        "-F", f"file=@{mp3}", "-F", "model=whisper-1",
        "-F", "response_format=verbose_json",
        "-F", "timestamp_granularities[]=word",
        "-F", "language=en"], capture_output=True, text=True)
    try:
        data = json.loads(r.stdout)
        words = [{"w": w["word"].strip(), "s": round(w["start"], 3), "e": round(w["end"], 3)}
                 for w in data["words"]]
    except Exception as e:
        print(f"{ad}: FAILED {e} :: {r.stdout[:200]}", flush=True)
        continue
    # normalize known mishearings
    joined = []
    i = 0
    while i < len(words):
        if i + 1 < len(words):
            pair = (words[i]["w"] + " " + words[i + 1]["w"]).lower()
            if pair in FIX:
                joined.append({"w": FIX[pair], "s": words[i]["s"], "e": words[i + 1]["e"]})
                i += 2
                continue
        w = dict(words[i])
        if w["w"].lower() in FIX:
            w["w"] = FIX[w["w"].lower()]
        joined.append(w)
        i += 1
    with open(outp, "w") as f:
        json.dump({"duration": data.get("duration"), "words": joined}, f)
    print(f"{ad}: {len(joined)} words, {data.get('duration')}s", flush=True)
print("done", flush=True)
