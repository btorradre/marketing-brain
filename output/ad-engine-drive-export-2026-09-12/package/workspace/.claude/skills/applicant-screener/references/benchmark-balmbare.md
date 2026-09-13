# The benchmark: Balmbare

Brooks named Balmbare as the standard an applicant's reel is measured against.
This file is what their ads actually do, measured rather than remembered, so the
scoring anchors in `rubric.md` come from numbers instead of impressions.

**Evidence lives in the vault** at `_engine/swipe-library/video-ads/balmbare-benchmark/`:
`measurements.json` (every cut timestamp for 10 ads), `frames/` (143 extracted
frames from the four highest-signal ads), and `measure.py` to redo the pass on a
new set. Existing copy swipes are in
`_engine/swipe-library/video-ads/references (transcripts)/balmbare_video_ad_transcripts.md`.

Brand context: Balmbare Hair Revive Gummies, GLP-1 hair loss. Runs through
persona pages (Elizabeth Moore, Denise Hughes, Courtney Kim, Emma's Little
Notes). Pulled 2026-08-03 via TrendTrack, 10 ads sorted by longest-running.

---

## Measured pacing

| Ad | Length | Cuts | Avg shot | First cut | Reach |
|---|---|---|---|---|---|
| why-didnt-work | 40.0s | 19 | **2.00s** | 2.23s | 31,726 |
| dht-block | 39.2s | 18 | **2.06s** | 1.47s | 13,609 |
| longest-running-240d | 42.3s | 20 | **2.01s** | 3.03s | 461 |
| top-reach | 41.7s | 12 | **3.21s** | 1.47s | 43,034 |
| chewies | 86.0s | 31 | 2.77s | 3.20s | 3,699 |
| podcast-doctor VSL | 192.1s | 108 | **1.76s** | 2.13s | 21,459 |
| md-hook VSL | 229.7s | 15 | 14.36s | 0.43s | 20,852 |
| nurse-science | 101.7s | 2 | 33.90s | **28.73s** | 987 |

**What the numbers say.** The short-form cluster sits at 39 to 42 seconds with
an average shot of **2.0 to 3.2 seconds**, and the first cut lands by **1.5 to
3.2 seconds**. Even the 192-second VSL holds a 1.76s average across 108 cuts,
which is faster than the 40-second ads. Length does not buy slower cutting.

The clearest negative signal in the set is `nurse-science`: two cuts in 102
seconds, first cut at 28.7 seconds, and the second-lowest reach in the pull. A
static talking head that never cuts does not perform here.

**Anchors this produces:** average shot at or under 3 seconds is the standard.
First cut inside 3 seconds. Any hold longer than about 5 seconds needs to be
earning something specific (a proof shot, a reveal), and a reel full of 8-second
holds is failing the thing this role is actually paid for.

---

## The visual grammar

Read from 143 frames across four ads.

**Every shot is a literal referent of the line on screen.** This is the single
most repeated move and it is the thing Brooks named first.

| Line on screen | What is in frame |
|---|---|
| "Vitamins feed your follicles. That's ALL they do" | Three competitor vitamin bottles on a counter |
| "But GLP-1 hair loss isn't a vitamin deficiency" | Hand pressing shed hair against white shower tile |
| "It's HORMONAL" | Top-down shot of a widening scalp part |
| "Your medication triggers a hormone called DHT" | Animated follicle cross-section with labelled DHT molecules |
| "Saw Palmetto" | Saw palmetto fronds and berries |
| "MONTHS IN THIS" | Top-down scalp shot, same woman |
| "My hair 6 months ago" → "VS NOW" | Two selfie clips of the same woman, before and after |

No decorative b-roll. Nothing is on screen because it looked nice. If the line
names a thing, the frame shows that thing.

**Captions are burned in, always present, one idea per shot.** Four treatments
appear, sometimes two in the same ad:

- black box, white text, centred, one or two lines (the workhorse)
- white box, black text, with a keyword in **red** (drug names: "Zepbound")
- plain white text with a soft drop shadow, no box (narrative beats)
- bold white all-caps in 2 to 4 word chunks, lower third (VO-synced karaoke)

**Captions stack progressively for the reveal.** In `why-didnt-work`, "But GLP-1
hair loss isn't a vitamin deficiency" holds, then a new cut adds "It's HORMONAL"
stacked below it. The turn lands on the cut, not inside a shot.

**Transitions are hard cuts.** No fades, wipes, zooms, or effects anywhere in
the set. What reads as "nice transitions" here is a clean cut landing on the
beat of the read, not a transition library.

**Source mixing is aggressive.** One 40-second ad runs real selfie UGC, phone
footage in a hallway, licensed lifestyle b-roll, an animated medical diagram
(one still carries a "VRecorder" watermark), competitor product shots, and
podcast interview footage. Different women, different rooms, different cameras,
different image quality, cut together without apology. Split screens stack two
creators with the caption spanning the seam.

**Everything is 9:16, phone-native, ungraded.** No cinematic colour, no
letterboxing, no horizontal reposts. This lines up with the standing no-3D-render
law: it has to look like something a person filmed.

---

## How to use this when scoring

The question is not "did the applicant make Balmbare ads." It is whether their
reel shows they could. Concretely:

- Measure their shot lengths the same way, from the `scene_*.jpg` count against
  the duration in `media.json`. A reel averaging 6-second holds is a different
  job from this one.
- Check whether their cuts are motivated by the line or by the music. Cutting on
  a beat with no relationship to what is being said is the common failure.
- Check whether captions exist at all. An unlettered reel is a real gap, since
  every ad here is carried by burned-in text.
- Do not reward cinematic polish. A colour-graded, slow-push, shallow-depth reel
  is further from this benchmark than a scrappy phone-shot one that cuts hard
  and puts the right thing under the right line.
