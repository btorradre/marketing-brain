---
name: velantra-boat-tote
description: Product scale for the Velantra Boat Tote. Trained on 14+ colorways including canvas-and-leather two-tone variants (navy, red, pink, dark green, olive green, orange, sunny yellow, yellow, emerald green, lady pink, light grey, lineman) and fully solid-color variants (solid green, solid navy, solid olive green, solid orange, solid pink, solid red, solid yellow). Use this skill whenever running the ad-replicator, video-scene-replicator, or broll-sourcer for the Velantra Boat Tote specifically. Provides product-specific image references, visual identity, and product context so downstream skills generate accurate product representations from multiple angles.
disable-model-invocation: false
---

# Velantra Boat Tote — Product Scale

This skill is a product-specific configuration layer for the Velantra Boat Tote. It ensures that downstream creative generation skills (ad-replicator, video-scene-replicator, broll-sourcer) use the correct product images, visual identity, and product context for this specific product.

## Product Identity

**Product:** Velantra Boat Tote
**Category:** Premium canvas tote bag
**Brand:** Velantra
**Brand Key:** `velantra-boat-tote`

### Visual Description (⚠️ CORRECTED 2026-07-24 — Brooks caught a shipped ad with a nonexistent design; anchor EVERY generation on a `colors/<name>/` reference image, never on this text alone)

- **Silhouette:** soft structured tote, Birkin-inspired outline, SOFT slouchy canvas body with gentle pleats at the lower corners — NOT stiff/boxy
- **Body:** natural cream/ivory canvas INCLUDING the fold-over top edge — the top of the bag is ALWAYS cream. There is NO wide colored top section, NO colored yoke, NO colored leather upper band. A colored top yoke = invented product, regenerate on sight.
- **Trim (THIN straps only):** two slim colored top handles, ONE thin colored belt strap high across the front with a small gold turn lock at its center (plus two small gold keeper bars), TWO colored vertical straps running from the belt down the front to the base, colored trimmed bottom edge. White contrast stitching on all trim.
- **Hardware:** ONLY the small gold turn lock + the two small gold belt keepers. No Kelly-style clasp plates, no big V-straps with silver/gold plate tips, no corner patches, no feet visible in most shots.
- **Construction:** cream canvas + thin colored trim two-tone (Solid colorways are the exception: fully colored body).

### Available Colorways

**⛔ REFERENCE-IMAGE LAW (2026-07-24):** the CANONICAL generation refs are the `colors/<name>/07–13` shots in `brands/velantra/products/boat-tote/product-references/boat tote/colors/` — these are the LIVE product. The root-folder flats (`navy blue .webp`, `red.webp`, `sunny yellow .webp`, etc.) show a DIFFERENT, RETIRED design (chunky leather trim, wide colored top sections, all-colored bodies) that does not match the live product — NEVER use them as generation references. This mismatch shipped a wrong-product ad (VEL-POV-SHELF-01 v1) that Brooks caught.

**Two-tone (cream canvas body + thin colored trim) — live refs:**

| Colorway | Canonical ref | Notes |
|----------|------|-------|
| Navy | `colors/Navy/07.jpg` | Very dark navy trim, near-black |
| Red | `colors/Red/07.png` | Deep red trim |
| Sunny Yellow | `colors/Sunny Yellow/07.png` | Warm mustard-yellow trim |
| Emerald Green | `colors/Emerald Green/07.png` | Rich emerald trim |
| Lady Pink | `colors/Lady Pink/07.png` | Soft coral-pink trim |
| Light Grey | `colors/Light Grey/07.png` | Light grey trim |
| Lineman | `colors/Lineman/07.png` | Lineman colorway |

**Solid (fully colored body, no two-tone canvas):**

| Colorway | File |
|----------|------|
| Solid Green | `colors/Solid Green/07.png` |
| Solid Navy | `colors/Solid Navy/07.png` |
| Solid Olive Green | `colors/Solid Olive Green/07.png` |
| Solid Orange | `colors/Solid Orange/07.png` |
| Solid Pink | `colors/Solid Pink/07.png` |
| Solid Red | `colors/Solid Red/07.png` |
| Solid Yellow | `colors/Solid Yellow/07.png` |

Each `colors/<name>/` subfolder contains 7 multi-angle shots (`07.png`–`13.png`). The `colors/model-shots/` subfolder contains a model-carrying shot per colorway.

### Reference Images (multi-angle)

| File | Description |
|------|-------------|
| `01.jpg` | Front view — navy trim, gold clasp centered |
| `02.jpg` | Front view — red/crimson trim variant |
| `03.jpg` | Front view — pink/coral trim variant |
| `04.jpg` | Alternate angle or detail shot |
| `05.jpg` | Alternate angle or detail shot |
| `06.jpg` | Alternate angle or detail shot |

## Product Image Directory

(Path updated 2026-07-24 — the old `statics/product references/velantra/boat tote/` location is DEAD post vault-reorg.)

```
~/Documents/marketing brain/brands/velantra/products/boat-tote/
├── product-images/boat tote/
│   ├── 01.jpg – 06.jpg      # ⚠️ RETIRED design — do not use for generation
│   └── *.webp               # ⚠️ RETIRED design flats — do not use for generation
└── product-references/boat tote/colors/   # ✅ CANONICAL live-product refs
    ├── Emerald Green/       # 07.png – 13.png
    ├── Lady Pink/
    ├── Light Grey/
    ├── Lineman/
    ├── Navy/                # 07.jpg – 13.jpg
    ├── Red/
    ├── Solid Green/
    ├── Solid Navy/
    ├── Solid Olive Green/
    ├── Solid Orange/
    ├── Solid Pink/
    ├── Solid Red/
    ├── Solid Yellow/
    ├── Sunny Yellow/
    └── model-shots/         # one model-carrying shot per colorway
```

Registry loads the 6 JPG multi-angle shots + 8 original two-tone `.webp` flats + the canonical `07` shot from each of the 14 `colors/<name>/` subfolders. ⚠️ If a pipeline auto-loads the registry, verify it is not injecting the retired root flats/JPGs — for any generation, wire `colors/<name>/` shots explicitly.

## How to Use with Downstream Skills

### Ad Replicator (static image generation)

When the user wants to replicate a reference ad for the Velantra Boat Tote:

```bash
python3 ~/.claude/skills/ad-replicator/ad_replicator.py \
  --reference "/path/to/reference-ad.png" \
  --brand "velantra-boat-tote" \
  --output-dir "./ad-replicator-output"
```

The brand key `velantra-boat-tote` auto-loads all 14 product images from the registry. The pipeline's smart product inclusion logic will inject the right product references when scenes contain a bag/product.

### Video Scene Replicator (video creative generation)

When the user wants to replicate a reference video for the Velantra Boat Tote:

```bash
python3 ~/.claude/skills/video-scene-replicator/pipeline.py \
  --video "/path/to/reference.mp4" \
  --brand "velantra-boat-tote" \
  --output-dir "./replicator-output"
```

### B-Roll Sourcer

When sourcing B-roll for a Boat Tote video:

```bash
python3 ~/.claude/skills/broll-sourcer/broll_sourcer.py \
  --video "/path/to/video.mp4" \
  --brand "velantra-boat-tote" \
  --output-dir "./broll-output"
```

### Specific Color Override

To force a specific colorway (e.g., only navy), override the product images:

```bash
python3 ~/.claude/skills/ad-replicator/ad_replicator.py \
  --reference "/path/to/ref.png" \
  --brand "velantra-boat-tote" \
  --product-images "~/Documents/marketing brain/statics/product references/velantra/boat tote/navy blue .webp,~/Documents/marketing brain/statics/product references/velantra/boat tote/01.jpg" \
  --output-dir "./output"
```

## Integration Notes

- The brand key `velantra-boat-tote` is registered in all three pipeline scripts: `ad_replicator.py`, `pipeline.py`, and `broll_sourcer.py`
- All 14 images are loaded as product references — the pipelines' smart product inclusion logic determines which scenes need product injection
- The `default_product_context` is pre-set with the full visual description so AI models understand the product even without seeing every image
- To add research docs later, update the `research_docs` array in each pipeline's `BRAND_REGISTRY`
