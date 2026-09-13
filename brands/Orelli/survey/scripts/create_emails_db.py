#!/usr/bin/env python3
"""HISTORICAL — DO NOT RERUN. Created the original "Orelli — Emails" Notion DB
in the VELANTRA workspace (2026-07-22). The live DBs moved to the Orelli
workspace 2026-07-28 and the schema has since changed (Q3 Fair Price deleted,
Q4 options reworded). Rerunning would create a duplicate legacy-schema DB in
the wrong workspace. Kept for reference only.

  SSL_CERT_FILE=$(python3 -c "import certifi;print(certifi.where())") python3 create_emails_db.py
"""
import json
import sys
import urllib.request

VAULT = "/Users/brooksorradre2/Documents/marketing brain"
PARENT_PAGE = "369eca1a-f5bf-8033-8797-e24d688e0303"  # Velantra workspace "UGC" page
WTP_DB = "3a1eca1a-f5bf-818a-b368-e1e2fd46409b"
SHEET_ID = "19W6qmHsYM_A0KUiohkuthLilA5rp4z_cyStDJ-kBNDc"
LABELS = {
    "Q1 Pill Struggle": ["Every single time", "Certain pills only", "Big pills only"],
    "Q2 Keep In Cabinet": ["Definitely", "If it tastes decent"],
    "Q3 Fair Price": ["$19-24", "$25-29", "$30-35", "Whatever it costs"],
    "Q4 At $29.99": ["Stock up (2-3 bottles)", "One bottle", "Reviews first", "Wait for discount"],
}

tok = [l.split("=", 1)[1].strip() for l in open(f"{VAULT}/.env") if l.startswith("NOTION_TOKEN=")][0]


def notion(path, body=None, method=None):
    req = urllib.request.Request(
        f"https://api.notion.com/v1/{path}",
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Authorization": f"Bearer {tok}", "Notion-Version": "2022-06-28",
                 "Content-Type": "application/json"},
        method=method or ("POST" if body is not None else "GET"))
    try:
        with urllib.request.urlopen(req) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code} {path}\n{e.read().decode()[:400]}")


def sheet_rows():
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    import csv, io
    creds = Credentials.from_authorized_user_file(
        f"{VAULT}/auth/bto-ec-google-auth/token.json", ["https://www.googleapis.com/auth/drive"])
    creds.refresh(Request())
    req = urllib.request.Request(
        f"https://www.googleapis.com/drive/v3/files/{SHEET_ID}/export?mimeType=text/csv",
        headers={"Authorization": f"Bearer {creds.token}"})
    with urllib.request.urlopen(req) as r:
        rows = list(csv.reader(io.StringIO(r.read().decode())))
    return [{"email": x[0].strip(), "ts": x[1].strip() if len(x) > 1 else "",
             "source": "orelli-emails-sheet"} for x in rows[1:] if x and x[0].strip()]


def wtp_rows():
    out, cursor = [], None
    while True:
        body = {"page_size": 100, "filter": {"and": [
            {"property": "Status", "select": {"equals": "Complete"}},
            {"property": "Email", "email": {"is_not_empty": True}}]}}
        if cursor:
            body["start_cursor"] = cursor
        j = notion(f"databases/{WTP_DB}/query", body)
        for page in j["results"]:
            p = page["properties"]
            sel = lambda n: (p.get(n, {}).get("select") or {}).get("name", "")
            rt = lambda n: "".join(t["plain_text"] for t in p.get(n, {}).get("rich_text", []))
            out.append({"email": p["Email"]["email"], "ts": (p.get("Submitted", {}).get("date") or {}).get("start", ""),
                        "creator": rt("Creator"), "source": rt("Source") or "wtp-survey",
                        "answers": {n: sel(n) for n in LABELS if sel(n)}})
        if not j.get("has_more"):
            return out
        cursor = j["next_cursor"]


def props_for(row):
    props = {"Email": {"title": [{"text": {"content": row["email"]}}]}}
    if row.get("ts"):
        props["Timestamp"] = {"date": {"start": row["ts"]}}
    if row.get("creator"):
        props["Creator"] = {"rich_text": [{"text": {"content": row["creator"]}}]}
    if row.get("source"):
        props["Source"] = {"rich_text": [{"text": {"content": row["source"]}}]}
    for name, label in row.get("answers", {}).items():
        props[name] = {"select": {"name": label}}
    return props


def main():
    db = notion("databases", {
        "parent": {"type": "page_id", "page_id": PARENT_PAGE},
        "title": [{"type": "text", "text": {"content": "Orelli — Emails"}}],
        "properties": {
            "Email": {"title": {}},
            "Timestamp": {"date": {}},
            "Creator": {"rich_text": {}},
            **{name: {"select": {"options": [{"name": o} for o in opts]}} for name, opts in LABELS.items()},
            "Source": {"rich_text": {}},
        }})
    print("DB_ID:", db["id"])
    print("URL:", db.get("url"))

    seen, added = set(), 0
    for row in sorted(sheet_rows() + wtp_rows(), key=lambda r: r.get("ts", "")):
        key = row["email"].lower()
        if key in seen:
            continue
        seen.add(key)
        notion("pages", {"parent": {"database_id": db["id"]}, "properties": props_for(row)})
        added += 1
    print(f"seeded {added} unique emails")


if __name__ == "__main__":
    main()
