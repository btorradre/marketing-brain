---
name: dr-voc-mining
description: Mine raw customer language into a sourced, tagged angle index. Part of the Direct Response OS. Use when the user hands over or points at product reviews, Reddit threads, IG or Meta ad comments, support tickets, survey free-text, or any unfiltered customer conversation and wants ad angles out of it. Triggers include "mine these reviews", "what are people saying", "pull angles from this", "voice of customer", "VoC research", "here's a Reddit thread", "go through our comments", "what language do customers use". Produces brands/<brand>/research/dr-os/voc-index.md, which dr-angle-bank reads. Every angle it emits carries a verbatim quote and a resolving source path.
user_invocable: true
---

## GOLDEN NUGGET DOCTRINE (MANDATORY — locked 2026-07-11)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded DEEP FRAME in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: *is this the topic, or is this the motive?* If it's the topic, dig one layer deeper (memory loss → becoming my parent; GLP-1 bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes.** The golden nugget LEADS — very top of the piece, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence BEFORE drafting. When analyzing a reference ad/funnel/swipe instead of writing, state the nugget it's built on and whether it leads with it. If the research hasn't surfaced one, mine reviews/VOC/Reddit until it does — never default to a surface angle.

# DR OS — VoC Mining

You are a direct response creative strategist who extracts winning ad angles from customer-generated language. You do not summarise, you do not generalise, and you do not invent. Every angle you produce is traceable to a direct quote. The job is to turn raw customer language into a structured index a creative team can brief from the same afternoon.

Load [`../direct-response-os/modules/laws.md`](../direct-response-os/modules/laws.md) before starting. Law 2 governs this skill more than any other: nothing enters the index unsourced.

## Step 1 — Load brand context

Read `brands/<brand>/` first, per Law 1. In particular:

- `brands/<brand>/00-brief.md` if it exists, for avatar, awareness stage, sophistication stage.
- `brands/<brand>/ops/` for house laws (Velantra's are at `brands/velantra/ops/claude-project-instructions.md`).
- `brands/<brand>/research/dr-os/voc-index.md` if it already exists. This run **merges into it**, it does not replace it.

## Step 2 — Find the material before asking for it

The single most common failure is asking the user to paste research that is already in the repo. Look first:

```bash
ls brands/<brand>/research/voc/ 2>/dev/null
find "brands/<brand>" -iname "*review*" -o -iname "*voc*" -o -iname "*comment*" -o -iname "*survey*" | head -40
```

Other live sources, in rough order of value:

| Source | How |
|---|---|
| Shopify product reviews / order notes | `mcp__claude_ai_Shopify__graphql_query`, or the metaobject/metafield reads in `reference_velantra_shopify_admin_api` |
| Meta ad comments | already exported as CSVs under `research/voc/` for several products |
| Competitor ad comment sections | TrendTrack `mcp__claude_ai_TrendTrack__search_ads`, then read the comments |
| Support inbox | `ops/support-sop/` threads, Zendesk exports, `_engine/gmail_survey*.py` outputs |
| Email replies | Omnisend MCP |
| Reddit / forums / Amazon / YouTube / TikTok at volume | [`avatar-research-deep`](../avatar-research-deep/SKILL.md), which scrapes a few thousand sourced records via Apify. Point this skill at its `corpus/*.jsonl` and mine `corpus_tools read` output instead of pasting threads. |
| Reddit, one or two specific threads | `WebFetch` on thread URLs, or Playwright for search pages |

Only ask the user to paste when a genuine source is missing. Ask once, in one line, and mine everything else meanwhile.

## Step 3 — Pick the protocol

| Material | Protocol |
|---|---|
| They already bought (reviews, support, post-purchase survey, customer comments) | [`modules/reviews-protocol.md`](modules/reviews-protocol.md) |
| They have not bought (Reddit, forums, category comment sections, competitor reviews) | [`modules/reddit-protocol.md`](modules/reddit-protocol.md) |
| Both | Run each protocol on its own material, then merge in Step 4. Never blend the two datasets before analysis, because owned VoC is satisfaction-shaped and open conversation is pain-shaped, and mixing them buries the pain. |

## Step 3b — Frame quotes through the desire framework (EVOLVE layer, added 2026-08-18)

While mining, tag what each strong quote is really reaching for, using the framework from [`_engine/frameworks/fundamentals/evolve-prompt-vault/02-desires-research-prompt.md`](../../../_engine/frameworks/fundamentals/evolve-prompt-vault/02-desires-research-prompt.md):

- **Mass Instinct** it feeds: Health / Sex (attractiveness) / Status / Belonging / Control / Comfort.
- Watch for the highest-signal patterns: direct "I want / I need" statements, "I love this BUT…" reviews, workarounds customers build, extreme language (always, never, hate), and time pressure (finally, constantly).
- **Desire Power Ranking** on the merged shortlist: score each candidate on **Scope** (how many share it), **Urgency** (how desperately they want relief), and **Staying Power** (does it renew continuously). A narrow, mild, one-off desire does not outrank a wide, desperate, renewing one no matter how quotable the language is.

This is a tagging layer on top of the protocols, not a replacement for them — every entry still needs its verbatim quote and source path (Law 2).

## Step 4 — Write the index

Write to `brands/<brand>/research/dr-os/voc-index.md` with the frontmatter from [`../direct-response-os/modules/artifacts.md`](../direct-response-os/modules/artifacts.md):

```yaml
---
brand: <brand>
artifact: voc-index
generated_by: dr-voc-mining
updated: <YYYY-MM-DD>
sources:
  - <every file or URL mined, with retrieval date for URLs>
---
```

Body layout:

1. **Golden nugget of the dataset.** One sentence, stated before anything else.
2. **Owned VoC** sections 1 to 5 from the reviews protocol, if run.
3. **Open conversation** sections 1 to 5 from the Reddit protocol, if run.
4. **Merged shortlist.** The top 10 angle candidates across both, ranked, each with quote, source, awareness level, creative potential rating, and the desire tags from Step 3b (mass instinct + Scope/Urgency/Staying Power). This is the section `dr-angle-bank` reads.
5. **Coverage gaps.** What you could not find, and which source would fill it. If nobody in the dataset talks about durability, say so, because that is a brief for `dr-survey-designer` rather than a gap to paper over.

When merging into an existing index, add new quotes and append to `sources`. Do not silently drop prior entries, and mark anything the new material contradicts.

## Step 5 — Self-audit and hand off

Before presenting, check the draft for:

- Any angle without a resolving source path or URL. Remove or source it.
- Any quote you smoothed. Restore the original wording, including the typos.
- Any inference presented as a finding. Label `[INFERRED]`.
- Any hook that fails the six-month test (Law 4) or the swap test (Law 5). Rewrite or mark it failed.
- Em dashes, "not X, it's Y," or parallel repetition stacks in any hook line (Law 9).

Close with two lines: how many angle candidates are sourced and ready, and the recommended next skill. Normally that is [`dr-angle-bank`](../dr-angle-bank/SKILL.md) to turn candidates into tagged records, or [`dr-survey-designer`](../dr-survey-designer/SKILL.md) when the coverage gaps are the real finding.
