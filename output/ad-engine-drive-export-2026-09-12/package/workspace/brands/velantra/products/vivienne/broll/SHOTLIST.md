# The Vivienne — B-roll library v2 (ORGANIC)

**v1 is dead.** It was twelve variations of the same catalogue still life: one wall, one wooden
plank surface, one warm key light, product centred. That is product photography with a push-in,
not b-roll. Brooks rejected it correctly.

## How v2 was built

1. **Crawled TikTok** for real organic handbag footage with no text (`tiktok-source/`).
   251 candidates across 6 slots, 3 search-term strategies, every one through the Gemini gate.
2. **The crawl did not yield drop-in b-roll, and that result is structural.** ~65% of organic
   TikTok handbag content is caption-burned, and the uncaptioned remainder is leather-craft
   workshop content about wallets and small goods, not handbags. Slots S01/S02/S05/S06 (the
   people-with-bag moments) returned ZERO after two term rewrites.
3. **My own frame audit killed most of what the gate passed.** S03 rank02 had burned text the
   gate missed. S03 rank05 was a woman smiling to camera. S04 rank01/04/05 were three copies of
   the same leather-tooling shot. Kept in `tiktok-source/matched/` for the record, not for use.
4. **What the crawl DID deliver is the register.** `tiktok-source/register/` holds the frames
   that define the look: real hands with visible skin texture, phone held overhead, ordinary
   indoor light, flat everyday surfaces, no styling, grain and imperfect focus.
5. **v2 was generated against that register** as a second reference on every prompt, with the
   v1 studio set explicitly negated in every prompt.

## The twelve shots

Vertical 9:16. Engine: **Google Omni**. Storyboard-first: these are keyframes, nothing renders
until Brooks approves. No shot may ship as a zooming still.

| ID | Moment | Where | Light |
|---|---|---|---|
| O1 | Bag on the counter with keys, mug, receipt | kitchen counter | morning window, flat |
| O2 | Hand grabs it off the bench on the way out | entryway | dim hallway |
| O3 | Riding on the passenger seat | car | daylight through glass, cool |
| O4 | Fingers pressing the leather, it gives | dining table, overhead | flat room light |
| O5 | Fingers turning the brass lock closed | kitchen table | flat, dim |
| O6 | On the cafe floor by her boots, POV down | cafe floor | shopfront daylight |
| O7 | Walking out the front door, bag in hand | doorway, from behind | blown daylight ahead |
| O8 | On an unmade bed with a sweater | bedroom | soft morning window |
| O9 | Shoulder strap, against her hip, hallway | apartment hallway | dim yellow overhead |
| O10 | Hand releasing the handles as it lands | dining table | window off to one side |
| O11 | Braided trim and stitching, overhead | kitchen table | flat overhead |
| O12 | Hung over a chair back in the evening | living room | single table lamp, noisy |

Product truth holds on every one: soft slumped body, matte grain leather, contrasting cognac
straps, Weekender hardware, flap CLOSED, cutouts occluded, no logo.

## Coverage

| Beat | Work | Everything | Fall |
|---|---|---|---|
| HOOK | O1 | O1 | O12 |
| PRODUCT INTRO | O1 | O8 | O12 |
| ATTRIBUTES | O11, O5 | O11, O4 | O11, O5 |
| PROOF | O4 | O4 | O4 |
| CAPACITY | O2, O3 | O10, O6 | O2 |
| VARIANTS | recolour O1 per colorway | same | same |
| OFFER | PDP screen recording | PDP screen recording | PDP screen recording |
| CTA | O7 | O7 | O9 |

## Still true from v1

- **No open-bag, interior or packing shots.** Lining and pocket count unconfirmed.
- **No real footage of our bag exists.** The TikToks are third-party, reference-only, never ship.
  When samples land, refilm O2, O4, O5, O7, O9, O10 for real.
- **The OFFER beat is a live screen recording**, shot the day an ad ships.

---

# ANIMATED — 12 clips, Omni, 2026-08-23

All twelve keyframes animated on Google Omni (Interactions API, curl transport, i2v from a
720x1280 JPEG). Output normalised to **locked 24fps CFR, 720x1280, no audio** in `final/`.
Raw renders in `clips/`, 3-frame drift strips in `clipqa/`.

## Drift QA result

Every clip audited on 3 frames (start / middle / end). The result reproduced the Omni macro law
exactly: **wide and motion shots held, extreme macros on metal re-synthesized.**

| Clip | Verdict | Note |
|---|---|---|
| O1 O2 O3 O4 O6 O7 O8 O9 | PASS first roll | Hardware and construction stable across all 3 frames |
| O11 | PASS on re-roll | First roll detached the braided trim into a separate rope lying on the bag |
| O12 | PASS on re-roll | First roll drifted the composition off the keyframe |
| O5 | PASS **trimmed to 6.5s** | Construction holds to 6s, then the camera pulls back and the plate grows a cross-shaped turn piece. Trimmed before the mutation |
| O10 | PASS **trimmed to 2.2s** | Keyframe regenerated first (see below), then trimmed. Closure restructures after ~2.5s |

## Two fixes worth keeping

**The camera push-in is what triggers re-synthesis.** Every first-roll failure had a drifting or
pushing camera in its motion prompt. Re-rolling with "THE CAMERA DOES NOT MOVE AT ALL. It is
locked off at exactly the framing of the still and never pushes in, pulls back or reframes"
fixed O11 and O12 outright and pushed O5's mutation from mid-clip to the final second.

**O10 grew an Apple logo on a plain laptop**, exactly the branded-prop attractor logged in
`feedback_omni_macro_mutation`. Negating it in the motion prompt does not work. The fix is at the
KEYFRAME: the laptop was removed from the scene entirely and replaced with blank unmarked
notebooks. The logo did not come back.

## Law resolution: no Ken Burns

`feedback_omni_macro_mutation` (8/05) says failed macros fall back to an ffmpeg zoompan push-in.
`feedback_no_kenburns_fill_use_real_footage` (8/22) is NEWER and is a direct Brooks rejection of
exactly that output. **The newer law governs: no zooming stills.** So the order of resort used
here was re-roll once, then TRIM to the clean window (still real motion), and only then cut.
Trimming saved both O5 and O10, so nothing was cut.

## Still open

- No real footage of our bag exists. When samples land, refilm O2, O4, O5, O7, O9, O10.
- The OFFER beat is a live PDP screen recording, shot the day an ad ships.
- O10 is only 2.2s. Fine as a fast insert, too short to carry a full beat alone.
