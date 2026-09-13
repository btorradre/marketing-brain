---
type: session-summary
date: 2026-04-17
session_id: local_04ebced9-4a54-4751-9dfc-10a3b097c06c
title: "Market analyst meta scraper"
category: competitor-analysis
brands_discussed: [Avalaine, Kialani, NERVana+, Chew Barkies, USA Health, Vaseon, Susan Bridgers, Carol Sullivan, Dr. James D. Abrams MD]
formats_worked: [long-form]
tags:
  - session-log
  - summary
  - competitor-analysis
  - meta-ad-library
  - swipe-file
  - long-form-copy
  - neuropathy
  - diabetes
  - dog-health
  - ED
  - native-narrative
---

# Market analyst meta scraper — Session Summary

**Date:** 2026-04-17
**Category:** competitor-analysis
**Transcript:** [[conversation-log/transcripts/2026-04-17_market-analyst-meta-scraper_10a3b097]]

## What Happened
Scheduled Meta Ad Library scrape for long-form narrative ads. The session successfully swiped two complete long-form ads — one from Avalaine/Kialani (Susan Bridgers page, neuropathy/NERVana+ transdermal patches) and one from Chew Barkies (Carol Sullivan page, dog CCL/joint supplement). A third target (USA Health / tryvaseon.com, ED/cardiac angle) was identified but the session appears to have ended mid-capture at the find-and-click stage on that ad.

## Key Decisions Made
- Prioritized "knee pain supplement" as a search keyword after "back pain relief" returned only romance-novel spam.
- Chose JavaScript DOM extraction over scroll-screenshots for capturing long-form ad copy after the visual approach kept truncating.
- Adopted a "close tab between brands" hygiene rule to avoid Chrome memory crashes on heavy Ad Library pages.
- Confirmed USA Health / Vaseon was not already tracked before pursuing it.

## Insights & Learnings
- "Back pain relief" as a keyword in the Meta Ad Library is flooded with romance-novel spam — not a viable search term for health supplement scraping.
- "Knee pain supplement" is a higher-signal keyword that surfaces real long-form health brands.
- The Ad Library "See more" expand is required before DOM text is available; JS extraction should run only after expansion.
- Long-form narrative ads frequently exceed the single-DOM-read limit — chunked extraction (by char-range slicing) is the reliable pattern.
- Susan Bridgers (Avalaine/Kialani, NERVana+) is a masterful long-form narrative: first-person, 63-year-old Type 2 diabetic, the nerve-damage-is-cumulative-and-irreversible reveal from the neurologist is the pivot.
- Carol Sullivan (Chew Barkies) uses dollar-figure specificity in the hook ("$5,000. For one knee. Then said 70% less the other one too…").
- USA Health / Vaseon is running a long-form ED angle tied to cardiac patients — a notable new ED mechanism angle worth tracking.

## Creative Output
- **Ad #1 swiped:** Avalaine / NERVana+ / Susan Bridgers — 12,357-char long-form narrative (neuropathy, Type 2 diabetes, transdermal patch). Saved to vault via Write tool.
- **Ad #2 swiped:** Chew Barkies / Carol Sullivan — 7,118-char long-form narrative (dog CCL, joint supplement, vet-estimate hook). Saved to vault via Write tool.
- **Ad #3 in progress:** USA Health / Vaseon (ED + cardiac angle) — session ended before full capture.

## Action Items & Next Steps
- Finish the USA Health / Vaseon swipe in a follow-up run — it was mid-capture when the session ended.
- Consider adding "knee pain supplement," "neuropathy," "nerve pain," and "diabetic nerve pain" to the standing keyword rotation; deprioritize "back pain relief" (romance spam).
- Add Avalaine, Kialani, Chew Barkies, and Vaseon to the tracked-brands list if not already there.
- The Susan Bridgers neuropathy ad is exemplar-grade — flag for a deeper teardown in a future session (mechanism beat, irreversibility pivot, dual-track narrative).

## Notable Quotes / Language
- Susan Bridgers hook: *"If your A1C is high and the pins and needles in your feet have already started, PLEASE don't make the same mistakes I did…"*
- Carol Sullivan hook: *"The vet put the estimate on the table. $5,000. For one knee. Then said 70% less the other one too…"*
- Carol Sullivan alt hook: *"My dog tore his CCL. Surgery wasn't an option."*
- Carol Sullivan CTA framing: *"If Your Dog Is On Rimadyl For A Torn CCL, Read This Before The Next Dose."*

## Connections to Vault
- Feeds the [[long form copy]] swipe file — specifically long-form narrative / native-story format.
- Susan Bridgers ad is a candidate reference for the [[long-form-copy]] skill's mechanism-irreversibility pivot pattern.
- The dollar-figure specificity hook from Carol Sullivan fits the [[hook-generation]] skill's specificity-engineering principles.
- New brands to add to the [[swipe-intake]] tracking: Avalaine, Kialani (NERVana+), Chew Barkies, Vaseon/USA Health.
- Ties to [[advertorial]] workflow — these pages are likely the advertorial layer behind the Meta ads; worth reviewing the full funnel.
