# VEL-STRAWTOTE-CASTING-VID01 — AI UGC Review, casting 5-pack (caramel)

**Date:** 2026-08-13, rebuilt 2026-08-14
**Product:** Velantra Straw Tote — **caramel** colorway
**Iteration axis:** new creator (casting swap). Script, structure, blocking, energy held constant.

## Why this exists

The winning ad is `120244377076590449` in campaign `120244360979180449`, creative
`1455673946339661` — a 15.1s single-take AI UGC review, one creator, one room, one continuous
take, native lip-synced audio. Brooks asked for five more in the same style with different actors.

This is a **pure casting test**: everything except the actor is frozen, so any lift reads as the
face, not the script.

## v2, 2026-08-14 — Seedance 2.5, 25 seconds, soft CTA

Three changes from v1:

1. **Engine:** Seedance 2.5 (was 2.0), 25s (was 15s), `omni_reference` mode, 720p, 9:16.
2. **Soft CTA** replacing the hard "summer sale, link below" close.
3. **Product truth rebuilt** — see below. v1 shipped a wrong bag.

### The v1 product error, and the fix

Brooks caught it: *"you also messed the bag up"* and *"regenerate the ugc creators so they are
properly holding this bag."* Both were real.

**Root cause: I anchored every keyframe on `caramel 1.png`, which is a tight crop that cuts the
handles off at the top and shows no depth.** With no handle in the reference, the model invented
them. v1 shipped:

- short stubby handles squashed against the bag top, instead of the real tall slim arches
- sharp square corners on the flap tabs, instead of the real softly rounded ones
- a flat slab body with no depth
- a carry where she gripped the two handles apart in two hands, which collapsed them

**Fix:** re-anchored on `on-model/caramel.webp` (full bag, straight on, correctly carried) plus
`caramel 2.png` (three-quarter, shows depth), and rewrote the identity block around the parts the
crop had hidden. The carry now matches the product photography: **both handles gathered in one
fist, bag hanging from them under its own weight.**

**Standing lesson: never anchor a generation on a cropped product shot. Whatever the crop cuts
off, the model invents.**

## Script (locked, identical across all five)

> Okay, wait. This is the Velantra straw tote, and I swear it's this year's Boatkin. Hand woven
> seagrass with gorgeous Italian leather. It's actually structured, so it holds its shape instead
> of flopping over like every other straw bag I've had. It feels lush, and it fits my whole day.
> The colors are selling out fast, and they're running an end of summer sale right now. Get yours
> before they sell out.

72 words, roughly 25s at natural pace. "Italian leather" is the approved *material* descriptor
(Brooks override, 2026-07-07), not an origin claim. "They're", never "our". No competitor named,
no Birkin, no origin claim.

## Casting

| ID | Creator | Wardrobe | Room |
|---|---|---|---|
| A | Blonde, long beachy waves, freckled | white ribbed tank, denim shorts | sunlit kitchen |
| B | Coppery auburn in a claw clip | cream linen button down | plant-filled sunroom |
| C | Light brown, low ponytail | pale blue gingham sundress | white shiplap entryway |
| D | Dark brown blunt bob | navy Breton tee, white shorts | bright bedroom |
| E | Strawberry blonde messy bun | oatmeal cardigan, cream linen | living room, afternoon light |

## Production

- **Keyframes:** GPT Image 2 i2i, 9:16 1k high, anchored on the two full-bag references.
- **Frame QA:** fresh-context subagent audit before any animation. Non-negotiable gate.
- **Animation:** Seedance 2.5, `omni_reference`, 25s, 720p, 9:16, native audio. ~163 credits each.
- **Delivery:** `output/VEL-STRAWTOTE-CASTING-VID01-{A..E}-25s.mp4`
