"""State transitions and provenance gates against adversarial review/session inputs."""
import asyncio
from concurrent.futures import ThreadPoolExecutor
import copy
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from adengine.harness import RunStore, start_run, ingest_review, revise_run
from adengine.harness.runtime import reserve_attempt, finish_attempt
from adengine.harness.sdk import run_reviewers, build_options


@pytest.fixture
def packet(tmp_path):
    roles = ("script", "storyboard", "render", "product_truth", "customer_voice", "avatar_brief", "reference", "timeline", "audio")
    for role in roles:
        (tmp_path / f"{role}.txt").write_text(f"Evidence for {role}: observed test content")
    path = tmp_path / "packet.json"
    path.write_text(json.dumps({"creator_id": "author", "stage": "storyboard",
        "artifacts": {key: f"{key}.txt" for key in ("script", "storyboard")},
        "context": {key: f"{key}.txt" for key in roles[3:]}}))
    return path


@pytest.fixture
def store(tmp_path):
    return RunStore(tmp_path / "state")


def review_for(run, kind="copy", score=4):
    current = run["rounds"][-1]
    artifact = current["artifacts"][{"copy": "script", "storyboard": "storyboard", "edit": "render"}[kind]]
    rubric = current["rubrics"][kind]
    def evidence(role):
        item = artifact if role in ("artifact", "render") else current["context"][role]
        return {"kind": role, "path": item["path"], "locator": "line 1", "observation": "Observed test evidence supporting criterion"}
    return {"rubric_id": kind, "rubric_version": rubric["version"], "reviewer_id": f"qc-{kind}",
        "artifact_hash": artifact["sha256"], "packet_hash": current["packet_hash"],
        "criteria": {criterion["id"]: {"score": score, "critical_failure": False,
            "feedback": "Actionable test feedback", "evidence": [evidence(role) for role in criterion["required_evidence"]]}
            for criterion in rubric["criteria"]}}


def ingest(store, run, kind="copy", **kwargs):
    review = review_for(run, kind, **kwargs)
    return ingest_review(store, run["id"], review, reviewer_id=review["reviewer_id"])


def test_persisted_complete_storyboard_is_not_final_delivery(store, packet):
    run = start_run(store, packet)
    run = ingest(store, run)
    assert run["status"] == "awaiting_reviews"
    run = ingest(store, run, "storyboard")
    assert run["status"] == "passed"
    assert not run["final_delivery_ready"]
    assert RunStore(store.root).get_run(run["id"]) == run
    assert len(store.events(run["id"])) == 3


@pytest.mark.parametrize("mutator", [
    lambda r: r.update(artifact_hash="f" * 64),
    lambda r: r.update(packet_hash="f" * 64),
    lambda r: r.update(reviewer_id="author"),
])
def test_reject_stale_or_creator_reviews(store, packet, mutator):
    run = start_run(store, packet)
    review = review_for(run)
    mutator(review)
    with pytest.raises(ValueError):
        ingest_review(store, run["id"], review, reviewer_id="qc-copy")
    assert not store.get_run(run["id"])["rounds"][-1]["reviews"]


def test_cannot_relabel_product_truth_as_customer_voice(store, packet):
    run = start_run(store, packet)
    review = review_for(run)
    for criterion in review["criteria"].values():
        for item in criterion["evidence"]:
            if item["kind"] == "customer_voice":
                item["path"] = run["rounds"][-1]["context"]["product_truth"]["path"]
    with pytest.raises(ValueError, match="source role"):
        ingest_review(store, run["id"], review, reviewer_id="qc-copy")


def test_source_changes_do_not_rewrite_snapshot_but_snapshot_tamper_fails(store, packet):
    run = start_run(store, packet)
    (packet.parent / "script.txt").write_text("Revised in working directory")
    run = ingest(store, run)
    Path(run["rounds"][-1]["artifacts"]["storyboard"]["path"]).write_text("Tampered snapshot")
    with pytest.raises(ValueError, match="missing or changed"):
        ingest(store, run, "storyboard")


def test_missing_criterion_evidence_never_passes(store, packet):
    run = start_run(store, packet)
    review = review_for(run)
    for item in review["criteria"].values():
        item["evidence"] = []
    run = ingest_review(store, run["id"], review, reviewer_id="qc-copy")
    run = ingest(store, run, "storyboard")
    assert run["status"] == "needs_evidence"


def test_revision_rechecks_all_reviews_and_obeys_round_limit(store, packet):
    run = start_run(store, packet, max_rounds=2)
    run = ingest(store, run, score=1)
    run = ingest(store, run, "storyboard")
    assert run["status"] == "needs_revision"
    old_review = review_for(run)
    (packet.parent / "customer_voice.txt").write_text("New customer evidence")
    run = revise_run(store, run["id"], packet)
    assert not run["rounds"][-1]["reviews"]
    with pytest.raises(ValueError, match="packet hash"):
        ingest_review(store, run["id"], old_review, reviewer_id="qc-copy")
    run = ingest(store, run, score=1)
    run = ingest(store, run, "storyboard")
    assert run["status"] == "round_limit"
    with pytest.raises(ValueError):
        revise_run(store, run["id"], packet)


def test_identical_revision_is_rejected_and_valid_retry_works(store, packet):
    run = start_run(store, packet)
    run = ingest(store, run, score=1)
    run = ingest(store, run, "storyboard")
    with pytest.raises(ValueError, match="must change"):
        revise_run(store, run["id"], packet)
    (packet.parent / "script.txt").write_text("Actual correction")
    assert revise_run(store, run["id"], packet)["rounds"][-1]["number"] == 2


def test_budget_claim_is_atomic_and_unknown_cost_remains_charged(store, packet):
    run = start_run(store, packet, max_budget_usd=1)
    def claim(_):
        try:
            return reserve_attempt(store, run["id"], 1)
        except ValueError:
            return None
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(claim, range(2)))
    winners = [item for item in results if item]
    assert len(winners) == 1
    completed = finish_attempt(store, run["id"], winners[0]["attempt"]["id"], error="interrupted")
    assert completed["spent_usd"] == 1
    (packet.parent / "script.txt").write_text("Recovery revision")
    revise_run(store, run["id"], packet)
    with pytest.raises(ValueError, match="budget"):
        reserve_attempt(store, run["id"], 0.1)


def test_duplicate_reviews_and_same_reviewer_across_rubrics_are_rejected(store, packet):
    run = start_run(store, packet)
    run = ingest(store, run)
    with pytest.raises(ValueError):
        ingest(store, run)
    review = review_for(run, "storyboard")
    review["reviewer_id"] = "qc-copy"
    with pytest.raises(ValueError, match="separate"):
        ingest_review(store, run["id"], review, reviewer_id="qc-copy")


def fake_sdk(run, *, error=False, structured=True):
    class Result:
        pass
    async def query(prompt, options):
        kind = "storyboard" if "qc-storyboard" in prompt else "copy"
        yield SimpleNamespace(data={"session_id": f"session-{kind}"})
        result = Result()
        result.is_error = error
        result.total_cost_usd = 0.12
        result.structured_output = review_for(run, kind) if structured else None
        yield result
    return SimpleNamespace(ResultMessage=Result, AgentDefinition=lambda **kw: SimpleNamespace(**kw),
        ClaudeAgentOptions=lambda **kw: SimpleNamespace(**kw), HookMatcher=lambda **kw: SimpleNamespace(**kw), query=query)


def test_sdk_isolated_reviewers_persist_sessions_and_validate_reviews(store, packet):
    run = start_run(store, packet)
    result = asyncio.run(run_reviewers(store, run["id"], model="test-model", sdk=fake_sdk(run)))
    assert result["status"] == "passed"
    assert result["spent_usd"] == pytest.approx(0.24)
    assert result["attempt"] is None
    assert len([event for event in store.events(run["id"]) if event["kind"] == "session_started"]) == 2


@pytest.mark.parametrize("kwargs", [{"error": True}, {"structured": False}])
def test_sdk_text_or_error_cannot_complete(store, packet, kwargs):
    run = start_run(store, packet)
    with pytest.raises(RuntimeError):
        asyncio.run(run_reviewers(store, run["id"], model="test-model", sdk=fake_sdk(run, **kwargs)))
    result = store.get_run(run["id"])
    assert result["status"] == "failed"
    assert result["spent_usd"] == 2
    assert not result["final_delivery_ready"]


def test_sdk_tool_guard_denies_shell_and_unpinned_reads(store, packet):
    run = start_run(store, packet)
    options = build_options(fake_sdk(run), run["rounds"][-1], "copy", "test-model", 1)
    assert set(options.tools) == {"Read"}
    assert options.setting_sources == []
    guard = options.hooks["PreToolUse"][0].hooks[0]
    for tool, args in [("Bash", {"command": "echo fail"}), ("Read", {"file_path": "/etc/passwd"}), ("Agent", {"subagent_type": "unknown"})]:
        result = asyncio.run(guard({"tool_name": tool, "tool_input": args}, None, None))
        assert result["hookSpecificOutput"]["permissionDecision"] == "deny"
    path = run["rounds"][-1]["artifacts"]["script"]["path"]
    assert asyncio.run(guard({"tool_name": "Read", "tool_input": {"file_path": path}}, None, None)) == {}


def test_reserved_context_roles_rejected(store, packet):
    payload = json.loads(packet.read_text())
    payload["context"]["artifact"] = "reference.txt"
    packet.write_text(json.dumps(payload))
    with pytest.raises(ValueError, match="reserved"):
        start_run(store, packet)


def test_sdk_reviews_use_distinct_sessions_and_prompts(store, packet):
    run = start_run(store, packet)
    sdk = fake_sdk(run)
    query = sdk.query
    seen = []
    async def instrumented(prompt, options):
        seen.append((prompt, options))
        async for message in query(prompt, options):
            yield message
    sdk.query = instrumented
    asyncio.run(run_reviewers(store, run["id"], model="test-model", sdk=sdk))
    assert len(seen) == 2
    assert seen[0][1] is not seen[1][1]
    assert "independent copy quality reviewer" in seen[0][1].system_prompt
    assert "independent storyboard quality reviewer" in seen[1][1].system_prompt
    assert all(options.tools == ["Read"] for _, options in seen)


def test_recursive_creator_loop_repins_and_rereviews(store, packet):
    from adengine.harness.sdk import run_loop
    run = start_run(store, packet)
    sdk = fake_sdk(run)
    calls = []
    async def query(prompt, options):
        current = store.get_run(run["id"])
        result = sdk.ResultMessage()
        result.is_error = False
        result.total_cost_usd = 0.1
        calls.append(prompt)
        if "Revise this ad" in prompt:
            result.structured_output = {"artifacts": {"script": "Corrected supported script"}, "summary": "Corrected unsupported claim"}
        else:
            kind = "storyboard" if "qc-storyboard" in prompt else "copy"
            score = 1 if current["rounds"][-1]["number"] == 1 and kind == "copy" else 4
            result.structured_output = review_for(current, kind, score)
        yield result
    sdk.query = query
    final = asyncio.run(run_loop(store, run["id"], model="test-model", sdk=sdk))
    assert final["status"] == "passed"
    assert len(final["rounds"]) == 2
    assert final["rounds"][0]["results"]["copy"]["status"] == "revise"
    assert final["rounds"][1]["results"]["copy"]["status"] == "pass"
    assert len(calls) == 5
    assert final["spent_usd"] == pytest.approx(0.5)
    assert (packet.parent / "script.txt").read_text().startswith("Evidence for script")


def test_loop_does_not_spend_past_total_budget(store, packet):
    from adengine.harness.sdk import run_loop
    run = start_run(store, packet, max_budget_usd=1)
    final = asyncio.run(run_loop(store, run["id"], model="test-model", sdk=fake_sdk(run)))
    assert final["loop_stop_reason"] == "budget_limit"
    assert final["spent_usd"] == 0


def test_text_labeled_as_render_never_authorizes_final_delivery(store, packet):
    payload = json.loads(packet.read_text())
    payload["stage"] = "render"
    payload["artifacts"]["render"] = "render.txt"
    packet.write_text(json.dumps(payload))
    run = start_run(store, packet)
    run = ingest(store, run)
    run = ingest(store, run, "storyboard")
    run = ingest(store, run, "edit")
    assert run["status"] == "needs_evidence"
    assert not run["final_delivery_ready"]


def test_sdk_refuses_uninspectable_media_review_before_spending(store, packet):
    payload = json.loads(packet.read_text())
    payload["stage"] = "render"
    payload["artifacts"]["render"] = "render.txt"
    packet.write_text(json.dumps(payload))
    run = start_run(store, packet)
    with pytest.raises(ValueError, match="cannot watch/listen"):
        asyncio.run(run_reviewers(store, run["id"], model="test-model", sdk=fake_sdk(run)))
    assert store.get_run(run["id"])["reserved_usd"] == 0


def test_sdk_timeout_interrupts_inflight_call_and_reserves_cost(store, packet):
    run = start_run(store, packet)
    sdk = fake_sdk(run)
    async def never_finishes(prompt, options):
        yield SimpleNamespace(data={"session_id": "interrupted-session"})
        await asyncio.sleep(30)
    sdk.query = never_finishes
    with pytest.raises(TimeoutError):
        asyncio.run(run_reviewers(store, run["id"], model="test-model", timeout_seconds=0.01, sdk=sdk))
    latest = store.get_run(run["id"])
    assert latest["status"] == "failed"
    assert latest["attempt"] is None
    assert latest["spent_usd"] == 2
    assert any(event["data"].get("session_id") == "interrupted-session" for event in store.events(run["id"]))
