---
name: n8n-expression-syntax
description: Reference for writing correct n8n expressions — the `{{ }}` templating syntax used inside node fields (Set, IF, Switch, HTTP Request, Slack, Email, Postgres, webhook response bodies, and virtually every other node type) to pull in dynamic data from previous nodes. Use this whenever configuring a node field that needs to reference data from a previous step — the webhook payload, another node's output, the current timestamp, an environment variable — or whenever troubleshooting an expression that's returning `undefined`, showing up as literal text, or throwing a syntax error. This is distinct from the Code node, which uses plain JavaScript instead of `{{ }}` expressions.
---

# n8n Expression Syntax

## How to Use This

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
   - `$env` — environment variables. `{{$env.API_KEY}}`, `{{$env.DATABASE_URL}}`. Warning: some n8n instances block `$env` access entirely via a security setting. If `$env` returns errors, fall back to: storing the value in the credential system instead, using a Set node with a manually entered value, or passing the value through webhook query parameters.

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

8. **When it fails, work through the debugging checklist in order:** braces present? webhook data needs `.body`? spaces in a field/node name needing brackets? node name case matches exactly? property path actually correct for the real data shape? Use the expression editor's live preview to check the actual result. Confirm you're not accidentally inside a Code node.

9. **Test every expression in the expression editor before shipping.** Click the field, open the expression editor (the "fx" icon), and read the live preview. Errors are highlighted in red there before the workflow ever runs.

## Validation Rules (hard requirements)

1. **Always use `{{ }}`.** Expressions must be wrapped in double curly braces to be evaluated; unwrapped text is treated as a literal string.
2. **Use bracket notation for spaces and special characters** in field or node names.
3. **Match exact node names**, case-sensitively.
4. **No nested `{{ }}`.**

## Debugging Process, in Order

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

## Quick Reference Table (symptom → fix)

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

For the full 15-item common-mistakes catalog (wrong/correct/why/how-to-identify for each), see `references/common-mistakes.md`.

## Do / Don't Summary

**Do:** Always use `{{ }}` for dynamic content · use bracket notation for field names with spaces · reference webhook data from `.body` · use `$node` for data from other nodes · test expressions in the expression editor.

**Don't:** Use `{{ }}` expressions in Code nodes · forget quotes around node names with spaces · double-wrap with extra `{{ }}` · assume webhook data is at the root (it's under `.body`) · use expressions in webhook paths or credential fields.

## Available Expression Helper Methods

**String**: `.toLowerCase()`, `.toUpperCase()`, `.trim()`, `.replace()`, `.substring()`, `.split()`, `.includes()`

**Array**: `.length`, `.map()`, `.filter()`, `.find()`, `.join()`, `.slice()`

**DateTime** (Luxon): `.toFormat()`, `.toISO()`, `.toLocal()`, `.plus()`, `.minus()`, `.set()`

**Number**: `.toFixed()`, `.toString()`, math operations `+`, `-`, `*`, `/`, `%`

## Quick Templates

```javascript
// Accessing nested fields
{{$json.user.email}}
{{$json.data[0].name}}
{{$json['field name']}}

// Referencing other nodes
{{$node["HTTP Request"].json.data}}
{{$node["Webhook"].json.body.email}}

// Combining variables
Hello {{$json.body.name}}!
https://api.example.com/users/{{$json.body.user_id}}

// Conditional content
{{$json.status === 'active' ? 'Active User' : 'Inactive User'}}
{{$json.email || 'no-email@example.com'}}

// Date manipulation
{{$now.plus({days: 7}).toFormat('yyyy-MM-dd')}}
{{$now.minus({hours: 24}).toISO()}}
```

Most common expression patterns, at a glance: `{{$json.body.field}}` (webhook data) · `{{$node["Name"].json.field}}` (other node's data) · `{{$now.toFormat('yyyy-MM-dd')}}` (timestamps) · `{{$json.array[0].field}}` (array access) · `{{$json.field || 'default'}}` (default values).

For ten fully worked, end-to-end examples (webhook-to-Slack, HTTP-API-to-database, multi-node data flow, array operations, conditional logic, string manipulation, fields with spaces, Code node contrast, environment variables, and a full weather-to-Slack workflow), see `references/worked-examples.md`.
