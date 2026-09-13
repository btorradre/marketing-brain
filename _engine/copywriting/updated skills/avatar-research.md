---
name: avatar-research
description: Use this skill whenever conducting avatar research, market research, consumer intelligence, desire mapping, competitive brand analysis, sub-avatar profiling, or niche exploration. Triggers include requests to research an avatar, analyze a market, study a niche, profile a customer, map desires, find consumer language, do VOC research, analyze a competitor's audience, or explore a new product angle. Also trigger when the user says "research this," "who is the customer for X," "pull consumer language for X," "do a deep dive on X," or needs to understand a target audience before writing copy. This is the FIRST skill in the creative pipeline — it produces consumer intelligence that feeds hook-generation, long-form-copy, advertorial, video-ad-scripts, and listicle-builder skills. Always use before writing for a new avatar, product, or angle.
---

# Avatar Intelligence & Market Research — Complete System

This skill governs how to conduct deep consumer intelligence research for direct response marketing. It produces the raw material that every other skill in the creative pipeline depends on — the pain themes, consumer language, awareness levels, and angle strategy that make copy resonate instead of guess.

This skill is grounded in Eugene Schwartz's Breakthrough Advertising framework and ethnographic research methodology. Every insight must trace back to how real people actually talk about their problem in unfiltered environments — not how marketers describe them.

Read this entire file before beginning research. The methodology and output structure are interdependent.

---

## 0. WHEN TO USE THIS SKILL

This skill covers any research task where the goal is to understand a customer deeply enough to sell to them. That includes but is not limited to:

- **New avatar research** — First time building intelligence on a customer type for a new product or brand.
- **Sub-avatar profiling** — Breaking an existing avatar into narrower segments (e.g., splitting "GLP-1 users" into "GLP-1 users with hair loss" vs. "GLP-1 users with digestive issues").
- **Desire mapping** — Identifying what a known avatar actually wants, in their words, when the product or angle is shifting.
- **Competitive brand analysis** — Studying who a competitor's audience is, what they respond to, and where the gaps are.
- **Niche exploration** — Evaluating whether a market is worth entering by understanding the depth, language, and sophistication of the people in it.
- **Angle validation** — Testing whether a specific angle or mechanism will land with an audience by checking it against real consumer language.

The output is always the same structure. The depth varies based on what's needed — a sub-avatar profile might skip Section 4 demographics if the parent avatar already covers it. A competitive analysis might weight Section 5 (sophistication) more heavily. But the framework stays consistent.

---

## 1. CRITICAL DEFINITIONS

These definitions prevent the most common failure mode: conflating pain points with angles. Every section of the output depends on keeping these clean.

> **CORRECTED 2026-08-17.** The definitions below previously called the argumentative claim the "angle" and rejected the problem as a mere pain point. That is backwards against how the ad account is actually built, and it collapsed the ad set layer. The corrected four-layer vocabulary is canonical in `.claude/skills/direct-response-os/modules/angle-schema.md`. Use that. This file is retained for its research methodology; for evidence-backed avatar research use the `avatar-research-deep` skill, which scrapes real sources instead of composing plausible quotes.

**AVATAR** = Who she is. One specific person in a specific situation. Becomes one CBO campaign.

**PAIN POINT** = The symptom or problem the avatar experiences, in her words. "My knees hurt." "My hair is falling out." Pain points are DESCRIPTIVE.

**ANGLE** = The specific problem, or the psychological reason she would buy. It is the same thing as a pain point, named as something you can buy an ad set against. One avatar has several. Becomes one ad set.

- RIGHT (an angle): "Knee pain when climbing stairs"
- ALSO RIGHT (a different angle, same avatar): "Knee pain that wakes you at night"

**HOOK** = The claim, reframe, or mechanism statement that opens the ad and argues about the angle. One angle has several. Becomes one ad variation.

- RIGHT (a hook, not an angle): "Your knee pain isn't caused by age, it's cartilage decay that started years before you noticed."

**MECHANISM** = The biological, chemical, or systemic explanation for WHY the problem exists. An ingredient inside a hook, and what makes it believable. It must align with what the avatar already believes about their body, so the belief shift feels like a revelation rather than a contradiction.

**CONCEPT** = The narrative vehicle that delivers the hook. Story structure, framing device, the way in. Three concepts can carry the same hook and arrive at it differently.

**GOLDEN NUGGET** = The emotional motive underneath the angle. Not a layer, a depth requirement: the angle may sit at problem level, the nugget may not sit at topic level, or every hook written from it comes out shallow.

**MECHANISM** = The biological, chemical, or systemic explanation for WHY the problem exists. The mechanism is what makes the angle believable. "Cartilage decay" is a mechanism. "Inflammation" is a mechanism. The mechanism must align with what the avatar already believes about their body — the belief shift should feel like a revelation, not a contradiction.

**CONCEPT** = The narrative vehicle that delivers the angle. It's the story structure, the framing device, the "way in." Three different concepts can all use the same angle but arrive at it differently — through a personal story, through an exposé, through a demonstration.

---

## 2. RESEARCH METHODOLOGY

This analysis must be conducted as if 40+ hours were spent immersed in the communities where this avatar actually talks. The research is ethnographic — it prioritizes unfiltered consumer language over clinical descriptions or marketer summaries.

### Source Hierarchy (in priority order)

1. **Reddit** — Subreddit posts, comments, and AMAs. Prioritize long-form personal posts ("I just need to vent...," "Does anyone else..."), high-upvote comments that signal shared experience, and threads describing journeys or failed attempts. Reddit produces the most detailed, confessional language.

2. **Facebook Support/Interest Groups** — Private and public groups where the avatar seeks advice, validation, or community. These produce the most emotionally raw language because people feel they're speaking to "their people."

3. **Niche Forums & Communities** — Condition-specific forums, hobbyist boards, dedicated community sites (PatientLikeMe, RealSelf, BabyCenter, bodybuilding.com forums, etc.). These contain diary-style accounts of living with the problem.

4. **Review Platforms** — Amazon reviews (especially 2-3 star reviews of competing products), Trustpilot, app store reviews. These reveal what people hoped would work and exactly why it failed.

5. **YouTube & TikTok Comments** — Comments under relevant videos where people share unsolicited personal stories in response to content about the problem.

### Source Citation Rule

Throughout every section, when surfacing a phrase, behavior, or insight, tag it with its likely source type in brackets: [Reddit], [FB Group], [Amazon Review], [Forum], [YT Comment], [TikTok]. This forces traceability and prevents generic marketing-speak from contaminating the output.

### Web Search Protocol

When conducting this research with web search tools available, use targeted queries to find real consumer language:

- Search Reddit directly: `site:reddit.com [problem] [emotional keyword]`
- Search for review language: `"I tried" "[product category]" site:amazon.com`
- Search for community discussions: `"does anyone else" [problem]`, `"I'm so frustrated" [problem]`
- Search for journey posts: `"finally found" [solution category]`, `"nothing worked until" [problem]`
- Search for objections: `"is [product type] worth it" reddit`, `"[product type] scam"`

Run multiple searches across source types. Don't stop at the first result. The goal is saturation — enough exposure to the avatar's language that patterns emerge.

---

## 3. RESEARCH PRIORITY WEIGHTING

Not all sections carry equal weight. The output quality depends on spending the most time where it matters most.

| Section | Weight | Why |
|---|---|---|
| Pain Themes | 35% | The foundation. Everything else builds from pain understood at the identity level. |
| Consumer Language | 25% | The exact words that go into copy. Pre-validated emotional language. |
| Routine & Situation Discovery | 20% | Where and when pain hits — these become ad openings and story entry points. |
| Avatar Identity | 12% | Demographics and psychographics that shape targeting and voice. |
| Awareness & Sophistication | 8% | Schwartz placement that determines what kind of copy to write. |

---

## 4. OUTPUT STRUCTURE

The output follows seven sections. Every section must trace back to real consumer language. If a claim can't be sourced to a plausible community conversation, it doesn't belong in the output.

### PRE-RESEARCH STEP: COMMUNITY MAPPING

Before generating any themes, identify the specific communities this avatar inhabits. This grounds every subsequent section.

**Top 3-5 Subreddits:** Name the actual subs (e.g., r/GLP1_Ozempic, r/Supplements, r/SkincareAddiction). Explain briefly why each is relevant.

**Top 3-5 Facebook Group Types:** Describe the group archetype and likely name patterns (e.g., "GLP-1 Weight Loss Support — Tips & Advice," "Ozempic/Mounjaro Side Effects Discussion"). These won't be exact names since FB groups are private, but describe the type precisely enough that someone could find them.

**Top 2-3 Niche Forums/Sites:** Name specific community sites relevant to this avatar (e.g., PatientLikeMe, RealSelf, specific condition forums, hobbyist boards).

**Top Review Sources:** Identify where this avatar leaves reviews — specific Amazon product categories, app stores, Trustpilot for specific brands.

---

### SECTION 1: DEEP PAIN THEME SYNTHESIS (35%)

Source priority: Reddit long-form posts, FB group vents, niche forum diary threads.

Identify 5-8 recurring pain themes using the avatar's own consumer language. For each theme:

**Theme Title:** Write it as the avatar would post it — a quote, not a clinical label. This should read like a Reddit post title or the first line of a Facebook group vent. Example: "I hide my smile in every photo" — NOT "Low self-confidence about appearance."

**Behavioral Evidence:** 3-5 specific behaviors that prove this pain is real, sourced from described behaviors in posts and comments. Tag each with source type. (e.g., "Covers mouth when laughing [Reddit]," "Orders room-temperature water at restaurants to avoid tooth pain [FB Group]," "Has a folder of photo editing apps specifically for teeth [Forum]")

**Consumer Voice Quote:** One raw, emotional sentence that captures the theme — written as it would actually appear in a Reddit comment or Facebook group post. It should have the cadence, grammar, and emotional texture of a real person typing through frustration, not a copywriter crafting a line. Tag the likely source.

**Severity Ranking:** Rate each theme:
- **Surface-Level Frustration** — Annoying but not life-altering. They mention it casually.
- **Daily Disruption** — Actively interferes with routines, relationships, or decisions multiple times per week.
- **Identity-Level Pain** — Has changed how they see themselves. The problem IS who they are now, not just something they have.

**Hidden Shame Layer:** For each theme, identify what they would NEVER post publicly but clearly feel based on subtext and patterns across multiple posts. This is inferred from reading between the lines of dozens of posts on the same topic.

**Constraint:** At least 3 themes must reach Identity-Level Pain. If the research doesn't surface identity-level themes, the avatar may not be deep enough for direct response — flag this.

---

### SECTION 2: COMMON PHRASES & EMOTIONAL EXPRESSIONS (25%)

Source priority: Reddit comments, FB group replies, Amazon/Trustpilot reviews, YouTube/TikTok comments.

This section captures the literal language the avatar uses. Every phrase should sound like it was copy-pasted from a real post, not written by a marketer.

**A) Pain Language Bank (10-15 phrases)**

Organize by emotional intensity. Tag each with likely source.

- **Mild/Casual:** The way they mention it in passing or when downplaying. (e.g., "It's not the worst thing but..." [Reddit], "I've just learned to deal with it" [FB Group])
- **Moderate/Frustrated:** When actively seeking help or venting. (e.g., "I'm so sick of spending money on things that don't work" [Amazon Review], "It's starting to affect my relationship" [FB Group])
- **Severe/Desperate:** Late-night posts, rock-bottom confessions. (e.g., "I don't even recognize myself anymore" [Reddit], "I broke down crying in the bathroom again" [Forum])

**B) Metaphors & Descriptions (5-7)**

The analogies, metaphors, and vivid descriptions the avatar uses to explain their experience. These are gold for copy because they're pre-validated emotional language. (e.g., "It feels like needles through my teeth" [Reddit], "My body is basically betraying me at this point" [FB Group])

**C) Self-Talk Patterns (3-5)**

Internal dialogue statements inferred from confessional posts and "anyone else feel this way?" threads. The things people type when they think only strangers are reading. (e.g., "What's wrong with me that I can't just fix this?" [Reddit], "Maybe I'm just meant to be like this" [Forum])

**D) Trigger Phrases That Stop the Scroll (5)**

Raw phrases (NOT polished headlines) that would make this avatar stop scrolling because they feel personally called out. Each phrase must be directly derived from a specific phrase or pattern identified in A, B, or C above — cite which one it came from.

---

### SECTION 3: ROUTINE & SITUATION DISCOVERY — STORY ENTRY POINTS (20%)

Source priority: "Day in the life" Reddit posts, situational complaints in FB groups, journaling-style forum threads, "does anyone else" posts.

This section maps where and when the pain becomes acute. These moments become ad opening scenes, VSL hooks, and email subject lines.

**A) The Daily Friction Map**

Walk through a typical day and identify 3-5 specific moments where the problem creates friction. Each moment must be sourced from described real scenarios, not invented.

For each:
- **Time/Situation:** (e.g., "Morning — looking in the mirror before work" [Reddit])
- **What Happens:** The specific behavior or avoidance pattern described.
- **Internal Monologue:** What they're thinking/feeling — pulled from confessional post language about that specific moment.
- **Story Entry Point Potential:** High / Medium / Low. High = multiple people have described this exact moment independently across different threads.

**B) The "Worst Moments" (3 Peak Pain Situations)**

The situations where pain is at its absolute worst. Source from the posts that get the most engagement — the ones where dozens of people respond with "OMG this is exactly me." Describe each as a SCENE, not a summary.

**C) The Purchase Trigger Event**

The single most common event that pushes the avatar from passive suffering to active solution-seeking. Source from "what finally made you do something about it?" threads and "I finally decided to..." posts. Describe as a specific scene.

**D) The Objection Threads (3-5)**

What people in these communities say when someone recommends a product or solution like the one being researched. Find the recurring skepticism patterns from product recommendation threads.

---

### SECTION 4: AVATAR IDENTITY BREAKDOWN (12%)

Source priority: User flair, bios, self-descriptions in introductory posts, demographic patterns inferred from community context.

**A) Demographics & Situation**
- Age range, gender, income bracket, life stage — inferred from community demographics and self-reported details.
- Key life context that makes this problem worse RIGHT NOW (e.g., "Many posters mention this getting worse after pregnancy" [FB Group])

**B) Psychographic Profile**
- **Core Values:** What they value most — inferred from what they upvote, defend, and react to.
- **Identity Statement:** How they see themselves — pulled from self-descriptions. (e.g., "I'm a researcher — I've read every study on this" [Reddit])
- **Sources of Influence:** Specific platforms, communities, influencers, podcasts, or authorities they reference and trust. Name them.
- **Insider Language:** 5-10 niche-specific terms, abbreviations, or shorthand used within these communities.

**C) The Emotional Dimensions**
- **The "Hell" (Current State):** Visceral, specific description of what life feels like now — written as a synthesis of the worst posts across all communities. Second person.
- **The "Heaven" (Desired State):** Specific, tangible outcomes sourced from success posts and "what I wish I could do" comments. Not vague feelings — real described scenarios.
- **The Hidden Desire:** The selfish, unstated desire inferred from subtext across dozens of posts — the thing they describe around but never say directly.

---

### SECTION 5: AWARENESS LEVEL & MARKET SOPHISTICATION (8%)

Source priority: Product recommendation threads, "has anyone tried...?" posts, review-sharing behavior, community attitudes toward marketing.

**A) Schwartz Awareness Level**

Classify the avatar:
- **Unaware** — Doesn't know they have a solvable problem.
- **Problem-Aware** — Knows the problem, doesn't know solutions exist.
- **Solution-Aware** — Knows solution categories exist, hasn't chosen one.
- **Product-Aware** — Knows specific products, hasn't bought or is comparing.
- **Most Aware** — Has bought, is evaluating whether to buy again or switch.

Provide evidence from communities proving the classification. Estimate percentage breakdown across the community — where does the largest actionable segment sit?

**B) Market Sophistication (Level 1-5)**

Based on how many products/solutions are regularly discussed, compared, and dismissed:
- **Cynicism Indicators:** What specific claims or product types does the community actively mock, warn against, or downvote?
- **What Still Works:** Despite sophistication, what type of messaging, proof, or framing still gets genuine engagement?

**C) The "Silent Questions" (Top 3)**

The immediate objections this avatar has upon seeing an ad — sourced from "is this legit?" posts and product recommendation thread objections.

---

### SECTION 6: ANGLE & CONCEPT STRATEGY (Applied Output)

This section translates all research into a creative strategy. This is where the research becomes actionable for the copy skills.

**Dominant Community Narrative:** Before selecting an angle, identify the single most dominant narrative or belief about this problem within the communities researched. This is the "community consensus" — the thing that would get upvoted to the top. The angle must either align with this narrative or strategically challenge it.

**The Angle — choose ONE type:**

| Type | Core Frame |
|---|---|
| **Mechanism Angle** | "It's not your fault — it's [biological/chemical process]." |
| **Identity Shift Angle** | "This problem is attacking who you are." |
| **Enemy/Exposé Angle** | "You're being lied to / exploited by [entity]." |
| **Struggle Angle** | "Validation of your past failures — they weren't your fault." |
| **Reframe Angle** | "Everything you believe about the cause is wrong." |

For the selected angle:
- **Why This Angle Wins (Community Evidence):** Explain why it resonates based on specific patterns in the communities. (e.g., "The Struggle Angle wins because the most common post type in r/[sub] is 'I've tried everything' — this community's dominant emotion is exhausted hope, not ignorance.")
- **The Hook Statement:** Write the specific angle statement based on the type.
- **Mechanism Alignment Check:** Does this angle's implied mechanism align with what the avatar already believes about their body/situation? If it contradicts their existing beliefs, flag the friction point and explain how to bridge it.

**The Concepts — 3 Narrative Vehicles:**

Each concept delivers the same angle through a different story structure:

1. **Concept 1 (Direct/Logical):** For high-awareness, skeptical community members. Leads with evidence.
2. **Concept 2 (Story/Narrative):** Built from an actual story pattern observed in the communities. Leads with a relatable character.
3. **Concept 3 (Demonstration/Visual):** Based on the type of proof this community actually responds to. Leads with showing, not telling.

For each concept, write a 2-3 sentence description of the narrative arc, not the full copy.

---

### SECTION 7: "FOR DUMMIES" SUMMARY

The quick-reference output for anyone on the team who needs to write for this avatar without reading the full analysis.

- **Avatar Snapshot:** One sentence defining who this person is — written as if describing the "typical poster" in the primary subreddit or FB group.
- **The "Way In":** The single most effective emotional trigger, tied directly to a Pain Theme from Section 1 and an Entry Point from Section 3, using language from Section 2.
- **The "Big No":** One thing you must NEVER say — sourced from words, phrases, or tones that get downvoted, criticized, or dismissed in these communities. Explain why it kills the sale.
- **Community Cheat Sheet:** Top 3 subreddits, top 3 FB group types, top 3 phrases to use, top 3 phrases to avoid — the minimum viable intelligence for anyone writing copy for this avatar.

---

## 5. SCOPE VARIATIONS

Not every use of this skill requires the full seven-section output. Here's how to scale:

**Full Avatar Research (new product, new market):** All 7 sections, full depth. This is the default.

**Sub-Avatar Profile (narrowing an existing avatar):** Sections 1, 2, 3, and 6 at full depth. Section 4 can reference the parent avatar and note only what's DIFFERENT for the sub-segment. Section 5 only if the sub-avatar's awareness level differs from the parent.

**Competitive Brand Analysis (studying who a competitor sells to):** Sections 1, 2, 4, and 5 at full depth. Section 3 focused on what triggers purchase of the competitor's product specifically. Section 6 focused on identifying gaps — angles the competitor ISN'T using.

**Desire Mapping (new angle for existing avatar):** Sections 1 and 2 at full depth focused on the specific desire. Section 6 at full depth with multiple angle options explored. Other sections abbreviated or skipped.

**Niche Viability Check (should we enter this market?):** Sections 1, 4, and 5 at full depth. If the pain themes don't reach Identity-Level and the sophistication is Level 4+, flag the niche as potentially not viable for direct response.

When the user's request implies a scope variation, confirm which variation before starting.

---

## 6. QUALITY GATES

Before delivering the output, run these checks:

1. **Source Tracing:** Every pain theme, phrase, and behavior must have a source tag. If more than 20% of claims lack source tags, the research isn't grounded enough — go back and source them.

2. **Pain Point / Angle Separation:** Check that Section 1 contains only pain points (symptoms, problems, suffering) and Section 6 contains only angles (narratives, claims, reframes). If any pain theme reads like an angle, rewrite it.

3. **Consumer Voice Authenticity:** Read every "Consumer Voice Quote" out loud. If it sounds like a copywriter wrote it, rewrite it. Real people use incomplete sentences, hedging language, typos in emotional posts, and self-deprecating humor. The quotes should feel raw.

4. **Identity-Level Pain Threshold:** At least 3 pain themes must reach Identity-Level. If they don't, either the research isn't deep enough or the avatar isn't a strong direct response target — flag which one.

5. **Mechanism Alignment:** The angle's implied mechanism must not contradict what the avatar already believes about their body or situation. If it does, the copy will trigger defensive rejection instead of a belief shift. Flag any misalignment.

6. **Schwartz Consistency:** The awareness level classification must be consistent with the type of language used. If the community discusses specific product brands by name, they're not Problem-Aware — they're at minimum Solution-Aware. Don't underclassify.
