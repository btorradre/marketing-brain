"""Campaign operations — create and list campaigns via Meta Marketing API."""

from facebook_business.adobjects.campaign import Campaign
from facebook_business.exceptions import FacebookRequestError

from meta_ads.api.client import MetaAdsClient
from meta_ads.utils.errors import handle_api_error, format_validation_error
from meta_ads.utils.logger import setup_logger

logger = setup_logger()

# Valid objectives for the current API version.
# Meta consolidated objectives — these are the main ones for v21.0+
VALID_OBJECTIVES = [
    "OUTCOME_AWARENESS",
    "OUTCOME_ENGAGEMENT",
    "OUTCOME_LEADS",
    "OUTCOME_SALES",
    "OUTCOME_TRAFFIC",
    "OUTCOME_APP_PROMOTION",
]

VALID_STATUSES = ["PAUSED", "ACTIVE"]

# Buying types determine auction vs fixed pricing
VALID_BUYING_TYPES = ["AUCTION", "RESERVED"]


def validate_campaign_params(params: dict) -> list[str]:
    """Validate campaign parameters before sending to API. Returns list of errors."""
    errors = []

    if not params.get("name"):
        errors.append(format_validation_error("name", "Campaign name is required"))

    objective = params.get("objective", "").upper()
    if objective and objective not in VALID_OBJECTIVES:
        errors.append(
            format_validation_error(
                "objective",
                f"Must be one of: {', '.join(VALID_OBJECTIVES)}",
            )
        )

    status = params.get("status", "PAUSED").upper()
    if status not in VALID_STATUSES:
        errors.append(
            format_validation_error("status", f"Must be one of: {', '.join(VALID_STATUSES)}")
        )

    # Budget validation — daily or lifetime, in cents
    daily = params.get("daily_budget")
    lifetime = params.get("lifetime_budget")
    if daily and lifetime:
        errors.append(
            format_validation_error("budget", "Set either daily_budget or lifetime_budget, not both")
        )
    for field_name, val in [("daily_budget", daily), ("lifetime_budget", lifetime)]:
        if val is not None:
            try:
                cents = int(val)
                if cents < 100:
                    errors.append(
                        format_validation_error(field_name, "Minimum budget is 100 (= $1.00)")
                    )
            except (ValueError, TypeError):
                errors.append(
                    format_validation_error(field_name, "Must be an integer (cents)")
                )

    return errors


def create_campaign(client: MetaAdsClient, params: dict) -> dict:
    """Create a new campaign.

    Required params:
        name (str): Campaign name
        objective (str): One of VALID_OBJECTIVES
    Optional params:
        status (str): PAUSED (default) or ACTIVE
        daily_budget (int): Daily budget in cents
        lifetime_budget (int): Lifetime budget in cents
        buying_type (str): AUCTION (default) or RESERVED
        special_ad_categories (list): e.g. ["HOUSING", "CREDIT", "EMPLOYMENT"]

    Returns dict with campaign id and name on success.
    """
    errors = validate_campaign_params(params)
    if errors:
        return {"success": False, "errors": errors}

    try:
        campaign_params = {
            Campaign.Field.name: params["name"],
            Campaign.Field.objective: params.get("objective", "OUTCOME_TRAFFIC").upper(),
            Campaign.Field.status: params.get("status", "PAUSED").upper(),
            Campaign.Field.buying_type: params.get("buying_type", "AUCTION").upper(),
        }

        # Special ad categories are required by Meta — default to empty list
        campaign_params[Campaign.Field.special_ad_categories] = params.get(
            "special_ad_categories", []
        )

        # Budget goes on campaign for CBO (Campaign Budget Optimization)
        if params.get("daily_budget"):
            campaign_params[Campaign.Field.daily_budget] = int(params["daily_budget"])
        if params.get("lifetime_budget"):
            campaign_params[Campaign.Field.lifetime_budget] = int(params["lifetime_budget"])

        account = client.get_account()
        campaign = account.create_campaign(params=campaign_params)

        result = {
            "success": True,
            "id": campaign["id"],
            "name": params["name"],
        }
        logger.info("Campaign created: %s (ID: %s)", result["name"], result["id"])
        return result

    except FacebookRequestError as e:
        msg = handle_api_error(e)
        logger.error("Failed to create campaign: %s", msg)
        return {"success": False, "errors": [msg]}


def list_campaigns(client: MetaAdsClient, limit: int = 25, status_filter: str = None) -> list[dict]:
    """List campaigns with pagination support.

    Args:
        limit: Max campaigns to return (handles pagination internally)
        status_filter: Optional filter — ACTIVE, PAUSED, ARCHIVED

    Returns list of campaign dicts.
    """
    try:
        account = client.get_account()
        fields = [
            Campaign.Field.id,
            Campaign.Field.name,
            Campaign.Field.objective,
            Campaign.Field.status,
            Campaign.Field.daily_budget,
            Campaign.Field.lifetime_budget,
            Campaign.Field.created_time,
        ]

        params = {}
        if status_filter:
            # effective_status filter accepts a list
            params["filtering"] = [
                {"field": "effective_status", "operator": "IN", "value": [status_filter.upper()]}
            ]

        # The SDK returns a Cursor that handles pagination automatically
        campaigns_cursor = account.get_campaigns(fields=fields, params=params)

        results = []
        for campaign in campaigns_cursor:
            results.append({
                "id": campaign["id"],
                "name": campaign["name"],
                "objective": campaign.get("objective", "N/A"),
                "status": campaign["status"],
                "daily_budget": campaign.get("daily_budget"),
                "lifetime_budget": campaign.get("lifetime_budget"),
                "created": campaign.get("created_time", "N/A"),
            })
            if len(results) >= limit:
                break

        logger.info("Listed %d campaigns", len(results))
        return results

    except FacebookRequestError as e:
        msg = handle_api_error(e)
        logger.error("Failed to list campaigns: %s", msg)
        return []
