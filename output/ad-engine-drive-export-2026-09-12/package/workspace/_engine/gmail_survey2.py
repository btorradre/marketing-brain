#!/usr/bin/env python3
"""Second pass: what else comes from customerservice@velantrafashion.com?"""
import collections
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOK = "/Users/brooksorradre2/Documents/marketing brain/_engine/oauth credentials/btorradre_gmail_modify_token.json"
svc = build("gmail", "v1", credentials=Credentials.from_authorized_user_file(TOK))


def scan(q, label, cap=600):
    ids, tok = [], None
    while True:
        r = svc.users().messages().list(userId="me", q=q, maxResults=500, pageToken=tok).execute()
        ids += [m["id"] for m in r.get("messages", [])]
        tok = r.get("nextPageToken")
        if not tok or len(ids) >= cap:
            break
    subs = collections.Counter()
    for mid in ids[:cap]:
        m = svc.users().messages().get(userId="me", id=mid, format="metadata",
                                       metadataHeaders=["Subject"]).execute()
        h = {x["name"]: x["value"] for x in m["payload"].get("headers", [])}
        subs[h.get("Subject", "?")[:85]] += 1
    print(f"\n=== {label}: {q} -> {len(ids)} msgs ===")
    for s, c in subs.most_common(30):
        print(f"  {c:4d}  {s}")
    return len(ids)


# Everything ever from the Velantra CS address
scan("from:customerservice@velantrafashion.com", "ALL from CS address")
# The precise notification pattern
scan('from:customerservice@velantrafashion.com subject:"assignment"', "CS + assignment")
# Zendesk vendor/marketing mail
scan("from:(zendesk.com OR support.zendesk.com OR btoecventures.zendesk.com)", "Zendesk vendor")
