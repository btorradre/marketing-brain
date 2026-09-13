"""Concept registry: the loop-closer, as Store records (no spreadsheet).

A concept that is agreed is recorded BEFORE production starts. The minted
asset_code follows the naming law {BRAND}-{PRODUCT}-{CONCEPT}-{TYPE}{NN}
(e.g. ACM-TOTE-FOUNDERSTORY-VID01) and NN increments per
(brand, product, concept, type) inside the workspace. Ad names in the ad
account must equal the asset_code so the 30-day verdict has somewhere to land.
"""
from __future__ import annotations

from adengine.core.auth import require_write

import datetime
import re
from typing import Any

from adengine.core.errors import NotFound

from .deps import brand_by_slug, store, ws

FORMAT_CODES = {"video": "VID", "image": "IMG", "dynamic": "DYN"}
CONCEPT_TYPES = ("net-new", "iteration")


def code(s: str, n: int) -> str:
    return re.sub(r"[^A-Z0-9]", "", (s or "").upper())[:n] or "X"


def _product_code(brand: dict[str, Any], product: str) -> tuple[str, str | None]:
    """Product code from the product record's `code` when it exists, else derived."""
    slug = re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", product.lower())).strip("-")
    rows = store().find("product", ws(), brand_id=brand["id"], slug=slug)
    if rows:
        rec = rows[0]
        return (rec.get("code") or code(rec.get("name") or product, 8)), rec["id"]
    return code(product, 8), None


@require_write
def push_concept(brand_slug: str, product: str, concept: str, angle: str, thesis: str,
                 format: str = "video", type: str = "net-new",
                 source: str | None = None, notes: str | None = None) -> dict[str, Any]:
    if format not in FORMAT_CODES:
        return {"error": f"format must be one of {sorted(FORMAT_CODES)}"}
    if type not in CONCEPT_TYPES:
        return {"error": f"type must be one of {list(CONCEPT_TYPES)}"}
    brand = brand_by_slug(brand_slug)
    brand_code = brand.get("code") or code(brand.get("slug") or brand_slug, 3)
    product_code, product_id = _product_code(brand, product)
    concept_code = code(concept, 14)
    type_code = FORMAT_CODES[format]
    prefix = f"{brand_code}-{product_code}-{concept_code}-{type_code}"

    siblings = store().find("concept", ws(), brand_id=brand["id"])
    nn = 0
    for rec in siblings:
        m = re.fullmatch(re.escape(prefix) + r"(\d+)", rec.get("asset_code") or "")
        if m:
            nn = max(nn, int(m.group(1)))
    asset_code = f"{prefix}{nn + 1:02d}"

    fields = {"date": datetime.date.today().isoformat(), "product": product, "product_id": product_id,
              "product_code": product_code, "concept": concept, "concept_code": concept_code,
              "angle": angle, "thesis": thesis, "format": format, "type": type,
              "source": source or "adengine-dr", "status": "idea", "notes": notes or "",
              "sequence": nn + 1}
    rec = store().create("concept", ws(), "cpt", brand_id=brand["id"], asset_code=asset_code, fields=fields)
    return {"ok": True, "concept_id": rec["id"], "asset_code": asset_code, "fields": fields,
            "next": "Write this asset_code into the angle record's tested_assets "
                    "(read_artifact / save_artifact on angle-bank) and name the ad exactly this."}


def list_concepts(brand_slug: str) -> dict[str, Any]:
    brand = brand_by_slug(brand_slug)
    rows = store().find("concept", ws(), brand_id=brand["id"])
    return {"brand": brand_slug,
            "concepts": [{"id": r["id"], "asset_code": r.get("asset_code"), **(r.get("fields") or {})}
                         for r in rows]}
