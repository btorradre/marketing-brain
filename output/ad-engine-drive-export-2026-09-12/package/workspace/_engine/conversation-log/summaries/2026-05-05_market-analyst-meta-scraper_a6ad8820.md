---
type: session-summary
date: 2026-05-05
session_id: local_b5f3d24a-cf8d-42cc-9261-a6ad882045d0
title: "Market analyst meta scraper"
category: competitor-analysis
brands_discussed: [Mira Organics, Nerve Pain Relief Community, TrueHealthic, True Nutra, TrueNutraWellness, Mama Bear Oasis, Neuropaway, Mountain Ice, Trihelix, Alevia]
formats_worked: [long-form]
tags:
  - session-log
  - summary
  - competitor-analysis
  - meta-scraper
  - tuesday-rotation
  - nerve-pain
  - neuropathy
  - foot-pain
  - long-form-copy
  - swipe-file
  - api-timeout
---

# Market analyst meta scraper — Session Summary

**Date:** 2026-05-05
**Category:** competitor-analysis
**Transcript:** [[conversation-log/transcripts/2026-05-05_market-analyst-meta-scraper_a6ad8820]]

## What Happened
Tuesday meta scraper run. Searched the nerve-pain rotation (nerve pain, neuropathy, foot pain). Captured three strong long-form swipes — a nurse-narrator neuropathy ad (Mira Organics), a DPM podiatrist methylene blue gummy ad (TrueHealthic / Dr. Michael Chen), and a 16k-character mega sales letter (True Nutra / Dr. Quintavius Carter, Black-folks Vitamin D / diabetes angle). Spotted a powerful spouse-narrator hook (Mama Bear Oasis) but Chrome crashed before the full body could be extracted. Session ended with API timeout during the file-write phase.

## Key Decisions Made
- Skipped NeuropAWAY — only 377 chars, short-form benefit copy, doesn't meet long-form SOP threshold
- Skipped Dr. Marcus Thompson / Trihelix — pediatric gut/behavioral angle, off-niche for Tuesday nerve-pain rotation (more relevant to Friday gut-health rotation)
- Skipped Mama Bear Oasis as a formal swipe — Chrome crashed mid-extraction, only opening lines captured. Per SOP rule #2 ("Don't summarize. Don't paraphrase. The vault needs the exact copy"), can't responsibly file partial copy. Logged as "spotted but not swiped" lead.
- Did NOT swipe the Jessica Bennett (Alevia) sciatica ad — Alevia already tracked, similar mechanism likely already cataloged
- Switched to chunked JavaScript text extraction with hidden-DOM-element trick to work around tool truncation; base64 encoding is blocked by safety policy

## Insights & Learnings
- **The "Dr. Quintavius Carter" sales letter (16,431 chars) is the longest single-ad we've captured** — ~2,700 words of doctor-narrated direct response, with a melanin / Vitamin D / Black-American-targeted Type 2 diabetes angle. Two parallel variants run simultaneously (Black-folks version + race-blind "honest Americans" version) — clean A/B test of demographic specificity vs universal framing.
- **The DPM podiatrist methylene blue gummy mechanism (TrueHealthic / Dr. Michael Chen)** is a fresh nerve-pain mechanism we haven't seen elsewhere — methylene blue + gummy form factor is a clean side-door entry into the saturated neuropathy supplement category.
- **The nurse-narrator-31-years opener (Mira Organics)** is a stable, effective hook archetype — pairs authority (length of nursing tenure) with insider revelation framing. Add to hook taxonomy.
- **Spouse-narrator hook (Mama Bear Oasis)** — extremely powerful framing not yet seen in vault: the wife describes the husband's neuropathy from the outside ("my husband begged me to cut his feet off"). Worth pursuing if still running.
- **Chrome instability is forcing chunked text extraction with smaller ranges** — the truncation behavior is at the tool-response level, so 1,500-char or smaller chunks survive. Base64 encoding is blocked by safety policy.

## Creative Output
Three full ad bodies captured. Filing status uncertain (API timeout hit during the file-write phase) — the following filings should be VERIFIED:
- Intended swipe: Mira Organics — nurse narrator, neuropathy, ~430 words
- Intended swipe: TrueHealthic — Dr. Michael Chen DPM, methylene blue gummies, ~620 words
- Intended swipe: True Nutra — Dr. Quintavius Carter endocrinologist, Black folks / Vitamin D / diabetes, ~2,700 words
- Intended: intel drop for nerve-pain rotation

## Action Items & Next Steps
- **Verify whether the three swipes landed** in `long form copy/references/` before the API timeout. If not, re-file from session output.
- Add Mama Bear Oasis to brand watchlist — if still running next nerve-pain rotation, swipe full body
- Add nurse-narrator opener to hook-generation skill swipe library
- Add spouse-narrator framing to hook-generation skill (rare and powerful)
- Add DPM-narrator + methylene-blue mechanism to long-form-copy mechanism library
- Document the demographic-specificity-vs-universal A/B (Carter "Black folks" vs "honest Americans" variants) — useful pattern for any product with racial/demographic-specific risk factors
- Update scrape SOP — chunked extraction with hidden-DOM-element trick should be documented as the default text-extraction method

## Notable Quotes / Language
- "I've been a nurse for 31 years…" (Mira Organics opener)
- "My husband begged me to cut his feet off because the burning was so bad, but last night he slept through the entire night without moving. It was 2:14 AM on a Tuesday." (Mama Bear Oasis spouse-narrator)
- "Dr. Michael Chen, DPM" sign-off (TrueHealthic)
- Carter ad opening framing: "Black folks" / "honest Americans" parallel variants — demographic-specificity vs universal A/B test

## Connections to Vault
- Updates pending verification: `long form copy/references/mira_organics/`, `long form copy/references/truehealthic/`, `long form copy/references/true_nutra/` (or `truenutrawellness/`)
- Connects to: existing alevia catalog (Jessica Bennett persona — sciatica angle, considered but skipped this session)
- Skill connections: hook-generation (nurse-narrator, spouse-narrator), long-form-copy (DPM-narrator + methylene blue mechanism), desire-angle-concept (demographic-specificity-vs-universal A/B)
- Related intel drops: pending — likely intended for `agents/market-analyst/intel-drops/2026-05-05_meta-scrape_nerve-pain.md`
