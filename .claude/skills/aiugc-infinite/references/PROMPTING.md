# Prompting References — Index

Production prompting references for the three models in heavy use across this brain. Read the full file when you need depth; cheat-sheet below when you need the lever fast.

| Model | Use for | File |
|---|---|---|
| **GPT Image 2** | Hero ad images, on-image text, before/after splits, branded layouts, anything with typography | [gpt-image-2-prompting.md](gpt-image-2-prompting.md) |
| **Kling 3.0** | Image-to-video for vibe / lifestyle / fashion / talking-head with native audio | [kling-3-prompting.md](kling-3-prompting.md) |
| **Seedance 2.0** | Cut 2 UGC product-action (literal physical verbs) seeded from a last frame | [seedance-2-prompting.md](seedance-2-prompting.md) |

---

## Universal cheat-sheet (all three models)

| Lever | GPT Image 2 | Kling 3.0 | Seedance 2.0 |
|---|---|---|---|
| Prompt length | 250–400 words | ≤2 sentences (i2v) | 60–120 words |
| Prompt focus when seeded | Describe CHANGES only | Describe MOTION only | Describe MOTION + identity lock |
| Negative prompt? | None — phrase as positive constraints | None — phrase positive | None — append explicit lock + negate phrases |
| Sound | n/a | `on`/`off` (native audio, dialogue + SFX) | Native audio always; tag `voiceover`/`ambient` |
| Sweet-spot duration | n/a | 5s | 5–6s |
| Sweet-spot resolution | 1024×1536 (9:16) | 720p | 720p |
| Mode tier | `low` / `medium` / `high` | `std` / `pro` | `fast` / `std` |
| Identity tactic | Re-state PRESERVE every turn | Bind Subject + same wording across clips | "maintain exact appearance from reference image, no drift, no morphing" |
| #1 failure | AI sheen / waxy skin | Face morphs at 10s | Face drifts when camera moves |
| #1 fix | Stack 3-5 "looks real" cues | Cap to 5s + Pro mode | Lock to handheld minimal motion |

## The "looks real" stack (use across all three)

For images and i2v alike, stack 3-5 of these to break AI gloss:
- handheld jitter / slight handheld tilt
- rolling shutter wobble
- eye-focus drift
- background motion blur
- 35mm grain / sensor noise
- visible skin pores / faint freckles
- imperfect framing / cropped at the elbow
- unedited RAW look / shot on iPhone
- mid-blink / mid-word expression
- ordinary background detail (half-empty mug, dishtowel)

## The 4-cue rule (Kling i2v + Seedance UGC Cut 2)

Always append to the motion prompt:
> `subtle handheld jitter, rolling shutter wobble, eye-focus drift, ambient background motion`

Source: confirmed across every credible Kling guide AND aligned with Seedance UGC anchor pattern. Difference between AI render and phone capture.

## Two-cut UGC pipeline (where each model fits)

```
[Optional: GPT Image 2 → product hero / before-after / native-image static ad]
                         |
                         v
[Cut 1] Marketing Studio Video (Higgsfield, mode=ugc) → talking head with native VO
                         |
                         v
[Frame extract] FFmpeg last frame  →  PNG
                         |
                         v
[Cut 2] Seedance 2.0 (i2v, --medias=lastframe.png) → creator-uses-product action
                         |
                         v
[Stitch] FFmpeg hard cut → final ad
```

Kling 3.0 is the substitute for either Cut 1 or Cut 2 if Higgsfield Marketing Studio doesn't fit (e.g., for the rapid-vsl skill where you want lipsynced talking heads from a static avatar).

## Banned vocabulary (all three models)

These don't help and often hurt:
- `cinematic`, `epic`, `dramatic`, `stunning`, `beautiful`, `masterpiece`
- `8k`, `4k`, `ultra-detailed`, `hyperrealistic` (use specific resolution params)
- `trending on artstation`, `award-winning`, `professional` (era-2023 SD tags)
- generic verbs: `moves`, `interacts`, `uses`, `experiences`, `enjoys`
- competitor brand names (rejected as IP)
- vague mood words — replace with concrete visual facts

## When in doubt, this order

1. **Start frame quality matters more than the prompt.** Garbage seed → garbage output. Spend 80% of effort on the seed.
2. **One concrete physical verb beats five abstract ones.** "She unscrews the cap" not "She uses the product."
3. **Stop redescribing what's in the frame.** Describe deltas only.
4. **Ship in `std`/`fast`, regen winners in `pro`/`std`.** Don't pay for tier you don't need until a creative wins.
5. **Pin every lever explicitly:** duration, resolution, AR, mode, sound, genre. The defaults will not match a UGC ad.
