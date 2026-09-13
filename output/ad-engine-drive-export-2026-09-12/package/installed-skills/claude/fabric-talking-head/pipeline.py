#!/usr/bin/env python3
"""
Fabric Talking Head Generator
===============================
Creates AI talking head videos using VEED Fabric 1.0 via fal.ai.
Takes a static avatar image + voiceover audio → lip-synced talking head video.

Usage:
    python3 pipeline.py \
        --image "/path/to/avatar.png" \
        --audio "/path/to/voiceover.mp3" \
        --resolution "720p" \
        --output-dir "./fabric-output"
"""

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime

try:
    import requests
except ImportError:
    print("[!] Missing: requests. Run: pip install requests")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

# Load from .env
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

FAL_API_KEY = os.environ.get("FAL_API_KEY", "")
FAL_BASE_URL = "https://fal.run/veed/fabric-1.0"
FAL_QUEUE_URL = "https://queue.fal.run/veed/fabric-1.0"
FAL_TEXT_URL = "https://fal.run/veed/fabric-1.0/text"

GDRIVE_CLIENT_ID = "630165550470-bk00miojfehkb5va5hdoupbn170lurhh.apps.googleusercontent.com"
GDRIVE_CLIENT_SECRET = "[REDACTED_SECRET]"
GDRIVE_TOKEN_PATH = os.path.expanduser("~/.claude/skills/fabric-talking-head/gdrive_token.json")

MAX_RETRIES = 3
POLL_INTERVAL = 10  # seconds

# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def log(stage, msg):
    prefix = f"[Stage {stage}]" if isinstance(stage, int) else f"[{stage}]"
    print(f"{prefix} {msg}")


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)
    return path


def get_fal_headers():
    return {
        "Authorization": f"Key {FAL_API_KEY}",
        "Content-Type": "application/json"
    }


# ---------------------------------------------------------------------------
# Stage 1: Upload assets to fal.ai storage
# ---------------------------------------------------------------------------

def upload_to_fal_storage(file_path):
    """Upload a local file to fal.ai storage and return the URL."""
    FAL_UPLOAD_URL = "https://fal.run/fal-ai/file-upload"

    # Determine MIME type
    ext = Path(file_path).suffix.lower()
    mime_map = {
        ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".webp": "image/webp", ".gif": "image/gif", ".avif": "image/avif",
        ".mp3": "audio/mpeg", ".wav": "audio/wav", ".ogg": "audio/ogg",
        ".m4a": "audio/mp4", ".aac": "audio/aac",
    }
    mime = mime_map.get(ext, "application/octet-stream")

    # Use fal.ai's file upload endpoint
    upload_url = "https://fal.ai/api/storage/upload"
    try:
        with open(file_path, "rb") as f:
            resp = requests.post(
                upload_url,
                headers={"Authorization": f"Key {FAL_API_KEY}"},
                files={"file": (os.path.basename(file_path), f, mime)},
                timeout=120,
            )

        if resp.status_code == 200:
            data = resp.json()
            url = data.get("url") or data.get("file_url")
            if url:
                return url

        # Fallback: try the REST upload
        resp2 = requests.put(
            f"https://fal.ai/api/storage/upload/public/{os.path.basename(file_path)}",
            headers={
                "Authorization": f"Key {FAL_API_KEY}",
                "Content-Type": mime,
            },
            data=open(file_path, "rb").read(),
            timeout=120,
        )
        if resp2.status_code == 200:
            data2 = resp2.json()
            return data2.get("url") or data2.get("file_url")

    except Exception as e:
        log(1, f"  Upload error: {e}")

    return None


def resolve_url(path_or_url):
    """If it's a URL, return as-is. If local file, upload to fal.ai storage."""
    if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
        return path_or_url

    if not os.path.exists(path_or_url):
        log(1, f"  File not found: {path_or_url}")
        return None

    log(1, f"Uploading {os.path.basename(path_or_url)} to fal.ai storage...")
    url = upload_to_fal_storage(path_or_url)
    if url:
        log(1, f"  Uploaded: {url[:80]}...")
    else:
        log(1, f"  Upload FAILED for {path_or_url}")
    return url


# ---------------------------------------------------------------------------
# Stage 2 & 3: Generate talking head video via Fabric 1.0
# ---------------------------------------------------------------------------

def generate_talking_head(image_url, audio_url=None, text=None, voice_description=None,
                          resolution="720p"):
    """Call VEED Fabric 1.0 API to generate talking head video."""
    headers = get_fal_headers()

    if text:
        # Text-to-video mode
        url = FAL_TEXT_URL
        payload = {
            "image_url": image_url,
            "text": text,
            "resolution": resolution,
        }
        if voice_description:
            payload["voice_description"] = voice_description
    else:
        # Image + audio mode (standard)
        url = FAL_BASE_URL
        payload = {
            "image_url": image_url,
            "audio_url": audio_url,
            "resolution": resolution,
        }

    log(2, f"Submitting to Fabric 1.0 ({'text' if text else 'audio'} mode, {resolution})...")

    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=7200)

            if resp.status_code == 200:
                data = resp.json()
                video_info = data.get("video", {})
                video_url = video_info.get("url")
                if video_url:
                    log(2, f"  Video generated: {video_url[:80]}...")
                    return {
                        "video_url": video_url,
                        "content_type": video_info.get("content_type", "video/mp4"),
                        "file_name": video_info.get("file_name", "fabric_output.mp4"),
                        "file_size": video_info.get("file_size", 0),
                    }
                else:
                    log(2, f"  No video URL in response: {data}")

            elif resp.status_code == 422:
                error_data = resp.json()
                log(2, f"  Validation error: {json.dumps(error_data.get('detail', []), indent=2)}")
                return None  # Don't retry validation errors

            else:
                log(2, f"  Attempt {attempt+1}: HTTP {resp.status_code} — {resp.text[:200]}")

        except requests.exceptions.Timeout:
            log(2, f"  Attempt {attempt+1}: Timeout (this is normal for long videos)")
        except Exception as e:
            log(2, f"  Attempt {attempt+1} error: {e}")

        if attempt < MAX_RETRIES - 1:
            wait = 10 * (attempt + 1)
            log(2, f"  Retrying in {wait}s...")
            time.sleep(wait)

    return None


def generate_talking_head_async(image_url, audio_url=None, text=None,
                                 voice_description=None, resolution="720p"):
    """Async/queue-based generation for longer videos."""
    headers = get_fal_headers()

    model_path = "veed/fabric-1.0/text" if text else "veed/fabric-1.0"
    queue_url = f"https://queue.fal.run/{model_path}"

    if text:
        payload = {"image_url": image_url, "text": text, "resolution": resolution}
        if voice_description:
            payload["voice_description"] = voice_description
    else:
        payload = {"image_url": image_url, "audio_url": audio_url, "resolution": resolution}

    log(2, f"Submitting async job to Fabric 1.0...")

    try:
        resp = requests.post(queue_url, headers=headers, json=payload, timeout=60)
        if resp.status_code != 200:
            log(2, f"  Queue submit failed: {resp.status_code} — {resp.text[:200]}")
            return None

        data = resp.json()
        request_id = data.get("request_id")
        if not request_id:
            log(2, f"  No request_id in response: {data}")
            return None

        log(2, f"  Job submitted: {request_id}")

        # Poll for completion
        status_url = f"https://queue.fal.run/{model_path}/requests/{request_id}/status"
        result_url = f"https://queue.fal.run/{model_path}/requests/{request_id}"

        max_wait = 7200  # 2 hours
        start = time.time()

        while time.time() - start < max_wait:
            try:
                status_resp = requests.get(status_url, headers=get_fal_headers(), timeout=30)
                if status_resp.status_code == 200:
                    status_data = status_resp.json()
                    status = status_data.get("status", "")

                    if status == "COMPLETED":
                        # Fetch result
                        result_resp = requests.get(result_url, headers=get_fal_headers(), timeout=60)
                        if result_resp.status_code == 200:
                            result_data = result_resp.json()
                            video_info = result_data.get("video", {})
                            return {
                                "video_url": video_info.get("url"),
                                "content_type": video_info.get("content_type", "video/mp4"),
                                "file_name": video_info.get("file_name", "fabric_output.mp4"),
                                "file_size": video_info.get("file_size", 0),
                            }

                    elif status == "FAILED":
                        log(2, f"  Job failed: {status_data}")
                        return None

                    else:
                        elapsed = int(time.time() - start)
                        log(2, f"  Status: {status} ({elapsed}s elapsed)")

            except Exception:
                pass

            time.sleep(POLL_INTERVAL)

        log(2, "  Job timed out after 2 hours")
        return None

    except Exception as e:
        log(2, f"  Error: {e}")
        return None


# ---------------------------------------------------------------------------
# Stage 4: Post-processing (FFmpeg)
# ---------------------------------------------------------------------------

def post_process(raw_video_path, output_dir, aspect_ratio=None, bg_music=None):
    """Optional post-processing: aspect ratio crop, background music, fade."""
    final_dir = ensure_dir(os.path.join(output_dir, "final"))

    ar_tag = aspect_ratio.replace(":", "x") if aspect_ratio else "original"
    final_path = os.path.join(final_dir, f"talking_head_{ar_tag}.mp4")

    if os.path.exists(final_path):
        log(4, f"Post-processed video already exists: {final_path}")
        return final_path

    # If no processing needed, just copy
    if not aspect_ratio and not bg_music:
        import shutil
        shutil.copy2(raw_video_path, final_path)
        return final_path

    cmd = ["ffmpeg", "-i", raw_video_path]
    filters = []

    # Aspect ratio cropping
    if aspect_ratio:
        ar_map = {
            "9:16": "crop=ih*9/16:ih",
            "1:1": "crop=min(iw\\,ih):min(iw\\,ih)",
            "16:9": "crop=iw:iw*9/16",
        }
        crop_filter = ar_map.get(aspect_ratio)
        if crop_filter:
            filters.append(crop_filter)

    # Build filter chain
    if filters:
        cmd.extend(["-vf", ",".join(filters)])

    if bg_music and os.path.exists(bg_music):
        cmd.extend(["-i", bg_music])
        # Mix original audio + background music at low volume
        cmd.extend([
            "-filter_complex",
            "[0:a]volume=1.0[orig];[1:a]volume=0.15[bg];[orig][bg]amix=inputs=2:duration=shortest[out]",
            "-map", "0:v", "-map", "[out]"
        ])
    else:
        cmd.extend(["-map", "0:v", "-map", "0:a"])

    cmd.extend([
        "-c:v", "libx264", "-crf", "18", "-preset", "medium",
        "-c:a", "aac", "-b:a", "192k",
        final_path, "-y"
    ])

    log(4, f"Post-processing: {' '.join(cmd[:5])}...")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

    if os.path.exists(final_path):
        log(4, f"  Saved: {final_path}")
        return final_path
    else:
        log(4, f"  FFmpeg error: {result.stderr[:300]}")
        # Fallback: return raw
        import shutil
        shutil.copy2(raw_video_path, final_path)
        return final_path


# ---------------------------------------------------------------------------
# Stage 5: Google Drive Upload
# ---------------------------------------------------------------------------

def get_drive_service():
    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build
    except ImportError:
        log(5, "Google Drive packages not installed.")
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


def upload_to_drive(output_dir, drive_folder_id, brand=""):
    from googleapiclient.http import MediaFileUpload

    service = get_drive_service()
    if not service:
        return

    date_str = datetime.now().strftime("%Y-%m-%d")
    folder_name = f"{brand + '_' if brand else ''}{date_str}_fabric"

    folder_metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [drive_folder_id]
    }
    folder = service.files().create(body=folder_metadata, fields="id").execute()
    parent_id = folder.get("id")

    upload_count = 0
    for subdir in ["raw", "final"]:
        dir_path = os.path.join(output_dir, subdir)
        if not os.path.exists(dir_path):
            continue
        for filename in sorted(os.listdir(dir_path)):
            filepath = os.path.join(dir_path, filename)
            if not os.path.isfile(filepath):
                continue
            mime = "video/mp4" if filepath.endswith(".mp4") else "application/octet-stream"
            file_metadata = {"name": filename, "parents": [parent_id]}
            media = MediaFileUpload(filepath, mimetype=mime, resumable=True)
            service.files().create(body=file_metadata, media_body=media, fields="id").execute()
            upload_count += 1
            log(5, f"  Uploaded: {filename}")

    # Upload metadata
    meta_path = os.path.join(output_dir, "metadata.json")
    if os.path.exists(meta_path):
        file_metadata = {"name": "metadata.json", "parents": [parent_id]}
        media = MediaFileUpload(meta_path, mimetype="application/json", resumable=True)
        service.files().create(body=file_metadata, media_body=media, fields="id").execute()
        upload_count += 1

    log(5, f"Uploaded {upload_count} files to Drive folder '{folder_name}'")


# ---------------------------------------------------------------------------
# Batch Mode: Process directory of audio segments
# ---------------------------------------------------------------------------

def process_batch(image_url, audio_dir, resolution, output_dir):
    """Process a directory of audio segments, generating one video per segment."""
    raw_dir = ensure_dir(os.path.join(output_dir, "raw"))
    results = []

    audio_files = sorted([
        f for f in os.listdir(audio_dir)
        if Path(f).suffix.lower() in (".mp3", ".wav", ".ogg", ".m4a", ".aac")
    ])

    log("B", f"Batch mode: {len(audio_files)} audio segments found")

    for i, audio_file in enumerate(audio_files):
        audio_path = os.path.join(audio_dir, audio_file)
        out_path = os.path.join(raw_dir, f"fabric_{i+1:03d}.mp4")

        if os.path.exists(out_path):
            log("B", f"  Segment {i+1} already exists — skipping")
            results.append({"segment": i+1, "video_path": out_path, "status": "cached"})
            continue

        log("B", f"  Processing segment {i+1}/{len(audio_files)}: {audio_file}")

        audio_url = resolve_url(audio_path)
        if not audio_url:
            results.append({"segment": i+1, "video_path": None, "status": "upload_failed"})
            continue

        result = generate_talking_head(image_url, audio_url=audio_url, resolution=resolution)

        if result and result.get("video_url"):
            vid_resp = requests.get(result["video_url"], timeout=300)
            with open(out_path, "wb") as f:
                f.write(vid_resp.content)
            log("B", f"    Saved: {out_path}")
            results.append({"segment": i+1, "video_path": out_path, "status": "success"})
        else:
            results.append({"segment": i+1, "video_path": None, "status": "failed"})

        time.sleep(2)

    succeeded = sum(1 for r in results if r["status"] in ("success", "cached"))
    log("B", f"Batch complete: {succeeded}/{len(audio_files)} segments")
    return results


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Fabric Talking Head Generator")
    parser.add_argument("--image", required=True, help="Avatar image (local path or URL)")
    parser.add_argument("--audio", default="", help="Voiceover audio (local path or URL)")
    parser.add_argument("--audio-dir", default="", help="Directory of audio segments (batch mode)")
    parser.add_argument("--text", default="", help="Text for TTS mode (instead of audio)")
    parser.add_argument("--voice-description", default="", help="Voice tone for TTS mode")
    parser.add_argument("--resolution", default="720p", choices=["480p", "720p"], help="Output resolution")
    parser.add_argument("--aspect-ratio", default="", help="Post-process aspect ratio (9:16, 1:1, 16:9)")
    parser.add_argument("--bg-music", default="", help="Background music path")
    parser.add_argument("--brand", default="", help="Brand name for file organization")
    parser.add_argument("--drive-folder", default="", help="Google Drive folder ID")
    parser.add_argument("--output-dir", default="./fabric-output", help="Output directory")
    parser.add_argument("--async-mode", action="store_true", help="Use async/queue API for long videos")

    args = parser.parse_args()

    if not FAL_API_KEY:
        print("ERROR: FAL_API_KEY not set. Add it to ~/Documents/marketing brain/.env")
        sys.exit(1)

    if not args.audio and not args.audio_dir and not args.text:
        print("ERROR: Provide --audio, --audio-dir, or --text")
        sys.exit(1)

    output_dir = args.output_dir
    ensure_dir(output_dir)
    raw_dir = ensure_dir(os.path.join(output_dir, "raw"))

    print("=" * 60)
    print("FABRIC TALKING HEAD GENERATOR")
    print(f"Image: {args.image}")
    print(f"Mode: {'text-to-speech' if args.text else 'batch' if args.audio_dir else 'audio'}")
    print(f"Resolution: {args.resolution}")
    print(f"Output: {output_dir}")
    print("=" * 60)

    # --- Stage 1: Upload assets ---
    print("\n[Stage 1] Uploading assets...")
    image_url = resolve_url(args.image)
    if not image_url:
        print("ERROR: Could not resolve image URL")
        sys.exit(1)

    # --- Stage 2 & 3: Generate ---
    if args.audio_dir:
        # Batch mode
        results = process_batch(image_url, args.audio_dir, args.resolution, output_dir)
        raw_path = None  # Multiple outputs
    else:
        audio_url = None
        if args.audio:
            audio_url = resolve_url(args.audio)
            if not audio_url:
                print("ERROR: Could not resolve audio URL")
                sys.exit(1)

        print(f"\n[Stage 2] Generating talking head video...")

        if args.async_mode:
            result = generate_talking_head_async(
                image_url, audio_url=audio_url,
                text=args.text if args.text else None,
                voice_description=args.voice_description if args.voice_description else None,
                resolution=args.resolution
            )
        else:
            result = generate_talking_head(
                image_url, audio_url=audio_url,
                text=args.text if args.text else None,
                voice_description=args.voice_description if args.voice_description else None,
                resolution=args.resolution
            )

        if not result or not result.get("video_url"):
            print("ERROR: Video generation failed")
            sys.exit(1)

        # Download
        raw_path = os.path.join(raw_dir, "fabric_001.mp4")
        log(3, f"Downloading video...")
        vid_resp = requests.get(result["video_url"], timeout=300)
        with open(raw_path, "wb") as f:
            f.write(vid_resp.content)
        log(3, f"  Saved: {raw_path} ({len(vid_resp.content) / 1024 / 1024:.1f}MB)")

    # --- Stage 4: Post-process ---
    final_path = None
    if raw_path and (args.aspect_ratio or args.bg_music):
        print(f"\n[Stage 4] Post-processing...")
        final_path = post_process(
            raw_path, output_dir,
            aspect_ratio=args.aspect_ratio if args.aspect_ratio else None,
            bg_music=args.bg_music if args.bg_music else None
        )
    elif raw_path:
        final_path = raw_path

    # --- Save metadata ---
    metadata = {
        "generated_at": datetime.now().isoformat(),
        "image": args.image,
        "audio": args.audio or args.text,
        "resolution": args.resolution,
        "aspect_ratio": args.aspect_ratio or "original",
        "brand": args.brand,
        "raw_path": raw_path,
        "final_path": final_path,
        "mode": "text" if args.text else "batch" if args.audio_dir else "audio",
    }
    meta_path = os.path.join(output_dir, "metadata.json")
    with open(meta_path, "w") as f:
        json.dump(metadata, f, indent=2)

    # --- Stage 5: Upload ---
    if args.drive_folder:
        print(f"\n[Stage 5] Uploading to Google Drive...")
        upload_to_drive(output_dir, args.drive_folder, args.brand)

    # --- Summary ---
    print("\n" + "=" * 60)
    print("GENERATION COMPLETE")
    print("=" * 60)
    if final_path:
        print(f"  Final video: {final_path}")
    if args.audio_dir:
        print(f"  Batch segments: {raw_dir}")
    print(f"  Output dir: {output_dir}")


if __name__ == "__main__":
    main()
