# MOT-VID-013 — 1.1× voice / sync revision, September 9

User correction: existing narration is too fast, dead spots must be removed, and every B-roll scene must be synchronized properly. This plan supersedes the September 8 timing and preserves its approved visual/editing choices.

1. Start from the original, unsped ElevenLabs take 4. Independently transcribe its actual speech and obtain fresh forced alignment of the exact script; do not infer real timing from the old TTS character timings.
2. Set native CapCut narration segments to exactly 1.10×, with pitch unchanged. Inspect waveform silence together with real word boundaries. Remove leading/trailing empty audio and excess inter-phrase pauses. Preserve a short natural gap and consonant protection at each speech join; do not cut through words or remove script content. Log every deleted source interval.
3. Map every surviving source word through the silence-deletion and 1.1× time transform. Rebuild all 37 narrative beats / 40 picture segments against this new word timeline. Keep the four remedy inserts on their named words. Move ingredient/organ labels, all 95 caption phrases, transitions, offer and CTA to their new cues. Use complete native clip handles; assess any source shorter than its newly required hold instead of leaving black gaps or stale frames.
4. Retain the accepted visual direction: scientific explanation, close-ups of named remedies and pen, four native Horizontal Blur resets, and the final lifestyle payoff. Create separate R2 A/B/C CapCut drafts and preserve the prior versions. Keep only a short intentional offer hold after the final words, not the old arbitrary padded timing.
5. Export from CapCut. Transcribe the actual final mixed export for an independent timing check, compare word/caption and narration/B-roll cues, scan for remaining excessive pauses and missing/duplicated speech, review rendered beat/cut samples, and measure the full mix. Final delivery replaces the review page with revised exports only after QA.

Fresh timing service: https://elevenlabs.io/docs/api-reference/forced-alignment/create . This aligns the supplied text to the supplied audio; it does not generate a new voice.

## Measured timing decisions

Fresh Scribe and forced alignment agree on the full script. Old TTS word-start estimates differed by up to 0.584 seconds in the source. Remove 31 verified quiet intervals totaling 10.34 seconds of source audio, retaining short consonant/breath protection. The native 1.1× narration becomes 95.4 seconds; the picture ends at 95.9 seconds with a 0.5-second deliberate offer hold. All cuts are rebuilt from the mapped actual words. S20 needs 4.067 seconds for the ingredient line; use the complete 4-second source with a native 0.983607× picture slowdown (silent source) to span that line without freezing or cutting away early. Place the end CTA below the caption area and reveal it with the offer so both remain readable through the shorter ending.

Final render correction: actual exported words consistently trail source-mapped cues by approximately two frames. Move picture/text cues two frames later, keeping continuous first/last picture coverage and all audio edits unchanged. Reduce voice and music together by 1.7 dB for true-peak headroom. Verify final audio retains exactly the tested timing through waveform comparison.
