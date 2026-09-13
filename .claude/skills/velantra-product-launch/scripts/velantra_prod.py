#!/usr/bin/env python3
"""Shared config + auth for the Velantra product-launch skill.

Resolves the PRODUCTION Velantra store from the vault .env (client_credentials),
mints an Admin API token, and locates the live (main) theme id.

Everything else in the skill imports from here so the existing theme-build
scripts (which hardcode the uzdgxy-sb sandbox) can be monkey-patched onto
production at runtime.
"""
import json, urllib.request, urllib.error
from pathlib import Path

VAULT = Path("/Users/brooksorradre2/Documents/marketing brain")
ENV_PATH = VAULT / ".env"
BUILD_DIR = VAULT / "brands/velantra/_shared/theme-build/_build"
API = "2024-10"

_cache = {}


def load_env():
    env = {}
    for line in ENV_PATH.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def _http(url, method="GET", data=None, headers=None, timeout=60):
    h = headers or {}
    body = data
    if isinstance(body, (dict, list)):
        body = json.dumps(body).encode()
        h.setdefault("Content-Type", "application/json")
    req = urllib.request.Request(url, data=body, method=method, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def mint_token(store, client_id, client_secret):
    """Exchange client_credentials for a short-lived Admin API access token."""
    url = f"https://{store}/admin/oauth/access_token"
    body = (
        f"grant_type=client_credentials&client_id={client_id}"
        f"&client_secret={client_secret}"
    ).encode()
    code, resp = _http(
        url, "POST", body,
        {"Content-Type": "application/x-www-form-urlencoded"},
    )
    if code != 200:
        raise RuntimeError(f"token mint failed {code}: {resp[:300]}")
    return json.loads(resp)["access_token"]


def main_theme_id(store, token):
    url = f"https://{store}/admin/api/{API}/themes.json"
    code, resp = _http(url, headers={"X-Shopify-Access-Token": token})
    if code != 200:
        raise RuntimeError(f"themes.json {code}: {resp[:300]}")
    themes = json.loads(resp)["themes"]
    for t in themes:
        if t.get("role") == "main":
            return t["id"]
    raise RuntimeError("no main theme found")


def context():
    """Return {store, token, theme_id, api} for production Velantra (cached)."""
    if _cache:
        return _cache
    env = load_env()
    store = env["SHOPIFY_VELANTRA_STORE"]
    if not store.endswith("myshopify.com"):
        store = f"{store}.myshopify.com" if "." not in store else store
    token = mint_token(
        store, env["SHOPIFY_VELANTRA_CLIENT_ID"],
        env["SHOPIFY_VELANTRA_CLIENT_SECRET"],
    )
    theme_id = main_theme_id(store, token)
    _cache.update(store=store, token=token, theme_id=theme_id, api=API)
    return _cache


if __name__ == "__main__":
    ctx = context()
    print(json.dumps({k: v for k, v in ctx.items() if k != "token"}, indent=2))
    print("token: (minted ok,", len(ctx["token"]), "chars)")
