# Video analysis to editing-agent handoff

The analysis agent analyzes rushes, transitions, cuts, pacing and animations,
then builds a source-grounded edit plan for the editing agent. This is the current
hosted workflow. Use the ad-engine tools and the internal `@adengine/timeline`
editor. Legacy local watcher scripts and editor-brief publishing routes do not
implement this handoff.

## Analysis agent

Use **Gemini 3.8 Flash** (`gemini-3.8-flash`) for reference/rush video analysis,
image/keyframe QA and detailed frame review. Older-model overrides are refused;
do not substitute another visual-analysis model.

1. Call `get_edit_plan_contract`. Resolve/watch the reference, and call
   `watch_reference(asset_id, media_role="rushes")` for each raw source clip.
   Poll jobs and read the full manifests. Keep reference observations separate
   from our footage, proposed changes, and product claims.
2. Inspect `analysis.status`, `analysis.issues`, transcript provenance, every
   review window and all five `editorial` categories. Never call a sampled
   preview or a full-video model pass exhaustive frame inspection. Scene-change
   detections are candidates; a sampling window is not a cut. Missing model
   output or unknown categories cannot become an executable handoff.
3. For rapid cuts, short transitions, overlay phases or uncertain timing, call
   `review_video_frames` around the event. It supplies every decoded frame with
   source index and timestamp, including variable frame rates. A window is
   limited to 120 frames. Split larger intervals into consecutive windows, and
   verify the returned frame indices and coverage status. To inspect an entire
   source frame by frame, cover its entire duration without gaps. Images have
   no audio: use the full-video pass/transcript for audio relationships. Compare
   visible frame evidence against the model's findings; claimed index coverage
   alone does not prove perceptual correctness.
4. Build the edit plan from the evidence. The observations describe what exists.
   The plan describes decisions and why they serve the intended ad. Preserve
   exact source trims and distinguish source time from destination timeline time.
   Cite observations on every clip and explain all five categories in
   `analysis_to_edit`, including deliberate absence of effects.
5. Save using `save_edit_plan(plan, reference_ids, frame_review_job_ids)`. Include
   both reference and rush analyses and any completed detailed reviews. Give the
   returned edit-plan asset id to the editing agent. The handoff contains the
   actual plan, source URLs/durations, analysis manifests, frame evidence and QA
   criteria. Keep unverified or unsupported decisions in `unresolved`; the save
   gate refuses to mark these ready. Rewatch a source if its analysis is incomplete.

## Required analysis depth

| Area | What to observe | What the editor must receive |
|---|---|---|
| Rushes | Takes, selects/rejects/alternates, useful action ranges, available handles, continuity, focus/exposure, shake, occlusion, delivery and audio defects | Chosen source asset and in/out, intended use, rejected alternatives and reasons in analysis, continuity constraints and per-clip QA |
| Cuts | Hard/jump/match cuts, action before/after, motivation, boundary confidence, audible J/L relationships | Source trims, timeline edit points, track relationship, rationale and synchronization requirements |
| Transitions | Type, direction, start/end, overlap/handles, sound cue; differentiate a camera whip from an added wipe | Boundary clip, duration and rationale; parameters/effects outside the compiler's supported contract remain unresolved |
| Pacing | Shot-duration pattern, hook rhythm, holds/pauses, acceleration, energy curve, dialogue/music relationship | Ordered durations, explicit speed changes, editorial purpose and timing acceptance checks |
| Animations | Camera vs subject vs baked-in vs editable graphic, target/layer, entry/hold/exit, state changes, text, direction, observed/uncertain easing | Clip-relative keyframes, property/value/easing, rationale and QA; never silently omit an unsupported overlay/graphic |

Use source seconds with exclusive end times. Animation times are relative to the
owning clip. Source duration divided by speed must equal timeline duration.
Never infer unseen takes from a finished reference, turn copied catalog numbers
into measurements, or invent precise easing/BPM from insufficient evidence.

## Editing agent

1. Call `get_edit_plan(asset_id)` immediately before editing. It rechecks source
   ownership and analysis fingerprints; stale evidence requires a new handoff.
2. Review `analysis_to_edit`, all clip rationales, `frame_reviews`, and acceptance
   checks. Report missing source material or unsupported operations as concrete
   blockers. Do not invent a transition, fill a gap, change speed, or substitute
   footage to make the plan compile.
3. Use `assembleFromEditPlan(envelope, options)` from `@adengine/timeline`.
   Supply the current renderer's explicitly supported transition kinds. The
   function dry-runs the batch through the editor reducer before returning it.
   It targets an empty timeline to preserve existing edits. Append the batch to
   the editor event log with the editing agent's author id so it remains undoable.
4. The initial compiler supports video/audio source clips, trims, hard cuts,
   explicit constant speed, transform/opacity keyframes, audio gain/fades and
   declared transitions. Arbitrary motion graphics, text/caption design, speed
   ramps, transition-specific parameters and generated assets need a deliberate
   extension or an explicit unresolved decision. Baked-in graphics stay in their
   source unless removal/recreation is part of the plan. Never equate a typed
   editor operation with renderer support.
5. Run the internal editor's playback/render path and inspect the executed video
   against per-clip `qa_checks` and global `acceptance_checks`. Check every cut,
   transition, motion phase, selected action, caption/audio cue and pacing hold.
   Return timeline identity/version, plan identity, performed operations,
   deviations, rendered asset and QA evidence. A valid plan or timeline document
   is not a verified render. Keep observed findings distinct from human judgment.

## Capability validation

Offline regression checks cover rapid cut retention, complete source durations,
preview isolation, source/timeline bounds, VFR frame timestamps, frame count
limits, incomplete/malformed analysis, evidence links, workspace isolation,
stale analysis, internal-editor compilation, transitions, animation and audio.
The Python and TypeScript tests consume the same synthetic handoff fixture.

Live model quality requires a held-out footage set with human-labeled cuts,
transition types/ranges, rush selects, animation phases and audio cues. Measure
missed/false cuts, boundary error in source frames, transition/animation timing,
select accuracy and editor reconstruction error. Include sub-half-second cuts,
dissolves, same-scene jump cuts, animated captions, continuous takes, silent
clips, speech/music sync and VFR. Do not claim perceptual accuracy or production
readiness from mocked provider responses or synthetic contract tests.
