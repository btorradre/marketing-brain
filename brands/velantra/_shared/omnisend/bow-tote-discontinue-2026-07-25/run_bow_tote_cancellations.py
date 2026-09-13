#!/usr/bin/env python3
"""
Bow Tote discontinue — cancel/refund executor.

Cohort A (12 Bow-Tote-only orders): orderCancel with refund, no restock, notify customer.
Cohort B (4 mixed orders):          refundCreate on the Bow Tote line only, at Shopify's
                                    suggestedRefund amount, then place a fulfillment HOLD on
                                    the leftover line so Dianxiaomi/SDH cannot fake-ship a bag
                                    that does not exist and fire another tracking email.

DRY RUN BY DEFAULT.  Nothing moves without --apply.

  python3 run_bow_tote_cancellations.py                # preview, no writes
  python3 run_bow_tote_cancellations.py --apply        # execute everything
  python3 run_bow_tote_cancellations.py --apply --cohort a
  python3 run_bow_tote_cancellations.py --apply --only '#30388,#30392'

Run this ONLY after E1-A and E1-B have actually sent (wait 45-60 min). Cancelling first makes
Shopify's automatic receipt land before the explanation, which is the exact collision that
burned the Straw Tote send.
"""

import argparse
import json
import pathlib
import ssl
import sys
import time
import urllib.request

import certifi

API_VERSION = "2026-07"
ROOT = pathlib.Path(__file__).resolve()
VAULT = ROOT.parents[5]                       # .../marketing brain
MANIFEST = ROOT.parent / "orders-manifest.json"
CTX = ssl.create_default_context(cafile=certifi.where())


# ---------------------------------------------------------------- auth / transport

def load_env() -> dict:
    env = {}
    for line in (VAULT / ".env").read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k] = v.strip().strip('"').strip("'")
    return env


def get_token(env: dict) -> tuple:
    store = env["SHOPIFY_VELANTRA_STORE"]
    body = json.dumps({
        "client_id": env["SHOPIFY_VELANTRA_CLIENT_ID"],
        "client_secret": env["SHOPIFY_VELANTRA_CLIENT_SECRET"],
        "grant_type": "client_credentials",
    }).encode()
    req = urllib.request.Request(
        f"https://{store}/admin/oauth/access_token", data=body,
        headers={"Content-Type": "application/json"})
    return store, json.load(urllib.request.urlopen(req, context=CTX))["access_token"]


def gql(store: str, token: str, query: str, variables: dict) -> dict:
    req = urllib.request.Request(
        f"https://{store}/admin/api/{API_VERSION}/graphql.json",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Content-Type": "application/json", "X-Shopify-Access-Token": token})
    for attempt in range(4):
        try:
            out = json.load(urllib.request.urlopen(req, context=CTX))
            if "errors" in out:
                raise RuntimeError(json.dumps(out["errors"]))
            return out["data"]
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 3:
                time.sleep(2 * (attempt + 1))
                continue
            raise


# ---------------------------------------------------------------- mutations

CANCEL = """
mutation Cancel($orderId: ID!, $reason: OrderCancelReason!, $refund: Boolean!,
                $restock: Boolean!, $notifyCustomer: Boolean, $staffNote: String) {
  orderCancel(orderId: $orderId, reason: $reason, refund: $refund, restock: $restock,
              notifyCustomer: $notifyCustomer, staffNote: $staffNote) {
    job { id done }
    orderCancelUserErrors { field message code }
  }
}"""

REFUND = """
mutation Refund($input: RefundInput!) {
  refundCreate(input: $input) {
    refund { id totalRefundedSet { shopMoney { amount currencyCode } } }
    userErrors { field message }
  }
}"""

HOLD = """
mutation Hold($fulfillmentOrderHold: FulfillmentOrderHoldInput!, $id: ID!) {
  fulfillmentOrderHold(fulfillmentOrderHold: $fulfillmentOrderHold, id: $id) {
    fulfillmentOrder { id status }
    userErrors { field message }
  }
}"""

VERIFY = """
query Verify($id: ID!) {
  order(id: $id) {
    name
    cancelledAt
    displayFinancialStatus
    displayFulfillmentStatus
    totalRefundedSet { shopMoney { amount } }
  }
}"""

STAFF_NOTE = "Bow Tote discontinued 2026-07-25 - manufacturer capacity shortfall. Customer emailed by founder before refund."


# ---------------------------------------------------------------- runners

def do_cohort_a(store, token, orders, apply_):
    print(f"\n{'='*78}\nCOHORT A - full cancel + refund ({len(orders)} orders)\n{'='*78}")
    total = 0.0
    for o in orders:
        total += float(o["refund"])
        label = f"  {o['name']:<8} {o['first_name']:<10} ${o['refund']:>7}  {'+'.join(o['variants'])}"
        if not apply_:
            print(f"{label}   [dry run]")
            continue
        data = gql(store, token, CANCEL, {
            "orderId": o["order_id"], "reason": "OTHER", "refund": True,
            "restock": False, "notifyCustomer": True, "staffNote": STAFF_NOTE})
        errs = data["orderCancel"]["orderCancelUserErrors"]
        if errs:
            print(f"{label}   FAILED: {errs}")
        else:
            print(f"{label}   cancelled (job {data['orderCancel']['job']['id'].split('/')[-1]})")
        time.sleep(0.6)
    print(f"  {'-'*72}\n  cohort A total: ${total:,.2f}")
    return total


def do_cohort_b(store, token, orders, apply_):
    print(f"\n{'='*78}\nCOHORT B - Bow Tote line refund only, rest of order untouched ({len(orders)} orders)\n{'='*78}")
    total = 0.0
    for o in orders:
        total += float(o["suggested_refund"])
        label = (f"  {o['name']:<8} {o['first_name']:<10} ${o['suggested_refund']:>7}"
                 f"  {o['bow_variant']:<6} (sticker ${o['sticker_price']})")
        if not apply_:
            print(f"{label}   [dry run]")
            print(f"           keeps: {o['other_lines']}")
            continue
        data = gql(store, token, REFUND, {"input": {
            "orderId": o["order_id"],
            "note": STAFF_NOTE,
            "notify": True,
            "refundLineItems": [{
                "lineItemId": o["bow_line_item_id"],
                "quantity": 1,
                "restockType": "NO_RESTOCK",
            }],
            "transactions": [{
                "orderId": o["order_id"],
                "parentId": o["parent_transaction_id"],
                "amount": o["suggested_refund"],
                "kind": "REFUND",
                "gateway": "shopify_payments",
            }],
        }})
        errs = data["refundCreate"]["userErrors"]
        if errs:
            print(f"{label}   REFUND FAILED: {errs}")
            continue
        got = data["refundCreate"]["refund"]["totalRefundedSet"]["shopMoney"]["amount"]
        print(f"{label}   refunded ${got}")

        # Stop SDH from fake-shipping the leftover line and firing another tracking email.
        h = gql(store, token, HOLD, {
            "id": o["fulfillment_order_id"],
            "fulfillmentOrderHold": {
                "reason": "OTHER",
                "reasonNotes": "Bow Tote discontinued and refunded - do not fulfil.",
                "notifyMerchant": False,
                "fulfillmentOrderLineItems": [{
                    "id": o["bow_line_item_id"], "quantity": 1,
                }],
            }})
        herrs = h["fulfillmentOrderHold"]["userErrors"]
        print(f"           hold: {'OK' if not herrs else herrs}")
        time.sleep(0.6)
    print(f"  {'-'*72}\n  cohort B total: ${total:,.2f}")
    return total


def verify(store, token, all_orders):
    print(f"\n{'='*78}\nVERIFY\n{'='*78}")
    for o in all_orders:
        d = gql(store, token, VERIFY, {"id": o["order_id"]})["order"]
        print(f"  {d['name']:<8} cancelled={str(bool(d['cancelledAt'])):<5} "
              f"{d['displayFinancialStatus']:<18} refunded=${d['totalRefundedSet']['shopMoney']['amount']}")
        time.sleep(0.3)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="actually write (default: dry run)")
    ap.add_argument("--cohort", choices=["a", "b", "both"], default="both")
    ap.add_argument("--only", help="comma-separated order names, e.g. '#30388,#30392'")
    ap.add_argument("--verify-only", action="store_true")
    args = ap.parse_args()

    m = json.loads(MANIFEST.read_text())
    a = m["cohort_a"]["orders"]
    b = m["cohort_b"]["orders"]

    if args.only:
        keep = {s.strip() for s in args.only.split(",")}
        a = [o for o in a if o["name"] in keep]
        b = [o for o in b if o["name"] in keep]

    env = load_env()
    store, token = get_token(env)
    print(f"store: {store}   mode: {'APPLY (writes are real)' if args.apply else 'DRY RUN'}")

    if args.verify_only:
        verify(store, token, a + b)
        return

    if not args.apply:
        print("\n  Nothing will be written. Re-run with --apply once E1-A/E1-B have sent.")

    total = 0.0
    if args.cohort in ("a", "both"):
        total += do_cohort_a(store, token, a, args.apply)
    if args.cohort in ("b", "both"):
        total += do_cohort_b(store, token, b, args.apply)

    print(f"\n{'='*78}\nGRAND TOTAL: ${total:,.2f} across {len(a) + len(b)} orders\n{'='*78}")

    if args.apply:
        print("\nWaiting 8s for cancel jobs to settle, then verifying...")
        time.sleep(8)
        verify(store, token, a + b)


if __name__ == "__main__":
    sys.exit(main())
