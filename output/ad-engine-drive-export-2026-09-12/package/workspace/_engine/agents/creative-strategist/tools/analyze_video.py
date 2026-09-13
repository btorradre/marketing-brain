#!/usr/bin/env python3
"""
Gemini Video Analyzer — Creative Strategist Tool
==================================================
Uploads a video to Gemini and returns a structured creative breakdown
for competitive analysis, adaptation planning, and creative brief generation.

Usage:
    python3 analyze_video.py --video "/path/to/video.mp4"
    python3 analyze_video.py --video "/path/to/video.mp4" --brand "Motilli"
    python3 analyze_video.py --video "/path/to/video.mp4" --mode quick
    python3 analyze_video.py --video "/path/to/video.mp4" --mode adaptation --brand "Motilli"

Modes:
    full        — Complete scene-by-scene breakdown (default)
    quick       — High-level concept + mechanics summary
    adaptation  — Full breakdown + brand-specific adaptation notes (requires --brand)
    hooks       — Extract and analyze hook technique only (first 5 seconds)
    ingredients — Focus on how ingredients/features are highlighted
"""

import argparse
import json
import os
import sys
import time
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

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
VAULT_ROOT = os.path.expanduser("~/Documents/marketing brain")
ENV_PATH = os.path.join(VAULT_ROOT, ".env")

def load_api_key():
    """Load GEMINI_API_KEY from environment or .env file."""
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH) as f:
            for line in f:
                line = line.strip()
                if line.startswith("GEMINI_API_KEY="):
                    return line.split("=", 1)[1].strip('"').strip("'")
    print("[!] No GEMINI_API_KEY found in environment or .env")
    sys.exit(1)

GEMINI_MODEL = "gemini-2.5-flash"

# ---------------------------------------------------------------------------
# Brand context loader
# ---------------------------------------------------------------------------
BRAND_REGISTRY = {
    "motilli": {
        "product": "Celery Juice Fiber Gummies for GLP-1 users",
        "mechanism": "Natural prokinetic (apigenin) stimulates stomach motility — upstream fix vs downstream laxatives",
        "key_ingredients": [
            "Celery Juice Extract (apigenin) — natural prokinetic, stimulates stomach muscles",
            "Chlorophyll — neutralizes hydrogen sulfide gas (sulfur burps)",
            "Prebiotic Fiber — gentle micro-dose feeds good bacteria",
            "Vitamins A, C, K, B6, Folate — replaces nutrients lost from restricted eating",
        ],
        "avatar": "Women 45-65 on GLP-1 medications (Ozempic, Wegovy, Mounjaro) suffering digestive side effects",
        "positioning": "The GLP-1 Companion — purpose-built for her specific lifestyle",
        "core_promise": "Keep the weight loss. Ditch the digestive nightmare.",
        "research_docs": [
            os.path.join(VAULT_ROOT, "motilli/Motilli_Master_Copywriting_Brief.md"),
            os.path.join(VAULT_ROOT, "motilli/Motilli_Product_Context.md"),
        ],
    },
    "lunessa": {
        "product": "Feminine health supplement",
        "mechanism": "Hormonal balance support",
        "key_ingredients": [],
        "avatar": "Women experiencing hormonal health challenges",
        "positioning": "Natural hormonal support",
        "core_promise": "",
        "research_docs": [],
    },
    "velantra": {
        "product": "Beauty/wellness supplement",
        "mechanism": "",
        "key_ingredients": [],
        "avatar": "",
        "positioning": "",
        "core_promise": "",
        "research_docs": [],
    },
}

# ---------------------------------------------------------------------------
# Prompt templates
# ---------------------------------------------------------------------------
PROMPTS = {
    "full": """You are a direct response creative strategist analyzing a competitor video ad. Watch this video carefully and provide a COMPREHENSIVE breakdown:

## 1. OVERALL CONCEPT
- Brand/product
- Core creative concept
- Format (animated, UGC, talking head, product demo, etc.)
- Estimated duration
- Overall visual style and tone

## 2. SCENE-BY-SCENE BREAKDOWN
For EACH distinct scene/segment:
- Timestamp range (approximate)
- Visual description (animation, text, imagery, transitions)
- Exact text overlays (if readable)
- Color palette and visual treatment
- Motion/animation style

## 3. INGREDIENT/PRODUCT HIGHLIGHTING
- How are ingredients or product features introduced?
- What visual techniques showcase them?
- How does each ingredient get its "moment"?
- What claims accompany each ingredient?

## 4. CREATIVE MECHANICS
- Hook technique (first 3 seconds)
- Pacing and rhythm
- Transition styles
- Text animation style
- Call-to-action approach
- Unique creative devices (personification, internal journey, humor, etc.)

## 5. PERSUASION ARCHITECTURE
- What beliefs does this ad try to shift?
- What villain is established (external, internal, philosophical)?
- How is the mechanism educated?
- Where does product integration sit (invisible, peripheral, supporting, central)?
- What awareness level is this targeting?

## 6. PRODUCTION NOTES
- Tools/software needed to recreate
- Key design elements
- Font styles, color scheme
- Aspect ratio

Be extremely detailed. This analysis will be used to create an adaptation for a different brand.""",

    "quick": """You are a creative strategist doing a rapid analysis of a video ad. Watch and provide:

## CONCEPT SUMMARY (2-3 sentences)
What is this ad doing and why does it work?

## FORMAT & STYLE
Type, duration, aspect ratio, animation style

## HOOK TECHNIQUE
What happens in the first 3 seconds and why it stops the scroll

## CORE MECHANIC
The primary creative device that makes this ad work (personification, story, demonstration, etc.)

## PERSUASION STRUCTURE
Villain → Mechanism → Solution → CTA (one line each)

## STEAL-WORTHY ELEMENTS
3-5 specific techniques worth adapting for other brands""",

    "hooks": """You are a hook specialist analyzing the opening of a video ad. Focus ONLY on the first 5 seconds:

## HOOK BREAKDOWN
- Exact opening visual (frame by frame for first 3 seconds)
- Opening text overlay (exact wording)
- Opening audio/voice (exact words)
- Hook category (curiosity, disbelief, specificity, counterintuitive, pattern interrupt, etc.)

## WHY IT WORKS
- What emotion does it trigger?
- What loop does it open?
- What makes the viewer NOT scroll?

## HOOK FORMULA
Extract the underlying formula that could be templated for other products.
Example: "[Personified Problem] + [Direct Address] + [Smug Attitude]"

## 5 ADAPTATION EXAMPLES
Write 5 hook variations using this same formula for different product categories.""",

    "ingredients": """You are analyzing how a video ad highlights its ingredients/product features. Watch carefully and document:

## INGREDIENT INTRODUCTION SEQUENCE
For each ingredient or feature shown:
- Timestamp when introduced
- Visual treatment (personification, text overlay, animation, close-up, etc.)
- Exact claims made
- Duration of screen time
- How it connects to the previous/next ingredient

## VISUAL HIERARCHY
- Which ingredient gets the most screen time?
- Which gets the most dramatic visual treatment?
- How is the "hero ingredient" differentiated?

## MECHANISM EDUCATION TECHNIQUE
- How does the ad teach WHY these ingredients work?
- Is it lecture-style, story-style, character-style, or demonstration-style?
- How technical does it get?

## ADAPTATION TEMPLATE
Provide a template for introducing 3-4 ingredients using this same visual/narrative approach.""",
}

ADAPTATION_SUFFIX = """

## 7. BRAND ADAPTATION ANALYSIS

Now analyze how this creative concept could be adapted for the following brand:

**Product:** {product}
**Mechanism:** {mechanism}
**Key Ingredients:** {ingredients}
**Target Avatar:** {avatar}
**Positioning:** {positioning}
**Core Promise:** {core_promise}

Provide:
### VILLAIN MAPPING
Map the original ad's villain to this brand's equivalent. What character/entity represents the problem?

### INGREDIENT HERO MAPPING
Map each original ingredient character to this brand's ingredients. Define each hero's:
- Visual appearance
- Personality
- Action in the body
- Key line of dialogue

### NARRATIVE ARC ADAPTATION
Rewrite the scene-by-scene breakdown adapted for this brand. Include:
- Approximate timestamps
- Visual descriptions
- Text overlays
- Character dialogue

### HOOK ADAPTATION
Write 3 opening hook variations using the original's technique but for this brand.

### PRODUCTION RECOMMENDATIONS
Specific tools, timeline, and budget estimate for producing this adaptation."""

# ---------------------------------------------------------------------------
# Core analyzer
# ---------------------------------------------------------------------------
def analyze_video(video_path: str, mode: str = "full", brand: str | None = None) -> str:
    """Upload video to Gemini and return structured creative analysis."""
    api_key = load_api_key()
    client = genai.Client(api_key=api_key)

    # Upload video
    print(f"[1/3] Uploading video to Gemini...")
    video_file = client.files.upload(file=video_path)
    print(f"  Uploaded: {video_file.name} (state: {video_file.state})")

    # Wait for processing
    print(f"[2/3] Processing video...")
    while video_file.state.name == "PROCESSING":
        time.sleep(3)
        video_file = client.files.get(name=video_file.name)

    if video_file.state.name == "FAILED":
        print("[!] Video processing failed")
        client.files.delete(name=video_file.name)
        sys.exit(1)

    # Build prompt
    prompt = PROMPTS.get(mode, PROMPTS["full"])

    if brand and mode == "adaptation":
        brand_key = brand.lower()
        if brand_key in BRAND_REGISTRY:
            b = BRAND_REGISTRY[brand_key]
            prompt = PROMPTS["full"] + ADAPTATION_SUFFIX.format(
                product=b["product"],
                mechanism=b["mechanism"],
                ingredients="\n".join(f"- {i}" for i in b["key_ingredients"]),
                avatar=b["avatar"],
                positioning=b["positioning"],
                core_promise=b["core_promise"],
            )
        else:
            print(f"[!] Brand '{brand}' not in registry. Using full mode without adaptation.")

    # Generate analysis
    print(f"[3/3] Analyzing with Gemini ({GEMINI_MODEL})...")
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=[
            types.Content(
                role="user",
                parts=[
                    types.Part.from_uri(
                        file_uri=video_file.uri,
                        mime_type="video/mp4",
                    ),
                    types.Part.from_text(text=prompt),
                ],
            )
        ],
    )

    # Cleanup uploaded file
    client.files.delete(name=video_file.name)
    print("[Done] Analysis complete. Uploaded file cleaned up.\n")

    return response.text


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Analyze a video ad creative using Gemini",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--video", required=True, help="Path to video file")
    parser.add_argument(
        "--mode",
        choices=["full", "quick", "adaptation", "hooks", "ingredients"],
        default="full",
        help="Analysis mode (default: full)",
    )
    parser.add_argument("--brand", help="Brand name for adaptation mode (e.g., Motilli, Lunessa)")
    parser.add_argument("--output", help="Save analysis to file (default: print to stdout)")

    args = parser.parse_args()

    if not os.path.exists(args.video):
        print(f"[!] Video not found: {args.video}")
        sys.exit(1)

    if args.mode == "adaptation" and not args.brand:
        print("[!] --brand is required for adaptation mode")
        sys.exit(1)

    result = analyze_video(args.video, args.mode, args.brand)

    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w") as f:
            f.write(result)
        print(f"Analysis saved to: {args.output}")
    else:
        print(result)


if __name__ == "__main__":
    main()
