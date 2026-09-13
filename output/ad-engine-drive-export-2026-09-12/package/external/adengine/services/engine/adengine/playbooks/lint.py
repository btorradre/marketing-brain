"""Playbook leak lint.

Playbooks are extracted from a single-operator vault. Anything in them that only
means something on that operator's machine (paths, local scripts, MCP tool names,
the owner's name as an approval authority, localhost ports, secrets) is a "leak":
it must be rewritten by a human before the playbook is served to other workspaces.

`audit(text)` returns one finding per (line, kind) as {line, kind, excerpt}.
`strip_secrets(text)` removes whole lines that carry a literal API key and reports them.

Ported from the vault's manus_export.py leak audit and extended.
"""
from __future__ import annotations
import re

# Token shapes that are real secrets, never prose. Lines carrying these are removed.
SECRET_PATTERNS: list[tuple[str, re.Pattern]] = [
    ("openai_key", re.compile(r"\bsk-[A-Za-z0-9_-]{16,}")),
    ("google_key", re.compile(r"\bAIza[0-9A-Za-z_-]{20,}")),
    ("github_token", re.compile(r"\bgh[pousr]?_[A-Za-z0-9]{16,}")),
    ("slack_token", re.compile(r"\bxox[abp]-[A-Za-z0-9-]{10,}")),
    ("aws_key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
]

_APPROVAL_WORDS = re.compile(
    r"approv|sign[- ]?off|signs off|confirm|ruled|ruling|decid|authori[sz]|"
    r"picks|chooses|names|supplied|wants|asks|says|overrode|override|law\b|gate|greenlight|go/no-go",
    re.IGNORECASE,
)

# (kind, compiled pattern). Order matters only for readability; every kind is checked per line.
LEAK_PATTERNS: list[tuple[str, re.Pattern]] = [
    ("absolute_path", re.compile(r"(?:/Users/|/private/)[^\s)\]'\"`>,]*")),
    ("home_path", re.compile(r"(?<![\w])~/[\w.\-][^\s)\]'\"`>,]*")),
    ("vault_path", re.compile(
        r"marketing brain|\bbrands/[\w.\-]+/?|(?<![\w])_engine/[^\s)\]'\"`>,]*|\.claude/skills[^\s)\]'\"`>,]*"
    )),
    ("script_invocation", re.compile(r"\bpython3?\s+(?:-m\s+)?[\w./\-]*\.py\b|\buv run\b")),
    # tool names, not model ids (eleven_multilingual_v2) and not file names (kie_tasks.json)
    ("mcp_tool", re.compile(
        r"\bmcp__\w+|(?<![\w.-])(?!eleven_(?:multilingual|turbo|flash|monolingual|english|v\d))"
        r"(?:dr|kie|heygen|eleven|plan)_[a-z][a-z0-9_]*\b(?!\.(?:json|py|md|txt|csv))"
    )),
    ("env_file", re.compile(r"(?<![\w/])\.env\b|\.mcp\.json\b")),
    ("localhost", re.compile(r"\b(?:localhost|127\.0\.0\.1|0\.0\.0\.0):\d{2,5}\b")),
    ("api_key", re.compile("|".join(p.pattern for _, p in SECRET_PATTERNS))),
]

_OWNER = re.compile(r"\bBrooks\b")

# Words that look like MCP tool prefixes but are ordinary identifiers.
_MCP_FALSE_POSITIVES = {"plan_id", "plan_name", "plan_file", "dr_os", "plan_b"}


def _excerpt(line: str, m: re.Match, width: int = 80) -> str:
    start = max(0, m.start() - 20)
    end = min(len(line), m.end() + width - 20)
    s = line[start:end].strip()
    if start > 0:
        s = "..." + s
    if end < len(line):
        s += "..."
    return s


def audit(text: str) -> list[dict]:
    """Return leak findings for `text`. One finding per (line, kind)."""
    hits: list[dict] = []
    for i, line in enumerate(text.splitlines(), 1):
        for kind, pat in LEAK_PATTERNS:
            m = pat.search(line)
            if not m:
                continue
            if kind == "mcp_tool" and m.group(0).lower() in _MCP_FALSE_POSITIVES:
                continue
            hits.append({"line": i, "kind": kind, "excerpt": _excerpt(line, m)})
        m = _OWNER.search(line)
        if m:
            kind = "approval_authority" if _APPROVAL_WORDS.search(line) else "person_name"
            hits.append({"line": i, "kind": kind, "excerpt": _excerpt(line, m)})
    return hits


def strip_secrets(text: str) -> tuple[str, list[dict]]:
    """Remove every line carrying a literal API key. Returns (clean_text, removed)."""
    kept: list[str] = []
    removed: list[dict] = []
    for i, line in enumerate(text.splitlines(keepends=True), 1):
        hit = None
        for kind, pat in SECRET_PATTERNS:
            m = pat.search(line)
            if m:
                hit = (kind, m.group(0))
                break
        if hit:
            kind, tok = hit
            removed.append({"line": i, "kind": kind, "excerpt": tok[:6] + "..." + tok[-4:]})
            kept.append("[line removed by playbook lint: contained a literal API key]\n")
        else:
            kept.append(line)
    return "".join(kept), removed


def summarize(hits: list[dict]) -> dict[str, int]:
    out: dict[str, int] = {}
    for h in hits:
        out[h["kind"]] = out.get(h["kind"], 0) + 1
    return out
