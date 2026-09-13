# The Vivienne Top Handle Bag — Product Scale & Locked Product Truth

Use this as the single source of product truth for any content generation involving the Vivienne Top Handle Bag — video ads, static ads, UGC, PDP imagery, b-roll, or concepts. It exists to stop an image or video generation model from hallucinating wrong product details. The blocks marked "verbatim" below must be pasted into every generation prompt exactly as written — do not paraphrase them.

## Product identity

- **Product:** The Vivienne Top Handle Bag
- **Price:** $149.99
- **Colorways:** Chocolate, Cognac, Black, Olive
- **Dimensions:** approx. 38 cm (15 in) across (confirmed Brooks 2026-08-22). Width only — height and depth are still unmeasured, and no capacity claim is cleared for this product.
- **Hardware:** the SAME hardware system as the Weekender (confirmed by Brooks 2026-08-22). Warm brass gold. Knurled mushroom post at front centre of the band, a gold OVAL plate with an empty keyhole cutout on the flap's centre tab, two flat vertical staples (each TWO PARALLEL BARS) left and right, belt-strap tips carrying flat gold rounded-rectangular end plates with an oblong slot and dome rivets, keyhole cutouts in the flap for the handles, a leather key bell at a handle base, one gold eyelet high on each side face. This reading supersedes an earlier, incorrect reading of the source listing's photos that described three separate rectangular plates.
- **Carry truth:** two SHORT rolled top handles, hand or crook of the elbow only. The top handles do NOT reach a shoulder. One detachable long leather shoulder strap clipped to brass side rings is the only legitimate shoulder or crossbody carry.
- **Positioning:** the all-leather one. Largest and most material-heavy handbag in the line, the only one with no canvas. Not simply a size variant of a smaller sibling bag.

## Reference images

Keep three categories of reference on hand: canonical image-to-image seed photos, a per-colorway angle set matching the live product gallery, and any competitor source reference (read-only — never publish this one, use it only to understand the silhouette).

## Verbatim identity block (paste into every prompt)

> A large structured trapezoid top-handle leather bag, wider at the base than at the mouth, built entirely from vegetable-tanned leather with a high-gloss waxy pull-up finish and heavy natural marbling and crease patina on every panel, with a single one-piece leather flap that folds all the way over the top from the back panel forward and has a notched scalloped front edge and braided whip-stitched leather trim along its rear edge, two short rolled leather top handles anchored with round brass rivets, one detachable long leather shoulder strap clipped to brass rings at the sides, and the Weekender closure system, a knurled gold mushroom post at the front centre of the leather band with a flat gold oval keyhole plate on the flap's centre tab resting over it, two flat vertical gold staples of two parallel bars each to the left and right, and two leather belt straps coming over the top from the back whose tips carry flat gold rounded rectangular end plates with an oblong slot and dome rivets, hanging near the side edges when unfastened, plus a small leather key bell at a handle base and one small gold eyelet high on each side face, plus reinforced curved leather corner caps saddle-stitched at all four bottom corners, rolled leather piping down the side seams and around the base, expandable side gussets with a vertical leather keeper on each side, and brass feet on the base, all hardware aged warm brass and never chrome or silver, no studs no padlock no clochette no keys no charms and no metal beyond what is named here, and no logos, no stamped lettering and no plaques anywhere on the bag.

## Verbatim closure hardware block (paste into every prompt, regardless of crop)

This mirrors the Weekender's closure system, which is the canonical version — if the two ever disagree, the Weekender's description wins.

> Front closure hardware: at the front centre of the leather band stands a small gold turn post with a round knurled mushroom shaped head. The flap's centre tab carries a polished gold OVAL plate with a shaped keyhole cutout in its middle, and when the flap is down this tab rests over the post so the gold post head shows through the cutout. To the left and right, two flat vertical gold staples stand on the band; when the flap is down its two small oval slots sit over these staples so the staples poke through. Each staple is TWO PARALLEL FLAT GOLD BARS side by side, never one solid blade and never a buckle. The two leather belt straps come over the top from the back of the bag, and each strap tip carries a flat gold rounded rectangular end plate with an oblong slot and small dome rivets, which hooks over its staple. When unfastened the straps hang straight DOWN close to the left and right SIDE edges with their gold end plates visible; they never cross the middle of the front, never run diagonally and never reach the bottom edge. The knurled mushroom post appears ONCE, at the front centre of the band. The oval plate is FLAT and flush against the leather with a smooth polished face and an EMPTY keyhole cutout punched through it, flanked by two tiny plain smooth dome rivets sitting almost flush: no barrel, no cylinder, no knurled drum, no turning bar or toggle standing proud of the plate face, and the rivets are never slotted screws. The handles pass through keyhole shaped cutouts in the flap with stitched edges. A small leather key bell is tied at a handle base. One small gold eyelet sits high on each side face near the gusset edge. All hardware is the same warm brass gold, both sides identical, no silver, no chrome.

**Do not regress on these** (inherited from the Weekender's logged failures): the band carries the POST, never a second oval. Straps hang near the SIDE edges, never across the front. Staples are two parallel bars, never a blade or buckle. No studs, no padlock, no extra metal.

## Verbatim material block (paste into every prompt — non-negotiable)

> MATERIAL: the leather is SMOOTH and HIGH-GLOSS, a waxy pull-up finish with a wet-looking lacquered sheen. Its variation is BROAD and SOFT: large gentle tonal shifts where the wax has burnished lighter over the curves, and only a few soft rolling creases. The surface must read SMOOTH and SUPPLE, like heavily oiled saddle leather. ABSOLUTELY NOT: no crack web, no crazing, no network of fine fracture lines, no dry veining, no spiderweb texture, no reptile or elephant skin, no distressed cracked finish, no bonded-leather pebbling, no crumpled foil look, no dense fine detail across the panels. Large clean glossy panels.

**Why this block exists.** An early full image set was generated using the words "high-gloss waxy pull-up finish with heavy natural marbling and crease patina." The generation model read "marbling" and "crease patina" as crazing and rendered every panel as a dense web of hairline cracks; the whole set was rejected as "heavily artifacted." The words "marbled," "marbling," "crease patina," and "heavily textured" are banned from Vivienne prompts. Always zoom a generated frame to 1:1 on a flat body panel and confirm the surface is smooth before accepting it.

## Verbatim scene block (the house look for this product)

> SCENE: the bag stands on a weathered grey-brown wooden plank surface, planks running horizontally, set against a plain DARK TEAL-GREEN wall in deep shadow, nearly black-green, unlit and featureless. Low-key moody lighting: one soft warm directional source from the front left raking across the leather so the gloss picks up long warm highlights down the body, with deep shadow falling to the right and behind. Warm amber colour temperature, rich dark mood. Square composition, the bag centred and filling most of the frame.

## Verbatim photoreal block (mandatory footer on every prompt)

A weaker footer ("real photograph on a physical set, real optics, natural falloff") let the leather come back blotchy and smeared with no photographic micro-detail. Use this stronger version, and don't shorten it.

**Preamble, at the TOP of every image-to-image prompt:**

> Use the attached photo ONLY as the reference for the bag's shape, proportions, materials, colours, stitching and hardware. Do NOT copy its lighting, its background, its clean edges or its polished product-photo look.

**Footer, at the END of every prompt:**

> CRITICAL RENDERING INSTRUCTION. This is a real photograph taken on a camera by a person. It is NOT a 3D render, NOT CGI, NOT a product visualisation, NOT Blender or Octane or Unreal or Keyshot, NOT ray traced, NOT retouched, NOT airbrushed. If it looks polished or computer generated it is wrong. Photographic evidence that must be present: visible digital sensor noise and fine grain through the shadows and midtones, highlights slightly blown out where the light source strikes the leather, mild chromatic aberration on high contrast edges, focus that is slightly imperfect so nothing is uniformly tack sharp, and real shadows falling off naturally with visible ambient bounce. Real surfaces at high micro-detail: individual stitch threads are separately resolved with visible twist, the whip-stitched braid reads as discrete interlocking strands and never as a soft repeating ripple, the leather shows real pore grain and fine wrinkle lines, faint scuffs and handling marks, and dust caught in the seams. The wood surface shows sharp individual grain lines, splits and saw marks. ABSOLUTELY NOT: blotchy smeared patches on the leather, low frequency mottling that does not follow the form, an airbrushed or waxy plastic surface, mushy or melted fine detail, or smooth featureless gradients standing in for texture.

## Verbatim occlusion block (paste into every prompt where the flap is visible)

On an earlier approved hero image, the two round handle cutouts in the flap rendered as transparent windows showing the background wall through them — physically impossible and an instant reject.

> The round cutouts in the leather flap that the handles pass through are NOT transparent windows. They are holes punched through an opaque leather flap that hangs in FRONT of the bag's body. Through each hole you see the DARK SHADOWED LEATHER of the bag's back panel sitting a short distance behind the flap, deep in shadow and nearly black, with a thin warm highlight on the cut edge where the light catches the thickness of the leather, and the rear handle visible in shadow where it enters the hole. NEVER show the background, the wall, the room or any part of the scene through these cutouts. The flap is opaque and the bag body behind it is opaque.

The same rule applies to the strap slots and the keyhole cutout in the oval plate: an empty cutout shows what is immediately behind it, never the scene.

**Fail on sight:** background visible through any cutout · blotchy smeared leather · mushy whipstitch · uniformly polished surfaces with no grain · tack-sharp everywhere · no sensor noise · malformed junctions where straps meet the body.

## Verbatim opening mechanism block (paste whenever the bag is open, loaded, or seen from above)

> A single one-piece leather flap folds all the way over the top of the bag from the back panel forward. It is not two doors, not a zip, not a drawstring. Closed, the flap lies flat across the top and its front edge hangs down over the closure band, and two belted straps run down over the flap into brass plates on the body. Open, the flap folds back over the top toward the rear of the bag and the mouth is a single wide opening between the two side gussets.

## Verbatim scale anchor (paste into every prompt with a person or a prop)

> Worn on the shoulder it reaches from just under her armpit to below her hip, and it is about as wide as her torso. Carried in the hand it hangs to mid-thigh. Her hand spans only a small fraction of its width.

**Never shrink the bag.** If two frames disagree on scale, enlarge the smaller one — never scale the bag down to match.

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

**Always generate from a REAL PHOTOGRAPH of the product, never from a previous generation.** An earlier image set derived several angles and all twelve recolors from one approved generated frame. Each generation-on-generation hop compounds the "render look," which is what produced the blotchy smeared leather that got rejected. Recolors are the one permitted exception to this, and even then the result must be re-checked at 1:1 for smearing.

### Mandatory frame QA

Every generated frame must be checked against real photos — not against this text — for: silhouette, closure mechanism, hardware count and placement, interior lining, logo-free surfaces, and the "3D-render tell." A frame that nails the product but reads as CGI is a reject. Generate three variants per scene and pick the one that passes.
