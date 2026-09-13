#!/usr/bin/env python3
"""
manus_export.py — flatten a skill into ONE self-contained Markdown doc you can
paste (or upload) into Manus as a Knowledge / Skill entry.

Manus has no notion of our folder layout, our python helpers, our MCP servers,
or the vault. So a bundle is: the SKILL body + every reference file inlined as a
lettered appendix, with the local plumbing called out by the auditor instead of
silently shipped.

Usage
  python3 manus_export.py --list
  python3 manus_export.py video-brief
  python3 manus_export.py video-brief --no-copy
  python3 manus_export.py --all
  python3 manus_export.py video-brief --raw --audit-only

Source priority for a skill named X:
  1. manus-export/X/            (already de-localized — preferred)
  2. .claude/skills/X/          (project skill — raw, will warn)
  3. ~/.claude/skills/X/        (user skill — raw, will warn)

Output: manus-export-bundles/X-MANUS.md, and the text on the clipboard.
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

VAULT = Path(__file__).resolve().parents[2]
SOURCES = [
    ("portable", VAULT / "manus-export"),
    ("raw-project", VAULT / ".claude" / "skills"),
    ("raw-user", Path.home() / ".claude" / "skills"),
]
OUT_DIR = VAULT / "manus-export-bundles"

# Things that mean nothing inside Manus and must be rewritten or cut.
LEAKS = [
    (r"/Users/[A-Za-z0-9._-]+", "absolute local path"),
    (r"~/\.claude", "local Claude config path"),
    (r"\.claude/skills", "local skills path"),
    (r"\bpython3?\s+\S+\.py", "local script invocation"),
    (r"\bmcp__\w+", "MCP tool name"),
    (r"\b(?:brands|_engine|cutroom|swipe-intake)/[\w./-]+", "vault-relative path"),
    (r"\b\w+\.py\b", "python helper file"),
    (r"\.(?:env|mcp\.json)\b", "local config file"),
]

SKIP_REF_SUFFIXES = {".py", ".sh", ".json", ".pyc", ".ds_store"}
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def find_skill(name, raw=False):
    sources = [s for s in SOURCES if s[0] != "portable"] if raw else SOURCES
    for kind, root in sources:
        d = root / name
        if (d / "SKILL.md").is_file():
            return kind, d
        f = root / f"{name}.md"
        if f.is_file():
            return kind, f
    return None, None


def list_skills():
    seen = {}
    for kind, root in SOURCES:
        if not root.is_dir():
            continue
        for p in sorted(root.iterdir()):
            n = p.name[:-3] if p.name.endswith(".md") else p.name
            if n.startswith(".") or n in seen:
                continue
            if (p / "SKILL.md").is_file() or p.suffix == ".md":
                seen[n] = kind
    return seen


def split_frontmatter(text):
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    raw, body = text[3:end], text[end + 4:]
    meta = {}
    for line in raw.splitlines():
        if ":" in line and not line.startswith((" ", "\t", "-")):
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, body.lstrip("\n")


def audit(text):
    hits = []
    for i, line in enumerate(text.splitlines(), 1):
        for pattern, label in LEAKS:
            for m in re.finditer(pattern, line):
                hits.append((i, label, m.group(0).strip()))
                break
    return hits


def reference_files(skill_dir):
    if skill_dir.is_file():
        return []
    out = []
    for sub in ("references", "reference"):
        d = skill_dir / sub
        if d.is_dir():
            for p in sorted(d.rglob("*")):
                if p.is_file() and p.suffix.lower() not in SKIP_REF_SUFFIXES \
                        and not p.name.startswith("."):
                    out.append(p)
    return out


def build(name, kind, path):
    skill_md = path if path.is_file() else path / "SKILL.md"
    meta, body = split_frontmatter(skill_md.read_text(encoding="utf-8"))
    refs = reference_files(path)

    # Point every in-body mention of a reference file at its appendix, so the
    # model never goes looking for a file that does not exist in Manus.
    for i, ref in enumerate(refs):
        letter = LETTERS[i] if i < len(LETTERS) else f"Z{i}"
        rel = ref.relative_to(path).as_posix()
        for form in (f"`{rel}`", f"`{ref.name}`"):
            body = re.sub(
                re.escape(form) + r"(?! \(Appendix)",
                f"{form} (Appendix {letter} below)",
                body,
            )

    lines = [
        f"# {meta.get('name', name)} — Manus Skill Bundle",
        "",
        "> Self-contained. Everything this skill needs is in this one document:",
        "> the instructions first, then every reference file inlined as an appendix.",
        "> Nothing here reads from an external file, script, or tool.",
        "",
        "## When to use this skill",
        "",
        meta.get("description", "_(no description in source)_"),
        "",
        "---",
        "",
        body.rstrip(),
        "",
    ]

    if refs:
        lines += [
            "---",
            "",
            "# Appendices — the reference files",
            "",
            "The instructions above point at reference files by name. "
            "Each one is reproduced in full below.",
            "",
        ]
        for i, ref in enumerate(refs):
            letter = LETTERS[i] if i < len(LETTERS) else f"Z{i}"
            rel = ref.relative_to(path)
            lines += [
                "---",
                "",
                f"## Appendix {letter} — `{rel.as_posix()}`",
                "",
                ref.read_text(encoding="utf-8").rstrip(),
                "",
            ]

    text = "\n".join(lines).rstrip() + "\n"
    return text, meta, refs, kind


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("skill", nargs="?", help="skill name, e.g. video-brief")
    ap.add_argument("--list", action="store_true", help="list exportable skills")
    ap.add_argument("--all", action="store_true", help="bundle every portable skill")
    ap.add_argument("--audit-only", action="store_true", help="report leaks, write nothing")
    ap.add_argument("--no-copy", action="store_true", help="skip the clipboard")
    ap.add_argument("--raw", action="store_true",
                    help="force the live local skill as the source, skipping manus-export/ "
                         "(use when the local skill has moved on and you need to re-derive it)")
    args = ap.parse_args()

    if args.list:
        for n, kind in sorted(list_skills().items()):
            flag = "" if kind == "portable" else f"   [{kind} — needs de-localizing]"
            print(f"  {n}{flag}")
        return

    targets = []
    if args.all:
        targets = sorted(n for n, k in list_skills().items() if k == "portable")
    elif args.skill:
        targets = [args.skill]
    else:
        ap.error("give a skill name, or --list, or --all")

    OUT_DIR.mkdir(exist_ok=True)
    for name in targets:
        kind, path = find_skill(name, raw=args.raw)
        if not path:
            print(f"!! {name}: not found in manus-export/, .claude/skills/, or ~/.claude/skills/")
            continue

        text, meta, refs, kind = build(name, kind, path)
        hits = audit(text)

        print(f"\n=== {name} ===")
        print(f"source   : {path}  ({kind})")
        print(f"size     : {len(text):,} chars  ~{len(text)//4:,} tokens")
        print(f"appendices: {len(refs)}" + (f"  ({', '.join(r.name for r in refs)})" if refs else ""))

        if kind != "portable":
            print("WARNING  : raw local skill. Bundled as-is — read the leaks below and rewrite\n"
                  "           them before this goes into Manus.")
        if hits:
            print(f"leaks    : {len(hits)} line(s) reference local plumbing:")
            for ln, label, frag in hits[:40]:
                print(f"   L{ln:<5} {label:<24} {frag}")
            if len(hits) > 40:
                print(f"   … {len(hits) - 40} more")
        else:
            print("leaks    : none — clean for Manus")

        if args.audit_only:
            continue

        out = OUT_DIR / f"{name}-MANUS.md"
        out.write_text(text, encoding="utf-8")
        print(f"wrote    : {out}")

        if not args.no_copy and len(targets) == 1:
            try:
                subprocess.run(["pbcopy"], input=text.encode("utf-8"), check=True)
                print("clipboard: copied — paste straight into Manus")
            except Exception as e:
                print(f"clipboard: skipped ({e})")


if __name__ == "__main__":
    main()
