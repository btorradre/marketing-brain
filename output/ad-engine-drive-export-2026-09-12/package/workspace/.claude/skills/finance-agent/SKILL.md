---
name: finance-agent
description: "The ecommerce accounting agent. Aggregates every money source into one transaction table — GPT 5.6 Sol's raw bank/card exports dropped in finances/inbox, Apple Card statement PDFs, supplier bill spreadsheets, the Meta API, and the Shopify Admin API — then categorizes every transaction (vendor rulebook → Plaid hints → Claude → a review queue Brooks rules on), splits spend into MARKETING / AI / OPERATING / COGS buckets, and builds the month-by-month P&L (Executive P&L tab + full P&L workbook + markdown + JSON) down to net profit. Use whenever Brooks says 'run the finance close', 'build the P&L', 'categorize these transactions', 'what did we spend on AI / marketing', 'import the bank export', 'read the supplier statements', 'how much did we make', or drops a bank export / statement and wants it in the books. Wraps and extends the shopify-financials skill (which owns the Shopify pull and the workbook)."
---

# finance-agent — aggregation + categorization + P&L

**Division of labour:** GPT 5.6 Sol fetches raw transactions (it is connected to the bank/card accounts). This skill — Claude — owns everything after that: one table, one rulebook, one ledger, one P&L.

```
GPT 5.6 Sol ──raw csv/json/xlsx──▶ finances/inbox/ ─┐
Apple Card PDFs   finances/statements/ ─────────────┤  ingest.py ──▶ data/transactions.json
Supplier bills    finances/supplier invoices/ ──────┤  supplier_bills.py ──▶ data/supplier_bills.json
Legacy ledger rows (Meta API pulls) ────────────────┘
                                                        │
                                   categorize.py  rules → hints → (Claude --llm) → review queue
                                                        │  rebuilds shopify-financials/data/expenses.json
Shopify Admin API (monthly_pl.py, live or --from-cache) ┤
                                                        ▼
                                   build_pl.py  → finances/finalized statements/PL_Monthly_*.xlsx + PL_*.md + PL_*.json
```

## Bank pull — Wells Fargo + Amex (SimpleFIN Bridge)

Neither bank has a public API; `scripts/fetch_simplefin.py` pulls both through SimpleFIN Bridge (already a
$1.50/mo line on the books) into the inbox in the raw fetch shape, so ingest treats it exactly like a GPT export.
One-time: Brooks connects the banks at bridge.simplefin.org, creates a **setup token**, and Claude runs
`fetch_simplefin.py claim <token>` (stores `SIMPLEFIN_ACCESS_URL` in `.env`). A 403 on any call = URL revoked → new token.
`finance_agent.py close --pull` runs the pull first. GPT 5.6 Sol's paste-the-prompt export remains the fallback.

## Run it

```bash
cd "<marketing brain>/.claude/skills/finance-agent/scripts"
python3 finance_agent.py status                          # inbox / table / queue / ledger coverage
python3 finance_agent.py close --year 2026 --from-cache  # full loop without touching Shopify
python3 finance_agent.py close --year 2026 --llm         # live Shopify pull + Claude on the leftovers
python3 review.py --show                                 # what needs a ruling
python3 review.py --set-merchant "kalodata" marketing_software --learn --name "Kalodata"
python3 categorize.py && python3 build_pl.py --year 2026 --from-cache
```

## The monthly close, step by step (what Claude does when Brooks says "run the close")

1. **Check the inbox.** `finance_agent.py status`. If a month has no bank export, say so and hand Brooks the fetch prompt in `references/gpt-sol-fetch-prompt.md` — do not estimate silently (the P&L will flag the month in red and fill with estimates until real data lands).
2. **Ingest.** `ingest.py` reads every file in the inbox (any of the three shapes), parses new Apple Card PDFs, moves inbox files to `inbox/processed/`. Dedupe is by date+amount+description+account — re-exports are safe.
3. **Supplier statements.** `supplier_bills.py` parses every bill in `finances/supplier invoices/` (brand from SKU prefix: BRO*/xwp = Velantra, brook5/bro023 = Motilli). These are the COGS truth used for the reconciliation table — they are NOT booked as an expense (hybrid COGS already accrues Shopify cost-per-item).
4. **Categorize.** `categorize.py` applies `config/vendor_rules.json` first, then Plaid hints, then (with `--llm`) Claude Opus 5 on the leftovers (`--provider openai` swaps in GPT 5.6 Sol). Rebuilds the ledger. Anything under 0.8 confidence or flagged by a rule goes to `data/review_queue.json`.
   **Two-model check:** `--second-opinion` sends every categorized, unlocked row to `gpt-5.6-sol` (OpenAI API, key in `.env`) with its current category; a confident disagreement that changes the BUCKET (marketing/ai/operating/cogs/excluded) is pushed to the queue with GPT's reasoning. Agreement raises confidence. Use `--limit N` to cap cost.
5. **Review.** Run `review.py --show`, read the queue yourself, and rule on what the house rulings in `references/category-taxonomy.md` already settle. Present Brooks ONLY what is genuinely his call (personal vs business, unknown wires, Coinbase-type items). Apply rulings with `review.py --set-merchant … --learn` so they become rules. Re-run `categorize.py`.
6. **Build.** `build_pl.py --year 2026 [--from-cache]` → workbook (Executive P&L tab first), markdown, JSON in `finances/finalized statements/`.
7. **Report** to Brooks: latest full month's net revenue, gross profit, Marketing, AI, Operating, Net profit, plus every data-quality flag (months with no bank data, unreviewed rows, estimated fills, COGS coverage). Numbers in a short table, flags as bullets.

## Laws

- **Never overstate profit.** Unknown rows are booked as other_opex until ruled; months without bank data get estimated fills (red) — say so every time.
- **Never invent a business purpose** for personal-looking spend. Flag it; Brooks decides.
- **Rules beat hints beat the model.** A vendor ruled once is a rule forever (`--learn`). Edit `config/vendor_rules.json` by hand for anything systematic; keep specific patterns above generic ones (meals/retail regexes are the tail).
- **AI is its own bucket** even when the tool is used for marketing. Marketing tools that are not AI products stay in marketing_software.
- **Hybrid COGS is the default**; supplier bills and wires reconcile, they don't replace. `--cogs-basis cash` exists for a cash view.
- **Consolidated only** — no per-brand expense allocation in the headline (Brooks's standing ruling).
- **Don't re-categorize locked rows.** Legacy Meta-API rows, supplier bills, and manual rulings are locked; `--recategorize` only touches unlocked rows.

## Files

- `scripts/finance_agent.py` — orchestrator (`status | ingest | supplier | categorize | review | build | close`)
- `scripts/fetch_simplefin.py` — `claim | status | pull` Wells Fargo + Amex via SimpleFIN → inbox CSV
- `scripts/ingest.py` — inbox (GPT Sol raw / Plaid workbook / legacy CSV) + Apple Card PDFs + legacy-ledger migration → `data/transactions.json`
- `scripts/supplier_bills.py` — supplier spreadsheets → `data/supplier_bills.json` (`--to-ledger` adds locked memo rows)
- `scripts/categorize.py` — rulebook → hints → `--llm` → review queue; rebuilds the ledger (backs up the old one)
- `scripts/review.py` — show / rule / learn
- `scripts/build_pl.py` — runs `shopify-financials/monthly_pl.py`, then writes markdown + JSON from `executive.json`
- `scripts/fin_common.py` — paths, taxonomy import, parsers
- `config/vendor_rules.json` — the rulebook (seeded with ~80 vendors from the 2026 ledger; grows via `--learn`)
- `references/gpt-sol-fetch-prompt.md` — the contract GPT 5.6 Sol must follow
- `references/category-taxonomy.md` — buckets + standing rulings
- OpenAI: `OPENAI_API_KEY` in `marketing brain/.env`; model id `gpt-5.6-sol` (verified on /v1/models 2026-09-02). Anthropic: `ANTHROPIC_API_KEY` same file.
- Taxonomy + workbook live in `shopify-financials` (`import_expenses.py` CATEGORIES/BUCKETS, `build_pl_workbook.py` Executive P&L tab)
