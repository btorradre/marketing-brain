#!/usr/bin/env python3
"""
Claymation Replicator Pipeline
==============================
Script + brief + brand → 9-shot claymation ad with burned captions.

Usage:
    python3 pipeline.py --brand Motilli --concept GG-CLAY-01 \
        --script ./script.md \
        --brief "villain: dysbiosis; hero: celery juice fiber"

    # Images only (stop after Stage 2):
    python3 pipeline.py --brand Motilli --concept GG-CLAY-01 \
        --script ./script.md --images-only

    # Autonomous (skip approval gates):
    python3 pipeline.py ... --no-gates
"""

import argparse
import io
import json
import os
import re
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
                    k, v = key.strip(), value.strip().strip('"').strip("'")
                    # Overwrite empty shell vars (setdefault misses these)
                    if not os.environ.get(k):
                        os.environ[k] = v
load_env()

try:
    import requests
except ImportError:
    print("[!] pip install requests"); sys.exit(1)

try:
    from google import genai
    from google.genai import types
    from PIL import Image
except ImportError:
    print("[!] pip install google-genai pillow"); sys.exit(1)

try:
    from anthropic import Anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
VAULT_ROOT = os.path.expanduser("~/Documents/marketing brain")
B_ROLL_ROOT = os.path.join(VAULT_ROOT, "b-roll")

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
# Hardcoded default matches aiugc-replicator / video-scene-replicator
KIE_API_KEY = os.environ.get("KIE_API_KEY") or "ea55b909fc9fefcb6b964e468062f2c2"
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

# Models
GEMINI_STRATEGIST_MODEL = "gemini-2.5-flash"
GEMINI_IMAGE_MODEL = "gemini-3.1-flash-image-preview"  # Nano Banana 2
ANTHROPIC_STRATEGIST_MODEL = "claude-opus-4-7"

# APIs
KIE_CREATE_URL = "https://api.kie.ai/api/v1/jobs/createTask"
KIE_STATUS_URL = "https://api.kie.ai/api/v1/jobs/recordInfo"
KIE_UPLOAD_URL = "https://kieai.redpandaai.co/api/file-stream-upload"

ELEVENLABS_TTS_URL = "https://api.elevenlabs.io/v1/text-to-speech"
ELEVENLABS_MODEL = "eleven_multilingual_v2"

DEFAULT_VOICES = {
    "rachel": "21m00Tcm4TlvDq8ikWAM",
    "drew": "29vD33N1CtxCmqQRPOHJ",
    "domi": "AZnzlk1XvdvUeBnXmlld",
}

# Generation limits
MAX_KLING_RETRIES = 3
KLING_POLL_INTERVAL = 15
KLING_MAX_WAIT = 600
SHOT_DURATION = 5  # seconds per shot
DEFAULT_ASPECT = "9:16"

# ---------------------------------------------------------------------------
# Brand Registry (synced with aiugc-replicator / animated-video-replicator)
# ---------------------------------------------------------------------------
BRAND_REGISTRY = {
    "motilli": {
        "research_docs": [
            os.path.join(VAULT_ROOT, "brands/motilli/Motilli_Master_Copywriting_Brief.md"),
            os.path.join(VAULT_ROOT, "brands/motilli/Motilli_Product_Context.md"),
            os.path.join(VAULT_ROOT, "brands/motilli/Motilli_Avatar_VoC.md"),
        ],
        # CANONICAL product reference — hero-01.webp is THE definitive Motilli product shot (PERMANENT)
        "product_images": [
            os.path.join(VAULT_ROOT, "brands/motilli/motilli pdp/images/hero-01.png"),
            os.path.join(VAULT_ROOT, "statics/product references/motilli/motilli product reference.png"),
        ],
        "default_product_context": (
            "Motilli Celery Juice Fiber Gummies. "
            "BOTTLE: CLEAR SQUARE/cubic plastic jar with rounded corners (NOT cylindrical, NOT round — it is a square prism). "
            "WHITE screw-top cap. "
            "LABEL (green background, white text, covers the front face): "
            "lowercase 'motilli' wordmark (large, at top), 'CELERY JUICE FIBER GUMMIES' title, "
            "'supports natural detoxification & a daily green boost*' tagline, "
            "'Clinically Tested Actives' white pill badge, "
            "'VERIFIED CLEAN' with 'CELERY JUICE, CHLOROPHYLL + PREBIOTIC FIBER' ingredient line, "
            "'5g FIBER' white circle callout, a small white HEART icon, "
            "'GREEN APPLE with other natural flavors' flavor line, "
            "'60 VEGAN GUMMIES / DIETARY SUPPLEMENT' bottom text. "
            "GUMMIES: HEART-SHAPED (classic 3D heart silhouette — two round lobes on top, pointed bottom), "
            "small, plump, DARK MATTE GREEN. "
            "NOT round. NOT oval. NOT pillow-shaped. NOT gummy-bear-shaped."
        ),
        "default_villain_hero": {
            "villain": "Dysbiosis (gut bacteria imbalance)",
            "hero": "Celery juice prebiotic fiber",
        },
    },
    "lunessa": {
        "research_docs": [
            os.path.join(VAULT_ROOT, "brands/lunessa/fh research docs/Lunessa Research Docs 3.0/Lunessa_Master_Copywriting_Brief.docx"),
            os.path.join(VAULT_ROOT, "brands/lunessa/menopause research 2.0/Lunessa_Master_Strategic_Brief.docx"),
        ],
        "product_images": [
            os.path.join(VAULT_ROOT, "brands/lunessa/fh research docs/Lunessa Research Docs 3.0/lunessa spelling corrected.jpg"),
        ],
        "default_product_context": (
            "Lunessa Red Yeast Rice + CoQ10 Gummies — heart health supplement for women. "
            "Supports cholesterol and cardiovascular restoration."
        ),
        "default_villain_hero": {
            "villain": "Oxidized LDL cholesterol plaque",
            "hero": "Red Yeast Rice + CoQ10",
        },
    },
    "velantra-boat-tote": {
        "research_docs": [],
        "product_images": [
            os.path.join(VAULT_ROOT, "statics/product references/velantra/boat tote/01.jpg"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/boat tote/02.jpg"),
        ],
        "default_product_context": "Velantra Boat Tote — canvas tote, leather trim, gold turn-lock.",
        "default_villain_hero": {"villain": "Ugly beat-up everyday bag", "hero": "Velantra Boat Tote"},
    },
    "velantra-meridian": {
        "research_docs": [],
        "product_images": [
            os.path.join(VAULT_ROOT, "statics/product references/velantra/meridian/black 1.webp"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/meridian/brown 1.webp"),
        ],
        "default_product_context": "Velantra Meridian — leather handbag, silver hardware.",
        "default_villain_hero": {"villain": "Bag-that-falls-apart", "hero": "Velantra Meridian"},
    },
    "velantra-weekender": {
        "research_docs": [],
        "product_images": [
            os.path.join(VAULT_ROOT, "statics/product references/velantra/weekender/1.webp"),
            os.path.join(VAULT_ROOT, "statics/product references/velantra/weekender/2.webp"),
        ],
        "default_product_context": "Velantra Weekender — canvas + leather travel bag.",
        "default_villain_hero": {"villain": "Bulky roll-aboard that weighs you down", "hero": "Velantra Weekender"},
    },
}

# ---------------------------------------------------------------------------
# Clay style block — enforced in every image prompt
# ---------------------------------------------------------------------------
CLAY_STYLE_BLOCK = """
CLAYMATION STYLE (MANDATORY, enforce in every pixel):
- Stop-motion clay aesthetic, hand-sculpted figures made of soft plasticine/Play-Doh
- Visible fingerprints, thumb indents, tool marks, seams, subtle asymmetry
- Matte clay texture — NO shine, NO plastic, NO CGI polish, NO 3D-render smoothness
- Shallow depth of field, soft directional key light (slightly warm)
- Tactile surfaces — viewer can see the clay was pressed, rolled, poked
- 9:16 vertical composition, macro framing on character-focused shots
- Frame slightly off-kilter (hand-held stop-motion rig feel)
"""

SHOT_TEMPLATES = {
    1: {
        "purpose": "Problem",
        "lighting": "muted earth tones, slightly cool",
        "framing": "medium shot on avatar mid-complaint",
    },
    2: {
        "purpose": "Tease — magical transformation hint",
        "lighting": "amber glow encroaching from edge",
        "framing": "same avatar, a warm light or sparkle enters frame",
    },
    3: {
        "purpose": "Villain reveal",
        "lighting": "cold steel-blue, dramatic under-lighting, lightning flash",
        "framing": "center-frame portrait, low angle, villain fills frame, menacing",
    },
    4: {
        "purpose": "Conflict — villain tormenting avatar",
        "lighting": "cold, harsh, shadowed",
        "framing": "medium two-shot, villain looming over avatar",
    },
    5: {
        "purpose": "Failed fixes — 3 ineffective solutions",
        "lighting": "neutral, slightly drab",
        "framing": "triptych or sequential: three failed products cracking/dissolving/failing",
    },
    6: {
        "purpose": "Internal repair — tiny clay crew fixing body mechanism",
        "lighting": "warm interior glow, biological scale",
        "framing": "macro inside-the-body view, tiny clay workers, hero ingredient flowing",
    },
    7: {
        "purpose": "Hero reveal (MIRROR Shot 3 composition)",
        "lighting": "warm amber/gold, heroic backlight, lush energy",
        "framing": "center-frame portrait, low angle, IDENTICAL framing to Shot 3 but warm+confident",
    },
    8: {
        "purpose": "Victory — hero defeating villain",
        "lighting": "warm overpowering cold",
        "framing": "hero foreground, villain crumbling in background",
    },
    9: {
        "purpose": "Resolution — product + guarantee",
        "lighting": "warm, clean, product-forward",
        "framing": "product center, avatar holding/using, 'money-back guarantee' text overlay (clay style)",
    },
}

# ---------------------------------------------------------------------------
# Logging & helpers
# ---------------------------------------------------------------------------
def log(stage, msg):
    prefix = f"[Stage {stage}]" if isinstance(stage, int) else f"[{stage}]"
    print(f"{prefix} {msg}", flush=True)

def ensure_dir(p):
    os.makedirs(p, exist_ok=True)
    return p

class Progress:
    def __init__(self, output_dir):
        self.path = os.path.join(output_dir, ".progress.json")
        self.data = {}
        if os.path.exists(self.path):
            with open(self.path) as f:
                self.data = json.load(f)
    def is_done(self, stage):
        return self.data.get(stage, {}).get("done", False)
    def mark(self, stage, info=None):
        self.data[stage] = {"done": True, "info": info or {}, "ts": time.time()}
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=2)

# ---------------------------------------------------------------------------
# Brand loading
# ---------------------------------------------------------------------------
def load_brand(brand_key):
    key = brand_key.lower().replace(" ", "-")
    brand = BRAND_REGISTRY.get(key)
    if not brand:
        log("Brand", f"Unknown brand '{brand_key}'. Known: {list(BRAND_REGISTRY)}")
        return None, [], "", {}

    # Research docs
    chunks = []
    for doc in brand.get("research_docs", []):
        if not os.path.exists(doc):
            continue
        ext = Path(doc).suffix.lower()
        try:
            if ext == ".md":
                with open(doc) as f:
                    chunks.append(f.read())
            elif ext == ".docx":
                try:
                    import docx
                    d = docx.Document(doc)
                    chunks.append("\n".join(p.text for p in d.paragraphs))
                except ImportError:
                    pass
            elif ext == ".pdf":
                try:
                    from pdfminer.high_level import extract_text
                    chunks.append(extract_text(doc))
                except ImportError:
                    pass
        except Exception as e:
            log("Brand", f"  Warn: {doc}: {e}")
    knowledge = "\n\n---\n\n".join(chunks)[:30000]

    product_images = [p for p in brand.get("product_images", []) if os.path.exists(p)]
    default_ctx = brand.get("default_product_context", "")
    default_vh = brand.get("default_villain_hero", {})
    return knowledge, product_images, default_ctx, default_vh

# ---------------------------------------------------------------------------
# Stage 1: Strategist — script → 9-shot plan
# ---------------------------------------------------------------------------
def build_strategist_prompt(script, brief, brand_knowledge, product_ctx, default_vh):
    return f"""You are a direct-response creative strategist building a CLAYMATION video ad.

# Two modes — detect which one the input uses

MODE A — STRUCTURED BRIEF (user provided explicit scene beats with timestamps, scene numbers, or "SCENE BEATS" section):
- Use EXACTLY the scenes the user defined. Do not add, merge, or drop scenes.
- One shot per user-defined beat. Preserve their timings, VO lines, visuals, and intent verbatim where provided.
- Your job is to enrich: flesh out the `image_prompt` and `motion_prompt` from their visual description, and propagate the global art direction into every shot.

MODE B — FREEFORM SCRIPT (no structured beats):
- Use the 9-shot villain/hero arc:
  1. Problem | 2. Tease | 3. Villain reveal (cold) | 4. Conflict | 5. Failed fixes | 6. Internal repair | 7. Hero reveal (MIRROR shot 3, warm) | 8. Victory | 9. Resolution + product
- Shots 3 and 7 MUST share identical composition (framing, angle, pose), opposite lighting (cold vs warm).

# Input Script
{script}

# Brief
{brief}

# Brand product context
{product_ctx}

# Default villain/hero (override if brief specifies)
Villain: {default_vh.get('villain', 'TBD')}
Hero: {default_vh.get('hero', 'TBD')}

# Brand research (voice, avatar language, proof points)
{brand_knowledge[:8000]}

# Task
Output a JSON object with these exact keys:
{{
  "mode": "A" or "B",
  "villain_name": "<specific biological/mechanical villain, or null if the brief doesn't use villain/hero framing>",
  "hero_name": "<specific hero ingredient/feature>",
  "avatar_description": "<2-3 sentence clay avatar: age, gender, wardrobe, distinguishing features, pose. Keep CONSISTENT across every shot unless the brief demands otherwise.>",
  "art_direction": "<2-5 sentences of global visual rules that must flow into EVERY image prompt: color palette, lighting mood, brand color usage rules, texture notes, recurring visual motifs (e.g. 'the pajama button popping off', 'green only on stomach'). This is appended to every shot's image prompt.>",
  "voice_direction": "<1-2 sentences on VO tone for ElevenLabs voice settings: pace, warmth, age, mood>",
  "shots": [
    {{
      "shot_number": 1,
      "purpose": "<short label for this shot's job in the ad>",
      "duration_seconds": 5,
      "vo_line": "<spoken line, avatar's voice, conversational. Use the exact VO from the brief if provided.>",
      "image_prompt": "<SELF-CONTAINED prompt describing the clay scene — avatar pose, setting, props, mood, camera framing. Do NOT include the clay style block or art_direction — those are appended automatically. Do NOT mention any product unless has_product=true.>",
      "motion_prompt": "<slow, deliberate stop-motion motion description — 1-2 sentences. Include any specific motion beats from the brief (e.g. 'button pops off with a tiny ting', 'green glow pulse').>",
      "has_product": false,
      "pure_i2i": false,
      "caption_text": "<4-7 word on-screen caption matching VO pacing. Break long VO lines into multiple caption cards if needed by joining with ' | '.>",
      "framing_notes": "<optional: camera angle, composition, key visual detail>",
      "lighting_notes": "<optional: color temperature, key light, mood>"
    }},
    ...
  ]
}}

# Hard rules
- Sum of durations should match the brief's total runtime target (default 42s if not specified)
- Motion prompts must specify SLOW, stop-motion-paced movement to preserve clay illusion
- No on-screen text descriptions in image_prompt — captions are burned post-production
- Set `has_product: true` ONLY on shots where the actual product appears in frame
- **Set `pure_i2i: true` on EVERY product-focused shot** (end card, hero product shot, close-up of the jar/bottle, or any shot where the product's exact label/shape/proportions must match the real product). Pure i2i bypasses the clay style block and art direction blocks — it tells Nano Banana to do a faithful 1:1 material transformation of the reference image. Keep `pure_i2i: true` on any shot where the product IS the subject, NOT a background element.
- Preserve every brand-specific directive from the brief (brand color restraint, visual callbacks, tagline, end card)
- Output ONLY the JSON object, no prose, no code fences"""

def call_strategist(prompt):
    """Prefer Claude Opus 4.7 if available; fall back to Gemini."""
    if HAS_ANTHROPIC and ANTHROPIC_API_KEY:
        try:
            client = Anthropic(api_key=ANTHROPIC_API_KEY)
            resp = client.messages.create(
                model=ANTHROPIC_STRATEGIST_MODEL,
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}],
            )
            return resp.content[0].text
        except Exception as e:
            log(1, f"  Anthropic call failed ({e}), falling back to Gemini")

    client = genai.Client(api_key=GEMINI_API_KEY)
    resp = client.models.generate_content(
        model=GEMINI_STRATEGIST_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.7),
    )
    return resp.text

def extract_json(text):
    """Extract JSON object from strategist response (strips code fences, prose)."""
    text = text.strip()
    # Strip code fences
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    # Find first { and last }
    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end > start:
        text = text[start:end+1]
    return json.loads(text)

def strategist_stage(script, brief, brand_knowledge, product_ctx, default_vh, output_dir):
    shot_plan_path = os.path.join(output_dir, "script", "shot_plan.json")
    if os.path.exists(shot_plan_path):
        log(1, f"Shot plan cached — reusing {shot_plan_path}")
        with open(shot_plan_path) as f:
            return json.load(f)

    log(1, "Calling strategist...")
    prompt = build_strategist_prompt(script, brief, brand_knowledge, product_ctx, default_vh)
    raw = call_strategist(prompt)

    try:
        plan = extract_json(raw)
    except Exception as e:
        log(1, f"  JSON parse failed: {e}")
        # Save raw for debugging
        raw_path = os.path.join(output_dir, "script", "strategist_raw.txt")
        with open(raw_path, "w") as f:
            f.write(raw)
        raise

    n = len(plan.get("shots", []))
    if n < 3 or n > 15:
        raise RuntimeError(f"Strategist returned {n} shots (expected 3-15)")

    # Normalize: ensure every shot has required fields
    for i, s in enumerate(plan["shots"], 1):
        s.setdefault("shot_number", i)
        s.setdefault("purpose", f"Shot {i}")
        s.setdefault("duration_seconds", SHOT_DURATION)
        s.setdefault("has_product", False)
        s.setdefault("caption_text", s.get("vo_line", "")[:40])
        s.setdefault("framing_notes", "")
        s.setdefault("lighting_notes", "")
    plan.setdefault("art_direction", "")
    plan.setdefault("voice_direction", "")

    ensure_dir(os.path.join(output_dir, "script"))
    with open(shot_plan_path, "w") as f:
        json.dump(plan, f, indent=2)
    log(1, f"Shot plan → {shot_plan_path} ({n} shots, mode={plan.get('mode','?')})")
    log(1, f"  Villain: {plan.get('villain_name')} | Hero: {plan.get('hero_name')}")
    return plan

# ---------------------------------------------------------------------------
# Stage 2: Nano Banana 2 i2i — 9 clay stills
# ---------------------------------------------------------------------------
def build_image_prompt(shot, avatar_desc, product_ctx, art_direction=""):
    """Build full prompt. Prefers strategist-provided shot-level fields; falls back to SHOT_TEMPLATES for default 9-shot mode.

    If shot has 'pure_i2i': true, returns a minimal 'edit this image' directive — no clay style block,
    no avatar, no art direction. Used when you want a faithful 1:1 i2i transformation of a product ref.
    """
    if shot.get("pure_i2i"):
        return (
            "Edit this image. "
            "Transform ONLY the material into hand-sculpted stop-motion claymation (matte clay texture, visible fingerprints, tool marks, tiny hand-made imperfections). "
            "PRESERVE EXACTLY: the shape of every object, the proportions, the label text content and layout, the colors, the arrangement, the composition, the background, the lighting angle. "
            "Do NOT change the jar silhouette. Do NOT re-interpret the label. Do NOT rearrange the gummies. Do NOT add or remove any element. "
            "This is a 1:1 material translation from plastic/gelatin to clay — geometry and labels must stay IDENTICAL to the reference image.\n\n"
            f"Additional direction: {shot.get('image_prompt', '')}"
        )

    sn = shot["shot_number"]
    purpose = shot.get("purpose") or SHOT_TEMPLATES.get(sn, {}).get("purpose", "")
    lighting = shot.get("lighting_notes") or SHOT_TEMPLATES.get(sn, {}).get("lighting", "")
    framing = shot.get("framing_notes") or SHOT_TEMPLATES.get(sn, {}).get("framing", "")

    has_product = shot.get("has_product", False)
    extra_refs = shot.get("extra_refs") or []
    extra_products_desc = shot.get("extra_products_description", "")

    if extra_refs:
        # Shot-specific reference products (e.g. failed solutions like Miralax/Align/Metamucil)
        product_block = (
            f"\nThe products in-frame are shown in the reference images and described as: {extra_products_desc}\n"
            "Each product must appear as a clay-sculpted replica with visible tool marks — but still CLEARLY RECOGNIZABLE as the real product (matching colors, shape, label text, proportions). Recreate the label and branding faithfully in clay."
        )
    elif has_product:
        product_block = (
            f"\nThe product in-frame is: {product_ctx}\n"
            "The product must appear as a clay-sculpted replica with visible tool marks — but still clearly recognizable as this exact product (matching colors, shape, label). Use the reference image for accuracy."
        )
    else:
        product_block = "\nDO NOT include ANY product, bottle, package, or branded item in this frame."

    art_block = f"\n\nGLOBAL ART DIRECTION (enforce in every frame):\n{art_direction}" if art_direction else ""

    return f"""{CLAY_STYLE_BLOCK}

SHOT {sn} — {purpose}
Lighting: {lighting}
Framing: {framing}
Avatar: {avatar_desc}{art_block}

Scene: {shot['image_prompt']}
{product_block}

Render as a single 9:16 frame. Tactile clay, NOT a 3D render. NO on-screen text, NO captions — those are added in post."""

def generate_images(shot_plan, product_images, output_dir):
    images_dir = ensure_dir(os.path.join(output_dir, "images"))
    client = genai.Client(api_key=GEMINI_API_KEY)
    avatar_desc = shot_plan.get("avatar_description", "")
    art_direction = shot_plan.get("art_direction", "")
    n_shots = len(shot_plan["shots"])
    results = []

    for shot in shot_plan["shots"]:
        sn = shot["shot_number"]
        out_path = os.path.join(images_dir, f"shot_{sn:02d}.png")

        if os.path.exists(out_path):
            log(2, f"  Shot {sn} cached")
            results.append({"shot": sn, "path": out_path, "status": "cached"})
            continue

        log(2, f"  Shot {sn}/{n_shots} generating...")
        prompt_text = build_image_prompt(shot, avatar_desc, "Product (see reference image)", art_direction)

        parts = []
        # Priority: shot-specific extra_refs > brand-level product images (when has_product)
        extra_refs = shot.get("extra_refs") or []
        refs_to_inject = []
        if extra_refs:
            for ref in extra_refs[:4]:
                if os.path.exists(ref):
                    refs_to_inject.append(ref)
                else:
                    log(2, f"    WARN: extra_ref not found: {ref}")
        elif shot.get("has_product") and product_images:
            refs_to_inject = [p for p in product_images[:2] if os.path.exists(p)]

        for pimg in refs_to_inject:
            try:
                # Normalize to PNG bytes (handles webp, jpg, etc.)
                with Image.open(pimg) as im:
                    im = im.convert("RGB")
                    buf = io.BytesIO()
                    im.save(buf, format="PNG")
                    img_bytes = buf.getvalue()
                parts.append(types.Part.from_bytes(data=img_bytes, mime_type="image/png"))
                log(2, f"    attached ref: {os.path.basename(pimg)} ({len(img_bytes)//1024}KB)")
            except Exception as e:
                log(2, f"    WARN: could not load ref {pimg}: {e}")

        parts.append(types.Part.from_text(text=prompt_text))

        success = False
        for attempt in range(3):
            try:
                resp = client.models.generate_content(
                    model=GEMINI_IMAGE_MODEL,
                    contents=types.Content(parts=parts),
                    config=types.GenerateContentConfig(
                        response_modalities=["image", "text"],
                        temperature=0.5,
                    ),
                )
                if resp.candidates:
                    for part in resp.candidates[0].content.parts:
                        if hasattr(part, "inline_data") and part.inline_data:
                            with open(out_path, "wb") as f:
                                f.write(part.inline_data.data)
                            log(2, f"    ✓ {out_path}")
                            results.append({"shot": sn, "path": out_path, "status": "success"})
                            success = True
                            break
                if success:
                    break
            except Exception as e:
                log(2, f"    Attempt {attempt+1} error: {e}")
                time.sleep(5)

        if not success:
            log(2, f"    ✗ Shot {sn} failed")
            results.append({"shot": sn, "path": None, "status": "failed"})
        time.sleep(2)

    ok = sum(1 for r in results if r["status"] in ("success", "cached"))
    log(2, f"Image generation: {ok}/{n_shots} shots")
    return results

# ---------------------------------------------------------------------------
# Stage 3: Kling 3.0 i2v — animate each still
# ---------------------------------------------------------------------------
def upload_to_kie(path, mime):
    try:
        with open(path, "rb") as f:
            resp = requests.post(
                KIE_UPLOAD_URL,
                headers={"Authorization": f"Bearer {KIE_API_KEY}"},
                files={"file": (os.path.basename(path), f, mime)},
                data={"uploadPath": "images" if mime.startswith("image") else "audio"},
                timeout=120,
            )
        data = resp.json()
        if data.get("code") == 200 and data.get("data", {}).get("downloadUrl"):
            return data["data"]["downloadUrl"]
    except Exception as e:
        log("upload", f"  Error: {e}")
    return None

def poll_kling(task_id, headers, max_wait=KLING_MAX_WAIT):
    start = time.time()
    while time.time() - start < max_wait:
        try:
            resp = requests.get(KIE_STATUS_URL, headers=headers,
                                params={"taskId": task_id}, timeout=30)
            data = resp.json()
            if data.get("code") != 200:
                time.sleep(KLING_POLL_INTERVAL); continue
            state = data["data"].get("state", "")
            if state == "success":
                result = json.loads(data["data"].get("resultJson", "{}"))
                urls = result.get("resultUrls", [])
                return urls[0] if urls else None
            if state == "fail":
                log(3, f"    Kling failed: {data['data'].get('failMsg','unknown')}")
                return None
            time.sleep(KLING_POLL_INTERVAL)
        except Exception:
            time.sleep(KLING_POLL_INTERVAL)
    return None

def animate_shots(shot_plan, image_results, output_dir):
    clips_dir = ensure_dir(os.path.join(output_dir, "clips"))
    headers = {"Authorization": f"Bearer {KIE_API_KEY}", "Content-Type": "application/json"}
    n_shots = len(shot_plan["shots"])
    results = []

    for shot, ir in zip(shot_plan["shots"], image_results):
        sn = shot["shot_number"]
        out_path = os.path.join(clips_dir, f"shot_{sn:02d}.mp4")

        if os.path.exists(out_path):
            log(3, f"  Shot {sn} cached")
            results.append({"shot": sn, "path": out_path, "status": "cached"})
            continue

        if ir.get("status") not in ("success", "cached") or not ir.get("path"):
            log(3, f"  Shot {sn} — no image, skipping")
            results.append({"shot": sn, "path": None, "status": "skipped"})
            continue

        log(3, f"  Shot {sn}/{n_shots} animating...")
        image_url = upload_to_kie(ir["path"], "image/png")
        if not image_url:
            results.append({"shot": sn, "path": None, "status": "upload_failed"})
            continue

        # Enforce slow stop-motion motion + organic imperfection cues (apply to every Kling prompt)
        motion = shot.get("motion_prompt", "Slow deliberate motion.")
        ORGANIC_CUES = (
            "Subtle inconsistent handheld micro jitter. "
            "Slight rolling shutter wobble during motion. "
            "Eyes briefly lose focus, then re-lock onto camera. "
            "Background movement continues even when subject is still."
        )
        kling_prompt = (
            f"Stop-motion claymation animation. Slow, deliberate, frame-by-frame "
            f"style with subtle jittery micro-motion (NOT smooth CGI interpolation). "
            f"Preserve clay texture and hand-made imperfections in every frame. "
            f"{ORGANIC_CUES} {motion}"
        )

        payload = {
            "model": "kling-3.0/video",
            "input": {
                "prompt": kling_prompt,
                "image_urls": [image_url],
                "sound": False,
                "duration": str(SHOT_DURATION),
                "aspect_ratio": DEFAULT_ASPECT,
                "mode": "pro",
                "multi_shots": False,
            }
        }

        success = False
        for attempt in range(MAX_KLING_RETRIES):
            try:
                resp = requests.post(KIE_CREATE_URL, headers=headers, json=payload, timeout=60)
                data = resp.json()
                if data.get("code") != 200:
                    log(3, f"    Attempt {attempt+1} create failed: {data.get('msg','?')}")
                    time.sleep(10); continue
                task_id = data["data"]["taskId"]
                log(3, f"    Task: {task_id}")
                video_url = poll_kling(task_id, headers)
                if video_url:
                    vid = requests.get(video_url, timeout=180)
                    with open(out_path, "wb") as f:
                        f.write(vid.content)
                    log(3, f"    ✓ {out_path}")
                    results.append({"shot": sn, "path": out_path, "status": "success"})
                    success = True
                    break
            except Exception as e:
                log(3, f"    Attempt {attempt+1} error: {e}")
                time.sleep(10)

        if not success:
            results.append({"shot": sn, "path": None, "status": "failed"})
        time.sleep(3)

    ok = sum(1 for r in results if r["status"] in ("success", "cached"))
    log(3, f"Animation: {ok}/{n_shots} shots")
    return results

# ---------------------------------------------------------------------------
# Stage 4: ElevenLabs VO
# ---------------------------------------------------------------------------
def generate_voiceover(shot_plan, voice_name, output_dir):
    audio_dir = ensure_dir(os.path.join(output_dir, "audio"))
    vo_full_path = os.path.join(audio_dir, "voiceover.mp3")

    # Compose full script from shot VO lines
    script_text = " ".join(s["vo_line"].strip() for s in shot_plan["shots"])
    voice_id = DEFAULT_VOICES.get(voice_name.lower(), voice_name)

    if os.path.exists(vo_full_path):
        log(4, f"  VO cached — {vo_full_path}")
    else:
        log(4, f"  Generating VO ({len(script_text)} chars, voice={voice_name})...")
        url = f"{ELEVENLABS_TTS_URL}/{voice_id}"
        payload = {
            "text": script_text,
            "model_id": ELEVENLABS_MODEL,
            "voice_settings": {
                "stability": 0.55,
                "similarity_boost": 0.75,
                "style": 0.2,
                "use_speaker_boost": True,
            },
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
                    with open(vo_full_path, "wb") as f:
                        f.write(resp.content)
                    log(4, f"  ✓ {vo_full_path}")
                    break
                log(4, f"  HTTP {resp.status_code}: {resp.text[:200]}")
            except Exception as e:
                log(4, f"  Error: {e}")
            time.sleep(5)
        else:
            raise RuntimeError("VO generation failed after 3 attempts")

    # Get VO duration; compute per-shot start/end times proportional to word counts
    probe = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", vo_full_path],
        capture_output=True, text=True,
    )
    try:
        total = float(probe.stdout.strip())
    except Exception:
        total = 42.0

    # Allocate time proportional to word count per shot
    word_counts = [max(1, len(s["vo_line"].split())) for s in shot_plan["shots"]]
    total_words = sum(word_counts)
    times = []
    t = 0.0
    for wc in word_counts:
        dur = total * wc / total_words
        times.append({"start": round(t, 2), "duration": round(dur, 2)})
        t += dur

    segments = [
        {"shot": s["shot_number"], "text": s["vo_line"],
         "start": times[i]["start"], "duration": times[i]["duration"],
         "caption": s.get("caption_text") or s["vo_line"]}
        for i, s in enumerate(shot_plan["shots"])
    ]

    manifest = {"voiceover": vo_full_path, "total_duration": total, "segments": segments}
    manifest_path = os.path.join(audio_dir, "segments.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    log(4, f"  Segments → {manifest_path}")
    return manifest

# ---------------------------------------------------------------------------
# Stage 5: FFmpeg stitch + burned captions
# ---------------------------------------------------------------------------
def write_srt(segments, path):
    """Write .srt captions for editors."""
    def fmt(t):
        h = int(t // 3600); m = int((t % 3600) // 60); s = t % 60
        return f"{h:02d}:{m:02d}:{int(s):02d},{int((s-int(s))*1000):03d}"
    with open(path, "w") as f:
        for i, seg in enumerate(segments, 1):
            end = seg["start"] + seg["duration"]
            f.write(f"{i}\n{fmt(seg['start'])} --> {fmt(end)}\n{seg['caption']}\n\n")

def escape_drawtext(s):
    """Escape characters special to ffmpeg drawtext filter."""
    return (s.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\u2019")
            .replace(",", "\\,").replace("[", "\\[").replace("]", "\\]")
            .replace(";", "\\;").replace("%", "\\%"))

def wrap_caption(text, max_chars=28):
    """Wrap a caption to max_chars per line (1-2 lines)."""
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        if not cur:
            cur = w
        elif len(cur) + 1 + len(w) <= max_chars:
            cur += " " + w
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return "\n".join(lines[:2])

def find_font():
    candidates = [
        "/System/Library/Fonts/Supplemental/Impact.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None

def render_caption_png(text, width, height, out_path):
    """Render caption PNG with white text + black outline using PIL. Transparent bg."""
    try:
        from PIL import Image as PILImage, ImageDraw, ImageFont
    except ImportError:
        return False

    img = PILImage.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Try a few font paths
    font = None
    for fp, size in [
        ("/System/Library/Fonts/Supplemental/Impact.ttf", 72),
        ("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 72),
        ("/System/Library/Fonts/Helvetica.ttc", 72),
    ]:
        if os.path.exists(fp):
            try:
                font = ImageFont.truetype(fp, size)
                break
            except Exception:
                continue
    if font is None:
        font = ImageFont.load_default()

    wrapped = wrap_caption(text, max_chars=22)
    # Measure
    bbox = draw.multiline_textbbox((0, 0), wrapped, font=font, align="center", spacing=8)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = (width - tw) // 2 - bbox[0]
    y = int(height * 0.78) - th // 2

    # Black outline — draw text with offset in 8 directions
    outline = 5
    for dx in range(-outline, outline + 1):
        for dy in range(-outline, outline + 1):
            if dx == 0 and dy == 0:
                continue
            draw.multiline_text((x + dx, y + dy), wrapped, font=font,
                                fill=(0, 0, 0, 245), align="center", spacing=8)
    # White fill
    draw.multiline_text((x, y), wrapped, font=font,
                        fill=(255, 255, 255, 255), align="center", spacing=8)

    img.save(out_path, "PNG")
    return True


def stitch_final(clip_results, vo_manifest, output_dir, burn_captions=True):
    """Stretch each Kling clip to match its VO segment duration, optionally overlay caption PNGs, mix VO."""
    final_dir = ensure_dir(os.path.join(output_dir, "final"))
    tmp_dir = ensure_dir(os.path.join(output_dir, "final", "_tmp"))
    captions_dir = ensure_dir(os.path.join(output_dir, "final", "_captions"))
    final_path = os.path.join(final_dir, "final.mp4")

    # Collect clips + segments
    clip_paths = []
    for cr in clip_results:
        if cr.get("status") in ("success", "cached") and cr.get("path"):
            clip_paths.append(cr["path"])
        else:
            log(5, f"  WARN: shot {cr['shot']} missing — stitch may be short")
    if not clip_paths:
        raise RuntimeError("No clips available for stitch")

    segments = vo_manifest["segments"]
    if len(segments) != len(clip_paths):
        log(5, f"  WARN: {len(segments)} segments vs {len(clip_paths)} clips — pairing by index")

    # Write SRT for editors
    srt_path = os.path.join(final_dir, "captions.srt")
    write_srt(segments, srt_path)
    log(5, f"  SRT → {srt_path}")

    # Probe first clip for dimensions
    probe = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json",
         "-show_streams", clip_paths[0]],
        capture_output=True, text=True,
    )
    try:
        streams = json.loads(probe.stdout)["streams"]
        vs = next(s for s in streams if s["codec_type"] == "video")
        W, H = int(vs["width"]), int(vs["height"])
    except Exception:
        W, H = 1076, 1924
    log(5, f"  Video dims: {W}x{H}")

    # Stage A: per-shot stretch + caption overlay → shot_final_NN.mp4
    stretched_paths = []
    for i, (clip, seg) in enumerate(zip(clip_paths, segments), 1):
        # Get current clip duration
        dp = subprocess.run(
            ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
             "-of", "default=nw=1:nk=1", clip],
            capture_output=True, text=True,
        )
        try:
            cur_dur = float(dp.stdout.strip())
        except Exception:
            cur_dur = 5.0
        target_dur = max(1.0, float(seg["duration"]))
        # setpts factor: multiply PTS to stretch (slow down)
        pts_factor = target_dur / cur_dur

        # Render caption PNG for this shot (only if burn_captions)
        caption_png = os.path.join(captions_dir, f"shot_{i:02d}.png")
        if burn_captions:
            caption_text = seg.get("caption") or seg.get("text", "")
            have_caption = render_caption_png(caption_text, W, H, caption_png)
        else:
            have_caption = False

        out = os.path.join(tmp_dir, f"shot_final_{i:02d}.mp4")
        if have_caption and os.path.exists(caption_png):
            filter_complex = (
                f"[0:v]setpts={pts_factor:.4f}*PTS,fps=30[v0];"
                f"[v0][1:v]overlay=0:0[vout]"
            )
            cmd = [
                "ffmpeg", "-y", "-i", clip, "-i", caption_png,
                "-filter_complex", filter_complex,
                "-map", "[vout]",
                "-an",
                "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                "-pix_fmt", "yuv420p",
                "-t", f"{target_dur:.3f}",
                out,
            ]
        else:
            cmd = [
                "ffmpeg", "-y", "-i", clip,
                "-vf", f"setpts={pts_factor:.4f}*PTS,fps=30",
                "-an",
                "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                "-pix_fmt", "yuv420p",
                "-t", f"{target_dur:.3f}",
                out,
            ]
        log(5, f"  Shot {i}: stretch {cur_dur:.2f}s→{target_dur:.2f}s (×{pts_factor:.2f}), caption={'yes' if have_caption else 'no'}")
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if not os.path.exists(out):
            log(5, f"    ERR: {r.stderr[-400:]}")
            raise RuntimeError(f"Stage A failed on shot {i}")
        stretched_paths.append(out)

    # Stage B: concat stretched clips
    concat_list = os.path.join(tmp_dir, "_concat.txt")
    with open(concat_list, "w") as f:
        for p in stretched_paths:
            safe = p.replace("'", "'\\''")
            f.write(f"file '{safe}'\n")

    stitched_video = os.path.join(tmp_dir, "_stitched.mp4")
    log(5, "  Concatenating stretched clips...")
    r = subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list,
         "-c", "copy", stitched_video],
        capture_output=True, text=True, timeout=600,
    )
    if not os.path.exists(stitched_video):
        log(5, f"    ERR: {r.stderr[-400:]}")
        raise RuntimeError("Concat failed")

    # Stage C: mix VO
    vo_path = vo_manifest["voiceover"]
    log(5, "  Mixing VO...")
    r = subprocess.run(
        ["ffmpeg", "-y", "-i", stitched_video, "-i", vo_path,
         "-map", "0:v", "-map", "1:a",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
         "-shortest",
         final_path],
        capture_output=True, text=True, timeout=300,
    )
    if not os.path.exists(final_path):
        log(5, f"    ERR: {r.stderr[-600:]}")
        raise RuntimeError("Final mix failed")

    # Cleanup temp (keep captions dir for re-runs)
    try:
        import shutil
        shutil.rmtree(tmp_dir)
    except Exception:
        pass

    log(5, f"  ✓ {final_path}")
    return final_path

# ---------------------------------------------------------------------------
# Assembly guide
# ---------------------------------------------------------------------------
def write_assembly_guide(shot_plan, clip_results, vo_manifest, final_path, output_dir, concept, brand):
    md = [
        f"# Claymation Ad Assembly Guide — {concept}",
        f"**Brand**: {brand}",
        f"**Final**: `{final_path}`",
        f"**Duration**: {vo_manifest['total_duration']:.1f}s",
        f"**Villain**: {shot_plan.get('villain_name')}",
        f"**Hero**: {shot_plan.get('hero_name')}",
        f"**Avatar**: {shot_plan.get('avatar_description')}",
        "",
        "## Shot List",
        "",
        "| # | Purpose | Start | Dur | VO | Caption |",
        "|---|---------|-------|-----|----|---------|",
    ]
    for seg, shot in zip(vo_manifest["segments"], shot_plan["shots"]):
        tmpl = SHOT_TEMPLATES[shot["shot_number"]]
        md.append(
            f"| {shot['shot_number']} | {tmpl['purpose']} | "
            f"{seg['start']:.1f}s | {seg['duration']:.1f}s | "
            f"{shot['vo_line']} | {seg['caption']} |"
        )
    md.extend([
        "",
        "## Regeneration Notes",
        "- To regenerate a single shot: delete `images/shot_NN.png` and `clips/shot_NN.mp4`, rerun pipeline.",
        "- To re-style captions: edit `final/captions.srt` and re-run FFmpeg stitch manually.",
        "- Shots 3 (villain) and 7 (hero) are highest-impact — regenerate if not intimidating/confident enough.",
    ])
    path = os.path.join(output_dir, "final", "assembly_guide.md")
    with open(path, "w") as f:
        f.write("\n".join(md))
    log("Guide", f"  → {path}")
    return path

# ---------------------------------------------------------------------------
# Approval gates
# ---------------------------------------------------------------------------
def gate(name, message, no_gates=False):
    if no_gates:
        log("Gate", f"{name}: auto-approved (--no-gates)")
        return True
    log("Gate", f"\n{'='*60}\n{name}\n{'='*60}\n{message}")
    try:
        ans = input("[gate] Approve? [y/N/regen=<shots>]: ").strip().lower()
    except EOFError:
        log("Gate", "No stdin — auto-approving")
        return True
    if ans.startswith("y"):
        return True
    if ans.startswith("regen"):
        # e.g. "regen=3,7" → delete those shot files and return None to signal re-run
        shots = re.findall(r"\d+", ans)
        log("Gate", f"Regen requested: {shots}. Delete the corresponding files and re-run.")
        return "regen:" + ",".join(shots)
    return False

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="Claymation Replicator Pipeline")
    ap.add_argument("--brand", required=True)
    ap.add_argument("--concept", required=True, help="e.g. GG-CLAY-01")
    ap.add_argument("--script", help="Path to script .md file")
    ap.add_argument("--script-text", help="Raw script text (use if no file)")
    ap.add_argument("--brief", default="", help="Brief description (villain, hero, failed fixes)")
    ap.add_argument("--voice", default="rachel", help="ElevenLabs voice name or ID")
    ap.add_argument("--no-gates", action="store_true", help="Skip approval gates")
    ap.add_argument("--no-captions", action="store_true", help="Skip burned-in captions (still outputs .srt)")
    ap.add_argument("--images-only", action="store_true", help="Stop after Stage 2 (images)")
    ap.add_argument("--output-dir", help="Override output directory")
    args = ap.parse_args()

    # Validate concept code
    if not re.match(r"^[A-Z]{2,3}-CLAY-\d{2}$", args.concept):
        log("Main", f"WARN: concept '{args.concept}' does not match ANGLE-CLAY-## convention")

    # Resolve output dir
    brand_lc = args.brand.lower()
    output_dir = args.output_dir or os.path.join(B_ROLL_ROOT, brand_lc, args.concept)
    ensure_dir(output_dir)
    log("Main", f"Output: {output_dir}")

    # Resolve script
    if args.script:
        if not os.path.exists(args.script):
            log("Main", f"Script not found: {args.script}"); sys.exit(1)
        with open(args.script) as f:
            script_text = f.read()
    elif args.script_text:
        script_text = args.script_text
    else:
        log("Main", "ERROR: --script or --script-text required"); sys.exit(1)

    # Save brief
    ensure_dir(os.path.join(output_dir, "script"))
    with open(os.path.join(output_dir, "script", "brief.md"), "w") as f:
        f.write(f"# Brief\n\n{args.brief}\n\n# Script\n\n{script_text}\n")

    # Load brand
    knowledge, product_images, product_ctx, default_vh = load_brand(args.brand)
    log("Brand", f"  Research: {len(knowledge)} chars | Product imgs: {len(product_images)}")

    progress = Progress(output_dir)

    # --- Stage 1: Strategist ---
    log(1, "STRATEGIST — 9-shot breakdown")
    shot_plan = strategist_stage(
        script_text, args.brief, knowledge, product_ctx, default_vh, output_dir
    )
    progress.mark("stage1_strategist")

    # --- Stage 2: Nano Banana 2 images ---
    log(2, "NANO BANANA 2 — clay stills")
    image_results = generate_images(shot_plan, product_images, output_dir)
    total_shots = len(shot_plan["shots"])
    ok_imgs = sum(1 for r in image_results if r["status"] in ("success", "cached"))
    if ok_imgs < total_shots:
        log(2, f"  WARN: only {ok_imgs}/{total_shots} images generated")
    progress.mark("stage2_images", {"ok": ok_imgs})

    # --- Approval Gate 1 ---
    n_shots = len(shot_plan["shots"])
    g1 = gate(
        f"Gate 1 — Review {n_shots} stills",
        f"{n_shots} clay stills generated in:\n  {os.path.join(output_dir, 'images')}\n\n"
        f"Review before spending Kling credits (~${0.5 * n_shots:.2f} total).\n"
        f"Villain: {shot_plan.get('villain_name') or '—'} | Hero: {shot_plan.get('hero_name') or '—'}",
        no_gates=args.no_gates,
    )
    if g1 is False:
        log("Main", "Gate 1 denied — exiting"); sys.exit(0)
    if isinstance(g1, str) and g1.startswith("regen:"):
        log("Main", f"Regen requested — delete listed shot files and rerun"); sys.exit(0)

    if args.images_only:
        log("Main", "Images-only mode — done"); return

    # --- Stage 3: Kling animate ---
    log(3, "KLING 3.0 — animate stills")
    clip_results = animate_shots(shot_plan, image_results, output_dir)
    progress.mark("stage3_clips")

    # --- Stage 4: VO ---
    log(4, "ELEVENLABS — voiceover")
    vo_manifest = generate_voiceover(shot_plan, args.voice, output_dir)
    progress.mark("stage4_vo")

    # --- Stage 5: Stitch + captions ---
    log(5, "FFMPEG — stitch + burned captions" if not args.no_captions else "FFMPEG — stitch (no captions)")
    final_path = stitch_final(clip_results, vo_manifest, output_dir, burn_captions=not args.no_captions)
    progress.mark("stage5_final")

    # Assembly guide
    write_assembly_guide(
        shot_plan, clip_results, vo_manifest, final_path,
        output_dir, args.concept, args.brand,
    )

    # --- Approval Gate 2 ---
    gate(
        "Gate 2 — Review final MP4",
        f"Finished:\n  {final_path}\n\nDuration: {vo_manifest['total_duration']:.1f}s",
        no_gates=args.no_gates,
    )

    log("Main", f"\n✓ Complete — {final_path}")

if __name__ == "__main__":
    main()
