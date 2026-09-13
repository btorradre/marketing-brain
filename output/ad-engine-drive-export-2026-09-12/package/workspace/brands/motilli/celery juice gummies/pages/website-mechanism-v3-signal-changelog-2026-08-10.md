# Motilli Website Congruency Rewrite — Mechanism v3 "THE SIGNAL" (2026-08-10)

**Mechanism source of truth:** `brands/motilli/research/glp/00-master-avatar/Motilli_Mechanism_Rebuild_GutBrain_Motility.md` (canonical 2026-08-03)
**Store:** getmotilli.com = `y9t3s8-ns.myshopify.com`, theme `188158148975` (shrine-pro-upstream-mechanism-2026-07-09, MAIN)
**Supersedes:** `pdp-90day-upstream-mechanism-changelog-2026-07-09.md` (v2 wrong-organ / three-pathway)

Scope agreed with Brooks: **core storefront + live listicles.** Advertorials (~40 pages) deliberately untouched, each being a distinct ad angle rather than a congruency edit.

---

## What changed conceptually

| | v2 (was live) | v3 (now live) |
|---|---|---|
| Spine | wrong ORGAN (stomach, not colon) | wrong SIGNAL (gut-brain axis drives the whole belt) |
| Metaphor | highway, on-ramp vs off-ramp | conveyor belt with one motor |
| Colon state | "your colon is empty" | slow transit, colon over-strips water, stool arrives as cement |
| Villain | laxatives aimed at the wrong end | Trap 1 osmotic laxative treadmill + Trap 2 protein-fiber trap |
| Fiber | "Pathway 3: downstream flow" | low-viscosity soluble, the anti-Metamucil, cannot pile up |
| Shorthand | "works on the organ every laxative ignores" | **"Stop forcing the exit. Restore the signal."** |

The wrong-organ line is **retained as the entry aha** in listicle headlines per v3 §2. The signal story is what sits behind that door.

---

## Surfaces updated

### 1. PDP templates — `templates/product.json`, `templates/product.upstream.json`
Identical copy; `product.json` serves the 6-bottle bundle, digestive-health and listicle products, `product.upstream.json` serves the 90-day reset.

- **Buy-box subhead**: rewritten to the signal frame, "restore the signal instead of forcing the exit, without touching your dose." All 4 bullets replaced.
- **Mechanism accordion**: rebuilt from 6 panels to 7, in v3 §6 beat order (vindication → traps → unbranded mechanism → product reveal):
  1. Why Nothing Else Has Worked, And What Actually Does
  2. **The Laxative Treadmill** (new, carries the fear beat)
  3. **120 Grams of Protein, Zero Grams of Fiber** (new, the protein-fiber trap)
  4. What to Expect, Week by Week
  5. Who Motilli Is Designed For
  6. Made in the USA
  7. The Stay-On-Your-GLP-1 90-Day Promise
- **Ingredient cards**: "The 3 Pathways Inside Motilli" → "The 3 Things a GLP-1 Gut Actually Needs". Reframed as restore the signal / neutralize the sulfur / keep water in the stool. i3 renamed to "Low-Viscosity Soluble Fiber".
- **Comparison table**: us/others labels now "Motilli Restores the Signal" vs "Miralax & Laxatives Force the Exit". Rows r5/r6 → "Built for a Signal-Quieted Gut" / "Fiber That Cannot Pile Up".
- **Stats, usage ladder, guarantee**: reworded onto the belt/signal language and the wk1 / wk2-3 / wk4-6 / day-90 ladder.
- **FAQ**: ingredients answer rewritten, new block b11 "Is Motilli a laxative? Can I stop my MiraLAX?" inserted after the timeline question. b6/b7/b9 cleaned.
- **Testimonial marquee**: t4 and t7 retired (both sold the dead vitamins/energy story) and replaced with treadmill and fiber-trap outcomes.

### 2. Homepage — `templates/index.json`
Same section types, same patch applied (32 changes). Note the homepage JS-redirects to the PDP via `custom_liquid_DJewbV`, so it barely renders, but it was also a generation *behind* the PDP and is now level with it.

### 3. Listicles
- `pages/listicles/wrong-organ-7-reasons/` → **getmotilli.com/pages/wrong-organ-breakthrough** (page 705827996015). All 7 reasons rewritten. Reason 2 becomes the wrong-end aha, reason 3 becomes both traps, reason 4 becomes the three v3 actors. Comparison table "Works On" row now The Signal vs The Exit. **LIVE and verified.**
- `pages/listicles/motilli-glp1-5reasons-obsessed/` → **/pages/5-reasons-obsessed-glp1** (704345440623). Reason 1 retitled "Works on the Signal, Not the Exit"; fiber reason rebuilt on the bulk-fiber backfire; close rebuilt. **LIVE and verified.**
- `pages/listicles/motilli-5reasons-miralax/` → **/pages/5-reasons-miralax-glp1** (704281182575). Body updated in Shopify and verified via Admin API; **storefront still serving a stale cached render, see Known issue below.**

Pre-edit backups: `index.html.PRE-v3.2026-08-10` in each listicle folder; theme templates in `ops/mechanism-v3-signal/backups/`.

---

## Claims changes worth knowing

1. **The vitamins claim is gone store-wide.** The PDP FAQ and buy box previously advertised "supporting vitamins (A, C, B6, K1, folate)". Those do not appear on the OEM label (`brand/website-assets/label 1.png` reads celery juice, chlorophyll, prebiotic fiber only) and v3 has no vitamins leg. Removed rather than reworded.
2. **Fiber stays unquantified**, per the v3 §5 label checkpoint. See open item 1.
3. **The osmotic-laxative fear beat is now on the storefront**, Brooks-approved, in strict association language: "associated with", "an association is not proof of cause", cited as "a large 2023 cohort study published in the journal *Neurology*". Never "causes". Appears on the PDP accordion, the wrong-organ listicle and the miralax listicle.
4. **The "your colon is empty" premise was removed** from the miralax listicle. It directly contradicts v3, which holds that stool *is* in transit and the colon over-dries it. Two reason headlines changed accordingly.
5. **All em dashes removed** from copy touched, per house law. Two knowingly remain: the `— {{ block.settings.body }}` separator hardcoded at `sections/motilli-bf-usage-v2.liquid:27` (a visual separator, not prose) and the "— Dr. Rebecca Marsh, MD" byline attribution.

## Bug found and fixed

**Both CTA buttons on the miralax listicle were 404ing.** They pointed at `https://www.getmotilli.com/products/motilli`, a handle that does not exist on this store (301 to apex, then 404). Repointed to `getmotilli.com/products/motilli-3-bottle-90day-reset?variant=53033648750959`, the canonical destination with the cache-bypass variant param. Unknown how long that funnel was dead.

Also fixed: the obsessed listicle's top bar still read "Spring Sale Live Now" in August.

---

## Known issue

`/pages/5-reasons-miralax-glp1` is serving a **stale full-page cache**. The stored `body_html` is correct (verified via Admin API, `updated_at` 2026-08-10T03:24), and the served HTML carries the right `resourceId` but the old text. This is the same signature documented on 7/09 for the bare 90-day-reset URL, where asset writes, settings touches, a publication bounce and a theme publish all failed to clear it and it eventually aged out on TTL. A `template_suffix` toggle was attempted here and did not clear it either.

Expected to age out on its own. If it persists: theme editor → Save, or ask Shopify support to purge. The other two listicles and both PDPs flipped immediately.

---

## Part 2: product imagery (same day)

Source + build files: `brands/motilli/product-images/v3-signal-2026-08-10/` (finals, the HTML that renders them, and the cropped/matted photographic elements). Deploy: `ops/mechanism-v3-signal/deploy_product_images_v3.py`.

**Rendering method:** the two infographic slides were rebuilt as HTML and screenshotted at 2048x2048 through headless Chrome, not regenerated with an image model. Text-heavy slides are exactly where diffusion models garble copy, and the supplement-facts panel below is what that failure looks like in production. Photographic elements were reused from the existing art: ingredient circles and the celery hero were cropped out of the old slide 3, and the bottle was matted off white with a corner flood-fill (a global luminance threshold eats the white cap).

### Gallery, all four GLP-1 products
`motilli-6-bottle-bundle`, `motilli-3-bottle-90day-reset`, `motilli-digestive-health-gummies`, `motilli-celery-juice-gummies-glp-1-listicle` shared one identical 6-image set. Now 5 images:

1. **Badges** rebuilt. Third badge was "Supports Natural Energy and Digestion" (a vitamins-era claim) and is now **"Works On the Signal"**. The product photography is the original, untouched; only the badge column was re-rendered over it.
2. **Mechanism slide** replaced. Was "The Upstream Way to Calm GLP-1 Digestion" with two pathways (Wakes the Stomach / Clears the Gas) and an outcome line ending in "Steady Energy". Now **"Stop Forcing the Exit. Restore the Signal."** with the three v3 actors (Restores the Signal / Clears the Sulfur / Keeps Water In) and an outcome line of Less bloating, Fewer sulfur burps, Mornings you can count on.
3. **"Inside Every Gummy"** replaced. The **Vitamin Blend card is gone**. Fiber's job was "Rebalances gut bacteria" with a 5g figure and is now the low-viscosity soluble beat with no gram value. Three cards instead of four.
4. Stats slide, unchanged.
5. Reviews slide, unchanged.
6. Supplement facts, **deleted**, see below.

### The supplement facts panel (deleted store-wide)
The panel on the live PDPs was a fabricated graphic, not a real facts panel, and it was internally garbled:

- `"*FDA Daily Value are urred based on your own 2,000 calorins calorie diet."`
- Other Ingredients read `"Celery Juice, Chlorophyll, Chlorophyll, Sodium Copper Chiloprophyllin, Sodium Copper Chlorophyllin, Like Imuliin), Copper Chlorophyll Sugars."`
- It listed `Dietary Fiber 5g` and `Prebiotic Fiber Blend 300mg` in the same table.
- `Total Carbohydrate 6g` at `45% DV` (the real figure is about 2%).

Brooks approved pulling it. The identical file (md5 `26f4d52d3a38015e8b1a00d60b27904f`) turned out to be on **eight** products, so it was removed from all of them, including `motilli-3-bottle-reset-cc` and the advertorial/listicle/pureveen variants. Verified zero copies remain store-wide.

### The mg figures (removed store-wide)
This panel is where `200mg apigenin` and `302.5mg chlorophyllin` came from: the graphic reads `Celery Juice Extract 200mg` and `Chlorophyll 300mg` + `Sodium Copper Chlorophyllin 2.5mg`, which sums to 302.5. Two problems: the source is a hallucinated image, and "Celery Juice Extract 200mg" is not the same claim as "200mg apigenin", which is what the site was saying. Brooks approved stripping them. All mg values are now gone from `product.json`, `product.upstream.json`, `index.json` and `product.cc.json`, including the disabled sections. The three actives are named without quantities.

### Fiber ingredient card
Open item 2 from the 7/09 changelog is closed. The card was rendering as a flat `#c9b370` swatch on the PDPs (and on the homepage and CC template it pointed at `i3_fiber_v3.png`, a dry bulk-powder macro that visually argues *for* bulk fiber, the opposite of the v3 claim). Generated a replacement showing fine powder dissolving into clear water with silky ribbons and no grain, matching the light-background macro register of the apigenin and chlorophyllin cards. 10 credits on kie GPT Image 2. Set on all four templates.

Note the kie balance is **184.3 credits and auto top-up is confirmed broken**, so anything larger needs a manual billing fix first.

### Verification
All four galleries confirmed at 5 media in the right order via the Admin API. The bare PDP URL renders every new asset. `?variant=53033648750959` is serving a stale cached copy of the render taken between the copy write and the image write, the same sticky-cache behaviour documented on 7/09 for this exact URL; a sibling product on the identical template renders correctly, so the templates are right and it will age out.

## Open items for Brooks

1. **Label reconciliation. Now the single biggest open risk.** Get the real supplement facts panel from the manufacturer. Three mutually inconsistent versions existed and the one the site was quoting turned out to be hallucinated:
   - OEM label art: celery juice, chlorophyll, prebiotic fiber, **5g fiber**, no vitamins.
   - Pureveen-style mock: celery juice 500mg, **inulin + acacia 5g**, chlorophyllin 100mg, plus ACV and green apple polyphenol.
   - The deleted PDP panel: celery juice extract 200mg, chlorophyll 300mg, prebiotic fiber blend 300mg, sodium copper chlorophyllin 2.5mg, dietary fiber 5g. Garbled and self-contradictory.

   Everything quantitative is now off the site, so nothing unsourced is live. But the **5g fiber figure on the physical label still conflicts with the v3 fiber beat**: 5g of inulin is a fermentable, gas-producing dose sitting behind an "adds no bulk, the anti-Metamucil" claim. If the label really is 5g inulin, the fiber beat needs rewording rather than the label needing a footnote. This is the one thing I could not resolve from anything in the vault.
2. **UGC review block** (`motilli-ugc`, 8 reviews) still sells brain fog, energy and "my mind is sharp" in r4 and r7. Left alone because they read as verbatim customer reviews rather than brand claims, but they are vestiges of the vitamins era.
3. **`templates/product.cc.json` was deliberately not touched.** It runs the chronic-constipation avatar on the butyrate/bacteria mechanism, which v3 §8 keeps as a separate doc for a non-GLP-1 buyer. Confirm that split still holds.
4. ~40 advertorial pages remain on v2. Out of the agreed scope but they are the biggest remaining incongruent surface.

---

## Reproducing

```
cd brands/motilli/ops/mechanism-v3-signal
SSL_CERT_FILE=$(python3 -c "import certifi;print(certifi.where())") python3 deploy_storefront_v3.py --dry-run
```
Copy lives in `copy_v3.py`, deploy logic in `deploy_storefront_v3.py`. The patcher is idempotent and diffs before writing, so re-running reports 0 changes. Listicles redeploy with each folder's own `deploy.py`.
