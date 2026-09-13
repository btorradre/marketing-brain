# Freja New York → Velantra Bow Tote — 1:1 Replication Pack (2026-07-08)

Three scaling Freja NYC ads (217 live ads, 1.83M total reach) replicated 1:1 for the **Velantra Bow Tote (denim colorway)**. Frame-by-frame teardown, reference videos, and Ad Library links live in the earlier run folder: `brands/velantra/products/meridian/concepts/7:7:26 - freja 1to1 replication/` (that run targeted the wrong product — the formats and beat maps there are the source of truth; this folder is the corrected Bow Tote production).

Product truth used in every prompt: small ivory cotton canvas tote, boat silhouette, twin ivory canvas handles, denim blue ribbon with white contrast stitching through gold oval grommets tied in a front bow, tiny gold feet, cream interior fully lined in small blue floral print + matching floral slip pocket, no logos.

| # | Concept | Format | Engine | Final |
|---|---|---|---|---|
| 1 | VEL-BOWTOTE-FREJA-01 café stills | 4 stills × 1s hard cuts, 9:16, caption top-center: "A pretty bag designed / for more than special occasions." (same reframe skeleton as Freja's "work bag / more than the office", adapted to product truth) | GPT Image 2 i2i (jobs 6d3bde0e/20bc5d90/fd653f5b/31a0aa0a) + Pillow caption + ffmpeg | `video/VEL-BOWTOTE-FREJA-01-cafe-stills.mp4` |
| 2 | VEL-BOWTOTE-FREJA-02 closer look | one 11s continuous take, 3:4, faceless model behind concrete plinth, floral-interior reveal 4–6s, native Seedance text: persistent bottom caption "A closer look at the Bow Tote" + VELANTRA serif wordmark from ~8s | Seedance 2.0, 1 task | `video/VEL-BOWTOTE-FREJA-02-closer-look.mp4` |
| 3 | VEL-BOWTOTE-FREJA-03 "1 bag 3 looks" | 3×4s locked-camera studio looks (Sloane), all-black outfits so the ivory/denim bag is the only light object, native text "1 bag 3 looks" + VELANTRA every segment | Seedance 2.0, 3 tasks | `video/VEL-BOWTOTE-FREJA-03-1bag3looks.mp4` |

Notes:
- Bow Tote run's native caption PERSISTED full length (unlike the meridian run where it faded at 2s) — same prompt language, nondeterministic; spot-check per run.
- The café stills feature the floral lining as the interior story (phone into floral slip pocket, sunglasses + cardholder in final still) — this bag's lining is the hook, lean on it.
- No music baked in; add trending audio at upload.
