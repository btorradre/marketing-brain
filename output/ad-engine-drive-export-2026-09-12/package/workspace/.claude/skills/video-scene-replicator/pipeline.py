#!/usr/bin/env python3
"""
Video Scene Replicator Pipeline
================================
Takes a reference video, extracts every scene, generates brand-adapted images
via Gemini, animates them with Kling 3.0, and uploads to Google Drive.

Usage:
    python3 pipeline.py \
        --video "/path/to/reference.mp4" \
        --brand "Motilli" \
        --product-context "Celery juice fiber gummies for GLP-1 users" \
        --style "claymation style, soft pastel colors, playful" \
        --drive-folder "FOLDER_ID" \
        --product-images "/path/to/img1.png,/path/to/img2.png" \
        --output-dir "./replicator-output"
"""

import argparse
import base64
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime

# ---------------------------------------------------------------------------
# Dependency check
# ---------------------------------------------------------------------------
REQUIRED_PACKAGES = ["google.genai", "PIL", "requests", "googleapiclient"]

def check_deps():
    missing = []
    for pkg in REQUIRED_PACKAGES:
        try:
            __import__(pkg.split(".")[0] if "." not in pkg else pkg.replace(".", "/").split("/")[0])
        except ImportError:
            missing.append(pkg)
    # More precise checks
    try:
        from google import genai  # noqa: F401
    except ImportError:
        if "google.genai" not in missing:
            missing.append("google-genai")
    if missing:
        print(f"[!] Missing packages: {missing}")
        print("    pip install google-genai google-api-python-client google-auth-httplib2 google-auth-oauthlib Pillow requests")
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
GDRIVE_CLIENT_ID = "630165550470-bk00miojfehkb5va5hdoupbn170lurhh.apps.googleusercontent.com"
GDRIVE_CLIENT_SECRET = "[REDACTED_SECRET]"
GDRIVE_TOKEN_PATH = os.path.expanduser("~/.claude/skills/video-scene-replicator/gdrive_token.json")

GEMINI_VIDEO_MODEL = "gemini-3-flash-preview"
GEMINI_IMAGE_MODEL = "gemini-3.1-flash-image-preview"  # Nano Banana 2 — supports image-to-image editing

KIE_CREATE_URL = "https://api.kie.ai/api/v1/jobs/createTask"
KIE_STATUS_URL = "https://api.kie.ai/api/v1/jobs/recordInfo"

SCENE_THRESHOLD = 0.3  # ffmpeg scene detection threshold (lower = more sensitive)
ANIMATED_INTERVAL = 3.0  # seconds between keyframes for animated/smooth-transition video
MAX_KLING_RETRIES = 3
KLING_POLL_INTERVAL = 15  # seconds
MAX_IMAGE_VALIDATION_RETRIES = 2  # Max regeneration attempts if Gemini visual validation fails

VAULT_ROOT = os.path.expanduser("~/Documents/marketing brain")

# Brand knowledge registry — maps brand name to research doc paths & product ref images
BRAND_REGISTRY = {
    "motilli": {
        "research_docs": [
            os.path.join(VAULT_ROOT, "brands/motilli/copy/briefs/Motilli_Master_Copywriting_Brief.md"),
            os.path.join(VAULT_ROOT, "brands/motilli/copy/strategy/Motilli_Product_Context.md"),
            os.path.join(VAULT_ROOT, "brands/motilli/copy/strategy/Motilli_Avatar_VoC.md"),
        ],
        "product_images": [
            "/Users/brooksorradre2/Documents/marketing brain/brands/motilli/website assets/product reference.png",
            os.path.join(VAULT_ROOT, "brands/motilli/brand/website-assets/motilli product reference.png"),
        ],
        "product_images_fallback": [
            "/Users/brooksorradre2/Documents/marketing brain/brands/motilli/website assets/product reference.png",
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
        "product_images_dir": os.path.join(VAULT_ROOT, "statics/product references/velantra/boat tote"),
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
        "product_images_dir": os.path.join(VAULT_ROOT, "statics/product references/velantra/meridian"),
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
        "product_images_dir": os.path.join(VAULT_ROOT, "statics/product references/velantra/weekender"),
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


def load_brand_knowledge(brand_name):
    """Load research docs from the vault for the specified brand.
    Returns a dict with 'context_text', 'product_images', 'default_product_context'."""
    key = brand_name.lower().strip()
    registry = BRAND_REGISTRY.get(key)

    if not registry:
        print(f"[Brand] No registry entry for '{brand_name}' — using manual context only")
        return {"context_text": "", "product_images": [], "default_product_context": ""}

    print(f"[Brand] Loading knowledge for: {brand_name}")

    context_parts = []
    for doc_path in registry["research_docs"]:
        if not os.path.exists(doc_path):
            print(f"[Brand]   SKIP (not found): {os.path.basename(doc_path)}")
            continue

        ext = Path(doc_path).suffix.lower()
        try:
            if ext == ".md":
                with open(doc_path, "r", encoding="utf-8") as f:
                    text = f.read()
                context_parts.append(f"--- {os.path.basename(doc_path)} ---\n{text}")
                print(f"[Brand]   Loaded: {os.path.basename(doc_path)} ({len(text)} chars)")

            elif ext == ".docx":
                # Extract text from .docx
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
                # Extract text via pdfminer if available, else skip
                try:
                    from pdfminer.high_level import extract_text
                    text = extract_text(doc_path)
                    context_parts.append(f"--- {os.path.basename(doc_path)} ---\n{text}")
                    print(f"[Brand]   Loaded: {os.path.basename(doc_path)} ({len(text)} chars)")
                except ImportError:
                    print(f"[Brand]   SKIP (pdfminer not installed): {os.path.basename(doc_path)}")
                    print(f"[Brand]   Install with: pip install pdfminer.six")

        except Exception as e:
            print(f"[Brand]   ERROR reading {os.path.basename(doc_path)}: {e}")

    full_context = "\n\n".join(context_parts)

    # Cap at ~30k chars to leave room in context window
    if len(full_context) > 30000:
        full_context = full_context[:30000] + "\n\n[... truncated for context window ...]"
        print(f"[Brand]   Truncated to 30,000 chars")

    # Collect product images: scan directory first, then explicit list, then fallback
    valid_images = []
    img_dir = registry.get("product_images_dir", "")
    if img_dir and os.path.isdir(img_dir):
        img_exts = {".png", ".jpg", ".jpeg", ".webp"}
        for fname in sorted(os.listdir(img_dir)):
            if Path(fname).suffix.lower() in img_exts:
                valid_images.append(os.path.join(img_dir, fname))
        print(f"[Brand]   Product images from dir: {len(valid_images)} found in {os.path.basename(img_dir)}/")
    if not valid_images and "product_images" in registry:
        valid_images = [p for p in registry["product_images"] if os.path.exists(p)]
        if valid_images:
            print(f"[Brand]   Product images (explicit): {len(valid_images)} found")
    if not valid_images:
        valid_images = [p for p in registry.get("product_images_fallback", []) if os.path.exists(p)]
        if valid_images:
            print(f"[Brand]   Product images (fallback): {len(valid_images)} found")

    print(f"[Brand] Total context: {len(full_context)} chars from {len(context_parts)} docs")

    return {
        "context_text": full_context,
        "product_images": valid_images,
        "default_product_context": registry["default_product_context"],
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
    """Load progress file to enable resume."""
    progress_file = os.path.join(output_dir, ".progress.json")
    if os.path.exists(progress_file):
        with open(progress_file) as f:
            return json.load(f)
    return {"completed_stages": {}, "scene_status": {}}


def save_progress(output_dir, progress):
    progress_file = os.path.join(output_dir, ".progress.json")
    with open(progress_file, "w") as f:
        json.dump(progress, f, indent=2)


# ---------------------------------------------------------------------------
# Stage 1: Scene Detection & Frame Extraction
# ---------------------------------------------------------------------------

def extract_scenes(video_path, output_dir, threshold=SCENE_THRESHOLD, interval=0.0):
    """Use ffmpeg to detect scene changes and extract keyframes + short clips.

    Args:
        interval: If > 0, extract keyframes at fixed intervals (seconds) instead of
                  scene detection. Best for animated/smooth-transition video where
                  ffmpeg scene detection misses visual changes.
    """
    scenes_dir = ensure_dir(os.path.join(output_dir, "scenes"))

    # Get video duration
    probe = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", video_path],
        capture_output=True, text=True
    )
    probe_data = json.loads(probe.stdout)
    duration = float(probe_data["format"]["duration"])
    log(1, f"Video duration: {duration:.1f}s")

    if interval > 0:
        # --- INTERVAL MODE (for animated / smooth-transition video) ---
        log(1, f"Extracting keyframes every {interval:.1f}s (interval mode — best for animated content)")
        timestamps = []
        t = 0.0
        while t < duration:
            timestamps.append(round(t, 2))
            t += interval
    else:
        # --- SCENE DETECTION MODE (for live-action / hard-cut video) ---
        log(1, f"Detecting scenes in {video_path} (threshold={threshold})")

        scene_cmd = [
            "ffmpeg", "-i", video_path,
            "-filter:v", f"select='gt(scene,{threshold})',showinfo",
            "-vsync", "vfr",
            "-f", "null", "-"
        ]
        result = subprocess.run(scene_cmd, capture_output=True, text=True)

        # Parse timestamps from showinfo output
        timestamps = [0.0]  # Always include the first frame
        for line in result.stderr.split("\n"):
            if "pts_time:" in line:
                match = re.search(r"pts_time:(\d+\.?\d*)", line)
                if match:
                    ts = float(match.group(1))
                    # Only add if sufficiently different from last timestamp
                    if ts - timestamps[-1] > 0.5:
                        timestamps.append(ts)

        # If scene detection finds too few scenes, fall back to interval mode
        if len(timestamps) <= 3 and duration > 15:
            fallback_interval = ANIMATED_INTERVAL
            log(1, f"Only {len(timestamps)} scenes detected in {duration:.0f}s video — falling back to {fallback_interval}s interval extraction")
            timestamps = []
            t = 0.0
            while t < duration:
                timestamps.append(round(t, 2))
                t += fallback_interval

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

        # Extract ~2s clip for motion analysis (or until next scene)
        next_ts = timestamps[i + 1] if i + 1 < len(timestamps) else min(ts + 2.0, duration)
        clip_duration = min(next_ts - ts, 5.0)  # Cap at 5s
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
    return scenes


# ---------------------------------------------------------------------------
# Stage 1.5: Smart Scene Classification
# ---------------------------------------------------------------------------
# Classifies each scene by TYPE so the pipeline can handle them differently:
#   TALKING_HEAD        → SKIP (we have our own AIUGC)
#   SCIENCE_ANIMATION   → GENERATE with Kling (adapted for brand mechanism)
#   STATISTICS_OVERLAY  → ADAPT for brand (research/stats graphic adapted for brand)
#   RESEARCH_SCREENSHOT → ADAPT for brand (study citation, paper excerpt, data card)
#   WEBSITE_SCREENSHOT  → ADAPT for brand (product page, landing page mockup)
#   GRAPHIC_OVERLAY     → ADAPT for brand (science diagram overlaid on talking head)
#   PRODUCT_SHOT        → GENERATE with brand product reference
#   CREATOR_ACTION      → GENERATE with Kling (same creator doing non-talking)
#   THIRD_PARTY_ACTION  → SOURCE from TikTok (real person, not creator)
#   PATRIOTIC_TRUST     → GENERATE with Kling
#   END_CARD            → SKIP

SCENE_CATEGORIES = [
    "TALKING_HEAD", "SCIENCE_ANIMATION", "STATISTICS_OVERLAY",
    "RESEARCH_SCREENSHOT", "WEBSITE_SCREENSHOT", "GRAPHIC_OVERLAY",
    "PRODUCT_SHOT", "CREATOR_ACTION", "THIRD_PARTY_ACTION",
    "PATRIOTIC_TRUST", "END_CARD"
]

SKIP_CATEGORIES = {"TALKING_HEAD", "END_CARD"}
KLING_CATEGORIES = {"SCIENCE_ANIMATION", "CREATOR_ACTION", "PATRIOTIC_TRUST"}
ADAPT_CATEGORIES = {"STATISTICS_OVERLAY", "RESEARCH_SCREENSHOT", "WEBSITE_SCREENSHOT", "GRAPHIC_OVERLAY"}
TIKTOK_CATEGORIES = {"THIRD_PARTY_ACTION"}

def classify_scenes(video_path, scenes, brand, product_context, output_dir):
    """Upload the full video + all keyframes to Gemini and classify each scene
    into a category that determines how it should be handled."""
    classification_path = os.path.join(output_dir, "analysis", "scene_classification.json")

    # Skip if already classified
    if os.path.exists(classification_path):
        log("1.5", f"Scene classification already exists — loading from {classification_path}")
        with open(classification_path) as f:
            return json.load(f)

    ensure_dir(os.path.join(output_dir, "analysis"))
    client = genai.Client(api_key=GEMINI_API_KEY)

    log("1.5", "Uploading reference video for scene classification...")
    video_file = client.files.upload(file=video_path)
    while video_file.state.name == "PROCESSING":
        time.sleep(5)
        video_file = client.files.get(name=video_file.name)

    if video_file.state.name == "FAILED":
        log("1.5", "WARNING: Video upload failed — skipping classification (all scenes will be processed)")
        client.files.delete(name=video_file.name)
        # Return default: process everything
        return [{"scene_number": s["scene_number"], "category": "SCIENCE_ANIMATION",
                 "action": "GENERATE_KLING", "description": "Classification unavailable"}
                for s in scenes]

    # Upload keyframes
    contents = [video_file]
    scene_uploads = []
    for s in scenes:
        try:
            sf = client.files.upload(file=s["keyframe"])
            scene_uploads.append((s["scene_number"], sf))
            contents.append(sf)
            contents.append(f"[scene_{s['scene_number']:03d}.png — keyframe #{s['scene_number']}]")
        except Exception as e:
            log("1.5", f"  Failed to upload keyframe {s['scene_number']}: {e}")

    prompt = f"""You are analyzing a direct response video ad. This video has been broken into {len(scenes)} keyframe screenshots.

We are adapting this reference ad for a DIFFERENT brand called {brand} ({product_context}). We already have our own AIUGC talking head, so we do NOT need the talking head scenes from this reference.

Classify each keyframe scene into EXACTLY ONE category:

1. **TALKING_HEAD** — Creator/doctor/presenter speaking to camera with ONLY speech caption text overlays. NO unique visual content worth replicating. Action: SKIP.

2. **SCIENCE_ANIMATION** — A standalone 3D medical/scientific animation (bacteria, enzymes, nerves, cells, biofilm, etc.) that fills the ENTIRE frame. NOT a small graphic overlaid on the talking head. Action: GENERATE_KLING.

3. **GRAPHIC_OVERLAY** — A talking head scene where a SCIENCE DIAGRAM, MEDICAL ILLUSTRATION, or INFOGRAPHIC is overlaid/composited onto the frame alongside the speaker (e.g., a glowing organ diagram appears while the doctor talks, an anatomical illustration pops up in the lower third). The key distinction: the speaker IS visible but there's a meaningful graphic element overlaid. Action: ADAPT_FOR_BRAND — recreate the graphic/diagram adapted for the target brand's mechanism.

4. **RESEARCH_SCREENSHOT** — A screenshot or card showing a STUDY CITATION, RESEARCH PAPER EXCERPT, SCIENTIFIC DATA, chemical structure diagram, or journal reference. May appear overlaid on the speaker or as a standalone card. Action: ADAPT_FOR_BRAND — recreate with equivalent research for the target brand's ingredients.

5. **WEBSITE_SCREENSHOT** — A screen recording or screenshot of a PRODUCT WEBSITE, landing page, Amazon listing, or e-commerce page showing the product. Action: ADAPT_FOR_BRAND — recreate as the target brand's product page/website.

6. **STATISTICS_OVERLAY** — Data visualizations, before/after comparisons, percentage stats, clinical trial results, or numerical claims shown as the PRIMARY visual. Action: ADAPT_FOR_BRAND — recreate with the target brand's data.

7. **PRODUCT_SHOT** — Physical product (bottle, gummies, packaging) being HELD or DISPLAYED in a real-world setting. Action: GENERATE_PRODUCT.

8. **CREATOR_ACTION** — The SAME creator/presenter doing something OTHER than talking to camera (holding product up, pointing, gesturing with product, demonstrating). Action: GENERATE_KLING.

9. **THIRD_PARTY_ACTION** — A DIFFERENT real person (not the creator) in an action/lifestyle shot. Action: SOURCE_TIKTOK.

10. **PATRIOTIC_TRUST** — Trust imagery (Statue of Liberty, flag, lab, facility, manufacturing). Action: GENERATE_KLING.

11. **END_CARD** — Black screen, logo, or end slate. Action: SKIP.

CRITICAL CLASSIFICATION RULES:
- Person speaking to camera with ONLY speech captions → TALKING_HEAD
- Person speaking to camera WITH a science graphic/diagram overlaid → GRAPHIC_OVERLAY (not TALKING_HEAD!)
- Person speaking with a research citation/study appearing on screen → RESEARCH_SCREENSHOT (not TALKING_HEAD!)
- Screen recording of a product website → WEBSITE_SCREENSHOT (not PRODUCT_SHOT!)
- Standalone 3D animation filling the whole frame → SCIENCE_ANIMATION
- Small graphic composited onto a talking head frame → GRAPHIC_OVERLAY
- 3D rendered animation of any kind → SCIENCE_ANIMATION
- Person holding/showing product (not just talking) → CREATOR_ACTION or PRODUCT_SHOT

IMPORTANT: Do NOT classify scenes with visual overlays (science graphics, research citations, website screenshots) as TALKING_HEAD just because the speaker is also visible. If there is ANY meaningful screenshot, graphic, diagram, or data overlay on the frame, it MUST be classified as the appropriate overlay category, NOT as TALKING_HEAD. These screenshot-style elements are CRITICAL B-roll components that need to be adapted for the target brand.

For each scene return:
- scene_number (1-{len(scenes)})
- category
- description (specific — what's in the frame, describe BOTH the speaker state AND any overlays/graphics)
- action (SKIP, GENERATE_KLING, ADAPT_FOR_BRAND, GENERATE_PRODUCT, SOURCE_TIKTOK)
- kling_prompt (if GENERATE_KLING — detailed prompt adapted for {brand}/{product_context})
- tiktok_search_query (if SOURCE_TIKTOK — search terms for TikTok, prefer no-text clips)
- adapted_version (if ADAPT_FOR_BRAND — detailed description of what the adapted version should contain for {brand}, matching the SAME visual format as the reference: same layout, same style of graphic/screenshot, but with {brand}'s content)

Return as valid JSON array."""

    contents.append(prompt)

    log("1.5", f"Classifying {len(scenes)} scenes...")
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents
        )

        text = response.text.strip()
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\n?", "", text)
            text = re.sub(r"\n?```$", "", text.rstrip())

        classifications = json.loads(text)

        # Log summary
        from collections import Counter
        cats = Counter(c.get("category") for c in classifications)
        skip_count = sum(1 for c in classifications if c.get("action") == "SKIP")
        log("1.5", f"Classification complete: {len(classifications)} scenes")
        for cat, count in cats.most_common():
            log("1.5", f"  {cat}: {count}")
        log("1.5", f"Scenes to SKIP: {skip_count}, to process: {len(classifications) - skip_count}")

    except Exception as e:
        log("1.5", f"WARNING: Classification failed: {e} — processing all scenes")
        classifications = [{"scene_number": s["scene_number"], "category": "SCIENCE_ANIMATION",
                           "action": "GENERATE_KLING", "description": "Classification unavailable"}
                          for s in scenes]

    # Cleanup uploaded files
    try:
        client.files.delete(name=video_file.name)
        for _, sf in scene_uploads:
            client.files.delete(name=sf.name)
    except Exception:
        pass

    with open(classification_path, "w") as f:
        json.dump(classifications, f, indent=2)

    return classifications


# ---------------------------------------------------------------------------
# Stage 2: Scene Analysis via Gemini
# ---------------------------------------------------------------------------

def analyze_scenes(scenes, output_dir, classifications=None):
    """Upload each scene to Gemini and get structured analysis.
    If classifications are provided, skip TALKING_HEAD and END_CARD scenes."""
    analysis_dir = ensure_dir(os.path.join(output_dir, "analysis"))
    client = genai.Client(api_key=GEMINI_API_KEY)

    # Build classification lookup
    class_lookup = {}
    if classifications:
        for c in classifications:
            class_lookup[c.get("scene_number")] = c

    analyses = []

    for scene in scenes:
        # Skip scenes classified as TALKING_HEAD or END_CARD
        scene_class = class_lookup.get(scene["scene_number"], {})
        if scene_class.get("category") in SKIP_CATEGORIES:
            log(2, f"Skipping scene {scene['scene_number']}/{len(scenes)} ({scene_class.get('category')})")
            continue
        log(2, f"Analyzing scene {scene['scene_number']}/{len(scenes)}...")

        # Read the keyframe image
        img_bytes = open(scene["keyframe"], "rb").read()

        # Read the clip for motion analysis
        clip_bytes = open(scene["clip"], "rb").read()

        prompt = """Analyze this video scene in detail. Return a JSON object with these exact fields:
{
  "scene_number": <int>,
  "description": "<detailed description of what's happening in the scene>",
  "composition": "<camera angle, framing, depth of field, layout of elements>",
  "style": "<visual style - lighting, color palette, texture, aesthetic (e.g. claymation, photorealistic, illustrated)>",
  "motion": "<describe all motion: camera movement (zoom, pan, tilt, static), subject movement, any particle effects or transitions>",
  "duration_estimate": "<estimated duration in seconds>",
  "text_overlays": "<any text visible in the scene, or 'None'>",
  "key_elements": ["<list>", "<of>", "<key visual elements>"],
  "mood": "<emotional tone of the scene>",
  "background": "<describe the background/environment in detail>"
}

Be extremely precise about the visual style and motion — these will be used to recreate this scene for a different brand. Return ONLY the JSON, no markdown fences."""

        try:
            # Analyze keyframe for composition/style
            response = client.models.generate_content(
                model=GEMINI_VIDEO_MODEL,
                contents=types.Content(
                    parts=[
                        types.Part(
                            inline_data=types.Blob(data=img_bytes, mime_type="image/png")
                        ),
                        types.Part(
                            inline_data=types.Blob(data=clip_bytes, mime_type="video/mp4"),
                            video_metadata=types.VideoMetadata(fps=5)
                        ),
                        types.Part(text=prompt)
                    ]
                )
            )

            # Parse the JSON response
            text = response.text.strip()
            # Remove markdown code fences if present
            if text.startswith("```"):
                text = re.sub(r"^```(?:json)?\n?", "", text)
                text = re.sub(r"\n?```$", "", text)

            analysis = json.loads(text)
            analysis["scene_number"] = scene["scene_number"]
            analysis["timestamp"] = scene["timestamp"]
            analysis["duration"] = scene["duration"]

        except Exception as e:
            log(2, f"  WARNING: Failed to analyze scene {scene['scene_number']}: {e}")
            analysis = {
                "scene_number": scene["scene_number"],
                "timestamp": scene["timestamp"],
                "duration": scene["duration"],
                "description": "Analysis failed — manual review needed",
                "composition": "",
                "style": "",
                "motion": "static",
                "text_overlays": "None",
                "key_elements": [],
                "mood": "",
                "background": "",
                "error": str(e)
            }

        analyses.append(analysis)
        time.sleep(1)  # Rate limiting

    # Save full analysis
    analysis_path = os.path.join(analysis_dir, "scene_analysis.json")
    with open(analysis_path, "w") as f:
        json.dump(analyses, f, indent=2)

    log(2, f"Analysis complete — saved to {analysis_path}")
    return analyses


# ---------------------------------------------------------------------------
# Stage 2.5: Creative Strategist — Holistic Video Adaptation
# ---------------------------------------------------------------------------

def generate_creative_direction(video_path, analyses, brand, product_context,
                                brand_knowledge, output_dir):
    """Upload the FULL video to Gemini and have it design a conceptual adaptation.

    This is the 'creative strategist brain' — it watches the entire video holistically,
    understands the narrative arc, villain/hero structure, and persuasion mechanics,
    then maps every scene to a brand-specific adaptation. This produces CONCEPTUAL
    direction (new villain, new heroes, new narrative) rather than surface-level brand swaps.
    """
    direction_dir = ensure_dir(os.path.join(output_dir, "creative_direction"))
    direction_path = os.path.join(direction_dir, "creative_direction.json")

    # Skip if already generated
    if os.path.exists(direction_path):
        log("2.5", f"Creative direction already exists — loading from {direction_path}")
        with open(direction_path) as f:
            return json.load(f)

    client = genai.Client(api_key=GEMINI_API_KEY)

    log("2.5", "Uploading full video to Gemini for holistic creative analysis...")
    video_file = client.files.upload(file=video_path)
    while video_file.state.name == "PROCESSING":
        time.sleep(3)
        video_file = client.files.get(name=video_file.name)

    if video_file.state.name == "FAILED":
        log("2.5", "WARNING: Video processing failed — falling back to per-scene adaptation")
        client.files.delete(name=video_file.name)
        return None

    # Build the scene timestamp map so Gemini can reference extracted scenes
    scene_map = "\n".join(
        f"Scene {a['scene_number']}: {a['timestamp']:.1f}s — {a.get('description', 'N/A')[:100]}"
        for a in analyses
    )

    # Truncate brand knowledge for prompt
    bk = brand_knowledge[:20000] if brand_knowledge else ""

    prompt = f"""You are an elite creative strategist designing a CONCEPTUAL ADAPTATION of a video ad for a different brand. You are NOT doing a brand swap — you are reimagining the entire creative concept while preserving the structural mechanics that make it work.

WATCH THIS VIDEO CAREFULLY. Understand:
1. The narrative arc (problem → failed solutions → mechanism education → product reveal → transformation)
2. The villain(s) and how they're portrayed
3. The hero ingredients/features and how they're introduced
4. The persuasion structure (what beliefs shift, in what order)
5. The creative devices (personification, humor, internal journey, demonstrations, etc.)
6. The visual style and production approach

EXTRACTED SCENES (these are the keyframes we'll be generating images for):
{scene_map}

TARGET BRAND: {brand}
PRODUCT: {product_context}

BRAND KNOWLEDGE:
{bk}

NOW DESIGN THE ADAPTATION. For each extracted scene, provide creative direction that REIMAGINES the content for the target brand. This means:
- If the original has a "bad breath monster," your adaptation needs {brand}'s equivalent villain character
- If the original shows "Oil of Oregano hero," your adaptation needs {brand}'s ingredient heroes
- If the original shows failed solutions, your adaptation shows {brand}'s avatar's failed solutions
- Preserve the STRUCTURE, PACING, and CREATIVE DEVICES — change the CONTENT

Return a JSON object with this exact structure:
{{
  "adaptation_concept": "<1-2 sentence summary of the adapted creative concept>",
  "villain": {{
    "name": "<the villain character/entity in the adaptation>",
    "visual_description": "<detailed visual description of the villain>",
    "personality": "<personality traits, voice, attitude>",
    "represents": "<what problem/enemy this villain personifies>"
  }},
  "heroes": [
    {{
      "name": "<ingredient/feature hero name>",
      "visual_description": "<detailed visual description>",
      "personality": "<personality traits>",
      "action": "<what this hero does to defeat the villain>",
      "key_line": "<what this character would say>"
    }}
  ],
  "avatar": {{
    "description": "<the person shown in the ad — age, appearance, situation>",
    "failed_solutions": ["<list of solutions they've tried that don't work>"]
  }},
  "scenes": [
    {{
      "scene_number": <int matching extracted scene>,
      "narrative_role": "<hook | problem_escalation | failed_solution | mechanism_reveal | villain_origin | ingredient_hero | transformation | product_reveal | cta | etc>",
      "generation_mode": "image_to_image"  — ALWAYS image-to-image. Every scene MUST use the reference keyframe as the base. Never use text-to-image.",
      "include_product": <true | false>  — Whether the brand's product should appear in this scene. Product should ONLY appear when the narrative has reached the product reveal/solution phase. All problem-aware, villain, and mechanism scenes should be false. Only late-act scenes (product discovery, CTA, transformation with product) should be true.",
      "adaptation_description": "<DETAILED description of what THIS scene should show in the adaptation — 2-3 sentences minimum. Be specific about characters, actions, visual elements, colors, composition.>",
      "key_text_overlay": "<what text should appear on screen, if any>",
      "mood": "<emotional tone of this scene in the adaptation>",
      "preserves_from_original": "<what structural element from the original is preserved>"
    }}
  ]
}}

CRITICAL RULES:
1. Every extracted scene MUST have a corresponding entry in the scenes array
2. The adaptation must make sense as a complete narrative — not just random scenes
3. Preserve the TIMING and PACING of the original — if the original reveals the product at scene 15 of 25, your adaptation should too
4. The villain, heroes, and avatar must be specific to the target brand
5. Visual descriptions must be detailed enough for an AI image generator
6. Return ONLY the JSON, no markdown fences"""

    log("2.5", f"Generating creative direction for {len(analyses)} scenes...")

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_uri(file_uri=video_file.uri, mime_type="video/mp4"),
                        types.Part.from_text(text=prompt),
                    ]
                )
            ]
        )

        text = response.text.strip()
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\n?", "", text)
            text = re.sub(r"\n?```$", "", text)

        creative_direction = json.loads(text)

        with open(direction_path, "w") as f:
            json.dump(creative_direction, f, indent=2)

        log("2.5", f"Creative direction generated — {len(creative_direction.get('scenes', []))} scene directives saved")

    except Exception as e:
        log("2.5", f"WARNING: Creative direction generation failed: {e}")
        creative_direction = None

    # Cleanup
    try:
        client.files.delete(name=video_file.name)
    except Exception:
        pass

    return creative_direction


# ---------------------------------------------------------------------------
# Stage 3: Brand-Adapted Image Prompts
# ---------------------------------------------------------------------------

def generate_brand_prompts(analyses, brand, product_context, style_notes, output_dir, brand_knowledge="", creative_direction=None):
    """Generate image prompts adapted for the target brand."""
    prompts_dir = ensure_dir(os.path.join(output_dir, "prompts"))
    client = genai.Client(api_key=GEMINI_API_KEY)

    brand_prompts = []

    # Build the brand knowledge block for the prompt
    knowledge_block = ""
    if brand_knowledge:
        knowledge_block = f"""

BRAND RESEARCH & KNOWLEDGE (use this to inform brand voice, avatar, product details, and visual identity):
{brand_knowledge}
"""

    # Build creative direction lookup by scene number
    cd_lookup = {}
    if creative_direction and "scenes" in creative_direction:
        for sd in creative_direction["scenes"]:
            cd_lookup[sd.get("scene_number")] = sd

    for analysis in analyses:
        log(3, f"Generating brand prompt for scene {analysis['scene_number']}/{len(analyses)}...")

        # Get creative direction for this scene (if available)
        scene_cd = cd_lookup.get(analysis["scene_number"])

        if scene_cd:
            # --- CREATIVE STRATEGIST MODE ---
            # Use conceptual adaptation direction from Stage 2.5
            cd_context = f"""
CREATIVE STRATEGIST DIRECTION FOR THIS SCENE:
- Narrative Role: {scene_cd.get('narrative_role', 'unknown')}
- What This Scene Should Show: {scene_cd.get('adaptation_description', 'N/A')}
- Mood: {scene_cd.get('mood', 'N/A')}
- Preserves From Original: {scene_cd.get('preserves_from_original', 'N/A')}

ADAPTATION CHARACTERS:
- Villain: {json.dumps(creative_direction.get('villain', {}), indent=2) if creative_direction else 'N/A'}
- Heroes: {json.dumps(creative_direction.get('heroes', []), indent=2) if creative_direction else 'N/A'}
- Avatar: {json.dumps(creative_direction.get('avatar', {}), indent=2) if creative_direction else 'N/A'}
"""
            prompt = f"""You are a creative director generating an image for a CONCEPTUAL ADAPTATION of a video ad.

ORIGINAL SCENE (for composition/style reference ONLY — the CONTENT is changing):
{json.dumps(analysis, indent=2)}

{cd_context}

TARGET BRAND: {brand}
PRODUCT CONTEXT: {product_context}
STYLE DIRECTION: {style_notes or 'Match the original visual style exactly'}
{knowledge_block}

Generate an image generation prompt that:
1. PRESERVES the composition, camera angle, lighting, and visual style from the original
2. REPLACES the content with the CREATIVE STRATEGIST'S adaptation direction above
3. Uses the adaptation's villain, heroes, and avatar instead of the original's
4. Is detailed enough for an AI image generator to create the scene from scratch
5. Includes specific details about: subject positioning, lighting, colors, textures, background
6. NEVER includes text, captions, subtitles, watermarks, or text overlays

The image should look like it belongs in the SAME video as the original (same animation style, quality level, lighting approach) but with COMPLETELY DIFFERENT content adapted for {brand}.

Return ONLY the image generation prompt as a single paragraph. No explanations, no markdown."""
        else:
            # --- FALLBACK: Standard brand-swap mode (no creative direction available) ---
            prompt = f"""You are a creative director adapting a reference video scene for a new brand.

REFERENCE SCENE ANALYSIS:
{json.dumps(analysis, indent=2)}

TARGET BRAND: {brand}
PRODUCT CONTEXT: {product_context}
STYLE DIRECTION: {style_notes}
{knowledge_block}

Generate an image generation prompt that recreates this exact scene composition, framing, and visual style — but adapted for the target brand and product.

RULES:
1. PRESERVE the exact composition, camera angle, lighting, and visual style from the reference
2. REPLACE the product/brand elements with the target brand's product
3. PRESERVE the overall mood, color palette direction, and aesthetic
4. The prompt must be detailed enough for an AI image generator to recreate the scene
5. Include specific details about: subject positioning, lighting direction, color values, texture, background elements
6. If the style is claymation/3D/illustrated, maintain that exact style
7. DO NOT add elements that weren't in the reference — stay faithful to the composition
8. NEVER include text, captions, subtitles, watermarks, or text overlays in the prompt — all images must be completely text-free
9. If scene 1 (the hook), do NOT include any product — this is problem-aware content before the product reveal

Return ONLY the image generation prompt as a single paragraph. No explanations, no markdown."""

        try:
            response = client.models.generate_content(
                model=GEMINI_VIDEO_MODEL,
                contents=prompt
            )
            image_prompt = response.text.strip()
        except Exception as e:
            log(3, f"  WARNING: Failed to generate prompt for scene {analysis['scene_number']}: {e}")
            image_prompt = f"Scene {analysis['scene_number']}: {analysis.get('description', 'unknown')} — adapted for {brand}"

        brand_prompts.append({
            "scene_number": analysis["scene_number"],
            "timestamp": analysis["timestamp"],
            "duration": analysis["duration"],
            "image_prompt": image_prompt,
            "motion_description": analysis.get("motion", "static"),
            "narrative_role": scene_cd.get("narrative_role", "") if scene_cd else "",
            "generation_mode": scene_cd.get("generation_mode", "image_to_image") if scene_cd else "image_to_image",
            "include_product": scene_cd.get("include_product", False) if scene_cd else True,
            "scene_category": analysis.get("scene_category", ""),
            "reference_analysis": analysis
        })

        time.sleep(1)

    prompts_path = os.path.join(prompts_dir, "image_prompts.json")
    with open(prompts_path, "w") as f:
        json.dump(brand_prompts, f, indent=2)

    log(3, f"Brand prompts generated — saved to {prompts_path}")
    return brand_prompts


# ---------------------------------------------------------------------------
# Stage 3b: Visual Validation (Gemini compares generated vs reference)
# ---------------------------------------------------------------------------

def validate_generated_image(generated_path, reference_path, scene_description, client):
    """Use Gemini to visually compare a generated image against the reference keyframe.
    Checks composition, camera angle, framing, and structural fidelity.
    Returns (passed: bool, reason: str)."""
    if not generated_path or not os.path.exists(generated_path):
        return True, "No generated image to validate"
    if not reference_path or not os.path.exists(reference_path):
        return True, "No reference to validate against"

    try:
        gen_bytes = open(generated_path, "rb").read()
        ref_bytes = open(reference_path, "rb").read()

        response = client.models.generate_content(
            model=GEMINI_VIDEO_MODEL,
            contents=types.Content(
                parts=[
                    types.Part(inline_data=types.Blob(data=ref_bytes, mime_type="image/png")),
                    types.Part(inline_data=types.Blob(data=gen_bytes, mime_type="image/png")),
                    types.Part(text=(
                        f"Image 1 is the REFERENCE frame from a video scene. "
                        f"Image 2 is a GENERATED adaptation of that scene for a different brand.\n\n"
                        f"Scene description: {scene_description}\n\n"
                        f"Evaluate whether the generated image is a faithful 1:1 replication of the reference in terms of:\n"
                        f"1. Same composition and layout (subject placement, framing)\n"
                        f"2. Same camera angle (close-up, medium, wide, overhead, etc.)\n"
                        f"3. Same type of action/subject matter (person doing same thing, same setting type)\n"
                        f"4. Same visual mood and lighting direction\n"
                        f"5. No hallucinated elements that weren't in the reference\n\n"
                        f"Minor brand/product changes are EXPECTED and should NOT cause a failure.\n"
                        f"FAIL only if the composition, angle, or subject matter fundamentally diverges.\n\n"
                        f"Reply with ONLY 'PASS' or 'FAIL' followed by a one-sentence reason."
                    ))
                ]
            )
        )

        result = response.text.strip()
        passed = result.upper().startswith("PASS")
        return passed, result

    except Exception as e:
        # On error, pass through to avoid blocking the pipeline
        return True, f"Validation error (passing through): {e}"


# ---------------------------------------------------------------------------
# Stage 4: Image Generation (Nano Banana 2 — Image-to-Image)
# ---------------------------------------------------------------------------

def generate_images(brand_prompts, scenes, product_images, output_dir):
    """Generate brand-adapted images using Nano Banana 2 (image-to-image).

    Always uses image-to-image mode with the reference keyframe guiding composition.
    Falls back to text-only generation if no reference keyframe is available.

    Product timing is per-scene (include_product flag from creative direction).
    The creative strategist decides when the product appears in the narrative.
    """
    gen_dir = ensure_dir(os.path.join(output_dir, "generated"))
    client = genai.Client(api_key=GEMINI_API_KEY)

    # Build a lookup from scene_number → keyframe path
    keyframe_map = {}
    for s in scenes:
        keyframe_map[s["scene_number"]] = s["keyframe"]

    # Pre-load product reference images (if any) as bytes
    product_parts = []
    for pimg in (product_images or []):
        if os.path.exists(pimg):
            ext = Path(pimg).suffix.lower()
            mime = "image/jpeg" if ext in (".jpg", ".jpeg") else f"image/{ext.lstrip('.')}"
            with open(pimg, "rb") as f:
                product_parts.append(
                    types.Part(inline_data=types.Blob(data=f.read(), mime_type=mime))
                )
            log(4, f"Loaded product reference: {os.path.basename(pimg)}")

    generated = []

    for bp in brand_prompts:
        scene_num = f"{bp['scene_number']:03d}"
        out_path = os.path.join(gen_dir, f"scene_{scene_num}_brand.png")

        # Skip if already generated
        if os.path.exists(out_path):
            log(4, f"Scene {bp['scene_number']} already generated — skipping")
            generated.append({"scene_number": bp["scene_number"], "image_path": out_path})
            continue

        # ALWAYS use image_to_image — reference frame is the source of truth
        # Text-to-image produces hallucinated compositions that don't match the reference
        gen_mode = "image_to_image"
        include_product_cd = bp.get("include_product", True)

        # For PRODUCT_SHOT scenes, always force product reference inclusion
        scene_category = bp.get("scene_category", "")
        if scene_category == "PRODUCT_SHOT":
            include_product_cd = True

        # Get the reference keyframe for this scene
        ref_keyframe = keyframe_map.get(bp["scene_number"])

        # Check if the REFERENCE scene had a product (product only when reference had one)
        ref_analysis = bp.get("reference_analysis", {})
        key_elements = [e.lower() for e in ref_analysis.get("key_elements", [])]
        scene_desc = ref_analysis.get("description", "").lower()
        product_keywords = {
            # Supplements / consumables
            "bottle", "gummy", "gummies", "supplement", "jar", "container",
            "pouch", "pill", "capsule", "packaging",
            # Fashion / accessories / bags
            "bag", "tote", "handbag", "purse", "clutch", "backpack",
            "weekender", "luggage", "satchel", "duffel", "crossbody",
            # General product terms
            "product", "package", "box", "label", "device", "gadget",
            "appliance", "tool", "item", "merchandise",
        }
        ref_has_product = any(
            kw in elem for elem in key_elements for kw in product_keywords
        ) or any(kw in scene_desc for kw in product_keywords)

        # Product is included ONLY if: reference had product AND creative direction says yes
        use_product = ref_has_product and include_product_cd and bool(product_parts)

        log(4, f"Generating image for scene {bp['scene_number']}/{len(brand_prompts)} ({gen_mode})...")

        try:
            if ref_keyframe and os.path.exists(ref_keyframe):
                # --- IMAGE-TO-IMAGE: Structure maps, use reference frame ---
                ref_bytes = open(ref_keyframe, "rb").read()
                parts = [
                    types.Part(inline_data=types.Blob(data=ref_bytes, mime_type="image/png"))
                ]

                product_note = ""
                if use_product:
                    parts.extend(product_parts)
                    product_note = (
                        "I've also included a product reference image. "
                        "Replicate this product EXACTLY — same shape, label, colors, branding. "
                    )
                    log(4, f"  Including product reference (image-to-image + product)")
                elif not ref_has_product:
                    product_note = (
                        "Do NOT add any product, bottle, or branded item to this scene. "
                    )

                # Category-specific prompt engineering for screenshot/overlay scenes
                # CRITICAL: These categories generate STANDALONE assets (no talking head)
                # The editor composites them onto the AIUGC footage in post-production
                category_prefix = ""
                if scene_category == "GRAPHIC_OVERLAY":
                    category_prefix = (
                        "This scene has a medical/science diagram overlaid on a talking head. "
                        "Generate ONLY the diagram itself as a STANDALONE graphic on a clean white/light background. "
                        "Do NOT include any person, talking head, or video frame — JUST the isolated diagram/illustration. "
                        "The editor will overlay this onto the video in post-production. "
                        "Create a clean medical illustration adapted for the target brand. "
                    )
                elif scene_category == "RESEARCH_SCREENSHOT":
                    category_prefix = (
                        "This scene has a research citation/study card overlaid on a talking head. "
                        "Generate ONLY the research card itself as a STANDALONE graphic — NO person, NO talking head, NO video frame. "
                        "Create an isolated research citation card on a clean rounded rectangle background with: "
                        "study title, brief excerpt, relevant ingredient illustration, and chemical structure diagram. "
                        "The editor will overlay this card onto the video in post-production. "
                    )
                elif scene_category == "WEBSITE_SCREENSHOT":
                    # NOTE: For website screenshots, the pipeline should ideally take a REAL
                    # screenshot of the brand's actual website using Playwright/headless browser,
                    # not AI-generate a fake one. When invoking the skill, Claude should:
                    # 1. Check if the brand has a registered website URL in the vault
                    # 2. Use Playwright to take a real mobile screenshot
                    # 3. Save it directly instead of going through Nano Banana 2
                    # If no website URL is available, fall back to AI generation:
                    category_prefix = (
                        "This scene shows a product website screenshot. "
                        "Generate ONLY the website screenshot itself as a STANDALONE graphic — NO person behind it, NO talking head. "
                        "Create an isolated product page mockup showing: brand name, product image, star rating, reviews, "
                        "benefit icons, product description, and key selling points. "
                        "The editor will overlay this onto the video in post-production. "
                        "NOTE: A real website screenshot is preferred over AI generation. "
                    )
                elif scene_category == "STATISTICS_OVERLAY":
                    category_prefix = (
                        "This scene has statistics/data as the primary visual. "
                        "Generate ONLY the data graphic itself as a STANDALONE asset — NO person, NO talking head, NO video frame. "
                        "Create an isolated data visualization (chart, comparison card, stat callout) on a clean background. "
                        "The editor will overlay this onto the video in post-production. "
                    )

                edit_prompt = (
                    f"{category_prefix}"
                    f"Edit this reference scene image to adapt it for a different brand. "
                    f"Replicate the scene 1:1 — EXACT same composition, camera angle, lighting, framing, and visual style. "
                    f"Only change the product/brand elements that already exist in the reference. "
                    f"Do NOT invent or add elements that are not in the original scene. "
                    f"{product_note}"
                    f"\n\nADAPTATION INSTRUCTIONS:\n{bp['image_prompt']}"
                )
                parts.append(types.Part(text=edit_prompt))

                response = client.models.generate_content(
                    model=GEMINI_IMAGE_MODEL,
                    contents=types.Content(parts=parts),
                    config=types.GenerateContentConfig(
                        response_modalities=["IMAGE", "TEXT"],
                    )
                )

            else:
                # HARD RULE: No text-to-image fallback. Skip scene if no reference keyframe.
                log(4, f"  No reference keyframe — SKIPPING (image-to-image required, no text-to-image fallback)")
                failed += 1
                continue

            # Extract image from response
            saved = False
            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    img_data = part.inline_data.data
                    with open(out_path, "wb") as f:
                        f.write(img_data)
                    saved = True
                    log(4, f"  Saved: {out_path}")
                    break

            if not saved:
                log(4, f"  WARNING: No image returned for scene {bp['scene_number']}")
                out_path = None

        except Exception as e:
            log(4, f"  ERROR generating scene {bp['scene_number']}: {e}")
            out_path = None
            time.sleep(5)  # Back off on error

        # --- Gemini Visual Validation ---
        # Compare generated image against reference keyframe
        if out_path and ref_keyframe and os.path.exists(ref_keyframe):
            passed, reason = validate_generated_image(
                out_path, ref_keyframe, bp.get("image_prompt", ""), client
            )
            if not passed:
                log(4, f"  VALIDATION FAILED: {reason}")
                # Retry with stricter prompt (up to MAX_IMAGE_VALIDATION_RETRIES)
                for retry_num in range(MAX_IMAGE_VALIDATION_RETRIES):
                    log(4, f"  Retrying ({retry_num + 1}/{MAX_IMAGE_VALIDATION_RETRIES}) with stricter composition enforcement...")
                    try:
                        ref_bytes_retry = open(ref_keyframe, "rb").read()
                        retry_parts = [
                            types.Part(inline_data=types.Blob(data=ref_bytes_retry, mime_type="image/png"))
                        ]
                        if use_product and product_parts:
                            retry_parts.extend(product_parts)

                        retry_prompt = (
                            f"CRITICAL: Your previous attempt did NOT match the reference composition. "
                            f"You MUST replicate this reference image with EXACT same:\n"
                            f"- Camera angle and perspective\n"
                            f"- Subject placement and framing\n"
                            f"- Scene layout and spatial composition\n"
                            f"- Type of action shown\n"
                            f"- Lighting direction\n"
                            f"Only change brand/product elements. Everything else must be 1:1.\n"
                            f"Previous failure reason: {reason}\n"
                            f"IMPORTANT: Do NOT add any text, captions, subtitles, watermarks, logos, or text overlays.\n"
                            f"\n\nADAPTATION INSTRUCTIONS:\n{bp['image_prompt']}"
                        )
                        retry_parts.append(types.Part(text=retry_prompt))

                        retry_response = client.models.generate_content(
                            model=GEMINI_IMAGE_MODEL,
                            contents=types.Content(parts=retry_parts),
                            config=types.GenerateContentConfig(
                                response_modalities=["IMAGE", "TEXT"],
                            )
                        )

                        retry_saved = False
                        for part in retry_response.candidates[0].content.parts:
                            if part.inline_data is not None:
                                with open(out_path, "wb") as f:
                                    f.write(part.inline_data.data)
                                retry_saved = True
                                break

                        if retry_saved:
                            passed2, reason2 = validate_generated_image(
                                out_path, ref_keyframe, bp.get("image_prompt", ""), client
                            )
                            if passed2:
                                log(4, f"  Retry {retry_num + 1} PASSED: {reason2}")
                                break
                            else:
                                log(4, f"  Retry {retry_num + 1} still failed: {reason2}")
                        else:
                            log(4, f"  Retry {retry_num + 1}: no image returned")

                    except Exception as e:
                        log(4, f"  Retry {retry_num + 1} error: {e}")

                    time.sleep(3)
            else:
                log(4, f"  Validation PASSED: {reason}")

        generated.append({"scene_number": bp["scene_number"], "image_path": out_path})
        time.sleep(2)  # Rate limiting for image gen

    log(4, f"Generated {sum(1 for g in generated if g.get('image_path'))} / {len(brand_prompts)} images")
    return generated


# ---------------------------------------------------------------------------
# Stage 5: Motion Prompts for Kling
# ---------------------------------------------------------------------------

def build_motion_prompts(brand_prompts, generated_images):
    """Combine motion analysis with brand prompts for Kling animation."""
    motion_prompts = []

    for bp, gi in zip(brand_prompts, generated_images):
        motion_desc = bp.get("motion_description", "static")
        scene_desc = bp["image_prompt"]

        # Build a Kling-compatible motion prompt
        kling_prompt = f"{scene_desc}. Motion: {motion_desc}"

        # Cap at 2500 chars (Kling limit)
        if len(kling_prompt) > 2500:
            kling_prompt = kling_prompt[:2497] + "..."

        motion_prompts.append({
            "scene_number": bp["scene_number"],
            "image_path": gi["image_path"],
            "kling_prompt": kling_prompt,
            "duration": str(min(int(bp.get("duration", 5)), 10)),  # Kling max 10s
            "motion_raw": motion_desc
        })

    log(5, f"Built {len(motion_prompts)} motion prompts for Kling")
    return motion_prompts


# ---------------------------------------------------------------------------
# Stage 6: Kling 3.0 Animation
# ---------------------------------------------------------------------------

def upload_image_for_kling(image_path):
    """Upload image to kie.ai's file hosting so Kling can access it via URL.
    Uses redpandaai.co file-stream-upload (same API key, files expire after 3 days)."""
    KIE_UPLOAD_URL = "https://kieai.redpandaai.co/api/file-stream-upload"
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
        else:
            log(6, f"  Upload to kie.ai failed: {data}")
    except Exception as e:
        log(6, f"  Upload to kie.ai error: {e}")

    return None


def animate_scenes(motion_prompts, product_images, output_dir):
    """Animate generated images using Kling 3.0 via kie.ai."""
    anim_dir = ensure_dir(os.path.join(output_dir, "animated"))

    headers = {
        "Authorization": f"Bearer {KIE_API_KEY}",
        "Content-Type": "application/json"
    }

    results = []

    # Pre-upload product images once (cache URLs for all scenes)
    product_image_urls = []
    if product_images:
        for pimg in product_images[:3]:
            if os.path.exists(pimg):
                pimg_url = upload_image_for_kling(pimg)
                if pimg_url:
                    log(6, f"Product image uploaded: {pimg_url}")
                    product_image_urls.append(pimg_url)

    for mp in motion_prompts:
        scene_num = f"{mp['scene_number']:03d}"
        out_path = os.path.join(anim_dir, f"scene_{scene_num}_animated.mp4")

        # Skip if already done
        if os.path.exists(out_path):
            log(6, f"Scene {mp['scene_number']} already animated — skipping")
            results.append({"scene_number": mp["scene_number"], "video_path": out_path, "status": "cached"})
            continue

        if not mp["image_path"] or not os.path.exists(mp["image_path"]):
            log(6, f"Scene {mp['scene_number']} — no image available, skipping")
            results.append({"scene_number": mp["scene_number"], "video_path": None, "status": "skipped"})
            continue

        log(6, f"Animating scene {mp['scene_number']}/{len(motion_prompts)}...")

        # Upload image to temp host so Kling can access via URL
        image_url = upload_image_for_kling(mp["image_path"])
        if not image_url:
            log(6, f"  FAILED: Could not upload image for scene {mp['scene_number']}")
            results.append({"scene_number": mp["scene_number"], "video_path": None, "status": "upload_failed"})
            continue

        log(6, f"  Image uploaded: {image_url}")

        # Build the Kling request
        duration = mp.get("duration", "5")
        if int(duration) < 3:
            duration = "3"
        if int(duration) > 10:
            duration = "10"

        payload = {
            "model": "kling-3.0/video",
            "input": {
                "prompt": mp["kling_prompt"],
                "image_urls": [image_url],
                "sound": False,
                "duration": duration,
                "aspect_ratio": "9:16",
                "mode": "pro",
                "multi_shots": False
            }
        }

        # Add product images as kling_elements if available (use cached URLs)
        if product_images and product_image_urls:
            elements = []
            for idx, pimg_url in enumerate(product_image_urls[:3]):
                elements.append({
                    "name": f"product_{idx+1}",
                    "description": f"Brand product reference image {idx+1}",
                    "element_input_urls": [pimg_url]
                })
            if elements:
                payload["input"]["kling_elements"] = elements

        # Submit task
        success = False
        for attempt in range(MAX_KLING_RETRIES):
            try:
                resp = requests.post(KIE_CREATE_URL, headers=headers, json=payload, timeout=60)
                resp_data = resp.json()

                if resp_data.get("code") != 200:
                    log(6, f"  Attempt {attempt+1} failed: {resp_data.get('msg', 'unknown error')}")
                    time.sleep(10)
                    continue

                task_id = resp_data["data"]["taskId"]
                log(6, f"  Task submitted: {task_id}")

                # Poll for completion
                video_url = poll_kling_task(task_id, headers)

                if video_url:
                    # Download the video
                    vid_resp = requests.get(video_url, timeout=120)
                    with open(out_path, "wb") as f:
                        f.write(vid_resp.content)
                    log(6, f"  Saved: {out_path}")
                    results.append({"scene_number": mp["scene_number"], "video_path": out_path, "status": "success"})
                    success = True
                    break
                else:
                    log(6, f"  Attempt {attempt+1}: generation timed out or failed")

            except Exception as e:
                log(6, f"  Attempt {attempt+1} error: {e}")
                time.sleep(10)

        if not success:
            log(6, f"  FAILED: Scene {mp['scene_number']} could not be animated after {MAX_KLING_RETRIES} attempts")
            results.append({"scene_number": mp["scene_number"], "video_path": None, "status": "failed"})

        time.sleep(5)  # Rate limiting between scenes

    succeeded = sum(1 for r in results if r["status"] == "success" or r["status"] == "cached")
    log(6, f"Animation complete: {succeeded}/{len(motion_prompts)} scenes")
    return results


def poll_kling_task(task_id, headers, max_wait=600):
    """Poll Kling task status until complete or timeout."""
    start = time.time()
    while time.time() - start < max_wait:
        try:
            resp = requests.get(
                KIE_STATUS_URL,
                headers=headers,
                params={"taskId": task_id},
                timeout=30
            )
            data = resp.json()

            if data.get("code") != 200:
                time.sleep(KLING_POLL_INTERVAL)
                continue

            state = data["data"].get("state", "")

            if state == "success":
                result_json = json.loads(data["data"].get("resultJson", "{}"))
                urls = result_json.get("resultUrls", [])
                if urls:
                    return urls[0]
                return None

            elif state == "fail":
                fail_msg = data["data"].get("failMsg", "unknown")
                log(6, f"    Kling task failed: {fail_msg}")
                return None

            else:
                elapsed = int(time.time() - start)
                log(6, f"    Status: {state} ({elapsed}s elapsed)")

        except Exception as e:
            log(6, f"    Poll error: {e}")

        time.sleep(KLING_POLL_INTERVAL)

    log(6, f"    Timeout waiting for task {task_id}")
    return None


# ---------------------------------------------------------------------------
# Stage 7: Google Drive Upload
# ---------------------------------------------------------------------------

def get_drive_service():
    """Authenticate to Google Drive via OAuth2 using client ID/secret.
    First run opens a browser for consent. Token is cached for future runs."""
    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build
    except ImportError:
        log(7, "Google Drive API packages not installed. Run:")
        log(7, "  pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")
        return None

    SCOPES = ["https://www.googleapis.com/auth/drive.file"]

    creds = None
    if os.path.exists(GDRIVE_TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(GDRIVE_TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Build client config from embedded credentials
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
    """Upload animated B-roll clips + assembly guide to Google Drive."""
    from googleapiclient.http import MediaFileUpload

    service = get_drive_service()
    if not service:
        return None

    # Create subfolder
    date_str = datetime.now().strftime("%Y-%m-%d")
    folder_name = f"{brand}_{date_str}_replicator"

    folder_metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [drive_folder_id]
    }
    folder = service.files().create(body=folder_metadata, fields="id").execute()
    parent_id = folder.get("id")
    log(7, f"Created Drive folder: {folder_name}")

    upload_count = 0

    # Upload animated B-roll clips (the final deliverable)
    anim_dir = os.path.join(output_dir, "animated")
    if os.path.exists(anim_dir):
        for filename in sorted(os.listdir(anim_dir)):
            filepath = os.path.join(anim_dir, filename)
            if not os.path.isfile(filepath):
                continue

            ext = Path(filepath).suffix.lower()
            mime = "video/mp4" if ext == ".mp4" else "application/octet-stream"

            file_metadata = {"name": filename, "parents": [parent_id]}
            media = MediaFileUpload(filepath, mimetype=mime, resumable=True)
            service.files().create(body=file_metadata, media_body=media, fields="id").execute()
            upload_count += 1
            log(7, f"  Uploaded: {filename}")

    # Upload assembly guide
    guide_path = os.path.join(output_dir, "assembly_guide.md")
    if os.path.exists(guide_path):
        file_metadata = {"name": "assembly_guide.md", "parents": [parent_id]}
        media = MediaFileUpload(guide_path, mimetype="text/markdown", resumable=True)
        service.files().create(body=file_metadata, media_body=media, fields="id").execute()
        upload_count += 1

    log(7, f"Uploaded {upload_count} files to Drive folder '{folder_name}'")
    return parent_id


# ---------------------------------------------------------------------------
# Assembly Guide
# ---------------------------------------------------------------------------

def write_assembly_guide(brand_prompts, animation_results, output_dir, brand):
    """Write a shot list / assembly guide for the video editor."""
    guide_path = os.path.join(output_dir, "assembly_guide.md")

    lines = [
        f"# Assembly Guide — {brand} Video Replicator",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## Shot List",
        "",
        "| Scene | Timestamp | Duration | Status | File |",
        "|-------|-----------|----------|--------|------|",
    ]

    for bp, ar in zip(brand_prompts, animation_results):
        status = ar.get("status", "unknown")
        filename = os.path.basename(ar["video_path"]) if ar.get("video_path") else "N/A"
        ts = f"{bp['timestamp']:.1f}s"
        dur = f"{bp['duration']}s"
        lines.append(f"| {bp['scene_number']} | {ts} | {dur} | {status} | {filename} |")

    lines.extend([
        "",
        "## Scene Details",
        "",
    ])

    for bp in brand_prompts:
        ref = bp.get("reference_analysis", {})
        lines.extend([
            f"### Scene {bp['scene_number']} ({bp['timestamp']:.1f}s)",
            f"**Motion:** {bp.get('motion_raw', 'N/A')}",
            f"**Mood:** {ref.get('mood', 'N/A')}",
            f"**Description:** {ref.get('description', 'N/A')}",
            "",
        ])

    with open(guide_path, "w") as f:
        f.write("\n".join(lines))

    log("G", f"Assembly guide saved to {guide_path}")


# ---------------------------------------------------------------------------
# Main Pipeline
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Video Scene Replicator Pipeline")
    parser.add_argument("--video", required=True, help="Path to reference video")
    parser.add_argument("--brand", required=True, help="Target brand name")
    parser.add_argument("--product-context", default="", help="Product description / context (auto-loaded from vault if brand is registered)")
    parser.add_argument("--style", default="", help="Style notes (e.g. 'claymation, soft pastel')")
    parser.add_argument("--drive-folder", default="", help="Google Drive folder ID for upload")
    parser.add_argument("--product-images", default="", help="Comma-separated product image paths")
    parser.add_argument("--output-dir", default="./replicator-output", help="Local output directory")
    parser.add_argument("--scene-threshold", type=float, default=SCENE_THRESHOLD, help="Scene detection sensitivity (0-1, lower=more scenes)")
    parser.add_argument("--interval", type=float, default=0.0, help="Extract keyframes at fixed intervals (seconds) instead of scene detection. Best for animated/smooth-transition video. 0=auto (use scene detection with fallback)")
    parser.add_argument("--creative-brief", default="", help="Path to creative direction JSON from creative strategist. Overrides Stage 3 auto-prompts with conceptual adaptation.")
    parser.add_argument("--skip-animation", action="store_true", help="Skip Kling animation (stages 5-6)")
    parser.add_argument("--skip-upload", action="store_true", help="Skip Google Drive upload (stage 7)")
    parser.add_argument("--skip-classification", action="store_true", help="Skip smart scene classification (process all scenes)")
    parser.add_argument("--force-reclassify", action="store_true", help="Force re-classification even if cached")
    parser.add_argument("--require-approval", action="store_true", help="Pause after image generation (Stage 4) for human approval before animating")

    args = parser.parse_args()

    # Validate
    if not os.path.exists(args.video):
        print(f"ERROR: Video file not found: {args.video}")
        sys.exit(1)

    output_dir = os.path.abspath(args.output_dir)
    ensure_dir(output_dir)

    product_images = [p.strip() for p in args.product_images.split(",") if p.strip()] if args.product_images else []

    # Auto-load brand knowledge from vault
    brand_data = load_brand_knowledge(args.brand)
    brand_knowledge_text = brand_data["context_text"]

    # Use default product context from registry if none provided
    product_context = args.product_context
    if not product_context and brand_data["default_product_context"]:
        product_context = brand_data["default_product_context"]
        print(f"[Brand] Using default product context: {product_context}")

    # Merge product images: CLI args take priority, fall back to registry
    if not product_images and brand_data["product_images"]:
        product_images = brand_data["product_images"]
        print(f"[Brand] Using registered product images: {[os.path.basename(p) for p in product_images]}")

    print("=" * 60)
    print("VIDEO SCENE REPLICATOR")
    print("=" * 60)
    print(f"Reference: {args.video}")
    print(f"Brand:     {args.brand}")
    print(f"Knowledge: {len(brand_knowledge_text)} chars from vault")
    print(f"Product:   {product_context}")
    print(f"Style:     {args.style or '(auto-detect from reference)'}")
    print(f"Output:    {output_dir}")
    print("=" * 60)

    progress = load_progress(output_dir)

    # Stage 1: Extract scenes
    scenes = extract_scenes(args.video, output_dir, args.scene_threshold, interval=args.interval)

    # Stage 1.5: Smart Scene Classification
    # Classifies each scene by type (talking head, science animation, product shot, etc.)
    # so the pipeline only processes scenes that need replication — skips talking heads
    classifications = None
    if not args.skip_classification:
        if args.force_reclassify:
            # Delete cached classification
            cached = os.path.join(output_dir, "analysis", "scene_classification.json")
            if os.path.exists(cached):
                os.remove(cached)
        classifications = classify_scenes(
            args.video, scenes, args.brand, product_context, output_dir
        )
    else:
        log("1.5", "Skipping scene classification (--skip-classification) — all scenes will be processed")

    # Stage 2: Analyze scenes (skips TALKING_HEAD and END_CARD if classified)
    analyses = analyze_scenes(scenes, output_dir, classifications=classifications)

    # Stage 2.5: Creative Strategist Holistic Adaptation (watches full video)
    # Uploads the ENTIRE video to Gemini for holistic understanding, then designs
    # a scene-by-scene conceptual adaptation — not just brand swap.
    creative_direction = None
    if args.creative_brief and os.path.exists(args.creative_brief):
        # Load pre-authored creative brief from creative strategist
        log("2.5", f"Loading creative direction from: {args.creative_brief}")
        with open(args.creative_brief) as f:
            creative_direction = json.load(f)
        log("2.5", f"Loaded creative direction with {len(creative_direction.get('scenes', []))} scene directives")
    else:
        # Auto-generate creative direction by having Gemini watch the full video
        creative_direction = generate_creative_direction(
            args.video, analyses, args.brand, product_context,
            brand_knowledge_text, output_dir
        )

    # Inject scene_category from classification into analyses for downstream use
    if classifications:
        cls_lookup = {c.get("scene_number"): c.get("category", "") for c in classifications}
        for a in analyses:
            a["scene_category"] = cls_lookup.get(a.get("scene_number"), "")

    # Stage 3: Generate brand prompts (with creative direction)
    brand_prompts = generate_brand_prompts(
        analyses, args.brand, product_context, args.style, output_dir,
        brand_knowledge=brand_knowledge_text,
        creative_direction=creative_direction,
    )

    # Stage 4: Generate images (image-to-image via Nano Banana 2)
    generated = generate_images(brand_prompts, scenes, product_images, output_dir)

    # Human Approval Gate — pause for review before animating
    if args.require_approval:
        gen_dir = os.path.join(output_dir, "generated")
        print("\n" + "=" * 60)
        print("APPROVAL REQUIRED")
        print("=" * 60)
        print(f"Generated images are ready for review at:")
        print(f"  {gen_dir}")
        print(f"\nTotal images: {len([g for g in generated if g.get('image_path')])}")
        print(f"\nReview the images. Delete any you want to skip.")
        print(f"When ready, press ENTER to continue to animation...")
        print("=" * 60)
        try:
            subprocess.run(["open", gen_dir])  # Open folder on macOS
        except Exception:
            pass
        input()  # Wait for user to press ENTER

        # Re-scan generated directory — user may have deleted rejected images
        remaining = []
        for g in generated:
            if g.get("image_path") and os.path.exists(g["image_path"]):
                remaining.append(g)
            else:
                log(4, f"Scene {g['scene_number']} removed by user — skipping animation")
        generated = remaining
        print(f"\nProceeding with {len(generated)} approved images...")

    if not args.skip_animation:
        # Stage 5: Build motion prompts
        motion_prompts = build_motion_prompts(brand_prompts, generated)

        # Stage 6: Animate with Kling
        animation_results = animate_scenes(motion_prompts, product_images, output_dir)
    else:
        log(5, "Skipping animation (--skip-animation)")
        log(6, "Skipping animation (--skip-animation)")
        animation_results = [
            {"scene_number": bp["scene_number"], "video_path": None, "status": "skipped"}
            for bp in brand_prompts
        ]

    # Write assembly guide
    write_assembly_guide(brand_prompts, animation_results, output_dir, args.brand)

    # Stage 7: Upload to Drive
    if args.drive_folder and not args.skip_upload:
        upload_to_drive(output_dir, args.drive_folder, args.brand)
    else:
        if not args.drive_folder:
            log(7, "No Drive folder specified — skipping upload")
        else:
            log(7, "Skipping upload (--skip-upload)")

    # Summary
    print("\n" + "=" * 60)
    print("PIPELINE COMPLETE")
    print("=" * 60)
    total = len(brand_prompts)
    imgs_ok = sum(1 for g in generated if g.get("image_path"))
    anims_ok = sum(1 for a in animation_results if a.get("status") in ("success", "cached"))
    print(f"Scenes detected:    {total}")
    print(f"Images generated:   {imgs_ok}/{total}")
    print(f"Clips animated:     {anims_ok}/{total}")
    print(f"Output directory:   {output_dir}")
    print("=" * 60)


if __name__ == "__main__":
    main()
