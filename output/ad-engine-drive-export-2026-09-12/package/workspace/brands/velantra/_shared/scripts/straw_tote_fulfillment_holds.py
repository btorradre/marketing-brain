#!/usr/bin/env python3
"""Hold (or release) fulfillment orders for unfulfilled Velantra Straw Tote orders.

Why: SDH/Dianxiaomi marks every order FULFILLED within ~12h of purchase — weeks
before production ships. That fake fulfillment fires Shopify's shipping
confirmation and arms 17TRACK/ParcelPanel status emails plus review-request
timers, which then contradict the delay notice. Placing the fulfillment orders
ON HOLD blocks Dianxiaomi from fulfilling them, so no premature "shipped"
emails fire. Release the holds when production actually ships.

DECISION REQUIRED BEFORE RUNNING — holds block SDH's ERP from syncing
fulfillment. Confirm with SDH/ops first, and remember to release when bags
actually move or real shipping confirmations will not reach customers.

Usage:
  python3 straw_tote_fulfillment_holds.py hold            # dry-run list
  python3 straw_tote_fulfillment_holds.py hold --apply    # place holds
  python3 straw_tote_fulfillment_holds.py release --apply # release all holds
"""
import json, os, subprocess, sys

VAULT = os.path.expanduser("~/Documents/marketing brain")
SCOPE_TITLE = "Straw Tote"
HOLD_NOTE = "Production delay - do not fulfill until batch ships (est. early Aug 2026)"


def env():
    vals = {}
    for line in open(os.path.join(VAULT, ".env")):
        line = line.strip()
        if line.startswith("SHOPIFY_VELANTRA") and "=" in line:
            k, v = line.split("=", 1)
            vals[k] = v.strip()
    return vals


def gql(store, token, query, variables=None):
    body = json.dumps({"query": query, "variables": variables or {}})
    r = subprocess.run(
        ["curl", "-s", f"https://{store}/admin/api/2024-10/graphql.json",
         "-H", f"X-Shopify-Access-Token: {token}",
         "-H", "Content-Type: application/json", "-d", body],
        capture_output=True, text=True)
    d = json.loads(r.stdout)
    if "errors" in d:
        sys.exit(f"GraphQL errors: {d['errors']}")
    return d["data"]


def get_token(e):
    r = subprocess.run(
        ["curl", "-s", "-X", "POST",
         f"https://{e['SHOPIFY_VELANTRA_STORE']}/admin/oauth/access_token",
         "-H", "Content-Type: application/json",
         "-d", json.dumps({"client_id": e["SHOPIFY_VELANTRA_CLIENT_ID"],
                            "client_secret": e["SHOPIFY_VELANTRA_CLIENT_SECRET"],
                            "grant_type": "client_credentials"})],
        capture_output=True, text=True)
    return json.loads(r.stdout)["access_token"]


def target_fulfillment_orders(store, token, want_status):
    # Note: held orders no longer match fulfillment_status:unfulfilled, so the
    # release pass scans by date only.
    status_filter = "fulfillment_status:unfulfilled " if want_status == "OPEN" else ""
    q = """query($cursor: String) {
      orders(first: 50, after: $cursor, query: "%screated_at:>2026-06-13") {""" % status_filter
    q += """
        pageInfo { hasNextPage endCursor }
        nodes { name
          lineItems(first: 10) { nodes { title } }
          fulfillmentOrders(first: 5) { nodes { id status
            lineItems(first: 10) { nodes { lineItem { title } } } } } } } }"""
    cursor, out = None, []
    while True:
        d = gql(store, token, q, {"cursor": cursor})
        for o in d["orders"]["nodes"]:
            if not any(SCOPE_TITLE in li["title"] for li in o["lineItems"]["nodes"]):
                continue
            for fo in o["fulfillmentOrders"]["nodes"]:
                fo_titles = [x["lineItem"]["title"] for x in fo["lineItems"]["nodes"]]
                if fo["status"] == want_status and any(SCOPE_TITLE in t for t in fo_titles):
                    out.append((o["name"], fo["id"], fo["status"]))
        pi = d["orders"]["pageInfo"]
        if not pi["hasNextPage"]:
            return out
        cursor = pi["endCursor"]


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "hold"
    apply = "--apply" in sys.argv
    e = env()
    store, token = e["SHOPIFY_VELANTRA_STORE"], get_token(e)
    want = "OPEN" if mode == "hold" else "ON_HOLD"
    targets = target_fulfillment_orders(store, token, want)
    print(f"{mode.upper()}: {len(targets)} fulfillment orders match (status {want})")
    for name, foid, st in targets:
        print(" ", name, foid.split("/")[-1], st)
    if not apply:
        print("\nDry run only. Re-run with --apply to execute.")
        return
    if mode == "hold":
        m = """mutation($id: ID!) { fulfillmentOrderHold(id: $id,
              fulfillmentHold: {reason: OTHER, reasonNotes: "%s"})
              { userErrors { field message } } }""" % HOLD_NOTE
    else:
        m = """mutation($id: ID!) { fulfillmentOrderReleaseHold(id: $id)
              { userErrors { field message } } }"""
    for name, foid, _ in targets:
        d = gql(store, token, m, {"id": foid})
        errs = list(d.values())[0]["userErrors"]
        print(" ", name, "OK" if not errs else errs)


if __name__ == "__main__":
    main()
