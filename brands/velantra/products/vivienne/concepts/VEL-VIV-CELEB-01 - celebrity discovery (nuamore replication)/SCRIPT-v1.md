# VEL-VIV-KATIE-01: Celebrity Discovery (Katie Holmes)
**Product:** The Vivienne Top Handle Bag · **Format:** greenscreen VO, 9:16
**Runtime:** 31.3s · 99 words · 190 wpm
**Reference:** Nuamore "Oceana watch" (31.3s, 100 words, 192 wpm), app.trendtrack.io/share/ads/nuamore-gxHhlw
**Date:** 2026-08-29

## Reference beat map

| Time | Beat | Reference line |
|---|---|---|
| 0.0-2.0 | Hook | "Okay, so I kept seeing this watch all over my feed." |
| 2.0-7.1 | Celebrity stack | "First on Hailey, then someone said Victoria Beckham wore it too, and I thought, all right, what's the hype?" |
| 7.1-9.9 | Product name | "It's called the Oceana watch," |
| 9.9-11.5 | Verdict | "and honestly, I get it now." |
| 11.5-16.3 | Value | "It's clean, it's minimal, it looks like money, but it's not." |
| 16.3-19.5 | Spec stack | "It's waterproof, scratch-proof, everyday gold," |
| 19.5-26.9 | Offer + scarcity | "50% off... 50,000+ waitlist... sold out seven times... first time I've seen it in stock," |
| 26.9-31.1 | CTA | "if you're thinking about it, don't. Just grab it." |

## Law-forced swaps from the reference

1. **Celebrity never on screen.** Reference runs unlicensed paparazzi footage of Hailey Bieber and
   Victoria Beckham with the product visible, which implies an endorsement they do not have.
   Her likeness is never used. The name lives in VO and caption only, over our own b-roll. Also fixes the reference's violation of product-on-screen-entire-ad for its first 10s.
2. **No claim she carries ours.** "Someone said Victoria Beckham wore it too" mirrored 1:1 would be
   a fabricated claim about a real person. Our line is an observation about her documented habit;
   she is a taste anchor, the creator is the one who found the bag.
3. **Invented scarcity dropped.** No waitlist, no sellout count, no review count. Replaced with the
   real offer: $149.99 from $199.99, pre-order, ships October (PRODUCT-TRUTH §10, the ship month
   is a public promise and must appear in any ad).
4. **No lived-proof beat.** The Vivienne has not shipped, so any "I've carried mine all season"
   line would be fabricated. Dropped, which matches the reference (it has no proof beat either).
5. **Capacity stays vague.** PRODUCT-TRUTH §11: no capacity or laptop claim is cleared until a real
   unit is measured. Only the cleared line is used.

## SCRIPT

| Beat | Time | Line |
|---|---|---|
| HOOK + anchor | 0.0-5.4 | "Katie Holmes gets copied more than anyone, and none of her bags have a logo on it." |
| PRODUCT INTRO | 5.4-8.2 | "This is the Vivienne Top Handle Bag from Velantra." |
| ATTRIBUTE STACK | 8.2-14.2 | "It's vegetable tanned leather all the way through, a belted brass turn lock, and no logo anywhere on it." |
| MECHANISM | 14.2-19.6 | "It's a Birkin inspired shape, just soft, so it slouches and softens as you carry it." |
| CAPACITY | 19.6-23.1 | "It carries far more than a top handle bag usually does." |
| VARIANTS | 23.1-24.7 | "It comes in four colors." |
| OFFER | 24.7-29.7 | "Right now it's one forty nine instead of one ninety nine, on pre order for October." |
| CTA | 29.7-31.3 | "I left the link below." |

### Optional swaps
- **33s cut:** add after CAPACITY: "It has a two year warranty."
- **Zero-likeness alt for line 1:** "The women who could buy any bag on earth are the ones carrying
  nothing with a logo on it." Same mechanic, no name.

## Visual spec

Greenscreen, 9:16 1080x1920. Creator cut out bottom-left at ~25% frame height, jumps to
bottom-right at 0:23.5. New visual every ~3.5s. Word-synced burned captions above the creator.
**On the hook the caption card does the celebrity work, because her face never appears.**
One continuous VO take. VO ~-14 LUFS, all generated b-roll audio muted.

| # | Time | Visual |
|---|---|---|
| 1 | 0.0-3.5 | Chocolate Vivienne on the arm, walking, flap and brass lock in frame |
| 2 | 3.5-5.4 | Macro on the bare band, nothing stamped on it |
| 3 | 5.4-8.2 | Three-quarter hero, chocolate |
| 4 | 8.2-11.2 | Raking-light macro, natural pore grain |
| 5 | 11.2-14.2 | Macro brass turn lock, belt straps hanging near the SIDE edges |
| 6 | 14.2-17.2 | Hand carry, body visibly slumping and creasing as she walks |
| 7 | 17.2-19.6 | Shoulder strap carry, scale against her torso |
| 8 | 19.6-23.1 | Loading it, flap folded all the way back |
| 9 | 23.1-24.7 | Four colorway lineup |
| 10 | 24.7-31.3 | PDP screen recording: real $149.99 over $199.99 strike, four swatches, October pre-order notice, Add to Cart |

## Production flags

- **"Birkin inspired" NEVER goes in a generation prompt.** VO and caption layer only. The kie
  claims-grep hard-fails the word.
- **The `velantra-vivienne` skill is STALE** and will regenerate a rejected set. Seed from
  `PRODUCT-TRUTH.md` and the real TikTok frames in `source/tiktok/`. Never prompt "structured",
  "high-gloss", "lacquered", "marbling" or "crease patina".
- **ElevenLabs renders the brand as "Volantra."** Check that word on every read.
- Katie Holmes line needs a sign-off before it ships. It is an observation about a documented
  press pattern, not an endorsement, and her likeness never appears on screen.

## Claim trace

| Claim | Source |
|---|---|
| Vegetable tanned leather all the way through | PRODUCT-TRUTH §11 cleared |
| Belted brass turn lock | PRODUCT-TRUTH §11 cleared |
| No logo anywhere | PRODUCT-TRUTH §11 cleared |
| Birkin inspired shape | laws.md §4, 2026-08-21 reversal, copy only |
| Soft, slouches and softens | PRODUCT-TRUTH §11 cleared |
| Carries far more than a top handle bag usually does | PRODUCT-TRUTH §11 cleared |
| Four colors | Live PDP: Chocolate, Cognac, Black, Olive |
| $149.99 from $199.99 | Live PDP 2026-08-29 |
| Pre order, ships October | Live PDP + PRODUCT-TRUTH §10 |
