"""Gmail (3 accounts) + Google Calendar.

Tokens live in launchpad/auth/gmail_<key>.json with gmail.readonly +
calendar.readonly scopes. Run gmail_auth.py once per account to create them.
Accounts without a token report status "needs_auth" instead of failing the
whole dashboard.
"""
import os
from datetime import datetime, timedelta
from .common import AUTH_DIR, VAULT, today_start

OAUTH_DIR = os.path.join(VAULT, "_engine", "oauth credentials")
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/calendar.readonly",
]

ACCOUNTS = [
    {"key": "gmail",    "email": "btorradre@gmail.com",
     "client_secret": os.path.join(OAUTH_DIR, "btorradre@gmail.json")},
    {"key": "btoec",    "email": "btorradre@btoecventures.com",
     "client_secret": os.path.join(OAUTH_DIR, "btorradre@btoecventures.json")},
    {"key": "orelli",   "email": "brooks@orelli.com",
     "client_secret": os.path.join(OAUTH_DIR, "client_secret_932297894555-cq6cn2b6t9ks39sjedh3rstifbbf9ar6.apps.googleusercontent.com.json")},
]


def token_path(key):
    return os.path.join(AUTH_DIR, f"gmail_{key}.json")


def _creds(acct):
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    tp = token_path(acct["key"])
    if not os.path.exists(tp):
        return None
    creds = Credentials.from_authorized_user_file(tp, SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        open(tp, "w").write(creds.to_json())
    return creds


def _header(headers, name):
    for h in headers:
        if h["name"].lower() == name.lower():
            return h["value"]
    return ""


def _emails(service):
    resp = service.users().messages().list(
        userId="me", q="in:inbox newer_than:2d", maxResults=25).execute()
    ids = [m["id"] for m in resp.get("messages", [])]
    out = []
    for mid in ids:
        m = service.users().messages().get(
            userId="me", id=mid, format="metadata",
            metadataHeaders=["From", "Subject", "Date"]).execute()
        labels = m.get("labelIds", [])
        hdrs = (m.get("payload") or {}).get("headers", [])
        out.append({
            "from": _header(hdrs, "From"),
            "subject": _header(hdrs, "Subject") or "(no subject)",
            "snippet": (m.get("snippet") or "")[:140],
            "ts": int(m.get("internalDate", 0)),
            "unread": "UNREAD" in labels,
            "important": "IMPORTANT" in labels,
            "primary": "CATEGORY_PERSONAL" in labels or not any(
                l.startswith("CATEGORY_") for l in labels),
        })
    # important+unread first, then unread, then recency
    out.sort(key=lambda e: (-(e["important"] and e["unread"]), -e["unread"], -e["ts"]))
    return out


def _unread_count(service):
    lbl = service.users().labels().get(userId="me", id="INBOX").execute()
    return lbl.get("messagesUnread", 0)


def _calendar_today(service):
    start = today_start()
    end = start + timedelta(days=1)
    resp = service.events().list(
        calendarId="primary",
        timeMin=start.isoformat(), timeMax=end.isoformat(),
        singleEvents=True, orderBy="startTime", maxResults=15).execute()
    events = []
    for ev in resp.get("items", []):
        st = ev.get("start", {})
        events.append({
            "summary": ev.get("summary", "(untitled)"),
            "start": st.get("dateTime") or st.get("date"),
            "all_day": "date" in st,
        })
    return events


def collect():
    try:
        from googleapiclient.discovery import build
    except ImportError:
        return {"accounts": [], "error": "google-api-python-client not installed"}

    accounts = []
    calendar = []
    for acct in ACCOUNTS:
        entry = {"key": acct["key"], "email": acct["email"]}
        try:
            creds = _creds(acct)
            if creds is None:
                entry["status"] = "needs_auth"
                accounts.append(entry)
                continue
            gmail = build("gmail", "v1", credentials=creds, cache_discovery=False)
            entry["status"] = "ok"
            entry["unread"] = _unread_count(gmail)
            entry["emails"] = _emails(gmail)
            try:
                cal = build("calendar", "v3", credentials=creds, cache_discovery=False)
                for ev in _calendar_today(cal):
                    ev["account"] = acct["email"]
                    calendar.append(ev)
            except Exception:
                pass
        except Exception as e:
            entry["status"] = "error"
            entry["error"] = str(e)[:200]
        accounts.append(entry)

    calendar.sort(key=lambda e: (not e["all_day"], e["start"] or ""))
    return {"accounts": accounts, "calendar_today": calendar}
