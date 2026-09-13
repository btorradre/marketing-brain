---
type: session-transcript
date: 2026-03-23
session_id: local_ca98c809-3fff-4470-8a8f-00a0b02982e6
title: "Build unbiased funnel analysis skill"
tags:
  - session-log
  - transcript
  - skill-development
  - funnel-analysis
---

# Session Transcript: Build unbiased funnel analysis skill

**Date:** 2026-03-23
**Session ID:** local_ca98c809-3fff-4470-8a8f-00a0b02982e6
**Status:** idle

---

## Summary of Activity

Built the funnel-analysis skill from scratch. User wanted an unbiased diagnostic tool that reads a complete funnel (ad → landing page → checkout) alongside Meta performance data to identify bottlenecks without hallucinating or making assumptions.

**Planning phase:** Claude proposed a detailed architecture with 4 phases: Data Intake & Triage, Bottleneck Identification (5-layer diagnostic), Congruence Analysis, and Diagnosis Output. User approved with refinements:
- Narrator voice doesn't have to match across funnel stages — only the angle does (same root cause)
- Emotional sales letter → logical advertorial is a congruence risk → listicle may perform better
- Must clearly identify which specific stage is the bottleneck

**Build phase:** Created 3 files:
1. `funnel-analysis/SKILL.md` (348 lines) — Core skill with:
   - Anti-hallucination protocol (7 rules)
   - 5-layer diagnostic: Delivery (CPM) → Thumb-Stop (CTR) → Click-to-Page (LP view rate) → On-Page (conversion) → Checkout (purchase rate)
   - 5 congruence dimensions: Angle Continuity, Mechanism Continuity, Emotional Temperature Match, Credibility Source Continuity, Promise-Delivery Alignment
   - Skill routing table (which creative skill to use after diagnosis)
2. `references/funnel-type-patterns.md` (151 lines) — 7 funnel configurations with architecture logic and characteristic break points
3. `references/metric-context.md` (138 lines) — DTC performance ranges, explicitly labeled as context not thresholds

**Fix:** YAML description was over 1024 chars — trimmed to 595 chars.
