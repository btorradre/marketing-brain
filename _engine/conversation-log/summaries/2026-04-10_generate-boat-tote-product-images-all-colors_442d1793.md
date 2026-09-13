---
type: session-summary
date: 2026-04-10
session_id: local_b58ebf24-9e05-412e-bf88-442d179378ac
title: "Generate boat tote product images all colors"
category: creative-production
brands_discussed: [Velantra]
formats_worked: [static, product-image, native-image]
tags:
  - session-log
  - summary
  - creative-production
  - velantra
  - product-photography
  - nano-banana
  - gemini-api
  - boat-tote
---

# Generate boat tote product images all colors — Session Summary

**Date:** 2026-04-10
**Category:** creative-production
**Transcript:** [[conversation-log/transcripts/2026-04-10_generate-boat-tote-product-images-all-colors_442d1793]]

## What Happened
Used Gemini 2.5 Flash Image (Nano Banana) image-to-image to take 7 baseline Navy multi-angle shots of the Velantra boat tote and regenerate them across all 14 colorways — producing 98 product shots — then layered on 14 lifestyle model shots (woman over 50, outdoor setting). Spent the back half of the session iterating on stubborn color bleed and missing-hardware artifacts that the model kept producing on certain angles.

## Key Decisions Made
- Used `gemini-2.5-flash-image` via direct API rather than browser/Nano Banana UI — much faster batching.
- Split workflow into two-tone colors (cream canvas + colored trim) and solid colors (entire bag one color) for prompt accuracy.
- Lifestyle model shots: 1 per color, woman over 50, outdoor settings, used the front standing view (angle 12) as reference per color.
- When direct prompting failed to remove navy bleed, switched to a two-image reference approach (using clean color as a base + target color guidance) to crack the hardest cases.

## Insights & Learnings
- Gemini 2.5 Flash Image is genuinely capable for image-to-image color swaps on product photography but has predictable failure modes: it preserves dark trim as "important detail," loses small hardware (turn-lock clasps), and drifts toward orange when asked for saturated yellow.
- Two-image reference prompting (clean reference + target reference) is the unlock for stubborn edits. Single-image regen kept bleeding.
- Group/family shots are the hardest because the model treats each bag as semi-independent — bleed across multiple bags in the frame even when prompt is uniform.
- Solid Yellow specifically wants to drift orange — the workaround was to use clean Solid Orange as the base and swap orange → canary yellow, which preserved the form while forcing the new hue.

## Creative Output
- 98 multi-angle product shots: 14 colors × 7 angles, saved to `boat-tote-colors/{color}/07.png–13.png` inside the user's mounted Velantra folder.
- 14 lifestyle model shots: `boat-tote-colors/model-shots/`.
- Multiple touch-up regenerations on Solid Pink 10 & 11, Lady Pink 08, Lineman 08, Solid Olive Green 11, Solid Green 09 & 11, and the entire Solid Yellow folder.

## Action Items & Next Steps
- User flagged "still some issues with color consistency" at the end of the session — pending which images and what's off. Pick this up next session.
- Solid Yellow group shot (07) should be re-spot-checked — it required multiple passes to get uniform canary yellow across all bags in frame.
- Consider building a reusable batch script + reference-image library for future colorway expansions on other Velantra products.

## Notable Quotes / Language
- User: "For the lineman color that's its own color, there's no color on it. I don't want you to use Lady Pink." — clarification that Lineman is a tonal cream/ivory monochrome, not a hue.
- Workflow concept worth keeping: **two-image reference unlock** for stubborn color/material edits.

## Connections to Vault
- Brand: [[Velantra]] (boat tote product line)
- Related: prior session [[2026-04-08_generate-multi-angle-boat-tote_0be4bc92]] and [[2026-04-08_generate-product-images-weekender_1bed5471]]
- Could feed into [[native-image-factory]] skill if patterns from this workflow get codified (especially the two-image reference approach for color swaps).
