---
name: avatar-research
description: Use this skill whenever conducting avatar research, market research, consumer intelligence, desire mapping, competitive brand analysis, sub-avatar profiling, or niche exploration. Triggers include requests to research an avatar, analyze a market, study a niche, profile a customer, map desires, find consumer language, do VOC research, pull voice-of-customer data, build a VOC corpus, run an awareness-level breakdown, size awareness stages, or explore a new product angle. Also trigger when the user says "research this," "who is the customer for X," "pull consumer language for X," "do a deep dive on X," "how much of the market is problem-aware," or needs to understand a target audience before writing copy. This is the FIRST skill in the creative pipeline — it produces consumer intelligence that feeds hook-generation, long-form-copy, advertorial, video-ad-scripts, and listicle-builder skills. Always use before writing for a new avatar, product, or angle.
---

# Avatar Intelligence & Market Research — Complete System

This skill governs how to conduct deep consumer intelligence research for direct response marketing. It produces the raw material that every other skill in the creative pipeline depends on — the pain themes, consumer language, awareness distribution, and angle strategy that make copy resonate instead of guess.

This skill is grounded in Eugene Schwartz's Breakthrough Advertising framework and ethnographic research methodology. Every insight must trace back to how real people actually talk about their problem in unfiltered environments — not how marketers describe them.

The skill runs in **two phases**. Phase 1 COLLECT builds a raw voice-of-customer corpus (the 50-100 pages of verbatim data). Phase 2 SYNTHESIZE turns that corpus into the seven-section intelligence report. Collection and synthesis are kept strictly separate — that separation is what produces volume instead of a thin summary.

Read this entire file before beginning. The methodology and output structure are interdependent.

---

## 0. WHEN TO USE THIS SKILL

This skill covers any research task where the goal is to understand a customer deeply enough to sell to them:

- **New avatar research** — First time building intelligence on a customer type for a new product or brand.
- **VOC corpus build** — The explicit ask for a large body of raw voice-of-customer data (50-100 pages) before any synthesis.
- **Awareness sizing** — Estimating what percentage of the market sits at each Schwartz awareness stage and where the addressable money is.
- **Sub-avatar profiling** — Breaking an existing avatar into narrower segments (e.g., splitting "GLP-1 users" into "GLP-1 users with hair loss" vs. "GLP-1 users with digestive issues").
- **Desire mapping** — Identifying what a known avatar actually wants, in their words, when the product or angle is shifting.
- **Competitive brand analysis** — Studying who a competitor's audience is, what they respond to, and where the gaps are.
- **Niche exploration** — Evaluating whether a market is worth entering by understanding the depth, language, and sophistication of the people in it.
- **Angle validation** — Testing whether a specific angle or mechanism will land by checking it against real consumer language.

---

## 1. CRITICAL DEFINITIONS

These definitions prevent the most common failure mode: conflating pain points with angles. Every section of the output depends on keeping these clean.

**PAIN POINT** = The symptom or problem the avatar experiences. It's what they feel and complain about. "My knees hurt." "I can't lose weight." Pain points are DESCRIPTIVE. They name the suffering.

**ANGLE** = The psychological entry point used to get attention. A NARRATIVE about the problem — a claim, a reframe, an explanation. Angles are ARGUMENTATIVE. They make a case.
- WRONG (pain point labeled as angle): "Knee Pain"
- RIGHT (actual angle): "Your knee pain isn't caused by age — it's caused by cartilage decay that started years before you noticed."

**MECHANISM** = The biological, chemical, or systemic explanation for WHY the problem exists. The mechanism is what makes the angle believable. It must align with what the avatar already believes about their body — the belief shift should feel like a revelation, not a contradiction.

**CONCEPT** = The narrative vehicle that delivers the angle. The story structure, the framing device, the "way in." Three concepts can use the same angle but arrive at it differently.

**VOC EXTRACTION** = A single captured unit of consumer language: a verbatim emotionally-loaded fragment plus its metadata (source, awareness stage, intensity, theme). The corpus is a stack of these. The synthesis is built entirely from them.

---

## 2. RUN MODES & THE TWO-PHASE ARCHITECTURE

### The two phases

- **Phase 1 — COLLECT.** Build the VOC corpus: hundreds of tagged verbatim extractions saved to a file. NO synthesis, NO theme essays, NO angle strategy. Just disciplined extraction at volume. The corpus is a real deliverable, not scratch work.
- **Phase 2 — SYNTHESIZE.** Read the corpus and produce the seven-section intelligence report (Section 5). Every synthesized claim cites the extraction numbers that support it.

Never synthesize while collecting. The instinct to start writing themes mid-collection is what caps the corpus at five pages. Hold the line.

### Run modes — pick one based on the volume needed

| Mode | Target | Mechanics | Use when |
|---|---|---|---|
| **Quick Pull** | ~8-20 pages | Single session. One pass of the query matrix, fetch the top threads, synthesize at the end. | Fast directional read, sub-avatar, angle validation, time-boxed. |
| **Deep Corpus** | 50-100 pages | Ralph loop. Fresh context each pass, append to the corpus file, stop at saturation. THEN synthesize in a final pass. | The full VOC ask. Realistic only as a loop — one session cannot hold 100 pages of fetched content in context. |

If the user asks for "50-100 pages," "a big VOC corpus," or "as much data as possible," default to **Deep Corpus**. State up front that this runs as a loop and the corpus accumulates across passes.

### Page-count reality check

One chat session has a practical ceiling on `web_search` / `web_fetch` calls, and much of Reddit/Facebook is gated or paywalled to scrapers. A single pass realistically yields ~10-25 pages. 50-100 pages is reached by **accumulation across loop passes**, not by one heroic session. Set this expectation explicitly rather than implying a single run will hit 100 pages.

---

## 3. PHASE 1 — THE VOC CORPUS ENGINE

This is the new heavy machinery. Its only job is volume of real, tagged, verbatim consumer language.

### 3.1 Seed the pain hypotheses

Before searching, write 5-8 hypothesized pain themes for the avatar (one line each). These are guesses — they exist only to seed the query matrix and will be confirmed, killed, or replaced by the data. Each hypothesis becomes a query cluster in 3.3.

### 3.2 Source map

Identify the specific places this avatar talks, in priority order. Reddit and forums are the richest because the content is long-form and fetchable.

1. **Reddit** — Long-form personal posts ("I just need to vent…," "Does anyone else…"), high-upvote shared-experience comments, journey/failed-attempt threads. The single best source.
2. **Niche forums & communities** — Condition or hobby-specific boards (PatientLikeMe, RealSelf, BabyCenter, bodybuilding.com, dedicated condition forums). Diary-style accounts.
3. **Review platforms** — Amazon (especially 2-3 star reviews of competing products), Trustpilot, app store reviews. Reveal what people hoped for and exactly why it failed.
4. **Quora & Q&A** — Problem-stage language; people describing a problem before they know solutions exist.
5. **YouTube & TikTok comments** — Unsolicited personal stories under relevant videos.
6. **Facebook support/interest groups** — Emotionally raw, but mostly gated. Describe the archetype; capture what is publicly visible.
7. **Competitor ad copy (optional accelerator)** — If a Meta Ad Library tool (e.g., TrendTrack `search_ads` / `creative_inspiration_pack`) or competitor email tooling is available, validated competitor language is a fast source of pre-tested phrasing. Tag these `[Competitor Ad]` — they are inspiration, not organic VOC, and never count toward the organic awareness distribution in 3.6.

### 3.3 The query matrix

Search is systematic, not ad-hoc. Build the query set as a matrix: **(pain hypothesis) × (source) × (emotional/awareness register)**. Run the full matrix; reformulate misses with different terms before moving on.

The five core query families (use the compact templates below; the exhaustive bank lives in `references/voc-query-matrix.md` — load it during collection):

- **Problem-language** (feeds problem-aware count): `site:reddit.com [symptom] "does anyone else"`, `"why does my [X]" [symptom]`, `"[symptom]" "so frustrated"`
- **Solution-category** (feeds solution-aware count): `"best [category] for [problem]" reddit`, `"does [category] actually work"`, `"nothing worked until" [problem]`
- **Brand/product** (feeds product-aware + most-aware count): `"[brand] reviews" reddit`, `"[brand A] vs [brand B]"`, `"[product type] worth it"`
- **Journey/victory**: `"finally found" [solution]`, `"I finally decided to" [problem]`, `"what finally made you"`
- **Objection/skepticism**: `"[product type] scam"`, `"is [category] legit" reddit`, `"waste of money" [category]`

Run multiple searches per family. The goal is **saturation** — enough exposure that new searches stop surfacing new language.

### 3.4 Fetch, don't snippet

Search snippets are 1-2 sentences — too thin to build a corpus from. For every high-value hit (a long Reddit thread, a dense review page, a Quora answer with many comments), `web_fetch` the full page and mine it. A single fetched thread can yield 10-30 distinct extractions — this is the main lever that turns 5 pages into 50. Budget most of the collection effort on fetching and mining, not on running more searches.

### 3.5 Extraction schema

Every captured unit is one row. Capture the emotionally-loaded fragment **verbatim and short** (the punchy phrase is what's useful for copy anyway — not the whole rambling post); paraphrase surrounding context in your own words. Keep verbatim fragments brief and attributed.

```
| #  | Verbatim fragment (short) | Source | Context (paraphrased) | Awareness | Intensity | Theme |
```

- **#** — sequential ID. Synthesis cites these.
- **Verbatim fragment** — the actual words, kept short (the loaded phrase, not the paragraph).
- **Source** — [Reddit] / [Forum] / [Amazon] / [Trustpilot] / [Quora] / [YT] / [TikTok] / [FB] / [Competitor Ad].
- **Context** — one paraphrased line: who's speaking, what thread, what prompted it.
- **Awareness** — U / PA / SA / ProdA / MA (see 3.6). Tag at capture — do not defer.
- **Intensity** — Mild / Moderate / Severe.
- **Theme** — short tag linking to a pain hypothesis or a new emergent theme.

### 3.6 Awareness tagging at capture (this is what makes the % breakdown rigorous)

Tag every extraction with the awareness stage the *speaker* is at, judged by their language — not the stage you wish they were at:

- **U — Unaware:** Describes symptoms as normal/unsolvable; no sense a fix exists. ("I guess this is just getting older.") Rare in active communities by definition.
- **PA — Problem-Aware:** Names the problem, actively bothered, but doesn't reference solution categories. ("Why does my stomach do this every morning??")
- **SA — Solution-Aware:** Discusses categories/approaches generically, no specific brand. ("Has anyone tried fiber supplements for this?")
- **ProdA — Product-Aware:** Names specific brands/products, comparing or considering. ("Is Metamucil better than [brand]?")
- **MA — Most-Aware:** Has bought; evaluating repurchase, switching, stacking. ("Been on [brand] 3 months, here's my update.")

This tag does double duty: it builds the corpus AND generates the raw counts that produce Section 5's percentage breakdown. The percentages literally fall out of `COUNT(stage) / COUNT(total)`.

### 3.7 Saturation protocol & volume targets

**Volume targets** (use both proxies):
- **Quick Pull:** 60-150 extractions (~8-20 pages).
- **Deep Corpus:** 300-600 extractions (~50-100 pages of structured corpus at ~6 extractions/page with context).

**Saturation is reached when BOTH are true:**
1. Volume target hit, AND
2. The last full query-matrix pass surfaced no new pain theme and no materially new language (diminishing returns).

If volume is hit but new themes are still emerging, keep going past target. If themes saturate early, stop early and note it — a thin market is itself a finding (flag for niche viability).

### 3.8 Loop mode (Ralph) mechanics — for Deep Corpus

Each pass runs in **fresh context**. Do not re-read the whole corpus each pass (it won't fit and it wastes context). Instead:

1. Read only the corpus file's **header block**: the running theme index, the highest extraction #, the awareness tally, and the saturation tracker.
2. Run the **next query batch** (the matrix cell not yet covered — tracked in the header).
3. Fetch and mine; **append** new extractions (continuing the # sequence). Append-only — never rewrite earlier rows.
4. Update the header: new theme tags, new max #, updated awareness tally, which matrix cells are now done, saturation check.
5. Stop when 3.7 is satisfied. Then trigger a final **synthesis pass** (Phase 2) that reads the full corpus.

This is the only architecture that genuinely reaches 50-100 pages without blowing context.

### 3.9 Corpus file format (the deliverable)

Save as `voc-corpus-[avatar].md`. Structure:

```
# VOC Corpus — [Avatar / Product]
## HEADER (update every pass)
- Total extractions: N
- Awareness tally: U __ | PA __ | SA __ | ProdA __ | MA __
- Theme index: [tag — count] ...
- Matrix coverage: [families/sources/registers covered vs pending]
- Saturation: NOT SATURATED / SATURATED (reason)

## EXTRACTIONS
| # | Verbatim fragment | Source | Context | Awareness | Intensity | Theme |
| 1 | ... | [Reddit] | ... | PA | Severe | morning-dread |
...
```

The corpus is presented to the user as its own file alongside the synthesis report.

---

## 4. PHASE 2 — SYNTHESIS WEIGHTING

Once the corpus is saturated, synthesize. Spend effort proportional to weight. Awareness is now a major section, not an afterthought.

| Section | Weight | Why |
|---|---|---|
| Pain Themes | 30% | The foundation. Pain understood at the identity level. |
| Consumer Language | 22% | The exact words that go into copy. Pre-validated emotional language. |
| Routine & Situation Discovery | 18% | Where and when pain hits — ad openings and story entry points. |
| Awareness Distribution & Sophistication | 20% | Sizes the market by stage, locates the addressable money, and dictates the lead. |
| Avatar Identity | 10% | Demographics and psychographics that shape targeting and voice. |

Every synthesized claim must cite supporting extraction #s, e.g. "(#12, #47, #203)". Untraceable claims get cut.

---

## 5. OUTPUT STRUCTURE

Seven sections, all built from the corpus.

### PRE-RESEARCH STEP: COMMUNITY MAPPING

Identify the specific communities the avatar inhabits (this also confirms the Phase-1 source map was right).

**Top 3-5 Subreddits:** Actual subs (e.g., r/GLP1_Ozempic, r/Supplements). Why each is relevant.
**Top 3-5 Facebook Group Types:** Archetype + likely name patterns (groups are private; describe precisely enough to find them).
**Top 2-3 Niche Forums/Sites:** Specific community sites.
**Top Review Sources:** Specific Amazon categories, app stores, Trustpilot brands.

---

### SECTION 1: DEEP PAIN THEME SYNTHESIS (30%)

Source priority: long-form posts, vents, diary threads. Identify 5-8 recurring pain themes in the avatar's own language. For each:

**Theme Title:** Written as the avatar would post it — a quote, not a clinical label. ("I hide my smile in every photo" — NOT "Low self-confidence.")
**Behavioral Evidence:** 3-5 specific proving behaviors, each cited to extraction #s and source. ("Covers mouth when laughing (#22 [Reddit]); orders room-temp water to avoid tooth pain (#88 [FB]).")
**Consumer Voice Quote:** One raw verbatim fragment from the corpus that captures the theme. Cite the #.
**Severity Ranking:** Surface-Level Frustration / Daily Disruption / Identity-Level Pain.
**Hidden Shame Layer:** What they'd never post but clearly feel, inferred from subtext across multiple extractions.

**Constraint:** At least 3 themes must reach Identity-Level Pain. If they don't, flag that the avatar may not be deep enough for DR.

---

### SECTION 2: COMMON PHRASES & EMOTIONAL EXPRESSIONS (22%)

The literal language, pulled straight from the corpus. Every phrase cites an extraction #.

**A) Pain Language Bank (12-18 phrases)** — organized by intensity:
- **Mild/Casual** ("I've just learned to deal with it" #__)
- **Moderate/Frustrated** ("I'm so sick of spending money on things that don't work" #__)
- **Severe/Desperate** ("I don't even recognize myself anymore" #__)

**B) Metaphors & Descriptions (5-7)** — the analogies they use ("it feels like needles through my teeth" #__). Pre-validated emotional language.

**C) Self-Talk Patterns (3-5)** — internal dialogue from confessional posts ("what's wrong with me that I can't fix this?" #__).

**D) Trigger Phrases That Stop the Scroll (5)** — raw phrases (NOT polished headlines) that make this avatar feel called out. Each must derive from a specific phrase in A/B/C — cite which #.

---

### SECTION 3: ROUTINE & SITUATION DISCOVERY — STORY ENTRY POINTS (18%)

Maps where/when pain becomes acute. These become ad opening scenes, VSL hooks, subject lines.

**A) The Daily Friction Map** — 3-5 specific moments, each sourced. Time/Situation, What Happens, Internal Monologue (from corpus language), Story Entry Point Potential (High = multiple people described this exact moment independently — cite the #s).
**B) The "Worst Moments" (3 Peak Pain Situations)** — sourced from highest-engagement posts. Describe as SCENES, not summaries.
**C) The Purchase Trigger Event** — the single most common event pushing from passive suffering to active solution-seeking. Cite the journey-post #s.
**D) The Objection Threads (3-5)** — recurring skepticism when products like this are recommended.

---

### SECTION 4: AVATAR IDENTITY BREAKDOWN (10%)

**A) Demographics & Situation** — age/gender/income/life-stage inferred from community context; the life context making this worse RIGHT NOW.
**B) Psychographic Profile** — Core Values; Identity Statement (self-descriptions, cite #s); Sources of Influence (name the platforms/people they trust); Insider Language (5-10 niche terms/abbreviations).
**C) The Emotional Dimensions** — The "Hell" (current state, 2nd person, synthesized from worst posts) and the "Heaven" (desired state — real described scenarios from success posts, not vague feelings); The Hidden Desire (the selfish unstated want inferred across many posts).

---

### SECTION 5: AWARENESS DISTRIBUTION & MARKET SOPHISTICATION (20%)

This is the full awareness breakdown. It answers: *what percentage of the market sits at each Schwartz stage, where is the addressable money, and what should the lead target?*

**A) The Awareness Distribution — % at each stage**

Derive the percentages from **two independent signals**, then reconcile. Do not pull numbers from the air; show the basis.

*Signal 1 — Corpus Distribution (bottom-up).* Count the awareness tags from Phase 1: `% = COUNT(stage) / COUNT(total)`. This is the distribution of *vocal* people. Known skew: it over-represents PA/SA (the bothered and the searching post most) and under-represents U (the unaware don't post about a problem they don't know they have) and somewhat MA (satisfied buyers go quiet). State the raw counts.

*Signal 2 — Demand Signal (top-down).* Gauge relative search demand across the three query classes from 3.3: problem-language vs. category-language vs. brand-language. Judge magnitude from results depth, autocomplete breadth, "People Also Ask" density, and — if a keyword/volume tool is available — actual volumes. The ratio approximates the *spending-intent* distribution and corrects the corpus's vocal-minority skew.

*Reconcile* into a single estimate with a per-stage confidence tag:

| Stage | Est. % | Confidence | Evidence basis | Reachable w/ paid? | Copy implication |
|---|---|---|---|---|---|
| Unaware | __% | Low* | residual / category-size logic | Hard (needs disruption) | Symptom-callout, "is this normal?" leads |
| Problem-Aware | __% | __ | corpus PA count + problem-query demand | Yes — best DR target | Story + mechanism long-form |
| Solution-Aware | __% | __ | corpus SA count + category-query demand | Yes | Mechanism differentiation, "why X beats Y category" |
| Product-Aware | __% | __ | corpus ProdA + brand-query demand | Yes (expensive — crowded) | Comparison, proof, offer/guarantee |
| Most-Aware | __% | __ | corpus MA count | Yes (retention/LTV) | Reorder, stack, loyalty |

\* Unaware is structurally undercounted — it cannot be measured directly from communities. Estimate it as a residual against total category size and flag low confidence explicitly. Never present a precise Unaware %.

**State plainly that this is a triangulated estimate, not a census.** The value is the *relative* shape and where the gap is — not decimal precision.

**B) "Where the Money Is" — the addressable block**

The biggest segment is not always the right target. Identify the largest segment that is BOTH sizable AND reachable with paid traffic at a sane cost. In most DR markets that's Problem-Aware. Name it and justify from the table.

**C) Awareness Arbitrage — the gap**

Where are competitors fishing vs. where is the under-served volume? Competitors usually cluster at Product-Aware (reviews, comparison, "us vs. them") because it's closest to the sale. The cheaper, larger, under-served block is usually Problem-Aware. State explicitly: *competitors are concentrated at [stage]; the under-served volume sits at [stage]; the arbitrage is to lead at [stage].*

**D) Market Sophistication (Level 1-5)**

Based on how many solutions are regularly discussed, compared, and dismissed:
- **Cynicism Indicators:** specific claims/product types the community mocks, warns against, downvotes (cite #s).
- **What Still Works:** the messaging/proof/framing that still earns genuine engagement despite sophistication (cite #s).

**E) The Awareness × Sophistication Lead Matrix**

Awareness sets *what they know*; sophistication sets *how tired they are of the pitch*. Together they pick the lead:

| | Low Sophistication (L1-2) | High Sophistication (L3-5) |
|---|---|---|
| **Problem-Aware** | Direct problem promise | New mechanism / unique reframe |
| **Solution-Aware** | "Best of category" claim | Mechanism differentiation, enemy/exposé |
| **Product-Aware** | Brand + offer | Comparison + heavy proof + guarantee |

State which cell this avatar lands in and therefore the recommended lead type.

**F) The "Silent Questions" (Top 3)**

The immediate objections on seeing an ad — sourced from "is this legit?" extractions and recommendation-thread objections (cite #s).

---

### SECTION 6: ANGLE & CONCEPT STRATEGY (Applied Output)

Translates research into creative strategy.

**Dominant Community Narrative:** The single most dominant belief about this problem in the communities — the thing that would get upvoted to the top. The angle must align with it or strategically challenge it. Cite the #s that establish it.

**The Angle — choose ONE type:**

| Type | Core Frame |
|---|---|
| **Mechanism Angle** | "It's not your fault — it's [biological/chemical process]." |
| **Identity Shift Angle** | "This problem is attacking who you are." |
| **Enemy/Exposé Angle** | "You're being lied to / exploited by [entity]." |
| **Struggle Angle** | "Your past failures weren't your fault." |
| **Reframe Angle** | "Everything you believe about the cause is wrong." |

For the selected angle:
- **Why This Angle Wins (Community Evidence):** tie to specific corpus patterns and the awareness distribution. (e.g., "Struggle Angle wins: the dominant post type is 'I've tried everything' (#s), and 64% of the corpus is Problem-Aware — the emotion is exhausted hope, not ignorance.")
- **The Hook Statement:** the specific angle statement.
- **Mechanism Alignment Check:** does the implied mechanism align with what the avatar already believes? If it contradicts existing beliefs, flag the friction and how to bridge it. (Mechanisms must align with the avatar's existing beliefs so the belief shift feels seamless.)
- **Awareness Fit:** confirm the angle is pitched at the stage identified in 5B/5C as the lead.

**The Concepts — 3 Narrative Vehicles** (same angle, different structure):
1. **Direct/Logical** — for skeptical high-awareness members. Leads with evidence.
2. **Story/Narrative** — built from an actual story pattern in the corpus. Leads with a relatable character.
3. **Demonstration/Visual** — based on the proof this community responds to. Leads with showing.

2-3 sentences of arc per concept, not full copy.

---

### SECTION 7: "FOR DUMMIES" SUMMARY

Quick-reference for anyone writing for this avatar without reading the full report.

- **Avatar Snapshot:** one sentence — the "typical poster" in the primary community.
- **Awareness One-Liner:** "X% problem-aware, lead at [stage]; competitors crowd [stage]." The single most important strategic fact.
- **The "Way In":** the most effective emotional trigger — a Section 1 pain theme × a Section 3 entry point × Section 2 language.
- **The "Big No":** the one thing never to say — sourced from what gets downvoted/dismissed (cite #s). Explain why it kills the sale.
- **Community Cheat Sheet:** top 3 subreddits, top 3 FB group types, top 3 phrases to use, top 3 to avoid.

---

## 6. SCOPE VARIATIONS

Scale the synthesis (Phase 2). Collection volume scales with the chosen run mode in Section 2.

**Full Avatar Research (new product/market):** All 7 sections, full depth. Deep Corpus collection. Default.
**Sub-Avatar Profile:** Sections 1, 2, 3, 5(A-C), 6 at depth. Section 4 references the parent, notes only differences. Reuse the parent's corpus and collect a focused top-up on the sub-segment.
**Competitive Brand Analysis:** Sections 1, 2, 4, 5 at depth. Section 3 focused on the competitor's purchase trigger. Section 6 focused on gaps the competitor isn't using. Lean on competitor-ad and review sources.
**Desire Mapping (new angle, existing avatar):** Sections 1, 2, 6 at depth on the specific desire. Reuse existing corpus; top-up collect on the new desire.
**Niche Viability Check:** Sections 1, 4, 5 at depth. If pain doesn't reach Identity-Level and sophistication is L4+, flag the niche as weak for DR.

When the request implies a variation, confirm which before starting collection.

---

## 7. QUALITY GATES

Before delivering, run every check:

1. **Corpus Volume Gate:** Deep Corpus must hit 300-600 extractions (~50-100 pages) or document why saturation came early. Quick Pull must hit 60-150. If short, collection isn't done — loop again.
2. **Verbatim Discipline:** Captured fragments are short, real, and attributed — not paraphrases dressed as quotes and not whole reproduced posts. If a "quote" reads like a copywriter wrote it, it's not from the corpus — cut or re-source.
3. **Source Tracing:** Every pain theme, phrase, and behavior cites extraction #s. If >20% of synthesis claims lack #s, it isn't grounded — go back.
4. **Awareness Method Gate:** The distribution shows BOTH signals (corpus count + demand), per-stage confidence tags, raw counts, and the explicit "triangulated estimate, not a census" caveat. Unaware is never given a precise %. If the percentages appear without a derivation, they're invalid.
5. **Pain Point / Angle Separation:** Section 1 = pain points only; Section 6 = angles only. Rewrite any leakage.
6. **Identity-Level Threshold:** ≥3 Identity-Level pain themes, or flag the avatar as shallow for DR.
7. **Mechanism Alignment:** The angle's implied mechanism must not contradict the avatar's existing beliefs. Flag misalignment.
8. **Schwartz Consistency:** Awareness classification matches the language. If the community names specific brands, they're at minimum Product-Aware — don't underclassify.
