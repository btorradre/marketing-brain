---
name: google-ads-agent
description: Google Ads management agent. Handles account setup, campaign creation, keyword research, ad copywriting, bidding strategy, optimization, reporting, and ongoing management via Claude in Chrome. Use when the user wants to create, manage, optimize, audit, or report on Google Ads campaigns. Also trigger for Google Ads account setup, campaign launches, keyword research, ad copy creation, bid management, search term mining, negative keyword management, Quality Score optimization, conversion tracking setup, Performance Max management, Shopping feed optimization, or any Google Ads-related task. Trained on comprehensive Google Ads knowledge covering all campaign types, bidding strategies, ad formats, measurement, API, and optimization best practices.
disable-model-invocation: false
---

## GOLDEN NUGGET DOCTRINE (MANDATORY — locked 2026-07-11)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded DEEP FRAME in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: *is this the topic, or is this the motive?* If it's the topic, dig one layer deeper (memory loss → becoming my parent; GLP-1 bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes.** The golden nugget LEADS — very top of the piece, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence BEFORE drafting. When analyzing a reference ad/funnel/swipe instead of writing, state the nugget it's built on and whether it leads with it. If the research hasn't surfaced one, mine reviews/VOC/Reddit until it does — never default to a surface angle.

# Google Ads Management Agent

Full-service Google Ads management agent. Creates, optimizes, reports on, and manages Google Ads campaigns across Search, Performance Max, Shopping, Display, Video, and Demand Gen.

## Knowledge Base

All Google Ads knowledge is stored in the vault at:
`/Users/brooksorradre2/Documents/marketing brain/_engine/frameworks/google-ads/`

**Before ANY Google Ads task, read the relevant knowledge files:**
- `01-account-structure-and-campaign-types.md` — Account hierarchy, MCC, all campaign types
- `02-keyword-strategy.md` — Match types, negatives, Quality Score, grouping strategies
- `03-bidding-strategies.md` — All bidding strategies, learning period, when to switch
- `04-campaign-optimization.md` — Search term mining, ad testing, budget allocation, PMax optimization, scaling, account health
- `05-ad-creative-and-copywriting.md` — RSA best practices, headline formulas, ad assets, Shopping feeds, policy compliance
- `06-conversion-tracking-and-measurement.md` — Tracking setup, enhanced conversions, attribution, metrics, formulas, benchmarks
- `07-google-ads-api-and-automation.md` — API services, GAQL queries, scripts, integrations
- `08-landing-page-best-practices.md` — Message match, speed, mobile, CRO, trust signals

---

## Capabilities

### 1. Account Setup & Structure
- Navigate to ads.google.com via Claude in Chrome
- Create new Google Ads account or configure existing one
- Set up account-level settings (time zone, currency, auto-tagging)
- Link Google Analytics 4, Merchant Center, Google Business Profile
- Set up conversion tracking (Google Ads tag or GTM)
- Configure enhanced conversions

### 2. Campaign Creation
- **Search Campaigns**: Create with proper settings, keyword themes, RSAs, all ad assets
- **Performance Max**: Set up asset groups, audience signals, search themes, brand exclusions
- **Shopping**: Configure Merchant Center feed, Standard Shopping + PMax hybrid
- **Display**: Remarketing campaigns, prospecting campaigns
- **Video/YouTube**: TrueView, Bumper, Shorts, Demand Gen
- **Demand Gen**: Cross-channel visual advertising

### 3. Keyword Research & Strategy
- Use Google Keyword Planner for volume, competition, CPC estimates
- Build STAG (Single Theme Ad Group) structures
- Set up negative keyword lists (universal + industry-specific)
- Match type strategy aligned with bidding approach

### 4. Ad Copywriting
- Write RSAs with 15 headlines + 4 descriptions following best practices
- Mix headline types: benefit, question, urgency, social proof, CTA, feature, price
- Set up DKI, ad customizers, countdown timers
- Strategic pinning (minimal — only for brand/legal requirements)
- Write ad assets: sitelinks, callouts, structured snippets, promotions

### 5. Bidding Strategy Selection
- Recommend strategy based on conversion volume and business goals
- Configure tCPA, tROAS, Max Conversions, Max Conversion Value
- Set up portfolio bid strategies when appropriate
- Monitor learning periods — enforce no-change windows

### 6. Ongoing Optimization
- Weekly search term mining → add negatives + new keywords
- Ad copy testing (champion/challenger)
- Budget allocation by marginal CPA/ROAS
- Quality Score monitoring and improvement
- Device, geo, daypart bid adjustments
- PMax: asset group optimization, audience signal tuning, brand exclusions
- Impression share analysis (Lost IS Budget vs Rank)

### 7. Reporting & Analysis
- Pull campaign/ad group/keyword performance data
- Calculate KPIs: CPA, ROAS, CTR, conversion rate, impression share
- Period-over-period comparisons
- Segment analysis (device, location, time, audience)
- Competitive analysis via Auction Insights
- Wasted spend analysis

### 8. Account Audits
- Full account health audit against checklist
- Common mistakes identification and fixes
- Optimization Score review (apply good recommendations, dismiss bad ones)
- Conversion tracking audit
- Negative keyword coverage audit

---

## Workflow: Account Setup via Claude in Chrome

When setting up a Google Ads account:

### Step 1: Navigate to Google Ads
```
1. Open ads.google.com in Chrome
2. Sign in with the user's Google account
3. If new account: Follow account creation flow
4. If existing: Navigate to the correct account
```

### Step 2: Account Settings
```
1. Set time zone and currency (CANNOT be changed later)
2. Enable auto-tagging (Settings > Account settings)
3. Set up conversion tracking (Tools > Measurement > Conversions)
4. Link GA4 (Tools > Data manager > Linked accounts)
5. Link Merchant Center if e-commerce
```

### Step 3: Campaign Creation
```
1. Determine campaign type based on business goal
2. Set campaign settings:
   - Name (descriptive: "Search - [Product] - [Geo]")
   - Networks (Search only for Search campaigns — uncheck Search Partners initially)
   - Locations (target by presence, NOT presence or interest)
   - Languages
   - Bidding strategy (start Manual CPC or Max Clicks if <30 conv/month)
   - Daily budget
   - Ad schedule (if applicable)
3. Create ad groups (STAG structure: 5-15 themed keywords each)
4. Add keywords with appropriate match types
5. Create RSAs (15 headlines, 4 descriptions per ad group)
6. Add all relevant ad assets (sitelinks, callouts, structured snippets, etc.)
```

### Step 4: Negative Keywords
```
1. Create shared negative keyword list with universal negatives
2. Add industry-specific negatives
3. Apply lists to all campaigns
```

### Step 5: Conversion Tracking
```
1. Create conversion actions (Tools > Measurement > Conversions)
2. Set counting method (One for leads, Every for e-commerce)
3. Set conversion window (match sales cycle)
4. Set attribution model (Data-Driven recommended)
5. Install tracking tag via GTM or direct
6. Set up enhanced conversions if possible
```

---

## Workflow: Campaign Optimization (Ongoing)

### Weekly Routine
```
1. Pull search terms report → add negatives, identify new keywords
2. Check conversion tracking for drops/anomalies
3. Review budget pacing vs monthly target
4. Check for disapproved ads → fix or appeal
5. Review bidding strategy status (learning? limited?)
6. Check impression share metrics
```

### Monthly Routine
```
1. Quality Score trend analysis
2. Geographic performance review → adjust bids/exclusions
3. Device performance review → adjust bids
4. Ad copy performance → pause losers, create challengers
5. Audience performance review
6. PMax Insights tab review
```

### Quarterly Routine
```
1. Full negative keyword audit
2. Landing page performance review
3. Campaign structure review (consolidate or expand?)
4. Conversion tracking audit
5. Competitor analysis (Auction Insights)
6. Account settings review
```

---

## Decision Trees

### Which Campaign Type?
```
High purchase intent + text ads → Search
E-commerce + product feed → Shopping + PMax hybrid
Brand awareness + visual → Display or YouTube
Cross-channel reach → Performance Max
App installs → App campaigns
Visual engagement + Gmail/Discover → Demand Gen
```

### Which Bidding Strategy?
```
0-15 conversions/month → Manual CPC or Maximize Clicks
15-30 conversions/month → Enhanced CPC (transitional)
30+ conversions/month (lead gen) → tCPA or Max Conversions + tCPA
50+ conversions/month (e-commerce) → tROAS or Max Conversion Value + tROAS
Brand defense → Target Impression Share (95% abs top)
```

### When to Scale?
```
CPA/ROAS meeting target for 2-4 weeks → Yes
IS Lost to Budget >10% → Increase budget (max 20% at a time)
Exhausted high-intent demand → Expand keywords, match types, campaign types, geos
```

---

## Critical Rules

1. **ALWAYS separate brand from non-brand campaigns**
2. **NEVER auto-apply Google's recommendations** — review each manually
3. **NEVER change budget >20% in a single day** (disrupts learning)
4. **NEVER make changes during learning period** (7-14 days after strategy change)
5. **ALWAYS set up negative keywords from day one**
6. **ALWAYS use ad assets** (sitelinks, callouts, structured snippets minimum)
7. **Target by "presence" NOT "presence or interest"** for location targeting
8. **Supply your own video for PMax** — Google auto-generates bad ones
9. **Add brand exclusions to PMax** — prevent brand cannibalization
10. **Optimize for macro conversions** — only use micro as stepping stone when volume is too low

---

## Supplement/Health Product Specific Rules

Since Brooks runs Motilli, Lunessa, and health brands:

### Google Ads Compliance for Supplements
- CANNOT claim: cure, treat, prevent diseases
- CAN say: "Supports healthy [function]", "May help with [general wellness]"
- Include FDA disclaimer: "These statements have not been evaluated by the FDA..."
- Avoid: "cure", "heal", "treatment", "remedy"
- Structure/function claims acceptable with disclaimers
- Before/after images may need disclaimers
- May need LegitScript certification
- Weight loss claims heavily scrutinized — avoid superlatives

### Shopping Feed for Supplements
- Product titles: Brand + Product Type + Key Attributes (count, flavor, form)
- Include GTIN if available
- No health claims in product descriptions
- High-quality product images on white background
- Custom labels: by margin, by performance, by product line
