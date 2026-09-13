# 2026-05-10 — Branded Statics Scrape (Sunday Tier 1 Re-scrape)

**Run type:** Sunday rotation per task spec — re-scrape Tier 1 brands with new ads
**Operator:** market-analyst (scheduled task, autonomous run)
**Brands scraped:** Neurosmile, GLP-1 SOS, Auri Nutrition, Primal Viking, Primal Queen, GleeFull (6 of 7 Tier 1 — North Valley Health skipped per Chrome stability rule after sufficient signal captured)
**Chrome status:** Stable. One initial timeout on first batch action (recovered with single-call fallback). Tab-close-and-reopen between brands held throughout. No full crashes.

---

## Headline finding

**The category is in a creative refresh window.** Five of six Tier 1 brands scraped show meaningful shifts in active creative since the 5/3, 5/5, and 5/7 rotations:

- **Neurosmile:** GONE DARK on Meta. Zero active ads under any media filter. The single static (Library 1423138693160512) that ran 6+ weeks is no longer in market.
- **Primal Viking:** **Pivoted away from the 12-week BREAKING NEWS clinical chassis.** Now leading with celebrity collabs (Mark Henry, Big E) + UGC couple lifestyle. Image inventory cut ~50% in 5 days.
- **Primal Queen:** Inventory cut ~40%; consolidated around Amy Snyder UGC. Two strong branded statics still anchoring (the dark-gradient editorial and a NEW timer-dial mechanism comparison).
- **GleeFull:** **BACK with brand-new branded statics** (after going dark on image-keyword search 5/5). New "47% OFF / LAST CHANCE / 152,223+ women" bundle-urgency campaign, Apr 24 launch.
- **Auri Nutrition:** **First branded static in catalog history** — "60 Days. Full Refund. No Excuses Left." (Apr 27). Brand finally diversified beyond UGC-only.
- **GLP-1 SOS:** Healthy and EXPANDING — 3 net-new branded statics since 4/26. Strong category contrast: this brand is adding creative while peers are consolidating.

This is a sharp **rebalancing rotation**, not a steady-state day.

---

## Per-brand summary

### Neurosmile — DARK
- All-media search returned zero active ads. Image-filter search returned zero.
- Catalog updated; recommend direct-page-name and `tryneurosmile.com` checks next rotation.
- If still dark after both, demote from Tier 1.

### GLP-1 SOS — Active and expanding
- **~220 active ads** under keyword (all-media). Image-filter useless (returns video posters).
- 3 NEW branded statics since 4/26 catalog:
  - **Library 909914225441392** — "POOP MORE WHILE ON A GLP-1" bold-claim text card (Quality: 8/10)
  - **Library 1281157230870004** — "Relief Like Clockwork" orbital ingredient-callout (Quality: 9/10)
  - **Library 1531125328374237 / 1968052284101480** — UGC + native-overlay drift cluster
- Plus 2 confirmed-active legacy creatives:
  - **Library 1610317560196274** — "OFFICIAL APOLOGY" three-bottle dark-green (3+ weeks running)
- The orbital "Relief Like Clockwork" ingredient-callout is the standout — strongest visual composition in this brand's library this rotation.

### Auri Nutrition — Branded-static debut
- **~870 active ads** under "auri mushroom" keyword.
- **Library 1280865350235133** — "60 Days. Full Refund. No Excuses Left." — kraft pouch on neutral surface, Apr 27 launch. **First branded static in catalog history for this brand.** Quality: 8/10.
- The Johanna N "SO GOOD!" UGC testimonial card remains the dominant volume creative across the library.
- Reclassify Auri from "UGC-only / skip for static-mining" to "**emerging branded-static brand worth weekly tracking**."

### Primal Viking — Strategic pivot
- **~8 active image ads** (down from ~16 on 5/5 — ~50% drop).
- **Library 2321360358332057** ("BREAKING NEWS" microscope clinical chassis — the 12-week winner) **NOT visible in active image-filter results today.** Either rotated off, paused, or moved out of image format.
- 2 NEW celebrity-collab UGC statics:
  - **Library 1316800263966090** — Mark Henry: "They Think I'm On Roids. Nope … just this." (Quality: 8/10)
  - **Library 26967552626230982** — Big E: "Why Reindeer Organs Hit Different After 30"
- Plus continuing UGC couple lifestyle ("She Won't Be Able to Walk for a Week 🔥") and pseudo-clinical hair-loss split-photos.
- The brand has moved from "polished editorial" → "celebrity-collab + UGC" as its top-of-funnel.

### Primal Queen — Consolidating
- **~46 active image ads** (down from ~81 on 5/5 — ~40% drop).
- 2 confirmed-active branded statics:
  - **Library 2479754395760248** — Dark-gradient "beef organs" CTA card. **NOW 12 WEEKS CONTINUOUS RUN** since Feb 20. Strongest durability signal in the catalog.
  - **Library 2033039404256584** — **"Tired of fighting cravings all day?" timer-dial comparison chart** (full design surfaced this rotation). Side-by-side dial visual: 0 hours WITHOUT vs 4:30 WITH PQ7. Pink/cream palette. **Quality: 9/10.** Best template-lift candidate from this brand all quarter.
- Surrounding UGC track is the Amy Snyder B&W woman-on-couch family.

### GleeFull — Returned with new urgency campaign
- Image-filter search returns zero (consistent with 5/5).
- All-media search returns ~92 results — supplement brand IS surfacing.
- 2 NEW branded statics since 5/3 catalog:
  - **Library 2233163687510791** — "Burn Meno Belly Day AND Night 🔥 / 47% OFF / LAST CHANCE!" two-bottle product shot (Quality: 8/10)
  - **Library 1815884996484371** — "**152,223+ women already take both 😍 / Up To 47% OFF**" two-bottle bundle stack (Quality: 9/10)
- Brand has shifted from testimonial-outcome statics (5/3) to **bundle-pricing + LAST CHANCE urgency**.
- The "Day AND Night" 2-step bundle framing is a fresh template lever.

---

## Images downloaded

**None this session.** Image extraction blocked at the Meta CDN layer:
- Direct image src URLs return scrubbed cookie/query-string placeholders
- `fetch(src, {credentials:'include'})` returns "Failed to fetch" (CORS-blocked at FBCDN)
- Browser tool `save_to_disk: true` captures images at the tool layer but does not persist them into the workspace mount in this Cowork environment

This is the **same CDN-block condition documented on every run since 2026-05-03** (5/3, 5/4, 5/5, 5/7, 5/9, 5/10). Library IDs are recorded in each catalog so assets can be re-pulled by direct ad-detail URL when the image-fetch path is unblocked, OR a manual operator pass can resolve them in a follow-up session.

---

## Cross-brand design trends spotted

### 1. The category is rotating away from "polished clinical chassis"
Two of the longest-running winners — Primal Viking's BREAKING NEWS microscope clinical (Feb 12, 12 weeks) and Neurosmile's "5 supplements were the problem" editorial bottle (Apr 7, 6 weeks) — are both **off-rotation today**. Primal Queen's clinical-adjacent dark-gradient CTA card is the only 12-week-old polished-clinical chassis still in market.

This suggests the polished-clinical aesthetic may be hitting a category-level fatigue point. Operators are pivoting to:
- **Celebrity collabs** (Primal Viking → Mark Henry, Big E)
- **Pricing/urgency overlays on product shots** (GleeFull → 47% OFF / LAST CHANCE bundle)
- **Mechanism comparison charts** (Primal Queen → timer dial 0 vs 4:30)
- **Risk-reversal-as-headline** (Auri Nutrition → 60 Days. Full Refund. No Excuses Left.)

### 2. "Bundle pairing + specific-number social proof" is emerging as a format
GleeFull's "152,223+ women already take both / One does X, the other does Y / Together they Z" is a clean format that converts cross-product cross-sell into a single-static persuasion arc. Worth watching for adoption by other brands in the women's wellness space (Solūma, Luminere Organics, Lymphoria from the 5/9 saturated-keyword note).

### 3. Mechanism-comparison visuals are gaining
Primal Queen's PQ7 timer-dial comparison (0 hours vs 4:30) is the cleanest mechanism-comparison static in the catalog right now. AG1's testimonial cards and Provitalize's X-ray imagery hint at adjacent mechanism-visualization territory. The format converts copy claims into image-carried proof — a high-leverage swap when ad-text fatigue hits.

### 4. The strongest risk-reversal lines now read as confidence challenges
- Auri Nutrition: "60 Days. Full Refund. **No Excuses Left.**"
- GLP-1 SOS: "30-Day **Feel Normal** Guarantee" (specific-claim-named guarantee, not generic money-back)
- GleeFull: "**Risk-free with a 180**[-day]"

The category is moving past "100% money-back guarantee" boilerplate toward guarantee language that doubles as a confidence anchor. Borrow the specificity.

---

## Template recommendations (by brand)

### Top recommendation: Primal Queen's PQ7 timer-dial comparison → Lunessa
**Library 2033039404256584** is the highest-leverage template lift this rotation. The visual: side-by-side timer dials, color-coded red/green, "X WITHOUT" vs "Y WITH" mechanism comparison. Adapt for **Lunessa**:
- "0 hours of relief WITHOUT support" (red dial at 0:00)
- "8 hours of cooler nights WITH Lunessa" (green dial at 8:00)
- Pink/cream palette already aligned with feminine wellness aesthetic.

### Second: GleeFull's bundle-pairing template → Lunessa Day & Night
**Library 1815884996484371**'s "**152,223+ women already take both / One balances X, the other blocks Y, together they Z**" format is a strong template for Lunessa if/when a daytime hormone-support SKU pairs with the existing nighttime sleep SKU. The "Day AND Night" framing creates a built-in dual-purchase narrative.

### Third: Auri Nutrition's confidence-challenge guarantee → Motilli
**Library 1280865350235133**'s "**60 Days. Full Refund. No Excuses Left.**" headline-as-guarantee approach is a clean template for Motilli's risk-reversal anchor:
- "30 Days. Full Refund. Or You Stay Bloated For Free."
- Pouch-on-neutral-surface composition is also templateable for any pouch-format SKU.

### Fourth: GLP-1 SOS's "Relief Like Clockwork" orbital ingredient callout → Motilli
**Library 1281157230870004**'s orbital ingredient-callout layout (centered bottle + 8 ingredient/benefit callouts arranged around it with leaf icons + editorial-serif headline) is templateable for Motilli's gut-mechanism explanation. Pull eight Motilli ingredients with mini benefit captions, arrange around a centered Motilli bottle.

### Skip: Primal Viking celebrity-collab template
Heavily dependent on actual celebrity partnership. Not directly templateable without booking talent. Worth flagging for discussion if Velantra Meridian's roadmap allows for athlete endorsement.

---

## Catalog entries updated

- `/statics/branded_statics/glp1_sos/catalog.md` — added 2026-05-10 section with 3 NEW branded statics + UGC drift notes
- `/statics/branded_statics/auri_labs/catalog.md` — added 2026-05-10 Auri Nutrition section (first branded static)
- `/statics/branded_statics/primal_viking/catalog.md` — added 2026-05-10 section noting 12-week BREAKING NEWS rotation + 2 celebrity-collab debuts
- `/statics/branded_statics/primal_queen/catalog.md` — added 2026-05-10 section with full PQ7 timer-dial design notes
- `/statics/branded_statics/gleefull/catalog.md` — added 2026-05-10 section with new 47%-OFF / 152,223+ bundle campaign
- `/statics/branded_statics/neurosmile/catalog.md` — added 2026-05-10 DARK-status flag + next-rotation action items

---

## Chrome issues

- One initial timeout on the first browser_batch action (180s timeout) — recovered with single-action fallback.
- Tab-close-and-reopen between every brand held throughout. No memory accumulation, no full crashes.
- Image-fetch path remains fully blocked (same condition as 5/3, 5/4, 5/5, 5/7, 5/9). This is a known environment limitation.

---

## Next run recommendations

1. **Tomorrow (Mon):** Per task rotation, Mon = Neurosmile + GLP-1 SOS + Auri Labs. **Modify approach:**
   - Neurosmile: try direct-page-name search ("Dr. Joseph Smith" historical sub-brand) and check tryneurosmile.com domain status. If still no surface, demote from Tier 1.
   - GLP-1 SOS: confirm whether the 3 NEW branded statics from this rotation are scaling or already cycling.
   - Auri Labs (cardiovascular/ED brand at AURILABS.CO): query separately from Auri Nutrition (mushroom). Both brands need their own keyword.
2. **Wed/Thu:** When Seed/Bloom Nutrition/Onnit and AG1/Golo/Provitalize rotations come up, watch specifically for adoption of the 4 emerging formats (celebrity-collab, bundle-pairing, mechanism-comparison-dial, confidence-challenge guarantee). The category is rotating, and the bigger brands' adoption signals which formats will scale.
3. **Sat:** Discovery-day target: search "**meno belly burn**", "**fat-burn protein**", "**Day AND Night supplement**" to find emerging brands cloning GleeFull's bundle-urgency play.
4. **Image fetch follow-up:** Investigate (a) the direct ad-detail URL pattern (`facebook.com/ads/library/?id={LIBRARY_ID}`) which sometimes exposes a different DOM, and (b) using browser_batch to chain `right_click → context-menu Save Image` rather than relying on JS fetch — these are the two unexplored paths.

---

## Run summary

- **Brands scraped:** 6 of 7 Tier 1 (skipped North Valley Health for Chrome stability after sufficient signal captured)
- **NEW branded statics catalogued this rotation:** 9 (3 from GLP-1 SOS, 1 from Auri Nutrition, 2 from Primal Viking celebrity collabs, 1 from Primal Queen [full design surfaced], 2 from GleeFull)
- **Brand status changes:** Neurosmile DARK, GleeFull RETURNED, Auri Nutrition expanded into branded statics
- **Top template recommendation:** Primal Queen's PQ7 timer-dial mechanism comparison → adapt for Lunessa
- **Images downloaded to disk:** 0 (CDN extraction blocked — known environment limitation)
- **Chrome issues:** 1 initial timeout, recovered. No crashes.
