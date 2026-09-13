# Methodology, Formulas & Templates

## Revenue

- Gross Sales = sum of line-item prices before discounts (pre-discount product revenue, excluding shipping/tax).
- Discounts = sum of total discounts applied.
- Net Sales = sum of the order's current subtotal price (product revenue after discounts AND refunds/returns/edits). **This is the topline metric.**
- Returns/Refunds (product) = Gross − Discounts − Net Sales (derived, not pulled directly).
- Shipping = current total price − net sales − tax − tips (net of any shipping refunds).
- Total Collected = sum of current total price (i.e., after refunds).
- Test orders should be excluded; include all order statuses (refunded/cancelled included) when pulling, then let the formulas net things out correctly.

## COGS

- Build a cost map from each product variant's per-unit cost (paginate through the full catalog).
- Units = per-variant (units sold − units refunded), from order line items plus refund line items.
- COGS = sum over variants of (net units × unit cost).
- Coverage = costed units ÷ (costed + uncosted) units. Anything under 100% means COGS is understated by that gap.

## Payment fees (from balance/transaction records)

- Processing fees = sum of fees on standard charge transactions.
- Dispute fees = sum of fees on dispute-type transactions (the flat per-chargeback fee, net of any reversal when a dispute is won).

## Chargebacks (from the disputes data, bucketed by the dispute's initiation date within the period)

- Lost = statuses meaning the merchant lost the dispute or the charge was refunded as a result.
- Won = statuses meaning the merchant won.
- Open = everything still pending.
- Lost chargebacks are booked as a P&L expense; order revenue itself is not reversed because of a chargeback.

## Refunds

- Sum of refund transaction amounts (refund-kind transactions) on orders created within the period. This is already inside Net Sales — treat as a memo line only, never subtract it a second time.

## Holds / payouts / reserves (point-in-time only)

- Available balance = current balance after chargebacks.
- Reserve = absolute value of the sum of reserved-funds/reserve-type balance transactions. Note: some admin-initiated review holds may not be visible via API at all.
- Stuck payouts = any payout with a status other than "paid" (failed/canceled/scheduled). Failed or canceled payout funds return to the available balance — don't double-count them as still "stuck."
- Track the last successful payout date and flag accounts where it's been unusually long, since that often signals a frozen or failing payment account.

## P&L treatment

- Tax collected is a passthrough liability — exclude it from profit calculations entirely.
- Net Sales is the profit basis. Refunds are already netted into it; chargebacks-lost and fees are each booked exactly once.

## Bank/expense export prompt (paste into a bank-data assistant)

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
    taxes_gov              (government fees, franchise tax, filing fees)
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
