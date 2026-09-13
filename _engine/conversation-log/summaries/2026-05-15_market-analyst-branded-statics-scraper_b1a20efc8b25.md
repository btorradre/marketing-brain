---
type: session-summary
date: 2026-05-15
session_id: local_417d7141-9c2c-486b-8ecd-b1a20efc8b25
title: "Market analyst branded statics scraper"
category: competitor-analysis
brands_discussed: [Arrae, Alethios, myNuora, North Valley Health]
formats_worked: [static, competitor-research]
tags:
  - session-log
  - summary
  - competitor-analysis
  - scheduled-scraper
  - branded-statics
  - arrae
  - nuora
  - feminine-health
  - clinical-proof-archetype
  - testimonial-card-archetype
---

# Market analyst branded statics scraper — Session Summary

**Date:** 2026-05-15
**Category:** competitor-analysis
**Transcript:** [[conversation-log/transcripts/2026-05-15_market-analyst-branded-statics-scraper_b1a20efc8b25]]

## What Happened

Scheduled scraper rotation hit Arrae, myNuora, and North Valley Health. Arrae produced zero qualifying branded statics — only 4 active image ads, all native-style lifestyle photography routed through the "Alethios" research-study front, no text overlays or product comparisons. myNuora produced three confirmed archetypes captured via zoom screenshots. Browser instability and the privacy guard blocking Facebook CDN image URLs forced a pivot from "download images" to "document archetypes from visual screenshots." North Valley pass was started but the transcript was idle before substantive findings surfaced.

## Key Decisions Made

- Confirmed Arrae is currently running a video-heavy ad mix (~1,100 video results) with only 4 active static creatives — all native UGC-style, none qualifying as branded statics.
- Confirmed Arrae uses "Alethios" as a research-study front sponsor name (URL: studies/arrae-bloat-digestive-gummies-study).
- Pivoted scrape methodology: since the privacy guard sanitizes Facebook CDN URLs and Chrome's save_to_disk doesn't surface to the sandbox file system, the catalog entries (with rich archetype descriptions) are the primary deliverable. Image files are nice-to-have.

## Insights & Learnings

- **Arrae has shifted to a research-study funnel architecture.** Sponsor name "Alethios" + URL path `/studies/arrae-...` suggests they're testing a study/clinical framing for cold traffic, separate from their direct-brand campaigns. Worth a deeper look in a separate session.
- **myNuora is running three distinct branded static archetypes in active rotation:**
  1. **Testimonial Card + Urgency Pricing** — two-woman selfie split with "Price increases again in 48 minutes" + "Excellent 4.9/5" star rating.
  2. **Product + Visual Metaphor (waste contrast)** — trash can full of pads/pantyliners next to sink with Nuora product. Headline "This helped me A LOT" + 5-star rating.
  3. **Medical/Clinical Proof** — three doctors/nurses in scrubs in a clinical setting with headline "New Vaginal Odor Research."
- **myNuora also runs:** anatomical illustration with red arrows (Medical/Clinical Proof), apple-cut-open biofilm visual metaphor, microscopic probiotic/biofilm black-and-white imagery (Medical/Clinical Proof).
- **Workflow constraint surfaced:** Chrome's `save_to_disk` action stores files client-side and they never surface in the sandbox file system. Facebook CDN URLs are sanitized by the privacy guard. The reliable extraction method is zoom-region screenshots with detailed archetype documentation, not raw image downloads.

## Creative Output

No new creative produced. Catalog file writes for myNuora archetypes were referenced as the deliverable (status: in progress when transcript closed). North Valley Health catalog entries were not captured in the visible transcript.

## Action Items & Next Steps

- Verify the Nuora archetype catalog files actually got written to the brand folder (the transcript ends mid-task with the assistant about to write them).
- Complete North Valley Health pass on the next scraper run.
- Add the "Alethios research-study front" finding to the Arrae brand profile — this is a new funnel architecture worth tracking.
- Consider building an "image extraction fallback" doc that codifies the screenshot-only workflow when the privacy guard blocks CDN URLs.
- The Nuora "Price increases again in 48 minutes" urgency overlay is worth swiping into the static archetype library.

## Notable Quotes / Language

- "Arrae is currently running zero qualifying branded statics."
- "Arrae has a research-study funnel running via Alethios as the sponsor name."
- "Per the stability rules — 'If Chrome crashes: Don't panic. Note where you were, reopen Chrome, and continue from the next brand. File whatever you already captured.'"
- Nuora headlines captured: "Price increases again in 48 minutes" / "This helped me A LOT" / "New Vaginal Odor Research"

## Connections to Vault

- Adds to the rolling Nuora swipe file (see [[mynuora-direct-response-video-ads]] for video coverage of the same brand).
- Static archetype catalog work — feeds into ongoing static creative reference library.
- Arrae profile gets a new note: research-study front via Alethios.
- North Valley Health remains incomplete this rotation — note for next pass.
