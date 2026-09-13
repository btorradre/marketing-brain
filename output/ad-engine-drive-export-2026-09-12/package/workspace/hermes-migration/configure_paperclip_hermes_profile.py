#!/usr/bin/env python3
"""Create and optionally activate an isolated Hermes profile for Paperclip."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import urllib.request

import yaml


SOURCE = Path("/root/.hermes")
TARGET = Path("/root/.hermes-paperclip")
API = "http://127.0.0.1:3100/api"
COMPANY_ID = "9341b832-0f97-4c3f-9171-fdfb899c2464"
MODEL = "gpt-5.6-sol"
PROVIDER = "openai-codex"
SHARED_DIR = "/opt/vault/agents/hermes/shared-skills"
DOMAIN_DIR = "/root/.hermes/skills/domain"

SOUL = """# Paperclip Hermes Runtime

You are executing as one employee in the BTO EC Ventures Paperclip company.
Follow the managed role instructions and task context supplied for the current
agent. Do the work directly; do not wake or recursively delegate to another
Paperclip employee unless the task explicitly requires coordination.

For marketing, copy, customer research, creative strategy, positioning, CRO,
funnels, offers, and paid media, load and follow
`dtc-marketing-operating-system`. Begin inside the customer's existing language
and understanding. Do not force belief shifts. Use the simplest accurate causal
mechanism, establish solution criteria before product evaluation, preserve
funnel congruence, and never invent claims, proof, people, studies, statistics,
reviews, urgency, or scarcity.
"""


def atomic_text(path: Path, text: str, mode: int = 0o600) -> None:
    tmp = path.with_name(path.name + ".bto-paperclip.tmp")
    tmp.write_text(text)
    os.chmod(tmp, mode)
    os.replace(tmp, path)


def api_json(method: str, path: str, body: dict | None = None):
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(
        API + path,
        data=data,
        method=method,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)


def create_profile() -> None:
    config = yaml.safe_load((SOURCE / "config.yaml").read_text()) or {}
    auth = json.loads((SOURCE / "auth.json").read_text())
    if not (auth.get("credential_pool") or {}).get(PROVIDER):
        raise SystemExit("Main profile has no openai-codex OAuth credential")

    model = config.setdefault("model", {})
    if not isinstance(model, dict):
        model = config["model"] = {}
    model.update(
        {
            "default": MODEL,
            "provider": PROVIDER,
            "base_url": "https://chatgpt.com/backend-api/codex",
            "api_mode": "codex_responses",
        }
    )
    model.pop("api_key", None)

    delegation = config.setdefault("delegation", {})
    delegation.update(
        {"model": MODEL, "provider": PROVIDER, "reasoning_effort": "medium"}
    )
    for key in ("api_key", "base_url", "api_mode"):
        delegation.pop(key, None)

    # Paperclip is a noninteractive worker. Recoverable commands may run, but
    # Hermes's code-shipped hardline blocks and any approvals.deny rules still
    # execute before the yolo bypass.
    approvals = config.setdefault("approvals", {})
    approvals["mode"] = "off"
    approvals["timeout"] = 60

    # Paperclip agents use Hermes-native terminal/file/web tools. Avoid starting
    # unrelated MCP clients, whose stale shutdown coroutine currently writes a
    # traceback to stderr and causes adapter false failures.
    config["mcp_servers"] = {}
    config.pop("prefill_messages_file", None)

    skills = config.setdefault("skills", {})
    dirs = skills.setdefault("external_dirs", [])
    for item in (SHARED_DIR, DOMAIN_DIR):
        if item not in dirs:
            dirs.append(item)

    TARGET.mkdir(parents=True, exist_ok=True, mode=0o700)
    atomic_text(
        TARGET / "config.yaml",
        yaml.safe_dump(config, sort_keys=False, allow_unicode=True),
    )
    atomic_text(TARGET / "auth.json", json.dumps(auth, indent=2) + "\n")
    atomic_text(TARGET / "SOUL.md", SOUL, 0o644)

    check = yaml.safe_load((TARGET / "config.yaml").read_text())
    assert check["model"]["provider"] == PROVIDER
    assert check["model"]["default"] == MODEL
    assert check["approvals"]["mode"] == "off"
    assert check["mcp_servers"] == {}


def activate_profile() -> dict:
    agents = api_json("GET", f"/companies/{COMPANY_ID}/agents")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = Path("/root/hermes-migration-backups") / f"pre-paperclip-profile-{stamp}"
    backup.mkdir(parents=True, mode=0o700)
    atomic_text(backup / "paperclip-agents.json", json.dumps(agents, indent=2) + "\n")

    changed = 0
    reset = 0
    for agent in agents:
        config = agent.get("adapterConfig") or {}
        env = config.get("env") if isinstance(config.get("env"), dict) else {}
        env = dict(env)
        env["HERMES_HOME"] = str(TARGET)

        extras = config.get("extraArgs") if isinstance(config.get("extraArgs"), list) else []
        extras = [item for item in extras if item != "--yolo"] + ["--yolo"]
        api_json(
            "PATCH",
            f"/agents/{agent['id']}",
            {
                "adapterType": "hermes_local",
                "adapterConfig": {
                    "provider": PROVIDER,
                    "model": MODEL,
                    "env": env,
                    "extraArgs": extras,
                },
            },
        )
        changed += 1

    for agent in agents:
        api_json("POST", f"/agents/{agent['id']}/runtime-state/reset-session", {})
        reset += 1
    return {"backup": str(backup), "agents_changed": changed, "sessions_reset": reset}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--activate", action="store_true")
    args = parser.parse_args()
    create_profile()
    result = {"profile": str(TARGET), "created": True, "activated": False}
    if args.activate:
        result.update(activate_profile())
        result["activated"] = True
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
