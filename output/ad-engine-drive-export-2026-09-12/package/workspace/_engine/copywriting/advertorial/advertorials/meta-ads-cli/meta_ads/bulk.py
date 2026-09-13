"""Bulk operations — load a JSON config file and execute batch creates."""

import json
from pathlib import Path

from meta_ads.api.client import MetaAdsClient
from meta_ads.api.campaigns import create_campaign
from meta_ads.api.adsets import create_adset
from meta_ads.api.ads import create_ad
from meta_ads.utils.logger import setup_logger

logger = setup_logger()


def load_bulk_config(filepath: str) -> dict:
    """Load and parse a JSON bulk config file.

    Expected structure:
    {
      "campaigns": [
        {
          "name": "...",
          "objective": "...",
          "ad_sets": [
            {
              "name": "...",
              "daily_budget": 500,
              "targeting": {...},
              "ads": [
                { "name": "...", "page_id": "...", "link": "...", ... }
              ]
            }
          ]
        }
      ]
    }
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Bulk config not found: {filepath}")
    if path.suffix not in (".json",):
        raise ValueError(f"Unsupported file format: {path.suffix}. Use .json")

    with open(path, "r") as f:
        data = json.load(f)

    if "campaigns" not in data:
        raise ValueError("Bulk config must have a top-level 'campaigns' key")

    return data


def execute_bulk(client: MetaAdsClient, filepath: str) -> dict:
    """Execute a bulk config: create campaigns → ad sets → ads in sequence.

    Returns a summary of all created objects and any errors.
    """
    config = load_bulk_config(filepath)
    summary = {"created": [], "errors": []}

    for camp_def in config["campaigns"]:
        # Extract nested ad_sets before passing to campaign create
        adset_defs = camp_def.pop("ad_sets", [])

        logger.info("Creating campaign: %s", camp_def.get("name"))
        camp_result = create_campaign(client, camp_def)

        if not camp_result.get("success"):
            summary["errors"].append({
                "type": "campaign",
                "name": camp_def.get("name"),
                "errors": camp_result.get("errors", []),
            })
            continue

        summary["created"].append({"type": "campaign", **camp_result})
        campaign_id = camp_result["id"]

        # Create ad sets under this campaign
        for adset_def in adset_defs:
            ad_defs = adset_def.pop("ads", [])
            adset_def["campaign_id"] = campaign_id

            logger.info("  Creating ad set: %s", adset_def.get("name"))
            adset_result = create_adset(client, adset_def)

            if not adset_result.get("success"):
                summary["errors"].append({
                    "type": "adset",
                    "name": adset_def.get("name"),
                    "errors": adset_result.get("errors", []),
                })
                continue

            summary["created"].append({"type": "adset", **adset_result})
            adset_id = adset_result["id"]

            # Create ads under this ad set
            for ad_def in ad_defs:
                ad_def["adset_id"] = adset_id

                logger.info("    Creating ad: %s", ad_def.get("name"))
                ad_result = create_ad(client, ad_def)

                if not ad_result.get("success"):
                    summary["errors"].append({
                        "type": "ad",
                        "name": ad_def.get("name"),
                        "errors": ad_result.get("errors", []),
                    })
                    continue

                summary["created"].append({"type": "ad", **ad_result})

    # Print summary
    created_count = len(summary["created"])
    error_count = len(summary["errors"])
    logger.info(
        "Bulk complete: %d objects created, %d errors", created_count, error_count
    )

    return summary
