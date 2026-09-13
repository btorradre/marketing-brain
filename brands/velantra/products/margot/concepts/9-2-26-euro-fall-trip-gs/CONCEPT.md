# VEL-MER-EUROFALL-01 — "Euro fall trip" (Paris / Milan / London) · greenscreen AI UGC

**Date:** 2026-09-02
**Product:** The Meridian Leather Tote · $124.99 from $149.99 · six colorways (live PDP 9/02)
**Reference:** `instagram.com/reels/DcWLvteqezx/` (Sara Ouardi, 85.8s, "what to pack for Paris, Milan and London this fall"). Copy, frames and transcript in `reference/`.
**Format:** greenscreen AI UGC, 1080x1920 30fps, one continuous VO, creator keyed as a greenscreen cutout (house geometry, bottom-left then bottom-right), hard-cut full-bleed stills every 2-4s, word-synced captions bottom-centre, live PDP screen recording as the close and the ad ends there.
**Runtime:** 60.7s (VO 60.2s, Woman Over 40, natural read, no atempo). Reference is 85.8s.
**Board:** `http://localhost:8765/b/vel-mer-eurofall-01-euro-fall-trip-paris-milan-london-greens` (Cutroom / velantra). Sibling builds: the same reel was mirrored for all three of Vivienne, Weekender and Meridian on 9/02, one board each, different creator and grid per product.
**Status:** BUILT 2026-09-02 on "continue going" after the board notes. Shipped cut: `final/VEL-MER-EUROFALL-01-C1-A.mp4` (60.7s, -14.5 LUFS, TP -1.2; C1 Eleanor on HeyGen Avatar V (look reused from OLDMONEY, head deltas 4.6-7.9); B03 intro swapped from the PDP studio hero to the MAR-030 cafe marble still so the bed stays in real rooms). Bed only: `final/*-bed-A.mp4`.

## Angle

Euro fall trip, one bag for three cities. "Fall" and "Euro trip" are the wrapper; the reasons to believe are our bag's physical facts, so the ad still reads in spring or for a domestic trip (six-month test) and does not survive with another brand's bag dropped in (swap test). No villain: the three-city dress-code framing is the reference's own grammar and the "don't pack three bags" line is her own packing hassle, not a claim about other bags.

## What the reference does (watched frame by frame, Whisper transcript)

Grid-and-title hook (2x2 real street-style photos, centred serif title, creator in an opaque inset with a mic) → "three fashion capitals, three dress codes" → three chapters (Paris: pack less, understated, "one good bag that works every day"; Milan: polished and intentional, richer colours, start with the shoes; London: experiment, four seasons in a day, walk a lot) → a question close ("Paris, London or Milan, which one are you packing for?"). One photo per item, hard cuts every 2-3s, captions bottom-centre.

What we mirror: the grid hook, the three-city chapter structure, the photo-per-line rhythm, the inset creator, the question close. What we change on law: the list is the hook only, from the product intro every frame is our bag; the house formula sits underneath (verdict hook, `This is the ... from Velantra` by 0:08, attributes, proof, capacity, variants, live offer, link); the close is the live PDP recording.

## Script

See `SCRIPT.md` (lawgate clean, speaker=creator). VO take A: `vo/VO-woman-over-40-A.mp3` + alignment; plain respellings fed to TTS (`Vivian` / `Vehlantra`, no hyphens). Whisper hears "Volantra" for the brand, which it does for every spelling (8/31 benchmark); no pause around either brand word.

## Creator

C1 Eleanor, 48 (dark blonde going grey, cream silk), reused from OLDMONEY-GRID-01. HeyGen Avatar V render fires only after board approval (`creator/`).

## Hook grid + scene seeds (real Pinterest street-style pins)

Crawled with Apify `fatihtahta/pinterest-scraper-search` (queries: paris / milan / london fall outfit street style). Grid tiles are used as-is (hook only). Scene seeds go through GPT Image 2 pixel-seed i2i on kie (`_build/gen_euro.py`, 2:3 @1K, 6cr, two variants per shot): the pin is the scene, the real product photo is the second input, and only the bag is swapped. Picks in `_build/picks.json`, contact sheets in `keyframes/_qa-*.jpg`.

| pin | role | source |
|---|---|---|
| p002 | grid EURO-P2 | https://www.pinterest.com/pin/294845106879325901/ |
| p007 |  EURO-P1 | https://www.pinterest.com/pin/50735933300080237/ |
| p014 | grid  | https://www.pinterest.com/pin/501940320993169106/ |
| p025 | grid  | https://www.pinterest.com/pin/44262008831947381/ |
| p044 | grid  | https://www.pinterest.com/pin/1688918605428602/ |
| p060 |  EURO-M1 | https://www.pinterest.com/pin/706009679116119544/ |
| p071 |  EURO-L1 | https://www.pinterest.com/pin/1108941108274952658/ |

## The bed — 18 beats

| beat | in–out | kind | frame | line |
|---|---|---|---|---|
| B01 | 0.00–4.40 | still | B01-GRID-A.jpg | Going to Europe this fall? Don't pack a different bag for Paris, Milan and London. |
| B02 | 4.40–6.72 | keyframe | B02-EURO-P1-v2.png | One tote works in all three. |
| B03 | 6.72–9.16 | still | B03-B03-PDP-brown-hero.jpg | This is the Meridian from Velantra. |
| B04 | 9.16–13.56 | keyframe | B04-EURO-P2-v1.png | Paris is where you keep everything understated, slightly undone, |
| B05 | 13.56–16.00 | still | B05-VEL-MAR-079-macro-swirl-grain.png | and this is grained leather in one color |
| B05b | 16.00–19.81 | still | B05b-VEL-MAR-077-macro-turnlock.png | with polished silver hardware and no logo anywhere. |
| B06 | 19.81–22.21 | still | B06-VEL-MAR-087-setdown-bar-hook.png | It just looks like a bag you've had for years. |
| B07 | 22.21–27.14 | keyframe | B07-EURO-M1-v1.png | Milan is where you dress it up, way more polished and intentional. |
| B08 | 27.14–30.10 | still | B08-VEL-MAR-078-macro-belt-v-plates.png | That's the belted front with the silver turn lock, |
| B08b | 30.10–31.56 | still | B08b-VEL-MAR-083-macro-hand-grip.png | the flat handles, |
| B09 | 31.56–34.22 | still | B09-VEL-MAR-088-setdown-bench-lobby.png | and the way it holds its line when you set it down. |
| B10 | 34.22–40.96 | keyframe | B10-EURO-L1-v2.png | London is where you walk all day and it's four seasons in one day, so I clip on the crossbody strap. |
| B11 | 40.96–43.39 | still | B11-VEL-MAR-061-pack-laptop-sleeve.png | The top stays open, so my laptop, |
| B11b | 43.39–46.22 | still | B11b-VEL-MAR-068-pack-umbrella-morning.png | an umbrella and a water bottle go straight in, |
| B11c | 46.22–48.59 | still | B11c-VEL-MAR-059-open-reach-wallet.png | and I can reach my wallet without stopping. |
| B12 | 48.59–50.52 | still | B12-COLORWAY-6up.jpg | It comes in six colors |
| B13 | 50.52–53.92 | pdp |  | and they're running a sale on it right now, so grab it before the trip. |
| B14 | 53.92–60.74 | still |  | So tell me, Paris, Milan or London. Which one are you packing for? I left the link below. |

## Flags

The Meridian oversold on 8/21 and the live page still carries backorder strings: build it, but do not run traffic until a restock date is on the PDP (same block as MER-OLDMONEY-GRID-01). Silver hardware, laptop, crossbody strap, umbrella and water bottle all trace to real photos in the 8/02 library or product truth.

Open ruling shared with HAALAND-01 / OLDMONEY-GRID-01: the grid tiles and scene seeds are third-party photographs of real, unlicensed people.

## Build log (9/02)

- `_build/build_ad.py <creator>`: hard-cut bed off `beat-map.json`, PDP recording slowed (never sped) to span the close, creator keyed off the HeyGen plate (chromakey sampled from the plate, 0.12/0.05, despill 0.15) and composited per the house greenscreen geometry: head 0.20 W, body cut by the bottom edge (60px bleed) and the near side edge (70px), bottom-left through Paris and Milan, jumps to bottom-right at the London chapter; captions 54px Arial Bold centred above her head (bottom edge y=1180) off the alignment, feathered scrim over the PDP; VO loudnorm -14. Brooks rejected the first pass (an opaque rounded inset mirroring the reference's PiP): "you didn't properly apply the green screen effect". The reference's inset is NOT the house look; the keyed cutout is. `_build/pip-<creator>.json` and `_build/caption-cards.json` record the numbers.
- No music bed (the reference's music was not auditioned; add one at ~-30 LUFS if wanted).

## Build (reference for re-runs)

1. Brooks approves keyframes on the board (re-roll any EURO-* card with `python3 _build/gen_euro.py <SHOT>`; swap the variant in `_build/picks.json`, re-run `build_beats.py` + `build_board_spec.py`, re-push).
2. HeyGen Avatar V render from the creator plate driven by take A (port `render_heygen.py` from OLDMONEY-GRID-01).
3. Recapture the PDP scroll on ship day (`capture_pdp_scroll.py`, 500 CSS px).
4. Assemble (port of OLDMONEY `build_ad.py`): inset PiP instead of the keyed cutout, hard cuts, captions bottom-centre, loudnorm -14. Deliver the full path.

Self-audit: passes the six-month test (season is a wrapper) and the swap test (attribute stack is our hardware, leather, strap and colorways).
