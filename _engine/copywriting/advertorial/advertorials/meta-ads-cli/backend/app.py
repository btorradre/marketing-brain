"""Flask API backend — multi-tenant Meta Marketing API for the frontend UI."""

import os
import sys
import json
import base64
import secrets
import tempfile
from datetime import datetime, timedelta, timezone
from flask import Flask, request, jsonify, g
from flask_cors import CORS
from dotenv import load_dotenv

# Add parent dir to path so we can import meta_ads modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from meta_ads.api.client import MetaAdsClient
from meta_ads.api.campaigns import create_campaign, list_campaigns
from meta_ads.api.adsets import create_adset, update_adset, list_adsets
from meta_ads.api.ads import create_ad, list_ads, _upload_image, _upload_video
from meta_ads.api.pixels import list_pixels
from meta_ads.api.pages import list_pages
from meta_ads.api.token import (
    exchange_token, check_token, get_oauth_url,
    exchange_code_for_token, fetch_ad_accounts,
)
from meta_ads.utils.encryption import encrypt, decrypt
from meta_ads.bulk import execute_bulk
from backend.auth import require_auth

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024 * 1024  # 1 GB max upload
CORS(app)

# Load config from parent .env (only if file exists — skipped on Vercel)
_env_file = os.path.join(os.path.dirname(__file__), "..", ".env")
if os.path.exists(_env_file):
    load_dotenv(_env_file)


# ── Supabase helper ──

_supabase_client = None


def get_supabase():
    """Cached Supabase client (module-level singleton — fine for serverless)."""
    global _supabase_client
    if _supabase_client is None:
        from supabase import create_client
        _supabase_client = create_client(
            os.environ["SUPABASE_URL"].strip(),
            os.environ["SUPABASE_SERVICE_KEY"].strip(),
        )
    return _supabase_client


def _get_data(result):
    """Safely extract .data from a Supabase query result (maybe_single can return None)."""
    if result is None:
        return None
    return result.data


# ── Per-request client helper ──

def get_user_client() -> MetaAdsClient:
    """Build a MetaAdsClient for the authenticated user.

    Reads the user's encrypted token and selected ad account from Supabase,
    decrypts the token, and constructs a per-request SDK instance.
    """
    user_id = g.user_id
    sb = get_supabase()

    # Get user's Meta token
    token_row = sb.table("user_meta_tokens") \
        .select("access_token, token_expires_at") \
        .eq("user_id", user_id) \
        .maybe_single() \
        .execute()

    token_data = _get_data(token_row)
    if not token_data:
        raise ValueError("No Meta account connected. Please connect via Settings.")

    # Get user's selected ad account
    account_row = sb.table("user_ad_accounts") \
        .select("meta_account_id") \
        .eq("user_id", user_id) \
        .eq("is_selected", True) \
        .maybe_single() \
        .execute()

    account_data = _get_data(account_row)
    if not account_data:
        raise ValueError("No ad account selected. Please select one in Settings.")

    access_token = decrypt(token_data["access_token"])
    ad_account_id = account_data["meta_account_id"]
    api_version = os.getenv("META_API_VERSION", "v21.0")

    return MetaAdsClient(access_token, ad_account_id, api_version)


def _get_redirect_uri():
    """Return the OAuth redirect URI — uses APP_URL in production, localhost in dev."""
    base = os.environ.get("APP_URL", "http://localhost:5001")
    return f"{base}/api/token/oauth-callback"


# ── Error handler ──

@app.errorhandler(500)
def handle_500(e):
    return jsonify({"error": f"Internal server error: {e}"}), 500


# ── Health check ──

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})



# ── Token Management (multi-user) ──

@app.route("/api/token/status", methods=["GET"])
@require_auth
def api_token_status():
    """Check current user's Meta token validity and expiry."""
    try:
        sb = get_supabase()
        token_row = sb.table("user_meta_tokens") \
            .select("access_token, token_expires_at") \
            .eq("user_id", g.user_id) \
            .maybe_single() \
            .execute()

        token_data = _get_data(token_row)
        if not token_data:
            return jsonify({"valid": False, "error": "No Meta account connected", "connected": False})

        access_token = decrypt(token_data["access_token"])
        app_id = os.getenv("META_APP_ID", "")
        app_secret = os.getenv("META_APP_SECRET", "")
        api_version = os.getenv("META_API_VERSION", "v21.0")

        result = check_token(access_token, app_id=app_id, app_secret=app_secret, api_version=api_version)
        result["connected"] = True
        return jsonify(result)
    except Exception as e:
        logger.error("token_status error: %s", e)
        return jsonify({"error": str(e)}), 500


@app.route("/api/token/exchange", methods=["POST"])
@require_auth
def api_token_exchange():
    """Manually exchange a short-lived token for a 60-day token (per-user)."""
    data = request.get_json()
    short_token = data.get("short_token", "").strip()
    if not short_token:
        return jsonify({"success": False, "errors": ["No token provided"]}), 400

    app_id = os.getenv("META_APP_ID", "")
    app_secret = os.getenv("META_APP_SECRET", "")
    api_version = os.getenv("META_API_VERSION", "v21.0")

    if not app_id or not app_secret:
        return jsonify({"success": False, "errors": ["META_APP_ID and META_APP_SECRET must be set"]}), 500

    try:
        result = exchange_token(app_id, app_secret, short_token, api_version)
        new_token = result["access_token"]
        expires_in = result.get("expires_in", 0)
        days = expires_in // 86400

        # Encrypt and store for this user
        encrypted_token = encrypt(new_token)
        expires_at = (datetime.now(timezone.utc) + timedelta(seconds=expires_in)).isoformat()

        sb = get_supabase()
        sb.table("user_meta_tokens").upsert({
            "user_id": g.user_id,
            "access_token": encrypted_token,
            "token_expires_at": expires_at,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }, on_conflict="user_id").execute()

        # Also discover ad accounts
        try:
            ad_accounts = fetch_ad_accounts(new_token, api_version)
            for acct in ad_accounts:
                sb.table("user_ad_accounts").upsert({
                    "user_id": g.user_id,
                    "meta_account_id": acct["id"],
                    "meta_account_name": acct["name"],
                }, on_conflict="user_id,meta_account_id").execute()

            # Auto-select first if none selected
            existing = sb.table("user_ad_accounts") \
                .select("id") \
                .eq("user_id", g.user_id) \
                .eq("is_selected", True) \
                .maybe_single() \
                .execute()
            if not _get_data(existing) and ad_accounts:
                sb.table("user_ad_accounts") \
                    .update({"is_selected": True}) \
                    .eq("user_id", g.user_id) \
                    .eq("meta_account_id", ad_accounts[0]["id"]) \
                    .execute()
        except Exception:
            pass

        return jsonify({
            "success": True,
            "message": f"Token exchanged! Valid for ~{days} days.",
            "expires_in_days": days,
        })

    except Exception as e:
        return jsonify({"success": False, "errors": [str(e)]}), 400


@app.route("/api/token/oauth-url", methods=["GET"])
@require_auth
def api_oauth_url():
    """Return the Facebook OAuth authorization URL with user-specific state."""
    app_id = os.getenv("META_APP_ID", "")
    api_version = os.getenv("META_API_VERSION", "v21.0")

    if not app_id:
        return jsonify({"success": False, "errors": ["META_APP_ID not set"]}), 400

    # Generate CSRF nonce and encode user_id in state parameter
    nonce = secrets.token_hex(16)
    state_data = json.dumps({"user_id": g.user_id, "nonce": nonce})
    state = base64.urlsafe_b64encode(state_data.encode()).decode()

    # Store nonce in Supabase for validation on callback
    sb = get_supabase()
    sb.table("oauth_states").upsert(
        {"nonce": nonce, "user_id": g.user_id, "created_at": datetime.now(timezone.utc).isoformat()},
        on_conflict="nonce",
    ).execute()

    redirect_uri = _get_redirect_uri()
    url = get_oauth_url(app_id, redirect_uri, api_version, state=state)
    return jsonify({"url": url})


@app.route("/api/token/oauth-callback", methods=["GET"])
def api_oauth_callback():
    """Handle Facebook OAuth callback — exchange code for long-lived token (multi-user)."""
    code = request.args.get("code")
    state = request.args.get("state")
    error = request.args.get("error")

    if error:
        error_desc = request.args.get("error_description", "Authorization denied")
        return f"""
        <html><body style="background:#0a0a0f;color:#f0f0f5;font-family:sans-serif;display:flex;align-items:center;justify-content:center;height:100vh;margin:0">
        <div style="text-align:center">
            <h2 style="color:#ef4444">Authorization Failed</h2>
            <p>{error_desc}</p>
            <p style="color:#888;font-size:14px;margin-top:16px">You can close this window.</p>
            <script>setTimeout(()=>window.close(),3000)</script>
        </div></body></html>
        """, 400

    if not code or not state:
        return "Missing authorization code or state", 400

    # Decode state parameter to get user_id and nonce
    try:
        state_data = json.loads(base64.urlsafe_b64decode(state))
        user_id = state_data["user_id"]
        nonce = state_data["nonce"]
    except Exception:
        return "Invalid state parameter", 400

    # Validate nonce against database
    sb = get_supabase()
    state_row = sb.table("oauth_states").select("user_id").eq("nonce", nonce).maybe_single().execute()
    state_data = _get_data(state_row)
    if not state_data or state_data["user_id"] != user_id:
        return "Invalid or expired state parameter", 400

    # Delete used nonce
    sb.table("oauth_states").delete().eq("nonce", nonce).execute()

    app_id = os.getenv("META_APP_ID", "")
    app_secret = os.getenv("META_APP_SECRET", "")
    api_version = os.getenv("META_API_VERSION", "v21.0")
    redirect_uri = _get_redirect_uri()

    try:
        # Step 1: Exchange code for short-lived token
        short_result = exchange_code_for_token(app_id, app_secret, code, redirect_uri, api_version)
        short_token = short_result["access_token"]

        # Step 2: Exchange short-lived for long-lived token
        long_result = exchange_token(app_id, app_secret, short_token, api_version)
        new_token = long_result["access_token"]
        expires_in = long_result.get("expires_in", 0)
        days = expires_in // 86400

        # Step 3: Encrypt and store token for this user
        encrypted_token = encrypt(new_token)
        expires_at = (datetime.now(timezone.utc) + timedelta(seconds=expires_in)).isoformat()

        sb.table("user_meta_tokens").upsert({
            "user_id": user_id,
            "access_token": encrypted_token,
            "token_expires_at": expires_at,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }, on_conflict="user_id").execute()

        # Step 4: Fetch user's ad accounts and store them
        try:
            ad_accounts = fetch_ad_accounts(new_token, api_version)
            for acct in ad_accounts:
                sb.table("user_ad_accounts").upsert({
                    "user_id": user_id,
                    "meta_account_id": acct["id"],
                    "meta_account_name": acct["name"],
                }, on_conflict="user_id,meta_account_id").execute()

            # Auto-select first account if none selected
            existing = sb.table("user_ad_accounts") \
                .select("id") \
                .eq("user_id", user_id) \
                .eq("is_selected", True) \
                .maybe_single() \
                .execute()
            if not _get_data(existing) and ad_accounts:
                sb.table("user_ad_accounts") \
                    .update({"is_selected": True}) \
                    .eq("user_id", user_id) \
                    .eq("meta_account_id", ad_accounts[0]["id"]) \
                    .execute()
        except Exception:
            pass  # Ad account discovery is best-effort

        return f"""
        <html><body style="background:#0a0a0f;color:#f0f0f5;font-family:sans-serif;display:flex;align-items:center;justify-content:center;height:100vh;margin:0">
        <div style="text-align:center">
            <h2 style="color:#22c55e">Connected Successfully!</h2>
            <p>Token valid for ~{days} days</p>
            <p style="color:#888;font-size:14px;margin-top:16px">This window will close automatically...</p>
            <script>
                if(window.opener){{window.opener.postMessage({{type:'META_TOKEN_REFRESHED',days:{days}}},'*')}}
                setTimeout(()=>window.close(),2000)
            </script>
        </div></body></html>
        """

    except Exception as e:
        return f"""
        <html><body style="background:#0a0a0f;color:#f0f0f5;font-family:sans-serif;display:flex;align-items:center;justify-content:center;height:100vh;margin:0">
        <div style="text-align:center">
            <h2 style="color:#ef4444">Token Exchange Failed</h2>
            <p>{str(e)}</p>
            <p style="color:#888;font-size:14px;margin-top:16px">You can close this window.</p>
            <script>setTimeout(()=>window.close(),5000)</script>
        </div></body></html>
        """, 500


# ── Ad Accounts ──

@app.route("/api/accounts", methods=["GET"])
@require_auth
def api_list_accounts():
    """List the authenticated user's connected Meta ad accounts."""
    sb = get_supabase()
    result = sb.table("user_ad_accounts") \
        .select("*") \
        .eq("user_id", g.user_id) \
        .execute()
    return jsonify({"accounts": result.data or []})


@app.route("/api/accounts/select", methods=["POST"])
@require_auth
def api_select_account():
    """Select an ad account as the active one for this user."""
    data = request.get_json()
    account_id = data.get("meta_account_id")
    if not account_id:
        return jsonify({"error": "meta_account_id required"}), 400

    sb = get_supabase()
    # Deselect all
    sb.table("user_ad_accounts") \
        .update({"is_selected": False}) \
        .eq("user_id", g.user_id) \
        .execute()
    # Select the chosen one
    sb.table("user_ad_accounts") \
        .update({"is_selected": True}) \
        .eq("user_id", g.user_id) \
        .eq("meta_account_id", account_id) \
        .execute()

    return jsonify({"success": True, "selected": account_id})


# ── Campaigns ──

@app.route("/api/campaigns", methods=["GET"])
@require_auth
def api_list_campaigns():
    try:
        client = get_user_client()
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    limit = request.args.get("limit", 50, type=int)
    status = request.args.get("status")
    result = list_campaigns(client, limit=limit, status_filter=status)
    return jsonify({"campaigns": result})


@app.route("/api/campaigns", methods=["POST"])
@require_auth
def api_create_campaign():
    try:
        client = get_user_client()
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    data = request.get_json()
    result = create_campaign(client, data)
    if result.get("success"):
        return jsonify(result), 201
    return jsonify(result), 400


# ── Ad Sets ──

@app.route("/api/adsets", methods=["GET"])
@require_auth
def api_list_adsets():
    try:
        client = get_user_client()
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    campaign_id = request.args.get("campaign_id")
    limit = request.args.get("limit", 50, type=int)
    status = request.args.get("status")
    result = list_adsets(client, campaign_id=campaign_id, limit=limit, status_filter=status)
    return jsonify({"adsets": result})


@app.route("/api/adsets", methods=["POST"])
@require_auth
def api_create_adset():
    try:
        client = get_user_client()
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    data = request.get_json()
    result = create_adset(client, data)
    if result.get("success"):
        return jsonify(result), 201
    return jsonify(result), 400


@app.route("/api/adsets/<adset_id>", methods=["PATCH"])
@require_auth
def api_update_adset(adset_id):
    try:
        client = get_user_client()
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    data = request.get_json()
    result = update_adset(client, adset_id, data)
    if result.get("success"):
        return jsonify(result)
    return jsonify(result), 400


# ── Pixels & Pages ──

@app.route("/api/pixels", methods=["GET"])
@require_auth
def api_list_pixels():
    try:
        client = get_user_client()
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    limit = request.args.get("limit", 50, type=int)
    result = list_pixels(client, limit=limit)
    return jsonify({"pixels": result})


@app.route("/api/pages", methods=["GET"])
@require_auth
def api_list_pages():
    try:
        client = get_user_client()
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    limit = request.args.get("limit", 50, type=int)
    result = list_pages(client, limit=limit)
    return jsonify({"pages": result})


# ── Ads ──

@app.route("/api/ads", methods=["GET"])
@require_auth
def api_list_ads():
    try:
        client = get_user_client()
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    adset_id = request.args.get("adset_id")
    limit = request.args.get("limit", 50, type=int)
    status = request.args.get("status")
    result = list_ads(client, adset_id=adset_id, limit=limit, status_filter=status)
    return jsonify({"ads": result})


@app.route("/api/ads", methods=["POST"])
@require_auth
def api_create_ad():
    try:
        client = get_user_client()
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    data = request.get_json()
    result = create_ad(client, data)
    if result.get("success"):
        return jsonify(result), 201
    return jsonify(result), 400


@app.route("/api/adsets/<adset_id>/bulk-ads", methods=["POST"])
@require_auth
def api_bulk_create_ads(adset_id):
    """Create multiple ads under an existing ad set."""
    try:
        client = get_user_client()
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    data = request.get_json()
    ads_list = data.get("ads", [])
    if not ads_list:
        return jsonify({"success": False, "errors": ["No ads provided"]}), 400

    results = {"created": [], "errors": []}
    for i, ad_def in enumerate(ads_list):
        ad_def["adset_id"] = adset_id
        ad_result = create_ad(client, ad_def)
        if ad_result.get("success"):
            results["created"].append(ad_result)
        else:
            results["errors"].append({
                "index": i,
                "name": ad_def.get("name", f"Ad {i + 1}"),
                "errors": ad_result.get("errors", []),
            })

    status_code = 201 if results["created"] else 400
    return jsonify(results), status_code


# ── Media Upload ──

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".flv", ".webm"}


@app.route("/api/media/upload", methods=["POST"])
@require_auth
def api_upload_media():
    """Upload an image or video to the Meta ad account and return its hash/ID."""
    try:
        client = get_user_client()
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    if "file" not in request.files:
        return jsonify({"success": False, "errors": ["No file provided"]}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"success": False, "errors": ["Empty filename"]}), 400

    ext = os.path.splitext(file.filename)[1].lower()
    is_image = ext in IMAGE_EXTENSIONS
    is_video = ext in VIDEO_EXTENSIONS

    if not is_image and not is_video:
        allowed = ", ".join(sorted(IMAGE_EXTENSIONS | VIDEO_EXTENSIONS))
        return jsonify({"success": False, "errors": [f"Unsupported file type: {ext}. Allowed: {allowed}"]}), 400

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
    try:
        file.save(tmp.name)
        tmp.close()

        if is_image:
            image_hash = _upload_image(client, tmp.name)
            return jsonify({"success": True, "type": "image", "image_hash": image_hash})
        else:
            video_id = _upload_video(client, tmp.name)
            return jsonify({"success": True, "type": "video", "video_id": video_id})

    except Exception as e:
        return jsonify({"success": False, "errors": [str(e)]}), 500
    finally:
        try:
            os.unlink(tmp.name)
        except OSError:
            pass


# ── Bulk ──

@app.route("/api/bulk", methods=["POST"])
@require_auth
def api_bulk():
    """Execute bulk operations from JSON payload (not file)."""
    try:
        client = get_user_client()
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    data = request.get_json()
    if not data or "campaigns" not in data:
        return jsonify({"success": False, "errors": ["Missing 'campaigns' key in payload"]}), 400

    # Write temp file and execute
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(data, f)
        temp_path = f.name

    try:
        summary = execute_bulk(client, temp_path)
        return jsonify(summary)
    finally:
        os.unlink(temp_path)


# ── Config info (non-sensitive) ──

@app.route("/api/config", methods=["GET"])
@require_auth
def api_config():
    """Return non-sensitive config info for the authenticated user."""
    sb = get_supabase()

    # Get user's selected ad account
    account_row = sb.table("user_ad_accounts") \
        .select("meta_account_id, meta_account_name") \
        .eq("user_id", g.user_id) \
        .eq("is_selected", True) \
        .maybe_single() \
        .execute()

    # Check if user has a Meta token
    token_row = sb.table("user_meta_tokens") \
        .select("id") \
        .eq("user_id", g.user_id) \
        .maybe_single() \
        .execute()

    account_data = _get_data(account_row)
    token_data = _get_data(token_row)
    return jsonify({
        "ad_account_id": account_data["meta_account_id"] if account_data else "",
        "ad_account_name": account_data.get("meta_account_name", "") if account_data else "",
        "api_version": os.getenv("META_API_VERSION", "v21.0"),
        "connected": bool(token_data),
    })


if __name__ == "__main__":
    app.run(debug=True, port=5001)
