# Python Standard Library Reference (n8n Code Node)

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

Module priority: **json** (most commonly used) · **datetime** (very common) · **re** (common) · **base64** (common) · **hashlib** (common) · **urllib.parse** (common) · **math**, **random**, **statistics**, **collections** (moderately useful) · **itertools**, **functools**, **operator**, **string**, **textwrap** (occasionally useful).

## json — parse and generate JSON

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

## datetime — date and time

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

## re — regular expressions

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

## base64 — encoding/decoding

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

## hashlib — hashing

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

## urllib.parse — URL operations

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

## math — mathematical operations

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

## random — random numbers and sampling

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

## statistics — statistical functions

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

## Combining modules for a real task

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

## Workaround pattern — "pandas-style" grouping and aggregation without pandas

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

## Workaround pattern — database/API results processed after an upstream n8n node did the actual I/O

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

## Complete Standard Library Availability List

**Available (commonly useful):**
`json` · `datetime`, `time` · `re` · `base64` · `hashlib` · `urllib.parse`, `urllib.request`, `urllib.error` · `math` · `random` · `statistics` · `collections` (`defaultdict`, `Counter`, `namedtuple`) · `itertools` · `functools` · `operator` · `string` · `textwrap`

**Available (less common):**
`os.path` (path operations only) · `copy` · `typing` · `enum` · `decimal` · `fractions`

**NOT available (external libraries — none of these can be imported):**
`requests` (HTTP) · `pandas` (data analysis) · `numpy` (numerical computing) · `bs4`/`beautifulsoup4` (HTML parsing) · `selenium` (browser automation) · `psycopg2`, `pymongo`, `sqlalchemy` (databases) · `flask`, `fastapi` (web frameworks) · `pillow` (image processing) · `openpyxl`, `xlsxwriter` (Excel)

## Standard-Library-Only HTTP (Last Resort)

When no HTTP Request node can be inserted upstream and JavaScript isn't an option, a bare unauthenticated GET is possible:

```python
from urllib.request import urlopen
from urllib.parse import urlencode
import json

url = "https://api.example.com/data"
with urlopen(url) as response:
    data = json.loads(response.read())

return [{"json": data}]
```

This has no support for custom headers or authentication — for anything beyond a bare GET, use an HTTP Request node or JavaScript instead.
