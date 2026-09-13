#!/usr/bin/env python3
"""Generate the two Fall AI-VO ad reads with ElevenLabs.

The API key is read from ELEVENLABS_API_KEY or from a hidden stdin prompt.
It is never written to disk.
"""

import base64
import getpass
import json
import os
import pathlib
import ssl
import sys
import urllib.error
import urllib.request


ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "voiceovers"
OUT.mkdir(parents=True, exist_ok=True)

VOICE_ID = "NBIPq5xdnIg9kaBH5Ape"  # Woman Over 40
VOICE_NAME = "Woman Over 40"
MODEL_ID = "eleven_v3"

# Existing Velantra production notes map the Eleven v3 Creative preset to
# stability 0.0. Similarity/speaker boost mirror prior successful Velantra runs.
VOICE_SETTINGS = {
    "stability": 0.0,
    "similarity_boost": 0.80,
    "use_speaker_boost": True,
}

ADS = {
    "sofia-fall": {
        "name": "VEL-SOFIA-FALL-VO-01",
        "product": "The Sofia Woven Tote",
        "text": (
            "Fall is almost here, and everyone I know swaps out their straw bags "
            "for suede and leather. I think I found the one that stays out all year. "
            "This is the Sofia Woven Tote from Velantra. It has that structured "
            "top-handle shape, so it holds its shape, and the belted leather flap "
            "keeps everything feeling secure. It fits everything, your wallet, a "
            "water bottle, a sweater for when it gets cold. And the caramel with "
            "boots and a chunky knit, it just works. They're having a fall sale "
            "right now, and the colorways go fast. I left the link below."
        ),
    },
    "eleanor-weekender-fall": {
        "name": "VEL-ELEANOR-WEEKENDER-FALL-VO-01",
        "product": "The Eleanor Weekender",
        "text": (
            "Fall is almost here, and I think I just found the perfect bag for every "
            "quick weekend trip between now and Thanksgiving. This is the Eleanor "
            "Weekender from Velantra. It has that structured top-handle shape and "
            "real brass hardware, but it's built like an actual travel bag. It fits "
            "everything, two outfits, shoes, your toiletries, and it holds its shape "
            "even packed full. It comes in light chocolate and army green, which "
            "feel like fall. They're having a fall sale right now, so if you've got "
            "a trip coming up, this is the one. I left the link below."
        ),
    },
}


def api_key() -> str:
    key = os.environ.get("ELEVENLABS_API_KEY")
    if key:
        return key.strip()
    if sys.stdin.isatty():
        return getpass.getpass("ElevenLabs API key: ").strip()
    return sys.stdin.readline().strip()


def words_from_alignment(alignment):
    chars = alignment["characters"]
    starts = alignment["character_start_times_seconds"]
    ends = alignment["character_end_times_seconds"]
    words = []
    current = ""
    start = None
    previous_end = 0

    for char, char_start, char_end in zip(chars, starts, ends):
        if char.isspace():
            if current:
                words.append({"word": current, "start": start, "end": previous_end})
                current = ""
                start = None
            continue
        if not current:
            start = char_start
        current += char
        previous_end = char_end

    if current:
        words.append({"word": current, "start": start, "end": previous_end})

    return words


def request_voice(key: str, text: str):
    payload = {
        "text": text,
        "model_id": MODEL_ID,
        "voice_settings": VOICE_SETTINGS,
        "apply_text_normalization": "on",
    }
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/with-timestamps",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "xi-api-key": key,
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        import certifi

        context = ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        context = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, context=context, timeout=300) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"ElevenLabs error {exc.code}: {body[:800]}") from exc


def generate_one(key: str, slug: str, spec: dict):
    data = request_voice(key, spec["text"])
    if "audio_base64" not in data:
        raise RuntimeError(json.dumps(data)[:800])

    audio = base64.b64decode(data["audio_base64"])
    alignment = data.get("alignment") or data.get("normalized_alignment")
    words = words_from_alignment(alignment) if alignment else []
    duration = words[-1]["end"] if words else None

    mp3_path = OUT / f"{spec['name']}.mp3"
    words_path = OUT / f"{spec['name']}.words.json"
    mp3_path.write_bytes(audio)
    words_path.write_text(
        json.dumps(
            {
                "slug": slug,
                "name": spec["name"],
                "product": spec["product"],
                "voice_name": VOICE_NAME,
                "voice_id": VOICE_ID,
                "model_id": MODEL_ID,
                "voice_settings": VOICE_SETTINGS,
                "duration_seconds": duration,
                "word_count": len(spec["text"].split()),
                "words": words,
                "script": spec["text"],
            },
            indent=2,
        )
    )
    wpm = (len(spec["text"].split()) / duration * 60) if duration else 0
    print(f"{spec['name']}: {duration:.2f}s, {wpm:.0f} wpm -> {mp3_path}")


def main():
    key = api_key()
    if not key:
        raise SystemExit("No ElevenLabs API key provided.")

    (OUT / "scripts-used.json").write_text(
        json.dumps(
            {
                "voice_name": VOICE_NAME,
                "voice_id": VOICE_ID,
                "model_id": MODEL_ID,
                "voice_settings": VOICE_SETTINGS,
                "ads": ADS,
            },
            indent=2,
        )
    )

    for slug, spec in ADS.items():
        generate_one(key, slug, spec)


if __name__ == "__main__":
    main()
