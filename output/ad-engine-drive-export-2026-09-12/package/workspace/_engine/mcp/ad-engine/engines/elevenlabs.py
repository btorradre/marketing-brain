"""ElevenLabs wrapper — voiceover generation on eleven_v3 / Creative.

DEFAULTS ARE DELIBERATE AND DIFFERENT FROM THE elevenlabs-agent SKILL.
That skill hardcodes eleven_multilingual_v2, which was blind-judged 2.5/10
against a real on-camera voice (flat pitch contour, even syllable spacing,
no breaths) on 2026-08-05. The v3 Creative rebuild scored 9.5/10. So:

  model_id            eleven_v3
  stability           0.0   (Creative — v3 accepts ONLY 0.0 / 0.5 / 1.0)
  similarity_boost    0.85  (0.95 reads more announcer)
  use_speaker_boost   true

Other laws baked in here:
  - ONE TAKE. A VO is one continuous generation, never per-line mp3s
    stitched together. segment_script-style splitting is intentionally
    absent from this module.
  - v3 hard-caps text at 5,000 chars (400 text_too_long). Over that, split
    at a natural PARAGRAPH boundary into two large takes, same voice and
    settings, and stitch with ~0.35s padding. Two large takes at a paragraph
    pause is the accepted reading of the one-take law.
  - v3 exposes no speed control — pace with ffmpeg atempo AFTER generation.
  - "Velantra" reliably comes back "Volantra". Respell it as Vell-Ahn-Trah
    in TTS input only (keep plain spelling in the human-readable script).
    "Motilli" / "getmotilli.com" need no respelling.

The persistent voice registry from the elevenlabs-agent skill is reused as-is
(~/Documents/marketing brain/voice-registry.json) so cloned voices stay shared
across both paths rather than forking into two registries.
"""

import importlib.util
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import db

VAULT = Path(__file__).resolve().parents[4]
ENV_PATH = VAULT / ".env"
DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "vo"

BASE_URL = "https://api.elevenlabs.io/v1"
MODEL_V3 = "eleven_v3"
MAX_CHARS_V3 = 5000

# v3 Creative preset — see module docstring, do not "tune" these casually
CREATIVE = {"stability": 0.0, "similarity_boost": 0.85, "use_speaker_boost": True}

# TTS-only respellings. Keep plain spellings in human-readable scripts.
PRONUNCIATION_FIXES = {"Velantra": "Vell-Ahn-Trah"}


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Reuse the skill's registry rather than forking a second one
_agent = _load("ad_engine_elevenlabs_agent",
                Path.home() / ".claude" / "skills" / "elevenlabs-agent" / "pipeline.py")


def _api_key() -> str:
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key and ENV_PATH.exists():
        for line in ENV_PATH.read_text().splitlines():
            if line.strip().startswith("ELEVENLABS_API_KEY="):
                key = line.strip().split("=", 1)[1]
                break
    if not key:
        raise RuntimeError(f"ELEVENLABS_API_KEY not found in env or {ENV_PATH}")
    return key


def list_voices() -> dict:
    """Registered clones + defaults from the shared voice registry."""
    reg = _agent.load_registry()
    return {"voices": reg.get("voices", {}), "default_voices": reg.get("default_voices", {})}


def resolve_voice(name_or_id: str) -> str:
    """Registry name -> voice_id. Passes raw voice IDs through untouched."""
    return _agent.get_voice_id(name_or_id)


def apply_pronunciation_fixes(text: str) -> str:
    for plain, respelled in PRONUNCIATION_FIXES.items():
        text = text.replace(plain, respelled)
    return text


def _split_at_paragraph(text: str, limit: int = MAX_CHARS_V3) -> list[str]:
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


def _tts_one_take(text: str, voice_id: str, out_path: Path,
                   with_timestamps: bool = False) -> dict:
    """Single continuous generation. with_timestamps returns character
    alignment (collapse to words downstream for caption sync / slicing) —
    no separate forced-alignment pass needed."""
    endpoint = f"{BASE_URL}/text-to-speech/{voice_id}"
    if with_timestamps:
        endpoint += "/with-timestamps"
    payload = {"text": text, "model_id": MODEL_V3, "voice_settings": CREATIVE}
    headers = {"xi-api-key": _api_key(), "Content-Type": "application/json"}
    if not with_timestamps:
        headers["Accept"] = "audio/mpeg"

    last_err = ""
    for attempt in range(3):
        if attempt:
            time.sleep(5 * attempt)
        resp = requests.post(endpoint, headers=headers, json=payload, timeout=180)
        if resp.status_code == 200:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            if with_timestamps:
                data = resp.json()
                import base64
                out_path.write_bytes(base64.b64decode(data["audio_base64"]))
                return {"path": str(out_path), "alignment": data.get("alignment")}
            out_path.write_bytes(resp.content)
            return {"path": str(out_path), "alignment": None}
        last_err = f"HTTP {resp.status_code}: {resp.text[:300]}"
    raise RuntimeError(f"ElevenLabs TTS failed after 3 attempts — {last_err}")


def _stitch(takes: list[Path], dest: Path, pad_s: float = 0.35) -> Path:
    """Concats multi-take VO with a short pause at the paragraph seam."""
    concat_file = dest.parent / "concat.txt"
    padded = []
    for i, take in enumerate(takes):
        if i == len(takes) - 1:
            padded.append(take)
            continue
        out = take.with_name(f"{take.stem}_padded.mp3")
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(take), "-af", f"apad=pad_dur={pad_s}",
             str(out)], capture_output=True, check=True)
        padded.append(out)
    concat_file.write_text("\n".join(f"file '{p}'" for p in padded))
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_file),
         "-c", "copy", str(dest)], capture_output=True, check=True)
    return dest


def generate_vo(script: str, voice: str, brand: str | None = None,
                 concept: str | None = None, with_timestamps: bool = False,
                 apply_fixes: bool = True) -> dict:
    """Generates ONE continuous voiceover on v3/Creative. Returns the job dict;
    output.asset_id is the mp3. Over 5k chars it splits at a paragraph
    boundary into large takes and stitches them — it never renders per line."""
    voice_id = resolve_voice(voice)
    text = apply_pronunciation_fixes(script) if apply_fixes else script

    job_id = db.create_job("elevenlabs", "tts", model=MODEL_V3, brand=brand,
                            concept=concept,
                            input_data={"voice": voice, "voice_id": voice_id,
                                        "chars": len(text)})
    work_dir = DATA_DIR / job_id
    try:
        takes_text = _split_at_paragraph(text)
        alignment = None
        if len(takes_text) == 1:
            final = work_dir / "voiceover.mp3"
            result = _tts_one_take(takes_text[0], voice_id, final, with_timestamps)
            alignment = result["alignment"]
        else:
            paths = []
            for i, chunk in enumerate(takes_text):
                p = work_dir / f"take_{i + 1:02d}.mp3"
                _tts_one_take(chunk, voice_id, p, with_timestamps=False)
                paths.append(p)
            final = _stitch(paths, work_dir / "voiceover.mp3")

        asset_id = db.create_asset(job_id, "audio", path=str(final), brand=brand,
                                    concept=concept,
                                    meta={"voice_id": voice_id, "model": MODEL_V3,
                                          "n_takes": len(takes_text),
                                          "settings": CREATIVE})
        if alignment is not None:
            (work_dir / "alignment.json").write_text(json.dumps(alignment))

        db.update_job(job_id, status="success", output_data={
            "asset_id": asset_id, "path": str(final), "n_takes": len(takes_text),
            "alignment_path": str(work_dir / "alignment.json") if alignment else None,
        })
    except Exception as exc:  # noqa: BLE001 — surfaced via job.error
        db.update_job(job_id, status="fail", error=str(exc))
    return db.get_job(job_id)


def clone_voice(reference_files: list[str], name: str, description: str = "",
                 brand: str = "", tags: list[str] | None = None) -> dict:
    """Clones a voice from reference audio/video and registers it in the shared
    registry. Clone from EVERY shipped segment, not just the first — two takes
    (~14s) beat one (~8s)."""
    job_id = db.create_job("elevenlabs", "clone", brand=brand,
                            input_data={"name": name, "files": reference_files})
    try:
        voice_id = _agent.clone_voice(reference_files, name, description=description,
                                       brand=brand, tags=tags)
        db.update_job(job_id, status="success",
                       output_data={"voice_id": voice_id, "name": name})
    except Exception as exc:  # noqa: BLE001
        db.update_job(job_id, status="fail", error=str(exc))
    return db.get_job(job_id)
