#!/usr/bin/env python3
"""Builds the month-by-month P&L workbook from monthly_pl.py dataset + expense ledger.

Tabs: P&L Monthly (consolidated) · Net Sales by Brand · Brand P&Ls (contribution) ·
Expenses (Imported) · Data Quality · Methodology
"""
import datetime as dt
from collections import defaultdict
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

from import_expenses import CATEGORIES

NAVY = "1F3864"; BLUE = "2E5496"; LBLUE = "D9E1F2"; LGREEN = "E2EFDA"; GREY = "F2F2F2"
AMBER = "FFF2CC"; WHITE = "FFFFFF"; LRED = "F8CBAD"
def fill(c): return PatternFill("solid", fgColor=c)
thin = Side(style="thin", color="BFBFBF"); BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
MONEY = '#,##0.00;[Red](#,##0.00)'; MONEY0 = '#,##0;[Red](#,##0)'; INT = '#,##0'; PCT = '0.0%'
H1 = Font(bold=True, size=16, color="FFFFFF"); H2 = Font(bold=True, size=11, color="FFFFFF")
BOLD = Font(bold=True); BOLDW = Font(bold=True, color="FFFFFF"); ITAL = Font(italic=True, size=9, color="555555")
REDF = Font(bold=True, color="C00000")
CTR = Alignment(horizontal="center")

SHOPIFY_KEYS = ["gross", "discounts", "net", "returns", "shipping", "tax", "tip", "total",
                "refund_total", "cogs", "fee_processing", "fee_dispute",
                "cb_total", "cb_lost", "cb_won", "cb_open", "orders", "refund_orders", "cb_count"]

OPEX_IMPORTED = ["ad_spend_meta", "ad_spend_google", "ad_spend_tiktok", "ad_spend_other",
                 "marketing_software", "creators_influencers", "ai_tools",
                 "shipping_postage", "software_saas", "contractors_agency", "payroll",
                 "merchant_fees", "legal_professional", "taxes_gov", "interest_expense",
                 "travel", "meals_entertainment", "office_misc", "other_opex"]
MEMO_IMPORTED = ["inventory_purchase", "owner_draw", "transfer", "cc_payment", "loan_principal", "income_tax"]


def _title(ws, title, span, sub):
    ws.merge_cells(f"A1:{get_column_letter(span)}1"); c = ws["A1"]; c.value = title; c.font = H1; c.fill = fill(NAVY)
    c.alignment = Alignment(horizontal="left", vertical="center"); ws.row_dimensions[1].height = 30
    ws.merge_cells(f"A2:{get_column_letter(span)}2"); c = ws["A2"]; c.value = sub
    c.font = Font(italic=True, size=10, color="404040"); c.fill = fill(LBLUE); ws.row_dimensions[2].height = 18


def _consolidate(dataset):
    months = dataset["months"]
    C = {mo: defaultdict(float) for mo in months}
    for st in dataset["stores"]:
        for mo, z in st["months"].items():
            if mo not in C: continue
            for k in SHOPIFY_KEYS: C[mo][k] += z.get(k, 0)
    return C


def _hybrid_cogs(dataset, months, min_cov=0.5):
    """Hybrid product COGS per month:
    - store-months with cost-per-item coverage >= min_cov: Shopify COGS grossed up
      to 100% coverage (cogs / coverage)
    - store-months with poor/no coverage but sales: net x blended cost ratio,
      borrowed from the same group's covered months, else the global covered blend
    Returns (month->total, [(brand, month, rate, est$)], global_rate, group_rates)."""
    gn, gc = defaultdict(float), defaultdict(float)
    for st in dataset["stores"]:
        for mo, z in st["months"].items():
            if mo in months and z["net"] > 0 and z["cogs_coverage"] >= min_cov and z["cogs"] > 0:
                gn[st["group"]] += z["net"]; gc[st["group"]] += z["cogs"] / z["cogs_coverage"]
    global_rate = (sum(gc.values()) / sum(gn.values())) if gn else 0.0
    group_rates = {g: gc[g] / gn[g] for g in gn}
    totals = {mo: 0.0 for mo in months}
    estimates = []
    for st in dataset["stores"]:
        for mo, z in st["months"].items():
            if mo not in months: continue
            if z["cogs_coverage"] >= min_cov and z["cogs"] > 0:
                totals[mo] += z["cogs"] / z["cogs_coverage"]
            elif z["net"] > 0:
                rate = group_rates.get(st["group"], global_rate)
                est = z["net"] * rate
                totals[mo] += est
                estimates.append((st["brand"], mo, rate, est))
            else:
                totals[mo] += z["cogs"]
    return totals, estimates, global_rate, group_rates


def _month_label(mo, mtd):
    y, m = mo.split("-")
    lbl = dt.date(int(y), int(m), 1).strftime("%b %y")
    return lbl + " (MTD)" if mo == mtd else lbl


class Grid:
    """Writes a months-as-columns sheet and tracks row numbers for formulas."""
    def __init__(self, ws, months, mtd, start_row=4, label_w=46):
        self.ws, self.months, self.r = ws, months, start_row
        self.ncols = 1 + len(months) + 1  # label + months + TOTAL
        ws.column_dimensions["A"].width = label_w
        for i in range(len(months) + 1):
            ws.column_dimensions[get_column_letter(2 + i)].width = 13
        hdr = [""] + [_month_label(m, mtd) for m in months] + ["TOTAL"]
        for i, h in enumerate(hdr, 1):
            c = ws.cell(self.r, i, h); c.font = H2; c.fill = fill(BLUE); c.alignment = CTR; c.border = BORDER
        ws.row_dimensions[self.r].height = 24
        self.r += 1
        ws.freeze_panes = f"B{self.r}"

    def col(self, i):  # 0-based month index -> column letter
        return get_column_letter(2 + i)

    @property
    def total_col(self):
        return get_column_letter(2 + len(self.months))

    def section(self, label):
        ws = self.ws
        ws.merge_cells(f"A{self.r}:{get_column_letter(self.ncols)}{self.r}")
        c = ws.cell(self.r, 1, label); c.font = H2; c.fill = fill(NAVY)
        ws.row_dimensions[self.r].height = 20; self.r += 1

    def row(self, label, values=None, formula=None, fmt=MONEY0, bold=False, fc=None,
            memo=False, total="sum", total_formula=None):
        """values: list per month · formula: callable(col_letter)->str applied per month column."""
        ws, r = self.ws, self.r
        a = ws.cell(r, 1, label); a.font = BOLD if bold else (ITAL if memo else Font()); a.border = BORDER
        if fc: a.fill = fill(fc)
        for i in range(len(self.months)):
            c = ws.cell(r, 2 + i)
            c.value = formula(self.col(i)) if formula else (values[i] if values else 0)
            c.number_format = fmt; c.border = BORDER
            if bold: c.font = BOLD
            if memo: c.font = ITAL
            if fc: c.fill = fill(fc)
        tc = ws.cell(r, 2 + len(self.months))
        if total_formula: tc.value = total_formula
        elif total == "sum": tc.value = f"=SUM({self.col(0)}{r}:{self.col(len(self.months)-1)}{r})"
        tc.number_format = fmt; tc.border = BORDER
        tc.font = BOLD if (bold or not memo) else ITAL
        if fc: tc.fill = fill(fc)
        self.r += 1
        return r

    def blank(self):
        self.r += 1


def build(dataset, expenses, out_path, cogs_basis="hybrid", estimate_fill=True):
    """cogs_basis:
    'hybrid'  = Shopify cost-per-item grossed up to 100% coverage; store-months with
                no cost data estimated at the covered stores' blended cost ratio (default)
    'cash'    = supplier wires (inventory_purchase) are COGS, Shopify cost-per-item is memo
    'shopify' = raw cost-per-item accrual is COGS, supplier wires are memo."""
    cash = cogs_basis == "cash"; hybrid = cogs_basis == "hybrid"
    months = dataset["months"]; mtd = dataset.get("mtd_month")
    label = f"{months[0]} to {months[-1]}"
    C = _consolidate(dataset)
    exp = expenses.get("by_month", {})
    expb = expenses.get("by_month_brand", {})
    def sv(key):            # shopify value list per month
        return [round(C[mo][key], 2) for mo in months]
    def ev(cat):            # expense value list per month
        return [round(exp.get(mo, {}).get(cat, 0.0), 2) for mo in months]
    has_expense_data = bool(expenses.get("entries"))

    # --- estimated OPEX fills for months whose bank (Amex/checking) data isn't imported ---
    # A month with recorded ad spend is treated as "complete". Incomplete months get:
    #   ad spend fill  = net sales x blended aMER of complete full months
    #   overhead fill  = per-category recurring average of complete months, minus actuals
    # Both fills vanish automatically once the month's real bank export is imported.
    AD_CATS = ("ad_spend_meta", "ad_spend_google", "ad_spend_tiktok", "ad_spend_other")
    OVH_CATS = ("software_saas", "contractors_agency", "merchant_fees", "chargeback_services", "shipping_postage")
    # a month is "complete" only if the bank/Amex export covers it (source prefixes from
    # the ChatGPT/Plaid converter) — Apple Card or Meta-API rows alone don't make it complete
    BANK_SRC = ("business_gold", "business_platinum", "checking", "business_checking", "simplefin")
    bank_months = {e["month"] for e in expenses.get("entries", [])
                   if any((e.get("source") or "").startswith(p) for p in BANK_SRC)}
    def _ads(mo): return sum(exp.get(mo, {}).get(k, 0.0) for k in AD_CATS)
    basis = [mo for mo in months if mo in bank_months and mo != mtd] or [mo for mo in months if mo in bank_months]
    fill_on = estimate_fill and bool(basis) and sum(C[mo]["net"] for mo in basis) > 0
    amer = (sum(_ads(mo) for mo in basis) / sum(C[mo]["net"] for mo in basis)) if fill_on else 0.0
    ovh_avg = {k: sum(exp.get(mo, {}).get(k, 0.0) for mo in basis) / len(basis) for k in OVH_CATS} if fill_on else {}
    ad_fill = {mo: (round(C[mo]["net"] * amer, 2)
                    if fill_on and mo not in bank_months and _ads(mo) == 0 and C[mo]["net"] > 0 else 0.0)
               for mo in months}
    ovh_fill = {mo: (round(sum(max(0.0, ovh_avg[k] - exp.get(mo, {}).get(k, 0.0)) for k in OVH_CATS), 2)
                     if fill_on and mo not in bank_months and C[mo]["net"] > 0 else 0.0) for mo in months}

    basis_note = ("COGS = hybrid (Shopify cost-per-item, gaps estimated)" if hybrid else
                  "COGS = supplier wires (cash basis)" if cash else "COGS = Shopify cost-per-item (accrual)")
    # ---------- 0. Executive rollup (finance-agent buckets: Revenue / COGS / Marketing / AI / Operating / Net) ----------
    hyb_tot0, _, _, _ = _hybrid_cogs(dataset, months) if hybrid else ({}, [], 0, {})
    def _bucket_sum(bucket, mo):
        return sum(exp.get(mo, {}).get(cat, 0.0) for cat in CATEGORIES
                   if CATEGORIES[cat]["section"] == "opex" and CATEGORIES[cat]["bucket"] == bucket)
    EXEC = {}
    for mo in months:
        rev_before = C[mo]["gross"] - C[mo]["discounts"] + C[mo]["shipping"] + exp.get(mo, {}).get("other_income", 0.0)
        refunds = C[mo]["returns"]
        net_rev = rev_before - refunds
        product_cogs = (exp.get(mo, {}).get("inventory_purchase", 0.0) if cash else
                        hyb_tot0.get(mo, C[mo]["cogs"]) if hybrid else C[mo]["cogs"])
        cogs = product_cogs + exp.get(mo, {}).get("fulfillment_3pl", 0.0) + exp.get(mo, {}).get("freight_duties", 0.0)
        marketing = _bucket_sum("marketing", mo) + ad_fill[mo]
        ai = _bucket_sum("ai", mo)
        shopify_fees = C[mo]["fee_processing"] + C[mo]["fee_dispute"]
        cb_lost = C[mo]["cb_lost"]
        operating = _bucket_sum("operating", mo) + ovh_fill[mo] + shopify_fees + cb_lost
        gp = net_rev - cogs
        np_ = gp - marketing - ai - operating
        EXEC[mo] = {"revenue_before_refunds": rev_before, "refunds": refunds, "net_revenue": net_rev,
                    "product_cogs": product_cogs, "cogs": cogs, "gross_profit": gp,
                    "marketing": marketing, "marketing_ads": sum(exp.get(mo, {}).get(k, 0.0) for k in AD_CATS) + ad_fill[mo],
                    "marketing_tools": exp.get(mo, {}).get("marketing_software", 0.0),
                    "marketing_creators": exp.get(mo, {}).get("creators_influencers", 0.0),
                    "ai": ai, "operating": operating, "shopify_fees": shopify_fees, "chargebacks_lost": cb_lost,
                    "operating_other": _bucket_sum("operating", mo) + ovh_fill[mo],
                    "net_profit": np_, "net_sales_ref": C[mo]["net"], "orders": C[mo]["orders"],
                    "estimated_ad_fill": ad_fill[mo], "estimated_overhead_fill": ovh_fill[mo]}
    dataset["executive"] = {mo: {k: round(v, 2) for k, v in EXEC[mo].items()} for mo in months}

    wb = Workbook()

    # ---------- Executive P&L tab (first tab) ----------
    wsx = wb.active; wsx.title = "Executive P&L"
    _title(wsx, "EXECUTIVE P&L — REVENUE · COGS · MARKETING · AI · OPERATING · NET",
           2 + len(months), f"Bucket rollup of every line below · {label} · {basis_note}")
    gx = Grid(wsx, months, mtd, label_w=48)
    def xv(k): return [round(EXEC[mo][k], 2) for mo in months]
    def pct_row(lbl, num_r, den_r):
        gx.row(lbl, formula=lambda c: f"=IF({c}{den_r}=0,0,{c}{num_r}/{c}{den_r})", fmt=PCT,
               total_formula=f"=IF({gx.total_col}{den_r}=0,0,{gx.total_col}{num_r}/{gx.total_col}{den_r})", total=None, memo=True)
    gx.section("REVENUE")
    x_rb = gx.row("Revenue before refunds (net sales − discounts + shipping + other income)", xv("revenue_before_refunds"))
    x_rf = gx.row("Refunds / returns", [-v for v in xv("refunds")])
    x_nr = gx.row("NET REVENUE", formula=lambda c: f"={c}{x_rb}+{c}{x_rf}", bold=True, fc=LBLUE, fmt=MONEY)
    gx.section("COST OF GOODS SOLD")
    x_pc = gx.row("Product COGS" + (" (supplier wires)" if cash else " (Shopify cost-per-item, hybrid)" if hybrid else " (Shopify)"), xv("product_cogs"))
    x_3p = gx.row("Fulfillment / 3PL + inbound freight", [round(EXEC[mo]["cogs"] - EXEC[mo]["product_cogs"], 2) for mo in months], fc=AMBER)
    x_cg = gx.row("TOTAL COGS", formula=lambda c: f"={c}{x_pc}+{c}{x_3p}", bold=True, fmt=MONEY)
    x_gp = gx.row("GROSS PROFIT", formula=lambda c: f"={c}{x_nr}-{c}{x_cg}", bold=True, fc=LGREEN, fmt=MONEY)
    pct_row("Gross margin", x_gp, x_nr)
    gx.section("MARKETING")
    x_m1 = gx.row("Paid ads (Meta + Google + TikTok + other, incl. estimated fill)", xv("marketing_ads"), fc=AMBER)
    x_m2 = gx.row("Marketing tools (email/SMS, ad intel, creative software)", xv("marketing_tools"), fc=AMBER)
    x_m3 = gx.row("Creators / influencers / UGC", xv("marketing_creators"), fc=AMBER)
    x_mk = gx.row("TOTAL MARKETING", formula=lambda c: f"=SUM({c}{x_m1}:{c}{x_m3})", bold=True, fmt=MONEY)
    pct_row("Marketing % of net revenue", x_mk, x_nr)
    gx.section("AI")
    x_ai = gx.row("TOTAL AI (LLM subscriptions, API usage, image/video/voice generation)", xv("ai"), bold=True, fc=AMBER, fmt=MONEY)
    pct_row("AI % of net revenue", x_ai, x_nr)
    gx.section("OPERATING")
    x_o1 = gx.row("Shopify Payments fees (processing + dispute)", xv("shopify_fees"))
    x_o2 = gx.row("Chargebacks lost", xv("chargebacks_lost"))
    x_o3 = gx.row("Software, contractors, payroll, fees, travel, meals, office, other (incl. est. fill)", xv("operating_other"), fc=AMBER)
    x_op = gx.row("TOTAL OPERATING", formula=lambda c: f"=SUM({c}{x_o1}:{c}{x_o3})", bold=True, fmt=MONEY)
    pct_row("Operating % of net revenue", x_op, x_nr)
    gx.section("NET")
    x_np = gx.row("NET PROFIT (pre-tax)", formula=lambda c: f"={c}{x_gp}-{c}{x_mk}-{c}{x_ai}-{c}{x_op}", bold=True, fc=LGREEN, fmt=MONEY)
    pct_row("Net margin", x_np, x_nr)
    gx.row("ROAS (net revenue ÷ paid ads)", formula=lambda c: f"=IF({c}{x_m1}=0,0,{c}{x_nr}/{c}{x_m1})", fmt='0.00"x"', memo=True,
           total_formula=f"=IF({gx.total_col}{x_m1}=0,0,{gx.total_col}{x_nr}/{gx.total_col}{x_m1})", total=None)
    gx.row("Orders", xv("orders"), fmt=INT, memo=True)
    if any(ad_fill.values()) or any(ovh_fill.values()):
        gx.row("⚠ Estimated fills included above (ads)", [ad_fill[mo] for mo in months], fc=LRED, memo=True)
        gx.row("⚠ Estimated fills included above (overhead)", [ovh_fill[mo] for mo in months], fc=LRED, memo=True)
    gx.blank()
    wsx.cell(gx.r, 1, "Buckets are driven by the category taxonomy in import_expenses.py (CATEGORIES[cat]['bucket']). "
                      "Yellow = bank/AI-categorized ledger, white = Shopify API, red = estimates. Full line detail on 'P&L Monthly'.").font = ITAL

    ws = wb.create_sheet("P&L Monthly")

    # ---------- 1. P&L Monthly (consolidated) ----------
    hyb_tot, hyb_est, hyb_global, hyb_group = _hybrid_cogs(dataset, months) if hybrid else ({}, [], 0, {})

    basis_note = ("COGS = hybrid (Shopify cost-per-item, gaps estimated)" if hybrid else
                  "COGS = supplier wires (cash basis)" if cash else "COGS = Shopify cost-per-item (accrual)")
    _title(ws, "CONSOLIDATED P&L — MONTH BY MONTH", 2 + len(months),
           f"All Shopify stores + imported bank/expense data · {label} · {basis_note} · tax excluded (passthrough)")
    g = Grid(ws, months, mtd)

    g.section("REVENUE (Shopify — before refunds; refunds are an OPEX line below)")
    r_gross = g.row("Gross Sales", sv("gross"))
    r_disc = g.row("Discounts", [-v for v in sv("discounts")])
    r_netrev = g.row("NET REVENUE (before refunds)", formula=lambda c: f"={c}{r_gross}+{c}{r_disc}",
                     bold=True, fc=LGREEN, fmt=MONEY)
    r_ship = g.row("Shipping income", sv("shipping"))
    r_oth = g.row(CATEGORIES["other_income"]["label"], ev("other_income"), fc=AMBER)
    r_rev = g.row("TOTAL REVENUE (before refunds)", formula=lambda c: f"={c}{r_netrev}+{c}{r_ship}+{c}{r_oth}",
                  bold=True, fc=LBLUE, fmt=MONEY)
    r_net = g.row("Net sales after refunds (reference — % bases below)", sv("net"), memo=True, fmt=MONEY)

    g.section("COST OF GOODS SOLD" + (" — CASH BASIS (supplier wires)" if cash else
                                      " — HYBRID (Shopify cost-per-item, gaps filled)" if hybrid else ""))
    if cash:
        r_cogs0 = g.row("Product COGS — supplier payments/wires (imported)", ev("inventory_purchase"), fc=AMBER)
    elif hybrid:
        r_cogs0 = g.row("Product COGS (Shopify + estimated fill — see Data Quality)",
                        [round(hyb_tot[mo], 2) for mo in months])
    else:
        r_cogs0 = g.row("Product COGS (Shopify cost-per-item)", sv("cogs"))
    g.row(CATEGORIES["fulfillment_3pl"]["label"] + " (imported)", ev("fulfillment_3pl"), fc=AMBER)
    r_cogs1 = g.row(CATEGORIES["freight_duties"]["label"] + " (imported)", ev("freight_duties"), fc=AMBER)
    r_tcogs = g.row("Total COGS", formula=lambda c: f"=SUM({c}{r_cogs0}:{c}{r_cogs1})", bold=True, fmt=MONEY)
    r_gp = g.row("GROSS PROFIT", formula=lambda c: f"={c}{r_rev}-{c}{r_tcogs}", bold=True, fc=LGREEN, fmt=MONEY)
    g.row("Gross margin (% of net sales)", formula=lambda c: f"=IF({c}{r_net}=0,0,{c}{r_gp}/{c}{r_net})",
          fmt=PCT, total_formula=f"=IF({g.total_col}{r_net}=0,0,{g.total_col}{r_gp}/{g.total_col}{r_net})", total=None)

    g.section("OPERATING EXPENSES (Shopify fees pulled · rest imported from bank data)")
    ox_start = g.r
    for cat in ["ad_spend_meta", "ad_spend_google", "ad_spend_tiktok", "ad_spend_other"]:
        g.row(CATEGORIES[cat]["label"], ev(cat), fc=AMBER)
    g.row("Ad spend — ESTIMATED fill (bank data not yet imported)",
          [ad_fill[mo] for mo in months], fc=LRED)
    g.row("Refunds / returns (product revenue reversed)", sv("returns"))
    g.row("Shopify Payments — processing fees", sv("fee_processing"))
    r_cbfee = g.row("Shopify Payments — dispute/chargeback fees", sv("fee_dispute"))
    r_cblost = g.row("Chargebacks — lost (clawed-back revenue)", sv("cb_lost"))
    r_cbsvc = g.row(CATEGORIES["chargeback_services"]["label"], ev("chargeback_services"), fc=AMBER)
    for cat in OPEX_IMPORTED[4:]:
        g.row(CATEGORIES[cat]["label"], ev(cat), fc=AMBER)
    g.row("Recurring overhead — ESTIMATED fill (bank data not yet imported)",
          [ovh_fill[mo] for mo in months], fc=LRED)
    ox_end = g.r - 1
    r_topex = g.row("Total Operating Expenses", formula=lambda c: f"=SUM({c}{ox_start}:{c}{ox_end})",
                    bold=True, fmt=MONEY)

    g.section("PROFIT")
    r_np = g.row("NET PROFIT (pre-tax)", formula=lambda c: f"={c}{r_gp}-{c}{r_topex}",
                 bold=True, fc=LGREEN, fmt=MONEY)
    g.row("Net margin (% of net sales)", formula=lambda c: f"=IF({c}{r_net}=0,0,{c}{r_np}/{c}{r_net})",
          fmt=PCT, total_formula=f"=IF({g.total_col}{r_net}=0,0,{g.total_col}{r_np}/{g.total_col}{r_net})", total=None)

    g.section("MARKETING EFFICIENCY (totals — no per-brand attribution)")
    ad_end = ox_start + 4  # the 4 ad-spend rows + estimated-fill row open the OPEX section
    r_ads = g.row("Total ad spend (incl. estimated fill)", formula=lambda c: f"=SUM({c}{ox_start}:{c}{ad_end})",
                  bold=True, fmt=MONEY)
    g.row("ROAS (net sales ÷ total ad spend)", formula=lambda c: f"=IF({c}{r_ads}=0,0,{c}{r_net}/{c}{r_ads})",
          fmt='0.00"x"', bold=True, fc=LGREEN,
          total_formula=f"=IF({g.total_col}{r_ads}=0,0,{g.total_col}{r_net}/{g.total_col}{r_ads})", total=None)
    g.row("Ad spend % of net sales (aMER)", formula=lambda c: f"=IF({c}{r_net}=0,0,{c}{r_ads}/{c}{r_net})",
          fmt=PCT, total_formula=f"=IF({g.total_col}{r_net}=0,0,{g.total_col}{r_ads}/{g.total_col}{r_net})", total=None)

    g.section("CHARGEBACK ECONOMICS — total actual expense")
    r_cbt = g.row("TOTAL CHARGEBACK EXPENSE (dispute fees + lost + management)",
                  formula=lambda c: f"={c}{r_cbfee}+{c}{r_cblost}+{c}{r_cbsvc}", bold=True, fc=LRED, fmt=MONEY)
    g.row("Chargebacks — count", sv("cb_count"), fmt=INT)
    g.row("Chargeback expense % of net sales", formula=lambda c: f"=IF({c}{r_net}=0,0,{c}{r_cbt}/{c}{r_net})",
          fmt=PCT, total_formula=f"=IF({g.total_col}{r_net}=0,0,{g.total_col}{r_cbt}/{g.total_col}{r_net})", total=None)

    g.section("MEMO (not in profit — informational)")
    g.row("Orders", sv("orders"), fmt=INT, memo=True)
    aov = [round(C[mo]["net"] / C[mo]["orders"], 2) if C[mo]["orders"] else 0 for mo in months]
    g.row("AOV (net)", aov, fmt=MONEY, memo=True,
          total_formula=f"=IF({g.total_col}{g.r-1}=0,0,{g.total_col}{r_net}/{g.total_col}{g.r-1})", total=None)
    g.row("Refunds issued — cash (reference; P&L books product returns above)", sv("refund_total"), memo=True)
    g.row("Chargebacks — open / at-risk", sv("cb_open"), memo=True)
    g.row("Chargebacks — won / recovered", sv("cb_won"), memo=True)
    if cash or hybrid:
        g.row("Product COGS per Shopify cost-per-item (unadjusted reference)", sv("cogs"), memo=True)
    for cat in MEMO_IMPORTED:
        if cash and cat == "inventory_purchase":
            continue  # promoted to the COGS section in cash basis
        vals = ev(cat)
        if any(vals):
            g.row(CATEGORIES[cat]["label"], vals, memo=True)
    g.blank()
    note = ("Yellow rows = imported from bank/expense data via ChatGPT (import_expenses.py). "
            if has_expense_data else
            "Yellow rows = EMPTY — no expense ledger imported yet. Export bank data via ChatGPT "
            "(references/chatgpt-interop.md), run import_expenses.py, then re-run monthly_pl.py --from-cache. ")
    ws.cell(g.r, 1, note + "White rows = pulled live from Shopify.").font = ITAL

    # ---------- 2. Net Sales by Brand ----------
    groups = defaultdict(lambda: {mo: defaultdict(float) for mo in months})
    for st in dataset["stores"]:
        for mo, z in st["months"].items():
            if mo not in months: continue
            for k in SHOPIFY_KEYS: groups[st["group"]][mo][k] += z.get(k, 0)
    order = sorted(groups, key=lambda gr: -sum(groups[gr][mo]["net"] for mo in months))

    ws2 = wb.create_sheet("Net Sales by Brand")
    _title(ws2, "NET SALES BY BRAND — MONTH BY MONTH", 2 + len(months), f"Net sales basis · {label}")
    g2 = Grid(ws2, months, mtd, label_w=26)
    for gr in order:
        g2.row(gr, [round(groups[gr][mo]["net"], 2) for mo in months], fmt=MONEY0, bold=True)
    g2.row("CONSOLIDATED", [round(C[mo]["net"], 2) for mo in months], fmt=MONEY0, bold=True, fc=LBLUE)

    # ---------- 2b. Chargebacks & Refunds (inserted as tab #2) ----------
    wscb = wb.create_sheet("Chargebacks & Refunds", 1)
    _title(wscb, "CHARGEBACKS & REFUNDS — MONTH BY MONTH", 2 + len(months),
           f"Consolidated across all stores · refunds are already netted inside Net Sales (memo) · {label}")
    gc_ = Grid(wscb, months, mtd)

    gc_.section("REFUNDS (booked as an OPEX line on the P&L — 'Refunds / returns')")
    r_gr = gc_.row("Gross sales (reference)", sv("gross"), memo=True)
    r_rf = gc_.row("Refunds issued $", sv("refund_total"))
    r_ro = gc_.row("Refund orders", sv("refund_orders"), fmt=INT)
    r_or = gc_.row("Total orders (reference)", sv("orders"), fmt=INT, memo=True)
    gc_.row("Refund rate (% of orders)", formula=lambda c: f"=IF({c}{r_or}=0,0,{c}{r_ro}/{c}{r_or})", fmt=PCT,
            total_formula=f"=IF({gc_.total_col}{r_or}=0,0,{gc_.total_col}{r_ro}/{gc_.total_col}{r_or})", total=None)
    gc_.row("Refunds % of gross sales", formula=lambda c: f"=IF({c}{r_gr}=0,0,{c}{r_rf}/{c}{r_gr})", fmt=PCT,
            total_formula=f"=IF({gc_.total_col}{r_gr}=0,0,{gc_.total_col}{r_rf}/{gc_.total_col}{r_gr})", total=None)

    gc_.section("CHARGEBACKS (disputes by initiated month)")
    r_cn = gc_.row("Chargebacks — count", sv("cb_count"), fmt=INT)
    gc_.row("Chargebacks — total $", sv("cb_total"))
    r_cl2 = gc_.row("— lost $ (booked as expense)", sv("cb_lost"))
    gc_.row("— won / recovered $", sv("cb_won"))
    gc_.row("— open / at-risk $", sv("cb_open"))
    r_df2 = gc_.row("Dispute fees (Shopify)", sv("fee_dispute"))
    r_ds2 = gc_.row(CATEGORIES["chargeback_services"]["label"], ev("chargeback_services"), fc=AMBER)
    gc_.row("TOTAL CHARGEBACK EXPENSE", formula=lambda c: f"={c}{r_df2}+{c}{r_cl2}+{c}{r_ds2}",
            bold=True, fc=LRED, fmt=MONEY)
    r_rate = gc_.row("Chargeback rate (count ÷ orders)", formula=lambda c: f"=IF({c}{r_or}=0,0,{c}{r_cn}/{c}{r_or})",
                     fmt=PCT, total_formula=f"=IF({gc_.total_col}{r_or}=0,0,{gc_.total_col}{r_cn}/{gc_.total_col}{r_or})",
                     total=None)
    for i, mo in enumerate(months):  # red-flag months at/above the ~0.9% network monitoring threshold
        if C[mo]["orders"] and C[mo]["cb_count"] / C[mo]["orders"] >= 0.009:
            cell = wscb.cell(r_rate, 2 + i); cell.font = REDF; cell.fill = fill(LRED)
    gc_.blank()

    gc_.section("BY BRAND — period totals")
    _gt = defaultdict(lambda: defaultdict(float))
    for st in dataset["stores"]:
        for mo, z in st["months"].items():
            if mo in months:
                for k in ("refund_total", "refund_orders", "cb_count", "cb_total", "cb_lost"):
                    _gt[st["group"]][k] += z.get(k, 0)
    for grp in sorted(_gt, key=lambda x: -_gt[x]["cb_total"]):
        t = _gt[grp]
        wscb.cell(gc_.r, 1, f"{grp}: refunds ${t['refund_total']:,.0f} ({t['refund_orders']:.0f} orders) · "
                            f"chargebacks {t['cb_count']:.0f} for ${t['cb_total']:,.0f} (lost ${t['cb_lost']:,.0f})").font = ITAL
        gc_.r += 1

    # ---------- 3. Brand P&Ls (contribution) ----------
    ws3 = wb.create_sheet("Brand P&Ls")
    _title(ws3, "BRAND CONTRIBUTION P&Ls — MONTH BY MONTH", 2 + len(months),
           f"Shopify-side + brand-tagged imported expenses · company-wide expenses NOT allocated · {label}")
    g3 = Grid(ws3, months, mtd)
    for gr in order:
        G = groups[gr]
        g3.section(gr)
        rn = g3.row("Net sales", [round(G[mo]["net"], 2) for mo in months], bold=True)
        rows = [rn]
        rows.append(g3.row("COGS (Shopify cost-per-item — reference)" if cash else "COGS (Shopify)",
                           [round(G[mo]["cogs"], 2) for mo in months]))
        rows.append(g3.row("Shopify fees (processing + dispute)",
                           [round(G[mo]["fee_processing"] + G[mo]["fee_dispute"], 2) for mo in months]))
        rows.append(g3.row("Chargebacks lost", [round(G[mo]["cb_lost"], 2) for mo in months]))
        brand_cats = sorted({e["category"] for e in expenses.get("entries", [])
                             if (e.get("brand") or "") == gr and CATEGORIES[e["category"]]["section"] in ("cogs", "opex")})
        for cat in brand_cats:
            vals = [round(expb.get(f"{mo}|{gr}", {}).get(cat, 0.0), 2) for mo in months]
            rows.append(g3.row(CATEGORIES[cat]["label"] + " (imported)", vals, fc=AMBER))
        cost_rows = rows[1:]
        contrib = lambda c, rn=rn, cr=tuple(cost_rows): f"={c}{rn}-" + "-".join(f"{c}{x}" for x in cr)
        rc = g3.row("CONTRIBUTION PROFIT", formula=contrib, bold=True, fc=LGREEN, fmt=MONEY)
        g3.row("Contribution margin", formula=lambda c, rn=rn, rc=rc: f"=IF({c}{rn}=0,0,{c}{rc}/{c}{rn})",
               fmt=PCT, total_formula=f"=IF({g3.total_col}{rn}=0,0,{g3.total_col}{rc}/{g3.total_col}{rn})", total=None)
        g3.blank()

    # ---------- 4. Expenses (Imported) ----------
    ws4 = wb.create_sheet("Expenses (Imported)")
    entries = expenses.get("entries", [])
    _title(ws4, "IMPORTED EXPENSE LEDGER", 7,
           f"{len(entries)} entries · source: ChatGPT bank/expense export → import_expenses.py · {label}")
    hdr = ["Month", "Date", "Brand", "Category", "Description", "Amount", "Source"]
    for i, h in enumerate(hdr, 1):
        c = ws4.cell(4, i, h); c.font = H2; c.fill = fill(BLUE); c.border = BORDER; c.alignment = CTR
    r = 5
    for e in sorted(entries, key=lambda x: (x["month"], x["category"], x["description"])):
        vals = [e["month"], e.get("date") or "", e.get("brand") or "Company-wide",
                CATEGORIES[e["category"]]["label"], e["description"], e["amount"], e.get("source") or ""]
        for i, v in enumerate(vals, 1):
            c = ws4.cell(r, i, v); c.border = BORDER; c.fill = fill(WHITE if r % 2 else GREY)
            if i == 6: c.number_format = MONEY
        if CATEGORIES[e["category"]]["section"] == "memo":
            ws4.cell(r, 4).font = ITAL
        r += 1
    if not entries:
        ws4.cell(5, 1, "No expenses imported yet — see references/chatgpt-interop.md for the ChatGPT export prompt.").font = ITAL
    for i, w in enumerate([10, 12, 14, 38, 44, 12, 16], 1):
        ws4.column_dimensions[get_column_letter(i)].width = w
    ws4.freeze_panes = "A5"

    # ---------- 5. Data Quality ----------
    ws5 = wb.create_sheet("Data Quality")
    _title(ws5, "DATA QUALITY — trust the numbers?", 2 + len(months), f"COGS coverage per store per month · expense-data coverage · {label}")
    g5 = Grid(ws5, months, mtd, label_w=26)
    g5.section("COGS COVERAGE (% of sold units with a Shopify cost-per-item; <100% ⇒ COGS understated)")
    for st in sorted(dataset["stores"], key=lambda s: s["brand"]):
        vals, row_r = [], g5.r
        for mo in months:
            z = st["months"].get(mo)
            vals.append(round(z["cogs_coverage"], 4) if z and z["orders"] else 1.0)
        g5.row(st["brand"] + (" [MANUAL ENTRY]" if st.get("manual") else ""), vals, fmt=PCT, total=None)
        for i, v in enumerate(vals):
            if v < 0.5:
                cell = ws5.cell(row_r, 2 + i); cell.font = REDF; cell.fill = fill(LRED)
    if any(ad_fill.values()):
        g5.section("ESTIMATED OPEX FILLS (Amex/checking data not imported for these months)")
        for mo in months:
            if ad_fill[mo]:
                ws5.cell(g5.r, 1, f"{mo}: ad spend est ${ad_fill[mo]:,.0f} (net × {amer:.1%} blended aMER) "
                                  f"+ recurring overhead est ${ovh_fill[mo]:,.0f}").font = ITAL
                g5.r += 1
        ws5.cell(g5.r, 1, f"Basis months (complete bank data): {', '.join(basis)}. Fills disappear automatically "
                          "when a month's real bank export is imported. ROAS for estimated months is circular "
                          f"(≈{(1/amer if amer else 0):.2f}x by construction) — do not read it as performance.").font = ITAL
        g5.r += 1

    if hybrid and hyb_est:
        g5.section("HYBRID COGS — ESTIMATED STORE-MONTHS (no cost-per-item entered in Shopify)")
        for brand, mo, rate, est in sorted(hyb_est):
            ws5.cell(g5.r, 1, f"{brand} — {mo}: estimated ${est:,.0f} (net sales × {rate:.1%} blended cost ratio)").font = ITAL
            g5.r += 1
        rates_txt = ", ".join(f"{gr} {r:.1%}" for gr, r in sorted(hyb_group.items()))
        ws5.cell(g5.r, 1, f"Blended cost ratios from covered stores — global {hyb_global:.1%}"
                          + (f" · by group: {rates_txt}" if rates_txt else "")).font = ITAL; g5.r += 1
        wires = sum(exp.get(mo, {}).get("inventory_purchase", 0) for mo in months)
        hybsum = sum(hyb_tot[mo] for mo in months)
        ws5.cell(g5.r, 1, f"Supplier-wire reconciliation: hybrid COGS {label} = ${hybsum:,.0f} vs supplier wires captured = "
                          f"${wires:,.0f}. Wires lag sales (inventory bought ahead) and only exist for months with bank data — "
                          "treat as a directional cross-check, not a match.").font = ITAL; g5.r += 1

    manual_sts = [s for s in dataset["stores"] if s.get("manual")]
    if manual_sts:
        g5.section("MANUAL ENTRIES (not pulled from Shopify — user-provided figures)")
        for st in manual_sts:
            detail = " · ".join(f"{mo}: net ${z['net']:,.0f}" for mo, z in sorted(st["months"].items()))
            ws5.cell(g5.r, 1, f"{st['brand']} — {detail}").font = ITAL; g5.r += 1
    g5.section("EXPENSE DATA COVERAGE (imported ledger)")
    have = set(expenses.get("months_present", []))
    g5.row("Expense entries imported?", [1 if mo in have else 0 for mo in months], fmt=INT)
    g5.blank()
    notes = ["Months with 0 above have NO imported expense data — their Net Profit is Shopify-side only (overstated).",
             "MTD column is a partial month — do not compare to full months."]
    for n in notes:
        ws5.cell(g5.r, 1, n).font = ITAL; g5.r += 1

    # ---------- 6. Methodology ----------
    ws6 = wb.create_sheet("Methodology"); ws6.column_dimensions["A"].width = 116
    lines = [
        ("METHODOLOGY", H2), ("", None),
        ("SHOPIFY SIDE — Admin API, bucketed by ORDER CREATION MONTH (accrual).", None),
        ("REVENUE is shown BEFORE refunds (gross − discounts); 'Refunds / returns' is an OPEX line (= gross − discounts −", None),
        ("current_subtotal_price, i.e. product revenue reversed, by order month). Net profit is identical to netting them", None),
        ("in revenue — this is presentation only. % metrics (margins, ROAS) use net sales AFTER refunds (reference row).", None),
        (("COGS = HYBRID: Shopify cost-per-item grossed up to 100% coverage per store-month; store-months with no "
          "cost data estimated at the covered stores' blended cost ratio (group ratio first, else global). Estimated "
          "cells are itemized on Data Quality, with a supplier-wire cross-check.") if hybrid else
         ("COGS = CASH BASIS: actual supplier payments/wires (inventory_purchase entries, e.g. Haikou Genyangkai) "
          "booked in the month PAID. Lumpy by design — a big inventory wire hits one month while the goods sell over "
          "several. Shopify cost-per-item shown as memo reference only.") if cash else
         "COGS = (units sold − refunded) × Shopify cost-per-item, same-month accrual. See Data Quality for coverage.", None),
        ("Fees = Shopify Payments balance transactions bucketed by processed_at month (charge = processing, dispute = CB fees).", None),
        ("Chargebacks bucketed by initiated_at month; LOST chargebacks are a real expense (order revenue never reverses).", None),
        ("Tax collected = passthrough, excluded from every profit line. Shipping income included in Total Revenue.", None),
        ("", None),
        ("BANK SIDE — imported ledger (data/expenses.json) built by import_expenses.py from a ChatGPT export.", None),
        ("Yellow rows come from the ledger. Categories map to fixed P&L lines (see references/chatgpt-interop.md).", None),
        (("inventory_purchase (supplier wires) IS the product COGS line under cash basis; Shopify cost-per-item is memo." if cash else
          "inventory_purchase is MEMO ONLY — product COGS accrues from Shopify cost-per-item; counting both double-counts."), None),
        ("Owner draws / transfers / CC payments / loan principal excluded from profit.", None),
        ("ESTIMATED FILLS: months with no imported bank data get ad spend (net × blended aMER of complete months) and", None),
        ("recurring overhead (complete-month category averages minus recorded actuals) — red rows, itemized on Data Quality.", None),
        ("", None),
        ("BRAND P&Ls = contribution view: brand Shopify figures + brand-tagged expenses only.", None),
        ("Company-wide (untagged) expenses appear only on the consolidated tab — brand contribution sums > company net profit.", None),
        (f"Generated {dt.date.today().isoformat()} by shopify-financials/monthly_pl.py.", None),
    ]
    for i, (txt, fnt) in enumerate(lines, 1):
        c = ws6.cell(i, 1, txt)
        c.font = fnt if fnt else Font(size=10, color="333333")

    wb.save(out_path)
    return out_path
