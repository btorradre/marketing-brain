# ✅ VALIDATED — Google Omni Open-Bag Packed Shot (2026-07-11)

> ⚠️ **INTERIOR LANGUAGE SUPERSEDED (2026-08-08).** The physical-bag footage proved the interior is **smooth caramel tan leather with a wide caramel slip pocket**, NOT "natural cream cotton canvas". The as-run prompt below still contains the old wrong interior line — when reusing this prompt, take the corrected mechanism block from SKILL.md (it has the caramel interior + keyhole handle cutouts) and wire the real stills `product-references/real-product-2026-08-08/LC-open-flap-inner-face-interior.jpg` + `LC-open-interior-slip-pocket.jpg` as references. The 7/11 clip's "zippered pocket" accepted-deviation note is also void: the real pocket is a wide caramel slip pocket.

Brooks-approved output: "this is perfect. This is exactly how the bag should open."

- **Engine:** Google Omni (video-native, single prompt, no keyframe step)
- **Reference wired in:** closed light chocolate hero ONLY
- **Format:** vertical 9:16, ~8-10s segment
- **What the approved output shows:** one-piece cognac flap folded backward, leaning back behind the open mouth and CLEARLY VISIBLE from the front (inner face with two round handle holes, strap slots, small gold plate; rear rolled handle rising above it). Front of the body keeps the exact same two-tone split as the closed bag: wide cognac leather upper band with the handles anchored into it, gold posts + oval turn lock on the band, straps hanging with clasp plates, cream canvas below, corner patches at the bottom. No zipper. Packed contents visible in the open mouth.

NOTE: the as-run prompt below contains one line Omni ignored in the winning render ("hangs down flat against the outside of the BACK of the bag, almost completely hidden from view; the flap does NOT stand upright"). The visible leaning-back flap IS the correct look per Brooks. The locked mechanism block in SKILL.md has been corrected to describe the visible flap; for future runs use the SKILL.md block, not this line.

## Exact as-run prompt

```
A close front facing shot looking slightly down into an open structured weekend bag, packed for a weekend away, the camera pushes in very slowly toward the opening of the bag, revealing everything packed inside. Nothing inside the bag moves, only the camera moves.

Open bag construction: the open bag keeps the exact same two tone split as the closed bag in the reference image. The entire upper section of the bag body, across the front, the back and both sides, is smooth rich cognac brown leather, exactly as deep as the cognac leather upper section on the closed reference bag, and everything below it is cream ivory woven canvas. Folding the flap back does NOT change this split: the line where the leather ends and the canvas begins sits in exactly the same place as on the closed reference bag. The two rolled cognac leather top handles are anchored directly into this wide leather upper band with sturdy leather bases, never into the canvas. Two thin gold posts stand upright on the leather band, and the small gold oval turn lock is mounted on the leather band at the top center of the front. The two cognac leather belt straps hang loose and unfastened down the front with their gold clasp plates. The wide leather band on the front is plain smooth leather and is part of the bag body: no tab sections, no scalloped edges, no pocket shape, no turn lock pocket, it is not a flap. The entire cognac leather flap, one single piece, is folded backward over the top rear edge of the bag and hangs down flat against the outside of the BACK of the bag, almost completely hidden from view; the flap does NOT stand upright behind the opening, and its handle holes and strap slots face away from the camera behind the bag. The mouth of the bag is a clean open oval at the top of the leather section, showing the natural cream cotton canvas interior lining and the cognac leather slip pocket on the back interior wall. The bag has NO zipper anywhere, no zipper track, no zipper teeth, no zipper pull along the mouth of the bag, and no embossed text or lettering anywhere on the bag. The two rolled top handles are smooth simple leather tubes with no wrapping, no braiding and no woven texture.

Inside the open mouth sits a neatly folded chunky cream cable knit sweater on the left, a folded pair of dark charcoal jeans beside it, and a small cognac pebbled leather toiletry pouch with a brass zipper resting on top of the clothes. The only zipper in the entire scene belongs to the small toiletry pouch. Soft warm natural window light, a plain warm beige wall softly out of focus behind the bag, shallow depth of field, calm editorial UGC product photography, vertical 9:16.

Ambient Sound. No cuts. No people. No hands. No on-screen text. ONE CONTINUOUS SHOT.
```

## Current canonical prompt (flap line corrected to the approved look)

Same as above, with the flap sentence replaced by:

```
The entire cognac leather flap, one single piece, is folded backward over the top rear edge of the bag and leans back behind the open mouth, clearly visible from the front: the inside face of the flap stands behind the opening showing its two round handle holes, its strap slots and its small gold plate, with the rear rolled handle rising above it. The flap never covers the front of the bag and never splits into pieces.
```

## Frame-by-frame QA of the approved clip (2026-07-11)

Clip: `brands/velantra/products/weekender/broll/Open_bag_packed_for_weekend_202607111429.mp4` (8.0s, 720x1280, slow push-in, 12 frames sampled at 1.5fps).

- t=0:00-0:02: full bag in frame. One-piece flap folded back leaning behind the mouth, two-tone split identical to closed bag, handles anchored into the leather band, posts + oval turn lock on the band, straps loose with clasp plates, key bell present, corner patches, NO zipper on the bag.
- t=0:03-0:05: mid push-in (where prior generations always broke) — flap inner face stays coherent (oval gold receiver plate center, stitched tab patches with gold bar fittings, rear handle through the round holes). Zero morphing of band depth, hardware, or flap shape.
- t=0:06-0:07: tightest framing — hardware crisp, still no zipper teeth, contents static, lighting continuous. Pouch brass zipper remains the only zipper in scene.

PASSES the locked QA line on all 12 frames. ACCEPTED minor deviations (do not fail future outputs on these alone): interior zippered pocket instead of cognac slip pocket on the back wall; slightly stylized flap inner-face fittings.

## Calibration history (why the block reads the way it does)

1. 2026-07-10 (Seedance): phantom flap-shaped panel (three tabs + lock pocket) left on the FRONT → banned.
2. Fix #1 over-corrected: "front is plain canvas, thin binding only" → Omni erased all front leather, invented a zipper mouth.
3. Fix #2 ("narrow ~1 inch trim band") still undersized → handles anchored into bare canvas with stitched tabs.
4. FINAL (Brooks, physical bag): the BODY has a wide cognac leather upper band; the two-tone split is identical open or closed; handles anchor into the band; flap folds back and is visibly leaning behind the mouth. → Validated output approved same day.
