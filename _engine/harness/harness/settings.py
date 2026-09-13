"""All paths and knobs come from env with vault-relative defaults.

Nothing else in the package touches Path.home() or hard-codes a location.
"""

from __future__ import annotations

import os
import shutil
from pathlib import Path

_HERE = Path(__file__).resolve()
VAULT = Path(os.environ.get("HARNESS_VAULT", _HERE.parents[3]))
HARNESS_DIR = Path(os.environ.get("HARNESS_DIR", _HERE.parents[1]))

RUNS_DIR = Path(os.environ.get("HARNESS_RUNS_DIR", HARNESS_DIR / "runs"))
DB_PATH = Path(os.environ.get("HARNESS_DB", HARNESS_DIR / "harness.db"))
WORKFLOWS_DIR = Path(os.environ.get("HARNESS_WORKFLOWS_DIR", _HERE.parent / "workflows"))

# laws-as-data: global.json + examples/<brand>.json + house-laws.md
LAWS_DIR = Path(os.environ.get("HARNESS_LAWS_DIR", VAULT / "_engine" / "laws"))

BRANDS_DIR = Path(os.environ.get("HARNESS_BRANDS_DIR", VAULT / "brands"))
MCP_CONFIG = Path(os.environ.get("HARNESS_MCP_CONFIG", VAULT / ".mcp.json"))

CLAUDE_CLI = os.environ.get("HARNESS_CLAUDE_CLI") or shutil.which("claude") \
    or str(Path(os.environ.get("HOME", "")) / ".local" / "bin" / "claude")

DEFAULT_MODEL = os.environ.get("HARNESS_MODEL", "opus")
DEFAULT_EFFORT = os.environ.get("HARNESS_EFFORT", "high")
DEFAULT_MAX_TURNS = int(os.environ.get("HARNESS_MAX_TURNS", "120"))
DEFAULT_MAX_BUDGET_USD = float(os.environ.get("HARNESS_MAX_BUDGET_USD", "15"))
PRIOR_RUN_REPORTS = int(os.environ.get("HARNESS_PRIOR_RUN_REPORTS", "5"))

# Telegram gate transport (H1). Unset = notifications are logged only.
TELEGRAM_BOT_TOKEN = os.environ.get("HARNESS_TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("HARNESS_TELEGRAM_CHAT_ID")


def ensure_dirs() -> None:
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
