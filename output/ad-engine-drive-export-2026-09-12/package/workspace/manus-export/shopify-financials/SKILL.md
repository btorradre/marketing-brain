---
name: shopify-financials
description: Produces two kinds of financial workbooks for a portfolio of Shopify stores grouped into brands — a month-by-month P&L (months as columns, full financial statement, blended across all stores) and a single-period deep-dive (a point-in-time close snapshot covering holds, stuck payouts, and reserves). Also defines a repeatable pipeline for importing bank/card expense data pulled by a separate assistant and merging it into the P&L below gross profit. Use whenever someone wants to pull financials, run a monthly or quarterly P&L, build a month-by-month P&L, import expenses, add a new Shopify store's credentials, or asks "how much did we make," "run the financials," "pull the numbers," "build the P&L," or "import my expenses."
---

# Shopify Financials — P&L System

Two report modes, plus a bank-expense import pipeline and Shopify auth management:

| Mode | What it produces |
|---|---|
| **Month-by-month P&L** (primary flow) | Months-as-columns workbook: consolidated P&L, brand net-sales grid, per-brand contribution P&Ls, imported-expense detail, data-quality tab, methodology tab |
| **Single-period deep-dive** | A point-in-time close snapshot: by-brand summary, cost breakdown, chargebacks, holds & payouts, stuck payouts, full P&L codex, mini per-brand P&Ls, methodology tab |

For the full formulas behind every line item, and the exact bank-expense export prompt/schema, see `references/methodology-and-templates.md` — read it before computing any number or running an expense import.

## Month-by-month P&L (primary flow)

1. For each Shopify store in the portfolio, authenticate against its Admin API (see Auth below) and pull orders, refunds, disputes, balance transactions, and product cost-per-item data for the requested date range.
2. Group stores into brands (a `group` concept — e.g. four different store instances that all roll up to one brand) so the report can show both per-brand and consolidated numbers.
3. Compute revenue, COGS, fees, chargebacks, and other metrics using the formulas in `references/methodology-and-templates.md`, bucketed by month.
4. Merge in the expense ledger (bank/card data imported via the expense-interop pipeline) if available, unless the user explicitly wants Shopify-only numbers.
5. For any month with no imported expense data, apply an "estimated fill" (see below) rather than showing an artificially inflated profit margin.
6. Assemble the output as a spreadsheet with, at minimum: a consolidated P&L tab, a brand net-sales grid, per-brand contribution P&L tabs, an imported-expense detail tab, a data-quality tab (flagging estimates and low-coverage months), and a methodology tab.
7. Save the workbook and report back: the file location, consolidated net sales / gross profit / net profit for the latest full month, and any data-quality flags (low COGS coverage, months missing expense data).

Useful date-range presets to support: full calendar year to date (Jan through current month, with the last column marked "MTD"), a trailing N months, or an explicit since/until range. Support a "rebuild from cached data, no new API calls" mode for iterating on formatting without re-pulling.

**COGS basis** — there are three ways to compute cost of goods sold; pick one explicitly and document it on the workbook:
- **Hybrid (recommended default)**: use Shopify's cost-per-item field, grossed up to 100% coverage where some SKUs are missing cost data, and for any store-month with no cost data at all, estimate using the blended cost ratio of the stores that do have data. Every estimate must be itemized on the Data Quality tab, cross-checked against actual supplier wire payments where available.
- **Cash basis**: book supplier wire payments as COGS in the month paid.
- **Shopify basis**: raw accrual — Shopify's cost-per-item times units sold, no estimation, no supplier-wire cross-check.

**Manual store entries**: some older store instances may no longer have a working API connection but still need historical figures represented (e.g. a discontinued store with a known net revenue for a given month, entered by hand from other records). Keep a small manual-entry table for this, merge it in at build time, and flag every manual figure clearly on the Data Quality tab. Never let a manual entry silently become part of the "live" cached dataset.

**Estimated fills** (on by default, should be possible to disable): for any month with no imported bank/expense data, don't just show revenue with zero expenses — that inflates margins misleadingly. Instead, fill in:
- An estimated ad-spend figure = that month's net revenue × the blended "ad spend as % of net revenue" (aMER) of the months that do have complete data.
- An estimated recurring-overhead figure = the average of each expense category from complete months, minus whatever actuals were recorded for that month.

Mark these rows visibly (e.g. red/flagged) on the P&L and itemize them on the Data Quality tab. As soon as a real bank export for that month is imported, the estimate should be automatically superseded.

**Reporting preference**: default to blended/consolidated reporting rather than granular per-brand expense attribution, unless asked otherwise. Headline metrics to always surface: total revenue, total expenses, total ad spend, ROAS/marketing efficiency, and total chargeback expense (dispute fees + lost chargebacks + any chargeback-management service fees).

## Bank/expense interop (the other side of the P&L)

The P&L merges two data sources:

| Side | Who pulls it | How it enters the P&L |
|---|---|---|
| Shopify (revenue, COGS, fees, chargebacks) | Pulled directly from each store's Admin API | Computed live per the formulas in `references/methodology-and-templates.md` |
| Bank/expenses (ad spend, 3PL, software, payroll, etc.) | Pulled by a separate assistant from bank/card connections or statements | Exported as a CSV/JSON file, imported into a persistent ledger, then merged automatically |

The monthly close loop:

1. Have the bank-data assistant export transactions using the exact prompt and schema in `references/methodology-and-templates.md`.
2. Save the resulting file and import it into the expense ledger, always replacing (not stacking on top of) any previously-imported data for the same month(s) when re-importing — otherwise edited/corrected rows will double up alongside the old versions. Exact-duplicate rows are deduplicated by content hash automatically, but a *changed* row (same date/merchant but edited amount or description) will NOT be caught by dedup and must be handled with an explicit "replace this month" import.
3. Rebuild the P&L so the newly imported expenses flow in.
4. Optionally, hand Shopify-side numbers back to the bank-data assistant as a JSON export if you want it to cross-check or build its own view.

Where each expense category lands on the P&L:
- `other_income` → Revenue section (below Net Sales).
- `fulfillment_3pl`, `freight_duties` → COGS section.
- All `ad_spend_*` categories plus the general operating categories → Operating Expenses.
- `inventory_purchase` → under cash-basis COGS, this becomes actual product COGS (booked in the month the supplier wire was paid). Under Shopify-basis COGS, this category is memo-only and excluded from the P&L math, because Shopify's cost-per-item field is already accruing product COGS — counting both would double-count.
- `owner_draw`, `transfer`, `cc_payment`, `loan_principal` → memo only, excluded from profit calculations entirely (these are not operating expenses).
- Brand-tagged rows also flow into that brand's individual contribution P&L tab; untagged rows appear only on the consolidated tab.

## Auth — connecting a new store

Each Shopify store needs either (a) a client ID + client secret (a client-credentials flow, minting a fresh token per run) or (b) a permanent admin access token. Store these credentials somewhere private, never in output files. When a store owner completes an OAuth-style authorization flow and hands you a "post-auth code," that code is **single-use and expires within minutes** — exchange it for a permanent admin token immediately, do not queue it up. When adding a store, group it under its parent brand name if it's one of several store instances that should roll up together in reporting.

## Single-period deep-dive

For a snapshot as of a specific point in time (a common use: closing out last month, or checking mid-transit money), pull the same data but present it differently — organized around close-related concerns: by-brand summary, cost breakdown, chargebacks, holds & payouts, stuck payouts, a full P&L codex, mini per-brand P&Ls, and a methodology tab. Confirm the requested period with the user first; default to the last full calendar month if unspecified.

## Rules & standards

- **Orders API pagination/scope**: to see orders older than roughly 60 days, the API connection needs the broadest possible order-read scope. If a newly connected store can't see older orders, this scope is the first thing to check.
- **Net sales = current subtotal price** (i.e., the subtotal after discounts and after refunds/returns/edits are already netted in). Never subtract refunds again on top of this figure — that would double-count them.
- **Chargebacks are NOT part of order revenue.** A lost chargeback is booked once, as its own P&L expense line, dated by the dispute's initiation date — not by subtracting it from revenue.
- **Monthly bucketing is accrual by order-creation month** for revenue; fees are bucketed by their processing date; a refund issued in a later month against an earlier order still counts toward the *order's* original month, not the refund's month.
- **COGS coverage matters.** Flag any store-month where cost-per-item data covers under 50% of units sold — in red, on the Data Quality tab. The fix is entering/backfilling cost-per-item in the store's product catalog, then re-pulling live (a from-cache rebuild will not pick up product-catalog changes made after the cache was built).
- **Reserves/holds are point-in-time only** — they belong in the single-period deep-dive, not the month-by-month P&L, since a "reserve" is a snapshot concept, not a monthly flow.
- Import validation for expenses should be all-or-nothing: if any row has an unrecognized category or a malformed date/amount, reject the entire import with row-numbered errors rather than silently skipping bad rows.

For the full revenue/COGS/fees/chargeback/refund/holds formulas and the exact bank-expense export prompt, see `references/methodology-and-templates.md`.
