"""CLI entry point for offline and model-backed evidence review."""
import argparse
import asyncio
import json
import os
from pathlib import Path

from .runtime import RunStore, start_run, ingest_review, revise_run, finish_attempt


def main(argv=None):
    parser = argparse.ArgumentParser(description="Evidence-bound ad quality review sessions")
    parser.add_argument("--state", default=os.environ.get("ADENGINE_HARNESS_STATE", ".adengine-harness"))
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init")
    start = sub.add_parser("start")
    start.add_argument("packet")
    start.add_argument("--max-rounds", type=int, default=3)
    start.add_argument("--max-budget-usd", type=float, default=10)
    review = sub.add_parser("review")
    review.add_argument("run_id")
    review.add_argument("review")
    review.add_argument("--round", type=int)
    review.add_argument("--reviewer", required=True)
    revise = sub.add_parser("revise")
    revise.add_argument("run_id")
    revise.add_argument("packet")
    for name in ("status", "events", "recover"):
        sub.add_parser(name).add_argument("run_id")
    run = sub.add_parser("run")
    run.add_argument("run_id")
    run.add_argument("--model")
    run.add_argument("--budget-usd", type=float, default=2)
    run.add_argument("--timeout-seconds", type=float, default=300)
    loop = sub.add_parser("loop")
    loop.add_argument("run_id")
    loop.add_argument("--model")
    loop.add_argument("--review-budget-usd", type=float, default=2)
    loop.add_argument("--revision-budget-usd", type=float, default=1)
    loop.add_argument("--timeout-seconds", type=float, default=300)
    args = parser.parse_args(argv)
    store = RunStore(args.state)
    try:
        if args.command == "init":
            result = {"state": str(store.root)}
        elif args.command == "start":
            result = start_run(store, args.packet, max_rounds=args.max_rounds, max_budget_usd=args.max_budget_usd)
        elif args.command == "review":
            result = ingest_review(store, args.run_id, json.loads(Path(args.review).read_text()), reviewer_id=args.reviewer, round_number=args.round)
        elif args.command == "revise":
            result = revise_run(store, args.run_id, args.packet)
        elif args.command == "status":
            result = store.get_run(args.run_id)
        elif args.command == "events":
            result = store.events(args.run_id)
        elif args.command == "recover":
            current = store.get_run(args.run_id)
            if not current["attempt"]:
                raise ValueError("No interrupted attempt to recover")
            result = finish_attempt(store, args.run_id, current["attempt"]["id"], error="Operator recovered interrupted session; full reservation charged")
        elif args.command == "loop":
            from .sdk import run_loop
            result = asyncio.run(run_loop(store, args.run_id, model=args.model, review_budget_usd=args.review_budget_usd, revision_budget_usd=args.revision_budget_usd, timeout_seconds=args.timeout_seconds))
        else:
            from .sdk import run_reviewers
            result = asyncio.run(run_reviewers(store, args.run_id, model=args.model, budget_usd=args.budget_usd, timeout_seconds=args.timeout_seconds))
    except (ValueError, RuntimeError, OSError, TimeoutError) as exc:
        print(json.dumps({"error": str(exc)}))
        return 2
    print(json.dumps(result, indent=2))
    return 0
