---
type: session-summary
date: 2026-04-25
session_id: local_a73be7ba-127e-47e7-ba89-b3378bee83fa
title: "Market analyst meta scraper"
category: competitor-analysis
brands_discussed: [Amanda Reeves, Haven Red Root Complex, Eddie Abbew, Abbewcrew, Betterthanbefore, Multi Collagen]
formats_worked: [long-form, swipe-file]
tags:
  - session-log
  - summary
  - competitor-analysis
  - meta-scraper
  - weight-loss
  - glp1
  - hair-loss
  - menopause
  - collagen
  - ozempic-face
  - intel-drop
---

# Market analyst meta scraper (Saturday weight-loss/GLP-1) — Session Summary

**Date:** 2026-04-25
**Category:** competitor-analysis
**Transcript:** [[conversation-log/transcripts/2026-04-25_market-analyst-meta-scraper_8bee83fa]]

## What Happened
Saturday's weight-loss/metabolism/GLP-1 keyword rotation surfaced three new brands in the first 30 results. Four long-form ads were captured cleanly via chunked JS injection (browser truncates at ~1000 chars per call, so used batch tool to grab 950-char slices). All four filed into the long-form reference vault with structured filenames.

## Key Decisions Made
- Captured 4 ads (1 from Amanda Reeves, 2 from Eddie Abbew, 1 from Betterthanbefore) instead of 3 — second Eddie ad was a contrarian short-form worth filing.
- Used 950-char chunked retrieval pattern to bypass the 1000-char browser truncation. Documented as a reusable workflow.

## Insights & Learnings

**The GLP-1 side-effect category is undergoing a positioning shift.** It's moving from generic "Ozempic Face → collagen" plays into specific sub-mechanism + compatibility positioning. Amanda Reeves's "I'm still on my GLP-1 because I don't have to choose" reframes the entire GLP-1-recovery category — instead of fix-the-side-effect-by-quitting, the product stacks compatibly with the drug. **This collapses the trade-off objection.** Test as an angle for any product that could plausibly stack with GLP-1 use.

**Three sub-angles emerging in the GLP-1 collateral-damage space:**
1. **Hair loss → Korean red root mechanism** (Amanda Reeves / Haven Red Root Complex) — picks one specific GLP-1 side effect and addresses it with a sub-mechanism narrative
2. **Menopause "one hormone" angle** (Eddie Abbew #1) — full long-form, free-training/email-capture funnel
3. **Ozempic Face → collagen depletion** (Betterthanbefore Multi Collagen) — tighter ~900-word punchy execution, simpler angle

**Eddie Abbew is running a contrarian short-form on top of his long-form.** "£250 a month — pharma business model" attacks the GLP-1 industry economics at ~1,300 chars. Different psychological play than the long emotional ads — anger-frame instead of compassion-frame. Worth studying as a stacking pattern.

**Browser scraping pattern locked in:** 950-char JS chunked retrieval via batch tool is the working method when ad bodies exceed 1000 chars. Documented for future scraper runs.

## Creative Output
Four ads filed to long-form references:
- [[long form copy/references/amanda_reeves/amanda_reeves_01_The_weight_loss_finally_worked_but_my_hair]]
- [[long form copy/references/eddie_abbew/eddie_abbew_01_My_wife_said_something_to_me_the_other]]
- [[long form copy/references/eddie_abbew/eddie_abbew_02_250_a_month_300_a_month_if_you]]
- [[long form copy/references/betterthanbefore/betterthanbefore_01_Lets_be_real_Ozempic_will_make_you]]

Intel drop: [[agents/market-analyst/intel-drops/2026-04-25_meta-scrape_weight-loss-metabolism-glp1]]

## Action Items & Next Steps
- **Test the GLP-1 compatibility angle** ("works alongside your medication" instead of "replaces it") for any product that could plausibly stack
- Consider monitoring Amanda Reeves and Haven Red Root Complex for additional sub-mechanism plays in the GLP-1 collateral-damage category
- Study Eddie Abbew's stacking pattern (long compassion-frame + short anger-frame) — could apply to Lunessa or Motilli rotations

## Notable Quotes / Language
- **Amanda Reeves reframe:** "I'm still on my GLP-1 because I don't have to choose" (compatibility positioning, not replacement)
- **Eddie Abbew #2 attack frame:** "£250 a month — £300 a month if you..." (pharma business model angle, contrarian short-form)
- **Betterthanbefore directness:** "Let's be real — Ozempic will make you..." (no preamble, direct collateral-damage acknowledgment)

## Connections to Vault
- **Skill referenced:** [[skills/long-form-copy]], [[skills/avatar-research]]
- **Sub-niche:** GLP-1 collateral damage is now a documented sub-category — should fold into [[brands/]] research notes
- **Pattern to replicate:** The 950-char chunked extraction pattern should be added to the meta-scraper task file as the standard method for >1000-char ad bodies
- **Connects to:** [[conversation-log/summaries/2026-04-06_segment-glp1-avatars-pain-points_d54ec8f2]] — earlier GLP-1 avatar segmentation work
