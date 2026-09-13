# Google Ads API & Automation

## Google Ads API Overview

### Authentication Requirements
1. **OAuth2 Credentials**: Google Cloud project with Google Ads API enabled → client ID + secret → refresh token
2. **Developer Token**: Obtained through MCC account. Basic (test accounts, 15K ops/day) → Standard (production, 15K ops/day/account)
3. **Login Customer ID**: Which MCC to authenticate through

### Current Version: v18 (check for updates)
- Protocol: gRPC (with REST fallback)
- New versions every 3-4 months, supported ~12 months
- Python library: `google-ads` (pip install google-ads)
- Config: google-ads.yaml or environment variables

---

## Key API Services

| Service | Purpose |
|---|---|
| **GoogleAdsService** | Universal entry — GAQL queries + multi-type mutations |
| **CampaignService** | CRUD campaigns, budgets, bidding, targeting |
| **AdGroupService** | Manage ad groups, bids, targeting |
| **AdGroupAdService** | Create/manage RSAs, display ads, video ads |
| **AdGroupCriterionService** | Keywords (with match types), audiences, placements |
| **KeywordPlanService** | Keyword research, volume, forecasts |
| **CampaignBudgetService** | Shared and campaign budgets |
| **BiddingStrategyService** | Portfolio bidding strategies |
| **ConversionActionService** | Conversion tracking, attribution models |
| **AssetService / AssetGroupService** | Creative assets, PMax asset groups |
| **BatchJobService** | Async bulk operations (10K+) |
| **OfflineUserDataJobService** | Offline conversions, customer match |
| **RecommendationService** | Retrieve/apply optimization recommendations |

---

## GAQL (Google Ads Query Language)

### Syntax
```sql
SELECT field1, field2, metrics.clicks, metrics.impressions
FROM resource_name
WHERE conditions
ORDER BY field
LIMIT n
```

### Key Resources (FROM clause)
campaign, ad_group, ad_group_ad, ad_group_criterion, keyword_view, search_term_view, geographic_view, landing_page_view, change_event, campaign_budget, bidding_strategy, asset, asset_group

### Key Metrics
- metrics.clicks, metrics.impressions, metrics.ctr
- metrics.cost_micros (divide by 1,000,000 for currency)
- metrics.conversions, metrics.conversions_value
- metrics.average_cpc, metrics.average_cpm
- metrics.search_impression_share
- metrics.all_conversions, metrics.view_through_conversions

### Key Segments
- segments.date, segments.month, segments.quarter, segments.year
- segments.device, segments.ad_network_type
- segments.conversion_action

### WHERE Operators
=, !=, <, >, IN, NOT IN, LIKE, CONTAINS ANY/ALL/NONE, IS NULL, BETWEEN, DURING (LAST_7_DAYS, LAST_30_DAYS, THIS_MONTH, etc.)

### Example Queries
```sql
-- Campaign performance last 30 days
SELECT campaign.name, campaign.status, metrics.clicks, metrics.impressions, metrics.cost_micros
FROM campaign
WHERE campaign.status = 'ENABLED' AND segments.date DURING LAST_30_DAYS

-- Top keywords by clicks
SELECT ad_group.name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, metrics.clicks, metrics.conversions
FROM keyword_view
WHERE segments.date DURING LAST_7_DAYS
ORDER BY metrics.clicks DESC LIMIT 50

-- Search terms with high impressions
SELECT search_term_view.search_term, metrics.clicks, metrics.impressions, metrics.conversions
FROM search_term_view
WHERE segments.date DURING LAST_30_DAYS AND metrics.impressions > 100
```

### Rate Limits
- Standard: 15,000 mutate ops/day/account (reads generally unlimited)
- Up to 5,000 operations per mutate request
- Use searchStream (streaming, no pagination) over search for large datasets
- Use BatchJobService for 10,000+ operations

---

## Google Ads Scripts

### Overview
- JavaScript-based automation within Google Ads UI
- No developer token or OAuth needed
- 30-minute execution limit per run
- Schedule: hourly, daily, weekly, monthly

### Common Use Cases
- Bid management based on rules/external data
- Budget pacing (monitor spend vs target)
- Auto-add negatives from search terms
- Quality Score monitoring + alerts
- Pause underperforming ads
- Broken URL detection
- Anomaly detection (spend spikes, CTR drops)
- Auto-generate reports to Google Sheets
- Cross-account management via MCC scripts

### Limitations
- JavaScript only
- Cannot manage PMax campaigns (limited support)
- No customer match or offline conversions
- Limited external API capabilities vs full API

---

## Automated Rules (In-UI)
- Set conditions and actions without coding
- Pause/enable entities based on performance
- Raise/lower bids when conditions met
- Email alerts on thresholds
- Example: "Pause any keyword with CPA > $50 and conversions < 2 in last 14 days"

---

## Integration Ecosystem

| Integration | Purpose |
|---|---|
| **GA4** | Audience sharing, conversion import, cross-channel attribution |
| **Google Tag Manager** | Conversion tracking, remarketing tags, enhanced conversions |
| **Merchant Center** | Product feeds for Shopping/PMax |
| **Looker Studio** | Dashboards combining Google Ads + GA4 + BigQuery |
| **BigQuery** | SQL analysis, historical data, advanced attribution |
| **Offline Conversions** | CRM data → Google Ads for revenue-based optimization |
| **Customer Match** | Upload hashed email/phone lists for targeting |

---

## What a Google Ads Management Agent Should Do

### Account Setup
- Create campaigns with proper settings
- Build ad group structures with themed keywords
- Create RSAs with multiple headline/description variations
- Set up conversion tracking
- Add all relevant ad assets

### Ongoing Optimization
- Pull performance reports via GAQL
- Identify underperforming keywords → pause/adjust
- Mine search terms for keyword + negative keyword opportunities
- Monitor Quality Scores
- Test ad copy systematically
- Manage bids / configure Smart Bidding
- Pace budgets
- Detect anomalies and alert

### Reporting & Analysis
- Generate performance summaries on demand
- Calculate KPIs (CPA, ROAS, impression share, QS trends)
- Compare time periods
- Segment analysis (device, location, time, audience)

### Advanced
- Manage customer match audiences
- Upload offline conversions
- Handle PMax asset group management
- Cross-account MCC management
- Execute multi-step optimization workflows
