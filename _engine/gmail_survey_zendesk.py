#!/usr/bin/env python3
"""Survey Zendesk / BTO EC Ventures notification mail before acting."""
import collections, json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOK = "/Users/brooksorradre2/Documents/marketing brain/_engine/oauth credentials/btorradre_gmail_modify_token.json"
svc = build("gmail", "v1", credentials=Credentials.from_authorized_user_file(TOK))

QUERIES = {
    "bto_subject": 'subject:"[BTO EC Ventures]"',
    "zendesk_domain": "from:zendesk.com",
    "zendeskcom_any": "zendesk",
}

for name, q in QUERIES.items():
    senders = collections.Counter()
    subjects = collections.Counter()
    ids, tok = [], None
    while True:
        r = svc.users().messages().list(userId="me", q=q, maxResults=500, pageToken=tok).execute()
        ids += [m["id"] for m in r.get("messages", [])]
        tok = r.get("nextPageToken")
        if not tok:
            break
    print(f"\n=== {name}: {q} -> {len(ids)} messages ===")
    for mid in ids[:400]:
        m = svc.users().messages().get(
            userId="me", id=mid, format="metadata",
            metadataHeaders=["From", "Subject"]).execute()
        h = {x["name"]: x["value"] for x in m["payload"].get("headers", [])}
        f = h.get("From", "?")
        addr = f.split("<")[-1].strip("> ").lower()
        senders[addr] += 1
        subjects[h.get("Subject", "?")[:70]] += 1
    for a, c in senders.most_common(20):
        print(f"  {c:5d}  {a}")
    print("  -- sample subjects --")
    for s, c in subjects.most_common(6):
        print(f"  {c:5d}  {s}")
