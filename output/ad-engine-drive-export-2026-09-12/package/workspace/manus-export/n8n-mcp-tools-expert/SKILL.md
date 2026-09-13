---
name: n8n-mcp-tools-expert
description: Reference for going from "I need an n8n workflow that does X" to a validated, deployable workflow — finding the right node type for each step, reading its real configuration schema before touching any parameters, assembling correct workflow JSON (nodes, connections, credentials), and running the structural/logical checks that catch a broken workflow before it goes live. Use this whenever building, editing, or reviewing an n8n workflow — picking the right node for an integration, wiring IF/Switch branches or AI Agent connections correctly, attaching credentials, or doing a security pass over an existing workflow.
---

# n8n Workflow Assembly & Validation

## How to Use This

1. **Identify the node(s) you need.** Before configuring anything, find the specific n8n node type that matches the integration or logic required (Slack, HTTP Request, Webhook, IF, Switch, Set, Code, AI Agent, etc.). Search n8n's own node reference — the node panel inside the n8n editor, or n8n's public docs at `docs.n8n.io/integrations/` — by keyword: the service name ("slack"), the general action ("http", "database", "email"), or the category ("ai agent"). If an exact term returns nothing, try a broader or typo-tolerant variant before giving up.

2. **Get the node's exact type string right.** In real n8n workflow JSON, a node's `type` field always uses the full, package-prefixed form:
   - Core/community nodes: `n8n-nodes-base.<nodeName>` — e.g. `n8n-nodes-base.slack`, `n8n-nodes-base.httpRequest`, `n8n-nodes-base.webhook`
   - LangChain/AI nodes: `@n8n/n8n-nodes-langchain.<nodeName>` — e.g. `@n8n/n8n-nodes-langchain.agent`

   n8n will not resolve a node from its display name or a guessed/shortened string — get the spelling exact. There is no shorthand form in real workflow JSON.

3. **Pull the node's full configuration schema before writing any parameters.** Open that node's documentation (docs.n8n.io, or inspect it directly by dragging it onto a canvas in the n8n editor and opening its parameter panel) and read its available resources/operations and which fields are required vs optional. Don't guess — many nodes expose several `resource` values (e.g. Slack: message / channel / user), each with its own `operation` list, and each operation reveals a different subset of fields. If you only need one specific answer — what the auth options are, which field holds the request body — search within that documentation for the specific term rather than re-reading the whole schema.

4. **Draft the node's parameters and, if needed, its credential.** Fill in the node's `parameters` object using the field names exactly as documented. If the node needs a credential, credentials live in n8n's own credential store and are referenced from the node by credential **type** (e.g. `slackApi`, `httpHeaderAuth`) with an `{id, name}` pair pointing at a stored credential — never inline a raw secret value into `parameters`.

5. **Assemble the full workflow JSON** — `nodes[]` + `connections{}` + optional `settings{}`. See `references/templates.md` for the exact shape, including IF/Switch branch wiring and AI Agent connection types.

6. **Run a validation pass over the whole workflow before deploying** — work through the checklist below. Treat this as a distinct step, not something you do once at the very end only.

7. **Import/create the workflow, then iterate in small edits and re-validate.** Building a workflow in one giant shot and hoping it's right the first time is the wrong instinct — configure a piece, validate it, fix it, move to the next piece. Re-validate after every non-trivial change, especially after adding/removing nodes or rewiring connections: a change in one place can silently break something elsewhere (a renamed node still referenced by a stale connection, a Switch node with 3 rules but only 2 wired outputs, a Code node edit that broke the return shape).

8. **Before calling it done, run one more full-workflow structural check**, and only then activate it.

## Rules & Standards

### Node type naming
Actual n8n workflow JSON always uses the full, package-prefixed node type string — `n8n-nodes-base.X` for core/community nodes, `@n8n/n8n-nodes-langchain.X` for the AI/LangChain nodes.

### Expression syntax marker
A field on a node is only treated as a live n8n expression when its **value is a string starting with `=`**, followed by `{{ ... }}` — e.g. `"text": "={{$json.body.message}}"`. Omit the leading `=` and n8n treats the whole thing as a literal string, not an expression. This is one of the most common node-configuration mistakes — always double-check any field meant to pull dynamic data actually starts with `=`.

### IF / Switch branch semantics
- **IF node**: has two outputs. Output index 0 fires when the condition is true; output index 1 fires when false.
- **Switch node**: each defined rule maps to an output index in the order the rules are defined — rule 0 → output 0, rule 1 → output 1, and so on.
- When wiring the `connections` object by hand, `connections["IF"]["main"]` is an array of two arrays — index 0 holds the targets fed from the true output, index 1 holds the targets fed from the false output. Each target is `{node: "TargetName", type: "main", index: 0}` (the target's own input index, almost always 0 for a single-input node).

### Filter/IF condition operator rule — binary vs unary
- **Binary operators** (equals, notEquals, contains, notContains, greaterThan, lessThan, startsWith, endsWith) compare two values and must **not** carry a `singleValue: true` flag.
- **Unary operators** (isEmpty, isNotEmpty, true, false) check a single value and **must** carry `singleValue: true`.
  ```javascript
  // Binary — correct
  { "type": "boolean", "operation": "equals" }        // no singleValue

  // Unary — correct
  { "type": "boolean", "operation": "isEmpty", "singleValue": true }
  ```
  Getting this backwards produces a broken/invalid IF or Filter condition. Check it explicitly rather than assuming something downstream will silently correct it.

### Credential structure
A node's `credentials` field is keyed by credential **type**, with each entry an `{id, name}` pair pointing at a credential stored in n8n's own credential store:
```javascript
"credentials": {
  "httpHeaderAuth": {
    "id": "abc123",
    "name": "My API Key"
  }
}
```
Never a flat string, and never the raw secret value inline in the node — the actual secret lives only inside the stored credential object, addressed by id.

### AI Agent connection types
n8n's LangChain-based AI nodes use eight distinct connection types (used as the connection-array key when wiring a supporting node into an AI Agent):
- `ai_languageModel`
- `ai_tool`
- `ai_memory`
- `ai_outputParser`
- `ai_embedding`
- `ai_vectorStore`
- `ai_document`
- `ai_textSplitter`

An AI Agent node needs at minimum a language model connected; tools, memory, and an output parser are wired in as the design calls for, each using its matching type from the list above. See `references/templates.md` for a worked example.

### Data Tables (n8n's structured-data feature)
n8n has a native Data Table feature for structured storage inside workflows: tables have typed columns (`string`, `number`, `boolean`, `date`), and rows are queried/filtered with these conditions: `eq`, `neq`, `like`, `ilike`, `gt`, `gte`, `lt`, `lte`. A bulk delete always requires a filter — n8n does not allow wiping an entire table with an unscoped delete. Before a bulk update or delete, preview the affected rows with the same filter first rather than running the mutating operation blind.

### Before deploying — workflow-level structural checklist
- **Trigger present.** Every workflow needs at least one trigger node (Webhook, Schedule, manual, chat, etc.) — a workflow with no trigger can't run automatically.
- **No dangling connections.** Every connection must reference node names (or ids) that actually exist in the current `nodes[]` array. A rename or deletion that leaves a connection pointing at a name that no longer exists is a structural error.
- **Branch count matches.** If a Switch node defines N case rules, exactly N outputs must be wired — a mismatch (e.g. 3 rules, only 2 wired outputs) is a structural error that will silently drop data down the unwired case.
- **Required parameters filled.** Every required field on every node must be filled in — check the node's documented required fields, not just what "looks obviously needed."
- **Expression fields use the `=` prefix.** Any field meant to pull dynamic data must use the `="{{ }}"` form described above.
- **AI Agent wiring is complete.** AI Agent nodes need their required upstream connections wired with the correct `ai_*` connection type — at minimum a language model.

### Common validation error categories
When reviewing a node's configuration or a whole workflow, sort findings into these categories:
- **missing_required** — a required field with no value. Must fix.
- **invalid_value** — a value outside the field's allowed set/range. Must fix.
- **type_mismatch** — wrong type for the field (e.g. a string where a number is expected). Must fix.
- **best_practice** (warning) — not fatal, but worth fixing — e.g. no retry/error-handling configured on a node that calls an external API.
- **suggestion** — optional improvement, lowest priority.

A useful shape for writing up validation findings on any node or workflow:
```javascript
{
  "valid": false,
  "errors": [
    {
      "type": "missing_required",
      "property": "name",
      "message": "Channel name is required",
      "fix": "Provide a channel name (lowercase, no spaces, 1-80 characters)"
    }
  ],
  "warnings": [
    {
      "type": "best_practice",
      "property": "errorHandling",
      "message": "This API can have rate limits",
      "suggestion": "Add retry-on-fail / continue-on-error handling"
    }
  ]
}
```

### Security review checklist — for a single workflow or a whole n8n instance
n8n has a native, built-in security audit covering five categories: **credentials, database, nodes, instance, filesystem** (available from the n8n UI or via its own audit API endpoint). On top of that, when reviewing workflow JSON directly, check for:
- **Hardcoded secrets** — a literal API key/token/password sitting in a node's `parameters` instead of a proper credential reference. Scan for common key-shape patterns (long random-looking strings with recognizable prefixes like `sk-`, `xoxb-`, `AKIA`, etc.) and obvious PII shapes (email, phone, credit-card-like strings). See `references/templates.md` for scan-pattern regexes.
- **Unauthenticated webhooks** — any Webhook or Form trigger node with no authentication parameter set is an open, unauthenticated endpoint.
- **Missing error handling** — a workflow with 3+ nodes and no error-handling path (no error-output branch, no dedicated error workflow attached) will fail silently or ungracefully in production.
- **Data retention** — check the workflow's `settings` for whether it's configured to save all execution data (success and failure). Saving everything by default can retain sensitive payloads longer than necessary.

When reporting a found secret, mask it (show only the first few and last few characters) rather than reproducing the whole value in your findings.

### Editing an existing workflow's JSON
- **Add a node**: append a new object to `nodes[]` with a unique name/id, the correct `type`/`typeVersion`, a `position: [x, y]`, and its `parameters`.
- **Remove a node**: delete its entry from `nodes[]` AND remove any connections that reference it — a dangling connection to a removed node is a structural error.
- **Update a node**: edit its `parameters` (or other top-level fields) in place. Nested fields are addressed by dot-notation path, e.g. `parameters.jsCode`, `parameters.assignments.assignments.6.value`.
- **Move a node**: change its `position` array.
- **Enable/disable a node**: toggle its `disabled` flag.
- **Wire two nodes together**: add an entry under `connections[SourceNodeName].main[outputIndex]` pointing at `{node: TargetName, type: "main", index: inputIndex}` (or the matching `ai_*` connection type/array for AI connections).
- **Activate/deactivate**: n8n workflows carry an `active` boolean. Toggling it is what actually puts a workflow live on its triggers versus leaving it dormant/importable-but-inactive.

### Targeted text edits inside a Code node (or any long string field)
When you only need to change one specific piece of a node's code, HTML, or JSON-body string — not rewrite the whole field — do a scoped find/replace rather than regenerating the entire value from scratch. Before committing the edit, confirm the exact substring you're targeting actually appears in the current field value, and if you intend a single, unambiguous change, confirm it appears only once — otherwise you risk silently clobbering the wrong occurrence or making an ambiguous edit. This matters most on long fields (a sizeable Code node script, an email template, a large JSON body) where full regeneration is slow and risks losing unrelated content.

### General build discipline
- Iterate — don't try to produce a whole complex workflow in one shot. Configure and validate a piece at a time.
- Validate after every significant change, not just once at the end.
- Prefer the simplest node that does the job — a Set node for basic field mapping, a Filter node for basic filtering, an IF/Switch for a simple conditional, an HTTP Request node for a plain API call with no transformation — and reach for a Code node only when the logic genuinely needs it.
- Check whether n8n's public template library (n8n.io/workflows/) already has something close to what you need — searchable by keyword or by which node types it uses — before building from a blank canvas. Reviewing an existing template's JSON is often faster than starting from zero, even if you end up substantially rewriting it.

For the full workflow JSON templates — a minimal two-node workflow, IF/Switch branch wiring, credential reference shape, an AI Agent with language model and tool wired in, binary vs unary condition examples, Data Table row-filter shapes, and security-scan regex patterns — see `references/templates.md`.
