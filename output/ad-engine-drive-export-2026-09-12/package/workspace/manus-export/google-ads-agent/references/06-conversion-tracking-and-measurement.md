# Google Ads Conversion Tracking & Measurement

## Conversion Tracking Setup

### Methods
1. **Google Ads tag (gtag.js)**: Direct implementation on site
2. **Google Tag Manager**: Preferred for flexibility
3. **GA4 Import**: Import GA4 key events into Google Ads

### Critical Setup Details
- Conversion window: Match to sales cycle (default 30 days; B2B may need 60-90)
- Counting: "One" for leads, "Every" for e-commerce
- Set conversion value (static for leads, dynamic for e-commerce)
- Best practice: Google Ads native tracking for Smart Bidding, GA4 for cross-channel analysis

### Conversion Actions vs Goals
- **Actions**: Individual tracked events (purchase, form fill, call)
- **Goals**: Groups of related actions. Set "account-default" (used for bidding) vs "observe only"
- Keep 1-2 primary default conversion actions per campaign — too many confuses bidding

---

## Enhanced Conversions
- Sends hashed first-party data (email, phone, name, address) to Google
- Recovers 5-15% of conversions lost to cookie restrictions
- Improves automated bidding accuracy
- Required for long-term measurement as cookies phase out
- Setup: GTM, Google Ads tag, or API

---

## Offline Conversion Imports
- For conversions happening offline (phone closes, in-store, sales team deals)
- Process: Click generates GCLID → store in CRM → upload GCLID + conversion data when lead converts
- Import regularly (daily or weekly), include conversion value
- Alternative: Enhanced Conversions for Leads (matches on hashed user data)
- **Game-changing for lead gen**: Without this, Google optimizes for form fills. With it, Google optimizes for actual revenue.

---

## Attribution Models

### Data-Driven Attribution (DDA) — RECOMMENDED DEFAULT
- ML assigns fractional credit based on observed contribution to conversion
- Considers: number of interactions, order, device, time between, creative, click type
- Smart Bidding optimized to work with DDA

### Other Models
- **Last Click**: 100% to final click. Simple but undervalues upper funnel
- **First Click**: 100% to first interaction. Good for understanding discovery
- **Linear/Time Decay/Position-Based**: Being deprecated. Use DDA.

---

## Key Metrics & KPIs

### Core Performance
| Metric | Formula | Benchmark |
|---|---|---|
| CTR | Clicks / Impressions | Search: 3-6%, Display: 0.4-0.6% |
| CPC | Cost / Clicks | Varies by industry ($1-$9+) |
| Conversion Rate | Conversions / Clicks | Search: 3-5%, Display: 0.5-1% |
| CPA | Cost / Conversions | Industry-dependent |
| ROAS | Conv Value / Cost | Must exceed break-even |

### Impression Share
| Metric | What It Means |
|---|---|
| Search IS | % of eligible impressions received |
| IS Lost (Budget) | Missed due to budget — increase budget or narrow targeting |
| IS Lost (Rank) | Missed due to low Ad Rank — improve bids/QS/extensions |
| Top IS | % shown above organic results |
| Abs Top IS | % shown in position 1 |

### Quality Score (1-10)
- Expected CTR (39%), Landing Page Experience (39%), Ad Relevance (22%)
- Each: Below Average / Average / Above Average

### Video Metrics
- View Rate: Views / Impressions
- Avg Watch Time / % Watched (quartile: 25/50/75/100%)
- Earned Actions: free post-view actions (subscribes, channel visits)

---

## Key Formulas

### Break-Even ROAS
```
Break-Even ROAS = 1 / Profit Margin
```
- 50% margin → 2.0x ROAS needed
- 25% margin → 4.0x ROAS needed
- 70% margin → 1.43x ROAS needed

### Target CPA from Unit Economics
```
Target CPA = AOV x Profit Margin x Acceptable Efficiency
```
- E-commerce: $100 AOV, $60 profit, retain 50% → Target CPA = $30
- Lead gen: $5K deal, 10% close rate → $500/lead value, 30% to acquisition → Target CPA = $150

### LTV:CAC Benchmarks
- 3:1 = healthy
- Below 1:1 = unsustainable
- Above 5:1 = may be underinvesting in acquisition

---

## Reporting Best Practices

### Key Segments
- Time (hour, day, week, month)
- Device (mobile, desktop, tablet)
- Network (Search vs Partners)
- Conversion Action (by type)
- Click Type (which ad element clicked)
- Audience Segment

### Competitive Analysis
- **Auction Insights**: Your IS vs competitors, overlap rate, position above rate, outranking share
- **Ad Preview Tool**: Check ad appearance without inflating impressions
- **Transparency Center**: See any advertiser's active ads

### GA4 Integration
- Link GA4 → Google Ads for audience sharing and conversion import
- GA4 audiences (behavioral) can be pushed to Google Ads
- Use GA4 for cross-channel attribution, Google Ads native tracking for bidding
- Predictive audiences (likely to purchase/churn) shareable

---

## Advanced Measurement

### Brand Lift Studies
- YouTube/Video campaigns with sufficient spend ($10K-$50K+)
- Surveys control vs test group on awareness, recall, consideration, intent
- Accessed: Measurement > Lift Measurement

### Store Visit Tracking
- Tracks ad viewers who later visit physical stores
- Requires Google Business Profile, multiple locations, sufficient volume

### Incrementality Testing
- Measures true incremental lift (conversions that wouldn't happen without ads)
- Geo-based experiments: pause ads in regions, compare to running regions
- Critical for validating brand search spend

### Consent Mode v2
- Required in EU/EEA for GDPR/DMA compliance
- Sends cookieless pings when users decline cookies
- Google models missing conversions from non-consenting users
