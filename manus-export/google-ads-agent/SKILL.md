---
name: google-ads-agent
description: Full-service Google Ads management agent covering account setup, campaign creation, keyword research, ad copywriting, bidding strategy, ongoing optimization, reporting, and account audits across Search, Performance Max, Shopping, Display, Video, and Demand Gen. Use whenever the task is to create, manage, optimize, audit, or report on a Google Ads account or campaign — account setup, campaign launches, keyword research, ad copy creation, bid management, search-term mining, negative-keyword management, Quality Score work, conversion tracking setup, Performance Max management, or Shopping feed optimization.
---

## Golden Nugget Doctrine (mandatory, applies before any ad copy or angle work)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded deep frame in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: is this the topic, or is this the motive? If it's the topic, dig one layer deeper.
- **Where it goes.** The golden nugget leads — very top of the piece, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence before drafting.

## Knowledge base

Deep reference material — full tables, formulas, GAQL examples, and policy detail — lives in `references/`, one file per topic:

- `references/01-account-structure-and-campaign-types.md` — account hierarchy, MCC, all campaign types
- `references/02-keyword-strategy.md` — match types, negatives, Quality Score, keyword grouping
- `references/03-bidding-strategies.md` — every bidding strategy, learning-period rules, when to switch
- `references/04-campaign-optimization.md` — search-term mining, ad testing, budget allocation, PMax optimization, scaling, account health checklist, common mistakes
- `references/05-ad-creative-and-copywriting.md` — RSA best practices, headline formulas, ad assets, Shopping feeds, policy compliance
- `references/06-conversion-tracking-and-measurement.md` — tracking setup, enhanced conversions, attribution, metrics/formulas, benchmarks
- `references/07-google-ads-api-and-automation.md` — API services, GAQL queries, Scripts, integrations
- `references/08-landing-page-best-practices.md` — message match, speed, mobile, CRO, trust signals

Before any Google Ads task, read the relevant reference file(s) rather than relying on memory — this knowledge base is more current and more precise than what a general model knows about Google Ads mechanics.

## Capabilities

1. **Account setup and structure** — create/configure an account; set account-level settings (time zone, currency, auto-tagging); link Google Analytics 4, Merchant Center, Google Business Profile; set up conversion tracking (native tag or via a tag manager); configure enhanced conversions.
2. **Campaign creation** — Search campaigns (proper settings, keyword themes, Responsive Search Ads, all ad assets); Performance Max (asset groups, audience signals, search themes, brand exclusions); Shopping (Merchant Center feed, Standard Shopping + PMax hybrid); Display (remarketing and prospecting); Video/YouTube (TrueView, Bumper, Shorts, Demand Gen); Demand Gen (cross-channel visual advertising).
3. **Keyword research and strategy** — use a keyword-volume/competition/CPC research tool; build Single Theme Ad Group (STAG) structures; set up negative keyword lists (universal + industry-specific); align match-type strategy with the bidding approach.
4. **Ad copywriting** — write Responsive Search Ads with 15 headlines and 4 descriptions following best practices; mix headline types (benefit, question, urgency, social proof, CTA, feature, price); set up dynamic keyword insertion, ad customizers, countdown timers; use strategic pinning minimally (only for brand/legal requirements); write ad assets — sitelinks, callouts, structured snippets, promotions.
5. **Bidding strategy selection** — recommend a strategy based on conversion volume and business goals; configure target CPA, target ROAS, Maximize Conversions, Maximize Conversion Value; set up portfolio bid strategies when appropriate; monitor learning periods and enforce no-change windows during them.
6. **Ongoing optimization** — weekly search-term mining to find new negatives and new keywords; ad copy testing (champion/challenger); budget allocation by marginal CPA/ROAS; Quality Score monitoring and improvement; device, geo, and daypart bid adjustments; Performance Max asset group optimization, audience signal tuning, brand exclusions; impression-share analysis (Lost IS to Budget vs. Lost IS to Rank).
7. **Reporting and analysis** — pull campaign/ad group/keyword performance data; calculate KPIs (CPA, ROAS, CTR, conversion rate, impression share); do period-over-period comparisons; segment by device, location, time, audience; run competitive analysis via Auction Insights; identify wasted spend.
8. **Account audits** — full account health audit against a checklist; identify and fix common mistakes; review Optimization Score recommendations (apply the good ones, dismiss the bad ones — never auto-apply blindly); audit conversion tracking; audit negative keyword coverage.

## Workflow: account setup

1. Sign in to the Google Ads account (create a new one if needed, or navigate to the existing one).
2. Set time zone and currency first — these cannot be changed later.
3. Enable auto-tagging in account settings.
4. Set up conversion tracking (native tag or via a tag manager).
5. Link Google Analytics 4.
6. Link Merchant Center if the business is e-commerce.
7. Determine the right campaign type for the business goal (see decision tree below), then set campaign-level settings: descriptive name (e.g. "Search - [Product] - [Geo]"), networks (Search campaigns: Search only, uncheck Search Partners initially), locations (target by "presence," not "presence or interest"), languages, bidding strategy (start with Manual CPC or Maximize Clicks if under 30 conversions/month), daily budget, ad schedule if applicable.
8. Build ad groups using the STAG structure — 5 to 15 tightly themed keywords per group.
9. Add keywords with appropriate match types.
10. Write Responsive Search Ads — 15 headlines, 4 descriptions per ad group.
11. Add all relevant ad assets: sitelinks, callouts, structured snippets, and others.
12. Create a shared negative keyword list with universal negatives, add industry-specific negatives, and apply the list to all campaigns.
13. Set up conversion actions: choose counting method (One for leads, Every for e-commerce), set conversion window to match the sales cycle, set attribution model (Data-Driven recommended), install the tracking tag, and set up enhanced conversions if possible.

## Workflow: ongoing optimization

**Weekly:**
1. Pull the search terms report → add negatives, identify new keywords.
2. Check conversion tracking for drops or anomalies.
3. Review budget pacing against the monthly target.
4. Check for disapproved ads → fix or appeal.
5. Review bidding strategy status (still learning? limited by budget?).
6. Check impression-share metrics.

**Monthly:**
1. Analyze Quality Score trends.
2. Review geographic performance → adjust bids/exclusions.
3. Review device performance → adjust bids.
4. Review ad copy performance → pause losers, launch challengers.
5. Review audience performance.
6. Review the Performance Max Insights tab.

**Quarterly:**
1. Full negative keyword audit.
2. Landing page performance review.
3. Campaign structure review (consolidate or expand?).
4. Conversion tracking audit.
5. Competitor analysis via Auction Insights.
6. Account settings review.

## Decision trees

**Which campaign type?**
- High purchase intent + text ads → Search
- E-commerce + product feed → Shopping + Performance Max hybrid
- Brand awareness + visual → Display or YouTube
- Cross-channel reach → Performance Max
- App installs → App campaigns
- Visual engagement + Gmail/Discover placements → Demand Gen

**Which bidding strategy?**
- 0–15 conversions/month → Manual CPC or Maximize Clicks
- 15–30 conversions/month → Enhanced CPC (transitional)
- 30+ conversions/month, lead gen → target CPA, or Maximize Conversions + target CPA
- 50+ conversions/month, e-commerce → target ROAS, or Maximize Conversion Value + target ROAS
- Brand defense → Target Impression Share (95% absolute top)

**When to scale?**
- CPA/ROAS has met target for 2–4 consecutive weeks → yes, scale
- Impression Share Lost to Budget is above 10% → increase budget, max 20% at a time
- High-intent demand is exhausted → expand keywords, match types, campaign types, or geos

## Critical rules

1. Always separate brand campaigns from non-brand campaigns.
2. Never auto-apply Google's optimization recommendations — review each one manually.
3. Never change budget by more than 20% in a single day — it disrupts the bidding algorithm's learning.
4. Never make strategy changes during a learning period (the 7–14 days after a bidding-strategy change).
5. Always set up negative keywords from day one.
6. Always use ad assets at minimum: sitelinks, callouts, structured snippets.
7. Target by "presence," never "presence or interest," for location targeting.
8. Supply your own video creative for Performance Max — Google's auto-generated video is poor quality.
9. Add brand exclusions to Performance Max campaigns to prevent them from cannibalizing brand search traffic.
10. Optimize for macro conversions (real business outcomes); only use micro-conversions as a stepping stone when conversion volume is too low to optimize on macro conversions directly.

## Supplement / health product specific rules

Apply these whenever the account is for a supplement or health product:

**Compliance:**
- Cannot claim to cure, treat, or prevent diseases.
- Can say things like "Supports healthy [function]," "May help with [general wellness]."
- Include an FDA-style disclaimer: "These statements have not been evaluated by the FDA..."
- Avoid the words "cure," "heal," "treatment," "remedy."
- Structure/function claims are acceptable when paired with disclaimers.
- Before/after images may require disclaimers.
- The account may need LegitScript certification.
- Weight-loss claims are heavily scrutinized — avoid superlative language.

**Shopping feed:**
- Product titles: Brand + Product Type + Key Attributes (count, flavor, form).
- Include a GTIN if one is available.
- No health claims in product descriptions.
- Use high-quality product images on a white background.
- Use custom labels segmented by margin, by performance, and by product line.

For the full common-disapproval-reasons list and the appeal process, see `references/05-ad-creative-and-copywriting.md`.
