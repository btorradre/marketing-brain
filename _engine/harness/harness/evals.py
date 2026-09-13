"""Per-run evals. H0 ships the deterministic checks; judge checks land in H2."""

from __future__ import annotations

import json
from pathlib import Path

from . import laws
from .models import Run
from .store import RunStore


def _saved_artifact_texts(run_dir: Path) -> list[tuple[str, str]]:
    """Text handed to dr_save_artifact / dr_push_brief_board during the run, from the trace."""
    out = []
    p = run_dir / "trace.jsonl"
    if not p.is_file():
        return out
    for line in p.read_text(errors="replace").splitlines():
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        if rec.get("kind") != "AssistantMessage":
            continue
        for b in (rec.get("payload") or {}).get("content") or []:
            if not isinstance(b, dict):
                continue
            is_tool_use = b.get("_type") == "ToolUseBlock" or (
                b.get("_type") is None and "name" in b and "input" in b)
            if not is_tool_use:
                continue
            name, inp = b.get("name", ""), b.get("input") or {}
            if name.endswith("dr_save_artifact") and isinstance(inp.get("content"), str):
                out.append((f"{name}:{inp.get('artifact')}", inp["content"]))
            elif name.endswith("dr_push_brief_board"):
                out.append((f"{name}:{inp.get('slug') or 'board'}", json.dumps(inp.get("spec"), ensure_ascii=False)))
    return out


COPY_KINDS = {"brief", "script", "hook", "hooks", "advertorial", "listicle", "winner",
              "ugc-brief", "email", "pdp", "statics"}


def _scope_for(label: str) -> str:
    """Customer-facing artifacts get copy rules; boards get everything; research
    artifacts (angle bank, adaptation plan, voc) get only the everywhere rules."""
    kind = label.split(":", 1)[-1].lower()
    if label.endswith("dr_push_brief_board") or "push_brief_board" in label:
        return "all"
    if kind in COPY_KINDS:
        return "copy"
    return "research"


def run_evals(store: RunStore, run: Run, run_dir: Path) -> None:
    # 1. lawgate over every artifact the run saved
    texts = _saved_artifact_texts(run_dir)
    total_b = total_w = 0
    for label, text in texts:
        res = laws.lawgate(text, run.brand, scope=_scope_for(label))
        total_b += len(res["blockers"]); total_w += len(res["warnings"])
    store.eval(run.id, "lawgate_artifacts", "deterministic",
               score=float(len(texts)), passed=(total_b == 0) if texts else None,
               detail=f"{len(texts)} artifacts, {total_b} blockers, {total_w} warnings")

    # 2. lawgate over the report itself (catches AI tells in what Brooks reads)
    # scope "report": only rules that apply everywhere (AI tells); prompt- and
    # copy-scoped rules skip, since a report legitimately names what it avoided
    report = run_dir / "report.md"
    if report.is_file():
        res = laws.lawgate(report.read_text(errors="replace"), run.brand, scope="report")
        store.eval(run.id, "lawgate_report", "deterministic", score=None,
                   passed=len(res["blockers"]) == 0,
                   detail=f"{len(res['blockers'])} blockers, {len(res['warnings'])} warnings")
        store.eval(run.id, "report_written", "deterministic", score=None, passed=True, detail="")
    else:
        store.eval(run.id, "report_written", "deterministic", score=None, passed=False,
                   detail="report.md missing")

    # 3. stop condition and cost
    store.eval(run.id, "stop_condition", "deterministic", score=None, passed=run.stop_met,
               detail=run.stop_detail or "")
    store.eval(run.id, "cost_usd", "deterministic", score=run.cost_usd, passed=None,
               detail=f"turns={run.num_turns}")
