"""Law gate for the dr tools.

Combines the global rules (adengine.laws, loaded from packages/laws) with the
brand's house_laws (rules stored on the brand record). When adengine.laws is
not importable yet, a small built-in set of the global mechanical rules keeps
the gate functional so saves are still protected; the response says which
engine ran.

Rule shape (house_laws and the fallback share it):
  {"law": str, "severity": "blocker"|"warning", "regex": str, "speaker": str|None}
"""
from __future__ import annotations

import re
from typing import Any

from .deps import brand_by_slug, optional_module

# Global, brand-agnostic mechanical laws. Brand-specific rules never live here
# (they are data on the brand record / packages/laws).
BUILTIN_RULES: list[dict[str, Any]] = [
    {"law": "no-ai-tell-patterns (em dash)", "severity": "blocker",
     "regex": "—"},
    {"law": "no-ai-tell-patterns (not X. It's Y.)", "severity": "blocker",
     "regex": r"(?i)\b(?:is|it['’]?s)?\s?not\s+(?:just\s+|only\s+|about\s+)?(?:a|an|the)?\s?[^.!?\n]{2,40}[.;]\s*(?:it|this|that|they)(?:['’]s|['’]re|\s+is|\s+are)\b"},
    {"law": "no-fabricated-citations (verify or cut)", "severity": "warning",
     "regex": r"(?i)(?:clinical(?:ly)?\s+(?:proven|stud(?:y|ies))|researchers?\s+(?:found|at)\b|\bn\s*=\s*\d+|\b\d{1,3}%\s+of\s+(?:women|men|users|participants|patients|customers))"},
    {"law": "no-transition-angles (1-month shelf life)", "severity": "warning",
     "regex": r"(?i)\b(?:day[-\s]to[-\s]night|desk[-\s]to[-\s]dinner|summer[-\s]to[-\s]fall|beach[-\s]to[-\s]brunch|seasonal\s+switch)\b"},
    {"law": "creator-never-speaks-as-brand (say 'they', never 'our/we')", "severity": "blocker",
     "speaker": "creator",
     "regex": r"(?i)\b(?:our\s+(?:bags?|brand|products?|company|team|customers)|we\s+(?:made|designed|built|created|launched|developed))\b|\bour\s+(?-i:[A-Z][a-z]+)\b"},
]

JUDGMENT_NOTE = ("Heuristic pre-filter only. Judgment laws (golden nugget, swap test, "
                 "six-month shelf life, demonstrate-never-describe) still require the "
                 "laws playbook: get_playbook('laws').")


_FLAGS = {"i": re.IGNORECASE, "ignorecase": re.IGNORECASE, "m": re.MULTILINE, "multiline": re.MULTILINE,
          "s": re.DOTALL, "dotall": re.DOTALL, "x": re.VERBOSE, "verbose": re.VERBOSE}


def normalize_rules(rules: Any) -> list[dict[str, Any]]:
    """Coerce house_laws into the adengine.laws rule shape: id, law, severity, regex, flags.
    Rules without a regex are dropped; missing id/law/severity get sensible defaults."""
    out: list[dict[str, Any]] = []
    for i, rule in enumerate(rules or []):
        if not isinstance(rule, dict) or not rule.get("regex"):
            continue
        law = rule.get("law") or rule.get("id") or f"house-law-{i + 1}"
        rid = rule.get("id") or re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", law.lower())).strip("-") or f"house-law-{i + 1}"
        sev = rule.get("severity") if rule.get("severity") in ("blocker", "warning") else "warning"
        norm = {**rule, "id": rid, "law": law, "severity": sev, "regex": rule["regex"],
                "flags": list(rule.get("flags") or [])}
        out.append(norm)
    return out


def apply_rules(rules: list[dict[str, Any]], text: str, speaker: str | None = None) -> dict[str, Any]:
    """Run a rule list over text. Pure; no store access."""
    blockers, warnings = [], []
    for rule in normalize_rules(rules):
        if rule.get("speaker") and speaker != rule["speaker"]:
            continue
        flags = 0
        for f in rule.get("flags") or []:
            flags |= _FLAGS.get(str(f).lower(), 0)
        try:
            pattern = re.compile(rule["regex"], flags)
        except re.error as exc:
            warnings.append({"law": rule.get("law", "?"), "match": "", "excerpt": f"invalid regex: {exc}"})
            continue
        for m in pattern.finditer(text or ""):
            start, end = max(0, m.start() - 40), min(len(text), m.end() + 40)
            hit = {"id": rule["id"], "law": rule["law"], "severity": rule["severity"], "match": m.group(0),
                   "index": m.start(), "excerpt": text[start:end].replace("\n", " ")}
            (blockers if rule.get("severity", "warning") == "blocker" else warnings).append(hit)
    return {"ok": not blockers, "blockers": blockers, "warnings": warnings}


def check(text: str, brand_slug: str | None = None, speaker: str | None = None) -> dict[str, Any]:
    """Global rules + the brand's house_laws. Never raises on a missing laws package."""
    brand_rules: list[dict[str, Any]] = []
    brand_id = None
    if brand_slug:
        brand = brand_by_slug(brand_slug)
        brand_id = brand["id"]
        brand_rules = normalize_rules(brand.get("house_laws"))

    laws = optional_module("adengine.laws")
    if laws is not None and hasattr(laws, "gate"):
        result = laws.gate(text, brand_rules=brand_rules or None, speaker=speaker)
        result = dict(result or {})
        result.setdefault("blockers", [])
        result.setdefault("warnings", [])
        result["ok"] = bool(result.get("ok", not result["blockers"]))
        result["engine"] = "adengine.laws"
    else:
        result = apply_rules(BUILTIN_RULES + brand_rules, text, speaker=speaker)
        result["engine"] = "builtin-fallback"
        result["engine_note"] = "adengine.laws not importable; built-in global rules + brand house_laws only."

    result["clean"] = not result["blockers"] and not result["warnings"]
    result["brand"] = brand_slug
    result["brand_id"] = brand_id
    result["speaker"] = speaker
    result["note"] = JUDGMENT_NOTE
    return result
