# n8n Python Code Node

Reference for writing Python inside n8n's Code node — the node type used for custom data transformation, aggregation, filtering, API-response processing, and any logic too complex for n8n's simpler nodes (Set, Filter, IF/Switch, HTTP Request), when Python specifically is the right tool. Use this whenever a workflow needs a Code node written in Python: choosing between its two Python execution modes (Beta vs Native), accessing input data correctly with the underscore-prefixed helpers, returning data in the exact shape n8n expects, working within the standard-library-only sandbox, or avoiding the handful of mistakes that cause the vast majority of Python Code node failures.

**Read this first: JavaScript is the better default.** n8n's Python Code node has **no external libraries** — no `requests`, no `pandas`, no `numpy`, nothing installable via pip. JavaScript Code nodes, by contrast, get `$helpers.httpRequest()` for HTTP calls and the full Luxon `DateTime` library for date/time work, with no such sandboxing. Because of this, **JavaScript is the right choice for about 95% of Code node tasks.** Only reach for Python when one of these is true:
- The task needs a Python-specific standard-library capability (`re` for regex, `hashlib` for hashing, `statistics` for mean/median/stdev, etc.)
- The person writing the workflow is significantly more comfortable in Python than JavaScript
- There's existing Python logic that needs to be reused as-is

If neither applies, write the Code node in JavaScript instead (see the companion n8n JavaScript Code Node reference for that path) — it has fewer limitations and better platform support.

## How to use this

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
   - **Need HTTP requests?** Add an HTTP Request node before the Code node and process its output, or switch to JavaScript and use `$helpers.httpRequest()`. As a last resort, standard-library `urllib.request` can do a bare, unauthenticated GET (see Templates & examples).
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
    - **Node reference syntax**: DATA_ACCESS-style code commonly writes `_node["NodeName"]["json"]` directly, and that pattern appears throughout the documented data-access examples. However, the production-gotchas guidance for Python Code nodes separately warns that the reliably correct form calls `.first()` before `["json"]`:
      ```python
      # ❌ flagged as WRONG in production use
      data = _node['HTTP Request']['json']

      # ✅ flagged as CORRECT in production use
      data = _node['HTTP Request'].first()['json']
      ```
      Treat `.first()` as the safer, production-tested form when referencing another node's output by name, even though the plain `_node["Name"]["json"]` form is what appears in most straightforward data-access examples.
    - **Cross-iteration accumulation is not reliably available in Python.** `$getWorkflowStaticData('global')` — the mechanism used in JavaScript Code nodes to accumulate results across a SplitInBatches loop — may not be available in Python Beta mode. If a workflow needs to accumulate data across loop iterations, do that accumulation step in a JavaScript Code node instead, even if the rest of the workflow's logic is in Python.

11. **Know the SplitInBatches loop semantics if the workflow uses one.** The node has two outputs and the naming is counterintuitive: the first output is "done" (fires once, after all batches finish) and the second is "each batch" (fires per batch — this is the loop body). Add a Limit-1 node after the "done" output as a safety net.

12. **Before finishing, run the checklist** under Rules & Standards below.

## Rules & standards

### Top 5 Python Code node errors

**#1 — ModuleNotFoundError (the single most Python-specific failure, and very common).** Any `import` of a package that isn't in the standard library fails immediately.
```python
# ❌ WRONG: External libraries not available
import requests  # ModuleNotFoundError: No module named 'requests'
import pandas    # ModuleNotFoundError: No module named 'pandas'
import numpy     # ModuleNotFoundError: No module named 'numpy'
import bs4       # ModuleNotFoundError: No module named 'bs4'
import pymongo   # ModuleNotFoundError: No module named 'pymongo'
import psycopg2  # ModuleNotFoundError: No module named 'psycopg2'

# This code will FAIL - these libraries are not installed!
response = requests.get("https://api.example.com/data")
```
Solutions, in order of preference:
```python
# Option 2: Add an HTTP Request node BEFORE the Python Code node,
# then just process its output in Python:
response = _input.first()["json"]

return [{
    "json": {
        "status": response.get("status"),
        "data": response.get("body"),
        "processed": True
    }
}]
```
```python
# Option 3: Standard-library-only HTTP as a last resort (no headers, no auth)
from urllib.request import urlopen
from urllib.parse import urlencode
import json

url = "https://api.example.com/data"
with urlopen(url) as response:
    data = json.loads(response.read())

return [{"json": data}]
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
# ❌ WRONG: Code but no return
items = _input.all()
processed = [item for item in items if item["json"].get("active")]
# Forgot to return!

# ❌ WRONG: Return in wrong scope
if _input.all():
    return [{"json": {"result": "success"}}]
# Return is inside if block - may not execute!

# ✅ CORRECT: Always return, at the end, unconditionally
all_items = _input.all()

if not all_items:
    return [{"json": {"error": "No items"}}]

processed = [item for item in all_items if item["json"].get("active")]

return processed if processed else [{"json": {"message": "No active items"}}]
```

**#3 — KeyError from direct dictionary access (very common).**
```python
# ❌ WRONG: Direct key access
item = _input.first()["json"]
name = item["name"]        # KeyError if "name" doesn't exist!
email = item["email"]      # KeyError if "email" doesn't exist!

# ✅ CORRECT: Use .get() with defaults
name = item.get("name", "Unknown")
email = item.get("email", "no-email@example.com")
```
Nested access:
```python
# ❌ WRONG: Nested key access
webhook = _input.first()["json"]
name = webhook["body"]["user"]["name"]  # Multiple possible KeyErrors!

# ✅ CORRECT: Safe nested access (either form)
webhook = _input.first()["json"]
body = webhook.get("body", {})
user = body.get("user", {})
name = user.get("name", "Unknown")

# ✅ ALSO CORRECT: Chained .get()
name = (
    webhook
    .get("body", {})
    .get("user", {})
    .get("name", "Unknown")
)
```

**#4 — IndexError from unchecked list access (common when processing arrays).**
```python
# ❌ WRONG: Assuming items exist
all_items = _input.all()
first_item = all_items[0]        # IndexError if list is empty!
second_item = all_items[1]       # IndexError if only 1 item!

# ✅ CORRECT: Check length first
all_items = _input.all()
if len(all_items) >= 2:
    first_item = all_items[0]["json"]
    second_item = all_items[1]["json"]
    return [{"json": {"first": first_item, "second": second_item}}]
else:
    return [{"json": {"error": f"Expected 2+ items, got {len(all_items)}"}}]

# ✅ Slicing never raises IndexError, even on empty/short lists
first_five = all_items[:5]
rest = all_items[1:]
```

**#5 — Incorrect return format (common for new users of either language).**
```python
# ❌ WRONG: Returning plain dictionary
return {"name": "Alice", "age": 30}

# ❌ WRONG: Returning array without "json" wrapper
return [{"name": "Alice"}, {"name": "Bob"}]

# ❌ WRONG: Returning None
return None

# ❌ WRONG: Returning string
return "success"

# ❌ WRONG: Returning single item still not array-wrapped
return {"json": {"name": "Alice"}}

# ✅ CORRECT forms
return [{"json": {"name": "Alice", "age": 30}}]
return [{"json": {"name": "Alice"}}, {"json": {"name": "Bob"}}]
return []                                     # empty is valid
return [{"json": item["json"]} for item in _input.all()]
```

**Bonus — AttributeError from using `_input.item` in the wrong mode.**
```python
# ❌ WRONG: Using _input.item in "All Items" mode
current = _input.item        # None in "All Items" mode
data = current["json"]       # AttributeError: 'NoneType' object has no attribute '__getitem__'

# ✅ SAFE: Check if item exists before assuming Each-Item mode
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

### Testing patterns

Test with empty input:
```python
all_items = _input.all()

if not all_items:
    return [{"json": {"message": "No items to process"}}]

# Continue with processing
```
Test with missing fields (use `.get()` everywhere so nothing fails even if fields are absent):
```python
item = _input.first()["json"]
name = item.get("name", "Unknown")
email = item.get("email", "no-email")
age = item.get("age", 0)
return [{"json": {"name": name, "email": email, "age": age}}]
```
Test code that needs to tolerate either item-processing mode:
```python
try:
    current = _input.item
    if current:
        return [{"json": current["json"]}]
except Exception:
    pass

all_items = _input.all()
return all_items if all_items else [{"json": {"message": "No data"}}]
```

### When to use Python vs JavaScript vs a simpler node

Use **Python** when:
- The task needs the `statistics` module for statistical operations
- The task's logic maps cleanly onto list comprehensions
- Python-specific standard-library functions are required (regex via `re`, hashing via `hashlib`, etc.)
- The person is significantly more comfortable in Python

Use **JavaScript** when:
- HTTP requests are needed (`$helpers.httpRequest()`)
- Advanced date/time handling is needed (Luxon `DateTime`)
- Better n8n platform integration matters
- For roughly 95% of cases generally — when in doubt, use JavaScript

Use a **simpler node instead of any Code node** when:
- It's simple field mapping → Set node
- It's basic filtering → Filter node
- It's a simple conditional → IF or Switch node
- It's just an HTTP call with no transformation → HTTP Request node

The Code node's real strength — in either language — is handling logic that would otherwise require chaining many simple nodes together: complex multi-step transformations, custom calculations/business logic, recursive operations, parsing complex API response structures, multi-step conditionals, cross-item aggregation.

## Templates & examples

### Data access patterns, in full

**`_input.all()` — the default, most common pattern.** Use for anything that needs to see multiple items at once: filtering, transforming, aggregating, sorting, grouping, deduplicating.

Filter:
```python
all_items = _input.all()
active_items = [
    item for item in all_items
    if item["json"].get("status") == "active"
]
```
Transform:
```python
all_items = _input.all()
transformed = []
for item in all_items:
    transformed.append({
        "json": {
            "id": item["json"].get("id"),
            "full_name": f"{item['json'].get('first_name', '')} {item['json'].get('last_name', '')}",
            "email": item["json"].get("email"),
            "processed_at": datetime.now().isoformat()
        }
    })
return transformed
```
Aggregate:
```python
all_items = _input.all()
total = sum(item["json"].get("amount", 0) for item in all_items)
return [{
    "json": {
        "total": total,
        "count": len(all_items),
        "average": total / len(all_items) if all_items else 0
    }
}]
```
Sort and limit (top 5 by score):
```python
all_items = _input.all()
sorted_items = sorted(
    all_items,
    key=lambda item: item["json"].get("score", 0),
    reverse=True
)
top_five = sorted_items[:5]
return [{"json": item["json"]} for item in top_five]
```
Group by category:
```python
all_items = _input.all()
grouped = {}
for item in all_items:
    category = item["json"].get("category", "Uncategorized")
    if category not in grouped:
        grouped[category] = []
    grouped[category].append(item["json"])

return [
    {"json": {"category": category, "items": items, "count": len(items)}}
    for category, items in grouped.items()
]
```
Deduplicate by ID:
```python
all_items = _input.all()
seen = set()
unique = []
for item in all_items:
    item_id = item["json"].get("id")
    if item_id and item_id not in seen:
        seen.add(item_id)
        unique.append(item)
return unique
```

**`_input.first()` — for single-object cases**, e.g. an API response that's a single object.
```python
response = _input.first()["json"]
return [{
    "json": {
        "user_id": response.get("data", {}).get("user", {}).get("id"),
        "user_name": response.get("data", {}).get("user", {}).get("name"),
        "status": response.get("status"),
        "fetched_at": datetime.now().isoformat()
    }
}]
```
Transform a single object into a nested shape:
```python
data = _input.first()["json"]
return [{
    "json": {
        "id": data.get("id"),
        "contact": {"email": data.get("email"), "phone": data.get("phone")},
        "address": {"street": data.get("street"), "city": data.get("city"), "zip": data.get("zip")}
    }
}]
```
Extract a nested list and fan it out into multiple items:
```python
response = _input.first()["json"]
users = response.get("data", {}).get("users", [])
return [
    {
        "json": {
            "id": user.get("id"),
            "name": user.get("profile", {}).get("name", "Unknown"),
            "email": user.get("contact", {}).get("email", "no-email")
        }
    }
    for user in users
]
```

**`_input.item` — only valid in "Each Item" mode.**
```python
item = _input.item
return [{
    "json": {
        **item["json"],
        "processed": True,
        "processed_at": datetime.now().isoformat()
    }
}]
```
Per-item validation:
```python
item = _input.item
data = item["json"]
errors = []
if not data.get("email"):
    errors.append("Email required")
if not data.get("name"):
    errors.append("Name required")
if data.get("age") and data["age"] < 18:
    errors.append("Must be 18+")

return [{
    "json": {
        **data,
        "valid": len(errors) == 0,
        "errors": errors if errors else None
    }
}]
```

**`_node["NodeName"]` — reference a specific other node**, useful for combining data from multiple named nodes or comparing across an execution.
```python
webhook_data = _node["Webhook"]["json"]
http_data = _node["HTTP Request"]["json"]
return [{
    "json": {
        "combined": {"webhook": webhook_data, "api": http_data}
    }
}]
```
Combine three sources:
```python
webhook = _node["Webhook"]["json"]
database = _node["Postgres"]["json"]
api = _node["HTTP Request"]["json"]

return [{
    "json": {
        "combined": {
            "webhook": webhook.get("body", {}),
            "db_records": len(database) if isinstance(database, list) else 1,
            "api_response": api.get("status")
        },
        "processed_at": datetime.now().isoformat()
    }
}]
```
Compare across two named nodes:
```python
old_data = _node["Get Old Data"]["json"]
new_data = _node["Get New Data"]["json"]

changes = {
    "added": [n for n in new_data if n.get("id") not in [o.get("id") for o in old_data]],
    "removed": [o for o in old_data if o.get("id") not in [n.get("id") for n in new_data]]
}

return [{
    "json": {
        "changes": changes,
        "summary": {"added": len(changes["added"]), "removed": len(changes["removed"])}
    }
}]
```
Remember the production-gotcha noted above: reliably correct usage calls `.first()` before `["json"]` — `_node['HTTP Request'].first()['json']` — even though the plain form appears throughout ordinary examples.

### Python vs JavaScript, side by side

Data access:
```python
# Python
all_items = _input.all()
first_item = _input.first()
current = _input.item
webhook_data = _json["body"]
```
```javascript
// JavaScript
const allItems = $input.all();
const firstItem = $input.first();
const current = $input.item;
const webhookData = $json.body;
```

Dictionary/object access:
```python
# Python - Dictionary key access
name = user["name"]           # May raise KeyError
name = user.get("name", "?")  # Safe with default
```
```javascript
// JavaScript - Object property access
const name = user.name;              // May be undefined
const name = user.name || "?";       // Safe with default
```

Array operations:
```python
# Python - List comprehension
filtered = [item for item in items if item["active"]]
```
```javascript
// JavaScript - Array methods
const filtered = items.filter(item => item.active);
```

Sorting:
```python
# Python
items.sort(key=lambda x: x["score"], reverse=True)
```
```javascript
// JavaScript
items.sort((a, b) => b.score - a.score);
```

Also note the Python-vs-JavaScript variable-naming table from step 4 above, and: `_json` in Python (Beta) corresponds to `$json` in JavaScript; there is no Python-Native equivalent to `_node` (not available in Native mode).

### Ten production-tested Python patterns

**1. Multi-source data aggregation** — normalize and combine data from different sources into one structure.
```python
from datetime import datetime

all_items = _input.all()
processed_articles = []

for item in all_items:
    source_name = item["json"].get("name", "Unknown")
    source_data = item["json"]

    if source_name == "Hacker News" and source_data.get("hits"):
        for hit in source_data["hits"]:
            processed_articles.append({
                "title": hit.get("title", "No title"),
                "url": hit.get("url", ""),
                "summary": hit.get("story_text") or "No summary",
                "source": "Hacker News",
                "score": hit.get("points", 0),
                "fetched_at": datetime.now().isoformat()
            })

    elif source_name == "Reddit" and source_data.get("data"):
        for post in source_data["data"].get("children", []):
            post_data = post.get("data", {})
            processed_articles.append({
                "title": post_data.get("title", "No title"),
                "url": post_data.get("url", ""),
                "summary": post_data.get("selftext", "")[:200],
                "source": "Reddit",
                "score": post_data.get("score", 0),
                "fetched_at": datetime.now().isoformat()
            })

processed_articles.sort(key=lambda x: x["score"], reverse=True)
return [{"json": article} for article in processed_articles]
```

**2. Regex-based filtering** — filter items using pattern matching in text fields.
```python
import re

all_items = _input.all()
priority_tickets = []

high_priority_pattern = re.compile(
    r'\b(urgent|critical|emergency|asap|down|outage|broken)\b',
    re.IGNORECASE
)

for item in all_items:
    ticket = item["json"]
    subject = ticket.get("subject", "")
    description = ticket.get("description", "")
    combined_text = f"{subject} {description}"

    matches = high_priority_pattern.findall(combined_text)

    if matches:
        priority_tickets.append({
            "json": {
                **ticket,
                "priority": "high",
                "matched_keywords": list(set(matches)),
                "keyword_count": len(matches)
            }
        })
    else:
        priority_tickets.append({
            "json": {
                **ticket,
                "priority": "normal",
                "matched_keywords": [],
                "keyword_count": 0
            }
        })

priority_tickets.sort(key=lambda x: x["json"]["keyword_count"], reverse=True)
return priority_tickets
```

**3. Markdown to structured data** — parse a markdown checklist into structured task records.
```python
import re

markdown_text = _input.first()["json"]["body"].get("markdown", "")

tasks = []
lines = markdown_text.split("\n")

for line in lines:
    # Match: - [ ] Task or - [x] Task
    match = re.match(r'^\s*-\s*\[([ x])\]\s*(.+)$', line, re.IGNORECASE)

    if match:
        checked = match.group(1).lower() == 'x'
        task_text = match.group(2).strip()

        # Extract priority if present (e.g., [P1], [HIGH])
        priority_match = re.search(r'\[(P\d|HIGH|MEDIUM|LOW)\]', task_text, re.IGNORECASE)
        priority = priority_match.group(1).upper() if priority_match else "NORMAL"

        clean_text = re.sub(r'\[(P\d|HIGH|MEDIUM|LOW)\]', '', task_text, flags=re.IGNORECASE).strip()

        tasks.append({
            "text": clean_text,
            "completed": checked,
            "priority": priority,
            "original_line": line.strip()
        })

return [{
    "json": {
        "tasks": tasks,
        "total": len(tasks),
        "completed": sum(1 for t in tasks if t["completed"]),
        "pending": sum(1 for t in tasks if not t["completed"])
    }
}]
```

**4. JSON object comparison** — detect additions, removals, and modifications between two JSON objects.
```python
import json

all_items = _input.all()

old_data = all_items[0]["json"] if len(all_items) > 0 else {}
new_data = all_items[1]["json"] if len(all_items) > 1 else {}

changes = {"added": {}, "removed": {}, "modified": {}, "unchanged": {}}

all_keys = set(old_data.keys()) | set(new_data.keys())

for key in all_keys:
    old_value = old_data.get(key)
    new_value = new_data.get(key)

    if key not in old_data:
        changes["added"][key] = new_value
    elif key not in new_data:
        changes["removed"][key] = old_value
    elif old_value != new_value:
        changes["modified"][key] = {"old": old_value, "new": new_value}
    else:
        changes["unchanged"][key] = old_value

return [{
    "json": {
        "changes": changes,
        "summary": {
            "added_count": len(changes["added"]),
            "removed_count": len(changes["removed"]),
            "modified_count": len(changes["modified"]),
            "unchanged_count": len(changes["unchanged"]),
            "has_changes": len(changes["added"]) > 0 or len(changes["removed"]) > 0 or len(changes["modified"]) > 0
        }
    }
}]
```

**5. CRM data transformation** — normalize inbound contact data from different CRM systems into one standard shape.
```python
from datetime import datetime
import re

all_items = _input.all()
normalized_contacts = []

for item in all_items:
    raw_contact = item["json"]
    source = raw_contact.get("source", "unknown")

    email = raw_contact.get("email", "").lower().strip()

    phone_raw = raw_contact.get("phone", "")
    phone = re.sub(r'\D', '', phone_raw)

    if "full_name" in raw_contact:
        name_parts = raw_contact["full_name"].split(" ", 1)
        first_name = name_parts[0] if len(name_parts) > 0 else ""
        last_name = name_parts[1] if len(name_parts) > 1 else ""
    else:
        first_name = raw_contact.get("first_name", "")
        last_name = raw_contact.get("last_name", "")

    status_raw = raw_contact.get("status", "").lower()
    status = "active" if status_raw in ["active", "enabled", "true", "1"] else "inactive"

    normalized_contacts.append({
        "json": {
            "id": raw_contact.get("id", ""),
            "first_name": first_name.strip(),
            "last_name": last_name.strip(),
            "full_name": f"{first_name} {last_name}".strip(),
            "email": email,
            "phone": phone,
            "status": status,
            "source": source,
            "normalized_at": datetime.now().isoformat(),
            "original_data": raw_contact
        }
    })

return normalized_contacts
```

**6. Release notes processing** — categorize release-note lines into features, fixes, breaking changes, and other.
```python
import re

release_notes = _input.first()["json"]["body"].get("notes", "")

categories = {"features": [], "fixes": [], "breaking": [], "other": []}

lines = release_notes.split("\n")

for line in lines:
    line = line.strip()
    if not line or line.startswith("#"):
        continue

    clean_line = re.sub(r'^[\*\-\+]\s*', '', line)

    if re.search(r'\b(feature|add|new)\b', clean_line, re.IGNORECASE):
        categories["features"].append(clean_line)
    elif re.search(r'\b(fix|bug|patch|resolve)\b', clean_line, re.IGNORECASE):
        categories["fixes"].append(clean_line)
    elif re.search(r'\b(breaking|deprecated|remove)\b', clean_line, re.IGNORECASE):
        categories["breaking"].append(clean_line)
    else:
        categories["other"].append(clean_line)

return [{
    "json": {
        "categories": categories,
        "summary": {
            "features": len(categories["features"]),
            "fixes": len(categories["fixes"]),
            "breaking": len(categories["breaking"]),
            "other": len(categories["other"]),
            "total": sum(len(v) for v in categories.values())
        }
    }
}]
```

**7. Array transformation** — reshape arrays and extract specific nested fields.
```python
all_items = _input.all()

transformed = []

for item in all_items:
    user = item["json"]
    profile = user.get("profile", {})
    settings = user.get("settings", {})

    transformed.append({
        "json": {
            "user_id": user.get("id"),
            "email": user.get("email"),
            "name": profile.get("name", "Unknown"),
            "avatar": profile.get("avatar_url"),
            "bio": profile.get("bio", "")[:100],  # Truncate to 100 chars
            "notifications_enabled": settings.get("notifications", True),
            "theme": settings.get("theme", "light"),
            "created_at": user.get("created_at"),
            "last_login": user.get("last_login_at")
        }
    })

return transformed
```

**8. Dictionary lookup** — build a lookup dictionary for fast ID-based access.
```python
all_items = _input.all()

users_by_id = {}

for item in all_items:
    user = item["json"]
    user_id = user.get("id")
    if user_id:
        users_by_id[user_id] = {
            "name": user.get("name"),
            "email": user.get("email"),
            "status": user.get("status")
        }

lookup_ids = [1, 3, 5]
looked_up = []

for user_id in lookup_ids:
    if user_id in users_by_id:
        looked_up.append({
            "json": {"id": user_id, **users_by_id[user_id], "found": True}
        })
    else:
        looked_up.append({"json": {"id": user_id, "found": False}})

return looked_up
```

**9. Top-N filtering** — get the top items by score or value, with rank attached.
```python
all_items = _input.all()

products = []
for item in all_items:
    product = item["json"]
    products.append({
        "id": product.get("id"),
        "name": product.get("name"),
        "sales": product.get("sales", 0),
        "revenue": product.get("revenue", 0.0),
        "category": product.get("category")
    })

products.sort(key=lambda p: p["sales"], reverse=True)
top_10 = products[:10]

return [
    {"json": {**product, "rank": index + 1}}
    for index, product in enumerate(top_10)
]
```

**10. String aggregation** — combine multiple items into one formatted text summary.
```python
all_items = _input.all()

messages = []
for item in all_items:
    data = item["json"]
    user = data.get("user", "Unknown")
    message = data.get("message", "")
    timestamp = data.get("timestamp", "")
    formatted = f"[{timestamp}] {user}: {message}"
    messages.append(formatted)

summary = "\n".join(messages)

total_length = sum(len(msg) for msg in messages)
average_length = total_length / len(messages) if messages else 0

return [{
    "json": {
        "summary": summary,
        "message_count": len(messages),
        "total_characters": total_length,
        "average_length": round(average_length, 2)
    }
}]
```

### Pattern selection guide

| Goal | Pattern |
|---|---|
| Combine multiple sources/nodes | Multi-source aggregation |
| Extract mentions or keywords | Regex-based filtering |
| Parse formatted text (markdown/checklists) | Markdown to structured data |
| Detect changes between two objects | JSON object comparison |
| Prepare/normalize CRM contact data | CRM data transformation |
| Categorize a text feed by keyword | Release notes processing |
| Reshape data, extract nested fields | Array transformation |
| Fast ID-based lookups | Dictionary lookup |
| Get the best/worst items by criteria | Top-N filtering |
| Build a formatted text report | String aggregation |

### Standard library reference

**No external libraries are available — standard library only.** This is the hard boundary of what Python Code nodes can do.

```python
# ❌ NOT AVAILABLE - Will cause ModuleNotFoundError
import requests      # No HTTP library!
import pandas        # No data analysis!
import numpy         # No numerical computing!
import bs4            # No web scraping!
import selenium      # No browser automation!
import psycopg2      # No database drivers!
import pymongo       # No MongoDB!
import sqlalchemy    # No ORMs!

# ✅ AVAILABLE - Standard library only
import json
import datetime
import re
import base64
import hashlib
import urllib.parse
import urllib.request
import math
import random
import statistics
```

Module priority:
1. **json** — most commonly used
2. **datetime** — very common
3. **re** — common
4. **base64** — common
5. **hashlib** — common
6. **urllib.parse** — common
7. **math**, **random**, **statistics**, **collections** — moderately useful
8. **itertools**, **functools**, **operator**, **string**, **textwrap** — occasionally useful

**json — parse and generate JSON.**
```python
import json

# Parse JSON string to Python dict
json_string = '{"name": "Alice", "age": 30}'
data = json.loads(json_string)

# Generate JSON string
data = {"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}], "total": 2}
json_string = json.dumps(data, indent=2)

# Handle JSON errors
try:
    parsed = json.loads(json_string)
    status = "valid"
    error = None
except json.JSONDecodeError as e:
    parsed = None
    status = "invalid"
    error = str(e)

# Pretty print
pretty_json = json.dumps(data, indent=2, sort_keys=True)
```

**datetime — date and time.**
```python
from datetime import datetime, timedelta

now = datetime.now()
now.isoformat()
now.strftime("%Y-%m-%d")
now.strftime("%H:%M:%S")
now.strftime("%B %d, %Y at %I:%M %p")

# Parse
dt = datetime.fromisoformat("2025-01-15T14:30:00")
dt.year; dt.month; dt.day; dt.hour; dt.strftime("%A")  # weekday name

# Arithmetic
tomorrow = now + timedelta(days=1)
yesterday = now - timedelta(days=1)
next_week = now + timedelta(weeks=1)
one_hour_ago = now - timedelta(hours=1)

# Compare
date1 = datetime(2025, 1, 15)
date2 = datetime(2025, 1, 20)
diff = date2 - date1
diff.days; diff.total_seconds()
date1 < date2   # is earlier
date2 > date1   # is later

# Format variants
dt.strftime("%m/%d/%Y")       # US format
dt.strftime("%d/%m/%Y")       # EU format
dt.strftime("%A, %B %d, %Y")  # long format
dt.strftime("%I:%M %p")       # 12h time
dt.strftime("%H:%M:%S")       # 24h time
```

**re — regular expressions.**
```python
import re

text = "Email: alice@example.com, Phone: 555-1234"

# Search for one match
email_match = re.search(r'\b[\w.-]+@[\w.-]+\.\w+\b', text)
email = email_match.group(0) if email_match else None

# Find all matches
hashtags = re.findall(r'#(\w+)', "Tags: #python #automation #workflow #n8n")

# Replace / clean
cleaned = re.sub(r'\$', '', "Price: $99.99, Discount: $10.00")
normalized = re.sub(r'\s+', ' ', cleaned)

# Validate format
email_pattern = r'^[\w.-]+@[\w.-]+\.\w+$'
is_valid = bool(re.match(email_pattern, email or ""))

# Split on multiple delimiters
items = re.split(r'[,;|]', "apple,banana;orange|grape")
items = [item.strip() for item in items]
```

**base64 — encoding/decoding.**
```python
import base64

# Encode
text = "Hello, World!"
encoded_string = base64.b64encode(text.encode('utf-8')).decode('utf-8')

# Decode
decoded_string = base64.b64decode("SGVsbG8sIFdvcmxkIQ==").decode('utf-8')

# Basic Auth header
credentials = f"{username}:{password}"
encoded = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
auth_header = f"Basic {encoded}"
```

**hashlib — hashing.**
```python
import hashlib
from datetime import datetime

# MD5
md5_hash = hashlib.md5("Hello, World!".encode('utf-8')).hexdigest()

# SHA256 (preferred over MD5 for anything sensitive)
sha256_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()

# Generate a short unique ID from multiple values
unique_string = f"{datetime.now().isoformat()}-{_json.get('user_id', 'unknown')}"
unique_id = hashlib.sha256(unique_string.encode('utf-8')).hexdigest()[:16]
```

**urllib.parse — URL operations.**
```python
from urllib.parse import urlparse, urlencode, parse_qs, quote, unquote

# Parse a URL
parsed = urlparse("https://example.com/path?key=value&foo=bar#section")
parsed.scheme    # "https"
parsed.netloc    # "example.com"
parsed.path      # "/path"
parsed.query     # "key=value&foo=bar"
parsed.fragment  # "section"

# Encode params for a URL
params = {"name": "Alice Smith", "email": "alice@example.com", "message": "Hello, World!"}
encoded = urlencode(params)

# Parse a query string
params = parse_qs("name=Alice&age=30&tags=python&tags=n8n")
params.get("name", [""])[0]
int(params.get("age", ["0"])[0])
params.get("tags", [])

# Encode/decode arbitrary strings
encoded = quote("Hello, World! 你好")
decoded = unquote(encoded)
```

**math — mathematical operations.**
```python
import math

math.ceil(16.7)       # 17
math.floor(16.7)      # 16
round(16.7)            # 17
math.sqrt(16)          # 4.0
math.pow(2, 3)         # 8.0
math.fabs(-5.5)        # 5.5

# Trigonometry
angle_radians = math.radians(45)
math.sin(angle_radians); math.cos(angle_radians); math.tan(angle_radians)
math.pi; math.e

# Logarithms
math.log10(100)   # 2.0
math.log(100)      # natural log, ~4.605
math.log2(100)     # ~6.644
```

**random — random numbers and sampling.**
```python
import random

random.random()               # 0.0 to 1.0
random.randint(1, 100)        # 1 to 100 inclusive
random.randrange(0, 100, 5)   # 0, 5, 10, ..., 95

random.choice(["red", "green", "blue", "yellow"])
random.choice([{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}])

items = [1, 2, 3, 4, 5]
shuffled = items.copy()
random.shuffle(shuffled)

sample = random.sample(list(range(1, 101)), 10)  # 10 unique items, no replacement
```

**statistics — statistical functions.**
```python
import statistics

numbers = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
statistics.mean(numbers)             # 55.0
statistics.median(numbers)           # 55.0
statistics.mode([1, 2, 2, 3])       # 2
statistics.stdev(numbers)            # ~30.28
statistics.variance(numbers)         # ~916.67

# Aggregate straight from n8n items
all_items = _input.all()
amounts = [item["json"].get("amount", 0) for item in all_items]
if amounts:
    return [{
        "json": {
            "count": len(amounts),
            "total": sum(amounts),
            "average": statistics.mean(amounts),
            "median": statistics.median(amounts),
            "min": min(amounts),
            "max": max(amounts),
            "range": max(amounts) - min(amounts)
        }
    }]
else:
    return [{"json": {"error": "No data"}}]
```

**Combining modules for a real task:**
```python
import json
import base64
import hashlib
from datetime import datetime

data = _input.first()["json"]["body"]

# Hash sensitive data into a stable pseudonymous ID
user_id = hashlib.sha256(data.get("email", "").encode()).hexdigest()[:16]

# Encode the payload for storage
encoded_data = base64.b64encode(json.dumps(data).encode()).decode()

return [{
    "json": {
        "user_id": user_id,
        "encoded_data": encoded_data,
        "timestamp": datetime.now().isoformat()
    }
}]
```

**Workaround pattern — "pandas-style" grouping and aggregation without pandas:**
```python
from collections import defaultdict
import statistics

all_items = _input.all()

# Filter
active_items = [item for item in all_items if item["json"].get("status") == "active"]

# Group by
grouped = defaultdict(list)
for item in all_items:
    category = item["json"].get("category", "other")
    grouped[category].append(item["json"])

# Aggregate
amounts = [item["json"].get("amount", 0) for item in all_items]
total = sum(amounts)
average = statistics.mean(amounts) if amounts else 0

return [{
    "json": {
        "active_count": len(active_items),
        "grouped": dict(grouped),
        "total": total,
        "average": average
    }
}]
```

**Workaround pattern — database/API results processed after an upstream n8n node did the actual I/O:**
```python
# For a database node upstream (Postgres/MySQL/MongoDB):
db_results = _input.first()["json"]

return [{
    "json": {
        "record_count": len(db_results) if isinstance(db_results, list) else 1,
        "processed": True
    }
}]
```

### Complete standard library availability list

**Available (commonly useful):**
`json` · `datetime`, `time` · `re` · `base64` · `hashlib` · `urllib.parse`, `urllib.request`, `urllib.error` · `math` · `random` · `statistics` · `collections` (`defaultdict`, `Counter`, `namedtuple`) · `itertools` · `functools` · `operator` · `string` · `textwrap`

**Available (less common):**
`os.path` (path operations only) · `copy` · `typing` · `enum` · `decimal` · `fractions`

**NOT available (external libraries — none of these can be imported):**
`requests` (HTTP) · `pandas` (data analysis) · `numpy` (numerical computing) · `bs4`/`beautifulsoup4` (HTML parsing) · `selenium` (browser automation) · `psycopg2`, `pymongo`, `sqlalchemy` (databases) · `flask`, `fastapi` (web frameworks) · `pillow` (image processing) · `openpyxl`, `xlsxwriter` (Excel)

### Related documents

For the JavaScript-equivalent Code node — the recommended default for most tasks, with no external-library restrictions and built-in HTTP/date helpers — see the companion n8n JavaScript Code Node reference document.
