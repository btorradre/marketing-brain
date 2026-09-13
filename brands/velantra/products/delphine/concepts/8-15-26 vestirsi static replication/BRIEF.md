# THE DELPHINE — Vestirsi 5-format static replication

**Date:** 2026-08-15
**Product:** The Delphine, 25 × 22 × 14 cm top-handle handbag · $125 · Shopify DRAFT `8041821143105`
**Format:** 5 statics — 4 × 1080×1920 (9:16), 1 × 1080×1350 (4:5)
**References:** five Vestirsi Meta statics supplied by Brooks, saved verbatim in `refs/`
**Deliverables:** `final/VEL-DELPHINE-D<n>-<slug>.jpg`

---

## The five formats, and what each one actually does

| Ours | Reference | The layout | The engine underneath |
| :--- | :--- | :--- | :--- |
| **D1** `new-arrival` | V1 Raffia Jess Pouch | Two bags on a warm seamless, lower two thirds. Centered wide-tracked caps + subhead at 26%. Wordmark bottom centre | Demand proof. The reference sells scarcity ("can't keep in stock"); the pair in frame does the range work silently |
| **D2** `everyday-size` | V2 Woven Bella | Model hard right, framed head to foot. Whole left half empty wall carrying a three-line block in plain dark sans at 27% | A review typed into negative space. No card, no box, no styling — it reads as somebody's words, not an ad unit |
| **D3** `effortless` | V3 Woven Bella 4:5 | Waist-down crop, no face. Wordmark left at mid-height, tagline + kicker right-aligned to x=1039 | Brand-level. The bag is the only thing identified, so the frame sells a wardrobe rather than a SKU |
| **D4** `on-the-fence` | V4 Sloane | Editorial studio, C-stand in shot. Big Didot tracked caps at 60%, small body, attribution line | The strongest of the five. Objection answered in the headline, photo pays it off in the same frame, type sits on the photo so it reads editorial |
| **D5** `everyday-staple` | V5 Jess Mini | Coastal close crop, back to camera. White tracked caps at 74%, body, attribution | Warmth and aspiration. Bag is sharpest thing in frame; the lower third is pure pale fabric so white type just lands |

## What was adapted, and why

**The avatar is the whole adaptation.** Vestirsi casts a 25-year-old in a cold studio with an
aloof stare. Ours is the ICP from `research/icp-branding/Ideal_Customer_Profile.md`: early
forties, coastal, linen and light denim, warm and unposed, "already arrived." Same layout,
opposite temperature. Four distinct castings across the set so it never reads as one woman
photographed five times — D3 carries no face at all, which is the reference's own choice.

**All three colorways ship.** D1 pairs Light Chocolate with Dark Chocolate, D2 and D5 run
Light Chocolate, D3 runs Army Green, D4 runs Dark Chocolate.

**Every plate is i2i-anchored on the real 25 cm photography** in `../../real-product/`, never
on the 46 cm Eleanor stills. That is the law from the 8/15 scrap documented in
`PRODUCT-TRUTH.md` §2b, and it is why the domed flap, the side-gusset roller buckles, the gold
feet and the grained chestnut leather are all present and correct here.

**No shoulder strap anywhere.** The long side straps in the supplier's dimensioned shots are
still unconfirmed as a detachable shoulder strap, so every prompt pins the bag as carried by
its two rolled top handles only. V2's reference bag has a long crossbody strap looping through
the frame; ours deliberately does not.

## Copy decisions

Guardrails held on all five: no competitor comparison, **no origin claim** (the reference's
"Handwoven in Italy" has no Velantra equivalent and was replaced with construction language),
no "Birkin"/"Hermes", no designer-inflation register, lineage claim only, and no reference to
how this stock came to exist.

**D1 could not run "BACK IN STOCK".** The Delphine has never been in stock, so the reference's
line would be false. The truthful equivalent of its scarcity engine is the launch mechanic
already in `PRODUCT-TRUTH.md` — one production run, finite units — which is what D5 carries,
while D1 runs the new-arrival + lineage line instead.

### ⚠️ Testimonial provenance — one open call for Brooks

Three of the five references (V2, V4, V5) are review statics carrying a named **Verified
Buyer**. The Delphine is a draft product with **no review corpus**, so putting invented names
under a verified badge would be a fabricated endorsement.

`_production/compose.py` therefore ships two copy modes and the finals are built in the safe one:

- **`MODE = "brand"` (shipped)** — identical layouts, copy in Velantra's own voice, no badge,
  no attributed name. Launch-safe today.
- **`MODE = "review"`** — the reference's exact device, badge and all. The strings are already
  written in `COPY`; they are placeholders in the avatar's voice, **not real buyer text**.

To ship the review version: replace those strings with real review copy, flip `MODE`, re-run.
Five seconds, and the plates are never touched.

## Production truth

- **Plates:** kie.ai GPT Image 2 i2i (`gpt-image-2-image-to-image`), 2K. **5/5 landed on the
  first attempt, zero rejects** — the first clean sweep this concept family has had, and it is
  down to anchoring on real photography instead of the Eleanor stills.
- **Type is composited locally with PIL**, never model-generated, so tracking and alignment are
  pixel-correct and copy stays swappable. Geometry in `compose.py:GEOM` is measured off the
  reference files (row-scan for text bands, ink extents per run) and stored as percentages of
  frame height so it carries across the 9:16 and 4:5 canvases.
- **Bag closed in all five**, so the opening-mechanism law is satisfied by construction rather
  than by prompt-wrestling.
- Blocks pasted into every prompt: the real-25cm identity block, the SMALL-SCALE block, the
  closed-state construction pins, the four MANDATORY DETAIL CORRECTIONS, the colour match, the
  GRIP law, and the anti-CGI footer.

### Two production laws this run added

**1. urllib has no cert bundle on this machine.** `gen_plates.py` originally used
`urllib.request` for the kie API and died on `CERTIFICATE_VERIFY_FAILED` after uploading every
reference. All API calls and result downloads now go through `curl`, which uses the system
trust store and was already the working path for uploads. Port this to any forked runner.

**2. Legibility must be measured against the reference, not eyeballed.** Two separate failures,
both invisible until measured:

- **D1** composited white type over our warm off-white sweep at L≈240-249. The V1 reference sits
  at L≈195. `edge_falloff()` now measures each type band, solves for the multiplier that lands
  it on 195, and interpolates back to 1.0 across the middle of the frame — so the bags keep
  their bright ground and the type reads exactly as the reference does.
- **D5** lost the final letter of its headline to a 222-bright patch of sand that a full-height
  band average reported as a comfortable 204. `band_local_max()` now scans in **2D** — thin rows
  crossed with 110px windows — and the scrim **solves** for the target rather than stepping
  through fixed strengths, because a fixed 0.32 took the band from 190 to 136 and visibly
  changed the photograph.

The general form: white type needs a brightest-window guard exactly the way dark type needs the
darkest-window guard that already existed, and both should solve for the reference's measured
luminance rather than a hardcoded strength.

## Files

- `refs/` — the five Vestirsi statics, downloaded verbatim
- `_production/gen_plates.py` — plate generation, idempotent (delete a PNG to regen)
- `_production/compose.py` — typography compositor; copy lives in `COPY`, geometry in `GEOM`
- `_production/refs/` — Delphine real-product anchors (LC / DC / AG)
- `_production/qa/` — magnified bag crops used for the frame-QA pass
- `plates/` — clean photography, no text
- `final/` — the five finished statics
