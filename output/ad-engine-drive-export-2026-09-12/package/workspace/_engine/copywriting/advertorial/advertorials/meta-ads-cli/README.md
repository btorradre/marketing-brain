# Meta Ads CLI

A command-line tool for managing Meta (Facebook/Instagram) advertising campaigns via the Marketing API.

## Features

- **Campaign management** — create and list campaigns with configurable objectives and budgets
- **Ad set management** — create, update, and list ad sets with audience targeting, scheduling, and bid strategies
- **Ad management** — create ads with inline creative building (image upload, copy, URLs) or reference existing creatives
- **Bulk operations** — define multiple campaigns, ad sets, and ads in a single JSON file and deploy them all at once
- **Production-ready** — input validation, API error handling (rate limits, permissions, token expiry), pagination, and structured logging

## Project Structure

```
meta-ads-cli/
├── .env                    # Your credentials (never committed)
├── .env.example            # Template for .env
├── requirements.txt
├── setup.py                # Install as CLI tool
├── config/
│   └── sample_bulk.json    # Example bulk config
├── meta_ads/
│   ├── cli.py              # CLI entry point (argparse)
│   ├── config.py           # Environment/config loading
│   ├── bulk.py             # Bulk JSON operations
│   ├── api/
│   │   ├── client.py       # SDK initialization wrapper
│   │   ├── campaigns.py    # Campaign CRUD
│   │   ├── adsets.py       # Ad set CRUD + update
│   │   └── ads.py          # Ad + creative CRUD
│   └── utils/
│       ├── logger.py       # Structured logging
│       └── errors.py       # API error translation
```

## Setup

### 1. Prerequisites

- Python 3.10+
- A Meta developer app with Marketing API access
- A long-lived access token (generate via [Access Token Tool](https://developers.facebook.com/tools/accesstoken/))
- Your Ad Account ID (find it in [Ads Manager](https://adsmanager.facebook.com/) → Account dropdown)

### 2. Install

```bash
cd meta-ads-cli

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install as CLI tool (optional — lets you run `meta-ads` from anywhere)
pip install -e .
```

### 3. Configure

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```
META_ACCESS_TOKEN=your_long_lived_token
META_AD_ACCOUNT_ID=act_123456789
META_API_VERSION=v21.0
```

## Usage

Run commands with `python -m meta_ads.cli` or `meta-ads` (if installed via setup.py).

### Campaigns

```bash
# Create a campaign
meta-ads campaign-create \
  --name "My Campaign" \
  --objective OUTCOME_TRAFFIC \
  --status PAUSED \
  --daily-budget 5000

# List campaigns
meta-ads campaign-list
meta-ads campaign-list --status ACTIVE --limit 10
```

### Ad Sets

```bash
# Create an ad set
meta-ads adset-create \
  --name "US Women 25-45" \
  --campaign-id 12345678 \
  --daily-budget 2000 \
  --optimization-goal LINK_CLICKS \
  --targeting '{"geo_locations": {"countries": ["US"]}, "age_min": 25, "age_max": 45, "genders": [2]}'

# Update an ad set
meta-ads adset-update 98765432 \
  --daily-budget 3000 \
  --status ACTIVE

# List ad sets
meta-ads adset-list --campaign-id 12345678
```

### Ads

```bash
# Create an ad with inline creative
meta-ads ad-create \
  --name "Hero Image Ad" \
  --adset-id 98765432 \
  --page-id 111222333 \
  --link "https://yoursite.com/landing" \
  --message "Check out our summer sale!" \
  --headline "Summer Sale - 50% Off" \
  --description "Shop now" \
  --image-path ./creative.jpg \
  --cta SHOP_NOW

# Create an ad using an existing creative
meta-ads ad-create \
  --name "Reuse Creative" \
  --adset-id 98765432 \
  --creative-id 444555666

# List ads
meta-ads ad-list --adset-id 98765432
```

### Bulk Operations

Define your full campaign structure in a JSON file and deploy everything at once:

```bash
meta-ads bulk config/sample_bulk.json
```

See `config/sample_bulk.json` for the full schema. The bulk engine creates campaigns → ad sets → ads in sequence, linking IDs automatically.

## Targeting Reference

The targeting JSON supports these fields:

| Field | Type | Example |
|-------|------|---------|
| `geo_locations` | object | `{"countries": ["US", "CA"]}` |
| `age_min` | int (18-65) | `25` |
| `age_max` | int (18-65) | `45` |
| `genders` | list | `[1]` male, `[2]` female |
| `interests` | list | `[{"id": "6003139266461", "name": "Yoga"}]` |
| `custom_audiences` | list | `[{"id": "23456789"}]` |
| `publisher_platforms` | list | `["facebook", "instagram"]` |
| `device_platforms` | list | `["mobile", "desktop"]` |

## Campaign Objectives (v21.0+)

| Objective | Use Case |
|-----------|----------|
| `OUTCOME_AWARENESS` | Brand awareness, reach |
| `OUTCOME_ENGAGEMENT` | Post engagement, page likes |
| `OUTCOME_LEADS` | Lead generation forms |
| `OUTCOME_SALES` | Conversions, catalog sales |
| `OUTCOME_TRAFFIC` | Website/app traffic |
| `OUTCOME_APP_PROMOTION` | App installs |

## Error Handling

The CLI translates Meta API errors into actionable messages:

- **Rate limits** (error 4, 17) — wait and retry
- **Token expired** (error 190) — regenerate your access token
- **Permission denied** (error 10, 200) — check app permissions
- **Invalid params** (error 100) — check your input values
- **Account not found** (error 2635) — verify your `META_AD_ACCOUNT_ID`

All errors include the original API error code for debugging.

## Adding New Operations

The codebase is structured for easy extension:

1. **New API operation** — add a function in the appropriate `meta_ads/api/` module
2. **New CLI command** — add a parser in `build_parser()` and a handler in `COMMANDS` dict in `cli.py`
3. **New bulk support** — extend `meta_ads/bulk.py` to handle the new object type
