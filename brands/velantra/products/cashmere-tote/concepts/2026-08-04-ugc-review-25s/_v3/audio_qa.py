#!/usr/bin/env python3
"""Gemini audio judge. Usage: audio_qa.py "<question>" file1 [file2 ...]

urllib dies on generativelanguage certs on this machine (see memory), so the
request goes out through curl --data-binary.
"""
import base64, json, os, subprocess, sys, tempfile

VAULT = os.path.expanduser("~/Documents/marketing brain")
ENV = {}
for line in open(os.path.join(VAULT, ".env")):
    line = line.strip()
    if "=" in line and not line.startswith("#"):
        k, v = line.split("=", 1)
        ENV[k] = v.strip().strip('"').strip("'")
KEY = ENV["GEMINI_API_KEY"]
MODEL = "gemini-3.6-flash"

MIME = {".mp3": "audio/mp3", ".wav": "audio/wav", ".m4a": "audio/mp4", ".aac": "audio/aac"}


def ask(question, files):
    parts = [{"text": question}]
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        parts.append({"text": f"\n--- FILE: {os.path.basename(f)} ---"})
        parts.append({"inline_data": {"mime_type": MIME.get(ext, "audio/mp3"),
                                      "data": base64.b64encode(open(f, "rb").read()).decode()}})
    payload = {"contents": [{"parts": parts}],
               "generationConfig": {"temperature": 0.2}}
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
        json.dump(payload, fh)
        p = fh.name
    try:
        out = subprocess.run(
            ["curl", "-s", "--max-time", "300",
             f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={KEY}",
             "-H", "Content-Type: application/json", "--data-binary", f"@{p}"],
            capture_output=True, text=True)
        d = json.loads(out.stdout)
    finally:
        os.unlink(p)
    if "candidates" not in d:
        return "ERROR: " + json.dumps(d)[:600]
    return "".join(c.get("text", "") for c in d["candidates"][0]["content"]["parts"])


if __name__ == "__main__":
    print(ask(sys.argv[1], sys.argv[2:]))
