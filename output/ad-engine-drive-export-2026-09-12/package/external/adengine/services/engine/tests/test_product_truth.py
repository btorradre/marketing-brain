import copy
import json
import os

import pytest

from adengine import product_truth as pt


@pytest.fixture(scope="module")
def seeds():
    recs = pt.load_examples()
    assert recs, f"no seed records under {pt.seed_dir()}"
    return {r["slug"]: r for r in recs}   # keyed by product slug; no brand literals in Python


def test_seed_records_validate(seeds):
    assert len(seeds) >= 8
    for key, rec in seeds.items():
        pt.validate(rec)                      # raises on failure
        assert rec["version"] == 1
        assert rec["extracted_from"]["path"].endswith("SKILL.md")


def test_seed_filenames_match_records():
    d = pt.seed_dir()
    for name in os.listdir(d):
        rec = json.load(open(os.path.join(d, name), encoding="utf-8"))
        assert name == f"{rec['brand_slug']}-{rec['slug']}.json"


def test_render_blocks_contains_identity_verbatim(seeds):
    for rec in seeds.values():
        out = pt.render_blocks(rec)
        assert rec["identity_block"] in out
        assert out.startswith("IDENTITY BLOCK (paste verbatim):\n" + rec["identity_block"])
        if rec["mechanism_block"]:
            assert "OPENING MECHANISM BLOCK (paste verbatim):\n" + rec["mechanism_block"] in out
            assert out.index(rec["identity_block"]) < out.index(rec["mechanism_block"])
        for b in rec["banned_terms"]:
            assert f'never write "{b["term"]}"' in out
        for c in rec["colorways"]:
            assert f"- {c['name']}" in out


def test_weekender_seed_shape(seeds):
    w = seeds["weekender"]
    assert w["identity_block"].startswith("a structured two tone weekend bag")
    assert w["mechanism_block"].startswith("Open bag construction:")
    assert w["dimensions"]["width_in"] == 18.0
    assert {c["name"] for c in w["colorways"]} == {"Light Chocolate", "Army Green", "Dark Chocolate"}
    assert any(b["term"] == "Birkin" for b in w["banned_terms"])
    assert any(a["role"] == "master_seed" for a in w["reference_assets"])
    assert all(a["asset_id"] is None for a in w["reference_assets"])
    assert any(n["engine"].lower().startswith("seedance") for n in w["engine_notes"])


def test_vivienne_mechanism_is_the_opening_block(seeds):
    v = seeds["vivienne"]
    assert v["mechanism_block"].startswith("A single one-piece leather flap")
    assert any(c["hex"] == "#4a2c1a" and c.get("hero") for c in v["colorways"])
    assert {b["name"] for b in v["extra_blocks"]} >= {"closure hardware", "material", "photoreal", "scale anchor"}


def test_render_blocks_colorway_line(seeds):
    w = seeds["weekender"]
    out = pt.render_blocks(w, colorway="army green")
    assert out.rstrip().splitlines()[-1].startswith("COLORWAY: Army Green")


def test_validate_rejects_bad_records(seeds):
    good = next(iter(seeds.values()))
    bad = copy.deepcopy(good); bad["slug"] = "Not A Slug"
    with pytest.raises(ValueError):
        pt.validate(bad)
    bad = copy.deepcopy(good); del bad["identity_block"]
    with pytest.raises(ValueError):
        pt.validate(bad)
    bad = copy.deepcopy(good); bad["reference_assets"] = [{"role": "hero", "asset_id": None, "source_path_original": "x"}]
    with pytest.raises(ValueError):
        pt.validate(bad)
    bad = copy.deepcopy(good); bad["unknown_field"] = 1
    with pytest.raises(ValueError):
        pt.validate(bad)


def test_minimal_record_validates_and_renders():
    rec = {"name": "Thing", "slug": "thing", "brand_slug": "acme", "category": "widget",
           "identity_block": "a small red widget", "mechanism_block": None, "colorways": [],
           "dimensions": {}, "materials": [], "banned_terms": [], "required_phrases": [], "claims": [],
           "engine_notes": [], "reference_assets": [], "qa_checklist": [], "version": 1,
           "extracted_from": {"path": "manual"}}
    pt.validate(rec)
    assert pt.render_blocks(rec) == "IDENTITY BLOCK (paste verbatim):\na small red widget"
