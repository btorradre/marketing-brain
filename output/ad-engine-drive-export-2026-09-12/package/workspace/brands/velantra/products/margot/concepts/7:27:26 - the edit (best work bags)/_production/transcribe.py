#!/usr/bin/env python3
"""VEL-MARGOT-EDIT-01 transcript QA — Gemini audio transcription per clip.

  transcribe.py            transcribe every downloaded clip, print line vs expected
  transcribe.py S03 S14    subset

Extracts mono 16k wav via ffmpeg, sends inline base64 to Gemini, compares
against the script line. Flags numerals, missing tails, stray words. The
Sofia v1 price bug ("$109") was audio-only and passed all visual checks —
transcript QA is a shipping gate, not a nicety.
"""
import base64, json, os, re, ssl, subprocess, sys, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import blocks as B

HERE = os.path.dirname(os.path.abspath(__file__))
CLIPS = os.path.normpath(os.path.join(HERE, "..", "assets", "clips"))
MODEL = "gemini-2.5-flash"

def ctx():
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()

def key():
    for line in open("/Users/brooksorradre2/Documents/marketing brain/.env"):
        if line.startswith("GEMINI_API_KEY="):
            return line.strip().split("=", 1)[1]
    raise SystemExit("GEMINI_API_KEY not found")

def transcribe(path, k):
    wav = "/tmp/margot_edit_qa.wav"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", path, "-vn", "-ac", "1", "-ar", "16000", wav], check=True)
    audio = base64.b64encode(open(wav, "rb").read()).decode()
    payload = {"contents": [{"parts": [
        {"text": "Transcribe this audio verbatim. Output ONLY the spoken words, no labels, no punctuation commentary."},
        {"inline_data": {"mime_type": "audio/wav", "data": audio}}]}]}
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={k}",
        data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, context=ctx(), timeout=120) as r:
        d = json.loads(r.read().decode())
    return d["candidates"][0]["content"]["parts"][0]["text"].strip()

def norm(s):
    return re.sub(r"[^a-z0-9 ]", "", s.lower()).split()

if __name__ == "__main__":
    ids = sys.argv[1:]
    k = key()
    issues = 0
    for shot in B.SHOTS:
        sid, line = shot[0], shot[6]
        if ids and sid not in ids:
            continue
        p = os.path.join(CLIPS, f"{sid}.mp4")
        if not os.path.exists(p):
            print(f"{sid}: MISSING")
            continue
        t = transcribe(p, k)
        exp, got = norm(line), norm(t)
        missing = [w for w in exp if w not in got]
        extra = [w for w in got if w not in exp]
        digits = [w for w in got if any(c.isdigit() for c in w)]
        flag = []
        if missing: flag.append(f"MISSING {missing}")
        if extra: flag.append(f"EXTRA {extra}")
        if digits: flag.append(f"NUMERAL {digits}")
        status = "OK " if not flag else "FLAG"
        if flag: issues += 1
        print(f"{sid} {status} | heard: {t}" + (f"  <-- {'; '.join(flag)}" if flag else ""))
    print(f"\n{issues} clips flagged" if issues else "\nall clean")
