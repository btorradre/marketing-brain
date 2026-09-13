# Branded Statics Scrape — 2026-04-30 (Thursday Rotation)

**Brands targeted:** AG1 (Athletic Greens), GOLO, Provitalize (BB Company)
**Source:** Meta Ad Library (active, US, image media filter where applicable)
**Time:** April 30, 2026

---

## Summary

| Brand | Active Static Results | Outcome | New Templates Added |
|---|---|---|---|
| AG1 | ~200 (incl. video); ~7 polished branded statics captured | Major scale-up since March (was 2 statics) | Pulled-quote testimonial card, Distribution-authority ("New at Target"), Welcome-kit pricing urgency |
| GOLO | 0 (page still dark; substring noise pulled 350 unrelated brands) | Status unchanged from March | None |
| Provitalize | ~50 active branded image statics; ~1,800 total active ads incl. video | Massive scale-up; multi-page strategy now 6 pages | Vintage medical-illustration pain angle, Anti-doctor rage story, "Cabinet of half-empty bottles" identification, Hexagonal benefit-callout |

**Catalogs updated for all 3 brands.** Image files were not downloaded — see "Image Capture Note" below.

---

## Image Capture Note (transparency)

Per task spec, the original plan was to right-click → save each qualifying image. In this run that wasn't possible:
- The Meta Ad Library page restricts image-source URLs from JavaScript via cookie/query-string blocking, so programmatic URL extraction returns nothing.
- The Chrome MCP zoom screenshots successfully captured each ad visually, but the `save_to_disk` flag stores the image inside the Chrome extension's local image store rather than in the workspace folder — those bytes weren't reachable from the file system.
- I made the call to prioritize **rich metadata + Library IDs** in the catalogs over image binaries, since: (a) every ad is re-fetchable in seconds via its Library ID, (b) the prior catalogs already follow this same convention, and (c) the design-DNA text descriptions are what's actually useful when templating future creative.

If image binaries become important for a specific brand, the right next step is a manual session with Cmd+Shift+4 region screenshots, or wiring up an Apify Meta Ad Library scraper (already in the connector list).

---

## Brand-by-Brand Findings

### 1. AG1 (Athletic Greens) — STATIC PROGRAM EXPANDED

In March the AG1 catalog noted only 2 active branded statics (Hugh Jackman timeline format). Today's scrape returned **~7 distinct polished statics** running concurrently. The dominant new template is a **pulled-quote testimonial card** that has effectively replaced the celebrity-only design.

Key new Library IDs (all "AG1 by Athletic Greens" page):
- 1603630744310905 — "$72 Free Welcome Kit Now" (ingredient grid + pricing urgency) — Quality 9/10
- 1275973514071067 — "AG1. New at Target Nationwide" (distribution authority) — Quality 9/10
- 2387373101715689 — "Make AG1 Your Morning Routine" — Austin Smith pulled quote — Quality 8/10
- 8333868497822330 — Older woman testimonial card — Quality 8/10
- 2207803266411261 — Tennis player pulled quote — Quality 8/10
- 2181100035750865 — Younger woman with quote — Quality 7/10
- 8806045411292075 — Variant of above with different model — Quality 7/10

**Top template recommendation:** Pulled-quote testimonial card. Reproducible at low cost with stock or UGC photography + an italicized credibility-line caption. Highest carryover value for Lunessa / Velantra / Motilli.

### 2. GOLO — STILL DARK ON META

Both "GOLO" and "GOLO Release" keyword searches returned no active GOLO weight-loss creative. The brand remains absent from Meta paid (consistent with March's "page unpublished" finding). 5+ weeks of darkness is meaningful — they have either fully exited Meta or restructured under a name we can't yet identify.

**Implication:** The slot GOLO occupied — natural-supplement weight loss / non-prescription metabolic — is being aggressively claimed by **Provitalize's anti-Ozempic series** (see below). Worth tracking as the GLP-1 backlash story continues.

### 3. PROVITALIZE — MASSIVE SCALE-UP + NEW PAGE ADDED

Provitalize is the standout finding of this scrape. ~7x growth in total active ads since March, ~30% growth in branded statics specifically, and the multi-page strategy expanded from 4 to 6 pages — including a brand-new page ("Lucy Chapman") added since the March pull.

Key new Library IDs:
- 1328618145987285 (Lucy Chapman page, NEW) — "I almost SLAPPED Dr Smith" — Quality 9/10
- 1727553928154301 — "Just as I suspected... It's Gluteal Tendinopathy" — neon AI-rendered skeletons — Quality 7/10
- 1216487670658763 — "It's probably not sciatica" pain-angle native — Quality 8/10
- 259751572988451317 — "Achy Hips? It's Not Arthritis" — Quality 8/10
- 1285861899580714 — "How's your hip pain after the cortisone shots?" + vintage anatomy illustration — Quality 9/10
- 1750278153021498 — "Attention women over 50… hip pain at night" + vintage illustration — Quality 8/10
- 819677711177527 — "I am FURIOUS at every doctor" anti-establishment rage — Quality 9/10
- 1910149622953034 / 716668034533932 — "Cabinet full of half-empty bottles" (running on TWO pages simultaneously) — Quality 9/10
- 1275947411343991 — "This was me after Tirzepatide... -70 lbs" anti-GLP-1 rebound — Quality 9/10
- 1831536194174280 — "Double-Dip Coupon Stacking Tip" + RISK FREE badge — Quality 7/10
- 1403352224881158 — "Nothing Comes Close To Provitalize" hexagonal benefit grid — Quality 8/10

**Top three template recommendations from Provitalize:**
1. **Vintage medical-illustration pain static** (Library IDs 1285861899580714, 1750278153021498) — public-domain, royalty-free, authority-coded, very scroll-stopping. Highest novelty in the supplement space right now.
2. **"Cabinet of half-empty bottles" identification story** — universal template for anyone whose avatar has tried-and-failed many alternatives.
3. **Anti-doctor rage story** — high-risk, high-reward voice. "I almost SLAPPED Dr Smith" is a textbook pattern-interrupt opener.

---

## Cross-Brand Design Trends Spotted

- **Pulled-quote testimonial cards are converging into a category-wide format** — both AG1 and Provitalize lean on quote + photo overlays. Differs in casting (AG1: aspirational athletes/professionals; Provitalize: real-women anger and pain).
- **Anti-GLP-1 / anti-Ozempic positioning is now a sustained creative theme**, not a momentary tactical play. Provitalize has run it from March → April with growing realism in the visuals (stock → mirror selfie).
- **Anti-doctor / anti-medical-establishment voice is the strongest emotional driver** in the menopause/perimenopause static space. Direct hostility outperforms gentle empathy in this category.
- **Public-domain vintage medical illustration** is emerging as a low-cost authority signal — appearing in 2+ Provitalize ads and worth testing more broadly.
- **Multi-page strategies are scaling** — BB Company is now running 6+ pages for Provitalize. The "single brand, single page" model is increasingly an artifact.

---

## Top Template Recommendation (Cross-Brand)

**Pulled-Quote Testimonial Card** is the highest-leverage immediate copy: AG1 is running 5+ variants, Provitalize is running variants of it, and it's the most reproducible polished format with modest production budget. Suggested priority deployment: Velantra (afternoon-energy quote, shift-worker subject) → Lunessa (sleep-quality quote, ER nurse subject) → Motilli (gut-comfort quote, post-meal scenario subject).

---

## Chrome Stability Report

- AG1 search: clean, no crashes
- GOLO search (both queries): clean
- Provitalize unfiltered search (~1,800 results): tab crashed on first scroll. Recovered with fresh tab + image-only filter.
- One additional silent tab dispose during AG1 JS extraction attempt
- Followed all 9 stability rules: closed tabs between brands, paused 5-7s between actions, capped at 5-10 quality images per brand, did not attempt to recover the crashed Provitalize tab.

---

## Files Touched This Run

- Updated: `statics/branded_statics/ag1/catalog.md` (appended 2026-04-30 section)
- Updated: `statics/branded_statics/golo/catalog.md` (appended 2026-04-30 status-unchanged note)
- Updated: `statics/branded_statics/provitalize/catalog.md` (appended 2026-04-30 section)
- Created: this file

No image binaries downloaded this run (see Image Capture Note above).
