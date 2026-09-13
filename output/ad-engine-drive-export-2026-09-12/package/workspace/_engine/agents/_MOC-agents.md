# Agents — Map of Content

Your agent system orchestrates research, strategy, creative production, quality control, and visual design. Each agent has a defined role and interfaces with specific other agents in the pipeline.

---

## Agent System Overview

```
Market Analyst (Research & Discovery)
        ↓
  [Findings & Intel]
        ↓
Creative Strategist (Strategy & Briefs)
        ↓
  [Creative Brief: angle + concept + mechanism + avatar + product]
        ↓
  ┌──────────────────────────────────────────────────────┐
  │                 PRODUCTION PIPELINE                   │
  │                                                      │
  │  Hook Writer                                         │
  │    ├──→ Long-Form Copywriter ←→ Copy Chief (8.0)     │
  │    └──→ Video Ad Scriptwriter ←→ Copy Chief (8.0)    │
  │                                                      │
  │  Long-Form Copywriter ──→ Native Image Designer      │
  │                                                      │
  │  Branded Statics Designer (independent from briefs)  │
  │                                                      │
  └──────────────────────────────────────────────────────┘
        ↓
  [All output uploaded to Google Drive]
        ↓
Campaign Ops (Deployment & Testing)
```

```
CFO Agent (Financial Intelligence — Independent)
  ├── Wells Fargo (via Plaid)
  ├── American Express (via Plaid)
  └── Spending Reports / Subscription Cleanup
```

---

## Agent Roster

### 1. Market Analyst
**File:** [[agents/market-analyst/AGENT.md]]
**Role:** Upstream intelligence gathering — Reddit scraping, Meta Ad Library monitoring, competitor tracking, angle saturation mapping, mechanism discovery.
**Outputs:** Intel drops deposited in `/agents/market-analyst/intel-drops/`
**Feeds into:** Creative Strategist

### 2. Creative Strategist
**File:** [[agents/creative-strategist/AGENT.md]]
**Role:** Downstream creative strategy — transforms intelligence into creative briefs, selects angles/concepts/mechanisms, chooses formats, designs funnels.
**Outputs:** Creative briefs, format recommendations, testing strategies
**Feeds into:** Long-Form Copywriter, Video Ad Scriptwriter, Branded Statics Designer, Native Image Designer

### 3. Hook Writer
**File:** [[agents/hook-writer/AGENT.md]]
**Role:** Writes the first 1-5 lines of every ad — the hook. Both written (Facebook primary text) and spoken (video opening lines). 13 hook types, 2 loop types, 4 specificity layers, awareness-level mapping.
**Skill:** `/hook generation/hook-generation-v2/SKILL.md`
**References:** Hook swipe file in `/hook generation/references/`
**Receives from:** Creative Strategist (brief with avatar, awareness level, angle, desire)
**Sends to:** Long-Form Copywriter (written hooks), Video Ad Scriptwriter (spoken hooks)
**Uploads to:** Google Drive

### 4. Long-Form Copywriter
**File:** [[agents/long-form-copywriter/AGENT.md]]
**Role:** Writes long-form direct response copy — Facebook ads, mechanism-education copy, narrative-driven sales copy.
**Skill:** `/long form copy/skills/long-form-copy/long-form-copy-SKILL-UPDATED-v5.md`
**References:** 95+ real ads in `/long form copy/references/`
**Receives from:** Creative Strategist (brief), Hook Writer (written hooks)
**Sends to:** Copy Chief (for scoring), Native Image Designer (hook for image pairing)
**Uploads to:** Google Drive

### 5. Video Ad Scriptwriter
**File:** [[agents/video-ad-scriptwriter/AGENT.md]]
**Role:** Writes direct response video ad scripts — 30s, 60s, 90s, VSL for Facebook, Instagram, TikTok, YouTube.
**Skill:** `/video ads/skills/video-ad-scripts/` (skill file + deep structural analysis + swipe file)
**References:** 48 transcripts in `/video ads/references (transcripts)/` (29 myNuora + 19 Balmbare)
**Receives from:** Creative Strategist (brief)
**Sends to:** Copy Chief (for scoring)
**Uploads to:** Google Drive

### 6. Branded Statics Designer
**File:** [[agents/branded-statics-designer/AGENT.md]]
**Role:** Creates branded static ad images — polished ads with product shots, pricing, benefit callouts, comparison charts.
**Skill:** `/statics/branded-static-ads/SKILL.md`
**References:** Brand catalogs in `/statics/branded_statics/` (Neurosmile, AG1, Golo, Provitalize)
**Receives from:** Creative Strategist (brief, product context)
**Uploads to:** Google Drive

### 7. Native Image Designer
**File:** [[agents/native-image-designer/AGENT.md]]
**Role:** Creates native ad images — images that make ads look like personal Facebook posts. No product shots ever.
**Skill:** `/native images/skill/Native_Image_Copy_Congruence_Analysis.md`
**References:** Amala + Sculptique swipe indexes in `/native images/references/`
**Receives from:** Long-Form Copywriter (hook/first 3 lines for image-copy congruence)
**Uploads to:** Google Drive

### 8. Copy Chief
**File:** [[agents/copy-chief/AGENT.md]]
**Role:** Quality gate. Scores all copy across 7 dimensions on a strict 10-point scale. Copy scoring below 8.0 is sent back for rewrite.
**Skill:** `/long form copy/skills/copy-chief/SKILL.md`
**Receives from:** Long-Form Copywriter, Video Ad Scriptwriter
**Sends back to:** The originating copywriter agent (with scorecard + weakness report) if score < 8.0
**Uploads to:** Google Drive

### 9. CFO
**File:** [[agents/cfo/AGENT.md]]
**Role:** Financial intelligence — connects to bank accounts via Plaid, pulls transactions, detects recurring subscriptions, generates spending reports, surfaces cleanup opportunities.
**Tools:** `plaid_server.py` (bank linking), `pull_transactions.py` (transaction analysis)
**Connected Accounts:** Wells Fargo, American Express
**Independent:** Does not feed into or receive from the creative pipeline

---

## How Agents Work Together

### The Quality Loop: Copywriter ↔ Copy Chief

```
Copywriter writes draft
        ↓
Copy Chief scores it (7 dimensions, 125-point raw → 10-point scale)
        ↓
Score ≥ 8.0? → APPROVED → Upload to Google Drive
Score < 8.0? → REWRITE → Back to Copywriter with weakness report
        ↓
Copywriter fixes identified weaknesses
        ↓
Re-submit to Copy Chief
        ↓
Repeat until 8.0+ achieved
```

This loop applies to both the Long-Form Copywriter and the Video Ad Scriptwriter.

### The Image-Copy Pair: Copywriter → Native Image Designer

The Native Image Designer cannot work independently — it needs the copy's hook to determine the image. The locked pair:

1. Long-Form Copywriter produces copy with a hook
2. The hook's first 1-3 lines determine the image congruence category
3. Native Image Designer creates an image that matches the hook
4. Image + copy deploy together as a paired unit

### The Branded Statics Flow

Branded Statics Designer can work independently from the copywriters because branded statics contain their own on-image copy. The flow:

1. Creative Strategist provides brief (product, avatar, angle)
2. Branded Statics Designer selects archetypes and executes
3. Output goes directly to Google Drive

### Cross-Agent Information Flow

| FROM | TO | WHAT |
|---|---|---|
| Market Analyst | Creative Strategist | Intel drops, angle saturation maps, mechanism discoveries |
| Creative Strategist | Hook Writer | Brief with avatar, awareness level, angle, desire, product |
| Hook Writer | Long-Form Copywriter | Written hooks with mechanical breakdowns |
| Hook Writer | Video Ad Scriptwriter | Spoken hooks with performance notes |
| Creative Strategist | Branded Statics Designer | Brief with product, avatar, angle |
| Long-Form Copywriter | Copy Chief | Finished copy (hook + body) for scoring |
| Video Ad Scriptwriter | Copy Chief | Finished scripts for scoring |
| Copy Chief | Copywriter/Scriptwriter | Scorecard + weakness report (if < 8.0) |
| Long-Form Copywriter | Native Image Designer | Hook/first 3 lines for image pairing |
| All Production Agents | Google Drive | All completed work |

---

## Starting a Production Session

### For Long-Form Copy
1. Creative Strategist provides brief (avatar, awareness level, angle, desire, product)
2. **Hook Writer** generates a batch of written hooks (5-10 hooks)
3. Best hook is selected and passed to Long-Form Copywriter
4. Long-Form Copywriter continues the hook's voice and writes the full copy
5. Copy Chief scores the complete piece (hook + body)
6. If < 8.0, Copywriter rewrites; if ≥ 8.0, approved
7. Native Image Designer creates paired image based on the hook
8. All output uploads to Google Drive

### For Video Scripts
1. Creative Strategist provides brief
2. **Hook Writer** generates a batch of spoken hooks (5-10 hooks)
3. Best hook is selected and passed to Video Ad Scriptwriter
4. Video Ad Scriptwriter builds the full script from the hook forward
5. Copy Chief scores the complete script
6. If < 8.0, Scriptwriter rewrites; if ≥ 8.0, approved
7. Upload to Google Drive

### For Branded Statics
1. Creative Strategist provides brief
2. Branded Statics Designer selects archetypes and executes
3. Upload to Google Drive

### For Native Images
1. Long-Form Copywriter provides approved copy with hook
2. Native Image Designer selects congruence category and creates image
3. Upload to Google Drive

---

## Google Drive Output

All agents upload their completed work to Google Drive for team access. Output types:
- Long-form copy (.md files)
- Video ad scripts (.md files)
- Branded static image briefs + generated images
- Native image briefs + generated images
- Copy Chief assessment scorecards

---

*Last updated: 2026-03-26*
