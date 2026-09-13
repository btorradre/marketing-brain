#!/usr/bin/env python3
"""Create the Velantra <> Supplier lead-time / processing-time sheet.

Run from the marketing brain root:
    SSL_CERT_FILE=$(python3 -m certifi) python3 <this file>
"""
import csv, json, os, urllib.parse, urllib.request
from collections import OrderedDict

ROOT = "/Users/brooksorradre2/Documents/marketing brain"
SKU_CSV = os.path.join(ROOT, "brands/velantra/_shared/ecomflow-3pl/velantra_sku_list.csv")

# ---------------------------------------------------------------- auth
tok = json.load(open(os.path.join(ROOT, "auth/bto-ec-google-auth/token.json")))
data = urllib.parse.urlencode({
    "client_id": tok["client_id"], "client_secret": tok["client_secret"],
    "refresh_token": tok["refresh_token"], "grant_type": "refresh_token",
}).encode()
ACCESS = json.load(urllib.request.urlopen(
    urllib.request.Request("https://oauth2.googleapis.com/token", data=data)))["access_token"]
H = {"Authorization": f"Bearer {ACCESS}", "Content-Type": "application/json"}

def api(url, body=None, method="POST"):
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None,
                                 method=method, headers=H)
    return json.load(urllib.request.urlopen(req))

# ---------------------------------------------------------------- source data
rows = list(csv.DictReader(open(SKU_CSV)))
products = OrderedDict()
for r in rows:
    hero = r["Hero SKU"]
    name = r["Product Name"].split(" - ")[0]
    products.setdefault(hero, {"name": name, "n": 0})
    products[hero]["n"] += 1

# ---------------------------------------------------------------- palette
NAVY   = {"red": 0.106, "green": 0.161, "blue": 0.239}
SLATE  = {"red": 0.290, "green": 0.337, "blue": 0.408}
YELLOW = {"red": 1.000, "green": 0.976, "blue": 0.851}
GREY   = {"red": 0.949, "green": 0.949, "blue": 0.941}
BORDER = {"red": 0.800, "green": 0.800, "blue": 0.788}
WHITE  = {"red": 1, "green": 1, "blue": 1}
AMBER  = {"red": 0.996, "green": 0.902, "blue": 0.667}

def txt(v, bold=False, size=10, color=None, wrap=True, italic=False):
    return {"userEnteredValue": ({"stringValue": v} if isinstance(v, str) else {"numberValue": v}),
            "userEnteredFormat": {"textFormat": {"bold": bold, "fontSize": size,
                                                 "foregroundColor": color or {"red": 0, "green": 0, "blue": 0},
                                                 "italic": italic},
                                  "wrapStrategy": "WRAP" if wrap else "OVERFLOW_CELL",
                                  "verticalAlignment": "MIDDLE"}}

# ================================================================ create
SHEETS = ["START HERE 开始", "Lead Times 交期", "Stock by SKU 库存", "Definitions 说明", "Lists"]
ss = api("https://sheets.googleapis.com/v4/spreadsheets", {
    "properties": {"title": "Velantra <> Supplier | Lead Times & Processing Times 交期与处理时间",
                   "locale": "en_US"},
    "sheets": [{"properties": {"title": t, "index": i,
                               "gridProperties": {"rowCount": 200, "columnCount": 20}}}
               for i, t in enumerate(SHEETS)],
})
SID = ss["spreadsheetId"]
IDS = {s["properties"]["title"]: s["properties"]["sheetId"] for s in ss["sheets"]}
print("created", SID)

# ================================================================ values
V = []

# ---------- START HERE
start = [
    ["Velantra — Product Lead Times & Processing Times"],
    ["Velantra 产品交期与订单处理时间表"],
    [""],
    ["Please complete every yellow cell and send this sheet back. Keep it updated — we check it before every order."],
    ["请填写所有黄色单元格后发回给我们。请保持更新 — 我们每次下单前都会查看这份表格。"],
    [""],
    ["HOW TO FILL THIS IN  填写说明"],
    ["1", "Yellow cells = you fill in. Grey cells = filled by Velantra, please do not change them.",
     "黄色单元格 = 您填写。灰色单元格 = Velantra 已填写，请勿修改。"],
    ["2", "Tab 'Lead Times 交期' — 11 rows, one per product. This is the most important tab.",
     "'Lead Times 交期' 标签页 — 11 行，每个产品一行。这是最重要的一页。"],
    ["3", "Tab 'Stock by SKU 库存' — 62 rows, one per colorway. Stock status and quantity only.",
     "'Stock by SKU 库存' 标签页 — 62 行，每个颜色一行。只需填写库存状态和数量。"],
    ["4", "All times in BUSINESS DAYS (Mon–Fri, excluding Chinese public holidays). Numbers only, no text.",
     "所有时间请以工作日计算（周一至周五，不含中国法定节假日）。只填数字，不要写文字。"],
    ["5", "If a time varies, give the realistic longest case — not the best case. We plan our stock on these numbers.",
     "如果时间有波动，请填写实际最长的情况，而不是最理想的情况。我们依据这些数字安排库存。"],
    ["6", "If something does not apply to a product, write N/A. Do not leave a cell blank.",
     "如果某项不适用于该产品，请填写 N/A。请不要留空。"],
    ["7", "See the 'Definitions 说明' tab for exactly what each column means.",
     "每一列的具体含义请查看 'Definitions 说明' 标签页。"],
    [""],
    ["SIGN-OFF  签字确认"],
    ["Completed by (name)  填写人姓名", ""],
    ["Company  公司名称", ""],
    ["Date completed  填写日期", ""],
    ["Email  邮箱", ""],
    ["WeChat / WhatsApp  微信 / WhatsApp", ""],
]
V.append({"range": f"'{SHEETS[0]}'!A1", "values": start})

# ---------- Lead Times
lt_en = ["Product", "Velantra Code", "# of Colorways",
         "Supplier Item Code", "Stock or Made to Order?",
         "Processing Time — single orders (business days)",
         "MOQ (units)",
         "Production Lead Time — 100 units (business days)",
         "Production Lead Time — 500 units (business days)",
         "QC + Packing (business days)",
         "Air Express to US Warehouse (business days)",
         "Sea Freight to US Warehouse (business days)",
         "TOTAL: PO → in hand at US warehouse (auto)",
         "Peak season / holiday extra delay (days)",
         "Notes / constraints"]
lt_cn = ["产品", "Velantra 编号", "颜色数量",
         "供应商货号", "现货还是定制生产？",
         "单件订单处理时间（工作日）",
         "最小起订量（件）",
         "生产周期 — 100 件（工作日）",
         "生产周期 — 500 件（工作日）",
         "质检 + 包装（工作日）",
         "空运快递到美国仓库（工作日）",
         "海运到美国仓库（工作日）",
         "总交期：下单 → 美国仓库到货（自动计算）",
         "旺季 / 节假日额外延迟（天）",
         "备注 / 限制条件"]

lt = [["Velantra — Lead Times by Product  各产品交期"], [""],
      ["FILLED BY VELANTRA — DO NOT EDIT  由 VELANTRA 填写，请勿修改", "", "",
       "TO BE COMPLETED BY SUPPLIER — 请供应商填写"],
      lt_en, lt_cn]
r = 6
for hero, p in products.items():
    lt.append([p["name"], hero, p["n"], "", "", "", "", "", "", "", "", "",
               f'=IF(COUNT(H{r},J{r},K{r})=3,H{r}+J{r}+K{r},"")', "", ""])
    r += 1
V.append({"range": f"'{SHEETS[1]}'!A1", "values": lt})

# ---------- Stock by SKU
sk_en = ["Product", "Colorway", "Velantra SKU", "Supplier Item Code", "Stock Status",
         "Units in Stock Now", "If out of stock, ready date", "Processing Time (business days)", "Notes"]
sk_cn = ["产品", "颜色", "Velantra SKU", "供应商货号", "库存状态",
         "现有库存（件）", "缺货的话，预计到货日期", "处理时间（工作日）", "备注"]
sk = [["Velantra — Stock & Processing by Colorway  各颜色库存与处理时间"], [""],
      ["FILLED BY VELANTRA — DO NOT EDIT  由 VELANTRA 填写，请勿修改", "", "",
       "TO BE COMPLETED BY SUPPLIER — 请供应商填写"],
      sk_en, sk_cn]
for row in rows:
    full = row["Product Name"]
    base, _, color = full.partition(" - ")
    sk.append([base, color or "—", row["Shopify SKU Variants"], "", "", "", "", "", ""])
V.append({"range": f"'{SHEETS[2]}'!A1", "values": sk})

# ---------- Definitions
d = [
    ["Definitions — what each column means  各列含义说明"], [""],
    ["The timeline we are measuring  我们要衡量的时间线"], [""],
    ["  Single customer order  单个客户订单:"],
    ["    order received 收到订单  →  picked & packed 拣货打包  →  handed to carrier with a real tracking scan 交给快递并有真实扫描记录"],
    ["    That whole span is the PROCESSING TIME.  这整段时间就是「处理时间」。"],
    ["    It ENDS when the carrier physically scans the parcel — not when a tracking number is created."],
    ["    处理时间结束于快递公司实际扫描包裹的那一刻 — 而不是生成运单号的那一刻。"], [""],
    ["  Bulk purchase order  批量订单:"],
    ["    PO placed 下单  →  production 生产  →  QC + packing 质检打包  →  freight 运输  →  in hand at US warehouse 到达美国仓库"],
    ["    That whole span is the TOTAL LEAD TIME.  这整段时间就是「总交期」。"], [""],
    ["Column by column  逐列说明"], [""],
    ["Supplier Item Code 供应商货号",
     "Your own internal code for this product, so we can match your system to ours.",
     "贵司内部的产品编号，方便我们两边系统对应。"],
    ["Stock or Made to Order? 现货还是定制生产？",
     "Do you hold finished units on hand, or is each order produced after we place it?",
     "是否有成品现货，还是每次下单后才生产？"],
    ["Processing Time — single orders 单件订单处理时间",
     "For one unit of an IN-STOCK item: order received → carrier scan. Business days.",
     "有现货的情况下，单件订单：收到订单 → 快递扫描。以工作日计。"],
    ["MOQ 最小起订量", "Smallest number of units you will produce in one run for this product.",
     "该产品一次生产的最小数量。"],
    ["Production Lead Time — 100 / 500 units 生产周期",
     "Cutting starts → finished units off the line, for that order size. Business days.",
     "从开始裁剪 → 成品下线，按该订单数量计算。以工作日计。"],
    ["QC + Packing 质检 + 包装", "After production finishes: inspection, polybagging, cartonisation.",
     "生产完成后：检验、装袋、装箱所需时间。"],
    ["Air Express / Sea Freight to US Warehouse 空运 / 海运到美国仓库",
     "Cartons leave your facility → received at our US 3PL. Business days, door to door.",
     "货箱离开贵司 → 我们美国仓库签收。门到门，以工作日计。"],
    ["TOTAL 总交期", "Calculated automatically: production (100u) + QC/packing + air express. Do not type in this column.",
     "自动计算：生产周期(100件) + 质检打包 + 空运快递。此列请勿填写。"],
    ["Peak season delay 旺季延迟",
     "Extra days to add around Chinese New Year, Golden Week, Singles Day, and peak Q4.",
     "春节、黄金周、双十一及第四季度旺季需额外增加的天数。"],
    ["Stock Status 库存状态",
     "In Stock 有货 / Made to Order 定制生产 / Out of Stock 缺货 / Discontinued 已停产",
     ""],
    [""],
    ["Two rules that matter most to us  对我们最重要的两条规则"], [""],
    ["1", "A tracking number is not a shipment. If a parcel has not been physically scanned by the carrier, it has not shipped, and the processing time is still running.",
     "运单号不等于已发货。如果包裹没有被快递公司实际扫描，就不算已发货，处理时间仍在计算中。"],
    ["2", "We would rather have a slow honest number than a fast optimistic one. We build our stock plan on these figures, so an underestimate costs us far more than a long lead time does.",
     "我们宁可要一个较慢但真实的数字，也不要一个乐观但不准的数字。我们依据这些数字制定库存计划，低估造成的损失远大于交期本身长一些。"],
]
V.append({"range": f"'{SHEETS[3]}'!A1", "values": d})

# ---------- Lists
V.append({"range": f"'{SHEETS[4]}'!A1", "values": [
    ["Stock Status", "Stock or Made to Order"],
    ["In Stock 有货", "Held in stock 备有现货"],
    ["Made to Order 定制生产", "Made to order 定制生产"],
    ["Out of Stock 缺货", "Both 两者皆有"],
    ["Discontinued 已停产", ""],
]})

api(f"https://sheets.googleapis.com/v4/spreadsheets/{SID}/values:batchUpdate",
    {"valueInputOption": "USER_ENTERED", "data": V})
print("values written")

# ================================================================ formatting
LAST_LT = 5 + len(products)      # 1-indexed last data row on Lead Times
LAST_SK = 5 + len(rows)
req = []

def fmt(sheet, r0, r1, c0, c1, cell, fields):
    req.append({"repeatCell": {"range": {"sheetId": IDS[sheet], "startRowIndex": r0, "endRowIndex": r1,
                                         "startColumnIndex": c0, "endColumnIndex": c1},
                               "cell": cell, "fields": fields}})

def dims(sheet, c0, c1, px):
    req.append({"updateDimensionProperties": {
        "range": {"sheetId": IDS[sheet], "dimension": "COLUMNS", "startIndex": c0, "endIndex": c1},
        "properties": {"pixelSize": px}, "fields": "pixelSize"}})

def rowh(sheet, r0, r1, px):
    req.append({"updateDimensionProperties": {
        "range": {"sheetId": IDS[sheet], "dimension": "ROWS", "startIndex": r0, "endIndex": r1},
        "properties": {"pixelSize": px}, "fields": "pixelSize"}})

# ---- global: white base, readable font
for s in SHEETS:
    fmt(s, 0, 200, 0, 20,
        {"userEnteredFormat": {"backgroundColor": WHITE,
                               "textFormat": {"fontFamily": "Inter", "fontSize": 10},
                               "verticalAlignment": "MIDDLE"}},
        "userEnteredFormat(backgroundColor,textFormat,verticalAlignment)")

# ---- START HERE
s = SHEETS[0]
dims(s, 0, 1, 260); dims(s, 1, 2, 620); dims(s, 2, 3, 620)
fmt(s, 0, 1, 0, 3, {"userEnteredFormat": {"textFormat": {"bold": True, "fontSize": 20, "foregroundColor": NAVY}}},
    "userEnteredFormat.textFormat")
fmt(s, 1, 2, 0, 3, {"userEnteredFormat": {"textFormat": {"fontSize": 14, "foregroundColor": SLATE}}},
    "userEnteredFormat.textFormat")
fmt(s, 3, 5, 0, 3, {"userEnteredFormat": {"backgroundColor": AMBER, "textFormat": {"bold": True, "fontSize": 11},
                                          "wrapStrategy": "WRAP", "padding": {"top": 6, "bottom": 6, "left": 8, "right": 8}}},
    "userEnteredFormat(backgroundColor,textFormat,wrapStrategy,padding)")
for hr in (6, 15):  # section headers
    fmt(s, hr, hr + 1, 0, 3, {"userEnteredFormat": {"backgroundColor": NAVY,
                                                    "textFormat": {"bold": True, "fontSize": 11, "foregroundColor": WHITE},
                                                    "padding": {"left": 8}}},
        "userEnteredFormat(backgroundColor,textFormat,padding)")
fmt(s, 7, 14, 0, 1, {"userEnteredFormat": {"horizontalAlignment": "CENTER",
                                           "textFormat": {"bold": True, "foregroundColor": SLATE}}},
    "userEnteredFormat(horizontalAlignment,textFormat)")
fmt(s, 7, 14, 1, 3, {"userEnteredFormat": {"wrapStrategy": "WRAP", "padding": {"left": 8, "top": 4, "bottom": 4}}},
    "userEnteredFormat(wrapStrategy,padding)")
fmt(s, 16, 21, 0, 1, {"userEnteredFormat": {"textFormat": {"bold": True}, "padding": {"left": 8}}},
    "userEnteredFormat(textFormat,padding)")
fmt(s, 16, 21, 1, 2, {"userEnteredFormat": {"backgroundColor": YELLOW,
                                            "borders": {"top": {"style": "SOLID", "color": BORDER},
                                                        "bottom": {"style": "SOLID", "color": BORDER},
                                                        "left": {"style": "SOLID", "color": BORDER},
                                                        "right": {"style": "SOLID", "color": BORDER}}}},
    "userEnteredFormat(backgroundColor,borders)")
rowh(s, 7, 14, 40)
rowh(s, 16, 21, 30)

# ---- shared grid styling for the two data tabs
def style_grid(sheet, last_row, ncols, lock_cols, fill_start):
    dims(sheet, 0, 1, 200)
    dims(sheet, 1, lock_cols, 130)
    dims(sheet, lock_cols, ncols, 118)
    # title
    fmt(sheet, 0, 1, 0, ncols, {"userEnteredFormat": {"textFormat": {"bold": True, "fontSize": 16, "foregroundColor": NAVY}}},
        "userEnteredFormat.textFormat")
    # band row 3
    req.append({"mergeCells": {"range": {"sheetId": IDS[sheet], "startRowIndex": 2, "endRowIndex": 3,
                                         "startColumnIndex": 0, "endColumnIndex": lock_cols}, "mergeType": "MERGE_ALL"}})
    req.append({"mergeCells": {"range": {"sheetId": IDS[sheet], "startRowIndex": 2, "endRowIndex": 3,
                                         "startColumnIndex": lock_cols, "endColumnIndex": ncols}, "mergeType": "MERGE_ALL"}})
    fmt(sheet, 2, 3, 0, lock_cols, {"userEnteredFormat": {"backgroundColor": SLATE, "horizontalAlignment": "CENTER",
                                                          "textFormat": {"bold": True, "fontSize": 10, "foregroundColor": WHITE}}},
        "userEnteredFormat(backgroundColor,horizontalAlignment,textFormat)")
    fmt(sheet, 2, 3, lock_cols, ncols, {"userEnteredFormat": {"backgroundColor": {"red": 0.85, "green": 0.62, "blue": 0.13},
                                                              "horizontalAlignment": "CENTER",
                                                              "textFormat": {"bold": True, "fontSize": 10, "foregroundColor": WHITE}}},
        "userEnteredFormat(backgroundColor,horizontalAlignment,textFormat)")
    # header rows 4 (EN) + 5 (CN)
    fmt(sheet, 3, 4, 0, ncols, {"userEnteredFormat": {"backgroundColor": NAVY, "wrapStrategy": "WRAP",
                                                      "horizontalAlignment": "CENTER", "verticalAlignment": "BOTTOM",
                                                      "textFormat": {"bold": True, "fontSize": 10, "foregroundColor": WHITE},
                                                      "padding": {"left": 6, "right": 6, "top": 4}}},
        "userEnteredFormat(backgroundColor,wrapStrategy,horizontalAlignment,verticalAlignment,textFormat,padding)")
    fmt(sheet, 4, 5, 0, ncols, {"userEnteredFormat": {"backgroundColor": NAVY, "wrapStrategy": "WRAP",
                                                      "horizontalAlignment": "CENTER", "verticalAlignment": "TOP",
                                                      "textFormat": {"fontSize": 9, "foregroundColor": {"red": 0.78, "green": 0.83, "blue": 0.89}},
                                                      "padding": {"left": 6, "right": 6, "bottom": 4}}},
        "userEnteredFormat(backgroundColor,wrapStrategy,horizontalAlignment,verticalAlignment,textFormat,padding)")
    rowh(sheet, 3, 4, 62); rowh(sheet, 4, 5, 46)
    # locked cols
    fmt(sheet, 5, last_row, 0, lock_cols, {"userEnteredFormat": {"backgroundColor": GREY,
                                                                 "textFormat": {"foregroundColor": SLATE},
                                                                 "padding": {"left": 6}}},
        "userEnteredFormat(backgroundColor,textFormat,padding)")
    # fill cols
    fmt(sheet, 5, last_row, fill_start, ncols, {"userEnteredFormat": {"backgroundColor": YELLOW,
                                                                      "horizontalAlignment": "CENTER"}},
        "userEnteredFormat(backgroundColor,horizontalAlignment)")
    # borders
    req.append({"updateBorders": {
        "range": {"sheetId": IDS[sheet], "startRowIndex": 2, "endRowIndex": last_row,
                  "startColumnIndex": 0, "endColumnIndex": ncols},
        "innerHorizontal": {"style": "SOLID", "color": BORDER},
        "innerVertical": {"style": "SOLID", "color": BORDER},
        "top": {"style": "SOLID_MEDIUM", "color": SLATE}, "bottom": {"style": "SOLID_MEDIUM", "color": SLATE},
        "left": {"style": "SOLID_MEDIUM", "color": SLATE}, "right": {"style": "SOLID_MEDIUM", "color": SLATE}}})
    rowh(sheet, 5, last_row, 30)
    # freeze
    req.append({"updateSheetProperties": {
        "properties": {"sheetId": IDS[sheet], "gridProperties": {"frozenRowCount": 5, "frozenColumnCount": lock_cols}},
        "fields": "gridProperties(frozenRowCount,frozenColumnCount)"}})

style_grid(SHEETS[1], LAST_LT, 15, 3, 3)
style_grid(SHEETS[2], LAST_SK, 9, 3, 3)

# TOTAL column on Lead Times: computed, not a fill cell
fmt(SHEETS[1], 5, LAST_LT, 12, 13, {"userEnteredFormat": {"backgroundColor": {"red": 0.902, "green": 0.933, "blue": 0.906},
                                                          "textFormat": {"bold": True}, "horizontalAlignment": "CENTER"}},
    "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)")
# Notes columns left-aligned
fmt(SHEETS[1], 5, LAST_LT, 14, 15, {"userEnteredFormat": {"horizontalAlignment": "LEFT", "wrapStrategy": "WRAP",
                                                          "padding": {"left": 6}}},
    "userEnteredFormat(horizontalAlignment,wrapStrategy,padding)")
fmt(SHEETS[2], 5, LAST_SK, 8, 9, {"userEnteredFormat": {"horizontalAlignment": "LEFT", "wrapStrategy": "WRAP",
                                                        "padding": {"left": 6}}},
    "userEnteredFormat(horizontalAlignment,wrapStrategy,padding)")
dims(SHEETS[1], 14, 15, 240); dims(SHEETS[2], 8, 9, 220)
dims(SHEETS[2], 1, 2, 190); dims(SHEETS[2], 2, 3, 150)

# ---- Definitions tab
s = SHEETS[3]
dims(s, 0, 1, 300); dims(s, 1, 2, 560); dims(s, 2, 3, 480)
fmt(s, 0, 1, 0, 3, {"userEnteredFormat": {"textFormat": {"bold": True, "fontSize": 16, "foregroundColor": NAVY}}},
    "userEnteredFormat.textFormat")
for hr in (2, 14, 30):
    fmt(s, hr, hr + 1, 0, 3, {"userEnteredFormat": {"backgroundColor": NAVY,
                                                    "textFormat": {"bold": True, "fontSize": 11, "foregroundColor": WHITE},
                                                    "padding": {"left": 8}}},
        "userEnteredFormat(backgroundColor,textFormat,padding)")
fmt(s, 4, 13, 0, 1, {"userEnteredFormat": {"textFormat": {"fontFamily": "Roboto Mono", "fontSize": 9,
                                                          "foregroundColor": SLATE}}},
    "userEnteredFormat.textFormat")
fmt(s, 16, 30, 0, 1, {"userEnteredFormat": {"textFormat": {"bold": True}, "padding": {"left": 8}, "wrapStrategy": "WRAP"}},
    "userEnteredFormat(textFormat,padding,wrapStrategy)")
fmt(s, 16, 34, 1, 3, {"userEnteredFormat": {"wrapStrategy": "WRAP", "padding": {"left": 8, "top": 4, "bottom": 4}}},
    "userEnteredFormat(wrapStrategy,padding)")
fmt(s, 32, 34, 0, 1, {"userEnteredFormat": {"horizontalAlignment": "CENTER",
                                            "textFormat": {"bold": True, "foregroundColor": SLATE}}},
    "userEnteredFormat(horizontalAlignment,textFormat)")
fmt(s, 32, 34, 0, 3, {"userEnteredFormat": {"backgroundColor": AMBER}}, "userEnteredFormat.backgroundColor")
rowh(s, 16, 34, 40)

# ---- data validation
def dv(sheet, r0, r1, c0, c1, src_range, strict=True):
    req.append({"setDataValidation": {
        "range": {"sheetId": IDS[sheet], "startRowIndex": r0, "endRowIndex": r1,
                  "startColumnIndex": c0, "endColumnIndex": c1},
        "rule": {"condition": {"type": "ONE_OF_RANGE", "values": [{"userEnteredValue": src_range}]},
                 "showCustomUi": True, "strict": strict}}})

dv(SHEETS[1], 5, LAST_LT, 4, 5, f"='{SHEETS[4]}'!$B$2:$B$4")     # stock or MTO
dv(SHEETS[2], 5, LAST_SK, 4, 5, f"='{SHEETS[4]}'!$A$2:$A$5")     # stock status

# numeric-only guards on the day columns
def numguard(sheet, r0, r1, c0, c1):
    req.append({"setDataValidation": {
        "range": {"sheetId": IDS[sheet], "startRowIndex": r0, "endRowIndex": r1,
                  "startColumnIndex": c0, "endColumnIndex": c1},
        "rule": {"condition": {"type": "NUMBER_GREATER_THAN_EQ", "values": [{"userEnteredValue": "0"}]},
                 "inputMessage": "Business days — numbers only  工作日 — 只填数字",
                 "strict": False}}})

numguard(SHEETS[1], 5, LAST_LT, 5, 12)   # F..L
numguard(SHEETS[1], 5, LAST_LT, 13, 14)  # N
numguard(SHEETS[2], 5, LAST_SK, 5, 6)    # F units
numguard(SHEETS[2], 5, LAST_SK, 7, 8)    # H processing

# date format on ready-date col
fmt(SHEETS[2], 5, LAST_SK, 6, 7, {"userEnteredFormat": {"numberFormat": {"type": "DATE", "pattern": "yyyy-mm-dd"}}},
    "userEnteredFormat.numberFormat")

# ---- conditional format: highlight blank required cells
for sheet, last, c0, c1 in [(SHEETS[1], LAST_LT, 3, 12), (SHEETS[1], LAST_LT, 13, 15),
                            (SHEETS[2], LAST_SK, 3, 8)]:
    req.append({"addConditionalFormatRule": {"rule": {
        "ranges": [{"sheetId": IDS[sheet], "startRowIndex": 5, "endRowIndex": last,
                    "startColumnIndex": c0, "endColumnIndex": c1}],
        "booleanRule": {"condition": {"type": "BLANK"},
                        "format": {"backgroundColor": {"red": 1.0, "green": 0.949, "blue": 0.800}}}},
        "index": 0}})

# ---- protect the Velantra columns (warning only; supplier is an editor)
for sheet, last, lock in [(SHEETS[1], LAST_LT, 3), (SHEETS[2], LAST_SK, 3)]:
    req.append({"addProtectedRange": {"protectedRange": {
        "range": {"sheetId": IDS[sheet], "startRowIndex": 0, "endRowIndex": last,
                  "startColumnIndex": 0, "endColumnIndex": lock},
        "description": "Filled by Velantra — please do not edit  由 Velantra 填写，请勿修改",
        "warningOnly": True}}})
req.append({"addProtectedRange": {"protectedRange": {
    "range": {"sheetId": IDS[SHEETS[1]], "startRowIndex": 0, "endRowIndex": LAST_LT,
              "startColumnIndex": 12, "endColumnIndex": 13},
    "description": "Calculated automatically  自动计算", "warningOnly": True}}})
for t in (SHEETS[0], SHEETS[3]):
    req.append({"addProtectedRange": {"protectedRange": {
        "range": {"sheetId": IDS[t], "startRowIndex": 0, "endRowIndex": 40,
                  "startColumnIndex": 0, "endColumnIndex": 1},
        "description": "Reference  参考", "warningOnly": True}}})

# hide the Lists tab
req.append({"updateSheetProperties": {"properties": {"sheetId": IDS[SHEETS[4]], "hidden": True},
                                      "fields": "hidden"}})
# hide gridlines on the two prose tabs
for t in (SHEETS[0], SHEETS[3]):
    req.append({"updateSheetProperties": {"properties": {"sheetId": IDS[t], "gridProperties": {"hideGridlines": True}},
                                          "fields": "gridProperties.hideGridlines"}})

api(f"https://sheets.googleapis.com/v4/spreadsheets/{SID}:batchUpdate", {"requests": req})
print("formatted")
print(f"https://docs.google.com/spreadsheets/d/{SID}/edit")
