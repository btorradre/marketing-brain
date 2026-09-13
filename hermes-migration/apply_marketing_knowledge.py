#!/usr/bin/env python3
"""Install the shared BTO marketing doctrine into Hermes and Paperclip prompts.

This script is deliberately additive and idempotent. It does not change model
providers or credentials; the model cutover is a separate, authenticated step.
"""

from __future__ import annotations

import json
from pathlib import Path
import re
import urllib.parse
import urllib.request

import yaml


SHARED_DIR = "/opt/vault/agents/hermes/shared-skills"
SHARED_SKILL = f"{SHARED_DIR}/dtc-marketing-operating-system/SKILL.md"
COMPANY_ID = "9341b832-0f97-4c3f-9171-fdfb899c2464"
API = "http://127.0.0.1:3100/api"

PROFILES = [
    Path("/root/.hermes"),
    Path("/root/.hermes-ceo"),
    Path("/root/.hermes-cfo"),
    Path("/root/.hermes-coo"),
    Path("/root/.hermes-designer"),
    Path("/root/.hermes-professor"),
    Path("/root/.hermes-strategist"),
    Path("/root/.hermes-cqm"),
    Path("/root/.hermes-creative"),
    Path("/root/.hermes-cro"),
    Path("/root/.hermes-mediabuyer"),
]

LEGACY_SKILLS = [
    "advertorial-listicle-funnel-pairing",
    "ancient-knowledge-advertorial-archetype",
    "dtc-avatar-research-synthesis",
    "dtc-listicle-advertorial",
    "dtc-mechanism-copy-language",
    "dtc-vsl-length-ladder",
    "forbidden-knowledge-advertorial",
    "long-form-belief-cascade-framework",
    "motilli-brief-pipeline",
    "native-avatar-advertorial",
    "vsl-copy-scoring-rubric",
]

SOUL_START = "<!-- BTO-MARKETING-OS:START -->"
SOUL_END = "<!-- BTO-MARKETING-OS:END -->"
SOUL_BLOCK = f"""{SOUL_START}
## Current BTO Marketing Authority

For any marketing, copywriting, creative strategy, customer research, funnel,
positioning, CRO, offer, or paid-media task, use the
`dtc-marketing-operating-system` skill at `{SHARED_SKILL}` as the governing
doctrine. Read the current brand master brief, product truth, customer evidence,
and latest applicable SOP before producing final work.

Core behavior:

- Begin inside the customer's present understanding. Marketing is not forced
  belief shifting. Confirm held beliefs, clarify uncertainty, bridge carefully
  when evidence supports it, and omit beliefs that do not need work.
- Use the customer's words and the simplest accurate causal mechanism. Prefer
  familiar conditions, physical verbs, and a short cause-and-effect chain.
- Establish credible solution criteria before asking the customer to judge the
  product. Product reveal timing is flexible, not a fixed late-reveal rule.
- Let awareness determine education, sophistication determine mechanism and
  objection burden, and belief distance determine length.
- Preserve psychological continuity from ad to bridge to PDP. Diagnose the
  first measurable bottleneck before rewriting the whole funnel.
- Never invent or disguise people, proof, studies, statistics, reviews,
  publications, urgency, scarcity, or product facts.

Current product truth and evidence outrank brand briefs; current brand briefs
outrank format SOPs; current SOPs and this operating system outrank classic
frameworks, swipes, winners, and legacy Hermes skills.
{SOUL_END}"""

LEGACY_START = "<!-- BTO-CURRENT-AUTHORITY:START -->"
LEGACY_END = "<!-- BTO-CURRENT-AUTHORITY:END -->"
LEGACY_NOTICE = f"""{LEGACY_START}
> **Current authority notice:** This is a legacy specialist skill. Before using
> it, load `dtc-marketing-operating-system` from `{SHARED_SKILL}`. The current
> operating system wins on conflict. Treat fixed belief cascades, fixed story
> shares, automatic advertorial selection, mandatory late product reveals,
> named mechanisms, narrators, and word counts as optional hypotheses—not laws.
> Never invent people, proof, claims, statistics, publications, urgency, or
> scarcity to satisfy an old template.
{LEGACY_END}"""

PAPERCLIP_START = "<!-- BTO-MARKETING-OS:START -->"
PAPERCLIP_END = "<!-- BTO-MARKETING-OS:END -->"
PAPERCLIP_BLOCK = f"""{PAPERCLIP_START}
## Governing Marketing Doctrine

For every marketing, copy, creative, research, positioning, CRO, funnel, offer,
or paid-media decision, load and follow `dtc-marketing-operating-system` at
`{SHARED_SKILL}`. Also read the current brand brief, product truth, customer
evidence, and latest applicable SOP under `/opt/vault/marketing-brain/`.

Do not mechanically force belief shifts. Start with the customer's existing
language and understanding; confirm, clarify, bridge carefully, or omit. Explain
mechanisms as a simple, accurate cause-and-effect chain the customer could repeat.
Set solution criteria before product evaluation, keep funnel stages congruent,
and diagnose the first measurable bottleneck. Current product truth and evidence
override every template, swipe, historical winner, and legacy skill. Never invent
claims, people, proof, reviews, studies, statistics, publications, urgency, or
scarcity.
{PAPERCLIP_END}"""


def replace_marked(text: str, start: str, end: str, block: str) -> str:
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    if pattern.search(text):
        return pattern.sub(block, text)
    return text.rstrip() + "\n\n" + block + "\n"


def add_external_dir(config_path: Path) -> bool:
    text = config_path.read_text()
    if SHARED_DIR in text:
        return False

    # All audited profiles currently use this exact empty-list form. Keep the
    # rest of the config byte-for-byte stable, including comments and secrets.
    old = "  external_dirs: []"
    new = f"  external_dirs:\n  - {SHARED_DIR}"
    if text.count(old) != 1:
        raise RuntimeError(f"Unexpected skills.external_dirs structure: {config_path}")
    updated = text.replace(old, new, 1)
    yaml.safe_load(updated)
    config_path.write_text(updated)
    return True


def insert_after_frontmatter(text: str, notice: str) -> str:
    if LEGACY_START in text:
        return replace_marked(text, LEGACY_START, LEGACY_END, notice)
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end < 0:
            raise RuntimeError("Unclosed Markdown frontmatter")
        pos = end + len("\n---\n")
        return text[:pos] + "\n" + notice + "\n\n" + text[pos:].lstrip("\n")
    return notice + "\n\n" + text


def api_json(method: str, path: str, body: dict | None = None):
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(
        API + path,
        data=data,
        method=method,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)


def update_paperclip_instructions() -> tuple[int, int]:
    agents = api_json("GET", f"/companies/{COMPANY_ID}/agents")
    changed = 0
    skipped = 0
    for agent in agents:
        agent_id = agent["id"]
        bundle = api_json("GET", f"/agents/{agent_id}/instructions-bundle")
        if not bundle.get("editable"):
            skipped += 1
            continue
        entry = bundle.get("entryFile") or "AGENTS.md"
        query = urllib.parse.quote(entry, safe="")
        file_data = api_json(
            "GET", f"/agents/{agent_id}/instructions-bundle/file?path={query}"
        )
        old = file_data.get("content", "")
        new = replace_marked(
            old, PAPERCLIP_START, PAPERCLIP_END, PAPERCLIP_BLOCK
        )
        if new == old:
            continue
        api_json(
            "PUT",
            f"/agents/{agent_id}/instructions-bundle/file",
            {"path": entry, "content": new},
        )
        changed += 1
    return changed, skipped


def main() -> None:
    skill_path = Path(SHARED_SKILL)
    if not skill_path.is_file():
        raise SystemExit(f"Shared skill missing: {skill_path}")

    configs_changed = 0
    souls_changed = 0
    for profile in PROFILES:
        config = profile / "config.yaml"
        soul = profile / "SOUL.md"
        if not config.is_file():
            raise RuntimeError(f"Missing config: {config}")
        configs_changed += int(add_external_dir(config))
        if soul.is_file():
            old = soul.read_text()
            new = replace_marked(old, SOUL_START, SOUL_END, SOUL_BLOCK)
            if new != old:
                soul.write_text(new)
                souls_changed += 1

    legacy_changed = 0
    domain_root = Path("/root/.hermes/skills/domain")
    for name in LEGACY_SKILLS:
        path = domain_root / name / "SKILL.md"
        if not path.is_file():
            raise RuntimeError(f"Expected legacy skill missing: {path}")
        old = path.read_text()
        new = insert_after_frontmatter(old, LEGACY_NOTICE)
        if new != old:
            path.write_text(new)
            legacy_changed += 1

    paperclip_changed, paperclip_skipped = update_paperclip_instructions()

    # Parse every changed config and the canonical frontmatter as a final check.
    for profile in PROFILES:
        data = yaml.safe_load((profile / "config.yaml").read_text())
        assert SHARED_DIR in data["skills"]["external_dirs"]
    canonical = skill_path.read_text()
    frontmatter = canonical.split("---\n", 2)[1]
    assert yaml.safe_load(frontmatter)["name"] == "dtc-marketing-operating-system"

    print(
        json.dumps(
            {
                "configs_changed": configs_changed,
                "souls_changed": souls_changed,
                "legacy_skills_marked": legacy_changed,
                "paperclip_agents_changed": paperclip_changed,
                "paperclip_agents_skipped": paperclip_skipped,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
