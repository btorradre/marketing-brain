"""Ad Set operations — create, update, and list ad sets via Meta Marketing API."""

from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.targeting import Targeting
from facebook_business.exceptions import FacebookRequestError

from meta_ads.api.client import MetaAdsClient
from meta_ads.utils.errors import handle_api_error, format_validation_error
from meta_ads.utils.logger import setup_logger

logger = setup_logger()

VALID_BID_STRATEGIES = [
    "LOWEST_COST_WITHOUT_CAP",
    "LOWEST_COST_WITH_BID_CAP",
    "COST_CAP",
    "MINIMUM_ROAS",
]

VALID_BILLING_EVENTS = [
    "IMPRESSIONS",
    "LINK_CLICKS",
    "APP_INSTALLS",
    "THRUPLAY",
]

VALID_OPTIMIZATION_GOALS = [
    "IMPRESSIONS",
    "LINK_CLICKS",
    "LANDING_PAGE_VIEWS",
    "REACH",
    "LEAD_GENERATION",
    "OFFSITE_CONVERSIONS",
    "VALUE",
    "APP_INSTALLS",
    "THRUPLAY",
    "POST_ENGAGEMENT",
    "PAGE_LIKES",
    "AD_RECALL_LIFT",
    "ENGAGED_USERS",
    "QUALITY_LEAD",
]

# Objective → valid optimization goals mapping
OBJECTIVE_GOAL_MAP = {
    "OUTCOME_TRAFFIC": ["LINK_CLICKS", "LANDING_PAGE_VIEWS", "IMPRESSIONS", "REACH"],
    "OUTCOME_AWARENESS": ["REACH", "IMPRESSIONS", "AD_RECALL_LIFT", "THRUPLAY"],
    "OUTCOME_ENGAGEMENT": ["POST_ENGAGEMENT", "IMPRESSIONS", "REACH", "THRUPLAY", "PAGE_LIKES", "ENGAGED_USERS"],
    "OUTCOME_LEADS": ["LEAD_GENERATION", "LINK_CLICKS", "LANDING_PAGE_VIEWS", "QUALITY_LEAD"],
    "OUTCOME_SALES": ["OFFSITE_CONVERSIONS", "VALUE", "LINK_CLICKS", "LANDING_PAGE_VIEWS"],
    "OUTCOME_APP_PROMOTION": ["APP_INSTALLS", "LINK_CLICKS", "OFFSITE_CONVERSIONS", "VALUE"],
}


def _build_targeting(targeting_params: dict) -> dict:
    """Build the targeting spec from user-friendly params.

    Accepts:
        geo_locations (dict): {"countries": ["US", "CA"]}
        age_min (int): Minimum age (18-65)
        age_max (int): Maximum age (18-65)
        genders (list[int]): [1] = male, [2] = female, [1,2] = all
        interests (list[dict]): [{"id": "123", "name": "Yoga"}]
        custom_audiences (list[dict]): [{"id": "12345"}]
        excluded_custom_audiences (list[dict]): [{"id": "67890"}]
        publisher_platforms (list): ["facebook", "instagram"]
        device_platforms (list): ["mobile", "desktop"]
    """
    targeting = {}

    if "geo_locations" in targeting_params:
        targeting[Targeting.Field.geo_locations] = targeting_params["geo_locations"]
    else:
        # Default to US if no geo specified
        targeting[Targeting.Field.geo_locations] = {"countries": ["US"]}

    if "age_min" in targeting_params:
        targeting[Targeting.Field.age_min] = max(18, min(65, int(targeting_params["age_min"])))
    if "age_max" in targeting_params:
        targeting[Targeting.Field.age_max] = max(18, min(65, int(targeting_params["age_max"])))
    if "genders" in targeting_params:
        targeting[Targeting.Field.genders] = targeting_params["genders"]
    if "interests" in targeting_params:
        targeting["flexible_spec"] = [{"interests": targeting_params["interests"]}]
    if "custom_audiences" in targeting_params:
        targeting[Targeting.Field.custom_audiences] = targeting_params["custom_audiences"]
    if "excluded_custom_audiences" in targeting_params:
        targeting[Targeting.Field.excluded_custom_audiences] = targeting_params[
            "excluded_custom_audiences"
        ]
    if "publisher_platforms" in targeting_params:
        targeting["publisher_platforms"] = targeting_params["publisher_platforms"]
    if "device_platforms" in targeting_params:
        targeting["device_platforms"] = targeting_params["device_platforms"]

    return targeting


def validate_adset_params(params: dict, campaign_objective: str = None) -> list[str]:
    """Validate ad set parameters before API call.

    Args:
        params: Ad set parameters dict.
        campaign_objective: Optional parent campaign objective for goal validation.
    """
    errors = []

    if not params.get("name"):
        errors.append(format_validation_error("name", "Ad set name is required"))
    if not params.get("campaign_id"):
        errors.append(format_validation_error("campaign_id", "Campaign ID is required"))

    bid_strategy = params.get("bid_strategy", "LOWEST_COST_WITHOUT_CAP").upper()
    if bid_strategy not in VALID_BID_STRATEGIES:
        errors.append(
            format_validation_error(
                "bid_strategy", f"Must be one of: {', '.join(VALID_BID_STRATEGIES)}"
            )
        )

    billing_event = params.get("billing_event", "IMPRESSIONS").upper()
    if billing_event not in VALID_BILLING_EVENTS:
        errors.append(
            format_validation_error(
                "billing_event", f"Must be one of: {', '.join(VALID_BILLING_EVENTS)}"
            )
        )

    optimization_goal = params.get("optimization_goal", "LINK_CLICKS").upper()
    if optimization_goal not in VALID_OPTIMIZATION_GOALS:
        errors.append(
            format_validation_error(
                "optimization_goal", f"Must be one of: {', '.join(VALID_OPTIMIZATION_GOALS)}"
            )
        )

    # Validate optimization goal against campaign objective
    if campaign_objective and campaign_objective in OBJECTIVE_GOAL_MAP:
        valid_goals = OBJECTIVE_GOAL_MAP[campaign_objective]
        if optimization_goal not in valid_goals:
            errors.append(
                format_validation_error(
                    "optimization_goal",
                    f"'{optimization_goal}' is not valid for {campaign_objective} campaigns. "
                    f"Valid goals: {', '.join(valid_goals)}"
                )
            )

    # Budget validation — at least one budget type required unless CBO is on the campaign
    daily = params.get("daily_budget")
    lifetime = params.get("lifetime_budget")
    if daily and lifetime:
        errors.append(
            format_validation_error("budget", "Set either daily_budget or lifetime_budget, not both")
        )

    return errors


def create_adset(client: MetaAdsClient, params: dict) -> dict:
    """Create a new ad set.

    Required params:
        name (str): Ad set name
        campaign_id (str): Parent campaign ID
    Optional params:
        daily_budget (int): Daily budget in cents
        lifetime_budget (int): Lifetime budget in cents
        bid_strategy (str): One of VALID_BID_STRATEGIES
        bid_amount (int): Bid cap in cents (required for BID_CAP strategy)
        billing_event (str): One of VALID_BILLING_EVENTS
        optimization_goal (str): One of VALID_OPTIMIZATION_GOALS
        start_time (str): ISO 8601 datetime
        end_time (str): ISO 8601 datetime (required for lifetime budget)
        status (str): PAUSED or ACTIVE
        targeting (dict): Targeting parameters (see _build_targeting)
        promoted_object (dict): e.g. {"page_id": "123"} or {"pixel_id": "456", "custom_event_type": "PURCHASE"}
    """
    errors = validate_adset_params(params)
    if errors:
        return {"success": False, "errors": errors}

    try:
        adset_params = {
            "name": params["name"],
            "campaign_id": params["campaign_id"],
            "billing_event": params.get("billing_event", "IMPRESSIONS").upper(),
            "optimization_goal": params.get("optimization_goal", "LINK_CLICKS").upper(),
            "bid_strategy": params.get("bid_strategy", "LOWEST_COST_WITHOUT_CAP").upper(),
            "status": params.get("status", "PAUSED").upper(),
        }

        # Targeting spec
        targeting_input = params.get("targeting", {})
        adset_params["targeting"] = _build_targeting(targeting_input)

        # Budget
        if params.get("daily_budget"):
            adset_params["daily_budget"] = int(params["daily_budget"])
        if params.get("lifetime_budget"):
            adset_params["lifetime_budget"] = int(params["lifetime_budget"])

        # Bid cap (only relevant for certain strategies)
        if params.get("bid_amount"):
            adset_params["bid_amount"] = int(params["bid_amount"])

        # Scheduling
        if params.get("start_time"):
            adset_params["start_time"] = params["start_time"]
        if params.get("end_time"):
            adset_params["end_time"] = params["end_time"]

        # Promoted object — required for certain objectives (e.g. conversions need a pixel)
        if params.get("promoted_object"):
            adset_params["promoted_object"] = params["promoted_object"]

        logger.info("Creating ad set with params: %s", list(adset_params.keys()))

        account = client.get_account()
        adset = account.create_ad_set(params=adset_params)

        result = {
            "success": True,
            "id": adset["id"],
            "name": params["name"],
            "campaign_id": params["campaign_id"],
        }
        logger.info("Ad set created: %s (ID: %s)", result["name"], result["id"])
        return result

    except FacebookRequestError as e:
        msg = handle_api_error(e)
        logger.error("Failed to create ad set: %s", msg)
        return {"success": False, "errors": [msg]}


def update_adset(client: MetaAdsClient, adset_id: str, updates: dict) -> dict:
    """Update an existing ad set.

    Updatable fields:
        name, status, daily_budget, lifetime_budget, bid_amount,
        bid_strategy, targeting, start_time, end_time,
        optimization_goal, billing_event
    """
    try:
        adset = AdSet(adset_id, api=client.get_api())
        update_params = {}

        # Map fields directly as string keys to avoid SDK enum issues
        simple_fields = [
            "name", "status", "daily_budget", "lifetime_budget",
            "bid_amount", "bid_strategy", "optimization_goal",
            "billing_event", "start_time", "end_time",
        ]

        for key in simple_fields:
            if key in updates:
                val = updates[key]
                if key in ("status", "bid_strategy", "optimization_goal", "billing_event"):
                    val = str(val).upper()
                if key in ("daily_budget", "lifetime_budget", "bid_amount"):
                    val = int(val)
                update_params[key] = val

        # Targeting is a nested dict — rebuild it
        if "targeting" in updates:
            update_params["targeting"] = _build_targeting(updates["targeting"])

        adset.api_update(params=update_params)

        logger.info("Ad set %s updated with: %s", adset_id, list(updates.keys()))
        return {"success": True, "id": adset_id, "updated_fields": list(updates.keys())}

    except FacebookRequestError as e:
        msg = handle_api_error(e)
        logger.error("Failed to update ad set %s: %s", adset_id, msg)
        return {"success": False, "errors": [msg]}


def list_adsets(
    client: MetaAdsClient, campaign_id: str = None, limit: int = 25, status_filter: str = None
) -> list[dict]:
    """List ad sets, optionally filtered by campaign or status.

    Handles pagination via the SDK cursor.
    """
    try:
        account = client.get_account()
        fields = [
            AdSet.Field.id,
            AdSet.Field.name,
            AdSet.Field.campaign_id,
            AdSet.Field.status,
            AdSet.Field.daily_budget,
            AdSet.Field.lifetime_budget,
            AdSet.Field.bid_strategy,
            AdSet.Field.billing_event,
            AdSet.Field.optimization_goal,
            AdSet.Field.targeting,
            AdSet.Field.start_time,
            AdSet.Field.end_time,
            AdSet.Field.created_time,
        ]

        params = {}
        filtering = []
        if status_filter:
            filtering.append(
                {"field": "effective_status", "operator": "IN", "value": [status_filter.upper()]}
            )
        if campaign_id:
            filtering.append(
                {"field": "campaign.id", "operator": "EQUAL", "value": campaign_id}
            )
        if filtering:
            params["filtering"] = filtering

        adsets_cursor = account.get_ad_sets(fields=fields, params=params)

        results = []
        for adset in adsets_cursor:
            results.append({
                "id": adset["id"],
                "name": adset["name"],
                "campaign_id": adset.get("campaign_id"),
                "status": adset["status"],
                "daily_budget": adset.get("daily_budget"),
                "lifetime_budget": adset.get("lifetime_budget"),
                "bid_strategy": adset.get("bid_strategy"),
                "optimization_goal": adset.get("optimization_goal"),
                "created": adset.get("created_time", "N/A"),
            })
            if len(results) >= limit:
                break

        logger.info("Listed %d ad sets", len(results))
        return results

    except FacebookRequestError as e:
        msg = handle_api_error(e)
        logger.error("Failed to list ad sets: %s", msg)
        return []
