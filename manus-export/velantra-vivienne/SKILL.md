---
name: velantra-vivienne
description: Product scale and locked product truth for the Vivienne Top Handle Bag. Use for ANY content generation involving this product — video ads, static ads, UGC, PDP imagery, b-roll, or concepts — to stop an image or video generation model from hallucinating the wrong hardware, closure, material finish, or scale. Trigger whenever the Vivienne is generated, rendered, prompted, or replicated.
---

# The Vivienne Top Handle Bag — Product Scale & Locked Product Truth

Use this as the single source of product truth for any content generation involving the Vivienne Top Handle Bag — video ads, static ads, UGC, PDP imagery, b-roll, or concepts. It exists to stop an image or video generation model from hallucinating wrong product details.

**The full set of locked verbatim prompt blocks (identity, closure hardware, material, scene, photoreal, occlusion, opening mechanism, and scale anchor) lives in `references/product-truth.md`. Paste each block into every generation prompt exactly as written, in the situations it specifies — do not paraphrase, summarize, or reword them, even slightly.** Paraphrasing single words in this product's history has already produced a fully artifacted, rejected image set — see the material block's history in the reference file.

## Product identity

- **Product:** The Vivienne Top Handle Bag
- **Price:** $149.99
- **Colorways:** Chocolate, Cognac, Black, Olive
- **Dimensions:** approx. 38 cm (15 in) across (confirmed by Brooks 2026-08-22). Width only — height and depth are still unmeasured, and no capacity claim is cleared for this product.
- **Hardware:** the SAME hardware system as the Weekender (confirmed by Brooks 2026-08-22). Warm brass gold. Knurled mushroom post at front centre of the band, a gold OVAL plate with an empty keyhole cutout on the flap's centre tab, two flat vertical staples (each TWO PARALLEL BARS) left and right, belt-strap tips carrying flat gold rounded-rectangular end plates with an oblong slot and dome rivets, keyhole cutouts in the flap for the handles, a leather key bell at a handle base, one gold eyelet high on each side face. This reading supersedes an earlier, incorrect reading of the source listing's photos that described three separate rectangular plates. Full spec: `references/product-truth.md`.
- **Carry truth:** two SHORT rolled top handles, hand or crook of the elbow only. The top handles do NOT reach a shoulder. One detachable long leather shoulder strap clipped to brass side rings is the only legitimate shoulder or crossbody carry.
- **Positioning:** the all-leather one. Largest and most material-heavy handbag in the line, the only one with no canvas. Not simply a size variant of a smaller sibling bag.

## Reference images

Keep three categories of reference on hand: canonical image-to-image seed photos, a per-colorway angle set matching the live product gallery, and any competitor source reference (read-only — never publish this one, use it only to understand the silhouette).

## Colorways

Chocolate is the hero colorway. Every other colorway derives from an approved Chocolate angle.

| Colorway | Hex | Body | Straps and trim |
|---|---|---|---|
| Chocolate | `#4a2c1a` | dark chocolate | contrast cognac, two-tone |
| Cognac | `#a8632f` | warm cognac | tonal |
| Black | `#1a1a1a` | black | strap treatment unconfirmed — tonal or contrast |
| Olive | `#4f5233` | olive | strap treatment unconfirmed — assumed tonal |

## Open items that block full generation

- **Interior lining and pockets are unknown.** Not visible in any reference photo. Don't generate an "interior" gallery shot until this is confirmed.
- **Dimensions unconfirmed** beyond width. No capacity claim, no laptop claim, no "fits X" line until height/depth are measured.
- **Black and Olive strap treatment unconfirmed.**

## Rules & standards

### Banned in prompts

- **"Birkin-inspired" must never appear in a generation prompt.** It is cleared for customer-facing copy only — never let it reach an image/video generation prompt.
- No origin claims, no rendered lettering, no logos.

### Seeding rule

**Always generate from a REAL PHOTOGRAPH of the product, never from a previous generation.** An earlier image set derived several angles and all twelve recolors from one approved generated frame. Each generation-on-generation hop compounds the "render look," which is what produced blotchy, smeared leather that got rejected. Recolors are the one permitted exception to this, and even then the result must be re-checked at 1:1 for smearing.

### Mandatory frame QA

Every generated frame must be checked against real photos — not against this text — for: silhouette, closure mechanism, hardware count and placement, interior lining, logo-free surfaces, and the "3D-render tell." A frame that nails the product but reads as CGI is a reject. Generate three variants per scene and pick the one that passes.

For the full identity, closure hardware, material, scene, photoreal, occlusion, opening mechanism, and scale-anchor prompt blocks — plus the exact wording histories behind why each one is locked — see `references/product-truth.md`.
