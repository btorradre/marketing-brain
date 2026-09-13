"""Deterministic gates over evidence-citing human/agent judgments.

This module validates review structure and provenance; it does not itself watch
video, authenticate reviewers, verify citations, or infer creative quality.
The caller must supply artifact and identity context from its trusted run store.
"""
from __future__ import annotations

import json
import re
from decimal import Decimal
from typing import Any

from ..core.settings import settings


def load_rubric(name: str) -> dict[str, Any]:
    """Load a fresh, versioned rubric from the deployment's packages directory."""
    if name not in {"copy", "storyboard", "edit", "edit_style"}:
        raise ValueError(f"Unknown rubric: {name}")
    with open(settings.packages_path("rubrics", f"{name}.json"), encoding="utf-8") as f:
        rubric = json.load(f)
    _validate_rubric(rubric)
    return rubric


def _validate_rubric(rubric: dict[str, Any]) -> None:
    maximum = rubric.get("scale", {}).get("max", 4)
    if type(maximum) is not int or maximum <= 0 or rubric.get("scale", {}).get("min", 0) != 0:
        raise ValueError("Rubric requires a positive integer scale with minimum zero")
    criteria = rubric.get("criteria", [])
    if not criteria or len({c["id"] for c in criteria}) != len(criteria):
        raise ValueError("Rubric requires unique criteria")
    if sum(c["weight"] for c in criteria) != 100:
        raise ValueError("Rubric weights must sum to 100")
    for c in criteria:
        if not 0 < c["weight"] <= 100 or not 0 <= c["minimum_score"] <= maximum:
            raise ValueError("Invalid criterion weight or minimum score")
        if not c.get("required_evidence"):
            raise ValueError("Every criterion must require evidence")
    if not 0 <= rubric["pass_threshold"] <= rubric.get("score_max", 100):
        raise ValueError("Invalid pass threshold")


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def evaluate_review(
    rubric: dict[str, Any], review: dict[str, Any], *,
    artifact_hash: str | None = None,
    artifact_kind: str | None = None,
    creator_id: str | None = None,
) -> dict[str, Any]:
    """Score one independent review; no mutation or provider calls.

    Missing trusted context/evidence cannot PASS. Critical failures and criterion
    floors override averages. A changed artifact or rubric invalidates the review.
    Identity equality catches self-review, but independence still requires the
    caller to authenticate reviewer identity rather than trust agent-written IDs.
    """
    _validate_rubric(rubric)
    maximum = rubric.get("scale", {}).get("max", 4)
    score_max = rubric.get("score_max", 100)
    blockers: list[str] = []
    missing: list[str] = []
    results: list[dict[str, Any]] = []
    if not isinstance(review, dict):
        review = {}
        missing.append("Review must be an object")
    if not isinstance(artifact_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", artifact_hash):
        missing.append("Trusted artifact SHA256 is required")
    elif review.get("artifact_hash") != artifact_hash:
        blockers.append("Review artifact hash does not match current artifact")
    if not artifact_kind:
        missing.append("Trusted artifact kind is required")
    elif artifact_kind != rubric["artifact_kind"]:
        missing.append(f"{rubric['id']} review requires a {rubric['artifact_kind']} artifact")
    if review.get("rubric_id") != rubric["id"] or review.get("rubric_version") != rubric["version"]:
        blockers.append("Review rubric ID/version does not match pinned rubric")
    if not _text(creator_id) or not _text(review.get("reviewer_id")):
        missing.append("Creator and independent reviewer identities are required")
    elif creator_id.strip() == review["reviewer_id"].strip():
        blockers.append("Artifact creator cannot act as its independent reviewer")

    submitted = review.get("criteria", {})
    if not isinstance(submitted, dict):
        submitted = {}
        missing.append("Review criteria must be an object keyed by criterion ID")
    unknown = set(submitted) - {c["id"] for c in rubric["criteria"]}
    if unknown:
        blockers.append("Unknown review criteria: " + ", ".join(sorted(unknown)))
    weighted = Decimal(0)
    scored_count = 0
    for criterion in rubric["criteria"]:
        cid = criterion["id"]
        assessment = submitted.get(cid)
        if not isinstance(assessment, dict):
            missing.append(f"{cid}: assessment missing")
            results.append({"id": cid, "score": None, "status": "needs_evidence"})
            continue
        raw_score = assessment.get("score")
        valid_score = (
            isinstance(raw_score, int) and not isinstance(raw_score, bool)
            and 0 <= raw_score <= maximum
        )
        criterion_missing: list[str] = []
        criterion_blockers: list[str] = []
        if not valid_score:
            criterion_missing.append(f"integer score from 0 to {maximum} required")
        else:
            weighted += Decimal(str(criterion["weight"])) * raw_score / maximum * score_max / 100
            scored_count += 1
            if raw_score < criterion["minimum_score"]:
                criterion_blockers.append(f"score below minimum {criterion['minimum_score']}")
        critical = assessment.get("critical_failure")
        if type(critical) is not bool:
            criterion_missing.append("explicit critical_failure boolean required")
        elif critical:
            criterion_blockers.append("critical failure")
        evidence = assessment.get("evidence", [])
        if not isinstance(evidence, list):
            evidence = []
        valid_evidence = [e for e in evidence if isinstance(e, dict) and all(
            _text(e.get(key)) for key in ("kind", "path", "locator", "observation")
        )]
        kinds = {e["kind"] for e in valid_evidence}
        for kind in criterion["required_evidence"]:
            if kind not in kinds:
                criterion_missing.append(f"{kind} evidence with path, locator and observation required")
        if not _text(assessment.get("feedback")):
            criterion_missing.append("actionable feedback or pass rationale required")
        missing.extend(f"{cid}: {m}" for m in criterion_missing)
        blockers.extend(f"{cid}: {b}" for b in criterion_blockers)
        status = "revise" if criterion_blockers else "needs_evidence" if criterion_missing else "pass"
        results.append({"id": cid, "score": raw_score if valid_score else None,
                        "status": status, "feedback": assessment.get("feedback", "")})

    score = float(round(weighted, 2)) if scored_count == len(rubric["criteria"]) else None
    if score is not None and weighted < Decimal(str(rubric["pass_threshold"])):
        blockers.append(f"Score {score:g} is below provisional threshold {rubric['pass_threshold']}")
    return {
        "status": "revise" if blockers else "needs_evidence" if missing else "pass",
        "score": score, "rubric_id": rubric["id"], "rubric_version": rubric["version"],
        "artifact_hash": artifact_hash, "calibration_status": rubric.get("calibration_status", "provisional"),
        "blockers": blockers, "missing_evidence": missing, "criterion_results": results,
    }
