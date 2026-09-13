# VEL-MER-JUDGE-01, "judging girls based on their bags" (insecurity angle, Meridian finale)

**Date:** 2026-09-02
**Product:** The Meridian Leather Tote, $124.99 from $149.99, six colorways live (Brown, Midnight Black, Coffee Brown, Cream, Taupe, Burgundy), PDP checked 9/02.
**Reference:** `instagram.com/reels/Dbdnok1ttWG/` (60.7s, 13 bags, male creator in a small rectangular selfie window bottom-left, full-bleed stills of women holding bags, persistent title, centred score, deadpan one-liners, no music). Watched frame by frame: `reference/manifest.json`, frames in `reference/frames/`.
**Angle:** VEL-A-001 "What my bag says about me" (angle bank). Golden nugget: the judgment happens before she opens her mouth, and she has no say in it.
**Format:** 1080x1920 30fps, one continuous VO, creator in a rectangular PiP window bottom-left (plain grey wall, not keyed to the plate, exactly like the reference), hard-cut stills, title card top-centre, score card centred, product tail on the house formula, live PDP scroll close.
**Runtime:** 64.6s (VO take A, natural read). Reference 60.7s.
**Status:** storyboard on Cutroom, awaiting Brooks approval of the plates and the creator. Nothing renders until approved.

## Flagged once, then built

1. **Tone.** The reference sneers (0/10, "ugly bag, ugly girl," "basic"). The 7/25 and 7/26 rulings kill that register (negative dissuades; a Saint Laurent owner must never feel stupid). Every competitor verdict here is praise plus a trade-off and nothing scores below 7. If Brooks wants the meme's bite back, that is his call and it is one VO line per beat.
2. **The list is short and the product intro is late.** Reference judges 13 bags and never sells. Ours judges four (Birkin, LV monogram, Chanel classic flap, Bottega Jodie), scores the Meridian ten at 0:25, and names it at 0:32. The 0:06 intro law is broken on purpose because the judging list IS the insecurity angle; the 9/1 ruling ("a listicle donates its look, not its ranking") is honoured from 0:32 on, where the script is pure house formula.
3. **Third-party photos.** The four judged bags are real Pinterest street-style stills (pins in `plates/index.json`), same open licensing ruling as HAALAND-01, VIV-CELEB-GS-01 and today's grid builds. Nothing generated, no bag prompted.
4. **Inventory.** The 8/21 oversell (about 1,760 units across six colorways) was a hard stop for paid traffic. All six variants show available on the PDP today. Confirm the restock landed before this gets spend.

## The bed, 15 cuts over 64.6s

Beat boundaries come off the VO alignment (`vo/VO-A-anchors.json`); machine-readable in `beat-map.json`; mocks in `board-frames/*-mock.jpg`. Zero new product generation: every product still is a QA-passed 8/31 Omni frame, a PDP still or the 9/02 PDP screen recording.

| Beat | In, Out | Screen | Score |
|---|---|---|---|
| B01 | 0.00, 6.76 | Birkin, torso, in hand (pin p086) | 8/10 |
| B02 | 6.76, 11.88 | LV monogram Neverfull on a cafe table (pin lv007) | 7/10 |
| B03 | 11.88, 17.47 | Chanel classic flap, white shirt, coffee (pin chanel026) | 7/10 |
| B04 | 17.47, 25.16 | Bottega Jodie, denim, held low (pin bv045) | 8/10 |
| B05 | 25.16, 31.78 | **Meridian** black, white shirt, coffee, torso (MAR002). Creator jumps bottom-right for this beat only, as the reference does on beat 4 | 10/10 |
| B06 | 31.78, 34.29 | Brown PDP hero. Title and score drop. Creator back bottom-left | |
| B07a-c | 34.29, 44.12 | On-model brown, macro turn-lock and buckle, coffee brown carried full | |
| B08a-b | 44.12, 49.47 | Cognac past the flower stand, brown at the crosswalk | |
| B09a-b | 49.47, 58.11 | Laptop sliding in, open-top overhead with the centre zip | |
| B10 | 58.11, 59.90 | Six-up colorway card | |
| B11 | 59.90, 64.96 | Live PDP scroll: $149.99 struck to $124.99, six swatches, Add to Cart, holds to the last frame | |

Alternates on the board: p042 (Birkin), lv011, chanel063, bv042.

## Creator

Cast from the 9/02 HAALAND-recipe plates (white women, 40s, per the 8/31 casting law). Default **C3v2 Claire, 45** (honey blonde, glasses on head, camel cardigan): the "editor with opinions" read that the deadpan verdicts want. Alternates C1v2 Eleanor 48 and C2 Helen 52 on the board. The reference creator sits in a rectangular selfie window on a grey wall, so the plate is keyed onto a flat grey card and cropped to a 300x360 window at x=20, bottom edge y=1720 (bottom-right x=760 on B05). Head about 40 percent of the window width, matching the reference's framing. The edge-cut law for keyed creators does not apply to this format because the reference's own geometry is a window, not a cut-out.

Voice: ElevenLabs Woman Over 40 (`NBIPq5xdnIg9kaBH5Ape`), eleven_v3 Creative, one take, ad-engine `job_24113816f40e`. 188 words, 64.56s, 175 wpm, median inter-word gap 0.053s, no pause above 0.52s. HeyGen Avatar V render fires only after board approval.

## Overlays

- Title: Arial 46px white, soft shadow, three centred lines from y=150, on screen B01 through B05 only.
- Score: Arial 60px white, centred at y=1190, one per judged bag.
- Captions on the product tail (B06 on): word-synced cards off the alignment, white bold, centred above the creator window, feathered dark scrim over the PDP page (today's build lesson).

## Next on approval

1. Brooks approves plates, creator and the five verdict lines on the board.
2. HeyGen Avatar V render from the chosen plate, driven by take A.
3. `_build/build_ad.py` (port of today's grid build: PiP window instead of chroma cut-out, title and score overlays on B01 to B05, caption cards from B06) assembles and delivers the full path.
