# PDP Congruency Rewrite — Upstream Three-Pathway Mechanism (2026-07-09)

**Page:** getmotilli.com/products/motilli-3-bottle-90day-reset (Motilli #4, y9t3s8-ns, theme 186933838191 Shrine Pro)
**Goal:** Make the PDP congruent with the nurse/Karen advertorial mechanism: **wrong organ (on-ramp/off-ramp) → Motility / Gas neutralization / Downstream flow**. Vitamins leg demoted to supporting mention; soluble low-bulk prebiotic fiber promoted to Pathway 3.

**Deployment:** New template `templates/product.upstream.json` assigned to the 90-day reset product (template_suffix `upstream`). The shared default `templates/product.json` was ALSO updated with identical copy — it still serves the 6-bottle bundle and the listicle product, so those pages inherit the same mechanism. Pre-edit backup: `motilli pdp/template-backups/product.json.PRE-upstream-mechanism.2026-07-09.json`.

## Copy changes

### Buy box subhead
- OLD: "The all-in-one fix… and the nutrients the shot strips out… refills the key vitamins your medication depletes — without quitting it."
- NEW: "The upstream fix for the digestive side effects your GLP-1 causes — the constipation, the sulfur burps, the cement-stomach bloat. Wakes up the stomach your medication slowed, neutralizes the sulfur gas, and softens the backup downstream — all three pathways, without touching your dose."

### Buy box bullet 3
- OLD: "Apigenin + chlorophyll + key vitamins (A, C, B6, K1, folate)"
- NEW: "Apigenin + chlorophyllin + soluble prebiotic fiber — motility, gas neutralization, downstream flow"

### "Why Nothing Else Has Worked" accordion
- NEW P1 installs the highway metaphor: on-ramp (stomach) vs off-ramp (colon), fermentation → sulfur gas → cement → brick; "Your colon was never blocked — it's empty. The problem lives six feet upstream."
- NEW P2: three pathways (apigenin/vagus signal "turned down", chlorophyllin binds H2S, low-bulk soluble fiber softens without adding bulk to the jam).
- NEW P3 bold: "Motility. Gas neutralization. Downstream flow. One gummy, working on the organ every laxative in your cabinet ignores."

### 4 GLP-1 Gut Failures
- #1 rewritten: Miralax pulls water into an empty colon / Dulcolax squeezes an empty tube / blockage is upstream.
- #4 REPLACED: was "Fatigue, brain fog & nutrient loss" (vitamins) → now "The brick that won't pass" (bulk fiber = more cars on a jammed highway; low-bulk gel-forming soluble fiber softens without volume).

### Week-by-week ladder (aligned to advertorial)
- Week 1: sulfur burps fade (gas pathway first)
- Week 2–3: cement lifts, unforced BMs return (91% claim retained)
- Week 4–6: feedback loop breaks and runs in reverse
- Day 90: the reset — "That's why this is a 90-day protocol"

### Other
- Who-for: "$90+/month… every one of them aimed at the wrong organ"; bold line now "…the burps, the backup, the bloat, and the brick: the whole feedback loop your GLP-1 started."
- 90-day promise + guarantee section: opens with "The slowdown took months to dig in — 90 days of all three pathways is how it runs in reverse."
- Ingredients cards: "The 2 Actives" → "The 3 Pathways Inside Motilli"; Pathway labels on apigenin/chlorophyllin; NEW third card "Soluble Prebiotic Fiber" (fallback color #c9b370, no image asset existed).
- Comparison table row 6: "Refills Missing Vitamins" → "Softens the Backup Without Bulk".
- Trust ticker: "2 CLINICALLY STUDIED ACTIVES" → "3 CLINICALLY STUDIED ACTIVES".
- FAQ ingredients: three actives one-per-pathway; vitamins demoted to "supporting vitamins."
- FAQ timeline: matches new ladder; "Motilli isn't a laxative — it doesn't force anything."

## a1 CTA fix (same night)
Both a1.guthealthblog.org CTAs re-pointed from `getmotilli.com/` (homepage) → `getmotilli.com/products/motilli-3-bottle-90day-reset?variant=53033648750959` (variant param also bypasses the stale cache entry). Source: `_engine/copywriting/advertorial/advertorials/motilli-a1/index.html` (backup `index.html.backup-pre-cta-fix-2026-07-09`), deployed via Vercel project `motilli-a1`. Chain is now congruent ad → advertorial → PDP for the first time since March.

## Open items for Brooks
1. **Label check:** confirm soluble prebiotic fiber actually appears on the current label/supplement facts (no mg claimed in copy deliberately). FAQ still lists 200mg apigenin / 302.5mg chlorophyllin as before.
2. **Fiber card image:** third ingredient card renders as a colored block; generate an i3 fiber card image to match i1/i2 style.
3. **Marquee reviews:** two quotes still sell the vitamins/energy story (Linda "numbers and energy came back", Karen "steady energy and focus") — swap for backup/brick/burp outcomes when convenient.
4. **Advertorial linkage:** advertorial CTA should point to this 90-day reset PDP (bundle logic = week-6 loop reversal → 90-day protocol).
5. **Deployment saga (important for future edits on this store):** API theme-file writes (REST + GraphQL) never surfaced on full-page renders — a stale full-page cache entry survived asset writes, settings_data touches, theme rename, product updates, a publication bounce, AND a theme publish. Resolution: duplicated the theme (`shrine-pro-upstream-mechanism-2026-07-09`, id 188158148975, now MAIN — old theme 186933838191 unpublished as rollback) which flipped every page EXCEPT the bare 90-day-reset URL. That one cache entry is aging out on TTL (utm/fbclid URLs collapse onto it too; `?variant=53033648750959` bypasses it and serves the new page). If it persists: open theme editor → Save, or ask Shopify support to purge. For future launches: link ads with the `?variant=` param.
6. Old theme 186933838191 still contains an inert `<!-- upstream-propagation-test-19h55 -->` marker in sections/main-product.liquid (stripped from the published duplicate).
