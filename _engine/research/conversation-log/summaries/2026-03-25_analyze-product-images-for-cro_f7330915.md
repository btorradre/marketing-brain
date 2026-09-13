---
type: session-summary
date: 2026-03-25
session_id: local_59de03ed-fcfa-47ac-980a-ddabf7330915
title: "Analyze product images for CRO"
category: creative-production
brands_discussed: [Motilli]
formats_worked: [static, native-image, sora-video, ugc]
tags:
  - session-log
  - summary
  - creative-production
  - motilli
  - product-images
  - sora
  - ugc
  - glp-1
---

# Analyze product images for CRO — Session Summary

**Date:** 2026-03-25
**Category:** creative-production
**Transcript:** [[conversation-log/transcripts/2026-03-25_analyze-product-images-for-cro_f7330915]]

## What Happened
Corrected Motilli product image prompts that had wrong jar dimensions, then created 5 Sora 2 Pro UGC testimonial video prompts for women 50+ on GLP-1 medications. Iterated through JSON format, audio integration, and adding the product jar into each creator's hands.

## Key Decisions Made
- Changed bloating copy from "Flattens Bloating Fast" → "Stops GLP-1 Bloating†" — stronger targeting signal that names the exact problem for the exact audience
- Front shot perspective (not 3/4 angle) for hero product image
- 12-second max per Sora clip (~30 words audio)
- Each UGC creator holds the Motilli jar — product must be visible in every testimonial
- Sora handles audio natively — no separate audio field needed, dialogue baked into prompt with "She says:"

## Insights & Learnings
- The original jar description was wrong in almost every dimension — overcorrected toward "mason jar" which confused AI generators. Real jar is a standard wide-mouth supplement jar, taller than wide (1:1.4), with visible neck threading
- "Stops GLP-1 Bloating" is a much stronger hook than "Flattens Bloating" because it names both the problem AND the cause (the medication) in 3 words
- For Sora prompts, the product jar description must match the real product exactly: wide-mouth glass jar, bright lime-green label, white lid, dark green heart-shaped gummies visible through glass

## Creative Output
- Updated Motilli Product Image Prompts.md (jar corrections, bloating copy, cropping fixes)
- Motilli Sora UGC Testimonial Prompts.md (5 prompts, markdown format)
- Motilli Sora UGC Testimonial Prompts.json (5 prompts, ready for Sora 2 Pro)

## Action Items & Next Steps
- Enable computer use to generate videos via Key.ai automatically
- Generate the 5 Sora clips and review output quality
- Test whether Sora renders the product jar accurately from the description

## Notable Quotes / Language
- "Stops GLP-1 Bloating†" — the winning copy for the hero card
- "My doctor asked what I changed" — strongest social proof angle (doctor validation)
- "I almost quit my medication" — highest-stakes emotional angle
- The five symptom angles: bloating, sulfur burps, constipation, multiple symptoms, doctor validation

## Connections to Vault
- Uses [[sora-scripting]] skill for video prompt architecture
- Product details pulled from Motilli research docs in vault
- Image prompts saved to root of marketing brain
- JSON prompts ready for production pipeline
