# The Feedback Loop — Market Analyst ↔ Creative Strategist

> **Purpose:** This document defines how intelligence flows between the Market Analyst and Creative Strategist, and critically, how creative performance data flows BACK to the Market Analyst to refine future intelligence gathering. Without this loop, the system is one-directional and degrades over time.

---

## The Core Loop

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   MARKET ANALYST                    CREATIVE STRATEGIST         │
│                                                                 │
│   ┌──────────────┐                 ┌──────────────────┐        │
│   │ Reddit Scrape │──── intel ────→│ Creative Brief    │        │
│   │ Competitor Mon│    drops       │ Hook + Copy       │        │
│   │ Angle Mapping │                │ Video Script      │        │
│   │ Mechanism Cat │                │ Advertorial       │        │
│   └──────┬───────┘                 └────────┬─────────┘        │
│          │                                   │                  │
│          │         FEEDBACK LOOP             │                  │
│          │                                   │                  │
│          │    ┌──────────────────────┐        │                  │
│          │◄───│  Performance Intel   │◄───────┘                  │
│          │    │  • Which angles won  │                           │
│          │    │  • Which hooks died  │                           │
│          │    │  • Score data        │                           │
│          │    │  • Metric signals    │                           │
│          │    └──────────────────────┘                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Forward Flow (Analyst → Strategist)

This is the standard intelligence delivery. The Market Analyst deposits structured notes into `/agents/market-analyst/intel-drops/` using the [[agents/market-analyst/templates/intel-drop-template|Intel Drop Template]].

**What flows forward:**
- Avatar language (exact phrases from Reddit, forums, reviews)
- Angle saturation assessments (which angles are overused, which are open)
- Competitor ad intelligence (new winning ads, mechanism shifts, spend signals)
- Market sophistication updates (stage shifts, new mechanism wars)
- Blue ocean opportunities (flagged as `#urgent-creative-opportunity`)
- New mechanism discoveries (novel cause-and-effect chains spotted in the wild)

**Cadence:**
- Daily: Quick competitor monitoring notes (15-30 min)
- Weekly: Full synthesis note with avatar language, angle map updates, and recommended angles
- Monthly: Market sophistication assessment + competitor profile updates
- Ad hoc: Urgent opportunity flags (new angle spotted, competitor vulnerability identified)

---

## Phase 2: Creative Production (Strategist Output)

The Creative Strategist consumes intel and produces creative using the [[agents/creative-strategist/SOPs/creative-sprint|Creative Sprint SOP]]. Every finished piece includes mandatory frontmatter:

```yaml
---
format: [long-form | video-script | advertorial | listicle | hook | static | native-image]
angle: "The specific emotional wound"
concept: "Who tells the story, how, at what temperature"
mechanism: "The cause-and-effect chain in plain language"
hook_type: [symptom-sniper | failed-solution | contrarian | authority-disruption | statistic-shock | behavior-mirror | identity-confession]
villain_types: [structurally-incapable | fake-industry | outdated-system]
product_integration_position: [1-5]
awareness_level: [unaware | problem-aware | solution-aware | product-aware | most-aware]
sophistication_stage: [1-5]
word_count:
copy_chief_score:
date:
status: [draft | production | scaling | paused | killed]
intel_source: "Link to the intel-drop that informed this piece"
---
```

The `intel_source` field is critical — it traces every piece of creative back to the intelligence that spawned it.

---

## Phase 3: The Feedback Loop (Performance → Analyst)

This is where the system becomes self-improving. After creative goes live and generates performance data, that data flows BACK to the Market Analyst.

### 3.1 Performance Signal Categories

**Hook Performance:**
| Signal | Metric | What It Tells the Analyst |
|--------|--------|--------------------------|
| Hook killed | CTR < 1.0% | This angle/hook type doesn't resonate with this avatar |
| Hook moderate | CTR 1.0-2.0% | Angle has potential but execution needs refinement |
| Hook strong | CTR 2.0-3.5% | Angle resonates — mine this territory deeper |
| Hook exceptional | CTR > 3.5% | Blue ocean confirmed — prioritize adjacent angles |

**Body/Mechanism Performance:**
| Signal | Metric | What It Tells the Analyst |
|--------|--------|--------------------------|
| Body fails | Good CTR + High bounce | Mechanism education isn't landing — research deeper |
| Body moderate | Good CTR + Moderate time on page | Mechanism partially resonates — refine the chain |
| Body strong | Good CTR + High time on page + CTA clicks | Mechanism education is working — catalog this chain |

**Funnel Performance:**
| Signal | Metric | What It Tells the Analyst |
|--------|--------|--------------------------|
| Handoff breaks | High CTR + Low LP conversion | Ad-to-page congruence issue — check continuity |
| Full funnel works | Strong metrics end to end | Entire angle/mechanism/concept combo is validated |
| Offer issue | High ATC + Low purchase | Not a creative problem — pricing/shipping/guarantee |

### 3.2 Performance Intel Note Format

When performance data comes in, the Creative Strategist (or media buyer) creates a Performance Intel note in `/agents/market-analyst/intel-drops/` with this structure:

```yaml
---
type: performance-feedback
date: YYYY-MM-DD
creative_ref: "[[path/to/finished-creative]]"
format: [long-form | video-script | advertorial | listicle]
angle: "The angle used"
mechanism: "The mechanism used"
hook_type: "The hook type used"
tags:
  - performance-feedback
  - [angle-validated | angle-killed | mechanism-validated | mechanism-weak | hook-validated | hook-killed]
---
```

**Sections:**

#### Performance Summary
- CTR:
- Outbound CTR:
- CPC:
- Hook Rate (video):
- Hold Rate (video):
- LP Bounce Rate:
- Time on Page:
- CTA Click Rate:
- Add to Cart:
- Purchase Rate:
- Overall CVR:
- Spend:
- Days running:

#### What Worked
- Which angle resonated and why (based on metrics)
- Which hook type performed and at what awareness level
- Which mechanism language got engagement

#### What Failed
- Where the funnel broke (using diagnostic patterns from [[funnel analysis/funnel-analysis/SKILL|Funnel Analysis]])
- Which beliefs weren't shifting (based on where users dropped)

#### Implications for Market Analyst
- Should this angle be mined deeper? (Y/N + reasoning)
- Should this mechanism chain be cataloged as validated? (Y/N)
- Should this hook type be prioritized for this avatar? (Y/N)
- Are there saturation signals? (Is this angle starting to fatigue?)
- New avatar language discovered from comments/engagement?

---

## Phase 4: Analyst Integrates Feedback

The Market Analyst processes performance feedback and updates its core intelligence:

### 4.1 Angle Saturation Map Updates
When performance data comes in:
- **Angle validated (CTR > 2.0%, CVR > 2.5%)** → Mark angle as "proven" in saturation map, note remaining runway
- **Angle killed (CTR < 1.0% across 3+ attempts)** → Mark angle as "exhausted" or "misaligned," investigate why
- **Angle moderate (mixed signals)** → Flag for concept variation testing (same angle, different narrator/posture)

### 4.2 Mechanism Library Updates
- **Mechanism validated** → Add to [[fundamentals/Mechanism Reference Library_ Top 100 Examples|Mechanism Reference Library]] with performance data
- **Mechanism weak** → Note which step in the cause-and-effect chain lost the reader, investigate if a simpler chain exists
- **Novel mechanism discovered through testing** → Full catalog entry with coherence + resonance scores

### 4.3 Avatar Intelligence Updates
- **New language from ad comments** → Feed into avatar research (exact phrases from high-engagement ads)
- **Awareness level confirmed** → Update Schwartz assessment for this niche
- **Hook type validated** → Update hook taxonomy with performance data for this avatar

### 4.4 Competitor Intelligence Cross-Reference
- **Our angle wins where competitor's doesn't** → Document the differentiation
- **Competitor's angle wins where ours doesn't** → Analyze what they're doing differently in mechanism education
- **Market shift detected** → Update sophistication stage assessment

---

## Phase 5: The Synthesis Cycle

Every **two weeks**, the Market Analyst produces a Feedback Synthesis Note that aggregates all performance feedback into strategic recommendations:

### Bi-Weekly Synthesis Template

```yaml
---
type: feedback-synthesis
date: YYYY-MM-DD
period: "YYYY-MM-DD to YYYY-MM-DD"
tags:
  - synthesis
  - feedback-loop
---
```

#### Period Performance Overview
- Total pieces launched:
- Pieces still running:
- Pieces killed:
- Average Copy Chief score of launched pieces:
- Best performer (link + metrics):
- Worst performer (link + metrics):

#### Angle Performance Map
| Angle | Pieces Tested | Best CTR | Best CVR | Status |
|-------|--------------|----------|----------|--------|
| [angle] | X | X.X% | X.X% | Validated / Moderate / Killed |

#### Mechanism Performance Map
| Mechanism Chain | Pieces Using It | Avg CTR | Avg CVR | Status |
|----------------|----------------|---------|---------|--------|
| [mechanism] | X | X.X% | X.X% | Validated / Needs Refinement / Killed |

#### Hook Type Performance
| Hook Type | Uses | Avg CTR | Best Performer | Status |
|-----------|------|---------|----------------|--------|
| [type] | X | X.X% | [[link]] | Hot / Stable / Cooling |

#### Strategic Recommendations
1. **Double down on:** [angles/mechanisms/hooks that are working]
2. **Test variations of:** [moderate performers that need concept refinement]
3. **Kill or pause:** [angles/mechanisms that have been tested 3+ times without success]
4. **Blue ocean to explore:** [new angles surfaced from performance patterns]
5. **Avatar insight update:** [new language/beliefs discovered through engagement data]

#### Updated Priorities for Next Sprint
- Priority 1: [most promising angle + recommended format]
- Priority 2: [second most promising]
- Priority 3: [exploratory/testing]

---

## Feedback Loop Rules

### Rule 1: No Creative Without Intel
The Creative Strategist should never write a piece without referencing at least one Market Analyst intel drop. The `intel_source` field in creative frontmatter enforces this.

### Rule 2: No Intel Without Performance Context
After the first month of operation, the Market Analyst should reference performance data when assessing angles. "This angle is open" means nothing if we've tested it three times and it failed.

### Rule 3: Kill Fast, Mine Deep
- If an angle fails 3 times across different concepts → kill it, document why
- If an angle succeeds once → mine it with 3-5 concept variations before moving on

### Rule 4: Mechanism Chains Are Assets
Every validated mechanism chain (cause-and-effect that converts) gets cataloged with its performance data. These are reusable across products in similar niches.

### Rule 5: The Loop Never Stops
Even when a campaign is performing well, the Market Analyst continues monitoring for:
- Competitor response (are they copying our angle?)
- Saturation signals (is our own angle fatiguing?)
- Market shifts (is the sophistication stage advancing?)
- New avatar language (are customer conversations evolving?)

---

## File Locations

| Component | Location |
|-----------|----------|
| Intel drops (Analyst → Strategist) | `/agents/market-analyst/intel-drops/` |
| Performance feedback (Strategist → Analyst) | `/agents/market-analyst/intel-drops/` (tagged `#performance-feedback`) |
| Finished creative | `/agents/creative-strategist/output/` |
| Feedback synthesis notes | `/agents/market-analyst/intel-drops/` (tagged `#synthesis`) |
| Angle saturation map | [[fundamentals/angle-saturation-map]] |
| Mechanism library | [[fundamentals/Mechanism Reference Library_ Top 100 Examples]] |
| Funnel diagnostics | [[funnel analysis/funnel-analysis/SKILL]] |

---

## Quick Start: Activating the Loop

**Week 1:** Market Analyst delivers first intel drops. Creative Strategist produces first batch.
**Week 2:** First creative goes live. Begin collecting performance data.
**Week 3:** First performance feedback notes filed. Market Analyst integrates.
**Week 4:** First bi-weekly synthesis. Loop is active.
**Month 2+:** Loop is self-improving. Each cycle produces better intel, better creative, and faster kills on losing angles.

---

*The feedback loop is what turns a collection of skills into an engine. Without it, you're guessing. With it, every dollar of ad spend teaches you something that makes the next dollar more efficient.*
