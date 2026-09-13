"""Veo 3 image-to-video via the Gemini API (google-genai SDK).

Generation is image-to-video ONLY: every segment is conditioned on a START
frame (the reference still for segment 1, or the previous segment's final frame
thereafter). Native audio is ALWAYS disabled (generate_audio=False) — speech
comes exclusively from ElevenLabs.

Outputs carry an invisible SynthID watermark; callers record that in the manifest.
"""
import time

import google.genai as genai
from google.genai import types
from google.genai.errors import APIError

from util import RetryableError, log, with_backoff

DEFAULT_MODEL = "veo-3.0-generate-001"
# One fixed negative prompt reused on EVERY call (consistency safeguard).
NEGATIVE_PROMPT = (
    "subtitles, captions, on-screen text, watermark, logo overlay, "
    "extra fingers, deformed hands, face morph, identity change, "
    "wardrobe change, scene cut, cartoon, oversaturated, jump cut"
)


class SafetyFiltered(Exception):
    pass


def _client():
    import os
    return genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def _image_from_path(path) -> types.Image:
    return types.Image.from_file(location=str(path))


def generate_segment(*, prompt: str, start_image_path: str, out_path: str,
                     aspect: str = "9:16", seed: int = 777,
                     model: str = DEFAULT_MODEL, duration_seconds: int = 8,
                     poll_interval: float = 10.0, timeout: float = 600.0) -> dict:
    """Generate one image-to-video segment from a start frame.

    Returns {"path", "seed", "model", "watermark": "SynthID"}.
    Raises SafetyFiltered when the request is blocked or returns empty so the
    caller can rework the prompt or skip.
    """
    client = _client()
    image = _image_from_path(start_image_path)

    config = types.GenerateVideosConfig(
        aspect_ratio=aspect,
        negative_prompt=NEGATIVE_PROMPT,
        number_of_videos=1,
        generate_audio=False,          # Veo native audio OFF — ElevenLabs only.
        person_generation="allow_adult",
        duration_seconds=duration_seconds,
        seed=seed,
    )

    def _start_op():
        try:
            return client.models.generate_videos(
                model=model, prompt=prompt, image=image, config=config
            )
        except APIError as e:
            status = getattr(e, "code", None) or getattr(e, "status_code", None)
            if status in (429, 500, 502, 503, 504):
                raise RetryableError(f"Veo HTTP {status}")
            raise

    op = with_backoff(_start_op, label="veo.start")

    waited = 0.0
    while not op.done:
        if waited >= timeout:
            raise SafetyFiltered("Veo operation timed out")
        time.sleep(poll_interval)
        waited += poll_interval
        op = client.operations.get(op)

    resp = getattr(op, "response", None)
    err = getattr(op, "error", None)
    if err:
        msg = str(err)
        if "safety" in msg.lower() or "blocked" in msg.lower():
            raise SafetyFiltered(msg)
        raise RuntimeError(f"Veo failed: {msg}")
    vids = getattr(resp, "generated_videos", None) if resp else None
    if not vids:
        raise SafetyFiltered("Veo returned no video (likely safety-filtered)")

    video = vids[0].video
    client.files.download(file=video)
    video.save(str(out_path))
    log(f"veo -> {out_path} (seed={seed})")
    return {"path": str(out_path), "seed": seed, "model": model, "watermark": "SynthID"}


def rework_prompt(prompt: str) -> str:
    """Soften a prompt for a safety-filter retry without changing the creative."""
    softer = prompt
    for bad, good in [
        ("close-up", "medium shot"),
        ("skin", "complexion"),
        ("body", "figure"),
    ]:
        softer = softer.replace(bad, good)
    return softer + " Wholesome, friendly, advertising-safe framing."
