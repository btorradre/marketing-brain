# manus_export.py — put a skill into Manus

Manus can't read the vault, run `publish_brief.py`, or call an MCP server. So a
skill only travels if it becomes **one self-contained document**. That's what
this makes.

```bash
python3 _engine/tools/manus_export.py --list          # what can be exported
python3 _engine/tools/manus_export.py video-brief     # bundle + copy to clipboard
python3 _engine/tools/manus_export.py --all           # bundle every portable skill
```

Output lands in `manus-export-bundles/<skill>-MANUS.md` and on the clipboard.
Paste it into Manus as a Knowledge entry, or upload the file.

## What a bundle is

Title + "when to use this" (from the skill's `description`) + the full skill
body + every reference file inlined as `## Appendix A`, `## Appendix B`, …
In-body mentions of `references/foo.md` get rewritten to `(Appendix A below)`
so Manus never goes hunting for a file that isn't there.

## Where it reads from

1. `manus-export/<skill>/` — the hand-de-localized fork. Preferred.
2. `.claude/skills/<skill>/` then `~/.claude/skills/<skill>/` — the live skill.
   Bundled as-is with a loud warning, because it still talks about our paths.

`--raw` forces 2 even when 1 exists. Use it when the live skill has moved on and
you need to re-derive the portable fork.

## The leak audit

Every bundle is scanned for things that mean nothing in Manus: absolute paths,
vault-relative paths, `python3 something.py`, MCP tool names, `.env`. Clean
portable exports report `leaks: none`. A raw export reports the list — that list
IS the rewrite worklist for the `manus-export/` fork.

```bash
python3 _engine/tools/manus_export.py video-brief --raw --audit-only
```

## Adding a skill Manus doesn't have yet

1. `--raw --audit-only` to see what has to change.
2. `cp -r .claude/skills/<skill> manus-export/<skill>`
3. Rewrite the flagged lines: local paths become plain descriptions of the step,
   `publish_brief.py --next-id` becomes "look at what exists and take the next
   number", MCP tools become "whatever tool you have that does X". Keep every
   law and every format rule verbatim — those are the point.
4. Re-run with no flags until it reports `leaks: none`.
