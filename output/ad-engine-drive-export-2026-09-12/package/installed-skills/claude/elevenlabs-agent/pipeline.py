#!/usr/bin/env python3
"""
ElevenLabs Agent Pipeline
==========================
Voice cloning, registry management, script segmentation, and TTS generation.

Usage:
    # Clone a voice from reference
    python3 pipeline.py clone --reference ./ref.mp4 --name "my-voice" --brand motilli

    # Generate voiceover
    python3 pipeline.py generate --script "Hello world" --voice "my-voice" --output-dir ./output

    # List registered voices
    python3 pipeline.py list

    # Sync registry with ElevenLabs account
    python3 pipeline.py sync
"""

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime, timezone

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
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")
ELEVENLABS_BASE_URL = "https://api.elevenlabs.io/v1"
ELEVENLABS_TTS_URL = f"{ELEVENLABS_BASE_URL}/text-to-speech"
ELEVENLABS_VOICES_URL = f"{ELEVENLABS_BASE_URL}/voices"
ELEVENLABS_ADD_VOICE_URL = f"{ELEVENLABS_BASE_URL}/voices/add"
ELEVENLABS_MODEL = "eleven_multilingual_v2"

REGISTRY_PATH = os.path.expanduser("~/Documents/marketing brain/voice-registry.json")

# Default ElevenLabs voices
DEFAULT_VOICES = {
    "rachel": "21m00Tcm4TlvDq8ikWAM",
    "drew": "29vD33N1CtxCmqQRPOHJ",
    "clyde": "2EiwWnXFnvU5JabPnv8n",
    "domi": "AZnzlk1XvdvUeBnXmlld",
}

VIDEO_EXTENSIONS = {".mp4", ".mov", ".webm", ".mkv", ".avi", ".flv"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac"}

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
def log(stage, msg):
    prefix = f"[{stage}]"
    print(f"{prefix} {msg}")

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)
    return path

# ---------------------------------------------------------------------------
# Voice Registry
# ---------------------------------------------------------------------------
def load_registry():
    """Load or initialize the voice registry."""
    if os.path.exists(REGISTRY_PATH):
        with open(REGISTRY_PATH) as f:
            return json.load(f)
    return {"voices": {}, "default_voices": DEFAULT_VOICES}

def save_registry(registry):
    """Save the voice registry to disk."""
    ensure_dir(os.path.dirname(REGISTRY_PATH))
    with open(REGISTRY_PATH, "w") as f:
        json.dump(registry, f, indent=2)
    log("Registry", f"Saved to {REGISTRY_PATH}")

def register_voice(name, voice_id, description="", source_files=None, brand="", tags=None):
    """Add a cloned voice to the registry."""
    registry = load_registry()
    registry["voices"][name] = {
        "voice_id": voice_id,
        "name": name,
        "description": description,
        "source_files": source_files or [],
        "cloned_at": datetime.now(timezone.utc).isoformat(),
        "brand": brand,
        "tags": tags or [],
    }
    save_registry(registry)
    log("Registry", f"Registered voice '{name}' → {voice_id}")
    return voice_id

def get_voice_id(name_or_id):
    """Resolve a voice name to its ID. Accepts registry name, default name, or raw voice ID."""
    registry = load_registry()

    # Check custom voices first
    if name_or_id in registry.get("voices", {}):
        return registry["voices"][name_or_id]["voice_id"]

    # Check default voices
    defaults = registry.get("default_voices", DEFAULT_VOICES)
    if name_or_id.lower() in defaults:
        return defaults[name_or_id.lower()]

    # Assume it's a raw voice ID
    return name_or_id

def list_voices():
    """Print all registered voices."""
    registry = load_registry()

    print("\n=== Cloned Voices ===")
    voices = registry.get("voices", {})
    if not voices:
        print("  (none)")
    for name, info in voices.items():
        brand = f" [{info.get('brand', '')}]" if info.get("brand") else ""
        tags = f" tags={info.get('tags', [])}" if info.get("tags") else ""
        print(f"  {name}: {info['voice_id']}{brand}{tags}")
        if info.get("description"):
            print(f"    {info['description']}")
        print(f"    cloned: {info.get('cloned_at', 'unknown')}")
        if info.get("source_files"):
            print(f"    sources: {', '.join(info['source_files'])}")

    print("\n=== Default Voices ===")
    for name, vid in registry.get("default_voices", DEFAULT_VOICES).items():
        print(f"  {name}: {vid}")
    print()

# ---------------------------------------------------------------------------
# Audio Extraction (FFmpeg)
# ---------------------------------------------------------------------------
def extract_audio_from_video(video_path, output_dir=None):
    """Extract audio from a video file using FFmpeg."""
    video_path = Path(video_path)
    if not video_path.exists():
        raise FileNotFoundError(f"Video not found: {video_path}")

    out_dir = output_dir or str(video_path.parent)
    ensure_dir(out_dir)
    audio_path = os.path.join(out_dir, f"{video_path.stem}_extracted.mp3")

    if os.path.exists(audio_path):
        log("Extract", f"Audio already extracted: {audio_path}")
        return audio_path

    log("Extract", f"Extracting audio from {video_path.name}...")

    cmd = [
        "ffmpeg", "-i", str(video_path),
        "-vn",                    # no video
        "-acodec", "libmp3lame",  # MP3 codec
        "-ab", "192k",            # 192kbps bitrate
        "-ar", "44100",           # 44.1kHz sample rate
        "-y",                     # overwrite
        audio_path,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        log("Extract", f"FFmpeg error: {result.stderr[:500]}")
        raise RuntimeError(f"FFmpeg failed: {result.stderr[:200]}")

    size_kb = os.path.getsize(audio_path) / 1024
    log("Extract", f"Extracted: {audio_path} ({size_kb:.0f}KB)")
    return audio_path

# ---------------------------------------------------------------------------
# Voice Cloning
# ---------------------------------------------------------------------------
def clone_voice(reference_files, name, description="", brand="", tags=None, remove_noise=False):
    """Clone a voice from reference audio/video files via ElevenLabs IVC."""
    if not ELEVENLABS_API_KEY:
        raise RuntimeError("ELEVENLABS_API_KEY not set in .env")

    # Check if already registered
    registry = load_registry()
    if name in registry.get("voices", {}):
        existing = registry["voices"][name]
        log("Clone", f"Voice '{name}' already registered → {existing['voice_id']}")
        return existing["voice_id"]

    # Process reference files — extract audio from videos
    audio_files = []
    source_names = []
    tmp_dir = ensure_dir("/tmp/elevenlabs-agent-extract")

    for ref in reference_files:
        ref_path = Path(ref)
        source_names.append(ref_path.name)

        if ref_path.suffix.lower() in VIDEO_EXTENSIONS:
            audio_path = extract_audio_from_video(ref, tmp_dir)
            audio_files.append(audio_path)
        elif ref_path.suffix.lower() in AUDIO_EXTENSIONS:
            audio_files.append(str(ref_path))
        else:
            log("Clone", f"Skipping unsupported file: {ref_path.name}")

    if not audio_files:
        raise RuntimeError("No valid audio/video files provided for cloning")

    # Upload to ElevenLabs
    log("Clone", f"Cloning voice '{name}' from {len(audio_files)} sample(s)...")

    headers = {"xi-api-key": ELEVENLABS_API_KEY}

    # Build multipart form
    files_list = []
    for af in audio_files:
        files_list.append(("files", (os.path.basename(af), open(af, "rb"), "audio/mpeg")))

    data = {"name": name}
    if description:
        data["description"] = description
    if remove_noise:
        data["remove_background_noise"] = "true"

    try:
        resp = requests.post(
            ELEVENLABS_ADD_VOICE_URL,
            headers=headers,
            data=data,
            files=files_list,
            timeout=120,
        )

        # Close file handles
        for _field, value in files_list:
            try:
                value[1].close()
            except Exception:
                pass

        if resp.status_code == 200:
            result = resp.json()
            voice_id = result.get("voice_id")
            log("Clone", f"Voice cloned successfully! voice_id={voice_id}")

            # Register in local registry
            register_voice(
                name=name,
                voice_id=voice_id,
                description=description,
                source_files=source_names,
                brand=brand,
                tags=tags or [],
            )
            return voice_id
        else:
            log("Clone", f"ElevenLabs error: HTTP {resp.status_code} — {resp.text[:300]}")
            raise RuntimeError(f"Voice cloning failed: {resp.status_code}")

    except requests.exceptions.Timeout:
        raise RuntimeError("Voice cloning timed out (120s)")

# ---------------------------------------------------------------------------
# Script Segmentation
# ---------------------------------------------------------------------------
def segment_script(script_text, mode="none"):
    """Break a script into segments based on the chosen mode."""
    if mode == "none":
        return [{"index": 1, "text": script_text.strip()}]

    if mode == "lines":
        lines = [l.strip() for l in script_text.strip().split("\n") if l.strip()]
        return [{"index": i + 1, "text": line} for i, line in enumerate(lines)]

    if mode == "paragraphs":
        paragraphs = [p.strip() for p in script_text.strip().split("\n\n") if p.strip()]
        return [{"index": i + 1, "text": para} for i, para in enumerate(paragraphs)]

    if mode == "scenes":
        import re
        # Split on scene markers: [Scene N], ## Scene, ---, ===
        parts = re.split(r'(?:\[Scene\s*\d*\]|##\s*Scene\s*\d*|^-{3,}$|^={3,}$)', script_text, flags=re.MULTILINE)
        scenes = [p.strip() for p in parts if p.strip()]
        return [{"index": i + 1, "text": scene} for i, scene in enumerate(scenes)]

    # Fallback
    return [{"index": 1, "text": script_text.strip()}]

# ---------------------------------------------------------------------------
# TTS Generation
# ---------------------------------------------------------------------------
def generate_voiceover(script_text, voice_name_or_id, output_dir, segment_mode="none",
                       stability=0.5, similarity=0.75, style=0.3, speaker_boost=True):
    """Generate voiceover audio from script using ElevenLabs TTS."""
    if not ELEVENLABS_API_KEY:
        raise RuntimeError("ELEVENLABS_API_KEY not set in .env")

    vo_dir = ensure_dir(output_dir)
    voice_id = get_voice_id(voice_name_or_id)

    segments = segment_script(script_text, segment_mode)
    log("TTS", f"Generating {len(segments)} segment(s) with voice {voice_id}...")

    results = []
    total_size = 0

    for seg in segments:
        if len(segments) == 1:
            filename = "voiceover.mp3"
        else:
            filename = f"segment_{seg['index']:03d}.mp3"

        out_path = os.path.join(vo_dir, filename)

        # Skip if already exists
        if os.path.exists(out_path):
            log("TTS", f"  Segment {seg['index']} already exists: {out_path}")
            results.append({**seg, "file": filename, "path": out_path})
            continue

        url = f"{ELEVENLABS_TTS_URL}/{voice_id}"
        payload = {
            "text": seg["text"],
            "model_id": ELEVENLABS_MODEL,
            "voice_settings": {
                "stability": stability,
                "similarity_boost": similarity,
                "style": style,
                "use_speaker_boost": speaker_boost,
            },
        }
        headers = {
            "xi-api-key": ELEVENLABS_API_KEY,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        }

        success = False
        for attempt in range(3):
            try:
                resp = requests.post(url, headers=headers, json=payload, timeout=120)

                if resp.status_code == 200:
                    with open(out_path, "wb") as f:
                        f.write(resp.content)
                    size_kb = len(resp.content) / 1024
                    total_size += len(resp.content)
                    log("TTS", f"  Segment {seg['index']}: {filename} ({size_kb:.0f}KB)")
                    results.append({**seg, "file": filename, "path": out_path})
                    success = True
                    break
                else:
                    log("TTS", f"  Attempt {attempt + 1}: HTTP {resp.status_code} — {resp.text[:200]}")
            except Exception as e:
                log("TTS", f"  Attempt {attempt + 1} error: {e}")

            time.sleep(5)

        if not success:
            log("TTS", f"  FAILED segment {seg['index']} after 3 attempts")

    # Write manifest
    manifest = {
        "segments": [
            {"index": r["index"], "text": r["text"], "file": r["file"]}
            for r in results
        ],
        "total_segments": len(results),
        "voice_id": voice_id,
        "voice_name": voice_name_or_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "output_dir": output_dir,
    }

    manifest_path = os.path.join(vo_dir, "segments.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    total_mb = total_size / 1024 / 1024
    log("TTS", f"Done! {len(results)} segment(s), {total_mb:.1f}MB total")
    log("TTS", f"Manifest: {manifest_path}")

    return manifest

# ---------------------------------------------------------------------------
# Sync with ElevenLabs
# ---------------------------------------------------------------------------
def sync_voices():
    """Sync local registry with ElevenLabs account voices."""
    if not ELEVENLABS_API_KEY:
        raise RuntimeError("ELEVENLABS_API_KEY not set in .env")

    log("Sync", "Fetching voices from ElevenLabs...")
    headers = {"xi-api-key": ELEVENLABS_API_KEY}

    resp = requests.get(
        ELEVENLABS_VOICES_URL,
        headers=headers,
        params={"show_legacy": "false"},
        timeout=30,
    )

    if resp.status_code != 200:
        raise RuntimeError(f"Failed to fetch voices: {resp.status_code}")

    data = resp.json()
    remote_voices = data.get("voices", [])

    registry = load_registry()
    added = 0

    for rv in remote_voices:
        vid = rv.get("voice_id")
        name = rv.get("name", "")
        category = rv.get("category", "")

        # Only sync cloned voices that aren't already in registry
        if category == "cloned":
            # Check if this voice_id is already registered
            already = any(
                v.get("voice_id") == vid
                for v in registry.get("voices", {}).values()
            )
            if not already:
                safe_name = name.lower().replace(" ", "-").replace("_", "-")
                registry.setdefault("voices", {})[safe_name] = {
                    "voice_id": vid,
                    "name": name,
                    "description": rv.get("description", ""),
                    "source_files": [],
                    "cloned_at": datetime.now(timezone.utc).isoformat(),
                    "brand": "",
                    "tags": list(rv.get("labels", {}).values()),
                    "synced_from_remote": True,
                }
                added += 1
                log("Sync", f"  Added: {name} → {vid}")

    save_registry(registry)
    log("Sync", f"Sync complete. {added} new voice(s) added, {len(remote_voices)} total on account.")

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="ElevenLabs Agent — Voice Cloning & TTS")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # --- clone ---
    clone_parser = subparsers.add_parser("clone", help="Clone a voice from reference files")
    clone_parser.add_argument("--reference", nargs="+", required=True, help="Audio/video reference files")
    clone_parser.add_argument("--name", required=True, help="Name for the cloned voice")
    clone_parser.add_argument("--description", default="", help="Voice description")
    clone_parser.add_argument("--brand", default="", help="Brand association")
    clone_parser.add_argument("--tags", nargs="*", default=[], help="Tags for the voice")
    clone_parser.add_argument("--remove-noise", action="store_true", help="Remove background noise")

    # --- generate ---
    gen_parser = subparsers.add_parser("generate", help="Generate voiceover from script")
    gen_parser.add_argument("--script", help="Script text (inline)")
    gen_parser.add_argument("--script-file", help="Path to script text file")
    gen_parser.add_argument("--voice", help="Voice name from registry")
    gen_parser.add_argument("--voice-id", help="Raw ElevenLabs voice ID")
    gen_parser.add_argument("--output-dir", required=True, help="Output directory")
    gen_parser.add_argument("--segment-by", choices=["lines", "paragraphs", "scenes", "none"], default="none")
    gen_parser.add_argument("--stability", type=float, default=0.5)
    gen_parser.add_argument("--similarity", type=float, default=0.75)
    gen_parser.add_argument("--style", type=float, default=0.3)
    gen_parser.add_argument("--no-speaker-boost", action="store_true")

    # --- list ---
    subparsers.add_parser("list", help="List all registered voices")

    # --- sync ---
    subparsers.add_parser("sync", help="Sync registry with ElevenLabs account")

    args = parser.parse_args()

    if args.command == "clone":
        voice_id = clone_voice(
            reference_files=args.reference,
            name=args.name,
            description=args.description,
            brand=args.brand,
            tags=args.tags,
            remove_noise=args.remove_noise,
        )
        print(f"\nVoice cloned: {args.name} → {voice_id}")

    elif args.command == "generate":
        script_text = args.script
        if args.script_file:
            with open(args.script_file) as f:
                script_text = f.read()
        if not script_text:
            print("Error: provide --script or --script-file")
            sys.exit(1)

        voice = args.voice or args.voice_id
        if not voice:
            print("Error: provide --voice (registry name) or --voice-id (raw ID)")
            sys.exit(1)

        manifest = generate_voiceover(
            script_text=script_text,
            voice_name_or_id=voice,
            output_dir=args.output_dir,
            segment_mode=args.segment_by,
            stability=args.stability,
            similarity=args.similarity,
            style=args.style,
            speaker_boost=not args.no_speaker_boost,
        )
        print(f"\nGenerated {manifest['total_segments']} segment(s) → {args.output_dir}")

    elif args.command == "list":
        list_voices()

    elif args.command == "sync":
        sync_voices()

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
