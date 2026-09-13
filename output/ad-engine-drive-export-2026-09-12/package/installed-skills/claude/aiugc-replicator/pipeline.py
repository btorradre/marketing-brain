#!/usr/bin/env python3
"""
AI UGC Video Replicator Pipeline
==================================
Takes any reference AI UGC video ad, extracts keyframes at scene shifts,
transforms avatars via Nano Banana 2, animates with Kling 3.0, lip-syncs
with Sync.so, polishes with Kling motion control, and stitches the final
video with FFmpeg.

Usage:
    python3 pipeline.py \
        --video "/path/to/reference.mp4" \
        --voiceover "/path/to/voiceover.mp3" \
        --brand "Motilli" \
        --output-dir "./aiugc-output"

    # Or with a GetHookd URL (auto-downloads the video):
    python3 pipeline.py \
        --video "https://app.gethookd.ai/share/ad/86606845?signature=[REDACTED_SECRET]" \
        --voiceover "/path/to/voiceover.mp3" \
        --brand "Motilli" \
        --output-dir "./aiugc-output"

    # Or with just a GetHookd ad ID:
    python3 pipeline.py \
        --video 86606845 \
        --voiceover "/path/to/voiceover.mp3" \
        --brand "Motilli" \
        --output-dir "./aiugc-output"
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

# Add tools directory to path for gethookd_resolver
sys.path.insert(0, os.path.expanduser("~/Documents/marketing brain/tools"))
from gethookd_resolver import resolve_video_input, is_gethookd_url

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

# ---------------------------------------------------------------------------
# Dependency check
# ---------------------------------------------------------------------------
REQUIRED_PACKAGES = ["google.genai", "PIL", "requests"]

def check_deps():
    missing = []
    try:
        from google import genai  # noqa: F401
    except ImportError:
        missing.append("google-genai")
    try:
        from PIL import Image  # noqa: F401
    except ImportError:
        missing.append("Pillow")
    try:
        import requests  # noqa: F401
    except ImportError:
        missing.append("requests")
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
SYNC_API_KEY = os.environ.get("SYNC_API_KEY", "")  # User must provide Sync.so API key

GDRIVE_CLIENT_ID = "630165550470-bk00miojfehkb5va5hdoupbn170lurhh.apps.googleusercontent.com"
GDRIVE_CLIENT_SECRET = "[REDACTED_SECRET]"
GDRIVE_TOKEN_PATH = os.path.expanduser("~/.claude/skills/aiugc-replicator/gdrive_token.json")

GEMINI_VIDEO_MODEL = "gemini-3-flash-preview"
GEMINI_IMAGE_MODEL = "gemini-3.1-flash-image-preview"  # Nano Banana 2

KIE_CREATE_URL = "https://api.kie.ai/api/v1/jobs/createTask"
KIE_STATUS_URL = "https://api.kie.ai/api/v1/jobs/recordInfo"

SYNC_API_BASE = "https://api.sync.so"
SYNC_GENERATE_URL = f"{SYNC_API_BASE}/v2/generate"

SCENE_THRESHOLD = 0.3
MAX_KLING_RETRIES = 3
KLING_POLL_INTERVAL = 15
SYNC_POLL_INTERVAL = 10
SEGMENT_TARGET_DURATION = 30  # seconds

VAULT_ROOT = os.path.expanduser("~/Documents/marketing brain")

# Brand registry — same as video-scene-replicator
BRAND_REGISTRY = {
    "motilli": {
        "research_docs": [
            os.path.join(VAULT_ROOT, "motilli/Motilli_Master_Copywriting_Brief.md"),
            os.path.join(VAULT_ROOT, "motilli/Motilli_Product_Context.md"),
            os.path.join(VAULT_ROOT, "motilli/Motilli_Avatar_VoC.md"),
        ],
        "product_images": [
            "/Users/brooksorradre2/Documents/marketing brain/brands/motilli/website assets/product reference.png",
            os.path.join(VAULT_ROOT, "motilli/website assets/motilli product reference.png"),
        ],
        "product_images_fallback": [
            "/Users/brooksorradre2/Documents/marketing brain/brands/motilli/website assets/product reference.png",
        ],
        "default_product_context": "Celery juice fiber gummies for GLP-1 users — supports gut health during weight loss medication",
    },
    "lunessa": {
        "research_docs": [
            os.path.join(VAULT_ROOT, "lunessa/fh research docs/Lunessa Research Docs 3.0/Lunessa Avatar Sheet.pdf"),
            os.path.join(VAULT_ROOT, "lunessa/fh research docs/Lunessa Research Docs 3.0/Lunessa_Master_Copywriting_Brief.docx"),
            os.path.join(VAULT_ROOT, "lunessa/menopause research 2.0/Lunessa_Master_Strategic_Brief.docx"),
        ],
        "product_images": [
            os.path.join(VAULT_ROOT, "lunessa/website assets/lunessa spelling corrected .jpg"),
        ],
        "default_product_context": "Heart health supplement for women — supports cholesterol, energy, and cardiovascular restoration",
    },
    "velantra-boat-tote": {
        "research_docs": [],
        "product_images_dir": os.path.join(VAULT_ROOT, "statics/product references/velantra/boat tote"),
        "product_images": [
            os.path.join(VAULT_ROOT, "statics/product references/velantra/boat tote/01.jpg"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/boat tote/02.jpg"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/boat tote/03.jpg"),
        ],
        "default_product_context": "Velantra Boat Tote — premium canvas tote bag with colored leather trim straps, gold turn-lock clasp, Birkin-inspired silhouette",
    },
    "velantra-meridian": {
        "research_docs": [],
        "product_images_dir": os.path.join(VAULT_ROOT, "statics/product references/velantra/meridian"),
        "product_images": [
            os.path.join(VAULT_ROOT, "statics/product references/velantra/meridian/black 1.webp"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/meridian/brown 1.webp"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/meridian/gray 1.webp"),
        ],
        "default_product_context": "Velantra Meridian — leather handbag, silver hardware, structured silhouette",
    },
    "velantra-weekender": {
        "research_docs": [],
        "product_images_dir": os.path.join(VAULT_ROOT, "statics/product references/velantra/weekender"),
        "product_images": [
            os.path.join(VAULT_ROOT, "statics/product references/velantra/weekender/1.webp"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/weekender/2.webp"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/weekender/3.webp"),
        ],
        "default_product_context": "Velantra Weekender — canvas + leather travel bag, olive/cognac and light chocolate/cream colorways",
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


def load_brand_knowledge(brand_key):
    """Load brand research docs from vault."""
    brand = BRAND_REGISTRY.get(brand_key.lower().replace(" ", "-"))
    if not brand:
        return "", [], ""

    knowledge_chunks = []
    for doc_path in brand.get("research_docs", []):
        if not os.path.exists(doc_path):
            continue
        ext = Path(doc_path).suffix.lower()
        try:
            if ext == ".md":
                with open(doc_path, "r") as f:
                    knowledge_chunks.append(f.read())
            elif ext == ".docx":
                try:
                    import docx
                    doc = docx.Document(doc_path)
                    knowledge_chunks.append("\n".join(p.text for p in doc.paragraphs))
                except ImportError:
                    pass
            elif ext == ".pdf":
                try:
                    from pdfminer.high_level import extract_text
                    knowledge_chunks.append(extract_text(doc_path))
                except ImportError:
                    pass
        except Exception as e:
            log("B", f"  Warning: could not read {doc_path}: {e}")

    knowledge = "\n\n---\n\n".join(knowledge_chunks)[:30000]

    product_images = []
    for img_path in brand.get("product_images", []):
        if os.path.exists(img_path):
            product_images.append(img_path)
    if not product_images:
        for img_path in brand.get("product_images_fallback", []):
            if os.path.exists(img_path):
                product_images.append(img_path)

    default_context = brand.get("default_product_context", "")
    return knowledge, product_images, default_context


def get_video_duration(video_path):
    """Get video duration in seconds using ffprobe."""
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", video_path],
            capture_output=True, text=True, timeout=30
        )
        return float(result.stdout.strip())
    except Exception:
        return 0.0


# ---------------------------------------------------------------------------
# Stage 1: Scene Detection & Keyframe Extraction
# ---------------------------------------------------------------------------

def extract_scenes(video_path, output_dir, threshold=SCENE_THRESHOLD):
    """Detect scene changes and extract keyframes + clips."""
    scenes_dir = ensure_dir(os.path.join(output_dir, "scenes"))

    # Get video duration
    duration = get_video_duration(video_path)
    log(1, f"Video duration: {duration:.1f}s")

    # Scene detection — get timestamps
    cmd = [
        "ffmpeg", "-i", video_path,
        "-filter:v", f"select='gt(scene\\,{threshold})',showinfo",
        "-vsync", "vfr", "-f", "null", "-"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    stderr = result.stderr

    # Parse timestamps from showinfo output
    timestamps = [0.0]  # Always include the first frame
    for line in stderr.split("\n"):
        if "pts_time:" in line:
            match = re.search(r"pts_time:(\d+\.?\d*)", line)
            if match:
                ts = float(match.group(1))
                if ts - timestamps[-1] > 1.0:  # Min 1s between scenes
                    timestamps.append(ts)

    log(1, f"Detected {len(timestamps)} scene(s)")

    # Fallback: if too few scenes, extract at regular intervals
    if len(timestamps) < 3 and duration > 10:
        interval = min(5.0, duration / 6)
        timestamps = [i * interval for i in range(int(duration / interval) + 1)]
        log(1, f"Fallback: extracting at {interval:.1f}s intervals ({len(timestamps)} frames)")

    # Extract keyframes and clips
    scenes = []
    for i, ts in enumerate(timestamps):
        scene_num = i + 1
        keyframe_path = os.path.join(scenes_dir, f"scene_{scene_num:03d}.png")
        clip_path = os.path.join(scenes_dir, f"scene_{scene_num:03d}_clip.mp4")

        # Calculate scene duration (until next scene or end)
        next_ts = timestamps[i + 1] if i + 1 < len(timestamps) else duration
        scene_duration = next_ts - ts

        # Extract keyframe
        if not os.path.exists(keyframe_path):
            subprocess.run(
                ["ffmpeg", "-ss", str(ts), "-i", video_path,
                 "-vframes", "1", "-q:v", "2", keyframe_path, "-y"],
                capture_output=True, timeout=30
            )

        # Extract short clip (up to 5s) for motion reference
        clip_dur = min(5.0, scene_duration)
        if not os.path.exists(clip_path):
            subprocess.run(
                ["ffmpeg", "-ss", str(ts), "-i", video_path,
                 "-t", str(clip_dur), "-c:v", "libx264", "-crf", "23",
                 clip_path, "-y"],
                capture_output=True, timeout=30
            )

        scenes.append({
            "scene_number": scene_num,
            "timestamp": ts,
            "duration": scene_duration,
            "keyframe_path": keyframe_path if os.path.exists(keyframe_path) else None,
            "clip_path": clip_path if os.path.exists(clip_path) else None,
        })

    log(1, f"Extracted {len(scenes)} keyframes + clips")
    return scenes, duration


# ---------------------------------------------------------------------------
# Stage 2: Scene Analysis via Gemini
# ---------------------------------------------------------------------------

def analyze_scenes(scenes, output_dir):
    """Analyze each scene with Gemini to get composition, motion, scene_type, etc."""
    analysis_dir = ensure_dir(os.path.join(output_dir, "analysis"))
    analysis_path = os.path.join(analysis_dir, "scene_analysis.json")

    if os.path.exists(analysis_path):
        log(2, "Scene analysis already exists — loading from cache")
        with open(analysis_path, "r") as f:
            return json.load(f)

    client = genai.Client(api_key=GEMINI_API_KEY)
    analyses = []

    for scene in scenes:
        if not scene["keyframe_path"]:
            analyses.append({"scene_number": scene["scene_number"], "error": "no keyframe"})
            continue

        log(2, f"Analyzing scene {scene['scene_number']}/{len(scenes)}...")

        # Build content parts
        parts = []
        try:
            img = Image.open(scene["keyframe_path"])
            parts.append(types.Part.from_image(img))
        except Exception as e:
            log(2, f"  Could not load image: {e}")
            analyses.append({"scene_number": scene["scene_number"], "error": str(e)})
            continue

        prompt = """Analyze this video frame from an AI-generated UGC video ad. Return a JSON object with EXACTLY these fields:

{
    "description": "What is happening in this scene",
    "composition": "Framing, layout, camera positioning",
    "style": "Visual style (studio, outdoor, graphic, etc.)",
    "motion": "Expected body movement, gestures, camera movement based on the pose",
    "scene_type": "ONE of: talking-head, multi-person, b-roll, product, graphic, text-overlay",
    "who_is_speaking": "Description of who appears to be speaking (or 'none' for non-speaking scenes)",
    "key_elements": ["list", "of", "visible", "objects", "and", "elements"],
    "mood": "Emotional tone",
    "camera_angle": "ONE of: wide, medium, close-up, extreme-close-up, over-shoulder, bird-eye, low-angle",
    "background": "Description of the background/setting",
    "num_people": 0,
    "has_product": false,
    "has_text_overlay": false
}

Be precise about scene_type. If there are 2+ people visible, use 'multi-person'. If one person is talking to camera, use 'talking-head'. If it's a product close-up with no person, use 'product'. If it's a lifestyle/action shot, use 'b-roll'. If it's a graphic or title card, use 'graphic'.

Return ONLY valid JSON, no markdown formatting."""

        parts.append(types.Part.from_text(text=prompt))

        try:
            response = client.models.generate_content(
                model=GEMINI_VIDEO_MODEL,
                contents=types.Content(parts=parts),
                config=types.GenerateContentConfig(temperature=0.2),
            )

            text = response.text.strip()
            # Clean up markdown wrapping
            if text.startswith("```"):
                text = re.sub(r"^```(?:json)?\n?", "", text)
                text = re.sub(r"\n?```$", "", text)

            analysis = json.loads(text)
            analysis["scene_number"] = scene["scene_number"]
            analysis["timestamp"] = scene["timestamp"]
            analysis["duration"] = scene["duration"]
            analyses.append(analysis)

        except Exception as e:
            log(2, f"  Error analyzing scene {scene['scene_number']}: {e}")
            analyses.append({"scene_number": scene["scene_number"], "error": str(e)})
            time.sleep(2)

        time.sleep(1)  # Rate limiting

    with open(analysis_path, "w") as f:
        json.dump(analyses, f, indent=2)

    log(2, f"Analysis complete: {len(analyses)} scenes")
    return analyses


# ---------------------------------------------------------------------------
# Stage 3: Brand-Adapted Image Prompts
# ---------------------------------------------------------------------------

def generate_brand_prompts(analyses, brand_knowledge, product_context, style_notes, output_dir):
    """Generate brand-adapted image editing prompts for Nano Banana 2."""
    prompts_dir = ensure_dir(os.path.join(output_dir, "prompts"))
    prompts_path = os.path.join(prompts_dir, "image_prompts.json")

    if os.path.exists(prompts_path):
        log(3, "Brand prompts already exist — loading from cache")
        with open(prompts_path, "r") as f:
            return json.load(f)

    client = genai.Client(api_key=GEMINI_API_KEY)
    brand_prompts = []

    for analysis in analyses:
        if analysis.get("error"):
            brand_prompts.append({
                "scene_number": analysis["scene_number"],
                "prompt": None,
                "error": analysis["error"]
            })
            continue

        log(3, f"Generating prompt for scene {analysis['scene_number']}...")

        system_prompt = f"""You are a creative director adapting an AI UGC video ad for a new brand.

BRAND KNOWLEDGE:
{brand_knowledge[:15000] if brand_knowledge else 'No brand docs provided.'}

PRODUCT CONTEXT:
{product_context}

{f'STYLE DIRECTION: {style_notes}' if style_notes else ''}

Your job: write an image editing prompt that transforms the reference frame for the target brand.
PRESERVE: composition, camera angle, framing, lighting, overall visual style, mood
ADAPT: people/avatars to match brand's target audience, products to brand's product, setting to brand's world

CRITICAL RULES:
- Replicate the scene 1:1 — do NOT invent or add elements not in the original
- If the scene has NO product, include this line: "Do NOT add any product, bottle, package, or branded item to this scene"
- If the scene HAS a product, describe exactly how the brand's product should appear
- Keep the same number of people, same poses, same camera angle
- Describe the target avatar(s) clearly: age range, gender, ethnicity diversity, style/clothing"""

        user_prompt = f"""REFERENCE SCENE ANALYSIS:
{json.dumps(analysis, indent=2)}

Write an image editing prompt for Nano Banana 2 (Gemini image-to-image) that transforms this reference frame for the target brand. The prompt should describe the OUTPUT image, not the reference.

Return ONLY the prompt text, no JSON wrapping or explanation."""

        try:
            response = client.models.generate_content(
                model=GEMINI_VIDEO_MODEL,
                contents=[
                    types.Content(role="user", parts=[
                        types.Part.from_text(text=f"{system_prompt}\n\n{user_prompt}")
                    ])
                ],
                config=types.GenerateContentConfig(temperature=0.4),
            )

            prompt_text = response.text.strip()
            has_product = analysis.get("has_product", False)
            scene_type = analysis.get("scene_type", "b-roll")

            brand_prompts.append({
                "scene_number": analysis["scene_number"],
                "timestamp": analysis.get("timestamp", 0),
                "duration": analysis.get("duration", 5),
                "prompt": prompt_text,
                "scene_type": scene_type,
                "has_product": has_product,
                "who_is_speaking": analysis.get("who_is_speaking", "none"),
                "motion_raw": analysis.get("motion", ""),
                "camera_angle": analysis.get("camera_angle", "medium"),
                "reference_analysis": analysis,
            })

        except Exception as e:
            log(3, f"  Error: {e}")
            brand_prompts.append({
                "scene_number": analysis["scene_number"],
                "prompt": None,
                "error": str(e)
            })
            time.sleep(2)

        time.sleep(1)

    with open(prompts_path, "w") as f:
        json.dump(brand_prompts, f, indent=2)

    log(3, f"Generated {len(brand_prompts)} brand-adapted prompts")
    return brand_prompts


# ---------------------------------------------------------------------------
# Stage 4: Image-to-Image via Nano Banana 2
# ---------------------------------------------------------------------------

def generate_images(brand_prompts, scenes, product_images, output_dir):
    """Generate brand-adapted images using Nano Banana 2 image-to-image."""
    gen_dir = ensure_dir(os.path.join(output_dir, "generated"))
    client = genai.Client(api_key=GEMINI_API_KEY)
    results = []

    for bp in brand_prompts:
        scene_num = bp["scene_number"]
        out_path = os.path.join(gen_dir, f"scene_{scene_num:03d}_brand.png")

        if os.path.exists(out_path):
            log(4, f"Scene {scene_num} already generated — skipping")
            results.append({"scene_number": scene_num, "image_path": out_path, "status": "cached"})
            continue

        if not bp.get("prompt"):
            results.append({"scene_number": scene_num, "image_path": None, "status": "skipped"})
            continue

        # Skip graphic/text-overlay scenes — these don't need image generation
        if bp.get("scene_type") in ("graphic", "text-overlay"):
            log(4, f"Scene {scene_num} is {bp['scene_type']} — skipping image generation")
            results.append({"scene_number": scene_num, "image_path": None, "status": "skipped_type"})
            continue

        log(4, f"Generating scene {scene_num}/{len(brand_prompts)}...")

        # Find the reference keyframe
        ref_scene = next((s for s in scenes if s["scene_number"] == scene_num), None)
        ref_keyframe = ref_scene["keyframe_path"] if ref_scene else None

        parts = []

        # Add reference keyframe as image input
        if ref_keyframe and os.path.exists(ref_keyframe):
            try:
                img = Image.open(ref_keyframe)
                parts.append(types.Part.from_image(img))
            except Exception:
                pass

        # Add product reference if scene has product
        if bp.get("has_product") and product_images:
            for pimg_path in product_images[:2]:
                if os.path.exists(pimg_path):
                    try:
                        pimg = Image.open(pimg_path)
                        parts.append(types.Part.from_image(pimg))
                    except Exception:
                        pass

        # Add the prompt
        guard = "" if bp.get("has_product") else "\n\nIMPORTANT: Do NOT add any product, bottle, package, or branded item to this scene."
        parts.append(types.Part.from_text(
            text=f"Edit this image: {bp['prompt']}{guard}\n\nReplicate the composition 1:1 — do NOT invent or add elements that are not in the original scene."
        ))

        try:
            response = client.models.generate_content(
                model=GEMINI_IMAGE_MODEL,
                contents=types.Content(parts=parts),
                config=types.GenerateContentConfig(
                    response_modalities=["image", "text"],
                    temperature=0.4,
                ),
            )

            # Extract generated image
            saved = False
            if response.candidates:
                for part in response.candidates[0].content.parts:
                    if hasattr(part, "inline_data") and part.inline_data:
                        img_data = part.inline_data.data
                        with open(out_path, "wb") as f:
                            f.write(img_data)
                        log(4, f"  Saved: {out_path}")
                        saved = True
                        break

            if saved:
                results.append({"scene_number": scene_num, "image_path": out_path, "status": "success"})
            else:
                log(4, f"  No image in response for scene {scene_num}")
                results.append({"scene_number": scene_num, "image_path": None, "status": "no_image"})

        except Exception as e:
            log(4, f"  Error: {e}")
            results.append({"scene_number": scene_num, "image_path": None, "status": "error"})
            time.sleep(3)

        time.sleep(2)  # Rate limiting

    succeeded = sum(1 for r in results if r["status"] in ("success", "cached"))
    log(4, f"Image generation complete: {succeeded}/{len(brand_prompts)} scenes")
    return results


# ---------------------------------------------------------------------------
# Stage 5: Kling 3.0 Animate
# ---------------------------------------------------------------------------

def upload_image_for_kling(image_path):
    """Upload image to kie.ai file hosting for Kling access."""
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
    except Exception as e:
        log(5, f"  Upload error: {e}")
    return None


def upload_video_for_sync(video_path):
    """Upload video to a temporary hosting service for Sync.so access.
    Uses kie.ai's file hosting (same endpoint, accepts video)."""
    KIE_UPLOAD_URL = "https://kieai.redpandaai.co/api/file-stream-upload"
    try:
        with open(video_path, "rb") as f:
            resp = requests.post(
                KIE_UPLOAD_URL,
                headers={"Authorization": f"Bearer {KIE_API_KEY}"},
                files={"file": (os.path.basename(video_path), f, "video/mp4")},
                data={"uploadPath": "videos"},
                timeout=120,
            )
        data = resp.json()
        if data.get("code") == 200 and data.get("data", {}).get("downloadUrl"):
            return data["data"]["downloadUrl"]
    except Exception as e:
        log(6, f"  Video upload error: {e}")
    return None


def upload_audio_for_sync(audio_path):
    """Upload audio to temp hosting for Sync.so access."""
    KIE_UPLOAD_URL = "https://kieai.redpandaai.co/api/file-stream-upload"
    try:
        ext = Path(audio_path).suffix.lower()
        mime = "audio/mpeg" if ext == ".mp3" else "audio/wav"
        with open(audio_path, "rb") as f:
            resp = requests.post(
                KIE_UPLOAD_URL,
                headers={"Authorization": f"Bearer {KIE_API_KEY}"},
                files={"file": (os.path.basename(audio_path), f, mime)},
                data={"uploadPath": "audio"},
                timeout=120,
            )
        data = resp.json()
        if data.get("code") == 200 and data.get("data", {}).get("downloadUrl"):
            return data["data"]["downloadUrl"]
    except Exception as e:
        log(6, f"  Audio upload error: {e}")
    return None


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
                return urls[0] if urls else None
            elif state == "fail":
                fail_msg = data["data"].get("failMsg", "unknown")
                log(5, f"    Kling task failed: {fail_msg}")
                return None
            else:
                time.sleep(KLING_POLL_INTERVAL)
        except Exception:
            time.sleep(KLING_POLL_INTERVAL)
    return None


def animate_scenes(brand_prompts, image_results, product_images, output_dir, aspect_ratio="9:16"):
    """Animate generated images using Kling 3.0 via kie.ai."""
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
                pimg_url = upload_image_for_kling(pimg)
                if pimg_url:
                    product_image_urls.append(pimg_url)

    results = []

    for bp, ir in zip(brand_prompts, image_results):
        scene_num = bp["scene_number"]
        out_path = os.path.join(anim_dir, f"scene_{scene_num:03d}_animated.mp4")

        if os.path.exists(out_path):
            log(5, f"Scene {scene_num} already animated — skipping")
            results.append({"scene_number": scene_num, "video_path": out_path, "status": "cached"})
            continue

        image_path = ir.get("image_path")
        if not image_path or not os.path.exists(image_path):
            log(5, f"Scene {scene_num} — no image, skipping")
            results.append({"scene_number": scene_num, "video_path": None, "status": "skipped"})
            continue

        # Skip graphic/text scenes
        if bp.get("scene_type") in ("graphic", "text-overlay"):
            results.append({"scene_number": scene_num, "video_path": None, "status": "skipped_type"})
            continue

        log(5, f"Animating scene {scene_num}/{len(brand_prompts)}...")

        image_url = upload_image_for_kling(image_path)
        if not image_url:
            results.append({"scene_number": scene_num, "video_path": None, "status": "upload_failed"})
            continue

        # Build motion prompt based on scene type
        scene_type = bp.get("scene_type", "b-roll")
        motion_raw = bp.get("motion_raw", "")

        if scene_type in ("talking-head", "multi-person"):
            kling_prompt = f"Character speaking naturally with subtle lip movement, natural hand gestures, slight head nods and turns. {motion_raw}"
        elif scene_type == "product":
            kling_prompt = f"Subtle product rotation or reveal, smooth cinematic motion. {motion_raw}"
        else:
            kling_prompt = f"Smooth natural motion. {motion_raw}"

        duration = str(min(10, max(5, int(bp.get("duration", 5)))))

        payload = {
            "model": "kling-3.0/video",
            "input": {
                "prompt": kling_prompt,
                "image_urls": [image_url],
                "sound": False,
                "duration": duration,
                "aspect_ratio": aspect_ratio,
                "mode": "pro",
                "multi_shots": False
            }
        }

        # Add product references if scene has product
        if bp.get("has_product") and product_image_urls:
            elements = []
            for idx, pimg_url in enumerate(product_image_urls[:3]):
                elements.append({
                    "name": f"product_{idx+1}",
                    "description": f"Brand product reference {idx+1}",
                    "element_input_urls": [pimg_url]
                })
            payload["input"]["kling_elements"] = elements

        # Submit and poll
        success = False
        for attempt in range(MAX_KLING_RETRIES):
            try:
                resp = requests.post(KIE_CREATE_URL, headers=headers, json=payload, timeout=60)
                resp_data = resp.json()

                if resp_data.get("code") != 200:
                    log(5, f"  Attempt {attempt+1} failed: {resp_data.get('msg', 'unknown')}")
                    time.sleep(10)
                    continue

                task_id = resp_data["data"]["taskId"]
                log(5, f"  Task submitted: {task_id}")

                video_url = poll_kling_task(task_id, headers)
                if video_url:
                    vid_resp = requests.get(video_url, timeout=120)
                    with open(out_path, "wb") as f:
                        f.write(vid_resp.content)
                    log(5, f"  Saved: {out_path}")
                    results.append({"scene_number": scene_num, "video_path": out_path, "status": "success"})
                    success = True
                    break
                else:
                    log(5, f"  Attempt {attempt+1}: generation failed/timed out")

            except Exception as e:
                log(5, f"  Attempt {attempt+1} error: {e}")
                time.sleep(10)

        if not success:
            results.append({"scene_number": scene_num, "video_path": None, "status": "failed"})

        time.sleep(5)

    succeeded = sum(1 for r in results if r["status"] in ("success", "cached"))
    log(5, f"Animation complete: {succeeded}/{len(brand_prompts)} scenes")
    return results


# ---------------------------------------------------------------------------
# Stage 6: Sync.so Lip Sync
# ---------------------------------------------------------------------------

def slice_audio(voiceover_path, start_time, duration, output_path):
    """Slice a segment of audio using ffmpeg."""
    try:
        subprocess.run(
            ["ffmpeg", "-ss", str(start_time), "-i", voiceover_path,
             "-t", str(duration), "-c:a", "copy", output_path, "-y"],
            capture_output=True, timeout=30
        )
        return os.path.exists(output_path)
    except Exception:
        return False


def poll_sync_task(generation_id, max_wait=600):
    """Poll Sync.so generation until complete."""
    headers = {"x-api-key": SYNC_API_KEY}
    url = f"{SYNC_GENERATE_URL}/{generation_id}"
    start = time.time()

    while time.time() - start < max_wait:
        try:
            resp = requests.get(url, headers=headers, timeout=30)
            data = resp.json()
            status = data.get("status", "")

            if status == "COMPLETED":
                return data.get("outputUrl")
            elif status in ("FAILED", "REJECTED"):
                log(6, f"    Sync.so failed: {data.get('error', 'unknown')}")
                return None
            else:
                time.sleep(SYNC_POLL_INTERVAL)
        except Exception:
            time.sleep(SYNC_POLL_INTERVAL)

    return None


def lip_sync_scenes(brand_prompts, animation_results, voiceover_path, output_dir):
    """Lip sync talking scenes using Sync.so API."""
    if not SYNC_API_KEY:
        log(6, "WARNING: No SYNC_API_KEY set. Skipping lip sync stage.")
        log(6, "  Set env var SYNC_API_KEY or pass --sync-api-key to enable lip sync.")
        # Return animation results as-is (fallback)
        return [{"scene_number": r["scene_number"], "video_path": r.get("video_path"),
                 "status": "skipped_no_key"} for r in animation_results]

    lipsync_dir = ensure_dir(os.path.join(output_dir, "lipsync"))
    audio_slices_dir = ensure_dir(os.path.join(output_dir, "audio_slices"))
    results = []

    for bp, ar in zip(brand_prompts, animation_results):
        scene_num = bp["scene_number"]
        out_path = os.path.join(lipsync_dir, f"scene_{scene_num:03d}_lipsync.mp4")

        if os.path.exists(out_path):
            log(6, f"Scene {scene_num} already lip-synced — skipping")
            results.append({"scene_number": scene_num, "video_path": out_path, "status": "cached"})
            continue

        # Only lip sync talking scenes
        scene_type = bp.get("scene_type", "b-roll")
        if scene_type not in ("talking-head", "multi-person"):
            # Pass through the animated video unchanged
            results.append({
                "scene_number": scene_num,
                "video_path": ar.get("video_path"),
                "status": "passthrough"
            })
            continue

        if not ar.get("video_path") or not os.path.exists(ar["video_path"]):
            results.append({"scene_number": scene_num, "video_path": None, "status": "no_video"})
            continue

        log(6, f"Lip-syncing scene {scene_num} ({scene_type})...")

        # Slice the audio for this scene's time range
        audio_slice_path = os.path.join(audio_slices_dir, f"scene_{scene_num:03d}_audio.mp3")
        timestamp = bp.get("timestamp", 0)
        duration = bp.get("duration", 5)

        if not os.path.exists(audio_slice_path):
            if not slice_audio(voiceover_path, timestamp, duration, audio_slice_path):
                log(6, f"  Could not slice audio for scene {scene_num}")
                results.append({
                    "scene_number": scene_num,
                    "video_path": ar.get("video_path"),
                    "status": "audio_slice_failed"
                })
                continue

        # Upload video and audio to temp hosting
        video_url = upload_video_for_sync(ar["video_path"])
        audio_url = upload_audio_for_sync(audio_slice_path)

        if not video_url or not audio_url:
            log(6, f"  Upload failed for scene {scene_num}")
            results.append({
                "scene_number": scene_num,
                "video_path": ar.get("video_path"),
                "status": "upload_failed"
            })
            continue

        # Call Sync.so API
        try:
            sync_headers = {
                "x-api-key": SYNC_API_KEY,
                "Content-Type": "application/json"
            }

            sync_payload = {
                "model": "lipsync-2",
                "input": [
                    {"type": "video", "url": video_url},
                    {"type": "audio", "url": audio_url}
                ],
                "options": {
                    "sync_mode": "cut_off",
                    "active_speaker_detection": scene_type == "multi-person",
                }
            }

            resp = requests.post(SYNC_GENERATE_URL, headers=sync_headers, json=sync_payload, timeout=60)
            resp_data = resp.json()

            gen_id = resp_data.get("id")
            if not gen_id:
                log(6, f"  Sync.so error: {resp_data}")
                results.append({
                    "scene_number": scene_num,
                    "video_path": ar.get("video_path"),
                    "status": "sync_error"
                })
                continue

            log(6, f"  Sync.so job submitted: {gen_id}")

            # Poll for completion
            output_url = poll_sync_task(gen_id)
            if output_url:
                vid_resp = requests.get(output_url, timeout=120)
                with open(out_path, "wb") as f:
                    f.write(vid_resp.content)
                log(6, f"  Saved: {out_path}")
                results.append({"scene_number": scene_num, "video_path": out_path, "status": "success"})
            else:
                log(6, f"  Sync.so timed out/failed for scene {scene_num} — using animated fallback")
                results.append({
                    "scene_number": scene_num,
                    "video_path": ar.get("video_path"),
                    "status": "sync_timeout"
                })

        except Exception as e:
            log(6, f"  Error: {e}")
            results.append({
                "scene_number": scene_num,
                "video_path": ar.get("video_path"),
                "status": "error"
            })

        time.sleep(3)

    succeeded = sum(1 for r in results if r["status"] in ("success", "cached"))
    log(6, f"Lip sync complete: {succeeded} synced, {len(results) - succeeded} passthrough/skipped")
    return results


# ---------------------------------------------------------------------------
# Stage 7: Segment into ~30-second chunks
# ---------------------------------------------------------------------------

def segment_scenes(brand_prompts, lipsync_results, output_dir):
    """Group lip-synced clips into ~30-second segments at natural scene breaks."""
    segments_dir = ensure_dir(os.path.join(output_dir, "segments"))
    segments = []
    current_segment = []
    current_duration = 0.0

    for bp, lr in zip(brand_prompts, lipsync_results):
        video_path = lr.get("video_path")
        if not video_path or not os.path.exists(video_path):
            continue

        scene_duration = bp.get("duration", 5)
        current_segment.append({
            "scene_number": bp["scene_number"],
            "video_path": video_path,
            "duration": scene_duration,
        })
        current_duration += scene_duration

        # Break at ~30 seconds
        if current_duration >= SEGMENT_TARGET_DURATION:
            segments.append(current_segment)
            current_segment = []
            current_duration = 0.0

    # Don't forget the last segment
    if current_segment:
        segments.append(current_segment)

    log(7, f"Created {len(segments)} segments from {sum(len(s) for s in segments)} scenes")

    # Concatenate clips within each segment using ffmpeg
    segment_paths = []
    for seg_idx, segment in enumerate(segments):
        seg_num = seg_idx + 1
        out_path = os.path.join(segments_dir, f"segment_{seg_num:03d}.mp4")

        if os.path.exists(out_path):
            log(7, f"Segment {seg_num} already exists — skipping")
            segment_paths.append(out_path)
            continue

        if len(segment) == 1:
            # Just copy the single clip
            import shutil
            shutil.copy2(segment[0]["video_path"], out_path)
        else:
            # Create concat list file
            concat_list = os.path.join(segments_dir, f"segment_{seg_num:03d}_list.txt")
            with open(concat_list, "w") as f:
                for clip in segment:
                    # Escape single quotes in paths
                    safe_path = clip["video_path"].replace("'", "'\\''")
                    f.write(f"file '{safe_path}'\n")

            subprocess.run(
                ["ffmpeg", "-f", "concat", "-safe", "0", "-i", concat_list,
                 "-c", "copy", out_path, "-y"],
                capture_output=True, timeout=120
            )

        if os.path.exists(out_path):
            segment_paths.append(out_path)
            log(7, f"  Segment {seg_num}: {len(segment)} clips → {out_path}")

    return segment_paths, segments


# ---------------------------------------------------------------------------
# Stage 8: Kling Motion Control (Camera Polish)
# ---------------------------------------------------------------------------

def motion_control_segments(segment_paths, output_dir, aspect_ratio="9:16"):
    """Apply Kling motion control to each segment for camera polish."""
    polished_dir = ensure_dir(os.path.join(output_dir, "polished"))
    headers = {
        "Authorization": f"Bearer {KIE_API_KEY}",
        "Content-Type": "application/json"
    }

    results = []

    for seg_idx, seg_path in enumerate(segment_paths):
        seg_num = seg_idx + 1
        out_path = os.path.join(polished_dir, f"segment_{seg_num:03d}_polished.mp4")

        if os.path.exists(out_path):
            log(8, f"Segment {seg_num} already polished — skipping")
            results.append(out_path)
            continue

        log(8, f"Polishing segment {seg_num}/{len(segment_paths)} with motion control...")

        # Upload segment video
        video_url = upload_video_for_sync(seg_path)  # Reuse the upload function
        if not video_url:
            log(8, f"  Upload failed — using raw segment")
            results.append(seg_path)  # Fallback to unpolished
            continue

        # Kling motion control request
        payload = {
            "model": "kling-3.0/video",
            "input": {
                "prompt": "Subtle professional camera movement: gentle sway, slight push-in, smooth cinematic feel. Maintain natural motion of all subjects. Do not alter faces or lip movements.",
                "video_url": video_url,
                "sound": False,
                "aspect_ratio": aspect_ratio,
                "mode": "pro",
                "motion_control": True,
            }
        }

        success = False
        for attempt in range(MAX_KLING_RETRIES):
            try:
                resp = requests.post(KIE_CREATE_URL, headers=headers, json=payload, timeout=60)
                resp_data = resp.json()

                if resp_data.get("code") != 200:
                    log(8, f"  Attempt {attempt+1} failed: {resp_data.get('msg', 'unknown')}")
                    time.sleep(10)
                    continue

                task_id = resp_data["data"]["taskId"]
                log(8, f"  Task submitted: {task_id}")

                video_result_url = poll_kling_task(task_id, headers, max_wait=900)
                if video_result_url:
                    vid_resp = requests.get(video_result_url, timeout=180)
                    with open(out_path, "wb") as f:
                        f.write(vid_resp.content)
                    log(8, f"  Saved: {out_path}")
                    results.append(out_path)
                    success = True
                    break

            except Exception as e:
                log(8, f"  Attempt {attempt+1} error: {e}")
                time.sleep(10)

        if not success:
            log(8, f"  Motion control failed — using raw segment as fallback")
            results.append(seg_path)

        time.sleep(5)

    log(8, f"Motion control complete: {len(results)} segments")
    return results


# ---------------------------------------------------------------------------
# Stage 9: FFmpeg Final Stitch
# ---------------------------------------------------------------------------

def stitch_final_video(polished_paths, voiceover_path, bg_music_path, output_dir, aspect_ratio="9:16"):
    """Stitch all polished segments together with audio using FFmpeg."""
    final_dir = ensure_dir(os.path.join(output_dir, "final"))
    ar_tag = aspect_ratio.replace(":", "x")
    final_path = os.path.join(final_dir, f"aiugc_final_{ar_tag}.mp4")

    if os.path.exists(final_path):
        log(9, f"Final video already exists: {final_path}")
        return final_path

    log(9, f"Stitching {len(polished_paths)} segments...")

    # Create concat list
    concat_list = os.path.join(final_dir, "concat_list.txt")
    with open(concat_list, "w") as f:
        for path in polished_paths:
            safe_path = path.replace("'", "'\\''")
            f.write(f"file '{safe_path}'\n")

    # Step 1: Concatenate video segments
    stitched_video = os.path.join(final_dir, "stitched_video_only.mp4")
    subprocess.run(
        ["ffmpeg", "-f", "concat", "-safe", "0", "-i", concat_list,
         "-c", "copy", stitched_video, "-y"],
        capture_output=True, timeout=300
    )

    if not os.path.exists(stitched_video):
        log(9, "ERROR: Video concatenation failed")
        return None

    # Step 2: Add voiceover audio (and optionally background music)
    if bg_music_path and os.path.exists(bg_music_path):
        # Mix VO + background music (music at -12dB)
        filter_complex = "[1:a]volume=1.0[vo];[2:a]volume=0.15[bg];[vo][bg]amix=inputs=2:duration=shortest[out]"
        cmd = [
            "ffmpeg", "-i", stitched_video,
            "-i", voiceover_path,
            "-i", bg_music_path,
            "-filter_complex", filter_complex,
            "-map", "0:v", "-map", "[out]",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            "-af", "afade=t=in:d=0.5,afade=t=out:st=-0.5:d=0.5",
            final_path, "-y"
        ]
    else:
        # Just VO audio
        cmd = [
            "ffmpeg", "-i", stitched_video,
            "-i", voiceover_path,
            "-map", "0:v", "-map", "1:a",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            final_path, "-y"
        ]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

    if os.path.exists(final_path):
        # Clean up temp file
        try:
            os.remove(stitched_video)
        except Exception:
            pass
        duration = get_video_duration(final_path)
        log(9, f"Final video: {final_path} ({duration:.1f}s)")
        return final_path
    else:
        log(9, f"ERROR: Final stitch failed. ffmpeg stderr: {result.stderr[:500]}")
        # Return stitched video without audio as fallback
        if os.path.exists(stitched_video):
            import shutil
            shutil.move(stitched_video, final_path)
            return final_path
        return None


# ---------------------------------------------------------------------------
# Stage 10: Google Drive Upload
# ---------------------------------------------------------------------------

def get_drive_service():
    """Authenticate to Google Drive via OAuth2."""
    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build
    except ImportError:
        log(10, "Google Drive packages not installed.")
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
    """Upload final video + polished segments + assembly guide to Drive."""
    from googleapiclient.http import MediaFileUpload

    service = get_drive_service()
    if not service:
        return None

    date_str = datetime.now().strftime("%Y-%m-%d")
    folder_name = f"{brand}_{date_str}_aiugc"

    folder_metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [drive_folder_id]
    }
    folder = service.files().create(body=folder_metadata, fields="id").execute()
    parent_id = folder.get("id")
    log(10, f"Created Drive folder: {folder_name}")

    upload_count = 0

    # Upload final video
    final_dir = os.path.join(output_dir, "final")
    if os.path.exists(final_dir):
        for filename in sorted(os.listdir(final_dir)):
            filepath = os.path.join(final_dir, filename)
            if not os.path.isfile(filepath) or filename.endswith(".txt"):
                continue
            mime = "video/mp4" if filepath.endswith(".mp4") else "application/octet-stream"
            file_metadata = {"name": filename, "parents": [parent_id]}
            media = MediaFileUpload(filepath, mimetype=mime, resumable=True)
            service.files().create(body=file_metadata, media_body=media, fields="id").execute()
            upload_count += 1
            log(10, f"  Uploaded: {filename}")

    # Upload polished segments
    polished_dir = os.path.join(output_dir, "polished")
    if os.path.exists(polished_dir):
        for filename in sorted(os.listdir(polished_dir)):
            filepath = os.path.join(polished_dir, filename)
            if not os.path.isfile(filepath):
                continue
            file_metadata = {"name": filename, "parents": [parent_id]}
            media = MediaFileUpload(filepath, mimetype="video/mp4", resumable=True)
            service.files().create(body=file_metadata, media_body=media, fields="id").execute()
            upload_count += 1
            log(10, f"  Uploaded: {filename}")

    # Upload assembly guide
    guide_path = os.path.join(output_dir, "assembly_guide.md")
    if os.path.exists(guide_path):
        file_metadata = {"name": "assembly_guide.md", "parents": [parent_id]}
        media = MediaFileUpload(guide_path, mimetype="text/markdown", resumable=True)
        service.files().create(body=file_metadata, media_body=media, fields="id").execute()
        upload_count += 1

    log(10, f"Uploaded {upload_count} files to Drive folder '{folder_name}'")
    return parent_id


# ---------------------------------------------------------------------------
# Assembly Guide
# ---------------------------------------------------------------------------

def write_assembly_guide(brand_prompts, lipsync_results, segment_paths, polished_paths, final_path, output_dir, brand):
    """Write production notes for the video editor."""
    guide_path = os.path.join(output_dir, "assembly_guide.md")

    lines = [
        f"# Assembly Guide — {brand} AI UGC Replicator",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## Pipeline Summary",
        "",
        f"- **Scenes extracted:** {len(brand_prompts)}",
        f"- **Segments created:** {len(segment_paths)}",
        f"- **Polished segments:** {len(polished_paths)}",
        f"- **Final video:** {os.path.basename(final_path) if final_path else 'N/A'}",
        "",
        "## Scene Breakdown",
        "",
        "| Scene | Timestamp | Duration | Type | Speaking | Lip Sync | File |",
        "|-------|-----------|----------|------|----------|----------|------|",
    ]

    for bp, lr in zip(brand_prompts, lipsync_results):
        ts = f"{bp.get('timestamp', 0):.1f}s"
        dur = f"{bp.get('duration', 0):.1f}s"
        stype = bp.get("scene_type", "?")
        speaking = bp.get("who_is_speaking", "none")
        sync_status = lr.get("status", "?")
        filename = os.path.basename(lr["video_path"]) if lr.get("video_path") else "N/A"
        lines.append(f"| {bp['scene_number']} | {ts} | {dur} | {stype} | {speaking} | {sync_status} | {filename} |")

    lines.extend([
        "",
        "## Segments",
        "",
    ])

    for i, (seg, pol) in enumerate(zip(segment_paths, polished_paths)):
        lines.append(f"- **Segment {i+1}:** {os.path.basename(pol)}")

    lines.extend([
        "",
        "## Notes",
        "",
        "- Polished segments have Kling motion control camera movement applied",
        "- If a segment looks worse after motion control, use the raw segment from `segments/` instead",
        "- Lip-synced scenes used Sync.so lipsync-2 model",
        "- Non-speaking scenes (b-roll, product) passed through animation only",
    ])

    with open(guide_path, "w") as f:
        f.write("\n".join(lines))

    log("G", f"Assembly guide saved: {guide_path}")


# ---------------------------------------------------------------------------
# Main Pipeline
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="AI UGC Video Replicator Pipeline")
    parser.add_argument("--video", required=True, help="Path to reference video OR GetHookd URL/ad ID")
    parser.add_argument("--voiceover", required=True, help="Path to voiceover audio (MP3/WAV)")
    parser.add_argument("--brand", required=True, help="Target brand name")
    parser.add_argument("--product-context", default="", help="Product description (auto-loaded from vault)")
    parser.add_argument("--style", default="", help="Style notes")
    parser.add_argument("--aspect-ratio", default="9:16", help="Output aspect ratio (9:16, 1:1, 16:9)")
    parser.add_argument("--bg-music", default="", help="Path to background music file")
    parser.add_argument("--drive-folder", default="", help="Google Drive folder ID for upload")
    parser.add_argument("--product-images", default="", help="Comma-separated product image paths")
    parser.add_argument("--output-dir", default="./aiugc-output", help="Local output directory")
    parser.add_argument("--scene-threshold", type=float, default=SCENE_THRESHOLD, help="Scene detection sensitivity")
    parser.add_argument("--sync-api-key", default="", help="Sync.so API key (or set SYNC_API_KEY env var)")
    parser.add_argument("--skip-lipsync", action="store_true", help="Skip Sync.so lip sync stage")
    parser.add_argument("--skip-motion-control", action="store_true", help="Skip Kling motion control stage")
    parser.add_argument("--skip-upload", action="store_true", help="Skip Google Drive upload")

    args = parser.parse_args()

    # Set Sync API key from arg if provided
    global SYNC_API_KEY
    if args.sync_api_key:
        SYNC_API_KEY = args.sync_api_key

    # --- Resolve video input (local path or GetHookd URL) ---
    gethookd_meta = None
    try:
        video_path, gethookd_meta = resolve_video_input(args.video)
        args.video = video_path  # Replace with local path
        if gethookd_meta:
            print(f"  [GetHookd] Ad resolved: {gethookd_meta.get('brand')} — \"{gethookd_meta.get('title', '')[:60]}\"")
            print(f"  [GetHookd] Score: {gethookd_meta.get('score')} ({gethookd_meta.get('score_title')}) | {gethookd_meta.get('days_active')} days active")
    except (ValueError, FileNotFoundError) as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    # Validate voiceover
    if not os.path.exists(args.voiceover):
        print(f"ERROR: Voiceover not found: {args.voiceover}")
        sys.exit(1)

    output_dir = args.output_dir
    ensure_dir(output_dir)

    # Save GetHookd metadata alongside output for context
    if gethookd_meta:
        meta_path = os.path.join(output_dir, "gethookd_source.json")
        with open(meta_path, "w") as f:
            json.dump(gethookd_meta, f, indent=2)

    # Load brand knowledge
    brand_key = args.brand.lower().replace(" ", "-")
    brand_knowledge, brand_product_images, default_context = load_brand_knowledge(brand_key)
    product_context = args.product_context or default_context

    # Resolve product images
    product_images = []
    if args.product_images:
        product_images = [p.strip() for p in args.product_images.split(",") if os.path.exists(p.strip())]
    if not product_images:
        product_images = brand_product_images

    print("=" * 60)
    print(f"AI UGC VIDEO REPLICATOR — {args.brand}")
    print(f"Reference: {args.video}")
    print(f"Voiceover: {args.voiceover}")
    print(f"Output: {output_dir}")
    print(f"Aspect ratio: {args.aspect_ratio}")
    print(f"Product images: {len(product_images)}")
    print(f"Brand knowledge: {len(brand_knowledge)} chars")
    print(f"Lip sync: {'ENABLED' if SYNC_API_KEY and not args.skip_lipsync else 'DISABLED'}")
    print(f"Motion control: {'ENABLED' if not args.skip_motion_control else 'DISABLED'}")
    print("=" * 60)

    # --- Stage 1: Scene Detection ---
    print("\n" + "=" * 40)
    print("STAGE 1: Scene Detection")
    print("=" * 40)
    scenes, video_duration = extract_scenes(args.video, output_dir, args.scene_threshold)

    # --- Stage 2: Scene Analysis ---
    print("\n" + "=" * 40)
    print("STAGE 2: Scene Analysis (Gemini)")
    print("=" * 40)
    analyses = analyze_scenes(scenes, output_dir)

    # --- Stage 3: Brand-Adapted Prompts ---
    print("\n" + "=" * 40)
    print("STAGE 3: Brand-Adapted Image Prompts")
    print("=" * 40)
    brand_prompts = generate_brand_prompts(analyses, brand_knowledge, product_context, args.style, output_dir)

    # --- Stage 4: Image Generation ---
    print("\n" + "=" * 40)
    print("STAGE 4: Image-to-Image (Nano Banana 2)")
    print("=" * 40)
    image_results = generate_images(brand_prompts, scenes, product_images, output_dir)

    # --- Stage 5: Kling Animate ---
    print("\n" + "=" * 40)
    print("STAGE 5: Kling 3.0 Animate")
    print("=" * 40)
    animation_results = animate_scenes(brand_prompts, image_results, product_images, output_dir, args.aspect_ratio)

    # --- Stage 6: Sync.so Lip Sync ---
    print("\n" + "=" * 40)
    print("STAGE 6: Sync.so Lip Sync")
    print("=" * 40)
    if args.skip_lipsync:
        log(6, "Lip sync SKIPPED (--skip-lipsync)")
        lipsync_results = [{"scene_number": r["scene_number"], "video_path": r.get("video_path"),
                           "status": "skipped"} for r in animation_results]
    else:
        lipsync_results = lip_sync_scenes(brand_prompts, animation_results, args.voiceover, output_dir)

    # --- Stage 7: Segment ---
    print("\n" + "=" * 40)
    print("STAGE 7: Segmentation (~30s chunks)")
    print("=" * 40)
    segment_paths, segments = segment_scenes(brand_prompts, lipsync_results, output_dir)

    # --- Stage 8: Motion Control ---
    print("\n" + "=" * 40)
    print("STAGE 8: Kling Motion Control")
    print("=" * 40)
    if args.skip_motion_control:
        log(8, "Motion control SKIPPED (--skip-motion-control)")
        polished_paths = segment_paths
    else:
        polished_paths = motion_control_segments(segment_paths, output_dir, args.aspect_ratio)

    # --- Stage 9: FFmpeg Stitch ---
    print("\n" + "=" * 40)
    print("STAGE 9: FFmpeg Final Stitch")
    print("=" * 40)
    final_path = stitch_final_video(
        polished_paths, args.voiceover,
        args.bg_music if args.bg_music else None,
        output_dir, args.aspect_ratio
    )

    # --- Assembly Guide ---
    write_assembly_guide(brand_prompts, lipsync_results, segment_paths, polished_paths, final_path, output_dir, args.brand)

    # --- Stage 10: Upload ---
    if args.drive_folder and not args.skip_upload:
        print("\n" + "=" * 40)
        print("STAGE 10: Google Drive Upload")
        print("=" * 40)
        upload_to_drive(output_dir, args.drive_folder, args.brand)

    # --- Summary ---
    print("\n" + "=" * 60)
    print("PIPELINE COMPLETE")
    print("=" * 60)

    total_scenes = len(brand_prompts)
    animated = sum(1 for r in animation_results if r.get("status") in ("success", "cached"))
    synced = sum(1 for r in lipsync_results if r.get("status") in ("success", "cached"))

    print(f"  Scenes: {total_scenes}")
    print(f"  Animated: {animated}/{total_scenes}")
    print(f"  Lip-synced: {synced}/{total_scenes}")
    print(f"  Segments: {len(segment_paths)}")
    print(f"  Final video: {final_path or 'FAILED'}")
    print(f"  Output dir: {output_dir}")


if __name__ == "__main__":
    main()
