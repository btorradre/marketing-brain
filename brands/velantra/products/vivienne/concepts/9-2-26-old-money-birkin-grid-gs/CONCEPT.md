# VEL-VIV-OLDMONEY-GRID-01 — "The Old Money Workday Look" · Birkin-grid greenscreen AI UGC

**Date:** 2026-09-02
**Product:** The Vivienne Top Handle Bag · $149.99 from $199.99 · pre-order, ships October · Chocolate / Cognac / Black / Olive (live PDP checked 9/02)
**Reference:** `instagram.com/reel/Dcjorv-y74O/` (Annalise Salm, 56.4s, "Oversized Travel Bags That Are Actually Chic"). Copy + frames in `reference/`.
**Format:** greenscreen AI UGC, 1080x1920 30fps, one continuous VO, creator keyed bottom-CENTRE and cut by the bottom edge (mirrors the reference), hard-cut stills, centred caption cards above the creator's head.
**Runtime:** 62.0s (VO take A, natural read, no atempo). Reference is 56.4s.
**Board:** pushed to Cutroom / velantra (URL in the handover).
**Status:** BUILT 2026-09-02 (Brooks: "great job now build out the ad"). Shipped cut: `final/VEL-VIV-OLDMONEY-GRID-01-C2-A.mp4` (62.4s, 1080x1920 30fps, -14.1 LUFS). C1/C3 not rendered; C2 Helen + GRID-A shipped as the default pair.

---

## Product call, flagged

Brooks said "for the vivienne" and the script he sent names the **Meridian** twice, with Meridian-shaped
claims (laptop, "doesn't slouch", brass). Built for the **Vivienne** on his explicit product call and
because the Birkin grid hook targets Birkin seekers (the Vivienne is the Birkin-inspired bag by stated
mechanism). The board re-points to the Meridian in one pass if that was the intent: swap the product
frames, restore "laptop" and "doesn't slouch" (both true of the Meridian and both banned for the
Vivienne), and re-run the VO for one line.

## What the reference does (watched frame by frame, transcript via Scribe)

| t | Beat | Screen |
|---|---|---|
| 0:00–0:08 | Hook: "As a girl, sometimes all you need is a massive oversized travel bag… here are some of my favorite travel bags" | **2x2 photo grid** of four bags, big centred serif title "Oversized Travel Bags That Are Actually Chic", creator keyed bottom-centre, chest-up, cut by the bottom edge |
| 0:08–0:56 | One brand per beat, 2–4s per still, hard cuts | screenshots of each brand's IG posts (UI chrome visible), creator stays keyed bottom-centre, small centred captions mid-frame |
| 0:54 | ends on the last brand still, no CTA card | |

Grammar we mirror: grid hook + centred title → hard-cut stills → creator never leaves the bottom
centre. Grammar we change on law: the list is the HOOK only; from the product intro every still is
the Vivienne (a listicle reference donates its look, not its ranking). The close is the live PDP
screen recording and the ad ends there. IG-post chrome is not reproduced (Velantra's IG is banned
and we do not fake posts); our beats are clean full-bleed stills.

## Hook plate: real women, real Birkins

Brooks: "grid hook image showing off different women holding birkin bags, then transition to our
product." Sourced 97 real street-style pins (Apify `fatihtahta/pinterest-scraper-search`, three
old-money/workday queries; crawl index in `plates/birkin-src/index.json`). Nothing generated; the
word Birkin never enters a prompt. Three plates in `plates/`, title set in Georgia Bold like the
reference's serif:

| Plate | Tiles | Read |
|---|---|---|
| **GRID-A-workday** (default on the board) | laptop-on-lap grey suit · white shirt + chocolate Birkin on the street · cream suit + tan Birkin · navy coat + cognac Birkin, heels | the workday version of the look |
| GRID-B-quiet | white shirt + burgundy · brown zip-knit + cream trousers · white shirt + brown, garden · cream coat + grey | quieter, more editorial |
| GRID-C-mixed | black blazer + black · navy coat · garden · street chocolate | darker, more Meta-feed contrast |

Open ruling, same as HAALAND-01 and VIV-CELEB-GS-01: these are third-party photographs of real,
unlicensed people used as hook stills. Brooks's call before it runs.

## Creator

Cast fresh on the HAALAND natural-creator recipe (propped-phone framing, head off centre, one hand
up at collarbone height, lips parted, real window light, flat chroma green) instead of reusing the
8/31 Diane/Bridget/Marguerite passport plates. kie GPT Image 2 text-to-image, 2:3, 6cr each.

| | Look | Green | Verdict |
|---|---|---|---|
| C1 Eleanor, 48 | dark blonde going grey, cream silk blouse, gold hoops | flat, holds | v1 cropped the top of her head; **v2 (`C1v2-*.png`) holds full headroom, green flat** |
| **C2 Helen, 52** | silver-blonde chignon, navy crewneck, pearl studs | flat #00B140, holds | **default on the board** |
| C3 Claire, 45 | honey blonde, camel cardigan, glasses on head | v1 DROPPED the green (dark vignette, same failure as HAALAND's dark-haired roll) | **v2 (`C3v2-*.png`) holds flat #00B140 after the wardrobe/hair lightened and the green line hardened** |

Voice: ElevenLabs **Woman Over 40** (`NBIPq5xdnIg9kaBH5Ape`), eleven_v3 Creative, one take
(`vo/VO-woman-over-40-A.mp3`, ad-engine `job_768665bb0537`). 184 words / 62.0s / 178 wpm. Fed plain
respellings `Vivian` / `Vehlantra` (no hyphens). Audit: median inter-word gap 0.053s, no pause
around either brand word (Vivian 0.36s, Vehlantra 0.96s, both inside the 8/31 benchmarks), Scribe
word-presence gate passes (Scribe hears "Velancia", which it does for every spelling). HeyGen Avatar V
render fires only after board approval.

## The bed — 17 cuts over 62s

Beat boundaries come off the alignment (`vo/VO-A-anchors.json`); machine-readable in `beat-map.json`;
board frames in `board-frames/`. Zero new product generation: every product still is a QA-passed
frame from the 8/31 Omni library, the PDP colorway set, or the editorial set.

| Beat | In → Out | Source | Line |
|---|---|---|---|
| B01 | 0.00–7.01 | GRID-A plate + title | Every woman wants that old money workday look, but nobody tells you how to actually get there without spending thousands. |
| B02 | 7.01–10.91 | O9 shoulder carry, hallway | That is until now, because this is the bag I bring everywhere, |
| B02b | 10.91–15.46 | Chocolate lifestyle (carried) | and people ask me where it's from constantly. |
| B03 | 15.46–18.29 | Chocolate front hero | This is the Vivienne from Velantra. |
| B04 | 18.29–20.49 | O4 fingers press the leather | It's soft vegetable tanned leather |
| B04b | 20.49–22.66 | O5 brass lock macro | with aged brass hardware, |
| B05 | 22.66–27.41 | O10 desk, notebook, mug | and it fits my planner, a water bottle, everything I carry in a day. |
| B06 | 27.41–32.27 | O2 clean front | It doesn't look like a work bag. It doesn't have a logo. It doesn't need one. |
| B07 | 32.27–34.60 | editorial bench | It just looks expensive. |
| B08 | 34.60–39.06 | O3 passenger seat | I don't want to carry three different bags for one day, and I know you don't either. |
| B09 | 39.06–40.96 | Chocolate three-quarter | That's why I carry the Vivienne. |
| B10 | 40.96–46.40 | Cognac lifestyle (carried) | You put your whole day in there and it still looks like an accessory, not a carry-on. |
| B11a | 46.40–49.80 | O1 morning counter | If you've been trying to find something that works for a nine a.m. meeting |
| B11b | 49.80–53.31 | O12 chair back, lamp | and drinks after, this is going to be the one. |
| B12 | 53.31–57.08 | four-up colorway card | If you want that old money look every single day like me, |
| B13 | 57.08–58.80 | **live PDP screen recording, continuous** | I'm going to leave a link on this video. |
| B14 | 58.80–62.40 | PDP settles on "Expected to ship October", holds | They do sell out, so grab yours while you can. |

Average cut 3.6s (reference averages ~3s). Two-still beats (B02, B04, B11) keep the eye moving on
the long sentences. No open-bag or interior frame exists and none is faked (lining unconfirmed).

## Script

`SCRIPT.md` carries the shipped text and every edit made to the script Brooks sent, with the
product-truth reason for each. Summary: dashes out; Meridian → Vivienne; "full grained / hand-antiqued"
→ "vegetable tanned / aged brass"; laptop dropped (uncleared capacity claim); "doesn't collapse or
slouch" dropped (the Vivienne is slouchy by truth). "They do sell out" kept and flagged (pre-order).

## Composite spec (for the build after approval)

Per the 8/31 edge-cut law: size on the HEAD, head width 0.20 W, head centre at 0.50 W (reference
keys her centre, like INVEST-01), 60px bottom bleed. Measured off C2's plate: scale 0.513, overlay
x=330 y=1192, head top y≈1256, so caption cards sit at y≈1120 max, centred, 1–2 lines, white bold,
soft stroke. ffmpeg chromakey on the sampled green (sweep per render, never inherit) similarity
0.08 blend 0.03, despill green 0.15. The `_build/mock-*.jpg` frames are a crude PIL key for the
board only; the fringe on the hair is the mock, not the build.

## Build log (9/02)

- **HeyGen Avatar V** from `creator/C2-helen-52-navy-chignon-green.png`, driven by take A. Look created,
  polled to `completed`, submitted `type:avatar` + `engine:avatar_v` (payload logged in
  `creator/renders/_state.json`). Plate came back 1080x1620 @ 25fps, green `0x00B430`. Head-region
  frame deltas 6.3-11.3 across six samples (healthy 7-10): gestures through the whole take.
- **PDP** recaptured live 9/02 (`pdp/capture_pdp_scroll.py`, 5.5s @ 30fps, 500 CSS px, DPR 3):
  $199.99 struck to $149.99, four swatches, Add to Cart, settles on "Expected to ship October".
- **Composite** (`_build/build_ad.py C2`): head width 0.20 W, centred, 60px bleed → 541x812 at
  x=320 y=1168, head top 1230. Captions 52px Arial Bold, centred, bottom edge at y=1110, 33 cards
  off the alignment with an orphan-merge pass (no 1-2 word cards). Cards over the PDP page carry a
  feathered dark scrim (plain white text was unreadable over the description block).
- **Key sweep on this plate:** 0.08/0.03 left a faint grey outline on the hair against the light
  PDP; 0.12/0.05 is clean; alpha erosion was cleaner still but eats the edge; despill mix 0.35
  turned her pink (the 0.5-pink law holds at 0.35 too). Shipped 0.12/0.05, despill 0.15.
- **Audio:** loudnorm I=-14 single-pass landed -15.4; +1.4 dB trim → -14.1 LUFS, TP -0.1.
- HeyGen wallet was $9.28 with auto-reload on before the render.

## Variants not built (cheap on request)

`KEY_SIM=0.12 KEY_BLEND=0.05 GRID=GRID-B-quiet python3 build_ad.py C2` swaps the hook plate in ~1 min.
C1/C3 need one HeyGen render each (`creator/renders/render_heygen.py C1 C3`) then the same command.

## Next on approval (original plan, superseded by the build above)

1. Brooks picks grid plate (A/B/C) and creator (C1/C2/C3) on the board, approves the keyframes.
2. HeyGen Avatar V render from the chosen still, driven by take A (~100 api credits).
3. Capture the PDP screen recording fresh on ship day (500px CSS width, settles on the pre-order line).
4. `_build/build_ad.py` (port of INVEST-01's) assembles: grid + title → stills → PDP, creator keyed centre, caption cards off the alignment. Deliver the full path.
