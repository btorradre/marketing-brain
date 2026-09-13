# Velantra <> Supplier — Lead Times & Processing Times (built 2026-08-10)

Live sheet: https://docs.google.com/spreadsheets/d/1Ct5PM4smZnJ-u_67Udgly7DKD6gmQ2Vc0mdrzRHw75o/edit

Bilingual (EN / 简体中文) template for the sourcing agent to fill in. Created in Brooks's
Drive via `auth/bto-ec-google-auth/token.json`. **Not shared with anyone yet** — share as
Editor from the Sheets UI.

## Tabs

| Tab | Rows | Who fills it |
|---|---|---|
| `START HERE 开始` | — | Instructions + sign-off block (supplier signs) |
| `Lead Times 交期` | 11 products | Supplier — the heavy tab, 12 columns |
| `Stock by SKU 库存` | 62 colorways | Supplier — light, 6 columns |
| `Definitions 说明` | — | Reference. Timeline diagram + column glossary |
| `Lists` | — | Hidden. Dropdown validation source |

Split deliberately: lead times and MOQ are per-product, so asking for them 62 times
guarantees a half-finished sheet. Per-colorway asks are cut down to stock status,
units on hand, ready date, processing time.

## Build

Source of truth for the row set is `../ecomflow-3pl/velantra_sku_list.csv` (62 SKUs,
11 hero products, pulled from Shopify 2026-08-06).

```
SSL_CERT_FILE=$(python3 -m certifi) python3 brands/velantra/_shared/supplier-leadtimes/build_supplier_sheet.py
```

Re-running creates a **new** spreadsheet every time — it does not update the existing one.
Trash the old one if you rebuild.

## Deliberate choices

**Previously quoted lead times are NOT prefilled.** `_engine/restock/products.json` already
carries agent-quoted figures — Camille 7d, Sofia 20d, Margot 20d, Eleanor 40d. Showing them
in the supplier's sheet invites copy-paste. Left blank so the answers are independent and can
be compared against the record as an audit.

**Unit cost is not a column.** Keeps the sheet focused and stops the agent stalling on it.

**The processing-time definition is written to close the stall loophole.** The `Definitions`
tab states that processing time ends at a physical carrier scan, not at tracking-number
creation. That is the exact behaviour that hit 93% on the Sofia in Aug 2026 while Shopify's
processing time still read 0.4 days (see `_engine/restock/products.json` → `baseline_stall_pct`).

**Protection is `warningOnly`.** The supplier is an Editor, so hard protection would lock
them out too. Velantra columns and the auto-TOTAL column warn on edit.

## Feeds

`Lead Times 交期` column H (production 100u) is the number that should be written back into
`_engine/restock/products.json` → `lead_time_days` for the restock watcher, once the agent
returns real figures.

## Other brands

Motilli / Lunessa run through a different (supplement) supplier and have no locked SKU list
yet. To clone this for them, build the equivalent of `velantra_sku_list.csv` first, then
point `SKU_CSV` in the build script at it.
