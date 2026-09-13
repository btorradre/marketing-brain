# Frame and audio audit

Use when inspecting an actual ad reference. The goal is an evidence-backed edit map, with an honest account of coverage.

## Establish the source clock

Retain the original media, source/share URL, retrieval date and file hash. Probe image dimensions, display orientation, duration, frame count, exact frame-rate rational and audio streams. Distinguish image duration from container/audio tail. Avoid changing the source before analysis.

Use zero-based decoded source frame indices and half-open intervals `[in, out)`. A hard cut at frame N means N−1 is the last outgoing frame and N is the first incoming frame. A known constant frame rate permits `seconds = frame / fps`; retain the exact rational. For variable-rate footage, use decoded presentation timestamps and durations rather than multiplying by an average rate. State the source clock and the separate target timeline rate. Do not confuse decimal seconds with frame timecode or silently substitute 30000/1001 for 29.97 exactly.

## Inspect in complementary passes

1. **Watch and listen across the entire ad** where playback/audio tools permit. Learn its overall coverage, narrative and energy. Log inaccessible streams. A transcript cannot establish sound design or vocal delivery.
2. **Build dense chronological evidence** to locate shot/layout/action changes. Combine visual review and detection; inspect both the main image and smaller overlay regions. Automated scoring locates candidates, not confirmed edits.
3. **Verify each mapped boundary on consecutive source frames.** Expand the surrounding span until the change is identified. Record false positives such as subject motion, particles, exposure shifts or captions; scan for missed small/brief inserts and same-setup jump cuts.
4. **Inspect complete transition spans frame by frame**, including before/after handles. Find first affected frame, any overlap/black/white or picture handoff, and first fully settled frame. The detector's largest difference may occur after the effect starts. Check picture, presenter, captions and graphics separately.
5. **Audit motion inside shots.** Compare early/middle/late framing, then inspect the relevant consecutive frames to distinguish continuous movement, a stepped crop, a freeze or a state change. A transition may straddle two clips while a zoom may occur entirely inside one.
6. **Align words and listen around audio events.** Keep raw ASR and corrected/aligned text separate; check clipped final words, hallucinated tails, proper names and apparent pauses against audio. Review picture/audio handoffs, voice continuity, music accents and SFX in context.

When the user explicitly asks for every individual frame, dense sampling is an indexing aid: continue through all source frames in chronological batches and maintain a coverage ledger. Inspect at sufficient resolution to see the detail under discussion. A strip of illegibly small frames does not verify captions or a subtle effect. If exhaustive coverage cannot be completed, report the remaining spans; do not relabel the partial review as complete. Do not log a frame as visually inspected merely because it was extracted, decoded, scored or submitted to an automatic video summary.

Maintain coverage separately for normal-speed playback, audible listening, sampled images, individually inspected consecutive ranges, boundary verification and full-resolution detail checks. Existing reference evidence can cover only what its original ledger establishes.

## Event map

Store a readable breakdown plus a structured CSV/JSON when the ad's complexity warrants it. Use stable IDs. A useful record contains:

| Field | Meaning |
|---|---|
| event_id / track | Base picture, overlay, caption, framing/effect, audio; concurrent events can share a time |
| source_in_frame / source_out_frame_exclusive | Exact source image span; add PTS when needed |
| event_type | Hard cut, overlap, overlay entrance/exit, crop change, continuous motion, caption, audio event, etc. |
| picture_before / picture_after | Observed subject, framing and visible action, plus continuing layers |
| effect_start / handoff / settled | Relevant exact frames or explicitly approximate ranges; null if inapplicable |
| narration_cue | Exact verified words or explicitly marked ASR/paraphrase; speech timing confidence |
| treatment | Observed direction, framing, mask, color, opacity or sound behavior; unknown parameters remain unknown |
| why_here | Inferred story/attention purpose tied to the cue and neighboring events |
| evidence | Source file, frame strip/detail path and audio interval where applicable |
| status | Observed/measured, inferred, unresolved; include competing plausible explanations when material |

Track shot intervals separately from other editorial events. Report shot-count and duration statistics only for a defined population. Overlay exits and caption updates do not create new base-picture shots. A decoded video may also contain same-source crops; those are edits, not new B-roll assets.

## Outputs and limits

Save provenance, media metadata, event map, representative full-resolution details, boundary/transition evidence and coverage status beside the analysis. Summarize pacing by story section with examples: fast recognition list, slower explanation, presenter hold, product routine, close. Do not let a global average erase these differences.

If audio cannot be auditioned, label music, SFX, J/L cuts, voice timbre and mix unverified. If only the finished video exists, exact font family, easing curve, original lens, capture rate, zoom percentage and effect preset may remain unidentified. A useful description of visible behavior is better than a false setting.
