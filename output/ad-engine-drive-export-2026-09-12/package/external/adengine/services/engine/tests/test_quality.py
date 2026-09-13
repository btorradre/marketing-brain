"""Quality gates fail closed on missing evidence, stale context and severe defects."""
from copy import deepcopy
import hashlib

import pytest

from adengine.quality import evaluate_review, load_rubric


def packet(name="copy", score=4):
    rubric = load_rubric(name)
    digest = hashlib.sha256(b"reviewed artifact").hexdigest()
    review = {
        "rubric_id": rubric["id"], "rubric_version": rubric["version"],
        "artifact_hash": digest, "reviewer_id": "reviewer-session-2",
        "criteria": {
            c["id"]: {
                "score": score, "critical_failure": False,
                "feedback": "The referenced evidence supports this score.",
                "evidence": [{"kind": k, "path": f"fixtures/{k}.txt",
                              "locator": "line 4", "observation": "Observed support for this criterion."}
                             for k in c["required_evidence"]],
            } for c in rubric["criteria"]
        },
    }
    context = {"artifact_hash": digest, "artifact_kind": rubric["artifact_kind"],
               "creator_id": "creator-session-1"}
    return rubric, review, context


@pytest.mark.parametrize("name", ["copy", "storyboard", "edit"])
def test_evidenced_independent_review_passes_each_stage(name):
    rubric, review, context = packet(name)
    result = evaluate_review(rubric, review, **context)
    assert result["status"] == "pass"
    assert result["score"] == 100
    assert result["calibration_status"] == "provisional"


def test_weighted_threshold_exact_boundary():
    rubric, review, context = packet()
    review["criteria"]["claim_truth"]["score"] = 3
    review["criteria"]["customer_voice"]["score"] = 3
    result = evaluate_review(rubric, review, **context)
    assert result["score"] == 90 and result["status"] == "pass"
    review["criteria"]["cta_offer"]["score"] = 3
    result = evaluate_review(rubric, review, **context)
    assert result["score"] == 87.5 and result["status"] == "revise"


def test_critical_failure_cannot_be_averaged_out():
    rubric, review, context = packet()
    review["criteria"]["claim_truth"]["critical_failure"] = True
    result = evaluate_review(rubric, review, **context)
    assert result["score"] == 100
    assert result["status"] == "revise"
    assert any("critical failure" in b for b in result["blockers"])


def test_minimum_criterion_score_cannot_be_averaged_out():
    rubric, review, context = packet()
    review["criteria"]["cta_offer"]["score"] = 2
    result = evaluate_review(rubric, review, **context)
    assert result["score"] == 95 and result["status"] == "revise"


def test_missing_voice_evidence_is_not_an_acceptable_guess():
    rubric, review, context = packet()
    review["criteria"]["customer_voice"]["evidence"] = [
        e for e in review["criteria"]["customer_voice"]["evidence"] if e["kind"] != "customer_voice"
    ]
    result = evaluate_review(rubric, review, **context)
    assert result["status"] == "needs_evidence"
    assert any("customer_voice evidence" in m for m in result["missing_evidence"])


@pytest.mark.parametrize("key", ["path", "locator", "observation"])
def test_evidence_requires_source_location_and_observation(key):
    rubric, review, context = packet()
    review["criteria"]["claim_truth"]["evidence"][0][key] = " "
    assert evaluate_review(rubric, review, **context)["status"] == "needs_evidence"


def test_storyboard_is_not_proof_of_final_edit():
    rubric, review, context = packet("edit")
    context["artifact_kind"] = "storyboard"
    assert evaluate_review(rubric, review, **context)["status"] == "needs_evidence"


def test_stale_artifact_and_rubric_are_rejected():
    rubric, review, context = packet()
    context["artifact_hash"] = hashlib.sha256(b"revised artifact").hexdigest()
    assert evaluate_review(rubric, review, **context)["status"] == "revise"
    context["artifact_hash"] = review["artifact_hash"]
    review["rubric_version"] = "0.0.1"
    assert evaluate_review(rubric, review, **context)["status"] == "revise"


def test_self_review_cannot_clear_gate():
    rubric, review, context = packet()
    review["reviewer_id"] = context["creator_id"]
    assert evaluate_review(rubric, review, **context)["status"] == "revise"


def test_untrusted_context_cannot_clear_gate():
    rubric, review, _ = packet()
    assert evaluate_review(rubric, review)["status"] == "needs_evidence"


@pytest.mark.parametrize("bad_score", [True, False, -1, 5, 3.5, "4", None, float("nan")])
def test_invalid_scores_cannot_silently_enter_average(bad_score):
    rubric, review, context = packet()
    review["criteria"]["claim_truth"]["score"] = bad_score
    result = evaluate_review(rubric, review, **context)
    assert result["status"] == "needs_evidence" and result["score"] is None


def test_critical_assessment_cannot_be_omitted():
    rubric, review, context = packet()
    del review["criteria"]["claim_truth"]["critical_failure"]
    assert evaluate_review(rubric, review, **context)["status"] == "needs_evidence"


def test_missing_criterion_and_non_object_review_do_not_crash_or_pass():
    rubric, review, context = packet()
    del review["criteria"]["claim_truth"]
    result = evaluate_review(rubric, review, **context)
    assert result["status"] == "needs_evidence" and result["score"] is None
    assert evaluate_review(rubric, [], **context)["status"] != "pass"


def test_reviews_and_loaded_rubrics_are_not_mutated():
    rubric, review, context = packet()
    before = deepcopy((rubric, review))
    evaluate_review(rubric, review, **context)
    assert (rubric, review) == before
    rubric["criteria"][0]["minimum_score"] = 0
    assert load_rubric("copy")["criteria"][0]["minimum_score"] == 3


def test_rubric_name_cannot_escape_packages_directory():
    with pytest.raises(ValueError):
        load_rubric("../laws/global")
