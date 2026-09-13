"""Shared accessors for the dr tools: store, workspace, brand lookup, and lazy
imports of the sibling packages (laws, playbooks, product_truth) that other
agents build concurrently. Every sibling import is optional: callers get a
clear error dict instead of an ImportError when a package is not there yet."""
from __future__ import annotations

import importlib
from types import ModuleType
from typing import Any

from adengine.core import get_store, current_workspace
from adengine.core.store import Store, Record

# Collections the Store documents; used by status() for counts.
COLLECTIONS = [
    "brand", "product", "artifact", "reference", "board", "approval", "job",
    "asset", "cost", "credential", "concept", "timeline", "style",
]

SIBLING_PACKAGES = ["adengine.laws", "adengine.playbooks", "adengine.product_truth",
                    "adengine.gen", "adengine.engines", "adengine.workers"]


def store() -> Store:
    return get_store()


def ws() -> str:
    return current_workspace()


def brand_by_slug(brand_slug: str) -> Record:
    """Brand record for this workspace, or NotFound."""
    return store().one("brand", ws(), slug=brand_slug)


def product_by_slug(brand: Record, product_slug: str) -> Record:
    return store().one("product", ws(), brand_id=brand["id"], slug=product_slug)


def optional_module(name: str) -> ModuleType | None:
    """Import a sibling package lazily; None if it is not importable yet."""
    try:
        return importlib.import_module(name)
    except Exception:  # noqa: BLE001 - a half-built sibling must never take this server down
        return None


def unavailable(package: str, extra: dict[str, Any] | None = None) -> dict[str, Any]:
    out = {"error": f"{package} is not available in this build",
           "hint": f"{package} is built separately; retry once it ships in the image."}
    if extra:
        out.update(extra)
    return out
