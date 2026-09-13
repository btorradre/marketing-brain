# Frame-QA Checklists — Velantra Claymation Campaign

Used by the mandatory frame-QA subagent pass: after ANY generated frame (keyframe or video still) containing a Velantra bag, a fresh-context subagent reads this file, the canonical product reference, and the frame, then returns PASS/FAIL per frame with reasons. FAIL → regenerate with the mechanism block (cap 3 attempts, then escalate to Brooks). This applies to ALL bags, closed or open, image or video.

## Canonical references

- Straw Tote: `brands/velantra/products/straw-birkin/product-images/straw birkin/caramel 1.png`
- Weekender closed: `brands/velantra/products/weekender/product-images/product images/light chocolate 1.webp`
- Weekender open truth: `_campaign/assets/weekender-open-truth-still.png` (from the Brooks-approved broll clip)

## Straw Tote — flap mechanism (THE 2026-07-18 failure class)

The flap is ONE SINGLE SEAMLESS SHEET of leather attached along the top rear edge, folded all the way forward over the front, lying completely flat. Its front lower edge is CUT into the panel-and-tabs silhouette (wide center + 2 squared tabs) — these are shapes of the same sheet, NEVER separate pieces. The only openings are the 2 narrow handle slots. Two belt straps crossed in an X on the front below it. No metal hardware.

**SEAMLESS SHEET TEST (2026-07-18, Brooks's second catch — MANDATORY on every tote frame): crop and magnify the flap. FAIL if any gap, seam shadow, or split appears between the flap shapes; if the leather band is interrupted anywhere across the top (especially between the two handle bases); if straw, contents, or background is visible THROUGH any part of the flap other than the 2 handle slots; or if the shapes read as separately applied pieces. The old acceptance language "3 sections joined at the top" is RETIRED — sections butted together with visible junctions are a FAIL.**

FAIL on sight:
1. Flap split in half, separate/butted pieces, any gap or seam between its shapes, any see-through other than the 2 handle slots, or a discontinuous top band between the handles
2. Flap half-open, lifted at an angle, or standing up instead of folded all the way over
3. Contents (croissant/baguette/flowers) poking THROUGH the flap or between its tabs — contents may only lean out of the woven mouth BEHIND the flap
4. Belt straps threaded through the flap, wrapped around contents, or missing their X cross
5. More or fewer than 3 flap sections; more or fewer than 2 belt straps; any metal hardware
6. Front flap/belt detailing duplicated on the back face (back is plain straw)
7. TONE-CONSISTENCY (2026-07-18, Brooks, Emilia-replica catch): within one video, the bag's leather and straw tone must match the tone established by the neighboring segments — a canonical-accurate but video-inconsistent tone (e.g. grey-taupe leather in one shot when the rest of the video renders warm caramel) is a FAIL. Audits of regenerated/partial segments must compare against a frame from an adjacent passing segment as the tone anchor, not only the canonical reference.

## Weekender — closed

Two-tone: cognac leather upper + cream canvas body, gold oval turn-lock, two flat gold clasp plates with belt straps, key bell at handle base, leather corner patches, two rolled handles, visible stitching. FAIL: any zipper, silver hardware, missing turn-lock/key bell, leather-canvas split misplaced, logos or embossed text.

## Weekender — open (verbatim from velantra-weekender skill FINAL calibration)

CORRECT = same leather/canvas two-tone split as the closed bag (wide cognac leather band on the BODY, handles anchored into it with leather bases) AND the one-piece flap clearly visible leaning back behind the open mouth, inner face showing. Interior: cream canvas lining + cognac slip pocket.

FAIL on sight:
1. Handles rooted in canvas (small stitched tabs on canvas)
2. Leather band missing or shrunk to a thin trim line
3. A flap-shaped panel on the FRONT (tab sections, scalloped edges, turn-lock pocket)
4. Malformed or missing flap behind the opening; flap split into pieces; flap covering the front
4b. Fold-back flap inner face rendered as a PLAIN SMOOTH SLAB (2026-07-18, Brooks catch #4): the visible inner face MUST show its two round handle holes, strap slots, and small gold plate — the articulated look. A merged featureless panel = FAIL. The old "stylized inner-face fittings accepted" deviation is RETIRED.
5. ANY zipper (track, teeth, or pull)
6. Front handle omitted (both handles must be visible standing upright)

## Secondary checks (all frames)

- Heroine matches `_campaign/assets/heroine.png` (braided low bun, cream linen dress w/ butter-yellow trim, gold hoops, woven sandals)
- Gull mascot on-model: round white body, dove-grey wings, small orange beak, orange stick legs
- No on-screen text, captions, or invented logos anywhere
- Clay world intact; the bag is the only photorealistic object

## ⛔ PRE-ANIMATION GATE (2026-07-18, Brooks — the artifact root cause rule)

A frame is NEVER sent to Seedance until it has PASSED its audit. Artifacted source frames are what cause most video artifacts — gate at the image, not after the video. The audit runs on the EXACT input that will be animated (the 9:16 crop, e.g. `K2-916.png`), not just the full 2:3 master — a crop can amputate or crowd the bag. Order is hard: generate keyframe → audit → only then animate. Never animate, and never stitch, an unaudited or failed frame.

## ⛔ Closure-interaction law (2026-07-18)

Never animate hands manipulating any bag closure (straps, flaps, locks) — three strikes proved Seedance reinvents the closure architecture mid-clip. Closure-state changes only across hard cuts between audited frames. Video audits FAIL any clip where the closure hardware changes between sampled frames.

## Video segments

Sample at 0.5 SECOND INTERVALS across the full segment (a 5s clip = 10 frames) and apply the same checklists — 3-frame sampling missed a mid-clip mutation that the brand owner caught (HARBOR S4, 2026-07-18: an invented leather trough grew at the tote's mouth between the sampled timestamps). Mid-clip drift peaks BETWEEN sparse samples — Seedance can break the mechanism mid-motion even from a clean first frame. Confirmed mutation classes (2026-07-18, both caught by Brooks):
1. FERRY S2: flap split in half during animation (gap opened between sections)
2. WOVEN: bag mutated into an INVENTED design mid-motion — chunky braided trim, brass belt buckles, smooth saddle flap, straps wrapping the body. FAIL any video frame where the bag grows hardware, braids, trim, pockets, or geometry that does not exist on the canonical reference.
