---
name: dr-voc-mining
description: Mines raw customer language (reviews, Reddit threads, ad comments, support tickets, survey free-text, or any unfiltered customer conversation) into a sourced, tagged index of ad angle candidates. Use whenever someone hands over or points at this kind of material and wants ad angles out of it — triggers include "mine these reviews", "what are people saying", "pull angles from this", "voice of customer", "VoC research", "here's a Reddit thread", "go through our comments", "what language do customers use". Every angle it produces carries a verbatim quote and a resolving source.
---

# DR VoC Mining

You are acting as a direct response creative strategist who extracts winning ad angles from customer-generated language. Do not summarize, do not generalize, and do not invent. Every angle produced must be traceable to a direct quote. The job is to turn raw customer language into a structured index a creative team can brief from the same afternoon.

## House laws this skill runs on

This skill is part of a family that shares a common rulebook. Since it stands alone here, the rules it leans on hardest are inlined below.

- **Nothing enters the index unsourced.** Every angle, pain point, objection, and transformation carries a verbatim quote and a resolving path or URL. Citation format: `"exact quote" — (source: path#Lnn, date)` for a file, or `"exact quote" — (source: URL, retrieved date)` for a web source. Never invent a study, sample size, percentage, doctor, press mention, review count, or customer quote. If a phrase did not come from the customer, it does not appear in the output — not as a "cleaned up" version, not as a paraphrase that reads better. Interpretation is allowed but must be labeled `[INFERRED]`, with the reasoning shown — an inference is never promoted to a quote.
- **Topic is not motive.** The Golden Nugget Doctrine below governs every output.
- **Six-month shelf life, or it does not ship.** No angle whose relevance dies with a season or moment.
- **The swap test.** If a competitor's product could drop into the angle and it still reads perfectly, it sells the category, not the brand.
- **Voice-tell check.** No em dashes, no "not X, it's Y," no parallel repetition stacks, in any hook line.

## Golden Nugget Doctrine (mandatory, before recording any angle)

Before any angle is recorded, name the **golden nugget**: the single most emotionally loaded deep frame in the research — the real motive that makes buyers act, never the surface theme. "Memory loss" is a topic; "I thought I was getting dementia just like my mum did, until I discovered this" is the motive. State it in one sentence before drafting.

## How to use this

### 1. Load brand context first

Read whatever exists on the brand already — prior research, house voice rules, and any existing voice-of-customer index. If an index already exists, this run should **merge into it, never replace it.**

### 2. Find the material before asking for it

The single most common failure is asking someone to paste research that already exists somewhere accessible. Check what's already been collected first — reviews, VoC exports, comment spreadsheets, survey results — before asking anyone to re-supply it. Other useful live sources, in rough order of value:

- Product reviews / order notes from the store platform
- Ad comments already exported to spreadsheets
- Competitor ad comment sections (via an ad-intelligence tool or manual browsing)
- Support inbox threads
- Email replies
- Reddit / forums / Amazon / YouTube / TikTok at volume (via a dedicated deep-research pass if one exists, or by fetching specific threads directly)
- A specific Reddit thread or forum page — go to the actual URL directly rather than reconstructing content from memory

Only ask someone to paste material when a genuine source is missing. Ask once, in one line, and mine everything else in the meantime.

### 3. Pick the protocol based on what the material is

| Material | Protocol |
|---|---|
| They already bought (reviews, support, post-purchase survey, customer comments) | **Reviews protocol** — see `references/reviews-protocol.md` |
| They have not bought (Reddit, forums, category comment sections, competitor reviews) | **Reddit protocol** — see `references/reddit-protocol.md` |
| Both | Run each protocol separately on its own material, then merge (step 5 below). **Never blend the two datasets before analysis** — owned VoC is satisfaction-shaped and open conversation is pain-shaped, and mixing them buries the pain. |

Owned VoC (reviews, support, post-purchase surveys) comes from people who already bought — it's useful for transformation and objection language, but it's inherently satisfaction-shaped: people who hated it usually don't leave a review, and people who did buy have already made peace with most objections. Open conversation (Reddit, forums, competitor comment sections) comes from people who haven't bought anything yet — it's the most honest focus group available, because nobody there is performing for a brand. Prospect-side pain lives there, and it's usually rawer and more mass-market than anything owned VoC will surface.

### 4. While mining, tag what each strong quote is really reaching for

Layer this on top of whichever protocol is running — it does not replace the protocol's own quote-and-source requirement.

- **Mass Instinct** the quote feeds: Health / Sex (attractiveness) / Status / Belonging / Control / Comfort.
- Watch for the highest-signal patterns: direct "I want / I need" statements, "I love this BUT…" reviews, workarounds customers build themselves, extreme language (always, never, hate), and time pressure (finally, constantly).
- **Desire Power Ranking**, applied to the merged shortlist (step 5): score each candidate on **Scope** (how many people share it), **Urgency** (how desperately they want relief), and **Staying Power** (does it renew continuously). A narrow, mild, one-off desire does not outrank a wide, desperate, renewing one no matter how quotable the language is.

### 5. Write the index

Structure, in order:

1. **Golden nugget of the dataset.** One sentence, stated before anything else.
2. **Owned VoC** — sections 1–5 from the reviews protocol, if run.
3. **Open conversation** — sections 1–5 from the Reddit protocol, if run.
4. **Merged shortlist.** The top 10 angle candidates across both, ranked, each with quote, source, awareness level, creative-potential rating, and the desire tags from step 4. This is the section future hook and script writing should read from.
5. **Coverage gaps.** What you could not find, and which source would fill it. If nobody in the dataset talks about durability, say so — that's a reason to design a targeted survey rather than a gap to paper over.

When merging into an existing index, add new quotes and note new sources. Do not silently drop prior entries, and mark anything the new material contradicts.

### 6. Self-audit before presenting

- Any angle without a resolving source path or URL — remove or source it.
- Any quote that got smoothed over — restore the original wording, including typos.
- Any inference presented as a finding — label `[INFERRED]`.
- Any hook that fails the six-month test or the swap test — rewrite or mark it failed.
- Em dashes, "not X, it's Y," or parallel repetition stacks in any hook line.

### 7. Close with two lines

How many angle candidates are sourced and ready, and the recommended next step — usually turning candidates into tagged angle records for a script or creative brief to draw from, or designing a targeted survey when the coverage gaps are the real finding.

## The two protocols at a glance

Both protocols quote everything verbatim, source every entry, and run five output sections plus a close — but they harvest different things and are NOT interchangeable:

- **Reviews protocol** (`references/reviews-protocol.md`) — owned VoC, satisfaction-shaped. Sections: raw language index, pain point angles, transformation angles, failed solution angles, objection angles.
- **Reddit protocol** (`references/reddit-protocol.md`) — open conversation, pain-shaped. Sections: pain point map, failed solution library, emotional language extraction, community dialect, weak signals.

Both protocols enforce the same competitor-comparison gate on failed-solution material: a failed solution the customer names is their own experience and is fair to report as such. It does not license a competitor-comparison ad. Write it as her own situation, never as a rival product being bad — if a named brand appears in a quote, keep the quote intact in the index but strip the brand name from any hook drawn from it.

## Handoff

The finished index feeds directly into hook and script writing (an angle-bank or angle-mapping process, and from there into video/copy scripting) — the merged shortlist is written specifically so a creative team can brief from it the same afternoon, with every candidate already carrying its source, awareness level, and desire tags.
