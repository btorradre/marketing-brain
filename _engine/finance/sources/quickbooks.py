"""QuickBooks Online: actual operating expenses, to replace the static estimates.

Talks to the QBO REST API directly using the same credentials the MCP server at
~/.claude/mcp-servers/quickbooks-online-mcp-server/.env holds. The MCP server is
for interactive use; a cron job cannot go through it, so the refresh-token grant
is done here.

Until the OAuth handshake is completed (refresh token empty) every function
returns `available: False` and the pipeline falls back to costs.json estimates.
That is the designed behaviour, not an error: the dashboard shows which source
each fixed-cost figure came from.
"""
import base64
import os
import sys
import urllib.parse
from collections import defaultdict

sys.path.insert(0, __file__.rsplit("/sources/", 1)[0])
from common import http_json, money  # noqa: E402

QBO_ENV_PATH = os.path.expanduser(
    "~/.claude/mcp-servers/quickbooks-online-mcp-server/.env")

BASE = {
    "sandbox": "https://sandbox-quickbooks.api.intuit.com",
    "production": "https://quickbooks.api.intuit.com",
}

# QuickBooks expense accounts that are fixed overhead, not variable cost.
# Anything matching these is amortized below CM3 into Net.
FIXED_COST_HINTS = (
    "payroll", "salar", "wage", "software", "subscription", "saas", "rent",
    "insurance", "legal", "account", "professional", "contractor", "office",
)


def _qbo_env():
    cfg = {}
    if os.path.exists(QBO_ENV_PATH):
        for line in open(QBO_ENV_PATH):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                cfg[k.strip()] = v.strip()
    return cfg


def is_configured():
    c = _qbo_env()
    return bool(c.get("QUICKBOOKS_REFRESH_TOKEN") and c.get("QUICKBOOKS_REALM_ID"))


def _access_token(cfg):
    basic = base64.b64encode(
        f"{cfg['QUICKBOOKS_CLIENT_ID']}:{cfg['QUICKBOOKS_CLIENT_SECRET']}".encode()
    ).decode()
    data, _ = http_json(
        "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer",
        headers={"Authorization": f"Basic {basic}",
                 "Accept": "application/json"},
        form={"grant_type": "refresh_token",
              "refresh_token": cfg["QUICKBOOKS_REFRESH_TOKEN"]})
    # Intuit rotates the refresh token on every exchange; persist the new one or
    # the next nightly run fails with invalid_grant.
    new_refresh = data.get("refresh_token")
    if new_refresh and new_refresh != cfg["QUICKBOOKS_REFRESH_TOKEN"]:
        _persist_refresh(new_refresh)
    return data["access_token"]


def _persist_refresh(token):
    if not os.path.exists(QBO_ENV_PATH):
        return
    lines = open(QBO_ENV_PATH).read().splitlines()
    out = []
    for line in lines:
        if line.startswith("QUICKBOOKS_REFRESH_TOKEN="):
            out.append(f"QUICKBOOKS_REFRESH_TOKEN={token}")
        else:
            out.append(line)
    tmp = QBO_ENV_PATH + ".tmp"
    with open(tmp, "w") as f:
        f.write("\n".join(out) + "\n")
    os.replace(tmp, QBO_ENV_PATH)


def fetch_expenses(start, end):
    """Monthly expense totals by account for [start, end].

    Returns {"available": bool, "reason": str|None, "months": {"YYYY-MM": {...}}}
    """
    if not is_configured():
        return {"available": False,
                "reason": "QuickBooks OAuth not completed (no refresh token). "
                          "Run `npm run auth` in the MCP server directory.",
                "months": {}}
    cfg = _qbo_env()
    try:
        token = _access_token(cfg)
        realm = cfg["QUICKBOOKS_REALM_ID"]
        base = BASE.get(cfg.get("QUICKBOOKS_ENVIRONMENT", "sandbox"), BASE["sandbox"])
        url = (f"{base}/v3/company/{realm}/reports/ProfitAndLoss"
               f"?{urllib.parse.urlencode({'start_date': start, 'end_date': end, 'summarize_column_by': 'Month', 'minorversion': '75'})}")
        data, _ = http_json(url, headers={"Authorization": f"Bearer {token}",
                                          "Accept": "application/json"})
    except Exception as e:  # noqa: BLE001 - never fail the nightly run on QBO
        return {"available": False, "reason": f"QuickBooks call failed: {e}",
                "months": {}}

    env_name = cfg.get("QUICKBOOKS_ENVIRONMENT", "sandbox")
    months = _parse_pl(data)

    # A sandbox company holds Intuit's fabricated demo data. It is useful for
    # proving the connection works, and actively harmful if it reaches the
    # margin ladder, so it is reported but never marked available.
    if env_name != "production":
        return {"available": False,
                "reason": f"Connected to the {env_name} company, whose figures are "
                          f"Intuit demo data. Fixed costs stay on the costs.json "
                          f"estimates until QUICKBOOKS_ENVIRONMENT=production.",
                "months": {}, "environment": env_name,
                "sandbox_preview_months": sorted(months.keys())}

    return {"available": True, "reason": None, "months": months,
            "environment": env_name}


def _parse_pl(report):
    """Flatten Intuit's nested ProfitAndLoss report into {month: {account: amount}}."""
    cols = [c.get("ColTitle", "") for c in report.get("Columns", {}).get("Column", [])]
    months = defaultdict(dict)

    def walk(rows):
        for row in rows or []:
            if row.get("Rows"):
                walk(row["Rows"].get("Row"))
            data = row.get("ColData")
            if not data:
                continue
            label = data[0].get("value", "").strip()
            if not label:
                continue
            for i, cell in enumerate(data[1:], start=1):
                if i >= len(cols):
                    break
                title = cols[i]
                val = cell.get("value", "")
                if not val:
                    continue
                try:
                    amt = float(val)
                except ValueError:
                    continue
                if amt:
                    months[title][label] = money(amt)

    walk(report.get("Rows", {}).get("Row"))
    return dict(months)


def classify_fixed(account_name):
    low = (account_name or "").lower()
    return any(h in low for h in FIXED_COST_HINTS)
