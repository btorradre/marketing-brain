"""Ad operations — create ads with creatives and list existing ads."""

from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.adimage import AdImage
from facebook_business.adobjects.advideo import AdVideo
from facebook_business.exceptions import FacebookRequestError

from meta_ads.api.client import MetaAdsClient
from meta_ads.utils.errors import handle_api_error, format_validation_error
from meta_ads.utils.logger import setup_logger

logger = setup_logger()


def _upload_image(client: MetaAdsClient, image_path: str) -> str:
    """Upload an image file to the ad account and return its hash.

    The image hash is used when creating ad creatives — Meta stores images
    by hash so the same image can be reused across creatives.
    """
    account = client.get_account()
    image = AdImage(parent_id=account.get_id(), api=client.get_api())
    image[AdImage.Field.filename] = image_path
    image.remote_create()
    # remote_create populates the hash field
    image_hash = image[AdImage.Field.hash]
    logger.info("Image uploaded: %s → hash %s", image_path, image_hash)
    return image_hash


def _upload_video(client: MetaAdsClient, video_path: str) -> str:
    """Upload a video file to the ad account and return its ID.

    The video ID is used when creating video ad creatives.
    """
    account = client.get_account()
    video = AdVideo(parent_id=account.get_id(), api=client.get_api())
    video[AdVideo.Field.filepath] = video_path
    video.remote_create()
    video_id = video["id"]
    logger.info("Video uploaded: %s → ID %s", video_path, video_id)
    return video_id


def _create_creative(client: MetaAdsClient, params: dict) -> str:
    """Create an ad creative and return its ID.

    Supports three creative types:
    1. Link ad (image + link) — most common for traffic/conversions
    2. Video ad (video + link) — video creatives
    3. Existing creative ID — skip creation, just reference it

    Required for link/video ads:
        page_id (str): Facebook Page ID to run ads from
        link (str): Destination URL
        message (str): Primary text above the ad
    Optional:
        image_hash (str): Pre-uploaded image hash (or video thumbnail)
        image_path (str): Local image file to upload first
        video_id (str): Pre-uploaded video ID
        video_path (str): Local video file to upload first
        headline (str): Link headline / video title
        description (str): Link description
        call_to_action_type (str): e.g. LEARN_MORE, SHOP_NOW, SIGN_UP
    """
    # If an existing creative ID was provided, skip creation
    if params.get("creative_id"):
        return params["creative_id"]

    account = client.get_account()

    # Upload image if a local path was given
    image_hash = params.get("image_hash")
    if not image_hash and params.get("image_path"):
        image_hash = _upload_image(client, params["image_path"])

    # Upload video if a local path was given
    video_id = params.get("video_id")
    if not video_id and params.get("video_path"):
        video_id = _upload_video(client, params["video_path"])

    cta_type = params.get("call_to_action_type", "LEARN_MORE")

    if video_id:
        # ── Video creative ──
        video_data = {
            "video_id": video_id,
            "message": params.get("message", ""),
            "link_description": params.get("description", ""),
            "call_to_action": {
                "type": cta_type,
                "value": {"link": params["link"]},
            },
        }
        if params.get("headline"):
            video_data["title"] = params["headline"]
        if image_hash:
            video_data["image_hash"] = image_hash  # thumbnail

        creative_params = {
            AdCreative.Field.name: params.get("creative_name", f"Creative - {params.get('headline', 'Ad')}"),
            AdCreative.Field.object_story_spec: {
                "page_id": params["page_id"],
                "video_data": video_data,
            },
        }
    else:
        # ── Image / link creative ──
        link_data = {
            "link": params["link"],
            "message": params.get("message", ""),
        }

        if image_hash:
            link_data["image_hash"] = image_hash
        if params.get("headline"):
            link_data["name"] = params["headline"]
        if params.get("description"):
            link_data["description"] = params["description"]

        link_data["call_to_action"] = {
            "type": cta_type,
            "value": {"link": params["link"]},
        }

        creative_params = {
            AdCreative.Field.name: params.get("creative_name", f"Creative - {params.get('headline', 'Ad')}"),
            AdCreative.Field.object_story_spec: {
                "page_id": params["page_id"],
                "link_data": link_data,
            },
        }

    creative = account.create_ad_creative(params=creative_params)
    creative_id = creative["id"]
    logger.info("Creative created: ID %s", creative_id)
    return creative_id


def validate_ad_params(params: dict) -> list[str]:
    """Validate ad parameters before API call."""
    errors = []

    if not params.get("name"):
        errors.append(format_validation_error("name", "Ad name is required"))
    if not params.get("adset_id"):
        errors.append(format_validation_error("adset_id", "Ad set ID is required"))

    # Must have either a creative_id or enough params to build one
    has_creative_id = bool(params.get("creative_id"))
    has_creative_params = bool(params.get("page_id") and params.get("link"))

    if not has_creative_id and not has_creative_params:
        errors.append(
            format_validation_error(
                "creative",
                "Provide either creative_id or (page_id + link) to build a creative",
            )
        )

    return errors


def create_ad(client: MetaAdsClient, params: dict) -> dict:
    """Create an ad within an existing ad set.

    Required params:
        name (str): Ad name
        adset_id (str): Parent ad set ID
        + creative params (see _create_creative) OR creative_id
    Optional params:
        status (str): PAUSED (default) or ACTIVE
        tracking_specs (list): Conversion tracking specs
    """
    errors = validate_ad_params(params)
    if errors:
        return {"success": False, "errors": errors}

    try:
        # Create or reference the creative
        creative_id = _create_creative(client, params)

        ad_params = {
            Ad.Field.name: params["name"],
            Ad.Field.adset_id: params["adset_id"],
            Ad.Field.creative: {"creative_id": creative_id},
            Ad.Field.status: params.get("status", "PAUSED").upper(),
        }

        if params.get("tracking_specs"):
            ad_params[Ad.Field.tracking_specs] = params["tracking_specs"]

        account = client.get_account()
        ad = account.create_ad(params=ad_params)

        result = {
            "success": True,
            "id": ad["id"],
            "name": params["name"],
            "adset_id": params["adset_id"],
            "creative_id": creative_id,
        }
        logger.info("Ad created: %s (ID: %s)", result["name"], result["id"])
        return result

    except FacebookRequestError as e:
        msg = handle_api_error(e)
        logger.error("Failed to create ad: %s", msg)
        return {"success": False, "errors": [msg]}


def list_ads(
    client: MetaAdsClient, adset_id: str = None, limit: int = 25, status_filter: str = None
) -> list[dict]:
    """List ads with optional filters. Handles pagination via SDK cursor."""
    try:
        account = client.get_account()
        fields = [
            Ad.Field.id,
            Ad.Field.name,
            Ad.Field.adset_id,
            Ad.Field.campaign_id,
            Ad.Field.status,
            Ad.Field.creative,
            Ad.Field.created_time,
        ]

        params = {}
        filtering = []
        if status_filter:
            filtering.append(
                {"field": "effective_status", "operator": "IN", "value": [status_filter.upper()]}
            )
        if adset_id:
            filtering.append({"field": "adset.id", "operator": "EQUAL", "value": adset_id})
        if filtering:
            params["filtering"] = filtering

        ads_cursor = account.get_ads(fields=fields, params=params)

        results = []
        for ad in ads_cursor:
            results.append({
                "id": ad["id"],
                "name": ad["name"],
                "adset_id": ad.get("adset_id"),
                "campaign_id": ad.get("campaign_id"),
                "status": ad["status"],
                "creative_id": ad.get("creative", {}).get("id"),
                "created": ad.get("created_time", "N/A"),
            })
            if len(results) >= limit:
                break

        logger.info("Listed %d ads", len(results))
        return results

    except FacebookRequestError as e:
        msg = handle_api_error(e)
        logger.error("Failed to list ads: %s", msg)
        return []
