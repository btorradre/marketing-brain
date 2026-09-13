import os
import pytest

from adengine import laws
from adengine.core.settings import settings


def test_packages_path_resolves_to_repo_packages():
    assert os.path.isfile(settings.packages_path("laws", "global.json"))


def example_house_laws_with(rule_id: str):
    """The seed example file that carries rule_id (tests stay free of brand literals)."""
    d = settings.packages_path("laws", "examples")
    for name in sorted(os.listdir(d)):
        rules = laws.load_example(name[:-5])
        if any(r["id"] == rule_id for r in rules):
            return rules
    raise AssertionError(f"no example file carries {rule_id}")


def test_global_rules_are_brand_agnostic():
    """No global rule id/law/note names a product; every example file id is absent from global."""
    global_ids = {r["id"] for r in laws.load_global()}
    d = settings.packages_path("laws", "examples")
    example_ids = {r["id"] for name in os.listdir(d) for r in laws.load_example(name[:-5])}
    assert global_ids.isdisjoint(example_ids)
    assert len(os.listdir(d)) >= 4


def test_em_dash_blocked():
    r = laws.gate("This bag holds a laptop — and a charger.")
    assert r["ok"] is False
    ids = [h["id"] for h in r["blockers"]]
    assert "no-em-dash" in ids
    hit = next(h for h in r["blockers"] if h["id"] == "no-em-dash")
    assert hit["match"] == "—" and hit["index"] == text_index("This bag holds a laptop — and a charger.", "—")
    assert set(hit) == {"id", "law", "severity", "match", "index"}


def text_index(s, needle):
    return s.index(needle)


@pytest.mark.parametrize("line", [
    "It's not a tote. It's a system.",
    "It’s not a tote. It’s a system.",        # curly apostrophes
    "This is not just a bag; it's the last one you buy.",
])
def test_not_x_its_y_blocked(line):
    r = laws.gate(line)
    assert not r["ok"]
    assert any(h["id"] == "no-not-x-its-y" for h in r["blockers"])


def test_creator_scope_only_with_speaker():
    line = "I love our bags, they hold everything."
    assert laws.gate(line)["ok"] is True
    assert laws.gate(line, speaker="vo")["ok"] is True
    r = laws.gate(line, speaker="creator")
    assert r["ok"] is False
    assert any(h["id"] == "creator-never-speaks-as-brand" and h["match"] == "our bags" for h in r["blockers"])


def test_brand_rules_only_when_passed():
    line = "The Strato is back in caramel."
    assert laws.gate(line)["ok"] is True                       # examples are never loaded by default
    house = example_house_laws_with("straw-tote-not-strato")
    r = laws.gate(line, brand_rules=house)
    assert r["ok"] is False
    assert [h["id"] for h in r["blockers"]] == ["straw-tote-not-strato"]
    assert r["blockers"][0]["match"] == "Strato"


def test_house_rule_from_brand_record_shape():
    house = [{"id": "no-purple", "law": "never say purple", "severity": "warning",
              "regex": r"\bpurple\b", "flags": ["i"], "note": ""}]
    r = laws.gate("A Purple bag.", brand_rules=house)
    assert r["ok"] is True and [h["id"] for h in r["warnings"]] == ["no-purple"]


def test_warnings_do_not_block():
    r = laws.gate("Clinically proven to fit a laptop. Goes from day to night.")
    assert r["ok"] is True
    ids = {h["id"] for h in r["warnings"]}
    assert {"no-fabricated-citations", "no-transition-angles"} <= ids


def test_clean_text_ok():
    r = laws.gate("This is the Weekender from the brand they keep talking about. It holds three days of clothes.", speaker="creator")
    assert r == {"ok": True, "blockers": [], "warnings": [], "note": laws.JUDGMENT_NOTE}


def test_compile_rules_rejects_bad_severity():
    with pytest.raises(ValueError):
        laws.compile_rules([{"id": "x", "law": "x", "severity": "fatal", "regex": "x"}])


def test_judgment_laws_generalized():
    md = laws.judgment_laws()
    assert md.startswith("# DR OS")
    assert "LAW 12" in md
    assert "house laws" in md and "override this file" in md
    assert "claude-project-instructions.md" not in md
