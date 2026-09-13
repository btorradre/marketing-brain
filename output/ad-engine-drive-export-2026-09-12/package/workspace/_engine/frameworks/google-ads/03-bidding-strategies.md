# Google Ads Bidding Strategies

## Strategy Overview

### Manual CPC
- Full control over keyword-level bids
- Use for: new accounts with <15-30 conversions/month, testing phases, tight cost control
- Drawback: can't react to real-time auction signals
- Use as stepping stone → gather 30-50 conversions → migrate to automated

### Enhanced CPC (eCPC)
- Hybrid: manual bids adjusted up/down by Google based on conversion likelihood
- No upward adjustment cap
- Use for: transitioning from Manual to full automation (15-30 conversions/month)
- Being phased out from some campaign types

### Target CPA (tCPA)
- "Get conversions at ~$X cost per acquisition"
- Uses 100s of real-time signals per auction
- **Requirements**: 30+ conversions/month (Google says 15, but 30+ is better)
- **Setting the target**: Start at historical CPA or slightly above. Never >20% below historical initially. Adjust 10-15% at a time, 2 weeks between changes
- **Gotchas**: Too aggressive target = volume cliff. Not a per-conversion guarantee. Conversion delays confuse algorithm

### Target ROAS (tROAS)
- "For every $1 spent, return $X in conversion value"
- Expressed as percentage (400% = $4 return per $1)
- **Requirements**: 50+ conversions/month with value data
- **Setting**: Start at historical ROAS or slightly below. Adjust 10-20% increments
- **Gotchas**: Requires accurate conversion value tracking. Sensitive to value fluctuations

### Maximize Conversions
- "Spend full budget, get maximum conversions"
- **Critical**: WILL spend entire daily budget regardless of CPA
- No CPA guardrail unless you add tCPA target
- Use for: fixed budget + max volume, promotional pushes, bootstrapping data
- **Best practice**: Always pair with tCPA target unless you want uncapped spend

### Maximize Conversion Value
- Optimizes for total conversion value, not volume
- Use over Max Conversions when: variable order values, value-based bidding needed
- Pair with tROAS target for value-constrained optimization

### Maximize Clicks
- Get most clicks within budget, no conversion optimization
- Use for: brand awareness, data gathering, no conversion tracking yet
- Set max CPC limit to prevent overpaying
- Not recommended for performance campaigns

### Target Impression Share
- Show ads X% of the time in position Y (anywhere, top, absolute top)
- Use for: brand defense (95% absolute top), competitive conquesting, awareness
- Always set max CPC cap
- Not a performance strategy

---

## Portfolio vs Campaign-Level Strategies

### Portfolio Bid Strategies
- Single strategy across multiple campaigns
- Pools conversion data → more signal for algorithm
- Use when: campaigns target similar audiences with same CPA/ROAS goal, individual campaigns have <30 conversions/month

### When NOT to Use Portfolio
- Campaigns with different goals/targets
- When one campaign's data would contaminate another's

---

## Strategy Progression

1. **Manual CPC / Max Clicks** (0-15 conv/month): Gather data
2. **Enhanced CPC** (15-30 conv/month): Partial automation
3. **tCPA / Max Conv + tCPA** (30+ conv/month): Full automation for lead gen
4. **tROAS / Max Value + tROAS** (50+ conv/month): Value-based bidding

---

## Learning Period Management

### Triggers
- Changing bid strategy type
- Changing the target (CPA/ROAS)
- Budget changes >20% in single day
- Changing conversion actions
- Pausing/reactivating campaigns

### Rules
1. Make one change at a time
2. Do NOT adjust anything for 7-14 days after change
3. Allow 2-3 conversion cycles before evaluating
4. If CPA spikes during learning, do NOT panic-reduce target (worsens problem)
5. Build a change log to track changes vs performance

### Switching Safely
- Use campaign experiments (50/50 split) for 2-4 weeks
- Compare performance, apply winner
- Never switch strategy AND change budget simultaneously
