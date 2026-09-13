---
type: session-summary
date: 2026-03-28
session_id: local_e8fae75e-6c9c-4535-a3b4-5d5708aaaa44
title: "Create product images for Solorna sandals"
category: creative-production
brands_discussed: [Solorna, Tory Burch]
formats_worked: [native-image, product-images]
tags:
  - session-log
  - summary
  - creative-production
  - img2img
  - gemini
  - product-photography
  - solorna
  - tory-burch
  - sandals
  - tiktok
---

# Create product images for Solorna sandals — Session Summary

**Date:** 2026-03-28
**Category:** creative-production
**Transcript:** [[conversation-log/transcripts/2026-03-28_create-product-images-for-solorna-sandals_5d5708aa]]

## What Happened
Created img2img prompts for restyling TikTok product photos of Solorna sandals into a Tory Burch luxury aesthetic. Initially attempted to use the native image factory n8n workflow, but pivoted to manual Gemini API img2img prompts after realizing text-to-image wouldn't preserve the actual product design. Went through several iterations to get the prompts right — separating by color, adding logo removal, switching from "restyle" to "generate new from reference," and converting to JSON format.

## Key Decisions Made
- Abandoned the native image factory workflow for this task — it only supports text-to-image, not img2img
- Decided to create manual prompts for Brooks to run through Gemini API directly rather than building a new n8n workflow
- Used 4 shot perspectives per color: angle, side, detail, overhead
- Added explicit logo removal instructions (replace existing brand logos on chain hardware with clean unbranded polished metal)
- Reframed prompts from "restyle this existing photo" to "use this as a reference and generate a brand new image" for better Gemini output

## Insights & Learnings
- The native image factory n8n workflow is text-only and cannot handle img2img tasks — this is a capability gap worth noting for future product image work
- Gemini img2img works better when framed as "generate new using reference" rather than "transform/restyle this image"
- For product images that need to match a real physical product, img2img with reference photos is essential — text-to-image can't accurately reproduce specific product designs

## Creative Output
- 6 JSON prompt files (one per color) saved to `/solorna/` folder:
  - prompts_beige.json, prompts_black.json, prompts_brown.json, prompts_coffee.json, prompts_khaki.json, prompts_skyblue.json
- Each file contains 4 prompts (angle, side, detail, overhead) with prompt_id, shot type, full prompt text, and aspect_ratio
- Total: 24 production-ready img2img prompts

## Action Items & Next Steps
- Brooks to run the 24 prompts through Gemini API with corresponding TikTok source photos
- Review generated images and iterate on prompts if needed
- Consider building a dedicated img2img n8n workflow for future product image restyling tasks

## Notable Quotes / Language
- Prompt engineering pattern: "Using this image as a reference for the product's exact design, materials, shape, and color, generate a brand new..."
- Logo removal instruction: "Remove any existing brand logos or text from the chain hardware and replace with clean, unbranded polished gold metal"

## Connections to Vault
- Related to [[solorna]] brand folder in vault
- The native-image-factory skill was NOT used (wrong tool for img2img) — potential skill update to note this limitation
- Product image prompts follow Tory Burch luxury aesthetic — could be templated for future brand restyling work
