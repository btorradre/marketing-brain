"""harness CLI: run · queue · work · list · show · workflows · laws"""

from __future__ import annotations

import argparse
import json
import sys
import time

from . import laws, settings
from .models import Run
from .store import RunStore
from .workflows import get as get_workflow, registry


def _parse_kv(items: list[str] | None) -> dict:
    out = {}
    for it in items or []:
        if "=" not in it:
            raise SystemExit(f"expected key=value, got {it!r}")
        k, v = it.split("=", 1)
        if v.lower() in ("true", "false"):
            v = v.lower() == "true"
        else:
            try:
                v = float(v) if "." in v else int(v)
            except ValueError:
                pass
        out[k] = v
    return out


def _make_run(args) -> Run:
    wf = get_workflow(args.workflow)
    inputs = _parse_kv(args.input)
    for k in ("ref", "concept", "board", "script", "n"):
        v = getattr(args, k, None)
        if v is not None:
            inputs[k] = v
    missing = wf.validate_inputs(inputs)
    if missing:
        raise SystemExit("missing inputs:\n  " + "\n  ".join(missing))
    flags = dict(wf.policy.get("flags") or {})
    flags.update(_parse_kv(args.flag))
    budget = dict(wf.policy.get("budget") or {})
    budget.update(_parse_kv(args.budget))
    stop = wf.policy.get("stop") or {}
    return Run.create(workflow=wf.name, brand=args.brand, product=args.product,
                      inputs=inputs, flags=flags,
                      policy={"allowed_tools": wf.policy.get("allowed_tools"),
                              "disallowed_tools": wf.policy.get("disallowed_tools"),
                              "flag_tools": wf.policy.get("flag_tools")},
                      budget=budget, stop=stop.get("tool") or stop.get("file"),
                      parent_run=args.parent, created_by=args.by)


def cmd_run(args, store: RunStore):
    from .runner import execute
    run = _make_run(args)
    store.save(run)
    print(f"run {run.id} created")
    if args.queue:
        return
    run = execute(store, run)
    _print_run(run)
    sys.exit(0 if run.status in ("done", "blocked_on_human") else 1)


def cmd_work(args, store: RunStore):
    from .runner import execute
    n = 0
    while True:
        run = store.next_queued()
        if not run:
            if args.once or n:
                break
            time.sleep(args.poll)
            continue
        print(f"working {run.id}")
        execute(store, run)
        n += 1
        if args.once:
            break
    print(f"{n} run(s) executed")


def _print_run(run: Run):
    d = settings.RUNS_DIR / (run.brand or "x") / run.id
    print(f"{run.id}\n  {run.workflow} · {run.brand}/{run.product} · {run.status}"
          f"\n  turns={run.num_turns} cost=${run.cost_usd} stop_met={run.stop_met}"
          f"\n  {d / 'index.html'}")
    if run.error:
        print(f"  error: {run.error}")


def cmd_list(args, store: RunStore):
    for r in store.list(status=args.status, brand=args.brand, limit=args.limit):
        age = time.strftime("%m-%d %H:%M", time.localtime(r.created_at))
        print(f"{age}  {r.status:16} {r.id:48} {r.workflow:18} ${r.cost_usd or 0:.2f}")


def cmd_show(args, store: RunStore):
    run = store.get(args.run_id)
    if not run:
        raise SystemExit("no such run")
    _print_run(run)
    print("\nevals:")
    for e in store.evals(run.id):
        p = "" if e["passed"] is None else ("pass" if e["passed"] else "FAIL")
        print(f"  {e['check_name']:22} {p:5} {e['score'] if e['score'] is not None else '':>6}  {e['detail']}")
    if args.json:
        print(run.to_json())


def cmd_workflows(args, store: RunStore):
    for name, wf in registry().items():
        print(f"{name:20} {wf.description}")
        if args.verbose:
            print("   " + json.dumps(wf.policy, indent=None)[:600])


def cmd_laws(args, store: RunStore):
    print(json.dumps(laws.status(), indent=2))
    if args.check:
        print(json.dumps(laws.lawgate(args.check, args.brand), indent=2))


def main(argv=None):
    settings.ensure_dirs()
    p = argparse.ArgumentParser(prog="harness")
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("run", help="create a run and execute it now (or --queue)")
    r.add_argument("workflow")
    r.add_argument("--brand"); r.add_argument("--product")
    r.add_argument("--ref"); r.add_argument("--concept"); r.add_argument("--board")
    r.add_argument("--script"); r.add_argument("-n", type=int)
    r.add_argument("--input", "-i", action="append", help="key=value")
    r.add_argument("--flag", "-f", action="append", help="generate=true etc")
    r.add_argument("--budget", action="append", help="max_turns=80 max_budget_usd=10")
    r.add_argument("--parent"); r.add_argument("--by", default="brooks")
    r.add_argument("--queue", action="store_true", help="enqueue only")
    r.set_defaults(fn=cmd_run)

    w = sub.add_parser("work", help="drain the queue")
    w.add_argument("--once", action="store_true"); w.add_argument("--poll", type=float, default=30)
    w.set_defaults(fn=cmd_work)

    ls = sub.add_parser("list"); ls.add_argument("--status"); ls.add_argument("--brand")
    ls.add_argument("--limit", type=int, default=30); ls.set_defaults(fn=cmd_list)
    sub.add_parser("queue").set_defaults(fn=lambda a, s: cmd_list(argparse.Namespace(status="queued", brand=None, limit=100), s))

    sh = sub.add_parser("show"); sh.add_argument("run_id"); sh.add_argument("--json", action="store_true")
    sh.set_defaults(fn=cmd_show)

    wf = sub.add_parser("workflows"); wf.add_argument("-v", "--verbose", action="store_true")
    wf.set_defaults(fn=cmd_workflows)

    lw = sub.add_parser("laws"); lw.add_argument("--check"); lw.add_argument("--brand")
    lw.set_defaults(fn=cmd_laws)

    args = p.parse_args(argv)
    store = RunStore(settings.DB_PATH)
    args.fn(args, store)


if __name__ == "__main__":
    main()
