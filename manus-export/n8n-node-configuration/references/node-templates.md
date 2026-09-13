# Node Configuration Templates & Examples

## Slack Operation Field-Visibility Matrix

| Field | post | update | delete | get |
|---|---|---|---|---|
| channel | Required | Optional | Required | Required |
| text | Required | Required | Hidden | Hidden |
| messageId | Hidden | Required | Required | Required |
| attachments | Optional | Optional | Hidden | Hidden |
| blocks | Optional | Optional | Hidden | Hidden |

This is the concrete illustration of "operation changes requirements" — the exact same node type shows an entirely different required-field set depending on `operation`.

## HTTP Request Node

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

## Webhook Node

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

## Slack Node

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

## Gmail Node

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

## Postgres Node

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

## Set Node

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

## Code Node

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

## IF Node

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

## Switch Node

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

## OpenAI (Chat Completion) Node

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

## Schedule Trigger Node

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

## Pattern-Selection Quick Reference

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
