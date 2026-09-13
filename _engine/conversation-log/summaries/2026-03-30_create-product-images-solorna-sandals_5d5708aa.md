---
type: session-summary
date: 2026-03-30
session_id: local_e8fae75e-6c9c-4535-a3b4-5d5708aaaa44
title: "Create product images for Solorna sandals"
category: creative-production
brands_discussed: [Solorna, Tory Burch]
formats_worked: [native-image]
tags:
  - session-log
  - summary
  - creative-production
  - product-photography
  - img2img
  - gemini
  - sandals
  - fashion
  - tiktok
---

# Create product images for Solorna sandals — Session Summary

**Date:** 2026-03-30
**Category:** creative-production
**Transcript:** [[conversation-log/transcripts/2026-03-30_create-product-images-solorna-sandals_5d5708aa.md]]

## What Happened
Created img2img product photography prompts for Solorna sandals (sourced from TikTok) to be restyled in a Tory Burch luxury aesthetic using Gemini API. Went through multiple iterations — started with text-to-image (wrong approach), pivoted to img2img, separated prompts by color, added logo removal, switched from "restyle" to "generate new from reference," and finally converted everything to JSON format.

## Key Decisions Made
- Text-to-image was rejected in favor of img2img — the actual product photos need to be fed as reference so Gemini understands the exact sandal design
- Logo removal baked into every prompt — existing brand logos on chain hardware replaced with clean unbranded polished metal
- Prompts use "generate new from reference" framing instead of "restyle" to ensure Gemini creates fresh shots rather than modifying existing ones
- 4 perspectives per color: angle, side, detail, overhead — all in Tory Burch minimalist luxury style with pure white seamless backgrounds

## Insights & Learnings
- Gemini img2img works better when framed as "use this as a reference for the product's exact design, then generate a brand new..." rather than "restyle this image"
- Separating prompts by color (one file per color) makes the production workflow much easier for manual generation

## Creative Output
- 6 JSON prompt files (one per color) saved to `/Users/brooksorradre2/Documents/marketing brain/solorna/`:
  - prompts_beige.json, prompts_black.json, prompts_brown.json, prompts_coffee.json, prompts_khaki.json, prompts_skyblue.json
- 24 total prompts (6 colors x 4 perspectives)

## Action Items & Next Steps
- Generate the images using Gemini API with the provided API key and the source product photos from TikTok
- Consider automating the generation via n8n workflow if the manual process is too tedious

## Notable Quotes / Language
- None specific — this was a production-focused session

## Connections to Vault
- Related to [[native-image-factory]] skill workflow, though this was branded product photography, not native ads
- Solorna is a new brand entering the vault — first creative work for this product
