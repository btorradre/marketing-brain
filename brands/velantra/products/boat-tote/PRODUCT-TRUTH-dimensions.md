# The Camille Boat Tote — Dimensions

**Shopify:** product 7694299856961 · handle `velantra-boat-tote-2` · template `product.boat-tote-2`
**3PL:** VEL-CAM · **Retail:** $79.99

## Spec

**20" W × 14" H × 8" D  (51 × 36 × 20 cm) · strap drop 10"**

Two independent sources agree exactly:

| Source | What it holds |
|---|---|
| Theme `139283431489` (Impulse), `templates/product.boat-tote-2.json`, block `tab_dimensions` | `Height 14" \| Width 20" \| Depth 8" \| Strap Drop 10"` |
| 3PL sheet `velantra_sku_list.csv`, VEL-CAM rows | `51x20x36` |

**The 3PL column is W × D × H, not L × W × H as the header claims.** Confirmed against two
products whose real dimensions are already known: Eleanor `46x18x37` = 18" W × 14.5" H × 7" D
(45.7 × 36.8 × 17.8), Colette `50x18x26` = 19.7" W × 10.2" H × 7.1" D (50 × 26 × 18). Read every
row in that sheet as W × D × H.

## ⚠️ Do not confuse with 40 × 30 × 20 cm

Three older themes publish `40 × 30 × 20 cm / 15.7" H × 12" W × 8" D` for a "Boat Tote". That is
the **ORIGINAL Velantra Boat Tote** — handle `boat-tote`, template `product.boat-tote.json`, now
DRAFT. A different, smaller bag. The Camille is the `boat-tote-2` lineage. An even earlier theme
(`132915200065`, `product.boat-tote.json`) has a third set again, 14" × 13" × 8". Three totes,
three specs, near-identical names. Always match on **template file**, never on the word "boat".

## What was actually wrong on the live PDP

The numbers were never missing. The LUXE rebuild dropped the old `tab_dimensions` **content**
into a tab **titled "Details"**, so a customer hunting for a size had no reason to open it, and
the 2026-08-11 support audit recorded the Camille as having no dimensions.

Fixed 2026-08-27: block retitled **Dimensions & Fit**, key renamed `tab_dim` to match the
Meridian, cm conversions added. The narrative copy that a "Details" tab would have carried is
already on the page via the `description` block (`is_tab: false`), so nothing was lost.

Push script: `products/boat-tote/pdp/push_dimensions_tab.py`.
