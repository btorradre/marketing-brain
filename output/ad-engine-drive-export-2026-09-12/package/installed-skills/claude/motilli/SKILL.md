---
name: motilli
description: Product scale for Motilli Celery Juice Fiber Gummies. Trained on product reference images (bottle, individual gummy, labels, lifestyle shots). Use this skill whenever running the ad-replicator, video-scene-replicator, or broll-sourcer for Motilli specifically. Provides product-specific image references, visual identity, brand research docs, and product context so downstream skills generate accurate product representations.
disable-model-invocation: false
---

# Motilli — Product Scale

This skill is a product-specific configuration layer for Motilli. It ensures that downstream creative generation skills (ad-replicator, video-scene-replicator, broll-sourcer) use the correct product images, visual identity, brand research, and product context.

## Product Identity

**Product:** Motilli Celery Juice Fiber Gummies
**Category:** Health supplement (gummies)
**Brand:** Motilli
**Brand Key:** `motilli`

### Visual Description

- **Container:** Clear plastic jar/bottle, cylindrical, white screw-top lid
- **Label:** Green/lime gradient background with white "motilli" wordmark at top
- **Sublabel:** "CELERY JUICE FIBER GUMMIES" in white text below brand name
- **Claims on label:** "Verified Clean", "5g" dosage callout, "GREEN APPLE" flavor
- **Gummies:** Dark green, heart-shaped, translucent/jewel-toned
- **Overall palette:** Green (lime to forest green), white, clean/clinical aesthetic
- **Count:** 60 gummies per bottle

### Key Product Reference Images

| File | Description |
|------|-------------|
| `motilli product reference.png` | Hero product shot — clear jar, green label, front-facing (PRIMARY) |
| `product reference.png` | Additional product reference |
| `gummy.png` | Single heart-shaped green gummy, close-up, transparent background |
| `label 1.png` | Label close-up |
| `label 2.jpg` | Label close-up alternate |
| `hand holding gummies.jpeg` | Lifestyle — hand holding gummies |
| `dr holding gummies .jpg` | Authority — doctor holding product |
| `gummies 2.jpeg` | Multiple gummies shot |
| `M.png` | Brand mark |
| `motilli-topaz-upscale-4x Medium.jpeg` | Upscaled product image |

### Product Image Directory

```
~/Documents/marketing brain/brands/motilli/brand/website-assets/
```

**HARDCODED PRIMARY product reference (used by ALL pipelines):**
```
/Users/brooksorradre2/Documents/marketing brain/brands/motilli/brand/website-assets/product reference.png
```
⚠️ Path corrected 2026-08-09. The old `brands/motilli/website assets/` (space, no
`brand/` parent) no longer exists; assets moved to `brand/website-assets/`. A second
copy of the hero shot also lives at `brand/product-references/`.
This path is the FIRST entry in every pipeline's BRAND_REGISTRY and will always be found before vault fallbacks.

**Key product-specific images** (not all 33 files are product shots — some are lifestyle, reviews, mechanism graphics):
- `product reference.png` — PRIMARY hero image (hardcoded absolute path in all pipelines)
- `motilli product reference.png` — secondary hero
- `gummy.png` — individual gummy
- `label 1.png`, `label 2.jpg` — label details
- `hand holding gummies.jpeg`, `gummies 2.jpeg` — product in-use
- `motilli-topaz-upscale-4x Medium.jpeg` — high-res upscale

### Brand Research Docs

The brand registry auto-loads these research docs for brand knowledge injection:

| Doc | Location |
|-----|----------|
| `Motilli_Master_Copywriting_Brief.md` | `~/Documents/marketing brain/motilli/` |
| `Motilli_Product_Context.md` | `~/Documents/marketing brain/motilli/` |
| `Motilli_Avatar_VoC.md` | `~/Documents/marketing brain/motilli/` |

## How to Use with Downstream Skills

### Ad Replicator (static image generation)

```bash
python3 ~/.claude/skills/ad-replicator/ad_replicator.py \
  --reference "/path/to/reference-ad.png" \
  --brand "motilli" \
  --output-dir "./ad-replicator-output"
```

### Video Scene Replicator (video creative generation)

```bash
python3 ~/.claude/skills/video-scene-replicator/pipeline.py \
  --video "/path/to/reference.mp4" \
  --brand "motilli" \
  --output-dir "./replicator-output"
```

### B-Roll Sourcer

```bash
python3 ~/.claude/skills/broll-sourcer/broll_sourcer.py \
  --video "/path/to/video.mp4" \
  --brand "motilli" \
  --output-dir "./broll-output"
```

## Integration Notes

- The brand key `motilli` is registered in all three pipeline scripts with research docs + product images pre-configured
- The PRIMARY product reference image is `motilli product reference.png` — this is the hero shot used by default
- Research docs are auto-loaded (up to 30k chars) so AI models understand the avatar (GLP-1 users), mechanism (celery juice fiber), and voice
- Smart product inclusion logic detects supplement-related keywords in scene analysis to determine when to inject product refs
