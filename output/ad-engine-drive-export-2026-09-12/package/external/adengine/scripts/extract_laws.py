#!/usr/bin/env python3
"""Seed packages/laws/ from the vault, ONCE.

Reads the deterministic law gate (dr-os/lawgate.py, 13 regex rules) and the
judgment laws (direct-response-os/modules/laws.md) and writes:

  packages/laws/global.json          brand-agnostic regex rules
  packages/laws/examples/<brand>.json brand-specific rules as example house-law files
  packages/laws/judgment.md          laws.md verbatim, one vault path generalized

The regex rules are converted from lawgate.py's inline shape
({law, severity, brands, speaker?, regex}) to the packaged shape
({id, law, severity, speaker?, regex, flags, note}). A leading inline "(?i)" is
lifted into flags: ["i"]. Nothing else about the pattern is changed, so straight
and curly apostrophes keep working exactly as in the original.

Usage:
  python scripts/extract_laws.py \
    --lawgate "/path/to/_engine/mcp/dr-os/lawgate.py" \
    --laws-md "/path/to/.claude/skills/direct-response-os/modules/laws.md"
"""
from __future__ import annotations
import argparse, importlib.util, json, os, re, sys
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT_DIR = os.path.join(REPO, "packages", "laws")

DEFAULT_LAWGATE = os.path.expanduser("~/Documents/marketing brain/_engine/mcp/dr-os/lawgate.py")
DEFAULT_LAWS_MD = os.path.expanduser("~/Documents/marketing brain/.claude/skills/direct-response-os/modules/laws.md")

# Stable ids keyed on the law text of the source rule. New rules get a slug id.
ID_MAP = {
    "no-ai-tell-patterns (em dash)": "no-em-dash",
    "no-ai-tell-patterns (not X. It's Y.)": "no-not-x-its-y",
    "no-fabricated-citations (verify or cut)": "no-fabricated-citations",
    "no-transition-angles (1-month shelf life)": "no-transition-angles",
    "creator-never-speaks-as-brand (say 'they', never 'our/we')": "creator-never-speaks-as-brand",
    "product naming: it is the Straw Tote, never 'Strato'": "straw-tote-not-strato",
    "no BNPL on Velantra": "no-bnpl",
    "no competitor comparisons (competitor named)": "no-competitor-names",
    "designer-inflation language: SCAM register banned": "no-scam-register",
    "no origin claims": "no-origin-claims",
    "guarantee is 30 days, NOT 90": "guarantee-30-not-90",
    "motilli guarantee is 90 days, not 30 -- verify the live policy page": "guarantee-90-not-30",
    "Monacolin K is BANNED in Lunessa copy": "no-monacolin",
}

# Human notes carried into the packaged files (the source only has the law title).
NOTES = {
    "no-em-dash": "Em dashes are the loudest AI tell. Use a period, comma, or parentheses. Applies to every customer-facing line.",
    "no-not-x-its-y": "The negation-then-affirmation beat ('It's not X. It's Y.') and every variant. Straight and curly apostrophes both match.",
    "no-fabricated-citations": "Heuristic. Studies, sample sizes, and percentages-of-people must be verified against a source in the brand folder or cut. Warning only because real, sourced citations are allowed.",
    "no-transition-angles": "Day-to-night / seasonal-switch angles carry a one-month shelf life. Judgment law 4 in judgment.md.",
    "creator-never-speaks-as-brand": "Only applies when speaker='creator'. A UGC creator says 'they', 'their', 'this brand'. Never 'our', never 'we made'. Judgment law 8.",
    "straw-tote-not-strato": "Registry key 'strato' is an internal id. The product is the Straw Tote in every output.",
    "no-bnpl": "No buy-now-pay-later mentions on this brand.",
    "no-competitor-names": "No competitor comparisons. Names are warnings so ranked-roundup formats can pass with a human read.",
    "no-scam-register": "Designer-inflation language in the SCAM register is banned; the avatar is not wounded.",
    "no-origin-claims": "No made-in / atelier / national-leather origin claims.",
    "guarantee-30-not-90": "This brand's guarantee is 30 days. A 90-day claim is a false offer.",
    "guarantee-90-not-30": "This brand's guarantee is 90 days. A 30-day claim is stale copy; verify the live policy page.",
    "no-monacolin": "The ingredient name is banned in this brand's copy.",
}

FLAG_MAP = {"i": "IGNORECASE"}


def load_rules(lawgate_path: str) -> list[dict]:
    spec = importlib.util.spec_from_file_location("vault_lawgate", lawgate_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return list(mod.RULES)


def convert(rule: dict) -> dict:
    regex: str = rule["regex"]
    flags: list[str] = []
    if regex.startswith("(?i)"):
        regex = regex[4:]
        flags.append("i")
    rid = ID_MAP.get(rule["law"]) or re.sub(r"[^a-z0-9]+", "-", rule["law"].lower()).strip("-")
    out = OrderedDict()
    out["id"] = rid
    out["law"] = rule["law"]
    out["severity"] = rule["severity"]
    if rule.get("speaker"):
        out["speaker"] = rule["speaker"]
    out["regex"] = regex
    out["flags"] = flags
    out["note"] = NOTES.get(rid, "")
    # sanity: the converted rule must compile with the lifted flags
    re.compile(regex, sum(getattr(re, FLAG_MAP[f]) for f in flags))
    return out


def write_json(path: str, obj) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write("\n")


def extract_judgment(laws_md_path: str) -> str:
    text = open(laws_md_path, encoding="utf-8").read()
    # The one brand-specific vault path line in LAW 1, generalized.
    old = ("3. `brands/<brand>/ops/` for house laws. Velantra's live at "
           "`brands/velantra/ops/claude-project-instructions.md` and they override anything in this OS.")
    new = "3. The brand's house laws (the `house_laws` on the brand record) override this file."
    if old not in text:
        print("WARN: expected LAW 1 path line not found; judgment.md written verbatim", file=sys.stderr)
    return text.replace(old, new)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lawgate", default=DEFAULT_LAWGATE)
    ap.add_argument("--laws-md", default=DEFAULT_LAWS_MD)
    ap.add_argument("--out", default=OUT_DIR)
    args = ap.parse_args()

    rules = load_rules(args.lawgate)
    global_rules, by_brand = [], {}
    for r in rules:
        conv = convert(r)
        if r.get("brands"):
            for b in r["brands"]:
                by_brand.setdefault(b, []).append(conv)
        else:
            global_rules.append(conv)

    write_json(os.path.join(args.out, "global.json"), global_rules)
    for brand, brules in sorted(by_brand.items()):
        write_json(os.path.join(args.out, "examples", f"{brand}.json"), brules)
    with open(os.path.join(args.out, "judgment.md"), "w", encoding="utf-8") as f:
        f.write(extract_judgment(args.laws_md))

    print(f"global: {len(global_rules)} rules")
    for brand, brules in sorted(by_brand.items()):
        print(f"examples/{brand}.json: {len(brules)} rules")
    print("judgment.md written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
