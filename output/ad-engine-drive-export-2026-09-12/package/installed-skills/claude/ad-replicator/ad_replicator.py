#!/usr/bin/env python3
"""
Ad Replicator Pipeline
=======================
Takes a reference ad image, analyzes why it works via Claude Opus 4.6,
adapts it for a target brand using vault research docs, and generates
the adapted image via Nano Banana 2 (image-to-image).

Usage:
    python3 ad_replicator.py \
        --reference "/path/to/reference-ad.png" \
        --brand "Motilli" \
        --output-dir "./ad-replicator-output"
"""

import argparse
import base64
import json
import os
import re
import sys
import time
from pathlib import Path
from datetime import datetime

# ---------------------------------------------------------------------------
# Dependency check
# ---------------------------------------------------------------------------
REQUIRED_PACKAGES = ["anthropic", "google.genai", "PIL", "dotenv"]


def check_deps():
    missing = []
    for pkg in REQUIRED_PACKAGES:
        top = pkg.split(".")[0]
        try:
            __import__(top)
        except ImportError:
            missing.append(pkg)
    # More precise check for google.genai
    try:
        from google import genai  # noqa: F401
    except ImportError:
        if "google.genai" not in missing:
            missing.append("google-genai")
    if missing:
        print(f"[!] Missing packages: {missing}")
        print("    pip install anthropic google-genai Pillow python-dotenv")
        sys.exit(1)


check_deps()

import anthropic
from google import genai
from google.genai import types
from PIL import Image
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
ENV_PATH = os.path.expanduser("~/Documents/marketing brain/.env")
load_dotenv(ENV_PATH, override=True)

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

if not ANTHROPIC_API_KEY:
    print("[!] ANTHROPIC_API_KEY not found in .env or environment")
    sys.exit(1)
if not GEMINI_API_KEY:
    print("[!] GEMINI_API_KEY not found in .env or environment")
    sys.exit(1)

CLAUDE_MODEL = "claude-opus-4-20250514"
GEMINI_IMAGE_MODEL = "gemini-3.1-flash-image-preview"  # Nano Banana 2

VAULT_ROOT = os.path.expanduser("~/Documents/marketing brain")

# Brand knowledge registry
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
    "velantra-straw-tote": {
        "research_docs": [
            "/Users/brooksorradre2/Documents/marketing brain/brands/velantra/research/icp-branding/Velantra_ Comprehensive Branding Kit.md",
            "/Users/brooksorradre2/Documents/marketing brain/brands/velantra/research/icp-branding/Ideal_Customer_Profile.md",
        ],
        "product_images": [
            "/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/straw-birkin/product-images/straw birkin/caramel 1.png",
            "/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/straw-birkin/product-images/straw birkin/caramel 2.png",
            "/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/straw-birkin/product-images/straw birkin/straw tote 1.webp",
            "/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/straw-birkin/product-images/straw birkin/black-colorway/black-tote-1.jpeg",
        ],
        "default_product_context": "Velantra Straw Tote ($119.99) - structured Birkin-style tote, hand-woven natural seagrass body with whipstitch cross-lacing, smooth taupe leather top flap with white contrast stitching, rolled leather handles, crossed leather belt straps, NO metal hardware, no visible logo. Hero colorway: caramel/natural. Quiet-luxury coastal brand, velantrafashion.com.",
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

MAX_BRAND_CONTEXT_CHARS = 30000
MAX_RETRIES = 3
NANO_BANANA_RATE_LIMIT_SLEEP = 2


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------
def log(stage, msg):
    prefix = f"[Stage {stage}]" if isinstance(stage, int) else f"[{stage}]"
    print(f"{prefix} {msg}")


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)
    return path


def _detect_mime(data, ext):
    """Detect actual MIME type from file magic bytes, falling back to extension."""
    if data[:8] == b'\x89PNG\r\n\x1a\n':
        return "image/png"
    if data[:2] == b'\xff\xd8':
        return "image/jpeg"
    if data[:4] == b'RIFF' and data[8:12] == b'WEBP':
        return "image/webp"
    mime_map = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}
    return mime_map.get(ext, f"image/{ext.lstrip('.')}")


def image_to_base64(path):
    """Read an image file and return base64-encoded string + mime type."""
    ext = Path(path).suffix.lower()
    with open(path, "rb") as f:
        data = f.read()
    mime = _detect_mime(data, ext)
    return base64.standard_b64encode(data).decode("utf-8"), mime


def image_to_bytes(path):
    """Read an image file and return raw bytes + mime type."""
    ext = Path(path).suffix.lower()
    with open(path, "rb") as f:
        data = f.read()
    mime = _detect_mime(data, ext)
    return data, mime


# ---------------------------------------------------------------------------
# Brand Knowledge Loading
# ---------------------------------------------------------------------------
def load_brand_knowledge(brand_name):
    """Load research docs from the vault for the specified brand."""
    key = brand_name.lower().strip()
    if key not in BRAND_REGISTRY:
        log("BRAND", f"Brand '{brand_name}' not in registry — using empty context")
        return {"context_text": "", "product_images": [], "default_product_context": ""}

    brand = BRAND_REGISTRY[key]
    context_parts = []

    for doc_path in brand.get("research_docs", []):
        if not os.path.exists(doc_path):
            log("BRAND", f"SKIP (not found): {os.path.basename(doc_path)}")
            continue

        ext = Path(doc_path).suffix.lower()
        try:
            if ext == ".md":
                with open(doc_path, "r", encoding="utf-8") as f:
                    content = f.read()
                context_parts.append(f"--- {os.path.basename(doc_path)} ---\n{content}")
                log("BRAND", f"Loaded: {os.path.basename(doc_path)} ({len(content)} chars)")

            elif ext == ".docx":
                import zipfile
                import xml.etree.ElementTree as ET
                with zipfile.ZipFile(doc_path, "r") as z:
                    xml_content = z.read("word/document.xml")
                tree = ET.fromstring(xml_content)
                ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
                paragraphs = []
                for p in tree.iter(f"{{{ns['w']}}}p"):
                    texts = [t.text for t in p.iter(f"{{{ns['w']}}}t") if t.text]
                    if texts:
                        paragraphs.append("".join(texts))
                content = "\n\n".join(paragraphs)
                context_parts.append(f"--- {os.path.basename(doc_path)} ---\n{content}")
                log("BRAND", f"Loaded: {os.path.basename(doc_path)} ({len(content)} chars)")

            elif ext == ".pdf":
                try:
                    from pdfminer.high_level import extract_text
                    content = extract_text(doc_path)
                    context_parts.append(f"--- {os.path.basename(doc_path)} ---\n{content}")
                    log("BRAND", f"Loaded: {os.path.basename(doc_path)} ({len(content)} chars)")
                except ImportError:
                    log("BRAND", f"SKIP (pdfminer not installed): {os.path.basename(doc_path)}")

        except Exception as e:
            log("BRAND", f"ERROR loading {os.path.basename(doc_path)}: {e}")

    full_context = "\n\n".join(context_parts)
    if len(full_context) > MAX_BRAND_CONTEXT_CHARS:
        log("BRAND", f"Context truncated from {len(full_context)} to {MAX_BRAND_CONTEXT_CHARS} chars")
        full_context = full_context[:MAX_BRAND_CONTEXT_CHARS]

    # Resolve product images
    product_imgs = []
    for pimg in brand.get("product_images", []):
        if os.path.exists(pimg):
            product_imgs.append(pimg)
    if not product_imgs:
        for pimg in brand.get("product_images_fallback", []):
            if os.path.exists(pimg):
                product_imgs.append(pimg)

    for pimg in product_imgs:
        log("BRAND", f"Product image: {os.path.basename(pimg)}")

    return {
        "context_text": full_context,
        "product_images": product_imgs,
        "default_product_context": brand.get("default_product_context", ""),
    }


# ---------------------------------------------------------------------------
# Stage 1: Ad Analysis via Claude Opus 4.6
# ---------------------------------------------------------------------------
def analyze_reference(ref_path, user_analysis=None):
    """Analyze a reference ad image using Claude Opus 4.6.
    Returns structured analysis of why it works, elements, composition, etc."""

    log(1, f"Analyzing reference: {os.path.basename(ref_path)}")

    if user_analysis:
        log(1, "Using user-provided analysis (skipping Claude)")
        return {
            "why_it_works": user_analysis,
            "visual_elements": "User-provided — see why_it_works",
            "composition": "User-provided — see why_it_works",
            "angle": "User-provided — see why_it_works",
            "audience": "User-provided — see why_it_works",
            "product_presence": {"has_product": True, "type": "unknown", "sentiment": "positive"},
            "text_content": "",
            "style": "unknown",
            "color_palette": [],
            "mood": "unknown",
            "user_provided": True,
        }

    img_b64, mime = image_to_base64(ref_path)

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    analysis_prompt = """Analyze this ad image in detail. Return a JSON object with these exact keys:

{
  "why_it_works": "A detailed explanation of WHY this ad is effective. What persuasion mechanics are at play? What psychological triggers does it use? What makes someone stop scrolling? What belief does it shift?",

  "visual_elements": "Every visual element catalogued: layout structure, colors, typography (fonts, sizes, weights), imagery type (photo, illustration, graphic), props visible, backgrounds, borders, badges, icons, buttons, overlays.",

  "composition": "How the image is structured. Examples: 'split layout 60/40 with text left, product right', 'centered hero image with text overlay', '3-column comparison grid', 'full-bleed lifestyle photo with bottom text bar'. Include aspect ratio if detectable.",

  "angle": "The persuasion angle. Examples: 'authority (doctor/clinical)', 'social proof (testimonial)', 'curiosity gap', 'fear of consequence', 'comparison/anchoring', 'urgency/scarcity', 'mechanism education', 'identity/tribe'.",

  "audience": "Who this targets. Demographics (age, gender), psychographics (what they care about, what they fear), and awareness level (problem-aware, solution-aware, product-aware).",

  "product_presence": {
    "has_product": true/false,
    "type": "bottle/gummy/pill/device/bag/handbag/tote/clothing/accessory/none/other",
    "sentiment": "positive (hero product) / negative (villain/competitor) / neutral / none",
    "description": "What the product looks like if present"
  },

  "text_content": "All text visible in the image, transcribed exactly. Include headlines, subheadlines, body copy, CTAs, badges, price tags, disclaimers.",

  "style": "The visual style category. Options: 'native/UGC' (looks like a real person's photo), 'branded/polished' (professional design with brand elements), 'editorial' (news/magazine style), 'clinical' (medical/scientific look), 'lifestyle' (aspirational photography), 'comparison' (side-by-side or chart), 'testimonial card' (review/quote format).",

  "color_palette": ["List of dominant colors as hex codes or descriptive names, with their psychological function in the ad"],

  "mood": "The emotional tone. Examples: 'urgent/alarming', 'clinical/authoritative', 'warm/hopeful', 'frustrated/defeated', 'curious/intriguing', 'aspirational/empowering'."
}

Return ONLY the JSON object. No markdown formatting, no code fences, no explanation outside the JSON."""

    for attempt in range(MAX_RETRIES):
        try:
            response = client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=4096,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": mime,
                                    "data": img_b64,
                                },
                            },
                            {
                                "type": "text",
                                "text": analysis_prompt,
                            },
                        ],
                    }
                ],
            )

            raw = response.content[0].text.strip()
            # Try to parse JSON (strip markdown fences if present)
            if raw.startswith("```"):
                raw = re.sub(r"^```(?:json)?\s*\n?", "", raw)
                raw = re.sub(r"\n?```\s*$", "", raw)

            analysis = json.loads(raw)
            log(1, f"Analysis complete — style: {analysis.get('style', 'unknown')}, "
                f"product: {analysis.get('product_presence', {}).get('has_product', 'unknown')}")
            return analysis

        except json.JSONDecodeError as e:
            log(1, f"JSON parse error (attempt {attempt + 1}): {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(2)
            else:
                log(1, f"Returning raw text as why_it_works fallback")
                return {
                    "why_it_works": raw,
                    "visual_elements": "Parse failed",
                    "composition": "Parse failed",
                    "angle": "Parse failed",
                    "audience": "Parse failed",
                    "product_presence": {"has_product": True, "type": "unknown", "sentiment": "positive"},
                    "text_content": "",
                    "style": "unknown",
                    "color_palette": [],
                    "mood": "unknown",
                }
        except Exception as e:
            log(1, f"ERROR (attempt {attempt + 1}): {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(5 * (attempt + 1))
            else:
                raise


# ---------------------------------------------------------------------------
# Stage 2: Brand Adaptation Strategy (Claude Opus 4.6 + Brand Knowledge)
# ---------------------------------------------------------------------------
def generate_adaptation(analysis, ref_path, brand_knowledge, brand_name,
                        product_context=None, adaptation_notes=None, variation_index=0):
    """Generate a brand adaptation strategy and image-to-image prompt."""

    log(2, f"Generating adaptation strategy for {brand_name} (variation {variation_index + 1})...")

    product_ctx = product_context or brand_knowledge.get("default_product_context", "")
    brand_ctx = brand_knowledge.get("context_text", "")

    img_b64, mime = image_to_base64(ref_path)

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    adaptation_prompt = f"""You are an expert direct response creative strategist. You're looking at a reference ad image and its analysis. Your job is to create a 1:1 adaptation of this ad for {brand_name}.

## Reference Ad Analysis
{json.dumps(analysis, indent=2)}

## Target Brand: {brand_name}
Product: {product_ctx}

## Brand Knowledge (from research docs)
{brand_ctx[:20000] if brand_ctx else "No brand research docs available. Work with the product context above."}

{f"## Additional Adaptation Notes from User{chr(10)}{adaptation_notes}" if adaptation_notes else ""}

{f"## Variation {variation_index + 1}{chr(10)}This is variation {variation_index + 1}. Create a meaningfully different interpretation — vary the setting, lighting, angle, or props while preserving the core composition and persuasion mechanics." if variation_index > 0 else ""}

## Your Task

Create a detailed image-to-image editing prompt for Nano Banana 2 (Gemini image generation) that will transform the reference ad into a {brand_name} adaptation.

Return a JSON object with these keys:

{{
  "adaptation_strategy": "2-3 sentences explaining what stays the same and what changes. What elements of the original are preserved (composition, style, mood, angle) and what is adapted (product, avatar, setting, text, colors).",

  "image_prompt": "The COMPLETE image-to-image editing prompt for Nano Banana 2. This prompt will be sent alongside the reference image. It must instruct Gemini to transform the reference while preserving the exact composition, camera angle, lighting style, and visual structure. Be extremely specific about what to change and what to keep. Include specific descriptions of the target avatar (age, appearance, setting based on brand research), the product appearance if applicable, and any text that should appear.",

  "product_handling": {{
    "include_product_ref": true/false,
    "reason": "Why product reference should or shouldn't be included"
  }},

  "text_replacements": {{
    "original": "text from the reference",
    "adapted": "equivalent text for {brand_name}"
  }}
}}

IMPORTANT RULES:
- The image prompt must instruct 1:1 composition replication — same layout, same visual hierarchy, same framing
- If the reference has a product, the adaptation should feature {brand_name}'s product in the same position/prominence
- If the reference has text/copy, adapt it for {brand_name}'s messaging (mechanism, benefits, claims)
- If the reference is native/UGC style, the adaptation must remain native/UGC — do NOT make it look more polished
- If the reference is branded/polished, maintain that level of production value
- Match the avatar to {brand_name}'s target audience (from brand research docs)
- NEVER add elements that aren't in the reference
- If the reference has NO text: instruct "Do NOT add any text, captions, subtitles, watermarks, logos, or text overlays to the image"
- If the reference HAS text: you MUST instruct Nano Banana to include the adapted text in the exact same positions, sizes, and styles as the original. NEVER say "Do NOT add text" when the reference contains text. List every text replacement explicitly in the image prompt.

Return ONLY the JSON object."""

    for attempt in range(MAX_RETRIES):
        try:
            response = client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=4096,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": mime,
                                    "data": img_b64,
                                },
                            },
                            {
                                "type": "text",
                                "text": adaptation_prompt,
                            },
                        ],
                    }
                ],
            )

            raw = response.content[0].text.strip()
            if raw.startswith("```"):
                raw = re.sub(r"^```(?:json)?\s*\n?", "", raw)
                raw = re.sub(r"\n?```\s*$", "", raw)

            adaptation = json.loads(raw)
            log(2, f"Adaptation strategy generated — product ref: {adaptation.get('product_handling', {}).get('include_product_ref', 'unknown')}")
            return adaptation

        except json.JSONDecodeError as e:
            log(2, f"JSON parse error (attempt {attempt + 1}): {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(2)
            else:
                # Fallback: use the raw text as the image prompt
                return {
                    "adaptation_strategy": "Parse failed — using raw response as prompt",
                    "image_prompt": raw,
                    "product_handling": {"include_product_ref": True, "reason": "Fallback"},
                    "text_replacements": {},
                }
        except Exception as e:
            log(2, f"ERROR (attempt {attempt + 1}): {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(5 * (attempt + 1))
            else:
                raise


# ---------------------------------------------------------------------------
# Stage 3: Image-to-Image Generation (Nano Banana 2)
# ---------------------------------------------------------------------------
def generate_adapted_image(ref_path, adaptation, analysis, product_images,
                           output_path, variation_index=0):
    """Generate the adapted image using Nano Banana 2 image-to-image editing."""

    log(3, f"Generating adapted image (variation {variation_index + 1})...")

    client = genai.Client(api_key=GEMINI_API_KEY)

    # Build content parts
    parts = []

    # 1. Reference image
    ref_bytes, ref_mime = image_to_bytes(ref_path)
    parts.append(types.Part(inline_data=types.Blob(data=ref_bytes, mime_type=ref_mime)))

    # 2. Product reference images (if applicable)
    product_presence = analysis.get("product_presence", {})
    has_product = product_presence.get("has_product", False)
    sentiment = product_presence.get("sentiment", "positive")
    include_product = adaptation.get("product_handling", {}).get("include_product_ref", has_product)

    # Only include product ref if the reference has a product with positive sentiment
    if include_product and has_product and sentiment != "negative" and product_images:
        for pimg in product_images:
            if os.path.exists(pimg):
                p_bytes, p_mime = image_to_bytes(pimg)
                parts.append(types.Part(inline_data=types.Blob(data=p_bytes, mime_type=p_mime)))
                log(3, f"  Included product reference: {os.path.basename(pimg)}")

    # 3. Build the editing prompt
    base_prompt = adaptation.get("image_prompt", "")

    product_ref_note = ""
    no_product_guard = ""
    competitor_note = ""

    if include_product and has_product and sentiment != "negative" and product_images:
        product_ref_note = (
            "I've also included product reference image(s) showing the EXACT product to feature. "
            "You MUST replicate this product EXACTLY as shown in the product reference — same shape, "
            "same design, same colors, same branding, same materials, and same proportions. "
            "The product in the output MUST be visually identical to the product reference image. "
            "Do NOT create a generic or approximated version. Do NOT use the product shape/style from the "
            "reference AD — use the product shape/style from the product REFERENCE IMAGE. "
            "Match the product reference precisely — same silhouette, hardware, texture, and construction. "
        )
    elif has_product and sentiment == "negative":
        competitor_note = (
            "IMPORTANT: This reference shows a FAILED SOLUTION / COMPETITOR PRODUCT. "
            "Do NOT replace it with the target brand's product. Instead, make it a "
            "GENERIC product — a plain white bottle, generic pill box, or unbranded supplement. "
            "This is a problem-aware scene, not product-aware. "
        )
    elif not has_product:
        no_product_guard = (
            "IMPORTANT: The reference does NOT contain a product. "
            "Do NOT add any product, bottle, package, or branded item. "
            "Only adapt the visual elements as described in the prompt. "
        )

    # Build text instruction based on whether reference has text
    text_content = analysis.get("text_content", "")
    text_replacements = adaptation.get("text_replacements", {})
    if text_content and text_replacements:
        # Reference has text — tell Nano Banana to include adapted text
        adapted_text_lines = []
        for orig, adapted in text_replacements.items():
            adapted_text_lines.append(f'  Replace "{orig[:60]}..." with "{adapted[:60]}..."')
        text_instruction = (
            "CRITICAL: The reference image contains text/copy. You MUST include ALL adapted text "
            "in the output image, positioned EXACTLY where the original text appears. "
            "Replicate the same font sizes, weights, colors, and positions. "
            "Text replacements:\n" + "\n".join(adapted_text_lines[:8])
        )
    elif text_content:
        text_instruction = (
            "The reference has text. Replicate the text layout but adapt brand names and claims "
            "to match the target brand described in the adaptation instructions."
        )
    else:
        text_instruction = "Do NOT add any text, captions, subtitles, watermarks, logos, or text overlays."

    edit_prompt = (
        f"Edit this reference ad image to adapt it for a different brand. "
        f"Replicate the composition 1:1 — EXACT same layout, camera angle, lighting, "
        f"framing, visual hierarchy, and overall style. "
        f"Only change the specific elements described in the adaptation instructions below. "
        f"Do NOT invent or add elements that are not in the original reference. "
        f"{product_ref_note}"
        f"{no_product_guard}"
        f"{competitor_note}"
        f"\n\n{text_instruction}"
        f"\n\nADAPTATION INSTRUCTIONS:\n{base_prompt}"
    )

    parts.append(types.Part(text=edit_prompt))

    # Generate
    for attempt in range(MAX_RETRIES):
        try:
            response = client.models.generate_content(
                model=GEMINI_IMAGE_MODEL,
                contents=types.Content(parts=parts),
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE", "TEXT"],
                ),
            )

            # Extract image from response
            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    with open(output_path, "wb") as f:
                        f.write(part.inline_data.data)
                    log(3, f"  Saved: {output_path}")
                    return output_path

            log(3, f"  WARNING: No image returned (attempt {attempt + 1})")
            if attempt < MAX_RETRIES - 1:
                time.sleep(3)

        except Exception as e:
            log(3, f"  ERROR (attempt {attempt + 1}): {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(5 * (attempt + 1))

    log(3, f"  FAILED: Could not generate image after {MAX_RETRIES} attempts")
    return None


# ---------------------------------------------------------------------------
# Main Pipeline
# ---------------------------------------------------------------------------
def run_pipeline(args):
    """Run the full ad replicator pipeline."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = args.output_dir or f"./ad-replicator-output-{timestamp}"

    analysis_dir = ensure_dir(os.path.join(output_dir, "analysis"))
    gen_dir = ensure_dir(os.path.join(output_dir, "generated"))

    # Load brand knowledge
    log("INIT", f"Brand: {args.brand}")
    brand_knowledge = load_brand_knowledge(args.brand)
    product_context = args.product_context or brand_knowledge.get("default_product_context", "")

    # Resolve product images
    product_images = []
    if args.product_images:
        product_images = [p.strip() for p in args.product_images.split(",") if p.strip()]
    else:
        product_images = brand_knowledge.get("product_images", [])

    log("INIT", f"Product context: {product_context[:80]}...")
    log("INIT", f"Product images: {len(product_images)}")
    log("INIT", f"Brand knowledge: {len(brand_knowledge.get('context_text', ''))} chars")
    log("INIT", f"Variations per reference: {args.variations}")

    # Process each reference
    references = args.reference if isinstance(args.reference, list) else [args.reference]
    results = []

    for ref_idx, ref_path in enumerate(references):
        ref_num = f"{ref_idx + 1:03d}"
        log("PIPELINE", f"Processing reference {ref_idx + 1}/{len(references)}: {os.path.basename(ref_path)}")

        if not os.path.exists(ref_path):
            log("PIPELINE", f"  ERROR: File not found: {ref_path}")
            results.append({"reference": ref_path, "status": "error", "error": "File not found"})
            continue

        # Stage 1: Analyze
        analysis_path = os.path.join(analysis_dir, f"ref_{ref_num}_analysis.json")
        if os.path.exists(analysis_path):
            log(1, f"Analysis already exists — loading from cache")
            with open(analysis_path, "r") as f:
                analysis = json.load(f)
        else:
            analysis = analyze_reference(ref_path, user_analysis=args.why_it_works)
            with open(analysis_path, "w") as f:
                json.dump(analysis, f, indent=2)
            log(1, f"Saved analysis to {analysis_path}")

        # Generate variations
        for var_idx in range(args.variations):
            var_num = f"{var_idx + 1:03d}"
            out_path = os.path.join(gen_dir, f"ref_{ref_num}_adapted_v{var_num}.png")

            if os.path.exists(out_path):
                log("PIPELINE", f"  Variation {var_idx + 1} already exists — skipping")
                results.append({
                    "reference": ref_path,
                    "variation": var_idx + 1,
                    "output": out_path,
                    "status": "cached",
                })
                continue

            # Stage 2: Adaptation strategy
            adaptation_path = os.path.join(analysis_dir, f"ref_{ref_num}_adaptation_v{var_num}.json")
            if os.path.exists(adaptation_path):
                log(2, f"Adaptation already exists — loading from cache")
                with open(adaptation_path, "r") as f:
                    adaptation = json.load(f)
            else:
                adaptation = generate_adaptation(
                    analysis, ref_path, brand_knowledge, args.brand,
                    product_context=product_context,
                    adaptation_notes=args.adaptation_notes,
                    variation_index=var_idx,
                )
                # Save the full analysis + adaptation together
                combined = {"analysis": analysis, "adaptation": adaptation}
                with open(adaptation_path, "w") as f:
                    json.dump(combined, f, indent=2)
                log(2, f"Saved adaptation to {adaptation_path}")

            # Stage 3: Image generation
            result_path = generate_adapted_image(
                ref_path, adaptation, analysis, product_images,
                out_path, variation_index=var_idx,
            )

            results.append({
                "reference": ref_path,
                "variation": var_idx + 1,
                "output": result_path,
                "status": "success" if result_path else "failed",
            })

            time.sleep(NANO_BANANA_RATE_LIMIT_SLEEP)

    # Write summary
    summary_path = os.path.join(output_dir, "summary.md")
    success_count = sum(1 for r in results if r.get("status") == "success")
    cached_count = sum(1 for r in results if r.get("status") == "cached")
    failed_count = sum(1 for r in results if r.get("status") == "failed")
    error_count = sum(1 for r in results if r.get("status") == "error")

    summary_lines = [
        f"# Ad Replicator — Run Summary",
        f"",
        f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Brand:** {args.brand}",
        f"**References:** {len(references)}",
        f"**Variations per ref:** {args.variations}",
        f"**Total generated:** {success_count} new, {cached_count} cached, {failed_count} failed, {error_count} errors",
        f"",
        f"## Results",
        f"",
    ]

    for r in results:
        status_icon = {"success": "OK", "cached": "CACHED", "failed": "FAIL", "error": "ERR"}.get(r["status"], "?")
        ref_name = os.path.basename(r["reference"])
        out_name = os.path.basename(r.get("output", "")) if r.get("output") else "none"
        summary_lines.append(f"- [{status_icon}] {ref_name} v{r.get('variation', '?')} -> {out_name}")

    with open(summary_path, "w") as f:
        f.write("\n".join(summary_lines))

    log("DONE", f"Pipeline complete — {success_count} generated, {cached_count} cached, {failed_count} failed")
    log("DONE", f"Output directory: {output_dir}")

    return results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Ad Replicator — adapt reference ads for your brand via Nano Banana 2")

    parser.add_argument("--reference", nargs="+", required=True,
                        help="Path(s) to reference ad image(s)")
    parser.add_argument("--brand", required=True,
                        help="Target brand name (Motilli, Lunessa, Velantra, etc.)")
    parser.add_argument("--output-dir", default=None,
                        help="Output directory (default: auto-generated)")
    parser.add_argument("--product-context", default=None,
                        help="Override product context (auto-loaded from vault if not set)")
    parser.add_argument("--product-images", default=None,
                        help="Comma-separated paths to product reference images (auto-loaded if not set)")
    parser.add_argument("--why-it-works", default=None,
                        help="User-provided analysis of why the reference works (skips Stage 1)")
    parser.add_argument("--adaptation-notes", default=None,
                        help="Extra adaptation direction")
    parser.add_argument("--variations", type=int, default=1,
                        help="Number of variations to generate per reference (default: 1)")

    args = parser.parse_args()
    run_pipeline(args)


if __name__ == "__main__":
    main()
