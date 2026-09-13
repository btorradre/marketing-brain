# AI ad system — implementation and acceptance plan

Build requested September 11, 2026, following the supplied ad-machine article and the recommendation to organize existing capabilities around one creative record. Motilli is the first brand; the data model and routing support other brands without weakening their own rules.

## Required outcomes

1. A usable local creative hub and command line, with persistent versioned creative records, event history, optimistic concurrency, and recoverable work queues.
2. Connected research, evidence, concepts, scripts/hooks, line-by-line scene rationale, asset provenance, production handoffs, QA, exact export/ad-ID mapping, performance, decisions and the next brief.
3. Explicit concept-versus-iteration distinctions and a comparison view. Every hook states its test. Observations, hypotheses, customer quotations and verified claims stay separate. A quote must match its source excerpt exactly.
4. Production planning precedes production. Existing specialist skills, GPT Image 2, Google Omni, Cut Room and DaVinci Resolve remain the execution routes. No old provider/editor defaults are inherited. The hub does not claim a board, media generation, editor operation or campaign launch merely from a status update.
5. Deterministic PASS / FLAG / FAIL checks identify the exact field/beat, reason and correction. Actual media QA is a separate evidenced review. Revisions invalidate outdated reviews and export mappings never float to a later version.
6. Sourcing calibration records sample size/yield and whether gaps were reviewed before scaling. It surfaces mismatches without changing the user's EV5/no-text requirements or silently authorizing generation.
7. Performance import preserves brand/account, dates, currency, attribution, conversion event and metric definitions. Joins use platform ad IDs bound to exact immutable exports; reject ambiguous/duplicate/overlapping rows and mixed reporting settings. Calculate ratios from totals, with missing denominators reported as missing rather than invented zeros. Save unmatched rows explicitly and permit rejoining after ID mapping.
8. Decisions reference performance rows and exact creative versions, distinguish observation from interpretation, name alternatives and define the next test's fixed/changed variables. Carry the decision into its next brief. No automatic causal or winning-ad claims.
9. Import a real Motilli workspace inventory conservatively, attach source paths/boards/scripts as discovered artifacts, and flag uncertain current versions/approvals. Preserve existing files and all historical drafts. Inventory legacy performance without passing it off as attributable Motilli results.
10. Operational metrics: recorded edit time, rework and valid-test coverage with explicit definitions and missing-data treatment.
11. Install one operating skill that uses the hub and existing specialist skills. Deliver instructions, a working local URL, real seeded records and meaningful automated/runtime verification.

## Boundary

This builds the organizing and operating system. It does not commission a new ad batch, generate paid media, contact creators, publish boards, edit existing ad assets, launch campaigns or fabricate campaign results. Those actions run through existing authorized workflows when requested. The hub prepares actionable briefs/work packets, tracks real receipts and preserves provenance.

## Implementation

- Python standard-library SQLite backend; JSON revision snapshots and append-only event history.
- Local HTTP API and browser interface on loopback; no third-party dashboard service.
- Import/export commands, resumable tasks with explicit external handles, repeatable QA and performance/decision logic.
- Motilli workspace inventory and context profile, with real file links and source verification status.

## Verification

Use isolated temporary databases for lifecycle tests. Exercise quotation fidelity, missing scene reasons, locked narration, stale reviews, stale writes, immutable export/ad joins, duplicate/mixed/overlapping metrics, aggregation, zero denominators, decision lineage, interrupted task reconciliation and path containment. Test HTTP mutations, restart persistence and the rendered UI. Keep synthetic campaign fixtures out of the live Motilli database. Finish with a requirement-by-requirement completion audit against this plan.
