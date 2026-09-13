#!/usr/bin/env python3
"""Cut all Hermes/Paperclip reasoning routes over to GPT-5.6 Sol.

Precondition: /root/.hermes/auth.json contains a working openai-codex OAuth
credential, verified with a live inference before this script is run.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import urllib.request

import yaml


PROVIDER = "openai-codex"
MODEL = "gpt-5.6-sol"
BASE_URL = "https://chatgpt.com/backend-api/codex"
COMPANY_ID = "9341b832-0f97-4c3f-9171-fdfb899c2464"
API = "http://127.0.0.1:3100/api"

PROFILES = [
    Path("/root/.hermes"),
    Path("/root/.hermes-ceo"),
    Path("/root/.hermes-cfo"),
    Path("/root/.hermes-coo"),
    Path("/root/.hermes-designer"),
    Path("/root/.hermes-professor"),
    Path("/root/.hermes-strategist"),
    Path("/root/.hermes-cqm"),
    Path("/root/.hermes-creative"),
    Path("/root/.hermes-cro"),
    Path("/root/.hermes-mediabuyer"),
]


def atomic_text(path: Path, text: str, mode: int | None = None) -> None:
    tmp = path.with_name(path.name + ".bto-cutover.tmp")
    tmp.write_text(text)
    if mode is not None:
        os.chmod(tmp, mode)
    os.replace(tmp, path)


def api_json(method: str, path: str, body: dict | None = None):
    data = None if body is None else json.dumps(body).encode()
    request = urllib.request.Request(
        API + path,
        data=data,
        method=method,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def require_oauth(main_auth: dict) -> None:
    pool = main_auth.get("credential_pool")
    entries = pool.get(PROVIDER) if isinstance(pool, dict) else None
    if not isinstance(entries, list) or not entries:
        raise SystemExit(
            "No openai-codex credential in the main profile; authenticate first."
        )


def backup_current_state() -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    root = Path("/root/hermes-migration-backups") / f"pre-sol-cutover-{stamp}"
    root.mkdir(parents=True, mode=0o700)
    for profile in PROFILES:
        target = root / "profiles" / profile.name
        target.mkdir(parents=True, mode=0o700)
        for filename in ("config.yaml", "auth.json", "SOUL.md"):
            source = profile / filename
            if source.is_file():
                shutil.copy2(source, target / filename)
    agents = api_json("GET", f"/companies/{COMPANY_ID}/agents")
    atomic_text(root / "paperclip-agents.json", json.dumps(agents, indent=2), 0o600)
    return root


def merge_codex_auth(main_auth: dict, profile: Path) -> None:
    path = profile / "auth.json"
    if path.exists():
        auth = json.loads(path.read_text())
    else:
        auth = {"version": main_auth.get("version", 1), "providers": {}, "credential_pool": {}}

    auth.setdefault("credential_pool", {})[PROVIDER] = deepcopy(
        main_auth["credential_pool"][PROVIDER]
    )
    main_provider_state = (main_auth.get("providers") or {}).get(PROVIDER)
    if main_provider_state is not None:
        auth.setdefault("providers", {})[PROVIDER] = deepcopy(main_provider_state)
    auth["active_provider"] = PROVIDER
    auth["updated_at"] = datetime.now(timezone.utc).isoformat()
    atomic_text(path, json.dumps(auth, indent=2) + "\n", 0o600)


def update_profile_config(profile: Path) -> None:
    path = profile / "config.yaml"
    config = yaml.safe_load(path.read_text()) or {}

    old_model = config.get("model")
    if isinstance(old_model, dict):
        model = dict(old_model)
    elif isinstance(old_model, str) and old_model.strip():
        model = {"default": old_model.strip()}
    else:
        model = {}
    model.update(
        {
            "default": MODEL,
            "provider": PROVIDER,
            "base_url": BASE_URL,
            "api_mode": "codex_responses",
        }
    )
    model.pop("api_key", None)
    config["model"] = model

    agent = config.setdefault("agent", {})
    if not agent.get("reasoning_effort"):
        agent["reasoning_effort"] = "medium"

    delegation = config.setdefault("delegation", {})
    delegation["model"] = MODEL
    delegation["provider"] = PROVIDER
    delegation["reasoning_effort"] = agent["reasoning_effort"]
    # Let the provider resolver obtain and refresh the OAuth credential. A
    # direct URL/key override would bypass that path or preserve Anthropic.
    delegation.pop("api_key", None)
    delegation.pop("base_url", None)
    delegation.pop("api_mode", None)

    rendered = yaml.safe_dump(config, sort_keys=False, allow_unicode=True)
    yaml.safe_load(rendered)
    atomic_text(path, rendered, 0o600)

    soul_path = profile / "SOUL.md"
    if soul_path.is_file():
        soul = soul_path.read_text()
        soul = soul.replace(
            "Runs on Sonnet — looser persona, executes without flinching.",
            "Runs on GPT-5.6 Sol through the shared Hermes reasoning route.",
        )
        atomic_text(soul_path, soul)


def update_paperclip_agents() -> tuple[int, int]:
    agents = api_json("GET", f"/companies/{COMPANY_ID}/agents")
    changed = 0
    reset = 0
    for agent in agents:
        body = {
            "adapterType": "hermes_local",
            "adapterConfig": {"provider": PROVIDER, "model": MODEL},
        }
        if agent.get("adapterType") != "hermes_local":
            # Adapter changes replace adapter-specific fields. Preserve the
            # fields that are valid and useful to Hermes while discarding
            # Claude-only permission switches.
            old = agent.get("adapterConfig") or {}
            keep = {
                key: old[key]
                for key in (
                    "enabledToolsets",
                    "graceSec",
                    "instructionsBundleMode",
                    "instructionsEntryFile",
                    "instructionsFilePath",
                    "instructionsRootPath",
                    "maxIterations",
                    "persistSession",
                    "timeoutSec",
                    "workingDirectory",
                )
                if key in old
            }
            keep.update(body["adapterConfig"])
            body["adapterConfig"] = keep
        api_json("PATCH", f"/agents/{agent['id']}", body)
        changed += 1

    # Existing sessions retain old provider/model context. Reset only runtime
    # session pointers; this does not delete issues, instructions, or work.
    for agent in agents:
        api_json("POST", f"/agents/{agent['id']}/runtime-state/reset-session", {})
        reset += 1
    return changed, reset


def validate_profiles() -> None:
    for profile in PROFILES:
        config = yaml.safe_load((profile / "config.yaml").read_text())
        assert config["model"]["provider"] == PROVIDER
        assert config["model"]["default"] == MODEL
        assert config["model"]["api_mode"] == "codex_responses"
        assert config["delegation"]["provider"] == PROVIDER
        assert config["delegation"]["model"] == MODEL
        auth = json.loads((profile / "auth.json").read_text())
        assert auth["credential_pool"][PROVIDER]


def main() -> None:
    main_auth = json.loads((PROFILES[0] / "auth.json").read_text())
    require_oauth(main_auth)
    backup = backup_current_state()

    for profile in PROFILES:
        merge_codex_auth(main_auth, profile)
        update_profile_config(profile)
    validate_profiles()

    paperclip_changed, paperclip_reset = update_paperclip_agents()
    print(
        json.dumps(
            {
                "backup": str(backup),
                "profiles_changed": len(PROFILES),
                "paperclip_agents_changed": paperclip_changed,
                "paperclip_sessions_reset": paperclip_reset,
                "provider": PROVIDER,
                "model": MODEL,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
