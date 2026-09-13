# Webhook Processing

**Pattern structure**: `Webhook → [Validate] → [Transform] → [Action] → [Response/Notify]`

**Key characteristic**: instant event-driven processing. This is the most common workflow pattern overall.

## Core Components

**1. Webhook node (trigger)** — creates an HTTP endpoint to receive data:
```javascript
{
  path: "form-submit",        // URL path: https://n8n.example.com/webhook/form-submit
  httpMethod: "POST",         // GET, POST, PUT, DELETE
  responseMode: "onReceived", // or "lastNode" for custom response
  responseData: "allEntries"  // or "firstEntryJson"
}
```
**Critical gotcha**: data is nested under `$json.body`.
```javascript
❌ {{$json.email}}
✅ {{$json.body.email}}
```

**2. Validation (optional but recommended)** — verify incoming data before processing. Options: an IF node (check required fields exist), a Code node (custom validation logic), or Stop-and-Error (fail gracefully with a message).

Example (IF node condition):
```javascript
{{$json.body.email}} is not empty AND
{{$json.body.name}} is not empty
```

**3. Transformation** — map webhook data to the desired format, typically with Set (field mapping) or Code (complex transformations).

Example (Set node):
```javascript
{
  "user_email": "={{$json.body.email}}",
  "user_name": "={{$json.body.name}}",
  "timestamp": "={{$now}}"
}
```

**4. Action** — common actions: store in database (Postgres, MySQL, MongoDB), send notification (Slack, Email, Discord), call another API (HTTP Request), update an external system (CRM, support ticket).

**5. Response (if responseMode: "lastNode")** — send a custom HTTP response via the Webhook Response node:
```javascript
{
  statusCode: 200,
  headers: {
    "Content-Type": "application/json"
  },
  body: {
    "status": "success",
    "message": "Form received"
  }
}
```

## Common Use Cases

**1. Form submissions** — `Form → Webhook → Validate → Database → Email Confirmation`

Example:
```
1. Webhook (path: "contact-form", POST)
2. IF (check email & message not empty)
3. Postgres (insert into contacts table)
4. Email (send confirmation to user)
5. Slack (notify team in #leads)
6. Webhook Response ({"status": "success"})
```
Real data access:
```javascript
Name: {{$json.body.name}}
Email: {{$json.body.email}}
Message: {{$json.body.message}}
```

**2. Payment webhooks (Stripe, PayPal)** — `Payment Provider → Webhook → Verify → Update Database → Send Receipt`

Security: verify webhook signatures.
```javascript
// Code node - verify Stripe signature
const crypto = require('crypto');
const signature = $input.item.headers['stripe-signature'];
const secret = $credentials.stripeWebhookSecret;

// Verify signature matches
const expectedSig = crypto
  .createHmac('sha256', secret)
  .update($input.item.body)
  .digest('hex');

if (signature !== expectedSig) {
  throw new Error('Invalid webhook signature');
}

return $input.item.body; // Return validated body
```

**3. Chat platform integrations (Slack, Discord, Teams)** — `Chat Command → Webhook → Process → Respond`

Example (Slack slash command):
```
1. Webhook (path: "slack-command", POST)
2. Code (parse Slack payload: $json.body.text, $json.body.user_id)
3. HTTP Request (fetch data from API)
4. Set (format Slack message)
5. Webhook Response (immediate Slack response)
```
Slack data access:
```javascript
Command: {{$json.body.command}}
Text: {{$json.body.text}}
User ID: {{$json.body.user_id}}
Channel ID: {{$json.body.channel_id}}
```

**4. GitHub/GitLab webhooks** — `Git Event → Webhook → Parse → Notify/Deploy`

Example (new PR notification):
```
1. Webhook (path: "github", POST)
2. IF (check $json.body.action equals "opened")
3. Set (extract PR details: title, author, url)
4. Slack (notify #dev-team)
5. Webhook Response (200 OK)
```
GitHub data access:
```javascript
Event Type: {{$json.headers['x-github-event']}}
Action: {{$json.body.action}}
PR Title: {{$json.body.pull_request.title}}
Author: {{$json.body.pull_request.user.login}}
URL: {{$json.body.pull_request.html_url}}
```

**5. IoT device data** — `Device → Webhook → Validate → Store → Alert (if threshold)`

Example (temperature sensor):
```
1. Webhook (path: "sensor-data", POST)
2. Set (extract sensor readings)
3. Postgres (insert into sensor_readings)
4. IF (temperature > 80)
5. Email (alert admin)
```

## Webhook Data Structure

Standard structure:
```json
{
  "headers": {
    "content-type": "application/json",
    "user-agent": "...",
    "x-custom-header": "..."
  },
  "params": {
    "id": "123"  // From URL: /webhook/form/:id
  },
  "query": {
    "token": "abc"  // From URL: /webhook/form?token=[REDACTED_SECRET]
  },
  "body": {
    // ⚠️ YOUR DATA IS HERE!
    "name": "John",
    "email": "john@example.com"
  }
}
```

Accessing different parts:
```javascript
// Headers
{{$json.headers['content-type']}}
{{$json.headers['x-api-key']}}

// URL Parameters
{{$json.params.id}}

// Query Parameters
{{$json.query.token}}
{{$json.query.page}}

// Body (MOST COMMON)
{{$json.body.email}}
{{$json.body.user.name}}
{{$json.body.items[0].price}}
```

## Authentication & Security

**1. Query parameter token** — simple but less secure:
```javascript
// IF node - validate token
{{$json.query.token}} equals "your-secret-token"
```

**2. Header-based auth** — better security:
```javascript
// IF node - check header
{{$json.headers['x-api-key']}} equals "your-api-key"
```

**3. Signature verification** — best security (for webhooks from services like Stripe, GitHub):
```javascript
// Code node
const crypto = require('crypto');
const signature = $input.item.headers['x-signature'];
const secret = $credentials.webhookSecret;

const calculatedSig = crypto
  .createHmac('sha256', secret)
  .update(JSON.stringify($input.item.body))
  .digest('hex');

if (signature !== `sha256=${calculatedSig}`) {
  throw new Error('Invalid signature');
}

return $input.item.body;
```

**4. IP whitelist** — restrict access by IP in workflow settings; configure specific allowed IP ranges; use for internal systems.

## Response Modes

**onReceived (default)** — immediate 200 OK response, workflow continues in the background. Use for long-running workflows, when the response doesn't depend on the workflow's result, or for fire-and-forget processing.
```javascript
{
  responseMode: "onReceived",
  responseCode: 200
}
```

**lastNode (custom response)** — wait for workflow completion, then send a custom response. Use when you need to return data to the caller, need synchronous processing, or are handling form submissions with a confirmation.
```javascript
{
  responseMode: "lastNode"
}
```
Then add a Webhook Response node:
```javascript
{
  statusCode: 200,
  headers: {
    "Content-Type": "application/json"
  },
  body: {
    "id": "={{$json.record_id}}",
    "status": "success"
  }
}
```

## Error Handling

**Pattern 1: try-catch with Error Trigger**
```
Main Flow:
  Webhook → [nodes...] → Success Response

Error Flow:
  Error Trigger → Log Error → Slack Alert → Error Response
```
Error Trigger configuration:
```javascript
{
  workflowId: "current-workflow-id"
}
```
Error response (if responseMode: "lastNode"):
```javascript
{
  statusCode: 500,
  body: {
    "status": "error",
    "message": "Processing failed"
  }
}
```

**Pattern 2: validation early exit**
```
Webhook → IF (validate) → [True: Process]
                       └→ [False: Error Response]
```
False-branch response:
```javascript
{
  statusCode: 400,
  body: {
    "status": "error",
    "message": "Invalid data: missing email"
  }
}
```

**Pattern 3: continue on fail** — a per-node setting to continue even if a node fails. Use for non-critical notifications:
```
Webhook → Database (critical) → Slack (continueOnFail: true)
```

## Testing Webhooks

1. **Use a Manual Trigger** with test data set manually in place of the webhook while developing.
2. **Use curl**:
```bash
curl -X POST https://n8n.example.com/webhook/form-submit \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "name": "Test User"}'
```
3. **Use Postman/Insomnia** — create a request collection, test different payloads, verify responses.
4. **Use a public webhook-capture site** (e.g. webhook.site) to view raw incoming requests while debugging the sending side.

## Performance Considerations

**Large payloads** — the default webhook timeout is 120 seconds. For large data, consider async processing:
```
Webhook → Queue (Redis/DB) → Response (immediate)

Separate Workflow:
Schedule → Check Queue → Process
```

**High volume** — use "Execute Once" mode if processing all items together; consider rate limiting; monitor execution times; scale the n8n instance if needed.

**Retries** — webhook calls typically don't retry automatically. Implement retry logic on the caller's side, or use a queue pattern for guaranteed processing.

## Common Gotchas

**1. Wrong: accessing webhook data as `{{$json.email}}`** — empty or undefined. **Correct**: `{{$json.body.email}}` — data is under `.body`.

**2. Wrong: response mode confusion** — using a Webhook Response node while `responseMode` is still `"onReceived"` (the node is ignored). **Correct**: set `responseMode: "lastNode"` to actually use the Webhook Response node.

**3. Wrong: no validation** — assuming data is always present and valid. **Correct**: validate data early with an IF node or Code node.

**4. Wrong: hardcoded paths** — using the same webhook path for dev and prod. **Correct**: use environment variables, e.g. `{{$env.WEBHOOK_PATH_PREFIX}}/form-submit`.

## Checklist for Webhook Workflows

**Setup**
- [ ] Choose descriptive webhook path
- [ ] Configure HTTP method (POST most common)
- [ ] Choose response mode (onReceived vs lastNode)
- [ ] Test webhook URL before connecting services

**Security**
- [ ] Add authentication (token, signature, IP whitelist)
- [ ] Validate incoming data
- [ ] Sanitize user input (if storing/displaying)
- [ ] Use HTTPS (always)

**Data Handling**
- [ ] Remember data is under $json.body
- [ ] Handle missing fields gracefully
- [ ] Transform data to desired format
- [ ] Log important data (for debugging)

**Error Handling**
- [ ] Add Error Trigger workflow
- [ ] Validate required fields
- [ ] Return appropriate error responses
- [ ] Alert team on failures

**Testing**
- [ ] Test with curl/Postman
- [ ] Test error scenarios
- [ ] Verify response format
- [ ] Monitor first executions
