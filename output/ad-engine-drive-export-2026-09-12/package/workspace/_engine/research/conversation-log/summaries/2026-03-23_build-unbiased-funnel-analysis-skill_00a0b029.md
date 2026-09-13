---
type: session-summary
date: 2026-03-23
session_id: local_ca98c809-3fff-4470-8a8f-00a0b02982e6
title: "Build unbiased funnel analysis skill"
category: skill-development
brands_discussed: []
formats_worked: [skill, funnel]
tags:
  - session-log
  - summary
  - skill-development
  - funnel-analysis
  - congruence
  - diagnostics
---

# Build unbiased funnel analysis skill — Session Summary

**Date:** 2026-03-23
**Category:** skill-development
**Transcript:** [[conversation-log/transcripts/2026-03-23_build-unbiased-funnel-analysis-skill_00a0b029]]

## What Happened
Built the funnel-analysis skill from scratch — an unbiased diagnostic tool for reading funnels alongside Meta performance data. Created the core skill (348 lines), funnel type patterns reference, and metric context reference. Fixed YAML description length issue.

## Key Decisions Made
- Anti-hallucination protocol: skill refuses to diagnose without both creative AND performance data
- Diagnoses the FIRST bottleneck only — don't analyze downstream when upstream is broken
- Narrator voice doesn't have to match across funnel stages — only the angle (root cause) does
- Emotional ad → logical advertorial flagged as inherently risky congruence pattern
- Emotional ads may flow more naturally to listicles than to clinical advertorials
- YAML description must stay under 1024 chars

## Insights & Learnings
- **Emotional-to-logical transitions are the most common congruence break in funnels.** When an ad sells through emotion and vulnerability, then lands on a clinical/authority advertorial, the emotional temperature drops and readers bounce. Listicles maintain emotional continuity better.
- The skill's 5 congruence dimensions (Angle, Mechanism, Emotional Temperature, Credibility Source, Promise-Delivery) provide a complete diagnostic framework without being prescriptive about format.
- General DTC metric ranges should be labeled as context, not thresholds — historical data is more reliable.

## Creative Output
- funnel-analysis/SKILL.md (348 lines)
- funnel-analysis/references/funnel-type-patterns.md (151 lines)
- funnel-analysis/references/metric-context.md (138 lines)

## Action Items & Next Steps
- Copy funnel-analysis/ folder into .skills/skills/ directory to install
- Test the skill against the Motilli funnel (emotional ad → authority advertorial)
- Run against competitor funnels to validate diagnostic accuracy

## Notable Quotes / Language
- "The skill diagnoses the FIRST bottleneck only. If CTR is 0.4%, it doesn't spend 2,000 words analyzing advertorial congruence — because nobody's getting to the advertorial."
- User: "Although I think if we're running an emotional sales letter to a logical advertorial, that doesn't really make any sense. Therefore, I think running to a listicle would perform better."

## Connections to Vault
- Integrates with [[ad-assessment]], [[long-form-copy]], [[advertorial]], [[listicle-builder]] skills via routing table
- Congruence framework should inform [[native-image-factory]] skill updates
