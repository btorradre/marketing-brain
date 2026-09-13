"""Queue + worker loop against a LocalStore under a temp dir."""
import os
import tempfile

os.environ.setdefault("ADENGINE_DATA_DIR", tempfile.mkdtemp(prefix="adengine-test-"))
os.environ.setdefault("ADENGINE_DEV_WORKSPACE", "ws_test")

import pytest  # noqa: E402

from adengine.core.store import LocalStore  # noqa: E402
from adengine.gen import registry as R  # noqa: E402
from adengine.workers import queue, run  # noqa: E402

WS = "ws_test"


@pytest.fixture
def store(tmp_path):
    return LocalStore(str(tmp_path / "data"))


def test_noop_job_completes_after_one_iteration(store):
    job = queue.enqueue(store, WS, "noop", {"hello": "world"})
    assert job["status"] == R.QUEUED
    done = run.run_once(store)
    assert done is not None and done["id"] == job["id"]
    assert done["status"] == R.COMPLETED
    assert done["output"] == {"echo": {"hello": "world"}}
    assert run.run_once(store) is None  # queue drained


def test_claim_is_fifo_and_moves_to_running(store):
    a = queue.enqueue(store, WS, "noop", {"n": 1})
    b = queue.enqueue(store, WS, "noop", {"n": 2})
    # make ordering unambiguous even if both were created in the same ms
    store.update("job", WS, a["id"], created=1.0)
    store.update("job", WS, b["id"], created=2.0)
    first = queue.claim(store, ["noop"])
    assert first["id"] == a["id"] and first["status"] == R.RUNNING
    second = queue.claim(store, ["noop"])
    assert second["id"] == b["id"]
    assert queue.claim(store, ["noop"]) is None
    # a running job is never re-claimed
    assert R.get_job(store, WS, a["id"])["status"] == R.RUNNING


def test_claim_filters_by_kind(store):
    queue.enqueue(store, WS, "kie_generate", {})
    assert queue.claim(store, ["noop"]) is None
    assert queue.claim(store, ["kie_generate"])["kind"] == "kie_generate"


def test_child_waits_for_parent_and_fails_if_parent_fails(store):
    parent = queue.enqueue(store, WS, "noop", {})
    child = queue.enqueue(store, WS, "noop", {}, parent_id=parent["id"])
    store.update("job", WS, parent["id"], created=1.0)
    store.update("job", WS, child["id"], created=2.0)
    p = queue.claim(store)
    assert p["id"] == parent["id"]
    assert queue.claim(store) is None  # child blocked while parent running
    queue.complete(store, p, {"ok": True})
    c = queue.claim(store)
    assert c["id"] == child["id"]

    parent2 = queue.enqueue(store, WS, "noop", {})
    child2 = queue.enqueue(store, WS, "noop", {}, parent_id=parent2["id"])
    store.update("job", WS, parent2["id"], created=3.0)
    store.update("job", WS, child2["id"], created=4.0)
    queue.fail(store, queue.claim(store), "boom")
    assert queue.claim(store) is None
    assert R.get_job(store, WS, child2["id"])["status"] == R.FAILED
    assert "parent job" in R.get_job(store, WS, child2["id"])["error"]


def test_unknown_kind_fails_cleanly(store):
    queue.enqueue(store, WS, "does_not_exist", {})
    done = run.run_once(store)
    assert done["status"] == R.FAILED and "no handler" in done["error"]


def test_handler_exception_lands_on_job(store, monkeypatch):
    from adengine.workers import tasks

    def boom(store, job):
        raise RuntimeError("provider exploded")

    monkeypatch.setitem(tasks.HANDLERS, "noop", boom)
    queue.enqueue(store, WS, "noop", {})
    done = run.run_once(store)
    assert done["status"] == R.FAILED and "provider exploded" in done["error"]


def test_complete_records_cost_row(store):
    job = queue.claim(store, None) or queue.enqueue(store, WS, "noop", {})
    job = queue.claim(store) if job["status"] == R.QUEUED else job
    queue.complete(store, job, {"x": 1}, cost={"provider": "kie", "units": 6.0,
                                               "unit_name": "credits", "usd": 0.024})
    summary = R.cost_summary(store, WS)
    assert summary["providers"]["kie"]["units"] == 6.0
    assert summary["total_usd"] == 0.024
