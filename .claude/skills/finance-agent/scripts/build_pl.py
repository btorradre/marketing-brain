#!/usr/bin/env python3
"""
Build the P&L: Shopify side (live or cached) + categorized ledger → Excel workbook + markdown + JSON.

  python3 build_pl.py --year 2026                # live Shopify pull for every store, then build
  python3 build_pl.py --year 2026 --from-cache   # no API calls (uses shopify-financials/data/monthly_shopify.json)
  python3 build_pl.py --since 2026-05 --until 2026-08 --cogs-basis cash

Outputs (finances/finalized statements/):
  PL_Monthly_<since>_to_<until>.xlsx   Executive P&L (buckets) + full P&L Monthly + brand tabs + ledger + data quality
  PL_<since>_to_<until>.md             the same executive view as markdown (paste into Notion / send to Brooks)
  PL_<since>_to_<until>.json           machine-readable executive numbers per month
"""
import os, re, sys, json, argparse, subprocess, datetime as dt
from collections import defaultdict
from fin_common import *  # noqa

EXEC_JSON = os.path.join(SF_DATA, "executive.json")


def money(v):
    if abs(v) < 0.005: return "$0"
    body = f"{abs(v):,.0f}" if abs(v) >= 1000 else f"{abs(v):,.2f}"
    return ("-$" if v < 0 else "$") + body
def pct(n, d): return f"{(n / d):.1%}" if d else "—"


def markdown(execd, months, extras):
    L = [f"# Executive P&L — {months[0]} → {months[-1]}", "",
         f"_Generated {dt.date.today().isoformat()} by finance-agent · COGS basis: {extras['cogs_basis']}_", ""]
    hdr = "| Line | " + " | ".join(months) + " | TOTAL |"
    sep = "|---|" + "---:|" * (len(months) + 1)
    def row(label, key, sign=1, bold=False):
        vals = [execd[m][key] * sign for m in months]
        lab = f"**{label}**" if bold else label
        cells = [f"**{money(v)}**" if bold else money(v) for v in vals]
        return f"| {lab} | " + " | ".join(cells) + f" | {'**' if bold else ''}{money(sum(vals))}{'**' if bold else ''} |"
    def pct_row(label, num, den):
        cells = [pct(execd[m][num], execd[m][den]) for m in months]
        tn, td = sum(execd[m][num] for m in months), sum(execd[m][den] for m in months)
        return f"| _{label}_ | " + " | ".join(cells) + f" | {pct(tn, td)} |"
    L += [hdr, sep,
          row("Revenue before refunds", "revenue_before_refunds"), row("Refunds / returns", "refunds", -1),
          row("NET REVENUE", "net_revenue", bold=True),
          row("Product COGS", "product_cogs", -1), row("3PL + freight", "cogs_3pl_freight", -1),
          row("GROSS PROFIT", "gross_profit", bold=True), pct_row("gross margin", "gross_profit", "net_revenue"),
          row("Marketing — paid ads", "marketing_ads", -1), row("Marketing — tools", "marketing_tools", -1),
          row("Marketing — creators", "marketing_creators", -1), row("TOTAL MARKETING", "marketing", bold=True),
          pct_row("marketing % of net revenue", "marketing", "net_revenue"),
          row("TOTAL AI", "ai", bold=True), pct_row("AI % of net revenue", "ai", "net_revenue"),
          row("Operating — Shopify fees", "shopify_fees", -1), row("Operating — chargebacks lost", "chargebacks_lost", -1),
          row("Operating — everything else", "operating_other", -1), row("TOTAL OPERATING", "operating", bold=True),
          pct_row("operating % of net revenue", "operating", "net_revenue"),
          row("NET PROFIT (pre-tax)", "net_profit", bold=True), pct_row("net margin", "net_profit", "net_revenue"), ""]
    L += ["## Data quality", ""]
    for n in extras["notes"]: L.append(f"- {n}")
    L += ["", "## Where the money went (ledger, this period)", ""]
    for bucket, vendors in extras["top_vendors"].items():
        L.append(f"**{bucket}** — " + ", ".join(f"{v} {money(a)}" for v, a in vendors[:8]))
    if extras.get("supplier"):
        L += ["", "## Supplier bills vs. booked COGS", "", "| Month | Supplier bills (statements) | Supplier wires (bank) | Product COGS on P&L |", "|---|---:|---:|---:|"]
        for m in months:
            s = extras["supplier"].get(m, {})
            L.append(f"| {m} | {money(s.get('bills', 0))} | {money(s.get('wires', 0))} | {money(execd[m]['product_cogs'])} |")
        L.append("")
        L.append("_Bills are dated by the statement's M.D filename (year assumed); wires are the bank outflows to the supplier; P&L COGS is accrual by order month. Expect timing gaps, not a match._")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--year", type=int); ap.add_argument("--since"); ap.add_argument("--until"); ap.add_argument("--months", type=int)
    ap.add_argument("--from-cache", action="store_true"); ap.add_argument("--cogs-basis", default="hybrid", choices=["hybrid", "cash", "shopify"])
    ap.add_argument("--no-estimated-fill", action="store_true"); ap.add_argument("--stores")
    ap.add_argument("--out-dir", default=FINAL_DIR)
    args = ap.parse_args()

    cmd = [sys.executable, os.path.join(SF_SCRIPTS, "monthly_pl.py"), "--cogs-basis", args.cogs_basis]
    if args.year: cmd += ["--year", str(args.year)]
    if args.since: cmd += ["--since", args.since]
    if args.until: cmd += ["--until", args.until]
    if args.months: cmd += ["--months", str(args.months)]
    if args.from_cache: cmd.append("--from-cache")
    if args.no_estimated_fill: cmd.append("--no-estimated-fill")
    if args.stores: cmd += ["--stores", args.stores]
    os.makedirs(args.out_dir, exist_ok=True)
    tmp_out = os.path.join(args.out_dir, "PL_Monthly_building.xlsx")
    cmd += ["--out", tmp_out]
    print("→", " ".join(os.path.basename(c) if c.endswith(".py") else c for c in cmd[1:]))
    r = subprocess.run(cmd, cwd=SF_SCRIPTS, capture_output=True, text=True)
    print(r.stdout[-3000:])
    if r.returncode != 0:
        print(r.stderr[-3000:]); sys.exit(r.returncode)

    ex = load_json(EXEC_JSON, None)
    if not ex:
        print("executive.json missing — monthly_pl.py did not export the executive block"); sys.exit(1)
    months = ex["months"]; execd = ex["executive"]
    for m in months:
        execd[m]["cogs_3pl_freight"] = execd[m]["cogs"] - execd[m]["product_cogs"]
    stem = f"PL_Monthly_{months[0]}_to_{months[-1]}"
    xlsx = os.path.join(args.out_dir, stem + ".xlsx")
    os.replace(tmp_out, xlsx)

    # ---- extras for the markdown: data quality, top vendors per bucket, supplier reconciliation
    led = load_json(LEDGER, {"entries": []})["entries"]
    led = [e for e in led if e["month"] in months]
    bank_months = {e["month"] for e in led if (e.get("source") or "").startswith(BANK_SRC)}
    queue = load_json(QUEUE, {"items": []})["items"]
    notes = []
    missing = [m for m in months if m not in bank_months]
    if missing: notes.append(f"Months with NO bank export (Amex/checking) — expenses estimated or Apple-Card-only: {', '.join(missing)}. Get GPT 5.6 Sol to fetch them (references/gpt-sol-fetch-prompt.md).")
    unrev = [e for e in led if e.get("cat_source") == "unreviewed"]
    if unrev: notes.append(f"{len(unrev)} transactions (${sum(e['amount'] for e in unrev):,.0f}) still uncategorized — booked as Other operating until ruled.")
    if queue: notes.append(f"{len(queue)} transactions in the review queue (`python3 review.py --show`).")
    est_ads = sum(execd[m]["estimated_ad_fill"] for m in months); est_ovh = sum(execd[m]["estimated_overhead_fill"] for m in months)
    if est_ads or est_ovh: notes.append(f"Estimated fills included: ads ${est_ads:,.0f}, overhead ${est_ovh:,.0f} (red rows in the workbook).")
    if ex.get("mtd_month"): notes.append(f"{ex['mtd_month']} is month-to-date — partial.")
    if not notes: notes.append("No data-quality flags.")
    tv = defaultdict(lambda: defaultdict(float))
    for e in led:
        if e["section"] != "opex": continue
        key = re.sub(r"[\d#*]+", "", e["description"].split(";")[0]).strip()[:28]
        tv[BUCKETS[e["bucket"]]][key] += e["amount"]
    top_vendors = {b: sorted(v.items(), key=lambda kv: -kv[1]) for b, v in tv.items()}
    supplier = {}
    bills = load_json(BILLS, {"bills": []})["bills"]
    for b in bills:
        if b.get("month") in months: supplier.setdefault(b["month"], {}).setdefault("bills", 0); supplier[b["month"]]["bills"] += b["grand_total"]
    for e in led:
        if e["category"] == "inventory_purchase": supplier.setdefault(e["month"], {}).setdefault("wires", 0); supplier[e["month"]]["wires"] += e["amount"]
    extras = {"cogs_basis": args.cogs_basis, "notes": notes, "top_vendors": top_vendors, "supplier": supplier if (bills or any('wires' in s for s in supplier.values())) else None}

    md_path = os.path.join(args.out_dir, f"PL_{months[0]}_to_{months[-1]}.md")
    open(md_path, "w").write(markdown(execd, months, extras))
    json_path = os.path.join(args.out_dir, f"PL_{months[0]}_to_{months[-1]}.json")
    save_json(json_path, {"generated_at": now_iso(), "months": months, "cogs_basis": args.cogs_basis, "executive": execd, "data_quality": notes, "supplier_reconciliation": supplier})

    print(f"\nWorkbook: {xlsx}\nMarkdown: {md_path}\nJSON:     {json_path}\n")
    last = [m for m in months if m != ex.get("mtd_month")][-1] if len(months) > 1 else months[-1]
    e = execd[last]
    print(f"Latest full month {last}: net revenue {money(e['net_revenue'])} · gross profit {money(e['gross_profit'])} · "
          f"marketing {money(e['marketing'])} · AI {money(e['ai'])} · operating {money(e['operating'])} · NET {money(e['net_profit'])}")
    for n in notes: print("  ⚠", n)


if __name__ == "__main__":
    main()
