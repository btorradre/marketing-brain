# Metric Context — General DTC Performance Ranges

**CRITICAL: These are general ranges, not thresholds.** They exist to give you a starting point when the user hasn't provided their own historical benchmarks. The user's specific vertical, offer price, audience temperature, and AOV will shift all of these — sometimes dramatically. Always prefer the user's own historical data when available. When using these ranges, explicitly label them as general and note the caveats.

These ranges are derived from common DTC direct response patterns. They are not gospel. They are not benchmarks. They are context.

---

## How to Use These Ranges

1. **The user provides their own benchmarks:** Ignore these ranges entirely. Their data is more relevant than any general range.
2. **The user provides no benchmarks:** Use these as a loose frame. Flag whether a metric is clearly outside the range, clearly within it, or ambiguous. For ambiguous cases, do NOT declare a problem — ask for historical comparison data.
3. **The user is in an unusual vertical:** Note that these ranges may not apply and ask if they have vertical-specific benchmarks.

---

## Ad Layer Metrics

### CPM (Cost Per 1,000 Impressions)

CPM varies enormously by audience, placement, time of year, and vertical. These are rough US Facebook/Instagram ranges for DTC health/wellness (the most common vertical for this skill's users):

| Audience Type | Typical Range | Notes |
|---|---|---|
| Broad / interest-based cold | $15–$40 | Wide range. Q4 holiday season pushes higher |
| Lookalike (1-3%) | $18–$45 | Usually slightly higher than broad due to narrower pool |
| Retargeting (site visitors) | $25–$60 | Higher CPM is expected — smaller, warmer audience |
| Retargeting (engaged) | $30–$70 | Highest CPMs, but should come with highest CTR |

**Context factors that shift CPM:**
- Q4 (Oct-Dec) can be 1.5-2x normal due to advertiser competition
- Health/wellness tends to run higher than fashion/apparel
- High-engagement creative lowers CPM over time (Meta rewards engagement)
- New ad accounts or new campaigns often see higher CPMs initially

**When CPM signals a problem:** CPM alone is rarely the bottleneck. It becomes a problem when it's high AND CTR is low — meaning Meta is paying a premium to show the ad to people who don't care. Or when CPM is trending sharply upward with stable spend — indicating audience saturation.

### CTR (Link Click-Through Rate)

**Important: always confirm the user is reporting LINK CTR, not "all clicks" CTR.** "All clicks" includes profile clicks, reactions, comments, and shares — it inflates the number and doesn't measure actual intent to visit the landing page.

| Creative Type | General Range | Notes |
|---|---|---|
| Long-form copy (text-heavy) | 0.8%–2.5% | Higher end for strong hooks with compelling copy |
| Video ad | 0.5%–1.5% | Lower CTR is normal — viewers watch instead of clicking |
| Image ad | 1.0%–3.0% | Tends to have highest CTR because there's less to engage with on-platform |

**Context factors:**
- Video ads naturally have lower CTR because the ad itself delivers value (the video) without requiring a click. For video ads, also look at ThruPlay rate and video completion rate as engagement signals alongside CTR.
- Retargeting audiences typically have higher CTR (they already know you) but the pool is smaller.
- CTR above 3% on cold traffic is exceptional. CTR below 0.5% on cold traffic with a long-form copy ad is a red flag.

**When CTR signals a problem:** Low CTR with reasonable CPM = the ad isn't compelling. The hook isn't stopping the scroll, or the body isn't building enough curiosity to click. High CTR with terrible downstream conversion = the ad is clickbaity — it drives curiosity clicks but the landing page can't capitalize because the click motivation doesn't match the page content.

### CPC (Cost Per Link Click)

CPC is a derivative metric (CPM ÷ CTR × 10). It's useful as a summary but diagnosing with CPC alone can be misleading — a high CPC could mean high CPM (audience issue) OR low CTR (creative issue) OR both.

| Vertical | General Range |
|---|---|
| Health/wellness supplements | $0.50–$2.50 |
| Physical devices ($100+) | $1.00–$4.00 |
| Low-price impulse offers (<$30) | $0.30–$1.50 |
| High-ticket ($200+) | $2.00–$6.00 |

Always decompose CPC into CPM and CTR for diagnosis. CPC by itself doesn't tell you WHERE the problem is.

---

## Page Layer Metrics

### Landing Page View Rate

This measures what percentage of link clicks actually resulted in the landing page loading.

| Range | Interpretation |
|---|---|
| 90%+ | Normal. Pipes are working |
| 80-90% | Slight loss. Check mobile load time |
| 70-80% | Significant loss. Likely a technical issue — slow load, redirect chain, or rendering problem |
| Below 70% | Critical. Something is broken technically. Do not diagnose creative until this is fixed |

### On-Page Conversion Rate

This varies dramatically by what "conversion" means on the page:

| Conversion Type | General Range | Notes |
|---|---|---|
| Advertorial → product page click-through | 15%–40% | Based on LP views, not link clicks |
| Listicle → product page click-through | 20%–45% | Listicles tend to convert slightly higher because they're more product-forward |
| Lead capture (email/phone) | 10%–30% | Depends heavily on what you're asking for and what you're offering |
| Direct ATC from landing page | 3%–10% | Rare configuration but some funnels skip the product page |

**Context factors:**
- Warm traffic (retargeting) converts at 1.5-3x the rate of cold traffic on the same page
- Higher price points have lower conversion rates
- Pages with video tend to have higher engagement but not necessarily higher conversion
- Mobile vs. desktop split matters — most DTC traffic is 70-85% mobile

### Time on Page / Scroll Depth (When Available)

These are secondary metrics but they're useful for distinguishing between "the reader arrived and immediately bounced" vs. "the reader engaged with the page but still didn't convert."

- High time on page + low conversion = the reader is engaging but not being moved to act. The content is interesting but not persuasive enough, or the CTA is weak/buried.
- Low time on page + low conversion = the reader bounced early. Either the page opening didn't hook them, or there's a congruence break at the ad-to-page transition (they expected something different from what they found).
- High scroll depth + low conversion = similar to high time on page. They read most of it but something didn't close them. Look at the CTA placement, the close, and the pricing reveal.

---

## Checkout Layer Metrics

### ATC-to-Purchase Rate

| Range | Interpretation |
|---|---|
| 60%+ | Strong. Checkout flow is working well |
| 40-60% | Normal range for DTC |
| 20-40% | Some friction or price resistance. Check for shipping cost surprise, trust issues, or UX problems |
| Below 20% | Significant problem. Something is breaking at checkout — could be price shock, lack of trust signals, or technical issue |

### CPA (Cost Per Acquisition)

CPA is the final scorecard, not a diagnostic metric. A high CPA tells you the funnel isn't working efficiently, but it doesn't tell you WHERE it's breaking. That's what the layer-by-layer analysis is for.

CPA targets are entirely dependent on the business model (margin, LTV, break-even point) and should come from the user, not from general ranges.

---

## Spend and Statistical Significance

This is not a statistics course, but a few practical guidelines:

- **Under $100 total spend:** The data is almost certainly noise. Do not diagnose from this. Tell the user they need more data.
- **$100–$500 total spend:** You can start to see patterns, but individual metrics will be volatile. Flag that the data is early and conclusions are directional, not definitive.
- **$500–$2,000 total spend:** Enough data for a reasonable read on CPM, CTR, and CPC. Landing page conversion may still be volatile if the page is getting fewer than 200 visitors.
- **$2,000+ total spend:** You can diagnose with reasonable confidence across all layers, assuming the spend is concentrated enough (not spread across 50 ad variations at $40 each).

**The practical rule:** You need roughly 200+ events at any given funnel stage to read that stage's conversion rate with useful confidence. If the landing page got 50 visitors and 2 converted, that 4% conversion rate could easily be 1% or 8% with more data. Note the sample size when it's small.
