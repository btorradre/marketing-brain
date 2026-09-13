---
name: ad-replicator
description: Takes a reference ad image (static, native, or branded), analyzes why it works using Claude Opus 4.6, adapts it for your brand using research docs from the vault, generates an image-to-image prompt, and sends it to Nano Banana 2 for generation. Supports image-to-image transformation with product reference injection. Use when the user wants to replicate, adapt, or riff on a reference ad creative for Motilli, Lunessa, Velantra, or any brand.
disable-model-invocation: false
---

## GOLDEN NUGGET DOCTRINE (MANDATORY — locked 2026-07-11)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded DEEP FRAME in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: *is this the topic, or is this the motive?* If it's the topic, dig one layer deeper (memory loss → becoming my parent; GLP-1 bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes.** The golden nugget LEADS — very top of the piece, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence BEFORE drafting. When analyzing a reference ad/funnel/swipe instead of writing, state the nugget it's built on and whether it leads with it. If the research hasn't surfaced one, mine reviews/VOC/Reddit until it does — never default to a surface angle.

# Ad Replicator

Takes a reference ad image, breaks down why it works, adapts it for your brand using vault research docs, and generates the adapted image via Nano Banana 2 (image-to-image).

## Pipeline Overview

```
Reference Ad Image(s)
    |
    v
[Stage 1] Ad Analysis via Claude Opus 4.6
    |       (why it works, elements, angle, composition, visual style)
    v
[Stage 2] Brand Adaptation Strategy (Opus 4.6 + vault brand knowledge)
    |       (1:1 adaptation plan, image generation prompt)
    v
[Stage 3] Image-to-Image Generation (Nano Banana 2)
    |       (reference image + product refs + adaptation prompt → branded image)
    v
[Output] Generated adapted ad image(s) saved locally
```

## Required Inputs

When the user invokes this skill, collect:

1. **Reference ad image path(s)** — one or more local file paths to the ad images to replicate/adapt. Can be PNG, JPG, JPEG, or WEBP.
2. **Brand name** — which brand this is for (Motilli, Lunessa, Velantra, or other). The pipeline auto-loads research docs, product context, and hero product images from the vault.
3. **"Why it works" analysis** (optional) — if the user provides their own breakdown of why the reference works, use it. Otherwise the pipeline generates the analysis automatically.
4. **Adaptation notes** (optional) — extra direction on how to adapt (e.g., "keep the same composition but swap for our product and avatar", "make it more native/less branded", "change the setting to a kitchen").
5. **Product context** (optional) — auto-loaded from vault for registered brands. Override if needed.
6. **Product reference images** (optional) — auto-loaded (hero images per brand). Override with comma-separated paths if the user wants specific product shots used.
7. **Output directory** (optional) — defaults to `./ad-replicator-output`.
8. **Number of variations** (optional) — how many adapted versions to generate per reference. Defaults to 1.

## Execution Instructions

Run the pipeline script at `~/.claude/skills/ad-replicator/ad_replicator.py`.

**Dependencies:**
```bash
pip install anthropic google-genai Pillow python-dotenv
```

**API keys:** Loaded from `~/Documents/marketing brain/.env`. Required keys: `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`.

### How to run

Minimal (brand auto-loads everything from vault):
```bash
python3 ~/.claude/skills/ad-replicator/ad_replicator.py \
  --reference "/path/to/reference-ad.png" \
  --brand "Motilli" \
  --output-dir "./ad-replicator-output"
```

With product image override:
```bash
python3 ~/.claude/skills/ad-replicator/ad_replicator.py \
  --reference "/path/to/reference-ad.png" \
  --brand "Lunessa" \
  --product-images "/path/to/product1.png,/path/to/product2.jpg" \
  --output-dir "./ad-replicator-output"
```

Multiple references with variations:
```bash
python3 ~/.claude/skills/ad-replicator/ad_replicator.py \
  --reference "/path/to/ref1.png" "/path/to/ref2.jpg" \
  --brand "Motilli" \
  --variations 3 \
  --adaptation-notes "Keep composition identical, swap product and avatar age to 45-55" \
  --output-dir "./ad-replicator-output"
```

With user-provided analysis:
```bash
python3 ~/.claude/skills/ad-replicator/ad_replicator.py \
  --reference "/path/to/reference-ad.png" \
  --brand "Motilli" \
  --why-it-works "Strong hook via curiosity gap. Split layout with ingredient callout left, product right. Clinical authority positioning. The bold claim stops scroll, ingredients provide mechanism proof." \
  --output-dir "./ad-replicator-output"
```

### What the pipeline does at each stage

**Stage 1 — Ad Analysis (Claude Opus 4.6)**
- Sends the reference ad image to Claude Opus 4.6 with a detailed analysis prompt
- Returns structured JSON with:
  - `why_it_works`: The persuasion mechanics — what makes this ad effective
  - `visual_elements`: Every visual element catalogued (layout, colors, typography, imagery, props)
  - `composition`: How the image is structured (split layout, centered, grid, etc.)
  - `angle`: The persuasion angle (authority, social proof, curiosity gap, fear, aspiration, etc.)
  - `audience`: Who this ad targets (demographics, psychographics, awareness level)
  - `product_presence`: Whether the reference contains a product and what kind
  - `text_content`: Any text/copy visible in the image
  - `style`: Visual style (native/UGC, branded/polished, editorial, clinical, lifestyle)
  - `color_palette`: Dominant colors and their psychological function
  - `mood`: Emotional tone of the image

**Stage 2 — Brand Adaptation Strategy (Claude Opus 4.6 + Brand Knowledge)**
- Takes the Stage 1 analysis + brand knowledge from vault + product context
- Generates a detailed adaptation plan that preserves what works while adapting for the target brand
- Produces an image generation prompt specifically crafted for Nano Banana 2's image-to-image mode
- The prompt preserves:
  - Composition and layout (1:1 structural match)
  - Visual style and mood
  - Persuasion mechanics and angle
- The prompt adapts:
  - Product to target brand's product (if product is present)
  - Avatar demographics to target brand's audience
  - Colors/branding to target brand's palette (if branded style)
  - Setting/environment to match target brand's avatar world
  - Any text/copy elements to target brand messaging
- Brand knowledge (up to 30k chars from vault research docs) is injected so Claude understands avatar, mechanism, voice, and visual identity
- Output: JSON with analysis + adaptation prompt per reference image

**Stage 3 — Image-to-Image via Nano Banana 2 (`gemini-3.1-flash-image-preview`)**
- For each reference, sends the **reference image** + brand adaptation prompt to Nano Banana 2
- This is IMAGE-TO-IMAGE editing — Gemini transforms the reference directly
- **Smart product inclusion**: only sends the hero product reference image when the reference actually contains a product (detected in Stage 1). References without products get a guard prompt: "Do NOT add any product to this image"
- If `--product-images` are provided and the reference has a product, those images are included so Nano Banana can replicate the exact product appearance
- Falls back to text-only generation if the reference image can't be loaded
- Rate limited (2s between generations)
- Output: `generated/ref_001_adapted_v001.png`, etc.

## Brand Knowledge Auto-Loading

When you specify `--brand "Motilli"`, the pipeline automatically:

1. Looks up the brand in the `BRAND_REGISTRY` dict
2. Reads all registered research docs (.md, .docx, .pdf) from the vault
3. Injects up to 30k chars of brand knowledge into Stage 2's Claude prompt
4. Loads the hero product image(s) for Stage 3's image-to-image editing
5. Falls back to the registered default product context if `--product-context` isn't provided

### Registered Brands

| Brand Key | Product | Images | Default Context |
|-----------|---------|--------|-----------------|
| `motilli` | Motilli Celery Juice Fiber Gummies | 1 hero image + research docs | Celery juice fiber gummies for GLP-1 users |
| `lunessa` | Lunessa Red Yeast Rice + CoQ10 | 1 hero image + research docs | Heart health supplement for women |
| `velantra-boat-tote` | Velantra Boat Tote | 14 images (8 colorways) | Canvas tote, gold hardware, Birkin-inspired |
| `velantra-meridian` | Velantra Meridian | 16 images (9 colorways) | Leather handbag, silver hardware |
| `velantra-weekender` | Velantra Weekender | 13 images (2 colorways) | Canvas + leather travel bag |

### Adding a New Brand

Edit the `BRAND_REGISTRY` dict in `ad_replicator.py` and add:
```python
"newbrand": {
    "research_docs": ["/path/to/doc1.md", "/path/to/doc2.docx"],
    "product_images": ["/path/to/hero-product.png"],
    "default_product_context": "One-line product description",
}
```

## Smart Product Inclusion

Stage 3 does NOT blindly inject the product image into every generation. It uses the Stage 1 analysis:

- If the reference contains a product → product reference IS included, Nano Banana is told to swap the product to match the brand's product exactly
- If the reference has NO product → product reference is NOT sent, and the prompt includes: "Do NOT add any product, bottle, package, or branded item"
- If the reference shows a competitor/villain product (negative context) → the product is replaced with a generic version, NOT the brand's product
- The prompt enforces 1:1 composition replication: "Replicate the composition 1:1 — do NOT invent or add elements that are not in the original"

## Output Structure

```
ad-replicator-output/
├── analysis/
│   └── ref_001_analysis.json     # Full Opus analysis + adaptation strategy
├── generated/
│   ├── ref_001_adapted_v001.png  # Nano Banana 2 adapted image
│   ├── ref_001_adapted_v002.png  # (if variations > 1)
│   └── ...
└── summary.md                    # Summary of all references processed
```

## Error Handling

- If Claude rate-limits, the pipeline backs off exponentially
- If Nano Banana fails on a generation, it retries up to 3 times before skipping
- All progress is saved incrementally — rerunning skips completed stages
- The pipeline prints a summary at the end showing which references succeeded/failed

## Higgsfield Mode

If the user says any of: `--use-higgsfield`, "use Higgsfield", "run this through Marketing Studio", "Higgsfield mode", **delegate to the `higgsfield-replicator` skill** instead of running this Nano Banana 2 pipeline. Higgsfield-replicator orchestrates the `higgsfield` CLI (`higgsfield generate create marketing_studio_image ...`) with native product-entity injection — faster + cheaper for one-click product image ads.

CLI is installed (`which higgsfield` should return a path). For raw, no-routing image gen, the official `higgsfield-product-photoshoot` and `higgsfield-generate` skills (installed at `~/.agents/skills/`) are the right primary path.

When to keep this skill (not delegate):
- The reference is a non-product native ad (no clean product swap path in Higgsfield)
- The user wants frame-perfect 1:1 visual replication of an unusual style Higgsfield can't reproduce
- The user explicitly says "don't use Higgsfield"
