---
type: session-summary
date: 2026-05-08
session_id: local_40debac1-c825-431c-a666-cd575efe944c
title: "Market analyst meta scraper"
category: competitor-analysis
brands_discussed: [Dr. Erin Harper, Purely Nutrient, Dr. Michael Samson, Natural Healing with Dawn Miller, The Balanced Gut, Cirvano, Bioma.Health, Dr. Micheal Jones, Essential Women's Health, Pupganics Co., Paws & Care Vet]
formats_worked: [long-form]
tags:
  - session-log
  - summary
  - competitor-analysis
  - meta-scraper
  - long-form-copy
  - gut-health
  - parasites
  - friday-rotation
  - chrome-stability-issues
  - incomplete-session
---

# Market analyst meta scraper — Session Summary

**Date:** 2026-05-08
**Category:** competitor-analysis
**Transcript:** [[conversation-log/transcripts/2026-05-08_market-analyst-meta-scraper_cd575efe944c]]

## What Happened
Friday gut-health rotation. Found multiple strong long-form candidates (Dr. Erin Harper / Purely Nutrient, Dr. Michael Samson, Natural Healing with Dawn Miller, The Balanced Gut / Cirvano, Dr. Micheal Jones). Successfully expanded the Dr. Erin Harper / Purely Nutrient ad and began chunked text extraction via JavaScript before the session timed out with an API error mid-extraction. No swipes were filed.

## Key Decisions Made
- Pivoted from initial junk results ("gut health supplement" pulling cholesterol/joint/dog ads) to a more targeted query that surfaced real gut/parasite long-form candidates
- Prioritized **Dr. Erin Harper (Purely Nutrient)** for first swipe due to 3 ads using the same creative — strong scaling signal
- Dr. Marcus Thompson noted but skipped — pediatric gut, off-niche for today
- Bioma.Health rejected as short-form/punchy with emojis

## Insights & Learnings
- **Ethiopian black seed oil** is an emerging mechanism-of-the-moment in the parasite/gut-cleanse niche — appearing in both Dr. Michael Samson and Dr. Erin Harper ads
- **3 AM / bloating** is a recurring narrative hook structure in this lane (specificity + "wakes you up" pattern interrupt)
- **The Balanced Gut / Cirvano** uses an "I was diagnosed with IBS at 19. I'm 34 now" narrator-with-chronological-arc framing — clean template for chronic-condition narratives
- Chrome extension is dropping during JavaScript-chunked text extraction — same pattern as recent sessions

## Creative Output
**None persisted.** Session terminated mid-extraction of Purely Nutrient / Dr. Erin Harper ad. Brand identified, scaling signal confirmed (3 creative versions running), but ad copy not captured fully or filed.

## Action Items & Next Steps
- **Re-run Purely Nutrient (Dr. Erin Harper) extraction** — 3-creative scaling signal makes this a high-priority swipe. Use a more robust extraction strategy than JS-chunking (consider rendered DOM dump + offline parse)
- **Investigate Ethiopian black seed oil mechanism cluster** — both Samson and Harper using it; possible category trend or shared affiliate network
- **The Balanced Gut / Cirvano** is a fresh long-form candidate worth pulling next
- **Natural Healing with Dawn Miller** (parasitologist / raw fish hook) noted as a strong narrative hook candidate
- **Engineering: chunked-text extraction is fragile.** Need a single-call method to extract full ad body without per-chunk browser round-trips that destabilize the session

## Notable Quotes / Language
- "I was diagnosed with IBS at 19. I'm 34 now" — Cirvano / Balanced Gut narrator framing
- "Ethiopian black seed oil" — recurring mechanism in parasite/gut lane
- "3 AM" — recurring time-stamp specificity pattern

## Connections to Vault
- Connects to the [[long form copy/references]] catalog
- Friday gut-health rotation per the market-analyst SOP
- Purely Nutrient and Cirvano are both new brands — no existing vault entries
- Reinforces the recurring Chrome instability issue
