---
name: velantra-meridian
description: Product scale for the Velantra Meridian. Trained on 40 product reference images across 9+ colorways (black, brown, coffee brown, gray, white, green, burgundy, light blue, ultra light blue). Use this skill whenever running the ad-replicator, video-scene-replicator, or broll-sourcer for the Velantra Meridian specifically. Provides product-specific image references, visual identity, and product context so downstream skills generate accurate product representations from multiple angles.
disable-model-invocation: false
---

# Velantra Meridian — Product Scale

This skill is a product-specific configuration layer for the Velantra Meridian. It ensures that downstream creative generation skills (ad-replicator, video-scene-replicator, broll-sourcer) use the correct product images, visual identity, and product context for this specific product.

## Product Identity

**Product:** Velantra Meridian
**Category:** Structured leather handbag
**Brand:** Velantra
**Brand Key:** `velantra-meridian`

### Visual Description

- **Silhouette:** Birkin-inspired structured handbag, wider than tall, clean geometric lines
- **Body:** Full premium pebbled leather construction (single color throughout)
- **Hardware:** Silver/palladium turn-lock clasp, silver buckle accents, silver feet
- **Handles:** Two rigid top handles in matching leather
- **Closure:** Front flap with centered turn-lock mechanism
- **Strap:** Front belt strap connecting handles through flap
- **Construction:** Single-material leather. The entire bag is one color — no canvas, no two-tone.

### Available Colorways

| Colorway | Images | Notes |
|----------|--------|-------|
| Black | 9 images (black 1-9) | Classic black leather, silver hardware |
| Brown | 7 images (brown 1-7) | Warm tan/camel leather |
| Coffee Brown | 7 images (coffee brown 1-7) | Darker espresso-toned brown |
| Gray | 6 images (gray 1-6) | Cool medium gray leather |
| White | 5 images (white 1-5) | Clean white/cream leather |
| Green | 1 image | Deep emerald green |
| Burgundy | 1 image | Rich wine/burgundy |
| Light Blue | 2 images (JPG) | Soft powder blue |
| Ultra Light Blue | 1 image | Very pale icy blue |

### Key Reference Images (selected for coverage)

| File | Description |
|------|-------------|
| `black 1.webp` | Front view — black, silver hardware, classic angle |
| `black 2.webp` | Alternate angle — black |
| `black 3.webp` | Detail/different perspective — black |
| `brown 1.webp` | Front view — warm brown/camel leather |
| `brown 2.webp` | Alternate angle — brown |
| `coffee brow n1.webp` | Front view — dark coffee brown |
| `gray 1.webp` | Front view — gray |
| `white 1.webp` | Front view — white/cream |
| `green.webp` | Front view — emerald green |
| `burgundy 1.webp` | Front view — wine/burgundy |
| `light blue 1.jpg` | Front view — powder blue |
| `ultra light blue 1.webp` | Front view — icy pale blue |

## Product Image Directory

```
~/Documents/marketing brain/statics/product references/velantra/meridian/
```

**40 total images** (2 JPG + 38 WEBP across 9 colorways with multiple angles per color)

## How to Use with Downstream Skills

### Ad Replicator (static image generation)

```bash
python3 ~/.claude/skills/ad-replicator/ad_replicator.py \
  --reference "/path/to/reference-ad.png" \
  --brand "velantra-meridian" \
  --output-dir "./ad-replicator-output"
```

The brand key `velantra-meridian` auto-loads 16 representative product images from the registry (a curated subset covering all colorways). The pipeline's smart product inclusion logic handles when to inject product references.

### Video Scene Replicator (video creative generation)

```bash
python3 ~/.claude/skills/video-scene-replicator/pipeline.py \
  --video "/path/to/reference.mp4" \
  --brand "velantra-meridian" \
  --output-dir "./replicator-output"
```

### B-Roll Sourcer

```bash
python3 ~/.claude/skills/broll-sourcer/broll_sourcer.py \
  --video "/path/to/video.mp4" \
  --brand "velantra-meridian" \
  --output-dir "./broll-output"
```

### Specific Color Override

To force a specific colorway (e.g., only black):

```bash
python3 ~/.claude/skills/ad-replicator/ad_replicator.py \
  --reference "/path/to/ref.png" \
  --brand "velantra-meridian" \
  --product-images "~/Documents/marketing brain/statics/product references/velantra/meridian/black 1.webp,~/Documents/marketing brain/statics/product references/velantra/meridian/black 2.webp,~/Documents/marketing brain/statics/product references/velantra/meridian/black 3.webp" \
  --output-dir "./output"
```

## Integration Notes

- The brand key `velantra-meridian` is registered in all three pipeline scripts: `ad_replicator.py`, `pipeline.py`, and `broll_sourcer.py`
- 16 curated images are explicitly registered in the brand registry (covering all 9 colorways). The `product_images_dir` on video-scene-replicator can scan the full 40-image directory.
- The `default_product_context` is pre-set with the full visual description so AI models understand the product even without seeing every image
- This is a LEATHER bag (not canvas) — the key visual distinction from the Boat Tote and Weekender
- To add research docs later, update the `research_docs` array in each pipeline's `BRAND_REGISTRY`
