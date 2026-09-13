"""Pixel operations — list Meta Pixels associated with the ad account."""

from facebook_business.adobjects.adspixel import AdsPixel
from facebook_business.exceptions import FacebookRequestError

from meta_ads.api.client import MetaAdsClient
from meta_ads.utils.errors import handle_api_error
from meta_ads.utils.logger import setup_logger

logger = setup_logger()


def list_pixels(client: MetaAdsClient, limit: int = 50) -> list[dict]:
    """List Meta Pixels for the ad account.

    Returns a list of dicts with 'id' and 'name' for each pixel.
    """
    try:
        account = client.get_account()
        fields = [
            AdsPixel.Field.id,
            AdsPixel.Field.name,
        ]

        pixels_cursor = account.get_ads_pixels(fields=fields, params={})

        results = []
        for pixel in pixels_cursor:
            results.append({
                "id": pixel["id"],
                "name": pixel.get("name", f"Pixel {pixel['id']}"),
            })
            if len(results) >= limit:
                break

        logger.info("Listed %d pixels", len(results))
        return results

    except FacebookRequestError as e:
        msg = handle_api_error(e)
        logger.error("Failed to list pixels: %s", msg)
        return []
