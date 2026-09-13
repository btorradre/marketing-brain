# Inventory Restock Watch Methodology

This document describes a two-alarm inventory monitoring methodology for a direct-to-consumer store where the platform's own inventory tracking cannot be trusted (e.g. inventory is untracked/negative store-wide) and fulfillment happens through an outsourced logistics agent. Use this as a template for building a restock-monitoring check for any product catalog with similar characteristics: unreliable on-platform inventory counts, variable supplier lead times, and a fulfillment partner that can issue tracking numbers before a parcel physically exists.

## Purpose

Check every SKU for two independent things: whether a new purchase order is due soon, and whether the fulfillment pipeline has quietly stalled (a sign of an undetected stockout). Both alarms were designed after a real stockout that neither a simple "days of inventory" calculation nor a naive shipping-time metric caught.

## The two alarms

**COVER** — estimated units remaining, divided by current sell-through velocity, expressed as days of cover. Since on-platform inventory tracking may not be trustworthy, infer units remaining as: (units received in the last confirmed purchase order) minus (units sold since that PO was placed). Flag RED when days of cover falls inside the supplier's lead time (you'll run out before a new order can arrive even if placed today). Flag AMBER when cover falls inside lead time plus a safety margin.

**STALL** — the share of shipping labels created 5-10 days ago that still show no carrier scan (i.e., a label exists but the physical parcel apparently doesn't yet, or hasn't moved). This is deliberately NOT a median processing-time metric: an unscanned label is right-censored data — a median of only the labels that HAVE moved will read healthy even while a growing backlog of stuck labels sits behind it, invisible to that median. In the real incident this methodology was built to catch, one SKU's stall rate hit 93% while a naive processing-time metric kept reporting sub-1-day averages the entire time, because it only measured labels that had actually shipped. Flag RED at 60% stall rate, AMBER at 40%. Healthy SKUs typically run 10-25%.

**Why STALL matters even when a fulfillment partner's own metrics look fine:** if a fulfillment agent issues tracking numbers before the parcel physically exists (which happens with some overseas fulfillment models), the agent's own "processing time" statistic will look artificially fast (e.g. reading well under a day) even during a period when a product is completely out of stock — because label creation isn't gated on actual stock. Don't trust a fulfillment partner's self-reported processing-time metric as evidence a SKU has real inventory; measure the scan-to-label ratio yourself instead.

## Setup / maintenance requirement

Each SKU needs its last confirmed purchase order recorded (date, units, any note) for the COVER alarm to function at all — until that's set for a SKU, COVER can't run for it and should be reported as "needs setup." The STALL alarm works regardless, since it only depends on label/scan data.

Whenever a new purchase order is placed, update that SKU's "last PO" record immediately — this is the one piece of ongoing maintenance the system needs, and it directly determines whether COVER stays accurate.

## Example lead-time table (illustrative — replace with your own SKUs)

| SKU | Lead time | Why it matters |
|---|---|---|
| Product A | 40 days | Longest lead time, fastest sales growth — highest risk in the catalog. |
| Product B | 20 days | Already cost real refunds and shipping delays once. |
| Product C | 20 days | Lower volume, lower absolute exposure even with the same lead time. |
| Product D | 7 days | Short and forgiving. Lowest risk. |

## How to build this

1. Maintain a small structured record per SKU: current velocity (units/day, trailing window), last confirmed PO (date + units), and supplier lead time in days.
2. Compute COVER: `(last_po_units - units_sold_since_po) / current_velocity` = days of cover remaining. Compare to lead time (RED) and lead time + safety margin (AMBER).
3. Compute STALL: for labels created 5-10 days ago, what fraction still show no carrier scan event? Compare to the 60%/40% thresholds.
4. Run the check on a recurring schedule (daily or weekly, timed so an alert reaches whoever needs to act while they can still act same-day — e.g. if placing orders with an overseas supplier, time the check for their business hours).
5. Report both alarms per SKU in plain language, leading with what the reader needs to DO today, not a raw data table.
6. Log each run's report to a dated file/record so history is preserved and comparable over time.

## Context worth carrying into any similar build

This methodology is only worth building when a preceding investigation has shown that (a) fulfillment execution itself is generally fine and (b) the actual recurring loss driver is inventory-planning blindness, not the fulfillment partner's competence. In the case this was built for, an analysis found fulfillment handovers were consistently fast (1.2-4.2 days every month) and that a single stockout, caused purely by an inventory-planning gap, cost far more than switching fulfillment partners would have saved. Build the monitoring fix, not a vendor-switch, when that's the actual failure mode.
