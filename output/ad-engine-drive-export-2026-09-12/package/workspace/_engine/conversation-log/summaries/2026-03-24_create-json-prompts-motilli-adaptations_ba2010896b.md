---
type: session-summary
date: 2026-03-24
session_id: local_183be588-a007-49cf-9038-ba2010896b9d
title: "Create JSON prompts for Motili image adaptations"
category: creative-production
brands_discussed: [Motilli, GLP-1 SOS]
formats_worked: [native-image, static]
tags:
  - session-log
  - summary
  - creative-production
  - branded-statics
  - product-images
  - GLP-1
  - motilli
  - gemini
  - color-system
---

# Create JSON prompts for Motilli image adaptations — Session Summary

**Date:** 2026-03-24
**Category:** creative-production
**Transcript:** [[conversation-log/transcripts/2026-03-24_create-json-prompts-motilli-adaptations_ba2010896b.md]]

## What Happened
Adapted 8 branded product image concepts from a GLP-1 SOS competitor reference into Motilli-specific prompts. Iteratively refined color system, removed Gemini watermark artifacts, fixed ingredient accuracy, resolved text overflow in comparison chart, and updated the guarantee from 60 to 90 days.

## Key Decisions Made
- Accent color set to `#A7D72F` (bright lime-green for highlights, checkmarks, bars)
- Background color changed from dark green `#1B3A2D` to `#8CC63F` (lime green) across images 1, 2, 5, and 6
- Ingredients wheel reduced to 4 actual ingredients: Celery Juice Extract, Chlorophyll, Green Apple, Prebiotic Fiber — removed fabricated Dandelion Root and Inulin Fiber
- Comparison chart claim shortened from "NO ARTIFICIAL COLORS OR FLAVORS" to "NO ARTIFICIAL INGREDIENTS" to prevent text overflow
- Guarantee updated from 60-day to 90-day ("Feel Clean Guarantee")
- Gemini watermark sparkles stripped from all prompts where they were accidentally included as design elements

## Insights & Learnings
- When adapting competitor creative, it's critical to verify actual product ingredients rather than guessing — the initial prompt included Dandelion Root which is not in Motilli
- The Gemini sparkle/star watermark was inadvertently being treated as a design element from the reference images — need to identify and strip these during adaptation
- Text overflow in comparison charts is a common generation issue — shorter text strings are essential for clean rendering

## Creative Output
- 8 Motilli branded product image prompts (JSON): `/Users/brooksorradre2/Documents/Ecommerce/motilli/motilli_product_image_prompts.json`
  1. Product Hero + 3 Benefits
  2. "Go green. Feel clean. Every day." benefits layout
  3. Testimonial (Sarah K., 42)
  4. Ingredients Wheel (4 ingredients)
  5. "Why Choose Motilli?" trust badges
  6. Comparison Chart (Motilli vs. Other Brands)
  7. 90-Day "Feel Clean Guarantee"
  8. Supplement Facts panel (needs verification against actual label)

## Action Items & Next Steps
- Verify Supplement Facts panel (image 8) against actual Motilli nutrition label before production
- Generate images via n8n native factory workflow or Gemini directly
- The prompts are production-ready pending the supplement facts verification

## Notable Quotes / Language
- "Feel Clean Guarantee" — the branded guarantee name for Motilli
- "Go green. Feel clean. Every day." — tagline concept

## Connections to Vault
- Used [[native-image-factory]] skill for prompt architecture
- Motilli color system documented: accent `#A7D72F`, background `#8CC63F`
- Connects to the broader Motilli branded creative asset pipeline alongside the product photography and UGC prompts from other sessions
