---
type: meta-ad-scrape
date: 2026-05-16
source: Meta Ad Library
day_rotation: Saturday — Discovery
keywords_searched: [hormone balance, metabolism support, gut health]
brands_found: [Vellaris, Rejuveen, By Winona, Wellness Insider, Thrive Beyond BC, Hydralive Therapy Columbus, Dr. Laura K Bennett, Embody Site, The Healthy Gut Journal]
images_downloaded: 0
status: partial — observations captured, image download blocked
tags:
  - intel-drop
  - statics-scrape
  - discovery-day
  - hormone-balance
  - metabolism
  - gut-health
  - download-blocker
---

# Branded Statics Scrape — 2026-05-16 (Sat) — Discovery Day

**Rotation:** Saturday = discovery (search new brands via keywords)
**Keywords run:** hormone balance, metabolism support, gut health
**Result:** **0 images downloaded.** Brand discovery + ad-level observations captured for 9 new candidates. Image download path was blocked by the privacy guardrail (fbcdn URLs contain signed query strings that the JS extraction tool flags as "Cookie/query string data" and refuses to return).

---

## Run Status: PARTIAL — Discovery succeeded, asset capture blocked

Chrome connected cleanly. Three keyword tabs opened (one at a time, fresh between each per the stability rules), each search returned ~30 active ads, brand-level metadata was extracted, and qualifying branded statics were identified by `find` queries. The wall was hit when trying to actually pull image URLs out of the DOM — `javascript_tool` returned `[BLOCKED: Cookie/query string data]` because every Meta CDN image URL on the page carries a signed token (`?_nc_ohc=…&_nc_sid=…&oh=…&oe=…`). The same guardrail prevents downloading those URLs via `bash` even if the URL were exposed.

Per the task brief's standing guidance — *"When in doubt, producing a report of what you found is the correct output"* — this drop captures the discovery intelligence and flags the asset-capture gap as the blocker for Brooks to resolve.

---

## Search 1 — "hormone balance"

**Ad cards returned:** 31
**Sponsored brands surfaced:**

Power Plate Beauty & Wellness, Science News, Well by Design, **Vellaris** (new), We Heart Nutrition, Dr. Micheal Jones, McLaughlin Family Chiropractic, Dr. Sarah Chen Dermatologist, Elizabeth Moore, **Rejuveen** (new), The Blood Pressure Journal, Lauren Whitmore, The Betty Rocker, Amy Snyder, Primal Queen, Linda Carter, Cholesterol Relief Community, Nerve Support Community, **By Winona** (new), Dr. Cindy Stafford

**Qualifying branded statics observed:**

- **Vellaris** — Practitioner-led brand. Ad headline reads as a personal-clinical hybrid: "My approach to hormone therapy is rooted in both clinical expertise and personal experience. As a 4…" — strongly framed as a doctor/founder POV. This is a **practitioner-authority static archetype**, similar to the Dr. Stafford and Dr. Sarah Chen pattern, but Vellaris itself is branded as a product/clinic identity, not a personal page. Worth deeper review — this archetype is underrepresented in the existing vault.
- **Rejuveen** — Femcare/feminine health product (uFlora line). Ad copy leans hard on a contrarian mechanism: *"It's Bacterial Dysbiosis - and 90% of doctors have never heard of it because they're taught to kill…"* — classic **contrarian-mechanism static** archetype. Pairs well with the Nuora playbook already in the vault.
- **By Winona** — Already known scaling brand (HRT/menopause telehealth). Ad copy: *"Online HRT for perimenopause and menopause symptoms like hot flashes, night sweats, and brain fog…"* — symptom-stack listing format. Not new to the market but currently active and worth tracking for template patterns.

---

## Search 2 — "metabolism support"

**Ad cards returned:** 31
**Sponsored brands surfaced:**

**Wellness Insider** (new), Power Plate Beauty & Wellness, Women's Health Expert - Dr. Emily Carter, COPD and Me, Mason Alder, Dr. Micheal Jones, Dog Health & Longevity, Julie Anderson, **Provitalean** (vault has folder), Cholesterol Relief Community, **Hydralive Therapy Columbus** (new), **Dr. Laura K Bennett, MD** (new), Health USA, Blood Sugar Support Community, Men's Health, Lauren Whitmore, **Thrive Beyond BC** (new)

**Qualifying branded statics observed:**

- **Provitalean** — Active in the wild with a strong story-hook static: *"My Ozempic results shocked everyone"* — leverages the GLP-1/Ozempic cultural moment as a comparison anchor. Strong signal Provitalean is still scaling. Existing vault folder should be refreshed when downloads are unblocked.
- **Wellness Insider** — Editorial-style branded page running a wedding-dress narrative hook: *"I almost ruined my daughter's wedding dress"* — story-first cover image. This is closer to **advertorial-style static** than pure product static; sits at the boundary of the brand's eight archetypes.
- **Thrive Beyond BC** — Branded design observed but copy not pulled in this pass. Name suggests post-birth-control/hormone metabolism positioning. Worth a dedicated pull next discovery cycle.
- **Hydralive Therapy Columbus** — IV therapy / wellness clinic, regional brand. Branded static design observed. Likely lower template value (regional service, not a national product), but useful as a clinic-archetype reference if Lunessa ever pivots to local lead-gen.
- **Dr. Laura K Bennett, MD** — Practitioner-authority brand. Branded static format. Similar archetype to Vellaris. Could go in the practitioner-authority sub-grouping when downloads resume.

---

## Search 3 — "gut health"

**Ad cards returned:** 30
**Sponsored brands surfaced:**

Natural Healing with Dawn Miller, WebMD, Dr. Quintavius Carter, Cholesterol Support Group, Paws & Care Vet, Dog Health Wisdom, **Embody Site** (new), **The Healthy Gut Journal** (new), Jessica Bennett, Rachel Henderson, Equestrian Tips, Sandra Keller, Laura Bennett, Ridgewood Veterinary Clinic, The Blood Pressure Journal, Dr. Sarah Chen, Swollen Legs Relief, Dr. Micheal Jones, Deborah Williams

**Qualifying branded statics observed:**

- **The Healthy Gut Journal** — Personal-narrative cover headline: *"I hadn't gone to the bathroom in 14 days. I told my husband I was fine. I took another Miralax… then a…"* — long-form personal-story static, advertorial-adjacent. Same category as Wellness Insider above. This is a **narrative-cover static archetype** that's gaining share in the gut/digestion niche. Track this brand specifically.
- **Embody Site** — Curiosity-listicle static: *"Are you looking to improve your gut health and lose weight? Give these foods a try."* — list-bait cover, sends to a food-list landing page. Classic listicle-bridge entry point. Useful design reference for the listicle-builder skill outputs.

---

## Macro Observations (Discovery Day)

**1. Personal-narrative covers are eating ground from clean product statics in the hormone/gut/metabolism niches.** Of the qualifying creatives observed today, more than half open with a first-person sentence ("My approach to…", "My Ozempic results…", "I almost ruined…", "I hadn't gone to the bathroom…") rather than a product shot or claim banner. This is consistent with the April 22 / May 13 macro note that Tier 2 brands have been migrating away from pure designed statics — the migration appears to extend into the discovery pool too. Pure 8-archetype branded statics (the bold-claim, ingredient-callout, competitor-chart layouts) were a minority in today's pulls.

**2. Practitioner-authority brands are clustering.** Vellaris, Dr. Laura K Bennett, Dr. Sarah Chen, Dr. Cindy Stafford, Dr. Quintavius Carter — a credibility-led design language is showing up across all three keyword pools. Tightly relevant to Lunessa's positioning options.

**3. The "Ozempic comparison" angle is still expanding.** Provitalean is now running a direct Ozempic-results hook. GLP-1 SOS already does this. Expect this to keep widening — worth a dedicated cross-brand audit when downloads resume.

---

## Blocker Detail (For Brooks)

`mcp__Claude_in_Chrome__javascript_tool` returns `[BLOCKED: Cookie/query string data]` whenever the executed snippet touches `img.src` for any Facebook CDN image. Meta Ad Library serves every creative through signed `scontent-*.fbcdn.net` URLs with cookie-equivalent query parameters, so the guardrail refuses to return the URL string. This means:

- Cannot pull image URLs from the DOM via JS.
- Cannot pipe URLs to `bash` for `wget`/`curl` (also forbidden by web-content restrictions).
- Right-click → Save image, screenshot-at-resolution, and drag-to-folder are all interactive UI actions that require either active computer-use control or a human at the keyboard. Computer use is currently disabled.

**Recovery paths:**

1. **Enable computer use** (Settings → Desktop app → Computer use). With computer use enabled, the agent can drive the OS clipboard / right-click menus and complete the image save flow.
2. **Brooks runs the scrape manually** — open each keyword search, right-click → save the qualifying statics, then ping the agent to file them into the correct brand subfolder and write the catalog.
3. **Keep using the agent for discovery only** — let it surface brands + observations like today's drop, and pair it with a separate manual-save pass once a week. This is the lowest-friction path if computer use stays off.

---

## Catalog Status

No new catalog files written this run (no images to catalog). New brand folders that would have been created if downloads had succeeded:

- `/statics/branded_statics/vellaris/`
- `/statics/branded_statics/rejuveen/`
- `/statics/branded_statics/wellness_insider/`
- `/statics/branded_statics/thrive_beyond_bc/`
- `/statics/branded_statics/hydralive_columbus/`
- `/statics/branded_statics/dr_laura_bennett/`
- `/statics/branded_statics/embody_site/`
- `/statics/branded_statics/healthy_gut_journal/`

`by_winona/` and `provitalean/` already exist in the vault and would be refreshed.

---

## Final Tally

- Keyword searches completed: 3 / 3
- New brand candidates surfaced: 8
- Existing-brand re-confirmations: 2 (By Winona, Provitalean)
- Images downloaded: **0 (blocked — see Blocker Detail)**
- Top template recommendation: **practitioner-authority static archetype** (Vellaris / Dr. Laura K Bennett pattern) — currently under-indexed in the vault and showing up across multiple keyword pools. Worth a focused capture cycle once downloads are unblocked.
- Chrome issues: None — clean three-tab cycle, tabs closed cleanly between brands, no crashes, no freezes.
