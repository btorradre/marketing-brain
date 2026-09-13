---
name: n8n-workflow-patterns
description: Reference for designing the structure of an n8n workflow — which trigger to start from, what sequence of nodes to put between the trigger and the final action, and how to handle errors, batching, pagination, and security for each major category of automation. Use this whenever building a new n8n workflow, choosing between workflow architectures, or planning how a webhook, API integration, database sync, AI agent, or scheduled job should be structured before wiring up individual nodes. Covers six core architectural patterns — webhook processing, HTTP/API integration, database operations, AI agent workflows, scheduled tasks, and batch processing — each with the trigger→transform→action shape that works, the common node sequences, and the error-handling and security conventions that keep it production-safe.
---

# n8n Workflow Architecture Patterns

## How to Use This

1. **Identify which of the six core patterns fits the request.** Match the automation need to a pattern:
   - **Webhook Processing** — receiving data from external systems, building integrations (Slack commands, form submissions, GitHub webhooks), needing an instant response to an event. Example: "Receive Stripe payment webhook → Update database → Send confirmation." This is the most common workflow pattern overall. Full detail in `references/webhook-processing.md`.
   - **HTTP API Integration** — fetching data from external APIs, synchronizing with third-party services, building data pipelines. Example: "Fetch GitHub issues → Transform → Create Jira tickets." Full detail in `references/http-api-integration.md`.
   - **Database Operations** — syncing between databases, running database queries on a schedule, ETL workflows. Example: "Read Postgres records → Transform → Write to MySQL." Full detail in `references/database-operations.md`.
   - **AI Agent Workflow** — building conversational AI, needing AI with tool access, multi-step reasoning tasks. Example: "Chat with AI that can search docs, query a database, send emails." Full detail in `references/ai-agent-workflows.md`.
   - **Scheduled Tasks** — recurring reports or summaries, periodic data fetching, maintenance tasks. Example: "Daily: fetch analytics → generate report → email team." Full detail in `references/scheduled-tasks.md`.
   - **Batch Processing** — processing large datasets that exceed API batch limits, needing to accumulate results across multiple API calls, nested loops (e.g. multiple categories × paginated API calls per category). Example: "Fetch products for 4 markets × 1000 per API call → aggregate all results." Covered below.
   - Many real workflows combine two or more of these (e.g. a webhook that triggers an AI agent that writes to a database) — pick the dominant pattern for the overall shape, then borrow sub-patterns (batching, pagination, auth) from the others as needed.

2. **Sketch the data flow shape before picking individual nodes.** Every workflow is one of five shapes:
   - **Linear**: `Trigger → Transform → Action → End` — use for simple workflows with a single path.
   - **Branching**: `Trigger → IF → [True Path] / [False Path]` — use when different actions depend on a condition.
   - **Parallel**: `Trigger → [Branch 1] → Merge` / `→ [Branch 2] ↗` — use for independent operations that can run simultaneously.
   - **Loop**: `Trigger → Split in Batches → Process → Loop (until done)` — use for processing large datasets in chunks.
   - **Error Handler**: `Main Flow → [Success Path]` / `→ [Error Trigger → Error Handler]` — use when you need a separate error-handling workflow.

3. **Lay out the common building blocks** that every pattern is assembled from:
   - **Triggers**: Webhook (HTTP endpoint, instant), Schedule (cron-based, periodic), Manual (click to execute, for testing), Polling (check for changes at intervals).
   - **Data sources**: HTTP Request (REST APIs), database nodes (Postgres, MySQL, MongoDB), service-specific nodes (Slack, Google Sheets, etc.), Code (custom logic).
   - **Transformation**: Set (map/transform fields), Code (complex logic), IF/Switch (conditional routing), Merge (combine data streams).
   - **Outputs**: HTTP Request (call APIs), database writes, communication (email, Slack, Discord), storage (files, cloud storage).
   - **Error handling**: an Error Trigger workflow to catch failures, IF nodes to check error conditions, Stop-and-Error nodes for explicit failure, and the per-node "Continue On Fail" setting.

4. **Work through the four-phase build checklist** for whichever pattern you picked (per-category checklists live in each reference file):
   - **Planning** — identify the pattern; list the node types you'll need; map out the data flow (input → transform → output); decide the error-handling strategy up front.
   - **Implementation** — build the trigger; add data-source nodes; configure authentication/credentials properly (never hardcode secrets in parameters); add transformation nodes (Set, Code, IF); add output/action nodes; wire up error handling.
   - **Validation** — check each node's configuration is complete and correct; check the workflow as a whole for structural problems (dangling connections, missing error paths); test with realistic sample data; deliberately test edge cases (empty data, malformed data, errors).
   - **Deployment** — review workflow-level settings (execution order, timeout, error-handling behavior); turn the workflow on (note: activation typically requires the n8n UI or an authenticated API call — it is a manual step, not something a workflow can do to itself); watch the first several live executions closely; write down what the workflow does and how data flows through it so the next person doesn't have to reverse-engineer it.

5. **For anything involving expressions, specific node configuration options, or workflow-structure validation**, treat this document as the architecture layer and pair it with the adjacent domain: expression syntax and `{{ }}` templating, node-specific configuration detail, and structural workflow validation each have their own dedicated reference. If the workflow needs a Code node anywhere, see the dedicated JavaScript or Python Code node reference for how to write the code itself — this document only covers where the Code node sits in the overall shape.

6. **Before finishing, run the workflow through the cross-cutting checklists below** — the batch-processing pattern, the integration-specific gotchas (Google Sheets, Google Drive), the general common-gotchas list, and the best-practices Do/Don't list all apply regardless of which of the six patterns you built.

## Batch Processing Pattern

**SplitInBatches loop.** The SplitInBatches node splits a large dataset into smaller chunks for processing. Understanding its two outputs is critical:

- `main[0]` = **done** — fires ONCE, after all batches complete.
- `main[1]` = **each batch** — fires per batch (this is the loop body).

```
Prepare Items → SplitInBatches → [main[1]: Process Batch] → (loops back)
                                  [main[0]: Done] → Limit 1 → Aggregate
```

Always add a **Limit 1** node after the done output as a safety net against edge cases where it fires with extra items.

**Cross-iteration data.** After the loop, referencing a node inside the loop and asking for all of its items returns **only the last batch's items** — this silently drops data from every batch but the final one. To accumulate across all iterations, use workflow static data in a Code node inside the loop: reset the accumulator before the loop starts, push into it on every iteration inside the loop body, and read the full accumulated set only after the loop's done output fires.

**Nested loops.** When processing N categories × M items per category (where an API has a per-call batch limit):

```
Define Categories (N items)
  → Outer Loop (SplitInBatches, batchSize=1)
    → Prepare category data
    → Inner Loop (SplitInBatches, batchSize=1000)
      → API Call → Verify → (loops back to Inner Loop via main[1])
    → Inner done[0] → Rate Limit Delay → back to Outer Loop
  → Outer done[0] → Limit 1 → Final Aggregate
```

**Wiring gotcha**: the inner loop's done[0] output must connect back to the OUTER loop's input, not to the final aggregate. The outer loop's done[0] is what feeds the final aggregate.

**API pagination.** For APIs without multi-ID filtering, use an `id_from` cursor plus date windowing for efficient pagination:

```
Schedule → Set Date Window → Fetch Page → Process
  → IF has more? → [true] Update id_from → Fetch Page (loop)
                  → [false] → Aggregate → Output
```

**Dry-run / verification tolerance.** When testing with API-write nodes disabled (for dry runs), downstream verification nodes receive the request body instead of the response. Make verification tolerant of that:

```javascript
// In verification Code node
const body = $input.first().json;
const looksLikeRequest = body.method && body.parameters && !body.status;
if (looksLikeRequest) {
  return [{ json: { status: 'SKIPPED', message: 'Upstream disabled for testing' }}];
}
// Normal response verification below...
```

## Integration-Specific Gotchas

**Google Sheets**
- **NEVER use `append`** on sheets with formula columns — it breaks formulas. Use the Google Sheets API's `values.update` (PUT) via an HTTP Request node with Google API credentials instead.
- **Write numbers, not strings** for formula-dependent columns — a string `"4.98"` breaks `ADD()` formulas. Use `parseFloat()` in a Code node before writing.
- **Per-item execution trap**: Google Sheets nodes execute once per input item. If you need a single bulk write, aggregate items into one item in a Code node first.
- **UNFORMATTED_VALUE returns numbers**, not text like `"N/A"` — filter explicitly in Code nodes rather than assuming a placeholder string.

**Google Drive**
- **`convertToGoogleDocument: true` creates a Google Doc (text)**, NOT a Google Sheet — to upload a CSV that stays downloadable as a CSV, omit this option entirely.
- **CSV download link format**: `https://drive.google.com/uc?id={fileId}&export=download` — use this instead of the standard `/view` link when you want a direct download.

**Bidirectional threshold checking.** When comparing values (prices, quantities, metrics), always check both directions of change:

```javascript
// ❌ Only catches increases
if (diff > threshold) { flag(); }

// ✅ Catches both spikes AND crashes — both are data-quality signals
if (Math.abs(diff) > threshold) { flag(); }
```

## Common Gotchas (All Patterns)

**1. Webhook data structure.** Can't access webhook payload data directly — it's nested under `.body`.
```javascript
❌ {{$json.email}}
✅ {{$json.body.email}}
```

**2. Multiple input items.** A node processes all input items by default, but sometimes you only want one — use "Execute Once" mode, or reference just the first item explicitly (e.g. `{{$json[0].field}}` for the first item only).

**3. Authentication issues (401/403 on API calls).** Configure credentials properly through the credentials system, not as plain parameters, and test credentials before activating the workflow.

**4. Node execution order.** If nodes execute in an unexpected order, check the workflow's Execution Order setting: v0 is legacy top-to-bottom ordering; v1 is connection-based and is the recommended setting.

**5. Expression errors (expressions showing as literal text).** Make sure the expression is actually wrapped in `{{ }}`.

## Workflow Creation Checklist

Apply this checklist to every workflow, regardless of pattern:

**Planning Phase**
- [ ] Identify the pattern (webhook, API, database, AI, scheduled, batch)
- [ ] List the node types the workflow will need
- [ ] Understand the data flow (input → transform → output)
- [ ] Plan the error-handling strategy

**Implementation Phase**
- [ ] Create the workflow with the appropriate trigger
- [ ] Add data-source nodes
- [ ] Configure authentication/credentials
- [ ] Add transformation nodes (Set, Code, IF)
- [ ] Add output/action nodes
- [ ] Configure error handling

**Validation Phase**
- [ ] Validate each node's configuration
- [ ] Validate the complete workflow structure
- [ ] Test with sample data
- [ ] Handle edge cases (empty data, errors)

**Deployment Phase**
- [ ] Review workflow settings (execution order, timeout, error handling)
- [ ] Activate the workflow (⚠️ this is typically a manual step in the n8n UI — it usually cannot be done by the workflow itself, or via a generic API write)
- [ ] Monitor the first executions closely
- [ ] Document the workflow's purpose and data flow

## Best Practices

**Do**
- Start with the simplest pattern that solves the problem
- Plan the workflow structure before building it
- Use error handling on every workflow
- Test with sample data before activation
- Follow the workflow creation checklist
- Use descriptive node names
- Document complex workflows (use the node/workflow notes field)
- Monitor workflow executions after deployment

**Don't**
- Build the entire workflow in one shot without checking intermediate results — iterate step by step
- Skip validation before activation
- Ignore error scenarios
- Use complex patterns when simple ones suffice
- Hardcode credentials in node parameters
- Forget to handle empty-data cases
- Mix multiple patterns without clear boundaries between them
- Deploy without testing

## Reference Files

Each of the six core patterns has a dedicated reference file with common use cases (worked examples), configuration templates, error-handling patterns, performance optimization, security considerations, common gotchas, and a pattern-specific checklist:

- `references/ai-agent-workflows.md` — the 8 AI connection types, tool configuration (including making any node a tool, MCP Client Tool, sub-agents), memory configuration, agent types, prompt engineering, security (treating tool output as untrusted input), and testing.
- `references/database-operations.md` — Postgres/MySQL/MongoDB node configuration, batch processing and pagination patterns, transaction handling, schema mapping, and security (parameterized queries, least privilege).
- `references/http-api-integration.md` — authentication methods, pagination patterns, rate limiting, request configuration by method, error-handling patterns (retry, fallback API, circuit breaker), and response transformation.
- `references/scheduled-tasks.md` — schedule configuration (interval/cron/days & hours), timezone handling, error handling, performance (locking against overlapping runs), and monitoring/logging patterns.
- `references/webhook-processing.md` — webhook data structure, authentication and security (signature verification), response modes (onReceived vs lastNode), error handling, and testing.
