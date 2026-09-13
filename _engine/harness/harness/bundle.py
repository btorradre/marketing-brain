"""Artifact bundle: run.json, evals.json, index.html next to trace.jsonl and report.md."""

from __future__ import annotations

import html
import json
import time
from pathlib import Path

from .models import Run
from .store import RunStore


def run_dir(runs_root: Path, run: Run) -> Path:
    d = runs_root / (run.brand or "x") / run.id
    (d / "artifacts").mkdir(parents=True, exist_ok=True)
    return d


def write_run_json(d: Path, run: Run) -> None:
    (d / "run.json").write_text(run.to_json())


def write_evals(d: Path, store: RunStore, run: Run) -> None:
    (d / "evals.json").write_text(json.dumps(store.evals(run.id), indent=2, default=str))


def _trace_rows(d: Path, limit: int = 400) -> list[dict]:
    p = d / "trace.jsonl"
    if not p.is_file():
        return []
    rows = []
    for line in p.read_text(errors="replace").splitlines()[-limit:]:
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def _summarize(row: dict) -> str:
    kind, p = row.get("kind"), row.get("payload") or {}
    if kind == "AssistantMessage":
        bits = []
        for b in p.get("content") or []:
            t = b.get("_type")
            if t == "TextBlock":
                bits.append(b.get("text", "")[:300])
            elif t == "ToolUseBlock":
                bits.append(f"→ {b.get('name')} {json.dumps(b.get('input'))[:200]}")
        return " | ".join(bits)
    if kind == "UserMessage":
        c = p.get("content")
        if isinstance(c, list):
            outs = []
            for b in c:
                if b.get("_type") == "ToolResultBlock":
                    txt = b.get("content")
                    outs.append(f"← {str(txt)[:200]}")
            return " | ".join(outs)
        return str(c)[:300]
    if kind == "ResultMessage":
        return f"result: {p.get('subtype')} turns={p.get('num_turns')} cost=${p.get('total_cost_usd')}"
    if kind.startswith("hook:"):
        return json.dumps(p)[:300]
    return ""


def write_index(d: Path, run: Run, store: RunStore) -> None:
    report = (d / "report.md").read_text(errors="replace") if (d / "report.md").is_file() else "(no report written)"
    evals = store.evals(run.id)
    rows = _trace_rows(d)
    ev_html = "".join(
        f"<tr><td>{html.escape(str(e['check_name']))}</td><td>{e['kind']}</td>"
        f"<td>{'' if e['score'] is None else e['score']}</td>"
        f"<td>{'' if e['passed'] is None else ('pass' if e['passed'] else 'FAIL')}</td>"
        f"<td>{html.escape(str(e['detail'] or ''))[:300]}</td></tr>" for e in evals)
    tr_html = "".join(
        f"<tr><td>{time.strftime('%H:%M:%S', time.localtime(r.get('ts', 0)))}</td>"
        f"<td>{html.escape(r.get('kind', ''))}</td><td><pre>{html.escape(_summarize(r))}</pre></td></tr>"
        for r in rows if _summarize(r))
    meta = run.to_dict()
    doc = f"""<!doctype html><meta charset="utf-8"><title>{html.escape(run.id)}</title>
<style>body{{font:14px/1.45 -apple-system,system-ui,sans-serif;max-width:1100px;margin:32px auto;padding:0 16px;color:#222}}
pre{{white-space:pre-wrap;margin:0;font-size:12px}}table{{border-collapse:collapse;width:100%}}td,th{{border:1px solid #ddd;padding:6px;vertical-align:top;text-align:left}}
.k{{color:#666}}h2{{margin-top:32px}}</style>
<h1>{html.escape(run.id)}</h1>
<p class="k">{html.escape(run.workflow)} · {html.escape(str(run.brand))} / {html.escape(str(run.product))} · status <b>{html.escape(run.status)}</b>
· turns {run.num_turns} · cost ${run.cost_usd} · stop met: {run.stop_met} {html.escape(run.stop_detail or '')}</p>
<h2>Report</h2><pre>{html.escape(report)}</pre>
<h2>Evals</h2><table><tr><th>check</th><th>kind</th><th>score</th><th>result</th><th>detail</th></tr>{ev_html}</table>
<h2>Run record</h2><pre>{html.escape(json.dumps(meta, indent=2, default=str))}</pre>
<h2>Trace (last {len(rows)} events)</h2><table>{tr_html}</table>
"""
    (d / "index.html").write_text(doc)
