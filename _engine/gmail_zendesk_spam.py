#!/usr/bin/env python3
"""Move Zendesk / BTO EC Ventures ticket notifications to Spam + create filters."""
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOK = "/Users/brooksorradre2/Documents/marketing brain/_engine/oauth credentials/btorradre_gmail_modify_token.json"
svc = build("gmail", "v1", credentials=Credentials.from_authorized_user_file(TOK))

# Precise: Zendesk notification mail only. Deliberately NOT a bare subject match on
# "[BTO EC Ventures]" -- that also hits real Armanino / Tom / Chargeblast threads.
TARGETS = [
    ('from:customerservice@velantrafashion.com subject:"[BTO EC Ventures]"', "Zendesk ticket notifications"),
    ("from:(zendesk.com OR support.zendesk.com OR btoecventures.zendesk.com)", "Zendesk vendor mail"),
]


def ids_for(q):
    out, tok = [], None
    while True:
        r = svc.users().messages().list(userId="me", q=q, maxResults=500, pageToken=tok).execute()
        out += [m["id"] for m in r.get("messages", [])]
        tok = r.get("nextPageToken")
        if not tok:
            break
    return out


print("=== EXISTING FILTERS ===")
for f in svc.users().settings().filters().list(userId="me").execute().get("filter", []):
    print(" ", f["id"], f.get("criteria"), "->", f.get("action"))

if "--go" not in sys.argv:
    for q, label in TARGETS:
        print(f"\nDRY RUN {label}: {len(ids_for(q))} messages match\n  {q}")
    sys.exit(0)

# 1. Move existing mail to Spam
total = 0
for q, label in TARGETS:
    ids = ids_for(q)
    for i in range(0, len(ids), 900):
        chunk = ids[i:i + 900]
        svc.users().messages().batchModify(userId="me", body={
            "ids": chunk,
            "addLabelIds": ["SPAM"],
            "removeLabelIds": ["INBOX"],
        }).execute()
    total += len(ids)
    print(f"MOVED {len(ids)} -> Spam  ({label})")
print(f"TOTAL moved: {total}")

# 2. Create filters so future mail skips the inbox.
# Gmail rejects SPAM in a filter's addLabelIds -- there is no "mark as spam"
# filter action. TRASH is the closest supported equivalent; same 30-day purge.
for q, label in TARGETS:
    created = svc.users().settings().filters().create(userId="me", body={
        "criteria": {"query": q},
        "action": {"addLabelIds": ["TRASH"], "removeLabelIds": ["INBOX"]},
    }).execute()
    print(f"FILTER {created['id']}  ({label})  {q}")
