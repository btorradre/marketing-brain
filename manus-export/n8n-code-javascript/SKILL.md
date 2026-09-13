---
name: n8n-code-javascript
description: Reference for writing JavaScript inside n8n's Code node — the node type used for custom data transformation, aggregation, filtering, API calls, and any logic too complex for n8n's simpler nodes (Set, Filter, IF/Switch, HTTP Request). Use this whenever a workflow needs a Code node — choosing between its two execution modes, accessing input data correctly, calling HTTP APIs from inside the node, working with dates, avoiding the handful of mistakes that cause the vast majority of Code node failures, or building any custom transformation logic (aggregation, filtering, format conversion, batch-processing logic).
---

# n8n JavaScript Code Node

## How to Use This

1. **Pick the execution mode first.** The Code node runs in one of two modes — get this right before writing anything, since it determines which data-access syntax is valid.
   - **Run Once for All Items** (the default, and correct choice ~95% of the time): the code executes once total, regardless of how many items came in. Access data via `$input.all()` (or the `items` array). Use this for aggregation, filtering, batch processing, transformations, sorting/ranking, deduplication, or any case where you're comparing or combining items across the dataset.
   - **Run Once for Each Item** (specialized cases only): the code executes separately per input item. Access the current item via `$input.item`. Use this only when each item genuinely needs independent handling — its own API call, its own validation with different error handling, or a transformation that depends on that item's own properties in a way that doesn't need to see other items.
   - Decision shortcut: need to look at multiple items at once → All Items mode. Each item is completely independent → Each Item mode. Not sure → default to All Items (you can always loop inside the code).

2. **Always return the correct format.** A Code node MUST return an array, and every element of that array MUST have a `json` property. This is the single most common source of failures.
   ```javascript
   // Correct — single result
   return [{ json: { field1: value1, field2: value2 } }];

   // Correct — multiple results
   return [
     { json: { id: 1, data: 'first' } },
     { json: { id: 2, data: 'second' } }
   ];

   // Correct — transformed array
   const transformed = $input.all()
     .filter(item => item.json.valid)
     .map(item => ({ json: { id: item.json.id, processed: true } }));
   return transformed;

   // Correct — empty result when there's nothing to return
   return [];
   ```
   Wrong formats that will break the workflow:
   ```javascript
   return { json: { field: value } };   // ✗ object, not array-wrapped
   return [{ field: value }];            // ✗ missing the json wrapper
   return "processed";                   // ✗ plain string
   return $input.all();                  // ✗ raw passthrough without mapping — risky, don't rely on existing structure
   return [{ data: value }];             // ✗ wrong key name — must be "json"
   ```

3. **Know that webhook data is nested under `.body`.** This is the single most common mistake. A Webhook node wraps everything — POST data, query parameters, JSON payloads — inside a `body` property.
   ```javascript
   // ✗ WRONG — returns undefined
   const name = $json.name;
   const email = $json.email;

   // ✓ CORRECT
   const name = $json.body.name;
   const email = $json.body.email;

   // or, extracting first
   const webhookData = $input.first().json.body;
   const name = webhookData.name;
   ```
   The full webhook output structure looks like:
   ```javascript
   {
     "headers": { "content-type": "application/json", "user-agent": "...", /* ... */ },
     "params": {},
     "query": {},
     "body": {
       // ← your actual data is here
       "name": "Alice",
       "email": "alice@example.com",
       "message": "Hello!"
     }
   }
   ```
   Also available on the same object: `webhook.query` (query-string parameters), `webhook.headers` (HTTP headers, e.g. `webhook.headers['content-type']`), and `webhook.method` / `webhook.url`.

4. **Use JavaScript directly — never n8n's `{{ }}` expression syntax inside a Code node.** The `{{ }}` templating syntax is for OTHER node types (Set, IF, HTTP Request). Inside a Code node, everything is plain JavaScript.
   ```javascript
   // ✗ WRONG
   const value = "{{ $json.field }}";           // literal string, not the value
   const message = `{{ $json.firstName }} {{ $json.lastName }}`;

   // ✓ CORRECT
   const value = $json.field;
   const message = `${$json.firstName} ${$json.lastName}`;  // template literal, backticks
   ```
   | Context | Syntax |
   |---|---|
   | Set node, IF node, HTTP Request URL, etc. | `{{ }}` expressions |
   | **Code node** | **plain JavaScript** |
   | Code node string interpolation | template literals with backticks: `` `Hello ${name}` `` |

5. **Guard against null/undefined before accessing nested data.** Use optional chaining (`?.`), nullish coalescing (`??`), default values (`||`), or explicit guard clauses — don't assume a field exists.
   ```javascript
   // ✗ crashes if item.json.user doesn't exist
   const value = item.json.user.email;

   // ✓ safe
   const value = item.json?.user?.email || 'no-email@example.com';

   // ✓ guard clause
   if (!item.json.user) { return []; }
   const value = item.json.user.email;
   ```

6. **Attach `pairedItem` when creating output items that don't map 1:1 to input items** — otherwise downstream Set nodes will fail with a `paired_item_no_info` error.
   ```javascript
   const results = [];
   for (let i = 0; i < $input.all().length; i++) {
     const item = $input.all()[i];
     results.push({
       json: { /* new data */ },
       pairedItem: { item: i }
     });
   }
   return results;
   ```

7. **Reference other nodes correctly.** Call `.first()` (or `.all()`) before `.json` — you cannot chain `.json` directly onto a node reference.
   ```javascript
   // ✗ WRONG
   const data = $('HTTP Request').json;

   // ✓ CORRECT
   const data = $('HTTP Request').first().json;
   const allData = $('HTTP Request').all();

   // Legacy-style but equivalent form using $node
   const webhookData = $node["Webhook"].json;
   ```

8. **Watch out for SplitInBatches loops.** The node has two outputs and the naming is counterintuitive: `main[0]` is "done" (fires once, after all batches finish) and `main[1]` is "each batch" (fires per batch — this is the loop body). Add a Limit-1 node after the "done" output as a safety net against edge cases where it fires with extra items.

9. **Accumulate data across loop iterations using workflow static data, not node references.** After a SplitInBatches loop, calling `.all()` on a node inside the loop returns only the LAST iteration's items, not the cumulative set — this silently drops data from every batch but the final one.
   ```javascript
   // BEFORE the loop (reset the accumulator)
   const staticData = $getWorkflowStaticData('global');
   staticData.results = [];
   return $input.all();

   // INSIDE the loop body (accumulate)
   const staticData = $getWorkflowStaticData('global');
   const results = [];
   for (const item of $input.all()) {
     const processed = { /* ... */ };
     results.push({ json: processed });
     staticData.results.push(processed);
   }
   return results;

   // AFTER the loop (read the full accumulated set)
   const staticData = $getWorkflowStaticData('global');
   const allResults = staticData.results || [];
   ```

10. **Round currency/price comparisons to cents before comparing** — floating-point noise causes false-positive "price changed" detections.
    ```javascript
    // ✗ unreliable
    if (newPrice !== oldPrice) { /* triggers on floating-point noise */ }

    // ✓ reliable
    if (Math.round(newPrice * 100) !== Math.round(oldPrice * 100)) {
      // real price change
    }
    ```

11. **Before finishing, run the checklist** under Rules & Standards below.

## Rules & Standards

### Top 5 error patterns (ranked by real-world frequency)

**#1 — Empty code or missing return statement (~38% of all failures, the single most common error).**
```javascript
// ✗ code executes but never returns
const items = $input.all();
for (const item of items) { console.log(item.json.name); }
// forgot to return!

// ✗ one path returns, another doesn't
if (items.length === 0) { return []; }
const processed = items.map(item => ({ json: item.json }));
// forgot to return processed!

// ✓ every path returns
const items = $input.all();
if (items.length === 0) {
  return [];
} else if (items.length === 1) {
  return [{ json: { single: true, data: items[0].json } }];
} else {
  return items.map(item => ({ json: item.json }));
}
```
Checklist: code field is not empty · a return statement exists · ALL code paths (every if/else branch) return · return format is correct · return happens even on the error path (use try/catch).

**#2 — Expression syntax confusion (~8% of failures)** — using `{{ }}` inside the Code node. Covered in step 4 above.

**#3 — Incorrect return wrapper (~5% of failures)** — covered in step 2 above. Quick reference for common scenarios:
```javascript
// Single object from an API response
const response = $input.first().json;
return [{ json: response }];          // ✓
// return {json: response};           // ✗

// Array of objects
const users = $input.all();
return users.map(user => ({ json: user.json })); // ✓
// return users;                      // ✗ risky — depends on existing structure

// Computed result
const total = $input.all().reduce((sum, item) => sum + item.json.amount, 0);
return [{ json: { total } }];         // ✓
// return {total};                    // ✗

// No results
return [];                            // ✓
// return null;                       // ✗
```

**#4 — Unmatched expression brackets (~6% of failures)** — usually from unbalanced quotes inside strings, multi-line strings with embedded quotes, or unescaped regex. Fix by preferring template literals (backticks) for anything multi-line or containing quotes:
```javascript
// ✗ risky
const message = "It's a nice day";
const html = "
  <div class="container"><p>Hello</p></div>
";

// ✓ safe — backticks handle multi-line and embedded quotes cleanly
const message = `It's a nice day`;
const html = `
  <div class="container">
    <p>Hello</p>
  </div>
`;
```
Escaping reference: `\'` for a single quote inside a single-quoted string, `\"` for a double quote inside a double-quoted string, `\\` for a literal backslash, `\n` for newline, `\t` for tab.

**#5 — Missing null checks / undefined access (very common runtime error).** Covered in step 5 above. Additional safe-access patterns:
```javascript
// Optional chaining (preferred)
const value = data?.nested?.property?.value;

// Logical OR with a default
const value = data.property || 'default';

// Nullish coalescing (only falls back on null/undefined, not on 0 or '')
const timeout = $json.settings?.advanced?.timeout ?? 30000;

// Guard clause
if (!data.property) { return []; }

// Try/catch for genuinely risky operations
try {
  const value = data.nested.property.value;
} catch (error) {
  const value = 'default';
}
```
Apply the same caution to webhook payloads (`const name = $json.body?.user?.name || 'Unknown';`) and to arrays (check `.length` before indexing, or use `$input.first()` which has built-in safety over `$input.all()[0]`).

### Quick-reference checklist before shipping a Code node

- [ ] Code is not empty and has meaningful logic
- [ ] A return statement exists on every code path
- [ ] Return format is `[{ json: {...} }]` — array of objects, each with a `json` key
- [ ] Data access uses `$input.all()`, `$input.first()`, or `$input.item` (matching the selected mode) — not bare `$json` used ambiguously
- [ ] No `{{ }}` expression syntax anywhere — plain JavaScript / template literals only
- [ ] Guard clauses or optional chaining protect every place null/undefined could appear
- [ ] Webhook data is accessed via `.body`
- [ ] Mode is "All Items" unless there's a specific reason for "Each Item"
- [ ] Prefer `.map()`/`.filter()`/`.reduce()` over manual loops where reasonable
- [ ] All code paths return the same shape of data

### When to use the Code node vs. a simpler node

Use Code node for: complex multi-step transformations, custom calculations/business logic, recursive operations, parsing complex API response structures, multi-step conditionals, cross-item aggregation.

Use a simpler node instead when: it's simple field mapping (→ Set node), basic filtering (→ Filter node), a simple conditional (→ IF or Switch node), or just an HTTP call with no transformation (→ HTTP Request node). The Code node's real strength is handling logic that would otherwise require chaining many simple nodes together.

## Data Access Quick Reference

- **`$input.all()`** — the default, most common pattern. Use for anything that needs to see multiple items at once: filtering, transforming, aggregating, sorting, grouping, deduplicating.
- **`$input.first()`** — for single-object cases, e.g. an API response that's a single object, or grabbing the first-in-first-out item.
- **`$input.item`** — only valid in "Each Item" mode.
- **`$node["NodeName"]` / `$("NodeName")`** — reference a specific other node, useful when combining data from multiple named nodes or comparing across an execution. Always call `.first()` or `.all()` before `.json`.

Decision tree: need ALL items → `$input.all()`. Need just the FIRST → `$input.first()`. In "Each Item" mode → `$input.item`. Need a specific named node's data → `$node["Name"]` / `$("Name")`. Default fallback → `$input.first()`.

For ten worked production-tested code patterns (multi-source aggregation, regex extraction, markdown parsing, JSON diffing, CRM data transformation, changelog processing, ranking/percentages, Slack Block Kit formatting, top-N filtering, report generation) with a pattern-selection table, see `references/patterns.md`.

For the full built-in function reference — `$helpers.httpRequest()` with auth patterns and error handling, `DateTime` (Luxon) date/time operations, `$jmespath()` JSON querying, `$getWorkflowStaticData()` persistent storage, available Node.js modules (crypto, Buffer, URL), and what's NOT available (no npm packages) — see `references/builtin-functions.md`.
