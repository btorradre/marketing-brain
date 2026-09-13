# Production log — VEL-SOFIA-ONEBAG-01

**Run date:** 2026-07-25 · **Total kie spend:** ~2,150 credits

## Pipeline

`GPT Image 2 i2i` (10 keyframes, caramel 1.png as ref) → `Kling 3.0 i2v` (4 b-roll clips)
→ `ElevenLabs /with-timestamps` (2 VO tracks + word alignment) → `ffmpeg` plate assembly.

All runners are idempotent and resumable off `state.json`.

## Still / b-roll split

Per Brooks: images for the majority, images through the first half, b-roll for the rest.

| | Shots | Runtime |
|---|---|---|
| Stills | S01–S05 + S10 (6) | 40.5s |
| B-roll | S06–S09 (4) | 28.7s |

S10 was added mid-run: the original S09 slot came out at 13.56s of VO once the real word
timings landed, which is far past the safe length for a single Kling clip. Splitting it into
S09 (b-roll, conviction beat) + S10 (still, CTA beat) keeps every clip inside the safe band
**and** puts the end card over a calm frame with real headroom for type.

## QA gate results

**Keyframes: 10/10 PASS first attempt.** Checked per frame — flap one continuous sheet with
the panel + 2 tabs cut into it, notches never reaching the top edge, 2 separate handle loops,
2 belt straps crossed in an X, zero metal, bag structured and upright, no contents protruding.
S08 and S10 are the strongest product reads; S04 renders the bag slightly wider/flatter than
the reference but is well within tolerance.

**Clips: 3/4 PASS first attempt. S06 FAILED and was regenerated.**

S06 v1 hit the documented invented-design mutation — by ~40% into the clip the flap had broken
into detached floating leather shapes and the handles had bunched. Cause was the known trigger
stack: bag small in frame + high angle + swinging with her stride. The v1 motion prompt already
said "held still and level" and that was **not** enough on its own.

**Fix that worked (v2, passed):** delete the walk entirely. She stands in place and shifts her
weight; only hair, dress hem and leaf shadows move. Prompt states the bag "hangs completely
frozen and level at her side and stays pixel for pixel identical to the first frame for the
whole clip." Rejected v1 kept at `_production/rejects/S06-v1-FAILED.mp4`.

**Reusable law:** for a Straw Tote i2v beat where the bag is under ~20% of frame, "carry it
still" is not a strong enough instruction — remove the locomotion from the shot and let the
person and the light carry the motion instead. Costs nothing visually.

## Voice

Two full-length single-take reads rendered. `w30` (Woman Over 30) at **68.64s / 198 wpm** is the
primary — it lands within 0.6s of the reference ad's own runtime, which is exactly the brisk
creator-recommendation pace the format needs. `w40` at 72.54s / 187 wpm is the slower alternate.
Both have word-level alignment JSON; the EDL and the SRT are both derived from it, so swapping
voice re-derives every cut boundary automatically.

## Clip retiming

Clips were generated slightly off their final slots. The plate applies:
S06 87%, S07 108%, S08 97%, S09 90%. Every one of these is a near-static shot by design, so the
retime is invisible. S07 was the only clip generated long.

## Gotchas hit

- `int(s)` inside the SRT timestamp formatter truncated every caption to whole seconds. Fixed.
- First caption grouping merged across sentence boundaries ("...effortless. Mine is the Sofia...")
  and capitalised mid-sentence words. Rewritten to break on sentences first, then commas.
- ffmpeg filter paths break on the `M:D:YY` colons in the concept folder name — every ffmpeg call
  runs with `cwd=` the work dir and relative filenames only.
