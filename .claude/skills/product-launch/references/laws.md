# The gate

Read before writing copy or firing a generation. Each of these came from something that
went wrong. The consequence is named so you can weigh it, not so you can argue with it.

## 1. Origin claims

Velantra products are **manufactured in China**. Never claim US, EU or Italian manufacture
anywhere: PDP, ads, email, popups, PR. "New York atelier", "Italian craftsmanship",
"made in Paris" are FTC country-of-origin misrepresentations and PR-fatal.

Approved framing: **"Designed in the U.S., handcrafted by skilled artisans overseas."**

**Carve-out:** the *material* descriptor "softest Italian leather" is approved and stays.
Brooks overrode a compliance strip of it. Material ≠ manufacture. Do not auto-remove it.

## 2. Nothing invented, ever

No fabricated study, sample size, percentage, doctor, tannery, certification, award,
review count or star rating. The donor templates contain historical inventions
("LWG Gold-rated tannery", "4th-generation Tuscan tannery", "our New York atelier",
"woven in a Como mill"). **Cloning a donor carries them over. Rewrite every one.**

Same rule for product facts. Dimensions, capacity, laptop sizes, materials, hardware
metal, lining, closure. Source from a real photo, the supplier, or Brooks. Never from the
competitor's listing and never from a plausible guess. Sofia's dimensions silently shrank
from 10x13x5.5 to 9.5x12x4 that way and nobody could say who authorised it.

## 3. Warranty and returns are policy, not flourish

The house line is "Guaranteed for two years. Built for decades." Before it goes on a page,
**verify it against the live policy pages**. Guarantee windows have moved. Do not copy a
number out of a donor template.

## 4. Competitor comparisons

No competitor comparisons in copy. **One reversal (2026-08-21):** "Birkin-inspired" is
approved as a *mechanism* description and is already live on the PDP. It is customer-facing
copy only. **It must never appear in a generation prompt** — the claims grep blocks it and
it must not reach a rendered frame.

## 5. DMCA / competitor photography

Velantra has a live DMCA history (luxboattote). Third strike terminates the store.

- Competitor photos are **reference only**. Never uploaded, never published, never used
  as the i2i seed for an asset that ships.
- Recolours of a claimant's photo are still the claimant's photo. This regressed once: eight
  banned recolours went back live on the Sofia PDP through a hero re-upload.
- The legitimate path when a competitor's *composition* is the goal: new model, new scene,
  new framing, generated from **our own** product reference. Zero derivation.

## 6. Imagery

- **i2i is always GPT Image 2.** Never Nano Banana for product shots.
- **The 3D-render look is a hard regenerate.** Not a compromise, not "good enough". Clean
  catalogue cutouts as i2i seeds are the known cause: every prompt must state that the
  reference supplies geometry and materials only, never its lighting, background, clean
  edges or polished product-photo look.
- **Three variants per scene, then pick.** Never ship the first roll.
- **Never shrink the bag on your own judgement.** Too small is the failure Brooks catches.
  Close-camera product photography legitimately inflates the near object. If scale looks
  wrong, present the measurements and let Brooks pick the direction *before* generating.
  If two shots disagree, enlarge the small one; never shrink the big one.

## 7. Gallery tagging

Every media alt ends `#color_<handleized-colorway>`. Untagged media shows on **every**
colorway at its raw global position. Shared shots are attached once per colorway with that
colorway's own tag. Never reuse one attachment across colorways.

## 8. Product creation

Never `productDuplicate`, never the admin Duplicate button. Rebuild the product field by
field. Brooks asked for this explicitly: he wants an independent product, not a linked copy.

## 9. Pre-orders

A pre-order colorway on a live product must carry the ship-date promise **on the PDP**,
scoped to the colorway, and must say which colorways ship now, or in-stock buyers assume
the delay is theirs. Working shape:

> **Black is a pre-order.** It is all leather with no canvas, made to order in the first
> run, and expected to ship mid September. Light Chocolate, Army Green and Dark Chocolate
> are in stock and ship now.

The date in the notice, the email and the ad must be the same date, and it must be the one
the supplier actually confirmed. Once public it is a promise. An unconfirmed placeholder
locked in the Colette pre-order exactly this way.

## 10. Voice

No em dashes (`build_pdp.py` normalises them, but write without them). No AI-tell cadence.
No "designer inflation" language. No scam register. Brand spine is **"Luxury, without the
logo"** — a value brand told in a premium voice. **Coastal is dropped**: no coastal
sections, imagery or framing until the coastal bags relaunch.

---

## Ship gate

Answer every line before asking Brooks to publish.

- [ ] Every colorway on the page is a real SKU we are manufacturing.
- [ ] Dimensions, materials and hardware trace to a photo, the supplier or Brooks.
- [ ] Zero origin claims. Zero invented certifications, tanneries, studies or review counts.
- [ ] Donor template's inherited claims rewritten, not carried.
- [ ] Warranty and returns lines verified against the live policy pages.
- [ ] No competitor photo, and no derivative of one, anywhere in the media.
- [ ] Every media alt carries its `#color_` tag; no untagged media.
- [ ] Each colorway's gallery reads in the intended order; each variant has its featured image.
- [ ] Every image passed frame QA: product truth correct AND does not read as a 3D render.
- [ ] Pre-order colorways carry the scoped ship-date notice with a supplier-confirmed date.
- [ ] `templateSuffix` set and the template exists on the **published** theme.
- [ ] No em dashes.
- [ ] PRODUCT-TRUTH.md TODOs either filled or explicitly reported as open.
- [ ] Product is still DRAFT and Brooks has seen the page.
