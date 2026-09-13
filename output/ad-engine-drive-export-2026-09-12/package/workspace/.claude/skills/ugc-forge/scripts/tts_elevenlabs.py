"""ElevenLabs speech synthesis — the ONLY speech source in the pipeline.

Veo's native audio is never used (we pass generate_audio=False to Veo and mux
these stems in untouched). Uses the ElevenLabs REST API via `requests` so no
extra SDK install is required. The API key is read from ELEVENLABS_API_KEY and
is never logged or printed.
"""
import os

import requests

from util import RetryableError, log, with_backoff, ffprobe_duration

API = "https://api.elevenlabs.io/v1"
# Multilingual v2 honors SSML <phoneme> tags and gives the most stable timbre
# across segments. Override with --tts-model if you need turbo/flash.
DEFAULT_MODEL = "eleven_multilingual_v2"


def _voice_settings():
    # Stable settings keep the timbre identical across every segment & creator.
    return {
        "stability": 0.5,
        "similarity_boost": 0.85,
        "style": 0.0,
        "use_speaker_boost": True,
    }


def synthesize(text: str, *, voice_id: str, out_path: str,
               model_id: str = DEFAULT_MODEL, ssml: bool = False) -> float:
    """Synthesize `text` to `out_path` (mp3). Returns measured duration (s).

    The audio is authoritative: callers must conform VIDEO to this duration and
    must never stretch / trim / pitch-shift / re-encode this audio.
    """
    key = os.environ["ELEVENLABS_API_KEY"]
    url = f"{API}/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": key,
        "accept": "audio/mpeg",
        "content-type": "application/json",
    }
    payload = {
        "text": text,
        "model_id": model_id,
        "voice_settings": _voice_settings(),
    }
    # SSML phoneme tags require the text to be flagged as SSML for capable models.
    if ssml:
        payload["text"] = f"<speak>{text}</speak>"

    def _call():
        resp = requests.post(url, headers=headers, json=payload, timeout=180)
        if resp.status_code == 429 or resp.status_code >= 500:
            raise RetryableError(f"ElevenLabs HTTP {resp.status_code}")
        if resp.status_code != 200:
            # Surface body for 4xx (bad voice id, quota) but never the key.
            raise SystemExit(f"[ugc-forge] ElevenLabs error {resp.status_code}: {resp.text[:300]}")
        return resp.content

    audio = with_backoff(_call, label="elevenlabs.tts")
    with open(out_path, "wb") as f:
        f.write(audio)
    dur = ffprobe_duration(out_path)
    log(f"tts -> {os.path.basename(out_path)} ({dur:.2f}s)")
    return dur
