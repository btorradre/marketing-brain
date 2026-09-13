---
type: session-summary
date: 2026-04-11
session_id: local_05079f95-b3db-4e6a-a9ef-bc0b5afb4cd7
title: "Verify and rebuild Q1 financial analysis"
category: strategy
brands_discussed: [Lunessa, Motilli, Motilli v2, Velantra, Solorna]
formats_worked: [funnel]
tags:
  - session-log
  - summary
  - strategy
  - financial-analysis
  - P&L
  - Q1-2026
  - lunessa
  - motilli
  - velantra
  - COGS
  - accrual-accounting
  - ROAS
  - meta-ads
  - shopify
---

# Verify and rebuild Q1 financial analysis — Session Summary

**Date:** 2026-04-11
**Category:** Strategy
**Transcript:** [[conversation-log/transcripts/2026-04-11_verify-rebuild-q1-financial-analysis_bc0b5afb]]

## What Happened
Major rebuild of the Q1 2026 P&L for BTO EC Ventures. Started with a broken P&L that showed false massive losses, then iteratively corrected it by switching from cash-basis to accrual COGS allocation, reclassifying supplier payments (Wise, Orelli) from OpEx to COGS, moving the $72.6K Delaware franchise tax below the line, and adding travel expense breakdowns from Amex statements. Multiple rounds of revision driven by Brooks catching numbers that didn't match reality.

## Key Decisions Made
- **Accrual COGS over cash-basis**: Allocated Haikou Genyangkai supplier payments proportionally to when revenue was earned, not when wires were sent. This fixed the false February loss.
- **Franchise tax below the line**: $72,600 is 2025 Delaware annual franchise tax, not a Q1 2026 operating expense. Moved to "Below the Line" section.
- **Wise US Inc ($12K) and Orelli Inc ($16K) reclassified as COGS**: Both are product suppliers (Motilli v2 and other stores), not general operating expenses.
- **Travel expenses separated**: Airlines ($2.7K), Hotels ($7.8K), Ground transport ($2K), Travel dining ($678) — all pulled from Amex and added as OpEx line items.

## Insights & Learnings
- **Q1 ROAS: 2.98x** on $186.5K Meta spend generating $555.5K in Shopify gross sales
- **Refunds are significant**: $27,416 Q1, with Lunessa Jan alone at $17.6K on 361 orders — high refund rate signals product/expectation issues
- **Lunessa drove January**: $372K in January revenue, then fell off a cliff to $35K net in February — brand was clearly winding down
- **Cash vs. accrual timing creates massive distortions**: February looked like a -$128K loss on cash basis but was actually +$14.5K when COGS were properly allocated
- **The business is operationally profitable**: $115-128K operating income for Q1 before franchise tax

## Creative Output
- Q1 2026 P&L spreadsheet (multiple iterations)
- Output saved to session outputs folder

## Action Items & Next Steps
- Fix Q1 percentage formulas (Gross Margin and Operating Margin showing summed monthly percentages instead of Q1 ratios)
- Address additional issues Brooks flagged in the final screenshot
- Get Lunessa Shopify API token with `read_orders` scope for granular order data
- Get Meta access tokens for additional ad accounts to break down the $146K in unattributed ad spend by store/campaign

## Notable Quotes / Language
- "You're sure you're correlating everything from all sources, like don't just assume something" — Brooks pushing for data integrity over speed
- "The final file you just sent is way off" — multiple rounds of correction needed; iterative verification is essential

## Connections to Vault
- Financial data feeds into [[funnel-analysis]] — ROAS metrics, per-store revenue allocation
- Lunessa's high refund rate ($17.6K in Jan) connects to product quality / avatar expectation alignment
- Meta ad spend breakdown needed for per-campaign ROAS analysis
- Connects to [[conversation-log/transcripts/2026-04-10_compile-financial-data-pl-analysis]] — the original P&L build session
