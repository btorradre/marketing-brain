"""First-class agent capabilities, shared by the strategy and generation servers."""
from __future__ import annotations

import json

from adengine.core.errors import NotFound
from adengine.core.settings import settings

EDIT_ANALYSIS = "video-edit-analysis"


def list_capabilities(agent_role: str | None = None) -> list[dict]:
    with open(settings.packages_path("capabilities", "registry.json"), encoding="utf-8") as stream:
        capabilities = json.load(stream)
    if agent_role is not None:
        capabilities = [c for c in capabilities if agent_role in (c["owner_agent"], c["handoff_agent"])]
    return capabilities


def get_capability(capability_id: str) -> dict:
    for capability in list_capabilities():
        if capability["id"] == capability_id:
            return capability
    raise NotFound(f"Unknown agent capability: {capability_id}")
