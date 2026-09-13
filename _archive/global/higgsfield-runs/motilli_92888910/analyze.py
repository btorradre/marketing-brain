#!/usr/bin/env python3
"""
Deep visual analysis of GLP-1 SOS reference video for Higgsfield Marketing
Studio replication pipeline (Motilli adaptation).

Uploads the local mp4 to Gemini, runs ONE comprehensive prompt, and writes
the result to reference_analysis.json next to this script.
"""
import json
import os
import re
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(line_buffering=True)

from google import genai
from google.genai import types

# --- Config ----------------------------------------------------------------
ROOT = Path("/Users/brooksorradre2/Documents/marketing brain")
ENV_PATH = ROOT / ".env"
VIDEO_PATH = ROOT / "gethookd-cache" / "gethookd_92888910.mp4"
OUT_DIR = ROOT / "higgsfield-runs" / "motilli_92888910"
OUT_PATH = OUT_DIR / "reference_analysis.json"
MODEL = "gemini-2.5-flash"


def load_env_key(env_path: Path, key: str) -> str:
    if not env_path.exists():
        raise SystemExit(f"Missing .env at {env_path}")
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        k, _, v = line.partition("=")
        if k.strip() == key:
            return v.strip().strip('"').strip("'")
    raise SystemExit(f"{key} not found in {env_path}")


# --- Prompt -----------------------------------------------------------------
BASE_PROMPT = """You are a senior direct response creative analyst. The video is a Facebook/Meta winning ad for "GLP-1 SOS Supplements" with the angle "Gentle Relief for GLP-1 Constipation". Performance score 91, 21 days active. The ad uses an ElevenLabs-style AI voiceover with visual scenes underneath.

Watch the entire video carefully and return ONE JSON object with this EXACT shape (no missing keys, no extra prose, no markdown fences):

{
  "full_transcript": "every word of the AI voiceover, with timestamps inline like (0:03)",
  "duration_seconds": <float>,
  "aspect_ratio": "9:16 | 1:1 | 16:9",
  "overall_creative_type": "ai_ugc | static_slideshow_with_vo | mixed_broll_with_vo | animated_3d | other",
  "narrative_arc": "one paragraph describing how the ad flows beat-by-beat",
  "scenes": [
    {
      "scene_number": 1,
      "timestamp_start": "0:00",
      "timestamp_end": "0:04",
      "duration_s": 4.0,
      "visual_description": "DETAILED — what's on screen, who/what, framing, lighting, composition, environment. Must be specific enough that an image generator could recreate the scene.",
      "scene_type": "talking_head | product_shot | broll_action | broll_lifestyle | broll_science | text_overlay | before_after | testimonial | infographic | animated_sequence | other",
      "narration_during_scene": "the VO line spoken during this scene (verbatim)",
      "text_on_screen": "any visible text/captions/overlays — verbatim",
      "key_visual_elements": ["list every distinct visible thing — product, person, object, setting, graphic"],
      "motion": "static | slow_pan | zoom_in | zoom_out | fast_cut | smooth_transition | handheld | animated",
      "color_palette": "dominant colors",
      "mood": "emotional tone",
      "has_glp1_sos_product": true,
      "has_competitor_product": false,
      "person_visible": "describe any person — demographics, expression, action — or null",
      "replication_notes": "what would need to swap when adapting for a different brand (Motilli celery juice fiber gummies)"
    }
  ],
  "products_shown": [{"name": "GLP-1 SOS bottle", "appearances": ["timestamps"], "shape": "...", "label_color": "...", "key_visible_text": "..."}],
  "people_shown": [{"description": "55+ woman in kitchen", "appearances": ["timestamps"], "role": "avatar / testimonial / actress"}],
  "text_overlays_used": ["full list of every text overlay shown, with timestamp"],
  "audio_voice_characteristics": "describe the VO voice — gender, age, accent, pace, tone (this is an ElevenLabs AI voiceover)",
  "music_or_sfx": "describe the bed",
  "best_higgsfield_preset_match": "ugc | tutorial | ugc_unboxing | hyper_motion | product_review | tv_spot | wild_card | ugc_virtual_try_on | virtual_try_on",
  "preset_match_reasoning": "why this preset fits"
}

Quality bar:
- Catalogue EVERY distinct visible scene. Do not merge cuts. If the camera cuts to a new shot, that's a new scene.
- visual_description must be detailed enough for downstream image regeneration: subjects, framing, lighting, environment, composition.
- full_transcript must be verbatim with inline timestamps in (m:ss) format.
- For best_higgsfield_preset_match pick exactly ONE from the listed enum.
- Output RAW JSON only. No markdown code fences. No commentary."""

RETRY_SUFFIX = "\n\nIMPORTANT: Respond with raw JSON only. No prose. No markdown fences. No backticks. The first character must be '{' and the last character must be '}'."


def parse_json(text: str) -> dict:
    text = text.strip()
    if text.startswith("```json"):
        text = text.split("```json", 1)[1]
        text = text.rsplit("```", 1)[0]
    elif text.startswith("```"):
        text = text.split("```", 1)[1]
        text = text.rsplit("```", 1)[0]
    text = text.strip()
    return json.loads(text)


def main():
    api_key = load_env_key(ENV_PATH, "GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    if not VIDEO_PATH.exists():
        raise SystemExit(f"Video not found: {VIDEO_PATH}")

    size_mb = VIDEO_PATH.stat().st_size / 1024 / 1024
    print(f"Uploading {VIDEO_PATH.name} ({size_mb:.1f} MB)...")

    uploaded = client.files.upload(file=str(VIDEO_PATH))
    while uploaded.state == "PROCESSING":
        time.sleep(2)
        uploaded = client.files.get(name=uploaded.name)
    if uploaded.state != "ACTIVE":
        raise SystemExit(f"Upload failed: state={uploaded.state}")
    print(f"Uploaded. URI: {uploaded.uri}")

    prompts = [BASE_PROMPT, BASE_PROMPT + RETRY_SUFFIX]
    analysis = None
    last_err = None
    for attempt, prompt in enumerate(prompts, 1):
        print(f"Attempt {attempt}: requesting analysis...")
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=[
                    types.Part.from_uri(file_uri=uploaded.uri, mime_type="video/mp4"),
                    prompt,
                ],
                config=types.GenerateContentConfig(
                    temperature=0.2,
                    max_output_tokens=65000,
                    response_mime_type="application/json",
                ),
            )
            text = response.text or ""
            analysis = parse_json(text)
            break
        except Exception as e:
            last_err = e
            print(f"  Parse/request failed: {e}")
            time.sleep(2)

    if analysis is None:
        raise SystemExit(f"Failed to get JSON after retry: {last_err}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(analysis, indent=2))
    print(f"Wrote: {OUT_PATH}")

    try:
        client.files.delete(name=uploaded.name)
    except Exception:
        pass

    scenes = analysis.get("scenes", [])
    print("\n" + "=" * 60)
    print(f"Total scenes: {len(scenes)}")
    print(f"Recommended Higgsfield preset: {analysis.get('best_higgsfield_preset_match')}")
    arc = analysis.get("narrative_arc", "")
    treatment = analysis.get("overall_creative_type", "")
    print("\nNarrative arc + dominant visual treatment:")
    print(f"- Creative type: {treatment}")
    # Print arc as up to ~5 sentences worth
    sentences = re.split(r"(?<=[.!?])\s+", arc.strip())
    for s in sentences[:5]:
        if s:
            print(f"- {s}")


if __name__ == "__main__":
    main()
