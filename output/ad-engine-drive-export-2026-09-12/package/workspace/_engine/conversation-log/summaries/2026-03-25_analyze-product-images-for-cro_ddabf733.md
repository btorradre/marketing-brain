---
type: session-summary
date: 2026-03-25
session_id: local_59de03ed-fcfa-47ac-980a-ddabf7330915
title: "Analyze product images for CRO"
category: creative-production
brands_discussed: [Motilli]
formats_worked: [native-image, video-script]
tags:
  - session-log
  - summary
  - creative-production
  - product-photography
  - sora-scripting
  - UGC
  - GLP-1
  - motilli
  - CRO
  - image-prompts
---

# Analyze product images for CRO — Session Summary

**Date:** 2026-03-25
**Category:** creative-production
**Transcript:** [[conversation-log/transcripts/2026-03-25_analyze-product-images-for-cro_ddabf733.md]]

## What Happened
Iteratively refined Motilli product image prompts — correcting jar proportions, fixing perspective angles, updating copy on cards (changed to "Stops GLP-1 Bloating"), removing cropping instructions so full product is visible. Then pivoted to creating 5 AI UGC testimonial video prompts for Sora 2 Pro, featuring women over 50 on GLP-1 medications reviewing the product.

## Key Decisions Made
- Jar description corrected from "short, squat mason jar 1:1.2 ratio" to actual proportions: standard wide-mouth supplement jar, 1:1.4 width-to-height ratio, visible neck threading, warm/olive tone from dark gummies showing through
- Hero card copy changed from "Flattens Bloating Fast" to "Stops GLP-1 Bloating" — stronger targeting signal that names the specific problem
- Product shots changed to front-facing view (not angled), lid ON
- Full jar must be visible — removed the 15% edge cropping from Images 4 and 6
- Sora prompts designed for 12-second clips with audio baked into the prompt (Sora 2 Pro generates audio natively)
- Each UGC testimonial creator holds or interacts with the Motilli jar — product visibility was missing in the first version

## Insights & Learnings
- "Stops GLP-1 Bloating" is better targeting language than "Flattens Bloating" — names the exact audience and problem in four words
- Sora 2 Pro handles audio natively, so dialogue should be embedded in the visual prompt with "She says:" framing
- Product must be physically present in UGC-style content — testimonials without the product in hand feel disconnected

## Creative Output
- Updated product image prompts: `/Users/brooksorradre2/Documents/marketing brain/Motilli Product Image Prompts.md`
- 5 Sora UGC testimonial prompts (JSON): `/Users/brooksorradre2/Documents/marketing brain/Motilli Sora UGC Testimonial Prompts.json`
  - Clip 1: "The Bloating Is Gone" — car yapper, Ozempic
  - Clip 2: "Sulfur Burps Finally Stopped" — kitchen table, Mounjaro
  - Clip 3: "I'm Finally Regular Again" — living room couch, Wegovy
  - Clip 4: "I Almost Quit My Medication" — bedroom, Ozempic
  - Clip 5: "My Doctor Asked What I Changed" — car yapper, Mounjaro

## Action Items & Next Steps
- Generate UGC videos via Key.ai or Sora 2 Pro (computer use needed for Key.ai automation)
- Enable computer use in settings if automation of Key.ai generation is desired

## Notable Quotes / Language
- "Stops GLP-1 Bloating" — the winning product card copy
- Each testimonial references a specific GLP-1 medication for audience matching

## Connections to Vault
- Used [[sora-scripting]] skill for UGC prompt architecture
- Product image prompts connect to the broader Motilli creative asset pipeline
- UGC testimonial angles align with the GLP-1 avatar symptom map from prior research sessions
