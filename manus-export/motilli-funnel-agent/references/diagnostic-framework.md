# Motilli Funnel Diagnostic Framework

Full detail for Phases 3-7 of the funnel analysis: page classification, funnel architecture types, the five-layer diagnosis with thresholds, the five congruence dimensions, the report template, and the bottleneck-to-fix routing table.

## Landing Page Classification

| Page Type | Identifying Features |
|-----------|---------------------|
| **Listicle** | Numbered list of reasons/benefits, "X Reasons Why...", benefit stacking, social proof items |
| **Advertorial** | Long-form editorial, authority voice, mechanism education, investigation/exposé framing |
| **Product Page** | Product images, pricing, add-to-cart, reviews, product description |
| **Direct Sales Page** | Advertorial + checkout combined on one page |
| **Bridge Page** | Short intermediate page between ad and final destination |

## Funnel Architecture Types

Classify each discovered path as one of:

- Long-Form Copy → Advertorial → Product Page
- Long-Form Copy → Listicle → Product Page
- Video Ad → Advertorial → Product Page
- Video Ad → Listicle → Product Page
- Video Ad → Video Advertorial → Product Page
- Three-Stage (Ad → Advertorial → Listicle → Product Page)
- Hybrid/Other

## The Five-Layer Diagnosis

**Layer 1 — Delivery (CPM).** Only assess if the user supplied ad-platform data (CPM, spend, time window, audience type). General DTC health/wellness cold-traffic CPM range is $15-$40 — label this explicitly as a general range, not a threshold. If no data was supplied, flag as `MISSING` and state exactly what's needed.

**Layer 2 — Thumb-stop (creative quality).** This layer can be assessed from the ad creative alone, no metrics needed:
- Does the hook stop the scroll? Quote the first 1-3 lines.
- Is the hook specific to the avatar's actual wound (GLP-1 side effects), not generic digestive-health language?
- Does it use insider language ("sulfur burps," "concrete," "brick in stomach," "shot sisters," etc.)?
- What awareness level does the hook target — problem-aware, solution-aware, or product-aware?
- Does the body copy build enough curiosity to earn the click? Is the upstream-vs-downstream mechanism explained clearly? Is the CTA clear about what the reader will find?
- If CTR data was supplied: general ranges are 0.8%-2.5% for long-form copy ads, 0.5%-1.5% for video. Cross-reference against the creative-quality read — does the CTR match what you'd expect from the ad's quality?

**Layer 3 — Click-to-page (landing page view rate).** Only assess with supplied data: 90%+ is healthy; 80-90% warrants a check on mobile load time; 70-80% signals a real technical issue; below 70% is critical and should halt creative analysis until fixed. If no data, flag `MISSING` and note that the user should check landing-page-views ÷ link-clicks; if it's meaningfully below ~85%, investigate page load speed before diagnosing creative.

**Layer 4 — On-page (congruence + page quality).** This is the core value of the audit — you have both the ad copy and the landing page copy, so run full congruence analysis on every ad-to-page transition. Score the five dimensions below.

**Layer 5 — Checkout (add-to-cart-to-purchase).** Only assess with supplied data: 60%+ healthy, 40-60% normal DTC range, 20-40% signals friction or price resistance, below 20% signals a significant checkout problem. Without data, flag `MISSING` but still note anything obviously wrong visible on the product page itself (no trust badges, confusing pricing, missing guarantee, etc.).

## The Five Congruence Dimensions (Layer 4 detail)

### 1. Angle Continuity
The angle is the specific emotional wound the ad used. Quote the ad's opening wound and the page's opening wound. Verdict: CONGRUENT (same wound, same vantage point) or BREAK (different wound, or a clinical reframing of an emotional entry).

**Motilli-specific:** the ad should enter through GLP-1 side effects specifically; if the page enters through generic "digestive health," that's a break.

### 2. Mechanism Continuity
What mechanism did the ad teach (upstream prokinetic vs. downstream, celery extract/apigenin, motility)? Does the page CONFIRM and ESCALATE it (roughly 15-20% confirmation, 80-85% new value = congruent), ECHO it at the same depth (echo problem), teach a different mechanism (break), or skip it entirely (break)?

**Motilli-specific:** the upstream-vs-downstream distinction is Motilli's core mechanism. If the ad teaches it and the landing page re-teaches it from scratch instead of confirming and escalating, that's an echo problem.

### 3. Emotional Temperature Match
Classify the ad's exit temperature and the page's opening temperature as one of: warm/vulnerable (peer narrative, hope, personal), analytical calm (data, research), righteous frustration (anger, villain-naming), desperate urgency, or cautious curiosity. Verdict: CONGRUENT or MISMATCH.

**Motilli-specific risk:** a warm/personal ad ("I finally found something that works") flowing into a clinical "EXPOSED: The GLP-1 Cover-Up" advertorial is a temperature break — emotional ads flow more naturally into listicles than clinical advertorials for this avatar.

### 4. Credibility Source Continuity
Classify the ad's credibility source (peer narrative, authority, clinical data, social proof, investigative) and the page's.

- **Natural escalations that work:** peer-narrative ad → authority advertorial; peer-narrative ad → peer listicle with social-proof stacking; authority ad → clinical advertorial.
- **Risky downgrades:** authority ad → peer confessional page; clinical ad → emotional narrative page; peer-narrative ad → pure clinical page with no narrative (loses the identification anchor).

### 5. Promise-Delivery Alignment
Quote what the ad's CTA/closing lines promised the reader would find, and check whether the page delivers that within the first scroll. Verdict: DELIVERED / DELAYED (delivers eventually but after too much preamble) / BROKEN (never delivers).

**Motilli-specific:** if the ad promises "discover the real reason your [symptom] won't stop," the page must reveal or confirm that reason in the first scroll, not after 500 words of authority-building.

### Additional page-quality checks (independent of congruence)
While assessing page quality, also check for: presence of a sticky/persistent CTA (its absence is often the #1 conversion killer), guarantee length and consistency across funnel stages, whether the product is introduced at the right point for the traffic temperature, whether the mechanism explanation disqualifies competing approaches, and whether social proof is layered across at least three different types (reviews, before/after, expert endorsement, etc.).

## Report Template

```
============================================================
MOTILLI FUNNEL ANALYSIS REPORT
Date: [today's date]
Ads Library Search: [search term used]
Active Ads Found: [N]
Unique Funnel Paths: [N]
============================================================

FUNNEL MAP
──────────
[Visual representation of ALL discovered funnel paths]

Path A: [Ad type] → [Page type] → [Page type] → Checkout
  Used by: Ads [list]

Path B: [Ad type] → [Page type] → Checkout
  Used by: Ads [list]

============================================================

ADS INVENTORY
─────────────
[For each ad:]

AD [N] — [Format: Video/Image/Long-form]
  Hook: "[first 1-3 lines, quoted exactly]"
  Angle: [specific wound/entry point]
  Mechanism taught: [Y/N, what level]
  Destination: [URL]
  Emotional temperature at exit: [warm/analytical/frustrated/urgent/curious]
  Credibility source: [peer/authority/clinical/social proof]
  Funnel path: [A/B/C]

============================================================

FUNNEL PATH ANALYSIS
────────────────────
[For each unique funnel path:]

PATH [X]: [Full path visualization]

  DATA SUMMARY (if metrics provided):
    Layer 1 — Delivery: CPM $[X] — [status]
    Layer 2 — Thumb-Stop: CTR [X]% — [status]
    Layer 3 — Click-to-Page: LP View Rate [X]% — [status]
    Layer 4 — On-Page: Conversion Rate [X]% — [status]
    Layer 5 — Checkout: ATC-to-Purchase [X]% — [status]

  CONGRUENCE REPORT — [Transition: e.g., "Ad → Listicle"]:

    1. Angle Continuity: [CONGRUENT / BREAK]
       Evidence: "[quote from ad]" → "[quote from page]"
       Assessment: [explanation]

    2. Mechanism Continuity: [CONGRUENT / ECHO / BREAK]
       Evidence: "[quote from ad]" → "[quote from page]"
       Assessment: [explanation]

    3. Emotional Temperature: [CONGRUENT / MISMATCH]
       Evidence: Ad exits at [temperature]. Page opens at [temperature].
       Assessment: [explanation]

    4. Credibility Source: [CONGRUENT / ESCALATION / DOWNGRADE]
       Evidence: Ad uses [source]. Page uses [source].
       Assessment: [explanation]

    5. Promise-Delivery: [DELIVERED / DELAYED / BROKEN]
       Evidence: Ad promises "[quote]". Page delivers [what/when].
       Assessment: [explanation]

    Congruence Verdict: [Summary]

  [If multi-stage funnel, repeat congruence report for each transition]

  PAGE QUALITY NOTES:
    [Any issues with the page itself, independent of congruence]
    [CTA clarity, pricing reveal, social proof quality, etc.]

============================================================

COPY ASSESSMENTS (if Phase 6 triggered)
────────────────────────────────────────
[For each flagged ad:]

AD [N] — COPY ASSESSMENT RESULTS:
  [Scores, specific weaknesses with line citations]

============================================================

PRIMARY BOTTLENECK
──────────────────
[The single most impactful issue — identified by evidence, not opinion]
[Why this is the bottleneck — cite specific evidence]

ROOT CAUSE ANALYSIS
───────────────────
[If creative: cite specific lines/elements]
[If congruence: cite the dimension(s) that break and exactly where]
[If technical: identify what the data pattern suggests]
[If offer/pricing: explain what the checkout data reveals]

============================================================

SECONDARY OBSERVATIONS
──────────────────────
[Other issues found, clearly labeled as secondary]
[Frame as "worth investigating once primary bottleneck is resolved"]

============================================================

PRIORITY FIXES (ordered by impact)
───────────────────────────────────
1. [Most impactful fix] — Fix type: [hook rewrite / body rewrite / page rebuild / etc.]
   Why: [how this addresses the root cause]

2. [Second priority] — Fix type: [...]
   Why: [rationale]

3. [Third priority] — Fix type: [...]
   Why: [rationale]

============================================================

DATA GAPS
─────────
[What the user needs to provide from the ad platform for full diagnosis]

Missing metrics:
- [ ] CPM by ad set
- [ ] Link CTR (not "all clicks" CTR)
- [ ] CPC
- [ ] Landing page view rate
- [ ] On-page conversion rate (LP views to clicks/ATCs)
- [ ] ATC-to-purchase rate
- [ ] Spend and time window per ad
- [ ] Audience type (cold/lookalike/retargeting)

Note: Provide these from the ad platform to unlock full quantitative diagnosis.
The current analysis is creative-only (ad quality + congruence + funnel architecture).

============================================================

RECOMMENDED NEXT ACTIONS
─────────────────────────
[For each fix, specify the type of work needed:]

| Fix | Fix Type | Why |
|-----|----------|-----|
| [description] | Hook rewrite | [Hook isn't stopping scroll] |
| [description] | Long-form body rewrite | [Body copy needs rebuild] |
| [description] | Advertorial rebuild | [Page needs congruent rewrite] |
| [description] | Listicle rebuild | [Listicle needs alignment] |
| [description] | Deep copy scoring | [Need deeper copy scoring] |
| [description] | Video script rework | [Video script needs work] |

============================================================
```

## Bottleneck-to-Fix Routing Reference

| Bottleneck found | Root cause | What kind of fix to route to |
|---|---|---|
| Ad creative, weak hook | Hook doesn't stop the scroll | Hook rewrite pass |
| Ad creative, weak body | Copy isn't building curiosity | Long-form body rewrite / video script rewrite |
| Ad creative, overall quality | Multiple copy issues | Deep copy scoring first, then a rewrite |
| Landing page, low quality | Weak copy, mechanism, or proof | Advertorial or listicle rebuild |
| Landing page, congruence break | Ad-to-page disconnect | Rebuild the page using the upstream ad as the anchor |
| Landing page, design/build | Layout/UX issues | Page redesign/build pass |
| Checkout, low purchase rate | Offer, pricing, or trust issue | Offer/UX changes (not a copy issue) |
| Technical, low LP view rate | Page load or redirect issue | Technical fix (not a copy issue) |

## CRO Cross-Reference

When auditing landing pages and funnel pages, cross-reference against empirical CRO laws derived from studying 30+ winning direct-response funnels across 10+ brands (300+ winning ads total). When page quality issues surface in Layer 4:

1. Check for sticky CTA presence — its absence is often the #1 conversion killer.
2. Check guarantee length and consistency across funnel stages.
3. Check product introduction timing versus traffic temperature.
4. Check whether the mechanism explanation disqualifies competing approaches.
5. Check social proof layering — minimum 3 distinct types (reviews, before/after, expert endorsement, etc.).
