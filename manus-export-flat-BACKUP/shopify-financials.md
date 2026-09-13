# Shopify Financials — P&L System

This skill produces two kinds of financial workbooks for a portfolio of Shopify stores (grouped into brands): a **month-by-month P&L** (months as columns, full financial statement, blended across all stores) and a **single-period deep-dive** (a point-in-time close snapshot covering holds, stuck payouts, and reserves). It also defines a repeatable pipeline for importing bank/card expense data (pulled by a separate AI assistant, e.g. ChatGPT, from bank connections or statements) and merging it into the P&L below gross profit. Use this whenever someone wants to pull financials, run a monthly or quarterly P&L, build a month-by-month P&L, import expenses, add a new Shopify store's credentials, or asks "how much did we make," "run the financials," "pull the numbers," "build the P&L," or "import my expenses."

## How to use this

### Month-by-month P&L (primary flow)

1. For each Shopify store in the portfolio, authenticate against its Admin API (see Auth section below) and pull orders, refunds, disputes, balance transactions, and product cost-per-item data for the requested date range.
2. Group stores into brands (a `group` concept — e.g. four different store instances that all roll up to one brand) so the report can show both per-brand and consolidated numbers.
3. Compute revenue, COGS, fees, chargebacks, and other metrics using the formulas in the Methodology section below, bucketed by month.
4. Merge in the expense ledger (bank/card data imported via the ChatGPT interop pipeline) if available, unless the user explicitly wants Shopify-only numbers.
5. For any month with no imported expense data, apply an "estimated fill" (see below) rather than showing an artificially inflated profit margin.
6. Assemble the output as a spreadsheet with, at minimum: a consolidated P&L tab, a brand net-sales grid, per-brand contribution P&L tabs, an imported-expense detail tab, a data-quality tab (flagging estimates and low-coverage months), and a methodology tab.
7. Save the workbook and report back: the file location, consolidated net sales / gross profit / net profit for the latest full month, and any data-quality flags (low COGS coverage, months missing expense data).

Useful date-range presets to support: full calendar year to date (Jan through current month, with the last column marked "MTD"), a trailing N months, or an explicit since/until range. Support a "rebuild from cached data, no new API calls" mode for iterating on formatting without re-pulling.

**COGS basis** — there are three ways to compute cost of goods sold; pick one explicitly and document it on the workbook:
- **Hybrid (recommended default)**: use Shopify's cost-per-item field, grossed up to 100% coverage where some SKUs are missing cost data, and for any store-month with no cost data at all, estimate using the blended cost ratio of the stores that do have data. Every estimate must be itemized on the Data Quality tab, cross-checked against actual supplier wire payments where available.
- **Cash basis**: book supplier wire payments as COGS in the month paid.
- **Shopify basis**: raw accrual — Shopify's cost-per-item times units sold, no estimation, no supplier-wire cross-check.

**Manual store entries**: some older store instances may no longer have a working API connection but still need historical figures represented (e.g. a discontinued store that did a known ~$90K net in a given month, entered by hand from other records). Keep a small manual-entry table for this, merge it in at build time, and flag every manual figure clearly on the Data Quality tab. Never let a manual entry silently become part of the "live" cached dataset.

**Estimated fills** (on by default, should be possible to disable): for any month with no imported bank/expense data, don't just show revenue with zero expenses — that inflates margins misleadingly. Instead, fill in:
- An estimated ad-spend figure = that month's net revenue × the blended "ad spend as % of net revenue" (aMER) of the months that do have complete data.
- An estimated recurring-overhead figure = the average of each expense category from complete months, minus whatever actuals were recorded for that month.
Mark these rows visibly (e.g. red/flagged) on the P&L and itemize them on the Data Quality tab. As soon as a real bank export for that month is imported, the estimate should be automatically superseded.

**Reporting preference**: default to blended/consolidated reporting rather than granular per-brand expense attribution, unless asked otherwise. Headline metrics to always surface: total revenue, total expenses, total ad spend, ROAS/marketing efficiency, and total chargeback expense (dispute fees + lost chargebacks + any chargeback-management service fees).

### ChatGPT expense interop (bank side of the P&L)

The P&L merges two data sources:

| Side | Who pulls it | How it enters the P&L |
|---|---|---|
| Shopify (revenue, COGS, fees, chargebacks) | Pulled directly from each store's Admin API | Computed live per the formulas below |
| Bank/expenses (ad spend, 3PL, software, payroll, etc.) | Pulled by a separate assistant (e.g. ChatGPT) from bank/card connections or statements | Exported as a CSV/JSON file, imported into a persistent ledger, then merged automatically |

The monthly close loop:

1. Have the bank-data assistant export transactions using the exact prompt and schema in the Templates section below.
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

### Auth — connecting a new store

Each Shopify store needs either (a) a client ID + client secret (a client-credentials flow, minting a fresh token per run) or (b) a permanent admin access token. Store these credentials somewhere private, never in output files. When a store owner completes an OAuth-style authorization flow and hands you a "post-auth code," that code is **single-use and expires within minutes** — exchange it for a permanent admin token immediately, do not queue it up. When adding a store, group it under its parent brand name if it's one of several store instances that should roll up together in reporting.

### Single-period deep-dive

For a snapshot as of a specific point in time (a common use: closing out last month, or checking mid-transit money), pull the same data but present it differently — organized around close-related concerns: by-brand summary, cost breakdown, chargebacks, holds & payouts, stuck payouts, a full P&L codex, mini per-brand P&Ls, and a methodology tab. Confirm the requested period with the user first; default to the last full calendar month if unspecified.

## Rules & standards

- **Orders API pagination/scope**: to see orders older than roughly 60 days, the API connection needs the broadest possible order-read scope. If a newly connected store can't see older orders, this scope is the first thing to check.
- **Net sales = current subtotal price** (i.e., the subtotal after discounts and after refunds/returns/edits are already netted in). Never subtract refunds again on top of this figure — that would double-count them.
- **Chargebacks are NOT part of order revenue.** A lost chargeback is booked once, as its own P&L expense line, dated by the dispute's initiation date — not by subtracting it from revenue.
- **Monthly bucketing is accrual by order-creation month** for revenue; fees are bucketed by their processing date; a refund issued in a later month against an earlier order still counts toward the *order's* original month, not the refund's month.
- **COGS coverage matters.** Flag any store-month where cost-per-item data covers under 50% of units sold — in red, on the Data Quality tab. The fix is entering/backfilling cost-per-item in the store's product catalog, then re-pulling live (a from-cache rebuild will not pick up product-catalog changes made after the cache was built).
- **Reserves/holds are point-in-time only** — they belong in the single-period deep-dive, not the month-by-month P&L, since a "reserve" is a snapshot concept, not a monthly flow.
- Import validation for expenses should be all-or-nothing: if any row has an unrecognized category or a malformed date/amount, reject the entire import with row-numbered errors rather than silently skipping bad rows.

## Templates & examples

### Methodology & formulas

**Revenue**
- Gross Sales = sum of line-item prices before discounts (pre-discount product revenue, excluding shipping/tax).
- Discounts = sum of total discounts applied.
- Net Sales = sum of the order's current subtotal price (product revenue after discounts AND refunds/returns/edits). **This is the topline metric.**
- Returns/Refunds (product) = Gross − Discounts − Net Sales (derived, not pulled directly).
- Shipping = current total price − net sales − tax − tips (net of any shipping refunds).
- Total Collected = sum of current total price (i.e., after refunds).
- Test orders should be excluded; include all order statuses (refunded/cancelled included) when pulling, then let the formulas net things out correctly.

**COGS**
- Build a cost map from each product variant's per-unit cost (paginate through the full catalog).
- Units = per-variant (units sold − units refunded), from order line items plus refund line items.
- COGS = sum over variants of (net units × unit cost).
- Coverage = costed units ÷ (costed + uncosted) units. Anything under 100% means COGS is understated by that gap.

**Payment fees** (from balance/transaction records)
- Processing fees = sum of fees on standard charge transactions.
- Dispute fees = sum of fees on dispute-type transactions (the flat per-chargeback fee, net of any reversal when a dispute is won).

**Chargebacks** (from the disputes data, bucketed by the dispute's initiation date within the period)
- Lost = statuses meaning the merchant lost the dispute or the charge was refunded as a result.
- Won = statuses meaning the merchant won.
- Open = everything still pending.
- Lost chargebacks are booked as a P&L expense; order revenue itself is not reversed because of a chargeback.

**Refunds**
- Sum of refund transaction amounts (refund-kind transactions) on orders created within the period. This is already inside Net Sales — treat as a memo line only, never subtract it a second time.

**Holds / payouts / reserves** (point-in-time only)
- Available balance = current balance after chargebacks.
- Reserve = absolute value of the sum of reserved-funds/reserve-type balance transactions. Note: some admin-initiated review holds may not be visible via API at all.
- Stuck payouts = any payout with a status other than "paid" (failed/canceled/scheduled). Failed or canceled payout funds return to the available balance — don't double-count them as still "stuck."
- Track the last successful payout date and flag accounts where it's been unusually long, since that often signals a frozen or failing payment account.

**P&L treatment**
- Tax collected is a passthrough liability — exclude it from profit calculations entirely.
- Net Sales is the profit basis. Refunds are already netted into it; chargebacks-lost and fees are each booked exactly once.

### Expense-export prompt (paste into a bank-data assistant like ChatGPT)

```
You are exporting my business bank/credit-card transactions for my P&L system.

Output ONLY a CSV code block with this exact header, one row per transaction:

date,description,amount,category,brand,source

Rules:
- date: YYYY-MM-DD (transaction date).
- description: merchant + short memo. No commas — replace with ";".
- amount: positive number = money OUT (expense). Use a NEGATIVE number only
  for a refund/credit against an expense. For category other_income,
  positive = money IN.
- category: EXACTLY one of:
    other_income          (non-Shopify income: affiliate payouts, rebates)
    fulfillment_3pl       (3PL, pick-pack, warehouse)
    freight_duties        (inbound freight, customs, duties)
    ad_spend_meta         (Facebook/Instagram ads)
    ad_spend_google       (Google/YouTube ads)
    ad_spend_tiktok       (TikTok ads)
    ad_spend_other        (any other ad platform, influencers, affiliates as media)
    shipping_postage      (outbound labels/postage billed directly, e.g. Shippo, USPS)
    software_saas         (apps, tools, subscriptions)
    contractors_agency    (freelancers, VAs, agencies, editors)
    payroll               (W2 wages + payroll fees)
    merchant_fees         (bank/wire/Stripe/PayPal fees — NOT the store platform's own fees)
    chargeback_services   (a chargeback-management service, e.g. Disputifier/Chargeflow)
    legal_professional    (legal, accounting, bookkeeping)
    taxes_gov             (government fees, franchise tax, filing fees)
    interest_expense      (loan/card interest ONLY)
    travel                (flights, hotels, rideshare, gas, parking)
    meals_entertainment   (restaurants, delivery, coffee)
    office_misc           (office, supplies, small misc)
    other_opex            (anything operational that fits nowhere else)
    inventory_purchase    (payments to product manufacturers/suppliers)
    owner_draw            (transfers to my personal accounts)
    transfer              (transfers between my own business accounts)
    cc_payment            (credit-card bill payments — the card's own transactions are booked individually)
    loan_principal        (loan principal repayment; split interest into interest_expense)
- brand: the brand name when the charge clearly belongs to one brand (e.g. an ad
  account or 3PL invoice for that brand). Leave blank if company-wide or unclear.
- source: short account tag, e.g. chase_checking, amex_plat, mercury.
- EVERY transaction must appear exactly once. Do not net, merge, or summarize rows.
- Do not skip transactions you can't categorize — use other_opex and keep the description.
- Categorize payout DEPOSITS from the sales platform as: transfer (revenue is tracked separately elsewhere).
- Money movement between my own accounts is ALWAYS transfer, never income or expense.
- Venmo/Wise transfers and bank wires TO INDIVIDUALS from business accounts are
  contractors_agency (freelancer payments) unless clearly personal.
- Chargeback-service charges are chargeback_services, not software.
```

JSON is also an acceptable import format — a list of objects with the same keys, or `{"entries": [...]}`.
</content>
