"""Deterministic law-gate — a heuristic pre-filter over copy/briefs/plans.

This catches the mechanical violations of the house laws (AI-tell patterns,
banned terms, brand-truth slips) before an artifact lands. It is NOT a
substitute for reading the laws playbook — judgment-level laws (golden
nugget, swap test, six-month shelf life) can only be enforced by the model.

Severity: "blocker" stops dr_save_artifact (unless force=True); "warning"
is surfaced but does not block.
"""

import re

RULES = [
    # -- global AI-tell / copy laws ------------------------------------
    {"law": "no-ai-tell-patterns (em dash)", "severity": "blocker", "brands": None,
     "regex": r"—"},
    {"law": "no-ai-tell-patterns (not X. It's Y.)", "severity": "blocker", "brands": None,
     "regex": r"(?i)\b(?:is|it['’]?s)?\s?not\s+(?:just\s+|only\s+|about\s+)?(?:a|an|the)?\s?[^.!?\n]{2,40}[.;]\s*(?:it|this|that|they)(?:['’]s|['’]re|\s+is|\s+are)\b"},
    {"law": "no-fabricated-citations (verify or cut)", "severity": "warning", "brands": None,
     "regex": r"(?i)(?:clinical(?:ly)?\s+(?:proven|stud(?:y|ies))|researchers?\s+(?:found|at)\b|\bn\s*=\s*\d+|\b\d{1,3}%\s+of\s+(?:women|men|users|participants|patients|customers))"},
    {"law": "no-transition-angles (1-month shelf life)", "severity": "warning", "brands": None,
     "regex": r"(?i)\b(?:day[-\s]to[-\s]night|desk[-\s]to[-\s]dinner|summer[-\s]to[-\s]fall|beach[-\s]to[-\s]brunch|seasonal\s+switch)\b"},

    # -- creator scripts (speaker="creator") ---------------------------
    {"law": "creator-never-speaks-as-brand (say 'they', never 'our/we')", "severity": "blocker",
     "brands": None, "speaker": "creator",
     "regex": r"(?i)\b(?:our\s+(?:bags?|brand|products?|company|team|customers)|we\s+(?:made|designed|built|created|launched|developed))\b|\bour\s+(?-i:[A-Z][a-z]+)\b"},

    # -- velantra ------------------------------------------------------
    {"law": "product naming: it is the Straw Tote, never 'Strato'", "severity": "blocker",
     "brands": ["velantra"], "regex": r"\bStrato\b"},
    {"law": "no BNPL on Velantra", "severity": "blocker", "brands": ["velantra"],
     "regex": r"(?i)\b(?:klarna|afterpay|affirm|shop\s?pay\s+installments|\d\s+interest[-\s]free\s+payments)\b"},
    {"law": "no competitor comparisons (competitor named)", "severity": "warning", "brands": ["velantra"],
     "regex": r"(?i)\b(?:quince|cuyana|longchamp|goyard|l\.?\s?l\.?\s?bean|bogg\s?bag)\b"},
    {"law": "designer-inflation language: SCAM register banned", "severity": "warning", "brands": ["velantra"],
     "regex": r"(?i)\b(?:scam(?:med|ming)?|rip[-\s]?off|ripping\s+you\s+off)\b"},
    {"law": "no origin claims", "severity": "warning", "brands": ["velantra"],
     "regex": r"(?i)\b(?:made\s+in\s+(?:italy|france)|italian\s+leather|french\s+atelier)\b"},

    # -- motilli / wend ------------------------------------------------
    {"law": "guarantee is 30 days, NOT 90", "severity": "blocker", "brands": ["wend"],
     "regex": r"(?i)\b90[-\s]?day\b"},
    # Motilli's guarantee was extended to a real 90 days on 2026-08-17 and re-verified
    # live on getmotilli.com/policies/refund-policy 2026-08-24. 30-day is now the stale one.
    {"law": "motilli guarantee is 90 days, not 30 -- verify the live policy page",
     "severity": "warning", "brands": ["motilli"],
     "regex": r"(?i)\b30[-\s]?day\b[^.\n]{0,30}\b(?:guarantee|money[-\s]?back|refund)\b"},

    # -- lunessa -------------------------------------------------------
    {"law": "Monacolin K is BANNED in Lunessa copy", "severity": "blocker", "brands": ["lunessa"],
     "regex": r"(?i)monacolin"},
]


# -- laws-as-data -------------------------------------------------------
# When _engine/laws (symlink to adengine packages/laws) exists, its JSON files
# are the single source of truth and the inline RULES above are the fallback.
import json as _json
from pathlib import Path as _Path

_LAWS_DIR = _Path(__file__).resolve().parents[2] / "laws"


def _rules_from_data() -> list[dict] | None:
    if not (_LAWS_DIR / "global.json").is_file():
        return None
    out = []

    def _add(path, brands):
        try:
            for r in _json.loads(path.read_text()):
                if not r.get("regex"):
                    continue
                flags = "(?i)" if "i" in (r.get("flags") or []) else ""
                rule = {"law": r.get("law") or r.get("id"), "severity": r.get("severity", "warning"),
                        "brands": brands, "regex": flags + r["regex"], "id": r.get("id"),
                        "scope": r.get("scope", "all")}
                if r.get("speaker"):
                    rule["speaker"] = r["speaker"]
                try:
                    re.compile(rule["regex"])
                except re.error:
                    continue
                out.append(rule)
        except (OSError, ValueError):
            pass

    _add(_LAWS_DIR / "global.json", None)
    for bp in sorted((_LAWS_DIR / "examples").glob("*.json")) if (_LAWS_DIR / "examples").is_dir() else []:
        _add(bp, [bp.stem])
    return out or None


_DATA_RULES = _rules_from_data()
if _DATA_RULES:
    RULES = _DATA_RULES


def check(text: str, brand: str | None = None, speaker: str | None = None) -> dict:
    blockers, warnings = [], []
    for rule in RULES:
        if rule.get("brands") and (brand or "").lower() not in rule["brands"]:
            continue
        if rule.get("speaker") and speaker != rule["speaker"]:
            continue
        for m in re.finditer(rule["regex"], text):
            start, end = max(0, m.start() - 40), min(len(text), m.end() + 40)
            hit = {"law": rule["law"],
                   "match": m.group(0),
                   "excerpt": text[start:end].replace("\n", " ")}
            (blockers if rule["severity"] == "blocker" else warnings).append(hit)

    return {"clean": not blockers and not warnings,
            "blockers": blockers,
            "warnings": warnings,
            "note": ("Heuristic pre-filter only. Judgment laws (golden nugget, swap test, "
                     "six-month shelf life, demonstrate-never-describe) still require the "
                     "laws playbook: dr_get_playbook('laws').")}
