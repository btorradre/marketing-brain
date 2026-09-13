# ChatGPT Interop — Bank & Expense Data In, Shopify Data Out

The monthly P&L merges two data sides:

| Side | Who pulls it | How it enters the P&L |
|---|---|---|
| **Shopify** (revenue, COGS, fees, chargebacks) | This skill — Admin API, per store | `monthly_pl.py` pulls live |
| **Bank/expenses** (ad spend, 3PL, software, payroll…) | **ChatGPT** — from bank/card connections or statements | ChatGPT exports a file → `import_expenses.py` → ledger → merged automatically |

## The loop (monthly close)

1. In ChatGPT: paste the **export prompt** below + your bank/card data (statements, CSV exports, or connected-account pulls). ChatGPT returns a CSV.
2. Save it (e.g. `~/Downloads/expenses_2026-06.csv`) and run:
   ```bash
   python3 scripts/import_expenses.py --file ~/Downloads/expenses_2026-06.csv --replace-months 2026-06
   ```
3. Build the P&L:
   ```bash
   python3 scripts/monthly_pl.py --year 2026
   ```
4. (Optional, reverse direction) hand Shopify-side numbers back to ChatGPT:
   ```bash
   python3 scripts/monthly_pl.py --year 2026 --chatgpt-export ~/shopify_monthly.json
   ```
   Paste that JSON into ChatGPT if you want it to cross-check or build its own view.

`--replace-months` wipes previously imported entries for those months first — use it when re-exporting a month so you never double-import. Without it, exact-duplicate rows are skipped by hash but *changed* rows (edited description/amount) would stack.

---

## 📋 Prompt to paste into ChatGPT

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
    merchant_fees         (bank/wire/Stripe/PayPal fees — NOT Shopify fees)
    chargeback_services   (Disputifier, Chargeflow, or other chargeback-management services)
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
    cc_payment            (credit-card bill payments — the card's transactions are booked individually)
    loan_principal        (loan principal repayment; split interest into interest_expense)
- brand: Motilli, Velantra, Lunessa, Solorna, Avelle, or Orelli when the charge
  clearly belongs to one brand (e.g. an ad account or 3PL invoice for that brand).
  Leave blank if company-wide or unclear.
- source: short account tag, e.g. chase_checking, amex_plat, mercury.
- EVERY transaction must appear exactly once. Do not net, merge, or summarize rows.
- Do not skip transactions you can't categorize — use other_opex and keep the description.
- Categorize Shopify payout DEPOSITS as: transfer (revenue is tracked separately in Shopify).
- Money movement between my own accounts is ALWAYS transfer, never income or expense.
- Venmo/Wise transfers and bank wires TO INDIVIDUALS from business accounts are
  contractors_agency (freelancer payments) unless clearly personal.
- Disputifier or other chargeback-service charges are chargeback_services, not software.
```

JSON is also accepted (a list of objects with the same keys, or `{"entries": [...]}`) — same rules.

## What lands where on the P&L

- `other_income` → Revenue section (below Net Sales).
- `fulfillment_3pl`, `freight_duties` → COGS section.
- All `ad_spend_*` + the operating categories → Operating Expenses.
- `inventory_purchase` → **product COGS** under the default cash basis (supplier
  wires, e.g. Haikou Genyangkai, booked in the month paid). Under `--cogs-basis
  shopify` it demotes to memo and Shopify cost-per-item accrues COGS instead —
  never both (double count).
- `owner_draw`, `transfer`, `cc_payment`, `loan_principal` → memo, excluded from profit.

Brand-tagged rows also flow into that brand's contribution P&L tab. Untagged rows
appear only on the consolidated tab.

## Importer commands

```bash
python3 scripts/import_expenses.py --file FILE            # validate + merge into ledger
python3 scripts/import_expenses.py --file FILE --dry-run  # validate + preview only
python3 scripts/import_expenses.py --file FILE --replace-months 2026-05,2026-06
python3 scripts/import_expenses.py --summary              # ledger by month × category
python3 scripts/import_expenses.py --clear                # wipe ledger
```

Validation is all-or-nothing: any bad row (unknown category, bad date/amount)
aborts the import with row-numbered errors — fix in the file (or re-ask ChatGPT)
and re-run. Ledger lives at `data/expenses.json` (gitignored).
