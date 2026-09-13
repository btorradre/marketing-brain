#!/usr/bin/env python3
"""
setup.py: preflight for applicant-screener. Silent on success.

Checks the media toolchain, the local Playwright MCP registration, and the
persistent browser profile that holds the OnlineJobs login.
"""

import json
import os
import shutil
import sys
from pathlib import Path

PROFILE = Path.home() / ".claude" / "playwright-profiles" / "hiring"
CLAUDE_JSON = Path.home() / ".claude.json"

problems, notes = [], []

for tool, how in (
    ("yt-dlp", "brew install yt-dlp"),
    ("ffmpeg", "brew install ffmpeg"),
    ("ffprobe", "brew install ffmpeg"),
):
    if not shutil.which(tool):
        problems.append(f"missing `{tool}`, install with: {how}")

# Local Playwright MCP. The Apify one cannot see a logged-in session, so its
# presence is not a substitute and is worth calling out explicitly.
try:
    cfg = json.loads(CLAUDE_JSON.read_text())
    servers = cfg.get("mcpServers", {})
    if "playwright" not in servers:
        problems.append(
            "local Playwright MCP not registered. Install with:\n"
            "  claude mcp add --scope user playwright "
            f"--env npm_config_cache={Path.home()}/.cache/npm-claude "
            "-- npx -y @playwright/mcp@latest "
            f"--user-data-dir {PROFILE} --viewport-size 1440x900"
        )
    elif "apify" in json.dumps(servers.get("playwright", {})).lower():
        problems.append(
            "the server named `playwright` points at Apify. This skill needs a "
            "LOCAL browser. The Apify one runs in their cloud and cannot see "
            "the OnlineJobs login."
        )
except FileNotFoundError:
    problems.append(f"cannot read {CLAUDE_JSON}")
except json.JSONDecodeError:
    problems.append(f"{CLAUDE_JSON} is not valid JSON")

if not PROFILE.exists():
    notes.append(
        f"browser profile {PROFILE} does not exist yet. It is created on the "
        "first Playwright run. Brooks signs into OnlineJobs.ph once in that "
        "window and the session persists afterwards."
    )
elif not any(PROFILE.iterdir()):
    notes.append(
        "browser profile is empty, so there is no saved OnlineJobs session yet. "
        "Expect a login page on the first navigate; ask Brooks to sign in rather "
        "than attempting it."
    )

if not os.environ.get("ELEVENLABS_API_KEY"):
    notes.append(
        "ELEVENLABS_API_KEY not in the environment. Loom transcripts will fall "
        "back to captions only, and Loom rarely has them. Source the vault .env "
        "before running the harvest for full transcripts."
    )

if problems:
    print("applicant-screener preflight FAILED:\n")
    for p in problems:
        print(f"  ✗ {p}\n")
    for n in notes:
        print(f"  · {n}\n")
    sys.exit(2)

if notes:
    for n in notes:
        print(f"note: {n}")
sys.exit(0)
