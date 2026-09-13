#!/usr/bin/env python3
"""Builds the 8-tab Shopify financials workbook from results produced by pull_financials.run_store()."""
import datetime as dt
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

NAVY="1F3864"; BLUE="2E5496"; LBLUE="D9E1F2"; LGREEN="E2EFDA"; GREY="F2F2F2"; AMBER="FFF2CC"; WHITE="FFFFFF"; LRED="F8CBAD"
def fill(c): return PatternFill("solid", fgColor=c)
thin=Side(style="thin", color="BFBFBF"); BORDER=Border(left=thin,right=thin,top=thin,bottom=thin)
MONEY='#,##0.00;[Red](#,##0.00)'; MONEY0='#,##0;[Red](#,##0)'; INT='#,##0'; PCT='0.0%'
H1=Font(bold=True,size=16,color="FFFFFF"); H2=Font(bold=True,size=11,color="FFFFFF")
BOLD=Font(bold=True); BOLDW=Font(bold=True,color="FFFFFF"); ITAL=Font(italic=True,size=9,color="555555")
REDF=Font(bold=True,color="C00000"); GRN=Font(bold=True,color="548235")
CTR=Alignment(horizontal="center"); LEFT=Alignment(horizontal="left")
def money(c, f=MONEY): c.number_format=f

def _title(ws, title, span, sub):
    ws.merge_cells(f"A1:{get_column_letter(span)}1"); c=ws["A1"]; c.value=title; c.font=H1; c.fill=fill(NAVY)
    c.alignment=Alignment(horizontal="left", vertical="center"); ws.row_dimensions[1].height=30
    ws.merge_cells(f"A2:{get_column_letter(span)}2"); c=ws["A2"]; c.value=sub; c.font=Font(italic=True,size=10,color="404040")
    c.fill=fill(LBLUE); ws.row_dimensions[2].height=18

def build(results, label, since, until, out_path):
    R = sorted(results, key=lambda x: -x["net"])  # biggest first
    today = dt.date.today()
    def days_since(d):
        if not d: return ""
        try: return (today - dt.date.fromisoformat(d[:10])).days
        except Exception: return ""
    wb = Workbook()

    # ---------- 1. By Brand ----------
    ws = wb.active; ws.title="By Brand"
    _title(ws, "UNIFIED SHOPIFY P&L — Revenue by Brand", 10, f"Net sales basis · {label} · revenue only")
    hdr=["Brand","Gross Sales","Discounts","Returns/Refunds","Net Sales","Shipping","Tax","Total Collected","Orders","AOV (net)"]
    for i,h in enumerate(hdr,1):
        c=ws.cell(4,i,h); c.font=H2; c.fill=fill(BLUE); c.alignment=CTR if i>1 else LEFT; c.border=BORDER
    ws.row_dimensions[4].height=28; r=5
    for x in R:
        vals=[x["brand"],x["gross"],-x["discounts"],-x["returns"],x["net"],x["shipping"],x["tax"],x["total"],x["orders"],x["aov"]]
        for i,v in enumerate(vals,1):
            c=ws.cell(r,i,v); c.border=BORDER; c.fill=fill(WHITE if r%2 else GREY)
            if i==1: c.font=BOLD
            elif i==9: money(c,INT)
            elif i==10: money(c,MONEY)
            else: money(c, MONEY0 if i in(2,3,4,6,7) else MONEY)
        r+=1
    T=_totals(R)
    trow=["CONSOLIDATED",T["gross"],-T["discounts"],-T["returns"],T["net"],T["shipping"],T["tax"],T["total"],T["orders"],(T["net"]/T["orders"] if T["orders"] else 0)]
    for i,v in enumerate(trow,1):
        c=ws.cell(r,i,v); c.fill=fill(NAVY); c.font=BOLDW; c.border=BORDER
        if i==9: money(c,INT)
        elif i==10: money(c,MONEY)
        elif i>1: money(c, MONEY0 if i in(2,3,4,6,7) else MONEY)
    for i,w in enumerate([26,15,13,15,16,12,10,17,9,11],1): ws.column_dimensions[get_column_letter(i)].width=w
    ws.freeze_panes="B5"

    # ---------- 2. Shopify Costs (COGS+Fees) ----------
    wsc=wb.create_sheet("Shopify Costs (COGS+Fees)")
    _title(wsc,"SHOPIFY-SIDE COSTS — COGS & Payment Fees",9,f"Cost-per-item COGS + Shopify Payments fees · {label}")
    hh=["Brand","Net Sales","COGS (Shopify)","COGS coverage","Processing fees","Dispute fees","Total SP fees","Fee % of collected","Chargeback losses"]
    for i,h in enumerate(hh,1):
        c=wsc.cell(4,i,h); c.font=H2; c.fill=fill(BLUE); c.alignment=Alignment(horizontal="center",wrap_text=True); c.border=BORDER
    wsc.row_dimensions[4].height=34; r=5
    for x in R:
        feepct = x["fee_total"]/x["total"] if x["total"] else 0
        vals=[x["brand"],x["net"],x["cogs"],x["cogs_coverage"],x["fee_processing"],x["fee_dispute"],x["fee_total"],feepct,x["cb"]["lost"]]
        for i,v in enumerate(vals,1):
            c=wsc.cell(r,i,v); c.border=BORDER; c.fill=fill(WHITE if r%2 else GREY)
            if i==1: c.font=BOLD
            elif i in (4,8): money(c,PCT)
            else: money(c, MONEY0 if i in (3,5,6,7,9) else MONEY)
        if x["cogs_coverage"]<0.5: wsc.cell(r,4).font=REDF; wsc.cell(r,4).fill=fill(LRED)
        r+=1
    trow=["TOTAL",T["net"],T["cogs"],None,T["fee_processing"],T["fee_dispute"],T["fee_total"],(T["fee_total"]/T["total"] if T["total"] else 0),T["cb_lost"]]
    for i,v in enumerate(trow,1):
        c=wsc.cell(r,i,v); c.fill=fill(NAVY); c.font=BOLDW; c.border=BORDER
        if v is None: continue
        if i in (4,8): money(c,PCT)
        elif i>1: money(c, MONEY0 if i in (3,5,6,7,9) else MONEY)
    for i,w in enumerate([22,15,14,12,14,12,13,14,15],1): wsc.column_dimensions[get_column_letter(i)].width=w
    wsc.freeze_panes="B5"

    # ---------- 3. Chargebacks & Refunds ----------
    wc=wb.create_sheet("Chargebacks & Refunds")
    _title(wc,"CHARGEBACKS & REFUNDS — by Brand",14,f"Shopify Payments disputes + order refunds · {label}")
    cols=["Brand","Orders","Refunds $","Refund orders","Chargebacks #","Chargeback $","Lost #","Lost $","Won #","Won $","Open #","Open $","CB rate (count)","CB $ % of net"]
    for i,h in enumerate(cols,1):
        c=wc.cell(4,i,h); c.font=H2; c.fill=fill(BLUE); c.alignment=Alignment(horizontal="center",wrap_text=True); c.border=BORDER
    wc.row_dimensions[4].height=30; r=5
    for x in R:
        cb=x["cb"]; n=x["orders"]; rate=cb["count"]/n if n else 0; cbpct=cb["total"]/x["net"] if x["net"] else 0
        vals=[x["brand"],n,x["refund_total"],x["refund_orders"],cb["count"],cb["total"],cb["lost_n"],cb["lost"],cb["won_n"],cb["won"],cb["open_n"],cb["open"],rate,cbpct]
        for i,v in enumerate(vals,1):
            c=wc.cell(r,i,v); c.border=BORDER; c.fill=fill(WHITE if r%2 else GREY)
            if i==1: c.font=BOLD
            elif i in(2,5,7,9,11): money(c,INT)
            elif i in(13,14): money(c,PCT)
            else: money(c, MONEY0 if i in(3,6,8,10,12) else MONEY)
        if rate>=0.02:
            for cc in (13,14): wc.cell(r,cc).font=REDF; wc.cell(r,cc).fill=fill(LRED)
        r+=1
    for i,w in enumerate([16,8,11,12,12,12,7,10,7,10,7,10,12,12],1): wc.column_dimensions[get_column_letter(i)].width=w
    wc.freeze_panes="B5"

    # ---------- 4. Shopify Holds & Payouts ----------
    wh=wb.create_sheet("Shopify Holds & Payouts")
    _title(wh,"SHOPIFY HOLDS & PAYOUT STATUS",8,f"Available balance, reserves & payout health · pulled {today.isoformat()}")
    hdr=["Brand","Available balance","Reserve (API)","Open disputes","Last successful payout","Last payout amount","Days since","Stuck payouts $"]
    for i,h in enumerate(hdr,1):
        c=wh.cell(4,i,h); c.font=H2; c.fill=fill(BLUE); c.alignment=Alignment(horizontal="center",wrap_text=True); c.border=BORDER
    wh.row_dimensions[4].height=30; r=5; pos=0.0; res_t=0.0
    for x in R:
        h=x["holds"]; ds=days_since(h["last_paid"]); stuck_sum=sum(s["amount"] for s in h["stuck"] if s["status"] in ("failed","canceled"))
        vals=[x["brand"],h["available"],h["reserve"],x["cb"]["open"],h["last_paid"] or "—",h["last_paid_amt"],ds,stuck_sum]
        for i,v in enumerate(vals,1):
            c=wh.cell(r,i,v); c.border=BORDER; c.fill=fill(WHITE if r%2 else GREY)
            if i==1: c.font=BOLD
            elif i in (2,3,4,6,8): money(c,MONEY)
            elif i==7: money(c,INT); c.alignment=CTR
            elif i==5: c.alignment=CTR
        if h["available"]<0: wh.cell(r,2).font=REDF
        if h["reserve"]>0: wh.cell(r,3).font=GRN
        if isinstance(ds,int) and ds>=40: wh.cell(r,7).font=REDF
        pos += h["available"] if h["available"]>0 else 0; res_t += h["reserve"]; r+=1
    for i,v in enumerate(["TOTALS (avail>0 / reserve)",pos,res_t,"","","","",""],1):
        c=wh.cell(r,i,v); c.fill=fill(NAVY); c.font=BOLDW; c.border=BORDER
        if i in (2,3): money(c,MONEY)
    for i,w in enumerate([22,17,14,13,18,15,9,14],1): wh.column_dimensions[get_column_letter(i)].width=w
    wh.freeze_panes="B5"

    # ---------- 5. Stuck Payouts Detail ----------
    ws5=wb.create_sheet("Stuck Payouts Detail")
    _title(ws5,"STUCK PAYOUTS — line-item detail",4,f"Every failed / canceled / scheduled payout · pulled {today.isoformat()}")
    r=4
    for x in R:
        h=x["holds"]
        if not h["stuck"]:
            continue
        rec=sum(s["amount"] for s in h["stuck"] if s["status"] in ("failed","canceled"))
        ws5.merge_cells(f"A{r}:D{r}"); c=ws5.cell(r,1,f"{x['brand']}   —   Available ${h['available']:,.2f}   |   Recoverable (failed/canceled) ${rec:,.2f}")
        c.font=H2; c.fill=fill(BLUE); ws5.row_dimensions[r].height=20; r+=1
        for i,hd in enumerate(["Payout date","Status","Amount",""],1):
            cc=ws5.cell(r,i,hd); cc.font=BOLD; cc.fill=fill(GREY); cc.border=BORDER
        r+=1
        for s in h["stuck"]:
            ws5.cell(r,1,s["date"]).border=BORDER; ws5.cell(r,1).alignment=CTR
            sc=ws5.cell(r,2,s["status"]); sc.border=BORDER; sc.alignment=CTR
            if s["status"]=="failed": sc.font=REDF
            ac=ws5.cell(r,3,s["amount"]); money(ac); ac.border=BORDER; ws5.cell(r,4,"").border=BORDER
            r+=1
        r+=1
    if r==4:
        ws5.cell(4,1,"No stuck payouts across any store. ✅").font=BOLD
    for i,w in enumerate([22,14,16,4],1): ws5.column_dimensions[get_column_letter(i)].width=w

    # ---------- 6. Full P&L (Codex) ----------
    ws2=wb.create_sheet("Full P&L (Codex)")
    _title(ws2,"CONSOLIDATED P&L — Shopify costs filled · external for Codex",3,f"{label}")
    ws2.column_dimensions["A"].width=4; ws2.column_dimensions["B"].width=48; ws2.column_dimensions["C"].width=20
    def sec(row,label_):
        ws2.merge_cells(f"A{row}:C{row}"); c=ws2[f"A{row}"]; c.value=label_; c.font=H2; c.fill=fill(BLUE); ws2.row_dimensions[row].height=22
    def line(row,lbl,val=None,bold=False,fmt=MONEY,fc=None,formula=None,memo=False):
        a=ws2.cell(row,2,lbl); a.font=BOLD if bold else (ITAL if memo else Font())
        cell=ws2.cell(row,3)
        if formula: cell.value=formula
        elif val is not None: cell.value=val
        money(cell,fmt)
        if bold: cell.font=BOLD
        if memo: cell.font=ITAL
        if fc:
            for col in (2,3): ws2.cell(row,col).fill=fill(fc)
        ws2.cell(row,2).border=BORDER; ws2.cell(row,3).border=BORDER
        return row+1
    r=4
    sec(r,"REVENUE (Shopify — final, net of refunds)"); r+=1
    r=line(r,"Gross Sales",T["gross"],fmt=MONEY0); r=line(r,"Discounts",-T["discounts"],fmt=MONEY0); r=line(r,"Returns / Refunds (product)",-T["returns"],fmt=MONEY0)
    r=line(r,"NET SALES",None,bold=True,formula="=C6+C7+C8",fc=LGREEN); NET=r-1
    r=line(r,"Shipping income",T["shipping"],fmt=MONEY0); r=line(r,"Tax collected (passthrough)",T["tax"],fmt=MONEY0)
    r=line(r,"TOTAL COLLECTED",None,bold=True,formula=f"=C{NET}+C{NET+1}+C{NET+2}",fc=LBLUE); r+=1
    sec(r,"COST OF GOODS SOLD (Shopify cost-per-item filled · external yellow)"); r+=1
    cs=r; r=line(r,"Product cost (COGS — Shopify, see coverage)",T["cogs"],fmt=MONEY0)
    r=line(r,"Fulfillment / 3PL / pick-pack",0,fmt=MONEY0,fc=AMBER); r=line(r,"Inbound freight / duties",0,fmt=MONEY0,fc=AMBER)
    ce=r-1; r=line(r,"Total COGS",None,bold=True,formula=f"=SUM(C{cs}:C{ce})"); TC=r-1
    r=line(r,"GROSS PROFIT",None,bold=True,formula=f"=C{NET}-C{TC}",fc=LGREEN); GP=r-1; r+=1
    sec(r,"OPERATING EXPENSES (Shopify fees filled · ad spend & external yellow)"); r+=1
    os_=r
    r=line(r,"Ad spend — Meta",0,fmt=MONEY0,fc=AMBER); r=line(r,"Ad spend — Google",0,fmt=MONEY0,fc=AMBER); r=line(r,"Ad spend — other",0,fmt=MONEY0,fc=AMBER)
    r=line(r,"Shopify Payments — processing fees",T["fee_processing"],fmt=MONEY0)
    r=line(r,"Shopify Payments — dispute/chargeback fees",T["fee_dispute"],fmt=MONEY0)
    r=line(r,"Chargebacks — lost (clawed-back revenue)",T["cb_lost"],fmt=MONEY0)
    r=line(r,"Shipping labels / postage (3PL — external)",0,fmt=MONEY0,fc=AMBER); r=line(r,"Software / apps / SaaS",0,fmt=MONEY0,fc=AMBER)
    r=line(r,"Agency / contractors",0,fmt=MONEY0,fc=AMBER); r=line(r,"Other operating",0,fmt=MONEY0,fc=AMBER)
    oe=r-1; r=line(r,"Total Operating Expenses",None,bold=True,formula=f"=SUM(C{os_}:C{oe})"); TO=r-1; r+=1
    sec(r,"PROFIT (updates as Codex fills yellow cells)"); r+=1
    r=line(r,"NET PROFIT (pre-tax)",None,bold=True,formula=f"=C{GP}-C{TO}",fc=LGREEN); NP=r-1
    r=line(r,"Net margin (% of net sales)",None,bold=True,formula=f"=C{NP}/C{NET}",fmt=PCT); r+=2
    sec(r,"MEMO — chargebacks/refunds & cash (not double-counted)"); r+=1
    r=line(r,"Refunds issued (already in Net Sales — informational)",T["refund_total"],fmt=MONEY0,memo=True)
    r=line(r,"Chargebacks — open / at-risk (pending)",T["cb_open"],fmt=MONEY0,memo=True)
    r=line(r,"Chargebacks — won / recovered",T["cb_won"],fmt=MONEY0,memo=True)
    r=line(r,"Cash — positive available balances",T["avail_pos"],fmt=MONEY0,memo=True)
    r=line(r,"Cash — reserves held by Shopify",T["reserve"],fmt=MONEY0,memo=True)
    r+=1; ws2.cell(r,2,"Yellow = Codex fills from bank/ad-account/3PL. Tax collected is passthrough (excluded from profit).").font=ITAL

    # ---------- 7. Brand Mini P&Ls ----------
    ws3=wb.create_sheet("Brand Mini P&Ls"); _title(ws3,"MINI P&Ls BY BRAND",2,f"{label}")
    ws3.column_dimensions["A"].width=40; ws3.column_dimensions["B"].width=18; r=4
    for x in R:
        cb=x["cb"]
        ws3.merge_cells(f"A{r}:B{r}"); c=ws3.cell(r,1,x["brand"]); c.font=H2; c.fill=fill(BLUE); ws3.row_dimensions[r].height=20; r+=1
        rows=[("Gross Sales",x["gross"],MONEY0,0),("Discounts",-x["discounts"],MONEY0,0),("Returns/Refunds",-x["returns"],MONEY0,0),
              ("Net Sales",x["net"],MONEY,1),("Shipping",x["shipping"],MONEY0,0),("Tax",x["tax"],MONEY0,0),("Total Collected",x["total"],MONEY,1),
              ("Orders",x["orders"],INT,0),(f"COGS ({x['cogs_coverage']*100:.0f}% cover)",x["cogs"],MONEY0,0),
              ("Processing fees",x["fee_processing"],MONEY0,0),("Dispute fees",x["fee_dispute"],MONEY0,0),
              ("Refunds issued",x["refund_total"],MONEY0,0),("Chargebacks lost $",cb["lost"],MONEY0,0)]
        for lbl,val,fmt,hl in rows:
            a=ws3.cell(r,1,lbl); cc=ws3.cell(r,2,val); money(cc,fmt)
            if hl: a.font=BOLD; cc.font=BOLD; a.fill=fill(LGREEN); cc.fill=fill(LGREEN)
            a.border=BORDER; cc.border=BORDER; r+=1
        r+=1

    # ---------- 8. Methodology ----------
    ws4=wb.create_sheet("Methodology"); ws4.column_dimensions["A"].width=112
    notes=[("METHODOLOGY & SOURCE",H2),("",None),
     (f"Source: Shopify Admin API (orders, refunds, variants/unitCost, disputes, payouts, balance transactions). Period: {label}.",None),
     ("Net Sales = Gross − Discounts − Returns (current_subtotal_price; already net of refunds/edits).",None),
     ("COGS = (units sold − refunded) × Shopify cost-per-item. Coverage = % of sold units with a cost set; <100% means COGS understated.",None),
     ("Fees = balance-transaction fees: 'charge' = processing; 'dispute' = $15 chargeback fees net of won-dispute reversals.",None),
     ("Chargebacks = disputes initiated in period. Lost booked as expense (not in order revenue). Refunds already inside Net Sales (memo only).",None),
     ("Reserve = net of reserved_funds balance transactions (admin-placed review-holds may not appear in the API).",None),
     ("Cash/holds = balance-sheet view, not P&L expenses. Tax collected is passthrough, excluded from profit.",None),
     ("",None),("Yellow cells on 'Full P&L (Codex)' = external costs (ad spend, 3PL, software) to be completed from bank/ad data.",None)]
    for i,(txt,fnt) in enumerate(notes,1):
        c=ws4.cell(i,1,txt)
        if fnt: c.font=fnt
        elif txt: c.font=Font(size=10,color="333333")

    wb.save(out_path)
    return out_path

# --- helpers ---
from collections import defaultdict as _dd
def defaultdict_like(): return _dd(float)
def _totals(R):
    T={k:0.0 for k in ["gross","discounts","returns","net","shipping","tax","total","orders","cogs","fee_processing","fee_dispute","fee_total","refund_total","cb_lost","cb_open","cb_won","avail_pos","reserve"]}
    for x in R:
        for k in ["gross","discounts","returns","net","shipping","tax","total","orders","cogs","fee_processing","fee_dispute","fee_total","refund_total"]:
            T[k]+=x[k]
        T["cb_lost"]+=x["cb"]["lost"]; T["cb_open"]+=x["cb"]["open"]; T["cb_won"]+=x["cb"]["won"]
        T["avail_pos"]+= x["holds"]["available"] if x["holds"]["available"]>0 else 0
        T["reserve"]+=x["holds"]["reserve"]
    return T
