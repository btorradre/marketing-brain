"""The run record. One run = one workflow execution = one Agent SDK session."""

from __future__ import annotations

import json
import secrets
import time
from dataclasses import asdict, dataclass, field
from typing import Any

STATUSES = ("queued", "running", "blocked_on_human", "done", "failed", "cancelled")


def new_run_id(workflow: str, brand: str | None) -> str:
    stamp = time.strftime("%Y%m%d-%H%M%S")
    return f"{(brand or 'x')[:8]}-{workflow[:16]}-{stamp}-{secrets.token_hex(2)}"


@dataclass
class Run:
    id: str
    workflow: str
    brand: str | None = None
    product: str | None = None
    inputs: dict[str, Any] = field(default_factory=dict)
    flags: dict[str, Any] = field(default_factory=dict)
    policy: dict[str, Any] = field(default_factory=dict)
    budget: dict[str, Any] = field(default_factory=dict)
    stop: str | None = None
    parent_run: str | None = None
    created_by: str = "brooks"
    status: str = "queued"
    session_id: str | None = None
    cost_usd: float | None = None
    num_turns: int | None = None
    stop_met: bool = False
    stop_detail: str | None = None
    error: str | None = None
    created_at: float = field(default_factory=time.time)
    started_at: float | None = None
    ended_at: float | None = None

    @classmethod
    def create(cls, workflow: str, brand: str | None, product: str | None,
               inputs: dict, flags: dict, policy: dict, budget: dict,
               stop: str | None, parent_run: str | None = None,
               created_by: str = "brooks") -> "Run":
        return cls(id=new_run_id(workflow, brand), workflow=workflow, brand=brand,
                   product=product, inputs=inputs, flags=flags, policy=policy,
                   budget=budget, stop=stop, parent_run=parent_run,
                   created_by=created_by)

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, default=str)

    @classmethod
    def from_dict(cls, d: dict) -> "Run":
        known = {f for f in cls.__dataclass_fields__}
        return cls(**{k: v for k, v in d.items() if k in known})
