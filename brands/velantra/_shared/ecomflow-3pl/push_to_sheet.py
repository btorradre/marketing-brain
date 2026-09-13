#!/usr/bin/env python3
"""Push velantra_sku_list.PASTE-AT-B6.tsv into the ecomflow SKU sheet at B6.

Prereq: the sheet must be shared as Editor with btorradre@btoecventures.com.
Run from the marketing brain root:
    SSL_CERT_FILE=$(python3 -m certifi) python3 brands/velantra/_shared/ecomflow-3pl/push_to_sheet.py
"""
import json
import os
import urllib.parse
import urllib.request

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..")
SID = "1kqszUVpM63CbWQimaHvFIdMf1mYxyKZ6XktUkwy9ydU"
TSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "velantra_sku_list.PASTE-AT-B6.tsv")

tok = json.load(open(os.path.join(ROOT, "auth/bto-ec-google-auth/token.json")))
data = urllib.parse.urlencode({
    "client_id": tok["client_id"],
    "client_secret": tok["client_secret"],
    "refresh_token": tok["refresh_token"],
    "grant_type": "refresh_token",
}).encode()
access = json.load(urllib.request.urlopen(
    urllib.request.Request("https://oauth2.googleapis.com/token", data=data)))["access_token"]

rows = [ln.rstrip("\n").split("\t") for ln in open(TSV) if ln.strip()]
assert len(rows) == 62, f"expected 62 rows, got {len(rows)}"

body = json.dumps({"range": "Sheet1!B6", "majorDimension": "ROWS", "values": rows}).encode()
req = urllib.request.Request(
    f"https://sheets.googleapis.com/v4/spreadsheets/{SID}/values/B6?valueInputOption=USER_ENTERED",
    data=body, method="PUT",
    headers={"Authorization": f"Bearer {access}", "Content-Type": "application/json"})
r = json.load(urllib.request.urlopen(req))
print(f"Wrote {r['updatedRows']} rows x {r['updatedColumns']} cols to {r['updatedRange']}")
