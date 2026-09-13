# Skill: Market Pain Point & Opportunity Research

**Description:** This skill enables the agent to systematically discover, extract, classify, and rank the most acute pain points and white-space opportunities within a target client segment—then assess each for AI-agent solvability. It encodes a repeatable research protocol that transforms unstructured public signals (complaints, reviews, job postings, forum rants, competitor gaps) into a prioritized opportunity map an operator can act on immediately. The purpose is to answer one question with high confidence: *"Where would a purpose-built AI agent create the most asymmetric value for this segment?"*

---

## Objective

Given a **target industry, client persona, or problem domain**, produce a ranked shortlist of the 5–10 highest-leverage opportunities where a focused AI agent can:

1. Solve a problem clients currently endure repeatedly.
2. Outperform or replace an existing solution that is overpriced, fragile, or poorly automated.
3. Address a gap no current product meaningfully covers.

The deliverable is an actionable opportunity brief—not a market report. Every finding must link back to raw evidence and pass a solvability filter.

---

## Research Sources

Scrape and mine the following sources **in priority order**. Each source is ranked by signal density—how reliably it surfaces genuine, unfiltered pain.

| Priority | Source | Why It Matters |
|----------|--------|---------------|
| 1 | **Reddit** (industry & role subreddits) | Unfiltered, first-person complaints with upvote-validated severity. Search for rant threads, "what tool do you wish existed" posts, and workflow frustration threads. |
| 2 | **G2 / Capterra / TrustRadius reviews** (1–3 star) | Structured negative reviews from paying customers. The "Cons" and "What do you dislike?" fields are gold. Filter by recency (<18 months). |
| 3 | **Support forums & community boards** (Zendesk communities, Discourse instances, Stack Overflow for dev tools) | Recurring unanswered or poorly-answered questions reveal product gaps. Thread length and repeat posters signal severity. |
| 4 | **Job postings** (LinkedIn, Indeed, Glassdoor) | When companies hire full-time humans to do a task, that task is a candidate for agent automation. Look for repetitive role descriptions and high-volume postings for the same title. |
| 5 | **Twitter/X and LinkedIn posts** | Real-time frustration signals. Search for complaint patterns, "I can't believe I still have to manually…" posts, and viral threads about broken workflows. |
| 6 | **App Store / Chrome Web Store reviews** (1–2 star) | End-user pain with existing tools. Look for patterns across multiple competing apps—shared complaints indicate structural market gaps. |
| 7 | **Competitor landing pages & changelogs** | What competitors promise but fail to deliver (check reviews against claims). What they explicitly mark as "coming soon" or "enterprise only" reveals unserved demand. |
| 8 | **Industry analyst reports & newsletters** (Gartner, Forrester, CB Insights, niche Substacks) | Macro trends, TAM signals, and named pain points at the segment level. Use for validation, not discovery. |
| 9 | **YouTube comments on tutorial/review videos** | Users watching tutorials are struggling. Comments reveal what steps break, what's confusing, and what people wish the tool did differently. |
| 10 | **Hacker News** | Technical audience with high signal for dev-tools, infra, and B2B SaaS pain points. "Ask HN" and "Show HN" comment threads are especially useful. |

### Source-Specific Search Patterns

```
Reddit:       "[segment] frustrating" OR "I hate [tool]" OR "wish there was" OR "anyone else struggle with"
G2/Capterra:  Filter: 1-3 stars, sort by recent, read "Cons" field
Job boards:   "[repetitive task keyword]" + high posting volume + low seniority
Twitter/X:    "[tool/process] is broken" OR "manual" OR "waste of time" OR "why is there no"
HN:           "Ask HN: how do you handle [process]" OR complaints in Show HN threads
```

---

## Data Extraction Protocol

### Step 1: Breadth Scan
- For each source, run 3–5 keyword queries derived from the target segment.
- Collect the first 30–50 relevant results per source.
- Log: source URL, date, verbatim quote, upvotes/reactions (if available).

### Step 2: Signal Filtering
Apply these filters to separate signal from noise:

**High-signal indicators (keep):**
- Emotional language: "nightmare," "hours wasted," "can't believe," "finally gave up"
- Specificity: names a concrete task, workflow step, or tool failure
- Social proof: high upvotes, "same here" replies, multiple independent reports
- Recency: posted within the last 18 months
- Role-specificity: complaint comes from the target persona, not a bystander

**Low-signal indicators (discard or deprioritize):**
- Vague dissatisfaction: "it's okay but could be better"
- One-off edge cases with no corroboration
- Complaints about price alone (without workflow pain)
- Feature requests that are nice-to-haves, not blockers
- Posts from competitors or affiliates (check post history)

### Step 3: Pattern Clustering
- Group filtered signals by **underlying problem**, not by source or surface-level keyword.
- A pain point is valid when it appears **independently across 2+ sources** or **3+ times within one high-signal source**.
- Name each cluster with a concise problem statement: *"[Persona] struggles to [task] because [root cause]."*

### Step 4: Root Cause Extraction
For each cluster, determine:
- **What** the user is trying to accomplish (the job-to-be-done).
- **Why** it's painful (manual steps, tool limitations, data silos, knowledge gaps).
- **What** they currently do about it (workarounds, duct-tape solutions, or nothing).
- **How often** it occurs (daily, weekly, per-project, per-client).

---

## Pain Point Classification Framework

Classify every validated pain point on these five dimensions:

| Dimension | Scale | Definition |
|-----------|-------|------------|
| **Severity** | 1–5 | 1 = mild annoyance → 5 = causes revenue loss, churn, or compliance risk |
| **Frequency** | 1–5 | 1 = rare/quarterly → 5 = daily or continuous |
| **Addressability** | 1–5 | 1 = requires deep domain expertise or regulatory change → 5 = clearly automatable with current AI capabilities |
| **Competition Density** | 1–5 (inverted) | 1 = crowded market with strong incumbents → 5 = no credible solution exists |
| **Monetization Signal** | 1–5 | 1 = users expect it free → 5 = users already pay for inferior alternatives or hire humans to do it |

**Composite Priority Score** = (Severity × 2) + (Frequency × 2) + (Addressability × 1.5) + (Competition Density × 1.5) + (Monetization Signal × 1)

Maximum possible score: **42.5**

### Classification Tags

Also tag each pain point with:
- `workflow-bottleneck` | `data-gap` | `tool-fragmentation` | `knowledge-access` | `compliance-burden` | `communication-overhead` | `manual-repetition`
- `B2B` | `B2C` | `internal-ops`
- `quick-win` (solvable in <4 weeks) | `strategic` (requires deeper build)

---

## Opportunity Scoring Criteria

For each pain point that scores ≥ 28 on the composite priority score, elevate it to an **Opportunity Card** and evaluate against these criteria:

| Criterion | Weight | What to Assess |
|-----------|--------|---------------|
| **Market Size Signal** | 20% | How many people/companies experience this? Use job posting volume, subreddit size, review count as proxies. |
| **Willingness to Pay** | 25% | Are users already spending money (tools, consultants, hires) to solve this? What's the current cost of the workaround? |
| **Existing Solution Gap** | 20% | Do current tools cover this? If so, where do they fail? (Look at the 1–3 star reviews of the closest competitor.) |
| **Agent Solvability** | 25% | Can an AI agent realistically handle this with current LLM + tool-use capabilities? Consider: structured vs. unstructured input, need for real-time data, human-in-the-loop requirements, integration complexity. |
| **Speed to Value** | 10% | How quickly can a first version deliver noticeable ROI? Prefer problems where a "good enough" agent beats the status quo immediately. |

**Opportunity Score** = weighted average across all criteria, each rated 1–10.

Threshold: Only include opportunities scoring **≥ 6.5** in the final deliverable.

---

## Output Format

The agent must produce a structured deliverable with the following sections:

### 1. Executive Summary (3–5 sentences)
- Target segment analyzed.
- Number of sources scraped and signals processed.
- Top 3 opportunities in one sentence each.

### 2. Pain Point Registry

For each validated pain point:

```markdown
### PP-[001]: [Concise Problem Statement]

**Summary:** [2-3 sentence description]
**Persona:** [Who feels this pain]
**Frequency:** [How often it occurs]
**Current Workaround:** [What they do today]
**Evidence:**
  - [Source 1]: "[verbatim quote]" (upvotes/reactions, date)
  - [Source 2]: "[verbatim quote]" (upvotes/reactions, date)
  - [Source 3]: "[verbatim quote]" (upvotes/reactions, date)
**Classification:** Severity=[X] | Frequency=[X] | Addressability=[X] | Competition=[X] | Monetization=[X]
**Composite Score:** [X/42.5]
**Tags:** [tags]
```

### 3. Opportunity Cards (Top 5–10)

For each qualifying opportunity:

```markdown
### OPP-[001]: [Opportunity Name]

**Derived from:** PP-[XXX], PP-[XXX]
**The Problem:** [1-2 sentences]
**Why Now:** [What makes this timely—new AI capability, market shift, regulatory change]
**Agent Concept:** [2-3 sentence sketch of what the agent would do]
**Target User:** [Specific role/persona]
**Revenue Model Signal:** [How users currently spend to solve this]
**Existing Alternatives:** [Name competitors + their key weakness]
**Opportunity Score:** [X/10]
  - Market Size: [X/10]
  - Willingness to Pay: [X/10]
  - Solution Gap: [X/10]
  - Agent Solvability: [X/10]
  - Speed to Value: [X/10]
```

### 4. Ranked Shortlist

A table ranking all opportunity cards by score:

```markdown
| Rank | ID       | Opportunity Name      | Score | Top Tag           | Recommendation     |
|------|----------|-----------------------|-------|-------------------|--------------------|
| 1    | OPP-001  | [Name]                | 8.7   | manual-repetition | Build immediately  |
| 2    | OPP-002  | [Name]                | 7.9   | tool-fragmentation| Validate with users|
| ...  | ...      | ...                   | ...   | ...               | ...                |
```

### 5. Research Confidence Notes
- Sources that yielded thin data (flag for follow-up).
- Assumptions made where evidence was indirect.
- Segments or sub-problems that warrant deeper investigation.

---

## Constraints & Guardrails

### Avoid
- **Vanity metrics**: subreddit subscriber counts, app download numbers, or follower counts as proof of pain. These indicate awareness, not suffering.
- **Solutions looking for problems**: Do not start with an agent capability and work backward to justify it. Start with the pain.
- **Single-source conclusions**: No pain point makes it into the registry without cross-source validation or 3+ independent reports from one high-signal source.
- **Stale data**: Exclude signals older than 24 months unless the problem is demonstrably ongoing.
- **Astroturfing & marketing content**: Discard signals from accounts that appear to be competitors, affiliates, or promotional.

### Handle Thin Data
- If fewer than 3 validated pain points emerge for a segment, flag the segment as **under-researched** and recommend alternative angles or adjacent segments to explore.
- If a pain point has strong severity but low frequency evidence, tag it as `needs-validation` and include it in the appendix, not the main shortlist.

### Flag Uncertainty
- Mark any opportunity where agent solvability depends on capabilities not yet proven in production (e.g., multi-step reasoning over live databases, real-time voice interaction) with a `⚠ capability-risk` flag.
- Mark any opportunity where monetization signal relies on inference rather than direct evidence with a `⚠ revenue-assumption` flag.

---

## Skill Activation Trigger

This skill activates when the agent receives input matching any of these patterns:

```
"Research pain points for [segment/industry/persona]"
"Find agent opportunities in [domain]"
"What are the biggest problems for [role/persona]?"
"Where should we build an agent for [market]?"
"Analyze [segment] for automation opportunities"
```

### Required Input
- **Target segment**: An industry (e.g., "real estate"), client persona (e.g., "e-commerce operations managers"), or problem domain (e.g., "invoice processing").

### Optional Input
- **Geographic focus**: Default is US/English-language sources.
- **Depth level**: `scan` (breadth-first, 1–2 hours of research) | `deep-dive` (exhaustive, 4–8 hours). Default is `scan`.
- **Exclusions**: Specific competitors, sub-segments, or pain categories to skip.

### Example Activation

```
User: "Research pain points for independent insurance agencies"

Agent activates: market-pain-point-research
Target segment: independent insurance agencies
Depth: scan (default)
Geographic focus: US (default)
```

---

## Appendix: Quick-Reference Checklists

### Before Starting Research
- [ ] Confirm target segment is specific enough (not "healthcare" → "outpatient physical therapy clinics")
- [ ] Identify 3–5 subreddits and 2–3 review platforms relevant to the segment
- [ ] Set date filters on all sources to the last 18 months

### Before Finalizing Output
- [ ] Every pain point has ≥ 2 source citations
- [ ] Every opportunity card has a plausible agent concept, not just a problem description
- [ ] Composite scores are calculated consistently
- [ ] No opportunity relies solely on assumed willingness to pay
- [ ] Confidence notes section is populated honestly
- [ ] Output follows the exact format specified above
