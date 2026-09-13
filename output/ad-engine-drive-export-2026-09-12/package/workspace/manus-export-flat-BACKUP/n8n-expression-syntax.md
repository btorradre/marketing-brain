# n8n Expression Syntax

Reference for writing correct n8n expressions — the `{{ }}` templating syntax used inside node fields (Set, IF, Switch, HTTP Request, Slack, Email, Postgres, webhook response bodies, and virtually every other node type) to pull in dynamic data from previous nodes. Use this whenever configuring a node field that needs to reference data from a previous step — the webhook payload, another node's output, the current timestamp, an environment variable — or whenever troubleshooting an expression that's returning `undefined`, showing up as literal text, or throwing a syntax error. This is distinct from the Code node, which uses plain JavaScript instead of `{{ }}` expressions — see the n8n-code-javascript doc for that.

## How to use this

1. **Always wrap dynamic content in double curly braces.** This is the fundamental rule everything else builds on.
   ```
   ✅ {{$json.email}}
   ✅ {{$json.body.name}}
   ✅ {{$node["HTTP Request"].json.data}}
   ❌ $json.email  (no braces - treated as literal text)
   ❌ {$json.email}  (single braces - invalid)
   ```
   If a field is showing the literal text `$json.email` instead of the actual value, this is the first thing to check — the braces are missing.

2. **Identify which core variable you need.**
   - `$json` — current node's output data. `{{$json.fieldName}}`, `{{$json['field with spaces']}}`, `{{$json.nested.property}}`, `{{$json.items[0].name}}`.
   - `$node` — reach into any previous node's output by name. `{{$node["Node Name"].json.fieldName}}`. Node names must be in quotes, are case-sensitive, and must match the exact node name shown in the workflow.
   - `$now` — current timestamp. `{{$now}}`, `{{$now.toFormat('yyyy-MM-dd')}}`, `{{$now.toFormat('HH:mm:ss')}}`, `{{$now.plus({days: 7})}}`.
   - `$env` — environment variables. `{{$env.API_KEY}}`, `{{$env.DATABASE_URL}}`. Warning: some n8n instances have `N8N_BLOCK_ENV_ACCESS_IN_NODE` enabled, which blocks `$env` access entirely. If `$env` returns errors, fall back to: storing the value in the credential system instead, using a Set node with a manually entered value, or passing the value through webhook query parameters.

3. **Before writing any expression that touches webhook data, remember the single most common mistake in n8n: webhook data is NOT at the root.** The Webhook node wraps everything — POST body, query parameters, headers — inside a `body` property, to preserve room for headers/params/query alongside it. This one gotcha causes more broken workflows than anything else in this document.
   ```
   ❌ WRONG: {{$json.name}}
   ❌ WRONG: {{$json.email}}

   ✅ CORRECT: {{$json.body.name}}
   ✅ CORRECT: {{$json.body.email}}
   ✅ CORRECT: {{$json.body.message}}
   ```
   Full webhook output shape:
   ```javascript
   {
     "headers": {...},
     "params": {...},
     "query": {...},
     "body": {           // ⚠️ USER DATA IS HERE!
       "name": "John",
       "email": "john@example.com",
       "message": "Hello"
     }
   }
   ```

4. **Decide whether you're in a context where `{{ }}` is even valid.** It is NOT valid in three places:
   - **Code nodes.** These use direct JavaScript access, not expressions.
     ```javascript
     // ❌ WRONG in Code node
     const email = '={{$json.email}}';
     const name = '{{$json.body.name}}';

     // ✅ CORRECT in Code node
     const email = $json.email;
     const name = $json.body.name;

     // Or using the Code node's own API
     const email = $input.item.json.email;
     const allItems = $input.all();
     ```
   - **Webhook paths.** Paths must be static strings.
     ```javascript
     // ❌ WRONG
     path: "{{$json.user_id}}/webhook"
     path: "users/={{$env.TENANT_ID}}"

     // ✅ CORRECT
     path: "my-webhook"              // Static paths only
     path: "user-webhook/:userId"    // Use dynamic URL parameters instead
     ```
   - **Credential fields.** Use n8n's credential system, not expressions, for API keys and secrets.
     ```javascript
     // ❌ WRONG
     apiKey: "={{$env.API_KEY}}"

     // ✅ CORRECT
     Use n8n credential system, not expressions
     ```

5. **When a field name or node name contains spaces, diacritics, or special characters, switch to bracket notation** — dot notation breaks the moment it hits a space.
   ```javascript
   ❌ {{$json.field name}}
   ✅ {{$json['field name']}}

   ❌ {{$node.HTTP Request.json}}
   ✅ {{$node["HTTP Request"].json}}

   // Bracket notation is mandatory for keys with special characters
   ✅ {{$json['Gross Price w/o shipment']}}
   ✅ {{$json['Cena brutto zł']}}
   ```

6. **Match node names exactly, including case.** Node references are case-sensitive.
   ```javascript
   ❌ {{$node["http request"].json}}  // lowercase
   ❌ {{$node["Http Request"].json}}  // wrong case
   ✅ {{$node["HTTP Request"].json}}  // exact match
   ```

7. **Never nest or double-wrap expressions.**
   ```javascript
   ❌ {{{$json.field}}}
   ✅ {{$json.field}}
   ```

8. **When it fails, work through the debugging checklist in order** (full detail under Rules & Standards): braces present? webhook data needs `.body`? spaces in a field/node name needing brackets? node name case matches exactly? property path actually correct for the real data shape? Use the expression editor's live preview to check the actual result. Confirm you're not accidentally inside a Code node.

9. **Test every expression in the expression editor before shipping.** Click the field, open the expression editor (the "fx" icon), and read the live preview. Errors are highlighted in red there before the workflow ever runs.

## Rules & standards

### Validation rules (hard requirements)

1. **Always use `{{ }}`.** Expressions must be wrapped in double curly braces to be evaluated; unwrapped text is treated as a literal string.
   ```javascript
   ❌ $json.field
   ✅ {{$json.field}}
   ```

2. **Use bracket notation for spaces and special characters** in field or node names.
   ```javascript
   ❌ {{$json.field name}}
   ✅ {{$json['field name']}}

   ❌ {{$node.HTTP Request.json}}
   ✅ {{$node["HTTP Request"].json}}
   ```

3. **Match exact node names**, case-sensitively.
   ```javascript
   ❌ {{$node["http request"].json}}
   ❌ {{$node["Http Request"].json}}
   ✅ {{$node["HTTP Request"].json}}
   ```

4. **No nested `{{ }}`.**
   ```javascript
   ❌ {{{$json.field}}}
   ✅ {{$json.field}}
   ```

### The 15-item common mistakes catalog

**1. Missing curly braces.** Expression not recognized, shows as literal text.
- Wrong: `$json.email`
- Correct: `{{$json.email}}`
- Why it fails: n8n treats text without `{{ }}` as a literal string. Expressions must be wrapped to be evaluated.
- How to identify: the field shows the exact text `$json.email` instead of the actual value.

**2. Webhook body access.** Undefined values when accessing webhook data.
- Wrong: `{{$json.name}}`, `{{$json.email}}`, `{{$json.message}}`
- Correct: `{{$json.body.name}}`, `{{$json.body.email}}`, `{{$json.body.message}}`
- Why it fails: the Webhook node wraps incoming data under a `.body` property. The root `$json` contains headers, params, query, and body.
- Webhook structure:
  ```javascript
  {
    "headers": {...},
    "params": {...},
    "query": {...},
    "body": {         // User data is HERE!
      "name": "John",
      "email": "john@example.com"
    }
  }
  ```
- How to identify: a webhook workflow shows "undefined" for fields that are definitely being sent by the client.

**3. Spaces in field names.** Syntax error or undefined value.
- Wrong: `{{$json.first name}}`, `{{$json.user data.email}}`
- Correct: `{{$json['first name']}}`, `{{$json['user data'].email}}`
- Why it fails: spaces break dot notation — JavaScript interprets a space as the end of the property name.
- How to identify: an "unexpected token" error message, or undefined even though the field exists.

**4. Spaces in node names.** Cannot access other node's data.
- Wrong: `{{$node.HTTP Request.json.data}}`, `{{$node.Respond to Webhook.json}}`
- Correct: `{{$node["HTTP Request"].json.data}}`, `{{$node["Respond to Webhook"].json}}`
- Why it fails: node names are treated as object property names and need quotes when they contain spaces.
- How to identify: an error like "Cannot read property 'Request' of undefined."

**5. Incorrect node reference case.** Undefined or wrong data returned.
- Wrong: `{{$node["http request"].json.data}}` (lowercase), `{{$node["Http Request"].json.data}}` (wrong capitalization)
- Correct: `{{$node["HTTP Request"].json.data}}` (exact match)
- Why it fails: node names are case-sensitive and must match exactly as shown in the workflow.
- How to identify: an undefined value even though the node exists and has data.

**6. Double wrapping.** Literal `{{ }}` appears in output.
- Wrong: `{{{$json.field}}}`
- Correct: `{{$json.field}}`
- Why it fails: only one set of `{{ }}` is needed; extra braces are treated as literal characters.
- How to identify: output shows `{{value}}` instead of just `value`.

**7. Array access with dots.** Syntax error or undefined.
- Wrong: `{{$json.items.0.name}}`, `{{$json.users.1.email}}`
- Correct: `{{$json.items[0].name}}`, `{{$json.users[1].email}}`
- Why it fails: array indices require brackets, not dots — a number after a dot is invalid JavaScript.
- How to identify: a syntax error, or "Cannot read property '0' of undefined."

**8. Using expressions in Code nodes.** Literal string instead of a value, or errors.
- Wrong (in Code node):
  ```javascript
  const email = '{{$json.email}}';
  const name = '={{$json.body.name}}';
  ```
- Correct (in Code node):
  ```javascript
  const email = $json.email;
  const name = $json.body.name;

  // Or using Code node API
  const email = $input.item.json.email;
  const allItems = $input.all();
  ```
- Why it fails: Code nodes have direct access to data. `{{ }}` syntax is for expression fields in other node types, not for JavaScript code.
- How to identify: the literal string `{{$json.email}}` appears in the Code node's output instead of the actual value.

**9. Missing quotes in `$node` reference.** Syntax error.
- Wrong: `{{$node[HTTP Request].json.data}}`
- Correct: `{{$node["HTTP Request"].json.data}}`
- Why it fails: node names must be quoted strings inside the brackets.
- How to identify: a syntax error reading "Unexpected identifier."

**10. Incorrect property path.** Undefined value.
- Wrong: `{{$json.data.items.name}}` (items is an array, not an object — needs an index), `{{$json.user.email}}` (the property is actually named `userData`, not `user`)
- Correct: `{{$json.data.items[0].name}}`, `{{$json.userData.email}}`
- Why it fails: the path to the data is wrong — arrays need an index, and property names must be exact.
- How to identify: check the actual data structure using the expression editor's live preview.

**11. Using the `=` prefix outside JSON mode.** Literal `=` appears in output.
- Wrong (in a plain text field): `Email: ={{$json.email}}`
- Correct (in a plain text field): `Email: {{$json.email}}`
- Note: the `=` prefix is only needed in JSON mode, or when you want to set an entire field's value to an expression's result:
  ```javascript
  // JSON mode (set property to expression)
  {
    "email": "={{$json.body.email}}"
  }

  // Text mode (no = needed)
  Hello {{$json.body.name}}!
  ```
- Why it fails: the `=` is parsed as literal text in non-JSON contexts.
- How to identify: output shows `=john@example.com` instead of `john@example.com`.

**12. Expressions in webhook path.** Path doesn't update, validation error.
- Wrong: `path: "{{$json.user_id}}/webhook"`, `path: "users/={{$env.TENANT_ID}}"`
- Correct: `path: "my-webhook"` (static paths only), `path: "user-webhook/:userId"` (use dynamic URL parameters instead)
- Why it fails: webhook paths must be static. Use dynamic URL parameters (`:paramName`) instead of expressions.
- How to identify: the webhook path doesn't change, or validation warns about an invalid path.

**13. Forgetting `.json` in `$node` reference.** Undefined or wrong data.
- Wrong: `{{$node["HTTP Request"].data}}` (missing `.json`), `{{$node["Webhook"].body.email}}` (missing `.json`)
- Correct: `{{$node["HTTP Request"].json.data}}`, `{{$node["Webhook"].json.body.email}}`
- Why it fails: node data is always under a `.json` property (or `.binary` for binary data).
- How to identify: an undefined value when you know the node has data.

**14. String concatenation confusion.** Attempting JavaScript template-literal syntax inside an expression field.
- Wrong: `` `Hello ${$json.name}!` `` (template literal syntax), `"Hello " + $json.name + "!"` (string concatenation)
- Correct: `Hello {{$json.name}}!` — n8n expressions auto-concatenate adjacent text and expressions.
- Why it fails: n8n expressions don't use JavaScript template-literal syntax.
- How to identify: literal backticks or `+` symbols appear in the output.

**15. Empty expression brackets.** Literal `{{}}` in output.
- Wrong: `{{}}`, `{{ }}`
- Correct: `{{$json.field}}` — include actual expression content.
- Why it fails: empty expression brackets have nothing to evaluate.
- How to identify: literal `{{ }}` text appears in the output.

### Quick reference table (symptom → fix)

| Error | Symptom | Fix |
|-------|---------|-----|
| No `{{ }}` | Literal text | Add `{{ }}` |
| Webhook data | Undefined | Add `.body` |
| Space in field | Syntax error | Use `['field name']` |
| Space in node | Undefined | Use `["Node Name"]` |
| Wrong case | Undefined | Match exact case |
| Double `{{ }}` | Literal braces | Remove extra `{{ }}` |
| `.0` array access | Syntax error | Use `[0]` |
| `{{ }}` in Code node | Literal string | Remove `{{ }}` |
| No quotes in `$node` | Syntax error | Add quotes |
| Wrong path | Undefined | Check data structure |
| `=` in text field | Literal `=` | Remove `=` prefix |
| Dynamic webhook path | Doesn't work | Use static path |
| Missing `.json` | Undefined | Add `.json` |
| Template literals | Literal text | Use `{{ }}` |
| Empty `{{ }}` | Literal braces | Add expression content |

### Debugging process, in order

When an expression doesn't work, work through these checks in sequence:

1. **Check braces**: Is it wrapped in `{{ }}`?
2. **Check data source**: Is it webhook data? Add `.body`.
3. **Check spaces**: Does the field or node name have spaces? Use bracket notation.
4. **Check case**: Does the node name match exactly?
5. **Check path**: Is the property path actually correct for the real data shape?
6. **Use the expression editor**: the live preview shows the actual result.
7. **Check context**: Is this a Code node? Remove the `{{ }}` — Code nodes use plain JavaScript.

### Common error messages and what they mean

- **"Cannot read property 'X' of undefined"** → the parent object doesn't exist. Check your data path.
- **"X is not a function"** → you're trying to call a method on something that isn't a function. Check the variable's actual type.
- **Expression shows as literal text** → missing `{{ }}`. Add curly braces.

### Do / Don't summary

**Do:**
- Always use `{{ }}` for dynamic content.
- Use bracket notation for field names with spaces.
- Reference webhook data from `.body`.
- Use `$node` for data from other nodes.
- Test expressions in the expression editor.

**Don't:**
- Don't use `{{ }}` expressions in Code nodes.
- Don't forget quotes around node names with spaces.
- Don't double-wrap with extra `{{ }}`.
- Don't assume webhook data is at the root — it's under `.body`.
- Don't use expressions in webhook paths or credential fields.

### Essential rules, condensed

1. Wrap expressions in `{{ }}`.
2. Webhook data is under `.body`.
3. No `{{ }}` in Code nodes.
4. Quote node names that contain spaces.
5. Node names are case-sensitive.

### Available expression helper methods

**String**: `.toLowerCase()`, `.toUpperCase()`, `.trim()`, `.replace()`, `.substring()`, `.split()`, `.includes()`

**Array**: `.length`, `.map()`, `.filter()`, `.find()`, `.join()`, `.slice()`

**DateTime** (Luxon): `.toFormat()`, `.toISO()`, `.toLocal()`, `.plus()`, `.minus()`, `.set()`

**Number**: `.toFixed()`, `.toString()`, math operations `+`, `-`, `*`, `/`, `%`

## Templates & examples

### Accessing nested fields

```javascript
// Simple nesting
{{$json.user.email}}

// Array access
{{$json.data[0].name}}
{{$json.items[0].id}}

// Bracket notation for spaces
{{$json['field name']}}
{{$json['user data']['first name']}}
```

### Referencing other nodes

```javascript
// Node without spaces
{{$node["Set"].json.value}}

// Node with spaces (common!)
{{$node["HTTP Request"].json.data}}
{{$node["Respond to Webhook"].json.message}}

// Webhook node
{{$node["Webhook"].json.body.email}}
```

### Combining variables

```javascript
// Concatenation (automatic)
Hello {{$json.body.name}}!

// In URLs
https://api.example.com/users/{{$json.body.user_id}}

// In object properties
{
  "name": "={{$json.body.name}}",
  "email": "={{$json.body.email}}"
}
```

### Data type handling

**Arrays**
```javascript
// First item
{{$json.users[0].email}}

// Array length
{{$json.users.length}}

// Last item
{{$json.users[$json.users.length - 1].name}}
```

**Objects**
```javascript
// Dot notation (no spaces)
{{$json.user.email}}

// Bracket notation (with spaces or dynamic)
{{$json['user data'].email}}
```

**Strings**
```javascript
// Concatenation (automatic)
Hello {{$json.name}}!

// String methods
{{$json.email.toLowerCase()}}
{{$json.name.toUpperCase()}}
```

**Numbers**
```javascript
// Direct use
{{$json.price}}

// Math operations
{{$json.price * 1.1}}  // Add 10%
{{$json.quantity + 5}}
```

### Advanced patterns

**Conditional content**
```javascript
// Ternary operator
{{$json.status === 'active' ? 'Active User' : 'Inactive User'}}

// Default values
{{$json.email || 'no-email@example.com'}}
```

**Date manipulation**
```javascript
// Add days
{{$now.plus({days: 7}).toFormat('yyyy-MM-dd')}}

// Subtract hours
{{$now.minus({hours: 24}).toISO()}}

// Set specific date
{{DateTime.fromISO('2025-12-25').toFormat('MMMM dd, yyyy')}}
```

**String manipulation**
```javascript
// Substring
{{$json.email.substring(0, 5)}}

// Replace
{{$json.message.replace('old', 'new')}}

// Split and join
{{$json.tags.split(',').join(', ')}}
```

### Timestamp formatting reference

```javascript
// Current date
{{$now.toFormat('yyyy-MM-dd')}}
// Result: 2025-10-20

// Time
{{$now.toFormat('HH:mm:ss')}}
// Result: 14:30:45

// Full datetime
{{$now.toFormat('yyyy-MM-dd HH:mm')}}
// Result: 2025-10-20 14:30
```

Additional date examples, with current time as a reference point of 2025-10-20 14:30:45:

```javascript
// ISO Format
{{$now.toISO()}}
// Output: 2025-10-20T14:30:45.000Z

// Custom Date Format
{{$now.toFormat('yyyy-MM-dd')}}
// Output: 2025-10-20

// Time Only
{{$now.toFormat('HH:mm:ss')}}
// Output: 14:30:45

// Full Readable Format
{{$now.toFormat('MMMM dd, yyyy')}}
// Output: October 20, 2025

// Date Math - Future
{{$now.plus({days: 7}).toFormat('yyyy-MM-dd')}}
// Output: 2025-10-27

// Date Math - Past
{{$now.minus({hours: 24}).toFormat('yyyy-MM-dd HH:mm')}}
// Output: 2025-10-19 14:30
```

### Worked example 1 — Webhook form submission to Slack

Workflow: Webhook → Slack.

Webhook input (POST):
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "company": "Acme Corp",
  "message": "Interested in your product"
}
```

Webhook node output (note everything moved under `body`):
```json
{
  "headers": {"content-type": "application/json"},
  "params": {},
  "query": {},
  "body": {
    "name": "John Doe",
    "email": "john@example.com",
    "company": "Acme Corp",
    "message": "Interested in your product"
  }
}
```

In the Slack node's text field:
```
New form submission! 📝

Name: {{$json.body.name}}
Email: {{$json.body.email}}
Company: {{$json.body.company}}
Message: {{$json.body.message}}
```

Resulting output:
```
New form submission! 📝

Name: John Doe
Email: john@example.com
Company: Acme Corp
Message: Interested in your product
```

### Worked example 2 — HTTP API to database

Workflow: Schedule → HTTP Request → Postgres.

HTTP Request returns:
```json
{
  "data": {
    "users": [
      {
        "id": 123,
        "name": "Alice Smith",
        "email": "alice@example.com",
        "role": "admin"
      }
    ]
  }
}
```

In the Postgres node's INSERT statement:
```sql
INSERT INTO users (user_id, name, email, role, synced_at)
VALUES (
  {{$json.data.users[0].id}},
  '{{$json.data.users[0].name}}',
  '{{$json.data.users[0].email}}',
  '{{$json.data.users[0].role}}',
  '{{$now.toFormat('yyyy-MM-dd HH:mm:ss')}}'
)
```

Result: the user row is inserted with the current timestamp.

### Worked example 3 — Multi-node data flow (Webhook → HTTP Request → Email)

Workflow structure:
1. Webhook receives an order ID.
2. HTTP Request fetches order details.
3. Email sends a confirmation.

**Node 1: Webhook** receives:
```json
{
  "body": {
    "order_id": "ORD-12345"
  }
}
```

**Node 2: HTTP Request** — URL field:
```
https://api.example.com/orders/{{$json.body.order_id}}
```

Returns:
```json
{
  "order": {
    "id": "ORD-12345",
    "customer": "Bob Jones",
    "total": 99.99,
    "items": ["Widget", "Gadget"]
  }
}
```

**Node 3: Email** — Subject:
```
Order {{$node["Webhook"].json.body.order_id}} Confirmed
```

Body:
```
Dear {{$node["HTTP Request"].json.order.customer}},

Your order {{$node["Webhook"].json.body.order_id}} has been confirmed!

Total: ${{$node["HTTP Request"].json.order.total}}
Items: {{$node["HTTP Request"].json.order.items.join(', ')}}

Thank you for your purchase!
```

Email result:
```
Subject: Order ORD-12345 Confirmed

Dear Bob Jones,

Your order ORD-12345 has been confirmed!

Total: $99.99
Items: Widget, Gadget

Thank you for your purchase!
```

### Worked example 4 — Array operations

Data:
```json
{
  "users": [
    {"name": "Alice", "email": "alice@example.com"},
    {"name": "Bob", "email": "bob@example.com"},
    {"name": "Charlie", "email": "charlie@example.com"}
  ]
}
```

First user: `{{$json.users[0].name}}` → `Alice`

Last user: `{{$json.users[$json.users.length - 1].name}}` → `Charlie`

All emails (join): `{{$json.users.map(u => u.email).join(', ')}}` → `alice@example.com, bob@example.com, charlie@example.com`

Array length: `{{$json.users.length}}` → `3`

### Worked example 5 — Conditional logic

Data:
```json
{
  "order": {
    "status": "completed",
    "total": 150
  }
}
```

Ternary operator: `{{$json.order.status === 'completed' ? 'Order Complete ✓' : 'Pending...'}}` → `Order Complete ✓`

Default values: `{{$json.order.notes || 'No notes provided'}}` → `No notes provided` (when the `notes` field doesn't exist)

Multiple conditions: `{{$json.order.total > 100 ? 'Premium Customer' : 'Standard Customer'}}` → `Premium Customer`

### Worked example 6 — String manipulation

Data:
```json
{
  "user": {
    "email": "JOHN@EXAMPLE.COM",
    "message": "  Hello World  "
  }
}
```

Lowercase: `{{$json.user.email.toLowerCase()}}` → `john@example.com`

Uppercase: `{{$json.user.message.toUpperCase()}}` → `  HELLO WORLD  `

Trim: `{{$json.user.message.trim()}}` → `Hello World`

Substring: `{{$json.user.email.substring(0, 4)}}` → `JOHN`

Replace: `{{$json.user.message.replace('World', 'n8n')}}` → `  Hello n8n  `

### Worked example 7 — Fields with spaces

Data:
```json
{
  "user data": {
    "first name": "Jane",
    "last name": "Doe",
    "phone number": "+1234567890"
  }
}
```

Bracket notation: `{{$json['user data']['first name']}}` → `Jane`

Combined: `{{$json['user data']['first name']}} {{$json['user data']['last name']}}` → `Jane Doe`

Nested spaces: `Contact: {{$json['user data']['phone number']}}` → `Contact: +1234567890`

### Worked example 8 — Code node (direct access, no `{{ }}`)

Input (from a Webhook node):
```json
{
  "body": {
    "items": ["apple", "banana", "cherry"]
  }
}
```

Code:
```javascript
// ✅ Direct access (no {{ }})
const items = $json.body.items;

// Transform to uppercase
const uppercased = items.map(item => item.toUpperCase());

// Return in n8n format
return [{
  json: {
    original: items,
    transformed: uppercased,
    count: items.length
  }
}];
```

Output:
```json
{
  "original": ["apple", "banana", "cherry"],
  "transformed": ["APPLE", "BANANA", "CHERRY"],
  "count": 3
}
```

### Worked example 9 — Environment variables

Setup: environment variable `API_KEY=secret123`.

In an HTTP Request header:
```javascript
Authorization: Bearer {{$env.API_KEY}}
```
Result: `Authorization: Bearer secret123`

In a URL:
```javascript
https://api.example.com/data?key={{$env.API_KEY}}
```
Result: `https://api.example.com/data?key=secret123`

### Worked example 10 — Real workflow template (Weather to Slack)

Workflow structure: Webhook → OpenStreetMap API → Weather API → Slack.

Webhook slash command input: `/weather London`

Webhook receives:
```json
{
  "body": {
    "text": "London"
  }
}
```

OpenStreetMap API — URL:
```
https://nominatim.openstreetmap.org/search?q={{$json.body.text}}&format=json
```

Weather API (NWS) — URL:
```
https://api.weather.gov/points/{{$node["OpenStreetMap"].json[0].lat}},{{$node["OpenStreetMap"].json[0].lon}}
```

Slack message:
```
Weather for {{$json.body.text}}:

Temperature: {{$node["Weather API"].json.properties.temperature.value}}°C
Conditions: {{$node["Weather API"].json.properties.shortForecast}}
```

### Most common expression patterns, at a glance

- `{{$json.body.field}}` — webhook data
- `{{$node["Name"].json.field}}` — other node's data
- `{{$now.toFormat('yyyy-MM-dd')}}` — timestamps
- `{{$json.array[0].field}}` — array access
- `{{$json.field || 'default'}}` — default values
