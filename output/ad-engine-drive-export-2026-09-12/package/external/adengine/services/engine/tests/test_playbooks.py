"""packages/playbooks is a shipped data package; these tests pin its contract."""
import os
import re

import pytest

from adengine import playbooks
from adengine.core.errors import NotFound

ROOT = playbooks._root()

GOOGLE_KEY = re.compile(r"AIza")
GITHUB_TOKEN = re.compile(r"\bgh[pousr]?_[A-Za-z0-9]{16,}")
OPENAI_KEY = re.compile(r"\bsk-[A-Za-z0-9_-]{16,}")


@pytest.fixture(scope="module")
def reg():
    return playbooks.reload()


def test_registry_loads_with_enough_playbooks(reg):
    assert len(reg) >= 30
    names = [p["name"] for p in reg]
    assert len(names) == len(set(names)), "duplicate playbook names"


def test_every_record_has_contract_fields(reg):
    for p in reg:
        for k in ("name", "version", "stage", "bucket", "description", "files", "sections", "size", "leaks"):
            assert k in p, f"{p['name']} missing {k}"
        assert p["version"] == "1.0.0"
        assert p["stage"] in playbooks.STAGES, f"{p['name']} bad stage {p['stage']}"
        assert p["bucket"] in ("strategy", "copy", "production", "editing"), f"{p['name']} excluded bucket shipped"
        assert p["files"][0] == "playbook.md"
        for rel in p["files"]:
            assert os.path.isfile(os.path.join(ROOT, p["name"], rel)), f"{p['name']}/{rel} missing"


def test_no_api_keys_anywhere(reg):
    for p in reg:
        for rel in p["files"]:
            with open(os.path.join(ROOT, p["name"], rel), encoding="utf-8") as f:
                text = f.read()
            assert not GOOGLE_KEY.search(text), f"{p['name']}/{rel} contains an AIza key"
            assert not GITHUB_TOKEN.search(text), f"{p['name']}/{rel} contains a gh_ token"
            assert not OPENAI_KEY.search(text), f"{p['name']}/{rel} contains an sk- key"


def test_read_whole_and_one_section(reg):
    p = next(r for r in reg if len(r["sections"]) >= 2)
    whole = playbooks.read(p["name"])
    assert whole.startswith("---") or whole.strip()
    sec = p["sections"][1]
    body = playbooks.read(p["name"], section=sec["id"])
    assert len(body) == sec["chars"]
    first_line = body.splitlines()[0]
    assert sec["title"] in first_line or sec["id"] == "preamble"
    short = playbooks.read(p["name"], max_chars=100)
    assert len(short) < 250


def test_get_and_stages(reg):
    rec = playbooks.get(reg[0]["name"])
    assert rec["name"] == reg[0]["name"]
    with pytest.raises(NotFound):
        playbooks.get("no-such-playbook")
    with pytest.raises(NotFound):
        playbooks.read(reg[0]["name"], section="no-such-section")
    st = playbooks.stages()
    assert sum(len(v) for v in st.values()) == len(reg)
    assert "script" in st and "generation" in st


def test_lint_catches_the_leak_kinds():
    text = "\n".join([
        "run python3 tools/publish_brief.py --next-id",
        "open /Users/someone/Documents/x.md",
        "see ~/.claude/skills/foo",
        "the board lives at http://localhost:8765/boards",
        "call mcp__dr-os__dr_push_concept then kie_generate",
        "keys are in .env",
        "Brooks approves the board before render",
        "the vault is under marketing brain/brands/acme/",
    ])
    kinds = {h["kind"] for h in playbooks.lint(text)}
    for k in ("script_invocation", "absolute_path", "home_path", "localhost", "mcp_tool", "env_file",
              "approval_authority", "vault_path"):
        assert k in kinds, f"lint missed {k}"
    assert playbooks.lint("plain doctrine with no plumbing") == []


def test_strip_secrets_removes_key_lines():
    clean, removed = playbooks.strip_secrets("ok line\nkey=[REDACTED_SECRET]\nfine\n")
    assert "AIza" not in clean
    assert len(removed) == 1 and removed[0]["line"] == 2
    assert clean.count("\n") == 3
