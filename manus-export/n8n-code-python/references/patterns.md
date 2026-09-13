# Ten Production-Tested Python Code Node Patterns

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

## Pattern Selection Guide

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
