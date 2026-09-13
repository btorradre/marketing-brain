---
name: lunessa
description: Product scale for Lunessa Red Yeast Rice + CoQ10 Gummies. Trained on product reference images (single bottle, triple bottles, gummy close-ups, lifestyle shots). Use this skill whenever running the ad-replicator, video-scene-replicator, or broll-sourcer for Lunessa specifically. Provides product-specific image references, visual identity, brand research docs, and product context so downstream skills generate accurate product representations.
disable-model-invocation: false
---

# Lunessa — Product Scale

This skill is a product-specific configuration layer for Lunessa. It ensures that downstream creative generation skills (ad-replicator, video-scene-replicator, broll-sourcer) use the correct product images, visual identity, brand research, and product context.

## Product Identity

**Product:** Lunessa Red Yeast Rice + CoQ10 Gummies
**Category:** Heart health supplement (gummies)
**Brand:** Lunessa
**Brand Key:** `lunessa`

### Visual Description

- **Container:** Clear plastic bottle, cylindrical, white screw-top lid
- **Label:** Deep burgundy/maroon background with white "Lunessa" wordmark at top (elegant serif font)
- **Sublabel:** "RED YEAST RICE + CoQ10" in large white text
- **Claims on label:** Checkmarks for "Cardiovascular", "Heart", "Cholesterol", "SUGAR FREE", "RASPBERRY FLAVOR"
- **Visual element on label:** Red yeast rice ingredient cluster at bottom of label
- **Gummies:** Red/ruby colored, visible through clear bottle
- **Overall palette:** Deep burgundy/maroon, white, red — warm clinical authority aesthetic
- **Count:** 60 vegan gummies per bottle

### Key Product Reference Images

| File | Description |
|------|-------------|
| `lunessa spelling corrected .jpg` | Hero product shot — single bottle, front-facing (PRIMARY) |
| `triple bottles.png` | Three bottles arranged — hero bundle shot |
| `lunessa bottles.png` | Multiple bottles arrangement |
| `single bottle .jpg` | Single bottle, clean shot |
| `hand with bottle transparent.png` | Hand holding bottle, transparent background |
| `gummy Medium.jpeg` | Individual gummy close-up |
| `gummy.jpeg` | Gummy close-up alternate |
| `gummy bear Background Removed.png` | Gummy with background removed |
| `gummies in hand (corrected).jpg` | Lifestyle — gummies in hand |
| `woman with gummies.jpg` | Lifestyle — woman holding gummies |
| `hero img Medium.jpeg` | Hero image, medium resolution |
| `hero img.jpeg` | Hero image |
| `removed bg.png` | Product with background removed |
| `spelling corrected 1-8` | Various spelling-corrected product/lifestyle shots |

### Product Image Directory

```
~/Documents/marketing brain/lunessa/website assets/
```

**Key product-specific images** (curated from 62 total files — many are lifestyle/mechanism graphics):
- `lunessa spelling corrected .jpg` — PRIMARY hero image (single bottle)
- `triple bottles.png` — bundle shot
- `lunessa bottles.png` — multiple bottles
- `single bottle .jpg` — clean single bottle
- `hand with bottle transparent.png` — bottle in hand
- `gummy Medium.jpeg`, `gummy.jpeg` — individual gummy
- `gummy bear Background Removed.png` — gummy cutout
- `hero img.jpeg`, `hero img Medium.jpeg` — hero compositions
- `removed bg.png` — product cutout

### Brand Research Docs

The brand registry auto-loads these research docs for brand knowledge injection:

| Doc | Location |
|-----|----------|
| `Lunessa Avatar Sheet.pdf` | `~/Documents/marketing brain/lunessa/fh research docs/Lunessa Research Docs 3.0/` |
| `Lunessa_Master_Copywriting_Brief.docx` | `~/Documents/marketing brain/lunessa/fh research docs/Lunessa Research Docs 3.0/` |
| `Lunessa_Master_Strategic_Brief.docx` | `~/Documents/marketing brain/lunessa/menopause research 2.0/` |

## How to Use with Downstream Skills

### Ad Replicator (static image generation)

```bash
python3 ~/.claude/skills/ad-replicator/ad_replicator.py \
  --reference "/path/to/reference-ad.png" \
  --brand "lunessa" \
  --output-dir "./ad-replicator-output"
```

### Video Scene Replicator (video creative generation)

```bash
python3 ~/.claude/skills/video-scene-replicator/pipeline.py \
  --video "/path/to/reference.mp4" \
  --brand "lunessa" \
  --output-dir "./replicator-output"
```

### B-Roll Sourcer

```bash
python3 ~/.claude/skills/broll-sourcer/broll_sourcer.py \
  --video "/path/to/video.mp4" \
  --brand "lunessa" \
  --output-dir "./broll-output"
```

## Integration Notes

- The brand key `lunessa` is registered in all three pipeline scripts with research docs + product images pre-configured
- The PRIMARY product reference image is `lunessa spelling corrected .jpg` — this is the hero shot used by default
- Research docs are auto-loaded (up to 30k chars) so AI models understand the avatar (women 35+ with heart health concerns), mechanism (red yeast rice + CoQ10), and voice
- Smart product inclusion logic detects supplement-related keywords in scene analysis to determine when to inject product refs
- The deep burgundy/maroon color palette is a key brand identifier — should be preserved in adaptations
