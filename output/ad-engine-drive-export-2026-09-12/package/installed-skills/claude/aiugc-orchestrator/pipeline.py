#!/usr/bin/env python3
"""
AI UGC Orchestrator Pipeline
==============================
End-to-end: Script + Brand → ElevenLabs TTS → Avatar Image → Fabric Talking Head → Final Video

Usage:
    python3 pipeline.py \
        --script "Your ad script here..." \
        --brand "Motilli" \
        --avatar-desc "35-year-old woman in a car" \
        --output-dir "./orchestrator-output"
"""

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime

# ---------------------------------------------------------------------------
# Load .env
# ---------------------------------------------------------------------------
ENV_PATH = os.path.expanduser("~/Documents/marketing brain/.env")
def load_env():
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, value = line.partition("=")
                    os.environ.setdefault(key.strip(), value.strip())
load_env()

try:
    import requests
except ImportError:
    print("[!] pip install requests")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
FAL_API_KEY = os.environ.get("FAL_API_KEY", "")
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")

ELEVENLABS_TTS_URL = "https://api.elevenlabs.io/v1/text-to-speech"
ELEVENLABS_DEFAULT_VOICE = "21m00Tcm4TlvDq8ikWAM"  # Rachel — calm, warm female
ELEVENLABS_MODEL = "eleven_multilingual_v2"

FAL_FABRIC_URL = "https://fal.run/veed/fabric-1.0"
FAL_FABRIC_TEXT_URL = "https://fal.run/veed/fabric-1.0/text"

GEMINI_IMAGE_MODEL = "gemini-3.1-flash-image-preview"  # Nano Banana 2

VAULT_ROOT = os.path.expanduser("~/Documents/marketing brain")

GDRIVE_CLIENT_ID = "630165550470-bk00miojfehkb5va5hdoupbn170lurhh.apps.googleusercontent.com"
GDRIVE_CLIENT_SECRET = "[REDACTED_SECRET]"
GDRIVE_TOKEN_PATH = os.path.expanduser("~/.claude/skills/aiugc-orchestrator/gdrive_token.json")

# Brand registry (lightweight — just avatar defaults)
BRAND_AVATARS = {
    "motilli": {
        "default_avatar_desc": "35-year-old American woman, warm and approachable, casual comfortable clothing, natural makeup, sitting in a bright modern kitchen or living room, natural daylight, iPhone-selfie quality, slightly imperfect framing",
        "default_voice_desc": "Warm, friendly, relatable female voice, American accent, conversational tone like talking to a friend",
    },
    "lunessa": {
        "default_avatar_desc": "50-year-old woman, elegant but approachable, wearing a casual blouse, sitting at a desk or kitchen counter, warm indoor lighting, natural and trustworthy appearance",
        "default_voice_desc": "Confident, warm female voice, American accent, 50s, sounds like a trusted friend sharing health advice",
    },
    "velantra-boat-tote": {
        "default_avatar_desc": "30-year-old stylish woman, summer outfit, holding or near a canvas tote bag, outdoor setting (cafe, beach boardwalk, or farmer's market), natural daylight, lifestyle aesthetic",
        "default_voice_desc": "Trendy, confident female voice, slightly aspirational but relatable, American accent",
    },
    "velantra-meridian": {
        "default_avatar_desc": "35-year-old professional woman, smart casual outfit, carrying or displaying a leather handbag, urban setting or modern office, polished but approachable",
        "default_voice_desc": "Confident, polished female voice, professional yet warm, American accent",
    },
    "velantra-weekender": {
        "default_avatar_desc": "30-year-old adventurous woman, travel outfit, with a canvas and leather weekender bag, airport or hotel lobby or car trunk, excited traveler energy",
        "default_voice_desc": "Energetic, adventurous female voice, relatable and enthusiastic, American accent",
    },
}

# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def log(stage, msg):
    prefix = f"[Stage {stage}]" if isinstance(stage, int) else f"[{stage}]"
    print(f"{prefix} {msg}")

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)
    return path

def upload_to_fal_storage(file_path):
    """Upload a local file to fal.ai storage."""
    ext = Path(file_path).suffix.lower()
    mime_map = {
        ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".webp": "image/webp", ".mp3": "audio/mpeg", ".wav": "audio/wav",
        ".m4a": "audio/mp4", ".aac": "audio/aac",
    }
    mime = mime_map.get(ext, "application/octet-stream")

    try:
        with open(file_path, "rb") as f:
            resp = requests.post(
                "https://fal.ai/api/storage/upload",
                headers={"Authorization": f"Key {FAL_API_KEY}"},
                files={"file": (os.path.basename(file_path), f, mime)},
                timeout=120,
            )
        if resp.status_code == 200:
            data = resp.json()
            return data.get("url") or data.get("file_url")
    except Exception as e:
        log("U", f"  Upload error: {e}")
    return None


# ---------------------------------------------------------------------------
# Stage 1: ElevenLabs TTS
# ---------------------------------------------------------------------------

def generate_voiceover(script_text, output_dir, voice_id=None):
    """Generate voiceover audio from script using ElevenLabs."""
    vo_dir = ensure_dir(os.path.join(output_dir, "voiceover"))
    vo_path = os.path.join(vo_dir, "script_vo.mp3")

    if os.path.exists(vo_path):
        log(1, f"Voiceover already exists: {vo_path}")
        return vo_path

    if not ELEVENLABS_API_KEY:
        log(1, "No ELEVENLABS_API_KEY set — skipping TTS. Will use Fabric built-in TTS.")
        return None

    vid = voice_id or ELEVENLABS_DEFAULT_VOICE
    url = f"{ELEVENLABS_TTS_URL}/{vid}"

    log(1, f"Generating voiceover ({len(script_text)} chars, voice: {vid})...")

    payload = {
        "text": script_text,
        "model_id": ELEVENLABS_MODEL,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.3,
            "use_speaker_boost": True,
        }
    }

    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }

    for attempt in range(3):
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=120)

            if resp.status_code == 200:
                with open(vo_path, "wb") as f:
                    f.write(resp.content)
                size_mb = len(resp.content) / 1024 / 1024
                log(1, f"  Saved: {vo_path} ({size_mb:.1f}MB)")
                return vo_path
            else:
                log(1, f"  Attempt {attempt+1}: HTTP {resp.status_code} — {resp.text[:200]}")

        except Exception as e:
            log(1, f"  Attempt {attempt+1} error: {e}")

        time.sleep(5)

    log(1, "  ElevenLabs TTS failed — will fall back to Fabric TTS")
    return None


# ---------------------------------------------------------------------------
# Stage 2: Avatar Image Generation (Nano Banana 2)
# ---------------------------------------------------------------------------

def generate_avatar_image(avatar_desc, brand_key, output_dir):
    """Generate avatar image using Nano Banana 2 (Gemini image generation)."""
    avatar_dir = ensure_dir(os.path.join(output_dir, "avatar"))
    avatar_path = os.path.join(avatar_dir, "avatar.png")

    if os.path.exists(avatar_path):
        log(2, f"Avatar image already exists: {avatar_path}")
        return avatar_path

    try:
        from google import genai
        from google.genai import types
    except ImportError:
        log(2, "google-genai not installed. pip install google-genai")
        return None

    client = genai.Client(api_key=GEMINI_API_KEY)

    # Get default avatar description from brand if not provided
    if not avatar_desc:
        brand_info = BRAND_AVATARS.get(brand_key, {})
        avatar_desc = brand_info.get("default_avatar_desc", "35-year-old woman, casual clothing, natural indoor setting, warm lighting")

    prompt = f"""Generate a photorealistic image of a person for a UGC-style video ad.

SUBJECT: {avatar_desc}

CRITICAL REQUIREMENTS:
- Photorealistic, not AI-looking. Must look like a real person.
- Natural, slightly imperfect lighting (like a phone camera, not studio)
- Person should be facing the camera, eyes looking at camera (talking-head framing)
- Medium shot (head and shoulders visible, some of torso)
- Natural facial expression — warm, approachable, mid-conversation
- Background should be slightly blurred/soft (shallow depth of field)
- The person's mouth should be CLOSED or in a neutral position (not mid-word)
- No text, no logos, no watermarks
- 9:16 portrait orientation preferred"""

    log(2, f"Generating avatar image...")

    try:
        response = client.models.generate_content(
            model=GEMINI_IMAGE_MODEL,
            contents=types.Content(parts=[types.Part.from_text(text=prompt)]),
            config=types.GenerateContentConfig(
                response_modalities=["image", "text"],
                temperature=0.6,
            ),
        )

        if response.candidates:
            for part in response.candidates[0].content.parts:
                if hasattr(part, "inline_data") and part.inline_data:
                    with open(avatar_path, "wb") as f:
                        f.write(part.inline_data.data)
                    log(2, f"  Saved: {avatar_path}")
                    return avatar_path

        log(2, "  No image generated by Nano Banana 2")
    except Exception as e:
        log(2, f"  Error: {e}")

    return None


# ---------------------------------------------------------------------------
# Stage 3: Fabric Talking Head
# ---------------------------------------------------------------------------

def generate_fabric_video(avatar_image_path, vo_audio_path, script_text,
                          voice_description, use_fabric_tts, resolution, output_dir):
    """Generate talking head video using VEED Fabric 1.0."""
    fabric_dir = ensure_dir(os.path.join(output_dir, "fabric"))
    fabric_path = os.path.join(fabric_dir, "talking_head.mp4")

    if os.path.exists(fabric_path):
        log(3, f"Fabric video already exists: {fabric_path}")
        return fabric_path

    if not FAL_API_KEY:
        log(3, "ERROR: FAL_API_KEY not set")
        return None

    # Upload image
    log(3, "Uploading avatar image to fal.ai...")
    image_url = upload_to_fal_storage(avatar_image_path)
    if not image_url:
        log(3, "  Image upload failed")
        return None

    headers = {
        "Authorization": f"Key {FAL_API_KEY}",
        "Content-Type": "application/json"
    }

    if use_fabric_tts or not vo_audio_path:
        # Text-to-video mode (Fabric TTS)
        log(3, f"Generating video with Fabric TTS ({resolution})...")
        payload = {
            "image_url": image_url,
            "text": script_text,
            "resolution": resolution,
        }
        if voice_description:
            payload["voice_description"] = voice_description
        url = FAL_FABRIC_TEXT_URL
    else:
        # Image + audio mode
        log(3, "Uploading voiceover audio to fal.ai...")
        audio_url = upload_to_fal_storage(vo_audio_path)
        if not audio_url:
            log(3, "  Audio upload failed")
            return None

        log(3, f"Generating video with audio ({resolution})...")
        payload = {
            "image_url": image_url,
            "audio_url": audio_url,
            "resolution": resolution,
        }
        url = FAL_FABRIC_URL

    for attempt in range(3):
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=7200)

            if resp.status_code == 200:
                data = resp.json()
                video_url = data.get("video", {}).get("url")
                if video_url:
                    log(3, "  Downloading video...")
                    vid_resp = requests.get(video_url, timeout=300)
                    with open(fabric_path, "wb") as f:
                        f.write(vid_resp.content)
                    size_mb = len(vid_resp.content) / 1024 / 1024
                    log(3, f"  Saved: {fabric_path} ({size_mb:.1f}MB)")
                    return fabric_path
                else:
                    log(3, f"  No video URL in response: {data}")

            elif resp.status_code == 422:
                log(3, f"  Validation error: {resp.json()}")
                return None
            else:
                log(3, f"  Attempt {attempt+1}: HTTP {resp.status_code}")

        except requests.exceptions.Timeout:
            log(3, f"  Attempt {attempt+1}: Timeout (normal for long videos, retrying...)")
        except Exception as e:
            log(3, f"  Attempt {attempt+1} error: {e}")

        time.sleep(10)

    return None


# ---------------------------------------------------------------------------
# Stage 4: AIUGC Replicator (Optional)
# ---------------------------------------------------------------------------

def run_aiugc_replicator(reference_video, vo_audio_path, brand, output_dir, aspect_ratio="9:16"):
    """Run the AIUGC replicator pipeline using the reference video."""
    replicator_dir = os.path.join(output_dir, "replicated")
    replicator_script = os.path.expanduser("~/.claude/skills/aiugc-replicator/pipeline.py")

    if not os.path.exists(replicator_script):
        log(4, "AIUGC replicator not found — skipping")
        return None

    log(4, f"Running AIUGC replicator on reference video...")

    cmd = [
        "python3", replicator_script,
        "--video", reference_video,
        "--voiceover", vo_audio_path,
        "--brand", brand,
        "--aspect-ratio", aspect_ratio,
        "--output-dir", replicator_dir,
        "--skip-upload",
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=7200)

    # Find the final video
    final_dir = os.path.join(replicator_dir, "final")
    if os.path.exists(final_dir):
        for f in os.listdir(final_dir):
            if f.endswith(".mp4"):
                return os.path.join(final_dir, f)

    log(4, f"  Replicator may have had issues. stdout: {result.stdout[-500:]}")
    return None


# ---------------------------------------------------------------------------
# Stage 5: Post-Processing (FFmpeg)
# ---------------------------------------------------------------------------

def post_process(input_video, output_dir, aspect_ratio="9:16", bg_music=None):
    """Crop to aspect ratio, add background music, fade in/out."""
    final_dir = ensure_dir(os.path.join(output_dir, "final"))
    ar_tag = aspect_ratio.replace(":", "x")
    final_path = os.path.join(final_dir, f"aiugc_final_{ar_tag}.mp4")

    if os.path.exists(final_path):
        log(5, f"Final video already exists: {final_path}")
        return final_path

    log(5, "Post-processing video...")

    cmd = ["ffmpeg", "-i", input_video]
    filters = []

    # Aspect ratio
    ar_map = {
        "9:16": "crop=ih*9/16:ih",
        "1:1": "crop=min(iw\\,ih):min(iw\\,ih)",
        "16:9": "crop=iw:iw*9/16",
    }
    crop = ar_map.get(aspect_ratio)
    if crop:
        filters.append(crop)

    # Fade
    filters.append("fade=t=in:d=0.5")

    if filters:
        cmd.extend(["-vf", ",".join(filters)])

    if bg_music and os.path.exists(bg_music):
        cmd.extend(["-i", bg_music])
        cmd.extend([
            "-filter_complex",
            "[0:a]volume=1.0[vo];[1:a]volume=0.15,afade=t=in:d=1[bg];[vo][bg]amix=inputs=2:duration=shortest[out]",
            "-map", "0:v", "-map", "[out]"
        ])
    else:
        cmd.extend(["-map", "0:v", "-map", "0:a"])

    cmd.extend([
        "-c:v", "libx264", "-crf", "18", "-preset", "medium",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        final_path, "-y"
    ])

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

    if os.path.exists(final_path):
        log(5, f"  Saved: {final_path}")
        return final_path
    else:
        log(5, f"  FFmpeg error, using input video as final")
        import shutil
        shutil.copy2(input_video, final_path)
        return final_path


# ---------------------------------------------------------------------------
# Stage 6: Google Drive Upload
# ---------------------------------------------------------------------------

def get_drive_service():
    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build
    except ImportError:
        return None

    SCOPES = ["https://www.googleapis.com/auth/drive.file"]
    creds = None

    if os.path.exists(GDRIVE_TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(GDRIVE_TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            client_config = {
                "installed": {
                    "client_id": GDRIVE_CLIENT_ID,
                    "client_secret": GDRIVE_CLIENT_SECRET,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": ["http://localhost"]
                }
            }
            flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(GDRIVE_TOKEN_PATH, "w") as token:
            token.write(creds.to_json())

    return build("drive", "v3", credentials=creds)


def upload_to_drive(output_dir, drive_folder_id, brand):
    from googleapiclient.http import MediaFileUpload

    service = get_drive_service()
    if not service:
        log(6, "Google Drive packages not installed — skipping upload")
        return

    date_str = datetime.now().strftime("%Y-%m-%d")
    folder_name = f"{brand}_{date_str}_orchestrator"

    folder_metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [drive_folder_id]
    }
    folder = service.files().create(body=folder_metadata, fields="id").execute()
    parent_id = folder.get("id")
    log(6, f"Created Drive folder: {folder_name}")

    upload_count = 0
    for subdir in ["final", "fabric", "voiceover"]:
        dir_path = os.path.join(output_dir, subdir)
        if not os.path.exists(dir_path):
            continue
        for filename in sorted(os.listdir(dir_path)):
            filepath = os.path.join(dir_path, filename)
            if not os.path.isfile(filepath):
                continue
            ext = Path(filepath).suffix.lower()
            mime = {"mp4": "video/mp4", "mp3": "audio/mpeg", "png": "image/png",
                    "json": "application/json"}.get(ext.lstrip("."), "application/octet-stream")
            file_metadata = {"name": filename, "parents": [parent_id]}
            media = MediaFileUpload(filepath, mimetype=mime, resumable=True)
            service.files().create(body=file_metadata, media_body=media, fields="id").execute()
            upload_count += 1
            log(6, f"  Uploaded: {filename}")

    log(6, f"Uploaded {upload_count} files")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="AI UGC Orchestrator — Script to Finished Video")
    parser.add_argument("--script", default="", help="Ad script text (inline)")
    parser.add_argument("--script-file", default="", help="Path to script file")
    parser.add_argument("--brand", required=True, help="Brand name")
    parser.add_argument("--avatar-desc", default="", help="Avatar appearance description")
    parser.add_argument("--avatar-image", default="", help="Existing avatar image path (skip generation)")
    parser.add_argument("--voice-id", default="", help="ElevenLabs voice ID")
    parser.add_argument("--voice-description", default="", help="Voice description for Fabric TTS")
    parser.add_argument("--use-fabric-tts", action="store_true", help="Use Fabric built-in TTS instead of ElevenLabs")
    parser.add_argument("--reference-video", default="", help="Reference video for AIUGC replicator")
    parser.add_argument("--resolution", default="720p", choices=["480p", "720p"])
    parser.add_argument("--aspect-ratio", default="9:16")
    parser.add_argument("--bg-music", default="", help="Background music path")
    parser.add_argument("--drive-folder", default="", help="Google Drive folder ID")
    parser.add_argument("--output-dir", default="./orchestrator-output")

    args = parser.parse_args()

    # Load script
    script_text = args.script
    if args.script_file:
        if os.path.exists(args.script_file):
            with open(args.script_file) as f:
                script_text = f.read().strip()
        else:
            print(f"ERROR: Script file not found: {args.script_file}")
            sys.exit(1)

    if not script_text:
        print("ERROR: Provide --script or --script-file")
        sys.exit(1)

    output_dir = args.output_dir
    ensure_dir(output_dir)
    brand_key = args.brand.lower().replace(" ", "-")

    # Get brand defaults
    brand_info = BRAND_AVATARS.get(brand_key, {})
    voice_desc = args.voice_description or brand_info.get("default_voice_desc", "")

    print("=" * 60)
    print(f"AI UGC ORCHESTRATOR — {args.brand}")
    print(f"Script: {len(script_text)} chars")
    print(f"Resolution: {args.resolution}")
    print(f"Aspect ratio: {args.aspect_ratio}")
    print(f"TTS: {'Fabric' if args.use_fabric_tts else 'ElevenLabs' if ELEVENLABS_API_KEY else 'Fabric (no ElevenLabs key)'}")
    print(f"Avatar: {'provided' if args.avatar_image else 'will generate'}")
    print(f"Reference video: {'yes' if args.reference_video else 'no'}")
    print("=" * 60)

    # =====================================================================
    # Stage 1: Voiceover
    # =====================================================================
    print(f"\n{'='*40}\nSTAGE 1: Voiceover Generation\n{'='*40}")

    vo_path = None
    use_fabric_tts = args.use_fabric_tts

    if not use_fabric_tts:
        vo_path = generate_voiceover(script_text, output_dir, args.voice_id or None)
        if not vo_path:
            log(1, "Falling back to Fabric built-in TTS")
            use_fabric_tts = True

    # =====================================================================
    # Stage 2: Avatar Image
    # =====================================================================
    print(f"\n{'='*40}\nSTAGE 2: Avatar Image Generation\n{'='*40}")

    avatar_path = args.avatar_image
    if avatar_path and os.path.exists(avatar_path):
        log(2, f"Using provided avatar: {avatar_path}")
    else:
        avatar_path = generate_avatar_image(args.avatar_desc, brand_key, output_dir)
        if not avatar_path:
            print("ERROR: Could not generate avatar image")
            sys.exit(1)

    # =====================================================================
    # Stage 3: Fabric Talking Head
    # =====================================================================
    print(f"\n{'='*40}\nSTAGE 3: Fabric Talking Head Video\n{'='*40}")

    fabric_path = generate_fabric_video(
        avatar_path, vo_path, script_text,
        voice_desc, use_fabric_tts, args.resolution, output_dir
    )

    if not fabric_path:
        print("ERROR: Fabric video generation failed")
        sys.exit(1)

    # =====================================================================
    # Stage 4: AIUGC Replicator (Optional)
    # =====================================================================
    video_for_final = fabric_path

    if args.reference_video and os.path.exists(args.reference_video):
        print(f"\n{'='*40}\nSTAGE 4: AIUGC Replicator\n{'='*40}")

        vo_for_replicator = vo_path or fabric_path  # Use fabric output as VO source if no separate VO
        replicated = run_aiugc_replicator(
            args.reference_video, vo_for_replicator,
            args.brand, output_dir, args.aspect_ratio
        )
        if replicated:
            video_for_final = replicated
        else:
            log(4, "Replicator failed — using Fabric output as final")
    else:
        log(4, "No reference video — skipping replicator (using Fabric output directly)")

    # =====================================================================
    # Stage 5: Post-Processing
    # =====================================================================
    print(f"\n{'='*40}\nSTAGE 5: Post-Processing\n{'='*40}")

    final_path = post_process(
        video_for_final, output_dir, args.aspect_ratio,
        args.bg_music if args.bg_music else None
    )

    # =====================================================================
    # Save metadata
    # =====================================================================
    metadata = {
        "generated_at": datetime.now().isoformat(),
        "brand": args.brand,
        "script_length": len(script_text),
        "resolution": args.resolution,
        "aspect_ratio": args.aspect_ratio,
        "tts_mode": "fabric" if use_fabric_tts else "elevenlabs",
        "voice_id": args.voice_id or ELEVENLABS_DEFAULT_VOICE,
        "avatar_source": "provided" if args.avatar_image else "generated",
        "reference_video": args.reference_video or None,
        "voiceover_path": vo_path,
        "avatar_path": avatar_path,
        "fabric_path": fabric_path,
        "final_path": final_path,
    }
    meta_path = os.path.join(output_dir, "metadata.json")
    with open(meta_path, "w") as f:
        json.dump(metadata, f, indent=2)

    # =====================================================================
    # Stage 6: Upload
    # =====================================================================
    if args.drive_folder:
        print(f"\n{'='*40}\nSTAGE 6: Google Drive Upload\n{'='*40}")
        upload_to_drive(output_dir, args.drive_folder, args.brand)

    # =====================================================================
    # Summary
    # =====================================================================
    print("\n" + "=" * 60)
    print("ORCHESTRATOR COMPLETE")
    print("=" * 60)
    print(f"  Script: {len(script_text)} chars")
    print(f"  Voiceover: {vo_path or 'Fabric TTS'}")
    print(f"  Avatar: {avatar_path}")
    print(f"  Fabric video: {fabric_path}")
    print(f"  Final video: {final_path}")
    print(f"  Output dir: {output_dir}")


if __name__ == "__main__":
    main()
