"""Meta ad spend (Motilli ad account) — today + week-to-date.

Velantra's Meta assets were banned 7/27; this token/account is the Motilli
side. Fails gracefully if the token has expired.
"""
import urllib.parse
from .common import env, http_json, week_start, today_start


def _insights(token, acct, since, until):
    params = {
        "access_token": token,
        "fields": "spend,impressions,clicks",
        "time_range": f'{{"since":"{since}","until":"{until}"}}',
        "level": "account",
    }
    url = f"https://graph.facebook.com/v21.0/{acct}/insights?" + urllib.parse.urlencode(params)
    data, _ = http_json(url)
    rows = data.get("data", [])
    if not rows:
        return {"spend": 0.0, "impressions": 0, "clicks": 0}
    r = rows[0]
    return {"spend": float(r.get("spend", 0)),
            "impressions": int(r.get("impressions", 0)),
            "clicks": int(r.get("clicks", 0))}


def collect():
    token = env("META_ACCESS_TOKEN")
    acct = env("META_AD_ACCOUNT_ID")
    if not token or not acct:
        return {"error": "META_ACCESS_TOKEN / META_AD_ACCOUNT_ID not set"}
    if not acct.startswith("act_"):
        acct = f"act_{acct}"
    today = today_start().strftime("%Y-%m-%d")
    wk = week_start().strftime("%Y-%m-%d")
    return {
        "account": acct,
        "today": _insights(token, acct, today, today),
        "week": _insights(token, acct, wk, today),
        "week_start": wk,
    }
