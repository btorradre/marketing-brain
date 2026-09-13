#!/usr/bin/env python3
"""
Supplier statements → data/supplier_bills.json (+ optional inventory_purchase ledger rows).

Reads every spreadsheet in finances/supplier invoices/. Each is a per-order bill from the
manufacturer (Haikou Genyangkai): columns Order | SKU | Product name | Quantity | Country | Total cost,
a "Total amount" footer, and occasionally extra footer rows (e.g. "4 Influener orders").

Brand is inferred from the SKU prefix (config below) and the filename; bill date from the
filename's M.D token (year = --year, default current year). Every bill records: file, brand,
date, order range, line count, units, product total, extras (influencer orders etc.), grand total,
per-SKU cost summary. This is the COGS TRUTH used to cross-check Shopify cost-per-item and the
supplier wires on the bank side.

Usage:
  python3 supplier_bills.py                # parse all, write data/supplier_bills.json, print summary
  python3 supplier_bills.py --year 2026
  python3 supplier_bills.py --to-ledger    # also emit inventory_purchase rows (source=supplier_bill:<file>)
"""
import os, re, sys, glob, argparse, datetime as dt
from collections import defaultdict
from fin_common import *  # noqa

SKU_BRAND = [  # (regex on first SKU token, brand)
    (r"^bro0\d\d", "Velantra"), (r"^xwp", "Velantra"), (r"^brook5", "Motilli"), (r"^brook\b", "Motilli"),
    (r"^bro023", "Motilli"),
]
FILE_BRAND = [(r"motilli", "Motilli"), (r"velantra", "Velantra"), (r"lunessa", "Lunessa")]


def infer_brand(skus, fname):
    for pat, b in FILE_BRAND:
        if re.search(pat, fname, re.I): return b
    votes = defaultdict(int)
    for sku in skus:
        for pat, b in SKU_BRAND:
            if re.match(pat, sku, re.I): votes[b] += 1; break
    return max(votes, key=votes.get) if votes else None


def bill_date(fname, year):
    m = re.search(r"(\d{1,2})\.(\d{1,2})", fname)
    if not m: return None
    try:
        return dt.date(year, int(m.group(1)), int(m.group(2))).isoformat()
    except ValueError:
        return None


def parse_bill(path, year):
    import openpyxl
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb.worksheets[0]
    rows = list(ws.iter_rows(values_only=True))
    if not rows: return None
    hdr = [str(c).strip().lower() if c else "" for c in rows[0]]
    def col(*names):
        for n in names:
            if n in hdr: return hdr.index(n)
        return None
    c_order, c_sku, c_name, c_qty, c_cost = col("order"), col("sku", "product name"), col("product name"), col("quantity"), col("total cost", "cost")
    lines, extras, total = [], [], None
    sku_cost, sku_units = defaultdict(float), defaultdict(int)
    for r in rows[1:]:
        cells = list(r)
        if not any(c is not None for c in cells): continue
        if any(isinstance(c, str) and "total amount" in c.lower() for c in cells):
            nums = [c for c in cells if isinstance(c, (int, float))]
            total = float(nums[-1]) if nums else None
            continue
        if c_order is not None and cells[c_order] is None:
            note = " ".join(str(c) for c in cells if isinstance(c, str))
            nums = [c for c in cells if isinstance(c, (int, float))]
            extras.append({"note": note.strip(), "qty": nums[0] if len(nums) > 1 else None, "amount": float(nums[-1]) if nums else 0.0})
            continue
        try:
            cost = float(cells[c_cost]) if c_cost is not None and cells[c_cost] is not None else 0.0
        except (TypeError, ValueError):
            cost = 0.0
        qty = cells[c_qty] if c_qty is not None else None
        try: qty = int(qty) if qty is not None else 0
        except (TypeError, ValueError): qty = 0
        skus = [s.strip() for s in str(cells[c_sku] or "").split("\n") if s.strip()] if c_sku is not None else []
        lines.append({"order": cells[c_order] if c_order is not None else None, "skus": skus, "qty": qty, "cost": cost})
        if skus:
            share = cost / len(skus)
            for s in skus:
                key = re.sub(r"[*].*$", "", s.split("-")[0]).strip().lower() or s
                sku_cost[s] += share; sku_units[s] += max(1, qty // len(skus))
    line_total = round(sum(l["cost"] for l in lines), 2)
    extra_total = round(sum(e["amount"] for e in extras), 2)
    orders = [l["order"] for l in lines if isinstance(l["order"], (int, float))]
    all_skus = [s for l in lines for s in l["skus"]]
    fname = os.path.basename(path)
    return {"file": fname, "brand": infer_brand(all_skus, fname), "date": bill_date(fname, year),
            "month": (bill_date(fname, year) or "")[:7] or None,
            "order_min": min(orders) if orders else None, "order_max": max(orders) if orders else None,
            "lines": len(lines), "units": sum(l["qty"] for l in lines), "line_total": line_total,
            "extras": extras, "extra_total": extra_total, "grand_total": total if total is not None else round(line_total + extra_total, 2),
            "reconciles": (abs((total or 0) - (line_total + extra_total)) < 1.0) if total is not None else None,
            "top_skus": sorted(({"sku": s, "cost": round(c, 2), "units": sku_units[s]} for s, c in sku_cost.items()),
                               key=lambda x: -x["cost"])[:8]}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--year", type=int, default=dt.date.today().year, help="year for M.D filename dates")
    ap.add_argument("--dir", default=SUPPLIER_DIR)
    ap.add_argument("--to-ledger", action="store_true", help="emit inventory_purchase rows into the transactions table (locked)")
    args = ap.parse_args()

    bills = []
    for p in sorted(glob.glob(os.path.join(args.dir, "*.xlsx"))):
        if os.path.basename(p).startswith("~$"): continue
        try:
            b = parse_bill(p, args.year)
        except Exception as e:
            print(f"  ERROR {os.path.basename(p)}: {e}"); continue
        if b: bills.append(b)
    out = {"generated_at": now_iso(), "year_assumed": args.year, "bills": bills}
    save_json(BILLS, out)

    print(f"{len(bills)} supplier bills → {BILLS}\n")
    print(f"{'file':46} {'brand':9} {'date':10} {'orders':13} {'lines':>5} {'units':>6} {'total':>11} ok")
    by_brand_month = defaultdict(float)
    for b in bills:
        rng = f"{b['order_min']}-{b['order_max']}" if b["order_min"] is not None else "-"
        print(f"{b['file'][:46]:46} {str(b['brand']):9} {str(b['date']):10} {rng:13} {b['lines']:5d} {b['units']:6d} {b['grand_total']:11,.2f} {'✓' if b['reconciles'] else ('?' if b['reconciles'] is None else '✗')}")
        if b["month"]: by_brand_month[(b["brand"], b["month"])] += b["grand_total"]
    print("\nBy brand × bill month:")
    for (br, mo), v in sorted(by_brand_month.items(), key=lambda kv: (kv[0][1], str(kv[0][0]))):
        print(f"  {mo}  {str(br):9} ${v:,.2f}")
    print(f"\nTOTAL billed: ${sum(b['grand_total'] for b in bills):,.2f}")

    if args.to_ledger:
        store = load_json(TXNS, {"transactions": [], "ingested_files": {}})
        existing = {t["id"] for t in store["transactions"]}
        n = 0
        for b in bills:
            if not b["date"] or not b["grand_total"]: continue
            desc = f"Supplier bill {b['file']} ; orders {b['order_min']}-{b['order_max']} ; {b['lines']} orders / {b['units']} units"
            t = {"id": txn_id(b["date"], b["grand_total"], desc, "supplier_bill"), "date": b["date"], "month": b["month"],
                 "account": "supplier statement", "source": f"supplier_bill:{b['file'][:24]}", "description": desc,
                 "merchant": "Haikou Genyangkai (bill)", "amount": b["grand_total"], "currency": "USD",
                 "source_file": b["file"], "hints": {"memo": "per-order supplier bill; memo/COGS cross-check, not a bank outflow"},
                 "category": "inventory_purchase", "brand": b["brand"], "cat_source": "supplier_bill", "confidence": 1.0, "locked": True}
            if t["id"] not in existing:
                store["transactions"].append(t); existing.add(t["id"]); n += 1
        store["updated_at"] = now_iso(); save_json(TXNS, store)
        print(f"\n+{n} inventory_purchase rows added to transactions (locked, source=supplier_bill:*)")


if __name__ == "__main__":
    main()
