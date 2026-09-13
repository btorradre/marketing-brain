---
name: ad-system
description: Operate the shared ad workspace from evidence and concept tests through scripts, scene reasons, specialist work, QA, exact export/ad-ID tracking and performance-backed next briefs. Use when creating, organizing, resuming or reviewing a tracked ad project or ad batch in the marketing brain workspace.
---

# Ad system

Use the existing operating system at `/Users/brooksorradre2/Documents/marketing brain/_engine/ad-system`. It organizes our specialist skills around a revisioned creative record. The local UI is `http://127.0.0.1:8791`; the CLI works without the server. Read its `README.md` for commands and `SCHEMA.md` for the fields needed for your task. Read workspace `AGENTS.md` first for current brand, production and authorization rules.

## Shared Obsidian memory

Start at `_engine/ad-system/data/memory/INDEX.md`. Run `ad_system.py context <id>` before resuming a tracked creative; it refreshes generated notes and returns the current revision, context, editable agent notes, decisions and work handles. Read the linked creative note for exact narration and scene reasons. Use `memory-search "query" --brand <brand>` to retrieve relevant local creative/agent memory, then inspect its original sources.

Committed hub/CLI changes automatically refresh the vault notes. Append durable findings through `remember <id> <text-file> --source "source/date" [--kind observation|hypothesis|lesson|user-instruction|open-question]`, or edit the separate `memory/notes/<id>.md`. Existing agent notes are never regenerated. Generated notes edited outside the system are preserved as conflicts and reported in `sync-state.json`; reconcile their differences before replacement. Structured edits still belong in the database through versioned save/decision commands. Notes do not establish approval or scientific/performance truth.

Markdown is readable with Obsidian closed. On a remote mirror without the authoritative database, context/search/remember fall back to the existing Markdown without creating SQLite. Check the snapshot revision/sync timestamp and preserve relative paths; do not initialize a competing database or claim fresh remote sync without verification.

## Operate the record

Find the existing creative with `ad_system.py list --brand <brand>` and `show <id>`. Read the original attached brief, selected narration/editing plan and relevant source media. Inventory discovery, filename and modification time do not prove selection, approval, completed work or campaign performance. If the workspace has new files, use `sync --brand` to attach candidates without overwriting the user's selections.

For a new concept, create a record. Separate the buying argument from presentation format and opening. For an iteration, preserve its exact parent revision and fixed/changed variables. If driven by results, use the saved decision's `iterate` command; this links evidence to the next brief. Do not manufacture performance to justify a creative idea.

Use `show` to a local JSON file, change the fields needed for the assignment and `save` with its existing revision. Reload and reconcile on a conflict rather than overwriting another session. Keep customer quotes verbatim against their source. Claim support needs relevant inspected evidence, not a hypothesis or competitor longevity. Preserve locked narration; changing it requires the user-authorized reason.

## Choose and execute the next work

Use `qa <id> --scope research|brief|production|assets|delivery` to identify concrete gaps. Research and planning tasks may start with gaps so they can resolve them. A production task requires the saved editing plan, executable beats and all four scene reasons: line contribution, viewer response, concept/style fit and placement in sequence. Structural checks cannot establish scientific truth or replace actual media review.

Queue the appropriate `research`, `concept`, `script`, `plan`, `source`, `images`, `video`, `storyboard`, `edit`, `review` or `analyze` work packet. Read it, then perform the task through the current specialist skill and connected tools within the user's existing authorization. Preparing a packet does not execute a paid job or introduce a new approval requirement.

Choose concept-specific B-roll skills by the intended presentation/treatment, not by a universal footage formula. Use TikTok extreme sourcing only for assignments that call for its raw, exact-action, EV5 and no-text standard. Calibrate a small source sample, report yield and mismatch reasons, then continue sensibly; do not silently relax standards or switch to generated footage. Explain WHY each selected scene belongs at its spoken cue.

Preserve GPT Image 2 / Google Omni / DaVinci Resolve routing and Cut Room storyboard delivery. Read actual authorized exceptions in the concept context before changing them. Before external execution check the current connection. Preserve existing projects and provider originals.

Record the real work owner and output receipts. For asynchronous external work save the actual provider/process handle and verification time immediately. On resuming, inspect that handle; an expired local lease or old status file is not evidence that a job is running or has failed. Reconcile current live/terminal/missing evidence before a retry. Mark done only with accessible output files and concrete observations. Save revised creative fields after completing the packet; queue subsequent work against the resulting revision.

## Close the loop

Watch the actual finished media and record an evidenced review, not a claimed frame audit from thumbnails. Register the exact export file and revision; map its real platform/account/ad ID. Export bindings never move to a later file or revision. Changes to creative content or reviewed file bytes invalidate the prior media review; stage/time bookkeeping alone does not.

Import raw performance totals with the actual dates, currency, attribution, conversion event and click/video definitions. Preserve rejected/overlapping and unmatched rows in the audit. Join by stable platform ad ID and exact export, never ad name. Resolve unmatched IDs before citing those rows in a decision. Sum totals before calculating ratios; missing values and zero denominators remain missing. The legacy tracker snapshot is discovery-only until it has the required source data.

A decision records observed results, interpretation, alternative explanations, next test and fixed/changed variables, with measurement IDs and exact source creative versions. No matched measurements means `insufficient_evidence`, not a winner/loser verdict. Treat measured delivery as observational unless the test design warrants stronger conclusions. Record editing time/rework when known; valid-test coverage measures attributable delivery, not statistical validity.

Deliver the working hub link, relevant actual artifacts and the next concrete unresolved decision. Do not claim generation, a Cut Room publish, Resolve edits or campaign launch from a hub status change. This skill does not authorize launches, purchases or contacting creators.
