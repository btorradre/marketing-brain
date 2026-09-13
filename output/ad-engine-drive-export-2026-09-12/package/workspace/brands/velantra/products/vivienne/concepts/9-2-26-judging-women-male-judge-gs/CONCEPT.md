# VEL-VIV-JUDGE-01 v3, the male judge (Vivienne, insecurity angle, greenscreen)

**Date:** 2026-09-02
**Product:** The Vivienne Top Handle Bag, $149.99 from $199.99, pre-order, ships October, four colorways (Chocolate, Cognac, Black, Olive). Live PDP checked 9/02.
**Reference:** `instagram.com/reels/Dbdnok1ttWG/` (60.7s, male creator judging women by their bags, selfie window bottom-left, real stills, title + centred score, deadpan, no music). Manifest + frames in `reference/`.
**Brooks's direction (9/02, three passes):** drop the listicle; the hook is a male content creator judging women's bags, guilt-shaming them toward a better bag; cast on the reference creator; product is the Vivienne. Third pass: apply the greenscreen properly (keyed cut-out, not a window), no scores or judged-bag list at all, reframe to cheap-bag shame that opens the loop (she needs the expensive bag, how does she afford it) and closes it (you don't have to spend all that money anymore, this is the Vivienne from Velantra).
**Angle:** VEL-A-001 "what my bag says about me," voiced through the male gaze.
**Format:** greenscreen AI UGC, 1080x1920 30fps, one VO take, judge chroma-keyed bottom-left over full-bleed stills per the 8/31 edge-cut law (head 0.20 W, head top y 1260, body past the bottom and left edges), one jump to bottom-right on the 'bag that looks like money' beat; hard-cut stills; title card through the reversal; word-synced captions on the product tail; live PDP scroll close.
**Runtime:** 60.5s (take D).
**Board:** `http://localhost:8765/b/vel-viv-judge-01-the-male-judge-vivienne-insecurity-angle` (Cutroom / velantra).
**Status:** v3 storyboard up, awaiting approval of the judge (G1 default), the three shame stills and the tone. HeyGen render and assembly fire after approval. v2 (grey-wall window, scored beats) is superseded; its plates M1-M3 and take B stay in the folder.

## Flagged once

1. Cheap-bag shame is Brooks's explicit register for this run; it overrides the no-wound default. No brand is named and no logo is visible in the shame stills.
2. The shame stills are real Pinterest photos of generic bags (`plates/C1-cheap-puffer-sl056.jpg`, `C2-cheap-houndstooth-sl055.jpg`, `C2alt-cheap-red-hobo-sl000.jpg`, pins in `plates/cheap-candidates-pins.json`). Same open licensing ruling as the grid builds.
3. Voice is the existing `gringo-tiktok-male` clone. I did not clone the reference creator's own voice (real person, paid ad). Brooks's word flips that.
4. Male casting on Brooks's explicit direction for this run.

## Creator

Three plates on flat chroma green, cast on the reference guy's vibe (mid-20s, dark curls, olive skin, plain tee, phone selfie, hand up, lips parted): `creator/G1-charcoal-green.png` (default), `G2-black-green.png`, `G3-heather-green.png`. kie GPT Image 2 t2i 2:3, 6cr each. Green holds edge to edge on all three (corner medians about 20/230/38). No reference frame was fed to the generator.

Key geometry measured off G1's alpha (`_build/pip-geometry.json`): scale 0.659, plate 674x1012, head top y 1260, x -70 (left) / 591 (right), y 968, so the body runs 60px past the bottom edge and 70px past the side. Captions sit above y 1200.

Voice: `hnRXaWYxr5tqZBrH55Cp` gringo-tiktok-male, eleven_v3 Creative, take D, ad-engine `job_243d805d6117` (`vo/VO-gringo-D.mp3`), 192 words, 60.1s, 192 wpm.

## The bed, 15 cuts

Boundaries off take D's alignment; machine-readable in `beat-map.json`; keyed mocks in `board-frames/*-mock.jpg` (`_build/mock_board.py`, `TAKE=D CREATOR=G1-charcoal-green`). Zero new product generation.

| Beat | In, Out | Screen | Title | Judge |
|---|---|---|---|---|
| B01 | 0.00, 5.66 | Cheap quilted puffer bag, cafe counter (real still) | on | L |
| B02 | 5.66, 13.20 | Cheap houndstooth hobo, street (real still) | on | L |
| B03 | 13.20, 16.76 | Red hobo, sunset street (real still) | on | L |
| B04 | 16.76, 23.06 | Vivienne editorial bench, the bag that looks like money | on | R |
| B05 | 23.06, 27.50 | Cognac carried full on the street | off | L |
| B06 | 27.50, 29.71 | Chocolate front hero | captions | L |
| B07a-d | 29.71, 39.36 | Fingers press leather, brass lock, on the hip on the strap, clean front | captions | L |
| B08a-b | 39.36, 48.85 | Chocolate three-quarter, desk with notebook | captions | L |
| B09 | 48.85, 50.72 | Four-up colorway card | captions | L |
| B10-11 | 50.72, 60.48 | Live PDP scroll to "Expected to ship October" | captions on scrim | L |

## Next on approval

1. Brooks approves judge, stills, tone on the board.
2. HeyGen Avatar V from G1 driven by take D.
3. Port today's grid `build_ad.py`: chromakey on the sampled green (sweep 0.08/0.03 to 0.12/0.05), despill 0.15, size on the head per `pip-geometry.json`, title card B01-B04, caption cards from B06, PDP scroll span, -14 LUFS. Deliver the full path.

## Build log (9/02, "now build out the ad")

- **HeyGen Avatar V** from `creator/G1-charcoal-green.png`, driven by take D (`render_heygen.py G1`, look `4cd7fbecd103f4ff0a3f03a0eea8e6a5`, video `941656a996238cf98aecdb8545ed6565`). The first submit returned the usual "missing image dimensions" 400 and the retry went through, same as today's C2. Plate 1080x1620 @ 25fps, 60.08s, green `0x0CEE20`. Head-region frame deltas 6.5 to 8.2 across six samples (healthy 7-10): he gestures through the whole take.
- **Composite** (`_build/build_ad.py G1`): head width 0.20 W (372px on the plate, scale 0.581), overlay 627x941 at x -70 (left) / 605 (right on B04), y 1039, so the body runs 60px past the bottom and 70px past the side and the head top lands at y 1318 (inside the 1220-1340 law band). Captions bottom edge at y 1180. Title card Arial 46 three lines from y 150 through 0:23.06. Key `0x0CEE20` similarity 0.10 blend 0.03, despill 0.15: no fringe on the curls, no pink on the skin. 17 caption cards from the product intro, the auto-respelled `Vell-Ahn-Trah` mapped back to `Velantra` on the cards.
- **Audio:** loudnorm I=-14 plus +0.8 dB trim. The +1.4 dB trim carried from the grid build landed -13.5 LUFS / -0.1 dBTP here, so it was pulled back.
- **Shipped:** `final/VEL-VIV-JUDGE-01-G1-D.mp4` (1080x1920 30fps, 60.5s). Bed-only reference cut `final/VEL-VIV-JUDGE-01-bed-D.mp4`.
- Variants not built: G2 / G3 need one HeyGen render each (`creator/renders/render_heygen.py G2 G3`) then `python3 _build/build_ad.py G2`.

## Revision 2 (9/02 night, Brooks: title off on the bag frame, faster read, cut the dead air, "Velantrah")

- **Pronunciation.** The VO tool auto-respells `Velantra` as `Vell-Ahn-Trah` for TTS, and on this voice that reads "Velantrah". Fed the plain `Vehlantra` respelling (the one today's Vivienne grid build shipped on) so the auto-respell never fires; captions map it back to `Velantra`.
- **Pace.** Atempo is banned (robotic), so three natural takes were generated on the new spelling: G 196 wpm, H 191, I 206. Take I kept.
- **Dead air.** Every inter-word gap above 0.22s in take I was cut to 0.18s (three cuts, 0.48s removed) and the alignment shifted to match: `vo/VO-gringo-J.mp3` + `.alignment.json` + `.cuts.json`. 55.4s, 208 wpm.
- **Title card** now ends with the last shame beat (0:15). It is off on the Vivienne bench frame and everything after.
- **Re-lipsync** (a VO change always re-renders): HeyGen Avatar V from G1 on take J, plate `creator/renders/G1-heygen-green-J.mp4`, green `0x0CED1F`, head deltas 7.1 to 10.5. Composite at head width 0.20 W, x -70 / 615, y 1066, head top 1337.
- **Shipped:** `final/VEL-VIV-JUDGE-01-G1-J.mp4` (55.8s, 1080x1920 30fps, -13.9 LUFS / -0.2 dBTP). The take-D cut stays in `final/` as the superseded first build.
