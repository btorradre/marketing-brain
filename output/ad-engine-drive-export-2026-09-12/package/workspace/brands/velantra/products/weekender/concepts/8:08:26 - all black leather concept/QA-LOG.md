# VEL-WEEKENDER-NOIR — Frame QA Log

**Date:** 2026-08-08
**Method:** Every frame compared directly against the real physical-bag stills in
`product-references/real-product-2026-08-08/` (primarily `LC-closed-front-unfastened.jpg`,
`LC-macro-turnlock-flap.jpg`, `LC-open-flap-inner-face-interior.jpg`), plus the open/closed
calibrations and photoreal block in the `velantra-weekender` skill. QA run inline, not delegated.

## Round 1 — killed after 2 frames

**Systematic FAIL: belt strap geometry.** Prompt said the straps "hang loose down the sides,"
which the model rendered as long straps running diagonally down the front body with the gold kelly
plates mounted low near the bottom corners, leaving the gold staples on the band orphaned. On the
real bag the straps are SHORT, flat and horizontal on the leather upper band beside the flap, each
plate hooked over its staple.

Corrected in the identity block, the hardware block, the mechanism block, the per-shot scene text
and the anti-drift line, with explicit negatives against diagonal/downward straps and low plates.
Rejects kept at `rejects/strap-geometry-v1/`.

## Round 2 — 15 frames, all shots

### Picks

| Shot | Pick | Why |
|---|---|---|
| 01 hero front | **v1** | On-brief straight-on front hero. Correct strap geometry, tonal seam reads across the front, both side eyelets, key bell, corner patches. v3 has better leather texture and harder directional sun but is a three-quarter, which duplicates shot 02's job |
| 02 three-quarter | **v1** | Best frame in the set. Deep gusset clearly readable, side eyelet visible, genuine grain and creasing in the leather, real bedroom light. v2 and v3 both render the left strap noticeably lower than the right |
| 03 hardware macro | **v3** | True black with correct architecture: gold oval keyhole plate with the knurled post head through the cutout, knurled post below the flap edge, both kelly end plates with dome rivets. Softer real light than v1 |
| 04 open interior | **v1** | Cleanest mechanism pass. One-piece flap folded back behind the mouth, inner face showing both keyhole handle cutouts, both oval strap slots and the gold oval plate. Caramel lining AND the wide caramel slip pocket both clearly visible. Both handles present. No zipper |
| 05 carry scale | **v3** | Strongest scale read — bag spans hip to below knee at near shoulder width, unmistakably a travel bag. Hand carry only, no invented shoulder strap |

### Rejects and why

- **03-v2 — REJECT.** Leather renders brownish-black, reading close to the existing Dark Chocolate
  colorway rather than true black. Fails the concept's core premise.
- **04-v2 — REJECT, hard fail.** Phantom flap-shaped panel on the FRONT of the open bag (rounded
  panel carrying a second gold oval turn lock, low center). This is the exact failure the mechanism
  block exists to prevent and it is on the regenerate-on-sight list.
- **05-v2 — REJECT.** Bag renders too small, reading as a large handbag rather than an 18" travel
  bag. Fails the scale anchor.
- **02-v2, 02-v3** — asymmetric strap placement (left lower than right). Usable but beaten by v1.
- **01-v2** — lost the tonal seam across the front; leather reads uniform. Beaten by v1 and v3.

### Standing notes for the next run

1. "Hang loose" is a poisoned phrase for this bag's straps in any engine. Always specify short,
   flat, horizontal, on the band, plate hooked over staple.
2. The open-bag shot still throws a phantom front flap roughly 1 in 3 rolls even with the full
   mechanism block. Three variants is the right minimum here, not a nicety.
3. Photoreal held well across the set. The one recurring soft spot is the macro, which drifts
   toward clean studio light; prefer the variant with visible falloff and blown highlights.
4. All frames clean on: no canvas anywhere, gold hardware both sides matching, no logos or
   lettering, no zipper, no shoulder strap.
