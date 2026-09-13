# SOP: Reddit Scraping & Avatar Language Mining

## Objective
Extract raw avatar data, emotional language, pain points, failed solutions, daily routines, and market sophistication from Reddit communities aligned to our niche targets (cholesterol, menopause, neuropathy, back pain, weight loss, skincare, supplements, women's health, men's health, joint care, sleep, digestive health, cognitive function).

---

## Target Subreddits by Niche

### Pain & Joint Care
- **r/neuropathy** — neuropathy sufferers, nerve pain experiences, medication side effects, daily life challenges
- **r/backpain** — back pain causes, failed treatments, exercises, daily routines, work impact
- **r/arthritis** — joint pain, inflammation, lifestyle adjustments, medication experiences
- **r/fibromyalgia** — chronic pain, fatigue, treatment attempts, emotional burden

### Women's Health
- **r/menopause** — menopause symptoms, hot flashes, mood changes, sexual function, HRT discussions
- **r/PCOS** — polycystic ovary syndrome, weight loss resistance, fertility concerns, medication experiences
- **r/IBS** — digestive issues, food triggers, medication trials, daily life impact

### Cholesterol & Cardiovascular
- **r/cholesterol** — high cholesterol, statin side effects, lifestyle modifications, doctor interactions
- **r/blood_pressure** — hypertension, medication compliance, lifestyle changes

### Weight Loss & Metabolic
- **r/loseit** — weight loss strategies, failed diets, calorie counting, exercise routines, psychological barriers
- **r/fitness** — exercise adherence, nutrition timing, supplement use, body composition goals
- **r/EatCheapAndHealthy** — budget-conscious nutrition, healthy eating on low income

### Skincare & Beauty
- **r/skincare** — skin conditions, product experiences, dermatologist recommendations, routine building
- **r/tretinoin** — prescription skincare, aging concerns, skin barrier issues, treatment timelines
- **r/30PlusSkincare** — aging skin, anti-aging strategies, preventative care, concerns by age

### Supplements & Wellness
- **r/Supplements** — supplement efficacy, quality concerns, stacking strategies, absorption issues
- **r/Nootropics** — cognitive enhancement, brain health, focus and memory, supplement combinations
- **r/keto** — ketogenic diet, weight loss, energy levels, health markers, sustainability concerns

### Sleep & Recovery
- **r/sleep** — insomnia, sleep quality, medication side effects, sleep routines, fatigue
- **r/DeepSleep** — sleep optimization, REM/NREM quality, supplements for sleep

### Men's Health
- **r/menshealth** — prostate health, erectile function, testosterone levels, lifestyle factors
- **r/testosterone** — hormone levels, TRT discussions, energy and vitality concerns

### Digestive & Gut Health
- **r/IBS** — irritable bowel syndrome, food sensitivities, medication trials
- **r/GERD** — acid reflux, lifestyle modifications, medication side effects
- **r/constipation** — digestive issues, medication-induced constipation, dietary solutions

---

## What to Extract (The 7-Category Framework)

### 1. Pain Themes
**Goal:** Identify the top 3-5 pain points mentioned across threads in the subreddit.

Extract:
- Physical pain characteristics (location, intensity, timing, triggers)
- Emotional burden (frustration, hopelessness, social isolation, embarrassment)
- Functional limitations (daily activities affected, work impact, sexual function, sleep quality)
- Social/relational impact (family dynamics, relationship strain, social withdrawal)
- Timeline questions (how long ago did this start? how long have treatments been failing?)

Example from r/neuropathy:
> "10 years of neuropathy. Gabapentin stopped working. Can't feel my feet. Walking is torture. My wife thinks I'm just lazy now."

**Extract:**
- Duration: 10 years
- Failed solution: Gabapentin
- Physical pain: feet numbness, walking difficulty
- Emotional: frustration (torture, stopped working)
- Social: relationship strain (wife thinks lazy)

### 2. Common Phrases & Emotional Language
**Goal:** Capture exact words, phrases, and emotional intensity the avatar uses.

Extract:
- Exact phrases (not paraphrased): "my doctor won't listen," "I've tried everything," "nothing works anymore," "at my wit's end"
- Emotional descriptors: "desperate," "hopeless," "frustrated," "exhausted," "embarrassed," "ashamed"
- Intensity markers: "can't sleep," "can't work," "ruining my life," "affecting everything"
- Doctor language: "my doc says," "my rheumatologist thinks," "my dermatologist recommended"
- Timeline language: "for years," "since last month," "after age 50," "in my 40s"

Create a running list of 10-15 exact phrases per scrape session.

### 3. Routine Discovery
**Goal:** Understand the avatar's daily routine, constraints, and behavior patterns.

Extract:
- Morning routine (how do they start the day? what hurts first?)
- Work routine (type of work, pain triggers, accommodations needed)
- Medication/supplement routine (when taken, with food, timing)
- Exercise/movement routine (what they try, what fails, what helps)
- Sleep routine (bedtime, wake time, sleep quality, factors affecting sleep)
- Social/relational routine (time with family, social engagement, intimacy)
- Meal timing and food patterns (breakfast time, eating frequency, meal preparation)
- Pain management routine throughout day

Example from r/backpain:
> "I wake up stiff. 30 min stretching helps. Can't sit more than 2 hours at desk. Afternoon walks. Ice at night. Some days I just can't move."

**Extract Routine:**
- Wake: stiff, needs 30 min stretching
- Work: can't sit > 2 hrs (desk job)
- Movement: afternoon walks help
- Night: ice, then sleep

### 4. Avatar Breakdown (Demographics & Psychographics)
**Goal:** Piece together who the avatar is based on self-reported data.

Extract:
- Age range (stated, implied, or inferred from references)
- Gender (explicit or inferred)
- Occupation/income level (type of work, flexibility, financial constraints)
- Relationship status (single, married, dependent care)
- Prior experience with health/wellness (fitness background, supplement knowledge, health literacy)
- Sophistication level (do they use medical jargon? understand mechanism of action? or do they want simple solutions?)
- Motivation driver (pain relief, appearance, performance, vitality, doctor approval)

### 5. Schwartz Stage Assessment
**Goal:** Identify what awareness/belief stage the avatar is in.

Using [[DR-SOP-Obsidian.md|Schwartz stages]]:

- **Stage 1 (Unaware):** "I didn't know this was a symptom." Rare in Reddit, but note if found.
- **Stage 2 (Problem Aware):** "I have neuropathy, but I'm not sure what causes it or what I can do." Seeking diagnosis/confirmation.
- **Stage 3 (Solution Aware):** "I know about Gabapentin, physical therapy, etc., but none of it works for me." Frustrated with known solutions.
- **Stage 4 (Ready to Change):** "I'm willing to try something different if it actually works." Open to new approaches, but skeptical.
- **Stage 5 (Transformation Ready):** "I've done everything the doctor said, I'm ready to take control myself." Highest agency, willing to experiment.

Determine stage for each thread based on question asked and tone.

### 6. Angle Strategy Signals
**Goal:** Identify what angles might resonate with this avatar segment.

Based on pain themes, routines, and stage, signal potential angles:

- **Mechanism-focused** ("This is how it actually works...") — For Stage 4-5, higher health literacy
- **Villain-focused** ("Here's what's keeping you stuck...") — For Stage 3, frustrated with standard solutions
- **Transformation-focused** ("Here's what's possible...") — For Stage 5, change-ready
- **Social proof-focused** ("Real people doing this...") — For Stage 2-3, doubt about solutions
- **Simplicity-focused** ("One simple fix...") — For lower health literacy, overwhelm
- **Lifestyle integration-focused** ("Fits your routine...") — For Stage 3-4, worried about friction

### 7. For Dummies Summary
**Goal:** Create a digestible snapshot for Creative Strategist.

Template:
- **Who:** Brief avatar description (age, occupation, pain profile)
- **What Hurts:** Top 3 pain points in order of intensity
- **What They've Tried:** Medications, supplements, behavioral interventions, and why they failed
- **Current Routine:** How they manage pain daily
- **Belief Stage:** What Schwartz stage they're in and why
- **Language:** 3-5 exact phrases they use
- **Angle Play:** What angle(s) might resonate
- **Red Flags:** Emotions that signal vulnerability (desperation, hopelessness) — use with ethical caution

---

## Reddit Scraping Execution Protocol

### Step 1: Select Target Subreddit
- Choose from list above based on strategic priority
- Check if subreddit has been scraped in last 7 days (avoid redundancy)

### Step 2: Browse Threads
- Sort by "Hot" (last 24-48 hours) for trending conversations
- Look for threads with 20+ comments (active community response)
- Prioritize threads that ask pain-focused or solution-focused questions
- Minimum 10 threads per scraping session

### Step 3: Extract Raw Data
For each thread:
1. Record thread title
2. Extract OP (original poster) description of pain/problem
3. Read top 20 comments for community response
4. Note pain language, failed solutions, routines, stage markers, exact phrases

### Step 4: Apply 7-Section Framework
Organize extractions into:
1. Pain Themes
2. Common Phrases & Language
3. Routine Discovery
4. Avatar Breakdown
5. Schwartz Stage Assessment
6. Angle Strategy Signals
7. For Dummies Summary

### Step 5: Output Template (See Template Section Below)

---

## Cadence & Quality Thresholds

### Weekly Deep Scrape (2 hours)
- 2-3 subreddits per session
- 10+ threads per subreddit
- Full 7-section framework applied
- Output: `reddit_NICHE_YYYYMMDD.md` with intel-drop template

### Daily Monitoring (30 minutes)
- Check top 5 target subreddits
- Capture any new pain themes, exact phrases, or Schwartz stage shifts
- Note if any signals contraddict previous scrapes
- Output: Quick tags in existing intel-drop or flag for next deep scrape

### Quality Thresholds
- **Avatar Breakdown:** Must include age, occupation, pain profile, relationship to healthcare
- **Routine Discovery:** Must include 3+ daily routine details (morning, work, evening, medication)
- **Exact Phrases:** At least 5 phrases captured, not paraphrased
- **Schwartz Assessment:** Must assign stage (1-5) with justification
- **Angle Signals:** Must tie angles to observed pain themes and stage

**Red Flag:** If a scrape session doesn't identify 2+ new pain themes or 3+ new phrases, expand thread sample size or switch subreddit.

---

## Output Template: Reddit Scrape Intel-Drop

```markdown
---
date: YYYY-MM-DD
type: reddit-scrape
brands: []
niche: [cholesterol | menopause | neuropathy | back-pain | weight-loss | skincare | supplements | etc.]
tags: [#avatar-language, #pain-themes, #routine-discovery, #stage-assessment]
source: reddit.com/r/[SUBREDDIT]
confidence: high
---

# Reddit Scrape: [NICHE] — [DATE]

## Summary
Brief 2-3 sentence overview of what this scrape revealed about the market.

Example: "r/neuropathy shows Stage 3-4 avatars frustrated with gabapentin ineffectiveness. Strong emotional language around social isolation and work impact. Routines heavily pain-management-focused."

---

## 1. Pain Themes (Top 5)

### Pain Theme 1: [Name]
- **Quotes:** Direct quotes from threads
- **Intensity:** How painful is this theme in community?
- **Frequency:** How often mentioned across threads?
- **Impact:** What does this pain affect in daily life?

Example:
### Pain Theme 1: Medication Failure
- **Quotes:** "Gabapentin doesn't work anymore," "No relief after 2 years," "My doc says there's nothing else"
- **Intensity:** Very high (frustration, hopelessness)
- **Frequency:** 8 out of 10 threads
- **Impact:** Work performance, daily function, quality of life, relationship strain

### Pain Theme 2: [Name]
... continue for 5 themes

---

## 2. Common Phrases & Emotional Language

### Exact Phrases (Not Paraphrased)
- "I've tried everything"
- "My doctor won't listen"
- "Nothing works anymore"
- "At my wit's end"
- "Ruining my life"
- [Add 5-10 more]

### Emotional Language Intensity Map
| Emotion | Frequency | Example Quotes |
|---------|-----------|---|
| Frustration | 9/10 | "So tired of this," "Fed up," "Nothing helps" |
| Hopelessness | 7/10 | "Will this ever end?," "Don't see a future," "Giving up" |
| Isolation | 6/10 | "Feel alone in this," "No one understands," "Withdrawing from life" |
| Shame | 5/10 | "Embarrassed," "Can't work like I used to," "Wife thinks I'm lazy" |
| Determination | 8/10 | "Will find a solution," "Trying everything," "Not giving up yet" |

---

## 3. Routine Discovery

### Morning Routine
- Wake time: [TIME]
- First action: [What does avatar do first? Stretch? Medicate? Pain assessment?]
- Pain level at wake: [Low | Medium | High]
- Activities before work: [Exercise? Shower? Medication timing?]
- Mood at start of day: [Positive | Neutral | Negative]

Example:
- Wake time: 6:30 AM
- First action: Stretch for 30 minutes
- Pain level at wake: High (stiffness)
- Activities before work: Stretch, ice, hot shower, take gabapentin
- Mood at start of day: Neutral to negative (pain-dependent)

### Work/Productivity Routine
- Occupation: [Job type]
- Work schedule: [9-5? Flexible? Remote?]
- Pain-limiting factors: [Can't sit > 2 hours? Need to stand? Lying down?]
- Management tactics: [Stretches at desk? Medication timing? Breaks?]
- Functional impact: [Can do full job? Limited? Considering leaving?]

### Evening/Sleep Routine
- Dinner time: [TIME]
- Evening activities: [Stretching? Walking? Rest? Socializing?]
- Pain management evening: [Ice? Heat? Medication? Supplements?]
- Bedtime: [TIME]
- Sleep quality: [Good | Okay | Poor] [Why?]

### Medication/Supplement Routine
- Time of day: [Morning? Evening? With meals? Bedtime?]
- Frequency: [Once daily? Twice? As needed?]
- Perception: [Helpful? Side effects? Inconsistent?]
- Compliance challenges: [Easy or forgets?]

### Exercise/Movement Routine
- Type of movement: [Walking? Stretching? Yoga? Swimming?]
- Frequency: [Daily? Weekly? As pain allows?]
- Duration: [Minutes]
- Effectiveness: [Helps? No change? Makes worse?]

---

## 4. Avatar Breakdown

### Demographics
- **Age Range:** [e.g., 45-65, implied from context]
- **Gender:** [Male | Female | Mixed mentions]
- **Occupation:** [e.g., Desk job, retail, retired]
- **Income Level (Inferred):** [Budget-conscious? Premium-seeking? Doesn't mention cost?]
- **Relationship Status:** [Single | Married | Divorced | Has dependents?]

### Psychographics
- **Health Literacy:** [Low (wants simple solutions) | Medium (understands some mechanism) | High (researches deeply)]
- **Prior Experience with Health:** [No background | Some fitness/supplement experience | Long history of health optimization]
- **Locus of Control:** [External (trusts doctors) | Internal (wants to control own health) | Mixed]
- **Openness to Non-Traditional Solutions:** [Skeptical | Open-minded | Actively seeking alternative approaches]
- **Motivation Driver:** [Pain relief | Appearance | Vitality | Doctor approval | Avoiding surgery | Self-reliance]

### Health Sophistication
- Do they mention understanding mechanisms of action? (e.g., "nerve regeneration," "inflammation pathways")
- Do they research supplements or medications before asking?
- Do they question doctor's advice or accept it?
- Are they looking for data/studies to back solutions?

---

## 5. Schwartz Stage Assessment

### Identified Stage: [1 | 2 | 3 | 4 | 5]

### Stage Definition & Evidence
(From [[DR-SOP-Obsidian.md|Schwartz stages]])

**Stage [X]: [NAME]**
- **Definition:** [What is the avatar's awareness/readiness level?]
- **Evidence from threads:** [3-5 quotes showing they're in this stage]
- **Implication for angles:** [What angles would resonate with this stage?]

Example for Stage 3:
**Stage 3: Solution Aware, Frustrated**
- **Definition:** Avatar knows about standard treatments (Gabapentin, physical therapy) but they're failing. Frustrated, starting to doubt the system.
- **Evidence:** "Gabapentin doesn't work," "PT hasn't helped," "Nothing my doctor recommends works," "There must be something else"
- **Implication for angles:** Villain-focused (what's keeping you stuck?), mechanism-focused (here's why standard solutions fail), transformation-focused (there's another way)

---

## 6. Angle Strategy Signals

### Angles with High Resonance Potential

#### Angle 1: [Name]
- **Why resonant:** [Based on pain themes and stage]
- **Hook opportunity:** [How to lead with this angle?]
- **Avatar language to use:** [Phrases from Section 2]
- **Risk/consideration:** [Any red flags?]

Example:
#### Angle 1: "Why Gabapentin Stops Working (And What Actually Helps)"
- **Why resonant:** Stage 3 avatars actively frustrated with medication failure; deep pain around "nothing works anymore"
- **Hook opportunity:** "If Gabapentin used to help but doesn't anymore, here's what's happening..."
- **Avatar language to use:** "My doctor won't listen," "Nothing works anymore," "At my wit's end"
- **Risk/consideration:** Avoid insulting doctors; position as complementary, not replacement

#### Angle 2: [Name]
... continue for 2-3 angles maximum

---

## 7. For Dummies Summary

**Who:** Stage 3-4 avatars in r/neuropathy, typically 50-70, desk workers or manual laborers, 5-15 years with neuropathy.

**What Hurts (Top 3):**
1. Foot numbness and walking pain (physical + functional)
2. Doctor's inability to help (systemic frustration)
3. Isolation and relationship strain (social/emotional)

**What They've Tried (Why It Failed):**
- Gabapentin (worked initially, tolerance built, now ineffective)
- Physical therapy (temporary relief, not solving root problem)
- Dietary changes (tried, inconsistent results)
- Topical treatments (messy, doesn't work deep enough)

**Current Routine:**
- Morning: Stretch, ice, medicate
- Work: Limit sitting, movement breaks
- Evening: Ice, heat, medication
- Sleep: Disrupted by pain, poor quality

**Belief Stage:** Stage 3-4 (knows about standard solutions, frustrated, starting to seek alternatives, but still somewhat trusting of medical system)

**Language:**
- "Nothing works anymore"
- "My doc says there's nothing else"
- "At my wit's end"
- "Ruining my life"
- "Been dealing with this for years"

**Angle Play:**
- Villain-focused: "Why standard treatments fail for chronic neuropathy"
- Mechanism-focused: "How [Product] targets the actual problem, not just symptoms"
- Transformation-focused: "From numb and isolated to walking pain-free"

**Red Flags (Use Ethically):**
- Deep hopelessness ("don't see a future") — signals vulnerability
- Relationship strain ("wife thinks I'm lazy") — signals life impact beyond pain
- Financial desperation (trying to avoid surgery) — signals urgency but also price-sensitivity

---

## Key Takeaways for Creative Strategist

### What's Changed Since Last Scrape?
- New pain themes? New stage distribution? New emotional language?

### What Should Creative Strategist Know?
- Specific angle opportunities
- Avatar language to use verbatim
- Sophisticated vs. simple positioning needed?
- Urgency level (transformation-ready vs. still exploring?)

### Files to Reference
- [[DR-SOP-Obsidian.md]] — For Schwartz stage interpretation
- [[Mechanism Reference Library_ Top 100 Examples.md]] — For mechanism alignment

---

## Next Steps

- [ ] Share with Creative Strategist
- [ ] Tag as #avatar-language, #pain-themes, #stage-assessment
- [ ] Monitor r/[SUBREDDIT] weekly for stage shifts
- [ ] Compare with angle-saturation-map to identify gaps

```

---

## Pro Tips for High-Quality Scrapes

1. **Read Carefully, Not Quickly** — Extract exact phrases, don't paraphrase. The avatar's words are more valuable than your interpretation.

2. **Thread Quality > Thread Quantity** — One deep, 50-comment thread beats 5 shallow threads. Look for engaged communities.

3. **Track Emotion Intensity** — Note which pain themes trigger the strongest emotional language. Those are the leverage points.

4. **Routine Specificity** — "They exercise" is useless. "They walk 30 minutes every morning because morning stiffness is worst, then sit-based work triggers afternoon pain" is actionable.

5. **Stage Assignment is Critical** — If you can't confidently assign Schwartz stage to a thread, re-read or skip it. Stage determines everything about angle strategy.

6. **Compare Across Subreddits** — Same pain theme across r/neuropathy and r/fibromyalgia might show different stages or routine patterns. Cross-reference.

7. **Watch for New Phrases Each Scrape** — If you're capturing the same phrases weekly, either you're in the same threads or the market is saturated. Move to new subreddits if needed.

8. **Red Flags on Health Literacy** — If avatars in r/cholesterol use medical jargon (LDL, HDL, oxidation), mechanism-focused angles work. If they don't, simplify to villain or transformation angles.

---

## Forbidden Patterns in Reddit Scraping

- **Generic pain mentions** ("I have back pain") without specificity — skip unless tied to routine or failure story
- **Doctor worship** ("My doctor is amazing, I trust everything") — note as external locus of control, but don't expect angle receptivity
- **Unattributed health claims** — If someone says "X cured me," note the claim but verify before using in copy
- **Obvious bot/spam comments** — Ignore completely; don't extract

---

## Notes

Reddit is the unfiltered avatar voice before it becomes a customer. The language here will show up in testimonials, reviews, and support emails. Capture it precisely. The routines here will inform product positioning and integration strategy. The stage assessment here determines whether [[DR-SOP-Obsidian.md|angles]] need to educate or transform.
