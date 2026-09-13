# The 15-Item Common Mistakes Catalog

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
