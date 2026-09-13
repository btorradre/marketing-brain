# VEL-COLETTE-LOOKRICH-01 · creator layer, BUILT

Brooks supplied a real photo on 2026-08-29 and rejected the generated avatar as reading too AI. This is that photo, animated. **Her face is never regenerated at any step**, only the background is replaced and the mouth is driven by the VO.

## Deliverables

| File | What |
|---|---|
| `creator-green.mp4` | HeyGen Avatar V render, 1080x1920, 43.03s, 25fps, flat green plate |
| **`creator-green_matte.webm`** | **The one the editor uses.** VP9 with a live alpha channel, keyed and verified |
| `108283fce2817fac9a4acde747b2e5be.jpg` | Brooks's original photo, untouched |
| `step1-cropped-nobag.png` → `step2-cutout.png` → `step3-greenscreen.png` | The prep chain |

## Prep chain, and why each step exists

**1. Cropped to 744x1322.** The original had a **white handbag with a tan leather tab and silver D-ring hardware** in the bottom-right corner. That is a second product on screen and it breaks the one-product law, so the frame was cut at y=1322, clear of the bag's top edge at ~1340. 744x1322 is 9:16 to within a rounding pixel, so nothing was letterboxed.

**2. Background removed**, then composited onto flat `#00B140`. The source was a car interior, which is not keyable. Removing it and laying in a real chroma plate is what makes the cutout possible.

**3. HeyGen photo avatar** from the green plate. Group `26b262f87f1d49ca9bfc2b8bf6c595f9`, look reports `avatar_v` in `supported_api_engines`.

**4. Rendered on `avatar_v`** driven by `audio_asset_id`, so HeyGen lip-syncs to our exact ElevenLabs mp3. No HeyGen voice, no script field, no re-read. Video `c65575e036618bda575e307c8eaf318c`.

## Key settings, measured not guessed

The render's plate came back at **`#09AC37`, green stdev 1.1**, which is about as flat as a plate gets.

- **chromakey `0x09AC37:0.10:0.03`.** Inside the house range of 0.08 to 0.10 similarity, 0.03 blend.
- **Despill 0.** Tested at 0, 0.20, 0.35 and 0.50 and counted green-dominant survivors across the whole subject at every level: **zero at all four**. There is no fringe to remove, so no despill runs, which also removes the pink-garment risk entirely.
- Red-card test passed. Subject fully opaque, no card bleeding through the navy puffer or the face. Alpha verified live on the finished webm at 30.9% background coverage.

Bottom frame corners read dark in the red-card test because her hair fills the frame edge to edge down there. That is the subject, not a key failure.

## Cost

Wallet went $5.27 → $17.60 across the render, so roughly **$2.67 spent** and the $15 auto-reload fired on cue. The legacy `api: 316` number was meaningless as usual.

## Note before this ships

HeyGen photo avatars of a real, identifiable person need the consent record on file. Worth confirming that is sorted.

## Next

Comp `creator-green_matte.webm` against §5 of `../2026-08-29-VEL-COLETTE-LOOKRICH-01.md`, at roughly a quarter of frame height, roaming positions per beat, dropping out entirely for the load-in run at 0:30.4 to 0:34.0 and returning on the set-down.
