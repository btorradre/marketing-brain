---
name: margin-dashboard
description: True contribution-margin reporting and the live Vercel dashboard. Scrapes every Shopify order for real per-order COGS, pulls ad spend, payment fees and channel attribution from Triple Whale, pulls chargebacks from Shopify Payments disputes, pulls operating expenses from QuickBooks, and amortizes monthly fixed costs to a daily rate to produce the CM1/CM2/CM3/Net ladder. Use whenever the user asks about contribution margin, CM1/CM2/CM3, true profit, net margin, COGS accuracy, MER, CAC, blended ROAS, "what did we actually make", "am I profitable", "run the margin report", "refresh the dashboard", "update the finance dashboard", or wants to change salaries, fixed costs, shipping assumptions or which brands are tracked. Also use when a nightly run fails or the dashboard looks stale.
---

# Contribution Margin Dashboard

Computes true profit for Velantra (and any brand switched on) and publishes it to
a password-protected Vercel dashboard. Runs itself nightly at 00:00 via a
LaunchAgent; everything below is for on-demand runs and changes.

## Where things live

| Thing | Path |
|---|---|
| Pipeline | `_engine/finance/run_nightly.py` |
| Cost model (EDIT THIS) | `_engine/finance/costs.json` |
| Sources | `_engine/finance/sources/{shopify_orders,triplewhale,quickbooks}.py` |
| Ladder math | `_engine/finance/margin.py` |
| Dashboard | `_engine/finance/dashboard/api/index.js` |
| Latest snapshot | `_engine/finance/data/snapshot.json` |
| Nightly wrapper | `_engine/finance/run_nightly.sh` |
| LaunchAgent | `~/Library/LaunchAgents/com.brooks.margin-nightly.plist` |
| Run logs | `_engine/finance/logs/YYYY-MM-DD.log` |

**Live dashboard:** https://margin-dashboard-one.vercel.app
Basic auth, user `brooks`. Password is in Vercel env `DASH_PASS` (`vercel env ls`).
Auth fails closed: if the env vars are missing the page 401s rather than exposing data.

## The ladder

```
Net revenue = Shopify gross revenue − refunds
CM1 = Net revenue − COGS                              product economics
CM2 = CM1 − shipping − payment fees − chargebacks     variable cost to serve
CM3 = CM2 − ad spend                                  marketing efficiency
Net = CM3 − amortized fixed costs                     true profit
```

Fixed costs never touch CM1–CM3. They are monthly figures divided by the days in
that month, so a partial month never overstates profit.

## Running it

```bash
cd "_engine/finance"
python3 run_nightly.py                          # trailing 60 days + deploy
python3 run_nightly.py --days 180               # longer window
python3 run_nightly.py --start 2026-01-01 --end 2026-08-08
python3 run_nightly.py --no-deploy              # compute only
./run_nightly.sh                                # exactly what the LaunchAgent runs
```

A run takes about 30 seconds for 60 days. It never dies on one bad source:
failures land in `snapshot["errors"]` and render on the dashboard, because a
margin dashboard that silently drops a cost line is worse than one that admits
it is broken.

## Which source owns which number

- **COGS — Shopify, authoritative.** Scraped per order from each line item's
  `variant.inventoryItem.unitCost`. Not Triple Whale: TW books refunded COGS on
  the return date while Shopify books it to the original order date.
- **Ad spend, payment fees, channel attribution — Triple Whale** (`blended_stats_tvf`,
  `ads_table`, `pixel_joined_tvf`).
- **Chargebacks — Shopify Payments disputes**, booked on the day the dispute is
  lost. Triple Whale does not model these at all and they have run five figures a month.
- **Fixed costs — QuickBooks** when connected, otherwise the estimates in `costs.json`.
- **Shipping — not currently measured.** See the known gaps below.

## Known gaps — check these before trusting a margin number

1. **COGS coverage is not 100%.** Any product with no "Cost per item" set in
   Shopify contributes $0 COGS, which inflates CM1 and everything under it. The
   dashboard's Data Quality panel names the offending products and the dollar
   value flowing through uncosted. As of 2026-08-08 The Sofia Woven Tote and The
   Colette Wool Tote had no cost set. **Fixing this in Shopify is the single
   highest-leverage accuracy improvement.**
2. **Shipping is $0.** Triple Whale reports no shipping cost (nothing configured
   in TW Admin, no 3PL integration) and Shopify carries 0g weights store-wide, so
   per-order shipping cannot be derived from order data. Set a flat estimate in
   `costs.json` → `brands.Velantra.shipping_cost_per_order_usd` using the Ecomflow
   rate card in `finances/shipping costs/`. Until then CM2 and below are overstated.
3. **QuickBooks is not connected.** Fixed costs are estimates from the historical
   P&L (mean of Apr/May/Jun 2026), not live actuals. To connect: complete the OAuth
   handshake with `npm run auth` in `~/.claude/mcp-servers/quickbooks-online-mcp-server/`,
   then re-run. The pipeline picks it up automatically and the dashboard stops
   showing the estimate warning.
4. **Triple Whale only covers Velantra.** Motilli, Lunessa and Solorna return
   `Access Denied` on this API key. They are present but disabled in `costs.json`.

## Making changes

**Add salaries or change fixed costs** — edit `monthly_fixed_costs.lines` in
`costs.json`. Each line is `{name, monthly_usd, brand}`; `brand: null` means shared
and gets allocated per the `allocation` block (default: by daily revenue share).
Payroll is currently $0 because the P&L shows no payroll Jan–Jul 2026.

**Turn on another brand** — set `enabled: true` on it in `costs.json`. If it has no
`triplewhale_shop_id` it runs Shopify-only: real revenue, COGS, refunds and
chargebacks, but no ad spend, so CM3 will equal CM2. Say so rather than presenting
CM3 as meaningful.

**Change the margin definition** — `margin.py`. Keep fixed costs below CM3.

**Change the dashboard** — `dashboard/api/index.js` renders the whole page from
`data.json`. Redeploy with `vercel deploy --prod --yes` from `dashboard/`, or just
run the pipeline, which deploys as its last step.

## Reporting to Brooks

Lead with the ladder, not the revenue. He already knows revenue; what he is buying
here is the part revenue hides. When a number is estimated rather than measured,
say which one and why. Never present a CM1 as accurate while COGS coverage is below
100% without naming the coverage percentage in the same breath.

## Chart work

Any new chart on this dashboard goes through the `dataviz` skill, and the palette
gets validated with its `validate_palette.js` rather than eyeballed. The current
stack palette (blue/orange/aqua/violet/green) passes all six checks in both light
and dark; a reorder can silently break CVD separation.
