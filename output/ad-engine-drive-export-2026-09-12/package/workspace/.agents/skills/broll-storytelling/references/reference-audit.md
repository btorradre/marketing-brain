# Reference audit protocol

The purpose is to learn which image performs which job at which spoken cue. Automated watching, ASR and scene detection help locate evidence; none is a complete manual frame audit.

Record the concept's visual treatment as well as its story: animated, live action, photographic, presenter-led or mixed; specific 2D/3D/render/illustration style; recurring character/product design; palette/materials/light; camera and action language; full-frame/inset choices; and precisely when/why it changes medium. Then compare this observed treatment with the target brief. A frame audit should help choose and produce matching B-roll, not just yield a list of timestamps.

## Acquire and identify

Save the original source without alteration, public share URL, resolved media URL, retrieval date, file hash and probe metadata. Recover existing files first. Record video frame count, actual timebase/FPS, image duration and container/audio tail separately. For variable frame rate, use decoded presentation timestamps rather than pretending `frame/fps` is exact.

## Review in layers

1. Review the whole ad in chronological context. Transcribe narration if needed. State separately whether audio was actually listened to.
2. Decode/score every frame where practical. Make dense chronological contact sheets, ordinarily around half-second spacing, with readable captions and source indexes. This is an overview, not proof of every frame.
3. Identify full-frame cuts, presenter pickups, inset on/off/replacements, layouts, graphic overlays and within-shot state changes separately. Scan inset regions more densely: a small sliding image may not register in a full-frame threshold.
4. Inspect consecutive source frames around every proposed boundary. Reject caption updates, exposure variation, fluid/particle motion and camera movement falsely flagged as cuts. Inspect the entire transition span, including settling frames, when a dissolve, flash, zoom/blur or slide appears.
5. Watch the action within each scene at enough temporal density to determine what happens. Check for sub-second inserts and gaps; don't rely only on first frames. If user explicitly requires every frame individually, inspect all frames in manageable source-indexed ranges and maintain a coverage ledger. Otherwise report the exact dense review and boundary coverage without calling it exhaustive.
6. Align each image event to the exact source words where verified, otherwise an explicitly approximate ASR overlap and paraphrased cue. Correct clear drift and hallucinated tails. Distinguish source captions from words actually spoken.
7. Record source reuse and similar compositions across the whole ad. Caption differences and file hashes of finished composites cannot prove that underlying clips are different.

For a requested frame-by-frame review, step through the original in ordered frame ranges, record reviewed ranges in a coverage ledger, and inspect the whole transition/action span. Native-frame extraction and short consecutive-frame sheets are useful when a player lacks frame stepping. A dense sampling pass remains interim evidence and must be labeled as such; decoding every frame is not equivalent to viewing every frame. If full requested coverage cannot be completed, name the unreviewed ranges and resulting limits rather than declaring the audit exhaustive.

## Keep three evidence levels separate

- **Measured/observed:** time/frame boundary, visible person/object/action, caption treatment, placement, movement/transition actually seen, sound actually heard.
- **Inferred function:** recognition, explanation, authority cue, escalation, relief, objection or click direction; why the juxtaposition likely serves the story.
- **Proposed transfer:** what to do in the new concept given its own script, audience, evidence and user constraints.

Explain the inferred purpose of each meaningful reference scene, not just its visual category: why the action illustrates this line, what it adds for the viewer and how the entry/exit connects the argument. Cite the observed action and cue supporting that interpretation. When transferring the lesson, write a separate explanation for the target scene; the competitor's use alone is not a reason to choose it.

Do not infer TikTok origin, camera device, AI model, real patient status, credential, product efficacy or conversion causality from a finished image.

## Save useful evidence

Under `edit/reference-analysis/` for a concept, or an explicitly named research folder for a skill study, save:

- Source/provenance/probe.
- Timestamped transcript and caveats.
- Shot/event map with frame/time range, narration cue, actual action/framing, visual family and placement, motion, transitions, story role and inferred purpose.
- Chronological evidence sheets, consecutive-frame cut/transition evidence and review coverage ledger.
- Summary of structure, emotional arc, image-to-narration relationships, pacing, visual variety and what should not transfer.

A source map is not a new storyboard. If the work proceeds to a proposed storyboard, follow Cut Room delivery rules and attach the selected first asset set.

## Audio and timing honesty

Document narration continuity, delivery, music/SFX, mix and pacing only to the level actually assessed. ASR gives approximate words/timing; it does not establish background music or a particular voice treatment. Silence in a transcript is not silence in the source. Final editing requires the actual selected narration's alignment, not the competitor's timing.
