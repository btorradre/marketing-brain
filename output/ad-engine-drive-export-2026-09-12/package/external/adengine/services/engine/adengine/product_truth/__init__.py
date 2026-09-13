"""Product truth as data.

A product_truth record is the ``truth`` dict on a ``product`` row (see Store).
It carries the verbatim identity and mechanism blocks that today's skills paste
into every generation prompt, plus colorways, banned terms, claims, engine
notes and reference assets. ``schema.json`` next to this file is the contract.

Seed records extracted from the vault skills live at
packages/schema/seed/product_truth/<brand>-<slug>.json (scripts/extract_product_truth.py).
"""
from __future__ import annotations
import json
import os
from functools import lru_cache
from typing import Any

from ..core.settings import settings

Record = dict[str, Any]


class ProductTruthError(ValueError):
    """The record does not match schema.json. Message names the failing path."""


_HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = os.path.join(_HERE, "schema.json")


@lru_cache(maxsize=1)
def schema() -> dict:
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        return json.load(f)


@lru_cache(maxsize=1)
def _validator():
    import jsonschema
    return jsonschema.Draft202012Validator(schema())


def validate(record: Record) -> None:
    """Raise ProductTruthError (a ValueError) if the record does not match schema.json."""
    errors = sorted(_validator().iter_errors(record), key=lambda e: list(e.path))
    if errors:
        e = errors[0]
        where = "/".join(str(p) for p in e.path) or "<root>"
        raise ProductTruthError(f"product_truth invalid at {where}: {e.message}")


def render_blocks(record: Record, colorway: str | None = None) -> str:
    """The prompt-ready product truth text.

    Identity block verbatim, then the mechanism block verbatim (when present),
    then any extra verbatim blocks, then banned terms and colorways. The two
    main blocks are emitted byte-for-byte as stored; only a leading label line
    is added above each. If ``colorway`` names one of the record's colorways,
    a "COLORWAY:" line is appended so the caller can resolve [a | b] brackets.
    """
    parts: list[str] = []
    parts.append("IDENTITY BLOCK (paste verbatim):\n" + record["identity_block"])
    if record.get("mechanism_block"):
        parts.append("OPENING MECHANISM BLOCK (paste verbatim):\n" + record["mechanism_block"])
    for blk in record.get("extra_blocks") or []:
        when = f" ({blk['when']})" if blk.get("when") else ""
        parts.append(f"{blk['name'].upper()}{when}:\n{blk['text']}")

    banned = record.get("banned_terms") or []
    if banned:
        lines = [f'- never write "{b["term"]}"' + (f": {b['reason']}" if b.get("reason") else "") for b in banned]
        parts.append("BANNED TERMS:\n" + "\n".join(lines))

    cws = record.get("colorways") or []
    if cws:
        lines = []
        for c in cws:
            desc = c.get("description") or ""
            tag = " (hero)" if c.get("hero") else ""
            hx = f" {c['hex']}" if c.get("hex") else ""
            lines.append(f"- {c['name']}{tag}{hx}" + (f": {desc}" if desc else ""))
        parts.append("COLORWAYS:\n" + "\n".join(lines))
        if colorway:
            match = next((c for c in cws if c["name"].lower() == colorway.lower()), None)
            if match:
                parts.append(f"COLORWAY: {match['name']}" + (f": {match['description']}" if match.get("description") else ""))
    return "\n\n".join(parts)


def seed_dir() -> str:
    return settings.packages_path("schema", "seed", "product_truth")


def load_examples() -> list[Record]:
    """All seed records under packages/schema/seed/product_truth/, validated, sorted by filename."""
    d = seed_dir()
    if not os.path.isdir(d):
        return []
    out = []
    for name in sorted(os.listdir(d)):
        if not name.endswith(".json"):
            continue
        with open(os.path.join(d, name), encoding="utf-8") as f:
            rec = json.load(f)
        validate(rec)
        out.append(rec)
    return out


__all__ = ["ProductTruthError", "schema", "validate", "render_blocks", "load_examples", "seed_dir", "SCHEMA_PATH", "Record"]
