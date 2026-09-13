#!/usr/bin/env python3
"""Read the vault's skills ONCE and seed packages/playbooks/.

    services/engine/.venv/bin/python scripts/extract_playbooks.py [--vault PATH] [--user-skills PATH]

Outputs (all under packages/playbooks/):
    <name>/playbook.md          SKILL.md body with frontmatter preserved (secret lines stripped)
    <name>/modules|references/  the skill's .md companions, copied as-is (secret lines stripped)
    <name>/sections.json        heading index for playbook.md
    registry.json               one record per included playbook
    CLASSIFICATION.md           every skill seen, its bucket, and why

This is the only code in the repo allowed to know where the vault lives. Nothing under
services/ imports it.
"""
from __future__ import annotations
import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "services" / "engine"))
from adengine.playbooks.lint import audit, strip_secrets, summarize  # noqa: E402

OUT = REPO / "packages" / "playbooks"
VERSION = "1.0.0"
STUB_BYTES = 200
COMPANION_DIRS = ("modules", "references", "reference")
SKIP_DIR_PARTS = {"output", "venv", ".venv", "node_modules", "__pycache__", "assets", "scripts", "build", "data"}

# ----------------------------------------------------------------------------- classification
# bucket rules, in priority order. First match wins. (bucket, stage, reason)
BRAND_PREFIXES = ("velantra-", "velantra", "motilli", "lunessa", "wend", "orelli", "solorna")
OPS = {
    "finance-agent", "shopify-financials", "margin-dashboard", "restock-watch", "applicant-screener",
    "google-ads-agent", "ui-ux-pro-max", "mbc-pipeline",
}
THIRDPARTY_PREFIXES = ("hyperframes", "website-to-hyperframes", "gsap", "chatcut", "n8n-", "media-use")

# name -> (bucket, stage, reason). Everything not listed falls to heuristics below.
EXPLICIT: dict[str, tuple[str, str, str]] = {
    # strategy
    "direct-response-os": ("strategy", "context", "DR OS router; shared spine, laws and artifact schema"),
    "dr-funnel-strategy": ("strategy", "context", "full-funnel creative strategy document"),
    "dr-market-intel": ("strategy", "research", "competitor / winning-ad intelligence"),
    "dr-voc-mining": ("strategy", "research", "mines customer language into an angle index"),
    "dr-survey-designer": ("strategy", "research", "post-purchase survey design for VoC"),
    "dr-awareness-audit": ("strategy", "research", "account audit against the five awareness levels"),
    "avatar-research-deep": ("strategy", "research", "scraped-evidence avatar research"),
    "swipe-intake": ("strategy", "research", "reference ad intake, classification and routing"),
    "ad-watcher": ("strategy", "research", "reference ad teardown; psychological breakdown"),
    "watch": ("strategy", "research", "reference video watch: frames + transcript"),
    "dr-angle-mapper": ("strategy", "angles", "research -> mapped angle tree"),
    "dr-angle-bank": ("strategy", "angles", "durable tagged angle library"),
    "dr-hook-lab": ("strategy", "hooks", "five hooks per angle by awareness level"),
    "hook-bank": ("strategy", "hooks", "written-copy hook patterns by awareness level (vault doctrine)"),
    "video-hook-bank": ("strategy", "hooks", "video hook skeletons by awareness level (vault doctrine)"),
    "cro-agent": ("strategy", "qa", "funnel / landing page conversion audit"),
    "strategize-ad-adaptation": ("strategy", "storyboard", "scene-by-scene adaptation plan from a watched reference"),
    "creative-velocity-system": ("strategy", "loop", "the 100/week creative operating loop (vault doctrine)"),
    # copy
    "long-form-copy": ("copy", "copy", "long-form DR copy laws; naturalizer pass for spoken scripts"),
    "advertorial": ("copy", "copy", "advertorial / presell page copy laws"),
    "ad-concept-builder": ("copy", "copy", "intent-first long-form ad concept builder"),
    "banned-patterns-ai-copy-blacklist": ("copy", "copy", "negative-constraint list for AI-tell copy patterns (vault doctrine)"),
    "native-image-factory": ("copy", "generation", "turns copy into native ad image prompts"),
    "dr-video-ads": ("copy", "script", "belief-shifting video ad / VSL script engine"),
    "vsl-build-method": ("copy", "script", "VSL build order of operations (vault doctrine)"),
    "rapid-vsl": ("production", "avatar", "script + avatar image -> lip-synced yapper VSL"),
    "dr-ugc-brief": ("copy", "brief", "creator brief from one angle + hook"),
    "creative-brief": ("copy", "brief", "creative strategist's five-part brief"),
    "video-brief": ("copy", "brief", "canonical house video production brief"),
    "video-brief-format-sop": ("copy", "brief", "house video brief format law (vault doctrine)"),
    "segment-brief-sop": ("copy", "brief", "segment map mechanics for chained generation runs (vault doctrine)"),
    "landing-page-builder": ("copy", "copy", "landing page structure + CRO; deploy steps are Shopify/Vercel-specific"),
    "sales-page-builder": ("copy", "copy", "long-form sales page structure; deploy steps are Shopify Elixir-specific"),
    "shopify-listicle-builder": ("copy", "copy", "listicle page structure; deploy steps are Shopify-specific"),
    "elixir-pdp-builder": ("copy", "copy", "PDP structure; deploy steps are Shopify Elixir-specific"),
    # production
    "seedance-prompt-system": ("production", "generation", "canonical Seedance prompt format (vault doctrine)"),
    "seedance-prompt-architect": ("production", "storyboard", "reference -> cut-aware prompt pack"),
    "seedance-directors-cut": ("production", "storyboard", "reference -> re-directed scene package"),
    "seedanceugcdirector": ("production", "storyboard", "concept -> complete UGC production package"),
    "cutroom": ("production", "storyboard", "visual storyboard board method for editors (board tool is internal)"),
    "elevenlabs-agent": ("production", "voice", "voice cloning + TTS"),
    "ugc-forge": ("production", "voice", "one voice across auto-segmented beats, then video"),
    "fabric-talking-head": ("production", "avatar", "avatar image + VO -> talking head"),
    "aiugc-orchestrator": ("production", "avatar", "script -> VO -> avatar -> talking head"),
    "raw-ugc-avatar": ("production", "avatar", "opening-frame avatar prompt for raw UGC"),
    "higgsfield-soul-id": ("production", "avatar", "identity-consistent character training"),
    "broll-auditor": ("production", "qa", "post-generation QA of b-roll against references"),
    "broll-sourcer": ("production", "editing", "finds b-roll slots in a creative and sources clips"),
    "b-roll-finder": ("production", "editing", "routes script beats to b-roll sourcing lanes"),
    "tiktok-broll-crawler": ("production", "editing", "real organic footage matched to script lines"),
    # editing
    "video-editor-brief": ("editing", "editing", "script + scenes -> editor timeline brief"),
    # brand (excluded): generic name, but the body and references/laws.md are one brand's PDP law and product-truth scaffolding
    "product-launch": ("brand", "context", "scaffolds product-truth skills and PDPs against one brand's house law; brand data, not doctrine"),
}

STAGE_HINTS = [
    (re.compile(r"replicator|animated|claymation|aiugc|omni-ugc|pov-trend|higgsfield|nano-banana|video-gen|video-scene|ad-replicator|brief-runner|fashion"), "generation"),
]


def classify(name: str, desc: str) -> tuple[str, str, str]:
    if name in EXPLICIT:
        return EXPLICIT[name]
    if name.startswith(BRAND_PREFIXES):
        return ("brand", "context", "brand-owned: name carries a brand prefix")
    if "-concept" in name or "product-truth" in name:
        return ("brand", "context", "product concept / product-truth skill")
    if name in OPS:
        return ("ops", "loop", "operations / back-office tooling, not creative doctrine")
    if name.startswith(THIRDPARTY_PREFIXES):
        return ("thirdparty", "generation", "vendor tool documentation (HyperFrames / n8n / GSAP family)")
    for pat, stage in STAGE_HINTS:
        if pat.search(name):
            return ("production", stage, "generation pipeline (heuristic: name)")
    return ("production", "generation", "UNCLASSIFIED by rule; defaulted to production/generation")


# ----------------------------------------------------------------------------- frontmatter
def split_frontmatter(text: str) -> tuple[dict, str, str]:
    """Return (meta, raw_frontmatter_block, body). Minimal YAML: scalars, quoted, >, >-, |."""
    if not text.startswith("---"):
        return {}, "", text
    lines = text.splitlines(keepends=True)
    end = None
    for i in range(1, len(lines)):
        if lines[i].rstrip("\n") == "---":
            end = i
            break
    if end is None:
        return {}, "", text
    fm_lines = [l.rstrip("\n") for l in lines[1:end]]
    meta: dict = {}
    key = None
    block_mode = None
    for line in fm_lines:
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m and not line.startswith((" ", "\t")):
            key, val = m.group(1), m.group(2).strip()
            if val in (">", ">-", "|", "|-"):
                block_mode = val
                meta[key] = ""
            else:
                block_mode = None
                if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
                    val = val[1:-1]
                meta[key] = val
        elif key is not None and (line.startswith((" ", "\t")) or line == ""):
            s = line.strip()
            if block_mode and block_mode.startswith("|"):
                meta[key] += s + "\n"
            elif block_mode:
                meta[key] += (s + " ") if s else "\n"
            else:
                meta[key] = (meta[key] + " " + s).strip()
    for k, v in list(meta.items()):
        if isinstance(v, str):
            meta[k] = re.sub(r"[ \t]+", " ", v).strip()
    raw = "".join(lines[: end + 1])
    body = "".join(lines[end + 1 :])
    return meta, raw, body


# ----------------------------------------------------------------------------- sections
_slug_rx = re.compile(r"[^a-z0-9]+")


def slug(s: str) -> str:
    s = re.sub(r"[*_`\[\]()#]", "", s).lower()
    s = _slug_rx.sub("-", s).strip("-")
    return s[:60] or "section"


def index_sections(text: str) -> list[dict]:
    """Split by top-level headings (# or ##) outside fenced code. Line numbers are 1-based over `text`."""
    lines = text.splitlines(keepends=True)
    heads: list[tuple[int, str]] = []
    in_fence = False
    in_fm = False
    for i, line in enumerate(lines, 1):
        stripped = line.rstrip("\n")
        if i == 1 and stripped == "---":
            in_fm = True
            continue
        if in_fm:
            if stripped == "---":
                in_fm = False
            continue
        if re.match(r"^\s*(```|~~~)", stripped):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = re.match(r"^(#{1,2})\s+(.+?)\s*#*\s*$", stripped)
        if m:
            heads.append((i, m.group(2).strip()))
    sections: list[dict] = []
    seen: dict[str, int] = {}

    def add(sid: str, title: str, start: int, end: int):
        base = sid
        n = seen.get(base, 0)
        seen[base] = n + 1
        if n:
            sid = f"{base}-{n + 1}"
        chars = sum(len(l) for l in lines[start - 1 : end])
        sections.append({"id": sid, "title": title, "start_line": start, "end_line": end, "chars": chars})

    first = heads[0][0] if heads else len(lines) + 1
    # preamble = everything before the first heading, frontmatter included
    if first > 1:
        pre = "".join(lines[: first - 1])
        if pre.strip():
            add("preamble", "(preamble)", 1, first - 1)
    for j, (start, title) in enumerate(heads):
        end = heads[j + 1][0] - 1 if j + 1 < len(heads) else len(lines)
        add(slug(title), title, start, end)
    return sections


# ----------------------------------------------------------------------------- sources
def unescape_gdoc_markdown(text: str) -> str:
    """Google-Docs exports escape markdown (\\# \\* \\- \\.). Undo so headings parse."""
    return re.sub(r"\\([#*_\-.\[\]()>`!])", r"\1", text)


def companion_files(skill_dir: Path) -> list[Path]:
    out: list[Path] = []
    for sub in COMPANION_DIRS:
        d = skill_dir / sub
        if not d.is_dir():
            continue
        for p in sorted(d.rglob("*.md")):
            rel_parts = set(p.relative_to(skill_dir).parts[:-1])
            if rel_parts & SKIP_DIR_PARTS or any(part.startswith("_retired") for part in rel_parts):
                continue
            out.append(p)
    return out


def discover_skills(project_root: Path, user_root: Path) -> dict[str, dict]:
    """name -> {dir, origin}. Project skills win over user skills with the same name."""
    found: dict[str, dict] = {}
    for origin, root in (("user-skill", user_root), ("project-skill", project_root)):
        if not root.is_dir():
            continue
        for d in sorted(root.iterdir()):
            if not d.is_dir() or d.name.startswith("."):
                continue
            found[d.name] = {"dir": d, "origin": origin}
    return found


def doctrine_sources(vault: Path) -> list[dict]:
    eng = vault / "_engine"
    items = [
        ("seedance-prompt-system", eng / "sops" / "Seedance-Prompt-System.md", False),
        ("vsl-build-method", eng / "sops" / "VSL-Build-Method.md", False),
        ("video-brief-format-sop", eng / "sops" / "Video-Brief-Format-SOP.md", False),
        ("segment-brief-sop", eng / "sops" / "Segment-Brief-SOP.md", False),
        ("creative-velocity-system", eng / "sops" / "Creative-Velocity-System.md", False),
        ("banned-patterns-ai-copy-blacklist", eng / "frameworks" / "fundamentals" / "# BANNED PATTERNS_ THE AI COPY BLACKLIST.md", True),
        ("hook-bank", eng / "swipe-library" / "hook-bank" / "HOOK-BANK.md", False),
        ("video-hook-bank", eng / "swipe-library" / "hook-bank" / "VIDEO-HOOK-BANK.md", False),
    ]
    return [{"name": n, "path": p, "unescape": u, "origin": "vault-doctrine"} for n, p, u in items]


def first_paragraph(body: str) -> str:
    for para in re.split(r"\n\s*\n", body):
        t = " ".join(l.strip() for l in para.strip().splitlines())
        t = re.sub(r"^#+\s*", "", t)
        if len(t) > 40 and not t.startswith(("**Scope", "|", "-", ">")):
            return re.sub(r"[*`]", "", t)[:400]
    return ""


# ----------------------------------------------------------------------------- main
def write_text(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def emit(name: str, origin: str, raw_fm: str, meta: dict, body: str, companions: list[tuple[str, str]],
         bucket: str, stage: str) -> dict:
    """Write <name>/ and return the registry record."""
    folder = OUT / name
    if folder.exists():
        shutil.rmtree(folder)
    folder.mkdir(parents=True)

    text = raw_fm + body
    text, removed = strip_secrets(text)
    write_text(folder / "playbook.md", text)
    sections = index_sections(text)
    write_text(folder / "sections.json", json.dumps(sections, indent=1))

    files = ["playbook.md"]
    leaks = [{"file": "playbook.md", **h} for h in audit(text)]
    stripped = [{"file": "playbook.md", **r} for r in removed]
    for rel, ctext in companions:
        ctext, crem = strip_secrets(ctext)
        write_text(folder / rel, ctext)
        files.append(rel)
        leaks += [{"file": rel, **h} for h in audit(ctext)]
        stripped += [{"file": rel, **r} for r in crem]

    desc = meta.get("description") or first_paragraph(body)
    title = None
    m = re.search(r"^#\s+(.+?)\s*$", body, re.MULTILINE)
    if m:
        title = m.group(1).strip()
    return {
        "name": name,
        "version": VERSION,
        "stage": stage,
        "bucket": bucket,
        "title": title or name,
        "description": desc,
        "origin": origin,
        "files": files,
        "sections": sections,
        "size": len(text.encode("utf-8")),
        "leaks": leaks,
        "leak_summary": summarize(leaks),
        "secrets_stripped": stripped,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vault", default=os.environ.get("MARKETING_BRAIN_VAULT", str(Path.home() / "Documents" / "marketing brain")))
    ap.add_argument("--user-skills", default=str(Path.home() / ".claude" / "skills"))
    args = ap.parse_args()
    vault = Path(args.vault)
    project_skills = vault / ".claude" / "skills"
    user_skills = Path(args.user_skills)

    OUT.mkdir(parents=True, exist_ok=True)
    registry: list[dict] = []
    table: list[dict] = []  # every skill seen
    skipped: list[dict] = []

    # 1. skills
    for name, info in sorted(discover_skills(project_skills, user_skills).items()):
        d: Path = info["dir"]
        skill_md = d / "SKILL.md"
        if not skill_md.is_file():
            skipped.append({"name": name, "origin": info["origin"], "why": "no SKILL.md"})
            table.append({"name": name, "origin": info["origin"], "bucket": "skipped", "stage": "-", "included": False, "reason": "no SKILL.md"})
            continue
        raw = skill_md.read_text(encoding="utf-8", errors="replace")
        if len(raw.encode("utf-8")) < STUB_BYTES:
            skipped.append({"name": name, "origin": info["origin"], "why": f"stub ({len(raw)} bytes)"})
            table.append({"name": name, "origin": info["origin"], "bucket": "skipped", "stage": "-", "included": False, "reason": f"stub, {len(raw)} bytes"})
            continue
        meta, raw_fm, body = split_frontmatter(raw)
        bucket, stage, reason = classify(name, meta.get("description", ""))
        included = bucket in ("strategy", "copy", "production", "editing")
        row = {"name": name, "origin": info["origin"], "bucket": bucket, "stage": stage if included else "-", "included": included, "reason": reason}
        table.append(row)
        if not included:
            continue
        comps = []
        for p in companion_files(d):
            rel = p.relative_to(d).as_posix()
            comps.append((rel, p.read_text(encoding="utf-8", errors="replace")))
        rec = emit(name, info["origin"], raw_fm, meta, body, comps, bucket, stage)
        rec["companion_count"] = len(comps)
        row["leaks"] = len(rec["leaks"])
        registry.append(rec)

    # 2. vault doctrine (no frontmatter at source; synthesize one)
    for src in doctrine_sources(vault):
        p: Path = src["path"]
        if not p.is_file():
            skipped.append({"name": src["name"], "origin": src["origin"], "why": "source missing"})
            table.append({"name": src["name"], "origin": src["origin"], "bucket": "skipped", "stage": "-", "included": False, "reason": "source file missing"})
            continue
        body = p.read_text(encoding="utf-8", errors="replace")
        if src["unescape"]:
            body = unescape_gdoc_markdown(body)
        bucket, stage, reason = classify(src["name"], "")
        desc = first_paragraph(body)
        fm = f"---\nname: {src['name']}\ndescription: {json.dumps(desc)}\nsource_kind: vault-doctrine\n---\n\n"
        rec = emit(src["name"], src["origin"], fm, {"description": desc}, body, [], bucket, stage)
        rec["companion_count"] = 0
        table.append({"name": src["name"], "origin": src["origin"], "bucket": bucket, "stage": stage, "included": True, "reason": reason, "leaks": len(rec["leaks"])})
        registry.append(rec)

    # 3. registry + classification table (and prune folders from earlier runs that are no longer included)
    keep = {r["name"] for r in registry}
    for d in OUT.iterdir():
        if d.is_dir() and d.name not in keep:
            shutil.rmtree(d)
            print(f"pruned stale playbook folder: {d.name}")
    registry.sort(key=lambda r: (r["bucket"], r["stage"], r["name"]))
    write_text(OUT / "registry.json", json.dumps(registry, indent=1, ensure_ascii=False))

    by_bucket: dict[str, int] = {}
    for row in table:
        by_bucket[row["bucket"]] = by_bucket.get(row["bucket"], 0) + 1
    lines = [
        "# Playbook classification",
        "",
        "Generated by `scripts/extract_playbooks.py`. Every skill folder seen in the vault's project skills and the user skills, plus the vault doctrine files, with its bucket and the reason.",
        "",
        "Included buckets: strategy, copy, production, editing. Excluded: brand, ops, thirdparty, skipped.",
        "",
        "| bucket | count |", "|---|---|",
    ]
    lines += [f"| {b} | {n} |" for b, n in sorted(by_bucket.items())]
    lines += ["", f"Total playbooks written: **{len(registry)}**", "", "| name | origin | bucket | stage | included | leaks | reason |", "|---|---|---|---|---|---|---|"]
    for row in sorted(table, key=lambda r: (not r["included"], r["bucket"], r["name"])):
        lines.append(f"| {row['name']} | {row['origin']} | {row['bucket']} | {row['stage']} | {'yes' if row['included'] else 'no'} | {row.get('leaks', '')} | {row['reason']} |")
    if skipped:
        lines += ["", "## Skipped", ""] + [f"- `{s['name']}` ({s['origin']}): {s['why']}" for s in skipped]
    lines += [
        "", "## Notes", "",
        "- Skills present in both the project and user skill folders were deduplicated; the project copy wins (they were byte-identical at extraction time).",
        "- `banned-patterns-ai-copy-blacklist` came from a Google-Docs export with backslash-escaped markdown; escapes were removed so headings parse. No wording was changed.",
        "- Vault doctrine files had no frontmatter; a `name` / `description` block was synthesized from the first paragraph.",
        "- Lines containing literal API keys are removed and listed in `registry.json` under `secrets_stripped`. No other text was rewritten; `leaks` is the human rewrite worklist.",
        "- Companion `.md` files are copied only from `modules/`, `references/`, `reference/`; run outputs, retired folders, scripts and vendored code are not.",
    ]
    write_text(OUT / "CLASSIFICATION.md", "\n".join(lines) + "\n")

    # 4. report
    print(f"playbooks written: {len(registry)}  ->  {OUT}")
    print("by bucket (all skills seen):", dict(sorted(by_bucket.items())))
    inc: dict[str, int] = {}
    for r in registry:
        inc[r["bucket"]] = inc.get(r["bucket"], 0) + 1
    print("included by bucket:", dict(sorted(inc.items())))
    print("skipped:", [f"{s['name']} ({s['why']})" for s in skipped])
    top = sorted(registry, key=lambda r: -len(r["leaks"]))[:10]
    print("leakiest:")
    for r in top:
        print(f"  {len(r['leaks']):4d}  {r['name']:34s} {r['leak_summary']}")
    strip_n = sum(len(r["secrets_stripped"]) for r in registry)
    print(f"secret lines stripped: {strip_n}")
    unsure = [r["name"] for r in table if "UNCLASSIFIED" in r["reason"]]
    print("unclassified-by-rule (defaulted):", unsure)


if __name__ == "__main__":
    main()
