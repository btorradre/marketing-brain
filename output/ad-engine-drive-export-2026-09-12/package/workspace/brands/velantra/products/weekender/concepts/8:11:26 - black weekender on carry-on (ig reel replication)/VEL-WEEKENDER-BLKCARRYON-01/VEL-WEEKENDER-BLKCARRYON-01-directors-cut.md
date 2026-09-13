# VEL-WEEKENDER-BLKCARRYON-01 — Black Weekender on the carry-on

**Reference:** IG reel `DbkwLfUAXf6` (@sebaswl), 18.4s, music-only, no dialogue.
Saved at `reference/sebaswl-DbkwLfUAXf6.mp4`.

**Brief (Brooks, 2026-08-11):** replicate this reel for Velantra — men's angle, BLACK
colorway, and instead of packing the suitcase he brings a suitcase out and sets the
Weekender **on top of it**. After that the shot cuts and the packing looks shot on
iPhone, natural light, ready to post to IG or TikTok.

> ⚠️ **Not the same ad as `8:10:26 - mens packing asmr`** (VEL-WEEKENDER-MENSPACK-01,
> shipped v3 the same week). That one is Light Chocolate, overhead ASMR only, no
> suitcase, and ends on a trolley handle. This one is Black, has a suitcase as its
> opening and closing image, and is a full arrive → pack → leave arc.

---

## What the reference actually does

| t | beat |
|---|---|
| 0:00-0:01 | dust bag lifted off |
| 0:01-0:03 | aluminium carry-on revealed, parked, trolley handle pulled up |
| 0:03-0:09 | overhead flat-lay packing on the floor, ~6 items |
| 0:09-0:10 | compression straps buckled, divider closed |
| 0:10-0:11 | laptop slid into the front pocket |
| 0:11-0:13 | case standing closed, then full body beside it |
| 0:13-0:18 | POV rolling shot, street tracking shot, bench outside a cafe, walk-off |

Music-driven, no VO, no captions. The whole thing is one man and one object moving
through a day. The hook is not the product: it is a person doing an ordinary thing.

## The redirect

| ref beat | ours |
|---|---|
| case revealed + handle pulled | **S01-S02** suitcase wheeled in, Weekender set on top of it |
| overhead flat-lay packing | **S03-S07** overhead packing into the Weekender, 5 items |
| straps buckled, case closed | **S09-S10** packed full, then closed |
| out into the city, 4 beats | **S12** walks out, bag in one hand, suitcase in the other |

**Deliberate departures, and why:**

1. **The suitcase is a plinth, not the product.** The reference packs the suitcase.
   Ours packs the Weekender while the suitcase carries it. That is the whole point of
   Brooks's redirect: the expected travel object is the pedestal, the Weekender is what
   lands on top of it. It reads as hierarchy without a single claim.
2. **The suitcase is unbranded.** The reference's case is a branded aluminium shell with
   orange trim. Ours is a plain pale silver-grey shell with no logos, badges or coloured
   trim — we don't replicate a competitor's product design, and nothing on it can render
   as lettering.
3. **The third act is two indoor beats, not four outdoor ones.** The reference's POV
   roll / street / bench / walk-off sells the creator's lifestyle, not the bag, and four
   generated outdoor locations is the most expensive continuity problem in the reference.
4. **🔒 The bag NEVER rides on the rolling suitcase.** The Weekender has no trolley
   sleeve — its back is a plain leather band. On-the-suitcase is the PARKED image (S02);
   the walking exit is one item in each hand. A bag balanced on a tilted case also just
   falls off.
5. **Packing happens on the bed, not the floor.** Brooks asked for the cut after the
   placement, so the packing is its own setup. A black bag on a dark floor goes muddy;
   plain white bedding separates it and makes the caramel interior read.

## The cut (10 scenes, ~25s)

| # | act | s | beat |
|---|---|---|---|
| S01 | hook | 3.0 | wheels the carry-on in, parks it at the foot of the bed |
| S02 | hook | 2.6 | lowers the closed Black Weekender onto the top of the suitcase |
| S03 | pack | 2.4 | *cut.* overhead: folded indigo jeans into the centre |
| S04 | pack | 2.4 | white tee + grey crewneck against the left end |
| S05 | pack | 2.2 | black dopp kit against the right end |
| S06 | pack | 2.2 | cream shoe bag along the far wall |
| S07 | pack | 2.2 | flat black tech pouch onto the jeans |
| S09 | payoff | 2.4 | packed full, hands out of frame |
| S10 | closure | 2.4 | closed and packed, front on |
| S12 | exit | 3.2 | walks out — bag in his left hand, suitcase rolling in his right |

Closure state never changes inside a clip; it changes across the S09 → S10 cut only.

**Optional adds, staged but not generated:** S08 (passport + sunglasses into the caramel
slip pocket — the best interior-detail beat) and S11 (packed bag set back on the
suitcase, bookending S02). Both are in `_build/scenes.py` and cost ~7cr each.

## Product truth locked for BLACK

Black is **not** a recolour of the other colorways. Ground truth is the five real iPhone
photos in `product-images/black/original-iphone-photos/`.

- **ALL smooth black leather over the whole exterior. No canvas anywhere.** The other
  colorways are leather-over-canvas two-tone; Black replaces the canvas panel with
  leather, leaving only a fine horizontal seam. `ANTI_CANVAS` in `_build/blocks.py` is
  the corrective for the signature i2i failure (the model recolours the canvas instead of
  replacing it and leaves a crosshatch weave or a grey wedge). It travels in every prompt.
- **Interior is smooth caramel tan leather** with a wide caramel slip pocket. Against the
  black exterior this is the single most valuable thing in the ad — S09 is the money frame.
- **The belt straps are SHORT and HORIZONTAL** into their gold clasp plates, open bag
  included. All three ground-truth photos show the fastened state, so this build locks
  it — which also removes the "straps drift diagonally across the body" failure class
  entirely, because there is nothing hanging to drift.
- Warm brass gold hardware, one oval keyhole plate (on the flap's centre tab, never
  duplicated), one gold eyelet per side face, black leather key bell on a long lace.
- Hand or forearm carry only. Never a shoulder.

## Production

- **Stills:** GPT Image 2 (`gpt_image_2`) i2i via the Higgsfield MCP, 2k/high, 9:16.
  kie is dry (114cr, auto top-up still broken). ~10 stills ≈ 70cr against a 1,983cr
  Ultra balance.
- **Motion:** Google Omni i2v from each locked still. **No Seedance anywhere** — 7 of the
  10 scenes are open-bag, and Seedance cannot hold the fold-back mechanism through motion
  even from a clean keyframe.
- **Reusable win — the sibling geometry anchor.** The S03 pick is wired as a third i2i
  reference on every later overhead beat with "match its proportions exactly". Combined
  with the cumulative CONTENTS map, six independently authored stills agree on camera,
  scale and on what is in the bag and where. S09 shows all six items in their stated
  positions.
- **Calibration note:** the authored OVERHEAD state put the bag's long axis vertical in
  frame; the model rendered it horizontal and the render was better (the bag is wider than
  tall, so horizontal shows the whole mouth). Footage-wins — the block was rewritten to
  describe what came back, then locked for the other five beats.

## Files

```
_build/          blocks.py (BLACK), scenes.py, dump_prompts.py, animate_omni.py,
                 picks.json, prompts.json, hf_media.json, S03-anchor.png
keyframes/S**/   generated stills
clips/S**.mp4    Omni clips
reference/       the source reel
```
