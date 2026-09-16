# Presenter layout, exact voice and timing handoff

Use with the [editing profile](ai-ugc-greenscreen-story-editing-profile.md). These are transferable procedures from W01; numeric starting points are proposals unless explicitly labeled source measurements.

## Layer and layout contract

Keep background, keyed presenter, captions, selective labels/CTA and audio independently editable in Resolve. Do not bake the presenter or captions into each generated background. Generate clean first frames; attach the actual selected images to Cut Room scene cards when storyboarding is requested. A layout proof supplements clean plates.

For a new 9:16 composition, a presenter around 25–35% of picture height is a useful starting trial, not a universal size. Measure the visible silhouette, not transparent canvas dimensions or Resolve's Zoom value. Protect eyes, mouth and informative hand gestures while clearing the product, full-look shoes, grid subjects and destination controls. Keep caption lines readable on a phone and within current delivery safe areas. Derive coordinates from the actual asset dimensions/aspect; the source project's pan/tilt values are not portable presets.

The Eleanor revision deliberately enlarged the guide and tucked her into the lower-left corner. Vivienne moved the guide from left to right at its wider outfit shot, then removed her on the PDP close. Both keep orientation predictable. Record any corner change or hide/show event separately from the background cut, with the exact cue and the object it exposes.

Review the matte around hair, fingers, cuffs and shoulder movement on light, dark and detailed backgrounds. A green source frame is not a finished transparent presenter. Adjust key/spill handling on the actual source; never prescribe one Delta Keyer threshold for every take. Do not erase product details or treat the guide's face with destructive edge smoothing.

## Narration and avatar source of truth

Record exact script version; provider voice identity; model/settings; synthesis speed; selected audio filename/hash; presenter identity/source image; authorized presenter provider; source duration/fps; audio provenance and alignment version. Verify named voices live when generating; an old display name or an age descriptor is insufficient. Preserve all source originals and selection/supersession status.

For a new audio-driven avatar, prefer this order when supported and authorized: exact final narration → conservative silence cleanup → approved continuous WAV → avatar driven by that exact WAV → final alignment → edit. The Vivienne correction followed this order after the first voice choice proved wrong. This is a timing workflow, not permission to clone a third party or to substitute a different provider.

For an existing selected avatar, preserve its exact matching audio. If narration changes materially, regenerate through the authorized route or verify a supported alignment method; replacing the waveform alone does not prove lip sync. A static guide may be an interim composition but is not a completed talking presenter.

Different source and delivery frame rates can preserve real-time playback. Do not reinterpret fps in a way that changes duration or pitch. Verify start, middle, end and every join in the actual export.

## Remove dead air while preserving the performance

1. Detect candidate quiet intervals, then review phonemes, breaths and hand/mouth states around them. Silence thresholds propose candidates; they do not decide the final cut. Do not remove meaningful hesitation, negation, consonant releases or all breathing.
2. Save an ordered source keep/remove map. For a retained source moment `s`, target time is `s` minus the total removed duration before it. If an old cue falls inside a removed interval, explicitly anchor it to the correct surviving word/action; do not blindly clamp every cue.
3. Apply the same source intervals to matched presenter and voice. Re-map background events, captions, emphasis and CTA to the new continuous timeline. A caption spanning a removed gap needs a revised interval or split while preserving the exact words.
4. Inspect visual discontinuities at the joins, even if a background cut hides them. Quiet-gap joins inside one scene are not new B-roll scenes. Use tiny audio smoothing only where needed and verify it does not clip speech.
5. Check intelligibility by actual listening when available, identity and lip sync through the full selected export, exact caption words, no duplicated/dropped syllables, all picture cut cues and last-word/end timing. Record the limits when audio is only model-reviewed.

The Eleanor source removed 27 internal quiet gaps and shortened its ending; its selected narration had already been synthesized at 1.1×. That is a historical setting, not a new speed default. Vivienne used a different silence map. Never run either map on a different performance or speed the voice a second time.

## Finish and close

Muted generated B-roll audio avoids unintended room, speech or musical changes beneath narration. Choose no music or a licensed low bed deliberately; neither is a proof of “native” origin. Prioritize intelligibility, inspect peaks and audition the mix. Historical loudness readings are measurements of those exports, not universal targets.

Show the CTA while it is spoken so the final silent hold can be short without sacrificing comprehension. A provisional 0.2–0.8 seconds after the last word is a starting trial only; extend if reading genuinely needs it. Check a page's actual name, product identity and current offer/shipping terms before using it. Stop scrolling while essential text is read; never invent storefront controls or inherit old sale claims.
