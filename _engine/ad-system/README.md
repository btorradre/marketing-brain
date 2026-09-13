# Ad Studio — shared AI ad system

The organizing layer for the existing marketing workspace. Motilli is the initial inventory. Records connect research, concept hypotheses, exact narration, hook tests, scene reasons, assets, specialist work, finished-media review, immutable exports, actual platform ad IDs, performance and the next decision.

**Open:** http://127.0.0.1:8791 on this Mac. [User guide](data/START-HERE.md), [record schema](SCHEMA.md), [acceptance plan](BUILD-PLAN.md), [verification](data/verification/acceptance.md).

## Run

Python 3.10+; the application uses only the standard library. The optional browser smoke test uses the already-installed Playwright package/browser.

From the workspace root:

```sh
python3 _engine/ad-system/manage.py start
python3 _engine/ad-system/manage.py status
python3 _engine/ad-system/manage.py stop
python3 _engine/ad-system/manage.py backup
```

`start` preserves occupied ports/processes, records its own process and checks a real response. `stop` only stops the verified owned process. No automatic login/startup service is installed. A restart preserves SQLite records. If another service occupies 8791, use `server.py --port <free-port>`; the managed startup uses 8791.

Data is in `data/system.sqlite3`; version snapshots and events remain in the database. Work packets, source CSVs, decisions, inventory reports and verification receipts are stored under `data/`. Backups use SQLite's consistent backup API, plus system artifacts. Original media is referenced in place, not copied into this database backup. Do not move selected source media without updating the record. Content changes need a new export/review.

## Operate by CLI

All commands below run from the workspace root. `--db <path>` before the command selects a separate database for isolated work. Inputs use files so narration, quotes and multiline notes do not undergo shell interpolation.

```sh
python3 _engine/ad-system/ad_system.py sync --brand motilli
python3 _engine/ad-system/ad_system.py list --brand motilli
python3 _engine/ad-system/ad_system.py show MOT-UGC-YAPPER-01
python3 _engine/ad-system/ad_system.py new --brand motilli --title 'Name the argument'
```

To edit a record, write `show <id>` output to a JSON file under `data/`, change the needed fields, then:

```sh
python3 _engine/ad-system/ad_system.py save _engine/ad-system/data/creative-draft.json --reason 'Describe the actual change'
python3 _engine/ad-system/ad_system.py qa CREATIVE_ID --scope production
python3 _engine/ad-system/ad_system.py stage CREATIVE_ID plan --revision 3
python3 _engine/ad-system/ad_system.py queue CREATIVE_ID plan
python3 _engine/ad-system/ad_system.py queue CREATIVE_ID source --after TASK_ID
```

Use the exact returned IDs/revisions. Do not save over stale writes; reload and reconcile. `--unlock-reason` on save is for an actual user-authorized narration change. The UI also locks narration. Work packet readiness snapshots are not live provider status. Queuing prepares a handoff; the agent still executes via the existing specialist tools.

Task input JSON:

```json
{"task_id":"TASK_ID","action":"start","owner":"current agent/session"}
```

Save it then run `ad_system.py task <file>`. Other actions:

- `submitted`: include `handle` with actual `provider`, `id`, `verified_at`.
- `reconcile`: include `receipt` with `state: live|terminal|missing` and current `observation`.
- `done`: include `receipt` with accessible `path` and `observation` of actual outputs.
- `failed` / `cancelled`: submitted external jobs must first be reconciled as terminal/missing. The system does not cancel provider jobs.

Expired leases display `needs_reconcile`; no automatic retry or provider status is inferred. Finish a task against the revision it executed, save resulting creative changes, then queue the next revision. An old pending task cannot start against new creative content.

## Finished media and reporting

A human-media review is JSON with reviewer, artifact_path, verdict (`PASS|FLAG|FAIL`) and concrete notes. `review <id> <file> --revision N` stores its media hash and creative content hash. Revision changes to the actual creative invalidate it; stage/operational bookkeeping does not. Structural QA does not prove accuracy, rights, scientific support or conversion performance.

```sh
python3 _engine/ad-system/ad_system.py review CREATIVE_ID _engine/ad-system/data/media-review.json --revision 4
python3 _engine/ad-system/ad_system.py export CREATIVE_ID brands/motilli/creative/CONCEPT/edit/final.mp4 --revision 4 --hook H1
python3 _engine/ad-system/ad_system.py bind --platform meta --account ACTUAL_ACCOUNT_ID --ad ACTUAL_AD_ID --export EXPORT_ID
python3 _engine/ad-system/ad_system.py import _engine/ad-system/data/report.csv --settings _engine/ad-system/data/actual-settings.json
python3 _engine/ad-system/ad_system.py results
python3 _engine/ad-system/ad_system.py operations
```

Exports reference and hash actual local image/video files. Registering a file is not a media decode or finished-review certification. A registered file modified in place fails a later binding check. Historical ad bindings preserve the originally recorded revision/hash; register a new file for future delivery. No live campaign launch is part of this system.

[CSV template](data/performance-template.csv) has only a header; no fabricated sample results. Copy [report settings](data/reporting-settings.json) and replace each marked value with the exact reporting configuration. Required columns: `ad_id,date_start,date_end,spend,purchases,impressions,clicks`. Optional: `revenue,video_starts,views_3s,thruplays`. Use ISO dates and unsymbolized nonnegative numbers. Blank optional values mean missing. Ad names are not IDs.

The supported hook definition is 3-second views / impressions; hold is thruplays / 3-second views. Other platform definitions require a separate adapter before comparison. A whole malformed/duplicate/overlapping file is rejected, saved with its errors and excluded from measurements. Reimporting identical content/settings is idempotent. Separate windows must not overlap for the same ad/settings. Currency, account, attribution, conversion event and definitions remain separate. Missing or zero denominators yield null metrics. Unmatched ad IDs stay in the audit and rejoin when the exact export is mapped.

Decision JSON includes `observation,interpretation,alternative,next_test,fixed,changed,outcome,measurement_ids`. Outcome: `test|iterate|retire|insufficient_evidence`. All except insufficient_evidence require matched source rows; no default performance verdict is inferred.

```sh
python3 _engine/ad-system/ad_system.py decision CREATIVE_ID _engine/ad-system/data/decision-input.json
python3 _engine/ad-system/ad_system.py iterate DECISION_ID --title 'Next evidence-backed test'
python3 _engine/ad-system/ad_system.py compare CREATIVE_ID_A CREATIVE_ID_B
```

Next briefs carry the exact parent revision, decision, evidence and fixed/changed variables; they do not silently inherit a finished script, assets or approval. Valid-test coverage measures positive-spend/impression, exact-ID attributable delivery among exported creatives. It does not assert sample sufficiency or causality. Editing time is nullable and reworks are recorded counts.

## Integration boundary

The installed `ad-system` skill coordinates existing specialists. Production routes remain GPT Image 2, Google Omni, Cut Room and DaVinci Resolve under current workspace/user instructions. Work packets include actual context, narration, evidence, scene reasons, artifact paths, readiness and receipt requirements. TikTok extreme is a specialization, not every concept's medium.

No new provider client, auto-launcher, paid generation, social posting or external sheet update is hidden behind the UI. Exact external operations require the currently available connection and the user's authorized scope. Existing folders, boards and old scripts remain unchanged. Legacy performance is inventoried but not imported as attributable Motilli results.

The local service binds to loopback, rejects nonlocal hosts and requires its session token for mutations. File links are confined to creative artifact roots; hidden files and symlink escapes are rejected. This is a personal local tool, not a hosted multi-user deployment or an authorization system for third parties.

## Validation

```sh
python3 -m unittest discover -s _engine/ad-system/tests -v
python3 _engine/ad-system/tests/browser_smoke.py
node --check _engine/ad-system/static/app.js
```

Tests use temporary databases and synthetic data only. Browser smoke writes only to an isolated test server; the live Motilli workspace is inspected read-only. The live application must be started first for the inventory checks. Synthetic fixtures never enter the production database.

## Obsidian and shared agent memory

This workspace is already the Obsidian vault. `data/memory/INDEX.md` links brand → creative → agent notes, plus original evidence, plans, task receipts, decisions and performance sources. The vault Dashboard and HOME now link this index. Obsidian does not need to be running for agents to read the Markdown.

Every committed system event through the UI/CLI refreshes the generated notes from a consistent database snapshot. Per-vault file locking serializes competing writers, individual files replace atomically, and `sync-state.json` reports freshness or conflicts. No background daemon or separate Obsidian plugin is required. Failed memory writes do not undo or misreport an already committed creative change; the error is exposed in service health and can be repaired with `memory-sync`. Manually altered generated files are preserved and flagged instead of overwritten. Keep editable commentary in `data/memory/notes/<creative-id>.md`; those files are never regenerated.

```sh
python3 _engine/ad-system/ad_system.py context MOT-UGC-YAPPER-01
python3 _engine/ad-system/ad_system.py memory-search "presenter" --brand motilli
python3 _engine/ad-system/ad_system.py remember MOT-UGC-YAPPER-01 path/to/note.txt --source "Original source/date" --kind observation
python3 _engine/ad-system/ad_system.py memory-sync
```

`context` refreshes the projection and retrieves current agent notes, record revision, strategy, decisions and work handles. `memory-search` scopes retrieval to creative and agent notes, optionally by brand, and returns source paths/excerpts. Work packets include memory links and note snapshots; agent startup instructions require rereading current notes when resuming older work. Structured claims, approvals, script choices and performance decisions still use their versioned system commands.

The Memory tab reads these same files and appends notes with source/kind. Direct edits in Obsidian's separate agent-note files appear on the next context/search/Memory read. All generated links are vault-relative so the Markdown can travel through the existing knowledge mirror. The remote Hermes sync has not been run as part of this local integration; remote agents must check mirror freshness and must not initialize an empty competing database. The context/search/remember commands fall back to Markdown when the database is absent; memory-sync refuses to regenerate a mirror from nothing. Existing mirror eligibility was checked for these Markdown files.
