# Google Ads Campaign Optimization

## Search Term Mining

### Adding Negatives
1. Review search terms report weekly (minimum)
2. Identify irrelevant, informational, competitor queries
3. Add negatives at ad group or campaign level
4. Use shared negative keyword lists for account-wide exclusions

### Finding New Keywords
1. Mine search terms report for high-converting queries not in keyword list
2. Add as exact/phrase match for control
3. Expand using Keyword Planner around winning themes

---

## Ad Copy Testing

### Champion/Challenger Method
1. Run 2-3 RSAs per ad group
2. Identify champion (best by conversion rate, not CTR alone)
3. Create challenger testing ONE variable
4. Run 2-4 weeks or until statistical significance
5. Winner = new champion. Create new challenger.

### Test Priority (highest impact first)
1. Offer/value proposition
2. CTA
3. Headline messaging angle
4. Social proof/trust signals
5. Urgency/scarcity

---

## Budget Optimization

### Principles
- Allocate by marginal CPA/ROAS, not historical spend
- Fund impression-share-limited campaigns before creating new ones
- "Lost IS (Budget)" >10% = campaign needs more budget
- Kill campaigns with consistently poor CPA/ROAS after sufficient data

### Budget Allocation Framework
1. Rank campaigns by CPA (lowest→highest) or ROAS (highest→lowest)
2. Fund best performers to full capacity first
3. Allocate remaining down the list
4. Cut/pause campaigns below profitability threshold

### Budget Change Rules
- Never change >20% in a single day (disrupts learning)
- Use shared budgets cautiously
- Google can spend up to 2x daily budget on any day (averages over 30 days)

---

## Dayparting (Ad Scheduling)
- B2B: Often best during business hours (Mon-Fri 8am-6pm)
- Ecommerce: Usually 24/7 with bid adjustments by conversion patterns
- With automated bidding, Google already factors time of day — dayparting less critical but useful for budget control
- Run 2-4 weeks with no schedule first to gather baseline data

---

## Device Bid Adjustments
- B2B: Desktop typically converts better (-20% to -50% on mobile)
- Ecommerce: Mobile traffic high but conversion rate often lower
- Local/services: Mobile often converts well (click-to-call)
- With tCPA/tROAS: Device adjustments largely ignored. Exception: -100% to fully exclude a device

---

## Geographic Bid Adjustments
- Analyze by state, city, DMA, radius
- Increase bids in high-performing geos, decrease/exclude low performers
- Target by "presence" NOT "presence or interest"
- Review geo reports monthly

---

## Campaign Experiments
- Test: bid strategy changes, landing page variants, audience targeting changes
- Create draft → make one change → launch as experiment (50/50 split)
- Run minimum 2 weeks (ideally 4)
- Test ONE variable at a time
- Don't run during seasonal peaks unless testing that specifically

---

## Performance Max Optimization

### Asset Group Structure
- Separate by product/service category OR by audience type
- Each needs: 5+ headlines, 5+ long headlines, 5+ descriptions, 5+ landscape images, 5+ square images, 1+ video (supply your own — Google auto-generates bad ones)
- Distinct final URLs per asset group
- Don't overlap audience signals across asset groups in same campaign

### Audience Signals
- Suggestions, not hard targeting — Google will go beyond them
- Layer strongest signals first: customer lists, high-intent custom segments
- Monitor Audiences insights to see where Google is actually serving

### Search Themes
- Add 10-25 per asset group
- Include top-performing keywords, category terms, competitor terms

### URL Expansion
- Default: PMax can send traffic to ANY page on your site
- Use URL exclusion rules to block unwanted pages
- Or turn off entirely and specify final URLs manually
- Check Landing Pages report to see where PMax sends traffic

### Brand Exclusions — CRITICAL
- PMax will spend budget on brand traffic (easy conversions)
- Add brand exclusions → force PMax to focus on incremental non-brand traffic
- Run separate branded Search campaign with Target Impression Share

### Cannibalization Management
- Search exact match takes priority over PMax for identical keywords
- For broad/unmatched queries, PMax can win the auction
- Monitor Search campaign impression share — drops after PMax launch = cannibalization
- Use Search for high-intent exact/phrase, let PMax handle long tail + upper funnel

---

## Scaling Strategies

### When to Scale
- CPA/ROAS meeting target consistently for 2-4 weeks
- IS lost to budget >10%
- New keyword/audience opportunities identified

### How to Scale Safely
1. Increase budget by max 20% at a time
2. Wait 7-14 days between increases
3. Monitor CPA/ROAS closely after each increase
4. At some point: diminishing returns (CPA rises as high-intent demand exhausts)

### Scaling Beyond the Ceiling
- Expand keyword themes
- Expand match types (phrase→broad with tCPA)
- Add new campaign types (PMax, Display, YouTube)
- Expand to new geographies
- Move up funnel with awareness campaigns

### Expansion Order
1. Search (brand + non-brand) — foundation
2. Performance Max — cross-channel + long-tail
3. YouTube/Demand Gen — upper funnel with conversion optimization
4. Display (remarketing first, then prospecting)

---

## Account Health Checklist

### Weekly
- Search terms → add negatives
- Conversion tracking (drops/anomalies?)
- Budget pacing (on track for monthly target?)
- Disapproved ads
- Bidding strategy status (learning? limited?)

### Monthly
- Quality Score trends
- Geographic performance
- Device performance
- Ad copy performance (pause losers, create challengers)
- Audience performance
- Impression share metrics
- PMax Insights tab

### Quarterly
- Full negative keyword audit
- Landing page performance review
- Campaign structure review (consolidate/expand?)
- Conversion tracking audit
- Competitor analysis (Auction Insights)
- Account-level settings review

---

## Common Mistakes

1. Too many campaigns with insufficient budget → consolidate
2. Optimizing for micro conversions when macro data exists → switch to macro
3. Changing bid strategies too frequently → pick one, run 2-4 weeks
4. No negative keywords → set up standard negatives from day one
5. Ignoring Quality Score → fix landing pages and ad relevance
6. Not using ad extensions → use all that apply (free CTR boost)
7. Only one ad per ad group → run 2-3 RSAs
8. Set and forget → weekly optimization minimum
9. Not splitting brand/non-brand → always separate
10. Broad match + manual CPC → only use broad with tCPA/tROAS
