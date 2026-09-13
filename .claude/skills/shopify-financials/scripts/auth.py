#!/usr/bin/env python3
"""
Shopify auth helper — turn credentials into permanent Admin API tokens and
manage config/stores.json.

Two ways a store gets an admin token:

1. client-credentials (default, what all current stores use)
   The custom app's client_id + client_secret mint a fresh token per run.
   Nothing is stored beyond the id/secret.

2. post-auth authorization code  ->  permanent offline access token
   For apps installed via the OAuth install flow: after the merchant approves
   the app, Shopify redirects with ?code=<post-auth code>. Exchange it here
   ONCE and the resulting offline access_token (shpat_/shpca_...) never
   expires; it is saved on the store entry and used directly from then on.

Commands:
  python3 auth.py exchange-code --domain x.myshopify.com --client-id ID \
      --client-secret SECRET --code POST_AUTH_CODE --brand "Orelli" [--group Orelli]
  python3 auth.py add-store --brand "Orelli" --domain x.myshopify.com \
      --client-id ID --client-secret SECRET [--group Orelli]
  python3 auth.py add-token --brand "Orelli" --domain x.myshopify.com \
      --access-token shpat_xxx [--group Orelli]
  python3 auth.py test                # verify every store in stores.json authenticates
  python3 auth.py list                # show configured stores (secrets redacted)

Post-auth codes are single-use and expire in minutes — exchange immediately.
"""
import json, os, sys, argparse, ssl, urllib.request, urllib.parse

# macOS python lacks system CA certs — use certifi's bundle when available
try:
    import certifi
    _SSL_CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    _SSL_CTX = ssl.create_default_context()
urllib.request.install_opener(urllib.request.build_opener(urllib.request.HTTPSHandler(context=_SSL_CTX)))

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(os.path.dirname(HERE), "config", "stores.json")


def _load(config_path):
    with open(config_path) as f:
        return json.load(f)


def _save(cfg, config_path):
    with open(config_path, "w") as f:
        json.dump(cfg, f, indent=2)
        f.write("\n")


def _post_json(url, payload):
    body = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=30))


def _post_form(url, data):
    body = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/x-www-form-urlencoded"})
    return json.load(urllib.request.urlopen(req, timeout=30))


def _shop_info(domain, ver, token):
    req = urllib.request.Request(
        f"https://{domain}/admin/api/{ver}/shop.json",
        headers={"X-Shopify-Access-Token": token})
    return json.load(urllib.request.urlopen(req, timeout=30))["shop"]


def token_for(store, ver="2025-01"):
    """Static access_token wins; else mint via client-credentials."""
    if store.get("access_token"):
        return store["access_token"]
    try:
        r = _post_form(f"https://{store['domain']}/admin/oauth/access_token",
                       {"grant_type": "client_credentials",
                        "client_id": store["client_id"],
                        "client_secret": store["client_secret"]})
        return r["access_token"]
    except urllib.error.HTTPError as e:
        if e.code == 400:
            raise RuntimeError(f"{store['domain']}: app_not_installed — install the custom app "
                               "in the store admin, or the store is closed / credentials revoked") from None
        raise


def _upsert(cfg, entry):
    for i, s in enumerate(cfg["stores"]):
        if s["domain"] == entry["domain"]:
            cfg["stores"][i] = {**s, **entry}
            return "updated"
    cfg["stores"].append(entry)
    return "added"


def cmd_exchange_code(args, cfg, ver):
    r = _post_json(f"https://{args.domain}/admin/oauth/access_token",
                   {"client_id": args.client_id,
                    "client_secret": args.client_secret,
                    "code": args.code})
    token = r["access_token"]
    shop = _shop_info(args.domain, ver, token)
    entry = {"brand": args.brand or shop["name"],
             "group": args.group or (args.brand or shop["name"]).split("#")[0].strip(),
             "domain": args.domain, "access_token": token}
    action = _upsert(cfg, entry)
    _save(cfg, args.config)
    print(f"OK — {action} '{entry['brand']}' ({args.domain})")
    print(f"     shop: {shop['name']} · plan: {shop.get('plan_name')} · scopes granted: {r.get('scope', '?')}")
    print("     Permanent offline token saved to stores.json — no re-auth needed.")


def cmd_add_store(args, cfg, ver):
    entry = {"brand": args.brand,
             "group": args.group or args.brand.split("#")[0].strip(),
             "domain": args.domain,
             "client_id": args.client_id, "client_secret": args.client_secret}
    token = token_for(entry, ver)  # proves the creds work before saving
    shop = _shop_info(args.domain, ver, token)
    action = _upsert(cfg, entry)
    _save(cfg, args.config)
    print(f"OK — {action} '{args.brand}' ({args.domain}) · shop: {shop['name']} · plan: {shop.get('plan_name')}")


def cmd_add_token(args, cfg, ver):
    shop = _shop_info(args.domain, ver, args.access_token)  # verify before saving
    entry = {"brand": args.brand,
             "group": args.group or args.brand.split("#")[0].strip(),
             "domain": args.domain, "access_token": args.access_token}
    action = _upsert(cfg, entry)
    _save(cfg, args.config)
    print(f"OK — {action} '{args.brand}' ({args.domain}) · shop: {shop['name']}")


def cmd_test(args, cfg, ver):
    bad = 0
    for s in cfg["stores"]:
        mode = "static token" if s.get("access_token") else "client-credentials"
        try:
            shop = _shop_info(s["domain"], ver, token_for(s, ver))
            print(f"  ✅ {s['brand']:14} {s['domain']:28} [{mode}] shop='{shop['name']}'")
        except Exception as e:
            bad += 1
            print(f"  ❌ {s['brand']:14} {s['domain']:28} [{mode}] {e}")
    sys.exit(1 if bad else 0)


def cmd_list(args, cfg, ver):
    for s in cfg["stores"]:
        auth = ("token " + s["access_token"][:9] + "…") if s.get("access_token") \
            else ("client " + s["client_id"][:8] + "…")
        print(f"  {s['brand']:14} group={s.get('group', '-'):10} {s['domain']:28} {auth}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", default=CONFIG)
    sub = ap.add_subparsers(dest="cmd", required=True)

    x = sub.add_parser("exchange-code", help="exchange a post-auth code for a permanent admin token")
    x.add_argument("--domain", required=True); x.add_argument("--client-id", required=True)
    x.add_argument("--client-secret", required=True); x.add_argument("--code", required=True)
    x.add_argument("--brand"); x.add_argument("--group")

    a = sub.add_parser("add-store", help="add a store using client-credentials")
    a.add_argument("--brand", required=True); a.add_argument("--domain", required=True)
    a.add_argument("--client-id", required=True); a.add_argument("--client-secret", required=True)
    a.add_argument("--group")

    t = sub.add_parser("add-token", help="add a store using an existing shpat_ admin token")
    t.add_argument("--brand", required=True); t.add_argument("--domain", required=True)
    t.add_argument("--access-token", required=True); t.add_argument("--group")

    sub.add_parser("test", help="verify every configured store authenticates")
    sub.add_parser("list", help="show configured stores (secrets redacted)")

    args = ap.parse_args()
    cfg = _load(args.config)
    ver = cfg.get("api_version", "2025-01")
    try:
        {"exchange-code": cmd_exchange_code, "add-store": cmd_add_store, "add-token": cmd_add_token,
         "test": cmd_test, "list": cmd_list}[args.cmd](args, cfg, ver)
    except (RuntimeError, urllib.error.HTTPError) as e:
        print(f"❌ {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
