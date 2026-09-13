#!/usr/bin/env python3
"""
B-Roll Sourcer Pipeline
========================
Scans a video creative (AI UGC, talking head, etc.), identifies B-roll segments
(when the creator ISN'T talking), classifies each B-roll type, then either:
  - Sources matching real-world clips from TikTok (action/lifestyle B-roll)
  - Generates science/mechanism clips via Veo 3.1 (diagrams, cells, molecular)

Usage:
    python3 broll_sourcer.py \
        --video "/path/to/ugc_creative.mp4" \
        --brand "Motilli" \
        --output-dir "./broll-output" \
        --drive-folder "FOLDER_ID"
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Dependency check
# ---------------------------------------------------------------------------
try:
    from google import genai
    from google.genai import types
except ImportError:
    print("[!] Missing google-genai. Run: pip install google-genai")
    sys.exit(1)

try:
    import requests
except ImportError:
    print("[!] Missing requests. Run: pip install requests")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "[REDACTED_SECRET]")
GEMINI_VIDEO_MODEL = "gemini-3-flash-preview"
GEMINI_IMAGE_MODEL = "gemini-3.1-flash-image-preview"  # Nano Banana 2
VEO_MODEL = "veo-3.1-generate-preview"

KIE_API_KEY = os.environ.get("KIE_API_KEY", "ea55b909fc9fefcb6b964e468062f2c2")
KIE_CREATE_URL = "https://api.kie.ai/api/v1/jobs/createTask"
KIE_STATUS_URL = "https://api.kie.ai/api/v1/jobs/recordInfo"
KLING_POLL_INTERVAL = 15
MAX_KLING_RETRIES = 3
KIE_UPLOAD_URL = "https://kieai.redpandaai.co/api/file-stream-upload"

# Google Drive OAuth2 (reuses replicator's token)
GDRIVE_CLIENT_ID = "630165550470-bk00miojfehkb5va5hdoupbn170lurhh.apps.googleusercontent.com"
GDRIVE_CLIENT_SECRET = "[REDACTED_SECRET]"
GDRIVE_TOKEN_PATH = os.path.expanduser("~/.claude/skills/video-scene-replicator/gdrive_token.json")

VAULT_ROOT = os.path.expanduser("~/Documents/marketing brain")

# Brand registry (same as replicator — kept in sync)
BRAND_REGISTRY = {
    "motilli": {
        "research_docs": [
            os.path.join(VAULT_ROOT, "brands/motilli/copy/briefs/Motilli_Master_Copywriting_Brief.md"),
            os.path.join(VAULT_ROOT, "brands/motilli/copy/strategy/Motilli_Product_Context.md"),
            os.path.join(VAULT_ROOT, "brands/motilli/copy/strategy/Motilli_Avatar_VoC.md"),
        ],
        "product_images": [
            os.path.join(VAULT_ROOT, "brands/motilli/brand/website-assets/motilli product reference.png"),
        ],
        "default_product_context": "Celery juice fiber gummies for GLP-1 users — supports gut health during weight loss medication",
    },
    "lunessa": {
        "research_docs": [
            os.path.join(VAULT_ROOT, "brands/lunessa/research/fh research docs/Lunessa Research Docs 3.0/Lunessa Avatar Sheet.pdf"),
            os.path.join(VAULT_ROOT, "brands/lunessa/research/fh research docs/Lunessa Research Docs 3.0/Lunessa_Master_Copywriting_Brief.docx"),
            os.path.join(VAULT_ROOT, "brands/lunessa/research/menopause research 2.0/Lunessa_Master_Strategic_Brief.docx"),
        ],
        "product_images": [
            os.path.join(VAULT_ROOT, "brands/lunessa/brand/website assets/lunessa spelling corrected .jpg"),
        ],
        "default_product_context": "Heart health supplement for women — supports cholesterol, energy, and cardiovascular restoration",
    },
    "velantra": {
        "research_docs": [],
        "product_images": [],
        "default_product_context": "Velantra luxury travel bags — premium canvas and leather construction with gold/silver hardware",
    },
    "velantra-boat-tote": {
        "research_docs": [],
        "product_images": [
            os.path.join(VAULT_ROOT, "statics/product references/velantra/boat tote/01.jpg"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/boat tote/02.jpg"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/boat tote/03.jpg"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/boat tote/04.jpg"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/boat tote/05.jpg"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/boat tote/06.jpg"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/boat tote/navy blue .webp"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/boat tote/pink.webp"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/boat tote/dark green.webp"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/boat tote/olive green.webp"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/boat tote/orange.webp"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/boat tote/red.webp"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/boat tote/sunny yellow .webp"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/boat tote/yellow .webp"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/boat tote/colors/Emerald Green/07.png"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/boat tote/colors/Lady Pink/07.png"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/boat tote/colors/Light Grey/07.png"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/boat tote/colors/Lineman/07.png"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/boat tote/colors/Navy/07.jpg"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/boat tote/colors/Red/07.png"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/boat tote/colors/Solid Green/07.png"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/boat tote/colors/Solid Navy/07.png"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/boat tote/colors/Solid Olive Green/07.png"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/boat tote/colors/Solid Orange/07.png"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/boat tote/colors/Solid Pink/07.png"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/boat tote/colors/Solid Red/07.png"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/boat tote/colors/Solid Yellow/07.png"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/boat tote/colors/Sunny Yellow/07.png"),
        ],
        "default_product_context": "Velantra Boat Tote — premium canvas tote bag with colored leather trim straps, gold turn-lock clasp, Birkin-inspired silhouette. Structured rectangular body in natural canvas with contrast-color leather handles, front strap, and base. Available in navy, red, pink, dark green, olive green, orange, sunny yellow, yellow, emerald green, lady pink, light grey, lineman, and additional solid colorways (solid green, solid navy, solid olive green, solid orange, solid pink, solid red, solid yellow).",
    },
    "velantra-meridian": {
        "research_docs": [],
        "product_images": [
            os.path.join(VAULT_ROOT, "statics/product references/velantra/meridian/black 1.webp"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/meridian/black 2.webp"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/meridian/black 3.webp"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/meridian/brown 1.webp"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/meridian/brown 2.webp"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/meridian/brown 3.webp"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/meridian/coffee brow n1.webp"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/meridian/coffee brown 2.webp"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/meridian/gray 1.webp"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/meridian/gray 2.webp"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/meridian/white 1.webp"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/meridian/white 2.webp"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/meridian/green.webp"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/meridian/burgundy 1.webp"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/meridian/light blue 1.jpg"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/meridian/ultra light blue 1.webp"),
        ],
        "default_product_context": "Velantra Meridian — structured full-leather handbag with silver hardware, Birkin-inspired design. Clean lines, top handles, front flap with turn-lock clasp. Premium pebbled leather construction. Available in black, brown, coffee brown, gray, white, green, burgundy, light blue, and ultra light blue.",
    },
    "velantra-weekender": {
        "research_docs": [],
        "product_images": [
            os.path.join(VAULT_ROOT, "statics/product references/velantra/weekender/1.png"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/weekender/2.png"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/weekender/3.png"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/weekender/4.png"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/weekender/5.png"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/weekender/1 2.png"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/weekender/2 2.png"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/weekender/3 2.png"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/weekender/light chocolate 1.png"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/weekender/light chocolate 2.png"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/weekender/light chocolate 3.png"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/weekender/light chocolate 4.png"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/weekender/light chocolate 5.png"),
        ],
        "default_product_context": "Velantra Weekender — large travel bag with canvas body and cognac leather trim, corners, and handles. Birkin-inspired design with shoulder strap, turn-lock hardware, leather lock tab. Two-tone construction (canvas + leather). Available in olive/cognac and light chocolate/cream colorways.",
    },
}

# B-roll classification categories
BROLL_TYPES = {
    "creator_action": "The SAME person from the talking head segments performing an action (exercising, cooking, unboxing, walking, etc.) — NOT talking to camera, but clearly the same creator",
    "action_lifestyle": "A DIFFERENT person (not the creator) doing an action, stock-style lifestyle footage, generic hands, strangers",
    "product_shot": "Product close-up, unboxing, pouring, holding product, product on surface",
    "science_mechanism": "Diagrams, cells, molecular animations, gut lining, biological processes, medical imagery",
    "text_graphic": "Text overlay, infographic, stat callout, before/after graphic",
    "nature_abstract": "Nature footage, abstract visuals, flowing water, light effects",
    "testimonial_social": "Screenshots of reviews, social proof, comments, ratings",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def log(stage, msg):
    print(f"[{stage}] {msg}")


def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)
    return path


def load_brand_knowledge(brand_name):
    """Load research docs from the vault for the specified brand."""
    import zipfile
    import xml.etree.ElementTree as ET

    key = brand_name.lower().strip()
    registry = BRAND_REGISTRY.get(key)

    if not registry:
        log("Brand", f"No registry entry for '{brand_name}'")
        return {"context_text": "", "product_images": [], "default_product_context": ""}

    log("Brand", f"Loading knowledge for: {brand_name}")

    context_parts = []
    for doc_path in registry["research_docs"]:
        if not os.path.exists(doc_path):
            continue
        ext = Path(doc_path).suffix.lower()
        try:
            if ext == ".md":
                with open(doc_path, "r", encoding="utf-8") as f:
                    text = f.read()
                context_parts.append(f"--- {os.path.basename(doc_path)} ---\n{text}")
            elif ext == ".docx":
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
            elif ext == ".pdf":
                try:
                    from pdfminer.high_level import extract_text
                    text = extract_text(doc_path)
                    context_parts.append(f"--- {os.path.basename(doc_path)} ---\n{text}")
                except ImportError:
                    pass
        except Exception as e:
            log("Brand", f"  ERROR reading {os.path.basename(doc_path)}: {e}")

    full_context = "\n\n".join(context_parts)
    if len(full_context) > 30000:
        full_context = full_context[:30000] + "\n\n[... truncated ...]"

    valid_images = [p for p in registry.get("product_images", []) if os.path.exists(p)]
    log("Brand", f"Loaded {len(context_parts)} docs ({len(full_context)} chars), {len(valid_images)} product images")

    return {
        "context_text": full_context,
        "product_images": valid_images,
        "default_product_context": registry["default_product_context"],
    }


# ---------------------------------------------------------------------------
# Stage 1: Extract Frames & Detect Segments
# ---------------------------------------------------------------------------

def extract_video_info(video_path):
    """Get video metadata via ffprobe."""
    probe = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", video_path],
        capture_output=True, text=True
    )
    return json.loads(probe.stdout)


def extract_keyframes(video_path, output_dir, interval=1.0):
    """Extract frames at regular intervals for analysis."""
    frames_dir = ensure_dir(os.path.join(output_dir, "frames"))

    probe_data = extract_video_info(video_path)
    duration = float(probe_data["format"]["duration"])
    log("Extract", f"Video duration: {duration:.1f}s")

    # Extract frames every N seconds
    subprocess.run([
        "ffmpeg", "-y", "-i", video_path,
        "-vf", f"fps=1/{interval}",
        "-q:v", "2",
        os.path.join(frames_dir, "frame_%04d.png")
    ], capture_output=True)

    frames = sorted([
        os.path.join(frames_dir, f)
        for f in os.listdir(frames_dir)
        if f.endswith(".png")
    ])

    log("Extract", f"Extracted {len(frames)} frames at {interval}s intervals")
    return frames, duration


# ---------------------------------------------------------------------------
# Stage 2: Segment Analysis via Gemini
# ---------------------------------------------------------------------------

def analyze_video_segments(video_path, frames, duration, brand_knowledge, brand, output_dir):
    """Upload video to Gemini and identify talking vs B-roll segments."""
    client = genai.Client(api_key=GEMINI_API_KEY)
    analysis_dir = ensure_dir(os.path.join(output_dir, "analysis"))

    log("Analyze", "Uploading video to Gemini for full analysis...")

    video_bytes = open(video_path, "rb").read()

    brand_block = ""
    if brand_knowledge:
        brand_block = f"""

BRAND CONTEXT (use this to understand what product/mechanism the B-roll should relate to):
{brand_knowledge[:15000]}
"""

    prompt = f"""You are a video production analyst. Analyze this video creative frame by frame.

BRAND: {brand}
{brand_block}

YOUR TASK:
1. Watch the entire video carefully
2. Identify every segment where the creator/speaker IS talking on camera (talking head segments)
3. Identify every segment where B-roll is playing (the creator is NOT visible or is covered by overlay footage)
4. For each B-roll segment, classify its type from these categories:
   - "creator_action": The SAME person from the talking head segments performing an action (exercising, cooking, unboxing, walking, holding something, daily routine). They are NOT talking to camera but are clearly the same creator. THIS IS CRITICAL TO DISTINGUISH from action_lifestyle.
   - "action_lifestyle": A DIFFERENT person (NOT the creator) doing an action, stock-style lifestyle footage, generic hands, strangers, people you haven't seen in the talking head segments
   - "product_shot": Product close-up, unboxing, pouring, holding product
   - "science_mechanism": Diagrams, cells, molecular animations, gut lining, biological processes, medical imagery
   - "text_graphic": Text overlay, infographic, stat callout, before/after graphic
   - "nature_abstract": Nature footage, abstract visuals, flowing water, light effects
   - "testimonial_social": Screenshots of reviews, social proof, comments, ratings

Return a JSON array of ALL segments (both talking and B-roll) in chronological order:
[
  {{
    "segment_number": 1,
    "start_time": 0.0,
    "end_time": 3.5,
    "type": "talking_head" | "broll",
    "broll_category": null | "action_lifestyle" | "product_shot" | "science_mechanism" | "text_graphic" | "nature_abstract" | "testimonial_social",
    "description": "<what's happening visually in this segment>",
    "script_text": "<what's being said during this segment, if audible>",
    "search_query": "<if broll, a TikTok search query that would find similar footage>",
    "veo_prompt": "<if science_mechanism broll, a Veo 3.1 prompt to generate similar footage>",
    "mood": "<emotional tone>",
    "key_elements": ["list", "of", "visual", "elements"]
  }}
]

Be precise with timestamps. Return ONLY the JSON array, no markdown fences."""

    try:
        response = client.models.generate_content(
            model=GEMINI_VIDEO_MODEL,
            contents=types.Content(
                parts=[
                    types.Part(
                        inline_data=types.Blob(data=video_bytes, mime_type="video/mp4"),
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

        segments = json.loads(text)

    except Exception as e:
        log("Analyze", f"ERROR: {e}")
        segments = []

    # Save analysis
    analysis_path = os.path.join(analysis_dir, "segment_analysis.json")
    with open(analysis_path, "w") as f:
        json.dump(segments, f, indent=2)

    broll_segments = [s for s in segments if s.get("type") == "broll"]
    talking_segments = [s for s in segments if s.get("type") == "talking_head"]
    log("Analyze", f"Found {len(talking_segments)} talking segments, {len(broll_segments)} B-roll segments")

    for s in broll_segments:
        cat = s.get("broll_category", "unknown")
        desc = s.get("description", "")[:60]
        log("Analyze", f"  B-roll #{s['segment_number']}: [{cat}] {desc}")

    return segments


# ---------------------------------------------------------------------------
# Stage 3: Extract B-Roll Clips from Original
# ---------------------------------------------------------------------------

def extract_broll_clips(video_path, segments, output_dir):
    """Extract the actual B-roll clips from the original video for reference."""
    clips_dir = ensure_dir(os.path.join(output_dir, "reference_clips"))

    broll_segments = [s for s in segments if s.get("type") == "broll"]

    for seg in broll_segments:
        num = seg["segment_number"]
        start = seg["start_time"]
        end = seg["end_time"]
        duration = end - start

        if duration < 0.3:
            continue

        out_path = os.path.join(clips_dir, f"broll_{num:03d}_ref.mp4")
        subprocess.run([
            "ffmpeg", "-y", "-ss", str(start), "-i", video_path,
            "-t", str(duration), "-c:v", "libx264", "-preset", "fast",
            "-an", out_path
        ], capture_output=True)

        seg["reference_clip"] = out_path

    log("Clips", f"Extracted {len(broll_segments)} reference B-roll clips")
    return broll_segments


# ---------------------------------------------------------------------------
# Stage 4: Source B-Roll from TikTok (action/lifestyle)
# ---------------------------------------------------------------------------

def search_tiktok(query, output_dir, segment_num, max_results=3):
    """Search TikTok for matching B-roll clips using yt-dlp."""
    sourced_dir = ensure_dir(os.path.join(output_dir, "sourced"))

    log("TikTok", f"  Searching: '{query}'")

    # Use yt-dlp to search and download from TikTok
    search_url = f"ytsearch{max_results}:{query} tiktok broll"

    try:
        result = subprocess.run([
            "yt-dlp",
            "--no-warnings",
            "-f", "best[height<=720]",
            "--max-downloads", str(max_results),
            "-o", os.path.join(sourced_dir, f"tiktok_{segment_num:03d}_%(autonumber)s.%(ext)s"),
            "--no-playlist",
            "--match-filter", "duration < 30",
            search_url
        ], capture_output=True, text=True, timeout=60)

        # Find downloaded files
        downloaded = [
            os.path.join(sourced_dir, f)
            for f in os.listdir(sourced_dir)
            if f.startswith(f"tiktok_{segment_num:03d}_")
        ]

        if downloaded:
            log("TikTok", f"  Downloaded {len(downloaded)} clips")
        else:
            log("TikTok", f"  No clips found for query")

        return downloaded

    except subprocess.TimeoutExpired:
        log("TikTok", f"  Search timed out")
        return []
    except FileNotFoundError:
        log("TikTok", "  yt-dlp not installed. Run: pip install yt-dlp")
        return []
    except Exception as e:
        log("TikTok", f"  Error: {e}")
        return []


def source_action_broll(broll_segments, output_dir, brand_knowledge=None):
    """Source action/lifestyle B-roll from TikTok with Gemini visual validation.
    Falls back to Kling image-to-image + animation for unmatched segments."""
    action_segments = [
        s for s in broll_segments
        if s.get("broll_category") in ("action_lifestyle", "nature_abstract", "testimonial_social")
    ]

    if not action_segments:
        log("TikTok", "No action/lifestyle B-roll segments to source")
        return

    log("TikTok", f"Sourcing {len(action_segments)} action/lifestyle clips from TikTok...")

    failed_segments = []  # Track segments that need Kling fallback

    for seg in action_segments:
        query = seg.get("search_query", seg.get("description", ""))
        if not query:
            continue

        downloaded = search_tiktok(query, output_dir, seg["segment_number"])

        # --- Gemini Visual Validation ---
        # Compare each downloaded clip against the reference frame
        if downloaded and seg.get("reference_clip"):
            validated = validate_tiktok_clips(downloaded, seg["reference_clip"], seg.get("description", ""))
            if validated:
                seg["sourced_clips"] = validated
                log("TikTok", f"  Visual validation: {len(validated)}/{len(downloaded)} clips passed")
            else:
                seg["sourced_clips"] = []
                log("TikTok", f"  Visual validation: ALL clips rejected — will use Kling fallback")
                failed_segments.append(seg)
        elif not downloaded:
            seg["sourced_clips"] = []
            failed_segments.append(seg)
        else:
            seg["sourced_clips"] = downloaded

        time.sleep(2)  # Rate limiting

    # --- Stage 4a-fallback: Kling fallback for failed TikTok segments ---
    if failed_segments:
        log("Kling Fallback", f"{len(failed_segments)} segments need Kling fallback (no valid TikTok match)")
        kling_fallback_broll(failed_segments, output_dir, brand_knowledge)


def validate_tiktok_clips(downloaded_clips, reference_clip, description):
    """Use Gemini to visually compare each TikTok clip against the reference B-roll.
    Returns only clips that pass visual correlation check."""
    client = genai.Client(api_key=GEMINI_API_KEY)
    validated = []

    # Extract a keyframe from the reference clip for comparison
    ref_keyframe = reference_clip.replace(".mp4", "_ref_kf.png")
    subprocess.run([
        "ffmpeg", "-y", "-i", reference_clip,
        "-frames:v", "1", "-q:v", "2", ref_keyframe
    ], capture_output=True)

    if not os.path.exists(ref_keyframe):
        log("Validate", "  Could not extract reference keyframe — skipping validation")
        return downloaded_clips  # Pass all through if we can't validate

    ref_bytes = open(ref_keyframe, "rb").read()

    for clip in downloaded_clips:
        try:
            # Extract keyframe from downloaded clip
            clip_kf = clip.replace(".mp4", "_kf.png").replace(".webm", "_kf.png")
            subprocess.run([
                "ffmpeg", "-y", "-i", clip,
                "-frames:v", "1", "-q:v", "2", clip_kf
            ], capture_output=True)

            if not os.path.exists(clip_kf):
                continue

            clip_bytes = open(clip_kf, "rb").read()

            # Ask Gemini to compare
            response = client.models.generate_content(
                model=GEMINI_VIDEO_MODEL,
                contents=types.Content(
                    parts=[
                        types.Part(inline_data=types.Blob(data=ref_bytes, mime_type="image/png")),
                        types.Part(inline_data=types.Blob(data=clip_bytes, mime_type="image/png")),
                        types.Part(text=(
                            f"I have two images. Image 1 is a REFERENCE frame from a video ad showing: {description}\n"
                            f"Image 2 is a CANDIDATE replacement clip.\n\n"
                            f"Does the candidate visually match the reference in terms of:\n"
                            f"1. Same type of shot (close-up, wide, medium)\n"
                            f"2. Same type of action or subject matter\n"
                            f"3. Similar mood/energy\n"
                            f"4. Could serve as a believable replacement in the same video\n\n"
                            f"Reply with ONLY 'PASS' or 'FAIL' followed by a one-sentence reason."
                        ))
                    ]
                )
            )

            result = response.text.strip()
            if result.upper().startswith("PASS"):
                validated.append(clip)
                log("Validate", f"    PASS: {os.path.basename(clip)} — {result}")
            else:
                log("Validate", f"    FAIL: {os.path.basename(clip)} — {result}")
                # Delete rejected clip to avoid confusion
                try:
                    os.remove(clip)
                except:
                    pass

            # Clean up keyframe
            try:
                os.remove(clip_kf)
            except:
                pass

        except Exception as e:
            log("Validate", f"    Error validating {os.path.basename(clip)}: {e}")
            validated.append(clip)  # Pass on error to avoid losing clips

        time.sleep(1)

    # Clean up reference keyframe
    try:
        os.remove(ref_keyframe)
    except:
        pass

    return validated


def upload_image_for_kling(image_path):
    """Upload image to kie.ai for Kling to access via URL."""
    try:
        with open(image_path, "rb") as f:
            resp = requests.post(
                KIE_UPLOAD_URL,
                headers={"Authorization": f"Bearer {KIE_API_KEY}"},
                files={"file": (os.path.basename(image_path), f, "image/png")},
                data={"uploadPath": "images"},
                timeout=60,
            )
        data = resp.json()
        if data.get("code") == 200 and data.get("data", {}).get("downloadUrl"):
            return data["data"]["downloadUrl"]
    except Exception as e:
        log("Kling Fallback", f"  Upload error: {e}")
    return None


def kling_fallback_broll(failed_segments, output_dir, brand_knowledge):
    """For segments where TikTok sourcing failed or clips were visually rejected,
    use Nano Banana 2 image-to-image to transform the reference frame,
    then animate with Kling 3.0."""
    client = genai.Client(api_key=GEMINI_API_KEY)
    fallback_dir = ensure_dir(os.path.join(output_dir, "kling_fallback"))

    headers = {
        "Authorization": f"Bearer {KIE_API_KEY}",
        "Content-Type": "application/json"
    }

    # Load product reference images
    product_parts = []
    product_url = None
    brand_key = brand_knowledge.get("brand_key", "")
    brand_entry = BRAND_REGISTRY.get(brand_key, {})
    product_images = brand_entry.get("product_images", [])

    for pimg in product_images[:1]:
        if os.path.exists(pimg):
            ext = Path(pimg).suffix.lower()
            mime = "image/jpeg" if ext in (".jpg", ".jpeg") else f"image/{ext.lstrip('.')}"
            with open(pimg, "rb") as f:
                product_parts.append(
                    types.Part(inline_data=types.Blob(data=f.read(), mime_type=mime))
                )
            product_url = upload_image_for_kling(pimg)

    product_context = brand_entry.get("default_product_context", "")

    for seg in failed_segments:
        num = seg["segment_number"]
        ref_clip = seg.get("reference_clip")

        if not ref_clip or not os.path.exists(ref_clip):
            log("Kling Fallback", f"  Segment {num}: no reference clip, skipping")
            continue

        out_video = os.path.join(fallback_dir, f"kling_{num:03d}_fallback.mp4")
        if os.path.exists(out_video):
            log("Kling Fallback", f"  Segment {num}: already generated — skipping")
            seg["sourced_clips"] = [out_video]
            seg["sourcing_method"] = "kling_fallback"
            continue

        # Step 1: Extract keyframe from reference
        keyframe = os.path.join(fallback_dir, f"kling_{num:03d}_keyframe.png")
        duration_str = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", ref_clip],
            capture_output=True, text=True
        ).stdout.strip()
        try:
            midpoint = float(duration_str) / 2
        except:
            midpoint = 0.5
        subprocess.run([
            "ffmpeg", "-y", "-ss", str(midpoint), "-i", ref_clip,
            "-frames:v", "1", "-q:v", "2", keyframe
        ], capture_output=True)

        if not os.path.exists(keyframe):
            log("Kling Fallback", f"  Segment {num}: keyframe extraction failed")
            continue

        # Step 2: Nano Banana 2 image-to-image
        log("Kling Fallback", f"  Segment {num}: image-to-image transformation...")
        transformed = os.path.join(fallback_dir, f"kling_{num:03d}_transformed.png")

        try:
            ref_bytes = open(keyframe, "rb").read()
            parts = [
                types.Part(inline_data=types.Blob(data=ref_bytes, mime_type="image/png"))
            ]

            # Determine if this is a product shot
            desc_lower = seg.get("description", "").lower()
            category = seg.get("broll_category", "")
            is_product_shot = category == "product_shot" or any(
                kw in desc_lower for kw in ("bottle", "product", "supplement", "gummy", "jar", "capsule")
            )

            if is_product_shot and product_parts:
                parts.extend(product_parts)
                product_note = (
                    f"I've included a product reference image. Replace the product in this scene with "
                    f"the reference product EXACTLY — same shape, label, colors, branding. "
                    f"Product context: {product_context}. "
                )
            elif not is_product_shot:
                product_note = "Do NOT add any product or branded item to this scene. "
            else:
                product_note = ""

            edit_prompt = (
                f"Edit this reference scene image to create a 1:1 replication adapted for a new brand. "
                f"Keep the EXACT same composition, camera angle, lighting, framing, and action. "
                f"Only change product/brand elements that are already visible. "
                f"IMPORTANT: Do NOT add any text, captions, subtitles, watermarks, logos, or text overlays. "
                f"{product_note}"
                f"\n\nScene description: {seg.get('description', '')}"
            )
            parts.append(types.Part(text=edit_prompt))

            response = client.models.generate_content(
                model=GEMINI_IMAGE_MODEL,
                contents=types.Content(parts=parts),
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE", "TEXT"],
                )
            )

            saved = False
            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    with open(transformed, "wb") as f:
                        f.write(part.inline_data.data)
                    saved = True
                    break

            if not saved:
                log("Kling Fallback", f"  Segment {num}: no image returned from Nano Banana")
                continue

        except Exception as e:
            log("Kling Fallback", f"  Segment {num}: image-to-image error: {e}")
            continue

        # Step 3: Animate with Kling 3.0
        log("Kling Fallback", f"  Segment {num}: animating with Kling 3.0...")

        image_url = upload_image_for_kling(transformed)
        if not image_url:
            log("Kling Fallback", f"  Segment {num}: image upload failed")
            continue

        seg_duration = seg.get("end_time", 5) - seg.get("start_time", 0)
        seg_duration = str(max(3, min(int(seg_duration), 10)))

        kling_prompt = f"{seg.get('description', 'action scene')}. Smooth natural motion."
        if len(kling_prompt) > 2500:
            kling_prompt = kling_prompt[:2497] + "..."

        payload = {
            "model": "kling-3.0/video",
            "input": {
                "prompt": kling_prompt,
                "image_urls": [image_url],
                "sound": False,
                "duration": seg_duration,
                "aspect_ratio": "9:16",
                "mode": "pro",
                "multi_shots": False
            }
        }

        if product_url and is_product_shot:
            payload["input"]["kling_elements"] = [{
                "name": "product",
                "description": product_context,
                "element_input_urls": [product_url]
            }]

        success = False
        for attempt in range(MAX_KLING_RETRIES):
            try:
                resp = requests.post(KIE_CREATE_URL, headers=headers, json=payload, timeout=60)
                resp_data = resp.json()

                if resp_data.get("code") != 200:
                    log("Kling Fallback", f"    Attempt {attempt+1} failed: {resp_data.get('msg', 'error')}")
                    time.sleep(10)
                    continue

                task_id = resp_data["data"]["taskId"]
                log("Kling Fallback", f"    Task submitted: {task_id}")

                video_url = poll_kling_task(task_id, headers)
                if video_url:
                    vid_resp = requests.get(video_url, timeout=120)
                    with open(out_video, "wb") as f:
                        f.write(vid_resp.content)
                    seg["sourced_clips"] = [out_video]
                    seg["sourcing_method"] = "kling_fallback"
                    log("Kling Fallback", f"  Segment {num}: saved {out_video}")
                    success = True
                    break

            except Exception as e:
                log("Kling Fallback", f"    Attempt {attempt+1} error: {e}")
                time.sleep(10)

        if not success:
            log("Kling Fallback", f"  Segment {num}: Kling animation FAILED")

        time.sleep(5)

    fallback_count = sum(1 for s in failed_segments if s.get("sourcing_method") == "kling_fallback")
    log("Kling Fallback", f"Generated {fallback_count}/{len(failed_segments)} fallback clips")


# ---------------------------------------------------------------------------
# Stage 4b: Replicate Creator Action B-Roll (Nano Banana 2 + Kling 3.0)
# ---------------------------------------------------------------------------

def poll_kling_task(task_id, headers, max_wait=600):
    """Poll Kling task status until complete or timeout."""
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
                log("Kling", f"    Task failed: {data['data'].get('failMsg', 'unknown')}")
                return None
            else:
                log("Kling", f"    Status: {state} ({int(time.time() - start)}s)")
        except Exception as e:
            log("Kling", f"    Poll error: {e}")
        time.sleep(KLING_POLL_INTERVAL)
    return None


def replicate_creator_action_broll(broll_segments, output_dir):
    """For creator_action segments: use Nano Banana 2 to replicate the frame,
    extract motion from reference, then animate with Kling 3.0."""
    client = genai.Client(api_key=GEMINI_API_KEY)
    replicated_dir = ensure_dir(os.path.join(output_dir, "replicated"))

    creator_segments = [
        s for s in broll_segments
        if s.get("broll_category") == "creator_action"
    ]

    if not creator_segments:
        log("Creator", "No creator action B-roll segments to replicate")
        return

    log("Creator", f"Replicating {len(creator_segments)} creator action segments via Nano Banana 2 + Kling...")

    headers = {
        "Authorization": f"Bearer {KIE_API_KEY}",
        "Content-Type": "application/json"
    }

    for seg in creator_segments:
        num = seg["segment_number"]
        ref_clip = seg.get("reference_clip")

        if not ref_clip or not os.path.exists(ref_clip):
            log("Creator", f"  Segment {num}: no reference clip, skipping")
            continue

        # Step 1: Extract the keyframe from the reference clip
        keyframe_path = os.path.join(replicated_dir, f"creator_{num:03d}_keyframe.png")
        subprocess.run([
            "ffmpeg", "-y", "-i", ref_clip,
            "-frames:v", "1", "-q:v", "1", keyframe_path
        ], capture_output=True)

        if not os.path.exists(keyframe_path):
            log("Creator", f"  Segment {num}: keyframe extraction failed")
            continue

        # Step 2: Nano Banana 2 image-to-image — replicate the frame for our brand
        log("Creator", f"  Segment {num}: Nano Banana 2 image-to-image...")
        ref_bytes = open(keyframe_path, "rb").read()

        edit_prompt = (
            f"Replicate this exact scene 1:1. Keep the same person, same action, same composition, "
            f"same camera angle, same lighting, same environment. "
            f"This is a creator performing an action — preserve the action exactly as shown. "
            f"Only adapt minor brand elements if visible (product labels, colors). "
            f"Do NOT change the person, the action, or the setting."
        )

        generated_path = os.path.join(replicated_dir, f"creator_{num:03d}_generated.png")

        try:
            response = client.models.generate_content(
                model=GEMINI_IMAGE_MODEL,
                contents=types.Content(
                    parts=[
                        types.Part(inline_data=types.Blob(data=ref_bytes, mime_type="image/png")),
                        types.Part(text=edit_prompt)
                    ]
                ),
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE", "TEXT"],
                )
            )

            saved = False
            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    with open(generated_path, "wb") as f:
                        f.write(part.inline_data.data)
                    saved = True
                    break

            if not saved:
                log("Creator", f"  Segment {num}: Nano Banana returned no image")
                continue

        except Exception as e:
            log("Creator", f"  Segment {num}: Nano Banana error: {e}")
            continue

        # Step 3: Extract motion description from reference via Gemini
        log("Creator", f"  Segment {num}: extracting motion from reference...")
        clip_bytes = open(ref_clip, "rb").read()

        try:
            motion_response = client.models.generate_content(
                model=GEMINI_VIDEO_MODEL,
                contents=types.Content(
                    parts=[
                        types.Part(
                            inline_data=types.Blob(data=clip_bytes, mime_type="video/mp4"),
                            video_metadata=types.VideoMetadata(fps=5)
                        ),
                        types.Part(text=(
                            "Describe the motion in this video clip in one paragraph. "
                            "Include: camera movement (pan, zoom, static, tracking), "
                            "subject movement (walking, reaching, pouring, etc.), "
                            "speed (slow, normal, fast), and any transitions. "
                            "This will be used as a prompt for an AI video generator. "
                            "Return ONLY the motion description, no markdown."
                        ))
                    ]
                )
            )
            motion_desc = motion_response.text.strip()
        except Exception as e:
            log("Creator", f"  Segment {num}: motion extraction error: {e}")
            motion_desc = seg.get("description", "person performing an action")

        # Step 4: Animate with Kling 3.0
        log("Creator", f"  Segment {num}: animating with Kling 3.0...")

        import base64
        with open(generated_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode()

        duration = seg.get("end_time", 5) - seg.get("start_time", 0)
        duration = str(max(3, min(int(duration), 10)))

        kling_prompt = f"{seg.get('description', '')}. Motion: {motion_desc}"
        if len(kling_prompt) > 2500:
            kling_prompt = kling_prompt[:2497] + "..."

        payload = {
            "model": "kling-3.0/video",
            "input": {
                "prompt": kling_prompt,
                "image_urls": [f"data:image/png;base64,{img_b64}"],
                "sound": False,
                "duration": duration,
                "aspect_ratio": "9:16",
                "mode": "pro",
                "multi_shots": False
            }
        }

        out_path = os.path.join(replicated_dir, f"creator_{num:03d}_animated.mp4")
        success = False

        for attempt in range(MAX_KLING_RETRIES):
            try:
                resp = requests.post(KIE_CREATE_URL, headers=headers, json=payload, timeout=60)
                resp_data = resp.json()

                if resp_data.get("code") != 200:
                    log("Creator", f"    Attempt {attempt+1} failed: {resp_data.get('msg', 'error')}")
                    time.sleep(10)
                    continue

                task_id = resp_data["data"]["taskId"]
                video_url = poll_kling_task(task_id, headers)

                if video_url:
                    vid_resp = requests.get(video_url, timeout=120)
                    with open(out_path, "wb") as f:
                        f.write(vid_resp.content)
                    seg["replicated_clip"] = out_path
                    log("Creator", f"  Segment {num}: saved {out_path}")
                    success = True
                    break

            except Exception as e:
                log("Creator", f"    Attempt {attempt+1} error: {e}")
                time.sleep(10)

        if not success:
            log("Creator", f"  Segment {num}: Kling animation FAILED after {MAX_KLING_RETRIES} attempts")

        time.sleep(5)

    replicated_count = sum(1 for s in creator_segments if s.get("replicated_clip"))
    log("Creator", f"Replicated {replicated_count}/{len(creator_segments)} creator action segments")


# ---------------------------------------------------------------------------
# Stage 5: Generate Science B-Roll via Veo 3.1
# ---------------------------------------------------------------------------

def generate_science_broll(broll_segments, brand_knowledge, output_dir):
    """Generate science/mechanism B-roll clips using Veo 3.1."""
    client = genai.Client(api_key=GEMINI_API_KEY)
    generated_dir = ensure_dir(os.path.join(output_dir, "generated"))

    science_segments = [
        s for s in broll_segments
        if s.get("broll_category") in ("science_mechanism",)
    ]

    if not science_segments:
        log("Veo", "No science/mechanism B-roll segments to generate")
        return

    log("Veo", f"Generating {len(science_segments)} science B-roll clips via Veo 3.1...")

    for seg in science_segments:
        num = seg["segment_number"]
        veo_prompt = seg.get("veo_prompt", "")

        if not veo_prompt:
            veo_prompt = f"Scientific visualization: {seg.get('description', 'biological process animation')}"

        out_path = os.path.join(generated_dir, f"veo_{num:03d}_science.mp4")

        if os.path.exists(out_path):
            log("Veo", f"  Segment {num} already generated — skipping")
            seg["generated_clip"] = out_path
            continue

        log("Veo", f"  Generating segment {num}: {veo_prompt[:80]}...")

        try:
            # Calculate target duration
            target_duration = seg.get("end_time", 5) - seg.get("start_time", 0)
            if target_duration < 2:
                target_duration = 3
            if target_duration > 8:
                target_duration = 8  # Veo max ~8s per clip

            operation = client.models.generate_videos(
                model=VEO_MODEL,
                prompt=veo_prompt,
                config=types.GenerateVideosConfig(
                    aspect_ratio="9:16",
                )
            )

            # Poll for completion
            max_wait = 300  # 5 minutes
            start = time.time()
            while not operation.done and (time.time() - start) < max_wait:
                log("Veo", f"    Waiting... ({int(time.time() - start)}s)")
                time.sleep(15)
                operation = client.operations.get(operation)

            if operation.done and operation.response:
                generated_video = operation.response.generated_videos[0]
                client.files.download(file=generated_video.video)
                generated_video.video.save(out_path)
                seg["generated_clip"] = out_path
                log("Veo", f"  Saved: {out_path}")
            else:
                log("Veo", f"  FAILED: Generation timed out for segment {num}")
                seg["generated_clip"] = None

        except Exception as e:
            log("Veo", f"  ERROR generating segment {num}: {e}")
            seg["generated_clip"] = None

        time.sleep(5)  # Rate limiting


# ---------------------------------------------------------------------------
# Stage 6: Generate Sourcing Report
# ---------------------------------------------------------------------------

def generate_report(segments, broll_segments, brand, output_dir, video_path):
    """Generate a sourcing report for the video editor."""
    report_path = os.path.join(output_dir, "broll_sourcing_report.md")
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        f"# B-Roll Sourcing Report — {brand}",
        f"**Date:** {date_str} | **Source Video:** `{os.path.basename(video_path)}`",
        "",
        "## Video Breakdown",
        "",
    ]

    talking = [s for s in segments if s.get("type") == "talking_head"]
    broll = [s for s in segments if s.get("type") == "broll"]
    total_talking = sum(s.get("end_time", 0) - s.get("start_time", 0) for s in talking)
    total_broll = sum(s.get("end_time", 0) - s.get("start_time", 0) for s in broll)

    lines.append(f"- **Talking head segments:** {len(talking)} ({total_talking:.1f}s)")
    lines.append(f"- **B-roll segments:** {len(broll)} ({total_broll:.1f}s)")
    lines.append("")

    # Category breakdown
    lines.append("### B-Roll by Category")
    lines.append("")
    from collections import Counter
    cats = Counter(s.get("broll_category", "unknown") for s in broll)
    for cat, count in cats.most_common():
        lines.append(f"- **{cat}:** {count} segments")
    lines.append("")

    # Timeline
    lines.append("## Full Timeline")
    lines.append("")
    lines.append("| # | Time | Dur | Type | Category | Description |")
    lines.append("|---|------|-----|------|----------|-------------|")

    for seg in segments:
        num = seg.get("segment_number", "?")
        start = seg.get("start_time", 0)
        end = seg.get("end_time", 0)
        dur = end - start
        seg_type = seg.get("type", "?")
        cat = seg.get("broll_category", "—") or "—"
        desc = seg.get("description", "")[:50]
        if len(seg.get("description", "")) > 50:
            desc += "..."
        lines.append(f"| {num} | {start:.1f}s | {dur:.1f}s | {seg_type} | {cat} | {desc} |")

    lines.append("")

    # B-Roll Details
    lines.append("## B-Roll Segment Details")
    lines.append("")

    for seg in broll_segments:
        num = seg["segment_number"]
        cat = seg.get("broll_category", "unknown")
        start = seg.get("start_time", 0)
        end = seg.get("end_time", 0)

        lines.append(f"### B-Roll #{num} — [{cat}] ({start:.1f}s → {end:.1f}s)")
        lines.append(f"**Description:** {seg.get('description', 'N/A')}")
        lines.append(f"**Script Audio:** {seg.get('script_text', 'N/A')}")
        lines.append(f"**Mood:** {seg.get('mood', 'N/A')}")

        if seg.get("reference_clip"):
            lines.append(f"**Reference Clip:** `{os.path.basename(seg['reference_clip'])}`")

        if seg.get("search_query"):
            lines.append(f"**TikTok Search Query:** `{seg['search_query']}`")

        if seg.get("sourced_clips"):
            lines.append(f"**Sourced Clips:**")
            for clip in seg["sourced_clips"]:
                lines.append(f"  - `{os.path.basename(clip)}`")

        if seg.get("veo_prompt"):
            lines.append(f"**Veo Prompt:** {seg['veo_prompt']}")

        if seg.get("generated_clip"):
            lines.append(f"**Generated Clip:** `{os.path.basename(seg['generated_clip'])}`")

        lines.append("")

    # Asset manifest
    lines.append("## Asset Manifest")
    lines.append("")

    lines.append("### Reference Clips (from original)")
    ref_dir = os.path.join(output_dir, "reference_clips")
    if os.path.isdir(ref_dir):
        for f in sorted(os.listdir(ref_dir)):
            if f.endswith(".mp4"):
                lines.append(f"- `reference_clips/{f}`")
    lines.append("")

    lines.append("### Sourced Clips (from TikTok)")
    src_dir = os.path.join(output_dir, "sourced")
    if os.path.isdir(src_dir):
        for f in sorted(os.listdir(src_dir)):
            lines.append(f"- `sourced/{f}`")
    lines.append("")

    lines.append("### Generated Clips (Veo 3.1)")
    gen_dir = os.path.join(output_dir, "generated")
    if os.path.isdir(gen_dir):
        for f in sorted(os.listdir(gen_dir)):
            if f.endswith(".mp4"):
                lines.append(f"- `generated/{f}`")
    lines.append("")

    report_text = "\n".join(lines)
    with open(report_path, "w") as f:
        f.write(report_text)

    log("Report", f"Saved sourcing report: {report_path}")
    return report_path


# ---------------------------------------------------------------------------
# Stage 7: Google Drive Upload
# ---------------------------------------------------------------------------

def upload_to_drive(output_dir, drive_folder_id, brand):
    """Upload sourced/generated B-roll + report to Google Drive."""
    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
    except ImportError:
        log("Drive", "Google Drive packages not installed. Skipping upload.")
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

    service = build("drive", "v3", credentials=creds)

    date_str = datetime.now().strftime("%Y-%m-%d")
    folder_name = f"{brand}_{date_str}_broll_sourced"

    folder_metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [drive_folder_id]
    }
    folder = service.files().create(body=folder_metadata, fields="id").execute()
    parent_id = folder.get("id")

    upload_count = 0

    # Upload sourced clips
    for subdir in ["sourced", "generated"]:
        subdir_path = os.path.join(output_dir, subdir)
        if not os.path.isdir(subdir_path):
            continue
        for filename in sorted(os.listdir(subdir_path)):
            filepath = os.path.join(subdir_path, filename)
            if not os.path.isfile(filepath):
                continue
            mime = "video/mp4" if filename.endswith(".mp4") else "application/octet-stream"
            file_metadata = {"name": filename, "parents": [parent_id]}
            media = MediaFileUpload(filepath, mimetype=mime, resumable=True)
            service.files().create(body=file_metadata, media_body=media, fields="id").execute()
            upload_count += 1
            log("Drive", f"  Uploaded: {filename}")

    # Upload report
    report_path = os.path.join(output_dir, "broll_sourcing_report.md")
    if os.path.exists(report_path):
        file_metadata = {"name": "broll_sourcing_report.md", "parents": [parent_id]}
        media = MediaFileUpload(report_path, mimetype="text/markdown", resumable=True)
        service.files().create(body=file_metadata, media_body=media, fields="id").execute()
        upload_count += 1

    log("Drive", f"Uploaded {upload_count} files to Drive folder '{folder_name}'")
    return parent_id


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="B-Roll Sourcer Pipeline")
    parser.add_argument("--video", required=True, help="Path to the video creative to analyze")
    parser.add_argument("--brand", default="", help="Brand name (loads vault research docs)")
    parser.add_argument("--output-dir", default="./broll-output", help="Output directory")
    parser.add_argument("--drive-folder", default="", help="Google Drive folder ID for upload")
    parser.add_argument("--skip-tiktok", action="store_true", help="Skip TikTok sourcing")
    parser.add_argument("--skip-veo", action="store_true", help="Skip Veo 3.1 generation")
    parser.add_argument("--skip-upload", action="store_true", help="Skip Google Drive upload")

    args = parser.parse_args()

    if not os.path.exists(args.video):
        print(f"ERROR: Video not found: {args.video}")
        sys.exit(1)

    output_dir = os.path.abspath(args.output_dir)
    ensure_dir(output_dir)

    # Load brand knowledge
    brand_knowledge = ""
    if args.brand:
        brand_data = load_brand_knowledge(args.brand)
        brand_knowledge = brand_data["context_text"]

    print("=" * 60)
    print("B-ROLL SOURCER")
    print("=" * 60)
    print(f"Video:     {args.video}")
    print(f"Brand:     {args.brand or '(unspecified)'}")
    print(f"Knowledge: {len(brand_knowledge)} chars from vault")
    print(f"Output:    {output_dir}")
    print("=" * 60)

    # Stage 1: Extract frames
    frames, duration = extract_keyframes(args.video, output_dir)

    # Stage 2: Analyze segments via Gemini
    segments = analyze_video_segments(
        args.video, frames, duration, brand_knowledge, args.brand, output_dir
    )

    if not segments:
        print("ERROR: No segments detected. Check the video file.")
        sys.exit(1)

    # Stage 3: Extract reference B-roll clips
    broll_segments = extract_broll_clips(args.video, segments, output_dir)

    # Stage 4a: Source action/lifestyle from TikTok (with Gemini validation + Kling fallback)
    if not args.skip_tiktok:
        source_action_broll(broll_segments, output_dir, brand_knowledge)
    else:
        log("TikTok", "Skipping TikTok sourcing (--skip-tiktok)")

    # Stage 4b: Replicate creator action B-roll (Nano Banana 2 + Kling 3.0)
    replicate_creator_action_broll(broll_segments, output_dir)

    # Stage 5: Generate science B-roll via Veo 3.1
    if not args.skip_veo:
        generate_science_broll(broll_segments, brand_knowledge, output_dir)
    else:
        log("Veo", "Skipping Veo generation (--skip-veo)")

    # Stage 6: Generate report
    report_path = generate_report(segments, broll_segments, args.brand, output_dir, args.video)

    # Stage 7: Upload to Drive
    if args.drive_folder and not args.skip_upload:
        upload_to_drive(output_dir, args.drive_folder, args.brand)
    elif not args.drive_folder:
        log("Drive", "No Drive folder specified — skipping upload")

    # Summary
    broll_total = len(broll_segments)
    sourced = sum(1 for s in broll_segments if s.get("sourced_clips") and s.get("sourcing_method") != "kling_fallback")
    generated = sum(1 for s in broll_segments if s.get("generated_clip"))
    kling_fb = sum(1 for s in broll_segments if s.get("sourcing_method") == "kling_fallback")

    print("\n" + "=" * 60)
    print("B-ROLL SOURCING COMPLETE")
    print("=" * 60)
    print(f"Total segments:     {len(segments)}")
    print(f"B-roll segments:    {broll_total}")
    print(f"Sourced (TikTok):   {sourced}")
    print(f"Generated (Veo):    {generated}")
    print(f"Kling Fallback:     {kling_fb}")
    print(f"Report:             {report_path}")
    print(f"Output directory:   {output_dir}")
    print("=" * 60)


if __name__ == "__main__":
    main()
