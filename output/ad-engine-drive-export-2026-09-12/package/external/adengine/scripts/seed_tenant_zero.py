"""Seed tenant zero (our own brands) into a workspace. The ONLY vault-aware runtime script.

Reads: packages/laws/examples/<brand>.json (house laws), packages/schema/seed/product_truth/*.json,
and optionally the vault brand folders for briefs + house-law markdown.
Writes: brand + product records into the Store for ADENGINE_DEV_WORKSPACE.

  ADENGINE_DATA_DIR=/tmp/adengine ADENGINE_DEV_WORKSPACE=ws_bto \
  ADENGINE_VAULT="/path/to/marketing brain" python scripts/seed_tenant_zero.py
"""
from __future__ import annotations
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "services", "engine"))
os.environ.setdefault("ADENGINE_PACKAGES_DIR", os.path.join(ROOT, "packages"))
from adengine.core import get_store, current_workspace
from adengine.product_truth import validate

BRANDS = {
    "velantra": {"name": "Velantra", "code": "VEL"},
    "motilli": {"name": "Motilli", "code": "MOT"},
    "lunessa": {"name": "Lunessa", "code": "LUN"},
    "wend": {"name": "Wend", "code": "WND"},
}
VAULT = os.environ.get("ADENGINE_VAULT")


def read(path, cap=20000):
    try:
        with open(path) as f:
            return f.read()[:cap]
    except OSError:
        return None


def main():
    store = get_store(); ws = current_workspace()
    laws_dir = os.path.join(ROOT, "packages", "laws", "examples")
    pt_dir = os.path.join(ROOT, "packages", "schema", "seed", "product_truth")
    brand_ids = {}
    for slug, meta in BRANDS.items():
        rules = []
        p = os.path.join(laws_dir, f"{slug}.json")
        if os.path.exists(p):
            with open(p) as f:
                rules = json.load(f)
                if isinstance(rules, dict):
                    rules = rules.get("rules", [])
        brief, house_md = {}, None
        if VAULT:
            bdir = os.path.join(VAULT, "brands", slug)
            house_md = read(os.path.join(bdir, "ops", "claude-project-instructions.md"))
            b = read(os.path.join(bdir, "00-brief.md"))
            if b:
                brief = {"markdown": b}
        existing = store.find("brand", ws, slug=slug)
        fields = dict(slug=slug, name=meta["name"], code=meta["code"], brief=brief,
                      house_laws=rules, house_laws_markdown=house_md)
        rec = store.update("brand", ws, existing[0]["id"], **fields) if existing else store.create("brand", ws, "brand", **fields)
        brand_ids[slug] = rec["id"]
        print(f"brand {slug}: {len(rules)} house rules, house_md={'yes' if house_md else 'no'}, brief={'yes' if brief else 'no'}")
    n = 0
    for name in sorted(os.listdir(pt_dir)):
        if not name.endswith(".json"):
            continue
        with open(os.path.join(pt_dir, name)) as f:
            truth = json.load(f)
        validate(truth)
        bslug = truth["brand_slug"]
        if bslug not in brand_ids:
            print(f"skip {name}: brand {bslug} not seeded"); continue
        existing = store.find("product", ws, brand_id=brand_ids[bslug], slug=truth["slug"])
        fields = dict(brand_id=brand_ids[bslug], brand_slug=bslug, slug=truth["slug"], name=truth["name"], truth=truth)
        if existing:
            store.update("product", ws, existing[0]["id"], **fields)
        else:
            store.create("product", ws, "prod", **fields)
        n += 1
        print(f"product {bslug}/{truth['slug']}: identity {len(truth.get('identity_block') or '')} chars, "
              f"{len(truth.get('colorways') or [])} colorways, {len(truth.get('banned_terms') or [])} banned")
    print(f"seeded {len(brand_ids)} brands, {n} products into workspace {ws}")


if __name__ == "__main__":
    main()
