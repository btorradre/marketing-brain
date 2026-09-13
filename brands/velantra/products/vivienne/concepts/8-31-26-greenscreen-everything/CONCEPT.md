# VEL-VIVIENNE-GS-EVERYTHING-01 — "One bag that holds everything," greenscreen AI UGC

**Date:** 2026-08-31
**Product:** The Vivienne Top Handle Bag · $149.99 from $199.99 (Save $50.00) · pre-order, first run ships October · Chocolate / Cognac / Black / Olive
**Format:** greenscreen AI UGC. Creator keyed as a PiP for the full runtime over full-frame b-roll, burned word-synced captions, one continuous VO, 1080x1920, 24fps
**Runtime:** 25.31s (dead space removed)
**Funnel:** TOF
**Source:** our own live ad `instagram.com/p/DcaPXM8Asrn` = `VEL-VIVIENNE-EVERYTHING-01`, 34.25s

---

## What this is

The live Vivienne "everything bag" VO ad, **script held word for word**, moved out of the
silent-b-roll format and into the greenscreen format proven by DC-04 / BLK-01 / GS-BIRKIN-01.

**The script did not move. The voice did.** Brooks directed ElevenLabs **Woman Over 40**
(`NBIPq5xdnIg9kaBH5Ape`), so the audio is a fresh one-take render, not the shipped file:

- VO: `_engine/mcp/ad-engine/data/vo/job_b9c9c407cad7/voiceover.mp3` — **28.96s**
- Alignment: `.../job_b9c9c407cad7/alignment.json` — drives the caption cards
- eleven_v3, Creative preset. STT-gated: all 87 words present, nothing dropped.

She reads at ~180wpm against the original's ~154, so the ad lands **5.3s shorter than the
live cut** and the whole bed re-times off her. **The read ships as-is. No atempo** — that is
what made the men's greenscreen cut sound robotic.

### Claim check, run 2026-08-31 against the live PDP

| Line | Live PDP | Verdict |
|---|---|---|
| "Fifteen inches across" | product truth, 15" | holds |
| "soft vegetable-tanned leather" | "Vegetable-tanned leather, no canvas" | holds |
| "reinforced corners" | "The corner caps, the gussets and the piping are the same leather" | holds |
| "brass feet" | product truth, aged brass | holds |
| "no logo anywhere" | "The leather, not the logo" | holds |
| "It comes in four colors" | Chocolate, Cognac, Black, Olive | holds |
| "twenty five percent off right now" | $199.99 → $149.99, Save $50.00 = exactly 25% | holds |
| "the first run ships in October" | "Expected to ship October" | holds |

---

## Script (locked, verbatim, as spoken in the live ad)

> If you want one bag that holds everything, I found it.
> This is the Vivienne from Velantra.
> Fifteen inches across, soft vegetable-tanned leather, reinforced corners, brass feet, and no logo anywhere.
> It's a soft bag, so it takes the shape of whatever you put in it instead of fighting you.
> A folder, a water bottle, a sweater and your wallet, all at once.
> It comes in four colors.
> It's twenty five percent off right now, and the first run ships in October.
> I left the link below.

88 words. TTS input feeds `Viv-ee-EN` and `Vell-Ahn-Trah`; the plain spelling stays in the
captions via the respell map.

---

## The three creators

Brooks directed: **women over 50, sourced from Pinterest.** Three pins were picked from a
90-pin crawl (`creators/refs/`, crawl index saved for reproducibility). Each pin is a **look
reference only** — age, hair, colouring, styling register. The person rendered is synthetic
and is not a copy of anyone in a pin.

| | Who | Look | Register |
|---|---|---|---|
| **A** | Diane, 58 | silver-blonde to the shoulders, freckles and sun lines, cream chunky knit | warm, the neighbour everybody trusts |
| **B** | Bridget, 53 | dark brown to the collarbone, grey coming through at the temples, rust fine knit | warm, practical, no-nonsense |
| **C** | Marguerite, 62 | sharp silver bob to the jaw, thin gold chain, black turtleneck | cool, precise, the friend with taste |

Keyframes: `creators/{A-diane,B-bridget,C-marguerite}-green.png` (kie
`gpt-image-2-text-to-image`, 2:3, 2K, native chroma green, hands out of frame, 10-15%
headroom, anti-polish cues on every prompt). Generator: `creators/gen_avatars.py`.

**One shared VO drives all three**, so the bed, the captions and every timing are identical
and only the creator changes — a clean creator-only A/B/C, same design as GS-BIRKIN-01.

---

## The bed — 14 cuts over 28.96s

Cut points sit inside beats; **beat boundaries are the alignment's own sentence ends.**

| Cut | In → Out | Source | PiP | Spoken over it |
|---|---|---|---|---|
| c01 | 0.00 – 1.55 | O1 counter, keys + mug | L | If you want one bag |
| c02 | 1.55 – 3.12 | O8 unmade bed | L | that holds everything, I found it. |
| c03 | 3.12 – 5.28 | O12 over the chair back | R | This is the Vivienne from Velantra. |
| c04 | 5.28 – 7.10 | O3 passenger seat (scale) | L | Fifteen inches across, |
| c05 | 7.10 – 9.00 | O4 fingers press, it gives | L | soft vegetable-tanned leather, |
| c06 | 9.00 – 10.60 | O11 braided corner macro | L | reinforced corners, |
| c07 | 10.60 – 11.90 | **GAP-01 brass feet** | L | brass feet, |
| c08 | 11.90 – 13.01 | O2 grab off the bench, clean front | L | and no logo anywhere. |
| c09 | 13.01 – 15.10 | O10 handles released, it settles | R | It's a soft bag, so it takes the shape |
| c10 | 15.10 – 17.36 | O9 on the hip, moulding | R | of whatever you put in it instead of fighting you. |
| c11 | 17.36 – 19.60 | O1 (late in-point) keys + receipt | L | A folder, a water bottle, |
| c12 | 19.60 – 21.97 | O8 (late in-point) sweater | L | a sweater and your wallet, all at once. |
| c13 | 21.97 – 23.71 | four-up colorway card | R | It comes in four colors. |
| c14 | 23.71 – 28.96 | **live PDP screen recording, continuous** | L | It's twenty five percent off right now, and the first run ships in October. I left the link below. |

Average cut 2.07s. Machine-readable: `beat-map.json`. Board frames: `board-frames/`.

### The close is one unbroken screen recording

**c14 runs 5.25s and carries the entire offer and CTA. The ad ends on the website — it never
cuts back to the bag.** O7 (walking out the front door), which closed the live ad, is dropped.

One slow continuous downward scroll, no cuts inside it:

| ~t | On screen |
|---|---|
| 23.7s | title, $199.99 struck to $149.99, Save $50.00, four swatches |
| ~26.2s | Add to Cart, free shipping / returns line, icon bar |
| ~28.2s | the pre-order paragraph — "expected to ship October" — **settles and HOLDS to the last frame** |

Editor option if the hold feels soft: on "I left the link below," ease the scroll back up so
it lands on Add to Cart instead. Do not cut — it stays one continuous move either way.

### Why the bed differs from the live ad's

1. **O6 (bag on the cafe floor) is cut entirely.** She would not set a leather bag on a cafe
   floor; the situational-plausibility law kills the shot. It carried "a water bottle" in the
   live ad and is replaced by O1's late in-point.
2. **"brass feet" had no frame.** Every claim owns a frame in this house, and the library has
   no base shot — O11's brass rivet is a corner rivet, not a foot. **GAP-01** was generated to
   close it: a table-level macro of the base showing the stitched cognac corner cap and two
   aged brass feet standing the bag off the wood. Seeded i2i from
   `source/tiktok/SEED-real-bag.jpg`, the supreme real reference.
3. **O7 is dropped** so the close stays on the PDP (above).

**GAP-01 is a still and cannot ship as one.** No Ken Burns fill: it goes to Omni for a 1.3s
live move before assembly, like the rest of the library.

### Also true of the bed

- **No face appears in any b-roll cut.** O9 is shot from behind. The keyed creator is the only
  person on screen for the whole runtime (one-creator element lock).
- **Colorways are the real per-colorway renders** (`product-images/colors/*/front.png`),
  never a recolour.
- **The PDP recording is captured the day the ad ships.** 500px CSS window width — 390 and 430
  clip the theme's title.

---

## Production recipe

| Step | How |
|---|---|
| VO | `job_b9c9c407cad7/voiceover.mp3`, Woman Over 40, eleven_v3 Creative, one take. Ship the natural read. No atempo, ever. |
| Creator render | HeyGen: upload keyframe → create photo avatar → `engine.type: avatar_v`, 1080p. ~205 api credits per 29s render; check `GET /v3/users/me` `wallet.remaining_balance` first. |
| Key | sweep the green per creator — HeyGen's green differs per source. Start `chromakey=<measured>:0.10:0.02` + `despill=type=green:mix=0.15`. Never 0.5 mix: it goes pink. |
| PiP | 32% of frame width, bottom-anchored, side alternating per beat as tabled above. |
| Captions | build from `job_b9c9c407cad7/alignment.json` with the card builder in `../8:22:26 - vivienne launch VO x3/build_ads.py`; respell `Viv-ee-EN` → Vivienne, `Vell-Ahn-Trah` → Velantra. Cards at y=1500. Scribe spells the brand by ear — respell before drawing cards. |
| Assembly | one ffmpeg pass, 1080x1920, 24fps CFR, VO at -14 LUFS, b-roll audio muted. |

⚠️ This machine's ffmpeg has no libass and no drawtext — caption cards are Pillow-rendered
and overlaid.

---

## BUILT — 2026-08-31

Brooks said build it, so the approval gate was skipped and all three creators shipped.
**Editable ChatCut project:** `app.chatcut.io/editor/7b36a20c-2baa-4862-bec3-c7eaa459d6be`
Three timelines, one per creator: **A — Diane** (24fps), **B — Bridget** (30fps),
**C — Marguerite** (30fps). All three are 25.31s; only the creator changes.

### Dead space removed — the VO is now 25.31s

`vo/tighten_vo.py` cut **3.65s** of silence out of the Woman Over 40 read (28.96 → 25.31s):
22 silences found, 12 compressed. Gaps under 0.22s are left alone (plosives and breaths are
speech rhythm; squeezing those is what makes a read sound clipped), anything longer collapses
to 0.15s, head and tail trim to 0.04s. **No sample is time-stretched — this is not atempo.**
STT-gated after the cut: all 87 words survive. Output `vo/VO-tight.mp3`, remapped word
timings `vo/words-tight.json`.

### The bed, as built — 14 cuts over 25.31s

| Cut | In → Out | Source | PiP |
|---|---|---|---|
| c01 | 0.00 – 1.40 | O1 counter | L |
| c02 | 1.40 – 2.80 | O8 bed | L |
| c03 | 2.80 – 4.66 | O12 chair back | R |
| c04 | 4.66 – 5.90 | O3 passenger seat | L |
| c05 | 5.90 – 6.90 | O4 fingers press | L |
| c06 | 6.90 – 7.81 | O11 braid macro | L |
| c07 | 7.81 – 9.91 | **GAP-01 base + brass feet** | L |
| c08 | 9.91 – 11.50 | O2 grab off bench | L |
| c09 | 11.50 – 13.60 | O10 settles on table | R |
| c10 | 13.60 – 15.31 | O9 on the hip | R |
| c11 | 15.31 – 17.35 | O1 late in-point | L |
| c12 | 17.35 – 19.39 | O8 late in-point | L |
| c13 | 19.39 – 20.85 | colorway four-up | R |
| c14 | 20.85 – 25.31 | **PDP screen recording, unbroken** | L |

GAP-01 came back from Omni showing the stitched cognac corner cap AND two brass feet in one
frame, so it carries "reinforced corners, brass feet" together. **Only its first 2.10s is
used** — the Omni clip drifts wider after that; the used window is locked off and clean.

### Production truths learned this build

| Gotcha | Fix |
|---|---|
| HeyGen `/v3/assets` 400s on a raw-body POST | it is **multipart** — `curl -F file=@` |
| A photo avatar lands `status: processing`, `image_width: 0`; the video submit fails "missing image dimensions" | **poll `GET /v3/avatars/{id}` until `completed`** before submitting |
| The video POST returns `data.video_id` | not `data.id` |
| **HeyGen's green differs per creator** | swept every time: A `0x008922`, B `0x00BA5F`, C `0x00923A`. Keyed at `0.10:0.02` + despill `mix=0.15`; 0% fringe, cream knit unshifted |
| **ChatCut's importer transcoded the alpha webms to mp4 and killed the alpha** — the PiP rendered as a solid rectangle | the importer only transcodes when `videoTranscodeReason` fires; the trigger here was **source bitrate over 8 Mbps**. Re-encoded the VP9 alpha under it (~6 Mbps) and all three came back **"source accepted"** — uploaded untouched, alpha intact |
| **`manage_timelines duplicate` does NOT preserve fps** — it resets to 30 and silently re-times everything | build each variant as a fresh timeline with frames recomputed at 30fps. A is 24fps because `create_project` set it; all three are still 25.31s in real time |
| Scribe spelled the brand **"Velentra"** on every timeline | `set_card_text` → "Velantra" on all three. Always audit this card |
| Captions defaulted to y1414, across the creator's face; y1640 put them ~90% down, inside the Reels/TikTok UI zone | **y1580** — her chest line, ~250px of bottom clearance |
| `rm -f v2_*.jpg` with no match aborts the whole zsh command | unmatched globs abort; guard or skip the `rm` |

### Still open

- Brooks picks which cut(s) actually run. All three are exportable as-is.
- Nothing has been exported to a file — the deliverable is the editable project.
