# Ad quality rubrics

These are **provisional quality gates, version 0.1.0**, not empirically proven
predictors of conversion. Do not call a generated score optimal or calibrated.

Use `copy.json` for scripts, `storyboard.json` for shot plans and `edit.json` only
for actual rendered video. Each criterion has anchored integer scores 0–4,
weights totaling 100, a minimum score of 3 and required evidence types. Current
overall thresholds are 90 for copy/boards and 95 for renders. Any critical
failure or criterion below its minimum blocks a pass regardless of the average.
Absent evidence produces `needs_evidence`; an explicit defect produces `revise`
and remains visible even when some evidence is also missing.

## Review contract

`adengine.quality.load_rubric(name)` returns a fresh rubric dictionary.
`evaluate_review(rubric, review, artifact_hash=..., artifact_kind=...,
creator_id=...)` validates and scores one review. Pass trusted artifact SHA256,
kind (`script`, `storyboard`, `render`) and creator identity from the run store.
These values must not come from the reviewing agent's own response. A review is:

```json
{
  "rubric_id": "copy",
  "rubric_version": "0.1.0",
  "artifact_hash": "64-character lowercase SHA256 of the reviewed artifact",
  "reviewer_id": "independent-reviewer-session-id",
  "criteria": {
    "claim_truth": {
      "score": 3,
      "critical_failure": false,
      "feedback": "Claim is supported; make the qualification easier to speak.",
      "evidence": [
        {"kind": "artifact", "path": "script.md", "locator": "line 8", "observation": "The capacity claim is qualified."},
        {"kind": "product_truth", "path": "product.json", "locator": "capacity", "observation": "The specification supports the qualified claim."}
      ]
    }
  }
}
```

Supply every criterion, not only the example above. Evidence kinds and score
anchors live in the rubric JSON. Return `status`, `score`, `blockers`,
`missing_evidence` and per-criterion results. A complete numerical score can still
have missing evidence; only `status=pass` clears the quality gate.

The evaluator is a deterministic review validator, not a vision model or source
authenticator. The runtime must authenticate reviewer identity, pin evidence
paths and hashes in its packet, check that cited evidence was available, and
have reviewers inspect the actual media. Different strings alone do not prove
independent agents. A changed artifact requires fresh reviews, even if a prior
version passed. Pin rubric content alongside its version for each run.

Customer-language evidence establishes phrasing and motivations. It does not
establish product truth. Reference-ad dialogue establishes structure, not the
customer's voice, verified testimonials, or the advertised product's capabilities.
If customer voice data is unavailable, request it and leave that criterion
unverified. Never invent a customer quote to satisfy a required citation.

## Bounded revision and calibration

Review copy before production, boards before generation and the export before
delivery. Independent reviewers receive raw artifacts and source context, not
the author's desired grade. Repair the identified line/shot/frame range, preserve
approved unaffected work, hash the revision and rerun the relevant gate. Stop at
the run's configured revision/budget cap or unresolved missing inputs. A quality
pass does not supply generation spending permission or replace board approval.

For calibration, retain several concepts, independently scored candidate
versions, review evidence, reviewer identities, human preference judgments,
revision diffs and any later outcome data. Keep draft, board and render outcomes
separate. Ad performance requires its own measured outcomes and cannot be
inferred from craft scores. Compare inter-reviewer disagreement and human
preferences before adjusting anchors or thresholds; log the reason and increment
the rubric version. Reserve unseen concepts to check that a revised rubric is
useful beyond the examples used to tune it. Do not silently relax a critical gate
to make a failing example pass.
