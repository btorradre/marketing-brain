# n8n Workflow Validation

Guide for interpreting and fixing n8n validation errors and warnings — on individual nodes and on whole workflows. Use this whenever you've configured an n8n node or workflow and need to check it against n8n's validation rules, whenever a validation check comes back with errors or warnings that need to be understood and triaged, or whenever you're not sure whether a warning is a real problem or a false positive that's fine to leave alone. It covers the severity levels, the standard error types with their fixes, the standard false-positive warnings and when each is genuinely acceptable, and the judgment calls for working through validation results systematically instead of guessing.

## How to use this

1. **Treat validation as iterative, not one-shot.** Build or adjust a node's configuration, check it against validation rules, read the errors and warnings carefully, fix what's needed, and check again. Expect roughly 2-3 rounds of this before a node or workflow comes back clean — that's the normal pattern, not a sign something is badly wrong.

2. **Sort every finding into one of three buckets by severity:**
   - **Errors — must fix.** These block execution. The workflow cannot run correctly, or cannot be activated, until they're resolved.
   - **Warnings — should fix.** These don't block execution but flag something that might be a real issue. Evaluate each one on its own merits rather than fixing or ignoring all of them by default.
   - **Suggestions — optional.** Nice-to-have improvements. Never required.

3. **Fix every error before doing anything else.** Errors mean the workflow literally cannot run correctly: a required field wasn't provided, a value doesn't match what's allowed, a value is the wrong data type, an expression has a syntax error, or something references a node that doesn't exist. See the Error Catalog below for each type and its fix.

4. **Run every warning through a decision framework instead of reflexively fixing or ignoring it:**
   - Is it a security warning (hardcoded credentials, an unvalidated public-facing webhook)? → Always fix.
   - Is this a production or business-critical workflow? → Lean toward fixing.
   - Does it touch critical data (payments, customer records, orders)? → Fix it.
   - Is there a known, deliberate reason the underlying risk doesn't apply here (e.g. the API already retries internally, the dataset is small and known, this is a dev/test workflow)? → Accepting it is fine.
   
   See the False Positives Catalog below for the specific, common warnings that fall into "often acceptable" and exactly when.

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

9. **Trust n8n's own save-time normalization for IF/Switch operator structure** (see "Operator structure" in the catalog below) — n8n automatically corrects certain structural issues (like the `singleValue` flag, or IF/Switch metadata) when a workflow is saved. Don't hand-fix these; just save and re-check to confirm they cleared.

10. **If a node comes back with a wall of errors, don't try to fix everything at once.** Strip the configuration back to a minimal valid version (just the required fields), confirm that passes, then re-add features one at a time, checking after each addition, until you're back to the full intended configuration.

11. **If a workflow validates cleanly but runs incorrectly, isolate the problem with a binary search:** disable or remove roughly half the nodes, re-test. If the problem disappears, it's in the half you removed; if it persists, it's in the half you kept. Repeat on the remaining half until the fault is isolated.

12. **For "node not found" / stale-reference problems** (a node was renamed or deleted, but a connection or an expression still points to its old name): either update every reference to the correct current node name, or remove the dangling connection/expression entirely.

## Rules & standards

### Error severity and type overview

| Error type | Priority | Severity | Auto-fixed by n8n on save? |
|---|---|---|---|
| `missing_required` | Highest | Error | No |
| `invalid_value` | High | Error | No |
| `type_mismatch` | Medium | Error | No |
| `invalid_expression` | Medium | Error | No |
| `invalid_reference` | Low | Error | No |
| `operator_structure` | Lowest | Warning | Yes |

Rough real-world frequency, most to least common: `missing_required` (~45% of all errors), `invalid_value` (~28%), `type_mismatch` (~12%), `invalid_expression` (~8%), `invalid_reference` (~5%).

---

### Errors (must fix)

#### 1. `missing_required` — a required field wasn't provided

The single most common validation error. Happens most often when creating a new node without filling in every required field, copying a configuration between different operations that have different requirements, or switching a node's operation/resource without updating the fields that go with it.

**Example — Slack channel missing:**
```
Error: { "type": "missing_required", "property": "channel", "message": "Channel name is required", "node": "Slack", "path": "parameters.channel" }

Broken:
{
  "resource": "message",
  "operation": "post"
  // Missing: channel
}

Fix:
{
  "resource": "message",
  "operation": "post",
  "channel": "#general"   // ✅ Added required field
}
```

**Example — HTTP Request missing URL:**
```
Error: { "type": "missing_required", "property": "url", "message": "URL is required for HTTP Request", "node": "HTTP Request", "path": "parameters.url" }

Broken:
{ "method": "GET", "authentication": "none" }   // Missing: url

Fix:
{ "method": "GET", "authentication": "none", "url": "https://api.example.com/data" }
```

**Example — database query missing:**
```
Error: { "type": "missing_required", "property": "query", "message": "SQL query is required", "node": "Postgres", "path": "parameters.query" }

Broken:
{ "operation": "executeQuery" }   // Missing: query

Fix:
{ "operation": "executeQuery", "query": "SELECT * FROM users WHERE active = true" }
```

**Example — conditionally-required field.** Some fields are only required depending on another field's value — these are easy to miss because the base config looks complete:
```
Error: { "type": "missing_required", "property": "body", "message": "Request body is required when sendBody is true", "node": "HTTP Request", "path": "parameters.body" }

Broken:
{
  "method": "POST",
  "url": "https://api.example.com/create",
  "sendBody": true
  // Missing: body (required because sendBody=true)
}

Fix:
{
  "method": "POST",
  "url": "https://api.example.com/create",
  "sendBody": true,
  "body": { "contentType": "json", "content": { "name": "John", "email": "john@example.com" } }
}
```

**How to identify required fields:** check that node type's documentation/field list and look for properties marked required, before guessing at a configuration.

#### 2. `invalid_value` — the value doesn't match an allowed option or format

Second most common error. Usually a wrong enum value, a typo in an operation name, or an invalid format for a specialized field (channel names, emails, URLs).

**Example — invalid operation:**
```
Error: { "type": "invalid_value", "property": "operation", "message": "Operation must be one of: post, update, delete, get", "current": "send", "allowed": ["post","update","delete","get"] }

Broken:  { "resource": "message", "operation": "send" }   // ❌ should be "post"
Fix:     { "resource": "message", "operation": "post" }
```

**Example — invalid HTTP method:**
```
Error: { "type": "invalid_value", "property": "method", "message": "Method must be one of: GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS", "current": "FETCH" }

Broken:  { "method": "FETCH", "url": "https://api.example.com" }
Fix:     { "method": "GET", "url": "https://api.example.com" }
```

**Example — invalid channel format:**
```
Error: { "type": "invalid_value", "property": "channel", "message": "Channel name must start with # and be lowercase (e.g., #general)", "current": "General" }

Broken:  { "resource": "message", "operation": "post", "channel": "General" }
Fix:     { "resource": "message", "operation": "post", "channel": "#general" }
```

**Example — enums are case-sensitive:**
```
Error: { "type": "invalid_value", "property": "resource", "message": "Resource must be one of: channel, message, user, file", "current": "Message", "allowed": ["channel","message","user","file"] }

Broken:  { "resource": "Message", "operation": "post" }   // ❌ capital M
Fix:     { "resource": "message", "operation": "post" }
```

#### 3. `type_mismatch` — wrong data type

Happens most often from hardcoding a value that should be a number as a string, using an expression where a literal is expected, or JSON serialization quirks.

**String instead of number:**
```
Error: { "type": "type_mismatch", "property": "limit", "message": "Expected number, got string", "expected": "number", "current": "100" }
Broken: { "operation": "executeQuery", "query": "SELECT * FROM users", "limit": "100" }
Fix:    { "operation": "executeQuery", "query": "SELECT * FROM users", "limit": 100 }
```

**Number instead of string** (channel names are strings, even if they look like an ID):
```
Error: { "type": "type_mismatch", "property": "channel", "message": "Expected string, got number", "expected": "string", "current": 12345 }
Broken: { "resource": "message", "operation": "post", "channel": 12345 }
Fix:    { "resource": "message", "operation": "post", "channel": "#general" }
```

**Boolean passed as a string:**
```
Error: { "type": "type_mismatch", "property": "sendHeaders", "message": "Expected boolean, got string", "expected": "boolean", "current": "true" }
Broken: { "method": "GET", "url": "https://api.example.com", "sendHeaders": "true" }
Fix:    { "method": "GET", "url": "https://api.example.com", "sendHeaders": true }
```

**Object instead of array:**
```
Error: { "type": "type_mismatch", "property": "tags", "message": "Expected array, got object", "expected": "array", "current": {"tag": "important"} }
Broken: { "name": "New Channel", "tags": {"tag": "important"} }
Fix:    { "name": "New Channel", "tags": ["important", "alerts"] }
```

#### 4. `invalid_expression` — n8n expression syntax error or invalid reference

Moderately common. Usually a missing `{{ }}` wrapper, a typo in a variable or node name, a reference to a field that doesn't exist, or invalid JavaScript inside the expression. See the n8n-expression-syntax reference doc for comprehensive expression guidance.

**Missing curly braces:**
```
Error: { "type": "invalid_expression", "property": "text", "message": "Expressions must be wrapped in {{}}", "current": "$json.name" }
Broken: { "resource": "message", "operation": "post", "channel": "#general", "text": "$json.name" }
Fix:    { "resource": "message", "operation": "post", "channel": "#general", "text": "={{$json.name}}" }
```

**Invalid node reference (typo in node name):**
```
Error: { "type": "invalid_expression", "property": "value", "message": "Referenced node 'HTTP Requets' does not exist", "current": "={{$node['HTTP Requets'].json.data}}" }
Broken: { "field": "data", "value": "={{$node['HTTP Requets'].json.data}}" }
Fix:    { "field": "data", "value": "={{$node['HTTP Request'].json.data}}" }
```

**Invalid property access — structure doesn't exist at runtime:**
```
Error: { "type": "invalid_expression", "property": "text", "message": "Cannot access property 'user' of undefined", "current": "={{$json.data.user.name}}" }
Broken: { "text": "={{$json.data.user.name}}" }
Fix (safe navigation + fallback): { "text": "={{$json.data?.user?.name || 'Unknown'}}" }
```

**Webhook data access error — the classic gotcha.** Webhook data is nested under `.body`:
```
Error: { "type": "invalid_expression", "property": "value", "message": "Property 'email' not found in $json", "current": "={{$json.email}}" }
Broken: { "field": "email", "value": "={{$json.email}}" }              // ❌ missing .body
Fix:    { "field": "email", "value": "={{$json.body.email}}" }         // ✅ webhook data lives under .body
```

#### 5. `invalid_reference` — configuration references a node that doesn't exist in the workflow

Less common. Usually a node was renamed or deleted, there's a typo in a node name, or a configuration was copy-pasted from a different workflow.

**Deleted node reference:**
```
Error: { "type": "invalid_reference", "property": "expression", "message": "Node 'Transform Data' does not exist in workflow", "referenced_node": "Transform Data" }
Broken: { "value": "={{$node['Transform Data'].json.result}}" }

Fix option 1 — update to the existing node:
{ "value": "={{$node['Set'].json.result}}" }

Fix option 2 — remove the expression if it's no longer needed:
{ "value": "default_value" }
```

**Connection pointing at a node that no longer exists:**
```
Error: { "type": "invalid_reference", "message": "Connection references node 'Slack1' which does not exist", "source": "HTTP Request", "target": "Slack1" }
```
**Fix:** remove the stale connection (or recreate a node with that exact name if it was meant to still exist).

**Renamed node, reference not updated:**
```
Error: { "type": "invalid_reference", "property": "expression", "message": "Node 'Get Weather' does not exist (did you mean 'Weather API'?)", "referenced_node": "Get Weather", "suggestions": ["Weather API"] }
Broken: { "value": "={{$node['Get Weather'].json.temperature}}" }
Fix:    { "value": "={{$node['Weather API'].json.temperature}}" }
```

---

### Warnings (should fix — context-dependent)

#### 6. `best_practice` — configuration works but doesn't follow best practice

Doesn't block execution. Acceptable in development/testing/simple workflows; should generally be fixed in production workflows handling important data.

**Missing error handling:**
```
Warning: { "type": "best_practice", "property": "onError", "message": "Slack API can have rate limits and connection issues", "suggestion": "Add error handling: onError: 'continueRegularOutput'" }

Current (no error handling):
{ "resource": "message", "operation": "post", "channel": "#alerts" }

Recommended fix:
{ "resource": "message", "operation": "post", "channel": "#alerts", "continueOnFail": true, "retryOnFail": true, "maxTries": 3 }
```

**No retry logic:**
```
Warning: { "type": "best_practice", "property": "retryOnFail", "message": "External API calls should retry on failure", "suggestion": "Add retryOnFail: true, maxTries: 3, waitBetweenTries: 1000" }
```
When to ignore: idempotent operations, or APIs that already retry internally. When to fix: flaky external services, production automation.

#### 7. `deprecated` — using an old API version or deprecated feature

Still works now, may stop working in future. Should generally be fixed eventually, even if not urgently.

```
Warning: { "type": "deprecated", "property": "typeVersion", "message": "typeVersion 1 is deprecated for Slack node, use version 2", "current": 1, "recommended": 2 }

Fix:
{ "type": "n8n-nodes-base.slack", "typeVersion": 2 }
// May need to update other fields to match the new version's shape.
```

#### 8. `performance` — configuration may cause performance issues

Relevant mainly for high-volume workflows or large datasets.

```
Warning: { "type": "performance", "property": "query", "message": "SELECT without LIMIT can return massive datasets", "suggestion": "Add LIMIT clause or use pagination" }

Current:  SELECT * FROM users WHERE active = true
Fix:      SELECT * FROM users WHERE active = true LIMIT 1000
```

---

### Operator structure — automatically corrected, don't hand-fix

`operator_structure` issues on IF/Switch nodes are rare in practice because n8n normalizes them itself when the workflow is saved. Trust this and don't waste time manually "fixing" these — if you see the warning, just save and re-check.

**Binary operators** (`equals`, `notEquals`, `contains`, `notContains`, `greaterThan`, `lessThan`, `startsWith`, `endsWith`) compare two values and should NOT carry a `singleValue` flag. If you (or a generated config) mistakenly include one, n8n removes it on save:
```
Before: { "type": "boolean", "operation": "equals", "singleValue": true }   // ❌ wrong for a binary operator
After (auto-corrected on save): { "type": "boolean", "operation": "equals" }   // singleValue removed
```

**Unary operators** (`isEmpty`, `isNotEmpty`, `true`, `false`) check a single value and DO need `singleValue: true`. If it's missing, n8n adds it on save:
```
Before: { "type": "boolean", "operation": "isEmpty" }                          // missing singleValue
After (auto-corrected on save): { "type": "boolean", "operation": "isEmpty", "singleValue": true }
```

n8n also fills in the complete `conditions.options` metadata for IF (v2.2+) and Switch (v3.2+) nodes automatically on save — if a validation check flags this metadata as missing before you've saved, it's a known false positive (see "Known quirks" below), not a real problem.

---

### Editing a specific field's text directly (e.g. a Code node script, or a long expression)

When making a targeted find-and-replace style edit inside one field of a node's configuration (rather than rewriting the whole field), three failure modes come up consistently:

1. **The exact text you're searching for isn't found.** This usually means the content already changed since you last looked at it, or your search string has a typo/whitespace mismatch. Re-read the field's *current* value before retrying — don't assume it still matches what you remember. Whitespace and line endings matter; if you're not sure they'll match exactly, search more loosely (e.g. treat runs of whitespace as flexible) rather than requiring an exact character match.
2. **The text you're searching for appears more than once, and it's unclear which one you mean.** Either broaden your intent to "replace every occurrence" deliberately, or make the search string more specific (include a bit more surrounding context) so it can only match the one location you actually want.
3. **A regex search pattern is unsafe or malformed.** Nested quantifiers like `(a+)+` and overlapping alternations like `(\w|\d)+` should be avoided — they're classic catastrophic-backtracking (ReDoS) patterns that can hang. Keep patterns simple and specific.

---

### Common workflow-level (structural) errors

Beyond individual node configs, a workflow as a whole should also be checked for:

1. **Broken connections** — a connection whose source or target node doesn't exist.
   ```
   Error: "Connection from 'Transform' to 'NonExistent' - target node not found"
   ```
   Fix: remove the stale connection, or create the missing node.

2. **Circular dependencies** — a loop in the node graph that isn't an intentional loop construct.
   ```
   Error: "Circular dependency detected: Node A → Node B → Node A"
   ```
   Fix: restructure the workflow to remove the loop.

3. **Multiple start/trigger nodes** — only one will actually execute.
   ```
   Warning: "Multiple trigger nodes found - only one will execute"
   ```
   Fix: remove the extra trigger(s), or split into separate workflows.

4. **Disconnected nodes** — a node that exists but isn't wired into the flow at all.
   ```
   Warning: "Node 'Transform' is not connected to workflow flow"
   ```
   Fix: connect it, or remove it if it's unused.

---

### False positives catalog — when a warning is genuinely acceptable

Not every warning needs fixing. Roughly 40% of warnings turn out to be acceptable given the specific context — the trick is recognizing which, and documenting the decision rather than either blindly fixing everything or blindly ignoring everything.

**Good practice:** validate → fix all errors → review each warning individually → decide if it's acceptable for this specific use case → document why → ship with confidence.
**Bad practice:** ignore all warnings blindly, deliberately validate at the lowest rigor level just to avoid seeing warnings, or ship without understanding the actual risk.

#### 1. Missing error handling

**Warning:** `No error handling configured` — suggestion is to add `continueOnFail: true` and `retryOnFail: true`.

**Acceptable when:**
- **Development/testing workflows** — you *want* to see failures during testing, not mask them.
  ```
  { "name": "Test Slack Integration", "nodes": [{ "type": "n8n-nodes-base.slack", "parameters": { "resource": "message", "operation": "post", "channel": "#test" } }] }
  ```
- **Non-critical notifications** — a failed FYI message doesn't affect core functionality.
  ```
  { "name": "Optional Slack Notification", "parameters": { "channel": "#general", "text": "FYI: Process completed" } }
  ```
- **Manual-trigger workflows** — a person is present, watching, and will retry manually if it fails.
  ```
  { "nodes": [{ "type": "n8n-nodes-base.webhook", "parameters": { "path": "manual-test" } }] }
  ```

**Fix when:**
- **Production automation handling important data:**
  ```
  Bad:  { "name": "Process Customer Orders", "nodes": [{ "type": "n8n-nodes-base.postgres", "parameters": { "query": "INSERT INTO orders..." } }] }   // ❌ no error handling
  Good: { "parameters": { "query": "INSERT INTO orders...", "continueOnFail": true, "retryOnFail": true, "maxTries": 3, "waitBetweenTries": 1000 } }
  ```
- **Critical integrations** (e.g. payment processing) — failures here MUST be handled, no exceptions.

#### 2. No retry logic

**Warning:** `External API calls should retry on failure` — suggestion is `retryOnFail: true` with exponential backoff.

**Acceptable when:**
- **The API already retries internally** (e.g. an SDK like Stripe's that retries under the hood).
- **The operation is idempotent**, e.g. a read-only GET request — safe to retry manually if ever needed.
- **It's a local/internal service** with high reliability, where failures are rare and immediately obvious.

**Fix when:**
- **The external API is known to be flaky:**
  ```
  Bad:  { "url": "https://unreliable-api.com/data" }
  Good: { "url": "https://unreliable-api.com/data", "retryOnFail": true, "maxTries": 3, "waitBetweenTries": 2000 }
  ```
- **The operation is non-idempotent** (e.g. a bare POST/create with no retry) — a timeout could silently lose data.

#### 3. Missing rate limiting

**Warning:** `API may have rate limits` — suggestion is to add rate limiting or batch requests.

**Acceptable when:**
- **It's an internal API** the same organization controls on both ends.
- **It's a genuinely low-volume workflow**, e.g. a once-a-day cron job hitting an endpoint once.
- **The API enforces its own server-side limits** and the workflow is already set up to error/retry on a 429 response.

**Fix when:**
- **It's a high-volume loop against a rate-limited public API:**
  ```
  Bad:
  { "nodes": [
      { "type": "n8n-nodes-base.splitInBatches", "parameters": { "batchSize": 100 } },
      { "type": "n8n-nodes-base.httpRequest", "parameters": { "url": "https://api.github.com/..." } }   // ❌ GitHub has strict rate limits
  ] }

  Good:
  { "type": "n8n-nodes-base.httpRequest", "parameters": {
      "url": "https://api.github.com/...",
      "options": { "batching": { "batch": { "batchSize": 10, "batchInterval": 1000 } } }
  } }
  ```

#### 4. Unbounded database queries

**Warning:** `SELECT without LIMIT can return massive datasets` — suggestion is to add a LIMIT or use pagination.

**Acceptable when:**
- **The table is small and known** (e.g. a config table with ~10 rows): `SELECT * FROM app_config`.
- **It's an aggregation query**, not returning rows: `SELECT COUNT(*) as total FROM users WHERE active = true`.
- **It's development/testing against a small dataset.**

**Fix when:**
- **It's a production query against a table that could be large:**
  ```
  Bad:    SELECT * FROM users
  Good:   SELECT * FROM users LIMIT 1000
  Better: SELECT * FROM users WHERE id > {{$json.lastId}} LIMIT 1000    // pagination
  ```

#### 5. Missing input validation

**Warning:** `Webhook doesn't validate input data` — suggestion is to add a conditional node to validate required fields.

**Acceptable when:**
- **The webhook is internal**, e.g. triggered only by your own backend, which already validates before sending.
- **The source is cryptographically trusted**, e.g. a Stripe webhook validated by its signature header.

**Fix when:**
- **It's a public-facing webhook** — anyone can send anything to it, so it needs its own validation:
  ```
  Bad:
  { "type": "n8n-nodes-base.webhook", "parameters": { "path": "public-form-submit" } }   // ❌ anyone can send anything

  Good — add a validation step after the webhook:
  {
    "nodes": [
      { "name": "Webhook", "type": "n8n-nodes-base.webhook" },
      { "name": "Validate Input", "type": "n8n-nodes-base.if", "parameters": {
          "conditions": { "boolean": [
            { "value1": "={{$json.body.email}}", "operation": "isNotEmpty" },
            { "value1": "={{$json.body.email}}", "operation": "regex", "value2": "^[^@]+@[^@]+\\.[^@]+$" }
          ] }
      } }
    ]
  }
  ```

#### 6. Hardcoded credentials

**Warning:** `Credentials should not be hardcoded` — suggestion is to use n8n's credential system.

**Acceptable when:**
- **The API is genuinely public with no auth**, e.g. `https://api.ipify.org` — there's no secret to protect.
- **It's a clearly-marked demo/example workflow**, e.g. `"Authorization": "Bearer DEMO_TOKEN"` in documentation.

**Always fix (no exceptions):**
- **Any real credential hardcoded into a workflow:**
  ```
  Bad:  { "headers": { "Authorization": "[REDACTED_SECRET]" } }   // ❌ NEVER hardcode real credentials

  Good: {
    "authentication": "headerAuth",
    "credentials": { "headerAuth": { "id": "credential-id", "name": "My API Key" } }
  }
  ```

#### Rigor-by-context cheat sheet

- **Quick automations:** be tolerant of most warnings; fix only errors plus security warnings.
- **Business-critical workflows:** apply maximum rigor; accept very few warnings; fix everything you reasonably can.
- **Integration testing:** accept essentially all warnings; fix only errors that actually prevent execution.

#### Decision framework for any individual warning

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

#### Known quirks that look like errors but aren't

- **IF-node "missing conditions.options metadata" warning** — false positive for IF v2.2+. n8n's own save-time normalization adds this metadata, but a validation check run *before* saving won't see it yet. Ignore it; it resolves itself once the workflow is saved.
- **Switch "N rules but N+1 output connections" warning** — false positive when the Switch node is deliberately using a fallback/"otherwise" mode, which legitimately creates one extra output beyond the rule count. Ignore it if the fallback output is intentional.
- **"Cannot validate credentials without execution context" warning** — false positive during static/build-time checking. Credential validity can only really be confirmed when the workflow actually runs, not while you're just reviewing the configuration. Ignore it at review time.

#### Summary: what to always/usually/often/always accept

- **Always fix:** security warnings, hardcoded real credentials, SQL-injection risks, any error (not warning) on a production workflow.
- **Usually fix:** missing error handling (in production), missing retry logic (on external APIs), missing input validation (on public webhooks), missing rate limiting (on high-volume calls).
- **Often acceptable:** missing error handling (dev/test), missing retry logic (internal/idempotent APIs), missing rate limiting (low volume), unbounded queries (small known datasets).
- **Always acceptable:** the three known quirks above, anything n8n's own save-time normalization handles automatically, metadata-completeness warnings that resolve on save.

**Golden rule: if you accept a warning instead of fixing it, document why.**

## Templates & examples

### What a validation report typically looks like

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

### Progressive validation — building up a config incrementally

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

### Error triage — reading a result systematically

```
1. MUST FIX — for each error: note property + message, apply the fix
2. SHOULD FIX — for each warning: note property + message, run it through the decision framework
3. OPTIONAL — for each suggestion: consider, but don't block on it
```

### Documenting an accepted warning

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

### Recovery patterns for stuck validations

**Start fresh** — when a configuration is severely broken: note the required fields, build the smallest possible valid configuration, then add features incrementally, checking after each one.

**Binary search** — when a workflow validates but produces wrong results at runtime: remove roughly half the nodes and re-test; if it now works, the fault was in the removed half, if it still fails, the fault is in the remaining half; repeat on that half until isolated.

**Clean up stale connections** — when you're seeing "node not found" errors: find every connection or expression referencing the old/missing node name and either point it at the correct current node or delete it.

### Common auto-fixable issue categories

These categories of problems are mechanical enough that they can usually just be corrected directly, rather than needing deep investigation:

1. **Expression missing its `=` prefix** — e.g. `{{ $json.field }}` should be `={{ $json.field }}`. Safe to just fix directly.
2. **`typeVersion` beyond what's actually supported** — downgrade to the highest version that node type actually supports.
3. **Conflicting `onError` settings** — remove the conflicting/redundant one.
4. **Unknown or misspelled node type** — correct it to the closest valid node type name; double-check the match is right before applying it if it's not an obvious typo.
5. **Webhook node missing a path** — generate a unique path (e.g. a UUID) for it.
6. **`typeVersion` behind the latest available** — upgrade, but check whether the newer version changed the shape of any fields, and migrate the configuration accordingly rather than assuming it's a drop-in change.
7. **Breaking changes between versions that don't have a mechanical fix** — these need a manual read of what changed and a deliberate migration; don't try to force an automatic fix here.

Treat 1-2 and 5 as safe to just apply. Treat 3-4 as worth a quick sanity check before applying. Treat 6-7 as needing an actual read of what changed before you touch anything.
