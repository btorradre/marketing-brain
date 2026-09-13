---
name: broll-auditor
description: >
  Post-generation QA auditor for B-roll assets. Compares every generated image/video
  against its reference frame and product reference images to catch hallucination,
  text-to-image fallbacks, wrong products, invented elements, and brand drift.
  Run this after video-scene-replicator, ad-replicator, or broll-sourcer.
user_invocable: true
---

# B-Roll Auditor

## Purpose

Quality-gate skill that audits generated B-roll assets AFTER any generation pipeline
(video-scene-replicator, ad-replicator, broll-sourcer, animated-video-replicator) has run.
Catches the most common and costly generation failures before assets reach the editor.

## What It Catches

| Failure Type | Detection Method | Severity |
|---|---|---|
| **Text-to-image fallback** | No structural similarity to reference frame — composition, layout, perspective all differ | CRITICAL |
| **Scene mismatch** | Generated scene depicts a fundamentally different subject, setting, or action than the reference frame — e.g., reference shows a kitchen scene but generated shows a park, or reference shows someone drinking but generated shows someone exercising | CRITICAL |
| **Failed adaptation** | Scene still visually belongs to the competitor/reference brand instead of being transformed for ours — competitor product still visible, competitor color scheme retained, competitor logo/text/branding not replaced, or scene was passed through unchanged | CRITICAL |
| **Product hallucination** | Generated product doesn't match any registered product reference image (wrong shape, color, label, hardware) | CRITICAL |
| **Invented elements** | Objects, people, products, or text appear that weren't in the reference frame | HIGH |
| **Missing product** | Scene was flagged for product inclusion but product is absent or barely visible | HIGH |
| **Wrong colorway/variant** | Product is recognizable but wrong color, wrong trim, wrong label variant | MEDIUM |
| **Text hallucination** | AI-generated text on labels, bottles, bags that doesn't match the real product | CRITICAL |
| **Brand drift** | Color palette, lighting mood, or visual style deviates significantly from reference | MEDIUM |
| **Overlay contamination** | Talking head or background leaked into what should be a standalone overlay asset | HIGH |

## Required Inputs

1. **Generated assets directory** — Path to folder containing the generated B-roll (images and/or videos)
2. **Reference frames directory** — Path to the extracted keyframes/reference frames used as input to generation
3. **Brand name** — Which product skill to load for reference images (e.g., `motilli`, `lunessa`, `velantra-meridian`, `velantra-boat-tote`, `velantra-weekender`)
4. **Pipeline source** (optional) — Which pipeline generated these (`video-scene-replicator`, `ad-replicator`, `broll-sourcer`). If omitted, auditor infers from directory structure.

## Usage

```
/broll-auditor <generated_assets_path> --refs <reference_frames_path> --brand <brand_name>
```

### Examples

```bash
# Audit video-scene-replicator output for Motilli
/broll-auditor /Users/brooksorradre2/Documents/marketing\ brain/brands/motilli/videos/PB-01/generated --refs /Users/brooksorradre2/Documents/marketing\ brain/brands/motilli/videos/PB-01/keyframes --brand motilli

# Audit ad-replicator output for Velantra Meridian
/broll-auditor ~/outputs/ad-replicator/meridian-batch --refs ~/outputs/ad-replicator/meridian-batch/references --brand velantra-meridian

# Audit with explicit pipeline source
/broll-auditor ./generated --refs ./keyframes --brand lunessa --pipeline broll-sourcer
```

## Audit Pipeline

### Stage 1: Asset Discovery & Pairing

Scan the generated assets directory for all images (.png, .jpg, .webp) and videos (.mp4).
Scan the reference frames directory for corresponding reference frames.

**Pairing logic:**
- Match by filename stem (e.g., `scene_03_generated.png` ↔ `scene_03.png`)
- Match by numeric index if naming conventions differ
- Flag any generated asset with NO matching reference as `UNPAIRED` (likely text-to-image)

### Stage 2: Load Product References

Based on `--brand`, load the product reference images from the product skill's registry:

| Brand | Product Image Directory |
|---|---|
| `motilli` | `~/Documents/marketing brain/brands/motilli/website assets/` |
| `lunessa` | `~/Documents/marketing brain/lunessa/website assets/` |
| `velantra-meridian` | `~/Documents/marketing brain/statics/product references/velantra/meridian/` |
| `velantra-boat-tote` | `~/Documents/marketing brain/statics/product references/velantra/boat tote/` |
| `velantra-weekender` | `~/Documents/marketing brain/statics/product references/velantra/weekender/` |

Load the **primary product reference image** and up to 4 additional angle/variant references.

Also load the product's `default_product_context` visual description from the product skill for textual grounding.

### Stage 3: Per-Asset Audit via Gemini Vision

For EACH generated asset, send a multi-image prompt to **Gemini 2.5 Flash** (`gemini-2.5-flash-preview-05-20`) with:

**Images provided:**
1. The generated asset (image, or first frame if video)
2. The paired reference frame (if found)
3. The primary product reference image
4. 1-2 additional product reference angles (if product scene)

**Audit prompt:**

```
You are a strict QA auditor for AI-generated advertising B-roll. Your job is to compare
a generated image against its reference frame and product reference images to catch
any generation failures.

## Images Provided
- IMAGE 1: The GENERATED asset (this is what the AI produced)
- IMAGE 2: The REFERENCE FRAME (this is what the AI was supposed to use as its base for image-to-image generation)
- IMAGE 3+: PRODUCT REFERENCE photos (this is what the real product looks like)

## Product Visual Description
{product_visual_description}

## Audit Checklist — Score each item PASS, WARN, or FAIL:

### 1. IMAGE-TO-IMAGE FIDELITY
Compare the generated asset to the reference frame:
- Does the generated image preserve the same composition/layout as the reference?
- Does it preserve the same camera angle and perspective?
- Does it preserve the same general scene structure (foreground/background arrangement)?
- If ALL of these differ, this is likely a TEXT-TO-IMAGE generation (not image-to-image). Score: FAIL.
- If most are preserved with stylistic changes, score: PASS.

### 2. SCENE MATCH
Compare WHAT is happening in the generated image vs the reference frame:
- Does the generated image depict the SAME subject matter as the reference? (same type of scene — kitchen vs kitchen, person drinking vs person drinking, product close-up vs product close-up)
- Does it show the SAME action or activity? (if reference shows someone pouring a drink, generated should also show someone pouring a drink — not a completely different activity)
- Does it preserve the SAME setting/environment? (indoor vs outdoor, kitchen vs bathroom, studio vs lifestyle)
- Does it preserve the SAME framing type? (close-up vs wide shot, overhead vs eye-level, product-only vs product-in-use)
- A scene that passes i2i fidelity (same layout) but depicts a COMPLETELY DIFFERENT subject is still a FAIL here. The AI sometimes preserves composition but swaps the entire subject.
- Score FAIL if the scene subject, action, or setting is fundamentally different from reference.
- Score WARN if the scene is recognizably similar but with notable drift (e.g., slightly different activity, changed environment details).
- Score PASS if scene content clearly matches the reference.

### 3. BRAND ADAPTATION
Verify the scene was actually ADAPTED for our brand and not left as the competitor's:
- Does the generated image still show the COMPETITOR's product instead of ours? (e.g., reference had a competitor's supplement bottle — generated should show OUR brand's bottle, not theirs)
- Does the generated image still retain the COMPETITOR's color scheme, aesthetic, or visual identity? (e.g., if reference brand uses blue/white and ours uses green/gold, the generated scene should reflect OUR palette)
- Is there any residual competitor branding? (logos, text, watermarks, URL slugs, social handles that belong to the reference brand)
- Was the scene passed through UNCHANGED? (identical or near-identical to the reference with no adaptation at all — this means the i2i prompt failed to transform anything)
- Does the adapted scene feel like it belongs to OUR brand? (check against product reference images — does the visual world match?)
- Score FAIL if competitor product/branding is still visible, or if the scene is essentially unchanged from reference.
- Score WARN if adaptation is partial (some competitor elements remain, or brand fit is weak).
- Score PASS if the scene has been clearly and fully adapted — our product, our aesthetic, no competitor residue.

### 4. PRODUCT ACCURACY (only if a product appears in the generated image)
Compare any product in the generated image against the product reference photos:
- Does the product shape match? (bottle shape, bag silhouette, gummy shape)
- Does the label/branding match? (correct text, correct colors, correct logo placement)
- Does the color match? (correct colorway — check against reference photos)
- Does the hardware/detail match? (correct clasps, zippers, caps, lids)
- Any hallucinated text on the product? (invented brand names, gibberish text, wrong spelling)
- Score FAIL if the product is clearly wrong or hallucinated. Score WARN if minor drift.

### 5. INVENTED ELEMENTS
Compare the generated image to the reference frame:
- Are there any objects, people, products, or text that appear in the generated image
  but were NOT in the reference frame?
- Pay special attention to: products appearing in non-product scenes, text/watermarks
  that weren't in the reference, extra people or hands.
- Score FAIL if significant invented elements. Score WARN if minor additions.

### 6. OVERLAY CONTAMINATION (only for overlay/graphic assets)
- Does this image contain a talking head, person's face, or video background that
  should NOT be there?
- Overlay assets must be STANDALONE — isolated graphics, diagrams, or product shots
  with NO talking head bleed-through.
- Score FAIL if contaminated. Score PASS if clean standalone.

### 7. BRAND CONSISTENCY
- Does the overall color palette feel consistent with the brand?
- Is the lighting mood appropriate?
- Does the visual quality meet advertising standards (no artifacts, no distortion)?
- Score WARN if drift detected. Score FAIL only if egregiously off-brand.

## Output Format (respond in EXACTLY this JSON):
{
  "asset_name": "<filename>",
  "overall_verdict": "PASS" | "WARN" | "FAIL",
  "i2i_fidelity": {
    "score": "PASS" | "WARN" | "FAIL",
    "confidence": 0.0-1.0,
    "notes": "<specific observations>"
  },
  "scene_match": {
    "score": "PASS" | "WARN" | "FAIL",
    "reference_depicts": "<brief description of what the reference frame shows>",
    "generated_depicts": "<brief description of what the generated image shows>",
    "confidence": 0.0-1.0,
    "notes": "<specific observations about scene content match/mismatch>"
  },
  "brand_adaptation": {
    "score": "PASS" | "WARN" | "FAIL",
    "competitor_residue_found": true/false,
    "adaptation_applied": true/false,
    "residue_details": ["<list any competitor branding, products, colors, logos, text still visible>"],
    "confidence": 0.0-1.0,
    "notes": "<specific observations about whether scene was properly adapted for our brand>"
  },
  "product_accuracy": {
    "score": "PASS" | "WARN" | "FAIL" | "N/A",
    "has_product": true/false,
    "confidence": 0.0-1.0,
    "notes": "<specific observations about product match/mismatch>"
  },
  "invented_elements": {
    "score": "PASS" | "WARN" | "FAIL",
    "elements_found": ["<list any invented elements>"],
    "notes": "<details>"
  },
  "overlay_contamination": {
    "score": "PASS" | "WARN" | "FAIL" | "N/A",
    "notes": "<details>"
  },
  "brand_consistency": {
    "score": "PASS" | "WARN" | "FAIL",
    "notes": "<details>"
  },
  "recommendation": "APPROVE" | "REGENERATE" | "MANUAL_REVIEW",
  "regeneration_notes": "<if REGENERATE, explain exactly what went wrong and what to fix>"
}
```

### Stage 4: Video Frame Sampling (for .mp4 assets)

For video assets, extract 3 frames (first, middle, last) and audit each.
If ANY frame fails, the video fails.

Use ffmpeg to extract frames:
```bash
ffmpeg -i <video> -vf "select=eq(n\\,0)+eq(n\\,{mid})+eq(n\\,{last})" -vsync vfill -frames:v 3 frame_%d.png
```

### Stage 5: Aggregate & Report

After auditing all assets, generate a markdown report:

```markdown
# B-Roll Audit Report
**Brand:** {brand}
**Pipeline:** {pipeline}
**Date:** {date}
**Assets Audited:** {total}

## Summary
- PASS: {count} ({pct}%)
- WARN: {count} ({pct}%)
- FAIL: {count} ({pct}%)
- UNPAIRED (no reference): {count}

## Critical Failures
{table of all FAIL assets with failure type and notes}

## Warnings
{table of all WARN assets with warning type and notes}

## Passed Assets
{list of passed asset names}

## Regeneration Queue
{list of assets that need regeneration with specific instructions for each}
```

Save report to: `{generated_assets_path}/audit_report.md`

### Stage 6: Regeneration Manifest (if failures found)

If any assets scored FAIL, generate a `regeneration_manifest.json`:

```json
{
  "brand": "motilli",
  "pipeline": "video-scene-replicator",
  "failures": [
    {
      "asset": "scene_03_generated.png",
      "reference": "scene_03.png",
      "failure_types": ["text_to_image_fallback", "scene_mismatch", "failed_adaptation", "product_hallucination"],
      "regeneration_instructions": "Must use image-to-image with scene_03.png as base. Scene depicts a park instead of the kitchen shown in reference. Competitor product still visible — needs full brand adaptation. Product bottle shape is wrong — use product reference.png as additional input.",
      "priority": "critical"
    }
  ]
}
```

Save to: `{generated_assets_path}/regeneration_manifest.json`

## Hard Rules

1. **EVERY generated asset gets audited.** No skipping, no sampling.
2. **Unpaired assets are automatic FAIL.** If there's no reference frame, the pipeline used text-to-image.
3. **Scene must match reference content.** If the reference shows a kitchen and the generated shows a park, that's a FAIL regardless of composition fidelity.
4. **Adaptation must be complete.** If a competitor's product, logo, color scheme, or branding is still visible, the scene was not properly adapted. Automatic FAIL.
5. **An unchanged scene is a failed adaptation.** If the generated image is near-identical to the reference with no brand transformation applied, the i2i prompt failed to adapt. FAIL.
6. **Product hallucination is CRITICAL.** A wrong product is worse than no product.
7. **Text on products is the #1 hallucination vector.** Scrutinize ALL text on labels, bottles, bags.
8. **Use the REAL product references, not memory.** Always load actual image files for comparison.
9. **Videos get multi-frame audit.** Don't just check the first frame.
10. **Report goes in the same directory as the generated assets.** Easy for the editor to find.

## Gemini Configuration

- **Model:** `gemini-2.5-flash-preview-05-20`
- **Temperature:** 0.1 (strict, consistent judgments)
- **Max tokens:** 2048 per asset audit
- **Rate limit:** Process assets sequentially to avoid quota issues

## API Call Structure

```python
import google.generativeai as genai
from PIL import Image

model = genai.GenerativeModel("gemini-2.5-flash-preview-05-20")

# Load images
generated = Image.open(generated_path)
reference = Image.open(reference_path)
product_ref = Image.open(product_ref_path)

response = model.generate_content(
    [audit_prompt, generated, reference, product_ref],
    generation_config=genai.GenerationConfig(
        temperature=0.1,
        max_output_tokens=2048,
        response_mime_type="application/json"
    )
)
```

## Integration with Existing Pipelines

This skill is designed to run AFTER generation, not during. Typical workflow:

```
1. /video-scene-replicator <reference_video> --brand motilli
   → generates B-roll to /videos/PB-01/generated/
   → extracts keyframes to /videos/PB-01/keyframes/

2. /broll-auditor /videos/PB-01/generated --refs /videos/PB-01/keyframes --brand motilli
   → audits every generated asset
   → produces audit_report.md + regeneration_manifest.json

3. Review audit report → re-run failed assets or proceed to editing
```

## Output Files

| File | Location | Purpose |
|---|---|---|
| `audit_report.md` | `{generated_assets_path}/` | Human-readable audit summary |
| `regeneration_manifest.json` | `{generated_assets_path}/` | Machine-readable failure list for re-generation |
| `audit_frames/` | `{generated_assets_path}/audit_frames/` | Extracted video frames used during audit (cleanup after) |
