"""Executes one run as one Claude Agent SDK session.

Deterministic code owns: policy enforcement, flag gating, budget, stop
detection, trace, bundle, evals, notifications. The agent owns the work.
"""

from __future__ import annotations

import asyncio
import json
import time
import traceback
from pathlib import Path
from typing import Any

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    HookMatcher,
    ResultMessage,
    TextBlock,
    query,
)

from . import bundle, evals, notify, settings
from .context import build_system_prompt
from .models import Run
from .store import RunStore
from .trace import Trace
from .workflows import Workflow, get as get_workflow

ALWAYS_ALLOWED_AFTER_STOP = {"Write", "Read", "Edit"}


class RunState:
    def __init__(self, run: Run, wf: Workflow, run_dir: Path, trace: Trace, store: RunStore):
        self.run, self.wf, self.run_dir, self.trace, self.store = run, wf, run_dir, trace, store
        self.stop_met = False
        self.stop_detail: str | None = None
        self.denied: list[dict] = []
        self.started = time.time()
        pol = wf.policy
        self.flag_tools: dict[str, set[str]] = {k: set(v or []) for k, v in (pol.get("flag_tools") or {}).items()}
        stop = pol.get("stop") or {}
        self.stop_tool: str | None = stop.get("tool")
        self.stop_contains: str | None = stop.get("result_contains")
        self.stop_file: str | None = stop.get("file")
        self.wall_clock_s = float((run.budget or {}).get("wall_clock_min") or 0) * 60


def _tool_gated_off(state: RunState, tool: str) -> str | None:
    for flag, tools in state.flag_tools.items():
        if tool in tools and not state.run.flags.get(flag, False):
            return flag
    return None


def make_hooks(state: RunState) -> dict[str, list[HookMatcher]]:
    async def pre_tool(inp: dict, tool_use_id: str | None, ctx: Any) -> dict:
        tool = inp.get("tool_name", "")
        state.trace.write("hook:PreToolUse", {"tool": tool, "input": inp.get("tool_input")})
        flag = _tool_gated_off(state, tool)
        if flag:
            reason = f"harness policy: tool '{tool}' is gated by flag '{flag}', which is off for this run"
            state.denied.append({"tool": tool, "reason": reason})
            return {"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                           "permissionDecision": "deny",
                                           "permissionDecisionReason": reason}}
        if state.wall_clock_s and time.time() - state.started > state.wall_clock_s:
            reason = "harness budget: wall clock exceeded, write report.md and end"
            if tool not in ALWAYS_ALLOWED_AFTER_STOP:
                state.denied.append({"tool": tool, "reason": reason})
                return {"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                               "permissionDecision": "deny",
                                               "permissionDecisionReason": reason}}
        if state.stop_met and tool not in ALWAYS_ALLOWED_AFTER_STOP:
            reason = ("harness stop: the stop artifact exists. Write report.md in the run "
                      "directory and end with RUN COMPLETE. No further tool calls.")
            state.denied.append({"tool": tool, "reason": reason})
            return {"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                           "permissionDecision": "deny",
                                           "permissionDecisionReason": reason}}
        return {}

    async def post_tool(inp: dict, tool_use_id: str | None, ctx: Any) -> dict:
        tool = inp.get("tool_name", "")
        resp = inp.get("tool_response")
        state.trace.write("hook:PostToolUse", {"tool": tool, "response": str(resp)[:2000]})
        if state.stop_tool and tool == state.stop_tool and not state.stop_met:
            text = json.dumps(resp, default=str) if not isinstance(resp, str) else resp
            if not state.stop_contains or state.stop_contains in text:
                if '"error"' not in text[:200].lower():
                    state.stop_met = True
                    state.stop_detail = f"{tool} returned {text[:160]}"
                    state.store.event(state.run.id, "stop_met", {"tool": tool})
                    return {"systemMessage": "Stop artifact exists. Write report.md now and end "
                                             "with RUN COMPLETE."}
        if state.stop_file and (state.run_dir / state.stop_file).is_file() and not state.stop_met:
            state.stop_met = True
            state.stop_detail = f"file {state.stop_file} written"
        return {}

    return {"PreToolUse": [HookMatcher(matcher=None, hooks=[pre_tool])],
            "PostToolUse": [HookMatcher(matcher=None, hooks=[post_tool])]}


def build_options(state: RunState, system_prompt: str) -> ClaudeAgentOptions:
    pol, run = state.wf.policy, state.run
    skills = list(pol.get("skills") or [])
    if run.product and run.brand:
        # product-truth skills follow <brand>-<product>; harmless if absent
        skills.append(f"{run.brand}-{run.product}")
    budget = run.budget or {}
    cwd = settings.BRANDS_DIR / run.brand if run.brand and (settings.BRANDS_DIR / run.brand).is_dir() else settings.VAULT
    return ClaudeAgentOptions(
        system_prompt={"type": "preset", "preset": "claude_code", "append": system_prompt},
        cwd=str(cwd),
        add_dirs=[str(settings.VAULT), str(state.run_dir)],
        setting_sources=["user", "project"],
        mcp_servers=str(settings.MCP_CONFIG) if settings.MCP_CONFIG.is_file() else {},
        allowed_tools=list(pol.get("allowed_tools") or []),
        disallowed_tools=list(pol.get("disallowed_tools") or []),
        skills=skills or None,
        permission_mode="bypassPermissions",
        max_turns=int(budget.get("max_turns") or settings.DEFAULT_MAX_TURNS),
        max_budget_usd=float(budget.get("max_budget_usd") or settings.DEFAULT_MAX_BUDGET_USD),
        model=pol.get("model") or settings.DEFAULT_MODEL,
        effort=pol.get("effort") or settings.DEFAULT_EFFORT,
        hooks=make_hooks(state),
        cli_path=settings.CLAUDE_CLI,
        env={"HARNESS_RUN_ID": run.id, "HARNESS_RUN_DIR": str(state.run_dir)},
    )


def _blocked_on_human(report: Path) -> bool:
    """True unless the '## Blocked on Brooks' section's first line is literally 'nothing'."""
    if not report.is_file():
        return False
    text = report.read_text(errors="replace")
    if "## Blocked on Brooks" not in text:
        return False
    section = text.split("## Blocked on Brooks", 1)[1]
    section = section.split("\n## ", 1)[0]
    lines = [ln.strip().strip("`*_.- ").lower() for ln in section.splitlines() if ln.strip()]
    if not lines:
        return False
    return lines[0] not in {"nothing", "none", "no", "nothing."}


def kickoff_prompt(state: RunState) -> str:
    return (f"Begin run {state.run.id}: workflow {state.wf.name} for brand {state.run.brand}, "
            f"product {state.run.product}. Follow the workflow spec in your system prompt "
            f"step by step. Inputs: {json.dumps(state.run.inputs)}")


async def _execute(store: RunStore, run: Run) -> Run:
    wf = get_workflow(run.workflow)
    run_dir = bundle.run_dir(settings.RUNS_DIR, run)
    trace = Trace(run_dir / "trace.jsonl")
    state = RunState(run, wf, run_dir, trace, store)

    run.status, run.started_at = "running", time.time()
    store.save(run); bundle.write_run_json(run_dir, run)
    store.event(run.id, "started", {"workflow": wf.name})

    system_prompt = build_system_prompt(wf, run, run_dir, store)
    (run_dir / "system_prompt.md").write_text(system_prompt)
    options = build_options(state, system_prompt)
    trace.write("options", {k: v for k, v in options.__dict__.items()
                            if k not in {"hooks", "can_use_tool", "debug_stderr", "stderr"}})

    result: ResultMessage | None = None
    last_text = ""
    try:
        async for msg in query(prompt=kickoff_prompt(state), options=options):
            trace.message(msg)
            if isinstance(msg, AssistantMessage):
                for b in msg.content:
                    if isinstance(b, TextBlock) and b.text.strip():
                        last_text = b.text
            elif isinstance(msg, ResultMessage):
                result = msg
    except Exception as e:  # noqa: BLE001
        run.error = f"{type(e).__name__}: {e}"
        trace.write("exception", {"error": run.error, "tb": traceback.format_exc()[-3000:]})

    run.stop_met, run.stop_detail = state.stop_met, state.stop_detail
    if result is not None:
        run.session_id = result.session_id
        run.cost_usd = result.total_cost_usd
        run.num_turns = result.num_turns
        if result.is_error and not run.error:
            run.error = f"sdk result {result.subtype}: {(result.errors or [result.result])}"
    if (run_dir / "report.md").is_file() and "RUN COMPLETE" not in (run_dir / "report.md").read_text(errors="replace") and last_text:
        # agent's final text is often the completion line; keep it with the report
        with open(run_dir / "report.md", "a") as fh:
            fh.write("\n\n---\n" + last_text[-2000:])

    blocked = _blocked_on_human(run_dir / "report.md")
    if run.error:
        run.status = "failed"
    elif not run.stop_met and state.stop_tool:
        run.status = "failed"
        run.error = run.error or "stop condition never met"
    else:
        run.status = "blocked_on_human" if blocked else "done"
    run.ended_at = time.time()
    if state.denied:
        store.event(run.id, "denied_tool_calls", {"count": len(state.denied), "sample": state.denied[:10]})

    trace.close()
    store.save(run)
    evals.run_evals(store, run, run_dir)
    bundle.write_run_json(run_dir, run)
    bundle.write_evals(run_dir, store, run)
    bundle.write_index(run_dir, run, store)
    store.event(run.id, "finished", {"status": run.status, "cost": run.cost_usd})

    summary = (f"[{run.status}] {run.id} · {wf.name} · {run.brand}/{run.product} · "
               f"turns {run.num_turns} · ${run.cost_usd}\n{run_dir / 'index.html'}")
    if run.status == "blocked_on_human":
        summary = "NEEDS YOU: " + summary
    notify.send(summary)
    return run


def execute(store: RunStore, run: Run) -> Run:
    return asyncio.run(_execute(store, run))
