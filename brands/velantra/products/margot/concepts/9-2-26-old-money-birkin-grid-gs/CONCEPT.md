# VEL-MER-OLDMONEY-GRID-01 — "The Old Money Look" · Birkin-grid greenscreen AI UGC (Meridian)

**Date:** 2026-09-02
**Product:** The Meridian Leather Tote (`velantra-margot-tote`, assets under `products/margot/`) · $124.99 from $149.99 · six colorways live (Brown, Midnight Black, Coffee Brown, Cream, Taupe, Burgundy)
**Reference:** `instagram.com/reel/Dcjorv-y74O/` (Annalise Salm). Same mirror as the Vivienne build (`products/vivienne/concepts/9-2-26-old-money-birkin-grid-gs/`), which carries the full reference breakdown.
**Format:** greenscreen AI UGC, 1080x1920 30fps, one VO, creator keyed bottom-centre and cut by the bottom edge, hard-cut stills, centred caption cards, live PDP close.
**Runtime:** 57.1s (VO 56.7s, natural read, no atempo).
**Status:** BUILT 2026-09-02 on "now same thing for the meridian".

## Differences from the Vivienne build (deliberate)

- **Creator C1 Eleanor** (cream silk, 48) instead of C2 Helen, so the two ads do not read as the same woman selling two bags in one feed. Same casting recipe, same voice.
- **GRID-B plate** (the quieter tile set) with the title "The Old Money Look / and what actually makes it work", so the hook is not a pixel copy of the Vivienne ad's.
- **Product frames from the Meridian's own 8/02 real-room library** (`broll/library-2026-08/stills/VEL-MAR-*`, 90 stills: commute, office, cafe, car, home, packing, macros) plus two PDP stills and a six-up colorway card. `VEL-DUO-*` stays banned. Zero new product generation.

## Claim check against `margot/PRODUCT-TRUTH.md` and the live PDP (9/02)

| Line | Truth | Verdict |
|---|---|---|
| grained leather | PDP "premium grained leather"; grade unknown | holds ("full grain" dropped) |
| polished silver hardware | silver/palladium in every photo | holds (sent script said brass: wrong) |
| the most perfect slouch / settles / drapes | PDP "softly structured"; on-model photos show the body relaxing | holds as an angle; "doesn't hold its shape" dropped because the PDP says "holds its line" |
| laptop, planner, everything | real laptop photographed inside | holds |
| six colorways on the card | six live variants | holds |
| $149.99 struck to $124.99 | live | holds |
| They do sell out | page carries backorder strings; ~1,760 oversold on 8/21 | true, but **traffic is blocked until a restock date is on the page** |

⚠️ The live PDP still carries the false "Drum-Dyed Full-Grain" and "Florentine Brass Hardware"
blocks lower down (product truth flags both). The PDP capture scrolls only from the title to Add to
Cart plus the description top, so neither block is ever on screen next to a VO that says silver.

## The bed — 21 beats over 57.1s (`beat-map.json`, frames in `board-frames/`)

| Beat | In | Source | Line |
|---|---|---|---|
| B01 | 0.00 | GRID-B + title | Every woman wants that old money look with her bag… |
| B02 | 5.31 | MAR-002 crook of the arm, coffee | That is until now, because this is the bag I carry every single day, |
| B02b | 9.01 | MAR-013 cognac, sidewalk | and people ask me where it's from constantly. |
| B03 | 12.35 | PDP brown three-quarter | This is the Meridian from Velantra. |
| B04 | 14.80 | MAR-079 grain macro | It's grained leather |
| B04b | 16.00 | MAR-077 silver turn-lock macro | with polished silver hardware, |
| B05 | 17.38 | MAR-014 black carried, soft | and it has the most perfect slouch. |
| B06 | 19.81 | MAR-047 cognac leaning on the floor | It doesn't sit stiff and rigid like a work bag. |
| B06b | 22.21 | MAR-048 armchair | It doesn't look like it's trying too hard. |
| B07 | 24.43 | MAR-046 unmade bed | It just settles. It drapes. |
| B08 | 26.83 | MAR-087 set down on the bar | It looks like it's been yours forever. |
| B09 | 29.12 | MAR-007 coffee balance | I don't want a bag that screams effort, and I know you don't either. |
| B10 | 32.88 | PDP brown on-model | That's why I carry the Meridian. |
| B11 | 34.60 | MAR-053 open overhead | You throw your whole day in there, |
| B11b | 36.48 | MAR-061 laptop sliding in | laptop, planner, everything, |
| B11c | 38.74 | MAR-009 crosswalk, full and soft | and the slouch just makes it look even better. |
| B12 | 41.41 | MAR-045 entry console | If you've been looking for that effortless, lived-in leather bag |
| B12b | 44.69 | MAR-089 picked up off the desk | that actually gets more beautiful over time, this is going to be the one. |
| B13 | 48.83 | six-up colorway card | If you want that old money look every single day like me, |
| B14 | 52.12 | live PDP scroll, continuous | I'm going to leave a link on this video. |
| B15 | 53.86 | PDP settles on Add to Cart + description | They do sell out, so grab yours while you can. |

## Build

VO: Woman Over 40, eleven_v3 Creative, one take, 185 words / 56.7s / 196 wpm, no pause around the
brand words (Meridian 0.52s, Vehlantra 1.08s), Scribe word gate passes. Creator: C1 Eleanor on
HeyGen Avatar V (`creator/renders/`). PDP: `pdp/capture_pdp_scroll.py` (5.2s, scroll 860 → 1150 CSS
px at 500 wide). Assembler: `_build/build_ad.py C1` (port of the Vivienne build: head 0.20 W centred,
60px bleed, key 0.12/0.05, despill 0.15, captions above the head, scrim from 52.0s, loudnorm -14).

## Build log (9/02, "great now build out")

- **HeyGen Avatar V** from `creator/C1v2-eleanor-48-cream-silk-green.png` driven by take A; plate 1080x1620,
  green came back `0x0D8C31` (darker than C2's `0x00B430`: sweep per render, never inherit). Head-region
  deltas 5.4 to 13.3 across six samples, gestures through the take.
- **Composite:** head 0.20 W centred, 60px bleed → 592x888 at x=287 y=1092, head top 1314. Key 0.12/0.05,
  despill 0.15, 34 caption cards, scrim from 52.0s over the PDP page.
- **Audio:** loudnorm I=-14 then +1.4 dB left the true peak at 0 dBTP on both ads. ffmpeg's `alimiter`
  auto-levels back up unless `level=false`; with `limit=0.84:level=false` the cut lands **-14.5 LUFS,
  -0.8 dBTP**. The Vivienne cut was re-exported with the same chain (-14.5 LUFS, -1.2 dBTP).
- **Shipped:** `final/VEL-MER-OLDMONEY-GRID-01-C1-B.mp4` (57.1s). Board `http://localhost:8765/b/vel-mer-oldmoney-grid-01`.
- Variants not built: `GRID=GRID-D-street` on the same command; C3 needs one HeyGen render.
