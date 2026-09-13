---
type: session-summary
date: 2026-03-21
session_id: local_4690ba4b-3e3c-4077-aa5c-d76b68d6b3c2
title: "Fix product image spelling errors"
category: creative-production
brands_discussed: [Lunessa]
formats_worked: [static]
tags:
  - session-log
  - summary
  - creative-production
  - product-images
  - image-generation
  - lunessa
  - cholesterol
  - gemini
  - nano-banana
---

# Fix product image spelling errors — Session Summary

**Date:** 2026-03-21
**Category:** creative-production
**Transcript:** [[conversation-log/transcripts/2026-03-21_fix-product-image-spelling-errors_d76b68d6]]

## What Happened
Fixed spelling errors on Lunessa product images (images 1, 8, and 9) where "RASPBERRY FLAVOR" was rendering as "FLOVOR" and checkmark text was garbled. After multiple failed attempts with Gemini flash model, switched to Google's nano-banana-pro-preview model which nailed the text rendering perfectly. Also had to regenerate as 1:1 aspect ratio after initially outputting landscape.

## Key Decisions Made
- Switched from Gemini flash to nano-banana-pro-preview for text-heavy image generation — dramatically better text rendering
- Generated from scratch rather than using reference images that contaminated output with original misspellings
- Used correctly-spelled bottle as reference design input for nano-banana

## Insights & Learnings
- **nano-banana-pro-preview is the go-to model for product images with text** — Gemini flash consistently reproduced spelling errors from reference images
- Generating without reference images avoids "contamination" from misspelled originals
- Always specify 1:1 aspect ratio explicitly — models default to landscape

## Creative Output
- 3 corrected Lunessa product images (1, 8, 9) at 1024x1024, all labels verified clean
- Images saved to "new product images" folder

## Action Items & Next Steps
- Use nano-banana-pro-preview as default for any future product image generation requiring text
- Verify remaining 7 product images (2-7, 10) don't need updates

## Notable Quotes / Language
None — production session.

## Connections to Vault
- Product images for Lunessa brand
- nano-banana model discovery applicable to future [[native-image-factory]] skill usage
