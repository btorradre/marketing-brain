# n8n Node Configuration

Reference for configuring individual nodes inside an n8n workflow — getting the right fields set, in the right shape, for whatever operation a node is performing. n8n nodes are "operation-aware": the same node type (Slack, HTTP Request, Postgres, IF, etc.) requires completely different fields depending on which resource/operation/method you've selected, and many fields only appear once some other field has been set to a particular value (n8n calls this mechanism `displayOptions`). Use this whenever you're building or editing an n8n workflow and need to know which fields a node actually needs, why a field you expect to see isn't showing up, or what a working configuration looks like for a common node type (HTTP Request, Webhook, Slack, Gmail, Postgres, Set, Code, IF, Switch, OpenAI, Schedule Trigger).

## How to use this

1. **Identify the node type, resource, and operation first.** Before configuring anything, pin down three things: which node type (e.g. `nodes-base.slack`, `nodes-base.httpRequest`), which resource if the node has one (e.g. "message" vs "channel" in Slack), and which operation (e.g. "post" vs "update"). Everything downstream — which fields are required, which are hidden — depends on getting these three right first.

2. **Look up the node's basic schema before configuring it.** Check n8n's node reference documentation (or the node's property panel in the n8n editor) for the required fields and common options for the resource/operation you picked. Start with the short, standard view — required fields plus common options — rather than trying to absorb every possible property up front. This covers the large majority of configuration needs; only pull up the full, exhaustive property list (every option, every nested field, every `displayOptions` rule) when the standard view genuinely doesn't answer your question.

3. **Configure only the minimal required fields first.** Don't add every optional field you can think of "just in case" — start lean:
   ```javascript
   // Good — start minimal
   { "method": "GET", "url": "...", "authentication": "none" }

   // Bad — over-configured upfront
   {
     "method": "GET", "url": "...",
     "sendQuery": false, "sendHeaders": false, "sendBody": false,
     "timeout": 10000, "ignoreResponseCode": false
     // ...20 more optional fields nobody asked for
   }
   ```
   Add optional fields only once you actually need them.

4. **Understand that fields appear and disappear based on other fields — this is the `displayOptions` mechanism.** A field's schema entry can carry a `displayOptions.show` rule, meaning it is only visible (and only required) when some other field matches a given value:
   ```javascript
   {
     "name": "body",
     "displayOptions": {
       "show": {
         "sendBody": [true],
         "method": ["POST", "PUT", "PATCH"]
       }
     }
   }
   ```
   Read as: "body" is shown when `sendBody = true` AND `method` is one of POST/PUT/PATCH. Multiple keys inside one `show` block are combined with AND logic; multiple values inside one array are combined with OR logic (e.g. `method` matching any of POST, PUT, or PATCH). A less common `displayOptions.hide` rule works the opposite way — the field disappears when the condition matches (e.g. an "advanced" field hidden while `simpleMode = true`).

5. **When a field seems to be missing that you know should be there, it's almost always hidden by a dependency, not actually absent.** Don't assume the node doesn't support something — check what other field controls that field's visibility (see the dependency patterns and troubleshooting section under Rules & Standards below), set that controlling field correctly, and the field you wanted will appear.

6. **Configure parent fields before child/nested fields.** Nested objects have their own internal dependencies — e.g. in an HTTP Request body, `contentType` determines what shape `content` needs to be (a JSON object for `contentType: "json"`, an array of `{name, value}` pairs for `contentType: "form-data"`). Set the parent field, then shape the child field to match:
   ```javascript
   // Step 1 — set the parent
   { "body": { "contentType": "json" } }

   // Step 2 — now shape the child to match
   { "body": { "contentType": "json", "content": { "key": "value" } } }
   ```

7. **Validate iteratively — don't expect to get it right in one pass.** A normal configuration cycle is: configure a minimal version → validate → get an error naming a missing/misconfigured field → add or fix that field → validate again → repeat until clean. Two to three iterations before something validates cleanly is completely normal, not a sign you're doing it wrong. "Validate" here means either using n8n's own validation (paste the config into the n8n editor, or use its built-in workflow validation if you have API access to it) or manually walking the configuration against the dependency rules and the checklist under Rules & Standards.

8. **Re-check requirements every time you change the operation — never assume a config carries over.** Switching a Slack node from `operation: "post"` to `operation: "update"` doesn't just add a field, it changes which fields are required and which are irrelevant (channel becomes optional, messageId becomes required). Treat every operation change as a fresh "what does this operation need" lookup, not a patch to the old config.

9. **Trust automatic structural fixes on conditional/operator fields, but never assume they'll add missing required business fields.** Some n8n node editors auto-correct structural details on save (for example, adding a `singleValue: true` flag automatically once you pick a unary IF-node operator like `isEmpty`). That kind of structural bookkeeping is not something you need to hand-manage. But this auto-fix behavior will never invent a business-logic field you forgot — if you forgot to set `channel` on a Slack "post" message, nothing will add it for you. Only structural/operator plumbing gets auto-corrected; actual required content never does.

10. **Run the final checklist before considering a node done.** See the "Quick-reference checklist" under Rules & Standards.

## Rules & standards

### The `displayOptions` mechanism, in full

- **`show`** (most common): the field is visible when the named condition(s) match.
- **`hide`** (less common): the field is visible by default and disappears when the named condition(s) match.
- **Multiple keys in one `show`/`hide` block = AND logic.** All named conditions must hold simultaneously for the rule to apply.
- **Multiple values inside one condition's array = OR logic.** Any one of the listed values satisfies that condition.
- Example combining both: `"show": { "sendBody": [true], "method": ["POST","PUT","PATCH"] }` means shown only when `sendBody` is `true` AND `method` is POST, PUT, **or** PATCH.

### Four common dependency patterns

**Pattern 1 — Boolean toggle.** A boolean field (e.g. `sendBody`) controls whether a dependent field (e.g. `body`) is shown at all. Unchecked/false → dependent field hidden. Checked/true → dependent field appears.

**Pattern 2 — Resource/operation cascade.** Changing `resource` and/or `operation` swaps which fields are shown entirely (see the Slack field-visibility matrix below) — this is not additive, fields genuinely disappear and get replaced by different ones.

**Pattern 3 — Type-specific configuration.** The "type" of a thing (e.g. the data type of an IF-node condition: string, number, boolean) determines which operators and which value fields are valid — a string condition and a boolean condition don't share the same operator list.

**Pattern 4 — Method-specific fields.** HTTP method determines which optional feature blocks are even reachable — e.g. only POST/PUT/PATCH (and sometimes DELETE, depending on the API) expose a body at all; GET does not.

### Dependency chain example (HTTP Request, full walk-through)

```
method=POST
  → sendBody visible
    → sendBody=true
      → body visible + required
        → body.contentType=json
          → body.content visible + required
```
Concretely, step by step:
```javascript
// Step 1 — set method
{ "method": "POST" }                     // → sendBody becomes visible

// Step 2 — enable body
{ "method": "POST", "sendBody": true }   // → body field becomes visible AND required

// Step 3 — configure body
{
  "method": "POST", "sendBody": true,
  "body": { "contentType": "json" }      // → content field becomes visible AND required
}

// Step 4 — add content
{
  "method": "POST", "sendBody": true,
  "body": {
    "contentType": "json",
    "content": { "name": "John", "email": "john@example.com" }
  }
}
// ✅ Valid
```

### IF-node operator dependency table (binary vs. unary)

| Operator | value1 | value2 | singleValue |
|---|---|---|---|
| equals | Required | Required | false |
| notEquals | Required | Required | false |
| contains | Required | Required | false |
| isEmpty | Required | Hidden | true |
| isNotEmpty | Required | Hidden | true |

Binary operators (equals, notEquals, contains, and similar two-sided comparisons) need both `value1` and `value2`. Unary operators (isEmpty, isNotEmpty, and boolean-only checks like `true`/`false`) only need `value1` — supplying a `value2` for these is wrong, and `singleValue: true` should accompany them (this flag is normally added automatically on save, but understand that it's the correct expected shape if you're hand-building the JSON).

### Slack operation field-visibility matrix

| Field | post | update | delete | get |
|---|---|---|---|---|
| channel | Required | Optional | Required | Required |
| text | Required | Required | Hidden | Hidden |
| messageId | Hidden | Required | Required | Required |
| attachments | Optional | Optional | Hidden | Hidden |
| blocks | Optional | Optional | Hidden | Hidden |

This is the concrete illustration of "operation changes requirements" — the exact same node type shows an entirely different required-field set depending on `operation`.

### Nested/child dependencies

Parent fields determine the valid shape of child fields, not just their visibility. Classic example — HTTP Request body:
```javascript
// contentType: json → content is a JSON object
{ "body": { "contentType": "json", "content": { "key": "value" } } }

// contentType: form-data → content is an array of {name, value} pairs
{ "body": { "contentType": "form-data", "content": [ { "name": "field1", "value": "value1" } ] } }
```
Always configure the parent (e.g. `contentType`) before shaping the child (`content`) — the child's correct structure depends on what the parent says.

### What gets auto-corrected vs. what doesn't

**Gets auto-corrected on save (structural/operator bookkeeping):** things like adding `singleValue: true` once a unary IF-operator is selected. Don't manually fight with this — let it happen.

**Never gets auto-corrected — you must supply it yourself:** any genuinely missing required business field. Example: if you configure a Slack "post" without `channel`, nothing will invent a channel for you:
```javascript
// You configure (missing channel) — NOT auto-fixed
{ "resource": "message", "operation": "post", "text": "Hello" }

// You must add it yourself
{ "resource": "message", "operation": "post", "channel": "#general", "text": "Hello" }
```

### Advanced dependency patterns worth knowing

- **Conditional required with fallback / accepted-either form** — some fields accept either a literal string or an expression, and either satisfies validation (e.g. Slack `channel` as `"#general"` or as `"={{$json.channelName}}"`).
- **Mutually exclusive fields** — sometimes you use one of two alternative fields, not both (e.g. `messageId` vs. `messageName` to identify a thread) — the dependency rules ensure only the one you're using is required.
- **Progressive complexity / simple vs. advanced mode** — a `mode` field (e.g. `"simple"` vs `"advanced"`) swaps an entire block of fields for a different one; simple-mode fields hide when advanced mode is selected and vice versa.

### Troubleshooting guide

**"Field X is required but I don't see it anywhere in the config."**
Almost always a hidden dependency. Find what controls that field's visibility (check the node's documented `displayOptions`, or search the node's property list for the field name to see its show/hide rule), then set the controlling field. Example: `body` is required but invisible because `sendBody` hasn't been set to `true` yet — set `sendBody: true` and `body` appears.

**"A field disappeared after I changed the operation."**
Expected behavior, not a bug — different operations have entirely different required-field sets (see the Slack matrix above). Re-check what the new operation actually needs rather than assuming the old fields still apply; drop the fields the old operation needed that the new one doesn't, and add whatever new required fields the new operation introduces.

**"Validation passed, but the field I set disappeared after saving."**
This happens when you set a field whose controlling condition doesn't hold — e.g. setting `sendBody: true` and a `body` while `method: "GET"` — the method hides `body` regardless of `sendBody`, so it gets stripped on save even though you set it:
```javascript
// You configure
{ "method": "GET", "sendBody": true, "body": {...} }   // ❌ GET doesn't support body

// After save
{ "method": "GET" }   // body silently removed
```
Fix: respect the full dependency chain from the start (right method AND the right toggle), not just one piece of it.

### Node-specific configuration notes

**SplitInBatches (loop) node.** Two outputs with counterintuitive naming:
- `main[0]` = "done" — fires once, after all batches finish. Connect this to downstream processing; add a Limit-1 node right after it as a safety net for edge cases where it fires with extra items.
- `main[1]` = "each batch" — fires per batch; this is the loop body. Wire it to the loop's processing steps, then loop the output back around to the SplitInBatches node's input.

**Google Sheets node — per-item execution.** Each input item triggers a separate API call. 100 input items with an "Append Row" operation means 100 separate API calls. To write in bulk instead, aggregate the items into one payload first (in a Code node), then make a single HTTP Request call to the Sheets API rather than looping the Sheets node itself.

**Google Sheets node — formula columns.** Never use the `append` operation on a sheet that has formula columns — it overwrites the formulas. Instead use an HTTP Request node calling the Google Sheets API's `values.update` method (PUT) with a Google API credential, which lets you target specific cells/ranges without clobbering formula columns.

### Quick-reference checklist before considering a node's configuration done

- [ ] Node type, resource, and operation are all explicitly chosen (not left ambiguous)
- [ ] Every field required by that specific resource/operation combination is present
- [ ] No leftover fields from a different operation that no longer applies
- [ ] Every conditionally-shown field you're relying on actually has its controlling field set correctly (e.g. `sendBody: true` present if you set a `body`)
- [ ] Parent fields (e.g. `contentType`) are set before their dependent child fields are shaped
- [ ] Binary condition operators have both value1 and value2; unary operators (isEmpty, isNotEmpty, true/false) have only value1
- [ ] Configuration has been validated at least once and any resulting errors resolved
- [ ] No obviously irrelevant/optional fields added "just in case" that aren't actually needed

### Anti-patterns to avoid

- **Over-configuring upfront.** Don't add every optional field a node exposes before you know you need it — start minimal and add as required.
- **Skipping validation.** Never configure a node and deploy/save it without validating first; always configure → validate → fix → re-validate.
- **Ignoring operation context.** Don't reuse a config built for one operation when switching to another operation on the same node — always re-check what the new operation actually requires (see the Slack post→update example above, where reusing the "post" config for "update" silently keeps the wrong field `channel` as required-feeling and omits the actually-required `messageId`).
- **Copying configs between contexts without re-validating.** A working config for one operation/node instance is not guaranteed to be valid for a different one — adjust for the new context and validate again.
- **Manually fighting auto-corrected structural fields** (like `singleValue`) instead of letting that bookkeeping happen and focusing your effort on the actual business logic.

## Templates & examples

### HTTP Request node

**GET — minimal:**
```javascript
{
  "method": "GET",
  "url": "https://api.example.com/users",
  "authentication": "none"
}
```

**GET — with query parameters:**
```javascript
{
  "method": "GET",
  "url": "https://api.example.com/users",
  "authentication": "none",
  "sendQuery": true,
  "queryParameters": {
    "parameters": [
      { "name": "limit", "value": "100" },
      { "name": "offset", "value": "={{$json.offset}}" }
    ]
  }
}
```

**GET — with authentication:**
```javascript
{
  "method": "GET",
  "url": "https://api.example.com/users",
  "authentication": "predefinedCredentialType",
  "nodeCredentialType": "httpHeaderAuth"
}
```

**POST with JSON — minimal:**
```javascript
{
  "method": "POST",
  "url": "https://api.example.com/users",
  "authentication": "none",
  "sendBody": true,
  "body": {
    "contentType": "json",
    "content": { "name": "John Doe", "email": "john@example.com" }
  }
}
```
Gotcha: remember `sendBody: true` for POST/PUT/PATCH — it's easy to forget and the body will silently be dropped without it.

**POST with JSON — with expressions:**
```javascript
{
  "method": "POST",
  "url": "https://api.example.com/users",
  "authentication": "none",
  "sendBody": true,
  "body": {
    "contentType": "json",
    "content": {
      "name": "={{$json.name}}",
      "email": "={{$json.email}}",
      "metadata": { "source": "n8n", "timestamp": "={{$now.toISO()}}" }
    }
  }
}
```

**PUT/PATCH** — same pattern as POST, only the method changes:
```javascript
{
  "method": "PUT",
  "url": "https://api.example.com/users/123",
  "authentication": "none",
  "sendBody": true,
  "body": { "contentType": "json", "content": { "name": "Updated Name" } }
}
```

**DELETE — minimal (no body):**
```javascript
{ "method": "DELETE", "url": "https://api.example.com/users/123", "authentication": "none" }
```

**DELETE — with body (some APIs allow this):**
```javascript
{
  "method": "DELETE",
  "url": "https://api.example.com/users",
  "authentication": "none",
  "sendBody": true,
  "body": { "contentType": "json", "content": { "ids": ["123", "456"] } }
}
```

### Webhook node

**Basic:**
```javascript
{ "path": "my-webhook", "httpMethod": "POST", "responseMode": "onReceived" }
```
Gotcha — the single most common Webhook mistake: incoming data is nested under `.body`, not at the top level.
```javascript
// ❌ Wrong
{ "text": "={{$json.email}}" }

// ✅ Correct
{ "text": "={{$json.body.email}}" }
```
The full webhook item structure:
```javascript
{
  "headers": { "content-type": "application/json", "user-agent": "..." },
  "params": {},
  "query": {},
  "body": {
    "name": "Alice",
    "email": "alice@example.com",
    "message": "Hello!"
  }
}
```
Also available on the same object: `.query` (query-string parameters), `.headers` (HTTP headers, e.g. `headers['content-type']`), and `.method` / `.url`.

**With header authentication:**
```javascript
{
  "path": "secure-webhook",
  "httpMethod": "POST",
  "responseMode": "onReceived",
  "authentication": "headerAuth",
  "options": { "responseCode": 200, "responseData": "{\n  \"success\": true\n}" }
}
```

**Returning custom data from the last node:**
```javascript
{
  "path": "my-webhook",
  "httpMethod": "POST",
  "responseMode": "lastNode",
  "options": {
    "responseCode": 201,
    "responseHeaders": { "entries": [ { "name": "Content-Type", "value": "application/json" } ] }
  }
}
```

### Slack node

**Post message — minimal:**
```javascript
{ "resource": "message", "operation": "post", "channel": "#general", "text": "Hello from n8n!" }
```

**Post message — with dynamic content:**
```javascript
{
  "resource": "message",
  "operation": "post",
  "channel": "={{$json.channel}}",
  "text": "New user: {{$json.name}} ({{$json.email}})"
}
```

**Post message — with attachments:**
```javascript
{
  "resource": "message",
  "operation": "post",
  "channel": "#alerts",
  "text": "Error Alert",
  "attachments": [
    {
      "color": "#ff0000",
      "fields": [
        { "title": "Error Type", "value": "={{$json.errorType}}" },
        { "title": "Timestamp", "value": "={{$now.toLocaleString()}}" }
      ]
    }
  ]
}
```
Gotcha: channel must start with `#` for public channels, or be a channel ID.

**Update message — minimal:**
```javascript
{
  "resource": "message",
  "operation": "update",
  "messageId": "1234567890.123456",
  "text": "Updated message content"
}
```
Note: `messageId` is required for update; `channel` is optional (it can be inferred).

**Create channel — minimal:**
```javascript
{ "resource": "channel", "operation": "create", "name": "new-project-channel", "isPrivate": false }
```
Gotcha: channel name must be lowercase, no spaces, 1–80 characters.

### Gmail node

**Send email — minimal:**
```javascript
{
  "resource": "message",
  "operation": "send",
  "to": "user@example.com",
  "subject": "Hello from n8n",
  "message": "This is the email body"
}
```

**Send email — with dynamic content:**
```javascript
{
  "resource": "message",
  "operation": "send",
  "to": "={{$json.email}}",
  "subject": "Order Confirmation #{{$json.orderId}}",
  "message": "Dear {{$json.name}},\n\nYour order has been confirmed.\n\nThank you!",
  "options": { "ccList": "admin@example.com", "replyTo": "support@example.com" }
}
```

**Get email — minimal:**
```javascript
{ "resource": "message", "operation": "getAll", "returnAll": false, "limit": 10 }
```

**Get email — with filters:**
```javascript
{
  "resource": "message",
  "operation": "getAll",
  "returnAll": false,
  "limit": 50,
  "filters": { "q": "is:unread from:important@example.com", "labelIds": ["INBOX"] }
}
```

### Postgres node

**Execute query — SELECT, minimal:**
```javascript
{ "operation": "executeQuery", "query": "SELECT * FROM users WHERE active = true LIMIT 100" }
```

**Execute query — with parameters (SQL injection prevention):**
```javascript
{
  "operation": "executeQuery",
  "query": "SELECT * FROM users WHERE email = $1 AND active = $2",
  "additionalFields": { "mode": "list", "queryParameters": "user@example.com,true" }
}
```
Gotcha — always use parameterized queries for anything derived from user/webhook input:
```javascript
// ❌ BAD — SQL injection risk
{ "query": "SELECT * FROM users WHERE email = '{{$json.email}}'" }

// ✅ GOOD — parameterized
{
  "query": "SELECT * FROM users WHERE email = $1",
  "additionalFields": { "mode": "list", "queryParameters": "={{$json.email}}" }
}
```

**Insert — minimal:**
```javascript
{
  "operation": "insert",
  "table": "users",
  "columns": "name,email,created_at",
  "additionalFields": { "mode": "list", "queryParameters": "John Doe,john@example.com,NOW()" }
}
```

**Insert — with expressions:**
```javascript
{
  "operation": "insert",
  "table": "users",
  "columns": "name,email,metadata",
  "additionalFields": {
    "mode": "list",
    "queryParameters": "={{$json.name}},={{$json.email}},{{JSON.stringify($json)}}"
  }
}
```

**Update — minimal:**
```javascript
{
  "operation": "update",
  "table": "users",
  "updateKey": "id",
  "columns": "name,email",
  "additionalFields": {
    "mode": "list",
    "queryParameters": "={{$json.id}},Updated Name,newemail@example.com"
  }
}
```

### Set node

**Set fixed values — minimal:**
```javascript
{
  "mode": "manual",
  "duplicateItem": false,
  "assignments": {
    "assignments": [
      { "name": "status", "value": "active", "type": "string" },
      { "name": "count", "value": 100, "type": "number" }
    ]
  }
}
```

**Set from input data — mapping:**
```javascript
{
  "mode": "manual",
  "duplicateItem": false,
  "assignments": {
    "assignments": [
      { "name": "fullName", "value": "={{$json.firstName}} {{$json.lastName}}", "type": "string" },
      { "name": "email", "value": "={{$json.email.toLowerCase()}}", "type": "string" },
      { "name": "timestamp", "value": "={{$now.toISO()}}", "type": "string" }
    ]
  }
}
```
Gotcha — always use the correct `type` for each field, or the value comes out wrong:
```javascript
// ❌ Wrong type — value stays a string "25"
{ "name": "age", "value": "25", "type": "string" }

// ✅ Correct type — value is the number 25
{ "name": "age", "value": 25, "type": "number" }
```

### Code node

**Run once for all items:**
```javascript
{
  "mode": "runOnceForAllItems",
  "jsCode": "return $input.all().map(item => ({\n  json: {\n    name: item.json.name.toUpperCase(),\n    email: item.json.email\n  }\n}));"
}
```

**Run once for each item:**
```javascript
{
  "mode": "runOnceForEachItem",
  "jsCode": "// Process each item\nconst data = $input.item.json;\n\nreturn {\n  json: {\n    fullName: `${data.firstName} ${data.lastName}`,\n    email: data.email.toLowerCase(),\n    timestamp: new Date().toISOString()\n  }\n};"
}
```
Gotcha: inside a Code node's `jsCode`, use `$input.item.json` or `$input.all()` to access data — never n8n's `{{ }}` expression syntax, which is for other node types (Set, IF, HTTP Request URL fields, etc.), not for the Code node's own JavaScript:
```javascript
// ❌ Wrong — expressions don't work inside Code node JavaScript
{ "jsCode": "const name = '={{$json.name}}';" }

// ✅ Correct — direct JavaScript access
{ "jsCode": "const name = $input.item.json.name;" }
```

### IF node

**String comparison — equals (binary):**
```javascript
{
  "conditions": {
    "string": [ { "value1": "={{$json.status}}", "operation": "equals", "value2": "active" } ]
  }
}
```

**String comparison — contains (binary):**
```javascript
{
  "conditions": {
    "string": [ { "value1": "={{$json.email}}", "operation": "contains", "value2": "@example.com" } ]
  }
}
```

**String comparison — isEmpty (unary):**
```javascript
{
  "conditions": {
    "string": [
      {
        "value1": "={{$json.email}}",
        "operation": "isEmpty"
        // No value2 — unary operator
        // singleValue: true is added automatically on save
      }
    ]
  }
}
```
Gotcha: unary operators (isEmpty, isNotEmpty) never need a `value2`.

**Number comparison — greater than:**
```javascript
{
  "conditions": {
    "number": [ { "value1": "={{$json.age}}", "operation": "larger", "value2": 18 } ]
  }
}
```

**Boolean comparison — is true (unary):**
```javascript
{
  "conditions": {
    "boolean": [ { "value1": "={{$json.isActive}}", "operation": "true" } ]
  }
}
```

**Multiple conditions — AND (all must match):**
```javascript
{
  "conditions": {
    "string": [ { "value1": "={{$json.status}}", "operation": "equals", "value2": "active" } ],
    "number": [ { "value1": "={{$json.age}}", "operation": "larger", "value2": 18 } ]
  },
  "combineOperation": "all"
}
```

**Multiple conditions — OR (any can match):**
```javascript
{
  "conditions": {
    "string": [
      { "value1": "={{$json.status}}", "operation": "equals", "value2": "active" },
      { "value1": "={{$json.status}}", "operation": "equals", "value2": "pending" }
    ]
  },
  "combineOperation": "any"
}
```

### Switch node

**Basic rules-based switch:**
```javascript
{
  "mode": "rules",
  "rules": {
    "rules": [
      {
        "conditions": {
          "string": [ { "value1": "={{$json.status}}", "operation": "equals", "value2": "active" } ]
        }
      },
      {
        "conditions": {
          "string": [ { "value1": "={{$json.status}}", "operation": "equals", "value2": "pending" } ]
        }
      }
    ]
  },
  "fallbackOutput": "extra"
}
```
Gotcha: the number of rules must match the number of output branches you've wired up.

### OpenAI (chat completion) node

**Minimal:**
```javascript
{
  "resource": "chat",
  "operation": "complete",
  "messages": { "values": [ { "role": "user", "content": "={{$json.prompt}}" } ] }
}
```

**With system prompt and options:**
```javascript
{
  "resource": "chat",
  "operation": "complete",
  "messages": {
    "values": [
      { "role": "system", "content": "You are a helpful assistant specialized in customer support." },
      { "role": "user", "content": "={{$json.userMessage}}" }
    ]
  },
  "options": { "temperature": 0.7, "maxTokens": 500 }
}
```

### Schedule Trigger node

**Daily at a specific time:**
```javascript
{
  "rule": {
    "interval": [ { "field": "hours", "hoursInterval": 24 } ],
    "hour": 9,
    "minute": 0,
    "timezone": "America/New_York"
  }
}
```
Gotcha: always set `timezone` explicitly — otherwise the trigger silently uses the server's timezone, which is rarely what you want.
```javascript
// ❌ Bad — uses server timezone
{ "rule": { "interval": [ /* ... */ ] } }

// ✅ Good — explicit timezone
{ "rule": { "interval": [ /* ... */ ], "timezone": "America/New_York" } }
```

**Every N minutes:**
```javascript
{ "rule": { "interval": [ { "field": "minutes", "minutesInterval": 15 } ] } }
```

**Cron expression (advanced scheduling):**
```javascript
{ "mode": "cron", "cronExpression": "0 */2 * * *", "timezone": "America/New_York" }
```

### Pattern-selection quick reference

| Category | Most common shape | Key gotcha |
|---|---|---|
| HTTP/API | GET, POST JSON | Remember `sendBody: true` |
| Webhooks | POST receiver | Incoming data lives under `.body` |
| Communication | Slack post | Channel must be `#name` format |
| Database | SELECT with params | Always use parameterized queries |
| Transform | Set assignments | Match the `type` to the actual value |
| Conditional | IF string equals | Unary operators skip `value2` |
| AI | OpenAI chat | Combine system + user messages |
| Schedule | Daily at time | Always set timezone explicitly |
