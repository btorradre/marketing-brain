---
type: session-summary
date: 2026-03-28
session_id: local_2dac719b-b431-4f86-9695-78e82dbb9d9d
title: "Mar 28 – Market analyst branded statics scraper"
category: competitor-analysis
brands_discussed: [Force Factor, NativePath]
formats_worked: [static, branded-statics]
tags:
  - session-log
  - summary
  - competitor-analysis
  - branded-statics
  - meta-ad-library
  - force-factor
  - nativepath
  - mens-supplements
  - collagen
  - automated-scrape
---

# Mar 28 – Market analyst branded statics scraper — Session Summary

**Date:** 2026-03-28
**Category:** competitor-analysis
**Transcript:** [[conversation-log/transcripts/2026-03-28_market-analyst-branded-statics-scraper_78e82dbb]]

## What Happened
Automated branded statics scrape session that discovered 2 new competitor brands (Force Factor, NativePath) but was unable to download actual ad images due to repeated Chrome crashes on the Meta Ad Library. Pivoted to writing detailed catalog entries and an intel drop based on visual observations gathered before the crashes.

## Key Decisions Made
- Classified Force Factor as HIGH VALUE for template adaptation — their dark-background product hero shots and bold claim graphics are strong candidates for feminine health adaptation
- Classified NativePath as lower priority for visual templates — mostly native/editorial-style images rather than polished branded statics
- Pivoted to deliverable writing after 4+ Chrome crashes rather than continuing to attempt image downloads

## Insights & Learnings
- **Force Factor** (442K followers, ~41 active ads) — men's performance supplements using polished branded statics with dark backgrounds, product hero shots, bold claim graphics ("PERFORM LIKE A MAN IN HIS PRIME"), and testimonial cards with quote overlays. Strong template potential.
- **NativePath** (75.6K followers, ~180 active ads) — collagen/CoQ10 supplements using mostly native/editorial-style images. More valuable for copy/framing patterns ("Forget Expensive Creams", "Health Expert urges...") than visual templates.
- Chrome continues to be unstable on the Meta Ad Library — this is a recurring issue across scrape sessions

## Creative Output
- `statics/branded_statics/force_factor/catalog.md` — brand catalog entry
- `statics/branded_statics/nativepath/catalog.md` — brand catalog entry
- `agents/market-analyst/intel-drops/2026-03-28_statics-scrape.md` — intel drop summary

## Action Items & Next Steps
- **Re-scrape Force Factor** during a more stable Chrome session to capture actual ad images
- Adapt Force Factor's dark-background hero bottle format for feminine health brands with a premium palette swap
- Explore Force Factor's testimonial card format as a template for Motilli/Velantra/Lunessa social proof statics

## Notable Quotes / Language
- Force Factor claims observed: "PERFORM LIKE A MAN IN HIS PRIME", "STRUGGLING WITH SOFT PUMPS?"
- NativePath framing: "Forget Expensive Creams", "Health Expert urges..."

## Connections to Vault
- New brand folders created under `statics/branded_statics/`
- Intel drop filed to `agents/market-analyst/intel-drops/`
- Force Factor templates could feed into the native-image-factory skill for branded static creation
