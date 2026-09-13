# False Positives Catalog — When a Warning Is Genuinely Acceptable

Not every warning needs fixing. Roughly 40% of warnings turn out to be acceptable given the specific context — the trick is recognizing which, and documenting the decision rather than either blindly fixing everything or blindly ignoring everything.

**Good practice:** validate → fix all errors → review each warning individually → decide if it's acceptable for this specific use case → document why → ship with confidence.
**Bad practice:** ignore all warnings blindly, deliberately validate at the lowest rigor level just to avoid seeing warnings, or ship without understanding the actual risk.

## 1. Missing Error Handling

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

## 2. No Retry Logic

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

## 3. Missing Rate Limiting

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

## 4. Unbounded Database Queries

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

## 5. Missing Input Validation

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

## 6. Hardcoded Credentials

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

## Known Quirks That Look Like Errors but Aren't

- **IF-node "missing conditions.options metadata" warning** — false positive for IF v2.2+. n8n's own save-time normalization adds this metadata, but a validation check run *before* saving won't see it yet. Ignore it; it resolves itself once the workflow is saved.
- **Switch "N rules but N+1 output connections" warning** — false positive when the Switch node is deliberately using a fallback/"otherwise" mode, which legitimately creates one extra output beyond the rule count. Ignore it if the fallback output is intentional.
- **"Cannot validate credentials without execution context" warning** — false positive during static/build-time checking. Credential validity can only really be confirmed when the workflow actually runs, not while you're just reviewing the configuration. Ignore it at review time.
