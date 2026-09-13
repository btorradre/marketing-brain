---
name: shopify-financials
description: "Pull complete Shopify financials across all brand stores and build formatted Excel P&Ls — both a single-period 8-tab deep-dive AND a full month-by-month P&L that merges bank/expense data exported from ChatGPT. Pulls EVERYTHING: revenue (net sales, gross sales, discounts, returns), COGS from cost-per-item, payment processing fees, dispute/chargeback fees, chargebacks & refunds (lost/won/open), holds/payouts/reserves. Imports ChatGPT-exported bank/expense data (ad spend, 3PL, software, payroll, contractors) into a persistent ledger and folds it into the monthly P&L below gross profit. Manages Shopify auth: client-credentials per store plus exchanging post-auth authorization codes for permanent admin tokens. Use whenever the user wants to pull financials, run the monthly/quarterly P&L, build the month-by-month P&L, import expenses from ChatGPT/bank data, add a new Shopify store / exchange an auth code for an admin key, get revenue, chargebacks, refunds, reserves, COGS, fees, or payout/hold data, or asks 'how much did we make', 'run the financials', 'pull the numbers', 'build the P&L', 'import my expenses'."
---

# Shopify Financials — P&L System

Two report modes + a ChatGPT expense-import pipeline + Shopify auth management.

| Mode | Script | Output |
|---|---|---|
| **Month-by-month P&L** (the full financial statement) | `scripts/monthly_pl.py` | Months-as-columns workbook: consolidated P&L, brand net sales grid, brand contribution P&Ls, imported-expense detail, data quality, methodology |
| **Single-period deep-dive** (close snapshot: holds, stuck payouts, reserves) | `scripts/pull_financials.py` | Canonical 8-tab workbook (By Brand, Costs, Chargebacks, Holds & Payouts, Stuck Payouts, Full P&L Codex, Mini P&Ls, Methodology) |

## finance-agent (2026-09-02) — the categorization layer now lives upstream

The `finance-agent` skill (`../finance-agent/`) is the entry point for the monthly close. It ingests GPT 5.6 Sol's raw
bank exports, Apple Card PDFs and supplier bills into one transaction table, categorizes them (vendor rulebook →
hints → Claude → review queue) and **rebuilds `data/expenses.json`** before calling `monthly_pl.py`. Do not hand-import
into the ledger with `import_expenses.py` unless finance-agent is unavailable — the next `categorize.py` run overwrites it.
Taxonomy additions: every category has a `bucket` (marketing / ai / operating / cogs / excluded); new categories
`ai_tools`, `marketing_software`, `creators_influencers`; the workbook opens with an **Executive P&L** tab (bucket
rollup) and `monthly_pl.py` writes `data/executive.json` for the markdown/JSON report.

## Month-by-month P&L (primary flow)

```bash
cd "<this skill>/scripts"
python3 monthly_pl.py --year 2026                 # Jan..current month (last col = MTD)
python3 monthly_pl.py --months 6                  # trailing 6 months
python3 monthly_pl.py --since 2026-01 --until 2026-06
python3 monthly_pl.py --year 2026 --from-cache    # rebuild workbook, no API calls
python3 monthly_pl.py --year 2026 --chatgpt-export ~/shopify_monthly.json
```

- Saves workbook to `~/PL_Monthly_<since>_to_<until>.xlsx` (override `--out`; the user's convention is `marketing brain/finances/finalized statements/`) and the raw dataset to `data/monthly_shopify.json` (reused by `--from-cache`).
- Automatically merges the expense ledger (`data/expenses.json`) if present; `--no-expenses` skips it. Raw ChatGPT/bank exports live in `marketing brain/finances/raw expenses/`.
- **COGS basis**: `--cogs-basis hybrid` (default, the user's preference) uses Shopify cost-per-item grossed up to 100% coverage, and estimates store-months with no cost data (the Motilli stores) at the covered stores' blended cost ratio — every estimate is itemized on the Data Quality tab with a supplier-wire (Haikou Genyangkai) cross-check. `cash` books supplier wires as COGS; `shopify` is raw accrual.
- The user wants **blended/consolidated reporting only** — no per-brand expense attribution. Headline metrics: total revenue, total expenses, total ad spend, ROAS (Marketing Efficiency block), and TOTAL CHARGEBACK EXPENSE (dispute fees + lost + Disputifier, Chargeback Economics block).
- **Manual stores**: `data/manual_stores.json` holds per-month figures for dead stores whose API is gone (e.g. Motilli #2 March 2026 ≈ $90K net, user-estimated). Merged at build time, flagged [MANUAL ENTRY] on Data Quality, never written into the cache.
- **Estimated fills** (on by default; `--no-estimated-fill` disables): months with no imported bank data get an ad-spend fill (net × blended aMER of complete months) and a recurring-overhead fill (complete-month category averages minus recorded actuals) so profit margins aren't inflated by missing expenses. Red rows on the P&L, itemized on Data Quality, auto-replaced when the month's real bank export is imported.
- Relay to the user: workbook path, consolidated net sales / gross profit / net profit for the latest full month, and any Data Quality flags (low COGS coverage, months missing expense data).

## ChatGPT expense interop (bank side of the P&L)

The user pulls bank/card/expense data with **ChatGPT**, which exports a CSV/JSON in a fixed schema. Full schema, category chart, and the exact paste-into-ChatGPT prompt: **`references/chatgpt-interop.md`** — read it whenever importing expenses or when the user asks how to get bank data in.

```bash
python3 import_expenses.py --file ~/Downloads/expenses_june.csv --replace-months 2026-06
python3 import_expenses.py --summary        # inspect ledger by month × category
```

- Import is all-or-nothing with row-numbered validation errors; duplicates dedupe by hash.
- **Always use `--replace-months`** when re-importing a month that was imported before.
- `inventory_purchase` is memo-only (Shopify cost-per-item already accrues product COGS — no double count). Owner draws / transfers / CC payments / loan principal are excluded from profit.
- Brand-tagged rows flow into that brand's contribution P&L tab.

## Auth — adding stores & post-auth codes

Store credentials live in `config/stores.json` (gitignored, auto-discovered). Two auth shapes per entry: `client_id`+`client_secret` (client-credentials, minted per run) **or** a permanent `access_token`.

```bash
python3 auth.py exchange-code --domain x.myshopify.com --client-id ID \
    --client-secret SECRET --code POST_AUTH_CODE --brand "Orelli"   # code → permanent admin token, saved
python3 auth.py add-store --brand "Orelli" --domain x.myshopify.com --client-id ID --client-secret SECRET
python3 auth.py add-token --brand "Orelli" --domain x.myshopify.com --access-token shpat_xxx
python3 auth.py test      # verify every store authenticates
python3 auth.py list      # show stores, secrets redacted
```

Post-auth codes are **single-use and expire in minutes** — exchange immediately. `group` field rolls stores up to one brand (e.g. Motilli #1–4 → Motilli).

## Single-period deep-dive

```bash
python3 pull_financials.py --period last-month   # or: mtd | ytd | ttm | --since/--until
```

Confirm the period with the user first (default = last full calendar month). Saves `~/Shopify_Financials_<since>_to_<until>.xlsx`; relay headline numbers (net sales, COGS, fees, chargebacks, holds/reserves).

## Notes & gotchas (learned the hard way)

- **Orders API needs `read_all_orders`** to see beyond 60 days — the custom apps have it; new stores added via `exchange-code` must request it in their scopes.
- **Net sales uses `current_subtotal_price`** — refunds already netted; never subtract refunds again (memo line).
- **Chargebacks are NOT in order revenue** — lost chargebacks are a real expense line, booked once, by `initiated_at` month.
- **Monthly bucketing is accrual by order-creation month**; fees bucket by `processed_at`; a refund on a January order lands in January (order month), not the refund month.
- **COGS coverage matters** — Data Quality tab flags store-months <50% in red; fix by entering cost-per-item in Shopify, then re-run (a `--from-cache` rebuild will NOT pick up Shopify-side changes).
- **Reserves/holds** only exist in the single-period report (point-in-time, not monthly).
- Requires `openpyxl`; everything else is pure stdlib `urllib`.

## Files

- `scripts/monthly_pl.py` — month-by-month puller + expense merge (CLI entry)
- `scripts/build_pl_workbook.py` — monthly P&L workbook builder
- `scripts/import_expenses.py` — ChatGPT expense import → `data/expenses.json` ledger
- `scripts/auth.py` — store management + post-auth-code → permanent admin token
- `scripts/pull_financials.py` / `scripts/build_workbook.py` — single-period deep-dive
- `config/stores.json` — store credentials (private, gitignored)
- `data/` — expense ledger + cached monthly dataset (private, gitignored)
- `references/chatgpt-interop.md` — ChatGPT export prompt + schema + category chart
- `references/methodology.md` — definitions & formulas
