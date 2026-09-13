# Branded Statics Scrape — 2026-04-20 (Monday rotation)

## Session Status: Partial-success — intel captured, image downloads still blocked

**Target rotation (Monday):** Neurosmile, GLP-1 SOS, Auri Labs (per task description).

---

## Executive Summary

Three brands surveyed cleanly through Meta Ad Library across separate Chrome tabs (one tab per brand, closed and reopened between to follow stability rules). Visual observation succeeded for all three brands — every active branded static was reviewed via screenshot. **Zero image files were downloaded** because the fbcdn signed-URL block, the suppressed right-click context menu, the JS URL output filter, and the tainted-canvas restriction together blocked every extraction path tried (right-click → save, JS → src extraction, JS → canvas → toDataURL, screenshot → cropped re-save). This is the same blocker pattern that has prevented downloads in every session since 2026-04-10.

The richer finding today is **strategic divergence**: the three rotation brands sit on three completely different points of the branded-static spectrum, and that contrast is itself the most valuable intel of the session.

---

## Headline finding — three brands, three creative strategies

| Brand | Active Statics | Strategy | Aesthetic |
|---|---|---|---|
| Neurosmile | 1 (new) | First-ever branded static — premium calm, editorial, anti-stack consolidation angle | Off-white/cream + dark teal product, serif headline, orbital mechanism callouts |
| GLP-1 SOS | 2 (fresh launches Apr 17) | Pattern-interrupt humility ("OFFICIAL APOLOGY") + apothecary ingredient transparency | Forest green, editorial serif, clear-capsule visibility lever, named-competitor displacement |
| Auri Labs | ~5 of ~83 | Anti-branded-static — minimal text overlays on lifestyle/UGC stills + persona authority | Native/editorial — designed layer is intentionally thin |

The contrast matters: Neurosmile and GLP-1 SOS both made deliberate moves *toward* branded design in April. Auri Labs validates the opposite path. For Lunessa/Motilli/Velantra positioning calls, this is the rare day where the rotation actually answers a strategic question — "polished branded design or native-first?" — with three live data points instead of one.

---

## Brand-by-brand

### Neurosmile (1 active branded static — first ever observed)
- **Library 1423138693160512**, launched Apr 7, 2026, status Active (Low impression count).
- **"5 supplements were the problem"** — single bottle centered, serif headline, four mechanism callouts orbiting the bottle. Sub-headline: "Taking them separately meant new worries together. One formula. Everything at clinical doses."
- **Aesthetic shift:** Neurosmile has been 100% video for our entire monitoring history. This is the first branded static to appear. Aesthetic is upscale-clinical/skincare-adjacent — a deliberate departure from the loud red-yellow neuropathy category norm.
- **Copy lever to steal:** "X supplements were the problem → one formula" anti-stack consolidation play. Strong fit for Lunessa (women juggling sleep/hormone routines) and Motilli (gut-stack consolidation).
- **Image saved:** No — Meta CDN blockers (see "Why downloads still don't work").
- **Quality score:** 8/10.

### GLP-1 SOS (2 active branded statics — both new this week)
- **Library 35607854008813009 — "OFFICIAL APOLOGY FROM GLP-1 SOS"** — three bottles on dark forest green, editorial serif headline. Pattern-interrupt humility framing in a category dominated by hype. Quality 9/10.
- **Library 1463067835468733 — "Relief Like Clockwork"** — single clear-capsule bottle in apothecary flat-lay with herbs/ingredients arranged around it. Sub-line "Without the cramping or urgency." Body copy names Miralax directly and claims relief in 48 hours. Quality 9/10.
- **Guarantee shift noted:** Brand has tightened from 60-day → **30-Day "Feel Normal" Guarantee.** Worth tracking — may indicate refund-volume signal or a decision to use specificity to lift conversion.
- **Copy levers to steal:** "OFFICIAL APOLOGY" pattern-interrupt; "Without the [bad side effect]" sub-line construction; named-competitor displacement; visual transparency through clear-capsule packaging; "Feel Normal" specific guarantee language.
- **Images saved:** 0/2 — Meta CDN blockers.

### Auri Labs (aurivita.co — ~83 active image ads, ~5 qualify as branded statics)
- The brand is running a deliberate **anti-branded-static** strategy. Of ~83 active image ads under sub-brand pages (Mark Zillmann, Mushroom Insider, Men's Health Insider, Rob Moore, Dr. Mike Harris, AuriLabs), almost all are UGC/lifestyle stills — bedroom imagery, body close-ups (cracked feet, heel ulcers), person-with-bowl shots, doctor's office interiors.
- The closest things to branded statics are **bold-text overlays on lifestyle photographs**: "70% of heart attack victims had ED first.", "The sign that predicts heart attacks", "The Silent Killer: Endothelial Dysfunction", "Why beetroot itself isn't enough." All link AURILABS.CO with "Learn more" CTA → advertorial funnel.
- **Strategic implication:** Auri Labs validates that scaled brands can win with native-first creative when paired with persona authority + sub-brand fragmentation + advertorial funnels. This is opposite of the GLP-1 SOS / new Neurosmile direction.
- **Recommendation:** Move Auri Labs out of the branded-statics rotation. Their value is in **video / long-form copy / advertorial** intelligence. Pull their copy patterns into long-form-copy and advertorial skills, not the statics catalog.
- **Images saved:** 0 — Meta CDN blockers.

---

## Why downloads still don't work — extraction path audit

Tried four independent extraction paths during the Neurosmile capture attempt. Logged here so the next session can skip dead paths:

1. **Right-click → Save image.** Suppressed. Meta Ad Library blocks the native context menu on ad images.
2. **JS → element.src extraction.** Blocked. The Chrome MCP `javascript_tool` returns `[BLOCKED: Cookie/query string data]` whenever an output value contains a fbcdn URL with query parameters (which is every ad image URL).
3. **JS → canvas → toDataURL.** Blocked by CORS — `Tainted canvases may not be exported.` fbcdn does not serve `Access-Control-Allow-Origin: *` for ad images.
4. **Screenshot → save_to_disk → re-crop in Bash.** Saved files don't appear in the agent sandbox filesystem — `save_to_disk: true` writes to the user's host filesystem only. The screenshots ARE saved on the user's machine but aren't accessible from the agent for cropping/renaming/filing into the brand folder.

**Net:** Four independent extraction paths, all blocked. The fundamental fix is environmental — either an MCP `download` action that writes to the agent sandbox path, or proxy/CORS allowance on fbcdn, or relaxing the JS query-string output filter. None of these are within the agent's control. Continuing to retry won't change the outcome.

---

## Chrome reliability — pattern review (updated)

| Date | Chrome Status | Image Downloads | Intel Captured |
|---|---|---|---|
| 2026-04-10 | OK, slow | 0 (fbcdn signed URL block) | Yes (screenshots) |
| 2026-04-13 | OK with crashes | 0 (same block) | Partial (Neurosmile screenshot lost) |
| 2026-04-17 | OK with crashes + popups | 0 (same block) | Yes (screenshots + IDs logged) |
| 2026-04-18 | Extension offline entire session | 0 | Discovery candidate list only |
| 2026-04-20 | OK, stable across 3 tab cycles | 0 (4 paths blocked) | Yes (3 brands surveyed, 7 statics observed, full metadata) |

Today's session was the most stable Chrome run since the blocker pattern began — three tab-open/tab-close cycles without crash, no popups, no extension dropouts. Stability problem solved; download problem persists.

---

## Recommendations

1. **Escalate the download blocker as a system issue.** Five consecutive sessions with zero image-file deliverables. The agent cannot fix this. Either give the agent an MCP `download` tool that writes to `/sessions/epic-festive-planck/`, or accept that this scheduled task delivers screenshots-on-host + intel-drops only. Update the task description accordingly to remove the "download images" step or mark it as best-effort.

2. **Permanently retire Auri Labs from the Monday branded-statics rotation.** The brand is running a documented anti-branded-static strategy. Replace with a brand where polished design is on-strategy — Bloom Nutrition or Provitalize would be stronger Monday rotation candidates.

3. **Add Neurosmile + GLP-1 SOS to a "weekly track" list.** Both brands launched fresh statics this week (Apr 7 / Apr 17). Worth a re-survey in 7 days to see what variants follow.

4. **Track the GLP-1 SOS guarantee shift (60-day → 30-day).** Specific change — likely meaningful signal. Note in the next intel drop whether it persists.

---

## Images Downloaded

**Total:** 0 image files saved to `/sessions/epic-festive-planck/mnt/marketing brain/statics/branded_statics/`.

**Why:** All four extraction paths blocked. See "Why downloads still don't work" section above.

---

## Catalogs Updated

| Brand | Catalog file | Updated |
|---|---|---|
| Neurosmile | `/statics/branded_statics/neurosmile/catalog.md` | Yes — first-ever branded static logged |
| GLP-1 SOS | `/statics/branded_statics/glp1_sos/catalog.md` | Yes — 2 fresh statics added, guarantee shift noted |
| Auri Labs | `/statics/branded_statics/auri_labs/catalog.md` | Yes — strategy reframe, deprioritization noted |

---

## Summary Table

| Brand | Ads Surveyed | Branded Statics Found | Quality Score | Images Saved | Catalog Updated |
|---|---|---|---|---|---|
| Neurosmile | 1 | 1 (new) | 8/10 | 0 | Yes |
| GLP-1 SOS | 2 | 2 (new) | 9/10 each | 0 | Yes |
| Auri Labs | ~83 | ~5 (text-overlay only) | 6-7/10 | 0 | Yes |
| **Totals** | **~86** | **~8** | — | **0** | **3** |

**Session Quality:** High intel value, zero image-file deliverables. Most strategically rich Monday-rotation session in the recent history because the three brands sit at three different points on the branded-design spectrum.

---

## Top Template Recommendation (single highest-leverage takeaway)

**For Lunessa: Steal the GLP-1 SOS "OFFICIAL APOLOGY" pattern-interrupt headline framing on a polished branded background.**

The supplement category is overrun with hype openers. Humility framing on a designed branded static is rare, distinctive, and immediately reads as different. Pair the format with Neurosmile's anti-stack consolidation copy lever ("X products were the problem") and the result is a Lunessa concept that breaks from category norms on both layers — design and headline. Worth a fresh-concept push next sprint.

---

## Action Items for Next Run (2026-04-21, Tuesday rotation)

1. Tuesday rotation per task description: **Primal Viking, GleeFull, Primal Queen.**
2. Skip download attempts unless an MCP `download` tool is added — file screenshots-on-host + intel only.
3. Re-survey Neurosmile and GLP-1 SOS in ~7 days to track variant evolution.
4. Note whether GLP-1 SOS guarantee language stays at 30-day or shifts again.

---

## Sources

- [Meta Ad Library — Neurosmile keyword search](https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=US&q=Neurosmile&search_type=keyword_unordered&media_type=image)
- [Meta Ad Library — GLP-1 SOS keyword search](https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=US&q=GLP-1%20SOS&search_type=keyword_unordered&media_type=image)
- [Meta Ad Library — Auri Labs keyword search](https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=US&q=Auri%20Labs&search_type=keyword_unordered&media_type=image)
- Neurosmile FB page: https://www.facebook.com/tryneurosmile/
- GLP-1 SOS FB page: https://www.facebook.com/glpsossuppls/
