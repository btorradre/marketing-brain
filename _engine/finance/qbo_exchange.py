#!/usr/bin/env python3
"""Exchange a QuickBooks authorization code for tokens and persist them.

    python3 qbo_exchange.py --code <CODE> --realm <REALM_ID> [--env production]

Used instead of the MCP server's `npm run auth` because production QuickBooks
apps cannot use a localhost redirect URI. The browser lands on the dashboard's
/qbo/callback route, which displays the code; this script does the rest.

Writes access/refresh tokens and the realm id into the MCP server's .env, so
both the MCP server and the nightly margin pipeline pick them up.
"""
import argparse
import base64
import json
import os
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request

QBO_ENV = os.path.expanduser(
    "~/.claude/mcp-servers/quickbooks-online-mcp-server/.env")
TOKEN_URL = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"

try:
    import certifi
    CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    CTX = ssl.create_default_context()


def read_env():
    cfg = {}
    if os.path.exists(QBO_ENV):
        for line in open(QBO_ENV):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                cfg[k.strip()] = v.strip()
    return cfg


def write_env(updates):
    lines = open(QBO_ENV).read().splitlines() if os.path.exists(QBO_ENV) else []
    seen = set()
    out = []
    for line in lines:
        key = line.split("=", 1)[0].strip() if "=" in line else None
        if key in updates:
            out.append(f"{key}={updates[key]}")
            seen.add(key)
        else:
            out.append(line)
    for k, v in updates.items():
        if k not in seen:
            out.append(f"{k}={v}")
    tmp = QBO_ENV + ".tmp"
    with open(tmp, "w") as f:
        f.write("\n".join(out).rstrip() + "\n")
    os.replace(tmp, QBO_ENV)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--code", required=True)
    ap.add_argument("--realm", required=True)
    ap.add_argument("--redirect",
                    default="https://f1.bto-financials.co/qbo/callback")
    ap.add_argument("--env", default="production",
                    choices=["production", "sandbox"])
    args = ap.parse_args()

    cfg = read_env()
    cid, secret = cfg.get("QUICKBOOKS_CLIENT_ID"), cfg.get("QUICKBOOKS_CLIENT_SECRET")
    if not cid or not secret:
        sys.exit("CLIENT_ID / CLIENT_SECRET missing from the MCP server .env")

    basic = base64.b64encode(f"{cid}:{secret}".encode()).decode()
    body = urllib.parse.urlencode({
        "grant_type": "authorization_code",
        "code": args.code,
        "redirect_uri": args.redirect,
    }).encode()
    req = urllib.request.Request(TOKEN_URL, data=body, method="POST", headers={
        "Authorization": f"Basic {basic}",
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    })
    try:
        with urllib.request.urlopen(req, timeout=45, context=CTX) as r:
            tok = json.load(r)
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")
        sys.exit(f"token exchange failed: HTTP {e.code}\n{detail}\n\n"
                 f"invalid_grant usually means the code was already used or "
                 f"expired (10 min), or redirect_uri does not match the one "
                 f"used to obtain it exactly.")

    write_env({
        "QUICKBOOKS_REFRESH_TOKEN": tok["refresh_token"],
        "QUICKBOOKS_REALM_ID": args.realm,
        "QUICKBOOKS_ENVIRONMENT": args.env,
        "QUICKBOOKS_REDIRECT_URI": args.redirect,
    })
    print("tokens written to", QBO_ENV)
    print(f"  environment       : {args.env}")
    print(f"  realm id          : {args.realm}")
    print(f"  access expires in : {tok.get('expires_in')}s")
    print(f"  refresh expires in: {tok.get('x_refresh_token_expires_in')}s")


if __name__ == "__main__":
    main()
