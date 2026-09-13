---
name: n8n-code-python
description: Reference for writing Python inside n8n's Code node — the node type used for custom data transformation, aggregation, filtering, API-response processing, and any logic too complex for n8n's simpler nodes (Set, Filter, IF/Switch, HTTP Request), when Python specifically is the right tool. Use this whenever a workflow needs a Code node written in Python — choosing between its two Python execution modes (Beta vs Native), accessing input data correctly with the underscore-prefixed helpers, returning data in the exact shape n8n expects, working within the standard-library-only sandbox, or avoiding the handful of mistakes that cause the vast majority of Python Code node failures.
---

# n8n Python Code Node

**Read this first: JavaScript is the better default.** n8n's Python Code node has **no external libraries** — no `requests`, no `pandas`, no `numpy`, nothing installable via pip. JavaScript Code nodes, by contrast, get an HTTP-request helper and the full Luxon `DateTime` library for date/time work, with no such sandboxing. Because of this, **JavaScript is the right choice for about 95% of Code node tasks.** Only reach for Python when one of these is true:
- The task needs a Python-specific standard-library capability (`re` for regex, `hashlib` for hashing, `statistics` for mean/median/stdev, etc.)
- The person writing the workflow is significantly more comfortable in Python than JavaScript
- There's existing Python logic that needs to be reused as-is

If neither applies, write the Code node in JavaScript instead (see the companion n8n JavaScript Code Node reference) — it has fewer limitations and better platform support.

## How to Use This

1. **Decide the language before writing anything.** Default to JavaScript. Switch to Python only for the reasons above. If Python is chosen, everything below applies.

2. **Pick the Python execution sub-mode: Beta vs Native.** n8n offers two distinct Python runtimes inside the Code node, and they use different variable names — get this right before writing a single line.

   | | Python (Beta) — recommended | Python (Native) |
   |---|---|---|
   | Data access | `_input`, `_json`, `_node` helpers | `_items`, `_item` only |
   | Extra helpers | `_now`, `_today`, `_jmespath()` | none — no `_input`, no `_now` |
   | Import for dates | `from datetime import datetime` | same |
   | Best for | Most Python use cases, full n8n integration | Pure Python with no n8n helpers |

   Beta-mode example:
   ```python
   # Python (Beta) example
   items = _input.all()
   now = _now  # Built-in datetime object

   return [{
       "json": {
           "count": len(items),
           "timestamp": now.isoformat()
       }
   }]
   ```

   Native-mode example:
   ```python
   # Python (Native) example
   processed = []

   for item in _items:
       processed.append({
           "json": {
               "id": item["json"].get("id"),
               "processed": True
           }
       })

   return processed
   ```

   Recommendation: use **Python (Beta)** for better n8n integration unless there's a specific reason to need pure Python with no helpers.

3. **Pick the item-processing mode: Run Once for All Items vs Run Once for Each Item.** Same decision as in JavaScript Code nodes.
   - **Run Once for All Items** (the default, correct ~95% of the time): the code executes once total, regardless of how many items came in. Access data via `_input.all()` (Beta) or the `_items` array (Native). Use for aggregation, filtering, batch processing, transformations, sorting/ranking, deduplication — anything comparing or combining items across the dataset.
   - **Run Once for Each Item** (specialized cases only): the code executes separately per input item. Access the current item via `_input.item` (Beta) or `_item` (Native). Use only when each item genuinely needs independent handling — its own validation with different error handling, or a transformation that depends only on that item's own properties.
   - Decision shortcut: need to look at multiple items at once → All Items mode. Each item is completely independent → Each Item mode. Not sure → default to All Items.

4. **Access data with the correct underscore-prefixed pattern.** Python's syntax mirrors JavaScript's `$`-prefixed helpers but uses `_` instead. Priority order by how often each is used:

   | Need | Use | Example |
   |---|---|---|
   | ALL items from previous node | `_input.all()` | `sum(i["json"].get("amount", 0) for i in items)` |
   | Just the FIRST item / an API response | `_input.first()` | `_input.first()["json"].get("data")` |
   | Current item, Each Item mode only | `_input.item` | `_input.item["json"]` |
   | A specific named node's output | `_node["NodeName"]` | `_node["API"]["json"]` |
   | Webhook payload | `_input.first()` then `["body"]` | `_input.first()["json"]["body"]` |

   Decision tree: Do you need ALL items? → `_input.all()`. Just the first? → `_input.first()`. In "Each Item" mode? → `_input.item`. Need a specific named node? → `_node["NodeName"]`. None of the above? → default to `_input.first()`.

   Avoid using bare `_json` — it's ambiguous about which item it refers to. Be explicit: `_input.first()["json"]["field"]` instead of `_json["field"]`.

5. **Know that webhook data is nested under `["body"]`.** This is the single most common mistake, identical to the JavaScript Code node. A Webhook node wraps everything — POST data, query parameters, JSON payloads — inside a `body` property.
   ```python
   # ❌ WRONG - Will raise KeyError
   name = _json["name"]
   email = _json["email"]

   # ✅ CORRECT - Webhook data is under ["body"]
   name = _json["body"]["name"]
   email = _json["body"]["email"]

   # ✅ SAFER - Use .get() for safe access
   webhook_data = _json.get("body", {})
   name = webhook_data.get("name")
   ```
   Full webhook output structure:
   ```python
   {
       "headers": {
           "content-type": "application/json",
           "user-agent": "..."
       },
       "params": {},
       "query": {},
       "body": {
           # ← YOUR DATA IS HERE
           "name": "Alice",
           "email": "alice@example.com",
           "message": "Hello!"
       }
   }
   ```
   Also available on the same object: `webhook.get("query", {})` (query-string parameters), `webhook.get("headers", {}).get("user-agent")` / `.get("content-type")` (HTTP headers), and `webhook.get("method")` / `webhook.get("url")`.

6. **Always return the correct format.** A Code node MUST return an array (list), and every element of that array MUST have a `json` key. This is the single most common source of failures across both languages.
   ```python
   # ✅ Single result
   return [{
       "json": {
           "field1": value1,
           "field2": value2
       }
   }]

   # ✅ Multiple results
   return [
       {"json": {"id": 1, "data": "first"}},
       {"json": {"id": 2, "data": "second"}}
   ]

   # ✅ List comprehension
   transformed = [
       {"json": {"id": item["json"]["id"], "processed": True}}
       for item in _input.all()
       if item["json"].get("valid")
   ]
   return transformed

   # ✅ Empty result (when there's nothing to return)
   return []
   ```
   Wrong formats that will break the workflow:
   ```python
   return {"json": {"field": value}}    # ❌ dict, not list-wrapped
   return [{"field": value}]            # ❌ missing the "json" key
   return "processed"                   # ❌ plain string
   return None                          # ❌ None instead of []
   return [{"data": value}]             # ❌ wrong key name — must be "json"
   ```

7. **Never try to `import` an external library — this is Python's single defining limitation.** No `requests`, `pandas`, `numpy`, `bs4`, `selenium`, `psycopg2`, `pymongo`, `sqlalchemy`, `flask`, `fastapi`, `pillow`, `openpyxl`, or anything else that needs `pip install`. Attempting it raises `ModuleNotFoundError`. Workarounds, in priority order:
   - **Need HTTP requests?** Add an HTTP Request node before the Code node and process its output, or switch to JavaScript and use its HTTP-request helper. As a last resort, standard-library `urllib.request` can do a bare, unauthenticated GET (see `references/stdlib-reference.md`).
   - **Need data analysis (pandas/numpy)?** Use plain list comprehensions, the `statistics` module for mean/median/stdev, and manual dict/list manipulation. Or switch to JavaScript.
   - **Need a database driver (psycopg2/pymongo)?** Use n8n's own Postgres/MySQL/MongoDB nodes upstream and process their output in the Code node.
   - **Need web scraping (BeautifulSoup/selenium)?** Use the HTML Extract node, or switch to JavaScript with regex/string methods.
   - **Need Excel (openpyxl)?** Use the Spreadsheet File node.

8. **Guard every dictionary access with `.get()`, not bare indexing.** `item["field"]` raises `KeyError` the instant a key is missing; `item.get("field", default)` never does.
   ```python
   # ❌ crashes if the key is missing
   value = item["json"]["user"]["email"]

   # ✅ safe, chained
   value = item["json"].get("user", {}).get("email", "no-email@example.com")
   ```

9. **Guard every list index with a length check or use slicing instead.** `items[0]` raises `IndexError` on an empty list; `items[:5]` never does, and `_input.first()` has built-in safety over manual `_input.all()[0]` indexing.
   ```python
   # ❌ WRONG - Assuming items exist
   all_items = _input.all()
   first_item = all_items[0]        # IndexError if list is empty!

   # ✅ CORRECT - Check length first, or use _input.first()
   all_items = _input.all()
   if all_items:
       first_item = all_items[0]["json"]
   else:
       first_item = {}
   ```

10. **Watch for the two production-only gotchas specific to Python mode.**
    - **Node reference syntax**: the reliably correct form calls `.first()` before `["json"]`:
      ```python
      # ❌ flagged as WRONG in production use
      data = _node['HTTP Request']['json']

      # ✅ flagged as CORRECT in production use
      data = _node['HTTP Request'].first()['json']
      ```
      Treat `.first()` as the safer, production-tested form when referencing another node's output by name, even though the plain `_node["Name"]["json"]` form appears in most straightforward data-access examples.
    - **Cross-iteration accumulation is not reliably available in Python.** The workflow-static-data mechanism used in JavaScript Code nodes to accumulate results across a SplitInBatches loop may not be available in Python Beta mode. If a workflow needs to accumulate data across loop iterations, do that accumulation step in a JavaScript Code node instead, even if the rest of the workflow's logic is in Python.

11. **Know the SplitInBatches loop semantics if the workflow uses one.** The node has two outputs and the naming is counterintuitive: the first output is "done" (fires once, after all batches finish) and the second is "each batch" (fires per batch — this is the loop body). Add a Limit-1 node after the "done" output as a safety net.

12. **Before finishing, run the checklist** under Rules & Standards below.

## Rules & Standards

### Top 5 Python Code node errors

**#1 — ModuleNotFoundError (the single most Python-specific failure, and very common).** Any `import` of a package that isn't in the standard library fails immediately.
```python
# ❌ WRONG: External libraries not available
import requests  # ModuleNotFoundError: No module named 'requests'
import pandas    # ModuleNotFoundError: No module named 'pandas'
import numpy     # ModuleNotFoundError: No module named 'numpy'
```
Common library replacements:

| Need | ❌ External library | ✅ Alternative |
|---|---|---|
| HTTP requests | `requests` | HTTP Request node, or JavaScript |
| Data analysis | `pandas` | Python list comprehensions |
| Database | `psycopg2`, `pymongo` | n8n database nodes |
| Web scraping | `beautifulsoup4` | HTML Extract node |
| Excel | `openpyxl` | Spreadsheet File node |
| Image processing | `pillow` | External API or dedicated node |

**#2 — Empty code or missing return (common across all Code nodes, both languages).**
```python
# ✅ CORRECT: Always return, at the end, unconditionally
all_items = _input.all()
if not all_items:
    return [{"json": {"error": "No items"}}]
processed = [item for item in all_items if item["json"].get("active")]
return processed if processed else [{"json": {"message": "No active items"}}]
```

**#3 — KeyError from direct dictionary access (very common).**
```python
# ❌ WRONG
name = item["name"]        # KeyError if "name" doesn't exist!

# ✅ CORRECT
name = item.get("name", "Unknown")
```
Nested access — chain `.get()` calls, or step through with intermediate `.get(x, {})` calls, rather than direct bracket chains.

**#4 — IndexError from unchecked list access.**
```python
all_items = _input.all()
if len(all_items) >= 2:
    first_item = all_items[0]["json"]
else:
    return [{"json": {"error": f"Expected 2+ items, got {len(all_items)}"}}]

# Slicing never raises IndexError, even on empty/short lists
first_five = all_items[:5]
```

**#5 — Incorrect return format.**
```python
# ✅ CORRECT forms only
return [{"json": {"name": "Alice", "age": 30}}]
return [{"json": {"name": "Alice"}}, {"json": {"name": "Bob"}}]
return []                                     # empty is valid
return [{"json": item["json"]} for item in _input.all()]
```

**Bonus — AttributeError from using `_input.item` in the wrong mode.**
```python
current = _input.item
if current:
    data = current["json"]
    return [{"json": data}]
else:
    # Running in "All Items" mode
    return _input.all()
```

### Quick fix reference

| Error | Quick fix |
|---|---|
| `ModuleNotFoundError` | Use JavaScript or an HTTP Request node instead |
| `KeyError: 'field'` | Change `data["field"]` to `data.get("field", default)` |
| `IndexError: list index out of range` | Check `if len(items) > 0:` before `items[0]`, or use slicing |
| Empty output | Add `return [{"json": {...}}]` at the end |
| `AttributeError: 'NoneType'` | Check mode setting or verify `_input.item` exists before using it |
| Wrong format error | Wrap the result: `return [{"json": result}]` |
| Webhook KeyError | Access via `_json.get("body", {})` |

### Error-prevention checklist before shipping a Python Code node

- [ ] No external imports — only standard library (`json`, `datetime`, `re`, etc.)
- [ ] Code returns data on every code path — every `if`/`else` branch ends with `return`
- [ ] Correct format — `[{"json": {...}}]`, array with a `json` key on every element
- [ ] Safe dictionary access — uses `.get()` instead of `[]` for dictionaries
- [ ] Safe list access — checks length before indexing, or uses slicing
- [ ] Webhook body access — reads webhook data via `_json["body"]` / `.get("body", {})`
- [ ] No `None` returns — returns empty list `[]` instead of `None`
- [ ] Mode awareness — uses `_input.all()`, `_input.first()`, or `_input.item` correctly for the selected item-processing mode
- [ ] Considered JavaScript first — Python is used only because it's specifically needed here

### When to use Python vs JavaScript vs a simpler node

Use **Python** when: the task needs the `statistics` module for statistical operations; the task's logic maps cleanly onto list comprehensions; Python-specific standard-library functions are required (regex via `re`, hashing via `hashlib`, etc.); or the person is significantly more comfortable in Python.

Use **JavaScript** when: HTTP requests are needed; advanced date/time handling is needed (Luxon `DateTime`); better n8n platform integration matters; or for roughly 95% of cases generally — when in doubt, use JavaScript.

Use a **simpler node instead of any Code node** when: it's simple field mapping (→ Set node), basic filtering (→ Filter node), a simple conditional (→ IF or Switch node), or just an HTTP call with no transformation (→ HTTP Request node).

The Code node's real strength — in either language — is handling logic that would otherwise require chaining many simple nodes together: complex multi-step transformations, custom calculations/business logic, recursive operations, parsing complex API response structures, multi-step conditionals, cross-item aggregation.

## Data Access Quick Reference

- **`_input.all()`** — the default, most common pattern. Use for anything that needs to see multiple items at once.
- **`_input.first()`** — for single-object cases, e.g. an API response that's a single object.
- **`_input.item`** — only valid in "Each Item" mode.
- **`_node["NodeName"]`** — reference a specific other node's output by name; use `.first()["json"]` for the production-safe form.

Python-vs-JavaScript equivalents: `_input.all()` ↔ `$input.all()`, `_input.first()` ↔ `$input.first()`, `_input.item` ↔ `$input.item`, `_json` (Beta) ↔ `$json`; there is no Python-Native equivalent to `_node` (not available in Native mode).

For ten worked production-tested Python patterns (multi-source aggregation, regex filtering, markdown-to-structured-data, JSON comparison, CRM normalization, release-notes categorization, array transformation, dictionary lookup, top-N filtering, string aggregation) with a pattern-selection table, see `references/patterns.md`.

For the complete standard-library reference — `json`, `datetime`, `re`, `base64`, `hashlib`, `urllib.parse`/`urllib.request`, `math`, `random`, `statistics`, plus combined-module workaround patterns for pandas-style grouping and database/API post-processing — see `references/stdlib-reference.md`.
