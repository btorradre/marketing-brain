# Ad Studio

Open http://127.0.0.1:8791 on this Mac.

This is the shared record for our ad work: evidence → concept → narration and scene reasons → specialist work → actual outputs and reviews → exact platform IDs → performance → next brief.

## Start with an existing Motilli concept

1. Select its record. The imported files are candidates, not automatically approved selections. Library searches all discovered creative and context files; Assets opens attached originals.
2. Fill Brief with the argument, buying situation, belief, promise, proof and test hypothesis. Add exact evidence with provenance. Keep hypotheses distinct from verified product facts.
3. In Story select the exact narration, hook tests and saved editing plan. Each scene explains why its action supports the line, what the viewer should understand/feel, why it fits the concept and why it appears here. Lock approved narration before visual-only changes.
4. Work prepares a version-specific packet for the existing skill. The agent executes within current authorization and records real source files, provider handles and observations. A button does not launch paid generation or edit a project.
5. Review surfaces exact missing fields. Watch the actual finished asset before recording a media review. Register the exact export and map its real platform ad ID.
6. Results imports raw totals from a reporting CSV with explicit account, dates, attribution and metric definitions. Resolve unmatched IDs, then record observation, interpretation, alternative explanation and fixed/changed variables. “Create next brief” preserves that decision and parent version.

## What is already here

Motilli workspace projects and original file paths are indexed. Existing scripts, edits and boards remain untouched. A discovered status file is not evidence that a job is still running. A script's filename or modification date does not prove it is approved. Review current work before selecting it.

No campaign results are preloaded. The older creative-tracker snapshot lacks the exact IDs/settings/raw totals needed here, so it has not been relabeled as Motilli performance.

## Current routes

Images: GPT Image 2. Video: Google Omni. Storyboards: Cut Room, including actual first assets and scene reasons. Editing: DaVinci Resolve after checking its connection. Existing user-authorized format exceptions must be read in their original brief; do not overwrite them with a guessed global default.

TikTok extreme action sourcing retains EV5, organic appearance, exact-action matching and complete selected-interval no-text inspection. Source permission and visual suitability are separate. Other concepts keep their own treatment; fully animated work is not forced into TikTok footage.

## Restart and backup

From the workspace root:

```sh
python3 _engine/ad-system/manage.py start
python3 _engine/ad-system/manage.py status
python3 _engine/ad-system/manage.py backup
```

The app uses a local database at `_engine/ad-system/data/system.sqlite3`. Work packets, reporting imports and decision documents are alongside it. A backup includes the database and system data; original brand media remains in its existing folders and requires its existing backup process. No network service or cloud login is required. Do not expose this local tool to a public network.

## Shared memory in Obsidian

Open `data/memory/INDEX.md` in this vault, or follow “Shared ad memory” from the Obsidian Dashboard. Each creative links its generated current record and a separate editable agent-notes file. System changes refresh the generated record automatically. Notes added in Obsidian or the hub's Memory tab remain intact across later saves.

Agents begin with `context CREATIVE_ID`, search with `memory-search`, and record durable observations with `remember` or by editing the linked notes. Always preserve the original source/date. The memory index exposes unresolved version choices and recorded external handles; it does not silently turn old notes into approvals or campaign results.
