#!/usr/bin/env python3
"""AD4 voiceover: one continuous ElevenLabs v3 pass + word timestamps."""
import base64, json, os, pathlib, subprocess, sys

HERE = pathlib.Path(__file__).parent
OUT = HERE / "vo"; OUT.mkdir(exist_ok=True)
ROOT = pathlib.Path("/Users/brooksorradre2/Documents/marketing brain")
for line in (ROOT / ".env").read_text().splitlines():
    if "=" in line and not line.strip().startswith("#"):
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
KEY = os.environ["ELEVENLABS_API_KEY"]

VOICE = "5VJqyR650KC1jubNlVCG"   # velantra-blair-colette-0805, the v3 re-clone

# Spoken-delivery version. Commas and periods only. Numerals spelled out.
SCRIPT = (
    "Girls, if you want one bag that gets you through the school run, the coffee run "
    "and everything after, this is it. This is the Colette from Velantra, in "
    "cashmere feel brushed wool. It's Loro Piana inspired, so the belted front holds "
    "it upright instead of slumping. Twenty inches across, and it fits a thirteen inch "
    "laptop with room left over. Leather wrapped handles, aged gold hardware, and no "
    "logo on it anywhere. Caramel or espresso. They're running a pre-order right now, "
    "thirty dollars off before it ships. So go get one, girls, and thank me later."
)


def gen(tag, seed=None):
    dest = OUT / f"cand-{tag}.mp3"
    words = OUT / f"cand-{tag}-words.json"
    if dest.exists() and words.exists():
        print(f"  cached {tag}"); return
    body = {
        "text": SCRIPT,
        "model_id": "eleven_v3",
        # Creative preset: stability 0.0, similarity 0.85 (see UGC-REVIEW v3 README)
        "voice_settings": {"stability": 0.0, "similarity_boost": 0.85, "use_speaker_boost": True},
    }
    if seed is not None:
        body["seed"] = seed
    pf = OUT / f"_body-{tag}.json"; pf.write_text(json.dumps(body))
    url = (f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}"
           f"/with-timestamps?output_format=mp3_44100_128")
    r = subprocess.run(["curl", "-s", "--max-time", "600", url,
                        "-H", f"xi-api-key: {KEY}",
                        "-H", "Content-Type: application/json",
                        "--data-binary", f"@{pf}"], capture_output=True, text=True)
    try:
        d = json.loads(r.stdout)
    except Exception:
        print(f"  {tag} FAIL: {r.stdout[:400]}"); return
    if "audio_base64" not in d:
        print(f"  {tag} ERR: {json.dumps(d)[:400]}"); return
    dest.write_bytes(base64.b64decode(d["audio_base64"]))
    words.write_text(json.dumps(d.get("alignment") or d.get("normalized_alignment"), indent=1))
    dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(dest)], capture_output=True, text=True).stdout.strip()
    wc = len(SCRIPT.split())
    print(f"  {tag}: {dest.name}  {dur}s  {wc}w  {wc/float(dur):.2f} w/s")


if __name__ == "__main__":
    print(f"script: {len(SCRIPT.split())} words")
    for tag, seed in (("A", 11), ("B", 27), ("C", 43)):
        gen(tag, seed)
