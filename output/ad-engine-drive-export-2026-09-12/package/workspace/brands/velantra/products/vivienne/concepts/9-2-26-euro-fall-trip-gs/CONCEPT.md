# VEL-VIV-EUROFALL-01 — "Euro fall trip" (Paris / Milan / London) · greenscreen AI UGC

**Date:** 2026-09-02
**Product:** The Vivienne Top Handle Bag · $149.99 from $199.99 · pre-order, ships October · Chocolate / Cognac / Black / Olive (live PDP 9/02)
**Reference:** `instagram.com/reels/DcWLvteqezx/` (Sara Ouardi, 85.8s, "what to pack for Paris, Milan and London this fall"). Copy, frames and transcript in `reference/`.
**Format:** greenscreen AI UGC, 1080x1920 30fps, one continuous VO, creator keyed as a greenscreen cutout (house geometry, bottom-left then bottom-right), hard-cut full-bleed stills every 2-4s, word-synced captions bottom-centre, live PDP screen recording as the close and the ad ends there.
**Runtime:** 59.8s (VO 59.3s, Woman Over 40, natural read, no atempo). Reference is 85.8s.
**Board:** `http://localhost:8765/b/vel-viv-eurofall-01-euro-fall-trip-paris-milan-london-greens` (Cutroom / velantra). Sibling builds: the same reel was mirrored for all three of Vivienne, Weekender and Meridian on 9/02, one board each, different creator and grid per product.
**Status:** BUILT 2026-09-02 on "continue going" after the board notes. Shipped cut: `final/VEL-VIV-EUROFALL-01-C2-A.mp4` (59.7s, -14.6 LUFS, TP -1.3; C2 Helen on HeyGen Avatar V (look reused from OLDMONEY, head deltas 12-19)). Bed only: `final/*-bed-A.mp4`.

## Angle

Euro fall trip, one bag for three cities. "Fall" and "Euro trip" are the wrapper; the reasons to believe are our bag's physical facts, so the ad still reads in spring or for a domestic trip (six-month test) and does not survive with another brand's bag dropped in (swap test). No villain: the three-city dress-code framing is the reference's own grammar and the "don't pack three bags" line is her own packing hassle, not a claim about other bags.

## What the reference does (watched frame by frame, Whisper transcript)

Grid-and-title hook (2x2 real street-style photos, centred serif title, creator in an opaque inset with a mic) → "three fashion capitals, three dress codes" → three chapters (Paris: pack less, understated, "one good bag that works every day"; Milan: polished and intentional, richer colours, start with the shoes; London: experiment, four seasons in a day, walk a lot) → a question close ("Paris, London or Milan, which one are you packing for?"). One photo per item, hard cuts every 2-3s, captions bottom-centre.

What we mirror: the grid hook, the three-city chapter structure, the photo-per-line rhythm, the inset creator, the question close. What we change on law: the list is the hook only, from the product intro every frame is our bag; the house formula sits underneath (verdict hook, `This is the ... from Velantra` by 0:08, attributes, proof, capacity, variants, live offer, link); the close is the live PDP recording.

## Script

See `SCRIPT.md` (lawgate clean, speaker=creator). VO take A: `vo/VO-woman-over-40-A.mp3` + alignment; plain respellings fed to TTS (`Vivian` / `Vehlantra`, no hyphens). Whisper hears "Volantra" for the brand, which it does for every spelling (8/31 benchmark); no pause around either brand word.

## Creator

C2 Helen, 52 (silver-blonde chignon, navy crewneck), reused from OLDMONEY-GRID-01. HeyGen Avatar V render fires only after board approval (`creator/`).

## Hook grid + scene seeds (real Pinterest street-style pins)

Crawled with Apify `fatihtahta/pinterest-scraper-search` (queries: paris / milan / london fall outfit street style). Grid tiles are used as-is (hook only). Scene seeds go through GPT Image 2 pixel-seed i2i on kie (`_build/gen_euro.py`, 2:3 @1K, 6cr, two variants per shot): the pin is the scene, the real product photo is the second input, and only the bag is swapped. Picks in `_build/picks.json`, contact sheets in `keyframes/_qa-*.jpg`.

| pin | role | source |
|---|---|---|
| p003 | grid  | https://www.pinterest.com/pin/1081497298055110238/ |
| p009 | grid  | https://www.pinterest.com/pin/1266706141793107/ |
| p012 |  EURO-P2 | https://www.pinterest.com/pin/1085367578972208937/ |
| p014 |  EURO-P1 | https://www.pinterest.com/pin/501940320993169106/ |
| p016 | grid  | https://www.pinterest.com/pin/319474167338833456/ |
| p017 |  EURO-L1 | https://www.pinterest.com/pin/41869471532107316/ |
| p043 | grid  | https://www.pinterest.com/pin/1083537991635088828/ |
| p053 |  EURO-M1 | https://www.pinterest.com/pin/1085156472732348849/ |
| p059 |  EURO-M2 | https://www.pinterest.com/pin/1103452346274693220/ |
| p073 |  EURO-L2 | https://www.pinterest.com/pin/355151120639843591/ |

## The bed — 16 beats

| beat | in–out | kind | frame | line |
|---|---|---|---|---|
| B01 | 0.00–4.76 | still | B01-GRID-A.jpg | Going to Europe this fall? Don't pack a different bag for Paris, Milan and London. |
| B02 | 4.76–6.70 | keyframe | B02-EURO-P1-v1.png | One bag works in all three. |
| B03 | 6.70–8.60 | still | B03-B03-front-hero.jpg | This is the Vivienne from Velantra. |
| B04 | 8.60–14.38 | keyframe | B04-EURO-P2-v1.png | Paris is where you keep everything understated, slightly undone, like you just threw it on. |
| B05 | 14.38–19.62 | still | B05-B04-O4-fingers-press.jpg | This is soft vegetable tanned leather, so it softens and slouches the longer you carry it, |
| B05b | 19.62–21.88 | still | B05b-B06-O2-clean-front-no-logo.jpg | and there's no logo on it anywhere. |
| B06 | 21.88–26.30 | keyframe | B06-EURO-M1-v1.png | Milan is where you dress it up, way more polished and intentional. |
| B07 | 26.30–29.22 | still | B07-B04b-O5-brass-lock.jpg | That's the belted closure with the aged brass lock, |
| B07b | 29.22–32.37 | still | B07b-detail.png | the rolled handles, and the reinforced leather corners. |
| B08 | 32.37–34.07 | keyframe | B08-EURO-M2-v1.png | It just looks expensive. |
| B09 | 34.07–42.37 | keyframe | B09-EURO-L1-v2.png | London is where you walk all day and it's four seasons in one day, so I clip on the shoulder strap and carry it crossbody. |
| B10 | 42.37–46.43 | still | B10-B05-O10-desk-notebook.jpg | It holds a sweater, my wallet, a water bottle, a real day. |
| B11 | 46.43–48.19 | still | B11-COLORWAY-4up.jpg | It comes in four colors. |
| B12 | 48.19–50.82 | keyframe | B12-EURO-L2-v1.png | It's on pre-order right now, ships in October, |
| B13 | 50.82–53.68 | pdp |  | and they're running a sale on it, so order it before the trip. |
| B14 | 53.68–59.78 | still |  | So tell me, Paris, Milan or London. Which one are you packing for? I left the link below. |

## Flags

The Vivienne is a pre-order shipping October, so the creator's line is a recommendation for the trip, not a lived trip; the VO says 'pre-order' and 'October' out loud and the PDP close settles on the October line. Capacity list (sweater, wallet, water bottle) matches the shipped EVERYTHING-01 list; no laptop claim. 'Structured' never said (banned for this bag); the generated Euro frames read a touch boxier than the product truth's slouch, flagged on the board for Brooks.

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
