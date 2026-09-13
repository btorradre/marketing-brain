# Methodology & Formulas

## Revenue
- **Gross Sales** = Σ `total_line_items_price` (pre-discount product revenue, excl. shipping/tax).
- **Discounts** = Σ `total_discounts`.
- **Net Sales** = Σ `current_subtotal_price` (product revenue after discounts AND refunds/returns/edits). This is the topline.
- **Returns/Refunds (product)** = Gross − Discounts − Net Sales (derived).
- **Shipping** = `current_total_price` − net − tax − tips (net of shipping refunds).
- **Total Collected** = Σ `current_total_price` (after refunds).
- Test orders excluded; `status=any` (includes refunded/cancelled).

## COGS
- Cost map: GraphQL `productVariants → inventoryItem.unitCost.amount` (paginated).
- Units: per-variant `(sold − refunded)` from order line items + refund_line_items.
- **COGS** = Σ net_units × unit_cost. **Coverage** = costed_units / (costed + uncosted). <100% ⇒ understated.

## Payment fees (balance transactions `fee` field)
- **Processing fees** = Σ fee where type = `charge`.
- **Dispute fees** = Σ fee where type = `dispute` (the ~$15 chargeback fees, net of won-dispute reversals).

## Chargebacks (disputes API, by `initiated_at` in period)
- Bucketed by status: **lost** = {lost, accepted, charge_refunded}; **won** = {won}; **open** = everything else.
- Lost chargebacks are booked as a P&L expense (order revenue does not reverse on a chargeback).

## Refunds
- Σ refund transaction amounts (kind=refund) on orders created in period. Already inside Net Sales → memo only, never subtract twice.

## Holds / payouts / reserves
- **Available** = `shopify_payments/balance.json` (after chargebacks).
- **Reserve** = |Σ amount of `reserved_funds`/`reserve` balance transactions|. Admin review-holds may not appear via API.
- **Stuck payouts** = payouts with status ≠ paid (failed/canceled/scheduled). Failed/canceled funds return to available (not additive).
- **Last payout** + days since flags frozen/failing accounts.

## P&L treatment
- Tax collected = passthrough liability, excluded from profit.
- Net Sales is the profit basis. Refunds already netted; chargebacks-lost + fees booked once.
