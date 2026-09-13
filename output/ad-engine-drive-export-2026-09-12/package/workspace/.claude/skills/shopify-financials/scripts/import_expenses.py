#!/usr/bin/env python3
"""
Expense importer — the ChatGPT side of the P&L.

ChatGPT (or any tool) exports bank/card/expense data as CSV or JSON in the
schema below (see references/chatgpt-interop.md for the exact prompt to give
ChatGPT). This script validates it, maps categories to P&L lines, dedupes,
and merges it into the persistent ledger at data/expenses.json. monthly_pl.py
then folds the ledger into the month-by-month P&L.

Input schema (CSV columns or JSON keys, one row per transaction):
  date         YYYY-MM-DD  (or supply `month` as YYYY-MM instead)
  description  free text (merchant / memo)
  amount       positive number = money OUT (expense). For other_income,
               positive = money IN. Negative = refund/credit on that line.
  category     one of the canonical categories (aliases accepted, see below)
  brand        optional: Motilli | Velantra | Lunessa | Solorna | Avelle | Orelli | blank=company-wide
  source       optional: which account it came from (e.g. chase_checking, amex)

Usage:
  python3 import_expenses.py --file ~/Downloads/expenses_june.csv
  python3 import_expenses.py --file expenses.json --dry-run
  python3 import_expenses.py --file expenses.csv --replace-months 2026-05,2026-06
  python3 import_expenses.py --summary            # show ledger by month x category
  python3 import_expenses.py --clear              # wipe the ledger (asks via flag only)
"""
import json, os, sys, csv, io, re, argparse, hashlib, datetime as dt
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(os.path.dirname(HERE), "data", "expenses.json")

# ---------------------------------------------------------------- categories
# section: where the line lands on the P&L. "memo" = shown but excluded from profit.
CATEGORIES = {
    # revenue
    "other_income":       {"section": "revenue", "bucket": "revenue",   "label": "Other income (imported)"},
    # cogs
    "fulfillment_3pl":    {"section": "cogs", "bucket": "cogs",         "label": "Fulfillment / 3PL / pick-pack"},
    "freight_duties":     {"section": "cogs", "bucket": "cogs",         "label": "Inbound freight / duties"},
    # opex — MARKETING bucket
    "ad_spend_meta":      {"section": "opex", "bucket": "marketing",    "label": "Ad spend — Meta"},
    "ad_spend_google":    {"section": "opex", "bucket": "marketing",    "label": "Ad spend — Google"},
    "ad_spend_tiktok":    {"section": "opex", "bucket": "marketing",    "label": "Ad spend — TikTok"},
    "ad_spend_other":     {"section": "opex", "bucket": "marketing",    "label": "Ad spend — other"},
    "marketing_software": {"section": "opex", "bucket": "marketing",    "label": "Marketing tools (email/SMS, ad intel, creative software)"},
    "creators_influencers": {"section": "opex", "bucket": "marketing",  "label": "Creators / influencers / UGC"},
    # opex — AI bucket
    "ai_tools":           {"section": "opex", "bucket": "ai",           "label": "AI tools & models (LLMs, image/video/voice gen)"},
    # opex — OPERATING bucket
    "shipping_postage":   {"section": "opex", "bucket": "operating",    "label": "Shipping labels / postage"},
    "software_saas":      {"section": "opex", "bucket": "operating",    "label": "Software / apps / SaaS (non-AI, non-marketing)"},
    "contractors_agency": {"section": "opex", "bucket": "operating",    "label": "Agency / contractors / VAs / editors"},
    "payroll":            {"section": "opex", "bucket": "operating",    "label": "Payroll"},
    "merchant_fees":      {"section": "opex", "bucket": "operating",    "label": "Merchant / bank fees (non-Shopify)"},
    "chargeback_services": {"section": "opex", "bucket": "operating",   "label": "Chargeback management (Disputifier etc.)"},
    "legal_professional": {"section": "opex", "bucket": "operating",    "label": "Legal / accounting / professional"},
    "taxes_gov":          {"section": "opex", "bucket": "operating",    "label": "Taxes & government fees"},
    "interest_expense":   {"section": "opex", "bucket": "operating",    "label": "Interest expense"},
    "travel":             {"section": "opex", "bucket": "operating",    "label": "Travel"},
    "meals_entertainment": {"section": "opex", "bucket": "operating",   "label": "Meals & entertainment"},
    "office_misc":        {"section": "opex", "bucket": "operating",    "label": "Office / misc"},
    "other_opex":         {"section": "opex", "bucket": "operating",    "label": "Other operating"},
    # memo — visible, excluded from profit
    "inventory_purchase": {"section": "memo", "bucket": "excluded",     "label": "Inventory — supplier payments/wires (COGS line under cash basis)"},
    "owner_draw":         {"section": "memo", "bucket": "excluded",     "label": "Owner draws (excluded)"},
    "transfer":           {"section": "memo", "bucket": "excluded",     "label": "Transfers between accounts (excluded)"},
    "cc_payment":         {"section": "memo", "bucket": "excluded",     "label": "Credit-card payments (excluded — spend booked at transaction)"},
    "loan_principal":     {"section": "memo", "bucket": "excluded",     "label": "Loan principal (excluded — book interest separately)"},
    "income_tax":         {"section": "memo", "bucket": "excluded",     "label": "Income tax payments — IRS / FTB (excluded — P&L is pre-tax)"},
}

# Executive P&L rollup buckets (finance-agent). Order = presentation order.
BUCKETS = {
    "revenue":   "Revenue",
    "cogs":      "Cost of goods sold",
    "marketing": "Marketing",
    "ai":        "AI",
    "operating": "Operating",
    "excluded":  "Excluded from profit",
}

ALIASES = {
    "meta": "ad_spend_meta", "facebook": "ad_spend_meta", "fb": "ad_spend_meta", "facebook_ads": "ad_spend_meta",
    "google": "ad_spend_google", "google_ads": "ad_spend_google", "adwords": "ad_spend_google",
    "tiktok": "ad_spend_tiktok", "tiktok_ads": "ad_spend_tiktok",
    "ads": "ad_spend_other", "ad_spend": "ad_spend_other", "advertising": "ad_spend_other",
    "3pl": "fulfillment_3pl", "fulfillment": "fulfillment_3pl", "pick_pack": "fulfillment_3pl",
    "freight": "freight_duties", "duties": "freight_duties", "customs": "freight_duties",
    "shipping": "shipping_postage", "postage": "shipping_postage", "labels": "shipping_postage",
    "software": "software_saas", "saas": "software_saas", "apps": "software_saas", "subscriptions": "software_saas",
    "contractor": "contractors_agency", "contractors": "contractors_agency", "agency": "contractors_agency",
    "freelance": "contractors_agency", "freelancer": "contractors_agency", "va": "contractors_agency",
    "wages": "payroll", "salary": "payroll", "salaries": "payroll",
    "disputifier": "chargeback_services", "chargeflow": "chargeback_services", "chargebacks911": "chargeback_services",
    "bank_fees": "merchant_fees", "bank_fee": "merchant_fees", "processing_fees": "merchant_fees",
    "stripe_fees": "merchant_fees", "paypal_fees": "merchant_fees", "wire_fee": "merchant_fees",
    "legal": "legal_professional", "accounting": "legal_professional", "bookkeeping": "legal_professional",
    "cpa": "legal_professional", "professional": "legal_professional",
    "tax": "taxes_gov", "taxes": "taxes_gov", "sales_tax": "taxes_gov", "franchise_tax": "taxes_gov",
    "interest": "interest_expense",
    "meals": "meals_entertainment", "dining": "meals_entertainment", "entertainment": "meals_entertainment",
    "uber": "travel", "flights": "travel", "hotels": "travel", "gas": "travel",
    "office": "office_misc", "misc": "office_misc", "miscellaneous": "office_misc", "supplies": "office_misc",
    "other": "other_opex", "uncategorized": "other_opex", "unknown": "other_opex",
    "inventory": "inventory_purchase", "cogs": "inventory_purchase", "product_cost": "inventory_purchase",
    "manufacturer": "inventory_purchase", "supplier": "inventory_purchase",
    "draw": "owner_draw", "owner": "owner_draw", "distribution": "owner_draw",
    "transfers": "transfer", "internal_transfer": "transfer",
    "credit_card_payment": "cc_payment", "card_payment": "cc_payment",
    "loan": "loan_principal", "loan_payment": "loan_principal",
    "ai": "ai_tools", "ai_tool": "ai_tools", "llm": "ai_tools", "ai_software": "ai_tools", "ai_subscriptions": "ai_tools",
    "marketing_tools": "marketing_software", "marketing_saas": "marketing_software", "email_sms": "marketing_software",
    "ad_tools": "marketing_software", "creative_software": "marketing_software",
    "creators": "creators_influencers", "influencers": "creators_influencers", "ugc": "creators_influencers",
    "creator": "creators_influencers", "influencer": "creators_influencers",
    "irs": "income_tax", "income_taxes": "income_tax", "estimated_tax": "income_tax",
    "income": "other_income", "revenue_other": "other_income", "refund_income": "other_income",
}

KNOWN_BRANDS = {"motilli", "velantra", "lunessa", "solorna", "avelle", "orelli", "renavita", "wend", "foliara"}


def norm_category(raw):
    key = re.sub(r"[^a-z0-9]+", "_", str(raw or "").strip().lower()).strip("_")
    if key in CATEGORIES: return key
    if key in ALIASES: return ALIASES[key]
    return None


def entry_id(month, amount, description, category, source):
    h = hashlib.sha1(f"{month}|{amount:.2f}|{description.lower().strip()}|{category}|{source}".encode())
    return h.hexdigest()[:16]


def load_ledger():
    if os.path.exists(LEDGER):
        with open(LEDGER) as f:
            return json.load(f)
    return {"entries": []}


def save_ledger(ledger):
    os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
    ledger["updated_at"] = dt.datetime.now().isoformat(timespec="seconds")
    with open(LEDGER, "w") as f:
        json.dump(ledger, f, indent=2)
        f.write("\n")


# ---------------------------------------------------------------- parsing
def parse_rows(path):
    """Yield raw dict rows from a CSV or JSON file (JSON may be a list or {'entries': [...]})"""
    text = open(path, encoding="utf-8-sig").read()
    if path.lower().endswith(".json") or text.lstrip()[:1] in "[{":
        data = json.loads(text)
        if isinstance(data, dict): data = data.get("entries") or data.get("expenses") or data.get("transactions") or []
        for i, row in enumerate(data, 1):
            yield i, row
    else:
        for i, row in enumerate(csv.DictReader(io.StringIO(text)), 2):  # row 1 = header
            yield i, {k.strip().lower(): (v.strip() if isinstance(v, str) else v) for k, v in row.items() if k}


def normalize(rowno, row, errors):
    def err(msg):
        errors.append(f"  row {rowno}: {msg}  ->  {json.dumps(row, default=str)[:140]}")
        return None

    # month
    month, date = None, str(row.get("date") or "").strip()
    if date:
        m = re.match(r"^(\d{4})-(\d{2})(-(\d{2}))?", date)
        if not m: return err(f"bad date '{date}' (want YYYY-MM-DD)")
        month = f"{m.group(1)}-{m.group(2)}"
    else:
        raw_m = str(row.get("month") or "").strip()
        if not re.match(r"^\d{4}-\d{2}$", raw_m): return err("need `date` (YYYY-MM-DD) or `month` (YYYY-MM)")
        month = raw_m

    # amount
    try:
        amount = float(str(row.get("amount", "")).replace(",", "").replace("$", "").strip())
    except ValueError:
        return err(f"bad amount '{row.get('amount')}'")

    # category
    cat = norm_category(row.get("category"))
    if not cat:
        return err(f"unknown category '{row.get('category')}' — valid: {', '.join(sorted(CATEGORIES))}")

    desc = str(row.get("description") or row.get("memo") or row.get("merchant") or "").strip() or "(no description)"
    brand = str(row.get("brand") or "").strip()
    if brand and brand.lower() not in KNOWN_BRANDS:
        # not fatal — new brands appear; keep as-is but title-case it
        brand = brand.strip().title()
    elif brand:
        brand = brand.strip().title()
    source = str(row.get("source") or row.get("account") or "").strip()

    return {"id": entry_id(month, amount, desc, cat, source), "month": month,
            "date": date or None, "description": desc, "amount": round(amount, 2),
            "category": cat, "section": CATEGORIES[cat]["section"],
            "brand": brand or None, "source": source or None}


def print_summary(entries):
    by = defaultdict(float)
    months = sorted({e["month"] for e in entries})
    for e in entries: by[(e["month"], e["category"])] += e["amount"]
    print(f"\nLedger: {len(entries)} entries across {len(months)} month(s): {', '.join(months)}")
    for m in months:
        print(f"\n  {m}")
        mtot = 0.0
        for cat in sorted(CATEGORIES):
            v = by.get((m, cat))
            if v:
                sect = CATEGORIES[cat]["section"]
                tag = " (memo/excluded)" if sect == "memo" else ""
                print(f"    {CATEGORIES[cat]['label']:52} ${v:>12,.2f}{tag}")
                if sect in ("cogs", "opex"): mtot += v
                elif sect == "revenue": mtot -= v
        print(f"    {'— P&L-affecting total (costs − other income)':52} ${mtot:>12,.2f}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", help="CSV or JSON export (from ChatGPT or elsewhere)")
    ap.add_argument("--dry-run", action="store_true", help="validate + preview, don't write")
    ap.add_argument("--replace-months", help="comma-separated YYYY-MM list: drop existing ledger entries for these months before merging")
    ap.add_argument("--summary", action="store_true", help="print ledger summary and exit")
    ap.add_argument("--clear", action="store_true", help="wipe the entire ledger")
    args = ap.parse_args()

    ledger = load_ledger()

    if args.clear:
        n = len(ledger["entries"]); ledger["entries"] = []
        save_ledger(ledger); print(f"Cleared ledger ({n} entries removed).")
        return
    if args.summary or not args.file:
        print_summary(ledger["entries"]) if ledger["entries"] else print("Ledger is empty.")
        if not args.file: return

    errors, incoming = [], []
    for rowno, row in parse_rows(args.file):
        e = normalize(rowno, row, errors)
        if e: incoming.append(e)

    if errors:
        print(f"❌ {len(errors)} invalid row(s) — nothing imported. Fix and re-run:")
        print("\n".join(errors[:25]))
        if len(errors) > 25: print(f"  ... and {len(errors) - 25} more")
        sys.exit(1)

    if args.replace_months:
        drop = {m.strip() for m in args.replace_months.split(",")}
        before = len(ledger["entries"])
        ledger["entries"] = [e for e in ledger["entries"] if e["month"] not in drop]
        print(f"Dropped {before - len(ledger['entries'])} existing entries for months: {', '.join(sorted(drop))}")

    existing = {e["id"] for e in ledger["entries"]}
    new = [e for e in incoming if e["id"] not in existing]
    dupes = len(incoming) - len(new)

    print(f"Parsed {len(incoming)} rows — {len(new)} new, {dupes} duplicates skipped.")
    if args.dry_run:
        print_summary(new)
        print("\n(dry run — ledger not modified)")
        return

    ledger["entries"].extend(new)
    ledger["entries"].sort(key=lambda e: (e["month"], e["category"], e["description"]))
    save_ledger(ledger)
    print_summary(ledger["entries"])
    print(f"\nSaved ledger: {LEDGER}")


if __name__ == "__main__":
    main()
