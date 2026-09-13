# VEL-WEEKENDER-NOIR — All-Black, All-Leather Weekender

**Date:** 2026-08-08
**Status:** Concept exploration (not a live variant, not on the store)
**Base:** The Eleanor Weekender, $159.99, 18" W × 14.5" H × 7" D

## The Concept

Exact same make and model as the Eleanor Weekender. One change: **the canvas is gone.** Every
exterior panel that is woven canvas on Light Chocolate / Army Green / Dark Chocolate is smooth
black leather instead, and the leather sections are that same black. The whole exterior is one
continuous black leather in a single tone.

The two-tone split does not disappear structurally — it survives as a **stitched seam line and a
faint change in grain direction**. That matters: it is what keeps the bag reading as the Weekender
and not as a shapeless black duffel. Same panels, same seams, same silhouette, no colour break.

## What Stays Locked

| Element | Truth |
|---|---|
| Silhouette | Identical. Wider than tall, 7" gusset, one generous size |
| Hardware | Warm brass **gold** throughout — turn post, oval keyhole plate, two staples, two kelly-style strap end plates, side eyelets. Gold on black is the whole point of the concept |
| Closure | Unchanged. Knurled mushroom-head post + oval keyhole plate, two flat staples, two belt straps anchored on the back band, keyhole handle cutouts in the flap |
| Flap | One seamless piece folded over. Never splits |
| Handles | Two rolled black leather top handles, anchored into the wide upper band. Hand/forearm carry only, no shoulder strap |
| Interior | **Smooth caramel tan leather lining + wide matching caramel slip pocket.** Kept deliberately — the warm caramel against a black exterior is the single strongest visual beat in the whole concept and it is already true of every colorway |
| Branding | None. No logos, no stamps, no embossing, inside or out |

## Why It's Worth Making

1. **It is the only version that reads as evening / business / travel-formal.** Every current
   colorway reads as summer or weekend-casual. All-black opens the men's segment and the
   work-travel segment without a new mould.
2. **Caramel interior becomes a reveal.** On the canvas colorways the interior is a nice detail.
   On black it is a reveal shot — the open-bag beat becomes the hero of the ad instead of a
   supporting frame.
3. **No canvas means no colorway drift.** Canvas is the fussiest material in generation and in
   manufacturing. All-leather removes the weave entirely.
4. **Gold hardware pops hardest against black.** The closure architecture is the most distinctive
   thing about this bag and it is currently competing with a patterned canvas for attention.

## Open Questions for Brooks

- Black-on-black hardware variant worth rolling too, or is gold the only version?
- Black topstitching (tonal, shown here) or contrast stitching? Contrast would echo the live PDP's
  "contrast stitching" claim but reads louder.
- Price — same $159.99, or does all-leather carry a premium?

## Production Notes

- All frames generated via **kie GPT Image 2 i2i** off the real physical-bag stills in
  `product-references/real-product-2026-08-08/`. No text-to-image, no Nano Banana.
- 3 variants per shot, picks not yet chosen. Rejects kept next to picks for audit.
- Open-bag shot carried the full mechanism block; hardware-prominent shots carried the closure
  hardware block; every prompt carried the scale anchor and the photoreal footer.
- Prompts saved alongside the renders as `<shot>.prompt.txt`.
- Build script: `_build/gen.py` (resumable — re-run to fill gaps).

## Shot List

| # | Shot | Ratio | Refs |
|---|---|---|---|
| 01 | Hero, front, closed-unfastened, on oak floor | 1:1 | `LC-closed-front-unfastened` |
| 02 | Three-quarter on linen bed, gusset + side eyelet readable | 1:1 | `LC-closed-front-unfastened`, `LC-closed-side-strap-detail` |
| 03 | Hardware macro, gold against black grain | 1:1 | `LC-macro-turnlock-flap`, `LC-closed-front-unfastened` |
| 04 | Open on hotel bench, caramel interior reveal | 1:1 | `LC-open-flap-inner-face-interior`, `LC-open-interior-slip-pocket` |
| 05 | Carried at hip in hallway, scale anchor | 9:16 | `LC-closed-front-unfastened`, `LC-hand-scale-front` |
