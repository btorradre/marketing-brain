# Validation Error & Warning Catalog

## Errors (Must Fix)

### 1. `missing_required` — a required field wasn't provided

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

### 2. `invalid_value` — the value doesn't match an allowed option or format

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

### 3. `type_mismatch` — wrong data type

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

### 4. `invalid_expression` — n8n expression syntax error or invalid reference

Moderately common. Usually a missing `{{ }}` wrapper, a typo in a variable or node name, a reference to a field that doesn't exist, or invalid JavaScript inside the expression.

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

### 5. `invalid_reference` — configuration references a node that doesn't exist in the workflow

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

## Warnings (Should Fix — Context-Dependent)

### 6. `best_practice` — configuration works but doesn't follow best practice

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

### 7. `deprecated` — using an old API version or deprecated feature

Still works now, may stop working in future. Should generally be fixed eventually, even if not urgently.

```
Warning: { "type": "deprecated", "property": "typeVersion", "message": "typeVersion 1 is deprecated for Slack node, use version 2", "current": 1, "recommended": 2 }

Fix:
{ "type": "n8n-nodes-base.slack", "typeVersion": 2 }
// May need to update other fields to match the new version's shape.
```

### 8. `performance` — configuration may cause performance issues

Relevant mainly for high-volume workflows or large datasets.

```
Warning: { "type": "performance", "property": "query", "message": "SELECT without LIMIT can return massive datasets", "suggestion": "Add LIMIT clause or use pagination" }

Current:  SELECT * FROM users WHERE active = true
Fix:      SELECT * FROM users WHERE active = true LIMIT 1000
```
