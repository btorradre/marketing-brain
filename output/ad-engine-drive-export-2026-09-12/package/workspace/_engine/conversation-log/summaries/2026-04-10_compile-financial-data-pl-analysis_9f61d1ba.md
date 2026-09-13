---
type: session-summary
date: 2026-04-10
session_id: local_42baca76-9358-4be9-8323-9f61d1ba4eae
title: "Compile financial data and P&L analysis"
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
  - solorna
  - shopify-api
  - wells-fargo
  - amex
  - cash-flow
  - expense-categorization
---

# Compile financial data and P&L analysis — Session Summary

**Date:** 2026-04-10
**Category:** Strategy
**Transcript:** [[conversation-log/transcripts/2026-04-10_compile-financial-data-pl-analysis_9f61d1ba]]

## What Happened
Built the initial Q1 2026 P&L for BTO EC Ventures from scratch using Shopify API data, Wells Fargo bank statements, and Amex transaction records. Started with a broken version that showed massive fake losses ($230K+ per month), identified the cash-basis vs. accrual-basis mismatch as the root cause, then rebuilt with corrected methodology. Expanded through multiple iterations to include 12 workbook tabs covering per-store revenue, supplier detail, cash flow reconciliation, and full expense categorization across 500+ Amex charges.

## Key Decisions Made
- **Hybrid revenue methodology**: Shopify API (accrual) for Motilli, Motilli v2, Velantra, Solorna + bank deposits for Lunessa (API token blocked)
- **Q1 operating income: $94.7K-$99.5K** (19% margin) — the business IS profitable at the operating level
- **Breakeven after taxes + personal**: The $72.6K franchise tax and ~$27K in personal spending ate essentially all the operating profit
- **Expense categorization**: 500+ Amex charges categorized into Meta ads, SaaS, AI tools, marketing software, contractors, personal, etc.
- **Meta API gap identified**: Only $40K of $186.5K in Meta ad spend captured from API — remaining $146K comes from other ad accounts without tokens

## Insights & Learnings
- **Lunessa was the revenue engine**: $385K deposited in January alone, then essentially zero after that. The business model shifted dramatically from Lunessa-dependent to multi-brand.
- **Supplier payment timing creates cash-basis distortions**: February appeared devastating on cash basis but was actually the supplier payments catching up to January's sales
- **5 Shopify stores running simultaneously**: Lunessa, Motilli, Motilli v2, Velantra, Solorna — each with different revenue profiles and supplier chains
- **Haikou Genyangkai is the main supplier**: $147.5K in Q1 wire transfers, primarily for Lunessa/Motilli product
- **The ~$58K gap between Shopify gross ($555K) and WF deposits ($497K)** = Shopify processing fees + timing + refunds processed before payout

## Creative Output
- Q1 2026 P&L Analysis spreadsheet — 12 tabs, 190 formulas, saved to `/marketing brain/Q1_2026_PL_Analysis.xlsx`

## Action Items & Next Steps
- Fix Lunessa Shopify API token with `read_orders` scope for granular order-level data
- Get Meta access tokens for additional ad accounts to attribute the $146K in unidentified ad spend
- This session feeds directly into the "Verify and rebuild" follow-up session where accrual COGS and franchise tax treatment were further refined
- Consider breaking out per-store ROAS once Meta tokens are available

## Notable Quotes / Language
- "So you're saying I lost 230 grand, 126 grand, 29 grand, and 385 grand. That is not accurate at all." — Brooks catching bad methodology immediately
- "Keep going." — Brooks pushing for deeper analysis, not satisfied with surface-level P&L

## Connections to Vault
- Directly followed by [[conversation-log/summaries/2026-04-11_verify-rebuild-q1-financial-analysis_bc0b5afb]] which refined the COGS allocation and franchise tax treatment
- Financial data informs [[funnel-analysis]] — per-store ROAS, ad spend allocation decisions
- Meta ad spend breakdown ($186.5K) connects to campaign-level performance analysis
- Supplier chain mapping (Haikou, Orelli, Wise, Kabir, Matvei) is business-critical intelligence
