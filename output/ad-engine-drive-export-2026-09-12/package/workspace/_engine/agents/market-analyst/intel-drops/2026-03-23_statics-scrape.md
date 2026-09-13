---
type: statics-scrape
date: 2026-03-23
source: Meta Ad Library
brands_scraped: [Neurosmile]
brands_deferred: [GLP-1 SOS, Auri Labs]
images_downloaded: 0
images_identified: 26
session_status: partial — Chrome MCP crashed mid-session
tags:
  - intel-drop
  - statics-scrape
  - branded-statics
---

# Branded Statics Scrape — March 23, 2026 (Monday)

## Session Summary
**Planned brands (Monday rotation):** Neurosmile, GLP-1 SOS, Auri Labs
**Completed:** Neurosmile (catalog created, images identified but not downloaded)
**Deferred:** GLP-1 SOS, Auri Labs (Chrome MCP became unresponsive before these could be scraped)

## Brands Scraped Today

### Neurosmile
- **Active image/meme ads found:** 26
- **Branded statics identified:** 8+ across 6 archetypes
- **Images downloaded:** 0 (Chrome crashed during download attempt — see Technical Notes)
- **Catalog created:** Yes — `/statics/branded_statics/neurosmile/catalog.md`

## New Statics Summary (Observed, Not Downloaded)

| Brand | Archetype | Key Claim / Copy | Quality (1-10) |
|-------|-----------|-----------------|----------------|
| Neurosmile | Bold Claim | "CHRONIC TINGLING ENDS IN PERMANENT NUMBNESS — STOP IT NOW!" | 8 |
| Neurosmile | Bold Claim | "Diabetic, Can't Sleep, and Still Believing 'There's No Cure?'" | 7 |
| Neurosmile | Bold Claim | "Diabetic Neuropathy Diagnosis... Still Getting Worse After 6 Months?" | 6 |
| Neurosmile | Authority Comparison | "Your Life Back vs. Gabapentin's Prison: Choose Wisely" | 7 |
| Neurosmile | Competitor Comparison | "Gabapentin's Lies vs. Real Nerve Repair" | 8 |
| Neurosmile | Testimonial Card | "From gabapentin zombie to human again" (5 stars) | 7 |
| Neurosmile | Clinical/Authority | "THE GABAPENTIN ALTERNATIVE DOCTOR'S DON'T MENTION" | 7 |
| Neurosmile | Ingredient-Benefit | 600mg ALA, 18 ingredients, Pharmaceutical-Grade (in copy) | 5 |

## Design Trends Spotted

- **Anti-competitor positioning is the dominant strategy.** Neurosmile runs nearly every ad as a "us vs. gabapentin" frame. This is aggressive competitive positioning that turns a prescription drug into the enemy — a pattern worth replicating for Lunessa (vs. melatonin dependency) or Motilli (vs. mainstream alternatives).

- **Fear-based bold claims dominate.** The most common archetype is Bold Claim — big text warning of consequences ("permanent numbness", "getting worse"). These are classic direct response fear hooks turned into static images.

- **Consistent visual system across all statics.** Deep red/maroon backgrounds, bold white/yellow all-caps headlines, green checkmark benefit lists, product bottle floating on right side. This consistency creates instant brand recognition in the feed.

- **Product bottle is ALWAYS visible.** Even in comparison and testimonial formats, the Neurovital bottle is prominently placed. No ad runs without the product hero shot.

- **Urgency pricing in every CTA area.** "Save Up To 64%" appears in every ad's link preview area, along with "Complete Your Neuropathy Recovery" and "Shop now" CTA.

- **Active testing phase.** Most ads launched March 20-23, 2026. Low impression counts suggest they're testing multiple creative variations simultaneously — classic rapid creative testing approach.

## Template Recommendations

1. **Highest-priority template: "CHRONIC TINGLING ENDS IN PERMANENT NUMBNESS — STOP IT NOW!"** (Bold Claim, quality 8/10). This layout — big fear headline on colored background + product bottle + checkmark benefits + CTA banner — is the strongest replicable format for any health supplement. **Priority for Lunessa:** swap to "CHRONIC SLEEP DEPRIVATION LEADS TO [CONSEQUENCE] — FIX IT NOW!" with Lunessa bottle.

2. **Competitor Comparison Chart: "Gabapentin's Lies vs. Real Nerve Repair"** (quality 8/10). Two-column checkmark/X format is a proven template. **Priority for Motilli:** create comparison chart vs. common alternatives in Motilli's category.

3. **Testimonial Card with 5-star rating** (quality 7/10). Clean white card + star rating + customer quote + product shot below. This format works across every product category. **Priority: all three brands** should have this template in rotation.

4. **Authority Comparison: "Your Life Back vs. Gabapentin's Prison"** (quality 7/10). Two-column lifestyle comparison with product on the "good" side. **Priority for Velantra:** could adapt as "Fast Fashion Falling Apart vs. Leather That Lasts" comparison.

## Technical Notes

- **Chrome MCP crashed** after a JavaScript blob download attempt triggered on the Meta Ad Library page. The `fetch()` + `blob` + programmatic download approach caused the Chrome extension to become completely unresponsive (all tools timed out for 60+ seconds).
- **Image extraction limitations:** Meta Ad Library images use CORS-restricted CDN URLs (scontent/fbcdn). Canvas export fails with "tainted canvas" errors. Full URLs contain authentication tokens that are blocked by the tool's cookie/query string filters.
- **Recommended approach for next session:** Use right-click > "Save Image As" on individual ad images instead of JavaScript-based download methods. Alternatively, open each ad detail page and use the browser's built-in save functionality.
- **GLP-1 SOS and Auri Labs** were not scraped due to the Chrome crash. These should be prioritized in tomorrow's session (Tuesday rotation normally covers different brands, but these should be caught up first).

## Action Items for Next Session
1. Re-scrape Neurosmile to actually download the 8 branded statics identified above
2. Complete GLP-1 SOS scrape (deferred from today)
3. Complete Auri Labs scrape (deferred from today)
4. Use right-click save method instead of JavaScript downloads
5. Avoid triggering blob downloads via JavaScript — this crashes Chrome MCP
