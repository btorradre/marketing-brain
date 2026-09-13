---
name: dr-survey-designer
description: Design post-purchase and post-refusal surveys engineered to produce quotable ad copy rather than satisfaction scores. Part of the Direct Response OS. Use when the user wants survey questions, says "what should we ask customers", "post-purchase survey", "our survey data is useless", "we need better VoC input", "how do we find out why they bought", or when dr-voc-mining reports coverage gaps that only a direct question can fill. Writes brands/<brand>/research/dr-os/surveys/<date>-post-purchase.md. Its output is an instrument, and the responses come back through dr-voc-mining.
user_invocable: true
---

## GOLDEN NUGGET DOCTRINE (MANDATORY — locked 2026-07-11)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded DEEP FRAME in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: *is this the topic, or is this the motive?* If it's the topic, dig one layer deeper (memory loss → becoming my parent; GLP-1 bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes.** The golden nugget LEADS — very top of the piece, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence BEFORE drafting. When analyzing a reference ad/funnel/swipe instead of writing, state the nugget it's built on and whether it leads with it. If the research hasn't surfaced one, mine reviews/VOC/Reddit until it does — never default to a surface angle.

# DR OS — Survey Designer

Most post-purchase surveys ask the questions the brand wants answered. This one asks the questions that produce the language a creative team can write ads from.

A survey that returns "great product, fast shipping" is dead weight. A survey that returns "I tried everything else for three years and nothing worked until this" is a brief that writes itself.

Load [`../direct-response-os/modules/laws.md`](../direct-response-os/modules/laws.md) first.

## Operating rules

1. **Every question must be capable of producing quotable ad copy.** If the best possible answer to a question could not appear in an ad, cut the question.
2. **Open-ended over closed-ended.** Scales and star ratings produce numbers, and numbers do not become hooks. Words do. One rating question is the maximum, and only when it is used to segment the free-text.
3. **Target the moment of decision.** The most valuable question in any post-purchase survey is some form of *what almost stopped you from buying?* The answer is routinely the best hook in the dataset, because it is the objection every non-buyer is still sitting with.
4. **Match questions to awareness levels deliberately.** Some questions surface problem-aware language ("what was going on that made you start looking"), others surface solution-aware language ("what had you already tried"). Design for the level the account is starved at, which `dr-awareness-audit` will have named.
5. **Brevity wins responses.** Five great questions beat fifteen average ones. Every question that does not produce creative-ready language is cut before delivery.

## Step 1 — Load context

- `brands/<brand>/00-brief.md` and `brands/<brand>/ops/` per Law 1.
- `brands/<brand>/research/dr-os/voc-index.md` if it exists. Read the **coverage gaps** section. Those gaps are the reason this survey exists, and the category-specific questions should be built to close them.
- `brands/<brand>/research/dr-os/awareness-map.md` if it exists, for the starved level.
- Any prior survey in `surveys/` so questions are not repeated verbatim across waves.

Velantra note: past survey work is recorded in the customer-quality survey project, and only about 14% of buyers are subscribed, so response volume is capped by reach rather than by question quality. Design for a small n and weight accordingly. Never report a percentage from a survey without stating the n (Law 2).

## Step 2 — Produce the instrument

### THE CORE FIVE

Five questions every brand needs. For each:

- **The question**, worded exactly as the customer will see it
- **What creative output it is designed to produce**
- **The awareness level of language it typically surfaces**
- **An example response that would become a winning hook** (clearly marked as an illustrative example, never presented as a real answer)

### CATEGORY-SPECIFIC QUESTIONS (5 to 8)

Tailored to this product and this customer, and aimed at the coverage gaps from the VoC index. For each:

- The question
- The creative angle it is designed to surface
- How the response would be used in a brief

### THE SINGLE BEST QUESTION

The one question that, answered honestly, produces the most powerful language in the entire survey. Write it, and explain why it beats the other twelve.

### SURVEY DESIGN NOTES

- Recommended format and timing (in-flow post-checkout, email at delivery + N days, SMS)
- How to frame the opening line so customers understand why they are being asked, which is the single biggest lever on free-text length
- The one framing mistake that kills response quality, and how to avoid it
- Expected n and what that n does and does not support claiming

## Step 3 — A word on the refusal survey

When the brand has traffic but weak conversion, the higher-value instrument is not post-purchase at all. It is the exit or post-refusal survey aimed at people who did not buy. Offer it as a second block when the brief indicates a CVR problem rather than a creative-supply problem, and keep it to three questions maximum.

## Step 4 — Write and hand off

Write to `brands/<brand>/research/dr-os/surveys/<YYYY-MM-DD>-post-purchase.md` with standard frontmatter (`artifact: survey`).

Deployment is Omnisend or the Shopify post-purchase page. Both are connected, but sending anything customer-facing is an outward action, so present the instrument and confirm before deploying it.

Close with two lines: which coverage gap each block closes, and the note that responses come back through [`dr-voc-mining`](../dr-voc-mining/SKILL.md) using the reviews protocol.
