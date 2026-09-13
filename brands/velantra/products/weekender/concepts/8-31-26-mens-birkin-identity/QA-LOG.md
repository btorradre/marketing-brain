# QA log — MENSID-01 keyframes

## Pass 1 (9/01, 20 stills @1K, 120cr)

Scenes, wardrobe, congruence and the iPhone aesthetic landed across all 10 setups.
One man throughout: tall, broad, backwards beige cap, black blazer, white tee, white high-tops.

| Frame | Verdict | Notes |
|---|---|---|
| K02 v2 | PICK | Bag on carry-on handle, hotel. Nit queued: straps flank the centre tab instead of the side edges |
| K02 v1 | reject | Invented front pocket architecture |
| K04 v1 | PICK | Open packed, flap back w/ correct inner face, palm pressing. Front handle resting forward = allowed state |
| K04 v2 | reject | Front handle drooped into a long slack loop over the canvas |
| K05 v1+v2 | FAIL → regen v3/v4 | Twist-bar postman's lock on the plate (banned geometry), straps flanking centre. Anti-pocket + blank-plate + edge-strap lines added |
| K06 v1 | reject | Pocket architecture + oval fittings on the canvas |
| K06 v2 | FAIL hard | Grew an EMBLEM on the plate (logo) + suede flap. Regen v3/v4 with anti-pocket + blank-plate lines |
| K07 v1 | PICK | Interior beat: caramel lining + slip pocket + correct flap inner face. Strongest product frame of the run |
| K08 v2 | PICK + CREATOR ANCHOR | Full-body scale frame; saved as _build/creator-ref.png, K03 generates against it |
| K08 v1 | reject | Pocket-front bag |
| K09 v1 | PICK | The terminal money frame. Hardware nit at distance queued |
| K10 v1 | PICK | Overhead bin, flat on base, clears the lip |
| K11 v1 | PICK | Laptop into interior at the gate. Nit queued: oval keyhole plate rendered ON the band |
| K12 v1+v2 | FAIL | Four-bag lineup: colorways correct but bags taller than wide (LINEUP block dropped "wider than tall") |
| K12 v3+v4 | pass, RETIRED | Lineup fixed, then Brooks (9/01) directed the beat stay on Light Chocolate |
| K12 v6 | PICK | Single LC bag on the bed, hand on the flap, straps at the edges, flat blank plate. v5 equivalent, v6 cleaner hardware read |

## Standing engine finding (9/01)

kie gpt-image-2 **rejects long prompts at 2K** ("content could not be processed"), passes the
same prompt at 1K. Board pass renders at 1K; approved picks get upscaled before animation.
1K success = 6cr. Failures cost 0.

## Pre-render regen queue (after Brooks approves scenes)

Hardware nits on otherwise-approved picks: K02 strap placement, K09 distant hardware,
K11 band plate. Fix per [[feedback_i2i_anchor_on_the_fitting_not_the_product]]: anchor on the
macro photo of the fitting, don't reword. Then upscale picks to 2K.

## Voice + HeyGen (9/01)

- Voice: ElevenLabs IVC `teva-yapper-male` (`v1yekEvIQ3vXOo7DnQ3g`) from tiktok @talktoteva/7677756402827414815, 64s single speaker, diarize-checked.
- VO take 1: eleven_v3 Creative preset, 60.96s, 150/149 words on STT, brand onset "Vel-" (e/a jitter only), no drops. PASS. No atempo.
- HeyGen audio_asset_id: `602c4482cd5a4fb895f82ec9cc88f494`. API pool 884 credits at start.
- Avatars: 3 Pinterest refs (men 35-45) -> GPT Image 2 i2i on flat chroma green, 2 variants each @1K.

## Avatars (9/01) — 6/6 PASS, picks for HeyGen
| Avatar | Pick | Why |
|---|---|---|
| M1 (~40, navy tee, ref p095) | v1 | Neutral frontal, mouth relaxed. v2 mid-word |
| M2 (~43, white shirt, ref p044) | v1 | Slight open smile, frontal. v2 wide grin bakes teeth into the source |
| M3 (~38, olive tee, ref p049) | v2 | Most frontal of the pair, watch visible |
All: flat chroma green, chest-up selfie framing, imperfection cues present, no lettering, 6cr each @1K.

## HeyGen renders fired 9/01 15:08 UTC (Avatar V, 1080p, 9:16, audio 602c4482cd5a4fb895f82ec9cc88f494)
| Avatar | source frame | HeyGen asset | look_id | ad-engine job | heygen video_id |
|---|---|---|---|---|---|
| M1 | avatars/M1/v1.png | 83e25b59914242539517a62263752ff1 | b8349beb6605ede5ceeabe5a04751802 | job_934fa0342e7a | f37e4f1fbe35dde1ed077a61b1876c9f |
| M2 | avatars/M2/v1.png | 7226872200874b91a56c0344d13f9495 | 113f8122421332ee3ef9875fba0cf22e | job_f7a05e945ad4 | 06d616dcfe1c09b00204406f8f843287 |
| M3 | avatars/M3/v2.png | 28b3013a6a044ea88c5330d2478ec3a1 | fef117902d8c795a05c6830278e9cd43 | job_d9d665ec19ed | aedfd484f36a80e724f95f36bfb318a7 |
Reuse these look_ids for any later men's cut instead of retraining.

## HeyGen renders — RESULT (9/01)
All three completed: 60.936s, 1080x1920, green preserved. Key test over red at 0.08/0.03: PASS on all three (no shirt transparency, clean edges; light despill on hair edges at composite).
Sampled greens: M1 0x35BB39 · M2 0x159B20 · M3 0x48D54B (sample per render, do not assume one value).
Files: avatars/renders/M{1,2,3}-heygen-green.mp4 + -keytest-red.mp4/.jpg + -render-still.jpg

## Final composite QA (9/01)
- All three: 60.97s, 1080x1920, -14.2 LUFS (first pass measured -15.6, lifted 1.6 dB).
- Hook caption moved to the top band (was crossing the bag on the plate). Close caption moved to the top band (was crossing the swatch row). Body captions at y=1010 above the creator.
- PDP close re-timed to END on the buy box (start = 18.9s - beat length) so 'I left the link below' lands on price + swatches + ATC.
- Caption chunking: 24 hand-set phrases aligned to word times; auto-chunking broke after 'from'/'slip'/'Bin,'.
- Key: no transparency, clean edges on all three; despill 0.15 (0.5 goes pink).
