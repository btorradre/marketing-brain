---
name: margin-dashboard
description: Compute and report TRUE contribution margin (not just revenue) for a DTC brand, and reason about the resulting numbers. Use whenever asked about contribution margin, CM1/CM2/CM3, true profit, net margin, COGS accuracy, MER, CAC, blended ROAS, "what did we actually make," "are we profitable," or when refreshing/reporting a margin or finance dashboard.
---

# Contribution Margin Dashboard

Computes true profit for a DTC brand (or several brands) and reports it in a structured, source-attributed way — not just top-line revenue.

The original implementation scraped every order for real per-order COGS, pulled ad spend/payment fees/channel attribution from an analytics platform, pulled chargebacks from the payment processor's dispute records, pulled operating expenses from accounting software, and amortized monthly fixed costs to a daily rate — then published the result to a password-protected dashboard, refreshed nightly. On a different platform, replicate the same logic against whatever equivalent data sources are available (store order/order-line data, ad platform spend data, payment processor dispute data, accounting-system fixed costs).

## How to use this

1. Identify your data sources: (a) an e-commerce platform's order data (for revenue, refunds, and per-line-item cost of goods), (b) an ad/attribution platform (for ad spend, payment processing fees, channel attribution), (c) the payment processor's dispute/chargeback records, and (d) accounting software (for monthly fixed costs like payroll, rent, software).
2. Pull orders for the reporting window (a trailing period, e.g. 60 days, or a custom date range) and compute net revenue as gross revenue minus refunds.
3. Compute COGS per order from the actual per-line-item unit cost recorded on each order — not from an ad-platform estimate, which books returns differently than the storefront does.
4. Compute the CM ladder (see formula below).
5. Amortize monthly fixed costs to a daily rate (divide the month's total by the number of days in that month) so a partial month is never overstated.
6. Never let a single failed data source silently zero out a cost line — if a source fails, record the failure explicitly and surface it in the report, rather than presenting an artificially rosy number.
7. Publish/report the result with the full ladder, not just top-line revenue, and flag any number that is estimated rather than measured.

## The margin ladder

```
Net revenue = Gross revenue − refunds
CM1 = Net revenue − COGS                              (product economics)
CM2 = CM1 − shipping − payment fees − chargebacks      (variable cost to serve)
CM3 = CM2 − ad spend                                   (marketing efficiency)
Net = CM3 − amortized fixed costs                      (true profit)
```

Fixed costs never touch CM1–CM3. They are monthly figures divided by the number of days in that month, so a partial month never overstates profit.

## Which source should own which number

- **COGS — the storefront/order platform is authoritative,** scraped per order from each line item's actual unit cost. Do not use an ad-attribution tool's cost figure for this: attribution tools tend to book refunded COGS on the return date, while the storefront books it to the original order date, which creates a mismatch.
- **Ad spend, payment fees, and channel attribution — the ad-attribution/analytics platform** (blended stats, ad-level spend tables, pixel-joined attribution).
- **Chargebacks — the payment processor's dispute records,** booked on the day the dispute is lost. Attribution tools typically do not model chargebacks at all, and they can run into five figures a month, so this line matters.
- **Fixed costs — the accounting system** when connected; otherwise a documented estimate.
- **Shipping — often not measured at all** unless a shipping-cost source is specifically wired up (see known gaps below).

## Known accuracy gaps — check these before trusting a margin number

1. **COGS coverage is rarely 100%.** Any product with no per-item cost set in the store's admin contributes $0 COGS, which inflates CM1 and everything under it. A dashboard should have a "data quality" panel that names the specific products with missing cost data and the dollar value flowing through uncosted. Fixing missing cost-per-item data in the store is usually the single highest-leverage accuracy improvement available.
2. **Shipping is often $0** if the ad-attribution tool has no shipping cost configured and the store's order data carries zero product weights (so per-order shipping can't be derived automatically). In that case, set a flat per-order shipping estimate manually from a real shipping/3PL rate card. Until that's done, CM2 and everything below it will be overstated.
3. **Accounting-system integration may not be connected**, in which case fixed costs are estimates derived from a historical P&L (e.g. an average of a few recent months) rather than live actuals. Connect the accounting integration when possible; the pipeline should pick it up automatically once connected and stop showing an "estimate" warning.
4. **An ad-attribution platform may only cover one brand** if you run multiple brands through a single API key — other brands may return "access denied" and should be marked disabled (Shopify-only) in the cost configuration rather than silently reporting $0 ad spend as if it were real.

## Making changes to the model

- **Adding salaries or changing fixed costs:** edit the fixed-costs configuration. Each line item should record a name, a monthly dollar amount, and which brand it belongs to (or "shared," in which case it should be allocated across brands — by default, pro-rated by daily revenue share).
- **Turning on another brand:** enable it in the cost configuration. If it has no ad-attribution integration configured, it will run "Shopify-only" — real revenue, COGS, refunds, and chargebacks, but no ad spend, meaning CM3 will equal CM2. State that explicitly rather than presenting CM3 as a meaningful marketing-efficiency number in that case.
- **Changing the margin definition:** edit the margin-calculation logic directly, but always keep fixed costs below CM3 in the ladder — never let fixed costs leak into CM1/CM2/CM3.
- **Changing the dashboard display:** the dashboard should render entirely from a single computed data snapshot; redeploy after any pipeline run, or make deployment the pipeline's last automatic step.

## How to report the numbers

- Lead with the ladder (CM1 → CM2 → CM3 → Net), not with revenue. Revenue is usually already known; the value of this report is showing what revenue hides.
- When a number is estimated rather than measured, say which one and why, in the same breath as the number itself.
- Never present CM1 as accurate while COGS coverage is below 100% without naming the coverage percentage alongside it.

## Chart/visualization work

Any chart built on top of this data should follow general data-visualization design principles (a validated, colorblind-safe categorical palette; consistent light/dark theming; clear legends and axis labeling) rather than an eyeballed color scheme — palette choices should be run through an accessibility/contrast check, since reordering colors in a stacked chart can silently break category separation for colorblind viewers.
