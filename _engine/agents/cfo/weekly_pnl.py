#!/usr/bin/env python3
"""
Weekly P&L Generator — CFO Agent
Pulls Shopify revenue from all stores + SimpleFIN bank expenses,
generates comprehensive weekly P&L, expense breakdown, and financial sheets.

Usage:
    python3 weekly_pnl.py                    # This week's P&L
    python3 weekly_pnl.py --weeks 4          # Last 4 weeks
    python3 weekly_pnl.py --full             # Full financial package (P&L + all sheets)
"""

import argparse
import base64
import json
import os
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(PROJECT_ROOT / ".env")

DATA_DIR = Path(__file__).parent / "data"
REPORTS_DIR = DATA_DIR / "reports"
CONFIG_FILE = Path(__file__).parent / "shopify_config.json"

SIMPLEFIN_ACCESS_URL = os.getenv("SIMPLEFIN_ACCESS_URL")


# ═══════════════════════════════════════════════════════════════
#  SHOPIFY: Revenue + Orders
# ═══════════════════════════════════════════════════════════════

def get_shopify_token(store):
    """Get fresh access token via client credentials."""
    r = subprocess.run(
        ["curl", "-s", "-X", "POST",
         f"https://{store['store_url']}/admin/oauth/access_token",
         "-H", "Content-Type: application/x-www-form-urlencoded",
         "-d", f"grant_type=client_credentials&client_id={store['client_id']}&client_secret={store['client_secret']}"],
        capture_output=True, text=True, timeout=15
    )
    try:
        return json.loads(r.stdout).get("access_token")
    except:
        return None


def fetch_shopify_orders(store, token, start_date, end_date):
    """Fetch all orders from a Shopify store in a date range."""
    all_orders = []
    api_version = "2024-01"
    next_url = None

    while True:
        if next_url:
            url = next_url
        else:
            url = (f"https://{store['store_url']}/admin/api/{api_version}/orders.json"
                   f"?status=any&limit=250"
                   f"&created_at_min={start_date}T00:00:00-06:00"
                   f"&created_at_max={end_date}T23:59:59-06:00"
                   f"&fields=id,name,created_at,total_price,subtotal_price,total_discounts,"
                   f"total_tax,financial_status,fulfillment_status,refunds,line_items,"
                   f"total_shipping_price_set,gateway,source_name")

        # Use -i to get headers inline, then split
        r = subprocess.run(
            ["curl", "-s", "-i",
             "-H", f"X-Shopify-Access-Token: {token}", url],
            capture_output=True, text=True, timeout=60
        )

        output = r.stdout
        # Find the JSON body (starts with { after headers)
        json_start = output.find('\n{')
        if json_start == -1:
            json_start = output.find('\r\n{')
        if json_start == -1:
            break

        headers_part = output[:json_start]
        body = output[json_start:].strip()

        try:
            data = json.loads(body)
            orders = data.get("orders", [])
            all_orders.extend(orders)
        except json.JSONDecodeError:
            break

        # Check for pagination via Link header
        next_url = None
        for line in headers_part.split("\n"):
            if line.lower().startswith("link:"):
                import re
                match = re.search(r'<([^>]+)>;\s*rel="next"', line)
                if match:
                    next_url = match.group(1)

        if not next_url or len(orders) == 0:
            break

    return all_orders


def process_shopify_orders(orders, brand, label):
    """Process Shopify orders into financial data."""
    revenue_data = []

    for order in orders:
        created = order.get("created_at", "")[:10]
        total = float(order.get("total_price", 0))
        subtotal = float(order.get("subtotal_price", 0))
        discounts = float(order.get("total_discounts", 0))
        tax = float(order.get("total_tax", 0))
        financial = order.get("financial_status", "")
        shipping_set = order.get("total_shipping_price_set", {})
        shipping = float(shipping_set.get("shop_money", {}).get("amount", 0)) if shipping_set else 0

        # Calculate refund amounts
        refund_total = 0
        for refund in order.get("refunds", []):
            for line in refund.get("refund_line_items", []):
                refund_total += float(line.get("subtotal", 0))

        # Determine order status
        if financial in ("refunded", "voided"):
            status = "refunded"
        elif financial == "partially_refunded":
            status = "partial_refund"
        else:
            status = "paid"

        revenue_data.append({
            "date": created,
            "brand": brand,
            "store": label,
            "order_name": order.get("name", ""),
            "gross_revenue": subtotal,
            "discounts": discounts,
            "shipping_revenue": shipping,
            "tax": tax,
            "total": total,
            "refunds": refund_total,
            "net_revenue": total - refund_total,
            "financial_status": financial,
            "status": status,
            "gateway": order.get("gateway", ""),
            "source": order.get("source_name", ""),
        })

    return revenue_data


# ═══════════════════════════════════════════════════════════════
#  SIMPLEFIN: Bank Expenses
# ═══════════════════════════════════════════════════════════════

def fetch_bank_transactions(days):
    """Pull transactions from SimpleFIN."""
    start_ts = int((datetime.now() - timedelta(days=days)).timestamp())
    url = f"{SIMPLEFIN_ACCESS_URL}/accounts?start-date={start_ts}"
    r = subprocess.run(["curl", "-s", url], capture_output=True, text=True, timeout=60)
    data = json.loads(r.stdout)
    return data.get("accounts", [])


def parse_bank_data(raw_accounts):
    """Parse SimpleFIN accounts into expenses + account balances."""
    expenses = []
    balances = []

    for acc in raw_accounts:
        org = acc.get("org", {}).get("name", "Unknown")
        acc_name = acc.get("name", "")
        balance = float(acc.get("balance", 0))
        available = float(acc.get("available-balance", 0))

        balances.append({
            "bank": org,
            "account": acc_name,
            "balance": balance,
            "available": available,
        })

        for tx in acc.get("transactions", []):
            posted = tx.get("posted") or tx.get("transacted_at")
            if not posted:
                continue

            date_str = datetime.fromtimestamp(posted).strftime("%Y-%m-%d")
            amount = float(tx.get("amount", 0))
            payee = tx.get("payee", "").strip()
            desc = tx.get("description", "").strip()
            merchant = payee if payee else desc[:60]

            expenses.append({
                "date": date_str,
                "merchant": merchant,
                "amount": -amount,  # flip: positive = outflow
                "account": f"{org} — {acc_name}",
                "raw_description": desc,
                "category": categorize_expense(merchant, desc),
            })

    return expenses, balances


# ═══════════════════════════════════════════════════════════════
#  CATEGORIZATION
# ═══════════════════════════════════════════════════════════════

EXPENSE_CATEGORIES = {
    "Ad Spend": [
        "facebook", "meta platforms", "facebk", "meta ", "fb ",
        "google ads", "adwords", "tiktok ads", "snap inc", "pinterest",
        "taboola", "outbrain", "microsoft advertising",
    ],
    "COGS / Shopify Fees": [
        "shopify",
    ],
    "Contractor / Freelancer": [
        "wise", "wire transfer", "jpmorgan chase bank bnf=",
        "kabir", "matvei", "orelli", "genyangkai",
    ],
    "SaaS / Tools": [
        "skool", "klaviyo", "similarweb", "intuit", "heygen",
        "frame.io", "paddle", "funnelish", "higgsfield", "rapid ads",
        "notion", "loom", "vercel", "netlify", "capcut", "flair ai",
        "brandwise", "gethookd", "kalodata", "synta", "quillbot",
        "docusign", "openrouter", "slack", "discord", "canva",
        "figma", "cursor", "apify", "cloudflare", "name-cheap",
        "namecheap", "google workspace", "microsoft", "zoom",
        "ddtech", "atria", "iproyal", "whop",
    ],
    "Subscriptions / Personal": [
        "netflix", "hbo", "spotify", "disney", "youtube",
        "nba league", "uber", "doordash", "1password",
        "rocket money", "hulu", "apple.com",
    ],
    "Rent / Housing": [
        "cedar at the bra", "rent",
    ],
    "Auto / Transport": [
        "mercedes benz", "carnation auto", "super star car wash",
        "tesla", "shell", "chevron", "parking",
    ],
    "Legal / Compliance": [
        "legalshield",
    ],
    "Insurance": [
        "insurance", "geico", "allstate",
    ],
    "Tax Payments": [
        "irs", "franchise tax board", "us treasury",
    ],
    "Credit Card Payments": [
        "american express credit card",
    ],
    "Brokerage / Investment": [
        "sweep transaction", "vanguard", "automated debit",
        "decrease from brokerage", "asset advisor",
    ],
    "Travel": [
        "andamextravel", "airline", "hotel", "airbnb",
    ],
    "Food / Dining": [
        "sweetgreen", "starbucks", "chipotle", "doordash",
        "uber eats", "grubhub", "blue bottle", "bijou",
        "star osco", "h-e-b", "armk frost",
    ],
    "Health / Fitness": [
        "bu fitrec", "gym", "pharmacy", "cvs", "walgreens",
    ],
    "Education": [
        "macmillan", "barnes & noble", "scratch",
    ],
    "Miscellaneous": [
        "aaa texas",
    ],
}


def categorize_expense(merchant, description):
    combined = f"{merchant} {description}".lower()
    for cat, keywords in EXPENSE_CATEGORIES.items():
        for kw in keywords:
            if kw in combined:
                return cat
    return "Uncategorized"


# ═══════════════════════════════════════════════════════════════
#  WEEK HELPERS
# ═══════════════════════════════════════════════════════════════

def get_week_boundaries(weeks_back=0):
    """Get Monday-Sunday boundaries for a given week."""
    today = datetime.now().date()
    # Current week's Monday
    monday = today - timedelta(days=today.weekday())
    # Go back N weeks
    monday = monday - timedelta(weeks=weeks_back)
    sunday = monday + timedelta(days=6)
    return monday, sunday


def get_week_label(monday):
    """Generate a human-readable week label."""
    sunday = monday + timedelta(days=6)
    return f"Week of {monday.strftime('%b %d')} - {sunday.strftime('%b %d, %Y')}"


# ═══════════════════════════════════════════════════════════════
#  REPORT GENERATION
# ═══════════════════════════════════════════════════════════════

def format_cell(val, fmt):
    """Format a P&L cell value."""
    if fmt == "count":
        return f" {int(val):,} |"
    elif fmt == "roas":
        return f" {val:.2f}x |"
    elif fmt == "cost":
        return f" (${val:,.0f}) |" if val > 0 else " — |"
    elif fmt == "profit":
        if val >= 0:
            return f" **${val:,.0f}** |"
        else:
            return f" **(${ abs(val):,.0f})** |"
    elif fmt == "money":
        return f" ${val:,.0f} |"
    else:
        return f" {val} |"


def generate_pnl(revenue_data, expenses, balances, weeks, week_boundaries):
    """Generate comprehensive weekly P&L."""
    lines = [
        "# Weekly P&L Report",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Weeks Covered:** {weeks}",
        "",
    ]

    # ── Account Balances ──
    lines.append("## Current Account Balances\n")
    lines.append("| Bank | Account | Balance | Available |")
    lines.append("|------|---------|---------|-----------|")
    total_bal = 0
    for b in balances:
        lines.append(f"| {b['bank']} | {b['account']} | ${b['balance']:,.2f} | ${b['available']:,.2f} |")
        total_bal += b['balance']
    lines.append(f"| **TOTAL** | | **${total_bal:,.2f}** | |")
    lines.append("")

    # ── Weekly P&L Table ──
    lines.append("## Weekly P&L Summary\n")

    header = "| Metric |"
    divider = "|--------|"
    for monday, sunday in week_boundaries:
        label = monday.strftime("%b %d")
        header += f" {label} |"
        divider += "--------|"
    header += " **Total** |"
    divider += "--------|"
    lines.append(header)
    lines.append(divider)

    # Calculate weekly metrics
    weekly_metrics = {}
    for monday, sunday in week_boundaries:
        start_str = str(monday)
        end_str = str(sunday)
        week_key = str(monday)

        # Revenue
        week_rev = [r for r in revenue_data if start_str <= r["date"] <= end_str and r["status"] != "refunded"]
        gross = sum(r["gross_revenue"] for r in week_rev)
        refunds = sum(r["refunds"] for r in week_rev)
        discounts = sum(r["discounts"] for r in week_rev)
        shipping = sum(r["shipping_revenue"] for r in week_rev)
        net_rev = gross - refunds - discounts + shipping
        order_count = len(week_rev)

        # Expenses
        week_exp = [e for e in expenses if start_str <= e["date"] <= end_str and e["amount"] > 0]

        ad_spend = sum(e["amount"] for e in week_exp if e["category"] == "Ad Spend")
        cogs = sum(e["amount"] for e in week_exp if e["category"] == "COGS / Shopify Fees")
        contractors = sum(e["amount"] for e in week_exp if e["category"] == "Contractor / Freelancer")
        saas = sum(e["amount"] for e in week_exp if e["category"] == "SaaS / Tools")
        tax = sum(e["amount"] for e in week_exp if e["category"] == "Tax Payments")
        cc_payments = sum(e["amount"] for e in week_exp if e["category"] == "Credit Card Payments")
        brokerage = sum(e["amount"] for e in week_exp if e["category"] == "Brokerage / Investment")

        # Business operating expenses (only categories that are real biz costs)
        biz_cats = {"Ad Spend", "COGS / Shopify Fees", "Contractor / Freelancer",
                    "SaaS / Tools", "Legal / Compliance"}
        biz_opex = sum(e["amount"] for e in week_exp if e["category"] in biz_cats)

        # Personal / overhead (rent, auto, subs, food, health, travel, etc.)
        non_biz = {"Tax Payments", "Credit Card Payments", "Brokerage / Investment", "Transfer/Payment"}
        personal_cats = set(EXPENSE_CATEGORIES.keys()) - biz_cats - non_biz
        personal = sum(e["amount"] for e in week_exp if e["category"] in personal_cats)
        uncategorized = sum(e["amount"] for e in week_exp if e["category"] == "Uncategorized")

        gross_profit = net_rev - cogs
        operating_profit = net_rev - biz_opex

        # ROAS
        roas = (net_rev / ad_spend) if ad_spend > 0 else 0

        weekly_metrics[week_key] = {
            "gross": gross, "refunds": refunds, "discounts": discounts,
            "shipping": shipping, "net_rev": net_rev, "orders": order_count,
            "ad_spend": ad_spend, "cogs": cogs, "contractors": contractors,
            "saas": saas, "biz_opex": biz_opex, "gross_profit": gross_profit,
            "operating_profit": operating_profit, "roas": roas,
            "personal": personal, "uncategorized": uncategorized,
            "tax": tax, "cc_payments": cc_payments, "brokerage": brokerage,
        }

    # Build P&L rows
    metrics_rows = [
        ("**REVENUE**", "", "header"),
        ("Gross Revenue", "gross", "money"),
        ("Discounts", "discounts", "cost"),
        ("Refunds", "refunds", "cost"),
        ("Shipping Revenue", "shipping", "money"),
        ("**Net Revenue**", "net_rev", "money"),
        ("Orders", "orders", "count"),
        ("", "", "spacer"),
        ("**COST OF GOODS**", "", "header"),
        ("Shopify / COGS", "cogs", "cost"),
        ("**Gross Profit**", "gross_profit", "money"),
        ("", "", "spacer"),
        ("**BUSINESS OPEX**", "", "header"),
        ("Ad Spend (Meta/Google)", "ad_spend", "cost"),
        ("Contractors / Freelancers", "contractors", "cost"),
        ("SaaS / Tools", "saas", "cost"),
        ("Total Biz OpEx", "biz_opex", "cost"),
        ("", "", "spacer"),
        ("**BOTTOM LINE**", "", "header"),
        ("**Operating Profit**", "operating_profit", "profit"),
        ("ROAS", "roas", "roas"),
        ("", "", "spacer"),
        ("**PERSONAL / OVERHEAD**", "", "header"),
        ("Personal Expenses", "personal", "cost"),
        ("Uncategorized", "uncategorized", "cost"),
        ("", "", "spacer"),
        ("**NON-OPERATING**", "", "header"),
        ("Tax Payments", "tax", "cost"),
        ("CC Payments (transfers)", "cc_payments", "cost"),
        ("Brokerage / Investment", "brokerage", "cost"),
    ]

    # Add Totals column
    total_metrics = {}
    for key in list(weekly_metrics.values())[0].keys() if weekly_metrics else []:
        if key == "roas":
            total_ad = sum(wm.get("ad_spend", 0) for wm in weekly_metrics.values())
            total_rev = sum(wm.get("net_rev", 0) for wm in weekly_metrics.values())
            total_metrics[key] = (total_rev / total_ad) if total_ad > 0 else 0
        else:
            total_metrics[key] = sum(wm.get(key, 0) for wm in weekly_metrics.values())

    for label, key, fmt in metrics_rows:
        if fmt == "spacer":
            row = f"| |"
            for _ in week_boundaries:
                row += " |"
            row += " |"
            lines.append(row)
            continue
        if fmt == "header":
            row = f"| {label} |"
            for _ in week_boundaries:
                row += " |"
            row += " |"
            lines.append(row)
            continue

        row = f"| {label} |"
        for monday, _ in week_boundaries:
            wk = str(monday)
            val = weekly_metrics.get(wk, {}).get(key, 0)
            row += format_cell(val, fmt)
        # Totals column
        row += format_cell(total_metrics.get(key, 0), fmt)
        lines.append(row)

    lines.append("")

    # ── Revenue by Brand ──
    lines.append("## Revenue by Brand (Weekly)\n")
    brands = sorted(set(r["brand"] for r in revenue_data))
    header = "| Brand |"
    divider = "|-------|"
    for monday, _ in week_boundaries:
        header += f" {monday.strftime('%b %d')} |"
        divider += "--------|"
    header += " Total |"
    divider += "-------|"
    lines.append(header)
    lines.append(divider)

    for brand in brands:
        row = f"| {brand} |"
        brand_total = 0
        for monday, sunday in week_boundaries:
            start_str, end_str = str(monday), str(sunday)
            rev = sum(r["net_revenue"] for r in revenue_data
                     if r["brand"] == brand and start_str <= r["date"] <= end_str)
            brand_total += rev
            row += f" ${rev:,.0f} |"
        row += f" ${brand_total:,.0f} |"
        lines.append(row)

    lines.append("")

    return "\n".join(lines)


def generate_expense_sheet(expenses, start_date, end_date):
    """Generate detailed expense breakdown sheet."""
    filtered = [e for e in expenses if str(start_date) <= e["date"] <= str(end_date) and e["amount"] > 0]
    filtered.sort(key=lambda e: e["date"], reverse=True)

    lines = [
        "# Detailed Expense Sheet",
        f"**Period:** {start_date} to {end_date}",
        f"**Total Transactions:** {len(filtered)}",
        "",
    ]

    # By category
    by_cat = defaultdict(list)
    for e in filtered:
        by_cat[e["category"]].append(e)

    cat_totals = {cat: sum(e["amount"] for e in txs) for cat, txs in by_cat.items()}
    sorted_cats = sorted(cat_totals.items(), key=lambda x: x[1], reverse=True)

    lines.append("## Expense Summary by Category\n")
    lines.append("| Category | Amount | Count | % of Total |")
    lines.append("|----------|--------|-------|------------|")
    total = sum(cat_totals.values())
    for cat, amount in sorted_cats:
        count = len(by_cat[cat])
        pct = (amount / total * 100) if total > 0 else 0
        lines.append(f"| {cat} | ${amount:,.2f} | {count} | {pct:.1f}% |")
    lines.append(f"| **TOTAL** | **${total:,.2f}** | **{len(filtered)}** | |")
    lines.append("")

    # Detailed per category
    for cat, amount in sorted_cats:
        if cat in ("Credit Card Payments", "Brokerage / Investment"):
            continue  # Skip transfer categories in detail
        txs = sorted(by_cat[cat], key=lambda e: e["amount"], reverse=True)
        lines.append(f"### {cat} — ${amount:,.2f}\n")
        lines.append("| Date | Merchant | Amount | Account |")
        lines.append("|------|----------|--------|---------|")
        for e in txs[:30]:  # Cap at 30 per category
            lines.append(f"| {e['date']} | {e['merchant']} | ${e['amount']:,.2f} | {e['account']} |")
        if len(txs) > 30:
            lines.append(f"| ... | *{len(txs)-30} more transactions* | | |")
        lines.append("")

    return "\n".join(lines)


def generate_subscription_sheet(expenses):
    """Generate recurring subscription detection sheet."""
    by_merchant = defaultdict(list)
    for e in expenses:
        if e["amount"] > 0:
            by_merchant[e["merchant"].lower()].append(e)

    subs = []
    for merchant, txs in by_merchant.items():
        if len(txs) < 2:
            continue
        txs.sort(key=lambda t: t["date"])
        amounts = [t["amount"] for t in txs]
        avg = sum(amounts) / len(amounts)
        if avg == 0:
            continue
        consistent = all(abs(a - avg) / avg < 0.30 for a in amounts)
        if not consistent:
            continue

        dates = [t["date"] for t in txs]
        if len(dates) >= 2:
            d_objs = [datetime.strptime(d, "%Y-%m-%d") for d in dates]
            intervals = [(d_objs[i+1] - d_objs[i]).days for i in range(len(d_objs)-1)]
            avg_int = sum(intervals) / len(intervals)
            freq = "weekly" if avg_int < 10 else "monthly" if avg_int < 40 else "quarterly" if avg_int < 100 else "annual"
        else:
            freq = "unknown"

        subs.append({
            "name": txs[0]["merchant"],
            "amount": round(avg, 2),
            "freq": freq,
            "count": len(txs),
            "last": dates[-1],
            "cat": txs[0]["category"],
            "account": txs[0]["account"],
        })

    subs.sort(key=lambda s: s["amount"], reverse=True)

    monthly_burn = sum(
        s["amount"] * (1 if s["freq"] == "monthly" else
                       4 if s["freq"] == "weekly" else
                       1/3 if s["freq"] == "quarterly" else
                       1/12 if s["freq"] == "annual" else 1)
        for s in subs
    )

    lines = [
        "# Recurring Subscriptions & Services",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Detected:** {len(subs)} recurring charges",
        f"**Estimated Monthly Burn:** ${monthly_burn:,.2f}",
        f"**Estimated Annual Burn:** ${monthly_burn * 12:,.2f}",
        "",
        "| # | Service | Amount | Frequency | Category | Last Charged | Account |",
        "|---|---------|--------|-----------|----------|--------------|---------|",
    ]
    for i, s in enumerate(subs, 1):
        lines.append(f"| {i} | {s['name']} | ${s['amount']:.2f} | {s['freq']} | {s['cat']} | {s['last']} | {s['account']} |")
    lines.append("")

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="CFO Agent — Weekly P&L Generator")
    parser.add_argument("--weeks", type=int, default=4, help="Number of weeks (default: 4)")
    parser.add_argument("--full", action="store_true", help="Generate full financial package")
    args = parser.parse_args()

    print(f"\n{'='*60}")
    print(f"  CFO Agent — Weekly P&L Generator")
    print(f"{'='*60}\n")

    # ── Load store configs ──
    config = json.loads(CONFIG_FILE.read_text())
    stores = config["stores"]

    # ── Calculate date boundaries ──
    week_boundaries = []
    for i in range(args.weeks - 1, -1, -1):
        monday, sunday = get_week_boundaries(i)
        week_boundaries.append((monday, sunday))

    earliest = str(week_boundaries[0][0])
    latest = str(week_boundaries[-1][1])
    days_needed = (datetime.now().date() - week_boundaries[0][0]).days + 7

    print(f"  Period: {earliest} to {latest}")
    print(f"  Weeks: {args.weeks}\n")

    # ── Pull Shopify Revenue ──
    print("  Pulling Shopify revenue...")
    all_revenue = []
    for store in stores:
        if store.get("status") == "locked":
            print(f"    {store['label']}: SKIPPED (locked)")
            continue

        token = get_shopify_token(store)
        if not token:
            print(f"    {store['label']}: FAILED (no token)")
            continue

        orders = fetch_shopify_orders(store, token, earliest, latest)
        rev_data = process_shopify_orders(orders, store["brand"], store["label"])
        all_revenue.extend(rev_data)
        total = sum(r["net_revenue"] for r in rev_data)
        print(f"    {store['label']}: {len(orders)} orders, ${total:,.2f} net revenue")

    # ── Pull Bank Data ──
    print(f"\n  Pulling bank transactions ({days_needed} days)...")
    raw_accounts = fetch_bank_transactions(days=min(days_needed, 90))
    all_expenses, balances = parse_bank_data(raw_accounts)
    print(f"    {len(all_expenses)} transactions from {len(balances)} accounts")

    # ── Generate P&L ──
    print(f"\n  Generating reports...")

    pnl = generate_pnl(all_revenue, all_expenses, balances, args.weeks, week_boundaries)
    pnl_file = REPORTS_DIR / f"weekly_pnl_{datetime.now().strftime('%Y%m%d')}.md"
    pnl_file.write_text(pnl)
    print(f"    P&L saved: {pnl_file.name}")

    if args.full:
        # Expense detail sheet
        exp_sheet = generate_expense_sheet(all_expenses, week_boundaries[0][0], week_boundaries[-1][1])
        exp_file = REPORTS_DIR / f"expense_detail_{datetime.now().strftime('%Y%m%d')}.md"
        exp_file.write_text(exp_sheet)
        print(f"    Expenses saved: {exp_file.name}")

        # Subscription sheet
        sub_sheet = generate_subscription_sheet(all_expenses)
        sub_file = REPORTS_DIR / f"subscriptions_{datetime.now().strftime('%Y%m%d')}.md"
        sub_file.write_text(sub_sheet)
        print(f"    Subscriptions saved: {sub_file.name}")

    print(f"\n{'='*60}")
    print(pnl)
    print(f"\n  All reports saved to: {REPORTS_DIR}/")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
