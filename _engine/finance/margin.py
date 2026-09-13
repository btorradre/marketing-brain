"""The contribution-margin ladder.

  Net revenue = Shopify gross revenue - refunds
  CM1  = Net revenue - COGS                            (product economics)
  CM2  = CM1 - shipping - payment fees - chargebacks    (variable cost to serve)
  CM3  = CM2 - ad spend                                 (marketing efficiency)
  Net  = CM3 - amortized fixed costs                    (true profit)

Fixed costs are monthly figures divided by the number of days in that month, so
a partial month never overstates profit.

Every day carries a `flags` list naming the specific assumptions that fed it, so
the dashboard can show which numbers are measured and which are estimated.
"""
import sys

sys.path.insert(0, __file__.rsplit("/margin.py", 1)[0])
from common import days_in_month, money  # noqa: E402


def daily_fixed_costs(config, day, brand, revenue_share):
    """Amortized fixed cost for one brand on one day, plus its breakdown."""
    dim = days_in_month(day)
    method = config.get("allocation", {}).get("method", "revenue_share")
    explicit = config.get("allocation", {}).get("explicit_share", {})

    breakdown, total = [], 0.0
    for line in config.get("monthly_fixed_costs", {}).get("lines", []):
        monthly = float(line.get("monthly_usd") or 0)
        if not monthly:
            continue
        if line.get("brand") and line["brand"] != brand:
            continue
        if line.get("brand") == brand:
            share = 1.0
        elif method == "fixed":
            share = float(explicit.get(brand, 0.0))
        else:
            share = revenue_share
        amount = monthly / dim * share
        if amount:
            breakdown.append({"name": line["name"], "amount": money(amount)})
            total += amount
    return money(total), breakdown


def build_day(day, brand, config, shopify, tw_blended, tw_channels,
              disputes, revenue_share=1.0):
    """Assemble one brand-day into a full margin ladder."""
    brand_cfg = config["brands"][brand]
    flags = []

    sh = shopify or {}
    gross = float(sh.get("gross_revenue") or 0)
    refunds = float(sh.get("refunds") or 0)
    orders = int(sh.get("orders") or 0)
    net_revenue = gross - refunds

    # --- COGS: Shopify is authoritative -------------------------------------
    cogs = float(sh.get("cogs") or 0)
    uncosted_rev = float(sh.get("uncosted_revenue") or 0)
    units_uncosted = int(sh.get("units_uncosted") or 0)
    if config.get("cogs", {}).get("source") == "triplewhale" and tw_blended:
        cogs = float(tw_blended.get("tw_cogs") or 0)
        flags.append("cogs_from_triplewhale")
    if units_uncosted:
        fallback = config.get("cogs", {}).get("fallback_margin_pct")
        if fallback:
            cogs += uncosted_rev * float(fallback)
            flags.append("cogs_imputed_for_uncosted_units")
        else:
            flags.append("cogs_missing_on_some_units")

    cm1 = net_revenue - cogs

    # --- Variable cost to serve ---------------------------------------------
    per_order_ship = brand_cfg.get("shipping_cost_per_order_usd")
    if per_order_ship is None:
        shipping = 0.0
        flags.append("shipping_not_configured")
    else:
        shipping = float(per_order_ship) * orders
        flags.append("shipping_estimated_flat_rate")

    fees_cfg = config.get("payment_fees", {})
    if tw_blended and tw_blended.get("payment_fees") is not None:
        payment_fees = float(tw_blended.get("payment_fees") or 0)
    else:
        payment_fees = gross * float(fees_cfg.get("rate_pct") or 0) + \
            orders * float(fees_cfg.get("flat_per_order_usd") or 0)
        flags.append("payment_fees_estimated")

    chargebacks = float(disputes or 0) if config.get("chargebacks", {}).get("include") else 0.0

    cm2 = cm1 - shipping - payment_fees - chargebacks

    # --- Marketing ----------------------------------------------------------
    ad_spend = float((tw_blended or {}).get("spend") or 0)
    if not tw_blended:
        flags.append("no_triplewhale_data")
    cm3 = cm2 - ad_spend

    # --- Fixed costs --------------------------------------------------------
    fixed, fixed_breakdown = daily_fixed_costs(config, day, brand, revenue_share)
    net_profit = cm3 - fixed

    def pct(numer):
        return round(numer / net_revenue * 100, 2) if net_revenue else None

    return {
        "date": day,
        "brand": brand,
        "orders": orders,
        "units": int(sh.get("units") or 0),
        "new_customer_orders": int(sh.get("new_customer_orders") or 0),
        "gross_revenue": money(gross),
        "refunds": money(refunds),
        "net_revenue": money(net_revenue),
        "discounts": money(sh.get("discounts")),
        "shipping_charged": money(sh.get("shipping_charged")),
        "costs": {
            "cogs": money(cogs),
            "shipping": money(shipping),
            "payment_fees": money(payment_fees),
            "chargebacks": money(chargebacks),
            "ad_spend": money(ad_spend),
            "fixed": money(fixed),
            "fixed_breakdown": fixed_breakdown,
        },
        "ladder": {
            "cm1": money(cm1), "cm1_pct": pct(cm1),
            "cm2": money(cm2), "cm2_pct": pct(cm2),
            "cm3": money(cm3), "cm3_pct": pct(cm3),
            "net": money(net_profit), "net_pct": pct(net_profit),
        },
        "efficiency": {
            "aov": money(net_revenue / orders) if orders else None,
            "mer": round(net_revenue / ad_spend, 2) if ad_spend else None,
            "cac": money(ad_spend / sh["new_customer_orders"])
                   if sh.get("new_customer_orders") else None,
            "cogs_pct": pct(cogs),
            "ad_spend_pct": pct(ad_spend),
        },
        "channels": tw_channels or {},
        "data_quality": {
            "units_costed": int(sh.get("units_costed") or 0),
            "units_uncosted": units_uncosted,
            "uncosted_revenue": money(uncosted_rev),
            "cogs_coverage_pct": round(
                sh["units_costed"] / sh["units"] * 100, 1)
                if sh.get("units") else None,
        },
        "flags": flags,
    }


def summarize(days):
    """Roll a list of brand-days into one total block."""
    if not days:
        return {}
    acc = {
        "orders": 0, "units": 0, "new_customer_orders": 0, "gross_revenue": 0.0,
        "refunds": 0.0, "net_revenue": 0.0, "cogs": 0.0, "shipping": 0.0,
        "payment_fees": 0.0, "chargebacks": 0.0, "ad_spend": 0.0, "fixed": 0.0,
    }
    for d in days:
        acc["orders"] += d["orders"]
        acc["units"] += d["units"]
        acc["new_customer_orders"] += d["new_customer_orders"]
        acc["gross_revenue"] += d["gross_revenue"]
        acc["refunds"] += d["refunds"]
        acc["net_revenue"] += d["net_revenue"]
        for k in ("cogs", "shipping", "payment_fees", "chargebacks", "ad_spend", "fixed"):
            acc[k] += d["costs"][k]

    nr = acc["net_revenue"]
    cm1 = nr - acc["cogs"]
    cm2 = cm1 - acc["shipping"] - acc["payment_fees"] - acc["chargebacks"]
    cm3 = cm2 - acc["ad_spend"]
    net = cm3 - acc["fixed"]

    def pct(x):
        return round(x / nr * 100, 2) if nr else None

    return {
        "orders": acc["orders"], "units": acc["units"],
        "new_customer_orders": acc["new_customer_orders"],
        "gross_revenue": money(acc["gross_revenue"]),
        "refunds": money(acc["refunds"]),
        "net_revenue": money(nr),
        "costs": {k: money(acc[k]) for k in
                  ("cogs", "shipping", "payment_fees", "chargebacks", "ad_spend", "fixed")},
        "ladder": {"cm1": money(cm1), "cm1_pct": pct(cm1),
                   "cm2": money(cm2), "cm2_pct": pct(cm2),
                   "cm3": money(cm3), "cm3_pct": pct(cm3),
                   "net": money(net), "net_pct": pct(net)},
        "efficiency": {
            "aov": money(nr / acc["orders"]) if acc["orders"] else None,
            "mer": round(nr / acc["ad_spend"], 2) if acc["ad_spend"] else None,
            "cac": money(acc["ad_spend"] / acc["new_customer_orders"])
                   if acc["new_customer_orders"] else None,
            "cogs_pct": pct(acc["cogs"]),
            "ad_spend_pct": pct(acc["ad_spend"]),
        },
    }
