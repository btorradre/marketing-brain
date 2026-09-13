"""Playbook registry: serves the extracted skill playbooks under packages/playbooks.

Loads registry.json from settings.packages_path("playbooks") once and serves whole
playbooks or single sections by id. No vault access, no HOME, no network.
"""
from __future__ import annotations
import json
import os
import threading
from ..core.settings import settings
from ..core.errors import NotFound
from .lint import audit, strip_secrets, summarize

lint = audit

STAGES = (
    "context", "research", "angles", "hooks", "script", "copy", "brief",
    "storyboard", "generation", "voice", "avatar", "editing", "qa", "loop",
)
BUCKETS = ("strategy", "copy", "production", "editing", "brand", "ops", "thirdparty")

_lock = threading.Lock()
_registry: list[dict] | None = None
_by_name: dict[str, dict] = {}


def _root() -> str:
    return settings.packages_path("playbooks")


def _load() -> list[dict]:
    global _registry, _by_name
    with _lock:
        if _registry is None:
            path = os.path.join(_root(), "registry.json")
            if not os.path.exists(path):
                raise NotFound(f"playbook registry missing: run scripts/extract_playbooks.py (looked in {_root()})")
            with open(path, encoding="utf-8") as f:
                _registry = json.load(f)
            _by_name = {p["name"]: p for p in _registry}
        return _registry


def reload() -> list[dict]:
    """Drop the cache (tests, or after re-extraction)."""
    global _registry, _by_name
    with _lock:
        _registry = None
        _by_name = {}
    return _load()


def registry() -> list[dict]:
    """Every playbook record: name, version, stage, bucket, description, files, sections, size, leaks."""
    return [dict(p) for p in _load()]


def get(name: str) -> dict:
    _load()
    try:
        return dict(_by_name[name])
    except KeyError:
        raise NotFound(f"playbook not found: {name}") from None


def stages() -> dict[str, list[str]]:
    """stage -> [playbook names], in pipeline order, only stages that have playbooks."""
    out: dict[str, list[str]] = {s: [] for s in STAGES}
    for p in _load():
        out.setdefault(p["stage"], []).append(p["name"])
    return {s: sorted(names) for s, names in out.items() if names}


def _playbook_path(name: str) -> str:
    p = get(name)
    return os.path.join(_root(), p["name"], "playbook.md")


def read(name: str, section: str | None = None, max_chars: int = 60000) -> str:
    """Whole playbook.md, or one section by id (see registry()[i]["sections"]). Truncated to max_chars."""
    p = get(name)
    path = _playbook_path(name)
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if section is not None:
        sec = next((s for s in p["sections"] if s["id"] == section), None)
        if sec is None:
            ids = ", ".join(s["id"] for s in p["sections"])
            raise NotFound(f"section {section!r} not in playbook {name}; have: {ids}")
        lines = text.splitlines(keepends=True)
        text = "".join(lines[sec["start_line"] - 1 : sec["end_line"]])
    if len(text) > max_chars:
        text = text[:max_chars] + f"\n\n[truncated at {max_chars} chars; request a section id to read the rest]"
    return text


def read_file(name: str, rel_path: str, max_chars: int = 60000) -> str:
    """One of the playbook's module/reference files, by the relative path listed in `files`."""
    p = get(name)
    if rel_path not in p["files"]:
        raise NotFound(f"{rel_path} is not a file of playbook {name}")
    with open(os.path.join(_root(), p["name"], rel_path), encoding="utf-8") as f:
        text = f.read()
    if len(text) > max_chars:
        text = text[:max_chars] + f"\n\n[truncated at {max_chars} chars]"
    return text


__all__ = [
    "registry", "get", "read", "read_file", "stages", "reload", "lint", "audit",
    "strip_secrets", "summarize", "STAGES", "BUCKETS",
]
