# Copy & image pipeline (per brand)

## Copy — build `copy.json` from the research docs
Read the brand's `research dossier/` and pull, in the brand's own avatar voice:
- **H1 + subtitle** — product name + 1-sentence promise (the mechanism, dose, format).
- **4 benefit bullets** + **4 benefit-grid labels** (organ/system → benefit†).
- **Mechanism** — the core metaphor + the 3-step belief shift (drives `rv-core` / problem sections).
- **Villain teardowns** — why each prior solution failed (drives `rv-feeling-worse` / compare).
- **4-point checklist / "what has to be true"** (drives the benefits section).
- **Stages over time** (drives `rv-stages` + `rv-timeline`).
- **Comparison rows** — true-X vs others (drives `rv-compare`).
- **FAQ** — the avatar's silent objections, each dismantled (drives `rv-faq`).
- **Reviews** — written from the **pain-language bank** in the avatar doc; mix 5★ + one 4★ (drives `rv-reviews`).
- **"Never say" list** — compliance guardrails.

Then **edit the example copy inside each `templates/*.liquid`** for this brand before running
`build_sections.py` (the templates ship with Renavita example copy as a structural reference).

## Images — what to provide and how
- **Gallery**: the product's real media (native — leave it).
- **Generate** (text-to-image; image-to-image with the product as reference where label fidelity matters):
  - mechanism/concept image (the metaphor)
  - lifestyle (the avatar, warm/brand-toned)
  - 3 "stage" photos
  - product macro / ingredients flat-lay
  - someone holding the product
- **Composite** product clusters with `scripts/composite.py`:
  - `transparent` → for floating product in `rv-compare` / `rv-core` (sits on the panel, no seam)
  - `onbg` → a brand-colored backdrop version if needed
  - Background-remove the real product shot first (any bg-removal tool) to get the transparent source.
- **Upload**: `shopify_api.py putb <theme> assets/<name>.png <local>` → reference via
  `{{ '<name>.png' | asset_url }}` in sections; OR `upload_file_graphql` to Files for a CDN URL.
- Fill `images.json`: `{ "__IMG_MIRROR__": "<url>", "__IMG_STAGE1__": "<url>", ... }`.

## Image gotchas (learned)
- Floating product needs a **transparent** PNG, not an on-bg rectangle (a baked bg shows a seam).
- In a panel cell use `object-fit:contain` + `max-height` + padding so the product never clips the rounded corner.
- For a 3-up cluster: front-center largest, two behind offset ~0.3/0.7 x, ~0.84 scale.
