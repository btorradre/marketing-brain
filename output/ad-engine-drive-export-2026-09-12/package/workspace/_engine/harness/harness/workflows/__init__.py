"""Workflow registry. A workflow is a directory with `policy.yaml` and `spec.md`.

policy.yaml keys (all optional except `stop`):
  description: one line
  stages: [research, angles, script, storyboard, ...]   house-law sections injected
  skills: [names]            preloaded skills (product-truth skill is added per product)
  allowed_tools: [names]     Claude Code tool names and mcp__server__tool names
  disallowed_tools: [names]
  flags: {generate: false, animate: false, publish: false, spend_cap_usd: 0}
  flag_tools: {generate: [tool names gated by the flag], animate: [...], publish: [...]}
  budget: {max_turns: 120, max_budget_usd: 15, wall_clock_min: 90}
  stop: {tool: mcp__dr-os__dr_push_brief_board, result_contains: "url"}   stop artifact
  model: opus | sonnet | claude-opus-5 ...
  effort: low|medium|high|xhigh|max
  inputs: {ref: {required: true, help: "..."}, ...}
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

from .. import settings


@dataclass
class Workflow:
    name: str
    path: Path
    policy: dict = field(default_factory=dict)
    spec: str = ""

    @property
    def description(self) -> str:
        return self.policy.get("description", "")

    def validate_inputs(self, inputs: dict) -> list[str]:
        missing = []
        for key, meta in (self.policy.get("inputs") or {}).items():
            if (meta or {}).get("required") and not inputs.get(key):
                missing.append(f"--{key}: {(meta or {}).get('help', '')}".rstrip())
        return missing


def _load(path: Path) -> Workflow:
    policy = yaml.safe_load((path / "policy.yaml").read_text()) or {}
    spec = (path / "spec.md").read_text() if (path / "spec.md").is_file() else ""
    return Workflow(name=path.name.replace("_", "-"), path=path, policy=policy, spec=spec)


def registry() -> dict[str, Workflow]:
    out = {}
    if not settings.WORKFLOWS_DIR.is_dir():
        return out
    for p in sorted(settings.WORKFLOWS_DIR.iterdir()):
        if p.is_dir() and (p / "policy.yaml").is_file():
            wf = _load(p)
            out[wf.name] = wf
    return out


def get(name: str) -> Workflow:
    reg = registry()
    key = name.replace("_", "-")
    if key not in reg:
        raise KeyError(f"unknown workflow '{name}'. Known: {', '.join(sorted(reg)) or 'none'}")
    return reg[key]
