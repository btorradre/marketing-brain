---
name: restock-watch
description: Velantra restock watch — checks every SKU for whether a purchase order is due and whether the agent has quietly run out of stock. Runs automatically every Monday 08:47 via LaunchAgent, and on demand here. Trigger on "restock check", "do I need to reorder", "am I about to run out", "check stock", "restock watch", or after Brooks places a PO with the agent.
---

# Restock watch

## Run it

```bash
cd "/Users/brooksorradre2/Documents/marketing brain/_engine/restock"
SSL_CERT_FILE=$(python3 -m certifi) python3 restock_check.py
```

Prints the brief, writes it to `reports/YYYY-MM-DD.md` and `reports/latest.md`, and fires a
macOS notification. Read the output and relay the alerts to Brooks in plain language — do not
just paste the table. Lead with what he has to *do* today.

## After Brooks places a PO

This is the one piece of maintenance and it matters. Edit
`_engine/restock/products.json` and set that SKU's `last_po`:

```json
"last_po": { "date": "2026-08-11", "units": 1800, "note": "placed with agent via WeChat" }
```

Until `last_po` is set for a SKU, the cover alarm cannot run for it and the report says so
under "Needs setup". The stall alarm works regardless.

## What it actually measures

Two independent alarms, because the June 2026 Sofia stockout tripped both and nothing caught it.

**COVER** — units left (last PO minus units sold since that PO) ÷ current velocity. Shopify
inventory is untracked on this store and reads negative store-wide, so on-hand has to be
inferred this way. RED when cover is inside the lead time, AMBER when inside lead time +
safety.

**STALL** — the share of labels created 5-10 days ago that still have no carrier scan.
Deliberately *not* a median gap: an unscanned label is right-censored data, so a median of
what has moved reads healthy while the queue behind it sits. Healthy SKUs run 10-25%. The
Sofia hit 93%. RED at 60%, AMBER at 40%.

The stall alarm exists because the agent issues tracking numbers before the parcel exists.
Shopify's own "processing time" therefore reads ~0.4 days on every product in every month,
including the two months the Sofia was completely out of stock. It is not a usable signal
and should never be quoted.

## Lead times (Brooks, 2026-08-08)

| SKU | Lead time | Why it matters |
|---|---|---|
| Eleanor Weekender | 40 days | Longest lead, fastest growth. Highest risk in the catalog. |
| Sofia Woven Tote | 20 days | Already cost 4.0% refunds and two months of delays in 2026. |
| Margot Leather Tote | 20 days | Low volume, low absolute exposure. |
| Camille Boat Tote | 7 days | Forgiving. Lowest risk. |

## Schedule

LaunchAgent `com.brooks.velantra-restock`, Mondays 08:47 local (mid-afternoon in Guangzhou, so
a message sent on the alert gets answered the same day).

```bash
launchctl list | grep velantra-restock          # is it loaded
launchctl start com.brooks.velantra-restock     # force a run now
tail -50 "/Users/brooksorradre2/Documents/marketing brain/_engine/restock/logs/$(date +%F).log"
```

Plist at `~/Library/LaunchAgents/com.brooks.velantra-restock.plist`. To change the day or time,
edit `StartCalendarInterval` then `launchctl unload` + `load`.

## Context

Built alongside the private-agent vs Ecomflow analysis (2026-08-08). The conclusion of that
analysis was that the agent's fulfillment is fine — 1.2 to 4.2 day handovers, every month —
and that the Sofia collapse was an inventory-planning failure worth ~$155k/yr less than
switching 3PLs. This automation is the fix that analysis called for.
