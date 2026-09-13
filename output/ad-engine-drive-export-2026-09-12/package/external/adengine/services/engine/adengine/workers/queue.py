"""Store-backed job queue.

    job = enqueue(store, ws, kind, input, parent_id=None)
    job = claim(store, kinds)          # queued -> running, oldest first
    complete(store, job, output, cost) # -> completed (+ cost row)
    fail(store, job, error)            # -> failed

Dependencies: a job with parent_id is only claimable once its parent is
completed; if the parent failed the child is failed too ("parent failed").

Atomicity: for LocalStore the claim runs under the store's process-wide lock
(one worker process per data dir is the supported dev topology). The Postgres
store claims with
    UPDATE job SET status='running', updated=now()
     WHERE id = (SELECT id FROM job WHERE status='queued' AND kind = ANY($1)
                 ORDER BY created LIMIT 1 FOR UPDATE SKIP LOCKED)
    RETURNING *;
so many workers can share one queue without double-claiming.
"""
from __future__ import annotations

import contextlib
import os
import time

from adengine.core.errors import NotFound
from adengine.core.store import LocalStore, Store
from adengine.gen import registry as R


def enqueue(store: Store, ws: str, kind: str, input: dict | None = None,
            parent_id: str | None = None, provider: str | None = None) -> dict:
    return R.create_job(store, ws, kind, provider=provider, input=input or {},
                        parent_id=parent_id, status=R.QUEUED)


def list_workspaces(store: Store) -> list[str]:
    lister = getattr(store, "list_workspaces", None)
    if callable(lister):
        return list(lister())
    if isinstance(store, LocalStore):
        if not os.path.isdir(store.root):
            return []
        return sorted(d for d in os.listdir(store.root)
                      if os.path.isdir(os.path.join(store.root, d)) and not d.startswith(".")
                      and d != "tmp")
    return []


def _lock(store: Store):
    lock = getattr(store, "_lock", None)
    return lock if lock is not None else contextlib.nullcontext()


def _parent_ready(store: Store, job: dict) -> bool | None:
    """True = parent done, False = parent failed, None = still pending."""
    pid = job.get("parent_id")
    if not pid:
        return True
    try:
        parent = store.get("job", job["workspace_id"], pid)
    except NotFound:
        return False
    if parent.get("status") == R.COMPLETED:
        return True
    if parent.get("status") in (R.FAILED, "cancelled"):
        return False
    return None


def claim(store: Store, kinds: list[str] | tuple[str, ...] | None = None,
          workspace_ids: list[str] | None = None) -> dict | None:
    """Move the oldest claimable queued job to running and return it."""
    claimer = getattr(store, "claim_job", None)
    if callable(claimer):  # PostgresStore: SKIP LOCKED
        return claimer(kinds, workspace_ids=workspace_ids)
    with _lock(store):
        candidates: list[dict] = []
        for ws in (workspace_ids if workspace_ids is not None else list_workspaces(store)):
            candidates.extend(store.find("job", ws, status=R.QUEUED))
        candidates.sort(key=lambda j: j.get("created", 0))
        for job in candidates:
            if kinds and job.get("kind") not in kinds:
                continue
            ready = _parent_ready(store, job)
            if ready is None:
                continue
            if ready is False:
                fail(store, job, f"parent job {job.get('parent_id')} failed")
                continue
            return R.update_job(store, job["workspace_id"], job["id"], status=R.RUNNING,
                                started=time.time())
    return None


def complete(store: Store, job: dict, output: dict | None = None,
             cost: dict | None = None) -> dict:
    """cost: {provider, units, unit_name, usd, note?} -> a cost row linked to the job."""
    ws = job["workspace_id"]
    if cost:
        R.record_cost(store, ws, job["id"], cost.get("provider") or job.get("provider") or "unknown",
                      cost.get("units"), cost.get("unit_name", "units"), cost.get("usd"),
                      note=cost.get("note"))
    total = R.cost_summary(store, ws, job_id=job["id"])["total_usd"]
    return R.update_job(store, ws, job["id"], status=R.COMPLETED, output=output or {},
                        cost=total, error=None, finished=time.time())


def fail(store: Store, job: dict, error: str, output: dict | None = None) -> dict:
    return R.update_job(store, job["workspace_id"], job["id"], status=R.FAILED,
                        error=str(error)[:2000], output=output, finished=time.time())
