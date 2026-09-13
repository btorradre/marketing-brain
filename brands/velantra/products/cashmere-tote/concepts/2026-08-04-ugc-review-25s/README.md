# VEL-COLETTE-UGC-REVIEW-03

> **⚠️ PRICE CLAIM NOW WRONG, 2026-08-08.** This ad's VO says "40 dollars off" and the live
> offer is **$30 off ($119.99 from $149.99)**. The transcript below is left as shipped, as the
> record. **The cut itself should be pulled or the offer line re-cut before it runs again.**


**Delivered 2026-08-05.** 28.1s, 720x1280, 9:16, 24fps, 48kHz, -13.5 LUFS. Avatar: Blair (velantra-ugc roster).
Angle: fits everything, does not look like it.

## Final file
`VEL-COLETTE-UGC-REVIEW-03.mp4` — **this is the deliverable.**
`-02.mp4` and `-01.mp4` are the earlier passes, kept only for comparison. Do not run them.

## Transcript (unchanged from v2)
> If you're looking for the perfect fall bag, I have it. This is the Colette from Velantra. It's Loro Piana inspired, so it's that soft belted shape that stands up on its own. Brushed wool body, twenty inches across, so a laptop, a water bottle and a sweater all fit. No logo anywhere. They're running a pre-order, so you get 40 dollars off.

## What v3 changed

**1. The middle voiceover was robotic.** v2's middle was an `eleven_multilingual_v2` clone at default settings — flat pitch contour, even syllable spacing, no breaths, and it mispronounced "Loro Piana" as *low-ro py-ana*. Blind A/B against the real on-camera voice scored it 2.5/10.

Fix: Blair re-cloned from **both** shipped Seedance segments (A1v2-take2 + A3v2-take2, ~14s of clean speech) instead of A1 alone, then regenerated on **`eleven_v3` with the Creative preset** (stability 0.0, similarity 0.85). Three candidates were cut and judged blind against the reference; the plain-script take won at 9.5/10 and says "Loh-roh pee-AH-nah" correctly. Tagged and higher-similarity variants both scored lower (stiffer pacing, more announcer).

The VO is generated as **one continuous pass over the whole script**, not just the middle — v3 is unstable under ~250 characters, and running the full script gives the middle its prosody from the hook that precedes it. The middle is then sliced out on its own word timestamps, so it flows out of A1 the way one take would.

**2. Room match on the splice.** ElevenLabs returns a dry close-mic take; A1/A3 carry the Seedance room, so the first cut read as an acoustic change even though the voice matched. The VO now gets a short early-reflection tail plus the A1 room-tone bed at -24dB. Seam scores went 6.5 → 8 and 7.5 → 8; a viewer on a phone does not hear either splice.

**3. "Loro Piana inspired" is now a full-bag pan.** It was a locked-off macro of one gold disc cap — a detail shot on the line that has to sell the whole object. Replaced with `COL-091-pan-full-bag`: a slow lateral glide past the bag on a bench in window light, whole bag in frame for the entire move.

**4. The packing beat is one continuous shot.** v2 cut three times across "a laptop, a water bottle and a sweater" (three separate library clips). Replaced with `COL-092b-pack-continuous-three`: one unbroken 5.7s take, hands lowering the laptop in, then the bottle, then the sweater, camera locked. The wide-mouth-hero cut was dropped with it — the packing shot proves the width better than a static shot of the opening does.

## Cut sheet

| Time | Source | Beat |
|---|---|---|
| 0:00–7.7 | **A1** (Seedance, A1v2-take2) | Hook + name. Bag up in both hands, never set down |
| 7.7–10.3 | **COL-091 pan (new)** | "It's Loro Piana inspired, so" |
| 10.3–12.2 | macro-side-gusset | "it's that soft belted shape" |
| 12.2–14.2 | setdown-park-bench | "that stands up on its own." |
| 14.2–16.3 | KB felt-fibre (locked off) | "Brushed wool body," |
| 16.3–21.9 | **COL-092b continuous pack (new)** | "twenty inches across, so a laptop, a water bottle and a sweater all fit." |
| 21.9–27.9 | **A3** (Seedance, A3v2-take2) | Hand across the blank front on "no logo anywhere," then the offer |

B-roll cuts are locked to the new VO's real word timestamps (`_v3/vo/cand-A-mid-words.json`), not estimates.

## How the two new clips were made

GPT Image 2 i2i keyframe → Omni i2v, on the exact prompt machinery that built the 200-clip library (`_v3/newshots.py` imports the library's `build_prompt`, so product truth and the photoreal footer are byte-identical). 3 variants per shot, judged against the canonical reference for product truth, width ratio, framing and photoreal before animating.

**The packing shot took three animation passes:**
- r1 and r2 both grew an **Apple logo** on the plain silver laptop lid. Omni resolves an ambiguous silver slab into a MacBook; prompting "unbranded" in the motion did not stop it. Fixed at the keyframe instead — the laptop is now matte charcoal and held **edge on**, so no lid face is toward camera. Logo gone.
- Both early passes also drifted the silhouette rounder over the back half. The hardened motion block (fixed-object clause + explicit no-new-hardware NEVER list + "all three items in within five seconds") held the shape through the whole clip.

**The snap tab on the inner rim is real, not drift.** Every pass grew a felt tab with a gold stud at the top centre of the inner rim, and I nearly re-rolled it away — `colette-v3-caramel-interior.png` shows exactly that tab on both the front and back inner rims. The library's product-truth text says "no closure of any kind on the mouth," which contradicts the interior reference. **The text is wrong, not the render.** Worth correcting in `broll-library-2026-08/pipeline.py:colette_id()` before the next library run, since 200 clips were prompted against it.

## Assets
- `VEL-COLETTE-UGC-REVIEW-03.mp4` final
- `_v3/vo/` — script, 3 v3 candidates, word timestamps, the sliced middle
- `_v3/voice/` — the clone source audio pulled from both shipped segments
- `_v3/keyframes/`, `_v3/clips/` — new shots, all variants kept for audit
- `_v3/qa/` — contact sheets and frame strips from the drift audits
- `_v3/newshots.py` (scenes + gen), `_v3/tts_v3.py`, `_v3/slice_mid.py`, `_v3/build.py` (the whole recut is one command)
- `broll/KB-075-felt-fibre-4s.mp4` — re-rendered; the 1.4s version in `broll/` was pre-trimmed for v2 and is too short for this cut
- `segments/`, `broll/`, `_build_v2/` — v2 material, unchanged

## Voice
`velantra-blair-colette-0805` → `5VJqyR650KC1jubNlVCG` (registered in `voice-registry.json`).
Model `eleven_v3`, stability 0.0 (Creative), similarity 0.85, speaker boost on.
The v2 voice `velantra-blair-colette-0804` / `ty8g1dhngZewrdjVKuI7` is superseded.

## Open items

1. **Ear check the two splices.** Machine-judged 8/10 both ways, level-consistent, no dead air. If the middle still reads slightly boxy to you, the cause is the `aecho` tail in `build.py` — lower the three gains and rebuild.
2. **Ear check "Velantra."** Speech-to-text returns "Volantra" on some passes and "Velantra" on others, from the same audio. Same as v2; a human ear check is still the only way to close this.
3. **No burned captions yet.** House style is white bold rounded sans, thin black outline, lowercase sentence case, one word per card across the capacity beat.
4. **October ship date is still the unconfirmed supplier placeholder.** The ad says "pre-order" without naming a month, so this cut is safe either way.
