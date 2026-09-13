# B-Roll Auditor

This document describes a quality-gate process for auditing AI-generated B-roll assets (images and videos) after any image-to-image or video generation pipeline has run. It compares every generated asset against (1) the reference frame it was supposed to be based on, and (2) real product reference photos, to catch the most common and costly generation failures before the assets reach an editor. Use this immediately after any pipeline that generates B-roll via image-to-image or video generation for an ad — before those assets are handed off for editing.

## What it catches

| Failure type | How to detect it | Severity |
|---|---|---|
| **Text-to-image fallback** | No structural similarity to the reference frame — composition, layout, and perspective all differ, suggesting the generator ignored the reference image entirely and generated from the text prompt alone | Critical |
| **Scene mismatch** | The generated scene depicts a fundamentally different subject, setting, or action than the reference frame — e.g. reference shows a kitchen scene but generated shows a park, or reference shows someone drinking but generated shows someone exercising | Critical |
| **Failed adaptation** | The scene still visually belongs to the competitor/reference brand instead of being transformed for the target brand — competitor product still visible, competitor color scheme retained, competitor logo/text not replaced, or the scene passed through essentially unchanged | Critical |
| **Product hallucination** | The generated product doesn't match any registered product reference image (wrong shape, color, label, hardware) | Critical |
| **Invented elements** | Objects, people, products, or text appear that weren't present in the reference frame | High |
| **Missing product** | A scene flagged for product inclusion is missing the product, or it's barely visible | High |
| **Wrong colorway/variant** | The product is recognizable but the wrong color, trim, or label variant | Medium |
| **Text hallucination** | AI-generated text on labels, bottles, or bags that doesn't match the real product | Critical |
| **Brand drift** | Color palette, lighting mood, or visual style deviates significantly from the brand's established look | Medium |
| **Overlay contamination** | A talking head or background has leaked into what should be a standalone overlay/graphic asset | High |

## How to use this

### Required inputs

1. **Generated assets** — the folder of generated B-roll (images and/or videos) to audit.
2. **Reference frames** — the folder of extracted keyframes/reference frames that were used as the input for generation.
3. **Brand product references** — a set of real product reference photos (multiple angles/colorways where relevant) for the brand this batch was generated for, plus a short written description of the product's actual visual truth (shape, materials, color, label text) to ground the audit.
4. **Pipeline source** (optional) — which pipeline/process generated these assets, for context in the report.

### Stage 1 — Discover and pair assets

Scan the generated-assets folder for all images and videos. Scan the reference-frames folder for the corresponding reference frame for each.

**Pairing logic:**
- Match by filename (e.g. `scene_03_generated.png` pairs with `scene_03.png`).
- Fall back to matching by numeric index if naming conventions differ.
- Any generated asset with **no matching reference** should be flagged `UNPAIRED` — this is a strong signal that generation fell back to text-to-image with no real reference input.

### Stage 2 — Load product references

Load the primary product reference image plus up to 4 additional angle/variant reference images for the brand in question, along with a short written visual-truth description of the product (grounding text: shape, materials, color, distinguishing details).

### Stage 3 — Per-asset audit against a checklist

For each generated asset, compare it side-by-side against: (1) its paired reference frame, and (2) the product reference photos. Use a capable multimodal vision model for this comparison — feed it all the relevant images plus the checklist below, and have it return a structured verdict. Score every item **PASS**, **WARN**, or **FAIL**, with a written note explaining the score.

**The audit checklist, item by item:**

**1. Image-to-image fidelity.** Compare the generated asset to the reference frame: does it preserve the same composition/layout, the same camera angle and perspective, and the same general scene structure (foreground/background arrangement)? If all of these differ, this is likely a text-to-image generation rather than a true image-to-image transformation — score FAIL. If most are preserved with only stylistic changes, score PASS.

**2. Scene match.** Compare *what is happening* in the generated image versus the reference frame — not just the layout, but the actual subject matter: same type of scene (kitchen vs. kitchen), same action or activity (pouring a drink vs. pouring a drink, not a completely different activity), same setting/environment (indoor vs. outdoor, kitchen vs. bathroom), same framing type (close-up vs. wide, overhead vs. eye-level, product-only vs. product-in-use). A scene that passes fidelity (same layout) but shows a completely different subject is still a FAIL here — generators sometimes preserve composition while swapping the entire subject out. FAIL if the subject, action, or setting is fundamentally different. WARN if recognizably similar but with notable drift. PASS if scene content clearly matches.

**3. Brand adaptation.** Verify the scene was actually adapted for the target brand and not left as the original reference/competitor brand's: does it still show the competitor's product instead of the target brand's? Does it retain the competitor's color scheme or visual identity? Is there any residual competitor branding — logos, text, watermarks, handles? Was the scene passed through essentially unchanged, meaning the transformation prompt failed to do anything? Does the adapted scene actually feel like it belongs to the target brand, checked against the product reference images? FAIL if competitor product/branding is still visible, or the scene is essentially unchanged. WARN if adaptation is partial. PASS if fully and clearly adapted with no competitor residue.

**4. Product accuracy** (only relevant if a product appears in the generated image). Compare against the real product reference photos: does the shape match (bottle shape, bag silhouette, product shape)? Does the label/branding match (correct text, colors, logo placement)? Does the color match the correct colorway? Do hardware/details match (clasps, zippers, caps, lids)? Is there any hallucinated text on the product (invented names, gibberish, misspellings)? FAIL if the product is clearly wrong or hallucinated; WARN for minor drift.

**5. Invented elements.** Compare against the reference frame: are there any objects, people, products, or text present in the generated image that were NOT in the reference frame? Pay particular attention to products appearing in scenes that shouldn't have them, text/watermarks that weren't in the reference, or extra people/hands. FAIL for significant invented elements; WARN for minor additions.

**6. Overlay contamination** (only relevant for overlay/graphic-only assets). Does the image contain a talking head, a person's face, or a video background that should not be there? Overlay assets must be fully standalone — isolated graphics, diagrams, or product shots with zero talking-head bleed-through. FAIL if contaminated, PASS if clean.

**7. Brand consistency.** Does the overall color palette feel consistent with the brand? Is the lighting mood appropriate? Does the visual quality meet advertising standards (no artifacts, no distortion)? WARN if drift is detected; FAIL only if egregiously off-brand.

**Output structure for each asset audit** — record, for each of the 7 checklist items above: the score (PASS/WARN/FAIL), a confidence level, and a specific written note. Roll these up into one **overall verdict** (PASS/WARN/FAIL) per asset, and a final **recommendation**: APPROVE, REGENERATE, or MANUAL_REVIEW. If the recommendation is REGENERATE, write specific regeneration notes explaining exactly what went wrong and what needs to change.

### Stage 4 — Video assets get multi-frame audits

For any video asset, extract at least 3 frames (first, middle, last) and run the full checklist above on each frame independently. **If any single frame fails, the whole video fails.** Do not audit only the first frame of a video.

### Stage 5 — Aggregate and report

After auditing every asset, produce a written report covering:

- **Summary**: total assets audited, and counts/percentages of PASS, WARN, FAIL, and UNPAIRED.
- **Critical failures**: a table of every FAIL asset with its failure type(s) and notes.
- **Warnings**: a table of every WARN asset with its warning type(s) and notes.
- **Passed assets**: a simple list.
- **Regeneration queue**: a list of every asset that needs to be regenerated, with specific instructions for each.

Save this report alongside the generated assets so it's easy for whoever picks up the work next to find.

### Stage 6 — Regeneration manifest for failures

If any assets scored FAIL, produce a separate structured list of failures for downstream regeneration, one entry per failed asset, containing: the asset name, its paired reference (if any), the specific failure type(s) (e.g. text_to_image_fallback, scene_mismatch, failed_adaptation, product_hallucination), detailed regeneration instructions (e.g. "Must use image-to-image with the correct reference frame as the base. Scene depicts the wrong setting compared to reference. Competitor product still visible — needs full brand adaptation. Product shape is wrong — use the correct product reference as an additional input."), and a priority level.

## Hard rules

1. **Every generated asset gets audited. No skipping, no sampling.**
2. **Unpaired assets are an automatic FAIL.** No reference frame available strongly suggests text-to-image was used instead of true image-to-image.
3. **Scene must match reference content.** If the reference shows one setting and the generated output shows a different one, that's a FAIL regardless of how well the composition otherwise matches.
4. **Adaptation must be complete.** Any visible competitor product, logo, color scheme, or branding remaining is an automatic FAIL.
5. **An unchanged scene is a failed adaptation.** If the generated image is near-identical to the reference with no brand transformation applied, the transformation step failed — FAIL.
6. **Product hallucination is critical.** A wrong product on screen is worse than no product at all.
7. **Text on products is the single biggest hallucination risk.** Scrutinize all text on labels, bottles, and bags closely.
8. **Compare against real product reference images, never from memory.** Always load the actual reference image files for every comparison.
9. **Videos get a multi-frame audit, not just a first-frame check.**
10. **Keep the audit report and regeneration list next to the generated assets** so an editor or the next step in the pipeline can find them easily.

## Suggested settings for the vision-model audit pass

- Use a low temperature setting (e.g. ~0.1) for strict, consistent judgments rather than creative ones.
- Process assets one at a time (sequentially) rather than in parallel, to avoid rate-limit issues and to keep judgments independent.

## Where this fits in a pipeline

This runs strictly **after** generation, never during. Typical flow:

1. Run whatever generation pipeline produces the B-roll (e.g. a video-scene-replication or ad-replication pipeline) — it outputs generated assets plus the reference keyframes it used.
2. Run this audit against those two folders plus the brand's product references — it produces an audit report and, if needed, a regeneration list.
3. Review the audit report, regenerate anything flagged, and only then hand the assets off to editing.
