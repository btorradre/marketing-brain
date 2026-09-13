#!/usr/bin/env python3
"""
Transaction Analyzer — CFO Agent (SimpleFIN)
Pulls transactions from all connected bank accounts via SimpleFIN API,
detects subscriptions, generates spending reports.

Usage:
    python3 pull_transactions.py                # Summary
    python3 pull_transactions.py --subs         # Subscriptions only
    python3 pull_transactions.py --report       # Full spending report
    python3 pull_transactions.py --days 30      # Last 30 days (default: 90)
    python3 pull_transactions.py --json         # Raw JSON output
"""

import argparse
import base64
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv

# Load .env from project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(PROJECT_ROOT / ".env")

DATA_DIR = Path(__file__).parent / "data"
TX_DIR = DATA_DIR / "transactions"
REPORTS_DIR = DATA_DIR / "reports"

SIMPLEFIN_ACCESS_URL = os.getenv("SIMPLEFIN_ACCESS_URL")
if not SIMPLEFIN_ACCESS_URL:
    print("ERROR: SIMPLEFIN_ACCESS_URL not set in .env")
    sys.exit(1)


# ─── SimpleFIN API ─────────────────────────────────────────────

def fetch_accounts(days=90):
    """Pull all accounts + transactions from SimpleFIN via curl."""
    start_ts = int((datetime.now() - timedelta(days=days)).timestamp())
    url = f"{SIMPLEFIN_ACCESS_URL}/accounts?start-date={start_ts}"

    result = subprocess.run(
        ["curl", "-s", url],
        capture_output=True, text=True, timeout=60
    )

    if result.returncode != 0:
        print(f"  curl error: {result.stderr}")
        sys.exit(1)

    data = json.loads(result.stdout)
    return data.get("accounts", []), data.get("errors", [])


# ─── Transaction Parsing ──────────────────────────────────────

def parse_accounts(raw_accounts):
    """Convert SimpleFIN accounts into normalized transactions."""
    all_transactions = []
    account_summaries = []

    for acc in raw_accounts:
        org_name = acc.get("org", {}).get("name", "Unknown Bank")
        acc_name = acc.get("name", "Unknown Account")
        balance = float(acc.get("balance", 0))
        available = float(acc.get("available-balance", 0))

        account_summaries.append({
            "id": acc.get("id", ""),
            "name": acc_name,
            "bank": org_name,
            "balance": balance,
            "available": available,
        })

        for tx in acc.get("transactions", []):
            posted = tx.get("posted") or tx.get("transacted_at")
            if not posted:
                continue

            date_str = datetime.fromtimestamp(posted).strftime("%Y-%m-%d")
            raw_desc = tx.get("description", "").strip()
            payee = tx.get("payee", "").strip()
            amount = float(tx.get("amount", 0))

            # Use payee if available, otherwise clean the raw description
            merchant = payee if payee else clean_merchant_name(raw_desc)

            all_transactions.append({
                "date": date_str,
                "name": merchant,
                "merchant_name": merchant,
                "amount": -amount,  # SimpleFIN: negative = charge, flip to positive = money out
                "category": categorize_by_name(merchant or raw_desc),
                "source": f"{org_name} — {acc_name}",
                "raw_description": raw_desc,
                "tx_id": tx.get("id", ""),
            })

    return all_transactions, account_summaries


# ─── Merchant Name Cleaning ───────────────────────────────────

def clean_merchant_name(raw):
    """Clean up bank merchant descriptions to readable names."""
    name = raw.strip()

    prefixes = [
        "PURCHASE AUTHORIZED ON", "RECURRING PAYMENT AUTHORIZED ON",
        "RECURRING PAYMENT", "ONLINE PAYMENT AUTHORIZED ON",
        "DEBIT CARD PURCHASE", "POS PURCHASE", "ACH DEBIT", "ACH CREDIT",
        "ONLINE TRANSFER", "BILL PAY", "PAYMENT TO", "DIRECT PAY",
        "BUSINESS TO BUSINESS ACH", "SQ *", "TST* ",
        "AMZN MKTP US*", "AMZN Mktp US", "Amazon.com*",
        "PAYPAL *", "VENMO *", "ZELLE ",
    ]
    for prefix in prefixes:
        if name.upper().startswith(prefix.upper()):
            name = name[len(prefix):].strip()

    # Remove trailing transaction IDs, dates, card numbers, whitespace junk
    name = re.sub(r'\s+AUTHORIZED ON\s+\d{2}/\d{2}', '', name)
    name = re.sub(r'\s+\d{2}/\d{2}\s*$', '', name)
    name = re.sub(r'\s+CARD\s+\d+\s*$', '', name)
    name = re.sub(r'\s+S\d{10,}\s*$', '', name)
    name = re.sub(r'\s+#\d+\s*$', '', name)
    name = re.sub(r'\s+x{2,}\d+\s*$', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\s+X{5,}\s*$', '', name)
    name = re.sub(r'\s+\d{10,}\s*$', '', name)
    name = re.sub(r'\s{2,}', ' ', name)  # collapse whitespace

    # Remove city/state suffixes
    name = re.sub(r'\s+[A-Z]{2}\s*$', '', name)
    name = re.sub(r'\s+\d{5}(-\d{4})?\s*$', '', name)

    # Take just the first meaningful chunk before long ID strings
    parts = name.split()
    cleaned = []
    for p in parts:
        if len(p) > 12 and p.isalnum() and not p.isalpha():
            break  # stop at long alphanumeric IDs
        cleaned.append(p)

    result = " ".join(cleaned).strip()
    return result if result else raw.strip()[:50]


# ─── Category Detection ───────────────────────────────────────

CATEGORY_RULES = {
    "Subscription/SaaS": [
        "netflix", "spotify", "hulu", "disney", "hbo", "apple.com/bill",
        "youtube", "amazon prime", "adobe", "dropbox", "google storage",
        "openai", "chatgpt", "anthropic", "claude", "notion", "slack",
        "zoom", "canva", "figma", "github", "heroku", "vercel", "aws",
        "digitalocean", "linode", "vultr", "cloudflare", "namecheap", "godaddy",
        "semrush", "ahrefs", "mailchimp", "convertkit", "klaviyo",
        "shopify", "zapier", "make.com", "n8n", "apify", "phantombuster",
        "elevenlabs", "midjourney", "runway", "fal.ai", "replicate",
        "cursor", "replit", "1password", "nordvpn", "expressvpn",
        "grammarly", "jasper", "copy.ai", "surfer", "descript",
        "loom", "calendly", "typeform", "webflow", "squarespace",
        "wix", "siteground", "bluehost", "intercom", "crisp",
        "hubspot", "salesforce", "pipedrive", "monday.com", "asana",
        "linear", "superhuman", "hey.com", "fastmail", "proton",
        "paramount", "peacock", "crunchyroll", "audible", "kindle",
        "xbox", "playstation", "steam", "twitch", "patreon",
        "substack", "medium", "nytimes", "wsj", "economist",
        "headspace", "calm", "peloton", "strava", "myfitnesspal",
        "icloud", "google one", "microsoft 365", "office 365",
        "creative cloud", "acrobat", "lightroom", "premiere",
        "gethookd", "kling", "fal", "pinecone", "openrouter",
        "skool", "gumroad", "teachable", "thinkific", "kajabi",
        "wise", "mercury", "brex", "ramp",
        "name-cheap", "simple fin", "simplefin",
        "perplexity", "copilot", "gemini",
    ],
    "Advertising": [
        "facebook", "meta platforms", "fb ads", "facebk", "meta ",
        "google ads", "adwords", "tiktok", "snap inc", "pinterest ads",
        "bing ads", "microsoft advertising", "taboola", "outbrain",
    ],
    "E-commerce/Shopify": [
        "shopify",
    ],
    "Food & Dining": [
        "doordash", "uber eats", "grubhub", "postmates",
        "mcdonald", "starbucks", "chipotle", "chick-fil-a",
        "subway", "taco bell", "wendy", "panera", "domino",
        "pizza hut", "five guys", "in-n-out", "shake shack",
        "restaurant", "cafe", "diner", "grill", "kitchen",
        "sushi", "thai", "mexican", "italian", "burger",
        "h-e-b", "heb ", "kroger", "publix", "whole foods",
        "trader joe", "aldi", "safeway", "costco",
    ],
    "Shopping": [
        "amazon", "walmart", "target", "best buy",
        "home depot", "lowes", "ikea", "wayfair", "etsy",
        "ebay", "aliexpress", "shein", "zara", "h&m",
        "nike", "adidas", "apple store",
    ],
    "Transportation": [
        "uber ", "lyft", "shell", "chevron", "exxon", "bp ",
        "gas station", "parking", "toll", "transit", "tesla",
    ],
    "Utilities": [
        "electric", "gas co", "water ", "internet", "comcast",
        "at&t", "verizon", "t-mobile", "sprint", "spectrum",
        "cox ", "frontier", "centurylink",
    ],
    "Insurance": [
        "geico", "state farm", "allstate", "progressive",
        "liberty mutual", "insurance", "usaa",
    ],
    "Health": [
        "pharmacy", "cvs", "walgreens", "doctor", "medical",
        "dental", "hospital", "urgent care", "labcorp", "quest diag",
    ],
    "Transfer/Payment": [
        "zelle", "venmo", "paypal", "cash app", "wire transfer",
        "ach ", "transfer to", "transfer from",
    ],
}


def categorize_by_name(description):
    desc_lower = description.lower()
    for category, keywords in CATEGORY_RULES.items():
        for kw in keywords:
            if kw in desc_lower:
                return [category]
    return ["Uncategorized"]


# ─── Subscription Detection ───────────────────────────────────

def detect_subscriptions(transactions):
    """Detect recurring charges."""
    by_merchant = defaultdict(list)
    for tx in transactions:
        name = (tx["merchant_name"] or tx["name"]).strip()
        if name and tx["amount"] > 0:
            by_merchant[name.lower()].append(tx)

    subscriptions = []
    for merchant, txs in by_merchant.items():
        if len(txs) < 2:
            continue

        txs.sort(key=lambda t: t["date"])
        amounts = [t["amount"] for t in txs]
        dates = [t["date"] for t in txs]

        avg_amount = sum(amounts) / len(amounts)
        if avg_amount == 0:
            continue

        # Check consistency (within 30% — some services fluctuate)
        consistent = all(abs(a - avg_amount) / avg_amount < 0.30 for a in amounts)
        if not consistent:
            continue

        # Estimate frequency
        if len(dates) >= 2:
            date_objs = [datetime.strptime(d, "%Y-%m-%d") for d in dates]
            intervals = [(date_objs[i+1] - date_objs[i]).days for i in range(len(date_objs)-1)]
            avg_interval = sum(intervals) / len(intervals)

            if avg_interval < 10:
                freq = "weekly"
            elif avg_interval < 40:
                freq = "monthly"
            elif avg_interval < 100:
                freq = "quarterly"
            else:
                freq = "annual"
        else:
            freq = "unknown"

        display_name = txs[0]["merchant_name"] or txs[0]["name"]
        subscriptions.append({
            "name": display_name,
            "avg_amount": round(avg_amount, 2),
            "frequency": freq,
            "occurrences": len(txs),
            "last_charge": dates[-1],
            "first_charge": dates[0],
            "category": txs[0].get("category", []),
            "source": txs[0].get("source", ""),
        })

    subscriptions.sort(key=lambda s: s["avg_amount"], reverse=True)
    return subscriptions


# ─── Report Generation ────────────────────────────────────────

def generate_report(all_transactions, account_summaries, subscriptions, days):
    now = datetime.now()
    dates = [tx["date"] for tx in all_transactions]
    min_date = min(dates) if dates else "N/A"
    max_date = max(dates) if dates else "N/A"

    lines = [
        f"# CFO Spending Report",
        f"**Generated:** {now.strftime('%Y-%m-%d %H:%M')}",
        f"**Period:** Last {days} days ({min_date} to {max_date})",
        f"**Accounts:** {len(account_summaries)}",
        f"**Transactions:** {len(all_transactions)}",
        "",
    ]

    # Account balances
    lines.append("## Account Balances\n")
    lines.append("| Bank | Account | Balance | Available |")
    lines.append("|------|---------|---------|-----------|")
    for acc in account_summaries:
        lines.append(f"| {acc['bank']} | {acc['name']} | ${acc['balance']:,.2f} | ${acc['available']:,.2f} |")
    total_balance = sum(a["balance"] for a in account_summaries)
    lines.append(f"| **TOTAL** | | **${total_balance:,.2f}** | |")
    lines.append("")

    # Spending summary
    charges = [tx for tx in all_transactions if tx["amount"] > 0]
    credits = [tx for tx in all_transactions if tx["amount"] < 0]
    total_out = sum(tx["amount"] for tx in charges)
    total_in = sum(abs(tx["amount"]) for tx in credits)

    lines.append("## Spending Summary\n")
    lines.append(f"- **Total Charges:** ${total_out:,.2f} ({len(charges)} transactions)")
    lines.append(f"- **Total Credits/Income:** ${total_in:,.2f} ({len(credits)} transactions)")
    lines.append(f"- **Net Cash Flow:** ${total_in - total_out:+,.2f}")
    lines.append("")

    # Category breakdown
    categories = defaultdict(float)
    for tx in charges:
        cat = tx["category"][0] if tx["category"] else "Uncategorized"
        categories[cat] += tx["amount"]
    sorted_cats = sorted(categories.items(), key=lambda x: x[1], reverse=True)

    lines.append("## Spending by Category\n")
    lines.append("| Category | Amount | % of Total |")
    lines.append("|----------|--------|------------|")
    for cat, amount in sorted_cats:
        pct = (amount / total_out * 100) if total_out > 0 else 0
        lines.append(f"| {cat} | ${amount:,.2f} | {pct:.1f}% |")
    lines.append("")

    # Subscriptions
    if subscriptions:
        monthly_burn = sum(
            s["avg_amount"] * (1 if s["frequency"] == "monthly" else
                               4 if s["frequency"] == "weekly" else
                               1/3 if s["frequency"] == "quarterly" else
                               1/12 if s["frequency"] == "annual" else 1)
            for s in subscriptions
        )

        lines.append("## Recurring Subscriptions\n")
        lines.append(f"**Estimated Monthly Subscription Burn: ${monthly_burn:,.2f}**\n")
        lines.append("| # | Service | Amount | Frequency | Last Charged | Account |")
        lines.append("|---|---------|--------|-----------|--------------|---------|")
        for i, sub in enumerate(subscriptions, 1):
            lines.append(
                f"| {i} | {sub['name']} | ${sub['avg_amount']:.2f} | {sub['frequency']} "
                f"| {sub['last_charge']} | {sub['source']} |"
            )
        lines.append("")

    # Top 25 charges
    top = sorted(charges, key=lambda t: t["amount"], reverse=True)[:25]
    lines.append("## Top 25 Largest Charges\n")
    lines.append("| Date | Merchant | Amount | Category | Account |")
    lines.append("|------|----------|--------|----------|---------|")
    for tx in top:
        cat = "/".join(tx["category"]) if tx["category"] else "—"
        lines.append(f"| {tx['date']} | {tx['merchant_name']} | ${tx['amount']:,.2f} | {cat} | {tx['source']} |")
    lines.append("")

    # Monthly trend
    by_month = defaultdict(float)
    for tx in charges:
        by_month[tx["date"][:7]] += tx["amount"]

    if by_month:
        lines.append("## Monthly Spending Trend\n")
        lines.append("| Month | Total Spent |")
        lines.append("|-------|-------------|")
        for month in sorted(by_month.keys()):
            lines.append(f"| {month} | ${by_month[month]:,.2f} |")
        lines.append("")

    return "\n".join(lines)


# ─── Main ─────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="CFO Agent — Bank Transaction Analyzer")
    parser.add_argument("--days", type=int, default=90, help="Days of history (default: 90)")
    parser.add_argument("--subs", action="store_true", help="Show subscriptions only")
    parser.add_argument("--report", action="store_true", help="Full spending report")
    parser.add_argument("--json", action="store_true", help="Raw JSON output")
    args = parser.parse_args()

    print(f"\nCFO Agent — Pulling transactions ({args.days} days)")
    print(f"Connecting to SimpleFIN...\n")

    raw_accounts, errors = fetch_accounts(days=args.days)
    if errors:
        print(f"  API Errors: {errors}")

    all_transactions, account_summaries = parse_accounts(raw_accounts)
    all_transactions.sort(key=lambda t: t["date"], reverse=True)

    print(f"  Accounts: {len(account_summaries)}")
    print(f"  Transactions: {len(all_transactions)}")

    # Cache raw data
    cache_file = TX_DIR / f"simplefin_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    cache_file.write_text(json.dumps({
        "pulled_at": datetime.now().isoformat(),
        "days": args.days,
        "accounts": account_summaries,
        "transactions": all_transactions,
    }, indent=2))

    subscriptions = detect_subscriptions(all_transactions)

    if args.subs:
        if args.json:
            print(json.dumps(subscriptions, indent=2))
        else:
            print(f"\n{'='*70}")
            print(f"  RECURRING SUBSCRIPTIONS ({len(subscriptions)} detected)")
            print(f"{'='*70}\n")
            monthly_burn = sum(
                s["avg_amount"] * (1 if s["frequency"] == "monthly" else
                                   4 if s["frequency"] == "weekly" else
                                   1/3 if s["frequency"] == "quarterly" else
                                   1/12 if s["frequency"] == "annual" else 1)
                for s in subscriptions
            )
            print(f"  Estimated Monthly Burn: ${monthly_burn:,.2f}\n")
            for i, sub in enumerate(subscriptions, 1):
                print(f"  {i:2d}. {sub['name']:<40} ${sub['avg_amount']:>8.2f}/{sub['frequency']}")
                print(f"      Last: {sub['last_charge']}  |  {sub['occurrences']}x  |  {sub['source']}")
            print()
        return

    if args.report:
        report = generate_report(all_transactions, account_summaries, subscriptions, args.days)
        report_file = REPORTS_DIR / f"spending_report_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
        report_file.write_text(report)
        print(f"\n{report}")
        print(f"\nReport saved: {report_file}")
        return

    # Default: summary
    if args.json:
        print(json.dumps({
            "accounts": account_summaries,
            "transactions": all_transactions,
            "subscriptions": subscriptions,
        }, indent=2))
    else:
        total_out = sum(tx["amount"] for tx in all_transactions if tx["amount"] > 0)
        total_in = sum(abs(tx["amount"]) for tx in all_transactions if tx["amount"] < 0)
        print(f"\n  Total Spent:  ${total_out:,.2f}")
        print(f"  Total In:     ${total_in:,.2f}")
        print(f"  Subscriptions: {len(subscriptions)} detected")
        print(f"\n  --subs    → subscription details")
        print(f"  --report  → full spending report\n")


if __name__ == "__main__":
    main()
