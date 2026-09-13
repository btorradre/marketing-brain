"""ElevenLabs adapter — voiceover on eleven_v3 / Creative, and voice cloning.

DEFAULTS ARE DELIBERATE. eleven_multilingual_v2 was blind-judged 2.5/10 against
a real on-camera voice (flat pitch contour, even syllable spacing, no breaths);
the v3 Creative rebuild scored 9.5/10. So:

  model_id            eleven_v3
  stability           0.0   (Creative — v3 accepts ONLY 0.0 / 0.5 / 1.0)
  similarity_boost    0.85  (0.95 reads more announcer)
  use_speaker_boost   true

Laws baked in here:
  - ONE TAKE. A VO is one continuous generation, never per-line mp3s stitched
    together. There is no per-line render path in this module.
  - v3 hard-caps text at 5,000 chars (400 text_too_long). Over that, split at a
    natural PARAGRAPH boundary into large takes, same voice and settings, and
    stitch with ~0.35s padding (ffmpeg concat). Two large takes at a paragraph
    pause is the accepted reading of the one-take law.
  - v3 exposes no speed control — pace with ffmpeg atempo AFTER generation.
  - Pronunciation respellings are DATA (workspace 'pronunciation' records or the
    job's `pronunciation_fixes`), applied to TTS input only; the human-readable
    script keeps plain spellings.
  - Library / premade voices read flat on v3; clone the creator (IVC) instead.
"""
from __future__ import annotations

import base64
import os
import time

import requests

from adengine.core.errors import ProviderError
from adengine.core.settings import settings
from adengine.engines import shell

BASE_URL = "https://api.elevenlabs.io/v1"
MODEL_V3 = "eleven_v3"
MAX_CHARS_V3 = 5000

# v3 Creative preset — see module docstring, do not "tune" these casually
CREATIVE = {"stability": 0.0, "similarity_boost": 0.85, "use_speaker_boost": True}

# ElevenLabs stock voices usable without cloning (provider ids, not brand data).
STOCK_VOICES = {
    "rachel": "21m00Tcm4TlvDq8ikWAM",
    "drew": "29vD33N1CtxCmqQRPOHJ",
    "clyde": "2EiwWnXFnvU5JabPnv8n",
    "domi": "AZnzlk1XvdvUeBnXmlld",
}

VIDEO_EXTENSIONS = {".mp4", ".mov", ".webm", ".mkv", ".avi", ".flv"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac"}


def apply_pronunciation_fixes(text: str, fixes: dict[str, str] | None) -> str:
    for plain, respelled in (fixes or {}).items():
        if plain:
            text = text.replace(plain, respelled)
    return text


def split_at_paragraph(text: str, limit: int = MAX_CHARS_V3) -> list[str]:
    """Splits only when over the API's hard cap, and only at a paragraph
    boundary — never mid-sentence, never per-line."""
    if len(text) <= limit:
        return [text]
    paragraphs = [p for p in text.split("\n\n") if p.strip()]
    takes, current = [], ""
    for para in paragraphs:
        candidate = f"{current}\n\n{para}" if current else para
        if len(candidate) > limit and current:
            takes.append(current)
            current = para
        else:
            current = candidate
    if current:
        takes.append(current)
    return takes


def tts_one_take(text: str, voice_id: str, key: str, with_timestamps: bool = False,
                 attempts: int = 3, sleep=time.sleep) -> tuple[bytes, dict | None]:
    """Single continuous generation. Returns (mp3 bytes, alignment|None).
    with_timestamps returns character alignment (collapse to words downstream
    for caption sync / slicing) — no separate forced-alignment pass needed."""
    endpoint = f"{BASE_URL}/text-to-speech/{voice_id}"
    if with_timestamps:
        endpoint += "/with-timestamps"
    payload = {"text": text, "model_id": MODEL_V3, "voice_settings": CREATIVE}
    headers = {"xi-api-key": key, "Content-Type": "application/json"}
    if not with_timestamps:
        headers["Accept"] = "audio/mpeg"

    last_err = ""
    for attempt in range(attempts):
        if attempt:
            sleep(5 * attempt)
        resp = requests.post(endpoint, headers=headers, json=payload, timeout=180)
        if resp.status_code == 200:
            if with_timestamps:
                data = resp.json()
                return base64.b64decode(data["audio_base64"]), data.get("alignment")
            return resp.content, None
        last_err = f"HTTP {resp.status_code}: {resp.text[:300]}"
    raise ProviderError(f"ElevenLabs TTS failed after {attempts} attempts — {last_err}")


def stitch(takes: list[str], dest: str, pad_s: float = 0.35) -> str:
    """Concats multi-take VO with a short pause at the paragraph seam (ffmpeg concat)."""
    concat_file = os.path.join(os.path.dirname(dest), "concat.txt")
    padded = []
    for i, take in enumerate(takes):
        if i == len(takes) - 1:
            padded.append(take)
            continue
        out = os.path.splitext(take)[0] + "_padded.mp3"
        shell.run([settings.ffmpeg, "-y", "-i", take, "-af", f"apad=pad_dur={pad_s}", out],
                  check=True)
        padded.append(out)
    with open(concat_file, "w") as f:
        f.write("\n".join(f"file '{p}'" for p in padded))
    shell.run([settings.ffmpeg, "-y", "-f", "concat", "-safe", "0", "-i", concat_file,
               "-c", "copy", dest], check=True)
    return dest


def extract_audio(video_path: str, out_dir: str) -> str:
    """Demux a video's audio to mp3 for cloning."""
    os.makedirs(out_dir, exist_ok=True)
    stem = os.path.splitext(os.path.basename(video_path))[0]
    audio_path = os.path.join(out_dir, f"{stem}_extracted.mp3")
    res = shell.run([settings.ffmpeg, "-i", video_path, "-vn", "-acodec", "libmp3lame",
                     "-ab", "192k", "-ar", "44100", "-y", audio_path])
    if res.returncode != 0:
        raise ProviderError(f"ffmpeg audio extract failed: {res.stderr[:200]}")
    return audio_path


def clone_voice(name: str, audio_paths: list[str], key: str, description: str = "",
                remove_noise: bool = False) -> str:
    """Instant voice clone from one or more audio files. Returns the voice_id.
    Clone from EVERY shipped segment of a creator's audio, not just the first —
    more reference audio measurably improves the clone."""
    if not audio_paths:
        raise ProviderError("no audio files provided for cloning")
    files_list = [("files", (os.path.basename(p), open(p, "rb"), "audio/mpeg")) for p in audio_paths]
    data = {"name": name}
    if description:
        data["description"] = description
    if remove_noise:
        data["remove_background_noise"] = "true"
    try:
        resp = requests.post(f"{BASE_URL}/voices/add", headers={"xi-api-key": key},
                             data=data, files=files_list, timeout=120)
    except requests.exceptions.Timeout:
        raise ProviderError("voice cloning timed out (120s)")
    finally:
        for _field, value in files_list:
            try:
                value[1].close()
            except Exception:  # noqa: BLE001
                pass
    if resp.status_code != 200:
        raise ProviderError(f"voice cloning failed: HTTP {resp.status_code} — {resp.text[:300]}")
    voice_id = resp.json().get("voice_id")
    if not voice_id:
        raise ProviderError("voice cloning returned no voice_id")
    return voice_id


def list_remote_voices(key: str) -> list[dict]:
    resp = requests.get(f"{BASE_URL}/voices", headers={"xi-api-key": key},
                        params={"show_legacy": "false"}, timeout=30)
    if resp.status_code != 200:
        raise ProviderError(f"failed to fetch voices: HTTP {resp.status_code}")
    return resp.json().get("voices", [])


def subscription(key: str) -> dict:
    """Character quota for provider_balance."""
    resp = requests.get(f"{BASE_URL}/user/subscription", headers={"xi-api-key": key}, timeout=30)
    if resp.status_code != 200:
        raise ProviderError(f"subscription read failed: HTTP {resp.status_code}")
    d = resp.json()
    used, limit = d.get("character_count"), d.get("character_limit")
    return {"character_count": used, "character_limit": limit,
            "characters_remaining": (limit - used) if (used is not None and limit is not None) else None,
            "tier": d.get("tier"), "next_reset_unix": d.get("next_character_count_reset_unix")}
