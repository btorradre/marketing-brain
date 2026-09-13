#!/usr/bin/env python3
"""
score_ledger.py, the arithmetic and the paper trail.

The agent doing the screening judges each applicant's actual submitted work.
This script adds up, applies the gates and caps, decides the verdict, and
writes the two files that matter: a report a human can audit and an action
queue the platform-execution step carries out.

Keeping the math here and out of the model is deliberate. A screen that drops
people has to produce the same number twice for the same evidence.

Commands
  init   --run DIR --brand <key in BRANDS> [--job-url URL] [--job-title T]
  score  --run DIR --file scores_in.json        (one object or a list)
  report --run DIR

Files
  <run>/config.json    brand, filter word, thresholds
  <run>/scores.json    accumulated, keyed by applicant id
  <run>/REPORT.md      ranked, with the reason for every drop
  <run>/actions.json   {"pin": [...], "archive": [...], "review": [...]}
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

PIN_THRESHOLD = 5.0  # strictly greater than 5.0 gets pinned

# Weighted toward the three things that matter most for this role: the right
# visual under the right line, fast pacing, and a reel that resembles the
# named benchmark advertiser (see references/benchmark-balmbare.md).
# Scripts and briefs are supplied, so writing ability is not scored on its own.
WEIGHTS = {
    "visual_line_match":     2.5,  # does the frame show what the line is saying
    "pacing":                2.0,  # shot length, first cut, dead air
    "benchmark_resemblance": 1.5,  # reads like benchmark-class DR, not a brand film
    "category_fit":          1.5,  # required work category for this posting
    "caption_craft":         1.0,  # burned-in text, one idea per shot, legible
    "ai_tooling":            1.0,  # hands-on depth in the named stack
    "throughput":            0.5,  # can they hold the daily count
}

GATES = {
    "filter_word":    "missing the filter word",
    "loom_link":      "no Loom video",
    "portfolio_link": "no portfolio or reel link",
    "timezone_hours": "did not state timezone and weekly hours",
}

# Caps clamp the total no matter how the components scored.
CAPS = {
    "no_ai_generated_work": (4.0, "portfolio shows no AI-generated work"),
    "wrong_category":       (5.0, "no work in the required category"),
    "not_direct_response":  (5.0, "portfolio is brand/event/vlog work, not direct response"),
    "unverifiable_media":   (5.0, "no playable work could be opened"),
    "too_slow":             (4.0, "average shot length over 5s across the reel"),
    "no_burned_captions":   (5.0, "no burned-in captions anywhere in the reel"),
}

# Worked example brands from the reference postings this rubric was built
# against (see references/rubric.md). Add a new key here for each new
# posting screened, with its own filter word and required category.
BRANDS = {
    "velantra": {"filter_word": "SAFFRON", "category": "fashion / apparel"},
    "motilli":  {"filter_word": "JUNIPER", "category": "supplement / health / wellness DR"},
}


def load(p: Path, default):
    return json.loads(p.read_text()) if p.exists() else default


def cmd_init(args):
    run_dir = Path(args.run).expanduser().resolve()
    run_dir.mkdir(parents=True, exist_ok=True)
    brand = args.brand.lower()
    if brand not in BRANDS:
        sys.exit(f"unknown brand {brand!r}, one of {list(BRANDS)}")
    cfg = {
        "brand": brand,
        **BRANDS[brand],
        "job_url": args.job_url,
        "job_title": args.job_title,
        "pin_threshold": PIN_THRESHOLD,
        "weights": WEIGHTS,
        "created": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    (run_dir / "config.json").write_text(json.dumps(cfg, indent=2))
    print(json.dumps(cfg, indent=2))
    print(f"\nrun dir ready: {run_dir}")
    print(f"filter word for this pile: {cfg['filter_word']}")


def evaluate(entry: dict) -> dict:
    """Gates, then weighted sum, then caps. Returns the entry mutated in place."""
    gates = entry.get("gates") or {}
    failed = [msg for key, msg in GATES.items() if gates.get(key) is not True]

    raw = entry.get("scores") or {}
    bad = [k for k in raw if k not in WEIGHTS]
    if bad:
        raise ValueError(f"{entry.get('id')}: unknown score keys {bad}")
    over = [f"{k}={raw[k]} > {WEIGHTS[k]}" for k in raw if float(raw[k]) > WEIGHTS[k]]
    if over:
        raise ValueError(f"{entry.get('id')}: score above its weight cap: {over}")

    subtotal = round(sum(float(raw.get(k, 0)) for k in WEIGHTS), 2)

    applied, noted = [], []
    total = subtotal
    for cap_key in entry.get("caps") or []:
        if cap_key not in CAPS:
            raise ValueError(f"{entry.get('id')}: unknown cap {cap_key!r}")
        ceiling, why = CAPS[cap_key]
        if total > ceiling:
            total = ceiling
            applied.append(why)   # this cap actually did the work
        else:
            noted.append(why)     # true, but the components already scored below it

    if failed:
        verdict, total = "archive", 0.0
    elif "unverifiable_media" in (entry.get("caps") or []) and subtotal > PIN_THRESHOLD:
        # Gates passed and the paper looks strong, but nothing playable came
        # back. That is usually a permissioned Drive link, not a bad applicant.
        # Park it for a human rather than dropping a possible hire.
        verdict = "review"
    else:
        verdict = "pin" if total > PIN_THRESHOLD else "archive"

    entry.update({
        "subtotal": subtotal,
        "total": round(total, 2),
        "gates_failed": failed,
        "caps_applied": applied,
        "caps_noted": noted,
        "verdict": verdict,
        "scored_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    })
    return entry


def cmd_score(args):
    run_dir = Path(args.run).expanduser().resolve()
    incoming = json.loads(Path(args.file).expanduser().read_text())
    if isinstance(incoming, dict):
        incoming = [incoming]
    store = load(run_dir / "scores.json", {})
    for entry in incoming:
        if not entry.get("id"):
            sys.exit("every score object needs an 'id'")
        store[str(entry["id"])] = evaluate(entry)
    (run_dir / "scores.json").write_text(json.dumps(store, indent=2))
    for e in incoming:
        print(f"{e['verdict']:>7}  {e['total']:>5}  {e.get('name') or e['id']}"
              + (f"   [{'; '.join(e['gates_failed'])}]" if e["gates_failed"] else ""))
    print(f"\n{len(store)} scored so far")


def bar(total: float) -> str:
    filled = int(round(total))
    return "#" * filled + "." * (10 - filled)


def cmd_report(args):
    run_dir = Path(args.run).expanduser().resolve()
    cfg = load(run_dir / "config.json", {})
    store = load(run_dir / "scores.json", {})
    if not store:
        sys.exit("nothing scored yet")

    rows = sorted(store.values(), key=lambda e: (-e["total"], e.get("name") or ""))
    pin = [e for e in rows if e["verdict"] == "pin"]
    review = [e for e in rows if e["verdict"] == "review"]
    drop = [e for e in rows if e["verdict"] == "archive"]

    actions = {
        "brand": cfg.get("brand"),
        "job_url": cfg.get("job_url"),
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "pin": [{"id": e["id"], "name": e.get("name"), "total": e["total"]} for e in pin],
        "archive": [{"id": e["id"], "name": e.get("name"), "total": e["total"],
                     "reason": "; ".join(e["gates_failed"]) or "scored at or below 5.0"}
                    for e in drop],
        "review": [{"id": e["id"], "name": e.get("name"), "total": e["total"]} for e in review],
        "executed": False,
    }
    (run_dir / "actions.json").write_text(json.dumps(actions, indent=2))

    L = []
    L.append(f"# Applicant screen, {cfg.get('brand', '?').title()}")
    L.append("")
    L.append(f"**{cfg.get('job_title') or 'AI Video Editor'}** · filter word "
             f"`{cfg.get('filter_word')}` · required category: {cfg.get('category')}")
    L.append(f"Scored {len(rows)} applications. "
             f"**{len(pin)} pin · {len(review)} review · {len(drop)} archive.** "
             f"Pin bar is a total above {PIN_THRESHOLD}.")
    L.append("")
    L.append("Nothing here has been actioned on OnlineJobs yet. `actions.json` is the queue; "
             "it runs only when you say go.")
    L.append("")

    L.append("## Pin")
    L.append("")
    if not pin:
        L.append("_Nobody cleared the bar._")
    for e in pin:
        L.append(f"### {e.get('name') or e['id']}, **{e['total']}/10** `{bar(e['total'])}`")
        L.append("")
        L.append("| " + " | ".join(WEIGHTS) + " |")
        L.append("|" + "---|" * len(WEIGHTS))
        L.append("| " + " | ".join(f"{e['scores'].get(k, 0)}/{WEIGHTS[k]}" for k in WEIGHTS) + " |")
        L.append("")
        for ev in e.get("evidence") or []:
            L.append(f"- {ev}")
        if e.get("caps_applied"):
            L.append(f"- Capped: {'; '.join(e['caps_applied'])}")
        L.append("")

    if review:
        L.append("## Review, gates passed, work could not be opened")
        L.append("")
        L.append("Usually a permissioned Drive folder or a dead link. Worth one email "
                 "before dropping someone who reads as strong on paper.")
        L.append("")
        for e in review:
            L.append(f"- **{e.get('name') or e['id']}**, paper score {e['subtotal']}/10. "
                     + (e.get("evidence") or ["no note"])[0])
        L.append("")

    L.append("## Archive")
    L.append("")
    L.append("| Applicant | Score | Why |")
    L.append("|---|---|---|")
    for e in drop:
        why = ("; ".join(e["gates_failed"])
               or "; ".join(e.get("caps_applied") or [])
               or (e.get("evidence") or ["scored at or below the bar"])[0])
        # Caps that were true but never clamped still describe the applicant,
        # so keep them visible without letting them stand in as the reason.
        extra = e.get("caps_noted") or []
        if extra and not e["gates_failed"]:
            why += f" _(also: {'; '.join(extra)})_"
        L.append(f"| {e.get('name') or e['id']} | {e['total']} | {why} |")
    L.append("")

    gate_counts = {}
    for e in drop:
        for g in e["gates_failed"]:
            gate_counts[g] = gate_counts.get(g, 0) + 1
    if gate_counts:
        L.append("## Where the pile died")
        L.append("")
        for g, n in sorted(gate_counts.items(), key=lambda kv: -kv[1]):
            L.append(f"- **{n}**, {g}")
        L.append("")

    (run_dir / "REPORT.md").write_text("\n".join(L))
    print(f"wrote {run_dir / 'REPORT.md'}")
    print(f"wrote {run_dir / 'actions.json'}")
    print(f"\n{len(pin)} pin · {len(review)} review · {len(drop)} archive "
          f"(of {len(rows)})")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("init")
    p.add_argument("--run", required=True)
    p.add_argument("--brand", required=True)
    p.add_argument("--job-url")
    p.add_argument("--job-title")
    p.set_defaults(fn=cmd_init)

    p = sub.add_parser("score")
    p.add_argument("--run", required=True)
    p.add_argument("--file", required=True)
    p.set_defaults(fn=cmd_score)

    p = sub.add_parser("report")
    p.add_argument("--run", required=True)
    p.set_defaults(fn=cmd_report)

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
