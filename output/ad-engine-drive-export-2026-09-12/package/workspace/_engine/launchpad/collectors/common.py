"""Shared utilities for launchpad collectors."""
import json, os, ssl, urllib.request, urllib.parse
from datetime import datetime, timedelta

try:
    import certifi
    SSL_CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CTX = ssl.create_default_context()

HERE = os.path.dirname(os.path.abspath(__file__))
LAUNCHPAD = os.path.dirname(HERE)
VAULT = os.path.dirname(os.path.dirname(LAUNCHPAD))  # marketing brain/
ENV_PATH = os.path.join(VAULT, ".env")
AUTH_DIR = os.path.join(LAUNCHPAD, "auth")
DATA_DIR = os.path.join(LAUNCHPAD, "data")

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


def http_json(url, headers=None, payload=None, form=None, method=None, timeout=30):
    if form is not None:
        body = urllib.parse.urlencode(form).encode()
        hdrs = {"Content-Type": "application/x-www-form-urlencoded"}
    elif payload is not None:
        body = json.dumps(payload).encode()
        hdrs = {"Content-Type": "application/json"}
    else:
        body, hdrs = None, {}
    hdrs.update(headers or {})
    req = urllib.request.Request(url, data=body, headers=hdrs, method=method)
    resp = urllib.request.urlopen(req, timeout=timeout, context=SSL_CTX)
    return json.load(resp), dict(resp.headers)


def week_start(now=None):
    """Most recent Sunday 00:00 local time (Brooks tracks weeks Sunday-to-date)."""
    now = now or datetime.now().astimezone()
    days_since_sunday = (now.weekday() + 1) % 7  # Mon=0 ... Sun=6 -> 0
    return (now - timedelta(days=days_since_sunday)).replace(hour=0, minute=0, second=0, microsecond=0)


def today_start(now=None):
    now = now or datetime.now().astimezone()
    return now.replace(hour=0, minute=0, second=0, microsecond=0)
