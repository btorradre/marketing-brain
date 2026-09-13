#!/usr/bin/env python3
"""Shopify Admin API access for the product-launch skill. Multi-brand, curl-backed.

WHY CURL: urllib in this environment has no CA bundle (CERTIFICATE_VERIFY_FAILED)
and has been observed to hang on Shopify GraphQL. Every request here shells out to
curl, which uses the system trust store and never hangs silently.

Brands resolve from `marketing brain/.env`:
    SHOPIFY_<BRAND>_STORE / _CLIENT_ID / _CLIENT_SECRET
Known: VELANTRA, MOTILLI_1, MOTILLI_2, LUNESSA, SOLORNA, WEND

Usage as a library:
    import shop
    ctx = shop.context("velantra")          # {store, token, theme_id, api}
    data = shop.gql(ctx, QUERY, {"id": ...})
    code, body = shop.rest(ctx, "products.json?limit=250")

Usage from the shell (sanity check / one-offs):
    python3 shop.py context velantra
    python3 shop.py theme-get velantra templates/product.weekender.json
"""
import json, os, subprocess, sys, tempfile, urllib.parse
from pathlib import Path

VAULT = Path("/Users/brooksorradre2/Documents/marketing brain")
ENV_PATH = VAULT / ".env"
API = "2025-07"

_cache = {}


# ── env ──────────────────────────────────────────────────────────────────────
def load_env():
    env = {}
    for line in ENV_PATH.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


# ── transport ────────────────────────────────────────────────────────────────
def curl(url, method="GET", data=None, headers=None, timeout=180):
    """Return (http_status:int, body:str). Never raises on HTTP errors."""
    cmd = ["curl", "-sS", "-m", str(timeout), "-X", method,
           "-w", "\n__HTTP_STATUS__%{http_code}", url]
    for k, v in (headers or {}).items():
        cmd += ["-H", f"{k}: {v}"]
    tmp = None
    if data is not None:
        if not isinstance(data, (str, bytes)):
            data = json.dumps(data)
        # route the body through a file: product images base64 blow past ARGV limits
        tmp = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
        tmp.write(data if isinstance(data, str) else data.decode())
        tmp.close()
        cmd += ["--data-binary", f"@{tmp.name}"]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 30)
    finally:
        if tmp:
            os.unlink(tmp.name)
    out = r.stdout
    if "__HTTP_STATUS__" not in out:
        return 0, (r.stderr or out)[-500:]
    body, _, status = out.rpartition("\n__HTTP_STATUS__")
    return int(status.strip() or 0), body


def _mint_token(store, cid, secret):
    code, body = curl(
        f"https://{store}/admin/oauth/access_token", "POST",
        json.dumps({"grant_type": "client_credentials",
                    "client_id": cid, "client_secret": secret}),
        {"Content-Type": "application/json"})
    if code != 200:
        raise RuntimeError(f"token mint failed {code}: {body[:300]}")
    return json.loads(body)["access_token"]


def context(brand="velantra"):
    """{store, token, theme_id, api} for a brand. Cached per-process. Never persist the token."""
    key = brand.lower()
    if key in _cache:
        return _cache[key]
    env = load_env()
    p = f"SHOPIFY_{brand.upper()}_"
    if p + "STORE" not in env:
        avail = sorted({k[8:-6] for k in env if k.startswith("SHOPIFY_") and k.endswith("_STORE")})
        raise SystemExit(f"unknown brand '{brand}'. .env has: {', '.join(avail)}")
    store = env[p + "STORE"]
    if not store.endswith(".myshopify.com"):
        store = f"{store}.myshopify.com"
    token = _mint_token(store, env[p + "CLIENT_ID"], env[p + "CLIENT_SECRET"])
    ctx = {"store": store, "token": token, "api": API, "brand": key}
    ctx["theme_id"] = main_theme_id(ctx)
    _cache[key] = ctx
    return ctx


def _h(ctx, extra=None):
    h = {"X-Shopify-Access-Token": ctx["token"], "Content-Type": "application/json"}
    h.update(extra or {})
    return h


# ── REST ─────────────────────────────────────────────────────────────────────
def rest(ctx, path, method="GET", data=None, timeout=180):
    url = f"https://{ctx['store']}/admin/api/{ctx['api']}/{path.lstrip('/')}"
    code, body = curl(url, method, data, _h(ctx), timeout)
    try:
        return code, (json.loads(body) if body.strip() else {})
    except json.JSONDecodeError:
        return code, {"_raw": body[:600]}


# ── GraphQL ──────────────────────────────────────────────────────────────────
def gql(ctx, query, variables=None, timeout=180):
    """Returns the `data` block. Raises on transport errors or userErrors."""
    url = f"https://{ctx['store']}/admin/api/{ctx['api']}/graphql.json"
    code, body = curl(url, "POST",
                      json.dumps({"query": query, "variables": variables or {}}),
                      _h(ctx), timeout)
    if code != 200:
        raise RuntimeError(f"graphql {code}: {body[:500]}")
    payload = json.loads(body)
    if payload.get("errors"):
        raise RuntimeError(f"graphql errors: {json.dumps(payload['errors'])[:600]}")
    data = payload.get("data") or {}
    for op in data.values():
        if isinstance(op, dict) and op.get("userErrors"):
            raise RuntimeError(f"userErrors: {json.dumps(op['userErrors'])[:600]}")
    return data


# ── themes ───────────────────────────────────────────────────────────────────
def main_theme_id(ctx):
    """The PUBLISHED theme. Never hardcode a theme id — Velantra republishes."""
    code, resp = rest(ctx, "themes.json")
    if code != 200:
        raise RuntimeError(f"themes.json {code}: {str(resp)[:300]}")
    for t in resp["themes"]:
        if t.get("role") == "main":
            return t["id"]
    raise RuntimeError("no main theme")


def theme_get(ctx, key, theme_id=None):
    """Read one theme asset (e.g. 'templates/product.weekender.json'). None if absent."""
    tid = theme_id or ctx["theme_id"]
    q = urllib.parse.urlencode({"asset[key]": key})
    code, resp = rest(ctx, f"themes/{tid}/assets.json?{q}")
    if code != 200:
        return None
    return resp.get("asset", {}).get("value")


def theme_put(ctx, key, value, theme_id=None):
    """Write one theme asset. value may be str or json-able."""
    tid = theme_id or ctx["theme_id"]
    if not isinstance(value, str):
        value = json.dumps(value, indent=2)
    code, resp = rest(ctx, f"themes/{tid}/assets.json", "PUT",
                      {"asset": {"key": key, "value": value}})
    return code in (200, 201), (None if code in (200, 201) else f"{code}: {str(resp)[:300]}")


def theme_list(ctx, prefix="templates/product.", theme_id=None):
    tid = theme_id or ctx["theme_id"]
    code, resp = rest(ctx, f"themes/{tid}/assets.json")
    if code != 200:
        return []
    return sorted(a["key"] for a in resp.get("assets", []) if a["key"].startswith(prefix))


# ── CLI ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    cmd = args[0]
    brand = args[1] if len(args) > 1 else "velantra"
    ctx = context(brand)
    if cmd == "context":
        print(json.dumps({k: v for k, v in ctx.items() if k != "token"}, indent=2))
        print(f"token minted ok ({len(ctx['token'])} chars)")
    elif cmd == "templates":
        print("\n".join(theme_list(ctx)))
    elif cmd == "theme-get":
        v = theme_get(ctx, args[2])
        print(v if v is not None else f"!! not found: {args[2]}")
    else:
        sys.exit(f"unknown command: {cmd}")
