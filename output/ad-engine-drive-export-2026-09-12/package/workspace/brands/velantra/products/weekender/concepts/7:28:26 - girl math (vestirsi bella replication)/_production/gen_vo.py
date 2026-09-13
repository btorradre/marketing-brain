"""Step 3 — ElevenLabs VO. One seamless full-length track per version, never per-line splices.

Uses /with-timestamps so the caption track and the timeline can be cut to real word times
instead of guessed ones.
"""
import base64, json, os, pathlib, subprocess, sys

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from scenes import SCRIPTS

KEY = os.environ["ELEVENLABS_API_KEY"]
OUT = HERE / "vo"; OUT.mkdir(exist_ok=True)

# Brooks 2026-07-29: the multilingual-v2 read came back robotic. Switched to the cloned
# "Woman Over 40" voice on eleven_v3 with the Creative stability preset.
VOICE = "NBIPq5xdnIg9kaBH5Ape"  # "Woman Over 40" (cloned)
MODEL = "eleven_v3"
# v3 maps stability to three presets: 0.0 Creative / 0.5 Natural / 1.0 Robust.
# v3 has no `speed` or `style` parameter, so runtime is whatever the read gives us.
SETTINGS = {"stability": 0.0, "similarity_boost": 0.80, "use_speaker_boost": True}


def words_from_alignment(a):
    """Collapse character alignment into (word, start, end)."""
    out, cur, st = [], "", None
    for ch, s, e in zip(a["characters"], a["character_start_times_seconds"],
                        a["character_end_times_seconds"]):
        if ch.isspace():
            if cur:
                out.append({"w": cur, "start": st, "end": prev_e}); cur, st = "", None
        else:
            if not cur:
                st = s
            cur += ch
            prev_e = e
    if cur:
        out.append({"w": cur, "start": st, "end": prev_e})
    return out


def tts(text, stem):
    body = {"text": text, "model_id": MODEL, "voice_settings": SETTINGS}
    req = HERE / ".tmp" / "el.json"
    req.parent.mkdir(exist_ok=True)
    req.write_text(json.dumps(body))
    raw = subprocess.run(
        ["curl", "-s", "-X", "POST",
         f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps",
         "-H", f"xi-api-key: {KEY}", "-H", "Content-Type: application/json", "-d", f"@{req}"],
        capture_output=True, text=True).stdout
    d = json.loads(raw)
    if "audio_base64" not in d:
        raise RuntimeError(raw[:400])
    (OUT / f"{stem}.mp3").write_bytes(base64.b64decode(d["audio_base64"]))
    a = d.get("alignment") or d["normalized_alignment"]
    (OUT / f"{stem}.words.json").write_text(json.dumps(words_from_alignment(a), indent=1))


def dur(p):
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
        capture_output=True, text=True).stdout.strip())


if __name__ == "__main__":
    for ver, text in SCRIPTS.items():
        stem = f"vo-{ver}"
        if not (OUT / f"{stem}.words.json").exists():
            tts(text, stem)
        w = json.loads((OUT / f"{stem}.words.json").read_text())
        print(f"{stem}.mp3  {dur(OUT / f'{stem}.mp3'):.1f}s  {len(w)} words  "
              f"last word ends {w[-1]['end']:.1f}s")
