---
type: session-summary
date: 2026-04-06
session_id: local_755b4e99-9038-456e-bc2c-7105ed679e8f
title: "Generate product image prompts for tote"
category: creative-production
brands_discussed: [Velantra]
formats_worked: [native-image]
tags:
  - session-log
  - summary
  - creative-production
  - velantra
  - boat-tote
  - image-prompts
  - product-photography
  - json
  - all-colorways
---

# Generate product image prompts for tote — Session Summary

**Date:** 2026-04-06
**Category:** creative-production
**Transcript:** [[conversation-log/transcripts/2026-04-06_generate-product-image-prompts-tote_7105ed67]]

## What Happened
Created 62 AI image generation prompts for the Velantra Boat Tote across all 14 color variations and 5 reference photo concepts. Prompts include specific bag construction details for accurate rendering. Delivered in both markdown and structured JSON format, organized by color.

## Key Decisions Made
- 5 concepts adapted from existing product page reference photos
- Concept 4 (shelf grid display) gets curated color groupings instead of individual prompts
- Lineman variant confirmed as all-neutral with brass hardware and no colored trim
- JSON organized by color (not concept) for easier batch processing per colorway

## Creative Output
- 62 prompts total in markdown format
- Structured JSON with metadata (id, concept, color, color_type, limited_edition, prompt)
- Output in `Ecommerce/velantra/products/boat tote/`

## Action Items & Next Steps
- Run prompts through image generation tool (Midjourney, DALL-E, or similar)
- Review generated images and iterate on prompts that don't render the tote accurately
- Consider creating similar prompt sets for other Velantra products

## Connections to Vault
- Connects to Velantra product catalog
- Could inform future [[skills/native-image-factory]] updates with product-specific prompt patterns
