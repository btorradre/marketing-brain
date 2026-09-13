#!/usr/bin/env python3
"""Build Q1 2026 P&L workbook from pulled Shopify raw_data.json.

Workbook structure
------------------
- One sheet per brand, showing a monthly P&L (Jan / Feb / Mar / Q1 total).
  Rows include Shopify-sourced revenue metrics plus placeholder rows for
  COGS, marketing, and operating expenses (user fills these in).
- "Q1 2026 Summary" sheet: roll-up of total sales, orders, and net sales
  across all brands for the quarter.

Motilli Store 1 and Motilli Store 2 are shown individually AND as a
combined "Motilli (Combined)" sheet, since the two stores appear to be
part of the same brand (different migration windows).
"""
import json
from copy import copy
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

HERE = Path(__file__).parent
RAW = json.loads((HERE / "raw_data.json").read_text())

MONTHS = ["January 2026", "February 2026", "March 2026"]

# Sheet ordering + which data keys to combine.
BRAND_SHEETS = [
    {"title": "Motilli - Store 1", "sources": ["Motilli (Store 1)"]},
    {"title": "Motilli - Store 2", "sources": ["Motilli (Store 2)"]},
    {"title": "Motilli (Combined)", "sources": ["Motilli (Store 1)", "Motilli (Store 2)"]},
    {"title": "Velantra",           "sources": ["Velantra"]},
    {"title": "Lunessa",            "sources": ["Lunessa"]},
    {"title": "Solorna",            "sources": ["Solorna"]},
]

# ----- styles -----
THIN = Side(border_style="thin", color="B7B7B7")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

HEADER_FILL = PatternFill("solid", fgColor="1F2937")
HEADER_FONT = Font(bold=True, color="FFFFFF", size=11)
SECTION_FILL = PatternFill("solid", fgColor="E5E7EB")
SECTION_FONT = Font(bold=True, size=11)
TOTAL_FILL = PatternFill("solid", fgColor="FEF3C7")
TOTAL_FONT = Font(bold=True, size=11)
SUBTOTAL_FILL = PatternFill("solid", fgColor="F3F4F6")
SUBTOTAL_FONT = Font(bold=True, size=10)
INPUT_FILL = PatternFill("solid", fgColor="ECFDF5")
CENTER = Alignment(horizontal="center", vertical="center")
RIGHT = Alignment(horizontal="right", vertical="center")
LEFT = Alignment(horizontal="left", vertical="center")

MONEY_FMT = '_($* #,##0.00_);_($* (#,##0.00);_($* "-"??_);_(@_)'
INT_FMT = "#,##0"
PCT_FMT = "0.0%"


def combine(sources):
    """Sum monthly summaries across a list of source-brand keys."""
    out = {}
    for m in MONTHS:
        # Build agg keys dynamically from the first source so schema changes
        # don't break the combine step.
        first = RAW[sources[0]][m]
        agg = {k: 0 for k in first}
        for src in sources:
            s = RAW[src][m]
            for k in agg:
                agg[k] += s.get(k, 0)
        out[m] = agg
    return out


def write_brand_sheet(wb, title, data):
    ws = wb.create_sheet(title=title)

    ws["A1"] = title
    ws["A1"].font = Font(bold=True, size=16)
    ws.merge_cells("A1:E1")

    ws["A2"] = "Q1 2026 Profit & Loss (Jan 1 – Mar 31, 2026)"
    ws["A2"].font = Font(italic=True, size=10, color="6B7280")
    ws.merge_cells("A2:E2")

    # Column headers
    headers = ["Line item", "January", "February", "March", "Q1 2026 Total"]
    for i, h in enumerate(headers, start=1):
        c = ws.cell(row=4, column=i, value=h)
        c.fill = HEADER_FILL
        c.font = HEADER_FONT
        c.alignment = CENTER
        c.border = BOX

    row = 5

    def section(label):
        nonlocal row
        c = ws.cell(row=row, column=1, value=label)
        c.fill = SECTION_FILL
        c.font = SECTION_FONT
        for col in range(2, 6):
            ws.cell(row=row, column=col).fill = SECTION_FILL
        ws.cell(row=row, column=1).border = BOX
        for col in range(2, 6):
            ws.cell(row=row, column=col).border = BOX
        row += 1

    def data_row(label, key, negative=False, fmt=MONEY_FMT, is_subtotal=False):
        nonlocal row
        lc = ws.cell(row=row, column=1, value=label)
        lc.alignment = LEFT
        lc.border = BOX
        if is_subtotal:
            lc.font = SUBTOTAL_FONT
            lc.fill = SUBTOTAL_FILL
        for i, m in enumerate(MONTHS):
            val = data[m][key]
            if negative and val != 0:
                val = -val
            c = ws.cell(row=row, column=2 + i, value=val)
            c.number_format = fmt
            c.alignment = RIGHT
            c.border = BOX
            if is_subtotal:
                c.font = SUBTOTAL_FONT
                c.fill = SUBTOTAL_FILL
        # Q1 total
        col_letters = [get_column_letter(2 + i) for i in range(3)]
        formula = f"=SUM({col_letters[0]}{row}:{col_letters[2]}{row})"
        tc = ws.cell(row=row, column=5, value=formula)
        tc.number_format = fmt
        tc.alignment = RIGHT
        tc.border = BOX
        if is_subtotal:
            tc.font = SUBTOTAL_FONT
            tc.fill = SUBTOTAL_FILL
        row += 1

    def input_row(label, fmt=MONEY_FMT, default=0):
        nonlocal row
        lc = ws.cell(row=row, column=1, value=label)
        lc.alignment = LEFT
        lc.border = BOX
        lc.font = Font(italic=True, color="065F46")
        for i in range(3):
            c = ws.cell(row=row, column=2 + i, value=default)
            c.number_format = fmt
            c.alignment = RIGHT
            c.border = BOX
            c.fill = INPUT_FILL
        col_letters = [get_column_letter(2 + i) for i in range(3)]
        tc = ws.cell(row=row, column=5,
                    value=f"=SUM({col_letters[0]}{row}:{col_letters[2]}{row})")
        tc.number_format = fmt
        tc.alignment = RIGHT
        tc.border = BOX
        row += 1
        return row - 1  # return the row written

    def formula_row(label, formula_fn, fmt=MONEY_FMT, highlight=False):
        nonlocal row
        lc = ws.cell(row=row, column=1, value=label)
        lc.alignment = LEFT
        lc.border = BOX
        fill = TOTAL_FILL if highlight else SUBTOTAL_FILL
        font = TOTAL_FONT if highlight else SUBTOTAL_FONT
        lc.font = font
        lc.fill = fill
        for i in range(3):
            col = get_column_letter(2 + i)
            c = ws.cell(row=row, column=2 + i, value=formula_fn(col, row))
            c.number_format = fmt
            c.alignment = RIGHT
            c.border = BOX
            c.font = font
            c.fill = fill
        col_letters = [get_column_letter(2 + i) for i in range(3)]
        tc = ws.cell(row=row, column=5,
                    value=f"=SUM({col_letters[0]}{row}:{col_letters[2]}{row})")
        tc.number_format = fmt
        tc.alignment = RIGHT
        tc.border = BOX
        tc.font = font
        tc.fill = fill
        row += 1
        return row - 1

    # --- Sales volume section ---
    section("ORDER VOLUME")
    data_row("Orders placed", "orders", fmt=INT_FMT)
    data_row("Cancelled orders", "cancelled_orders", fmt=INT_FMT)
    data_row("Orders with refunds", "refunded_orders", fmt=INT_FMT)
    data_row("Orders tagged chargeback (awareness)", "chargeback_tagged_orders", fmt=INT_FMT)

    # --- Revenue section (Shopify) ---
    section("REVENUE (from Shopify — Finance Summary logic)")
    data_row("Gross sales (line items at list price)", "gross_sales")
    data_row("Discounts", "discounts", negative=True)
    data_row("Returns / refunded subtotal", "returns", negative=True)
    net_sales_row = row
    data_row("Net sales", "net_sales", is_subtotal=True)
    data_row("Shipping (net of refunds)", "shipping")
    data_row("Taxes (net of refunds)", "taxes")
    total_sales_row = row
    data_row("Total sales (net revenue)", "total_sales", is_subtotal=True)

    # --- Cash-flow view ---
    section("CASH-FLOW VIEW (reconciliation)")
    data_row("Customer payments at checkout", "order_total_gross_before_refunds")
    data_row("Total refunded (incl. chargebacks)", "total_refunded", negative=True)
    data_row("Net revenue retained", "net_revenue_check", is_subtotal=True)

    # --- COGS section (inputs) ---
    section("COST OF GOODS SOLD (input)")
    cogs_prod = input_row("Product cost (landed)")
    cogs_fulfill = input_row("Fulfillment / 3PL")
    cogs_ship_out = input_row("Outbound shipping cost")
    cogs_pay = input_row("Payment processing fees (~2.9% + $0.30)")
    # total COGS
    cogs_rows = [cogs_prod, cogs_fulfill, cogs_ship_out, cogs_pay]
    total_cogs_row = formula_row(
        "Total COGS",
        lambda col, r: "=" + "+".join(f"{col}{rr}" for rr in cogs_rows),
        highlight=False,
    )

    # --- Gross profit ---
    gp_row = formula_row(
        "Gross profit",
        lambda col, r, ns=net_sales_row, tc=total_cogs_row: f"={col}{ns}-{col}{tc}",
        highlight=True,
    )
    gp_margin_row = formula_row(
        "Gross margin %",
        lambda col, r, gp=gp_row, ns=net_sales_row: f"=IF({col}{ns}=0,0,{col}{gp}/{col}{ns})",
        fmt=PCT_FMT,
        highlight=False,
    )

    # --- Operating expenses (inputs) ---
    section("MARKETING & OPERATING EXPENSES (input)")
    opex_rows = []
    for label in [
        "Meta / Facebook ad spend",
        "Google / YouTube ad spend",
        "TikTok ad spend",
        "Influencer / UGC spend",
        "Creative production (video, images, copy)",
        "Email / SMS platform (Klaviyo etc.)",
        "Shopify + app stack (Shopify, ReCharge, etc.)",
        "Software & tools (other)",
        "Contractors / agency retainers",
        "Salaries & payroll",
        "Customer service",
        "Other operating expenses",
    ]:
        opex_rows.append(input_row(label))
    total_opex_row = formula_row(
        "Total operating expenses",
        lambda col, r: "=" + "+".join(f"{col}{rr}" for rr in opex_rows),
    )

    # --- Net profit ---
    section("BOTTOM LINE")
    net_row = formula_row(
        "Net profit (pre-tax)",
        lambda col, r, gp=gp_row, op=total_opex_row: f"={col}{gp}-{col}{op}",
        highlight=True,
    )
    formula_row(
        "Net margin % (of net sales)",
        lambda col, r, n=net_row, ns=net_sales_row: f"=IF({col}{ns}=0,0,{col}{n}/{col}{ns})",
        fmt=PCT_FMT,
    )
    formula_row(
        "MER (Net sales / Total ad spend)",
        lambda col, r, ns=net_sales_row, ad_rows=opex_rows[:4]:
            f"=IF(SUM({','.join(f'{col}{rr}' for rr in ad_rows)})=0,0,"
            f"{col}{ns}/SUM({','.join(f'{col}{rr}' for rr in ad_rows)}))",
        fmt='0.00"x"',
    )
    aov_row = formula_row(
        "AOV (Total sales / Orders)",
        lambda col, r, ts=total_sales_row: f"=IFERROR({col}{ts}/{col}5,0)",
    )

    # Notes
    note_row = row + 1
    ws.cell(row=note_row, column=1,
            value=("Notes: Green cells are inputs — fill in your actual costs. "
                   "All other cells pull from Shopify (Q1 2026 orders) or are computed. "
                   "Total COGS + operating expense rows roll into net profit automatically."))
    ws.cell(row=note_row, column=1).font = Font(italic=True, color="6B7280", size=9)
    ws.merge_cells(start_row=note_row, start_column=1, end_row=note_row, end_column=5)
    ws.row_dimensions[note_row].height = 30
    ws.cell(row=note_row, column=1).alignment = Alignment(
        wrap_text=True, horizontal="left", vertical="top"
    )

    # Column widths
    ws.column_dimensions["A"].width = 42
    for c in ["B", "C", "D", "E"]:
        ws.column_dimensions[c].width = 18

    ws.freeze_panes = "B5"


def write_summary_sheet(wb, combined_data):
    """Summary sheet showing each brand's Q1 total side by side."""
    ws = wb.create_sheet(title="Q1 2026 Summary", index=0)

    ws["A1"] = "Q1 2026 Summary — All Brands"
    ws["A1"].font = Font(bold=True, size=18)
    ws.merge_cells("A1:G1")
    ws["A2"] = "January 1 – March 31, 2026 | Revenue data from Shopify"
    ws["A2"].font = Font(italic=True, size=10, color="6B7280")
    ws.merge_cells("A2:G2")

    headers = ["Metric"] + [b["title"] for b in BRAND_SHEETS if b["title"] != "Motilli (Combined)"] + ["All Brands Total"]
    # We want: Metric | Motilli S1 | Motilli S2 | Velantra | Lunessa | Solorna | All Brands Total
    brand_titles = [b["title"] for b in BRAND_SHEETS if "Combined" not in b["title"]]

    headers = ["Metric"] + brand_titles + ["All Brands Total"]
    for i, h in enumerate(headers, start=1):
        c = ws.cell(row=4, column=i, value=h)
        c.fill = HEADER_FILL
        c.font = HEADER_FONT
        c.alignment = CENTER
        c.border = BOX

    metrics = [
        ("Orders placed", "orders", INT_FMT, False),
        ("Orders with refunds", "refunded_orders", INT_FMT, False),
        ("Gross sales", "gross_sales", MONEY_FMT, False),
        ("Discounts", "discounts", MONEY_FMT, True),
        ("Returns / refunds", "returns", MONEY_FMT, True),
        ("Net sales", "net_sales", MONEY_FMT, False),
        ("Shipping", "shipping", MONEY_FMT, False),
        ("Taxes", "taxes", MONEY_FMT, False),
        ("Total sales", "total_sales", MONEY_FMT, False),
    ]

    row = 5
    for label, key, fmt, negate in metrics:
        is_total = key in ("net_sales", "total_sales")
        c = ws.cell(row=row, column=1, value=label)
        c.alignment = LEFT
        c.border = BOX
        if is_total:
            c.font = TOTAL_FONT
            c.fill = TOTAL_FILL

        for i, title in enumerate(brand_titles):
            # sum the 3 months for this brand
            total = sum(combined_data[title][m][key] for m in MONTHS)
            if negate and total != 0:
                total = -total
            cc = ws.cell(row=row, column=2 + i, value=total)
            cc.number_format = fmt
            cc.alignment = RIGHT
            cc.border = BOX
            if is_total:
                cc.font = TOTAL_FONT
                cc.fill = TOTAL_FILL

        # All Brands total column
        start = get_column_letter(2)
        end = get_column_letter(1 + len(brand_titles))
        total_cell = ws.cell(row=row, column=2 + len(brand_titles),
                              value=f"=SUM({start}{row}:{end}{row})")
        total_cell.number_format = fmt
        total_cell.alignment = RIGHT
        total_cell.border = BOX
        total_cell.font = TOTAL_FONT
        total_cell.fill = TOTAL_FILL

        row += 1

    # AOV row
    row += 1
    c = ws.cell(row=row, column=1, value="AOV (Total sales / Orders)")
    c.alignment = LEFT
    c.border = BOX
    c.font = SUBTOTAL_FONT
    c.fill = SUBTOTAL_FILL
    for i, title in enumerate(brand_titles):
        orders_total = sum(combined_data[title][m]["orders"] for m in MONTHS)
        sales_total = sum(combined_data[title][m]["total_sales"] for m in MONTHS)
        aov = sales_total / orders_total if orders_total else 0
        cc = ws.cell(row=row, column=2 + i, value=aov)
        cc.number_format = MONEY_FMT
        cc.alignment = RIGHT
        cc.border = BOX
        cc.font = SUBTOTAL_FONT
        cc.fill = SUBTOTAL_FILL
    # all brands AOV
    total_orders = sum(
        sum(combined_data[t][m]["orders"] for m in MONTHS) for t in brand_titles
    )
    total_sales = sum(
        sum(combined_data[t][m]["total_sales"] for m in MONTHS) for t in brand_titles
    )
    total_aov = total_sales / total_orders if total_orders else 0
    cc = ws.cell(row=row, column=2 + len(brand_titles), value=total_aov)
    cc.number_format = MONEY_FMT
    cc.alignment = RIGHT
    cc.border = BOX
    cc.font = SUBTOTAL_FONT
    cc.fill = SUBTOTAL_FILL

    # Note about combined Motilli
    row += 2
    note = ws.cell(row=row, column=1, value=(
        "Note: Motilli operates across two Shopify stores during Q1. "
        "Store 1 holds January–February orders; Store 2 holds February–March orders. "
        "See the 'Motilli (Combined)' sheet for the unified Motilli brand P&L."
    ))
    note.font = Font(italic=True, color="6B7280", size=10)
    note.alignment = Alignment(wrap_text=True, horizontal="left", vertical="top")
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=7)
    ws.row_dimensions[row].height = 32

    ws.column_dimensions["A"].width = 34
    for col_idx in range(2, 2 + len(brand_titles) + 1):
        ws.column_dimensions[get_column_letter(col_idx)].width = 20

    ws.freeze_panes = "B5"


def main():
    wb = Workbook()
    # remove default sheet
    wb.remove(wb.active)

    # build combined data per sheet title
    combined_per_sheet = {}
    for b in BRAND_SHEETS:
        combined_per_sheet[b["title"]] = combine(b["sources"])

    # Summary first
    write_summary_sheet(wb, combined_per_sheet)

    # Then per-brand sheets
    for b in BRAND_SHEETS:
        write_brand_sheet(wb, b["title"], combined_per_sheet[b["title"]])

    out = HERE / "Q1_2026_PnL.xlsx"
    wb.save(out)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
