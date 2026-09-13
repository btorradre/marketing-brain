---
type: session-summary
date: 2026-05-07
session_id: local_03e443a5-ea6b-4568-b311-59fee8dcd2fa
title: "Market analyst meta scraper"
category: competitor-analysis
brands_discussed: [GoodGrove, Alevia, BioRoot Labs, Vitality Extracts, Mama Bear Oasis, True Nutra, TrueHealthic, Mira Organics, TrueNutraWellness]
formats_worked: [long-form]
tags:
  - session-log
  - summary
  - competitor-analysis
  - meta-scraper
  - joint-pain
  - knee-pain
  - back-pain
  - nerve-pain
  - long-form-copy
  - swipe-file
---

# Market analyst meta scraper — Session Summary

**Date:** 2026-05-07
**Category:** competitor-analysis
**Transcript:** [[conversation-log/transcripts/2026-05-07_market-analyst-meta-scraper_59fee8dc]]

## What Happened
Scheduled Thursday meta scraper run. Searched the joint-pain rotation keywords (joint pain relief, knee pain supplement, back pain relief). Hunted for fresh long-form winners. Identified one major new brand (GoodGrove) plus a major scaling-up moment for BioRoot Labs (which previously had only one short-form ad cataloged but is now running a 69-ad "Dr Ruth White" persona with long-form narratives). Filed three swipes. Chrome dropped three times during extraction; switched to chunked JavaScript text extraction to work around payload-size truncation.

## Key Decisions Made
- Skip the Alevia "Jessica Bennett" RA / mitochondria ad — same Amla mechanism as existing alevia-ad-07 (already cataloged); avoid duplicate intel
- Skip Dr. Marcus Thompson / Trihelix — kid pediatric gut, off-niche for joint-pain Thursday
- Skip Vitality Extracts — short-form testimonial only, not the 1,000+ word native story we're after
- Skip Mama Bear Oasis as a formal swipe — only opening lines captured before crash; per SOP, don't file partial copy
- Limit to 3 swipes (vs target 3-5) given Chrome instability — quality over volume

## Insights & Learnings
- **GoodGrove's Three-Generation Compression Hook** is genuinely new — "My grandmother lived to 94 and never had knee pain. My mother needed double knee replacement at 68. I'm 52, and my knees are already grinding bone-on-bone." Three lifetimes compressed into one opening creates instant self-placement for the reader. Add to hook taxonomy.
- **GoodGrove's manufacturing-process attack mechanism** — heat destroys anthocyanins in tart cherry. This is a clean side-door for entering saturated supplement categories: position the existing market's products as broken-by-process rather than wrong-ingredient. Worth testing in our own knee/joint and skin/anti-aging lanes.
- **BioRoot Labs is scaling fast** — went from 1 short-form ad on file to a 69-ad doctor-persona library running long-form. Existing catalog is now stale; brand needs fresh deep-read.
- **Mama Bear Oasis spouse-narrator hook** — "My husband begged me to cut his feet off because the burning was so bad..." — flagged as a future swipe target if it stays running. The spouse-as-narrator angle is rare in neuropathy.
- **Chrome stability is now a real planning constraint** — three dropped connections in one session. Chunked JavaScript extraction with 1,500-char ranges is the workaround that survives most timeouts.

## Creative Output
Three swipes filed to long-form references:
- `bioroot_labs_02` — RA / Methotrexate failed-solution graveyard, 377 words, 5+ months active
- `bioroot_labs_03` — doctor / 5-benefits turmeric listicle variant, 495 words, 9.5+ months active
- `goodgrove_01` — three-generation grandmother→mother→me knee-fate story, 2,464 words, 3 months active
- Intel drop filed at `agents/market-analyst/intel-drops/2026-05-07_meta-scrape_joint-pain-knee-back.md`

## Action Items & Next Steps
- Re-deep-read BioRoot Labs — they've scaled 69x since previous catalog; whole new persona/mechanism set
- Add Three-Generation Compression to the hook-generation skill swipe library
- Add Manufacturing-Process Attack as an angle template under desire-angle-concept
- Watch Mama Bear Oasis — if still running next rotation, swipe the full body
- Consider whether to restructure scrape SOP given persistent Chrome instability — chunked-text workflow needs to be documented as the default, not the fallback

## Notable Quotes / Language
- "My grandmother lived to 94 and never had knee pain. My mother needed double knee replacement at 68. I'm 52, and my knees are already grinding bone-on-bone." (GoodGrove three-generation opener)
- "My husband begged me to cut his feet off because the burning was so bad, but last night he slept through the entire night without moving. It was 2:14 AM on a Tuesday." (Mama Bear Oasis spouse-narrator)
- BioRoot Labs framing: "I was diagnosed with rheumatoid arthritis back in..." (failed-solution graveyard structure)

## Connections to Vault
- Updates needed: `long form copy/references/bioroot_labs/` (whole new persona library), `long form copy/references/goodgrove/` (new brand folder)
- Connects to: existing alevia catalog (Jessica Bennett persona is shared/similar mechanism — Amla/mitochondria)
- Skill connections: hook-generation (three-generation hook), desire-angle-concept (manufacturing-process attack), long-form-copy (multi-generation framing law candidate)
- Related intel drops: `agents/market-analyst/intel-drops/2026-05-07_meta-scrape_joint-pain-knee-back.md`
