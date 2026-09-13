"""Shared utilities for the contribution-margin pipeline."""
import calendar
import json
import os
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta

try:
    import certifi
    SSL_CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CTX = ssl.create_default_context()

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
VAULT = os.path.dirname(ENGINE)
ENV_PATH = os.path.join(VAULT, ".env")
DATA_DIR = os.path.join(HERE, "data")
CONFIG_PATH = os.path.join(HERE, "costs.json")
STORES_JSON = os.path.join(
    VAULT, ".claude", "skills", "shopify-financials", "config", "stores.json")

_env_cache = None


def env(key, default=None):
    global _env_cache
    if _env_cache is None:
        _env_cache = {}
        if os.path.exists(ENV_PATH):
            for line in open(ENV_PATH):
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, _, v = line.partition("=")
                    _env_cache[k.strip()] = v.strip()
    return os.environ.get(key) or _env_cache.get(key, default)


def http_json(url, headers=None, payload=None, form=None, method=None,
              timeout=90, retries=4):
    """JSON over HTTP with backoff on 429 and 5xx.

    Triple Whale's SQL endpoint allows 5 req/sec and 100 req/min despite the
    docs claiming 600/min, so callers must be paced and 429s must be honoured.
    """
    if form is not None:
        body = urllib.parse.urlencode(form).encode()
        hdrs = {"Content-Type": "application/x-www-form-urlencoded"}
    elif payload is not None:
        body = json.dumps(payload).encode()
        hdrs = {"Content-Type": "application/json"}
    else:
        body, hdrs = None, {}
    hdrs.update(headers or {})

    last = None
    for attempt in range(retries):
        req = urllib.request.Request(url, data=body, headers=hdrs, method=method)
        try:
            resp = urllib.request.urlopen(req, timeout=timeout, context=SSL_CTX)
            return json.load(resp), dict(resp.headers)
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")[:400]
            last = RuntimeError(f"HTTP {e.code} {url.split('?')[0]}: {detail}")
            if e.code == 429:
                time.sleep(float(e.headers.get("Retry-After") or 2 ** attempt))
                continue
            if 500 <= e.code < 600:
                time.sleep(2 ** attempt)
                continue
            raise last
        except (urllib.error.URLError, TimeoutError) as e:
            last = RuntimeError(f"network error on {url.split('?')[0]}: {e}")
            time.sleep(2 ** attempt)
    raise last


def load_config():
    return json.load(open(CONFIG_PATH))


def load_stores():
    stores = json.load(open(STORES_JSON))
    if isinstance(stores, dict):
        stores = stores.get("stores", [])
    return stores


def store_by_domain(domain):
    for s in load_stores():
        if s["domain"] == domain:
            return s
    raise KeyError(f"no store in stores.json with domain {domain}")


def daterange(start, end):
    """Inclusive list of ISO date strings."""
    d0 = date.fromisoformat(start)
    d1 = date.fromisoformat(end)
    out = []
    while d0 <= d1:
        out.append(d0.isoformat())
        d0 += timedelta(days=1)
    return out


def days_in_month(iso_day):
    d = date.fromisoformat(iso_day)
    return calendar.monthrange(d.year, d.month)[1]


def month_key(iso_day):
    return iso_day[:7]


def money(x):
    return round(float(x or 0), 2)


def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f, indent=2, sort_keys=False)
    os.replace(tmp, path)
    return path
