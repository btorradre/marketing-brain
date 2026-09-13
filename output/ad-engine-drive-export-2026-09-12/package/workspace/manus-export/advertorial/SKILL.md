---
name: advertorial
description: Write advertorials, editorial-style landing pages, native ad pages, bridge pages, and presell pages converting ad traffic into product-page clicks or purchases. Trigger when writing/editing an advertorial, turning an ad concept into a landing page, writing a COMPLEMENTARY advertorial from long-form ad copy (same product, different angle, shifted awareness stage), or creating editorial content that sells. Governs narrative architecture, editorial framing, the awareness-stage shift, mechanism education, social-proof formatting, pricing/urgency/guarantee structures, and the conversion close. PRIMARY use: given a winning long-form ad plus brand and product-page URL, analyze the ad's awareness stage and write a complementary advertorial at a DIFFERENT stage, plus a hero-image prompt and headline variations. SECONDARY use (after copy is approved): build an importable landing-page file. Read before writing any advertorial — rules differ from short-form ad copy. Governs the page an ad LINKS TO, not the ad itself.
---

# Advertorial Writing

An advertorial is an editorial-style landing page that converts ad traffic into product-page clicks or direct purchases. It looks like an article. It reads like a report or a revelation. It sells like a machine.

The skill runs in two parts, in order:

1. **PRIMARY PROTOCOL — the advertorial COPY.** The main job: analyze the upstream ad, shift the awareness stage, write the complementary advertorial.
2. **SECONDARY PROTOCOL — the landing-page build.** Mechanical. Runs AFTER the copy exists, only when the page itself is wanted.

Read this entire file before writing. Then pull the relevant deeper reference based on the situation (pointers are inline below).

---

## PRIMARY PROTOCOL — THE ADVERTORIAL COPY

This is the default mode. When handed a winning long-form ad (plus a brand name and a product-page URL) and asked for an advertorial, write a complementary advertorial that pre-sells the same product from a DIFFERENT angle and a DIFFERENT awareness stage. It must NOT repeat or rehash the ad's pitch, mechanism explanation, or narrative structure. Everything below — the Awareness-Stage Shift, Confirm-and-Escalate, the six frameworks, the 13 laws, the section architecture — is the engine this protocol runs on. The protocol decides *what* to write; the engine decides *how* to write it well.

### What you produce, every copy run

1. **One complementary advertorial**, operating at a different awareness stage than the upstream ad.
2. **A hero-image generation prompt** — one image-gen prompt for the hero slot, matched to the advertorial's avatar, scene, and emotional tone.
3. **3-4 hero headline variations**, varying in length, each carrying an open loop. List all; mark the strongest.

### Step 1 — Inputs

Required: brand name; product-page URL (becomes the CTA button link); the winning long-form ad copy (the upstream "ad" the whole engine keys off).

Optional (find on the product page or infer, then state the assumption): exit awareness level + avatar (derive from the ad if not supplied); offer details (price, guarantee, bonus); the brand's market research — reviews, voice-of-customer notes, past research — mined for the avatar's actual language.

### Step 2 — Analyze the ad and lock the pre-flight

Before writing, extract from the long-form ad (full extraction list in "The Governing Principle" below): awareness stage, core angle/storyline, avatar, mechanism/USP, desire targeted, tone/voice/language patterns, emotional exit state, installed beliefs.

Then lock these:

**(a) Continuation.** The advertorial continues the ad — same product, same core promise, same avatar. The angle shifts; the destination doesn't.

**(b) Awareness target — SHIFT THE STAGE (mandatory).** The advertorial must land at a DIFFERENT stage than the ad — never the same stage (see The Awareness-Stage Shift below). Default shift: one stage deeper. Problem-aware ad → advertorial picks up at solution-aware or product-aware. Solution-aware ad → advertorial goes product-aware. Product-aware ad → advertorial goes most-aware. If the ad never names the brand, the reader exits between solution-aware and product-aware — the advertorial's job is to bridge that gap. This is a soft-close destination by default (see the funnel-conditional close rule in Law 7 below) — push intensity stays low, but "soft" is not brand concealment; the product may be named.

**(c) Product category → style.** Improvement product (a better version of something already used) → lean Crisis Narrative / personal-story + failed-solutions graveyard, product shown later. Innovation / genuinely new → lean Authority Expert or System Exposé with a big-revelation frame, product shown earlier. Default to Authority-style unless the ad's narrator or category clearly pulls toward Crisis Narrative.

**(d) Ad selling-intensity → advertorial length (inverse, within the word-count band).** Low-selling/curiosity-gap upstream ad → upper end of the band, longer lead. High-selling/VSL-style upstream ad → lower end, more direct. Either way the advertorial stays shorter than the upstream ad.

**(e) Confirm the four locked variables are at or above break-even:** Avatar, Desire/Problem, Angle, Unique Mechanism. If the long-form ad is a confirmed winner, inherit these intact — don't reinvent them.

### Step 3 — The Continuation Mandate (non-negotiable, every run)

The advertorial must: shift the awareness stage (same storyline, different lens — the ad opened the door, the advertorial walks through a different room in the same house); add at least two complementary layers the ad didn't cover (Law 4); continue the narrative as the next chapter, same metaphor, different but compatible voice; be more logical than the ad (tighten reasoning, close gaps, answer "but how do I know"); not be repetitive (Echo test < 15%); confirm then escalate; obey the Rule of One (Law 13); run shorter than the ad (800-1,200 words by default).

### Step 4 — Write the copy

Run the engine: pick the framework (Step 2c is the selector), run the Awareness-Stage Shift and Confirm-and-Escalate, obey the 13 Laws, fill the Section Architecture on the Hook → Lead → Body → Bridge → CTA spine. Produce the Strategy Brief + full advertorial copy + audit per the Output Format below.

The advertorial copy itself is pure copy — no visual design notes, no meta-commentary. The strategy brief and audit wrap around it; the copy block is just the advertorial.

**Headline:** write 3-4 variations of different lengths, each with an open loop (Law 1 — sells the article, never the product). Mark the strongest; list the rest as A/B alternates.

---

## SECONDARY PROTOCOL — THE LANDING-PAGE BUILD

Secondary and mechanical. Run this AFTER the copy exists — when the page itself is wanted, or the copy is approved and needs to ship. If only copy was asked for, stop after the Primary Protocol and offer the build.

**The template is a layout shell, not a script.** A master advertorial page template has a fixed inventory of editorial slots — a masthead, a headline, a hero image, roughly a dozen H2-headline + paragraph content blocks, three testimonials, an offer block, two CTA buttons, a closing block. Map *your* framework's narrative beats onto those generic blocks **in reading order**. Any inherited slot role-names (from whatever example page the template was built from) are just that one page's beats — treat them as generic "headline + body" containers, not a required sequence. Do NOT robotically clone one example's beat-by-beat structure onto every advertorial; let the copy be governed by the chosen framework, the 13 laws, and the ad's exit state. If the narrative needs fewer beats than there are slots, consolidate and leave lighter blocks; if it needs a different order of ideas, write them in reading order and ignore the inherited labels.

**The build, in outline** (full mechanics — the exact content-map shape, the slot inventory, the residue-check procedure — are in `references/pagefly-build-protocol.md`):
1. Write a small **role-keyed content map** — human-readable role names (e.g. `headline`, `lede`, `setup_h2`, `cta_button_1`) mapped to the actual content (HTML strings for text; a label + URL for buttons; a source + alt text for images). Only include roles being filled — anything left out keeps the template's placeholder content, so fill every slot intended for use.
2. Apply the map to the template — a straightforward find-and-replace/templating pass that overwrites each named slot's content — then run a **residue check**: search the output for leftover placeholder tokens from the template's original example content. Residue in a text slot means a role was missed; fix and reapply. Residue only in deliberately-deferred image fields is expected — confirm it traces to those images, then swap them in the page builder's own editor after import.
3. Hand off the finished importable page file for import into the landing-page platform in use, then publish.

**Ship alongside the build:** the hero-image generation prompt (one vivid prompt — subject, scene, emotion, composition, style, aspect ratio — matched to the avatar and opening); the 3-4 headline variations, listed for A/B testing beyond the one shipped in the build.

**When to deviate:** no long-form ad supplied (cold/standalone) → use `references/standalone-mode.md`, build belief from scratch, carry the HARD close on-page (build mechanics unchanged). Page wanted in one shot → run Primary then Secondary back-to-back. Narrative genuinely won't fit the template's slot inventory → say so; propose consolidating beats or flag that a custom template is needed.

---

## Reference Files — When to Read What

| Situation | Read |
|---|---|
| Full narrator-type lists per framework, the framework-choice table, the complete 13 Laws, full section-by-section guidance, Pre-Writing Locks, Handoff Tests, Anti-Mimicry, and the Final Audit Checklist | `references/frameworks-and-laws.md` |
| Writing WITHOUT an upstream ad (cold traffic, organic, direct link) | `references/standalone-mode.md` |
| The mechanism is complex and needs deep educational treatment | `references/mechanism-education.md` |
| Headline formulas, pricing patterns, social proof formats, comment-section architecture, urgency patterns | `references/swipe-pattern-library.md` |
| Building the actual landing-page file (content-map shape, slot inventory, residue check) | `references/pagefly-build-protocol.md` |

**Always pull the swipe pattern library before writing.** It carries the headline formulas, pricing psychology, social-proof architecture, and close components this system is built on. The other references load based on the specific situation.

---

## The Governing Principle: Analyze the Ad First

The advertorial exists downstream of an ad. The ad installed beliefs. The advertorial confirms those beliefs and escalates with new value the ad couldn't deliver.

Before writing, identify from the upstream ad: the awareness stage it's written in (unaware, problem-aware, solution-aware, product-aware, most-aware); the core angle and storyline; the avatar (demographics, pains, desires, beliefs); the desire being targeted; tone/voice/language patterns; the narrator and their voice (peer, spouse, authority guide, analytical, emotional); the mechanism taught (the root-cause reframe) and the USP; the core metaphor; the emotional exit state (cautious hope, righteous anger, desperate curiosity); what beliefs the ad installed vs. what's still missing; what proof type it used (personal story, clinical data, insider revelation).

This analysis drives every downstream decision: stage shift, framework, narrator, escalation angle, proof format, close.

If there is no upstream ad, read `references/standalone-mode.md` instead of running Confirm-and-Escalate — standalone builds the full case from scratch.

---

## The Awareness-Stage Shift

The advertorial must operate at a DIFFERENT awareness stage than the upstream ad. The ad opened the door; the advertorial walks the reader through a different room in the same house. Same narrative arc, different lens — never the same pitch, mechanism explanation, or structure re-run.

**The ladder, each stage's job:** Unaware → educate, introduce the problem. Problem-aware → amplify urgency, dramatize the problem. Solution-aware → compare options, guide toward this category. Product-aware → address beliefs, past failures, positioning, authority, mechanism. Most-aware → trust, offer, final persuasion.

**The shift rule:** name the ad's stage, then write the advertorial at least one stage deeper. Problem-aware ad → advertorial at solution/product-aware (proof, authority, comparison, social validation). Solution-aware ad → advertorial at product-aware (objections, past failures, positioning). Product-aware ad → advertorial at most-aware (trust, offer, final persuasion).

This is the awareness-level expression of Confirm-and-Escalate: confirmation lives at the ad's stage, escalation lives at the advertorial's stage. If the advertorial's body sits at the ad's own stage, it's echoing — no matter how different the words are.

---

## The Confirm-and-Escalate Principle

The governing principle for every ad-driven advertorial. It is not a standalone persuasion piece building belief from scratch — it confirms and escalates.

**Confirm:** acknowledge what the reader already believes in 2-4 sentences, using the ad's core metaphor. Don't re-teach it — reference it like shared knowledge. Validates the reader's intelligence, bridges the ad-to-page transition.

**Escalate:** deliver what the ad structurally couldn't — new credibility, new proof category, new depth on an objection the ad had no room for. This is the layer that converts "interested" into "ready to buy."

**Weight split:** 15-20% confirmation and bridge; 80-85% escalation, proof, objection handling, and close. More than a fifth spent re-teaching the mechanism means echoing.

**Assume mixed readership** — some read the full ad, some skimmed it. Reference the mechanism briefly and confidently: enough for a skimmer to follow, never so much a full reader feels re-taught.

**Arrives WITH:** emotional investment in the problem; understanding of the root cause; belief current solutions target the wrong thing; a mental checklist for the right solution; curiosity whether anything actually addresses it.
**Arrives WITHOUT:** confidence THIS product is the one; trust in the brand; answers to remaining objections; proof from a different source than the ad's narrator; enough certainty to buy.

The advertorial's job is to deliver what's missing — not repeat what's already installed.

---

## The Six Frameworks (summary — full narrator types and the choice table in `references/frameworks-and-laws.md`)

Orientations, not boxes — a good piece can blur two. They exist to prevent structural errors and guide narrator selection.

1. **Authority Expert** — a credentialed figure (doctor, researcher, PT, pharmacist) independently confirms the mechanism. Not lecturing — revealing: access the reader doesn't have. Credential + tension + inciting incident within the first 50 words, not a bio.
2. **Crisis Narrative** — one person's dramatic story carries the piece: crisis → escalation → intervention → mechanism learned through the story → discovery → transformation → urgent close. The reader lives the discovery WITH the narrator.
3. **System Exposé / Whistleblower** — a patient, former insider, or survivor reveals something about the system. Credibility = lived experience + insider access. Tells a DIFFERENT story that independently arrives at the ad's same conclusion.
4. **Expert Comparison / Review** — reviews multiple options against criteria, reveals a winner. Answers "which one?" not "should I?" Side-by-side table, sequential review, or a failure-comparison chart.
5. **Listicle / Discovery** — numbered revelations, each independently valuable, product emerges as the logical conclusion in the final 1-2 items.
6. **Suppression / Conspiracy** — the product/science has been buried or attacked; existence despite resistance. Needs a plausible economic motive tied to something the reader has personally felt (a bill, a denial, a 12-minute appointment).

**Choosing:** whatever the ad delivered, the advertorial delivers something the ad structurally COULDN'T — contrast reads as independent confirmation. Peer-narrated ad → lean Authority. Analytical ad → lean Whistleblower/insider. Emotional ad → lean Authority for clinical contrast. Audience distrusts the system → Suppression. Audience overwhelmed by options → Comparison. Audience in research mode → Listicle.

---

## The 13 Advertorial Laws (summary — full text in `references/frameworks-and-laws.md`)

Non-negotiable regardless of framework.

1. **Headline sells the article, never the product.** Product name never appears in it.
2. **The opening delivers on the ad's promise without repeating it.** First 150-200 words continue the ad's emotional exit state; reader knows within 50 words this is a different person talking.
3. **Confirm, don't re-teach.** Mechanism gets 2-4 sentences, same metaphor, brief and confident. Exception: genuinely new depth = escalation, not echo.
4. **The advertorial adds what the ad couldn't.** At least two complementary layers not in the ad: social proof, authority, comparison framing, story-driven angle, objection handling (or clinical depth, broader proof density, insider info, a different emotional angle, economic motive).
5. **The product enters through the mechanism** — never before it's established.
6. **Social proof from multiple categories**, layered — individual + professional + community + clinical + comments — for triangulated belief.
7. **Formatting serves the editorial frame** — masthead, breadcrumbs, scannable headers, bold on mechanism terms not sales language, short paragraphs, subheads. *(The funnel-conditional close rule lives here: by default the advertorial is the SOFT-close half of a 2-step funnel — bridge advertorial → dedicated product page carries the hard close. A standalone/fused advertorial with no separate product page carries the HARD close itself. "Soft" means push intensity, not brand concealment — the product can still be named.)*
8. **The CTA bridge is a continuation, not a pitch.** It sounds like the next paragraph, not an ad — "We built [Product] because of [mechanism]. Here's what to expect in the first 30 days." Then the button. Never "BUY NOW" straight off an editorial narrative.
9. **The close matches the framework's voice** — clinical for Authority, personal urgency for Crisis, "I wish someone had told me" for Whistleblower, editorial recommendation for Comparison.
10. **Objections are handled inside the narrative**, not a bolted-on FAQ (FAQ is fine near the close for pure logistics).
11. **Write with the product-page handoff in mind.** Whatever language/mechanism/frame the advertorial closes on, the dedicated product page MUST open with — same exact language. Advertorial traffic goes to a DEDICATED page, never the main product page, with navigation and exit points stripped.
12. **Every sentence earns its place.** 800-1,200 words, shorter than the upstream ad, never longer.
13. **The Rule of One.** One avatar, one deep desire, one core message — every sentence serves that single thread.

---

## Section Architecture (Ad-Driven) — summary

Five-part spine: **Hook → Lead → Body → Bridge → CTA.** Full section-by-section guidance in `references/frameworks-and-laws.md`.

| Section | Spine | Words | Function |
|---|---|---|---|
| 1. Editorial Frame + Headline | Hook | 40-60 | Masthead, breadcrumbs, byline, headline, subhead |
| 2. Opening Hook + Bridge | Hook/Lead | 100-150 | Validates ad promise from the NEW stage, new voice within 50 words |
| 3. Mechanism Confirmation | Lead | 40-80 | 2-4 sentences, same metaphor, confirmation not re-teaching |
| 4. Escalation / New Value | Body | 250-400 | The main event — complementary layers the ad couldn't deliver |
| 5. Product Confidence | Body | 120-200 | Not an intro — objection handling through product assessment |
| 6. Proof Density | Body | 120-200 | Different proof category than the ad used |
| 7. CTA Bridge | Bridge | 50-100 | 2-4 sentence continuation paragraph, primes the product-page language |
| 8. Conversion Close | CTA | 80-200 | Offer + CTA + post-CTA reinforcement (full hard apparatus only in standalone) |
| **TOTAL** | | **800-1,200** | Shorter than the ad, never longer |

### The Post-Reveal Skepticism Run (mandatory)

**Never close the sale immediately after the product reveal.** The reveal answers "what is it?" not "why should I believe you?" Everyone who was going to click already clicked the first CTA — everything after the reveal exists for the skeptic who kept scrolling.

After the reveal + first CTA, continue in the SAME narrator voice with (pick 3-5, roughly this order):
1. **Comparison chart** — failed-solutions table: what the reader owns vs. where it works vs. the product. A table is a different format than the ad's narrative takedown, so it doesn't echo.
2. **Expectations timeline** — what weeks one/two/three actually feel like, including the honest "quiet start — don't quit on day four" beat. Kills the silent refund-and-churn objection.
3. **Reviews block** — 2-4 "Verified Buyer" reviews spanning demographics, including one slow-responder/almost-returned-it review. The imperfect review converts harder than the glowing ones.
4. **Guarantee expansion** — the full no-hoops policy, reframed as "what does it cost me to find out?"
5. **Two-options close** — keep doing what you're doing (painted concretely) vs. try it risk-free, plus a "you didn't read this far for nothing" consistency beat. THEN the final CTA.

CTA placement across the run: reveal CTA → mid-run CTA (varied language) → final CTA after two-options. Max 4 total. A sticky CTA covers the reader who's ready early.

**Word-count interaction:** the 800-1,200 band covers the STORY (hook through reveal) only. A page running the full skepticism run lands at roughly 1,800-2,100 total — that's correct for a universal/high-skepticism page (one receiving traffic from multiple ads should always run it). Never cut the run short just to protect the band.

---

## Word Count Targets

Ad-driven default: **800-1,200 words for the story** (hook through reveal), always shorter than the upstream ad — the ad already did the belief work. Stretch above 1,200 only when the pre-flight demands it (a low-selling/curiosity-gap ad, or a high-ticket/complex-mechanism product). The Post-Reveal Skepticism Run sits ON TOP of this band, not inside it.

| Product Type | Ad-Driven | Standalone |
|---|---|---|
| Simple consumer (<$50) | 800-1,000 | 1,800-2,500 |
| Supplement/health ($30-80) | 800-1,200 | 2,200-3,500 |
| Medical device/premium ($80-200) | 1,000-1,500 | 3,000-4,500 |
| High-ticket/surgery alternative ($200+) | 1,200-2,000 | 3,500-5,000+ |

Longer copy correlates with higher price points and more complex mechanisms — but every word earns its place regardless of length. Full standalone architecture and word counts in `references/standalone-mode.md`.

---

## Pre-Writing Locks (quick list — full 16-point version in `references/frameworks-and-laws.md`)

Before writing, confirm: the driving ad is read and understood (or standalone mode is in play); the stage shift is locked (ad's stage ≠ advertorial's); the Rule of One is written out (avatar / desire / message, one line each); the framework (or blend) is chosen; the narrator is a specific person with a specific inciting incident; at least two complementary layers are named; the primary objection is named; the editorial frame (publication, byline, breadcrumbs) is set; the metaphor continuity is locked; avatar language is sourced from real market research where available; the social-proof format is chosen; the close architecture (pricing/urgency/guarantee) is chosen; the CTA bridge language is drafted and matches what the product page must open with; a dedicated product page is confirmed to exist (flag hard if not — advertorial traffic should never land on the main product page); the word target is set; an anti-mimicry check has been run against existing advertorials for this product.

---

## The Handoff Tests (quick list — full version in `references/frameworks-and-laws.md`)

Before finalizing, run: the Emotional Bridge Test (ad's last 200 words → advertorial's first 200 — does the temperature flow?); the Echo Test (<15% restated content); the Stage-Shift Test (ad's stage vs. the advertorial body's stage — must differ); the Rule of One Test (does every section serve the one avatar/desire/message?); the Escalation Test (at least 3 things delivered that the ad didn't); the CTA Bridge Test (does the pre-CTA paragraph read as continuation, not pitch?); the Product-Page Handoff Test (does the page lead with the exact language the advertorial closed on, on a dedicated, nav-stripped URL?).

---

## Anti-Mimicry

Writing multiple advertorials for the same product: each must vary its FRAMEWORK, NARRATOR, AWARENESS STAGE (where the funnel allows), PRIMARY OBJECTION, PROOF FORMAT, OPENING EVENT, and URGENCY TYPE. The test: if two advertorials for the same product read as "basically the same page," it failed.

---

## Output Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ADVERTORIAL STRATEGY BRIEF
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Mode: [Ad-Driven / Standalone]
Framework: [which of the six, or blend with center of gravity]
Upstream Ad: [narrator, angle/storyline, mechanism, metaphor, desire targeted, emotional exit state, installed beliefs, tone/voice patterns]
Ad Awareness Stage: [stage the ad is written in]
Advertorial Target Stage: [different stage — the shift, and why]
Rule of One: [one avatar / one deep desire / one core message — one line each]
Complementary Layers: [the 2+ layers NOT in the ad]
Narrator: [specific person, credential/experience, inciting incident]
Publication Name: [editorial frame]
Byline: [name, credential, date]
Primary Objection Handled: [central objection]
Metaphor Continuity: [same metaphor, extended how]
Proof Format: [which patterns, how they differ from ad]
CTA Bridge Language: [what the bridge paragraph will say — this defines the product-page hero]
Dedicated Product Page: [URL if exists / "NEEDED — flag for build" if not]
Product-Page Hero Must Lead With: [exact language/mechanism the page opens on]
Pricing Pattern: [which pattern]
Urgency Type: [which pattern]
Target Word Count: [range — 800-1,200 ad-driven, shorter than the ad]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ADVERTORIAL COPY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Full advertorial in markdown — pure copy only. No visual design notes.
No meta-commentary about what you're doing. Just the advertorial.]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AUDIT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Audit checklist results — full checklist in references/frameworks-and-laws.md]
```

Run the Final Audit Checklist from `references/frameworks-and-laws.md` (Confirm-and-Escalate compliance, all 13 Laws, structural audit, language audit) before delivering.
