"""Law gate: mechanical house-law checks over copy, briefs, and plans.

Rules are DATA, never code. The brand-agnostic rules ship with the image at
packages/laws/global.json. Brand-specific rules live on the brand record
(``brand.house_laws``) in the Store and are passed in per call as
``brand_rules``; packages/laws/examples/*.json are seed examples only and are
never loaded by default.

Rule shape (global.json entry, house_laws entry):
    {"id": str, "law": str, "severity": "blocker" | "warning",
     "speaker": "creator" (optional), "regex": str, "flags": ["i", ...],
     "note": str}

A rule with ``speaker`` set only fires when ``gate(..., speaker=...)`` matches.

The judgment laws (golden nugget, swap test, six-month shelf life, ...) cannot
be regexed. ``judgment_laws()`` returns them as markdown for the model to read.
"""
from __future__ import annotations
import json
import os
import re
from functools import lru_cache
from typing import Any

from ..core.settings import settings

Rule = dict[str, Any]

_FLAG_MAP = {
    "i": re.IGNORECASE, "ignorecase": re.IGNORECASE,
    "m": re.MULTILINE, "multiline": re.MULTILINE,
    "s": re.DOTALL, "dotall": re.DOTALL,
    "x": re.VERBOSE, "verbose": re.VERBOSE,
}
_SEVERITIES = ("blocker", "warning")

JUDGMENT_NOTE = ("Heuristic pre-filter only. Judgment laws (golden nugget, swap test, "
                 "six-month shelf life, demonstrate-never-describe) still require the "
                 "judgment laws text: adengine.laws.judgment_laws().")


def _flags(names: list[str] | None) -> int:
    val = 0
    for n in names or []:
        try:
            val |= _FLAG_MAP[str(n).lower()]
        except KeyError:
            raise ValueError(f"unknown regex flag {n!r}") from None
    return val


def _validate(rule: Rule) -> None:
    for k in ("id", "law", "severity", "regex"):
        if k not in rule:
            raise ValueError(f"law rule missing {k!r}: {rule}")
    if rule["severity"] not in _SEVERITIES:
        raise ValueError(f"law rule {rule['id']!r}: severity must be one of {_SEVERITIES}")


def load_global() -> list[Rule]:
    """The brand-agnostic rules from packages/laws/global.json (fresh copy each call)."""
    return [dict(r) for r in _read_global()]


@lru_cache(maxsize=1)
def _read_global() -> tuple[Rule, ...]:
    path = settings.packages_path("laws", "global.json")
    with open(path, encoding="utf-8") as f:
        rules = json.load(f)
    if not isinstance(rules, list):
        raise ValueError(f"{path}: expected a list of rules")
    for r in rules:
        _validate(r)
    return tuple(rules)


def compile_rules(rules: list[Rule]) -> list[Rule]:
    """Attach a compiled pattern to each rule (as ``_pattern``). Input is not mutated."""
    out = []
    for r in rules:
        _validate(r)
        c = dict(r)
        c["_pattern"] = re.compile(r["regex"], _flags(r.get("flags")))
        out.append(c)
    return out


@lru_cache(maxsize=1)
def _compiled_global() -> tuple[Rule, ...]:
    return tuple(compile_rules(list(_read_global())))


def gate(text: str, brand_rules: list[Rule] | None = None, speaker: str | None = None) -> dict:
    """Run the global rules plus the brand's house laws over ``text``.

    Returns {"ok": bool, "blockers": [hit...], "warnings": [hit...], "note": str}
    where each hit is {"id", "law", "severity", "match", "index"}.
    ``ok`` is False when there is at least one blocker.
    """
    rules: list[Rule] = list(_compiled_global())
    if brand_rules:
        rules.extend(compile_rules(list(brand_rules)))

    blockers: list[dict] = []
    warnings: list[dict] = []
    for rule in rules:
        if rule.get("speaker") and rule["speaker"] != speaker:
            continue
        for m in rule["_pattern"].finditer(text):
            hit = {"id": rule["id"], "law": rule["law"], "severity": rule["severity"],
                   "match": m.group(0), "index": m.start()}
            (blockers if rule["severity"] == "blocker" else warnings).append(hit)
    return {"ok": not blockers, "blockers": blockers, "warnings": warnings, "note": JUDGMENT_NOTE}


def judgment_laws() -> str:
    """The judgment laws as markdown (packages/laws/judgment.md)."""
    path = settings.packages_path("laws", "judgment.md")
    with open(path, encoding="utf-8") as f:
        return f.read()


def load_example(brand: str) -> list[Rule]:
    """Seed example house laws for a brand (packages/laws/examples/<brand>.json).

    Only for seeding a brand record or for tests. Never called by the gate itself.
    """
    safe = os.path.basename(brand)
    path = settings.packages_path("laws", "examples", f"{safe}.json")
    with open(path, encoding="utf-8") as f:
        rules = json.load(f)
    for r in rules:
        _validate(r)
    return rules


__all__ = ["load_global", "compile_rules", "gate", "judgment_laws", "load_example", "Rule"]
