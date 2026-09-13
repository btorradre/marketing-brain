"""API client — initializes the Meta SDK and provides the ad account handle."""

from facebook_business.api import FacebookAdsApi
from facebook_business.session import FacebookSession
from facebook_business.adobjects.adaccount import AdAccount

from meta_ads.utils.logger import setup_logger

logger = setup_logger()


class MetaAdsClient:
    """Per-user Meta API client.

    Creates a non-global FacebookAdsApi instance so multiple users
    can operate concurrently on Vercel serverless without clobbering
    each other's credentials.
    """

    def __init__(self, access_token: str, ad_account_id: str, api_version: str = "v21.0"):
        self.access_token = access_token
        self.ad_account_id = ad_account_id
        self.api_version = api_version
        self.api = self._create_api()
        self.account = AdAccount(ad_account_id, api=self.api)
        logger.info(
            "SDK initialized for account %s (API %s)",
            ad_account_id,
            api_version,
        )

    def _create_api(self) -> FacebookAdsApi:
        """Create a non-global FacebookAdsApi instance."""
        session = FacebookSession(access_token=self.access_token)
        return FacebookAdsApi(session, api_version=self.api_version)

    def get_account(self) -> AdAccount:
        return self.account

    def get_api(self) -> FacebookAdsApi:
        return self.api
