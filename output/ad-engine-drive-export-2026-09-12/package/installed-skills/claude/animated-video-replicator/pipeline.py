#!/usr/bin/env python3
"""
Animated Video Replicator Pipeline

Takes a reference animated video ad, extracts the script and scene structure,
rewrites the script for a target brand, analyzes each scene via Gemini,
generates brand-adapted animated scenes via Veo 3.1, and produces an assembly guide.

Usage:
    python3 pipeline.py --video ref.mp4 --brand Motilli --concept GG-ANI-01 --skip-upload

    # Or with a GetHookd URL (auto-downloads the video):
    python3 pipeline.py --video "https://app.gethookd.ai/share/ad/86606845?signature=[REDACTED_SECRET]" --brand Motilli --concept GG-ANI-01 --skip-upload

    # Or with just a GetHookd ad ID:
    python3 pipeline.py --video 86606845 --brand Motilli --concept GG-ANI-01 --skip-upload
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

# Add tools directory to path for gethookd_resolver
sys.path.insert(0, os.path.expanduser("~/Documents/marketing brain/tools"))
from gethookd_resolver import resolve_video_input, is_gethookd_url

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

VAULT_ROOT = os.path.expanduser("~/Documents/marketing brain")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "[REDACTED_SECRET]")

# Models
GEMINI_ANALYSIS_MODEL = "gemini-2.5-flash"       # Video analysis + script adaptation

# Scene detection
ANIMATED_INTERVAL = 3.0       # Extract a keyframe every N seconds (for animated video)
SCENE_THRESHOLD = 0.3         # ffmpeg scene detection threshold (backup)
MIN_SCENE_DURATION = 2.0      # Minimum seconds between scenes

# Veo 3.1 config
VEO_MAX_RETRIES = 3
VEO_POLL_INTERVAL = 15        # seconds
VEO_RATE_LIMIT_BACKOFF = 120  # seconds base backoff for 429s

# Brand context cap
MAX_BRAND_CONTEXT_CHARS = 30000

# ---------------------------------------------------------------------------
# Brand Registry
# ---------------------------------------------------------------------------

BRAND_REGISTRY = {
    "motilli": {
        "research_docs": [
            os.path.join(VAULT_ROOT, "brands/motilli/Motilli_Master_Copywriting_Brief.md"),
            os.path.join(VAULT_ROOT, "brands/motilli/Motilli_Product_Context.md"),
            os.path.join(VAULT_ROOT, "brands/motilli/Motilli_Avatar_VoC.md"),
        ],
        "product_images": [
            "/Users/brooksorradre2/Documents/marketing brain/brands/motilli/website assets/product reference.png",
            os.path.join(VAULT_ROOT, "brands/motilli/website assets/motilli product reference.png"),
            os.path.join(VAULT_ROOT, "brands/motilli/website assets/product reference.png"),
            os.path.join(VAULT_ROOT, "brands/motilli/website assets/gummy.png"),
            os.path.join(VAULT_ROOT, "brands/motilli/website assets/hand holding gummies.jpeg"),
        ],
        "default_product_context": (
            "Celery juice fiber gummies for GLP-1 users — supports gut health "
            "during weight loss medication. Contains prebiotic fiber from celery juice "
            "to feed beneficial gut bacteria and reduce bloating."
        ),
        "product_visual_description": (
            "A clear plastic jar (NOT glass, NOT opaque) filled with DARK GREEN gummies. "
            "WHITE screw-on cap (NOT green, NOT mint). "
            "Label: solid green background with lowercase white 'motilli' text at top, "
            "then 'CELERY JUICE FIBER GUMMIES' in white text below. "
            "Small green apple icon at bottom of label. "
            "The jar is see-through — you can clearly see the dark green gummies inside. "
            "60 count. The overall color palette is green and white."
        ),
    },
    "lunessa": {
        "research_docs": [
            os.path.join(VAULT_ROOT, "brands/lunessa/fh research docs/Lunessa Research Docs 3.0/Lunessa Avatar Sheet.pdf"),
            os.path.join(VAULT_ROOT, "brands/lunessa/fh research docs/Lunessa Research Docs 3.0/Lunessa_Master_Copywriting_Brief.docx"),
            os.path.join(VAULT_ROOT, "brands/lunessa/menopause research 2.0/Lunessa_Master_Strategic_Brief.docx"),
        ],
        "product_images": [
            os.path.join(VAULT_ROOT, "brands/lunessa/fh research docs/Lunessa Research Docs 3.0/lunessa spelling corrected.jpg"),
        ],
        "default_product_context": (
            "Lunessa Red Yeast Rice + CoQ10 Gummies — heart health supplement for women. "
            "Supports healthy cholesterol levels naturally with clinically studied ingredients."
        ),
    },
    "velantra": {
        "research_docs": [],
        "product_images": [],
        "default_product_context": "",
    },
}

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def log(stage, msg):
    print(f"[{stage}] {msg}", flush=True)

# ---------------------------------------------------------------------------
# Progress tracking
# ---------------------------------------------------------------------------

class Progress:
    """Simple JSON-based progress tracker for incremental runs."""

    def __init__(self, output_dir):
        self.path = os.path.join(output_dir, ".progress.json")
        self.data = {}
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                self.data = json.load(f)

    def is_done(self, stage):
        return self.data.get(stage, {}).get("done", False)

    def mark_done(self, stage, info=None):
        self.data[stage] = {"done": True, "info": info or {}, "ts": time.time()}
        self._save()

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=2)

# ---------------------------------------------------------------------------
# Stage 1: Scene Detection & Frame Extraction
# ---------------------------------------------------------------------------

def extract_scenes(video_path, output_dir):
    """Extract keyframes from animated video using interval + scene detection."""
    frames_dir = os.path.join(output_dir, "frames")
    os.makedirs(frames_dir, exist_ok=True)

    # Get video duration
    probe = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", video_path],
        capture_output=True, text=True,
    )
    duration = float(json.loads(probe.stdout)["format"]["duration"])
    log("Stage1", f"Video duration: {duration:.1f}s")

    # Extract frames at 2fps for Gemini analysis
    log("Stage1", "Extracting frames at 2fps...")
    subprocess.run(
        ["ffmpeg", "-y", "-i", video_path, "-vf", "fps=2",
         os.path.join(frames_dir, "frame_%04d.jpg")],
        capture_output=True,
    )

    # Interval-based keyframes (for animated videos with smooth transitions)
    timestamps = []
    t = 0.0
    while t < duration:
        timestamps.append(round(t, 2))
        t += ANIMATED_INTERVAL

    # Also run scene detection as backup
    scene_cmd = [
        "ffmpeg", "-i", video_path,
        "-filter:v", f"select='gt(scene,{SCENE_THRESHOLD})',showinfo",
        "-vsync", "vfr", "-f", "null", "-",
    ]
    result = subprocess.run(scene_cmd, capture_output=True, text=True)
    for line in result.stderr.split("\n"):
        if "pts_time:" in line:
            match = re.search(r"pts_time:(\d+\.?\d*)", line)
            if match:
                ts = float(match.group(1))
                # Only add if not too close to existing timestamps
                if all(abs(ts - existing) > 1.5 for existing in timestamps):
                    timestamps.append(round(ts, 2))

    timestamps = sorted(set(timestamps))
    log("Stage1", f"Found {len(timestamps)} keyframe timestamps")

    # Extract keyframe PNGs at each timestamp
    keyframes = []
    for i, ts in enumerate(timestamps):
        scene_num = f"{i+1:03d}"
        kf_path = os.path.join(frames_dir, f"keyframe_{scene_num}.png")
        subprocess.run(
            ["ffmpeg", "-y", "-ss", str(ts), "-i", video_path,
             "-frames:v", "1", "-q:v", "1", kf_path],
            capture_output=True,
        )
        if os.path.exists(kf_path):
            keyframes.append({"scene_number": i + 1, "timestamp": ts, "keyframe": kf_path})

    log("Stage1", f"Extracted {len(keyframes)} keyframes")
    return {"keyframes": keyframes, "duration": duration, "timestamps": timestamps}


# ---------------------------------------------------------------------------
# Stage 2: Full Video Analysis via Gemini
# ---------------------------------------------------------------------------

def analyze_video(video_path, brand_knowledge, output_dir):
    """Upload full video to Gemini and get comprehensive analysis."""
    from google import genai
    from google.genai import types

    analysis_dir = os.path.join(output_dir, "analysis")
    os.makedirs(analysis_dir, exist_ok=True)

    client = genai.Client(api_key=GEMINI_API_KEY)

    # Upload video
    log("Stage2", "Uploading video to Gemini...")
    video_file = client.files.upload(file=video_path)

    # Wait for processing
    while video_file.state.name == "PROCESSING":
        log("Stage2", "  Waiting for video processing...")
        time.sleep(5)
        video_file = client.files.get(name=video_file.name)

    if video_file.state.name != "ACTIVE":
        raise RuntimeError(f"Video processing failed: {video_file.state.name}")

    log("Stage2", "Video ready. Analyzing...")

    brand_context = brand_knowledge.get("context_text", "")
    product_context = brand_knowledge.get("default_product_context", "")

    prompt = f"""You are a world-class video ad creative analyst. Analyze this animated video ad in extreme detail.

BRAND CONTEXT (this is the brand we want to REPLICATE this ad for — use this to understand what product adaptations are needed):
Product: {product_context}
{brand_context[:10000] if brand_context else '(No additional brand context)'}

Return a JSON object with this EXACT structure:
{{
  "full_transcript": "Complete transcript with timestamps in format [MM:SS] text...",
  "scenes": [
    {{
      "scene_number": 1,
      "start_time": 0.0,
      "end_time": 6.0,
      "visual_description": "Detailed description of what's shown in this scene",
      "animation_style": "3D CGI, cartoonish anthropomorphic characters",
      "characters": [
        {{
          "name": "Probiotics",
          "description": "Light blue pill-shaped character with doctor's coat and stethoscope",
          "role": "competitor_product"
        }}
      ],
      "environment": "Inside human colon, pinkish-orange textured walls with villi",
      "text_overlay": "HI",
      "narration": "Hi, I'm Probiotics. And I can't do anything when parasites are already living inside you eating your food.",
      "motion": "Character floats and gestures with hands. Camera slowly tracks forward through colon.",
      "mood": "concerned, helpless",
      "color_palette": ["pinkish-orange", "light blue", "dark grey"],
      "has_product": false,
      "scene_role": "competitor_failure",
      "transition_to_next": "Quick cut"
    }}
  ],
  "overall_style": {{
    "animation_type": "3D CGI with cartoonish anthropomorphic characters",
    "rendering_quality": "High-quality, smooth surfaces, detailed organic textures",
    "lighting": "Soft diffused ambient with dynamic glowing effects",
    "environment": "Stylized internal human anatomy (colon/intestines)",
    "character_design": "Anthropomorphic product characters with cartoon faces, doctor coats"
  }},
  "color_palette": ["pinkish-orange", "dark brown", "golden yellow", "light blue", "white"],
  "narrative_structure": {{
    "type": "competitor_comparison_to_hero",
    "flow": "Multiple competitors fail → Hero product introduced → Hero demonstrates superiority → Benefits/transformation",
    "competitor_count": 5,
    "competitor_products": ["Probiotics", "Juice Cleanse", "Fiber Supplements", "Detox Tea", "Laxatives"],
    "hero_product": "Soursop Bitters"
  }},
  "music_description": "Upbeat, cheerful, whimsical with light bouncy instrumentation",
  "text_overlay_style": "Bold white text with black outline, 1-3 words at a time, bottom center"
}}

Be extremely thorough. Every scene must be captured. The transcript must be word-for-word accurate with timestamps.
Return ONLY valid JSON — no markdown, no explanation."""

    response = client.models.generate_content(
        model=GEMINI_ANALYSIS_MODEL,
        contents=[video_file, prompt],
    )

    # Parse JSON response
    text = response.text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)

    analysis = json.loads(text)

    # Save
    out_path = os.path.join(analysis_dir, "full_video_analysis.json")
    with open(out_path, "w") as f:
        json.dump(analysis, f, indent=2)

    log("Stage2", f"Analysis complete: {len(analysis.get('scenes', []))} scenes identified")
    log("Stage2", f"Narrative structure: {analysis.get('narrative_structure', {}).get('type', 'unknown')}")

    return analysis


# ---------------------------------------------------------------------------
# Stage 3: Script Adaptation (Copywriting Agent)
# ---------------------------------------------------------------------------

def adapt_script(analysis, brand_knowledge, brand, output_dir, script_direction=None):
    """Rewrite the reference script for the target brand."""
    from google import genai
    from google.genai import types

    scripts_dir = os.path.join(output_dir, "scripts")
    os.makedirs(scripts_dir, exist_ok=True)

    client = genai.Client(api_key=GEMINI_API_KEY)

    # Save original transcript
    original_transcript = analysis.get("full_transcript", "")
    with open(os.path.join(scripts_dir, "original_transcript.md"), "w") as f:
        f.write(f"# Original Transcript\n\n{original_transcript}\n")

    # Build the adaptation prompt
    brand_context = brand_knowledge.get("context_text", "")
    product_context = brand_knowledge.get("default_product_context", "")
    narrative = analysis.get("narrative_structure", {})
    scenes = analysis.get("scenes", [])

    scene_breakdown = ""
    for s in scenes:
        scene_breakdown += f"\n### Scene {s['scene_number']} ({s['start_time']:.1f}s - {s['end_time']:.1f}s)\n"
        scene_breakdown += f"- **Role:** {s.get('scene_role', 'unknown')}\n"
        scene_breakdown += f"- **Characters:** {', '.join(c['name'] for c in s.get('characters', []))}\n"
        scene_breakdown += f"- **Narration:** {s.get('narration', '')}\n"
        scene_breakdown += f"- **Text overlay:** {s.get('text_overlay', '')}\n"

    direction_note = ""
    if script_direction:
        direction_note = f"\n\nADDITIONAL DIRECTION FROM THE USER:\n{script_direction}\n"

    prompt = f"""You are a world-class direct response copywriter specializing in health supplement ads.

TASK: Rewrite the following animated video ad script for a DIFFERENT brand. You must preserve the EXACT narrative structure, pacing, and emotional beats while adapting the product, mechanism, competitors, and claims.

## ORIGINAL SCRIPT STRUCTURE

Narrative type: {narrative.get('type', 'competitor_comparison_to_hero')}
Flow: {narrative.get('flow', '')}
Total scenes: {len(scenes)}
Competitor products in original: {', '.join(narrative.get('competitor_products', []))}
Hero product in original: {narrative.get('hero_product', '')}

{scene_breakdown}

## TARGET BRAND

Product: {product_context}

Brand Knowledge:
{brand_context[:15000] if brand_context else '(No additional brand context available)'}
{direction_note}

## RULES

1. **PRESERVE the exact same number of scenes** ({len(scenes)} scenes)
2. **PRESERVE the narrative structure** — same number of competitor "failures" before the hero reveal
3. **Map each competitor to a relevant competitor** for the target brand's category
4. **Adapt the mechanism** — use the target brand's actual product mechanism and ingredients
5. **Keep the same emotional arc** — frustration → confidence → transformation
6. **Match the word count per scene** — approximately the same speaking duration
7. **Preserve text overlay structure** — same key-word emphasis pattern (1-3 bold words per overlay)
8. **Use the brand's authentic voice** — pulled from the brand knowledge above
9. **Keep it conversational** — this is spoken narration for animation, not written copy
10. **ONE hero character only** — the hero product must be represented as a SINGLE character: the actual product BOTTLE (anthropomorphic walking version with cartoon arms, legs, eyes). Do NOT use gummy bears, capsules, or any other form. The hero_character_description must describe the BOTTLE. This same character must appear identically in every hero/product/benefit/final scene.

## OUTPUT FORMAT

Return a JSON object with this EXACT structure:
{{
  "adapted_scenes": [
    {{
      "scene_number": 1,
      "original_narration": "Hi, I'm Probiotics...",
      "adapted_narration": "Hi, I'm generic fiber supplements...",
      "text_overlays": ["HI", "GENERIC FIBER SUPPLEMENTS", "I CAN'T DO ANYTHING..."],
      "character_name": "Generic Fiber Supplements",
      "character_description": "A beige fiber supplement capsule with a concerned expression and doctor coat",
      "scene_role": "competitor_failure",
      "adapted_visual_notes": "Same colon environment. This character represents generic fiber supplements that don't address the root cause."
    }}
  ],
  "hero_product_name": "Motilli Celery Juice Fiber Gummies",
  "hero_character_description": "The actual Motilli product BOTTLE — an anthropomorphic walking version of the real product bottle with cartoon arms, legs, eyes, and a friendly expression. Use ONLY the bottle as the hero character (NOT a gummy bear, NOT a capsule — the BOTTLE itself). Must look identical in every hero scene.",
  "competitor_mapping": {{
    "Probiotics": "Generic Fiber Supplements",
    "Juice Cleanse": "Psyllium Husk Powder",
    "...": "..."
  }},
  "key_mechanism": "Prebiotic celery juice fiber that feeds beneficial gut bacteria",
  "full_adapted_script": "Complete adapted script as continuous text with scene breaks"
}}

Return ONLY valid JSON."""

    log("Stage3", "Running copywriting agent to adapt script...")

    response = client.models.generate_content(
        model=GEMINI_ANALYSIS_MODEL,
        contents=prompt,
    )

    text = response.text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)

    adapted = json.loads(text)

    # Validate scene count
    adapted_count = len(adapted.get("adapted_scenes", []))
    original_count = len(scenes)
    if adapted_count != original_count:
        log("Stage3", f"WARNING: Scene count mismatch! Original: {original_count}, Adapted: {adapted_count}")
        log("Stage3", "Re-prompting with strict count constraint...")
        # Retry with explicit constraint
        response = client.models.generate_content(
            model=GEMINI_ANALYSIS_MODEL,
            contents=f"{prompt}\n\nCRITICAL: You MUST return EXACTLY {original_count} scenes. No more, no less.",
        )
        text = response.text.strip()
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\s*", "", text)
            text = re.sub(r"\s*```$", "", text)
        adapted = json.loads(text)

    # Save adapted script as markdown
    with open(os.path.join(scripts_dir, "adapted_script.md"), "w") as f:
        f.write(f"# Adapted Script — {brand}\n\n")
        f.write(f"**Hero Product:** {adapted.get('hero_product_name', brand)}\n")
        f.write(f"**Key Mechanism:** {adapted.get('key_mechanism', '')}\n\n")
        f.write("## Competitor Mapping\n\n")
        for orig, new in adapted.get("competitor_mapping", {}).items():
            f.write(f"- {orig} → {new}\n")
        f.write("\n## Scene-by-Scene\n\n")
        for s in adapted.get("adapted_scenes", []):
            f.write(f"### Scene {s['scene_number']} — {s.get('scene_role', '')}\n")
            f.write(f"**Character:** {s.get('character_name', '')}\n")
            f.write(f"**Original:** {s.get('original_narration', '')}\n")
            f.write(f"**Adapted:** {s.get('adapted_narration', '')}\n")
            f.write(f"**Text Overlays:** {', '.join(s.get('text_overlays', []))}\n\n")
        f.write("## Full Script\n\n")
        f.write(adapted.get("full_adapted_script", ""))
        f.write("\n")

    # Save JSON
    with open(os.path.join(scripts_dir, "adapted_script.json"), "w") as f:
        json.dump(adapted, f, indent=2)

    log("Stage3", f"Script adapted: {len(adapted.get('adapted_scenes', []))} scenes")
    log("Stage3", f"Hero product: {adapted.get('hero_product_name', 'unknown')}")
    log("Stage3", f"Competitor mapping: {adapted.get('competitor_mapping', {})}")

    return adapted


# ---------------------------------------------------------------------------
# Stage 4: Brand-Adapted Scene Prompts for Veo
# ---------------------------------------------------------------------------

def generate_veo_prompts(analysis, adapted_script, brand_knowledge, brand, output_dir):
    """Generate Veo 3.1 text-to-video prompts for each scene."""
    from google import genai
    from google.genai import types

    prompts_dir = os.path.join(output_dir, "prompts")
    os.makedirs(prompts_dir, exist_ok=True)

    client = genai.Client(api_key=GEMINI_API_KEY)

    overall_style = analysis.get("overall_style", {})
    color_palette = analysis.get("color_palette", [])
    text_overlay_style = analysis.get("text_overlay_style", "")
    original_scenes = analysis.get("scenes", [])
    adapted_scenes = adapted_script.get("adapted_scenes", [])
    product_context = brand_knowledge.get("default_product_context", "")

    style_description = json.dumps(overall_style, indent=2)

    veo_prompts = []

    for i, (orig, adapted) in enumerate(zip(original_scenes, adapted_scenes)):
        scene_num = orig.get("scene_number", i + 1)
        duration = orig.get("end_time", 0) - orig.get("start_time", 0)
        duration = max(3, min(8, duration))  # Clamp to 3-8s for Veo

        # Build the Veo prompt
        prompt_text = f"""You are a Veo 3.1 prompt engineer. Create a text-to-video prompt for an animated scene.

REFERENCE SCENE (from original ad):
- Visual: {orig.get('visual_description', '')}
- Animation style: {orig.get('animation_style', '')}
- Environment: {orig.get('environment', '')}
- Motion: {orig.get('motion', '')}
- Mood: {orig.get('mood', '')}
- Color palette: {', '.join(orig.get('color_palette', []))}
- Characters: {json.dumps(orig.get('characters', []))}

ADAPTED VERSION (for target brand):
- Character: {adapted.get('character_name', '')} — {adapted.get('character_description', '')}
- Narration: {adapted.get('adapted_narration', '')}
- Text overlays: {', '.join(adapted.get('text_overlays', []))}
- Scene role: {adapted.get('scene_role', '')}
- Visual notes: {adapted.get('adapted_visual_notes', '')}

TARGET BRAND: {product_context}

OVERALL ANIMATION STYLE:
{style_description}

COLOR PALETTE: {', '.join(color_palette)}

HERO CHARACTER RULE: If this is a hero/product/benefit/final scene, the hero character MUST be the actual product BOTTLE — an anthropomorphic walking version of the real product bottle with cartoon arms, legs, eyes, and a friendly expression, wearing a doctor coat. Use ONLY the bottle. Do NOT use gummy bears, capsules, pills, or multiple product forms. The bottle character must look IDENTICAL across all hero scenes.

Write a single, detailed Veo 3.1 prompt that will generate this animated scene WITH AUDIO. The prompt should:
1. Describe the EXACT visual composition (environment, camera angle, lighting)
2. Describe the character appearance — for hero scenes, always describe the SAME anthropomorphic bottle character
3. Describe the motion/animation (what moves, how)
4. Specify the animation style (3D CGI, cartoonish, etc.)
5. Do NOT include ANY text, captions, subtitles, or text overlays in the video. The video must be purely visual with no on-screen text whatsoever.
6. Be approximately {int(duration)} seconds of animation
7. Use 9:16 vertical format
8. CRITICAL — AUDIO/VOICEOVER: The character MUST speak the following dialogue aloud in a clear, friendly, conversational voice: "{adapted.get('adapted_narration', '')}". Include this as explicit spoken dialogue in the prompt. Also include upbeat, whimsical background music and cartoon sound effects (sparkles, whooshes, squishy sounds).

The prompt MUST describe the character speaking/narrating the dialogue. Veo 3.1 generates audio natively — the character should be talking, with lip movement matching the dialogue.
9. IMPORTANT: Do NOT render any text, titles, captions, or words on screen. Zero text overlays.

Return ONLY the Veo prompt text — no JSON, no explanation. Just the prompt."""

        response = client.models.generate_content(
            model=GEMINI_ANALYSIS_MODEL,
            contents=prompt_text,
        )

        veo_prompt = response.text.strip()
        if veo_prompt.startswith('"') and veo_prompt.endswith('"'):
            veo_prompt = veo_prompt[1:-1]

        veo_prompts.append({
            "scene_number": scene_num,
            "veo_prompt": veo_prompt,
            "duration": duration,
            "adapted_narration": adapted.get("adapted_narration", ""),
            "text_overlays": adapted.get("text_overlays", []),
            "scene_role": adapted.get("scene_role", ""),
        })

        log("Stage4", f"  Scene {scene_num}: prompt generated ({len(veo_prompt)} chars)")

        # Rate limiting
        time.sleep(1)

    # Save
    out_path = os.path.join(prompts_dir, "veo_scene_prompts.json")
    with open(out_path, "w") as f:
        json.dump(veo_prompts, f, indent=2)

    log("Stage4", f"Generated {len(veo_prompts)} Veo prompts")
    return veo_prompts


# ---------------------------------------------------------------------------
# Stage 5: Generate Animated Scenes via Veo 3.1
# ---------------------------------------------------------------------------

def generate_reference_frames(analysis, adapted_script, brand_knowledge, output_dir):
    """Stage 4b: Use Nano Banana 2 image-to-image to transform EVERY reference keyframe.

    ALWAYS image-to-image — never text-to-image.
    Generates a hero character template first, then uses it for consistency across all hero scenes.
    """
    from google import genai
    from google.genai import types

    i2i_dir = os.path.join(output_dir, "i2i_frames")
    os.makedirs(i2i_dir, exist_ok=True)

    client = genai.Client(api_key=GEMINI_API_KEY)
    GEMINI_IMAGE_MODEL = "gemini-3.1-flash-image-preview"

    # Load product reference image (use the primary one)
    product_part = None
    for pimg in brand_knowledge.get("product_images", []):
        if os.path.exists(pimg):
            ext = Path(pimg).suffix.lower()
            mime = "image/jpeg" if ext in (".jpg", ".jpeg") else f"image/{ext.lstrip('.')}"
            with open(pimg, "rb") as f:
                product_part = types.Part(inline_data=types.Blob(data=f.read(), mime_type=mime))
            break  # Use the first (primary) product image

    product_visual_desc = brand_knowledge.get("product_visual_description", "")

    # --- Step 1: Generate hero character template ---
    # Create ONE consistent hero character render, then reuse it as reference for all hero scenes
    hero_template_path = os.path.join(i2i_dir, "hero_character_template.png")
    hero_template_part = None

    if os.path.exists(hero_template_path) and os.path.getsize(hero_template_path) > 0:
        log("Stage4b", "Hero character template: already exists, loading")
        with open(hero_template_path, "rb") as f:
            hero_template_part = types.Part(inline_data=types.Blob(data=f.read(), mime_type="image/png"))
    else:
        log("Stage4b", "Generating hero character template...")
        # Find any hero scene's reference frame to use as base
        frames_dir = os.path.join(output_dir, "frames")
        original_scenes = analysis.get("scenes", [])
        adapted_scenes = adapted_script.get("adapted_scenes", [])

        hero_ref_frame = None
        for orig, adapted in zip(original_scenes, adapted_scenes):
            role = adapted.get("scene_role", "")
            if "hero" in role or "product" in role:
                start_time = orig.get("start_time", 0)
                frame_idx = max(1, int(start_time * 2) + 1)
                candidate = os.path.join(frames_dir, f"frame_{frame_idx:04d}.jpg")
                if os.path.exists(candidate):
                    hero_ref_frame = candidate
                    break

        if hero_ref_frame and product_part:
            with open(hero_ref_frame, "rb") as f:
                hero_ref_bytes = f.read()

            template_prompt = (
                f"Edit this animated scene image. Replace the main character with an anthropomorphic 3D cartoon version of "
                f"the product shown in the reference photo. "
                f"The product looks like this: {product_visual_desc} "
                f"Match the product reference photo EXACTLY — same jar, same label, same cap color, same gummies. "
                f"Give the bottle cartoon arms, legs, big expressive eyes, and a friendly smile. "
                f"Add a white doctor coat and stethoscope. "
                f"Keep the same 3D CGI animated style and background from the original scene. "
                f"Do NOT add any text or captions. "
                f"This character design will be reused in every scene — make it clean, clear, and well-defined."
            )
            parts = [
                types.Part(inline_data=types.Blob(data=hero_ref_bytes, mime_type="image/jpeg")),
                product_part,
                types.Part(text=template_prompt),
            ]
            try:
                response = client.models.generate_content(
                    model=GEMINI_IMAGE_MODEL,
                    contents=types.Content(parts=parts),
                    config=types.GenerateContentConfig(response_modalities=["IMAGE", "TEXT"]),
                )
                for part in response.candidates[0].content.parts:
                    if part.inline_data is not None:
                        with open(hero_template_path, "wb") as f:
                            f.write(part.inline_data.data)
                        hero_template_part = types.Part(inline_data=types.Blob(
                            data=part.inline_data.data, mime_type="image/png"
                        ))
                        log("Stage4b", f"Hero character template: generated ({len(part.inline_data.data)} bytes)")
                        break
            except Exception as e:
                log("Stage4b", f"Hero character template: error - {str(e)[:200]}")

    # --- Step 2: Transform every scene using image-to-image ---
    original_scenes = analysis.get("scenes", [])
    adapted_scenes = adapted_script.get("adapted_scenes", [])
    frames_dir = os.path.join(output_dir, "frames")
    results = []

    for i, (orig, adapted) in enumerate(zip(original_scenes, adapted_scenes)):
        scene_num = orig.get("scene_number", i + 1)
        out_path = os.path.join(i2i_dir, f"scene_{scene_num:03d}_i2i.png")

        if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
            log("Stage4b", f"  Scene {scene_num}: already transformed, skipping")
            results.append({"scene_number": scene_num, "path": out_path})
            continue

        # Find the closest reference keyframe — REQUIRED (no text-to-image fallback)
        start_time = orig.get("start_time", 0)
        frame_idx = max(1, int(start_time * 2) + 1)
        ref_frame = os.path.join(frames_dir, f"frame_{frame_idx:04d}.jpg")
        if not os.path.exists(ref_frame):
            ref_frame = os.path.join(frames_dir, f"keyframe_{scene_num:03d}.png")
        if not os.path.exists(ref_frame):
            # Try adjacent frames
            for offset in [-1, 1, -2, 2, -3, 3]:
                alt = os.path.join(frames_dir, f"frame_{max(1, frame_idx + offset):04d}.jpg")
                if os.path.exists(alt):
                    ref_frame = alt
                    break
        if not os.path.exists(ref_frame):
            log("Stage4b", f"  Scene {scene_num}: NO reference frame found — cannot do i2i, skipping")
            results.append({"scene_number": scene_num, "path": None})
            continue

        with open(ref_frame, "rb") as f:
            ref_bytes = f.read()

        role = adapted.get("scene_role", "")
        char_name = adapted.get("character_name", "")
        char_desc = adapted.get("character_description", "")
        visual_notes = adapted.get("adapted_visual_notes", "")

        is_hero_scene = "hero" in role or "product" in role or "benefit" in role or "final" in role

        # Build parts: always start with reference frame (image-to-image)
        parts = [
            types.Part(inline_data=types.Blob(data=ref_bytes, mime_type="image/jpeg")),
        ]

        if is_hero_scene:
            # Add hero character template for consistency
            if hero_template_part:
                parts.append(hero_template_part)
            # Add product reference photo
            if product_part:
                parts.append(product_part)

            edit_prompt = (
                f"Edit this animated scene image. Replace the hero character with the EXACT SAME character "
                f"shown in the second image (the hero character template). "
                f"The character is an anthropomorphic version of the product in the third image. "
                f"Product details: {product_visual_desc} "
                f"CRITICAL: The character must look IDENTICAL to the template — copy the template character's face EXACTLY: "
                f"same eye shape, same eye color, same eye size, same mouth shape, same expression style, "
                f"same head-to-body ratio, same arm style, same leg style, same doctor coat. "
                f"The character's face and body proportions must be a pixel-perfect match to the template. "
                f"Keep the EXACT same background, environment, lighting, camera angle, and composition from the first image. "
                f"REMOVE all text, captions, subtitles, watermarks, UI elements, icons, and overlays from the scene. "
                f"The final image must contain ZERO text or graphic overlays of any kind. "
                f"Visual notes: {visual_notes}"
            )
        else:
            # Competitor/other scenes — still image-to-image
            if product_part:
                parts.append(product_part)

            edit_prompt = (
                f"Edit this animated scene image to adapt it for a different brand. "
                f"The character in this scene is: {char_name} — {char_desc}. "
                f"Adapt the character's appearance to match this description while keeping "
                f"the EXACT same background, environment, lighting, camera angle, and composition. "
                f"Keep the same style: 3D CGI, cartoonish, anthropomorphic with doctor coat. "
                f"Do NOT add any text, captions, or words to the image. "
                f"Visual notes: {visual_notes}"
            )

        parts.append(types.Part(text=edit_prompt))

        try:
            response = client.models.generate_content(
                model=GEMINI_IMAGE_MODEL,
                contents=types.Content(parts=parts),
                config=types.GenerateContentConfig(response_modalities=["IMAGE", "TEXT"]),
            )

            saved = False
            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    with open(out_path, "wb") as f:
                        f.write(part.inline_data.data)
                    log("Stage4b", f"  Scene {scene_num}: transformed ({len(part.inline_data.data)} bytes)")
                    results.append({"scene_number": scene_num, "path": out_path})
                    saved = True
                    break

            if not saved:
                log("Stage4b", f"  Scene {scene_num}: no image returned")
                results.append({"scene_number": scene_num, "path": None})

        except Exception as e:
            log("Stage4b", f"  Scene {scene_num}: error - {str(e)[:200]}")
            results.append({"scene_number": scene_num, "path": None})

        time.sleep(3)  # Rate limiting

    succeeded = sum(1 for r in results if r.get("path"))
    log("Stage4b", f"Image-to-image complete: {succeeded}/{len(results)} frames transformed")
    return results


def audit_i2i_frames(i2i_frames, brand_knowledge, hero_template_path, adapted_script, analysis, output_dir):
    """Stage 4c: QA audit every i2i frame. Checks for rule violations and auto-retries failures."""
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=GEMINI_API_KEY)
    product_visual_desc = brand_knowledge.get("product_visual_description", "")
    adapted_scenes = adapted_script.get("adapted_scenes", [])

    # Load hero template for comparison
    hero_template_bytes = None
    if os.path.exists(hero_template_path):
        with open(hero_template_path, "rb") as f:
            hero_template_bytes = f.read()

    # Load product reference
    product_ref_bytes = None
    for pimg in brand_knowledge.get("product_images", []):
        if os.path.exists(pimg):
            with open(pimg, "rb") as f:
                product_ref_bytes = f.read()
            break

    MAX_RETRIES = 2

    # Different rules for hero vs competitor scenes
    hero_audit_rules = (
        "Check this animated scene image for ALL of the following rules:\n"
        "1. NO OVERLAY TEXT — no captions, subtitles, watermarks, or UI overlays floating OVER the scene. "
        "Text that is ON the product's label is FINE and expected — do NOT flag label text as a violation.\n"
        "2. NO EXTRA CHARACTERS — only ONE hero product character should be present. No competitor characters, no extra pills, no extra bottles.\n"
        "3. CORRECT EYES — the character must have exactly 2 eyes (not 4, not 0)\n"
        f"4. PRODUCT ACCURACY — the hero product must match: {product_visual_desc}\n"
        "5. CHARACTER CONSISTENCY — the character must match the provided hero template (same face, proportions, style)\n"
        "6. NO ANATOMICAL ERRORS — arms, legs, face should look natural for a cartoon character\n\n"
        "Respond ONLY with a JSON object: {\"pass\": true/false, \"violations\": [\"list of rule numbers broken\"], \"details\": \"brief description\"}\n"
        "Be strict. If ANY rule is broken, pass must be false."
    )

    competitor_audit_rules = (
        "Check this animated scene image for the following rules. "
        "This is a COMPETITOR scene — the character shown is a COMPETITOR product, NOT the hero product. "
        "Do NOT check whether the character matches the hero product description.\n"
        "1. NO OVERLAY TEXT — no captions, subtitles, watermarks, or UI overlays floating OVER the scene.\n"
        "2. CORRECT EYES — the character must have exactly 2 eyes (not 4, not 0)\n"
        "3. NO ANATOMICAL ERRORS — arms, legs, face should look natural for a cartoon character\n"
        "4. SCENE COHERENCE — the scene should be a clean 3D CGI animated scene inside the human gut/digestive system\n\n"
        "Respond ONLY with a JSON object: {\"pass\": true/false, \"violations\": [\"list of rule numbers broken\"], \"details\": \"brief description\"}\n"
        "Be strict. If ANY rule is broken, pass must be false."
    )

    results = []
    for frame_data in i2i_frames:
        scene_num = frame_data["scene_number"]
        frame_path = frame_data.get("path")

        if not frame_path or not os.path.exists(frame_path):
            results.append(frame_data)
            continue

        # Find scene role
        scene_role = ""
        if scene_num - 1 < len(adapted_scenes):
            scene_role = adapted_scenes[scene_num - 1].get("scene_role", "")
        is_hero = "hero" in scene_role or "product" in scene_role or "benefit" in scene_role or "final" in scene_role

        passed = False
        for attempt in range(MAX_RETRIES + 1):
            # Build audit parts
            with open(frame_path, "rb") as f:
                frame_bytes = f.read()

            parts = [types.Part(inline_data=types.Blob(data=frame_bytes, mime_type="image/png"))]
            if is_hero:
                if hero_template_bytes:
                    parts.append(types.Part(text="Hero character template (the character should match this):"))
                    parts.append(types.Part(inline_data=types.Blob(data=hero_template_bytes, mime_type="image/png")))
                if product_ref_bytes:
                    parts.append(types.Part(text="Product reference photo (the product should look like this):"))
                    parts.append(types.Part(inline_data=types.Blob(data=product_ref_bytes, mime_type="image/png")))
                parts.append(types.Part(text=hero_audit_rules))
            else:
                parts.append(types.Part(text=competitor_audit_rules))

            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=types.Content(parts=parts),
                    config=types.GenerateContentConfig(response_modalities=["TEXT"]),
                )
                audit_text = response.candidates[0].content.parts[0].text.strip()
                # Parse JSON from response
                json_match = re.search(r'\{.*\}', audit_text, re.DOTALL)
                if json_match:
                    audit_result = json.loads(json_match.group())
                else:
                    audit_result = {"pass": True, "violations": [], "details": "Could not parse audit"}

                if audit_result.get("pass", True):
                    log("Stage4c", f"  Scene {scene_num}: PASS")
                    passed = True
                    break
                else:
                    violations = audit_result.get("violations", [])
                    details = audit_result.get("details", "")
                    log("Stage4c", f"  Scene {scene_num}: FAIL (rules {violations}) — {details}")

                    if attempt < MAX_RETRIES:
                        log("Stage4c", f"  Scene {scene_num}: regenerating (attempt {attempt + 2})...")
                        # Delete the bad frame and regenerate
                        os.remove(frame_path)
                        # Re-run i2i for just this scene
                        _regenerate_single_frame(
                            scene_num, analysis, adapted_script, brand_knowledge, output_dir,
                            client, hero_template_bytes, product_ref_bytes
                        )
                        if os.path.exists(frame_path) and os.path.getsize(frame_path) > 0:
                            log("Stage4c", f"  Scene {scene_num}: regenerated, re-auditing...")
                        else:
                            log("Stage4c", f"  Scene {scene_num}: regeneration failed")
                            break

            except Exception as e:
                log("Stage4c", f"  Scene {scene_num}: audit error — {str(e)[:150]}")
                passed = True  # Don't block on audit errors
                break

        if not passed:
            log("Stage4c", f"  Scene {scene_num}: FAILED audit after {MAX_RETRIES + 1} attempts — keeping last version")

        results.append(frame_data)
        time.sleep(1)

    pass_count = sum(1 for r in results if r.get("path"))
    log("Stage4c", f"Audit complete: {pass_count}/{len(results)} frames passed")
    return results


def _regenerate_single_frame(scene_num, analysis, adapted_script, brand_knowledge, output_dir,
                              client, hero_template_bytes, product_ref_bytes):
    """Regenerate a single i2i frame for a specific scene."""
    from google.genai import types

    GEMINI_IMAGE_MODEL = "gemini-3.1-flash-image-preview"
    i2i_dir = os.path.join(output_dir, "i2i_frames")
    frames_dir = os.path.join(output_dir, "frames")
    out_path = os.path.join(i2i_dir, f"scene_{scene_num:03d}_i2i.png")

    original_scenes = analysis.get("scenes", [])
    adapted_scenes = adapted_script.get("adapted_scenes", [])
    product_visual_desc = brand_knowledge.get("product_visual_description", "")

    if scene_num - 1 >= len(original_scenes):
        return

    orig = original_scenes[scene_num - 1]
    adapted = adapted_scenes[scene_num - 1]

    start_time = orig.get("start_time", 0)
    frame_idx = max(1, int(start_time * 2) + 1)
    ref_frame = os.path.join(frames_dir, f"frame_{frame_idx:04d}.jpg")
    if not os.path.exists(ref_frame):
        for offset in [-1, 1, -2, 2]:
            alt = os.path.join(frames_dir, f"frame_{max(1, frame_idx + offset):04d}.jpg")
            if os.path.exists(alt):
                ref_frame = alt
                break
    if not os.path.exists(ref_frame):
        return

    with open(ref_frame, "rb") as f:
        ref_bytes = f.read()

    role = adapted.get("scene_role", "")
    visual_notes = adapted.get("adapted_visual_notes", "")
    is_hero = "hero" in role or "product" in role or "benefit" in role or "final" in role

    parts = [types.Part(inline_data=types.Blob(data=ref_bytes, mime_type="image/jpeg"))]

    if is_hero:
        if hero_template_bytes:
            parts.append(types.Part(inline_data=types.Blob(data=hero_template_bytes, mime_type="image/png")))
        if product_ref_bytes:
            ext = brand_knowledge.get("product_images", [""])[0].split(".")[-1].lower()
            mime = "image/jpeg" if ext in ("jpg", "jpeg") else f"image/{ext}"
            parts.append(types.Part(inline_data=types.Blob(data=product_ref_bytes, mime_type=mime)))

        edit_prompt = (
            f"Edit this animated scene image. Replace the hero character with the EXACT SAME character "
            f"shown in the second image (the hero character template). "
            f"The character is an anthropomorphic version of the product in the third image. "
            f"Product details: {product_visual_desc} "
            f"CRITICAL: The character must look IDENTICAL to the template — copy the template character's face EXACTLY: "
            f"same eye shape, same eye color, same eye size, same mouth shape, same expression style, "
            f"same head-to-body ratio, same arm style, same leg style, same doctor coat. "
            f"The character's face and body proportions must be a pixel-perfect match to the template. "
            f"Keep the EXACT same background, environment, lighting, camera angle, and composition from the first image. "
            f"REMOVE all text, captions, subtitles, watermarks, UI elements, icons, and overlays from the scene. "
            f"The final image must contain ZERO text or graphic overlays of any kind. "
            f"Visual notes: {visual_notes}"
        )
    else:
        char_name = adapted.get("character_name", "")
        char_desc = adapted.get("character_description", "")
        edit_prompt = (
            f"Edit this animated scene image to adapt it for a different brand. "
            f"The character in this scene is: {char_name} — {char_desc}. "
            f"Adapt the character's appearance to match this description while keeping "
            f"the EXACT same background, environment, lighting, camera angle, and composition. "
            f"Keep the same style: 3D CGI, cartoonish, anthropomorphic with doctor coat. "
            f"REMOVE all text, captions, subtitles, watermarks, UI elements, icons, and overlays. "
            f"Visual notes: {visual_notes}"
        )

    parts.append(types.Part(text=edit_prompt))

    try:
        response = client.models.generate_content(
            model=GEMINI_IMAGE_MODEL,
            contents=types.Content(parts=parts),
            config=types.GenerateContentConfig(response_modalities=["IMAGE", "TEXT"]),
        )
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                with open(out_path, "wb") as f:
                    f.write(part.inline_data.data)
                log("Stage4c", f"  Scene {scene_num}: regenerated ({len(part.inline_data.data)} bytes)")
                return
    except Exception as e:
        log("Stage4c", f"  Scene {scene_num}: regeneration error — {str(e)[:150]}")


def generate_scenes(veo_prompts, i2i_frames, brand_knowledge, output_dir):
    """Stage 5: Animate i2i frames using Veo 3.1 image-to-video with start frame. Generates audio."""
    import requests
    from google import genai
    from google.genai import types
    import base64

    gen_dir = os.path.join(output_dir, "generated")
    os.makedirs(gen_dir, exist_ok=True)

    client = genai.Client(api_key=GEMINI_API_KEY)

    # Build lookup of i2i frames
    i2i_map = {r["scene_number"]: r.get("path") for r in i2i_frames}

    results = []
    for prompt_data in veo_prompts:
        scene_num = prompt_data["scene_number"]
        out_path = os.path.join(gen_dir, f"scene_{scene_num:03d}_animated.mp4")

        # Skip if already generated
        if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
            log("Stage5", f"  Scene {scene_num}: already generated, skipping")
            results.append({"scene_number": scene_num, "path": out_path, "status": "cached"})
            continue

        # MUST have i2i frame — always image-to-video with start frame
        frame_path = i2i_map.get(scene_num)
        if not frame_path or not os.path.exists(frame_path):
            log("Stage5", f"  Scene {scene_num}: NO i2i frame available, skipping")
            results.append({"scene_number": scene_num, "path": None, "status": "skipped"})
            continue

        log("Stage5", f"  Scene {scene_num}: generating with Veo 3.1 (image-to-video, start frame)...")

        veo_prompt = prompt_data.get("veo_prompt", "")

        # Load start frame image
        with open(frame_path, "rb") as f:
            frame_bytes = f.read()

        start_frame_image = types.Image(
            image_bytes=frame_bytes,
            mime_type="image/png",
        )

        # Determine duration (clamp 5-8s for Veo)
        duration = min(8, max(5, int(prompt_data.get("duration", 5))))

        success = False
        for attempt in range(VEO_MAX_RETRIES):
            try:
                operation = client.models.generate_videos(
                    model="veo-3.1-generate-preview",
                    prompt=veo_prompt,
                    image=start_frame_image,
                    config=types.GenerateVideosConfig(
                        aspect_ratio="9:16",
                        number_of_videos=1,
                        person_generation="allow_adult",
                    ),
                )

                # Poll until done
                elapsed = 0
                while not operation.done:
                    log("Stage5", f"    Waiting... ({elapsed}s)")
                    time.sleep(VEO_POLL_INTERVAL)
                    elapsed += VEO_POLL_INTERVAL
                    operation = client.operations.get(operation)

                if operation.result and operation.result.generated_videos:
                    video = operation.result.generated_videos[0]
                    video_uri = video.video.uri
                    # Append API key if URI is from generativelanguage.googleapis.com
                    if "generativelanguage.googleapis.com" in video_uri:
                        sep = "&" if "?" in video_uri else "?"
                        video_uri = f"{video_uri}{sep}key={GEMINI_API_KEY}"
                    vid_resp = requests.get(video_uri, timeout=120)
                    # Validate we got actual video content, not a JSON error
                    content_type = vid_resp.headers.get("Content-Type", "")
                    if vid_resp.status_code != 200 or "json" in content_type or "text" in content_type:
                        log("Stage5", f"  Scene {scene_num}: download failed (HTTP {vid_resp.status_code}, type={content_type})")
                        log("Stage5", f"    Response: {vid_resp.text[:300]}")
                        continue  # retry
                    with open(out_path, "wb") as f_out:
                        f_out.write(vid_resp.content)
                    file_size = os.path.getsize(out_path)
                    if file_size < 10000:  # Real videos are much larger than 10KB
                        log("Stage5", f"  Scene {scene_num}: file too small ({file_size} bytes), likely not a video")
                        os.remove(out_path)
                        continue  # retry
                    log("Stage5", f"  Scene {scene_num}: saved ({file_size} bytes)")
                    results.append({"scene_number": scene_num, "path": out_path, "status": "success"})
                    success = True
                    break
                else:
                    log("Stage5", f"  Scene {scene_num}: no video returned (attempt {attempt+1})")

            except Exception as e:
                err_str = str(e)
                log("Stage5", f"  Scene {scene_num}: error (attempt {attempt+1}): {err_str}")
                if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                    wait = VEO_RATE_LIMIT_BACKOFF * (attempt + 1)
                    log("Stage5", f"    Rate limited, waiting {wait}s...")
                    time.sleep(wait)
                else:
                    time.sleep(10)

        if not success:
            log("Stage5", f"  Scene {scene_num}: FAILED after {VEO_MAX_RETRIES} attempts")
            results.append({"scene_number": scene_num, "path": None, "status": "failed"})

        time.sleep(5)  # Rate limiting between scenes

    succeeded = sum(1 for r in results if r["status"] in ("success", "cached"))
    failed = sum(1 for r in results if r["status"] == "failed")
    log("Stage5", f"Animation complete: {succeeded} succeeded, {failed} failed")

    return results


# ---------------------------------------------------------------------------
# Assembly Guide
# ---------------------------------------------------------------------------

def generate_assembly_guide(analysis, adapted_script, veo_results, brand, concept, output_dir):
    """Generate the assembly guide markdown for the video editor."""
    guide_path = os.path.join(output_dir, "assembly_guide.md")

    original_scenes = analysis.get("scenes", [])
    adapted_scenes = adapted_script.get("adapted_scenes", [])
    hero = adapted_script.get("hero_product_name", brand)
    mechanism = adapted_script.get("key_mechanism", "")
    mapping = adapted_script.get("competitor_mapping", {})

    # Build result lookup
    result_map = {r["scene_number"]: r for r in veo_results}

    with open(guide_path, "w") as f:
        f.write(f"# Assembly Guide — {concept}\n\n")
        f.write(f"**Brand:** {brand}\n")
        f.write(f"**Hero Product:** {hero}\n")
        f.write(f"**Key Mechanism:** {mechanism}\n")
        f.write(f"**Total Scenes:** {len(adapted_scenes)}\n\n")

        f.write("## Competitor Mapping\n\n")
        for orig, new in mapping.items():
            f.write(f"- {orig} → **{new}**\n")
        f.write("\n---\n\n")

        f.write("## Scene-by-Scene\n\n")
        for i, (orig, adapted) in enumerate(zip(original_scenes, adapted_scenes)):
            scene_num = orig.get("scene_number", i + 1)
            result = result_map.get(scene_num, {})

            f.write(f"### Scene {scene_num} ({orig.get('start_time', 0):.1f}s - {orig.get('end_time', 0):.1f}s)\n\n")
            f.write(f"**Role:** {adapted.get('scene_role', '')}\n")
            f.write(f"**Character:** {adapted.get('character_name', '')}\n\n")
            f.write(f"**Original Narration:** {adapted.get('original_narration', '')}\n\n")
            f.write(f"**Adapted Narration:** {adapted.get('adapted_narration', '')}\n\n")
            f.write(f"**Text Overlays:** {', '.join(adapted.get('text_overlays', []))}\n\n")

            status = result.get("status", "unknown")
            clip_path = result.get("path", "N/A")
            if status == "success" or status == "cached":
                f.write(f"**Clip:** `{os.path.basename(clip_path)}`\n\n")
            else:
                f.write(f"**Clip:** FAILED — needs manual generation\n\n")

            f.write("---\n\n")

        f.write("## Full Adapted Script\n\n")
        f.write(adapted_script.get("full_adapted_script", "(not available)"))
        f.write("\n")

    log("Guide", f"Assembly guide saved: {guide_path}")
    return guide_path


# ---------------------------------------------------------------------------
# Stage 6: Google Drive Upload
# ---------------------------------------------------------------------------

def upload_to_drive(output_dir, drive_folder_id, concept_code):
    """Upload generated clips + assembly guide to Google Drive."""
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from google.auth.transport.requests import Request

    TOKEN_PATH = os.path.expanduser("~/.claude/skills/video-scene-replicator/gdrive_token.json")
    SCOPES = ["https://www.googleapis.com/auth/drive.file"]

    # Embedded client config (same as video-scene-replicator)
    CLIENT_CONFIG = {
        "installed": {
            "client_id": "463624262612-j2d9015gf72nmnjn65m2ggfq35qavpc0.apps.googleusercontent.com",
            "client_secret": "[REDACTED_SECRET]",
            "redirect_uris": ["http://localhost"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }

    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(CLIENT_CONFIG, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, "w") as tok:
            tok.write(creds.to_json())

    service = build("drive", "v3", credentials=creds)

    # Create subfolder named with concept code
    folder_meta = {
        "name": concept_code,
        "mimeType": "application/vnd.google-apps.folder",
    }
    if drive_folder_id:
        folder_meta["parents"] = [drive_folder_id]

    folder = service.files().create(body=folder_meta, fields="id").execute()
    folder_id = folder["id"]
    log("Upload", f"Created Drive folder: {concept_code} ({folder_id})")

    # Upload generated clips
    gen_dir = os.path.join(output_dir, "generated")
    uploaded = 0
    if os.path.exists(gen_dir):
        for fname in sorted(os.listdir(gen_dir)):
            if fname.endswith(".mp4"):
                fpath = os.path.join(gen_dir, fname)
                media = MediaFileUpload(fpath, mimetype="video/mp4")
                service.files().create(
                    body={"name": fname, "parents": [folder_id]},
                    media_body=media,
                ).execute()
                uploaded += 1
                log("Upload", f"  Uploaded: {fname}")

    # Upload assembly guide
    guide_path = os.path.join(output_dir, "assembly_guide.md")
    if os.path.exists(guide_path):
        media = MediaFileUpload(guide_path, mimetype="text/markdown")
        service.files().create(
            body={"name": "assembly_guide.md", "parents": [folder_id]},
            media_body=media,
        ).execute()
        log("Upload", "  Uploaded: assembly_guide.md")

    # Upload adapted script
    script_path = os.path.join(output_dir, "scripts", "adapted_script.md")
    if os.path.exists(script_path):
        media = MediaFileUpload(script_path, mimetype="text/markdown")
        service.files().create(
            body={"name": "adapted_script.md", "parents": [folder_id]},
            media_body=media,
        ).execute()
        log("Upload", "  Uploaded: adapted_script.md")

    log("Upload", f"Upload complete: {uploaded} clips + guide + script")
    return folder_id


# ---------------------------------------------------------------------------
# Brand Knowledge Loading
# ---------------------------------------------------------------------------

def load_brand_knowledge(brand_name):
    """Load research docs from the vault for the specified brand."""
    key = brand_name.lower().strip()

    # Check for hyphenated variants
    registry = BRAND_REGISTRY.get(key)
    if not registry:
        # Try without hyphens
        for k, v in BRAND_REGISTRY.items():
            if k.replace("-", "") == key.replace("-", ""):
                registry = v
                break

    if not registry:
        log("Brand", f"WARNING: Brand '{brand_name}' not in registry. Using empty context.")
        return {"context_text": "", "product_images": [], "default_product_context": ""}

    context_parts = []
    for doc_path in registry.get("research_docs", []):
        if not os.path.exists(doc_path):
            log("Brand", f"  Doc not found: {doc_path}")
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
                from pdfminer.high_level import extract_text
                text = extract_text(doc_path)
                context_parts.append(f"--- {os.path.basename(doc_path)} ---\n{text}")

        except Exception as e:
            log("Brand", f"  Error reading {doc_path}: {e}")

    full_context = "\n\n".join(context_parts)
    if len(full_context) > MAX_BRAND_CONTEXT_CHARS:
        full_context = full_context[:MAX_BRAND_CONTEXT_CHARS]

    log("Brand", f"Loaded {len(context_parts)} docs ({len(full_context)} chars) for {brand_name}")
    return {
        "context_text": full_context,
        "product_images": registry.get("product_images", []),
        "default_product_context": registry.get("default_product_context", ""),
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Animated Video Replicator Pipeline")
    parser.add_argument("--video", required=True, help="Path to reference video OR GetHookd URL/ad ID")
    parser.add_argument("--brand", required=True, help="Target brand name")
    parser.add_argument("--concept", required=True, help="Concept code (e.g., GG-ANI-01)")
    parser.add_argument("--product-context", help="Override product context")
    parser.add_argument("--style", help="Extra style notes")
    parser.add_argument("--script-direction", help="Notes for copywriting agent")
    parser.add_argument("--drive-folder", help="Google Drive folder ID for upload")
    parser.add_argument("--skip-upload", action="store_true", help="Skip Drive upload")
    parser.add_argument("--output-dir", help="Override output directory")
    args = parser.parse_args()

    # --- Resolve video input (local path or GetHookd URL) ---
    try:
        video_path, gethookd_meta = resolve_video_input(args.video)
        args.video = video_path  # Replace with local path
        if gethookd_meta:
            log("Main", f"GetHookd ad resolved: {gethookd_meta.get('brand')} — \"{gethookd_meta.get('title', '')[:60]}\"")
            log("Main", f"  Score: {gethookd_meta.get('score')} ({gethookd_meta.get('score_title')}) | {gethookd_meta.get('days_active')} days active")
    except (ValueError, FileNotFoundError) as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    # Resolve output dir
    if args.output_dir:
        output_dir = os.path.expanduser(args.output_dir)
    else:
        output_dir = os.path.join(
            VAULT_ROOT, "b-roll", args.brand.lower(), args.concept
        )
    os.makedirs(output_dir, exist_ok=True)

    # Save GetHookd metadata alongside output for Gemini context
    if gethookd_meta:
        meta_path = os.path.join(output_dir, "gethookd_source.json")
        with open(meta_path, "w") as f:
            json.dump(gethookd_meta, f, indent=2)

    log("Main", f"Animated Video Replicator — {args.brand} / {args.concept}")
    log("Main", f"Output: {output_dir}")

    progress = Progress(output_dir)

    # Load brand knowledge
    brand_knowledge = load_brand_knowledge(args.brand)
    if args.product_context:
        brand_knowledge["default_product_context"] = args.product_context

    # --- Stage 1: Scene Detection ---
    if not progress.is_done("stage1"):
        log("Main", "=== Stage 1: Scene Detection & Frame Extraction ===")
        scene_data = extract_scenes(args.video, output_dir)
        progress.mark_done("stage1", {"keyframe_count": len(scene_data["keyframes"])})
    else:
        log("Main", "Stage 1: cached, skipping")
        scene_data = None  # Will reload from files if needed

    # --- Stage 2: Video Analysis ---
    analysis_path = os.path.join(output_dir, "analysis", "full_video_analysis.json")
    if not progress.is_done("stage2"):
        log("Main", "=== Stage 2: Full Video Analysis via Gemini ===")
        analysis = analyze_video(args.video, brand_knowledge, output_dir)
        progress.mark_done("stage2", {"scene_count": len(analysis.get("scenes", []))})
    else:
        log("Main", "Stage 2: cached, loading from file")
        with open(analysis_path, "r") as f:
            analysis = json.load(f)

    # --- Stage 3: Script Adaptation ---
    adapted_path = os.path.join(output_dir, "scripts", "adapted_script.json")
    if not progress.is_done("stage3"):
        log("Main", "=== Stage 3: Script Adaptation (Copywriting Agent) ===")
        adapted_script = adapt_script(
            analysis, brand_knowledge, args.brand, output_dir, args.script_direction
        )
        progress.mark_done("stage3", {"scene_count": len(adapted_script.get("adapted_scenes", []))})
    else:
        log("Main", "Stage 3: cached, loading from file")
        with open(adapted_path, "r") as f:
            adapted_script = json.load(f)

    # --- Stage 4: Veo Prompt Generation ---
    prompts_path = os.path.join(output_dir, "prompts", "veo_scene_prompts.json")
    if not progress.is_done("stage4"):
        log("Main", "=== Stage 4: Brand-Adapted Veo Prompts ===")
        veo_prompts = generate_veo_prompts(
            analysis, adapted_script, brand_knowledge, args.brand, output_dir
        )
        progress.mark_done("stage4", {"prompt_count": len(veo_prompts)})
    else:
        log("Main", "Stage 4: cached, loading from file")
        with open(prompts_path, "r") as f:
            veo_prompts = json.load(f)

    # --- Stage 4b: Nano Banana 2 Image-to-Image ---
    i2i_dir = os.path.join(output_dir, "i2i_frames")
    if not progress.is_done("stage4b"):
        log("Main", "=== Stage 4b: Nano Banana 2 Image-to-Image (reference → brand) ===")
        i2i_frames = generate_reference_frames(
            analysis, adapted_script, brand_knowledge, output_dir
        )
        succeeded = sum(1 for r in i2i_frames if r.get("path"))
        progress.mark_done("stage4b", {"succeeded": succeeded, "total": len(i2i_frames)})
    else:
        log("Main", "Stage 4b: cached, loading from files")
        i2i_frames = []
        for p in veo_prompts:
            sn = p["scene_number"]
            path = os.path.join(i2i_dir, f"scene_{sn:03d}_i2i.png")
            if os.path.exists(path):
                i2i_frames.append({"scene_number": sn, "path": path})
            else:
                i2i_frames.append({"scene_number": sn, "path": None})

    # --- Stage 4c: Audit i2i frames ---
    hero_template_path = os.path.join(i2i_dir, "hero_character_template.png")
    if not progress.is_done("stage4c"):
        log("Main", "=== Stage 4c: Audit i2i Frames ===")
        i2i_frames = audit_i2i_frames(
            i2i_frames, brand_knowledge, hero_template_path,
            adapted_script, analysis, output_dir
        )
        progress.mark_done("stage4c", {"audited": len(i2i_frames)})
    else:
        log("Main", "Stage 4c: cached, skipping")

    # --- Stage 5: Animate with Veo 3.1 (image-to-video, start frame) ---
    if not progress.is_done("stage5"):
        log("Main", "=== Stage 5: Animate with Veo 3.1 (image-to-video, start frame) ===")
        veo_results = generate_scenes(veo_prompts, i2i_frames, brand_knowledge, output_dir)
        succeeded = sum(1 for r in veo_results if r["status"] in ("success", "cached"))
        progress.mark_done("stage5", {"succeeded": succeeded, "total": len(veo_results)})
    else:
        log("Main", "Stage 5: cached, skipping")
        # Rebuild results from files
        gen_dir = os.path.join(output_dir, "generated")
        veo_results = []
        for p in veo_prompts:
            sn = p["scene_number"]
            path = os.path.join(gen_dir, f"scene_{sn:03d}_animated.mp4")
            if os.path.exists(path):
                veo_results.append({"scene_number": sn, "path": path, "status": "cached"})
            else:
                veo_results.append({"scene_number": sn, "path": None, "status": "failed"})

    # --- Assembly Guide ---
    log("Main", "Generating assembly guide...")
    generate_assembly_guide(
        analysis, adapted_script, veo_results, args.brand, args.concept, output_dir
    )

    # --- Stage 6: Upload ---
    if not args.skip_upload and args.drive_folder:
        if not progress.is_done("stage6"):
            log("Main", "=== Stage 6: Upload to Google Drive ===")
            folder_id = upload_to_drive(output_dir, args.drive_folder, args.concept)
            progress.mark_done("stage6", {"drive_folder_id": folder_id})
        else:
            log("Main", "Stage 6: cached, skipping")
    elif args.skip_upload:
        log("Main", "Upload skipped (--skip-upload)")
    else:
        log("Main", "No --drive-folder specified, skipping upload")

    # --- Summary ---
    succeeded = sum(1 for r in veo_results if r["status"] in ("success", "cached"))
    failed = sum(1 for r in veo_results if r["status"] == "failed")
    log("Main", "=" * 60)
    log("Main", f"PIPELINE COMPLETE — {args.brand} / {args.concept}")
    log("Main", f"  Scenes generated: {succeeded}/{len(veo_results)}")
    if failed > 0:
        log("Main", f"  Failed scenes: {failed}")
    log("Main", f"  Output: {output_dir}")
    log("Main", "=" * 60)


if __name__ == "__main__":
    main()
