# SOP: Winning Ad Download & Cataloging

## Objective
Systematically download, catalog, and analyze winning ads across formats (long-form copy, video transcripts, advertorials, static images) to build a proprietary library of proven creative patterns, mechanisms, and angles for reference and inspiration by the Creative Strategist.

---

## What Qualifies as "Winning"

An ad qualifies as "winning" based on combined signals:

### Primary Signals
1. **Run Time Duration** (Strongest Signal)
   - Ads running 4+ weeks indicate basic performance (low bar)
   - Ads running 8+ weeks indicate strong performance (validated by spend)
   - Ads running 12+ weeks indicate exceptional performance (likely still profitable)
   - Ads still running after 16+ weeks are franchise winners (proven long-term ROI)

2. **Mechanism Score** (Secondary Signal)
   - Combined Logical Coherence + Market Resonance score of 15+ indicates a winning mechanism
   - Novelty: Mechanism not yet saturated in competitor landscape

3. **Angle Freshness** (Secondary Signal)
   - Angle not oversaturated in [[angle-saturation-map.md|angle saturation map]]
   - Differentiated positioning vs. competitors using similar angles

### Supporting Signals
- **Library Indicators** (if visible in Meta Ad Library)
  - Multiple language variations (indicates multi-market testing)
  - Frequent updates to creative (indicates active optimization)
  - Large creative set (5+ ad variations, indicates committed spend)

- **Avatar Resonance** (from Reddit scrapes)
  - Mechanism directly addresses pain theme identified in Reddit
  - Language matches avatar voice from [[reddit-scraping.md|reddit scrapes]]
  - Belief shift aligns with avatar's Schwartz stage

### Disqualifying Factors
- Ad running for 2-3 weeks only (likely still testing, not proven winner)
- Generic hook/angle/mechanism (appears in 5+ competitors)
- Mechanism score below 12 (weak Coherence + Resonance)
- Outdated visual/copy (indicates brand shifting away from this creative)

---

## Download Process by Format

### Format 1: Long-Form Copy Ads

**Source:** Meta Ad Library, Facebook ads library by brand, screenshots

**Download Process:**

1. **Identify Candidate**
   - Find ad in Meta Ad Library running 8+ weeks
   - Verify mechanism score 15+
   - Check against [[angle-saturation-map.md|angle saturation map]] for freshness

2. **Extract Full Copy**
   - Read headline
   - Read body copy (all sections)
   - Extract CTA (call-to-action)
   - Note any embedded images/visuals referenced
   - Screenshot for backup if needed

3. **Analyze Structure**
   - Identify hook (opening line)
   - Identify main sections (problem, villain, mechanism, social proof, offer, CTA)
   - Note copy flow/structure (problem-agitate-solve model? Or different?)
   - Assess copy length (short form <200 words | medium form 200-600 | long form 600+)

4. **Create Markdown File**
   - Use naming convention: `brand_copy_XX_first_words_of_hook.md`
   - Include YAML frontmatter (see Required Frontmatter section below)
   - Preserve original copy exactly (don't edit or rewrite)
   - Add Analysis Note section (see template below)

**Example: amala_health Long-Form Copy Ad**

```markdown
---
date: 2026-03-20
type: ad-download
format: long-form-copy
brand: amala_health
hook_type: villain-reveal
angle: "Why medications fail and what actually works"
mechanism: plant-sterol-alternative-to-statins
villain_types: [medication-failure, doctor-ignorance, symptom-only-thinking]
product_integration_position: late-stage
awareness_level: 3
sophistication_stage: 3
run_time: 12-weeks
run_time_signal: established-winner
source_url: meta-ad-library
confidence: high
tags: [#mechanism-scoring, #winning-ad, #cholesterol-niche]
---

# Ad: "The Cholesterol Medication Your Doctor Won't Talk About"
**Brand:** amala_health
**Format:** Long-form copy
**Estimated Run Time:** 12+ weeks

---

## Original Copy

[Full ad copy here, preserved exactly]

Headline:
The cholesterol medication your doctor won't talk about...

Body:
[Full copy sections...]

CTA:
Click below to discover the plant-based alternative that works...

---

## Analysis Note

### Hook Breakdown
- **Hook:** "The cholesterol medication your doctor won't talk about..."
- **Type:** Villain reveal (doctor as incomplete authority)
- **Mechanism:** Doctor is hiding/avoiding a solution
- **Emotional Trigger:** Frustration (doctors know more than they tell) + Hope (solution exists)

### Structure Analysis
- **Opening Hook:** Villain reveal (5 words)
- **Section 2:** Problem amplification (neuropathy medications fail, statins have side effects)
- **Section 3:** Villain expansion (why doctors don't recommend alternative)
- **Section 4:** Mechanism introduction (how plant sterols work differently)
- **Section 5:** Social proof (testimonials of success)
- **Section 6:** Transformation promise ("Cholesterol below 160 in 6 weeks")
- **Section 7:** Risk reversal (60-day money-back guarantee)
- **Section 8:** CTA (Click here for exclusive access)
- **Structure Type:** Problem-Villain-Mechanism-Social Proof-Guarantee-CTA (7-point formula)

### Mechanism Scoring
- **Type:** Ingredient-based mechanism (plant sterols vs. statin mechanism)
- **Logical Coherence:** 8 (specific biochemical claim, plausible, backed by plant sterol research)
- **Market Resonance:** 8 (avatars with statin side effects would embrace "same benefit, no side effects" claim)
- **Combined Score:** 16 (winning mechanism)

### Angle Assessment
- **Primary Angle:** "Natural/plant-based alternative to medication"
- **Saturation Status:** Moderate (3-4 competitors using this angle in cholesterol niche)
- **Differentiation:** Uses "plant sterol + bioavailability optimization" (specific mechanism, not generic "natural")
- **Competitive Threat:** Medium (angle isn't new, but mechanism specificity creates differentiation)

### Villain Archetype
- **Primary Villain:** Doctor as incomplete expert (knows standard treatment, withholds alternatives)
- **Secondary Villain:** Medication design failure (statins fail because they numb the problem, not solve it)
- **Emotional Resonance:** High (Stage 3 avatars frustrated with doctors; Stage 4 avatars suspicious of medication-only approach)

### Belief Shift
- **Current Belief:** "My doctor knows all available cholesterol options; statins are my only choice"
- **New Belief:** "There's a proven alternative to statins that my doctor may not recommend; I can control cholesterol naturally"
- **Shift Mechanism:** Education (how plant sterols work) + Authority (doctor endorsement in copy) + Social proof (testimonials)

### Product Integration
- **Position:** Late-stage (80% of copy is about problem/villain/mechanism; product introduced at 80% mark)
- **Style:** Problem-solving (here's what solves your statin side effects without doctor pushback)
- **Offer Framing:** Risk-reversal (60-day guarantee) + Exclusivity ("available only for [timeframe]")

### Copy Mechanics
- **Sentence Structure:** Mix of short (1-3 word) emotional hooks + medium (10-15 word) explanatory sentences
- **Active Voice:** "Doctors won't tell you..." vs. "You haven't been told..." = Active (punchy, emotional)
- **Power Words:** "Medication," "alternative," "fails," "scientifically proven," "exclusive," "access"
- **Emotional Language:** "Your doctor won't..." (exclusion/frustration), "Finally..." (relief), "Proven..." (authority)

### Why This Ad Wins
1. **High mechanism score (16)** — Specific, plausible mechanism that avatars care about
2. **Villain specificity** — Not "doctors are bad," but "doctors have blind spots" (more believable)
3. **Stage alignment** — Targets Stage 3-4 avatars with "alternatives exist" positioning
4. **Proof integration** — Testimonials + scientific backing without being preachy
5. **Long run time** — 12+ weeks indicates sustained ROI (avatar problem statement is accurate)

### Vulnerabilities
- **Risk:** Doctor pushback ("Your doctor says...") might alienate avatars who trust their doctors
- **Limitation:** Plant sterol mechanism might not work for all cholesterol profiles (oversold?)
- **Competitor Risk:** As angle saturates, differentiation erodes

### Recommendations for Creative Strategist
- **Model For:** This ad structure (villain reveal → education → social proof → risk reversal) works for Stage 3 avatars frustrated with standard solutions
- **Adapt For:** Back pain (why physical therapy fails), neuropathy (why gabapentin stops working), menopause (why HRT isn't enough)
- **Avoid:** Using same villain structure if [Competitor] already dominates this angle in your niche

---

## Folder Destination
`/agents/market-analyst/intel-drops/ads/long-form-copy/amala_health/`

```

---

### Format 2: Video Transcripts

**Source:** Meta Ad Library, advertorial transcripts (if available), transcribed from video ads

**Download Process:**

1. **Identify Candidate**
   - Find video ad in Meta Ad Library running 8+ weeks
   - Verify mechanism score 15+
   - Note video length (15-30 sec = short form | 60-90 sec = medium form | 3+ min = long form/advertorial)

2. **Obtain Transcript**
   - If transcript available: extract from advertorial PDFs in `/advertorial/references/`
   - If no transcript: extract from `/video ads/references (transcripts)/` (Balmbare 19, myNuora 29)
   - If not transcribed: Note in metadata that transcript is not available; include visual description instead

3. **Extract Video Metadata**
   - Duration: [seconds]
   - Visual style: [animation | talking head | testimonial | before-after | lifestyle | product demo]
   - Voiceover gender/tone: [authority | friendly | empathetic | urgent]
   - Music/sound design: [None | background music | sound effects | narrated]
   - Visual transitions: [Cuts | Fades | Motion graphics]

4. **Create Markdown File**
   - Use naming convention: `brand_video_XX_first_words_of_hook.md`
   - Include YAML frontmatter (see Required Frontmatter section below)
   - Preserve transcript exactly
   - Add Analysis Note section (see template below)

**Example: boostiva Video Transcript**

```markdown
---
date: 2026-03-20
type: ad-download
format: video-transcript
brand: boostiva
video_length_seconds: 120
visual_style: talking-head-testimonial
hook_type: transformation-promise
angle: "Cognitive restoration without medication"
mechanism: mitochondrial-ATP-restoration
villain_types: [brain-fog-normalization, aging-acceptance]
product_integration_position: middle-stage
awareness_level: 4
sophistication_stage: 4
run_time: 10-weeks
run_time_signal: established-winner
source_url: meta-ad-library
confidence: high
tags: [#mechanism-scoring, #winning-video, #cognitive-niche, #transformation-angle]
---

# Video Transcript: "Forget Everything You Know About Memory Loss"
**Brand:** boostiva
**Format:** Video (120 seconds)
**Visual Style:** Talking head testimonial + before-after sequence
**Estimated Run Time:** 10+ weeks

---

## Video Metadata

- **Duration:** 2 minutes (120 seconds)
- **Visual Style:** Talking head (woman, 55-65, professional setting) + before-after sequences + product demo
- **Voiceover:** Woman, 55-65, warm tone, slow delivery (emphasizes credibility)
- **Music:** Soft background, increases at transformation moments
- **Transitions:** Cuts between testimonial segments; fade-in for before-after visuals
- **Visual Content:** [0-5s] Title card "Forget Everything You Know About Memory Loss" [5-30s] Woman speaking directly to camera [30-60s] Before-after sequences (woman struggling with memory, then confident) [60-90s] Product reveal and mechanism explanation [90-120s] CTA to website

---

## Transcript (Exact)

[Full transcript here, speaker labels + exact words]

**[0:00-0:05]**
Title Card: "Forget Everything You Know About Memory Loss"

**[0:05-0:30]**
[Woman, 55-65, professional setting, direct eye contact]

"I used to think memory loss was just part of aging. That I had to accept it. But after I learned about the real cause, everything changed."

**[0:30-0:60]**
[Before-after sequence: woman looking confused at computer, then confidently solving a puzzle]

"Memory loss isn't a brain problem. It's a MITOCHONDRIAL problem."

[Visual: animation showing mitochondria inside brain cell]

"Your brain cells need energy to function. Mitochondria are the power plants. When they get tired, your memory fails."

**[0:60-0:90]**
[Woman back on camera]

"What shocked me was that doctors don't test mitochondrial function. They just tell you memory loss is normal for your age."

[Visual: product bottle appears in hand]

"But there's something you can do. It's called ATP restoration."

**[0:90-0:120]**
[Woman holding product, speaking with confidence]

"I took this every morning. In six weeks, my husband said, 'You're back.' I could remember conversations. I could focus on work again."

[Final visual: website URL + phone number]

"Visit [website] to learn how to restore your cognitive function naturally."

---

## Analysis Note

### Hook Breakdown
- **Hook:** "Forget everything you know about memory loss"
- **Type:** Transformation promise + villain reveal (aging acceptance is wrong)
- **Mechanism:** Memory loss is not brain aging; it's mitochondrial failure
- **Emotional Trigger:** Hope (I'm not losing my mind, it's fixable) + Empowerment (I can act on this)

### Video Structure Analysis
- **0-5s:** Hook (title card, curiosity built)
- **5-30s:** Problem + personal stake (woman credibly states memory loss belief; audience identifies)
- **30-60s:** Villain reveal + mechanism introduction (aging belief is wrong; mitochondria is real cause)
- **60-90s:** Authority building (doctors miss this) + solution hint (ATP restoration exists)
- **90-120s:** Transformation proof (testimonial + results) + CTA

### Mechanism Scoring
- **Type:** Process-based (mitochondrial energy restoration)
- **Specificity:** Specific (mitochondria, ATP, energy production in brain cells) but simplified for lay audience
- **Logical Coherence:** 7 (mechanism is real science, but simplified explanation lacks rigor; average avatar won't understand ATP deeply)
- **Market Resonance:** 9 (avatars desperate for cognitive restoration; mitochondrial framing feels new/scientific vs. generic "brain health")
- **Combined Score:** 16 (winning mechanism, high resonance overcomes moderate coherence)

### Angle Assessment
- **Primary Angle:** "Cognitive restoration through mitochondrial energy, not medication"
- **Saturation Status:** Emerging (few competitors positioning on mitochondrial mechanism; most use "brain health" generically)
- **Differentiation:** Specific mechanism (mitochondria) + clear villain (doctor ignorance) = differentiated
- **Competitive Advantage:** Blue ocean potential; not yet oversaturated

### Villain Archetype
- **Primary Villain:** Aging acceptance ("memory loss is normal at your age")
- **Secondary Villain:** Doctor ignorance (doctors don't test mitochondrial function; they assume it's inevitable decline)
- **Emotional Resonance:** High (Stage 4-5 avatars ready to reject "aging is inevitable" narrative)

### Belief Shift
- **Current Belief:** "Memory loss is inevitable aging; I have to accept it"
- **New Belief:** "Memory loss is fixable through mitochondrial restoration; I can actively restore my cognition"
- **Shift Mechanism:** Mechanism education (mitochondrial energy) + Testimonial (real woman's results) + Authority (scientific positioning)

### Product Integration
- **Position:** Middle-late stage (mechanism education first, product introduced 60% through)
- **Style:** Process-focused (here's the mechanism) → Outcome-focused (here's what's possible)
- **Reveal Timing:** Product bottle shown at 60% mark; prominent at 90% (CTA stage)
- **Visual Integration:** Product naturalistically held in testimonial (not jarring introduction)

### Video Mechanics
- **Voiceover Tone:** Warm, authoritative, slightly slower (implies thoughtfulness, credibility)
- **Visual Pace:** Slow reveals build curiosity; before-after sequences demonstrate transformation
- **Testimonial Structure:** Personal story (I believed X) → Education (here's why X is wrong) → Transformation (this is what changed it) → CTA
- **Music:** Emotional lift at transformation moments (primes viewer for hope/change)

### Why This Video Wins
1. **High mechanism score (16)** — Specific, credible mechanism that resonates with Avatar's desire for cognitive restoration
2. **Personal credibility** — Woman testimonial is believable (age-appropriate, professional setting, eye contact, no scripted feel)
3. **Villain clarity** — Not "pharmaceuticals bad," but "aging acceptance is wrong; mitochondria is the real issue" (credible villain)
4. **Stage alignment** — Targets Stage 4-5 avatars ready for alternative understanding of aging
5. **Educational + Emotional** — Mechanism education (credibility) + personal story (emotion) = powerful combination
6. **Long run time** — 10+ weeks indicates sustained avatar resonance

### Vulnerabilities
- **Risk:** Mitochondrial mechanism might oversimplify for health-literate avatars (looks pseudoscientific if not well explained)
- **Limitation:** Testimonial's "6 weeks to results" claim is aggressive; might disappoint avatars with slower recovery
- **Competitor Risk:** Mitochondrial angle will saturate as other brands copy it

### Recommendations for Creative Strategist
- **Model For:** This video structure (testimonial + mechanism education + transformation) works for Stage 4-5 avatars ready to reject aging narratives
- **Adapt For:** Neuropathy (why nerve cells fail, mitochondrial restoration heals nerves), menopause (mitochondrial energy + hormone balance), back pain (mitochondrial energy in spinal muscles)
- **Avoid:** Using same testimonial structure without strong mechanism education (testimonial alone is weak)

---

## Folder Destination
`/agents/market-analyst/intel-drops/ads/video-transcripts/boostiva/`

```

---

### Format 3: Advertorial PDFs

**Source:** `/advertorial/references/` (66 PDFs)

**Download Process:**

1. **Identify Candidate**
   - Find advertorial in reference folder
   - Extract brand, headline, key claims
   - Verify mechanism score 15+ (if extractable)
   - Check [[angle-saturation-map.md|angle saturation map]] for freshness

2. **Extract Key Content**
   - Headline
   - Subheadline
   - Opening section (problem statement)
   - Main body sections (mechanism, villain, social proof, results)
   - Product/offer section
   - CTA section
   - Visual descriptions (if any)

3. **Create Markdown File**
   - Use naming convention: `brand_advertorial_XX_headline_summary.md`
   - Include YAML frontmatter (see Required Frontmatter section below)
   - Preserve key content exactly
   - Add Analysis Note section (see template below)

---

### Format 4: Static Images/Graphics

**Source:** Meta Ad Library, brand websites, advertorial visuals

**Download Process:**

1. **Identify Candidate**
   - Find high-performing static image ad (8+ weeks run time)
   - Screenshot or download from Meta Ad Library
   - Verify mechanism/angle quality

2. **Download and Catalog**
   - Use naming convention: `brand_image_XX_brief_description.jpg`
   - Save in high resolution if possible
   - Include metadata (brand, visual elements, text on image)
   - Create accompanying .md file with analysis (below)

3. **Create Analysis File**
   - File: `brand_image_XX_brief_description.md` (analysis companion)
   - Include YAML frontmatter
   - Describe visual elements
   - Analyze headline/copy on image
   - Add Analysis Note section

---

## Required Frontmatter Fields

Every downloaded ad must include YAML frontmatter with these fields:

```yaml
---
date: YYYY-MM-DD
type: ad-download
format: [long-form-copy | video-transcript | advertorial | static-image]
brand: [Brand name from list]
hook_type: [curiosity | villain-reveal | problem-statement | transformation-promise | social-proof | statistics | question | benefit-statement]
angle: "[Primary angle description]"
mechanism: [mechanism-type: mechanism-specificity]
villain_types: [comma-separated list of villain archetypes]
product_integration_position: [early | middle | late | multi-stage]
awareness_level: [1-5]
sophistication_stage: [1-5]
run_time: [duration running in competitor landscape]
run_time_signal: [emerging-test | early-winner | established-winner | franchise-winner]
source_url: [exact URL or Meta Ad Library identifier]
confidence: [high | medium | low]
tags: [comma-separated tag list]
---
```

### Field Definitions

- **date:** Date you downloaded/cataloged the ad
- **type:** Always "ad-download" for this SOP
- **format:** Long-form copy, video transcript, advertorial, or static image
- **brand:** Exact brand name from 14-brand portfolio
- **hook_type:** [[DR-SOP-Obsidian.md|Hook category]] the ad uses
- **angle:** The primary argument/promise (e.g., "Why medications fail and what actually works")
- **mechanism:** What mechanism is claimed (e.g., "plant-sterol-alternative-to-statins")
- **villain_types:** [[DR-SOP-Obsidian.md|Villain archetypes]] the ad invokes
- **product_integration_position:** Where product appears in funnel (early = problem introduction; late = solution reveal)
- **awareness_level:** [[DR-SOP-Obsidian.md|Awareness level 1-5]] the ad targets
- **sophistication_stage:** [[DR-SOP-Obsidian.md|Schwartz stage 1-5]] the ad targets
- **run_time:** How long the ad has been running (e.g., "12-weeks", "8-weeks", "16+-weeks")
- **run_time_signal:** Strength indicator based on duration (emerging = 2-4 weeks; early winner = 4-8 weeks; established = 8-12 weeks; franchise = 12+ weeks)
- **source_url:** Where you found it (Meta Ad Library URL, brand website, advertorial PDF name)
- **confidence:** How confident are you this is a "winning" ad? (high = multiple signals; medium = 1-2 signals; low = single signal)
- **tags:** Filter tags for search and cross-referencing (#mechanism-scoring, #avatar-language, #urgent-creative-opportunity, #blue-ocean, etc.)

---

## Analysis Note Template (All Formats)

Every ad file must include an Analysis Note section with these subsections:

```markdown
## Analysis Note

### Hook Breakdown
- **Hook:** [Exact first line]
- **Type:** [Hook category from [[DR-SOP-Obsidian.md|hook types]]]
- **Mechanism:** [What's the implied mechanism?]
- **Emotional Trigger:** [What emotion does it activate?]

### Structure Analysis
- **Format-Specific Structure:** [How is the ad structured? Problem-solution? Villain-mechanism-proof?]
- **Flow:** [Does it follow a known formula?]
- **Length Assessment:** [Short/medium/long for the format]

### Mechanism Scoring
- **Type:** [Ingredient | Process | System | Behavioral]
- **Logical Coherence:** [1-9] (Does it make sense?)
- **Market Resonance:** [1-9] (Do avatars care?)
- **Combined Score:** [2-18]

### Angle Assessment
- **Primary Angle:** [What's the central argument?]
- **Saturation Status:** [Emerging | Moderate | Saturated] (Reference [[angle-saturation-map.md]])
- **Differentiation:** [What makes this angle distinct?]
- **Competitive Threat:** [Low | Medium | High]

### Villain Archetype
- **Primary Villain:** [What's the enemy?]
- **Secondary Villain:** [Optional; any supporting villain]
- **Emotional Resonance:** [Low | Medium | High]

### Belief Shift
- **Current Avatar Belief:** [What do they currently believe?]
- **New Belief (Ad's Goal):** [What should they believe?]
- **Shift Mechanism:** [How does ad facilitate shift?]

### Product Integration
- **Position:** [Early | Middle | Late | Multi-stage]
- **Style:** [Ingredient-focused | Lifestyle | Problem-solving | Outcome-focused]
- **Reveal Timing:** [What % through ad is product introduced?]
- **Framing:** [Risk-reversal | Scarcity | Guarantee | Result-centric]

### Why This Ad Wins
[3-5 bullets explaining what makes this ad effective]

### Vulnerabilities
[Any potential weaknesses or risks in the positioning]

### Recommendations for Creative Strategist
- **Model For:** [What should this ad be a template for?]
- **Adapt For:** [What other niches/angles could use this structure?]
- **Avoid:** [What should NOT be copied from this ad?]

```

---

## Folder Structure & Organization

All downloaded ads are organized by format and brand:

```
/agents/market-analyst/intel-drops/ads/
├── long-form-copy/
│   ├── amala_health/
│   │   ├── amala_health_copy_01_the_cholesterol_medication.md
│   │   └── amala_health_copy_02_why_statins_fail.md
│   ├── primus_health/
│   ├── grandmas_care/
│   ... (13 other brands)
├── video-transcripts/
│   ├── boostiva/
│   │   ├── boostiva_video_01_forget_everything_memory.md
│   │   └── boostiva_video_02_mitochondrial_energy.md
│   ├── myNuora/
│   ... (other brands with video)
├── advertorial/
│   ├── brand_advertorial_01_headline.md
│   ├── brand_advertorial_02_headline.md
├── static-images/
│   ├── brand_image_01_description.jpg
│   ├── brand_image_01_description.md (analysis)
```

---

## Download Cadence

### Weekly Download (1 hour)
- Review new competitor ads (running <2 weeks)
- Download 2-3 new winning ads (if qualify based on signals)
- Catalog and analyze immediately
- Tag for Creative Strategist if blue ocean or novel mechanism

### Monthly Deep Download (2 hours)
- Review all ads from past month across 14 brands
- Identify and download all ads with 8+ week run times
- Update mechanism scores and angle saturation
- Create monthly winning-ad summary report

### Quarterly Archive Review (1 hour)
- Review downloaded ads from past quarter
- Identify patterns: Which mechanisms scored highest? Which angles dominated?
- Update [[Mechanism Reference Library_ Top 100 Examples.md|mechanism library]] with new patterns
- Report insights to Creative Strategist

---

## Quality Assurance Checklist

Before depositing a downloaded ad file:

- [ ] YAML frontmatter complete (all fields filled)
- [ ] Format verified (long-form copy preserved exactly, video transcript accurate, etc.)
- [ ] Mechanism scored (both Logical Coherence and Market Resonance, 1-9 each)
- [ ] Angle identified and cross-referenced with saturation map
- [ ] Villain archetype(s) identified
- [ ] Analysis Note section complete (all subsections)
- [ ] File named correctly (brand_format_XX_description.md)
- [ ] Saved in correct folder (format/brand/file.md)
- [ ] Tagged appropriately (#mechanism-scoring, #winning-ad, #[niche]-niche, etc.)
- [ ] Run time verified (8+ weeks minimum for "winning" designation)
- [ ] Confidence level justified (why is this a winner?)

---

## Pro Tips for Winning Ad Download

1. **Run Time is King** — Don't download ads running less than 4 weeks. They're not validated winners yet. Stick to 8+ week criteria.

2. **Mechanism Score First** — Before downloading, score the mechanism. If Logical Coherence + Market Resonance < 12, skip it. You're building a library of high-quality patterns.

3. **Preserve Exactly** — Long-form copy must be preserved word-for-word. Your future creative will reference these, and exact words matter.

4. **Angle Freshness Check** — Always cross-reference with [[angle-saturation-map.md|angle saturation map]]. Downloading a saturated angle is low-value unless there's novel differentiation.

5. **Villain Specificity** — Generic villains (doctors bad, pharma bad) are everywhere. Download ads with specific villain positioning (doctors address symptoms, not root cause).

6. **Video Transcripts > Visual Memos** — If you watch a video ad, transcribe it. The words are more valuable than your visual description.

7. **Testify the Testimony** — If an ad uses testimonials, verify they match avatar pain themes from Reddit scrapes. If testimonial matches Reddit language exactly, it's a high-confidence download.

---

## Forbidden Patterns in Ad Downloading

- **Copying entire ads verbatim for your own use** — Download is for analysis and pattern recognition, not copy-paste creatives
- **Downloading ads with mechanism score <12** — Low-quality mechanisms clutter the library
- **Skipping Analysis Note** — Every download needs analysis; undocumented downloads lose value
- **Downloading the same angle from multiple competitors** — One strong example per angle is enough; avoid redundancy
- **Ignoring red flags** — If an ad makes claims you can't verify, note it in vulnerabilities; don't download unless confidence is high

---

## Notes

The goal of this download SOP is to build a proprietary library of proven creative patterns for the Creative Strategist. Every downloaded ad is a data point: "This mechanism + villain + angle + structure worked long enough to justify continued spend."

Over time, patterns emerge: Which mechanisms score highest across categories? Which villain archetypes resonate? Which hook types drive engagement? Which product integration positions minimize friction?

The library becomes the foundation of strategic creative briefs. Creative Strategist references winning patterns, avoids saturation pitfalls, and builds differentiated creative rooted in market validation.

Download with intention. Catalog with precision. Analyze with rigor.
