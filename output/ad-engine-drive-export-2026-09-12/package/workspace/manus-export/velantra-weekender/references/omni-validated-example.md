# Validated Example — Open-Bag Packed Shot on a Video-Native Engine

A worked, brand-approved example of a correctly generated open-bag shot on a video-native generation engine (no separate keyframe step) — included here as a template to adapt. The engine used the closed-front hero photo as its only image reference, plus the Opening Mechanism Block from `product-truth.md`.

- **Format:** vertical 9:16, ~8-10s segment
- **Reference wired in:** closed light-chocolate hero photo ONLY
- **What the approved output shows:** one-piece cognac flap folded backward, leaning back behind the open mouth and CLEARLY VISIBLE from the front (inner face with two round handle holes, strap slots, small gold plate; rear rolled handle rising above it). Front of the body keeps the exact same two-tone split as the closed bag: wide cognac leather upper band with the handles anchored into it, gold posts + oval turn lock on the band, straps hanging with clasp plates, cream canvas below, corner patches at the bottom. No zipper. Packed contents visible in the open mouth.

## Exact prompt (current canonical version)

```
A close front facing shot looking slightly down into an open structured weekend bag, packed for a weekend away, the camera pushes in very slowly toward the opening of the bag, revealing everything packed inside. Nothing inside the bag moves, only the camera moves.

Open bag construction: the open bag keeps the exact same two tone split as the closed bag in the reference image. The entire upper section of the bag body, across the front, the back and both sides, is smooth rich cognac brown leather, exactly as deep as the cognac leather upper section on the closed reference bag, and everything below it is cream ivory woven canvas. Folding the flap back does NOT change this split: the line where the leather ends and the canvas begins sits in exactly the same place as on the closed reference bag. The two rolled cognac leather top handles are anchored directly into this wide leather upper band with sturdy leather bases, never into the canvas. Two thin gold posts stand upright on the leather band, and the small gold oval turn lock is mounted on the leather band at the top center of the front. The two cognac leather belt straps hang loose and unfastened down the front with their gold clasp plates. The wide leather band on the front is plain smooth leather and is part of the bag body: no tab sections, no scalloped edges, no pocket shape, no turn lock pocket, it is not a flap. The entire cognac leather flap, one single piece, is folded backward over the top rear edge of the bag and leans back behind the open mouth, clearly visible from the front: the inside face of the flap stands behind the opening showing its two round handle holes, its strap slots and its small gold plate, with the rear rolled handle rising above it. The flap never covers the front of the bag and never splits into pieces. The mouth of the bag is a clean open oval at the top of the leather section, showing the smooth caramel tan leather interior lining and the wide matching caramel slip pocket on the interior wall. The bag has NO zipper anywhere, no zipper track, no zipper teeth, no zipper pull along the mouth of the bag, and no embossed text or lettering anywhere on the bag. The two rolled top handles are smooth simple leather tubes with no wrapping, no braiding and no woven texture.

Inside the open mouth sits a neatly folded chunky cream cable knit sweater on the left, a folded pair of dark charcoal jeans beside it, and a small cognac pebbled leather toiletry pouch with a brass zipper resting on top of the clothes. The only zipper in the entire scene belongs to the small toiletry pouch. Soft warm natural window light, a plain warm beige wall softly out of focus behind the bag, shallow depth of field, calm editorial UGC product photography, vertical 9:16.

Ambient Sound. No cuts. No people. No hands. No on-screen text. ONE CONTINUOUS SHOT.
```

## Frame-by-frame QA of the approved clip

A ~8.0s, 720x1280 slow push-in clip, sampled at 12 frames (1.5fps):

- t=0:00-0:02: full bag in frame. One-piece flap folded back leaning behind the mouth, two-tone split identical to closed bag, handles anchored into the leather band, posts + oval turn lock on the band, straps loose with clasp plates, key bell present, corner patches, NO zipper on the bag.
- t=0:03-0:05: mid push-in (where prior generations always broke) — flap inner face stays coherent (oval gold receiver plate center, stitched tab patches with gold bar fittings, rear handle through the round holes). Zero morphing of band depth, hardware, or flap shape.
- t=0:06-0:07: tightest framing — hardware crisp, still no zipper teeth, contents static, lighting continuous. Pouch brass zipper remains the only zipper in scene.

PASSES the locked QA line on all 12 frames. ACCEPTED minor deviations (do not fail future outputs on these alone): interior zippered pocket instead of caramel slip pocket on the back wall; slightly stylized flap inner-face fittings.

## Calibration history (why the block reads the way it does)

1. First attempt (talking-head-audio engine): phantom flap-shaped panel (three tabs + lock pocket) left on the FRONT → banned.
2. Fix attempt #1 over-corrected: "front is plain canvas, thin binding only" → the engine erased all front leather and invented a zipper mouth.
3. Fix attempt #2 ("narrow ~1 inch trim band") still undersized → handles anchored into bare canvas with stitched tabs.
4. FINAL (from studying the physical bag): the BODY has a wide cognac leather upper band; the two-tone split is identical open or closed; handles anchor into the band; flap folds back and is visibly leaning behind the mouth. → Validated output approved same day, and this became the canonical block in `product-truth.md`.
