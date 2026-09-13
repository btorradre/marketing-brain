"""Error handling — translates Meta API errors into actionable CLI messages."""

from facebook_business.exceptions import FacebookRequestError


def handle_api_error(error: FacebookRequestError) -> str:
    """Parse a Meta API error and return a human-readable message.

    Common error codes:
      1   - Unknown error (transient, retry)
      2   - Service temporarily unavailable
      4   - Rate limit hit
      10   - Permission denied
      17   - Rate limit (account level)
      100  - Invalid parameter
      190  - Invalid/expired access token
      200  - Permission error
      2635 - Ad account doesn't exist or no access
    """
    code = error.api_error_code()
    subcode = error.api_error_subcode()
    message = error.api_error_message()

    # Try to get the full body for more detail
    try:
        body = error.body()
        if isinstance(body, dict):
            err_obj = body.get("error", {})
            detail = err_obj.get("error_user_msg") or err_obj.get("message") or message
        else:
            detail = message
    except Exception:
        detail = message

    error_map = {
        4: "Rate limit reached. Wait a few minutes before retrying.",
        17: "Account-level rate limit. Wait 5-10 minutes.",
        10: f"Permission denied. Check your app permissions. Detail: {detail}",
        100: f"Invalid parameter: {detail}",
        190: "Access token is invalid or expired. Generate a new long-lived token.",
        200: f"Insufficient permissions: {detail}",
        2635: "Ad account not found or no access. Check META_AD_ACCOUNT_ID in .env",
    }

    if code in error_map:
        return f"[Error {code}] {error_map[code]}"

    return f"[Error {code}/{subcode}] {detail}"


def format_validation_error(field: str, reason: str) -> str:
    """Format a local validation error before it hits the API."""
    return f"Validation error on '{field}': {reason}"
