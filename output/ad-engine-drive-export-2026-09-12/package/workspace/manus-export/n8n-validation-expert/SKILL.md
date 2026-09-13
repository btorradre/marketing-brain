---
name: n8n-validation-expert
description: Guide for interpreting and fixing n8n validation errors and warnings — on individual nodes and on whole workflows. Use this whenever you've configured an n8n node or workflow and need to check it against n8n's validation rules, whenever a validation check comes back with errors or warnings that need to be understood and triaged, or whenever you're not sure whether a warning is a real problem or a false positive that's fine to leave alone. Covers severity levels, standard error types with fixes, standard false-positive warnings and when each is genuinely acceptable, and the judgment calls for working through validation results systematically instead of guessing.
---

# n8n Workflow Validation

## How to Use This

1. **Treat validation as iterative, not one-shot.** Build or adjust a node's configuration, check it against validation rules, read the errors and warnings carefully, fix what's needed, and check again. Expect roughly 2-3 rounds of this before a node or workflow comes back clean — that's the normal pattern, not a sign something is badly wrong.

2. **Sort every finding into one of three buckets by severity:**
   - **Errors — must fix.** These block execution. The workflow cannot run correctly, or cannot be activated, until they're resolved.
   - **Warnings — should fix.** These don't block execution but flag something that might be a real issue. Evaluate each one on its own merits rather than fixing or ignoring all of them by default.
   - **Suggestions — optional.** Nice-to-have improvements. Never required.

3. **Fix every error before doing anything else.** Errors mean the workflow literally cannot run correctly: a required field wasn't provided, a value doesn't match what's allowed, a value is the wrong data type, an expression has a syntax error, or something references a node that doesn't exist. See `references/error-catalog.md` for each type and its fix.

4. **Run every warning through a decision framework instead of reflexively fixing or ignoring it:**
   - Is it a security warning (hardcoded credentials, an unvalidated public-facing webhook)? → Always fix.
   - Is this a production or business-critical workflow? → Lean toward fixing.
   - Does it touch critical data (payments, customer records, orders)? → Fix it.
   - Is there a known, deliberate reason the underlying risk doesn't apply here (e.g. the API already retries internally, the dataset is small and known, this is a dev/test workflow)? → Accepting it is fine.

   See `references/false-positives.md` for the specific, common warnings that fall into "often acceptable" and exactly when.

5. **When you accept a warning instead of fixing it, write down why**, next to the configuration (a comment, a note in the brief, whatever the project already uses). That way nobody re-litigates it later, and nobody "fixes" something that was left that way on purpose.

6. **Match your rigor to the stage of the build:**
   - Quick edits / early iteration → check only the essentials (required fields, basic structure); don't get distracted by best-practice nits yet.
   - Pre-deployment → check required fields, value types, allowed values, and basic dependencies. This is the right default level for most situations.
   - Reviewing an AI-generated configuration → be more tolerant of minor stylistic issues; focus on genuine correctness problems.
   - Production / business-critical workflow → check everything, including best practices, performance, and security. Expect more warnings to *review* — not necessarily more to *fix*.

7. **Before configuring an unfamiliar node, look up what it actually requires** rather than guessing. Most "missing required field" and "invalid value" errors are really a documentation-lookup problem: check that node type's field list for which properties are marked required and what values/format each one accepts.

8. **After the individual nodes are clean, validate the workflow as a whole:**
   - Every node's configuration is valid on its own.
   - Every connection points to a node that actually exists (no stale references to renamed or deleted nodes).
   - Every expression has valid syntax and valid node/field references.
   - The overall flow makes sense: one clear entry point, no accidental circular dependencies, no nodes left disconnected from the flow.

9. **Trust n8n's own save-time normalization for IF/Switch operator structure** — n8n automatically corrects certain structural issues (like the `singleValue` flag, or IF/Switch metadata) when a workflow is saved. Don't hand-fix these; just save and re-check to confirm they cleared. See "Operator structure" below.

10. **If a node comes back with a wall of errors, don't try to fix everything at once.** Strip the configuration back to a minimal valid version (just the required fields), confirm that passes, then re-add features one at a time, checking after each addition, until you're back to the full intended configuration.

11. **If a workflow validates cleanly but runs incorrectly, isolate the problem with a binary search:** disable or remove roughly half the nodes, re-test. If the problem disappears, it's in the half you removed; if it persists, it's in the half you kept. Repeat on the remaining half until the fault is isolated.

12. **For "node not found" / stale-reference problems** (a node was renamed or deleted, but a connection or an expression still points to its old name): either update every reference to the correct current node name, or remove the dangling connection/expression entirely.

## Error Severity and Type Overview

| Error type | Priority | Severity | Auto-fixed by n8n on save? |
|---|---|---|---|
| `missing_required` | Highest | Error | No |
| `invalid_value` | High | Error | No |
| `type_mismatch` | Medium | Error | No |
| `invalid_expression` | Medium | Error | No |
| `invalid_reference` | Low | Error | No |
| `operator_structure` | Lowest | Warning | Yes |

Rough real-world frequency, most to least common: `missing_required` (~45% of all errors), `invalid_value` (~28%), `type_mismatch` (~12%), `invalid_expression` (~8%), `invalid_reference` (~5%).

For the full catalog of these five error types — with concrete broken/fixed examples for each — plus the three warning types (`best_practice`, `deprecated`, `performance`), see `references/error-catalog.md`.

## Operator Structure — Automatically Corrected, Don't Hand-Fix

`operator_structure` issues on IF/Switch nodes are rare in practice because n8n normalizes them itself when the workflow is saved. Trust this and don't waste time manually "fixing" these — if you see the warning, just save and re-check.

**Binary operators** (`equals`, `notEquals`, `contains`, `notContains`, `greaterThan`, `lessThan`, `startsWith`, `endsWith`) compare two values and should NOT carry a `singleValue` flag. If mistakenly included, n8n removes it on save.

**Unary operators** (`isEmpty`, `isNotEmpty`, `true`, `false`) check a single value and DO need `singleValue: true`. If it's missing, n8n adds it on save.

n8n also fills in the complete `conditions.options` metadata for IF (v2.2+) and Switch (v3.2+) nodes automatically on save — if a validation check flags this metadata as missing before you've saved, it's a known false positive, not a real problem (see `references/false-positives.md`).

## Editing a Specific Field's Text Directly (e.g. a Code Node Script, or a Long Expression)

When making a targeted find-and-replace style edit inside one field of a node's configuration (rather than rewriting the whole field), three failure modes come up consistently:

1. **The exact text you're searching for isn't found.** This usually means the content already changed since you last looked at it, or your search string has a typo/whitespace mismatch. Re-read the field's *current* value before retrying — don't assume it still matches what you remember. Whitespace and line endings matter; if you're not sure they'll match exactly, search more loosely (e.g. treat runs of whitespace as flexible) rather than requiring an exact character match.
2. **The text you're searching for appears more than once, and it's unclear which one you mean.** Either broaden your intent to "replace every occurrence" deliberately, or make the search string more specific (include a bit more surrounding context) so it can only match the one location you actually want.
3. **A regex search pattern is unsafe or malformed.** Nested quantifiers like `(a+)+` and overlapping alternations like `(\w|\d)+` should be avoided — they're classic catastrophic-backtracking (ReDoS) patterns that can hang. Keep patterns simple and specific.

## Common Workflow-Level (Structural) Errors

Beyond individual node configs, a workflow as a whole should also be checked for:

1. **Broken connections** — a connection whose source or target node doesn't exist. Fix: remove the stale connection, or create the missing node.
2. **Circular dependencies** — a loop in the node graph that isn't an intentional loop construct. Fix: restructure the workflow to remove the loop.
3. **Multiple start/trigger nodes** — only one will actually execute. Fix: remove the extra trigger(s), or split into separate workflows.
4. **Disconnected nodes** — a node that exists but isn't wired into the flow at all. Fix: connect it, or remove it if it's unused.

## Rigor-by-Context Cheat Sheet

- **Quick automations:** be tolerant of most warnings; fix only errors plus security warnings.
- **Business-critical workflows:** apply maximum rigor; accept very few warnings; fix everything you reasonably can.
- **Integration testing:** accept essentially all warnings; fix only errors that actually prevent execution.

## Decision Framework for Any Individual Warning

```
Is it a SECURITY warning?
  YES → always fix
  NO  → continue

Is this a production workflow?
  YES → continue
  NO  → probably acceptable

Does it handle critical data?
  YES → fix the warning
  NO  → continue

Is there a known, deliberate workaround?
  YES → acceptable, if documented
  NO  → fix the warning
```

## Summary: What to Always/Usually/Often/Always Accept

- **Always fix:** security warnings, hardcoded real credentials, SQL-injection risks, any error (not warning) on a production workflow.
- **Usually fix:** missing error handling (in production), missing retry logic (on external APIs), missing input validation (on public webhooks), missing rate limiting (on high-volume calls).
- **Often acceptable:** missing error handling (dev/test), missing retry logic (internal/idempotent APIs), missing rate limiting (low volume), unbounded queries (small known datasets).
- **Always acceptable:** known quirks (see `references/false-positives.md`), anything n8n's own save-time normalization handles automatically, metadata-completeness warnings that resolve on save.

**Golden rule: if you accept a warning instead of fixing it, document why.**

For the full false-positives catalog (missing error handling, no retry logic, missing rate limiting, unbounded database queries, missing input validation, hardcoded credentials — each with when-acceptable and when-to-fix examples) plus the known quirks that look like errors but aren't, see `references/false-positives.md`.

## Working a Validation Report

However the check is actually run — n8n's own workflow editor, an automated lint pass, or manual review against this catalog — organize the result the same way: a flat list of errors, a flat list of warnings, an optional list of suggestions, and a short summary count. For example:

```json
{
  "valid": false,
  "errors": [
    {
      "type": "missing_required",
      "property": "channel",
      "message": "Channel name is required",
      "fix": "Provide a channel name (lowercase, no spaces)"
    }
  ],
  "warnings": [
    {
      "type": "best_practice",
      "property": "errorHandling",
      "message": "Slack API can have rate limits",
      "suggestion": "Add onError: 'continueRegularOutput'"
    }
  ],
  "suggestions": [
    { "type": "optimization", "message": "Consider using batch operations for multiple messages" }
  ],
  "summary": { "hasErrors": true, "errorCount": 1, "warningCount": 1, "suggestionCount": 1 }
}
```

How to work through it:
1. Check whether it's valid overall — if not, there's at least one error that must be fixed before deployment.
2. Fix every error first: for each one, note the field it's on, the message, and the suggested fix, then apply it.
3. Review every warning individually and decide, using the decision framework above, whether it's acceptable here or needs fixing.
4. Consider suggestions last — they're optional polish, never blocking.

## Progressive Validation — Building Up a Config Incrementally

When a configuration has many errors at once, don't try to fix them all simultaneously. Start minimal and valid, then add complexity one piece at a time, checking after each addition:

```
Step 1 — minimal valid config:
{ "resource": "message", "operation": "post", "channel": "#general", "text": "Hello" }
→ check → valid

Step 2 — add a feature, check again:
config.attachments = [...]
→ check

Step 3 — add another feature, check again:
config.blocks = [...]
→ check
```

## Documenting an Accepted Warning

When you decide a warning doesn't need fixing, record the decision next to the configuration so it's not silently "corrected" later by someone who doesn't have the context:

```json
// workflows/customer-notifications.json
{
  "nodes": [{
    "name": "Send Slack Notification",
    "type": "n8n-nodes-base.slack",
    "parameters": {
      "channel": "#notifications"
      // ACCEPTED WARNING: No error handling
      // Reason: Non-critical notification, failures are acceptable
      // Reviewed: 2025-10-20
      // Reviewer: Engineering Team
    }
  }]
}
```

## Recovery Patterns for Stuck Validations

**Start fresh** — when a configuration is severely broken: note the required fields, build the smallest possible valid configuration, then add features incrementally, checking after each one.

**Binary search** — when a workflow validates but produces wrong results at runtime: remove roughly half the nodes and re-test; if it now works, the fault was in the removed half, if it still fails, the fault is in the remaining half; repeat on that half until isolated.

**Clean up stale connections** — when you're seeing "node not found" errors: find every connection or expression referencing the old/missing node name and either point it at the correct current node or delete it.

## Common Auto-Fixable Issue Categories

These categories of problems are mechanical enough that they can usually just be corrected directly, rather than needing deep investigation:

1. **Expression missing its `=` prefix** — e.g. `{{ $json.field }}` should be `={{ $json.field }}`. Safe to just fix directly.
2. **`typeVersion` beyond what's actually supported** — downgrade to the highest version that node type actually supports.
3. **Conflicting `onError` settings** — remove the conflicting/redundant one.
4. **Unknown or misspelled node type** — correct it to the closest valid node type name; double-check the match is right before applying it if it's not an obvious typo.
5. **Webhook node missing a path** — generate a unique path (e.g. a UUID) for it.
6. **`typeVersion` behind the latest available** — upgrade, but check whether the newer version changed the shape of any fields, and migrate the configuration accordingly rather than assuming it's a drop-in change.
7. **Breaking changes between versions that don't have a mechanical fix** — these need a manual read of what changed and a deliberate migration; don't try to force an automatic fix here.

Treat 1-2 and 5 as safe to just apply. Treat 3-4 as worth a quick sanity check before applying. Treat 6-7 as needing an actual read of what changed before you touch anything.
