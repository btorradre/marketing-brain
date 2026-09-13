---
name: ad-quality-control
description: Independently review ad scripts, storyboards, and rendered edits with versioned copy, customer-voice, product-truth, B-roll, and frame-accuracy rubrics; return evidence-bound feedback for bounded revision.
---

Use the repository's [rubric contract](../../rubrics/README.md). Load only the
rubric for the artifact being reviewed: [copy](../../rubrics/copy.json),
[storyboard](../../rubrics/storyboard.json), or [edit](../../rubrics/edit.json).
The thresholds are provisional until calibrated against human judgments.

Work as an independent reviewer with the artifact, pinned source packet, product
truth, customer language, target avatar and brief. Keep the author's proposed
grade out of the review context. If asked to review your own output, use an
independent reviewer; self-scoring can be drafting feedback but cannot clear QC.
Review identities and artifact hashes come from the orchestrator's run record.

Inspect each criterion and return the contract's JSON assessment for every one:
score 0–4, explicit critical-failure decision, source path, precise locator,
observed evidence and actionable revision or pass rationale. Use actual lines,
shot IDs, timecodes or frame numbers. Missing or inaccessible evidence is
`needs_evidence`, never an assumed pass. Do not fabricate citations. Customer
phrasing and reference scripts cannot substantiate product features, prices or
first-person ownership claims. Avatar fit follows the supplied research and
brief; do not introduce universal demographic or casting requirements.

For copy, read the complete script aloud or perform a spoken read-through; assess
natural rhythm as well as documented customer language and objections. Trace
product claims separately to product truth. For boards, map every line to a shot
and reconcile shot counts, generated scenes and existing assets.

For editing, inspect and listen to the actual final render. A storyboard or
timeline plan cannot establish rendered quality. Compare every B-roll interval
to the spoken claim, verify product identity and demonstrations, and inspect both
sides of every cut at native FPS against the intended in/out points. Use the
brief's cut tolerance, defaulting to one frame. Flag wrong products, misleading
demonstrations and materially incorrect cuts as critical failures even when the
rest of the edit is strong. Inspect captions against actual speech, not only the
script. Cite render frames and audio intervals for visual/audio findings.

Return feedback to the creator; do not modify artifacts during the independent
review. After revision, inspect the new hash and rerun affected gates. Preserve
approved work outside the requested correction. Respect the run's revision and
spend limits; unresolved evidence or the iteration cap stops the loop with a
concrete reason. Never relax the rubric solely to finish a run. A passing QC
review does not replace human approval or authorize provider spending.
