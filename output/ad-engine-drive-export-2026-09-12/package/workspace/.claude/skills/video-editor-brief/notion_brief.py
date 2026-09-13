#!/usr/bin/env python3
"""
Notion Brief Publisher
======================
Takes video-editor-brief matching data + replicator output and creates a
Notion database entry with script lines paired with scene images.

Each brief page contains alternating text/image blocks:
  - Text: script line (with segment number)
  - Image: corresponding brand-adapted still from generated/

Usage:
    python3 notion_brief.py \
        --replicator-dir "./replicator-output" \
        --matches "./replicator-output/matches.json" \
        --script "./script.txt" \
        --brand "Motilli" \
        --title "GLP-1 Claymation Ad" \
        --database-id "abc123" \
        --angle "Metabolism Angle" \
        --format "Claymation"

    # Or called programmatically from brief_generator.py
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    print("[!] Missing requests. Run: pip install requests")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "[REDACTED_SECRET]")
NOTION_API_VERSION = "2022-06-28"
NOTION_BASE = "https://api.notion.com/v1"

# Default parent page for all briefs
# https://www.notion.so/Briefs-334c96bf99828053b6b6f47e5897590b
DEFAULT_BRIEFS_PAGE_ID = "334c96bf-9982-8053-b6b6-f47e5897590b"

# Google Drive OAuth2 (reuses replicator's token for image hosting)
GDRIVE_CLIENT_ID = "630165550470-bk00miojfehkb5va5hdoupbn170lurhh.apps.googleusercontent.com"
GDRIVE_CLIENT_SECRET = "[REDACTED_SECRET]"
GDRIVE_TOKEN_PATH = os.path.expanduser(
    "~/.claude/skills/video-scene-replicator/gdrive_token.json"
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def log(stage, msg):
    print(f"[{stage}] {msg}")


def notion_headers():
    return {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_API_VERSION,
    }


def notion_request(method, endpoint, payload=None):
    """Make a Notion API request with error handling."""
    url = f"{NOTION_BASE}/{endpoint}"
    resp = getattr(requests, method)(url, headers=notion_headers(), json=payload)
    if resp.status_code >= 400:
        log("Notion", f"ERROR {resp.status_code}: {resp.text[:500]}")
        return None
    return resp.json()


# ---------------------------------------------------------------------------
# Google Drive: Upload images and get shareable links
# ---------------------------------------------------------------------------

def get_gdrive_service():
    """Get authenticated Google Drive service using replicator's OAuth2 token."""
    try:
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build
    except ImportError:
        log("Drive", "Google API packages not installed. Run: pip install google-auth google-auth-oauthlib google-api-python-client")
        return None

    SCOPES = ["https://www.googleapis.com/auth/drive.file"]

    creds = None
    if os.path.exists(GDRIVE_TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(GDRIVE_TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(GDRIVE_TOKEN_PATH, "w") as token:
                token.write(creds.to_json())
        else:
            log("Drive", "No valid Drive token. Run video-scene-replicator first to authenticate.")
            return None

    return build("drive", "v3", credentials=creds)


def upload_image_to_drive(service, file_path, folder_id=None):
    """Upload an image to Google Drive and return a shareable link."""
    from googleapiclient.http import MediaFileUpload

    filename = os.path.basename(file_path)
    file_metadata = {"name": filename}
    if folder_id:
        file_metadata["parents"] = [folder_id]

    media = MediaFileUpload(file_path, mimetype="image/png", resumable=True)
    uploaded = service.files().create(
        body=file_metadata, media_body=media, fields="id,webContentLink"
    ).execute()

    file_id = uploaded.get("id")

    # Make it publicly viewable
    service.permissions().create(
        fileId=file_id,
        body={"role": "reader", "type": "anyone"},
    ).execute()

    # Direct download link
    direct_url = f"https://drive.google.com/uc?export=view&id={file_id}"
    log("Drive", f"Uploaded {filename} -> {direct_url}")
    return direct_url


# ---------------------------------------------------------------------------
# Notion: File Upload API (alternative to Google Drive)
# ---------------------------------------------------------------------------

def upload_image_to_notion(file_path):
    """Upload a local image via Notion File Upload API and return the file_upload id."""
    url = f"{NOTION_BASE}/file-uploads"
    filename = os.path.basename(file_path)

    # Step 1: Create file upload object
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": NOTION_API_VERSION,
    }

    # Multipart upload
    with open(file_path, "rb") as f:
        resp = requests.post(
            url,
            headers=headers,
            files={"file": (filename, f, "image/png")},
        )

    if resp.status_code >= 400:
        log("Notion", f"File upload failed ({resp.status_code}): {resp.text[:300]}")
        return None

    data = resp.json()
    file_upload_id = data.get("id")
    log("Notion", f"Uploaded {filename} -> file_upload:{file_upload_id}")
    return file_upload_id


# ---------------------------------------------------------------------------
# Notion: Create database entry with brief content
# ---------------------------------------------------------------------------

def create_brief_page(
    parent_page_id,
    title,
    brand,
    date_str,
    angle,
    format_type,
    scene_count,
    script_text,
    segment_image_pairs,
    image_mode="gdrive",
):
    """Create a Notion child page under the Briefs page with script lines + scene images.

    segment_image_pairs: list of dicts with:
        - segment_number: int
        - segment_text: str
        - image_url: str (if gdrive mode) or image_upload_id: str (if notion mode)
        - scene_number: int
        - confidence: str
        - editor_notes: str
    """
    log("Notion", f"Creating brief page: {title}")

    # --- Page properties (child pages only support title) ---
    properties = {
        "title": {"title": [{"text": {"content": title}}]},
    }

    # --- Build page body (children blocks) ---
    children = []

    # Metadata block (replaces database properties since we're using page parent)
    meta_parts = []
    if brand:
        meta_parts.append(f"Brand: {brand}")
    meta_parts.append(f"Date: {date_str}")
    if angle:
        meta_parts.append(f"Angle: {angle}")
    if format_type:
        meta_parts.append(f"Format: {format_type}")
    meta_parts.append(f"Scenes: {scene_count}")
    meta_parts.append("Status: In Review")

    children.append({
        "object": "block",
        "type": "callout",
        "callout": {
            "rich_text": [
                {"type": "text", "text": {"content": " | ".join(meta_parts)}},
            ],
            "icon": {"emoji": "📋"},
        },
    })

    if script_text:
        truncated = script_text[:2000]
        children.append({
            "object": "block",
            "type": "toggle",
            "toggle": {
                "rich_text": [{"type": "text", "text": {"content": "Full Script"}, "annotations": {"bold": True}}],
                "children": [{
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": truncated}}]
                    },
                }],
            },
        })

    children.append({
        "object": "block",
        "type": "divider",
        "divider": {},
    })

    # --- Script line + image pairs ---
    for pair in segment_image_pairs:
        seg_num = pair["segment_number"]
        seg_text = pair["segment_text"]
        confidence = pair.get("confidence", "")
        editor_notes = pair.get("editor_notes", "")
        scene_num = pair.get("scene_number", "?")

        # Script line as callout block
        children.append({
            "object": "block",
            "type": "callout",
            "callout": {
                "rich_text": [
                    {"type": "text", "text": {"content": f"[{seg_num}] "}, "annotations": {"bold": True}},
                    {"type": "text", "text": {"content": seg_text}},
                ],
                "icon": {"emoji": "🎬"},
            },
        })

        # Image block
        image_url = pair.get("image_url")
        image_upload_id = pair.get("image_upload_id")

        if image_mode == "gdrive" and image_url:
            children.append({
                "object": "block",
                "type": "image",
                "image": {
                    "type": "external",
                    "external": {"url": image_url},
                },
            })
        elif image_mode == "notion" and image_upload_id:
            children.append({
                "object": "block",
                "type": "image",
                "image": {
                    "type": "file_upload",
                    "file_upload": {"id": image_upload_id},
                },
            })

        # Editor notes as small text
        if editor_notes:
            children.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {"type": "text", "text": {"content": f"Scene {scene_num} | {confidence} confidence | "}, "annotations": {"italic": True, "color": "gray"}},
                        {"type": "text", "text": {"content": editor_notes}, "annotations": {"italic": True, "color": "gray"}},
                    ]
                },
            })

        # Divider between segments
        children.append({
            "object": "block",
            "type": "divider",
            "divider": {},
        })

    # Notion API limits children to 100 blocks per request
    # Split into batches if needed
    first_batch = children[:100]
    remaining = children[100:]

    # Create page as child of the Briefs page
    payload = {
        "parent": {"page_id": parent_page_id},
        "properties": properties,
        "children": first_batch,
    }

    result = notion_request("post", "pages", payload)
    if not result:
        log("Notion", "ERROR: Failed to create page")
        return None

    page_id = result.get("id")
    page_url = result.get("url", "")
    log("Notion", f"Page created: {page_url}")

    # Append remaining blocks in batches of 100
    while remaining:
        batch = remaining[:100]
        remaining = remaining[100:]
        append_payload = {"children": batch}
        append_result = notion_request("patch", f"blocks/{page_id}/children", append_payload)
        if not append_result:
            log("Notion", "WARNING: Failed to append some blocks")

    return {"page_id": page_id, "page_url": page_url}


# ---------------------------------------------------------------------------
# Main pipeline: Build pairs and publish
# ---------------------------------------------------------------------------

def publish_to_notion(
    replicator_dir,
    matches,
    script_segments,
    scenes,
    parent_page_id=None,
    brand="",
    title="Video Ad",
    angle="",
    format_type="",
    drive_folder_id=None,
    database_id=None,  # Legacy compat — ignored, use parent_page_id
):
    """Full pipeline: upload images -> create Notion child page with paired content."""
    if not parent_page_id:
        parent_page_id = DEFAULT_BRIEFS_PAGE_ID

    date_str = datetime.now().strftime("%Y-%m-%d")

    # Build scene lookup
    scene_map = {s["scene_number"]: s for s in scenes}

    # Filter to segment matches (exclude unmatched_scenes entry)
    segment_matches = [m for m in matches if "segment_number" in m]

    # --- Upload images ---
    log("Upload", f"Uploading {len(segment_matches)} scene images...")

    # Try Google Drive first (more reliable for Notion external images)
    gdrive_service = get_gdrive_service()
    image_mode = "gdrive" if gdrive_service else "notion"

    segment_image_pairs = []
    for m in segment_matches:
        scene_num = m.get("matched_scene", 0)
        scene = scene_map.get(scene_num, {})

        # Find the brand-adapted still
        gen_file = scene.get("generated_file")
        if gen_file:
            img_path = os.path.join(replicator_dir, "generated", gen_file)
        else:
            # Fallback to original keyframe
            kf_file = scene.get("keyframe_file")
            if kf_file:
                img_path = os.path.join(replicator_dir, "scenes", kf_file)
            else:
                img_path = None

        pair = {
            "segment_number": m["segment_number"],
            "segment_text": m.get("segment_text", ""),
            "scene_number": scene_num,
            "confidence": m.get("confidence", ""),
            "editor_notes": m.get("editor_notes", ""),
        }

        if img_path and os.path.exists(img_path):
            if image_mode == "gdrive":
                url = upload_image_to_drive(gdrive_service, img_path, drive_folder_id)
                pair["image_url"] = url
                time.sleep(0.3)  # Rate limit
            else:
                upload_id = upload_image_to_notion(img_path)
                pair["image_upload_id"] = upload_id
                time.sleep(0.5)
        else:
            log("Upload", f"WARNING: No image for scene {scene_num}")

        segment_image_pairs.append(pair)

    # --- Create Notion page ---
    full_script = "\n".join(script_segments)
    result = create_brief_page(
        parent_page_id=parent_page_id,
        title=f"{brand} — {title}" if brand else title,
        brand=brand,
        date_str=date_str,
        angle=angle,
        format_type=format_type,
        scene_count=len(scenes),
        script_text=full_script,
        segment_image_pairs=segment_image_pairs,
        image_mode=image_mode,
    )

    if result:
        log("Done", f"Brief published to Notion: {result['page_url']}")
    return result


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Notion Brief Publisher")
    parser.add_argument("--replicator-dir", required=True, help="Path to replicator output")
    parser.add_argument("--matches", required=True, help="Path to matches JSON from brief_generator")
    parser.add_argument("--script", default="", help="Path to script file")
    parser.add_argument("--script-text", default="", help="Inline script text")
    parser.add_argument("--brand", default="", help="Brand name")
    parser.add_argument("--title", default="Video Ad", help="Video title")
    parser.add_argument("--page-id", default=DEFAULT_BRIEFS_PAGE_ID, help="Notion parent page ID (default: Briefs page)")
    parser.add_argument("--database-id", default="", help="[DEPRECATED] Use --page-id instead")
    parser.add_argument("--angle", default="", help="Creative angle")
    parser.add_argument("--format", default="", dest="format_type", help="Format type (UGC, Claymation, etc.)")
    parser.add_argument("--drive-folder", default="", help="Google Drive folder ID for image hosting")
    parser.add_argument("--notion-token", default="", help="Notion API token (overrides env)")

    args = parser.parse_args()

    global NOTION_TOKEN
    if args.notion_token:
        NOTION_TOKEN = args.notion_token
    if not NOTION_TOKEN:
        print("ERROR: Set NOTION_TOKEN env var or pass --notion-token")
        sys.exit(1)

    # Load script
    if args.script and os.path.exists(args.script):
        with open(args.script) as f:
            script_text = f.read()
    elif args.script_text:
        script_text = args.script_text
    else:
        print("ERROR: Provide --script or --script-text")
        sys.exit(1)

    # Load matches
    with open(args.matches) as f:
        matches = json.load(f)

    # Load scenes (reuse brief_generator's loader)
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from brief_generator import load_replicator_output, parse_script

    scenes = load_replicator_output(args.replicator_dir)
    script_segments = parse_script(script_text)

    result = publish_to_notion(
        replicator_dir=args.replicator_dir,
        matches=matches,
        script_segments=script_segments,
        scenes=scenes,
        parent_page_id=args.page_id,
        brand=args.brand,
        title=args.title,
        angle=args.angle,
        format_type=args.format_type,
        drive_folder_id=args.drive_folder or None,
    )

    if result:
        print(f"\nNotion brief URL: {result['page_url']}")
    else:
        print("\nFailed to publish to Notion.")
        sys.exit(1)


if __name__ == "__main__":
    main()
