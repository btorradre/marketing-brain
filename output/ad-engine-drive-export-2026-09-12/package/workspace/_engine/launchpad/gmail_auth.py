#!/usr/bin/env python3
"""One-time Gmail + Calendar OAuth for the launchpad dashboard.

Run from a terminal (it opens your browser once per account):

    cd "~/Documents/marketing brain/_engine/launchpad"
    SSL_CERT_FILE=$(python3 -m certifi) python3 gmail_auth.py

For each account, sign in with the matching Google identity and approve
read-only Gmail + Calendar access. Tokens are saved to auth/gmail_<key>.json
and refresh automatically after that — you should never need this again
unless a token is revoked.

    python3 gmail_auth.py gmail     # just one account (gmail | btoec | orelli)
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from collectors.gmail_cal import ACCOUNTS, SCOPES, token_path

try:
    import certifi
    os.environ.setdefault("SSL_CERT_FILE", certifi.where())
except ImportError:
    pass


def auth(acct):
    from google_auth_oauthlib.flow import InstalledAppFlow
    tp = token_path(acct["key"])
    if os.path.exists(tp):
        print(f"[{acct['key']}] token already exists at {tp} — delete it to re-auth. Skipping.")
        return
    if not os.path.exists(acct["client_secret"]):
        print(f"[{acct['key']}] MISSING client secret: {acct['client_secret']}")
        return
    print(f"\n=== {acct['email']} ===")
    print(f"Sign in as {acct['email']} in the browser window that opens.")
    flow = InstalledAppFlow.from_client_secrets_file(acct["client_secret"], SCOPES)
    creds = flow.run_local_server(
        port=0, open_browser=True,
        authorization_prompt_message="If the browser didn't open, visit:\n{url}\n")
    os.makedirs(os.path.dirname(tp), exist_ok=True)
    open(tp, "w").write(creds.to_json())
    print(f"[{acct['key']}] saved {tp}")


if __name__ == "__main__":
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for acct in ACCOUNTS:
        if only and acct["key"] != only:
            continue
        try:
            auth(acct)
        except Exception as e:
            print(f"[{acct['key']}] FAILED: {e}")
    print("\nDone. Refresh the dashboard — email panels will light up.")
