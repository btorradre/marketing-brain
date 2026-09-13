# AI Creative Strategist Agent System

## Overview

This directory contains the complete operating system for the AI Creative Strategist agent. The Creative Strategist's job is downstream creative output—transforming strategic briefs and market intelligence into production-ready marketing creative across all formats.

**Total documentation:** 4,132 lines of production-ready content

---

## File Structure

```
/agents/creative-strategist/
├── AGENT.md                          [279 lines] — Agent identity document & system prompt
├── SOPs/                             [2,320 lines total]
│   ├── creative-sprint.md            [752 lines] — Master SOP for production sprints
│   ├── brief-creation.md             [516 lines] — SOP for creating creative briefs
│   ├── format-selection-guide.md     [601 lines] — Decision tree for format selection
│   ├── self-assessment.md            [725 lines] — Copy Chief grading framework
│   └── funnel-congruence-check.md    [526 lines] — Multi-piece funnel auditing
├── templates/                        [733 lines total]
│   ├── creative-brief-template.md    [429 lines] — Frontmatter-rich brief template
│   └── finished-creative-template.md [304 lines] — Frontmatter-rich filing template
└── README.md                         [This file]
```

---

## Quick Start

### For the Creative Strategist (You)

**1. Read the Agent Identity Document**
- Start with [[AGENT.md]]
- Understand your role, responsibilities, and decision-making framework
- Review the context loading checklist and workflow

**2. Choose Your Task**
- **Producing a sprint of creative?** → [[SOPs/creative-sprint.md]]
- **Writing a creative brief?** → [[SOPs/brief-creation.md]]
- **Unsure which format to write?** → [[SOPs/format-selection-guide.md]]
- **Grading your creative?** → [[SOPs/self-assessment.md]]
- **Writing multi-piece funnels?** → [[SOPs/funnel-congruence-check.md]]

**3. Use the Templates**
- **Starting a brief?** → Copy [[templates/creative-brief-template.md]]
- **Filing finished creative?** → Copy [[templates/finished-creative-template.md]]

**4. Reference the Master Operating System**
- [[DR-SOP-Obsidian.md]] — Your constitution. Schwartz stages, belief shifts, villain architecture, product integration spectrum, hook engineering, funnel architecture, assessment framework, anti-mimicry system, forbidden patterns

### For Campaign Ops (Consumer of Your Work)

**Finding Production-Ready Creative:**
- Navigate to `/output/` folder
- Filter by product, format, score
- Copy files scoring 6.5+ for immediate deployment
- Review the Creative Brief (referenced in frontmatter) for strategic context

**Understanding a Creative Piece:**
- Read the finished creative's frontmatter for quick reference
- Click the brief link in frontmatter to understand strategic intent
- Review Copy Chief notes for execution insights

**Reusing or Revising Creative:**
- All creative is filed with full YAML frontmatter
- Vault search by angle, mechanism, villain, awareness level, format
- Avoid duplicating angles — check anti-mimicry audit in frontmatter

---

## Core Workflows

### Workflow 1: Creative Sprint (6-8 hours → 5-10 production-ready ads)

```
1. Read AGENT.md (5 min refresh)
2. Follow creative-sprint.md (complete pre-production checklist)
3. Create briefs using creative-brief-template.md
4. Produce creative following format-specific guidance
5. Self-assess using self-assessment.md
6. Check funnel congruence using funnel-congruence-check.md
7. File with finished-creative-template.md
```

### Workflow 2: Single Creative Piece (2-3 hours → 1 production-ready ad)

```
1. Review AGENT.md (context loading checklist)
2. Identify angle/format using format-selection-guide.md
3. Create brief using creative-brief-template.md
4. Produce creative following relevant skill file
5. Self-assess using self-assessment.md
6. File with finished-creative-template.md
```

### Workflow 3: Multi-Piece Funnel (8-12 hours → 2-4 coordinated pieces)

```
1. Complete full AGENT.md context load
2. Use creative-sprint.md for batch production strategy
3. Create separate briefs for each funnel piece
4. Produce in sequence (lead → bridge → product page)
5. After each piece: Self-assess and continue
6. Before filing: Run funnel-congruence-check.md on all pieces together
7. File all pieces with front matter
```

---

## Key Documents to Understand First

### 1. AGENT.md
**Read this first.** Defines your identity, responsibilities, context loading protocol, and overall workflow. This is your constitution.

**Key sections:**
- System identity and core responsibilities
- Context loading checklist (exact files to read when starting)
- Master workflow (from intelligence to filed creative)
- Quality gates (Copy Chief minimums)
- Anti-mimicry protocol
- Output standards (frontmatter requirements)

### 2. creative-sprint.md
**Read this next.** The master SOP for a production sprint—designed to generate 5-10 ads in 6-8 hours while maintaining quality and variety.

**Key sections:**
- Pre-production checklist (10 gates before writing)
- Step-by-step workflow (7 phases from intelligence to filing)
- Batch production guidelines (preventing repetition fatigue)
- Time estimates and production sequence examples

### 3. format-selection-guide.md
**Use this to choose format.** A decision tree that matches format choice to awareness level, mechanism complexity, villain type, and funnel architecture.

**Key sections:**
- Format comparison matrix (9 formats, when to use each)
- Decision tree (questions 1-4 lead you to the right format)
- Format-specific guidance (what each format is best for)
- Quick decision framework

### 4. self-assessment.md
**Use this to grade every piece.** The Copy Chief framework: 5 dimensions, anti-inflation rules, Kill List, and production decision gates.

**Key sections:**
- 5-dimension scoring framework (Belief-Shift, Dual-Track, Pacing, Voice, Structure)
- Anti-inflation rules (default 5, earn every point above)
- Kill List (8 instant deductions)
- Assessment process (phase by phase)
- Production decision criteria (6.5 production, 7.5 scaling)

### 5. brief-creation.md
**Use this to write briefs.** Everything you need to create a specification document that guides your own writing.

**Key sections:**
- What is a creative brief (7 core questions it answers)
- Pre-brief preparation (pulling from Market Analyst intel)
- Brief template structure (9 comprehensive sections)
- Brief approval checklist
- Common mistakes and fixes

---

## Quality Standards

### Copy Chief Scoring (0-10 scale)
- **6.5-7.4**: Production-ready (safe to deploy in campaigns, test before scaling)
- **7.5+**: Scaling-ready (approved for aggressive volume deployment)
- **Below 6.5**: Archive (do not use in campaigns)

### Anti-Inflation Rules
- Default starting score: 5 (market average)
- You must earn every half-point above 5
- No single dimension above 8
- Justify every score above 5

### Kill List (Instant Score Caps)
1. Obvious AI language → Cap 7.0
2. Transparent marketing tells → Cap 7.0
3. Naked asks (CTA without trust) → Cap 7.0
4. Mechanism vagueness → Cap 7.0
5. Villain absence → Cap 7.0
6. Approval-seeking language → Cap 6.5
7. Failed funnel congruence → Cap 6.5
8. Logical fallacies → Cap 6.0

---

## Integration with Larger System

### Upstream Context
- **[[DR-SOP-Obsidian.md]]** — Master operating system (read in full at sprint start)
- **[[/agents/market-analyst/intel-drops/]]** — Where Market Analyst deposits latest intelligence
- **Skill files** — Format-specific playbooks you reference during production

### Output Destination
- **[[/output/]]** folders by format
- Campaign Ops pulls production-ready pieces (6.5+)
- Creative archive becomes searchable library

### References Used During Production
- **[[/long form copy/references/]]** — 100+ real ads (for angle/mechanism inspiration)
- **[[/video ads/references (transcripts)/]]** — 48 video transcripts (for pacing/structure study)
- **[[/long form copy/skills/long-form-copy/]]** — 5 belief shifts + 16 pacing laws + 13 beats
- **[[hook-generation-v2]]** — Hook engineering system
- **[[/advertorial/copy skill files/]]** — 6 advertorial frameworks
- **[[/listicle/skill/]]** — Listicle builder
- **[[/statics/branded-static-ads/SKILL.md]]** — Static ad creation
- **[[/native images/skill/]]** — Native image briefs
- **[[/copy-chief/SKILL.md]]** — Copy grading system

---

## Common Workflows at a Glance

### "I need to write 3 hooks testing different angles"
1. Review AGENT.md (5 min refresh)
2. Check [[/agents/market-analyst/intel-drops/]] for unsaturated angles
3. Create 3 brief sketches (identify villain, mechanism, narrator for each)
4. Generate 3 hooks using [[hook-generation-v2]]
5. Self-assess each using self-assessment.md
6. File in `/output/hooks/[PRODUCT]/`

**Total time:** 60-90 minutes

### "I need to write a full 3-piece funnel"
1. Load full AGENT.md context
2. Use creative-sprint.md for batch planning
3. Create 3 briefs using creative-brief-template.md
4. Produce Lead Ad (45-60 min)
5. Produce Bridge (75-90 min)
6. Produce Bridge 2 / Product Page context (60-75 min)
7. Run funnel-congruence-check.md on all three together
8. Self-assess and adjust for congruence
9. File all three with frontmatter

**Total time:** 8-10 hours

### "I'm scoring a piece and it feels weak"
1. Use self-assessment.md step-by-step
2. Score the 5 dimensions honestly (default 5, earn every point)
3. Check the Kill List (any instant caps?)
4. If score < 6.5: Archive with revision notes
5. If score 6.5-7.4: File as production-ready
6. If score 7.5+: File as scaling-ready

**Total time:** 10-15 minutes

---

## Troubleshooting

### "I'm writing but feel lost"
→ Open your Creative Brief and re-read it. Brief is your north star.

### "My piece feels weak"
→ Run self-assessment.md. Don't guess the score. Use the framework.
Most likely issues: vague mechanism, missing villain, no belief shift, wrong voice.

### "Is my funnel going to work?"
→ Run funnel-congruence-check.md. Check Exit-State / Entry-State match at each transition.
Then check the 5 Handoff Checks (voice, mechanism language, temperature, awareness, trust).

### "Should I rewrite this or archive it?"
→ If score below 6.5: Archive with revision notes.
If one specific dimension drags you down: Identify which one.
Revise just that dimension or archive.

### "How do I know what angle to write?"
→ Run anti-mimicry audit: What angles are in the vault already?
Check Market Analyst intel: What angles are flagged as unsaturated?
Find the gap. That's your angle.

### "What format should I use?"
→ Use format-selection-guide.md. Answer the 4 decision tree questions.
Format choice depends on awareness level, mechanism complexity, villain type, funnel position.

---

## File Paths for Quick Reference

**Master System:**
- `[[DR-SOP-Obsidian.md]]` — Constitution

**Market Intelligence:**
- `[[/agents/market-analyst/intel-drops/]]` — Fresh intel

**Skill Files:**
- `[[/long form copy/skills/long-form-copy/]]`
- `[[hook-generation-v2]]`
- `[[/advertorial/copy skill files/]]`
- `[[/listicle/skill/]]`
- `[[/statics/branded-static-ads/SKILL.md]]`
- `[[/native images/skill/]]`

**Reference Libraries:**
- `[[/long form copy/references/]]`
- `[[/video ads/references (transcripts)/]]`

**Products:**
- Lunessa, Motilli, Velantra (specs in vault)

---

## Success Metrics for the System

### Agent-Level Success
- Every creative piece has a Copy Chief score (no exceptions)
- Scoring is consistent and justified (you can explain every score)
- 70%+ of output scores 6.5+ (production-ready)
- 40%+ of output scores 7.5+ (scaling-ready)

### Creative-Level Success
- Each piece clearly shifts a specific belief (not multiple beliefs)
- Each piece identifies and tears down a specific villain
- Each piece has a clear, credible mechanism
- Each piece uses the avatar's actual language
- Each piece feels human, not AI or marketing-y

### System-Level Success
- Every creative piece is filed with complete frontmatter (searchable)
- No angle is repeated within 30 days (anti-mimicry system works)
- Funnel pieces work together without fractures (congruence verified)
- Campaign Ops can easily find and deploy production-ready creative

---

## Getting Help

**Questions about strategy?** → Read the relevant SOP
**Questions about your brief?** → Read brief-creation.md
**Questions about format choice?** → Read format-selection-guide.md
**Questions about scoring?** → Read self-assessment.md
**Questions about funnels?** → Read funnel-congruence-check.md

**Still stuck?** → Return to AGENT.md. Everything connects back to the core operating system.

---

## Version & Maintenance

**System Version:** 1.0 (March 2026)
**Last Updated:** 2026-03-22
**Maintainer:** Creative Strategist Agent System

**Revision Schedule:**
- Monthly: Review scoring calibration
- Quarterly: Update brief templates based on learnings
- As-needed: Add new angle frameworks or mechanism categories

---

## Ready?

Start with [[AGENT.md]]. Then choose your task. The system is built to get out of your way and let you focus on creative production.

**You have everything you need. Go make great ads.**
