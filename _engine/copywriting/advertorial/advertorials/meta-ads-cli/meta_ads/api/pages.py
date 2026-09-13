"""Page operations — list Facebook Pages available to the current user."""

from facebook_business.adobjects.user import User
from facebook_business.exceptions import FacebookRequestError

from meta_ads.api.client import MetaAdsClient
from meta_ads.utils.errors import handle_api_error
from meta_ads.utils.logger import setup_logger

logger = setup_logger()


def list_pages(client: MetaAdsClient, limit: int = 50) -> list[dict]:
    """List Facebook Pages the authenticated user manages.

    Uses the /me/accounts endpoint via the User SDK class.
    Returns a list of dicts with 'id' and 'name' for each page.
    """
    try:
        # The User('me') endpoint returns pages managed by the access token owner
        user = User(fbid="me", api=client.get_api())
        pages_cursor = user.get_accounts(fields=["id", "name"], params={})

        results = []
        for page in pages_cursor:
            results.append({
                "id": page["id"],
                "name": page.get("name", f"Page {page['id']}"),
            })
            if len(results) >= limit:
                break

        logger.info("Listed %d pages", len(results))
        return results

    except FacebookRequestError as e:
        msg = handle_api_error(e)
        logger.error("Failed to list pages: %s", msg)
        return []
