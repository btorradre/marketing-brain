"""Token management — exchange, check, and persist Meta API access tokens."""

import os
import re
import requests
from datetime import datetime, timezone
from meta_ads.utils.logger import setup_logger

logger = setup_logger()

GRAPH_BASE = "https://graph.facebook.com"


def exchange_token(app_id: str, app_secret: str, short_token: str, api_version: str = "v21.0") -> dict:
    """Exchange a short-lived token for a long-lived one (~60 days).

    Returns: { "access_token": "...", "expires_in": 5184000, "token_type": "bearer" }
    Raises on failure.
    """
    url = f"{GRAPH_BASE}/{api_version}/oauth/access_token"
    params = {
        "grant_type": "fb_exchange_token",
        "client_id": app_id,
        "client_secret": app_secret,
        "fb_exchange_token": short_token,
    }

    resp = requests.get(url, params=params, timeout=15)
    data = resp.json()

    if "error" in data:
        err = data["error"]
        msg = err.get("message", "Unknown error")
        raise RuntimeError(f"Token exchange failed: {msg}")

    if "access_token" not in data:
        raise RuntimeError("Token exchange returned no access_token")

    logger.info(
        "Token exchanged successfully — expires in %d seconds (~%d days)",
        data.get("expires_in", 0),
        data.get("expires_in", 0) // 86400,
    )
    return data


def check_token(access_token: str, app_id: str = None, app_secret: str = None, api_version: str = "v21.0") -> dict:
    """Check the validity and expiry of an access token.

    Returns: {
        "valid": bool,
        "expires_at": "ISO timestamp" | None,
        "expires_in_seconds": int | None,
        "expires_in_days": int | None,
        "scopes": [...],
        "app_id": "...",
        "error": "..." | None,
    }
    """
    # Try a lightweight API call first — /me with minimal fields
    url = f"{GRAPH_BASE}/{api_version}/me"
    resp = requests.get(url, params={"access_token": access_token, "fields": "id"}, timeout=10)
    data = resp.json()

    if "error" in data:
        err = data["error"]
        return {
            "valid": False,
            "expires_at": None,
            "expires_in_seconds": None,
            "expires_in_days": None,
            "scopes": [],
            "app_id": None,
            "error": err.get("message", "Token invalid"),
        }

    # Token is valid — try to get debug info for expiry
    result = {
        "valid": True,
        "expires_at": None,
        "expires_in_seconds": None,
        "expires_in_days": None,
        "scopes": [],
        "app_id": None,
        "error": None,
    }

    # Use debug_token endpoint if we have app credentials
    if app_id and app_secret:
        app_token = f"{app_id}|{app_secret}"
        debug_url = f"{GRAPH_BASE}/{api_version}/debug_token"
        debug_resp = requests.get(
            debug_url,
            params={"input_token": access_token, "access_token": app_token},
            timeout=10,
        )
        debug_data = debug_resp.json().get("data", {})

        if debug_data.get("expires_at"):
            expires_ts = debug_data["expires_at"]
            expires_dt = datetime.fromtimestamp(expires_ts, tz=timezone.utc)
            now = datetime.now(tz=timezone.utc)
            diff = expires_dt - now
            result["expires_at"] = expires_dt.isoformat()
            result["expires_in_seconds"] = max(0, int(diff.total_seconds()))
            result["expires_in_days"] = max(0, diff.days)

        result["scopes"] = debug_data.get("scopes", [])
        result["app_id"] = debug_data.get("app_id")

    return result


def get_oauth_url(app_id: str, redirect_uri: str, api_version: str = "v21.0", state: str = "") -> str:
    """Build the Facebook OAuth authorization URL.

    The state parameter encodes the user_id + CSRF nonce so the callback
    can identify which user initiated the flow.
    """
    scopes = "ads_management,ads_read,pages_show_list,pages_read_engagement"
    url = (
        f"https://www.facebook.com/{api_version}/dialog/oauth"
        f"?client_id={app_id}"
        f"&redirect_uri={redirect_uri}"
        f"&scope={scopes}"
        f"&response_type=code"
    )
    if state:
        url += f"&state={state}"
    return url


def fetch_ad_accounts(access_token: str, api_version: str = "v21.0") -> list[dict]:
    """Fetch the ad accounts accessible to the given access token.

    Returns: [{"id": "act_123", "name": "My Account"}, ...]
    """
    url = f"{GRAPH_BASE}/{api_version}/me/adaccounts"
    resp = requests.get(url, params={
        "access_token": access_token,
        "fields": "id,name,account_id",
    }, timeout=15)
    data = resp.json()

    if "error" in data:
        raise RuntimeError(data["error"].get("message", "Failed to fetch ad accounts"))

    results = []
    for acct in data.get("data", []):
        acct_id = acct.get("id") or f"act_{acct.get('account_id', '')}"
        results.append({
            "id": acct_id,
            "name": acct.get("name", acct_id),
        })
    return results


def exchange_code_for_token(app_id: str, app_secret: str, code: str, redirect_uri: str, api_version: str = "v21.0") -> dict:
    """Exchange an OAuth authorization code for an access token.

    Returns: { "access_token": "...", "token_type": "bearer" }
    Raises on failure.
    """
    url = f"{GRAPH_BASE}/{api_version}/oauth/access_token"
    params = {
        "client_id": app_id,
        "client_secret": app_secret,
        "redirect_uri": redirect_uri,
        "code": code,
    }

    resp = requests.get(url, params=params, timeout=15)
    data = resp.json()

    if "error" in data:
        err = data["error"]
        msg = err.get("message", "Unknown error")
        raise RuntimeError(f"Code exchange failed: {msg}")

    if "access_token" not in data:
        raise RuntimeError("Code exchange returned no access_token")

    logger.info("Authorization code exchanged for short-lived token")
    return data


def update_env_token(env_path: str, new_token: str) -> None:
    """Update META_ACCESS_TOKEN in the .env file, preserving all other values."""
    if not os.path.exists(env_path):
        raise FileNotFoundError(f".env file not found: {env_path}")

    with open(env_path, "r") as f:
        content = f.read()

    # Replace the token line
    new_content = re.sub(
        r"^META_ACCESS_TOKEN=.*$",
        f"META_ACCESS_TOKEN={new_token}",
        content,
        flags=re.MULTILINE,
    )

    with open(env_path, "w") as f:
        f.write(new_content)

    logger.info("Updated META_ACCESS_TOKEN in %s", env_path)


def update_token_supabase(new_token: str) -> None:
    """Upsert META_ACCESS_TOKEN in the Supabase 'settings' table.

    Requires SUPABASE_URL and SUPABASE_SERVICE_KEY env vars.
    """
    url = os.environ.get("SUPABASE_URL", "")
    key = os.environ.get("SUPABASE_SERVICE_KEY", "")

    if not url or not key:
        logger.warning("Supabase env vars not set — skipping Supabase token update")
        return

    from supabase import create_client
    sb = create_client(url, key)

    sb.table("settings").upsert(
        {"key": "META_ACCESS_TOKEN", "value": new_token},
        on_conflict="key",
    ).execute()

    logger.info("Updated META_ACCESS_TOKEN in Supabase settings table")


def load_token_from_supabase() -> str | None:
    """Load META_ACCESS_TOKEN from Supabase settings table.

    Returns the token string or None if not found / not configured.
    """
    url = os.environ.get("SUPABASE_URL", "")
    key = os.environ.get("SUPABASE_SERVICE_KEY", "")

    if not url or not key:
        return None

    try:
        from supabase import create_client
        sb = create_client(url, key)
        result = sb.table("settings").select("value").eq("key", "META_ACCESS_TOKEN").single().execute()
        token = result.data.get("value") if result.data else None
        if token:
            logger.info("Loaded META_ACCESS_TOKEN from Supabase")
        return token
    except Exception as e:
        logger.warning("Failed to load token from Supabase: %s", e)
        return None
