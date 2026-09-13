"""Builds the encoded system prompt for a run.

Order matters for prompt caching: stable material first (harness frame,
workflow spec, laws), volatile material last (run inputs, prior reports).
"""

from __future__ import annotations

from pathlib import Path

from . import laws, settings
from .models import Run
from .store import RunStore
from .workflows import Workflow

HARNESS_FRAME = """You are running inside Brooks's marketing harness, not an open-ended chat.
This session is ONE run of the workflow named below. You have a fixed job, a fixed
tool policy, and a stop condition. When the stop artifact exists, write the run
report and end. Do not ask Brooks questions; he is not watching. Make every
routine call yourself and state assumptions in the report. If a hard blocker
appears (missing product truth, provider balance, an unverifiable claim), stop,
write the report with the blocker named, and end.

Every deliverable path you mention in the report is a full absolute path.
Never invent citations, studies, reviews, or quotes. Never paste a filesystem path
into copy meant for an editor or a customer. No em dashes anywhere you write,
including the report and working notes; use a period, comma, or parentheses."""


def _read(path: Path, limit: int = 20_000) -> str:
    if not path.is_file():
        return ""
    text = path.read_text(errors="replace")
    return text if len(text) <= limit else text[:limit] + "\n\n[truncated]"


def brand_block(brand: str | None, product: str | None) -> str:
    if not brand:
        return ""
    bdir = settings.BRANDS_DIR / brand
    parts = [f"# Brand: {brand}\nBrand folder: {bdir}"]
    brief = _read(bdir / "00-brief.md")
    parts.append("## 00-brief.md\n" + brief if brief else
                 "## 00-brief.md\nMissing. Reconstruct from research/ and products/ via "
                 "dr_load_brand and say which files you used.")
    if product:
        pdir = bdir / "products" / product
        if pdir.is_dir():
            files = sorted(str(p.relative_to(bdir)) for p in pdir.rglob("*")
                           if p.is_file() and p.suffix in {".md", ".json", ".txt"})[:60]
            parts.append(f"# Product: {product}\nProduct folder: {pdir}\nFiles:\n" +
                         "\n".join(f"- {f}" for f in files))
        else:
            parts.append(f"# Product: {product}\nNo folder at {pdir}. Load the product-truth "
                         "skill and verify against the live store.")
    return "\n\n".join(parts)


def prior_runs_block(store: RunStore, run: Run) -> str:
    prior = [r for r in store.recent_done(run.brand, run.product, settings.PRIOR_RUN_REPORTS)
             if r.id != run.id]
    if not prior:
        return ""
    out = ["# What the last runs for this brand and product learned"]
    for r in prior:
        report = _read(settings.RUNS_DIR / (r.brand or "x") / r.id / "report.md", limit=4_000)
        if report:
            out.append(f"## {r.id} ({r.workflow}, {r.status})\n{report}")
    return "\n\n".join(out) if len(out) > 1 else ""


def run_block(run: Run, run_dir: Path) -> str:
    inputs = "\n".join(f"- {k}: {v}" for k, v in run.inputs.items()) or "- none"
    flags = "\n".join(f"- {k}: {v}" for k, v in run.flags.items()) or "- none"
    return f"""# This run
- run id: {run.id}
- workflow: {run.workflow}
- brand: {run.brand}
- product: {run.product}
- run directory (write report.md and any working files here): {run_dir}
- stop condition: {run.stop}

## Inputs
{inputs}

## Flags (tools gated by a false flag are denied by the harness, do not retry them)
{flags}

## Ending the run
When the stop artifact exists, write `{run_dir}/report.md` with these sections:
`## Outcome`, `## Decisions and assumptions`, `## Artifacts` (full absolute paths and
board URLs), `## Blocked on Brooks` (what needs approval, or "nothing"),
`## What the next run should know`. Then end with one line: `RUN COMPLETE`."""


def build_system_prompt(wf: Workflow, run: Run, run_dir: Path, store: RunStore) -> str:
    stages = wf.policy.get("stages") or []
    law_text = laws.house_laws(stages, run.brand)
    blocks = [
        HARNESS_FRAME,
        f"# Workflow: {wf.name}\n{wf.description}\n\n{wf.spec}",
        ("# House laws for the stages this run touches\n" + law_text) if law_text else
        "# House laws\nNo house-laws.md found in the laws directory. Load dr_get_playbook('laws').",
        brand_block(run.brand, run.product),
        prior_runs_block(store, run),
        run_block(run, run_dir),
    ]
    return "\n\n---\n\n".join(b for b in blocks if b)
