---
type: session-transcript
date: 2026-05-09
session_id: local_0813d89c-655a-47a8-81d6-ee4970dbc70e
title: "Market analyst branded statics scraper"
tags:
  - session-log
  - transcript
  - market-analyst
  - branded-statics
  - scraper
  - bloom-and-bond
  - nuvara
  - provitalean
  - hair-loss
  - glp-1-damage
---

# Session Transcript: Market analyst branded statics scraper

**Date:** 2026-05-09
**Session ID:** local_0813d89c-655a-47a8-81d6-ee4970dbc70e
**Status:** idle

---

[assistant] (called mcp__Claude_in_Chrome__tabs_close_mcp)
[assistant] (called mcp__Claude_in_Chrome__tabs_context_mcp)
[assistant] (called mcp__Claude_in_Chrome__navigate)
[assistant] (called mcp__Claude_in_Chrome__browser_batch)
[assistant] ~330 results for Bloom & Bond. The images I'm seeing are mostly NATIVE/UGC-style images (woman lifting shirt, hair photos, etc.). These do NOT qualify as branded statics per the 8 archetypes. Bloom & Bond appears to be running native-style image ads, not polished branded statics. Let me scroll down briefly to see if there are any branded statics deeper in.
[assistant] (called mcp__Claude_in_Chrome__browser_batch)
[assistant] Confirmed: Bloom & Bond is running pure native/UGC images — they don't qualify as branded statics. The deeper results are unrelated (Romance Novels, etc.).

Bloom & Bond is a NO for branded statics. Let me capture screenshots of the Bloom & Bond ads I see (since they're the brand's actual creatives — even native images can be cataloged in a separate native_ads pool, but per the task scope, I need branded statics only). I'll move on.

Let me close and try the next candidate brand. Let me check whether the existing **nuora** folder has anything (similar to Nuvara — could be variant) and try Nuvara.
[assistant] (called mcp__Claude_in_Chrome__tabs_close_mcp)
[assistant] (called mcp__Claude_in_Chrome__tabs_create_mcp)
[assistant] (called TaskUpdate)
[assistant] (called TaskUpdate)
[assistant] (called mcp__Claude_in_Chrome__tabs_context_mcp)
[assistant] (called mcp__Claude_in_Chrome__navigate)
[assistant] (called mcp__Claude_in_Chrome__browser_batch)
[assistant] No direct match for "Nuvara wellness". Let me try just "Nuvara".
[assistant] (called mcp__Claude_in_Chrome__browser_batch)
[assistant] Nuvara has 19 results. They're running the SAME advertorial-style image — a graphic showing "hair loss due to GLP-1" with a clinical illustration of follicles + a close-up before/after image. This QUALIFIES as a branded static — specifically archetype #7 (Medical/Clinical Proof) blended with #6 (Before/After Visual). Let me click into one to see the full image and download it.
[assistant] (called mcp__Claude_in_Chrome__browser_batch)
[assistant] The click triggered a "Learn more" navigation (opened a Nuvara landing page in a new tab). Let me close that landing page tab and instead use a different approach. The Nuvara ad images are clearly visible. Let me use JavaScript to extract image URLs directly from the ad cards rather than clicking.
[assistant] (called mcp__Claude_in_Chrome__tabs_close_mcp)
[assistant] (called mcp__Claude_in_Chrome__javascript_tool)
[assistant] The image URLs are blocked from my view (cookie/query strings), but I can capture the screenshot crops directly. Let me use the zoom action to capture each Nuvara ad image at the highest fidelity, then save those screenshots as the static assets.
[assistant] (called mcp__Claude_in_Chrome__browser_batch)
[assistant] The zoom captures are showing the lower half of the cards (image bottom + button area). The crops aren't capturing the full image. Looking at the screenshot — these aren't strongly "branded statics" — they're more like advertorial/UGC native-style images. Nuvara/Sophie's Natural Health Guide is running clinical illustrations + before/after photo composites, but the layout is editorial, not designed-graphic with text overlays/pricing/charts.

This brand technically uses ONE archetype (medical/clinical illustration + before/after) but very loosely. Per the strict criteria, this is a borderline case. Let me note it as such, save the catalog entry, then move on. The image URL extraction is blocked, so I need to capture full ad images via screenshot of the card itself.

Let me try clicking "See ad details" instead which usually opens a modal with the full image accessible.
[assistant] (called mcp__Claude_in_Chrome__browser_batch)
[assistant] (called mcp__Claude_in_Chrome__tabs_context_mcp)
[assistant] Page recovered. Let me change strategy — I'll capture the FULL ad cards as screenshots (entire card with image and text) and save those as the static archive entries. That's actually more useful than just the image since it shows the brand context.
[assistant] (called mcp__Claude_in_Chrome__computer)
[assistant] The Ad Details modal is now open showing the Nuvara ad clearly — clinical illustration of follicles + Library ID 2022964021986552. This IS a clean clinical/medical archetype branded static. Let me capture this image at full quality.
[assistant] (called mcp__Claude_in_Chrome__computer)
[assistant] Got a clean capture of the Nuvara clinical illustration. Saved to disk. Let me find where the screenshot was saved and copy to the brand folder.
[assistant] (called mcp__workspace__bash)
[assistant] Screenshots saved via the browser tool aren't appearing in my mounted filesystem. The save_to_disk likely puts them in a Chrome-managed location I can't reach from the workspace. Let me change strategy: since image extraction via URL is blocked and zoom screenshots aren't accessible to my filesystem, I'll need to take a different practical approach — create comprehensive **catalog.md entries** documenting what I observed in the Ad Library, including Library IDs, ad copy, and visual descriptions. The brand folders already exist, and a robust catalog with Library IDs and visual specs is more valuable than just images for a strategist's reference.

Given Chrome stability rules and that this is a discovery day with limited new branded statics found, let me close out the browser work, document everything observed, and write the intel drop.
[assistant] (called TaskUpdate)
[assistant] (called TaskUpdate)
[assistant] (called mcp__Claude_in_Chrome__tabs_close_mcp)
[assistant] (called mcp__Claude_in_Chrome__tabs_context_mcp)
[assistant] (called mcp__Claude_in_Chrome__navigate)
[assistant] (called mcp__Claude_in_Chrome__browser_batch)
[assistant] **Provitalean** (REJUVEEN.COM) — 8 active image ads. The images shown are:
- X-ray/medical imagery (Library 1671329217192526) — Clinical archetype
- Casual lifestyle/UGC photos (women in homes/stores)
- Before/after composites (women side-by-side)

The X-ray clinical illustration IS a branded static (clinical archetype). The before/afters are also branded static archetype #6. But the rest are native-style. Two card images are clearly different from native UGC.

Provitalean QUALIFIES with 2 archetypes spotted: clinical (X-ray) and before/after side-by-side. Let me close this tab and finalize the work — I have enough data to write a meaningful intel drop and catalog entries.
[assistant] (called mcp__Claude_in_Chrome__tabs_close_mcp)
[assistant] (called TaskUpdate)
[assistant] (called TaskUpdate)
[assistant] Now let me check existing catalog files to match format, then write entries.
[assistant] (called mcp__workspace__bash)
[assistant] Good — the catalog format is established. The "Nuvara" I was finding is actually a separate brand from Nuora — different domain (NUVARAWELLNESS.COM vs mynuora.com). Let me check if a Nuvara folder needs creating.
[assistant] (called mcp__workspace__bash)
[assistant] Nuvara doesn't exist (Nuora is a different brand). Provitalize exists but Provitalean is a different brand (REJUVEEN.COM). Let me check the provitalize catalog and create new folders for Nuvara and Provitalean.
[assistant] (called mcp__workspace__bash)
[assistant] Now let me write the catalog files. First the Nuvara catalog:
[assistant] (called Write)
[assistant] (called Write)
[assistant] (called Write)
[assistant] (called TaskUpdate)
[assistant] (called TaskUpdate)
[assistant] Now write the intel drop:
[assistant] (called Write)
[assistant] (called TaskUpdate)
[assistant] All tasks complete. Browser is already closed. Final summary:

## Run Summary — 2026-05-09 Statics Scrape

**Brands scraped:** 3 (Saturday discovery rotation)
- **Bloom & Bond** (bloomandbonds.com) — does NOT qualify; runs native/UGC only. New folder created with non-qualifying verdict.
- **Nuvara / Sophie's Natural Health Guide** (nuvarawellness.com) — qualifies. New folder. Clinical follicle illustration + before/after archetypes documented (9 Library IDs captured).
- **Provitalean** (rejuveen.com) — marginal. 2 of 8 ads qualify (X-ray clinical + side-by-side before/after). New folder, 5 Library IDs captured.

**Images downloaded:** 0. Image URL extraction was blocked by FB CDN cookie/auth gating, and browser screenshot save_to_disk did not surface files into the workspace mount in this scheduled-task environment. **Library IDs preserved in each catalog for re-pull.** Flagged in intel drop for engineering follow-up.

**Top template recommendation:** Adapt Nuvara's split-panel medical-illustration archetype (#7 Clinical Proof) for **Lunessa** as a "receptor cross-section" static — open lane in menopause vertical.

**Design trend:** Anti-GLP-1-damage angle is now a category, not a niche. Operators are differentiating on **rendered clinical illustration** (Nuvara, Provitalean) as a pattern-interrupt against the UGC-saturated feed.

**Chrome stability:** Stable run. One initial connection blip, one click-induced 180s timeout — both recovered. All tabs closed at end.

**Files created:**
- [Nuvara catalog](computer:///Users/brooksorradre2/Documents/marketing%20brain/statics/branded_statics/nuvara/catalog.md)
- [Provitalean catalog](computer:///Users/brooksorradre2/Documents/marketing%20brain/statics/branded_statics/provitalean/catalog.md)
- [Bloom & Bond catalog](computer:///Users/brooksorradre2/Documents/marketing%20brain/statics/branded_statics/bloom_and_bond/catalog.md)
- [Intel drop 2026-05-09](computer:///Users/brooksorradre2/Documents/marketing%20brain/agents/market-analyst/intel-drops/2026-05-09_statics-scrape.md)
