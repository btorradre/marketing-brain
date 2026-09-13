---
type: session-summary
date: 2026-04-30
session_id: local_cf3d7230-242e-4c6f-a2e9-a24a46feba9f
title: "Market analyst branded statics scraper"
category: competitor-analysis
brands_discussed: [AG1, GOLO, Provitalize]
formats_worked: [static]
tags:
  - session-log
  - summary
  - competitor-analysis
  - statics-scraper
  - branded-statics
  - thursday-rotation
  - ag1
  - golo
  - provitalize
  - menopause
  - hip-pain
  - testimonial-card
  - pain-angle-native
  - anti-glp1
---

# Market analyst branded statics scraper — Session Summary

**Date:** 2026-04-30
**Category:** competitor-analysis
**Transcript:** [[conversation-log/transcripts/2026-04-30_market-analyst-branded-statics-scraper_46feba9f]]

## What Happened
Thursday-rotation branded statics scrape covering AG1, GOLO, and Provitalize. AG1 yielded 7 polished statics (major scale-up since March); GOLO confirmed still dark on Meta; Provitalize yielded 11 new statics (~7x volume increase since March, with multi-page strategy expanded from 4 to 6 brand pages). All three brand catalogs updated; intel drop filed.

## Key Decisions Made
- Pivot away from JS-based image URL extraction (security-blocked + crash-inducing) and image_only filtering for Provitalize's heavy 1,800-result page.
- Document statics by Library ID + visual archetype rather than downloading binaries (Chrome MCP `save_to_disk` doesn't expose paths back to workspace; Meta's anti-scrape JS blocks URL extraction).
- Confirm GOLO continues to be unpublished/inactive on Meta — no further action required for this brand.
- Recommend pulled-quote testimonial card as the highest-carryover archetype for Lunessa / Velantra / Motilli.

## Insights & Learnings
- **AG1 dominant template shift:** Pulled-quote testimonial card (athlete / professional / older woman + italicized quote overlay) is now AG1's lead static format. Two new utility templates emerged: distribution-authority ("New at Target Nationwide") and welcome-kit pricing urgency ("$72 Free").
- **Provitalize doubling down on pain-angle native:** Confirmed continuation and expansion of pain-angle native creative — sciatica/sacroiliac/hip-arthritis misdirection, vintage medical-illustration pain ads, and anti-doctor rage stories ("I almost SLAPPED Dr Smith").
- **New Provitalize page added:** "Lucy Chapman" page joins the multi-page strategy (was 4 pages in March, now 6: BB Company, Provitalize, Best Probiotics For Menopause, Menopause And Me, Menopause Care And Relief, Lucy Chapman).
- **Anti-Ozempic/GLP-1 angle persists at Provitalize:** Tirzepatide weight-rebound transformation testimonials still active.
- **Cross-brand testimonial card convergence:** Both AG1 and Provitalize now run pulled-quote testimonial card variants — strongest cross-category template.
- **Chrome stability lesson:** Heavy Ad Library result pages (1,800+ results) reliably crash tabs during scroll/JS extraction. Mitigation: use `media_type=image` URL filter to narrow result count before scrolling.

## Creative Output
- `statics/branded_statics/ag1/catalog.md` — appended 2026-04-30 section (+84 lines)
- `statics/branded_statics/golo/catalog.md` — appended status note (+14 lines)
- `statics/branded_statics/provitalize/catalog.md` — appended 2026-04-30 section (+135 lines)
- `agents/market-analyst/intel-drops/2026-04-30_statics-scrape.md` — new intel drop, 112 lines

## Action Items & Next Steps
- Wire up Apify Meta Ad Library scraper if image-binary download becomes a hard requirement (currently Library IDs serve as re-fetch handles).
- Test pulled-quote testimonial card format for Lunessa / Velantra / Motilli — easy to produce on modest budget, validated across two scaling brands.
- Continue tracking Provitalize multi-page expansion and watch for additional pages added to the network.
- Capture vintage medical-illustration pain ad as a creative reference for future Lunessa pain-angle work.
- Use `media_type=image` URL filter as default for any brand with >500 active results to avoid Chrome tab crashes.

## Notable Quotes / Language
- Provitalize anti-doctor opener: "I almost SLAPPED Dr Smith. You should have seen his annoying smirk when I said it wasn't hip arthritis."
- Provitalize collagen-rage opener: "I just threw away the collagen my doctor told me to take for my hip pain — and I am FURIOUS."
- Provitalize qualification opener: "Attention women over 50 who struggle with hip pain at night. When was the last time you slept through a full night on your right hip without waking up at 2am with that deep, burning ache?"
- AG1 pulled-quote: "AG1 is one of those little things that helps me feel grounded and perform my best."
- Provitalize sciatica misdirection: "If your lower back pain shoots down your thigh but stops before the knee, it's probably not sciatica."

## Connections to Vault
- Updates [[statics/branded_statics/ag1/catalog]], [[statics/branded_statics/golo/catalog]], [[statics/branded_statics/provitalize/catalog]].
- Reinforces multi-page brand strategy intel — feed into any [[funnel-advisory]] / [[funnel-analysis]] discussions about brand network expansion.
- Pain-angle native creative templates from Provitalize should feed [[native-image-factory]] swipe references.
- Pulled-quote testimonial card archetype should be added as a swipe template referenced from [[native-image-factory]] and Lunessa/Velantra/Motilli creative briefs.
- GOLO confirmed-dark status — note in any future GOLO references; brand effectively inactive on Meta channel.
