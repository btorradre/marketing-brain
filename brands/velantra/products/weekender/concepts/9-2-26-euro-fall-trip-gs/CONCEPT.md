# VEL-WEEKENDER-EUROFALL-01 — "Euro fall trip" (Paris / Milan / London) · greenscreen AI UGC

**Date:** 2026-09-02
**Product:** The Eleanor Weekender · $159.99 from $209.99 · Light Chocolate / Army Green / Dark Chocolate in stock · Black pre-order ships mid September (live PDP 9/02)
**Reference:** `instagram.com/reels/DcWLvteqezx/` (Sara Ouardi, 85.8s, "what to pack for Paris, Milan and London this fall"). Copy, frames and transcript in `reference/`.
**Format:** greenscreen AI UGC, 1080x1920 30fps, one continuous VO, creator keyed as a greenscreen cutout (house geometry, bottom-left then bottom-right), hard-cut full-bleed stills every 2-4s, word-synced captions bottom-centre, live PDP screen recording as the close and the ad ends there.
**Runtime:** 61.5s (VO 61.0s, Woman Over 40, natural read, no atempo). Reference is 85.8s.
**Board:** `http://localhost:8765/b/vel-weekender-eurofall-01-euro-fall-trip-paris-milan-london-greens` (Cutroom / velantra). Sibling builds: the same reel was mirrored for all three of Vivienne, Weekender and Meridian on 9/02, one board each, different creator and grid per product.
**Status:** BUILT 2026-09-02 on "continue going" after the board notes. Shipped cut: `final/VEL-WEEKENDER-EUROFALL-01-C3-A.mp4` (C3 Claire on HeyGen Avatar V (new look created from the C3v2 green still)). Bed only: `final/*-bed-A.mp4`.

## Angle

Euro fall trip, one bag for three cities. "Fall" and "Euro trip" are the wrapper; the reasons to believe are our bag's physical facts, so the ad still reads in spring or for a domestic trip (six-month test) and does not survive with another brand's bag dropped in (swap test). No villain: the three-city dress-code framing is the reference's own grammar and the "don't pack three bags" line is her own packing hassle, not a claim about other bags.

## What the reference does (watched frame by frame, Whisper transcript)

Grid-and-title hook (2x2 real street-style photos, centred serif title, creator in an opaque inset with a mic) → "three fashion capitals, three dress codes" → three chapters (Paris: pack less, understated, "one good bag that works every day"; Milan: polished and intentional, richer colours, start with the shoes; London: experiment, four seasons in a day, walk a lot) → a question close ("Paris, London or Milan, which one are you packing for?"). One photo per item, hard cuts every 2-3s, captions bottom-centre.

What we mirror: the grid hook, the three-city chapter structure, the photo-per-line rhythm, the inset creator, the question close. What we change on law: the list is the hook only, from the product intro every frame is our bag; the house formula sits underneath (verdict hook, `This is the ... from Velantra` by 0:08, attributes, proof, capacity, variants, live offer, link); the close is the live PDP recording.

## Script

See `SCRIPT.md` (lawgate clean, speaker=creator). VO take A: `vo/VO-woman-over-40-A.mp3` + alignment; plain respellings fed to TTS (`Vivian` / `Vehlantra`, no hyphens). Whisper hears "Volantra" for the brand, which it does for every spelling (8/31 benchmark); no pause around either brand word.

## Creator

C3 Claire, 45 (honey blonde, camel cardigan), reused from OLDMONEY-GRID-01. HeyGen Avatar V render fires only after board approval (`creator/`).

## Hook grid + scene seeds (real Pinterest street-style pins)

Crawled with Apify `fatihtahta/pinterest-scraper-search` (queries: paris / milan / london fall outfit street style). Grid tiles are used as-is (hook only). Scene seeds go through GPT Image 2 pixel-seed i2i on kie (`_build/gen_euro.py`, 2:3 @1K, 6cr, two variants per shot): the pin is the scene, the real product photo is the second input, and only the bag is swapped. Picks in `_build/picks.json`, contact sheets in `keyframes/_qa-*.jpg`.

| pin | role | source |
|---|---|---|
| p006 | grid EURO-P1 | https://www.pinterest.com/pin/1407443630789419/ |
| p033 |  EURO-M1 | https://www.pinterest.com/pin/85427724178634738/ |
| p034 | grid  | https://www.pinterest.com/pin/8655424282857883/ |
| p051 | grid  | https://www.pinterest.com/pin/1086000897675039272/ |
| p070 | grid  | https://www.pinterest.com/pin/537406168057715045/ |
| q016 |  EURO-P2 | https://www.pinterest.com/pin/498984833737347153/ |
| q070 |  EURO-L1 | https://www.pinterest.com/pin/1093178509576659843/ |

## The bed — 17 beats

| beat | in–out | kind | frame | line |
|---|---|---|---|---|
| B01 | 0.00–4.12 | still | B01-GRID-A.jpg | Going to Europe this fall? Don't check a bag for Paris, Milan and London. |
| B02 | 4.12–5.56 | keyframe | B02-EURO-P1-v2.png | I pack one weekender |
| B02b | 5.56–7.39 | keyframe | B02b-BIN-01-v2.png | and it goes in the overhead bin. |
| B03 | 7.39–9.79 | keyframe | B03-HERO-01-v1.png | This is the Eleanor Weekender from Velantra. |
| B04 | 9.79–13.92 | keyframe | B04-EURO-P2-v2.png | Paris is where you pack less, pieces that work together, |
| B05 | 13.92–16.62 | keyframe | B05-OPEN-PACK-01-v1.png | so three days of clothes fit in here, |
| B05b | 16.62–20.29 | keyframe | B05b-OPEN-FLAP-01-v1.png | and the flap folds all the way back so I can see everything. |
| B06 | 20.29–23.39 | keyframe | B06-EURO-M1-v2.png | Milan is where it gets polished and intentional. |
| B07 | 23.39–26.16 | still | B07-askme-ELEANOR-K04-hand-stroke-leather.png | Full grain leather over woven canvas, |
| B07b | 26.16–29.42 | keyframe | B07b-MACRO-01-v2.png | real brass hardware, no logo anywhere, |
| B08 | 29.42–32.99 | still | B08-askme-ELEANOR-K11-standing-unsupported.png | and it keeps its shape packed full or barely at all. |
| B09 | 32.99–37.84 | keyframe | B09-EURO-L1-v1.png | London is where you walk all day and it's four seasons in one day, |
| B10 | 37.84–41.92 | keyframe | B10-KNIT-01-v1.png | so the knitwear and the coat come too, and it still keeps its shape. |
| B11 | 41.92–45.57 | still | B11-b09.jpg | I've dragged mine through three airports and it still looks new. |
| B12 | 45.57–50.16 | still | B12-COLORWAY-4up.jpg | It comes in four colors, and the black one is a pre-order that ships mid September. |
| B13 | 50.16–55.01 | pdp |  | They're running a sale on it right now and the colors go fast, so grab it before the trip. |
| B14 | 55.01–61.54 | still |  | So tell me, Paris, Milan or London. Which one are you packing for? I left the link below. |

## Flags

**Brooks's board notes, 9/02 pm, applied:** (1) the overhead-bin library frame was artifacted, replaced by `keyframes/BIN-01-v2.png`; (2) no real iPhone stills in the ad ("looks too low quality"), so the closed hero, the open-flap beat and the hardware macro are now generated (`HERO-01`, `OPEN-FLAP-01`, `MACRO-01`, i2i anchored on the real stills, which stay as anchors only); (3) the two askme open-bag frames showed a cream interior and a broken flap and shared a scene, replaced by `OPEN-PACK-01` (bed) and `KNIT-01` (desk) generated against the fold-back mechanism block with the caramel interior. `_build/gen_wk_fix.py`, 60cr + 12cr for the bin.


Black pre-order ship date is spoken in the VO and labelled on the colorway card. First Paris seed was a New York brownstone street (ONE WAY sign) and the first London seeds were a Black woman (casting law) then a Cologne street; then a man (flower shop) and an East Asian woman on the second pass; a fresh Apify crawl (`pins2`, queries 'paris street style woman trench coat autumn eiffel' / 'london street style woman autumn outfit red bus') gave q016 (Paris crosswalk, trench) and q070 (London, red bus + phone box). Superseded frames in keyframes/_superseded/. The q016 seed carried a CELINE storefront sign top-left; it is painted out on the picked frame (raw copy kept as `_superseded/EURO-P2-v2-raw-celine-sign.png`).

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
