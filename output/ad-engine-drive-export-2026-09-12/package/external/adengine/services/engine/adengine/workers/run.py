"""Worker loop: claim a queued job, dispatch by kind, complete or fail it.

    python -m adengine.workers                 # all kinds, poll every 3s
    python -m adengine.workers --kinds kie_generate,eleven_vo --once
"""
from __future__ import annotations

import argparse
import logging
import signal
import sys
import time
import traceback

from adengine.core.store import Store, get_store
from adengine.workers import queue
from adengine.workers.tasks import HANDLERS, CreditRefire

log = logging.getLogger("adengine.workers")


def run_job(store: Store, job: dict) -> dict:
    handler = HANDLERS.get(job.get("kind"))
    if handler is None:
        return queue.fail(store, job, f"no handler for kind '{job.get('kind')}'")
    try:
        output = handler(store, job)
    except CreditRefire as exc:
        return queue.fail(store, job, str(exc),
                          output={"should_refire": True, "refire_note":
                                  "Credit failure. Automatic top-up fires on a rejected render "
                                  "(not on a quota read), so re-enqueue this job rather than "
                                  "reporting a hard block."})
    except Exception as exc:  # noqa: BLE001 — every failure lands on the job record
        log.error("job %s (%s) failed: %s\n%s", job["id"], job.get("kind"), exc, traceback.format_exc())
        return queue.fail(store, job, f"{type(exc).__name__}: {exc}")
    return queue.complete(store, job, output)


def run_once(store: Store | None = None, kinds: list[str] | None = None) -> dict | None:
    """Claim and run at most one job. Returns the finished job or None if idle."""
    store = store or get_store()
    job = queue.claim(store, kinds)
    if job is None:
        return None
    log.info("running %s %s", job["id"], job.get("kind"))
    return run_job(store, job)


def loop(store: Store | None = None, kinds: list[str] | None = None, poll_s: float = 3.0,
         stop=None) -> None:
    store = store or get_store()
    while not (stop and stop()):
        try:
            if run_once(store, kinds) is None:
                time.sleep(poll_s)
        except KeyboardInterrupt:
            break
        except Exception:  # noqa: BLE001 — a bad claim must not kill the worker
            log.error("worker iteration failed:\n%s", traceback.format_exc())
            time.sleep(poll_s)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m adengine.workers")
    ap.add_argument("--kinds", default="", help="comma-separated job kinds to serve (default all)")
    ap.add_argument("--once", action="store_true", help="run at most one job and exit")
    ap.add_argument("--poll", type=float, default=3.0)
    args = ap.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    kinds = [k.strip() for k in args.kinds.split(",") if k.strip()] or None
    store = get_store()
    if args.once:
        job = run_once(store, kinds)
        print(job["id"] if job else "idle")
        return 0
    stopping = {"v": False}
    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, lambda *_: stopping.__setitem__("v", True))
    log.info("worker up: kinds=%s data_dir via settings", kinds or "all")
    loop(store, kinds, args.poll, stop=lambda: stopping["v"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
