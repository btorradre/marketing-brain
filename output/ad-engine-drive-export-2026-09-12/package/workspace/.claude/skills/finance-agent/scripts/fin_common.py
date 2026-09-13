#!/usr/bin/env python3
"""Shared paths, taxonomy access and helpers for the finance-agent skill.

Layout (all under `marketing brain/`):
  finances/inbox/                 drop zone for GPT 5.6 Sol raw exports (csv/json/xlsx)
  finances/inbox/processed/       ingested files are moved here (never re-read)
  finances/statements/            Apple Card PDFs
  finances/supplier invoices/     supplier bill spreadsheets (per-order cost lines)
  finances/finalized statements/  finished P&L workbooks + markdown
  .claude/skills/finance-agent/data/         transactions.json, supplier_bills.json, review_queue.json, decisions.json
  .claude/skills/shopify-financials/data/    expenses.json (the categorized ledger the P&L merges) + Shopify cache
"""
import os, re, sys, json, hashlib, datetime as dt

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
BRAIN = os.path.abspath(os.path.join(SKILL, "..", "..", ".."))
FIN = os.path.join(BRAIN, "finances")
INBOX = os.path.join(FIN, "inbox")
PROCESSED = os.path.join(INBOX, "processed")
STATEMENTS = os.path.join(FIN, "statements")
SUPPLIER_DIR = os.path.join(FIN, "supplier invoices")
FINAL_DIR = os.path.join(FIN, "finalized statements")
DATA = os.path.join(SKILL, "data")
CONFIG = os.path.join(SKILL, "config")
RULES = os.path.join(CONFIG, "vendor_rules.json")
TXNS = os.path.join(DATA, "transactions.json")
BILLS = os.path.join(DATA, "supplier_bills.json")
QUEUE = os.path.join(DATA, "review_queue.json")
DECISIONS = os.path.join(DATA, "decisions.json")

SF_SKILL = os.path.join(BRAIN, ".claude", "skills", "shopify-financials")
SF_SCRIPTS = os.path.join(SF_SKILL, "scripts")
SF_DATA = os.path.join(SF_SKILL, "data")
LEDGER = os.path.join(SF_DATA, "expenses.json")
SHOPIFY_CACHE = os.path.join(SF_DATA, "monthly_shopify.json")

sys.path.insert(0, SF_SCRIPTS)
from import_expenses import CATEGORIES, BUCKETS, ALIASES, norm_category  # noqa: E402

BRANDS = ["Velantra", "Motilli", "Lunessa", "Solorna", "Renavita", "Orelli", "Avelle", "Wend", "Foliara"]

# source-tag prefixes that count as "the bank export covers this month" (mirrors build_pl_workbook.BANK_SRC)
BANK_SRC = ("business_gold", "business_platinum", "checking", "business_checking", "simplefin")


def load_json(path, default):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return default


def save_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp, path)


def now_iso():
    return dt.datetime.now().isoformat(timespec="seconds")


def parse_date(v):
    """Accepts datetime/date, 'YYYY-MM-DD', 'MM/DD/YYYY', 'M/D/YY', 'Mon D, YYYY'. Returns 'YYYY-MM-DD' or None."""
    if v is None or v == "":
        return None
    if isinstance(v, dt.datetime):
        return v.date().isoformat()
    if isinstance(v, dt.date):
        return v.isoformat()
    s = str(v).strip()
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%m/%d/%Y", "%m/%d/%y", "%b %d, %Y", "%B %d, %Y", "%d %b %Y", "%Y/%m/%d"):
        try:
            return dt.datetime.strptime(s[:len(fmt) + 6] if "T" in fmt else s, fmt).date().isoformat()
        except ValueError:
            continue
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})", s)
    return f"{m.group(1)}-{m.group(2)}-{m.group(3)}" if m else None


def parse_amount(v):
    """'$1,234.56' / '(12.00)' / '-12' / 12.0 -> float. Parentheses = negative."""
    if v is None or v == "":
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip().replace(",", "").replace("$", "").replace("USD", "").strip()
    neg = s.startswith("(") and s.endswith(")")
    s = s.strip("()")
    try:
        x = float(s)
    except ValueError:
        return None
    return -x if neg else x


def account_tag(name):
    """'Business Platinum Card®' -> business_platinum · 'BUSINESS CHECKING ...0189' -> business_checking_0189"""
    s = str(name or "").lower().replace("®", "").replace("card", "")
    s = re.sub(r"\(\s*\d{4}\s*\)", " ", s)          # SimpleFIN appends "(3009)"; the last-4 is already in "...3009" when present
    s = s.encode("ascii", "ignore").decode()
    last4 = re.search(r"(\d{4})\b", s)
    s = re.sub(r"[^a-z]+", "_", s).strip("_")
    s = re.sub(r"_+", "_", s)
    if last4 and last4.group(1) not in s:
        s = f"{s}_{last4.group(1)}" if s else last4.group(1)
    return s or "unknown"


def clean_merchant(desc):
    """Strip transaction noise so rules match the vendor: card-network prefixes, store numbers, addresses, zips."""
    s = str(desc or "")
    s = re.sub(r"^(TST\*|SQ \*|SQ\*|PP\*|PAYPAL \*|APLPAY |APPLE PAY |RECURRING PAYMENT AUTHORIZED ON \d\d/\d\d |PURCHASE AUTHORIZED ON \d\d/\d\d )", "", s, flags=re.I)
    s = re.sub(r"\s+(#|No\.?)\s*\d+\b", " ", s)
    s = re.sub(r"\b\d{5}(-\d{4})?\b", " ", s)             # zips
    s = re.sub(r"\b[A-Z]{2}\s+USA\b", " ", s)               # state + USA
    s = re.sub(r"\s{2,}", " ", s).strip(" ;,-")
    return s


def txn_id(date, amount, description, account):
    key = f"{date}|{amount:.2f}|{re.sub(r'\s+', ' ', str(description).lower().strip())}|{account}"
    return hashlib.sha1(key.encode()).hexdigest()[:16]


def month_of(date):
    return date[:7] if date else None
