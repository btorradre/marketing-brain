import os, json, base64, sys, pathlib, urllib.request, ssl, certifi
CTX = ssl.create_default_context(cafile=certifi.where())

ROOT = "/Users/brooksorradre2/Documents/marketing brain"
KEY = None
for line in open(os.path.join(ROOT, ".env")):
    if line.startswith("ELEVENLABS_API_KEY="):
        KEY = line.split("=", 1)[1].strip().strip('"').strip("'")
assert KEY, "no key"

VOICE = "NBIPq5xdnIg9kaBH5Ape"  # Woman Over 40

TEXT = ("On a girls trip you live out of your bag, so bring one that stands open on its own. "
        "This is the Eleanor Weekender from Vell-Ahn-Trah. "
        "It's fully structured, smooth leather fold-over flap, brass hardware, no logo anywhere on it, "
        "so it keeps its shape packed full or half empty. "
        "I took mine to Charleston in June and never actually unpacked, it just sat open by the bed for three days. "
        "Three days of clothes, shoes, toiletries, and it still goes in the overhead bin. "
        "It comes in four colors, three ship now. "
        "They're running a sale right now, and the colorways go fast. "
        "I left the link below.")

url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps"
out = pathlib.Path("vo"); out.mkdir(exist_ok=True)

for take in (1, 2, 3):
    body = json.dumps({
        "text": TEXT,
        "model_id": "eleven_v3",
        "voice_settings": {"stability": 0.0, "similarity_boost": 0.85, "use_speaker_boost": True},
    }).encode()
    req = urllib.request.Request(url, data=body, headers={
        "xi-api-key": KEY, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300, context=CTX) as r:
            d = json.load(r)
    except urllib.error.HTTPError as e:
        print("take", take, "HTTP", e.code, e.read()[:400].decode()); continue
    (out / f"take{take}.mp3").write_bytes(base64.b64decode(d["audio_base64"]))
    al = d.get("alignment") or d.get("normalized_alignment")
    (out / f"take{take}_align.json").write_text(json.dumps(al))
    print("take", take, "ok", (out / f"take{take}.mp3").stat().st_size, "bytes",
          "end", al["character_end_times_seconds"][-1] if al else "?")
print("chars", len(TEXT))
