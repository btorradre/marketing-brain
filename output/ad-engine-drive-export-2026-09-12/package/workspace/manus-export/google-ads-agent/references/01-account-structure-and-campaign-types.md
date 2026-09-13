# Google Ads Account Structure & Campaign Types

## Account Hierarchy

**Account > Campaign > Ad Group > Ads/Keywords**

### Account Level
- Unique Customer ID (xxx-xxx-xxxx format)
- Settings: time zone (immutable after creation), currency, auto-tagging, tracking templates, linked accounts
- Each account has its own billing

### MCC (Manager Accounts)
- Umbrella account sitting above individual Google Ads accounts
- Single sign-in for all client/sub accounts
- Cross-account reporting, consolidated billing
- Shared resources: negative keyword lists, remarketing lists, conversion actions
- Can nest sub-MCCs by geo, business line, or client type
- MCC scripts automate cross-account tasks

### Campaign Level
- Budget, bidding strategy, targeting settings
- Campaign types determine ad formats and placements
- Organize by: business goal, product line, geography, or budget allocation

### Ad Group Level
- Contains ads + keywords grouped by theme
- Default max CPC bid, audience targeting
- Best practice: tightly themed keyword clusters (STAGs)

---

## Campaign Types

### Search Campaigns
- Text ads on Google Search results
- RSAs (Responsive Search Ads) — up to 15 headlines, 4 descriptions
- Keyword-based targeting with match types
- Best for: high purchase intent, leads, sales
- **AI Max for Search (2025)**: Campaign toggle using Gemini AI for expanded matching, auto-generated text, dynamic landing pages. Average 14% conversion lift at similar CPA

### Performance Max (PMax)
- AI-driven across ALL Google channels (Search, Display, YouTube, Gmail, Discover, Maps)
- Asset Groups: up to 15 headlines, 5 descriptions, 20 images, 5 videos per group
- Audience Signals: directional hints (not hard restrictions)
- Search Themes: indicate queries your customers use
- 62% of all Google ad clicks (Feb 2026)
- For e-commerce: 74-97% of PMax spend goes to Shopping/feed-based ads
- Run hybrid: PMax for scale + Standard Shopping for margin control
- Brand exclusions critical to prevent brand cannibalization

### Shopping Campaigns
- Product listing ads from Google Merchant Center feed
- Standard Shopping: granular control over bids and product segmentation
- PMax for Shopping: AI-driven, all channels
- Feed quality is the #1 lever

### Display Campaigns
- Banner/visual ads across Google Display Network (millions of sites + YouTube + Gmail)
- Responsive Display Ads auto-adjust to fit placements
- Targeting: contextual (keywords, topics, placements), audience-based, demographic
- Best for: brand awareness, remarketing

### Video Campaigns (YouTube)
- **Skippable In-Stream (TrueView)**: Skip after 5s, pay at 30s or interaction
- **Non-Skippable**: 15-30s, CPM billing
- **Bumper Ads**: 6s max, non-skippable, Target CPM
- **In-Feed**: Thumbnail + text, user clicks to watch
- **YouTube Shorts**: Vertical 9:16, between organic Shorts, 70B+ daily views

### Demand Gen Campaigns
- Replaced Discovery Ads + Video Action Campaigns
- Placements: YouTube (Shorts, in-stream, in-feed, Home), Gmail, Discover, Maps
- Formats: short-form video, images (square, portrait, carousels), text
- Bidding: Max Conversions, Max Conversion Value, Max Clicks
- New metric: Attributed Branded Searches

### App Campaigns
- Fully automated across Search, YouTube, Display, Play Store, Discover
- Subtypes: App Installs (tCPI), App Engagement (tCPA), Pre-Registration
- Budget minimum: 50x target CPI for installs

### Local (Now PMax)
- Standalone Local Campaigns deprecated (July 2022), migrated to PMax
- Options: PMax for Store Goals, Search with Location Intent, Local Services Ads (pay per lead)

---

## Account Structure Best Practices (2026)

- **Consolidation over fragmentation**: Fewer, larger campaigns with themed ad groups
- Google's AI needs sufficient data per campaign/ad group to learn
- Clear conversion signals matter more than granular structure
- Separate brand from non-brand campaigns (non-negotiable)
- Separate campaigns for fundamentally different goals/budgets
- Each campaign needs enough budget for 30+ conversions/month for Smart Bidding
