# 2026-05-05 — Branded Statics Scrape (Tuesday Rotation)

**Brands scraped:** Primal Viking, GleeFull, Primal Queen
**Operator:** Market Analyst (scheduled task)
**Session conditions:** Two Chrome tab disconnects mid-session; no full crashes. Image-download path fully blocked again (Meta CDN: cookie/query-string filter on JS, tainted canvas, suppressed right-click). All updates this run are observation-only.

---

## Summary

- **Net new creative across all three brands today:** 0 ads
- **Library IDs visible today vs Sunday's scrape:** ~100% overlap on Primal Viking and Primal Queen
- **GleeFull:** zero image-ad results across six keyword variants — first time we've seen the brand fully out of the image-search index. Either they paused image creative or the keyword index dropped them
- **No new images downloaded to disk this run** (CDN extraction fully blocked — same as 5/3 and 5/4 sessions)

The Tuesday brand set is in a steady-state period. Primal Viking has stabilized after its April refresh, Primal Queen has stabilized after its May 1 launch, and GleeFull is either dark on image creative or temporarily un-indexed. This is a "no new news" day — but the absence of new news is itself the signal: these brands are not in fresh-creative mode this week.

---

## Brand-by-brand observations

### Primal Viking
- **~16 active image ads** (unchanged from 5/3)
- All 10 visible Library IDs match the 5/3 scrape — same "BREAKING NEWS" microscope clinical statics (Library 2321360358332057 from Feb 12 still running — now 12+ weeks continuous), same SEM hair-shaft (896220413400170), same UGC-overlay urgency family
- The barbell strategy (highly-designed clinical at the top + native UGC at the bottom, no middle ground) is holding
- **Quality assessment:** Library 2321360358332057 remains the strongest single asset in the brand's library — 9/10. The clinical chassis with red "BREAKING NEWS" bar + black-headline-block + microscope-photo is a 12-week winner

### GleeFull
- **Zero image ads returned** across six keyword variants ("gleefull", "glee full", "gleefull supps", "menopause but better", "meno-shred", "over 30 hormone support")
- The "over 30 hormone support" search returned ~9,800 results — predominantly Solūma, Luminere Organics, North Valley Health Clinic, Lymphoria, and a "Dr. Emily Carter" persona — but no GleeFull
- **Hypothesis:** Either GleeFull rotated all image creative off this week, or their indexed keywords have shifted away from the terms we've been using. Try direct page-ID navigation on next rotation
- **Incidental discovery:** The "Over 30 Hormone Support" keyword space is now crowded with polished competitive statics from Solūma, Luminere Organics, and Lymphoria — worth a discovery-day scrape on Saturday

### Primal Queen
- **~81 active image ads** (vs ~85 on 5/3 — essentially flat)
- Same Amy Snyder native-UGC long-form-text family from 5/3
- Same May 1 GLP-1 narrative cluster (wedding dress, McDonald's drive-thru, personal trainer)
- Same single polished branded static (Library 2479754395760248 — dark beef organs gradient with editorial CTA card; Feb 20 start date = 11+ weeks running)
- "GLP-1 Support From Mother Nature, Not a Lab" CTA positioning is sticky across all May 1 creatives — major repositioning vs 4 weeks ago when the brand was "energy + vitality"

---

## Cross-brand design trends spotted

1. **The "BREAKING NEWS" editorial chassis is now a category template.** Both Primal Viking (Library 2321360358332057) and Primal Queen (Library 2479754395760248) — same shared design vendor or one cloned the other. Red bar + white headline block + circular microscope photo + brand CTA card. Both are 11–12 week runners. Strongest evidence yet that this is a winning template, not a one-off.

2. **The barbell strategy is becoming a category default.** Primal Viking, Primal Queen, and (per 5/3 catalog) GleeFull are all running highly-designed clinical statics at the top of the rotation alongside near-native UGC in the body. The middle ground (text-overlay-on-product-photo) is dying across brands.

3. **Long-form personal narrative is now in image ads, not just video.** Primal Queen's May 1 launch wave puts 200+ word first-person narratives in the primary text of static UGC ads. The static is just casting; the persuasion is the text. This breaks the prior assumption that static = short copy.

4. **GLP-1 alternative positioning is the new battleground.** Primal Queen's PQ7 "natural GLP-1 alternative" CTA is sticky. Watch for Lunessa/Motilli/Velantra-adjacent competitors to start running the same language.

---

## Template recommendations (priority order)

### #1 — Lift the "BREAKING NEWS" chassis for our portfolio
- Cross-brand confirmed winner (Primal Viking + Primal Queen, both 11–12 week runners)
- Layout: red horizontal bar with "BREAKING NEWS" white text → black headline block with white type → circular microscope/cellular photo → brand CTA card below
- **For Lunessa:** Swap microscope photo to brain-cell or hormone-receptor visual; headline = "Woman Reveals Decades of 'Empty Sleep' Triggered Hormonal Burnout"
- **For Motilli:** Swap to gut-bacteria/microbiome visual; headline = "Doctor Reveals Why 1 in 3 Women Have a 'Sleeping' Microbiome After 35"
- **For Velantra:** Swap to mitochondria/cellular-energy visual; headline = "Researchers Discover Why Caffeine Quit Working After 30"

### #2 — Steal the Primal Queen "dark gradient + CTA card" minimalism
- Library 2479754395760248 has been running 11+ weeks with a near-empty image (black + red center glow)
- The persuasion is entirely in the CTA card text below
- Cheap to produce, durable in rotation
- **For Velantra:** Black background + amber center glow + CTA card "Why caffeine quit working — and what's replacing it"

### #3 — Adopt the long-form-narrative-on-static format
- Primal Queen's May 1 launch proves this works for image ads (not just video)
- 200+ word first-person primary text + casting-photo image
- **For Lunessa:** Burnout-mom narrative ("I used to be sharp. Now I cancel plans...")
- **For Motilli:** Gut-distress narrative ("I'd had lunch an hour earlier. But I was already in the McDonald's drive-thru...")

---

## Action items for next sessions

- [ ] **Saturday discovery day:** Scrape Solūma, Luminere Organics, Lymphoria — these are now competing in the same hormone-support category as GleeFull and may be gaining share
- [ ] **Sunday Tier-1 re-scrape:** Try direct page-ID navigation for GleeFull (keyword search has stopped surfacing the brand)
- [ ] **Engineering ask:** The image-download blockers (CDN cookie filter, tainted canvas, suppressed right-click) have now blocked downloads on 4 consecutive sessions. We need either a different capture path (full-viewport screenshot crop pipeline, or a server-side extension that fetches Meta CDN URLs with proper auth headers) or to accept that observation-only updates are the new default for this agent

---

## Chrome stability notes
- Two tab disconnects during the GleeFull → Primal Queen transition. Both recovered within ~10 seconds via tabs_context_mcp.
- No full Chrome crashes this session.
- Followed one-tab-at-a-time rule strictly. Closed tab between brands.
