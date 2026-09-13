---
type: session-summary
date: 2026-03-21
session_id: local_33b749ad-60ab-4539-adc0-e578cbd0f6b3
title: "Organize ads and build static strategy"
category: strategy
brands_discussed: [Auri Labs, Primal Viking, GleeFull, GLP-1 SOS, North Valley Health Clinic, Neurosmile, Primal Queen]
formats_worked: [static, branded-statics, skill, brief]
tags:
  - session-log
  - summary
  - strategy
  - branded-statics
  - skill-development
  - n8n
  - competitor-analysis
  - gethookd
  - automation
---

# Organize ads and build static strategy — Session Summary

**Date:** 2026-03-21
**Category:** strategy
**Transcript:** [[conversation-log/transcripts/2026-03-21_organize-ads-and-build-static-strategy_e578cbd0]]

## What Happened
Comprehensive session that classified 172 ad images into native vs. branded categories, conducted competitive intelligence on 7 brands via GetHookd (36,000+ ads, 9,500+ statics), built a branded static ad strategy document, created a 25KB branded-static-ads skill, and deployed an n8n workflow for automated branded static generation.

## Key Decisions Made
- Image classification: 139 native/UGC → native_ads/, 33 branded → branded_statics/
- Identified 8 branded static archetypes from competitive analysis
- Built 6 core personas with micro-angles for static targeting
- 4-layer copy architecture hierarchy for branded statics
- n8n workflow uses Claude for concept generation + OpenAI for image generation
- Skill description trimmed from 1,383 to 922 characters to fit 1,024 char limit

## Insights & Learnings
- **8 branded static archetypes** identified from 7-brand competitive analysis — these are the repeating patterns across all successful health supplement statics
- **GetHookd** is effective for bulk competitive intelligence — 36,000+ ads catalogued in a single session
- **Skill description limit is 1,024 characters** — must be concise while still triggering correctly
- **n8n workflow** can automate the concept → image pipeline, reducing manual work significantly

## Creative Output
- Branded_Static_Ad_Strategy.docx — comprehensive strategy document
- branded-static-ads/SKILL.md — 25KB skill file encoding all analysis
- n8n workflow "Branded Static Ad Generator" (ID: HaRlOGN82HaTYvpV)
- Image classification (139 native + 33 branded) with proper folder structure

## Action Items & Next Steps
- Connect Anthropic and OpenAI API credentials in n8n to activate the workflow
- Test the workflow with a real product brief
- Install the branded-static-ads skill
- Generate first batch of statics using the new system

## Notable Quotes / Language
None — strategy/production session.

## Connections to Vault
- New [[branded-static-ads]] skill created
- Strategy doc provides archetypes and personas for all future static production
- n8n workflow connects to automation infrastructure
- Competitive intel from GetHookd informs overall creative direction
