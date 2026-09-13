# Velantra restock watch — 2026-08-08

## Ask the agent to restock today

**The Eleanor Weekender** — 18.0 units/day, 40-day lead time
- 79% of week-old parcels have still never scanned with the carrier, against a 20% healthy baseline (n=100). Tracking numbers are being issued for parcels that do not exist. This is what a stockout looks like before anyone tells you — ask the agent for on-hand units today.
- Suggested PO size: **1,800 units** (two lead-time cycles plus safety).

**The Sofia Woven Tote** — 29.0 units/day, 20-day lead time
- 93% of week-old parcels have still never scanned with the carrier, against a 15% healthy baseline (n=27). Tracking numbers are being issued for parcels that do not exist. This is what a stockout looks like before anyone tells you — ask the agent for on-hand units today.
- Suggested PO size: **1,449 units** (two lead-time cycles plus safety).

## All SKUs

| Product | Units/day | Lead | Est. left | Days cover | Reorder by | Week-old parcels not scanned | Healthy | Median scan gap |
|---|---|---|---|---|---|---|---|---|
| The Eleanor Weekender | 18.0 | 40d | — | — | — | 79% (n=100) | 20% | 1.6d |
| The Sofia Woven Tote | 29.0 | 20d | — | — | — | 93% (n=27) | 15% | 28.2d |
| The Margot Leather Tote | 1.5 | 20d | — | — | — | n=7, too few | 10% | 1.4d |
| The Camille Boat Tote | 12.7 | 7d | — | — | — | 20% (n=15) | 20% | 3.8d |

## Needs setup

- **The Eleanor Weekender** — no PO on record. Add `last_po` (date + units) to `_engine/restock/products.json`.
- **The Sofia Woven Tote** — no PO on record. Add `last_po` (date + units) to `_engine/restock/products.json`.
- **The Margot Leather Tote** — no PO on record. Add `last_po` (date + units) to `_engine/restock/products.json`.
- **The Camille Boat Tote** — no PO on record. Add `last_po` (date + units) to `_engine/restock/products.json`.

---
Cover is estimated as (units on the last PO − units sold since that PO) ÷ current velocity, because Shopify inventory is untracked on this store. Update `last_po` in `products.json` every time you order and this stays honest.

Label→scan is the real prep time. Shopify's own processing time reads ~0.4 days on everything because the agent issues tracking numbers before the parcel exists.