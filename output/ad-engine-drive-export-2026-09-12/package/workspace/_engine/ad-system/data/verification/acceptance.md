# Implementation acceptance — September 11, 2026

Built against `_engine/ad-system/BUILD-PLAN.md`. This completes the organizing/operating-system build, not a new paid ad batch or campaign launch.

| Requirement | Implemented and verified evidence |
|---|---|
| 1. Persistent hub, CLI, versions and work queue | Local UI at 127.0.0.1:8791; SQLite snapshots/events; expected-revision conflicts tested; real server stop/start preserved 11 records. Task dependencies, idempotent queue and reconciliation tested. |
| 2. Connected creative lifecycle | Brief, Story, Assets, Work, Review, Results, Library and History interfaces. Browser exercised create/save → hook → work packet/start → QA → decision → child brief in an isolated database. |
| 3. Concepts, hook tests and evidence fidelity | Argument/format comparison with caveat; exact parent revision; hook line/visual/test fields; verbatim quote/source check; hypotheses separate from product facts; claim support and relevance flags. Automated tests exercised quote mismatch and format-only comparison. |
| 4. Planning and existing routes | Production tasks require saved plan and executable scene fields. Packets name current specialist instructions and GPT Image 2 / Google Omni / Cut Room / DaVinci Resolve. TikTok is conditional on that sourcing treatment. Actual external handles and output receipts required; no hidden external job launcher. |
| 5. Specific QA, actual-media review and exact exports | PASS/FLAG/FAIL reports field/reason/fix. Human review records actual media path/hash, reviewer/observations and content version. Changed media/content invalidate reviews; ready/live content edits return to review. Stage-only bookkeeping preserves review. Exact export bindings reject rebinding/changed bytes; tests cover these transitions. |
| 6. Sourcing calibration | Reviewed/accepted counts, gap notes, next action, valid count bounds and zero-yield flag. TikTok action match, EV5, rawness and complete clean-text audit gates remain separate; wrong/unknown action fails. No automatic standard relaxation or generation substitution. |
| 7. Reliable reporting | CSV originals/settings/error audits preserved; stable ad-ID/export joins; atomic duplicate/header/overlap/mixed-setting rejection; totals-based ratios; null missing/zero denominators; unmatched rows rejoin later; wrong-brand binding rejected. All exercised with synthetic temporary data. |
| 8. Results → next brief | Decisions require observation, interpretation, alternatives, next test, fixed/changed variables and matched source rows or insufficient_evidence. Exact source export/revision retained. New brief preserves lineage/evidence while leaving script/assets unselected. Unit and browser tests passed. |
| 9. Real Motilli inventory | 11 discovered creative projects, 126 related creative artifacts, 691 context files: 817 indexed paths total at verification. Source originals unchanged. Yapper README/full-ad v12 vs v24 presenter scope recorded as an observed document conflict. One real research/reconciliation work packet prepared. Legacy performance explicitly not imported. |
| 10. Operations | Recorded editing minutes with missingness, rework count, exported/attributable creative counts and coverage from exact joins. Coverage explicitly measures trackable delivery, not statistically sufficient tests. Unit tests verify absent and matched data behavior. |
| 11. Operating skill, docs and verification | `~/.codex/skills/ad-system/SKILL.md`, workspace `.claude`/`.agents` symlinks, skill validator passed. README/SCHEMA/user guide/templates/run-and-backup commands delivered. 21 tests passed; browser smoke passed; actual rendered screenshots inspected; no browser JavaScript errors. |

## Verification artifacts

- `unit-tests.txt`: 21 passing lifecycle/API/inventory tests.
- `browser-smoke.json`: actual interface flow results from isolated writable fixture plus read-only live inventory checks.
- `ad-studio-overview.png`, `ad-studio-library.png`: actual local interface screenshots, visually inspected.
- `backup-check.json`: backup file/integrity and contained creative counts (written after backup verification).
- `runtime-check.json`: live service identity, record count and response checks.

## Practical limits

The Codex in-app browser connection failed during bootstrap (`sandboxPolicy` missing). Verification used a separate local headless Chromium browser already available in the environment. No claim is made that the in-app browser connection was fixed.

The hub prepares actionable specialist work packets and tracks actual receipts. It does not itself call paid providers, publish Cut Room boards, operate Resolve, source an ad batch, send messages or launch campaigns. Those operations continue through the existing skills and currently verified connections when requested.

No real campaign reporting was imported: current database has zero registered exports and zero measurement imports. Existing export-candidate files remain discoverable. This accurately describes registration status, not an assertion that the workspace has never rendered an ad. Current approvals, script selections and scientific claims are not inferred from old filenames/status documents.

Automated review checks record structure and explicit evidence fields; it cannot certify source truth, rights, visual meaning, clinical efficacy or future conversion performance. Performance joins preserve attribution context and exact source versions; observational metrics alone do not establish causality.

## Corrections made during verification

Fixed import SQL arity, metadata-only review invalidation, stage bypasses/stale live content, wrong-brand joins, duplicate CSV headers, exact TikTok action-match checks and immediate server restart after a closed socket. Final tests include these behaviors. Original brand files and existing production tools remain intact.
