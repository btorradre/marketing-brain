"""Exercise the complete board -> approval -> queue -> worker boundary, without providers."""
import copy

import pytest

from adengine.core import store as store_module
from adengine.core.auth import AuthContext, _ctx, set_auth_context
from adengine.core.errors import Forbidden, GateRefused
from adengine.core.store import LocalStore
from adengine.dr import boards, server as dr
from adengine.gen import server as gen
from adengine.engines import credentials, kie
from adengine.workers import tasks


WS = "ws_approval"


@pytest.fixture
def setup(tmp_path, monkeypatch):
    store = LocalStore(str(tmp_path))
    monkeypatch.setattr(store_module, "_store", store)
    monkeypatch.setattr(gen, "_store", lambda: store)
    token = set_auth_context(AuthContext(WS, "human", "owner"))
    store.create("brand", WS, "brand", slug="acme", name="Acme")
    assets = [store.create("asset", WS, "asset", kind="image")["id"] for _ in range(3)]
    spec = {"title": "Review", "timelines": [
        {"role": "reference", "beats": [{"frame": assets[2]}]},
        {"role": "ours", "beats": [{"frame": assets[0], "script": "Original line"},
                                     {"frame": assets[1], "script": "Second line"}]}]}
    boards.push_board("acme", spec)
    for i in range(2):
        boards.approve_card("review", f"l1-b{i}-frame", "approved")
    yield store, spec, assets
    _ctx.reset(token)


def test_missing_beat_and_script_change_reopen_approval(setup):
    store, spec, _ = setup
    assert boards.approval_status(store, WS, "review")["approved"]
    changed = copy.deepcopy(spec)
    changed["timelines"][1]["beats"][0]["script"] = "Changed claim"
    boards.push_board("acme", changed)
    status = boards.approval_status(store, WS, "review")
    assert not status["approved"] and status["approved_count"] == 1
    assert status["pending"][0]["stale"]
    changed["timelines"][1]["beats"][0] = {"visual": "Awaiting a new keyframe"}
    boards.push_board("acme", changed)
    status = boards.approval_status(store, WS, "review")
    assert not status["approved"] and status["missing"][0]["beat"] == 0


def test_legacy_and_deleted_asset_approvals_fail_closed(setup):
    store, _, assets = setup
    approval = store.find("approval", WS)[0]
    store.update("approval", WS, approval["id"], fingerprint=None, asset_id=None)
    assert not boards.approval_status(store, WS, "review")["approved"]
    for i in range(2):
        boards.approve_card("review", f"l1-b{i}-frame", "approved")
    store.delete("asset", WS, assets[0])
    assert not boards.approval_status(store, WS, "review")["approved"]


def test_reference_lane_cannot_authorize_animation(setup):
    store, _, assets = setup
    with pytest.raises(GateRefused):
        gen.generate_video("motion", first_frame_asset_id=assets[2], board_slug="review")
    assert store.find("job", WS) == []


@pytest.mark.parametrize("call", [
    lambda: gen.generate_video("motion"),
    lambda: gen.generate_image("motion", model=kie.DEFAULT_VIDEO_MODEL),
    lambda: gen.heygen_generate("asset_audio", "avatar"),
])
def test_ungated_video_routes_refuse_before_enqueue(setup, call):
    store, _, _ = setup
    with pytest.raises(GateRefused):
        call()
    assert store.find("job", WS) == []


def test_worker_rechecks_rejection_and_version_before_spend(setup, monkeypatch):
    store, spec, assets = setup
    def no_provider(*args, **kwargs):
        pytest.fail("provider credentials must not be accessed for a stale job")
    monkeypatch.setattr(tasks, "get_key", no_provider)
    out = gen.generate_video("motion", first_frame_asset_id=assets[0], board_slug="review")
    job = store.get("job", WS, out["job_id"])
    boards.approve_card("review", "l1-b0-frame", "rejected")
    with pytest.raises(GateRefused):
        tasks.kie_generate(store, job)
    boards.approve_card("review", "l1-b0-frame", "approved")
    boards.push_board("acme", spec)  # approvals survive identical content, queued version does not
    assert boards.approval_status(store, WS, "review")["approved"]
    with pytest.raises(GateRefused, match="changed after"):
        tasks.kie_generate(store, job)


def test_worker_rejects_directly_injected_video_job(setup, monkeypatch):
    store, _, _ = setup
    monkeypatch.setattr(tasks, "get_key", lambda *a: pytest.fail("no provider access"))
    for purpose in ("image", "video", "animation"):
        with pytest.raises(GateRefused):
            tasks.kie_generate(store, {"workspace_id": WS, "input": {
                "model": kie.DEFAULT_VIDEO_MODEL, "purpose": purpose, "input": {}}})
    with pytest.raises(GateRefused):
        tasks.heygen_avatar(store, {"workspace_id": WS, "input": {}})


def test_approved_video_reaches_provider_and_records_output(setup, monkeypatch):
    from adengine.workers import run, queue
    store, _, assets = setup
    monkeypatch.setattr(tasks, "get_key", lambda *a: "test-key")
    monkeypatch.setattr(tasks, "_resolve_asset_refs", lambda *a: {"prompt": "motion"})
    calls = []
    monkeypatch.setattr(kie, "create_task", lambda *a: calls.append(a) or "provider_task")
    monkeypatch.setattr(kie, "wait_for_task", lambda *a: {
        "state": "success", "creditsConsumed": 6})
    monkeypatch.setattr(kie, "result_urls", lambda *a: ["https://example.com/result.mp4"])
    def download(url, destination):
        from pathlib import Path
        Path(destination).write_bytes(b"test video")
    monkeypatch.setattr(kie, "download", download)
    out = gen.generate_video("motion", first_frame_asset_id=assets[0], board_slug="review")
    job = queue.claim(store, workspace_ids=[WS])
    result = run.run_job(store, job)
    assert result["id"] == out["job_id"] and result["status"] == "completed"
    assert len(calls) == 1 and result["external_task_id"] == "provider_task"
    assert len(result["output"]["asset_ids"]) == 1
    assert result["cost"] == kie.credits_to_usd(6)


def test_rejection_during_upload_prevents_provider_submission(setup, monkeypatch):
    store, _, assets = setup
    monkeypatch.setattr(tasks, "get_key", lambda *a: "test-key")
    def upload(*args):
        boards.approve_card("review", "l1-b0-frame", "rejected")
        return {"prompt": "motion"}
    monkeypatch.setattr(tasks, "_resolve_asset_refs", upload)
    monkeypatch.setattr(kie, "create_task", lambda *a: pytest.fail("approval was revoked"))
    out = gen.generate_video("motion", first_frame_asset_id=assets[0], board_slug="review")
    with pytest.raises(GateRefused):
        tasks.kie_generate(store, store.get("job", WS, out["job_id"]))


@pytest.mark.parametrize("name,args", [
    ("resolve_reference", ("https://example.com/a.mp4",)),
    ("watch_reference", ("asset_x",)),
    ("analyze_video", ("asset_x", "review")),
    ("generate_anchors", ({}, "product")),
    ("generate_keyframes", ({},)),
    ("animate_scenes", ({}, {}, "review")),
    ("generate_image", ("prompt",)),
    ("generate_video", ("prompt",)),
    ("generate_vo", ("hello", "voice")),
    ("clone_voice", ("name", [])),
    ("heygen_generate", ("asset_x", "avatar")),
    ("upload_asset", ("https://example.com/a.png",)),
])
def test_viewer_cannot_call_generation_mutations(setup, name, args):
    store, _, _ = setup
    token = set_auth_context(AuthContext(WS, "viewer", "viewer"))
    try:
        with pytest.raises(Forbidden):
            getattr(gen, name)(*args)
        assert gen.list_jobs() == []
    finally:
        _ctx.reset(token)
    assert store.find("job", WS) == []


def test_viewer_cannot_mutate_dr_or_credentials(setup):
    _, spec, _ = setup
    token = set_auth_context(AuthContext(WS, "viewer", "viewer"))
    try:
        for result in (
            dr.push_board("acme", spec),
            dr.save_artifact("acme", "brief", "text", name="test"),
            dr.push_concept("acme", "product", "concept", "angle", "thesis"),
            dr.ingest_reference("https://example.com/ad.mp4"),
        ):
            assert result["error"] == "Forbidden"
        with pytest.raises(Forbidden):
            credentials.save_key("kie", "test-only")
        assert dr.get_board("acme", "review")["title"] == "Review"
    finally:
        _ctx.reset(token)


def test_another_workspace_cannot_use_board(setup):
    _, _, assets = setup
    token = set_auth_context(AuthContext("ws_other", "other", "owner"))
    try:
        with pytest.raises(GateRefused):
            gen.generate_video("motion", first_frame_asset_id=assets[0], board_slug="review")
    finally:
        _ctx.reset(token)
