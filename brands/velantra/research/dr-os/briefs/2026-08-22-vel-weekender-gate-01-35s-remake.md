---
brand: velantra
artifact: brief
generated_by: dr-os-mcp
updated: 2026-08-22
sources:
  - brands/velantra/products/weekender/concepts/8-22-26-gate-35s-remake/STORYBOARD.md
  - brands/velantra/products/weekender/actual product assets/ (real 4K footage, 2026-08-08)
  - brands/velantra/products/weekender/broll/Open_bag_packed_for_weekend_202607111429.mp4
  - brands/velantra/products/weekender/video/VEL-WEEKENDER-ZEDE-X5/ (retired, defect audit)
  - Shopify Admin API, velantra-weekender product, verified 2026-08-22
  - skill: velantra-weekender
  - skill: velantra-ad-script
---

# VEL-WEEKENDER-GATE-01 (35s remake)

**Status:** storyboard on Cutroom (`vel-weekender-gate-01-35s-remake`), awaiting Brooks approval. Nothing renders until approved.
**Replaces:** VEL-WEEKENDER-ZEDE-X5 (five cuts, 74-89s, ~40% frozen stills). Retired, do not re-cut.
**Product:** The Eleanor Weekender, Light Chocolate. **Awareness:** solution aware.
**Angle (the problem):** a short trip forces a choice between the bag that holds everything and the bag she wants to be seen with.

## Why the last build failed, and the structural fix

1. **Forty percent frozen photo.** Seedance cannot animate an open bag, a hand on hardware, or a walking carry, so every one of those beats became a GPT Image still on a Ken Burns zoom. Four of them, in two back-to-back pairs, 32.5s of 80s on cut 01.
   **Fix: the real 4K footage Brooks filmed 8/08 carries the product beats.** Five of eleven beats come straight off those clips. Real footage cannot mutate, cannot look 3D, cannot be a still.
2. **The bag was mutated in every live clip.** Gold turn lock rendering as a star medallion, belt straps and key bell gone, the overhead-bin still a different colorway on a different canvas. The medallion sat center-flap while the VO said "no logo anywhere on it."
   **Fix: every beat where the hardware is large in frame is real footage.** Nothing left to invent.
3. **The same shot ran twice.** The seated take returned for 4s after 18s of it (correlation 0.91 to 0.96 across all five cuts), and the last 29s was one walking corridor three times.
   **Fix: no shot appears twice, and there is no walking-carry beat at all.**

Only one beat in the whole ad needs new non-talking generation. Last time it was nine.

## Script: 100 words, 35s, ~171 wpm

If you take a lot of short trips, this is the one I'd get. This is the Eleanor Weekender from Velantra. It's Birkin-inspired, scaled up to a travel bag, structured, real brass hardware, no logo anywhere on it. The whole flap folds back in one piece, so you can see everything at once. Three days of clothes, my laptop, my chargers, all of it. I've flown with it all summer and it goes straight in the overhead bin. It comes in four colors. They're running a sale right now and the colors go fast. I left the link below.

One continuous VO take across the full 35s. Never spliced per beat.

## Shot plan

| # | TC | Dur | Beat | Source | Shot |
|---|----|-----|------|--------|------|
| 1 | 0:00.0 | 4.0s | HOOK | Seedance 2.5 | Creator seated at the gate, bag upright on her lap, hands resting on the canvas, front-on, locked |
| 2 | 0:04.0 | 2.5s | PRODUCT INTRO | Seedance 2.5 (same take) | Same framing, she tips the bag toward lens |
| 3 | 0:06.5 | 3.0s | ATTRIBUTES a | REAL IMG_4049 @ 0.5-3.5s | LC closed on the counter, slow handheld drift |
| 4 | 0:09.5 | 3.0s | ATTRIBUTES b | REAL IMG_4052 @ 2.0-5.0s | Macro, a real hand twists the real gold turn post |
| 5 | 0:12.5 | 2.0s | ATTRIBUTES c | REAL IMG_4050 @ 3.0-5.0s | Push across the clean front band |
| 6 | 0:14.5 | 5.0s | FLAP DEMO | REAL IMG_4051 @ 1.5-6.5s | The one-piece flap folding back, caramel interior opening, one take |
| 7 | 0:19.5 | 3.5s | CAPACITY | APPROVED b-roll Open_bag_packed_for_weekend @ 1.0-4.5s | Packed and open, push-in |
| 8 | 0:23.0 | 4.5s | PROOF | GENERATE (Omni) | Bag lifts into the overhead bin, hands release, door shuts |
| 9 | 0:27.5 | 2.0s | VARIANTS | REAL x4, 0.5s each | IMG_4049 / IMG_4054 / IMG_4058 / black carry-on reel @ 4.0s |
| 10 | 0:29.5 | 4.0s | OFFER | Seedance 2.5 | Back to her, same framing as beat 1 |
| 11 | 0:33.5 | 1.5s | CTA | SCREEN RECORDING | Live PDP, $159.99 struck from $209.99, four swatches, Add to Cart |

Cut rhythm averages 3.2s. Nothing on screen longer than 5s. Zero frozen frames.

## Production laws for this build

1. **Zero frozen stills.** If a beat cannot be produced as motion it gets cut and the VO line goes with it. It never becomes a Ken Burns photo.
2. **Never regenerate what was filmed.** Beats 3, 4, 5, 6 and 9 come off the real 8/08 clips.
3. **Seedance gets beats 1, 2 and 10 only.** Bag still, front-on, no hand on hardware, no camera orbit, no walking carry anywhere.
4. **Beat 8 is the only generation risk.** Three variants, pick clean, frame-QA against `LC-closed-front-unfastened.jpg`. If all three fail, cut the beat and run 30.5s.
5. **One continuous VO take**, lipsync beats 1/2/10 to it.
6. **Single locked 24fps CFR, one encode pass.** The retired files declared five different frame rates with a hitch at every join.
7. **Captions burn from the script, never from ASR.**
8. **Frame-QA subagent pass** on every generated frame before it animates.

## Verified against the live store, 2026-08-22

The Eleanor Weekender, ACTIVE, $159.99 from $209.99 (sale is live, the offer line is true as written). Four colorways: Light Chocolate, Army Green, Dark Chocolate, Black. "Three colors" from the retired script is now wrong. Overhead-bin and three-days claims are live PDP copy.

**Open item:** every variant shows negative inventory. Fulfilment question, not creative, but "the colors go fast" should be true rather than ironic.

## Self-audit

Product intro reads `This is the Eleanor Weekender from Velantra.` and lands at 0:04. The verdict lands inside the hook. Swap test: Birkin-inspired scaled to travel size, one-piece fold-back flap, brass turn post, no logo, four colors, $159.99, no competitor bag drops into this. Six-month test: swap "all summer" for "all year" and every reason to believe stands. Every claim has a demo beat. Creator says "they're," never "our." No em dashes, no personification, no origin claim, no competitor. Law gate clean.
