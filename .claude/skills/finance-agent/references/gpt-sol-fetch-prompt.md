# GPT 5.6 Sol — the fetch contract

GPT 5.6 Sol is connected to the bank and card accounts. Its ONLY job in this system is to **fetch raw
transactions and hand them over in one fixed shape**. It does not categorize, net, summarize, or judge
what is business vs personal — Claude (finance-agent) does that against the vendor rulebook and the
house rulings, so decisions are made once and remembered.

## The loop (monthly close)

1. Paste the prompt below into GPT 5.6 Sol with the month(s) you want (or "everything since 2026-07-01").
2. Save what it returns into `marketing brain/finances/inbox/` — one file per account is fine, or one
   combined file. CSV, JSON or XLSX all work. Any filename.
3. Tell Claude: **"run the finance close for August"** (or run `python3 finance_agent.py close --year 2026`).
   Claude ingests the inbox, parses new Apple Card PDFs and supplier statements, categorizes, shows you
   the review queue for anything it couldn't settle, rebuilds the ledger, and writes the P&L.
4. Rule on the review queue (a sentence per vendor is enough). Claude turns each ruling into a rule so it
   never asks again.

## Prompt to paste into GPT 5.6 Sol

```
Export every transaction from ALL of my connected business bank and card accounts for <PERIOD>.

Output a CSV (or JSON array) with EXACTLY these columns, one row per transaction:

date,account,description,merchant,amount,direction,currency,txn_id,hint

- date: posted/transaction date as YYYY-MM-DD.
- account: the account's display name exactly as your connection shows it, including last-4
  (e.g. "Business Platinum Card", "BUSINESS CHECKING ...0189", "Mercury Checking ...1234").
- description: the raw bank/card descriptor, untouched. No commas — replace with ";".
- merchant: the cleaned merchant/counterparty name if your connection provides one, else blank.
- amount: absolute value, 2 decimals.
- direction: "out" for money leaving the account (purchases, payments, wires, fees),
  "in" for money arriving (deposits, refunds, credits, payouts).
- currency: ISO code (USD unless the account is not USD).
- txn_id: the provider's transaction id if you have one, else blank.
- hint: OPTIONAL. Any category, memo, or counterparty detail your connection already attaches
  (e.g. Plaid personal_finance_category, a wire's beneficiary name). Never invent one.

Rules — these matter more than formatting:
- EVERY transaction appears exactly once. Do not net, merge, dedupe across accounts, or summarize.
- Include card bill payments, transfers between my accounts, ATM withdrawals, refunds, and deposits.
  I exclude them on my side; leaving them out breaks reconciliation.
- Include pending transactions only if you can mark them: append ";PENDING" to the description.
- Do not categorize, do not flag as personal, do not drop small amounts.
- If an account failed to sync or is missing days, say so in a note ABOVE the CSV block, with the
  account name and the date range affected.
- Finish with one line per account: account name, number of rows, first date, last date, sum of "out".
```

## GPT 5.6 Sol over the API (no bank access there)

`gpt-5.6-sol` is also reachable through the OpenAI API (`OPENAI_API_KEY` in `.env`). The API model does NOT see the
bank connections — those live in the ChatGPT app — so fetching stays a paste-the-prompt step. The API path is used for
the **second-opinion classifier** (`categorize.py --second-opinion`) and as an alternative primary classifier
(`--llm --provider openai`).

## What Claude does with it

| Column | Used for |
|---|---|
| account | becomes the `source` tag (`business_platinum`, `business_checking_0189`…). The P&L only treats a month as "complete" when a real bank/card source covers it — Apple Card or Meta-API rows alone don't. |
| description + merchant | vendor rulebook matching, then Plaid hints, then Claude's judgment for leftovers |
| amount + direction | positive = money out. Refunds/credits arrive as negative expenses on the same line. |
| txn_id | stored; dedupe is by date+amount+description+account so re-exports never double count |
| hint | secondary signal only; a rule always beats a hint |

Older shapes still work: the previous ChatGPT/Plaid workbook ("All Expenses" sheet) and the legacy
`date,description,amount,category,brand,source` CSV. In the legacy shape the `category` column is
treated as a hint, not a lock.
