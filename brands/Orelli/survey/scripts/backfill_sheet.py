#!/usr/bin/env python3
"""One-shot sync: Notion "Orelli — WTP Survey Responses" → "Orelli Emails" Google Sheet.

Run after (a) Sheets API is enabled on GCP project 863548873182 and
(b) btorradre@btoecventures.com has Editor on the sheet. Safe to re-run:
dedupes on email against rows already in the sheet.

  SSL_CERT_FILE=$(python3 -c "import certifi;print(certifi.where())") python3 backfill_sheet.py
"""
import json
import os
import sys
import urllib.request

VAULT = "/Users/brooksorradre2/Documents/marketing brain"
TOKEN_FILE = os.path.join(VAULT, "auth/bto-ec-google-auth/token.json")
SHEET_ID = "19W6qmHsYM_A0KUiohkuthLilA5rp4z_cyStDJ-kBNDc"
# Orelli workspace DB (survey backend moved off the Velantra workspace 2026-07-28)
NOTION_DB_ID = "3ab0cd83-f2e5-8166-abda-ea607827c9fb"
HEADER_EXT = ["Creator", "Q1 Pill Struggle", "Q2 Keep In Cabinet", "(retired)", "Q3 At $29.99", "Source"]


def notion_token():
    with open(os.path.join(VAULT, ".env")) as f:
        for line in f:
            if line.startswith("ORELLI_NOTION_TOKEN="):
                return line.split("=", 1)[1].strip()
    sys.exit("ORELLI_NOTION_TOKEN not found in .env")


def google_token():
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, ["https://www.googleapis.com/auth/drive"])
    creds.refresh(Request())
    return creds.token


def call(url, token, body=None, method=None, notion=False):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    if notion:
        headers["Notion-Version"] = "2022-06-28"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method or ("POST" if data else "GET"))
    try:
        with urllib.request.urlopen(req) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code} {url.split('?')[0]}\n{e.read().decode()[:400]}")


def fetch_notion_rows(ntoken):
    rows, cursor = [], None
    while True:
        body = {"page_size": 100, "filter": {"and": [
            {"property": "Status", "select": {"equals": "Complete"}},
            {"property": "Email", "email": {"is_not_empty": True}},
        ]}}
        if cursor:
            body["start_cursor"] = cursor
        j = call(f"https://api.notion.com/v1/databases/{NOTION_DB_ID}/query", ntoken, body, notion=True)
        for page in j.get("results", []):
            p = page["properties"]
            sel = lambda name: (p.get(name, {}).get("select") or {}).get("name", "")
            rt = lambda name: "".join(t["plain_text"] for t in p.get(name, {}).get("rich_text", []))
            rows.append([
                p.get("Email", {}).get("email") or "",
                (p.get("Submitted", {}).get("date") or {}).get("start", ""),
                rt("Creator"),
                sel("Q1 Pill Struggle"), sel("Q2 Keep In Cabinet"),
                # column F is a blank spacer where retired Q3 lived (property deleted from Notion)
                "", sel("Q3 At $29.99"),
                rt("Source"),
            ])
        if not j.get("has_more"):
            return rows
        cursor = j.get("next_cursor")


def main():
    gtoken = google_token()
    ntoken = notion_token()

    sheet = call(f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/A:H", gtoken)
    existing = sheet.get("values", [])
    have = {r[0].strip().lower() for r in existing[1:] if r and r[0].strip()}

    if not existing:
        call(f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/A1:H1?valueInputOption=RAW",
             gtoken, {"values": [["Email", "Timestamp"] + HEADER_EXT]}, method="PUT")
        print("header written: A1:H1")
    elif len(existing[0]) < 8:
        call(f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/C1:H1?valueInputOption=RAW",
             gtoken, {"values": [HEADER_EXT]}, method="PUT")
        print("header extended: C1:H1 =", ", ".join(HEADER_EXT))

    rows = fetch_notion_rows(ntoken)
    fresh = [r for r in rows if r[0].strip().lower() not in have]
    print(f"notion complete responses: {len(rows)} | already in sheet: {len(rows) - len(fresh)} | to append: {len(fresh)}")
    if fresh:
        fresh.sort(key=lambda r: r[1])
        call(f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/A:H:append"
             "?valueInputOption=RAW&insertDataOption=INSERT_ROWS", gtoken, {"values": fresh})
        print(f"appended {len(fresh)} rows")


if __name__ == "__main__":
    main()
