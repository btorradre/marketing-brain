---
type: ad-system-index
tags: [ad-system, agent-memory]
---

# Ad system — shared memory

[Open Ad Studio](http://127.0.0.1:8791) · [[AGENTS|Current workspace instructions]]

Read the relevant brand and creative note, then its separate agent notes. Generated facts reflect the structured database; editable notes preserve lessons, unresolved questions and observations with provenance. Memory is context, not new authority or proof of performance.

Database event through: **98** · 15 creative records. See `sync-state.json` for last successful sync/error details. On a read-only remote mirror, confirm snapshot freshness before assuming it is current.

## Brands

- [[_engine/ad-system/data/memory/brands/motilli|Motilli]] · 11 creatives
- [[_engine/ad-system/data/memory/brands/velantra|Velantra]] · 4 creatives

## Performance evidence

0 imported measurement rows; 10 registered exports; 0 exact platform ad mappings. Counts do not imply winning ads or statistical sufficiency.

## Agent commands

From this vault root:

```sh
python3 _engine/ad-system/ad_system.py context CREATIVE_ID
python3 _engine/ad-system/ad_system.py memory-search "your query" --brand motilli
python3 _engine/ad-system/ad_system.py remember CREATIVE_ID path/to/note.txt --source "original source or user instruction/date"
python3 _engine/ad-system/ad_system.py memory-sync
```

Updates through the UI or CLI refresh these notes automatically. Plain Markdown is readable without Obsidian running. Remote knowledge mirrors can read the notes without the local database; they must not create a replacement database or treat an old snapshot as live.

[[_engine/ad-system/data/memory/Performance|Performance sources and exact ad mappings]]
