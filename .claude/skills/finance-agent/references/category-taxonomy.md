# Category taxonomy and house rulings

Source of truth for categories: `shopify-financials/scripts/import_expenses.py` → `CATEGORIES` (each has
`section`, `bucket`, `label`). Buckets drive the Executive P&L: **Revenue → COGS → Gross profit →
Marketing → AI → Operating → Net profit.**

| Bucket | Categories | What belongs |
|---|---|---|
| **Marketing** | ad_spend_meta, ad_spend_google, ad_spend_tiktok, ad_spend_other, marketing_software, creators_influencers | Paid media; email/SMS platforms (Klaviyo, Omnisend); ad-intel/spy tools (AdSpy, TrendTrack, Kalodata, Similarweb, Atria, AdRevival, GetHookd); creative editing software (CapCut, Frame.io, Adobe, Canva); attribution (Triple Whale); creators, UGC, influencer seeding (Trybe) |
| **AI** | ai_tools | Every AI product regardless of what it's used for: Anthropic/Claude, OpenAI, OpenRouter, Manus, Higgsfield, ElevenLabs, HeyGen, kie.ai, Runway/Kling/Seedance/Hailuo, Magnific, Pixelcut, GPTZero, WriteHuman, QuillBot, Adnova, Blort, Sync Labs, Wispr, Cursor… |
| **Operating** | software_saas, contractors_agency, payroll, shipping_postage, merchant_fees, chargeback_services, legal_professional, taxes_gov, interest_expense, travel, meals_entertainment, office_misc, other_opex + Shopify Payments fees + chargebacks lost (from the Shopify API) | Everything that runs the company and isn't marketing, AI or product cost |
| **COGS** | Shopify cost-per-item (hybrid, default) or supplier wires (cash basis), + fulfillment_3pl, freight_duties | Product cost, 3PL (Ecomflow), inbound freight/duties |
| **Excluded** | cc_payment, transfer, owner_draw, loan_principal, inventory_purchase (memo under hybrid) | Money movement, not expense. Shown in the memo block, never in profit |

## Standing rulings (from Brooks — do not re-litigate)

- **Consolidated reporting only.** No per-brand expense allocation; brand tags are kept for the contribution tabs but the headline is one company P&L.
- **COGS basis = hybrid** by default. Supplier statements and wires are a cross-check, not the COGS line (that would double count Shopify cost-per-item).
- **Contractors = Venmo / Wise / Upwork to people.** The Dhanraj Gala JPMorgan wire ($1,850, 2026-05) is NOT a contractor → other_opex. Ecom Elixir is a Shopify theme → software_saas.
- **Coinbase $5,500 (2026-06-29)** booked other_opex pending Brooks's call (contractor vs personal).
- **Disputifier = chargeback_services**, and the P&L's TOTAL CHARGEBACK EXPENSE = Shopify dispute fees + lost chargebacks + Disputifier.
- **Refunds** are an OPEX line; revenue is shown before refunds; % metrics use net sales after refunds.
- **Personal-looking spend** (apparel, gym, spa, streaming, casinos, tuition) is never given an invented business purpose. It sits in other_opex flagged for review until Brooks says business or owner_draw.
- **Shopify Payments fees never come from the bank** — the API pulls them per order; a bank "Shopify" charge is the subscription/apps → software_saas.
- **Dose, product, and brand truths** live in the brand folders; finance never overrides them.

## Confidence and the review queue

| Source | Confidence | Goes to review? |
|---|---|---|
| Locked (manual ruling, legacy Meta-API rows, supplier bills) | 1.0 | never |
| Vendor rule | 0.90 | only if the rule says `review: true` |
| Legacy export's own category | 0.70 | yes (below the 0.8 threshold) unless a rule also matched |
| Plaid business_category / detail | 0.2–0.6 | yes |
| Claude (`--llm`) | model's own | if below threshold |
| Nothing matched | 0 | yes; booked as other_opex meanwhile |

Every ruling in `review.py` locks the rows and (with `--learn`) appends a regex rule to
`config/vendor_rules.json`, so the queue shrinks month over month.
