# Worked Examples — n8n Expression Syntax

## Data Type Handling

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

## Advanced Patterns

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

## Timestamp Formatting Reference

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

## Worked Example 1 — Webhook Form Submission to Slack

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

## Worked Example 2 — HTTP API to Database

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

## Worked Example 3 — Multi-Node Data Flow (Webhook → HTTP Request → Email)

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

## Worked Example 4 — Array Operations

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

## Worked Example 5 — Conditional Logic

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

## Worked Example 6 — String Manipulation

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

## Worked Example 7 — Fields with Spaces

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

## Worked Example 8 — Code Node (Direct Access, No `{{ }}`)

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

## Worked Example 9 — Environment Variables

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

## Worked Example 10 — Real Workflow Template (Weather to Slack)

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
