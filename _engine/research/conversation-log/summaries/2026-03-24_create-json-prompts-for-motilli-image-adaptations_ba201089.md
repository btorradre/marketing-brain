---
type: session-summary
date: 2026-03-24
session_id: local_183be588-a007-49cf-9038-ba2010896b9d
title: "Create JSON prompts for Motili image adaptations"
category: creative-production
brands_discussed: [Motilli, GLP-1 SOS]
formats_worked: [native-image, static, brief]
tags:
  - session-log
  - summary
  - creative-production
  - motilli
  - product-images
  - branded-statics
---

# Create JSON prompts for Motili image adaptations — Session Summary

**Date:** 2026-03-24
**Category:** creative-production
**Transcript:** [[conversation-log/transcripts/2026-03-24_create-json-prompts-for-motilli-image-adaptations_ba201089]]

## What Happened
Created 8 JSON image generation prompts for Motilli branded product statics, adapted from GLP-1 SOS reference images. Multiple rounds of revisions addressed color accuracy, ingredient correctness, layout overflow, guarantee duration, and Gemini watermark removal.

## Key Decisions Made
- Motilli accent color set to #A7D72F, background color to #8CC63F (not dark green)
- Ingredients wheel locked to 4 verified ingredients only: Celery Juice Extract, Chlorophyll, Green Apple, Prebiotic Fiber
- Guarantee is 90 days, not 60
- Gemini watermark sparkles are NOT design elements — must be excluded from all prompts

## Insights & Learnings
- When adapting product image prompts from reference images, verify actual product ingredients rather than guessing from label front. Dandelion Root and Inulin Fiber were incorrectly added.
- AI-generated image artifacts (like Gemini watermarks) can accidentally get replicated as "design elements" in prompts — always audit reference images for generation artifacts.
- Long text in grid layouts causes overflow — keep benefit claims under ~25 characters for clean rendering.

## Creative Output
- 8 Motilli product image JSON prompts saved to `/Users/brooksorradre2/Documents/Ecommerce/motilli/motilli_product_image_prompts.json`

## Action Items & Next Steps
- Verify Supplement Facts panel values against actual Motilli label before generating image 8
- Generate all 8 images through the native factory workflow
- Review generated outputs for quality

## Notable Quotes / Language
- "Feel Clean Guarantee" — guarantee branding for Motilli
- "Go green. Feel clean. Every day." — tagline for benefits layout

## Connections to Vault
- Used the [[native-image-factory]] skill
- Motilli brand assets being built for branded statics pipeline
