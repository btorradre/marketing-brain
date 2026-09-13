# The Meridian / Margot Leather Tote — Product Truth

**Shopify:** product 7648515031105 · handle `velantra-margot-tote` · template `product.meridian-tote`
**Supplier SKU:** BRO011 (color suffixes -1 taupe, -2 cream, -4 black, -5 brown)
**Retail:** $124.99 · **Landed:** $27.76/unit DDP · **Weight on file:** 500 g
**Status of this doc:** created 2026-08-27 during the "add dimensions to the store" pass.

---

## DIMENSIONS — ESTABLISHED

**14.6" W × 9.4" H × 5.9" D  (37 × 24 × 15 cm)**

Recovered 2026-08-27 from two earlier Velantra themes that both published the spec:

| Theme | id | What it carried |
|---|---|---|
| `theme-export-velantra-us-impulse-13aug2025-03` | 139489542209 | "Measuring 37 cm by 24 cm by 15 cm" + a spec bullet |
| `Copy of Atelier` | 141982138433 | "Dimensions: 37 × 24 × 15 cm / 14.6 × 9.4 × 5.9 in" |

**Label correction.** Theme 139489542209 wrote the spec as `14.6" H × 9.4" W` — that assigns
37 cm to HEIGHT. Wrong. This bag is wider than it is tall in every photograph and in the
identity block. The numbers are right, the labels were transposed. Published as
**W 14.6 / H 9.4 / D 5.9**.

Cross-check: photogrammetry off the reference set (laptop-in-bag anchor in
`coffee brown 7.webp`, model shots) put it at roughly 34 × 25 × 15 cm before the themes were
found. Independent agreement inside the error bar.

Also on file from theme 141982138433, published nowhere and not yet verified:
- Weight approximately **2.0 lb / 0.91 kg** — conflicts with the 500 g in the 3PL sheet.
  Do not publish a weight until one of the two is confirmed.
- Leather described as "genuine litchi grain" (litchi grain = the pebbled texture).

### Still not measured
- [ ] Handle drop. Never published anywhere. Copy says "short, hand or forearm" with no number.
- [ ] Crossbody strap drop at its longest setting. Strap has punched adjustment holes.

### Live on the PDP as of 2026-08-27
`Dimensions & Fit` tab, template `product.meridian-tote.json`, theme 150684762177.
Push script: `products/margot/pdp/push_dimensions_tab.py`.

---

## VERIFIED TRUE — read off real product photography

Every item below is visible in the reference set at
`products/margot/product-references/meridian/`.

- **Silver / palladium hardware throughout** — turn-lock plate, two side buckles, base feet,
  strap swivel snaps. (all colorways)
- **Pebbled / grained leather, single colour**, no canvas, no two-tone, no logos anywhere.
- **Open top, no flap.** A short front tab carries the turn-lock; a belt strap runs across the
  front face through a buckle at each edge. Wider than it is tall.
- **Two flat leather strap handles**, upright, short — hand or forearm carry.
- **Removable adjustable crossbody strap included**, with punched adjustment holes and swivel
  snap hooks. Worn crossbody in `black 8.webp`. **Not mentioned anywhere on the live PDP.**
- **Suede-lined interior** in a tonal taupe. (`coffee brown 7`, `black 7`, `white 5`)
- **One full-length centre zip pocket** dividing the interior into two open halves.
- **Snap buttons on the side walls** that cinch the gusset in. (`coffee brown 7`)
- **Metal feet on the base.**
- **Fits a laptop flat**, dropped into the main compartment against the back wall.
  (`coffee brown 7.webp` — a real silver laptop inserted, with clearance)

## FALSE OR UNSUPPORTED — live on the PDP right now

Donor-template contamination. All three are in the live theme template today:

| Live claim | Reality |
|---|---|
| "Florentine Brass Hardware", "Solid brass feet, recessed pulls, antiqued by hand" | Hardware is **silver/palladium** in every photo and in our own Kanary spec. Flatly wrong. |
| "Four solid brass feet" | Silver feet. |
| "15-inch sleeve, padded — drops in flat against the rigid back panel" | **No padded laptop sleeve exists.** The laptop sits loose in the main compartment. Our Kanary ask literally requests "a padded laptop sleeve *if it can be added cheaply*" — i.e. we know it isn't there. |
| "Drum-Dyed Full-Grain" | Leather grade is unknown. Our own Kanary brief asks the factory to "tell us exactly what is on it today" and quotes microfiber PU as a fallback. Unsupported. |
| Care tab: "Premium grained leather" | Same issue, softer. Acceptable until the factory answers. |

## COLORWAY WARNING

`light blue 1.jpg`, `light blue 2.jpg` and `ultra light blue 1.webp` carry
`kMDItemWhereFroms` pointing at **gemini.google.com** — they are AI-generated recolors, not
product photography. The six real colorways are Brown, Midnight Black, Coffee Brown, Cream,
Taupe, Burgundy. Same failure mode as the Sofia recolor incident.
