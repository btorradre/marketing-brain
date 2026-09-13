"""CLI entry point — argparse-based interface for all Meta Ads operations."""

import argparse
import json
import sys

from meta_ads.config import load_config
from meta_ads.api.client import MetaAdsClient
from meta_ads.api.campaigns import create_campaign, list_campaigns
from meta_ads.api.adsets import create_adset, update_adset, list_adsets
from meta_ads.api.ads import create_ad, list_ads
from meta_ads.bulk import execute_bulk
from meta_ads.utils.logger import setup_logger


def print_table(rows: list[dict], columns: list[str] = None):
    """Print a list of dicts as a formatted table."""
    if not rows:
        print("  (no results)")
        return

    if not columns:
        columns = list(rows[0].keys())

    # Calculate column widths
    widths = {col: len(col) for col in columns}
    for row in rows:
        for col in columns:
            val = str(row.get(col, ""))
            widths[col] = max(widths[col], len(val))

    # Header
    header = "  ".join(col.upper().ljust(widths[col]) for col in columns)
    print(header)
    print("  ".join("-" * widths[col] for col in columns))

    # Rows
    for row in rows:
        line = "  ".join(str(row.get(col, "")).ljust(widths[col]) for col in columns)
        print(line)


# ── Campaign commands ──────────────────────────────────────────────


def cmd_create_campaign(client: MetaAdsClient, args):
    params = {
        "name": args.name,
        "objective": args.objective,
        "status": args.status,
        "buying_type": args.buying_type,
    }
    if args.daily_budget:
        params["daily_budget"] = args.daily_budget
    if args.lifetime_budget:
        params["lifetime_budget"] = args.lifetime_budget
    if args.special_ad_categories:
        params["special_ad_categories"] = args.special_ad_categories.split(",")

    result = create_campaign(client, params)
    if result.get("success"):
        print(f"\nCampaign created successfully!")
        print(f"  ID:   {result['id']}")
        print(f"  Name: {result['name']}")
    else:
        print(f"\nFailed to create campaign:")
        for err in result.get("errors", []):
            print(f"  - {err}")
        sys.exit(1)


def cmd_list_campaigns(client: MetaAdsClient, args):
    campaigns = list_campaigns(client, limit=args.limit, status_filter=args.status)
    print(f"\nCampaigns ({len(campaigns)} found):")
    print_table(campaigns, ["id", "name", "objective", "status", "daily_budget", "created"])


# ── Ad Set commands ────────────────────────────────────────────────


def cmd_create_adset(client: MetaAdsClient, args):
    params = {
        "name": args.name,
        "campaign_id": args.campaign_id,
        "billing_event": args.billing_event,
        "optimization_goal": args.optimization_goal,
        "bid_strategy": args.bid_strategy,
        "status": args.status,
    }
    if args.daily_budget:
        params["daily_budget"] = args.daily_budget
    if args.lifetime_budget:
        params["lifetime_budget"] = args.lifetime_budget
    if args.bid_amount:
        params["bid_amount"] = args.bid_amount
    if args.start_time:
        params["start_time"] = args.start_time
    if args.end_time:
        params["end_time"] = args.end_time

    # Parse targeting from JSON string if provided
    if args.targeting:
        try:
            params["targeting"] = json.loads(args.targeting)
        except json.JSONDecodeError:
            print("ERROR: --targeting must be valid JSON")
            sys.exit(1)

    # Parse promoted object from JSON if provided
    if args.promoted_object:
        try:
            params["promoted_object"] = json.loads(args.promoted_object)
        except json.JSONDecodeError:
            print("ERROR: --promoted-object must be valid JSON")
            sys.exit(1)

    result = create_adset(client, params)
    if result.get("success"):
        print(f"\nAd set created successfully!")
        print(f"  ID:          {result['id']}")
        print(f"  Name:        {result['name']}")
        print(f"  Campaign ID: {result['campaign_id']}")
    else:
        print(f"\nFailed to create ad set:")
        for err in result.get("errors", []):
            print(f"  - {err}")
        sys.exit(1)


def cmd_update_adset(client: MetaAdsClient, args):
    updates = {}
    if args.name:
        updates["name"] = args.name
    if args.status:
        updates["status"] = args.status
    if args.daily_budget:
        updates["daily_budget"] = args.daily_budget
    if args.lifetime_budget:
        updates["lifetime_budget"] = args.lifetime_budget
    if args.bid_amount:
        updates["bid_amount"] = args.bid_amount
    if args.bid_strategy:
        updates["bid_strategy"] = args.bid_strategy
    if args.start_time:
        updates["start_time"] = args.start_time
    if args.end_time:
        updates["end_time"] = args.end_time
    if args.targeting:
        try:
            updates["targeting"] = json.loads(args.targeting)
        except json.JSONDecodeError:
            print("ERROR: --targeting must be valid JSON")
            sys.exit(1)

    if not updates:
        print("ERROR: No update fields provided. Use --help to see options.")
        sys.exit(1)

    result = update_adset(client, args.adset_id, updates)
    if result.get("success"):
        print(f"\nAd set {args.adset_id} updated successfully!")
        print(f"  Updated fields: {', '.join(result['updated_fields'])}")
    else:
        print(f"\nFailed to update ad set:")
        for err in result.get("errors", []):
            print(f"  - {err}")
        sys.exit(1)


def cmd_list_adsets(client: MetaAdsClient, args):
    adsets = list_adsets(
        client,
        campaign_id=args.campaign_id,
        limit=args.limit,
        status_filter=args.status,
    )
    print(f"\nAd Sets ({len(adsets)} found):")
    print_table(adsets, ["id", "name", "campaign_id", "status", "daily_budget", "bid_strategy"])


# ── Ad commands ────────────────────────────────────────────────────


def cmd_create_ad(client: MetaAdsClient, args):
    params = {
        "name": args.name,
        "adset_id": args.adset_id,
        "status": args.status,
    }

    if args.creative_id:
        params["creative_id"] = args.creative_id
    else:
        # Building a new creative inline
        if args.page_id:
            params["page_id"] = args.page_id
        if args.link:
            params["link"] = args.link
        if args.message:
            params["message"] = args.message
        if args.headline:
            params["headline"] = args.headline
        if args.description:
            params["description"] = args.description
        if args.image_path:
            params["image_path"] = args.image_path
        if args.image_hash:
            params["image_hash"] = args.image_hash
        if args.cta:
            params["call_to_action_type"] = args.cta

    result = create_ad(client, params)
    if result.get("success"):
        print(f"\nAd created successfully!")
        print(f"  ID:          {result['id']}")
        print(f"  Name:        {result['name']}")
        print(f"  Ad Set ID:   {result['adset_id']}")
        print(f"  Creative ID: {result['creative_id']}")
    else:
        print(f"\nFailed to create ad:")
        for err in result.get("errors", []):
            print(f"  - {err}")
        sys.exit(1)


def cmd_list_ads(client: MetaAdsClient, args):
    ads = list_ads(client, adset_id=args.adset_id, limit=args.limit, status_filter=args.status)
    print(f"\nAds ({len(ads)} found):")
    print_table(ads, ["id", "name", "adset_id", "campaign_id", "status", "creative_id"])


# ── Bulk command ───────────────────────────────────────────────────


def cmd_bulk(client: MetaAdsClient, args):
    print(f"\nExecuting bulk config: {args.file}")
    summary = execute_bulk(client, args.file)

    print(f"\n{'='*60}")
    print(f"BULK OPERATION SUMMARY")
    print(f"{'='*60}")

    if summary["created"]:
        print(f"\nCreated ({len(summary['created'])} objects):")
        for obj in summary["created"]:
            print(f"  [{obj['type'].upper():8s}] {obj.get('name', 'N/A'):30s} → ID: {obj['id']}")

    if summary["errors"]:
        print(f"\nErrors ({len(summary['errors'])}):")
        for err in summary["errors"]:
            print(f"  [{err['type'].upper():8s}] {err.get('name', 'N/A')}:")
            for e in err.get("errors", []):
                print(f"    - {e}")

    if not summary["errors"]:
        print("\nAll operations completed successfully!")
    else:
        sys.exit(1)


# ── Parser setup ──────────────────────────────────────────────────


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="meta-ads",
        description="Meta Marketing API CLI — manage campaigns, ad sets, and ads",
    )
    parser.add_argument("--env", help="Path to .env file", default=None)
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # ── campaign create ──
    p = subparsers.add_parser("campaign-create", help="Create a new campaign")
    p.add_argument("--name", required=True, help="Campaign name")
    p.add_argument(
        "--objective",
        default="OUTCOME_TRAFFIC",
        help="Campaign objective (default: OUTCOME_TRAFFIC)",
    )
    p.add_argument("--status", default="PAUSED", help="PAUSED or ACTIVE (default: PAUSED)")
    p.add_argument("--daily-budget", type=int, dest="daily_budget", help="Daily budget in cents")
    p.add_argument(
        "--lifetime-budget", type=int, dest="lifetime_budget", help="Lifetime budget in cents"
    )
    p.add_argument("--buying-type", default="AUCTION", dest="buying_type", help="AUCTION or RESERVED")
    p.add_argument(
        "--special-ad-categories",
        dest="special_ad_categories",
        help="Comma-separated: HOUSING,CREDIT,EMPLOYMENT",
    )

    # ── campaign list ──
    p = subparsers.add_parser("campaign-list", help="List campaigns")
    p.add_argument("--limit", type=int, default=25, help="Max results (default: 25)")
    p.add_argument("--status", help="Filter by status: ACTIVE, PAUSED, ARCHIVED")

    # ── adset create ──
    p = subparsers.add_parser("adset-create", help="Create a new ad set")
    p.add_argument("--name", required=True, help="Ad set name")
    p.add_argument("--campaign-id", required=True, dest="campaign_id", help="Parent campaign ID")
    p.add_argument("--daily-budget", type=int, dest="daily_budget", help="Daily budget in cents")
    p.add_argument("--lifetime-budget", type=int, dest="lifetime_budget", help="Lifetime budget in cents")
    p.add_argument("--billing-event", default="IMPRESSIONS", dest="billing_event")
    p.add_argument("--optimization-goal", default="LINK_CLICKS", dest="optimization_goal")
    p.add_argument("--bid-strategy", default="LOWEST_COST_WITHOUT_CAP", dest="bid_strategy")
    p.add_argument("--bid-amount", type=int, dest="bid_amount", help="Bid cap in cents")
    p.add_argument("--start-time", dest="start_time", help="ISO 8601 start time")
    p.add_argument("--end-time", dest="end_time", help="ISO 8601 end time")
    p.add_argument("--status", default="PAUSED", help="PAUSED or ACTIVE")
    p.add_argument("--targeting", help='Targeting spec as JSON string')
    p.add_argument("--promoted-object", dest="promoted_object", help='Promoted object as JSON string')

    # ── adset update ──
    p = subparsers.add_parser("adset-update", help="Update an existing ad set")
    p.add_argument("adset_id", help="Ad set ID to update")
    p.add_argument("--name", help="New name")
    p.add_argument("--status", help="ACTIVE, PAUSED")
    p.add_argument("--daily-budget", type=int, dest="daily_budget")
    p.add_argument("--lifetime-budget", type=int, dest="lifetime_budget")
    p.add_argument("--bid-amount", type=int, dest="bid_amount")
    p.add_argument("--bid-strategy", dest="bid_strategy")
    p.add_argument("--start-time", dest="start_time")
    p.add_argument("--end-time", dest="end_time")
    p.add_argument("--targeting", help='Targeting spec as JSON string')

    # ── adset list ──
    p = subparsers.add_parser("adset-list", help="List ad sets")
    p.add_argument("--campaign-id", dest="campaign_id", help="Filter by campaign ID")
    p.add_argument("--limit", type=int, default=25)
    p.add_argument("--status", help="Filter by status")

    # ── ad create ──
    p = subparsers.add_parser("ad-create", help="Create a new ad")
    p.add_argument("--name", required=True, help="Ad name")
    p.add_argument("--adset-id", required=True, dest="adset_id", help="Parent ad set ID")
    p.add_argument("--status", default="PAUSED")
    # Creative — either provide an ID or build inline
    p.add_argument("--creative-id", dest="creative_id", help="Existing creative ID")
    p.add_argument("--page-id", dest="page_id", help="Facebook Page ID (for new creative)")
    p.add_argument("--link", help="Destination URL")
    p.add_argument("--message", help="Primary text")
    p.add_argument("--headline", help="Link headline")
    p.add_argument("--description", help="Link description")
    p.add_argument("--image-path", dest="image_path", help="Local image file path")
    p.add_argument("--image-hash", dest="image_hash", help="Pre-uploaded image hash")
    p.add_argument("--cta", default="LEARN_MORE", help="Call to action type (default: LEARN_MORE)")

    # ── ad list ──
    p = subparsers.add_parser("ad-list", help="List ads")
    p.add_argument("--adset-id", dest="adset_id", help="Filter by ad set ID")
    p.add_argument("--limit", type=int, default=25)
    p.add_argument("--status", help="Filter by status")

    # ── bulk ──
    p = subparsers.add_parser("bulk", help="Execute bulk operations from JSON file")
    p.add_argument("file", help="Path to JSON config file")

    return parser


# Command dispatch map
COMMANDS = {
    "campaign-create": cmd_create_campaign,
    "campaign-list": cmd_list_campaigns,
    "adset-create": cmd_create_adset,
    "adset-update": cmd_update_adset,
    "adset-list": cmd_list_adsets,
    "ad-create": cmd_create_ad,
    "ad-list": cmd_list_ads,
    "bulk": cmd_bulk,
}


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    # Load config and initialize client
    config = load_config(args.env)
    logger = setup_logger(config["log_level"])
    client = MetaAdsClient(config)

    # Dispatch to the appropriate command handler
    handler = COMMANDS.get(args.command)
    if handler:
        handler(client, args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
