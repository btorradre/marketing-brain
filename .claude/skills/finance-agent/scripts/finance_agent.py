#!/usr/bin/env python3
"""
finance-agent orchestrator — one command per stage, or `close` for the whole monthly loop.

  python3 finance_agent.py status                 # what's in the inbox / table / queue / ledger
  python3 finance_agent.py ingest                 # inbox + new Apple Card PDFs → transactions.json
  python3 finance_agent.py supplier               # parse supplier statements
  python3 finance_agent.py categorize [--llm]     # rules (+ Claude) → ledger + review queue
  python3 finance_agent.py review                 # show the queue
  python3 finance_agent.py build --year 2026 [--from-cache]
  python3 finance_agent.py pull [--since 2026-01-01]                  # Wells Fargo + Amex via SimpleFIN → inbox
  python3 finance_agent.py close --year 2026 [--pull] [--llm] [--from-cache]   # (pull →) ingest → supplier → categorize → build
"""
import os, sys, subprocess
from fin_common import *  # noqa


def run(script, *a):
    r = subprocess.run([sys.executable, os.path.join(HERE, script), *a], cwd=HERE)
    if r.returncode != 0: sys.exit(r.returncode)


def status():
    inbox = [f for f in os.listdir(INBOX) if os.path.isfile(os.path.join(INBOX, f)) and not f.startswith(".")] if os.path.isdir(INBOX) else []
    print(f"Inbox ({INBOX}): {len(inbox)} file(s)" + (": " + ", ".join(inbox) if inbox else ""))
    run("ingest.py", "--status")
    q = load_json(QUEUE, {"items": []})["items"]
    print(f"Review queue: {len(q)} items")
    led = load_json(LEDGER, {"entries": []})["entries"]
    months = sorted({e["month"] for e in led})
    bank = sorted({e["month"] for e in led if (e.get("source") or "").startswith(BANK_SRC)})
    print(f"Ledger: {len(led)} entries, months {months[0] if months else '-'}..{months[-1] if months else '-'} · bank-complete months: {', '.join(bank) or 'none'}")
    if os.path.exists(BILLS):
        b = load_json(BILLS, {"bills": []})["bills"]; print(f"Supplier bills: {len(b)} parsed, ${sum(x['grand_total'] for x in b):,.0f}")


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__); return
    cmd, rest = sys.argv[1], sys.argv[2:]
    if cmd == "status": status()
    elif cmd == "pull": run("fetch_simplefin.py", "pull", *rest)
    elif cmd == "ingest": run("ingest.py", *rest)
    elif cmd == "supplier": run("supplier_bills.py", *rest)
    elif cmd == "categorize": run("categorize.py", *rest)
    elif cmd == "review": run("review.py", *(rest or ["--show"]))
    elif cmd == "build": run("build_pl.py", *rest)
    elif cmd == "close":
        llm = "--llm" in rest; do_pull = "--pull" in rest; rest = [a for a in rest if a not in ("--llm", "--pull")]
        if do_pull: run("fetch_simplefin.py", "pull", "--months", "2")
        run("ingest.py"); run("supplier_bills.py"); run("categorize.py", *(["--llm"] if llm else []))
        run("build_pl.py", *rest)
    else:
        print(f"unknown command {cmd}\n{__doc__}"); sys.exit(2)


if __name__ == "__main__":
    main()
