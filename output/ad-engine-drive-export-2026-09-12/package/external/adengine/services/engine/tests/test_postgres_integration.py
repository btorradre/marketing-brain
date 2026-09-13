"""Real PostgreSQL tests in a disposable cluster; never use DATABASE_URL.

Set ADENGINE_TEST_PG_BIN to the directory containing initdb/pg_ctl, or put them
on PATH. Without those binaries these tests skip. No external providers run.
"""
from concurrent.futures import ThreadPoolExecutor
import os
from pathlib import Path
import shutil
import socket
import subprocess
import tempfile
import threading
import uuid

import pytest

from adengine.core.pg_store import PostgresStore
from adengine.workers import queue, run


@pytest.fixture(scope="module")
def database():
    bindir = os.environ.get("ADENGINE_TEST_PG_BIN")
    initdb = str(Path(bindir) / "initdb") if bindir else shutil.which("initdb")
    pgctl = str(Path(bindir) / "pg_ctl") if bindir else shutil.which("pg_ctl")
    if not initdb or not pgctl:
        pytest.skip("set ADENGINE_TEST_PG_BIN to run real Postgres integration tests")
    with tempfile.TemporaryDirectory(prefix="adengine-pg-") as root:
        data = str(Path(root) / "data")
        # Reserve an unused loopback port for this isolated test cluster.
        with socket.socket() as sock:
            sock.bind(("127.0.0.1", 0))
            port = sock.getsockname()[1]
        subprocess.run([initdb, "-D", data, "-U", "postgres", "-A", "trust", "--no-locale", "-E", "UTF8"],
                       check=True, capture_output=True, timeout=60)
        subprocess.run([pgctl, "-D", data, "-l", str(Path(root) / "server.log"),
                        "-o", f"-h 127.0.0.1 -p {port} -k {root}", "-w", "start"],
                       check=True, capture_output=True, timeout=60)
        dsn = f"postgresql://postgres@127.0.0.1:{port}/postgres"
        try:
            store = PostgresStore(dsn)
            migrations = Path(__file__).resolve().parents[3] / "packages/schema/migrations"
            for migration in sorted(migrations.glob("*.sql")):
                store.conn().execute(migration.read_text())
            store.conn().close()
            yield dsn
        finally:
            subprocess.run([pgctl, "-D", data, "-m", "immediate", "-w", "stop"],
                           check=True, capture_output=True, timeout=30)


@pytest.fixture
def pg(database):
    store = PostgresStore(database)
    workspace = str(uuid.uuid4())
    store._run("insert into workspace (id, slug, name) values (%s, %s, %s)",
               [workspace, workspace, "Test"])
    try:
        yield store, workspace
    finally:
        store._run("delete from workspace where id = %s", [workspace])
        store.conn().close()


def test_queue_runs_on_postgres_and_persists_cost(pg):
    store, ws = pg
    job = queue.enqueue(store, ws, "noop", {"hello": "world"})
    assert job["cost"] == 0
    done = run.run_once(store, kinds=["noop"])
    assert done["id"] == job["id"] and done["status"] == "completed"
    assert done["output"] == {"echo": {"hello": "world"}}
    paid = queue.enqueue(store, ws, "noop")
    claimed = queue.claim(store, workspace_ids=[ws])
    completed = queue.complete(store, claimed, cost={"provider": "test", "units": 1,
                                                   "unit_name": "credits", "usd": 0.125})
    assert completed["id"] == paid["id"] and float(completed["cost"]) == 0.125
    assert queue.claim(store, workspace_ids=[ws]) is None


def test_two_workers_cannot_claim_same_job(pg, database):
    store, ws = pg
    jobs = [queue.enqueue(store, ws, "noop") for _ in range(12)]
    barrier = threading.Barrier(2)
    def consume():
        worker = PostgresStore(database)
        claimed = []
        try:
            barrier.wait(timeout=10)
            while job := queue.claim(worker, workspace_ids=[ws]):
                claimed.append(job["id"])
            return claimed
        finally:
            worker.conn().close()
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(consume) for _ in range(2)]
        ids = [id for future in futures for id in future.result(timeout=20)]
    assert len(ids) == len(set(ids)) == len(jobs)
    assert set(ids) == {j["id"] for j in jobs}


def test_locked_job_is_skipped(pg, database):
    store, ws = pg
    first, second = [queue.enqueue(store, ws, "noop") for _ in range(2)]
    locker = PostgresStore(database)
    try:
        with locker.conn().transaction():
            locker._run("select id from job where workspace_id = %s and id = %s for update",
                        [ws, first["id"]])
            store._run("set statement_timeout = '2s'", [])
            assert queue.claim(store, workspace_ids=[ws])["id"] == second["id"]
        assert queue.claim(store, workspace_ids=[ws])["id"] == first["id"]
    finally:
        locker.conn().close()


def test_parent_dependencies_filters_and_empty_workspace_list(pg):
    store, ws = pg
    parent = queue.enqueue(store, ws, "parent")
    child = queue.enqueue(store, ws, "child", parent_id=parent["id"])
    assert queue.claim(store, workspace_ids=[]) is None
    assert queue.claim(store, kinds=["child"], workspace_ids=[ws]) is None
    p = queue.claim(store, kinds=["parent"], workspace_ids=[ws])
    queue.complete(store, p)
    assert queue.claim(store, kinds=["child"], workspace_ids=[ws])["id"] == child["id"]
    failed = queue.enqueue(store, ws, "parent")
    dependent = queue.enqueue(store, ws, "child", parent_id=failed["id"])
    queue.fail(store, failed, "test failure")
    assert queue.claim(store, kinds=["child"], workspace_ids=[ws]) is None
    assert store.get("job", ws, dependent["id"])["status"] == "failed"


def test_parent_from_another_workspace_cannot_release_child(pg):
    store, ws = pg
    other = str(uuid.uuid4())
    store._run("insert into workspace (id, slug, name) values (%s, %s, %s)", [other, other, "Other"])
    try:
        parent = queue.enqueue(store, other, "noop")
        queue.complete(store, parent)
        child = queue.enqueue(store, ws, "noop", parent_id=parent["id"])
        assert queue.claim(store, workspace_ids=[ws]) is None
        assert store.get("job", ws, child["id"])["status"] == "failed"
    finally:
        store._run("delete from workspace where id = %s", [other])


def test_board_approval_and_job_version_roundtrip_on_postgres(pg, monkeypatch):
    from adengine.core import store as store_module
    from adengine.core.auth import AuthContext, _ctx, set_auth_context
    from adengine.core.errors import GateRefused
    from adengine.dr import boards
    from adengine.gen import server
    from adengine.gen.approval import require_job_board
    store, ws = pg
    monkeypatch.setattr(store_module, "_store", store)
    monkeypatch.setattr(server, "_store", lambda: store)
    token = set_auth_context(AuthContext(ws, "human", "owner"))
    try:
        store.create("brand", ws, "brand", slug="acme", name="Acme")
        asset = store.create("asset", ws, "asset", kind="image", mime="image/png", storage_key="test.png")
        spec = {"title": "Review", "timelines": [{"role": "ours", "beats": [
            {"frame": asset["id"], "script": "Original claim"}]}]}
        boards.push_board("acme", spec)
        assert not boards.approval_status(store, ws, "review")["approved"]
        boards.approve_card("review", "l0-b0-frame", "approved")
        out = server.generate_video("motion", first_frame_asset_id=asset["id"], board_slug="review")
        job = store.get("job", ws, out["job_id"])
        assert require_job_board(store, job, [asset["id"]])["approved"]
        spec["timelines"][0]["beats"][0]["script"] = "Revised claim"
        boards.push_board("acme", spec)
        assert not boards.approval_status(store, ws, "review")["approved"]
        with pytest.raises(GateRefused):
            require_job_board(store, job, [asset["id"]])
    finally:
        _ctx.reset(token)
