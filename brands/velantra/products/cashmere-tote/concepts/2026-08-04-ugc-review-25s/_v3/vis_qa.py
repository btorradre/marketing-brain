#!/usr/bin/env python3
"""Gemini vision judge for keyframes / extracted video frames.

Usage: vis_qa.py "<question>" img1 [img2 ...]
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
MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}


def ask(question, files):
    parts = [{"text": question}]
    for f in files:
        parts.append({"text": f"\n--- IMAGE: {os.path.basename(f)} ---"})
        parts.append({"inline_data": {
            "mime_type": MIME.get(os.path.splitext(f)[1].lower(), "image/png"),
            "data": base64.b64encode(open(f, "rb").read()).decode()}})
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
        json.dump({"contents": [{"parts": parts}],
                   "generationConfig": {"temperature": 0.2}}, fh)
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
