#!/usr/bin/env python3
"""
Fashion Replicator Pipeline
============================
Takes a reference video (POV, lifestyle, product demo), replicates every scene 1:1
for a fashion brand using image-to-image, extracts music, clones voiceover, rewrites
script, and stitches everything together with FFmpeg.

Inspired by Alex Djordjevic's workflow:
1. Scene detection + keyframe extraction
2. Movement JSON extraction via Gemini
3. Text removal from keyframes (clean backgrounds)
4. Image-to-image product swap (Nano Banana 2)
5. Upscale winners 2x
6. Kling 3.0 animation with movement JSON
7. Audio extraction (music + voice separation)
8. Voice transcription + script rewriting
9. ElevenLabs voice cloning + TTS
10. FFmpeg final stitch (scenes + music + voiceover)

Usage:
    python3 fashion_replicator.py \
        --video "/path/to/reference.mp4" \
        --brand "Solorna" \
        --product-context "Premium comfort sandals for women" \
        --style "warm Mediterranean aesthetic, golden hour lighting" \
        --product-images "/path/to/product1.png,/path/to/product2.png" \
        --output-dir "./output" \
        --concept-code "SD-POV-01" \
        [--skip-voiceover]  # Skip voice cloning/TTS if reference has no VO
        [--skip-upload]     # Skip Google Drive upload
        [--voice-name "Reference Voice"]  # Name for cloned voice in ElevenLabs
"""

import argparse
import base64
import json
import os
import re
import subprocess
import sys
import time
import tempfile
from pathlib import Path
from datetime import datetime

# ---------------------------------------------------------------------------
# Dependency check
# ---------------------------------------------------------------------------
REQUIRED_PACKAGES = ["google.genai", "PIL", "requests"]

def check_deps():
    missing = []
    for pkg in REQUIRED_PACKAGES:
        try:
            __import__(pkg.split(".")[0] if "." not in pkg else pkg.replace(".", "/").split("/")[0])
        except ImportError:
            missing.append(pkg)
    try:
        from google import genai
    except ImportError:
        if "google.genai" not in missing:
            missing.append("google-genai")
    if missing:
        print(f"[!] Missing packages: {missing}")
        print("    pip install google-genai Pillow requests elevenlabs")
        sys.exit(1)

check_deps()

import requests
from google import genai
from google.genai import types
from PIL import Image

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "[REDACTED_SECRET]")
KIE_API_KEY = os.environ.get("KIE_API_KEY", "ea55b909fc9fefcb6b964e468062f2c2")
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "[REDACTED_SECRET]")

GEMINI_VIDEO_MODEL = "gemini-3-flash-preview"
GEMINI_IMAGE_MODEL = "gemini-3.1-flash-image-preview"

KIE_CREATE_URL = "https://api.kie.ai/api/v1/jobs/createTask"
KIE_STATUS_URL = "https://api.kie.ai/api/v1/jobs/recordInfo"

ELEVENLABS_BASE = "https://api.elevenlabs.io/v1"

SCENE_THRESHOLD = 0.3
MAX_KLING_RETRIES = 3
KLING_POLL_INTERVAL = 15

VAULT_ROOT = os.path.expanduser("~/Documents/marketing brain")

# Google Drive OAuth2 (shared with video-scene-replicator)
GDRIVE_CLIENT_ID = "630165550470-bk00miojfehkb5va5hdoupbn170lurhh.apps.googleusercontent.com"
GDRIVE_CLIENT_SECRET = "[REDACTED_SECRET]"
GDRIVE_TOKEN_PATH = os.path.expanduser("~/.claude/skills/video-scene-replicator/gdrive_token.json")

# Brand knowledge registry — fashion brands
BRAND_REGISTRY = {
    "solorna": {
        "research_docs": [
            os.path.join(VAULT_ROOT, "solorna/solorna_brand_document.txt"),
        ],
        "product_images_dir": os.path.join(VAULT_ROOT, "solorna/product images "),
        "product_images": [],
        "default_product_context": "Premium comfort sandals bridging luxury craftsmanship and everyday wearability — Mediterranean-inspired, cushioned footbeds, refined silhouettes",
    },
    "velantra": {
        "research_docs": [],
        "product_images_dir": "",
        "product_images": [],
        "default_product_context": "Premium fashion accessories — bags and leather goods with timeless design",
    },
    "velantra-boat-tote": {
        "research_docs": [],
        "product_images_dir": os.path.join(VAULT_ROOT, "statics/product references/velantra/boat tote"),
        "product_images": [
            os.path.join(VAULT_ROOT, "statics/product references/velantra/boat tote/navy blue .webp"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/boat tote/01.jpg"),
        ],
        "default_product_context": "Velantra Boat Tote in Navy Blue — Birkin-inspired structured rectangular tote with cream/off-white canvas body, dark navy leather trim (straps, handles, front belt strap, base), gold turn-lock clasp on front strap, gold feet on base, two short top handles in navy leather. Canvas + leather two-tone construction.",
    },
    # Supplement brands (inherited from video-scene-replicator)
    "motilli": {
        "research_docs": [
            os.path.join(VAULT_ROOT, "brands/motilli/copy/briefs/Motilli_Master_Copywriting_Brief.md"),
            os.path.join(VAULT_ROOT, "brands/motilli/copy/strategy/Motilli_Product_Context.md"),
            os.path.join(VAULT_ROOT, "brands/motilli/copy/strategy/Motilli_Avatar_VoC.md"),
        ],
        "product_images": [
            os.path.join(VAULT_ROOT, "brands/motilli/brand/website-assets/motilli product reference.png"),
        ],
        "default_product_context": "Celery juice fiber gummies for GLP-1 users",
    },
    "lunessa": {
        "research_docs": [
            os.path.join(VAULT_ROOT, "brands/lunessa/research/fh research docs/Lunessa Research Docs 3.0/Lunessa Avatar Sheet.pdf"),
            os.path.join(VAULT_ROOT, "brands/lunessa/research/fh research docs/Lunessa Research Docs 3.0/Lunessa_Master_Copywriting_Brief.docx"),
        ],
        "product_images": [
            os.path.join(VAULT_ROOT, "brands/lunessa/brand/website assets/lunessa spelling corrected .jpg"),
        ],
        "default_product_context": "Heart health supplement for women",
    },
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def log(stage, msg):
    print(f"[Stage {stage}] {msg}")


def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)
    return path


def load_progress(output_dir):
    progress_file = os.path.join(output_dir, ".progress.json")
    if os.path.exists(progress_file):
        with open(progress_file) as f:
            return json.load(f)
    return {"completed_stages": {}, "scene_status": {}}


def save_progress(output_dir, progress):
    progress_file = os.path.join(output_dir, ".progress.json")
    with open(progress_file, "w") as f:
        json.dump(progress, f, indent=2)


def load_brand_knowledge(brand_name):
    """Load research docs from the vault for the specified brand."""
    key = brand_name.lower().strip()
    registry = BRAND_REGISTRY.get(key)

    if not registry:
        print(f"[Brand] No registry entry for '{brand_name}' — using manual context only")
        return {"context_text": "", "product_images": [], "default_product_context": ""}

    print(f"[Brand] Loading knowledge for: {brand_name}")

    context_parts = []
    for doc_path in registry.get("research_docs", []):
        if not os.path.exists(doc_path):
            print(f"[Brand]   SKIP (not found): {os.path.basename(doc_path)}")
            continue

        ext = Path(doc_path).suffix.lower()
        try:
            if ext in (".md", ".txt"):
                with open(doc_path, "r", encoding="utf-8") as f:
                    text = f.read()
                context_parts.append(f"--- {os.path.basename(doc_path)} ---\n{text}")
                print(f"[Brand]   Loaded: {os.path.basename(doc_path)} ({len(text)} chars)")
            elif ext == ".docx":
                import zipfile
                import xml.etree.ElementTree as ET
                with zipfile.ZipFile(doc_path, "r") as z:
                    with z.open("word/document.xml") as xml_file:
                        tree = ET.parse(xml_file)
                        ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
                        paragraphs = tree.findall(".//w:p", ns)
                        text = "\n".join(
                            "".join(node.text or "" for node in p.findall(".//w:t", ns))
                            for p in paragraphs
                        )
                context_parts.append(f"--- {os.path.basename(doc_path)} ---\n{text}")
                print(f"[Brand]   Loaded: {os.path.basename(doc_path)} ({len(text)} chars)")
            elif ext == ".pdf":
                try:
                    from pdfminer.high_level import extract_text
                    text = extract_text(doc_path)
                    context_parts.append(f"--- {os.path.basename(doc_path)} ---\n{text}")
                    print(f"[Brand]   Loaded: {os.path.basename(doc_path)} ({len(text)} chars)")
                except ImportError:
                    print(f"[Brand]   SKIP (pdfminer not installed): {os.path.basename(doc_path)}")
        except Exception as e:
            print(f"[Brand]   ERROR reading {os.path.basename(doc_path)}: {e}")

    full_context = "\n\n".join(context_parts)
    if len(full_context) > 30000:
        full_context = full_context[:30000] + "\n\n[... truncated ...]"

    # Collect product images
    valid_images = []
    img_dir = registry.get("product_images_dir", "")
    if img_dir and os.path.isdir(img_dir):
        img_exts = {".png", ".jpg", ".jpeg", ".webp"}
        for fname in sorted(os.listdir(img_dir)):
            if Path(fname).suffix.lower() in img_exts:
                valid_images.append(os.path.join(img_dir, fname))
        print(f"[Brand]   Product images from dir: {len(valid_images)} found")
    if not valid_images:
        valid_images = [p for p in registry.get("product_images", []) if os.path.exists(p)]

    return {
        "context_text": full_context,
        "product_images": valid_images,
        "default_product_context": registry.get("default_product_context", ""),
    }


# ===========================================================================
# STAGE 0: Audio Extraction + Music/Voice Separation
# ===========================================================================

def extract_audio(video_path, output_dir):
    """Extract full audio track from reference video, then separate voice and music."""
    audio_dir = ensure_dir(os.path.join(output_dir, "audio"))

    full_audio_path = os.path.join(audio_dir, "full_audio.wav")
    music_path = os.path.join(audio_dir, "music.wav")
    vocals_path = os.path.join(audio_dir, "vocals.wav")

    # Extract full audio
    log(0, "Extracting audio from reference video...")
    subprocess.run([
        "ffmpeg", "-y", "-i", video_path,
        "-vn", "-acodec", "pcm_s16le", "-ar", "44100", "-ac", "2",
        full_audio_path
    ], capture_output=True)

    if not os.path.exists(full_audio_path):
        log(0, "WARNING: No audio track found in reference video")
        return {"full_audio": None, "music": None, "vocals": None, "has_voiceover": False}

    file_size = os.path.getsize(full_audio_path)
    log(0, f"Full audio extracted: {full_audio_path} ({file_size / 1024:.0f} KB)")

    # Attempt voice/music separation using ffmpeg's built-in filters
    # Method: Use a center-channel extraction approach
    # Vocals tend to be centered in stereo; music tends to be spread
    log(0, "Separating vocals from music (center-channel extraction)...")

    # Extract vocals (center channel — where voice usually sits)
    subprocess.run([
        "ffmpeg", "-y", "-i", full_audio_path,
        "-af", "pan=stereo|c0=c0-c1|c1=c1-c0",
        music_path
    ], capture_output=True)

    # Extract music (remove center = remove vocals)
    # This is a simple approach; for better results, use demucs
    subprocess.run([
        "ffmpeg", "-y", "-i", full_audio_path,
        "-af", "pan=mono|c0=0.5*c0+0.5*c1",
        vocals_path
    ], capture_output=True)

    # Detect if there's actual voice content using audio levels
    has_voiceover = detect_voiceover(full_audio_path)
    log(0, f"Voiceover detected: {has_voiceover}")

    # Try demucs if available for better separation
    try:
        demucs_result = subprocess.run(["demucs", "--version"], capture_output=True, text=True)
        if demucs_result.returncode == 0:
            log(0, "Demucs available — running AI-powered separation...")
            demucs_out = os.path.join(audio_dir, "demucs_out")
            subprocess.run([
                "demucs", "-n", "htdemucs",
                "--two-stems", "vocals",
                "-o", demucs_out,
                full_audio_path
            ], capture_output=True, timeout=300)

            # Find demucs output
            stem_name = Path(full_audio_path).stem
            demucs_vocals = os.path.join(demucs_out, "htdemucs", stem_name, "vocals.wav")
            demucs_music = os.path.join(demucs_out, "htdemucs", stem_name, "no_vocals.wav")

            if os.path.exists(demucs_vocals):
                subprocess.run(["cp", demucs_vocals, vocals_path], capture_output=True)
                log(0, "Demucs vocals extracted successfully")
            if os.path.exists(demucs_music):
                subprocess.run(["cp", demucs_music, music_path], capture_output=True)
                log(0, "Demucs music extracted successfully")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        log(0, "Demucs not available — using FFmpeg center-channel extraction (install demucs for better quality)")

    return {
        "full_audio": full_audio_path if os.path.exists(full_audio_path) else None,
        "music": music_path if os.path.exists(music_path) else None,
        "vocals": vocals_path if os.path.exists(vocals_path) else None,
        "has_voiceover": has_voiceover,
    }


def detect_voiceover(audio_path):
    """Detect if audio contains speech using volume analysis.
    Speech has consistent mid-range volume; music-only has more dynamic range."""
    try:
        result = subprocess.run([
            "ffprobe", "-v", "quiet", "-print_format", "json",
            "-show_format", audio_path
        ], capture_output=True, text=True)
        data = json.loads(result.stdout)
        duration = float(data.get("format", {}).get("duration", 0))

        # Check audio volume statistics
        vol_result = subprocess.run([
            "ffmpeg", "-i", audio_path,
            "-af", "volumedetect",
            "-f", "null", "-"
        ], capture_output=True, text=True)

        stderr = vol_result.stderr
        # Parse mean volume
        mean_match = re.search(r"mean_volume:\s*([-\d.]+)\s*dB", stderr)
        max_match = re.search(r"max_volume:\s*([-\d.]+)\s*dB", stderr)

        if mean_match:
            mean_vol = float(mean_match.group(1))
            # Speech typically has mean volume above -30dB
            # Pure music with no voice tends to be louder but more variable
            if mean_vol > -40:
                return True

        return duration > 3  # Assume voiceover if audio exists and is > 3s
    except Exception:
        return False


# ===========================================================================
# STAGE 1: Scene Detection & Keyframe Extraction
# ===========================================================================

def extract_scenes(video_path, output_dir, threshold=SCENE_THRESHOLD):
    """Use ffmpeg to detect scene changes and extract keyframes + short clips."""
    scenes_dir = ensure_dir(os.path.join(output_dir, "scenes"))

    log(1, f"Detecting scenes in {video_path} (threshold={threshold})")

    # Get video duration and properties
    probe = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", video_path],
        capture_output=True, text=True
    )
    probe_data = json.loads(probe.stdout)
    duration = float(probe_data["format"]["duration"])
    log(1, f"Video duration: {duration:.1f}s")

    # Detect scene changes
    scene_cmd = [
        "ffmpeg", "-i", video_path,
        "-filter:v", f"select='gt(scene,{threshold})',showinfo",
        "-vsync", "vfr",
        "-f", "null", "-"
    ]
    result = subprocess.run(scene_cmd, capture_output=True, text=True)

    timestamps = [0.0]
    for line in result.stderr.split("\n"):
        if "pts_time:" in line:
            match = re.search(r"pts_time:(\d+\.?\d*)", line)
            if match:
                ts = float(match.group(1))
                if ts - timestamps[-1] > 0.5:
                    timestamps.append(ts)

    if len(timestamps) <= 1:
        log(1, "No scene changes detected — sampling every 2 seconds")
        timestamps = [i * 2.0 for i in range(int(duration / 2) + 1)]

    log(1, f"Found {len(timestamps)} scenes at: {[f'{t:.1f}s' for t in timestamps]}")

    scenes = []
    for i, ts in enumerate(timestamps):
        scene_num = f"{i+1:03d}"
        keyframe_path = os.path.join(scenes_dir, f"scene_{scene_num}.png")
        clip_path = os.path.join(scenes_dir, f"scene_{scene_num}_clip.mp4")

        # Extract keyframe
        subprocess.run([
            "ffmpeg", "-y", "-ss", str(ts), "-i", video_path,
            "-frames:v", "1", "-q:v", "1", keyframe_path
        ], capture_output=True)

        # Extract clip for motion analysis
        next_ts = timestamps[i + 1] if i + 1 < len(timestamps) else min(ts + 2.0, duration)
        clip_duration = min(next_ts - ts, 5.0)
        if clip_duration < 0.3:
            clip_duration = 1.0

        subprocess.run([
            "ffmpeg", "-y", "-ss", str(ts), "-i", video_path,
            "-t", str(clip_duration), "-c:v", "libx264", "-preset", "fast",
            "-an", clip_path
        ], capture_output=True)

        scenes.append({
            "scene_number": i + 1,
            "timestamp": ts,
            "duration": clip_duration,
            "keyframe": keyframe_path,
            "clip": clip_path
        })

    log(1, f"Extracted {len(scenes)} scene keyframes and clips")
    return scenes, duration


# ===========================================================================
# STAGE 2: Scene Analysis + Movement JSON Extraction via Gemini
# ===========================================================================

def analyze_scenes_with_movement(scenes, video_path, output_dir):
    """Analyze each scene AND extract detailed movement JSON (Alex's 'real unlock').
    Feeds the full video to Gemini for global movement extraction, then per-scene analysis."""
    analysis_dir = ensure_dir(os.path.join(output_dir, "analysis"))
    client = genai.Client(api_key=GEMINI_API_KEY)

    # STEP 2a: Extract global movement JSON from full video
    log(2, "Extracting movement JSON from full video via Gemini...")
    movement_json = extract_movement_json(video_path, client)

    movement_path = os.path.join(analysis_dir, "movement_data.json")
    with open(movement_path, "w") as f:
        json.dump(movement_json, f, indent=2)
    log(2, f"Movement data saved to {movement_path}")

    # STEP 2b: Per-scene analysis
    analyses = []
    for scene in scenes:
        log(2, f"Analyzing scene {scene['scene_number']}/{len(scenes)}...")

        img_bytes = open(scene["keyframe"], "rb").read()
        clip_bytes = open(scene["clip"], "rb").read()

        prompt = """Analyze this video scene for a fashion brand creative replication pipeline. Return a JSON object:
{
  "scene_number": <int>,
  "description": "<detailed description of what's happening>",
  "composition": "<camera angle, framing, depth of field, layout>",
  "style": "<visual style - lighting, color palette, texture, aesthetic>",
  "motion": "<ALL motion: camera movement (zoom, pan, tilt, shake, static), subject movement, transitions>",
  "motion_json": {
    "camera": "<pan_left, pan_right, zoom_in, zoom_out, tilt_up, tilt_down, static, shake, orbit, dolly>",
    "camera_speed": "<slow, medium, fast>",
    "subject_motion": "<describe subject movement in detail>",
    "background_motion": "<any background movement>",
    "vibration": "<none, subtle, moderate, strong>"
  },
  "duration_estimate": "<seconds>",
  "text_overlays": "<any text visible, or 'None'>",
  "key_elements": ["<list of key visual elements>"],
  "mood": "<emotional tone>",
  "background": "<background/environment description>",
  "scene_type": "<one of: pov_shot, product_closeup, lifestyle, outfit_reveal, unboxing, walking, hands_detail, flat_lay, mirror_shot, street_style, text_screen, transition, other>",
  "product_visible": <true/false>,
  "product_description": "<if product visible, describe it: type, color, position, how it's being used/worn/held>"
}

Be EXTREMELY precise about motion — this will be used to recreate the exact camera behavior with AI video generation.
Return ONLY the JSON, no markdown fences."""

        try:
            response = client.models.generate_content(
                model=GEMINI_VIDEO_MODEL,
                contents=types.Content(
                    parts=[
                        types.Part(inline_data=types.Blob(data=img_bytes, mime_type="image/png")),
                        types.Part(
                            inline_data=types.Blob(data=clip_bytes, mime_type="video/mp4"),
                            video_metadata=types.VideoMetadata(fps=5)
                        ),
                        types.Part(text=prompt)
                    ]
                )
            )

            text = response.text.strip()
            if text.startswith("```"):
                text = re.sub(r"^```(?:json)?\n?", "", text)
                text = re.sub(r"\n?```$", "", text)

            analysis = json.loads(text)
            analysis["scene_number"] = scene["scene_number"]
            analysis["timestamp"] = scene["timestamp"]
            analysis["duration"] = scene["duration"]

            # Merge global movement data for this scene's timestamp
            scene_movement = get_movement_for_timestamp(movement_json, scene["timestamp"])
            if scene_movement:
                analysis["global_motion"] = scene_movement

        except Exception as e:
            log(2, f"  WARNING: Failed to analyze scene {scene['scene_number']}: {e}")
            analysis = {
                "scene_number": scene["scene_number"],
                "timestamp": scene["timestamp"],
                "duration": scene["duration"],
                "description": "Analysis failed",
                "composition": "", "style": "", "motion": "static",
                "motion_json": {"camera": "static", "camera_speed": "medium",
                                "subject_motion": "", "background_motion": "", "vibration": "none"},
                "text_overlays": "None", "key_elements": [], "mood": "",
                "background": "", "error": str(e)
            }

        analyses.append(analysis)
        time.sleep(1)

    analysis_path = os.path.join(analysis_dir, "scene_analysis.json")
    with open(analysis_path, "w") as f:
        json.dump(analyses, f, indent=2)

    log(2, f"Analysis complete — saved to {analysis_path}")
    return analyses, movement_json


def extract_movement_json(video_path, client):
    """Feed the full video to Gemini and extract detailed movement JSON per scene."""
    try:
        video_bytes = open(video_path, "rb").read()
        # Cap at 20MB for Gemini
        if len(video_bytes) > 20 * 1024 * 1024:
            log(2, "Video too large for direct upload — using first 20s clip")
            clip_path = video_path + "_movement_clip.mp4"
            subprocess.run([
                "ffmpeg", "-y", "-i", video_path,
                "-t", "20", "-c:v", "libx264", "-preset", "fast",
                "-crf", "28", clip_path
            ], capture_output=True)
            video_bytes = open(clip_path, "rb").read()

        response = client.models.generate_content(
            model=GEMINI_VIDEO_MODEL,
            contents=types.Content(
                parts=[
                    types.Part(
                        inline_data=types.Blob(data=video_bytes, mime_type="video/mp4"),
                        video_metadata=types.VideoMetadata(fps=10)
                    ),
                    types.Part(text="""Extract the movement from this video into detailed JSON.
For each distinct shot/scene, provide:
{
  "scenes": [
    {
      "timestamp_start": <seconds>,
      "timestamp_end": <seconds>,
      "camera_movement": "<pan_left, pan_right, zoom_in, zoom_out, tilt_up, tilt_down, static, shake, orbit, dolly_in, dolly_out, handheld, tracking>",
      "camera_speed": "<slow, medium, fast>",
      "vibration": "<none, subtle, moderate, strong — if there's any camera shake or vibration>",
      "subject_motion": "<detailed description of how subjects move within the frame>",
      "easing": "<linear, ease_in, ease_out, ease_in_out>",
      "motion_intensity": <1-10 scale>,
      "transition_to_next": "<cut, fade, dissolve, swipe, zoom_transition, none>"
    }
  ]
}

Be extremely precise — this data will be used to recreate the exact same motion patterns with AI video generation tools.
Return ONLY the JSON, no markdown fences.""")
                ]
            )
        )

        text = response.text.strip()
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\n?", "", text)
            text = re.sub(r"\n?```$", "", text)

        return json.loads(text)

    except Exception as e:
        log(2, f"Movement extraction failed: {e}")
        return {"scenes": []}


def get_movement_for_timestamp(movement_json, timestamp):
    """Find the movement data for a given timestamp."""
    for scene in movement_json.get("scenes", []):
        start = scene.get("timestamp_start", 0)
        end = scene.get("timestamp_end", 999)
        if start <= timestamp <= end:
            return scene
    return None


# ===========================================================================
# STAGE 3: Voiceover Transcription + Script Rewriting
# ===========================================================================

def transcribe_and_rewrite_script(audio_data, brand, product_context, output_dir, brand_knowledge=""):
    """Transcribe the reference voiceover, then rewrite the script 1:1 for the target brand."""
    script_dir = ensure_dir(os.path.join(output_dir, "script"))

    if not audio_data.get("has_voiceover") or not audio_data.get("vocals"):
        log(3, "No voiceover detected — skipping transcription")
        return {"original_script": None, "adapted_script": None, "has_voiceover": False}

    vocals_path = audio_data["vocals"]
    client = genai.Client(api_key=GEMINI_API_KEY)

    # Step 3a: Transcribe the voiceover using Gemini
    log(3, "Transcribing voiceover via Gemini...")

    try:
        audio_bytes = open(vocals_path, "rb").read()
        # Cap audio for Gemini
        if len(audio_bytes) > 10 * 1024 * 1024:
            # Convert to smaller format
            compressed = vocals_path + ".compressed.mp3"
            subprocess.run([
                "ffmpeg", "-y", "-i", vocals_path,
                "-acodec", "libmp3lame", "-b:a", "64k", compressed
            ], capture_output=True)
            audio_bytes = open(compressed, "rb").read()
            mime = "audio/mpeg"
        else:
            mime = "audio/wav"

        response = client.models.generate_content(
            model=GEMINI_VIDEO_MODEL,
            contents=types.Content(
                parts=[
                    types.Part(inline_data=types.Blob(data=audio_bytes, mime_type=mime)),
                    types.Part(text="""Transcribe this audio exactly as spoken. Include timing markers.
Return JSON:
{
  "full_transcript": "<complete transcript>",
  "segments": [
    {
      "timestamp": "<approximate seconds>",
      "text": "<what was said>",
      "tone": "<conversational, excited, serious, etc.>"
    }
  ]
}
Return ONLY JSON, no markdown.""")
                ]
            )
        )

        text = response.text.strip()
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\n?", "", text)
            text = re.sub(r"\n?```$", "", text)

        transcript = json.loads(text)

    except Exception as e:
        log(3, f"Transcription failed: {e}")
        transcript = {"full_transcript": "", "segments": []}

    # Save original transcript
    transcript_path = os.path.join(script_dir, "original_transcript.json")
    with open(transcript_path, "w") as f:
        json.dump(transcript, f, indent=2)
    log(3, f"Original transcript saved: {transcript_path}")

    if not transcript.get("full_transcript"):
        log(3, "Empty transcript — no rewrite needed")
        return {"original_script": transcript, "adapted_script": None, "has_voiceover": False}

    # Step 3b: Rewrite the script 1:1 for the target brand
    log(3, f"Rewriting script for {brand}...")

    knowledge_block = ""
    if brand_knowledge:
        knowledge_block = f"\n\nBRAND KNOWLEDGE:\n{brand_knowledge[:10000]}"

    rewrite_prompt = f"""You are a direct response copywriter. Rewrite this voiceover script 1:1 for a different brand.

ORIGINAL SCRIPT:
{transcript['full_transcript']}

TARGET BRAND: {brand}
PRODUCT CONTEXT: {product_context}
{knowledge_block}

RULES:
1. Keep the EXACT same structure, pacing, and emotional arc
2. Replace brand/product references with the target brand
3. Keep the same tone and speaking style (conversational, excited, etc.)
4. If the original mentions a specific problem, adapt it for the target brand's problem
5. Keep the same approximate word count per segment
6. Maintain the same hooks, transitions, and call-to-action structure
7. The rewrite should sound natural when spoken — not robotic or overly polished

Return JSON:
{{
  "full_script": "<complete rewritten script>",
  "segments": [
    {{
      "timestamp": "<matching original timing>",
      "text": "<rewritten segment>",
      "tone": "<matching original tone>"
    }}
  ]
}}
Return ONLY JSON, no markdown."""

    try:
        response = client.models.generate_content(
            model=GEMINI_VIDEO_MODEL,
            contents=rewrite_prompt
        )

        text = response.text.strip()
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\n?", "", text)
            text = re.sub(r"\n?```$", "", text)

        adapted_script = json.loads(text)

    except Exception as e:
        log(3, f"Script rewrite failed: {e}")
        adapted_script = {"full_script": transcript["full_transcript"], "segments": transcript.get("segments", [])}

    adapted_path = os.path.join(script_dir, "adapted_script.json")
    with open(adapted_path, "w") as f:
        json.dump(adapted_script, f, indent=2)
    log(3, f"Adapted script saved: {adapted_path}")

    return {
        "original_script": transcript,
        "adapted_script": adapted_script,
        "has_voiceover": True,
    }


# ===========================================================================
# STAGE 4: Brand-Adapted Image Prompts (with text removal)
# ===========================================================================

def generate_brand_prompts(analyses, brand, product_context, style_notes, output_dir, brand_knowledge=""):
    """Generate image prompts — includes text removal instruction (Alex's workflow)."""
    prompts_dir = ensure_dir(os.path.join(output_dir, "prompts"))
    client = genai.Client(api_key=GEMINI_API_KEY)

    brand_prompts = []

    knowledge_block = ""
    if brand_knowledge:
        knowledge_block = f"\n\nBRAND KNOWLEDGE:\n{brand_knowledge}"

    for analysis in analyses:
        log(4, f"Generating prompt for scene {analysis['scene_number']}/{len(analyses)}...")

        # Include motion JSON in the prompt for downstream use
        motion_json = analysis.get("motion_json", {})
        global_motion = analysis.get("global_motion", {})

        prompt = f"""You are a creative director adapting a fashion brand reference video scene.

REFERENCE SCENE:
{json.dumps(analysis, indent=2)}

TARGET BRAND: {brand}
PRODUCT: {product_context}
STYLE: {style_notes}
{knowledge_block}

Generate an image editing prompt that:
1. PRESERVES exact composition, camera angle, lighting, framing
2. REMOVES ALL text overlays — the image must be completely text-free
3. REPLACES any visible product with the target brand's product (if product_visible is true)
4. MAINTAINS the overall mood, color palette, and aesthetic
5. For fashion: adapt the clothing/accessories to match the target brand
6. Include SPECIFIC details: lighting direction, color values, material textures, background

IMPORTANT: Generate text-free images FIRST — text overlays are added in post-production.
This produces measurably better image generation quality.

Return ONLY the image editing prompt as a single paragraph. No explanations."""

        try:
            response = client.models.generate_content(
                model=GEMINI_VIDEO_MODEL,
                contents=prompt
            )
            image_prompt = response.text.strip()
        except Exception as e:
            log(4, f"  WARNING: Prompt generation failed for scene {analysis['scene_number']}: {e}")
            image_prompt = f"Scene {analysis['scene_number']}: {analysis.get('description', 'unknown')} — adapted for {brand}"

        brand_prompts.append({
            "scene_number": analysis["scene_number"],
            "timestamp": analysis["timestamp"],
            "duration": analysis["duration"],
            "image_prompt": image_prompt,
            "motion_description": analysis.get("motion", "static"),
            "motion_json": motion_json,
            "global_motion": global_motion,
            "reference_analysis": analysis,
        })

        time.sleep(1)

    prompts_path = os.path.join(prompts_dir, "image_prompts.json")
    with open(prompts_path, "w") as f:
        json.dump(brand_prompts, f, indent=2)

    log(4, f"Brand prompts generated — saved to {prompts_path}")
    return brand_prompts


# ===========================================================================
# STAGE 5: Image-to-Image Generation (Nano Banana 2) + Text Removal
# ===========================================================================

def generate_images(brand_prompts, scenes, product_images, output_dir):
    """Two-pass image generation:
    Pass 1: Remove text from reference keyframe
    Pass 2: Product swap on the text-free image"""
    gen_dir = ensure_dir(os.path.join(output_dir, "generated"))
    textfree_dir = ensure_dir(os.path.join(output_dir, "generated_textfree"))
    client = genai.Client(api_key=GEMINI_API_KEY)

    keyframe_map = {s["scene_number"]: s["keyframe"] for s in scenes}

    # Pre-load product reference images
    product_parts = []
    for pimg in (product_images or []):
        if os.path.exists(pimg):
            ext = Path(pimg).suffix.lower()
            mime = "image/jpeg" if ext in (".jpg", ".jpeg") else f"image/{ext.lstrip('.')}"
            with open(pimg, "rb") as f:
                product_parts.append(
                    types.Part(inline_data=types.Blob(data=f.read(), mime_type=mime))
                )
            log(5, f"Loaded product reference: {os.path.basename(pimg)}")

    generated = []

    for bp in brand_prompts:
        scene_num = f"{bp['scene_number']:03d}"
        textfree_path = os.path.join(textfree_dir, f"scene_{scene_num}_textfree.png")
        final_path = os.path.join(gen_dir, f"scene_{scene_num}_brand.png")

        # Skip if already generated
        if os.path.exists(final_path):
            log(5, f"Scene {bp['scene_number']} already generated — skipping")
            generated.append({"scene_number": bp["scene_number"], "image_path": final_path})
            continue

        ref_keyframe = keyframe_map.get(bp["scene_number"])

        if not ref_keyframe or not os.path.exists(ref_keyframe):
            log(5, f"  No keyframe for scene {bp['scene_number']} — skipping")
            generated.append({"scene_number": bp["scene_number"], "image_path": None})
            continue

        ref_bytes = open(ref_keyframe, "rb").read()

        # --- PASS 1: Text Removal ---
        log(5, f"Scene {bp['scene_number']} — Pass 1: Removing text...")
        try:
            text_removal_prompt = (
                "Remove ALL text, captions, subtitles, watermarks, and text overlays from this image. "
                "Fill in the areas where text was with a natural continuation of the background. "
                "Keep everything else EXACTLY the same — composition, lighting, colors, subjects, products. "
                "The output must look like the text was never there."
            )

            response = client.models.generate_content(
                model=GEMINI_IMAGE_MODEL,
                contents=types.Content(parts=[
                    types.Part(inline_data=types.Blob(data=ref_bytes, mime_type="image/png")),
                    types.Part(text=text_removal_prompt),
                ]),
                config=types.GenerateContentConfig(response_modalities=["IMAGE", "TEXT"]),
            )

            saved_textfree = False
            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    with open(textfree_path, "wb") as f:
                        f.write(part.inline_data.data)
                    saved_textfree = True
                    break

            if not saved_textfree:
                log(5, f"  Text removal returned no image — using original keyframe")
                textfree_path = ref_keyframe

        except Exception as e:
            log(5, f"  Text removal failed: {e} — using original keyframe")
            textfree_path = ref_keyframe

        time.sleep(2)

        # --- PASS 2: Product Swap ---
        log(5, f"Scene {bp['scene_number']} — Pass 2: Product swap...")
        try:
            # Use text-free image as the base
            base_bytes = open(textfree_path, "rb").read()

            parts = [types.Part(inline_data=types.Blob(data=base_bytes, mime_type="image/png"))]

            # Check if scene has product visible
            ref_analysis = bp.get("reference_analysis", {})
            has_product = ref_analysis.get("product_visible", False)

            if has_product and product_parts:
                parts.extend(product_parts)
                swap_prompt = (
                    f"Edit this image to adapt it for a different fashion brand. "
                    f"I've included product reference images — replace the visible product/accessory "
                    f"with the EXACT product shown in the reference images. Match the product precisely: "
                    f"shape, color, material, hardware details. "
                    f"Keep the EXACT same composition, camera angle, lighting, and framing. "
                    f"Do NOT add any text. "
                    f"\n\nADAPTATION:\n{bp['image_prompt']}"
                )
            else:
                swap_prompt = (
                    f"Edit this image to adapt it for a fashion brand. "
                    f"Keep the EXACT same composition, camera angle, lighting, and framing. "
                    f"Do NOT add any product, text, or branded elements. "
                    f"\n\nADAPTATION:\n{bp['image_prompt']}"
                )

            parts.append(types.Part(text=swap_prompt))

            response = client.models.generate_content(
                model=GEMINI_IMAGE_MODEL,
                contents=types.Content(parts=parts),
                config=types.GenerateContentConfig(response_modalities=["IMAGE", "TEXT"]),
            )

            saved = False
            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    with open(final_path, "wb") as f:
                        f.write(part.inline_data.data)
                    saved = True
                    log(5, f"  Saved: {final_path}")
                    break

            if not saved:
                log(5, f"  WARNING: No image returned for scene {bp['scene_number']}")
                final_path = None

        except Exception as e:
            log(5, f"  ERROR: {e}")
            final_path = None
            time.sleep(5)

        generated.append({"scene_number": bp["scene_number"], "image_path": final_path})
        time.sleep(2)

    log(5, f"Generated {sum(1 for g in generated if g.get('image_path'))} / {len(brand_prompts)} images")
    return generated


# ===========================================================================
# STAGE 6: Upscale Winners 2x
# ===========================================================================

def upscale_images(generated_images, output_dir):
    """Upscale generated images 2x before video generation (Alex's workflow step)."""
    upscale_dir = ensure_dir(os.path.join(output_dir, "upscaled"))
    client = genai.Client(api_key=GEMINI_API_KEY)

    upscaled = []

    for gi in generated_images:
        if not gi.get("image_path") or not os.path.exists(gi["image_path"]):
            upscaled.append({"scene_number": gi["scene_number"], "image_path": gi.get("image_path")})
            continue

        scene_num = f"{gi['scene_number']:03d}"
        out_path = os.path.join(upscale_dir, f"scene_{scene_num}_upscaled.png")

        if os.path.exists(out_path):
            log(6, f"Scene {gi['scene_number']} already upscaled — skipping")
            upscaled.append({"scene_number": gi["scene_number"], "image_path": out_path})
            continue

        log(6, f"Upscaling scene {gi['scene_number']}...")

        try:
            # Use PIL to upscale 2x with Lanczos
            img = Image.open(gi["image_path"])
            new_size = (img.width * 2, img.height * 2)
            upscaled_img = img.resize(new_size, Image.LANCZOS)
            upscaled_img.save(out_path, quality=95)
            log(6, f"  Upscaled to {new_size[0]}x{new_size[1]}: {out_path}")
            upscaled.append({"scene_number": gi["scene_number"], "image_path": out_path})

        except Exception as e:
            log(6, f"  Upscale failed: {e} — using original")
            upscaled.append({"scene_number": gi["scene_number"], "image_path": gi["image_path"]})

    log(6, f"Upscaled {len([u for u in upscaled if u.get('image_path')])} images")
    return upscaled


# ===========================================================================
# STAGE 7: Kling 3.0 Animation with Movement JSON
# ===========================================================================

def upload_image_for_kling(image_path):
    """Upload image to temp host for Kling URL access."""
    try:
        with open(image_path, "rb") as f:
            resp = requests.post("https://0x0.st", files={"file": (os.path.basename(image_path), f)}, timeout=30)
        if resp.status_code == 200:
            return resp.text.strip()
    except Exception:
        pass

    try:
        with open(image_path, "rb") as f:
            resp = requests.post(
                "https://catbox.moe/user/api.php",
                data={"reqtype": "fileupload"},
                files={"fileToUpload": (os.path.basename(image_path), f)},
                timeout=30,
            )
        if resp.status_code == 200 and resp.text.startswith("http"):
            return resp.text.strip()
    except Exception:
        pass

    return None


def animate_scenes(upscaled_images, brand_prompts, product_images, output_dir):
    """Animate with Kling 3.0 using movement JSON for precise motion replication."""
    anim_dir = ensure_dir(os.path.join(output_dir, "animated"))

    headers = {
        "Authorization": f"Bearer {KIE_API_KEY}",
        "Content-Type": "application/json"
    }

    # Pre-upload product images
    product_image_urls = []
    if product_images:
        for pimg in product_images[:3]:
            if os.path.exists(pimg):
                url = upload_image_for_kling(pimg)
                if url:
                    product_image_urls.append(url)

    results = []

    for ui, bp in zip(upscaled_images, brand_prompts):
        scene_num = f"{ui['scene_number']:03d}"
        out_path = os.path.join(anim_dir, f"scene_{scene_num}_animated.mp4")

        if os.path.exists(out_path):
            log(7, f"Scene {ui['scene_number']} already animated — skipping")
            results.append({"scene_number": ui["scene_number"], "video_path": out_path, "status": "cached"})
            continue

        if not ui.get("image_path") or not os.path.exists(ui["image_path"]):
            results.append({"scene_number": ui["scene_number"], "video_path": None, "status": "skipped"})
            continue

        log(7, f"Animating scene {ui['scene_number']}/{len(upscaled_images)}...")

        image_url = upload_image_for_kling(ui["image_path"])
        if not image_url:
            log(7, f"  FAILED: Could not upload image")
            results.append({"scene_number": ui["scene_number"], "video_path": None, "status": "upload_failed"})
            continue

        # Build Kling prompt with movement JSON
        motion_json = bp.get("motion_json", {})
        global_motion = bp.get("global_motion", {})
        motion_desc = bp.get("motion_description", "static")

        # Compose detailed motion prompt from movement data
        motion_parts = [bp["image_prompt"]]
        if motion_json:
            cam = motion_json.get("camera", "static")
            speed = motion_json.get("camera_speed", "medium")
            vib = motion_json.get("vibration", "none")
            subj = motion_json.get("subject_motion", "")
            motion_parts.append(f"Camera: {cam} at {speed} speed.")
            if vib != "none":
                motion_parts.append(f"Camera vibration: {vib}.")
            if subj:
                motion_parts.append(f"Subject motion: {subj}.")

        if global_motion:
            cam = global_motion.get("camera_movement", "")
            intensity = global_motion.get("motion_intensity", 5)
            if cam:
                motion_parts.append(f"Global camera: {cam} (intensity {intensity}/10).")

        kling_prompt = " ".join(motion_parts)
        if len(kling_prompt) > 2500:
            kling_prompt = kling_prompt[:2497] + "..."

        duration = str(min(max(int(bp.get("duration", 5)), 3), 10))

        payload = {
            "model": "kling-3.0/video",
            "input": {
                "prompt": kling_prompt,
                "image_urls": [image_url],
                "sound": False,
                "duration": duration,
                "aspect_ratio": "9:16",
                "mode": "pro",
                "multi_shots": False
            }
        }

        if product_image_urls:
            elements = []
            for idx, purl in enumerate(product_image_urls[:3]):
                elements.append({
                    "name": f"product_{idx+1}",
                    "description": f"Brand product reference {idx+1}",
                    "element_input_urls": [purl]
                })
            payload["input"]["kling_elements"] = elements

        success = False
        for attempt in range(MAX_KLING_RETRIES):
            try:
                resp = requests.post(KIE_CREATE_URL, headers=headers, json=payload, timeout=60)
                resp_data = resp.json()

                if resp_data.get("code") != 200:
                    log(7, f"  Attempt {attempt+1} failed: {resp_data.get('msg', 'unknown')}")
                    time.sleep(10)
                    continue

                task_id = resp_data["data"]["taskId"]
                log(7, f"  Task: {task_id}")

                video_url = poll_kling_task(task_id, headers)
                if video_url:
                    vid_resp = requests.get(video_url, timeout=120)
                    with open(out_path, "wb") as f:
                        f.write(vid_resp.content)
                    log(7, f"  Saved: {out_path}")
                    results.append({"scene_number": ui["scene_number"], "video_path": out_path, "status": "success"})
                    success = True
                    break
                else:
                    log(7, f"  Attempt {attempt+1}: timed out")

            except Exception as e:
                log(7, f"  Attempt {attempt+1} error: {e}")
                time.sleep(10)

        if not success:
            results.append({"scene_number": ui["scene_number"], "video_path": None, "status": "failed"})

        time.sleep(5)

    succeeded = sum(1 for r in results if r["status"] in ("success", "cached"))
    log(7, f"Animation complete: {succeeded}/{len(upscaled_images)} scenes")
    return results


def poll_kling_task(task_id, headers, max_wait=600):
    """Poll Kling task until complete."""
    start = time.time()
    while time.time() - start < max_wait:
        try:
            resp = requests.get(KIE_STATUS_URL, headers=headers, params={"taskId": task_id}, timeout=30)
            data = resp.json()

            if data.get("code") != 200:
                time.sleep(KLING_POLL_INTERVAL)
                continue

            state = data["data"].get("state", "")
            if state == "success":
                result_json = json.loads(data["data"].get("resultJson", "{}"))
                urls = result_json.get("resultUrls", [])
                return urls[0] if urls else None
            elif state == "fail":
                log(7, f"    Kling failed: {data['data'].get('failMsg', 'unknown')}")
                return None

        except Exception:
            pass

        time.sleep(KLING_POLL_INTERVAL)

    return None


# ===========================================================================
# STAGE 8: ElevenLabs Voice Cloning + TTS
# ===========================================================================

def clone_voice_and_generate_tts(audio_data, script_data, output_dir, voice_name=None):
    """Clone the reference voice via ElevenLabs, then generate TTS from adapted script."""
    tts_dir = ensure_dir(os.path.join(output_dir, "tts"))

    if not script_data.get("has_voiceover") or not script_data.get("adapted_script"):
        log(8, "No voiceover/script — skipping voice cloning + TTS")
        return {"voiceover_path": None, "voice_id": None}

    vocals_path = audio_data.get("vocals") or audio_data.get("full_audio")
    if not vocals_path or not os.path.exists(vocals_path):
        log(8, "No vocals audio for cloning — skipping")
        return {"voiceover_path": None, "voice_id": None}

    headers = {"xi-api-key": ELEVENLABS_API_KEY}

    # Step 8a: Clone the voice
    if not voice_name:
        voice_name = f"Fashion_Ref_{datetime.now().strftime('%Y%m%d_%H%M')}"

    log(8, f"Cloning voice as '{voice_name}'...")

    # Check if voice already exists
    existing_voice_id = find_existing_voice(voice_name, headers)

    if existing_voice_id:
        voice_id = existing_voice_id
        log(8, f"Voice already exists: {voice_id}")
    else:
        try:
            # Convert vocals to mp3 for ElevenLabs
            mp3_path = os.path.join(tts_dir, "vocals_for_cloning.mp3")
            subprocess.run([
                "ffmpeg", "-y", "-i", vocals_path,
                "-acodec", "libmp3lame", "-b:a", "128k",
                "-t", "30",  # ElevenLabs needs max ~30s for cloning
                mp3_path
            ], capture_output=True)

            with open(mp3_path, "rb") as f:
                resp = requests.post(
                    f"{ELEVENLABS_BASE}/voices/add",
                    headers=headers,
                    data={
                        "name": voice_name,
                        "description": "Cloned from fashion reference video"
                    },
                    files={"files": (os.path.basename(mp3_path), f, "audio/mpeg")}
                )

            if resp.status_code == 200:
                voice_id = resp.json().get("voice_id")
                log(8, f"Voice cloned successfully: {voice_id}")
            else:
                log(8, f"Voice cloning failed: {resp.status_code} — {resp.text[:200]}")
                return {"voiceover_path": None, "voice_id": None}

        except Exception as e:
            log(8, f"Voice cloning error: {e}")
            return {"voiceover_path": None, "voice_id": None}

    # Step 8b: Generate TTS from adapted script
    adapted_script = script_data["adapted_script"]
    full_script = adapted_script.get("full_script", "")

    if not full_script:
        log(8, "Empty adapted script — skipping TTS")
        return {"voiceover_path": None, "voice_id": voice_id}

    log(8, "Generating voiceover via ElevenLabs TTS...")
    voiceover_path = os.path.join(tts_dir, "voiceover.mp3")

    try:
        resp = requests.post(
            f"{ELEVENLABS_BASE}/text-to-speech/{voice_id}",
            headers={**headers, "Content-Type": "application/json"},
            json={
                "text": full_script,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.8,
                    "style": 0.3,
                    "use_speaker_boost": True
                }
            },
            timeout=120,
        )

        if resp.status_code == 200:
            with open(voiceover_path, "wb") as f:
                f.write(resp.content)
            log(8, f"Voiceover saved: {voiceover_path}")
        else:
            log(8, f"TTS failed: {resp.status_code} — {resp.text[:200]}")
            voiceover_path = None

    except Exception as e:
        log(8, f"TTS error: {e}")
        voiceover_path = None

    # Save voice registry
    registry_path = os.path.join(tts_dir, "voice_registry.json")
    with open(registry_path, "w") as f:
        json.dump({
            "voice_name": voice_name,
            "voice_id": voice_id,
            "cloned_from": vocals_path,
            "created_at": datetime.now().isoformat(),
        }, f, indent=2)

    return {"voiceover_path": voiceover_path, "voice_id": voice_id}


def find_existing_voice(name, headers):
    """Check if a voice with this name already exists in ElevenLabs."""
    try:
        resp = requests.get(f"{ELEVENLABS_BASE}/voices", headers=headers, timeout=30)
        if resp.status_code == 200:
            for voice in resp.json().get("voices", []):
                if voice.get("name") == name:
                    return voice.get("voice_id")
    except Exception:
        pass
    return None


# ===========================================================================
# STAGE 9: FFmpeg Final Stitch
# ===========================================================================

def stitch_final_video(animated_results, audio_data, tts_data, brand_prompts, output_dir, video_duration):
    """Stitch all animated scenes together with music + voiceover using FFmpeg."""
    stitch_dir = ensure_dir(os.path.join(output_dir, "final"))

    # Collect all successful animated clips in order
    clips = []
    for ar in animated_results:
        if ar.get("video_path") and os.path.exists(ar["video_path"]):
            clips.append(ar["video_path"])

    if not clips:
        log(9, "No animated clips to stitch — skipping")
        return None

    log(9, f"Stitching {len(clips)} clips together...")

    # Step 9a: Concatenate all video clips
    concat_path = os.path.join(stitch_dir, "concatenated.mp4")
    concat_list = os.path.join(stitch_dir, "concat_list.txt")

    with open(concat_list, "w") as f:
        for clip in clips:
            f.write(f"file '{clip}'\n")

    # First, normalize all clips to same resolution/fps
    normalized_dir = ensure_dir(os.path.join(stitch_dir, "normalized"))
    normalized_clips = []
    for i, clip in enumerate(clips):
        norm_path = os.path.join(normalized_dir, f"norm_{i:03d}.mp4")
        subprocess.run([
            "ffmpeg", "-y", "-i", clip,
            "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1",
            "-r", "30", "-c:v", "libx264", "-preset", "fast",
            "-an", norm_path
        ], capture_output=True)
        if os.path.exists(norm_path):
            normalized_clips.append(norm_path)

    # Write normalized concat list
    with open(concat_list, "w") as f:
        for clip in normalized_clips:
            f.write(f"file '{clip}'\n")

    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list,
        "-c:v", "libx264", "-preset", "fast",
        concat_path
    ], capture_output=True)

    if not os.path.exists(concat_path):
        log(9, "Concatenation failed!")
        return None

    log(9, f"Concatenated video: {concat_path}")

    # Step 9b: Add audio layers
    final_path = os.path.join(stitch_dir, "final_output.mp4")

    music_path = audio_data.get("music")
    voiceover_path = tts_data.get("voiceover_path") if tts_data else None

    if voiceover_path and music_path and os.path.exists(voiceover_path) and os.path.exists(music_path):
        # Both voiceover and music
        log(9, "Adding voiceover + music...")
        subprocess.run([
            "ffmpeg", "-y",
            "-i", concat_path,
            "-i", voiceover_path,
            "-i", music_path,
            "-filter_complex",
            "[1:a]volume=1.0[vo];[2:a]volume=0.3[music];[vo][music]amix=inputs=2:duration=first[aout]",
            "-map", "0:v", "-map", "[aout]",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            final_path
        ], capture_output=True)

    elif music_path and os.path.exists(music_path):
        # Music only
        log(9, "Adding music...")
        subprocess.run([
            "ffmpeg", "-y",
            "-i", concat_path,
            "-i", music_path,
            "-map", "0:v", "-map", "1:a",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            final_path
        ], capture_output=True)

    elif voiceover_path and os.path.exists(voiceover_path):
        # Voiceover only
        log(9, "Adding voiceover...")
        subprocess.run([
            "ffmpeg", "-y",
            "-i", concat_path,
            "-i", voiceover_path,
            "-map", "0:v", "-map", "1:a",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            final_path
        ], capture_output=True)

    else:
        # No audio — just copy
        log(9, "No audio layers — using video only")
        subprocess.run(["cp", concat_path, final_path], capture_output=True)

    if os.path.exists(final_path):
        file_size = os.path.getsize(final_path) / (1024 * 1024)
        log(9, f"Final video: {final_path} ({file_size:.1f} MB)")
    else:
        log(9, "Final stitch failed — falling back to concatenated video")
        final_path = concat_path

    return final_path


# ===========================================================================
# STAGE 10: Google Drive Upload
# ===========================================================================

def upload_to_drive(output_dir, drive_folder_id, folder_name):
    """Upload final output to Google Drive."""
    if not drive_folder_id:
        log(10, "No Drive folder ID — skipping upload")
        return

    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
    except ImportError:
        log(10, "Google Drive libraries not installed — skipping upload")
        return

    # Authenticate
    creds = None
    if os.path.exists(GDRIVE_TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(GDRIVE_TOKEN_PATH)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(
                {"installed": {
                    "client_id": GDRIVE_CLIENT_ID,
                    "client_secret": GDRIVE_CLIENT_SECRET,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
                }},
                ["https://www.googleapis.com/auth/drive.file"]
            )
            creds = flow.run_local_server(port=0)
        with open(GDRIVE_TOKEN_PATH, "w") as f:
            f.write(creds.to_json())

    service = build("drive", "v3", credentials=creds)

    # Create subfolder
    folder_meta = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [drive_folder_id]
    }
    folder = service.files().create(body=folder_meta, fields="id").execute()
    subfolder_id = folder["id"]
    log(10, f"Created Drive folder: {folder_name} ({subfolder_id})")

    # Upload files from final/ and animated/
    upload_dirs = ["final", "animated"]
    for subdir in upload_dirs:
        dir_path = os.path.join(output_dir, subdir)
        if not os.path.isdir(dir_path):
            continue
        for fname in sorted(os.listdir(dir_path)):
            fpath = os.path.join(dir_path, fname)
            if not os.path.isfile(fpath) or fname.startswith("."):
                continue
            media = MediaFileUpload(fpath, resumable=True)
            file_meta = {"name": fname, "parents": [subfolder_id]}
            service.files().create(body=file_meta, media_body=media, fields="id").execute()
            log(10, f"  Uploaded: {fname}")

    # Upload assembly guide if exists
    guide_path = os.path.join(output_dir, "assembly_guide.md")
    if os.path.exists(guide_path):
        media = MediaFileUpload(guide_path, mimetype="text/markdown")
        file_meta = {"name": "assembly_guide.md", "parents": [subfolder_id]}
        service.files().create(body=file_meta, media_body=media, fields="id").execute()
        log(10, "  Uploaded: assembly_guide.md")

    log(10, "Upload complete!")


# ===========================================================================
# Assembly Guide Generator
# ===========================================================================

def generate_assembly_guide(animated_results, brand_prompts, script_data, audio_data, output_dir, brand, concept_code):
    """Generate an assembly guide for the video editor."""
    guide_path = os.path.join(output_dir, "assembly_guide.md")

    lines = [
        f"# Assembly Guide — {concept_code}",
        f"**Brand:** {brand}",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## Scene Order",
        "",
    ]

    for ar, bp in zip(animated_results, brand_prompts):
        status = ar.get("status", "unknown")
        video = os.path.basename(ar["video_path"]) if ar.get("video_path") else "MISSING"
        motion = bp.get("motion_description", "static")[:100]

        lines.append(f"### Scene {ar['scene_number']}")
        lines.append(f"- **File:** `{video}` ({status})")
        lines.append(f"- **Duration:** {bp.get('duration', '?')}s")
        lines.append(f"- **Motion:** {motion}")
        lines.append(f"- **Type:** {bp.get('reference_analysis', {}).get('scene_type', 'unknown')}")
        lines.append("")

    if script_data and script_data.get("adapted_script"):
        lines.append("## Voiceover Script")
        lines.append("")
        lines.append(script_data["adapted_script"].get("full_script", "N/A"))
        lines.append("")

    if audio_data and audio_data.get("music"):
        lines.append("## Audio")
        lines.append(f"- **Music:** `{os.path.basename(audio_data['music'])}`")
        lines.append(f"- **Has voiceover:** {audio_data.get('has_voiceover', False)}")
        lines.append("")

    with open(guide_path, "w") as f:
        f.write("\n".join(lines))

    log("guide", f"Assembly guide saved: {guide_path}")
    return guide_path


# ===========================================================================
# MAIN PIPELINE
# ===========================================================================

def main():
    parser = argparse.ArgumentParser(description="Fashion Replicator Pipeline")
    parser.add_argument("--video", required=True, help="Path to reference video")
    parser.add_argument("--brand", required=True, help="Target brand name")
    parser.add_argument("--product-context", default="", help="Product description")
    parser.add_argument("--style", default="", help="Style notes")
    parser.add_argument("--product-images", default="", help="Comma-separated product image paths")
    parser.add_argument("--output-dir", required=True, help="Output directory")
    parser.add_argument("--concept-code", default="", help="Concept code (e.g., SD-POV-01)")
    parser.add_argument("--drive-folder", default="", help="Google Drive folder ID for upload")
    parser.add_argument("--drive-folder-name", default="", help="Drive subfolder name")
    parser.add_argument("--voice-name", default="", help="Name for cloned voice in ElevenLabs")
    parser.add_argument("--skip-voiceover", action="store_true", help="Skip voice cloning/TTS")
    parser.add_argument("--skip-upload", action="store_true", help="Skip Google Drive upload")
    parser.add_argument("--scene-threshold", type=float, default=SCENE_THRESHOLD, help="Scene detection threshold")

    args = parser.parse_args()

    video_path = os.path.expanduser(args.video)
    output_dir = os.path.expanduser(args.output_dir)
    ensure_dir(output_dir)

    if not os.path.exists(video_path):
        print(f"ERROR: Video not found: {video_path}")
        sys.exit(1)

    # Load brand knowledge
    bk = load_brand_knowledge(args.brand)
    product_context = args.product_context or bk["default_product_context"]
    product_images = [p.strip() for p in args.product_images.split(",") if p.strip()] if args.product_images else bk["product_images"]
    brand_knowledge = bk["context_text"]

    print("=" * 60)
    print(f"FASHION REPLICATOR PIPELINE")
    print(f"Brand: {args.brand}")
    print(f"Video: {video_path}")
    print(f"Output: {output_dir}")
    print(f"Product images: {len(product_images)}")
    print(f"Skip voiceover: {args.skip_voiceover}")
    print("=" * 60)

    # Load progress for resume capability
    progress = load_progress(output_dir)

    # --- STAGE 0: Audio Extraction ---
    if "stage_0" not in progress["completed_stages"]:
        audio_data = extract_audio(video_path, output_dir)
        progress["completed_stages"]["stage_0"] = True
        progress["audio_data"] = audio_data
        save_progress(output_dir, progress)
    else:
        audio_data = progress.get("audio_data", {})
        log(0, "Already completed — loaded from progress")

    # --- STAGE 1: Scene Detection ---
    if "stage_1" not in progress["completed_stages"]:
        scenes, video_duration = extract_scenes(video_path, output_dir, args.scene_threshold)
        progress["completed_stages"]["stage_1"] = True
        progress["scenes"] = scenes
        progress["video_duration"] = video_duration
        save_progress(output_dir, progress)
    else:
        scenes = progress.get("scenes", [])
        video_duration = progress.get("video_duration", 0)
        log(1, "Already completed — loaded from progress")

    # --- STAGE 2: Scene Analysis + Movement JSON ---
    if "stage_2" not in progress["completed_stages"]:
        analyses, movement_json = analyze_scenes_with_movement(scenes, video_path, output_dir)
        progress["completed_stages"]["stage_2"] = True
        save_progress(output_dir, progress)
    else:
        analysis_path = os.path.join(output_dir, "analysis", "scene_analysis.json")
        movement_path = os.path.join(output_dir, "analysis", "movement_data.json")
        analyses = json.load(open(analysis_path)) if os.path.exists(analysis_path) else []
        movement_json = json.load(open(movement_path)) if os.path.exists(movement_path) else {}
        log(2, "Already completed — loaded from progress")

    # --- STAGE 3: Transcription + Script Rewriting ---
    if not args.skip_voiceover and "stage_3" not in progress["completed_stages"]:
        script_data = transcribe_and_rewrite_script(audio_data, args.brand, product_context, output_dir, brand_knowledge)
        progress["completed_stages"]["stage_3"] = True
        progress["script_data"] = {"has_voiceover": script_data["has_voiceover"]}
        save_progress(output_dir, progress)
    elif args.skip_voiceover:
        script_data = {"original_script": None, "adapted_script": None, "has_voiceover": False}
        log(3, "Skipped (--skip-voiceover)")
    else:
        # Load from saved files
        script_dir = os.path.join(output_dir, "script")
        adapted_path = os.path.join(script_dir, "adapted_script.json")
        script_data = {
            "adapted_script": json.load(open(adapted_path)) if os.path.exists(adapted_path) else None,
            "has_voiceover": progress.get("script_data", {}).get("has_voiceover", False),
        }
        log(3, "Already completed — loaded from progress")

    # --- STAGE 4: Brand-Adapted Image Prompts ---
    if "stage_4" not in progress["completed_stages"]:
        brand_prompts = generate_brand_prompts(analyses, args.brand, product_context, args.style, output_dir, brand_knowledge)
        progress["completed_stages"]["stage_4"] = True
        save_progress(output_dir, progress)
    else:
        prompts_path = os.path.join(output_dir, "prompts", "image_prompts.json")
        brand_prompts = json.load(open(prompts_path)) if os.path.exists(prompts_path) else []
        log(4, "Already completed — loaded from progress")

    # --- STAGE 5: Image-to-Image (Text Removal + Product Swap) ---
    if "stage_5" not in progress["completed_stages"]:
        generated_images = generate_images(brand_prompts, scenes, product_images, output_dir)
        progress["completed_stages"]["stage_5"] = True
        save_progress(output_dir, progress)
    else:
        gen_dir = os.path.join(output_dir, "generated")
        generated_images = []
        for bp in brand_prompts:
            scene_num = f"{bp['scene_number']:03d}"
            path = os.path.join(gen_dir, f"scene_{scene_num}_brand.png")
            generated_images.append({
                "scene_number": bp["scene_number"],
                "image_path": path if os.path.exists(path) else None
            })
        log(5, "Already completed — loaded from progress")

    # --- STAGE 6: Upscale 2x ---
    if "stage_6" not in progress["completed_stages"]:
        upscaled_images = upscale_images(generated_images, output_dir)
        progress["completed_stages"]["stage_6"] = True
        save_progress(output_dir, progress)
    else:
        upscale_dir = os.path.join(output_dir, "upscaled")
        upscaled_images = []
        for gi in generated_images:
            scene_num = f"{gi['scene_number']:03d}"
            path = os.path.join(upscale_dir, f"scene_{scene_num}_upscaled.png")
            upscaled_images.append({
                "scene_number": gi["scene_number"],
                "image_path": path if os.path.exists(path) else gi.get("image_path")
            })
        log(6, "Already completed — loaded from progress")

    # --- STAGE 7: Kling 3.0 Animation ---
    if "stage_7" not in progress["completed_stages"]:
        animated_results = animate_scenes(upscaled_images, brand_prompts, product_images, output_dir)
        progress["completed_stages"]["stage_7"] = True
        save_progress(output_dir, progress)
    else:
        anim_dir = os.path.join(output_dir, "animated")
        animated_results = []
        for bp in brand_prompts:
            scene_num = f"{bp['scene_number']:03d}"
            path = os.path.join(anim_dir, f"scene_{scene_num}_animated.mp4")
            animated_results.append({
                "scene_number": bp["scene_number"],
                "video_path": path if os.path.exists(path) else None,
                "status": "cached" if os.path.exists(path) else "missing"
            })
        log(7, "Already completed — loaded from progress")

    # --- STAGE 8: Voice Cloning + TTS ---
    if not args.skip_voiceover and script_data.get("has_voiceover") and "stage_8" not in progress["completed_stages"]:
        tts_data = clone_voice_and_generate_tts(audio_data, script_data, output_dir, args.voice_name or None)
        progress["completed_stages"]["stage_8"] = True
        save_progress(output_dir, progress)
    elif args.skip_voiceover:
        tts_data = {"voiceover_path": None, "voice_id": None}
        log(8, "Skipped (--skip-voiceover)")
    else:
        tts_path = os.path.join(output_dir, "tts", "voiceover.mp3")
        tts_data = {"voiceover_path": tts_path if os.path.exists(tts_path) else None}
        log(8, "Already completed or no voiceover")

    # --- STAGE 9: FFmpeg Stitch ---
    if "stage_9" not in progress["completed_stages"]:
        final_video = stitch_final_video(animated_results, audio_data, tts_data, brand_prompts, output_dir, video_duration)
        progress["completed_stages"]["stage_9"] = True
        save_progress(output_dir, progress)

        # Generate assembly guide
        concept_code = args.concept_code or f"{args.brand.upper()[:3]}-REP-01"
        generate_assembly_guide(animated_results, brand_prompts, script_data, audio_data, output_dir, args.brand, concept_code)
    else:
        final_video = os.path.join(output_dir, "final", "final_output.mp4")
        if not os.path.exists(final_video):
            final_video = None
        log(9, "Already completed — loaded from progress")

    # --- STAGE 10: Google Drive Upload ---
    if not args.skip_upload and args.drive_folder:
        folder_name = args.drive_folder_name or args.concept_code or f"{args.brand}_{datetime.now().strftime('%Y%m%d')}"
        upload_to_drive(output_dir, args.drive_folder, folder_name)
    else:
        log(10, "Skipped (--skip-upload or no --drive-folder)")

    # --- SUMMARY ---
    print("\n" + "=" * 60)
    print("PIPELINE COMPLETE")
    print("=" * 60)
    succeeded_scenes = sum(1 for r in animated_results if r.get("video_path"))
    print(f"Scenes animated: {succeeded_scenes}/{len(brand_prompts)}")
    if final_video:
        print(f"Final video: {final_video}")
    if tts_data and tts_data.get("voiceover_path"):
        print(f"Voiceover: {tts_data['voiceover_path']}")
    if tts_data and tts_data.get("voice_id"):
        print(f"Cloned voice ID: {tts_data['voice_id']}")
    print(f"Output dir: {output_dir}")
    print("=" * 60)


if __name__ == "__main__":
    main()
