---
name: advertorial
description: Use this skill whenever writing advertorials, editorial-style landing pages, native ad pages, bridge pages, presell pages, or article-style sales content. Also trigger when editing or improving existing advertorials, turning an ad concept into a landing page, writing a COMPLEMENTARY advertorial from long-form native ad copy (same product, different angle, shifted awareness stage), or creating editorial content that sells. This skill governs narrative architecture, editorial framing, the awareness-stage shift, mechanism education at landing page depth, social proof formatting, pricing/urgency/guarantee structures, and the conversion close. Its PRIMARY PROTOCOL is the COPY: given a winning long-form ad plus a brand and product URL, it analyzes the ad's awareness stage and writes a complementary authority-style advertorial at a DIFFERENT awareness stage — plus a Nano Banana hero-image prompt and 3-4 headline variations. Its SECONDARY PROTOCOL (run after the copy, when the user wants the page) builds an importable PageFly (.pagefly) file the user uploads straight to Shopify. Always use this skill before writing advertorials — it contains critical laws that differ from short-form ad copy. Do NOT use the long-form-copy skill for advertorials — that governs Facebook ad body copy. This skill governs the page the ad LINKS TO.
---

# Advertorial Writing

This skill governs how to write advertorials — editorial-style landing pages that convert ad traffic into product page clicks or direct purchases. An advertorial looks like an article. It reads like a report or a revelation. It sells like a machine.

**Read this entire file before writing. Then read the relevant reference files based on the situation.**

The skill runs in two parts, in order:

1. **PRIMARY PROTOCOL — the advertorial COPY.** This is the skill's main job. Analyze the upstream ad, shift the awareness stage, and write the complementary advertorial.
2. **SECONDARY PROTOCOL — the PageFly landing-page build.** Mechanical. Runs AFTER the copy exists, when the user wants the page built. Never let build mechanics shape the copy.

---

## PRIMARY PROTOCOL — THE ADVERTORIAL COPY

**This is the default operating mode of the skill.** When the user hands you a winning long-form ad (plus a brand + product URL) and asks for an advertorial, you write a complementary advertorial that pre-sells the same product from a DIFFERENT angle and a DIFFERENT awareness stage. The advertorial must NOT repeat or rehash the same pitch, mechanism explanation, or narrative structure as the ad. Everything below this section — the Awareness-Stage Shift, the Confirm-and-Escalate principle, the six frameworks, the thirteen laws, the section architecture, the references — is the **engine** this protocol runs on. The protocol decides *what to write*; the engine decides *how to write it well*. Do not skip the engine; this section just sequences it.

### What you produce (every copy run)
1. **One complementary advertorial**, written by the engine below, operating at a different awareness stage than the upstream ad.
2. **A Nano Banana hero-image prompt** (`.txt`) — a single image-gen prompt for the hero slot, matched to the advertorial's avatar, scene, and emotional tone.
3. **3–4 hero headline variations** — varying in length, each carrying an open loop. (List all; mark the strongest.)

### Step 1 — Inputs
Required:
- **Brand Name**
- **Product Page URL** (becomes the CTA button `href`)
- **The winning long-form ad copy** (this is the upstream "ad" the whole engine keys off — read it the way "Analyze the Ad First" describes)

Optional (scrape the product page or infer if absent, then state your assumption):
- Exit awareness level + avatar (if not supplied, derive from the long-form ad)
- Offer details (price, guarantee, bonus) for the offer/close slots
- The brand's market research files (reviews, VOC, research docs from the vault) — mine these for the avatar's actual language

### Step 2 — Analyze the ad and lock the pre-flight
Before writing, extract from the long-form ad (see "Analyze the Ad First" for the full extraction list):
- The **awareness stage** the ad is written in (unaware, problem-aware, solution-aware, product-aware, most-aware)
- The **core angle and storyline**
- The **avatar** targeted (demographics, pains, desires, beliefs)
- The **mechanism or unique selling proposition**
- The **desire being targeted**
- The **tone, voice, and language patterns** used
- Its **emotional exit state** and **installed beliefs**

Then lock these (they come from a thorough analysis of the Anthony Camacho advertorial transcript and reconcile onto the six frameworks below — they are a *selector*, not a competing taxonomy):

**(a) Continuation.** The advertorial is a *continuation* of this ad, not a restart. Same product, same core promise, same avatar. The angle shifts but the destination is the same.

**(b) Awareness target — SHIFT THE STAGE (mandatory).**
- The advertorial must operate at a **DIFFERENT awareness stage** than the ad — never re-run the ad's stage. See "The Awareness-Stage Shift" below for the ladder and each stage's job.
- Default shift: one stage deeper. Problem-aware ad (introducing the problem and mechanism) → advertorial picks up at **solution-aware or product-aware** (proof, authority, comparison, social validation). Solution-aware ad → advertorial goes **product-aware** (objections, past failures, positioning). Product-aware ad → advertorial goes **most-aware** (trust, offer, final persuasion).
- **If the long-form ad never names the brand**, the reader exits *between Solution-Aware and Product-Aware*. The advertorial's job is to **bridge that gap** — name and prove the specific product without re-teaching the mechanism.
- This is a **soft-close** destination by default (see the funnel-conditional close rule below): push intensity stays low, but "soft" ≠ brand concealment. You may name the product.

**(c) Product category → style (Camacho Axis A).**
- **Improvement product** (better version of a thing they already use): lean **Crisis Narrative / personal-story + failed-solutions graveyard**. Product shown later, after the mechanism earns it.
- **Innovation / gadget / genuinely new**: lean **Authority Expert or System Exposé with a breaking-news / big-revelation frame**, product shown earlier.
- **Default to Authority-style** unless the long-form ad's narrator or category clearly pulls toward Crisis Narrative.

**(d) Ad selling-intensity → advertorial length (Camacho Axis B, inverse — within the word-count band).**
- Low-selling / clickbait / curiosity-gap upstream ad → **upper end** of the word-count band, longer lead (more belief to build).
- High-selling long-form / VSL-style upstream ad → **lower end**, more direct, product shown sooner (belief is already built; don't bore them).
- Either way the advertorial stays **shorter than the upstream ad** — see Word Count Targets.

**(e) Confirm the 4 locked variables are at/above break-even before writing:** **Avatar**, **Desire/Problem**, **Angle**, **Unique Mechanism**. If the long-form ad is a confirmed winner, these are inherited intact — do not reinvent them.

### Step 3 — The Continuation Mandate (non-negotiable for every run)
The advertorial must:
- **SHIFT THE AWARENESS STAGE** — operate at a different stage than the ad (Step 2b). Same storyline, different lens: the ad opened the door; the advertorial walks the reader through a **different room in the same house**. Never the same pitch, mechanism explanation, or narrative structure re-run.
- **ADD COMPLEMENTARY LAYERS** — deliver at least two net-new layers the long-form ad did not cover (Law 4).
- **CONTINUE THE NARRATIVE** — it is the *next chapter* of the long-form ad, in a *different but compatible voice*. Same metaphor, same angle, picked up where the ad left off.
- **BE MORE LOGICAL** — the ad worked on emotion + curiosity; the advertorial tightens the logic, closes the reasoning gaps, answers "but how do I know."
- **NOT BE REPETITIVE** — never re-teach what the ad installed (Echo test < 15%).
- **CONFIRM + ADD VALUE** — validate what they already believe, then escalate.
- **OBEY THE RULE OF ONE** — one specific avatar, one deep desire, one core message (Law 13). Every sentence serves that single thread.
- **RUN SHORTER THAN THE AD** — 800–1,200 words by default; never longer than the upstream ad (see Word Count Targets).

### Step 4 — Write the copy (run the engine)
Now run the engine below: pick the framework (Step 2c is your selector), run the Awareness-Stage Shift and Confirm-and-Escalate, obey the 13 Laws, fill the Section Architecture on the Hook → Lead → Body → Bridge → CTA spine. Produce the Strategy Brief + the full advertorial copy + the audit, exactly as the Output Format specifies.

**The advertorial copy itself is pure copy.** No visual design notes inside it. No meta-commentary about what you're doing. The strategy brief and audit wrap around the copy; the copy block is just the advertorial.

**Headline:** write 3–4 variations of different lengths, each with an open loop (Law 1 — sells the article, never the product). Mark the strongest; list the rest as A/B alternates.

---

## SECONDARY PROTOCOL — THE PAGEFLY LANDING-PAGE BUILD

**Secondary and mechanical.** Run this AFTER the copy exists — when the user wants the page built, asks for the `.pagefly`, or approves the copy and wants it shipped. If the user only asked for copy, stop after the Primary Protocol and offer the build.

**The template is a layout shell, NOT a script.** The master PageFly template has a fixed inventory of editorial slots (a masthead, a headline, a hero image, ~12 H2-headline + paragraph content blocks, three testimonials, an offer block, two CTA buttons, a closing block — see `build/slot_map.json`). Map *your* framework's narrative beats onto those generic blocks **in reading order**. The slot role-names (`problem_reveal`, `myth`, `solution_cat`, `mechanism`, `transformation`, `results`, `why_hidden`, `math`, `offer`, `two_futures`, etc.) are the *Haloven example's* beats — treat them as generic "headline + body" containers, not a required sequence. **Do NOT robotically clone the swipe's beat-by-beat structure onto every advertorial.** Use the swipe every time as a *layout and proof-density reference* to pull from — but let the copy be governed by the chosen framework, the 13 laws, and the ad's exit state. If your narrative needs fewer beats than there are slots, consolidate and leave lighter blocks; if it needs a different order of ideas, write the ideas in reading order and ignore the inherited role labels.

### Build the `.pagefly` (slot-swap, never hand-built)
The build is mechanical and lives in `build/`:
- `build/template.json` — the master export (the "Health Insider Kids" authority/crisis advertorial).
- `build/slot_map.json` — the role→UUID map (42 slots: text, 2 buttons, 3 images). `headline` maps to two synced slots.
- `build/apply_swaps.py` — the Mac/Python builder (no dependencies).

**Procedure:**
1. Write a **role-keyed swaps file** (`swaps.json`) — keys are human role names from `slot_map.json`, NOT UUIDs. Shape:
   ```json
   {
     "brand": "BrandName",
     "text":    { "brand_header": "<p>...</p>", "headline": "...", "lede": "<p>...</p>", "setup_h2": "...", "setup_para": "<p>...</p>", "...": "..." },
     "buttons": { "cta_button_1": {"value": "CHECK AVAILABILITY", "href": "PRODUCT_URL"},
                  "cta_button_2": {"value": "CHECK AVAILABILITY", "href": "PRODUCT_URL"} },
     "images":  { "hero_image":    {"src": "IMAGE_URL", "alt": "..."},
                  "product_image": {"src": "IMAGE_URL", "alt": "..."},
                  "closing_image": {"src": "IMAGE_URL", "alt": "..."} }
   }
   ```
   - Text values are HTML strings (wrap body copy in `<p>…</p>`; the template's paragraph slots render HTML). `headline` is written once and the script syncs both headline slots.
   - Only include the roles you're filling. Any text slot you leave out keeps the template's original copy — so **fill every content slot you intend to use** and the residue check will catch leftovers.
   - For images: if the user hasn't supplied hosted image URLs, leave the `images` block out and tell the user the hero/product/closing images must be swapped in PageFly's editor after import (the Nano Banana prompt feeds the hero). Image `src` must be a hosted URL, not a local file.
2. Run the builder:
   ```bash
   cd "build" && python3 apply_swaps.py swaps.json --brand "BrandName"
   ```
   It writes `build/output/{brand-slug}-advertorial.pagefly` (a zip with the page JSON at its root) and runs a **residue check** against source-template tokens (Haloven, Sarah, Emma, Dr. Morrison, Japanese, etc.). The `.pagefly` is always written; the residue check is a warning gate (exit code 2 if anything matches).
   - If residue appears in **text slots** you intended to fill, you left a slot out — fix the swaps file and re-run.
   - If you **deliberately deferred images**, the source image `src`/`alt` still carry "Haloven" tokens — that residue is expected; just confirm every flagged hit traces back to an image slot, then swap those images in PageFly's editor after import. When you fill all text + images, residue should come back **CLEAN**.
3. Hand the user the `.pagefly` path. They import it into PageFly → publish on Shopify.

### Ship the side assets
- **Nano Banana hero-image prompt** → write to `build/output/{brand-slug}-hero-prompt.txt`: a single, vivid image-gen prompt for the hero slot (subject, scene, emotion, composition, editorial/photographic style, aspect ratio) matched to the avatar and the advertorial's opening. No text-in-image instructions unless the user asks.
- **Headline variations** → list the 3–4 length-varied, open-loop headlines in your final message so the user can A/B beyond the one shipped in the build.

### When to deviate from the protocols
- **No long-form ad supplied (cold/standalone):** drop to `references/standalone-mode.md` — build belief from scratch and carry the HARD close on-page. The build mechanics are unchanged.
- **User wants the page in one shot:** run Primary then Secondary back-to-back.
- **User wants a different layout than the master template provides:** the slot inventory is fixed by the template; if the narrative genuinely won't fit, say so and propose either consolidating beats or a custom template (out of scope for the swap builder).

---

## Reference Files — When to Read What

This skill uses progressive disclosure. The core system lives here. Deeper guidance lives in `references/`:

| Situation | Read This Reference |
|-----------|-------------------|
| Writing WITHOUT an upstream ad (cold traffic, organic, direct link) | `references/standalone-mode.md` |
| The mechanism is complex and needs deep educational treatment | `references/mechanism-education.md` |
| Need headline formulas, pricing patterns, social proof formats, comment section architecture, or urgency patterns | `references/swipe-pattern-library.md` |

**Always read the swipe pattern library before writing.** It contains the headline formulas, pricing psychology, social proof architecture, and close components derived from 66 analyzed real-world advertorials. The other two references load based on the specific situation.

---

## The Governing Principle: Analyze the Ad First

The advertorial exists downstream of an ad. The ad installed beliefs. The advertorial confirms those beliefs and escalates with new value the ad couldn't deliver.

**Before writing, analyze the upstream ad.** Identify:
- The **awareness stage** the ad is written in (unaware, problem-aware, solution-aware, product-aware, most-aware)
- The **core angle and storyline**
- The **avatar** targeted (demographics, pains, desires, beliefs)
- The **desire being targeted** (the one deep desire the ad keys on)
- The **tone, voice, and language patterns** used
- The narrator and their voice (peer, spouse, authority guide, analytical, emotional)
- The mechanism taught (the root cause reframe — what the reader now believes is the real problem) and the unique selling proposition
- The core metaphor used to explain the mechanism
- The emotional exit state (where the reader's feelings are when the ad ends — cautious hope, righteous anger, desperate curiosity)
- What beliefs the ad installed vs. what's still missing
- What proof type the ad used (personal story, clinical data, insider revelation)

This analysis drives every downstream decision: awareness-stage shift, framework, narrator, escalation angle, proof format, and close.

**If there is no upstream ad** (standalone advertorial for cold traffic, organic, or direct link), read `references/standalone-mode.md` before proceeding. The standalone system builds the full case from scratch instead of confirming and escalating.

---

## The Awareness-Stage Shift

The advertorial must operate at a **DIFFERENT awareness stage** than the upstream ad. The ad opened the door; the advertorial walks the reader through a **different room in the same house**. The same storyline can be told differently — same narrative arc, different lens. Never the same pitch, mechanism explanation, or narrative structure re-run.

**The ladder — each stage's job:**
- **Unaware** → educate and introduce the problem
- **Problem-aware** → amplify urgency and dramatize the problem
- **Solution-aware** → compare options and guide toward this category
- **Product-aware** → address beliefs, past failures, positioning, authority, mechanism
- **Most-aware** → trust, offer, final persuasion

**The shift rule:** name the stage the ad is written in, then write the advertorial at least one stage deeper.
- **Problem-aware ad** (introducing the problem and mechanism) → advertorial picks up at **solution-aware or product-aware**: proof, authority, comparison, social validation.
- **Solution-aware ad** → advertorial goes deeper into **product-aware**: objections, past failures, positioning.
- **Product-aware ad** → advertorial goes **most-aware**: trust, offer, final persuasion.

This is the awareness-level expression of Confirm-and-Escalate: confirmation lives at the ad's stage, escalation lives at the advertorial's stage. If the advertorial spends its body at the same stage as the ad, it is echoing — no matter how different the words are.

---

## The Confirm-and-Escalate Principle

This is the governing principle for every ad-driven advertorial. It replaces the old model where advertorials were standalone persuasion pieces that built belief from scratch.

**Confirm:** Acknowledge what the reader already believes in 2-4 sentences. Use the same core metaphor from the upstream ad. Don't re-teach it. Reference it like shared knowledge. This confirmation validates the reader's intelligence, bridges the ad-to-page transition, and signals that this page respects their time.

**Escalate:** Deliver what the ad structurally couldn't. New credibility. New proof category. New depth on a specific objection the ad didn't have room to address. The advertorial adds a layer the reader didn't have — and that layer converts them from "interested" to "ready to buy."

**The weight split:** 15-20% confirmation and bridge. 80-85% escalation, proof, objection handling, and close. If more than a fifth of the advertorial is mechanism education the reader already has, you're echoing.

**Assume mixed readership:** some readers consumed the full ad; others skimmed it. Reference the mechanism briefly and confidently — enough that a skimmer can follow, never so much that a full reader feels re-taught.

**What the reader arrives WITH (from the ad):**
- Emotional investment in the problem
- Understanding of the root cause (the mechanism)
- Belief that their current solutions target the wrong thing
- A mental checklist of what the right solution must do
- Curiosity about whether something actually addresses it

**What the reader arrives WITHOUT:**
- Confidence that THIS specific product is the one
- Trust in the brand behind it
- Answers to their remaining objections
- Proof from a DIFFERENT source than the ad's narrator
- Enough certainty to put their credit card in

The advertorial's job is to deliver what's missing — not repeat what's already installed.

---

## The Six Frameworks

Every advertorial uses one of six frameworks. These are orientations — a direction the piece leans, not a box it's locked into. A good advertorial might blur the line between two. That's fine. The frameworks exist to prevent structural errors and guide narrator selection, not to constrain creative execution.

### Framework 1: Authority Expert

A credentialed figure — doctor, researcher, specialist, physical therapist, pharmacist — delivers independent confirmation of the mechanism and adds a layer of credibility the peer-voiced ad couldn't provide.

**Why it works:** The upstream ad is peer-voiced. The reader identified with the narrator. But identification alone doesn't close a skeptical buyer. Authority closes the gap between "I believe her story" and "I trust this product."

**The authority is NOT lecturing. The authority is revealing.** A lecture re-teaches. A revelation shows something new — something the reader couldn't have found on their own. The authority has access the reader doesn't: clinical data, patient patterns, insider knowledge about why the system fails.

**Authority establishment:** Credential + tension + inciting incident within the first 50 words. Not a bio — an inciting incident. "I stopped prescribing the drug I was trained to prescribe after watching my 847th patient complain about the same side effects" beats "I'm Dr. Sarah Chen, preventive cardiologist" every time.

**Authority narrator types:**
- **The Renegade Clinician** — diverged from standard of care. "I prescribed statins for seventeen years. I don't anymore."
- **The Pharmacist Who Sees Everything** — fills prescriptions, watches refills, sees what doctors don't. "I've filled 40,000 prescriptions. I know which ones people stop taking."
- **The Researcher** — studies the mechanism professionally. Tension: gap between research and clinical practice.
- **The Physical Therapist / Practitioner** — hands-on, 20-55+ years, thousands of patients. "In 55 years and 6,000 patients, the pattern never changed."
- **The Investigative Voice** — health journalist or writer who investigated the topic. Credibility is objectivity.

### Framework 2: Crisis Narrative

A single person's dramatic story drives the entire piece. The crisis creates emotional stakes. The discovery resolves it. The product introduction feels inevitable.

**Why it works:** The reader lives the discovery WITH the narrator. They don't feel sold to — they feel like they witnessed someone's breakthrough.

**Crisis narrative beats:**
1. Dramatic opening moment (the fall at the graduation, the 2:47 AM emergency, the wife on the bathroom floor)
2. Problem escalation (tried everything, costs mounting, identity eroding)
3. Intervention moment (neighbor's suggestion, doctor's offhand remark, desperate late-night research)
4. Mechanism learned THROUGH the story (not a separate education section)
5. Product discovery and skeptical evaluation
6. Transformation with specific measurable results
7. Close with urgency tied to the emotional arc

### Framework 3: System Exposé / Whistleblower

A patient, former insider, or system survivor reveals something about the medical system, the industry, or the standard of care that reframes understanding. Credibility comes from lived experience PLUS insider access.

**Why it works:** This audience has been failed by authority figures. A patient or whistleblower who has been through the same system — and found where it broke — speaks a language authority figures can't.

**The whistleblower tells a DIFFERENT story that independently arrives at the same conclusion as the ad.** Two different people, two different paths, same truth. That's not a sales pitch. That's a pattern.

**Whistleblower narrator types:**
- **The Records Requester** — found something the doctor never mentioned
- **The Former Industry Rep** — knows how products are marketed vs. how they work
- **The Retired Insider** — can now say what they couldn't while employed
- **The Trial Participant** — saw something from inside a clinical study
- **The Support Group Moderator** — has heard hundreds of versions of the same story

### Framework 4: Expert Comparison / Review

An expert or editorial voice reviews multiple options, evaluates each against criteria, and reveals a winner. The recommended product emerges from seemingly objective evaluation.

**Why it works:** The audience knows they need something but is overwhelmed by options. The primary objection is "which one?" not "should I?"

**Comparison structure:**
1. Problem framing (why this category matters now)
2. Evaluation criteria established (3-5 things that matter, explained with authority)
3. Competitor reviews — each gets a brief assessment and a verdict on its weakness
4. Winner reveal — positioned as meeting all criteria
5. Deeper dive on the winner with social proof
6. Close with risk reversal

**Comparison formats:** Side-by-side table, sequential review, or "Why They All Failed You" chart (competitor in one column, failure reason in the second, cost in the third).

### Framework 5: Listicle / Discovery

Structured as numbered revelations. "7 Hidden Truths Every GLP-1 User Must Know." Each item builds the case progressively until the product emerges as the logical conclusion.

**Why it works:** The audience is in research mode. They want to feel informed, not sold to. The listicle earns trust through consistent value delivery before asking for the sale.

**Rules:** Each numbered item must be independently valuable. If the reader stopped at item 3, they should still feel they learned something. The product is introduced in the final 1-2 items or immediately after the list concludes.

### Framework 6: Suppression / Conspiracy

The product or science behind it has been buried, hidden, or attacked by the establishment. The product exists despite resistance, not because of support.

**Why it works:** The audience already distrusts the system. They believe industries protect profits over patients. The suppression angle explains WHY they haven't heard of this before.

**Key element: The economic motive.** WHY would the system suppress this? Can't patent it. Eliminates recurring revenue. Makes expensive procedures unnecessary. Tie the motive to something the reader has personally experienced — their $3,000 medical bill, their 12-minute appointment, their insurance denial.

**Urgency through suppression:** "We've received cease-and-desist letters." "Forced to remove by midnight." "Surgeons are filing injunctions." Urgency feels real because it's tied to narrative conflict.

### Choosing a Framework Based on the Upstream Ad

| If the upstream ad used... | Lean toward... | Because... |
|---------------------------|---------------|------------|
| Peer narrator (sufferer telling her story) | Authority Expert | Adds a different credibility category |
| Peer narrator with strong guide character | Whistleblower or Crisis Narrative | Avoids doubling up on authority |
| Spouse/witness narrator | Either — avoid another spouse voice | Voice register must shift |
| Analytical narrator (systems thinker) | Whistleblower with insider angle | Matches desire for insider data |
| Emotional narrator (identity/grief-driven) | Authority Expert | Shifts from emotional to clinical — creates contrast |
| Any narrator — audience deeply distrusts system | Suppression / Conspiracy | Validates their distrust and gives a reason |
| Any narrator — audience overwhelmed by options | Expert Comparison | Answers "which one?" directly |
| Any narrator — audience in research mode | Listicle / Discovery | Earns trust through progressive education |

**The governing principle:** Whatever the ad delivered, the advertorial delivers something the ad structurally COULDN'T. Contrast creates the perception of independent confirmation.

**Frameworks blend.** A Crisis Narrative can encounter an Authority figure. A Suppression piece can include Comparison elements. An Authority can open with a patient case study. One center of gravity — the borrowed elements support it.

---

## The 13 Advertorial Laws

Non-negotiable. Apply to every advertorial regardless of framework.

### Law 1: The Headline Sells the Article, Not the Product
Product name NEVER appears in the headline. The headline must trigger the same click impulse as a real article. See `references/swipe-pattern-library.md` for 8 headline formula patterns extracted from top-performing swipes.

### Law 2: The Opening Delivers on the Ad's Promise — Without Repeating It
The first 150-200 words validate whatever curiosity drove the click. The emotional temperature continues from the ad's exit state — it doesn't restart. The reader must know within 50 words that this is a DIFFERENT person talking. **Never repeat the ad's opening** — open with curiosity or drama that aligns with the ad's angle but approaches from the new awareness stage.

### Law 3: Confirm, Don't Re-Teach
The mechanism gets 2-4 sentences of confirmation. Same metaphor as the ad. Brief, confident, validating. Assume some readers consumed the ad and others skimmed it — reference the mechanism, don't re-explain it in full. The ONLY exception: genuinely new depth the ad didn't cover. That's escalation, not echo.

### Law 4: The Advertorial Adds What the Ad Couldn't
The advertorial's job is to complement, not duplicate. Every advertorial must deliver **at least two complementary layers that are NOT already in the ad copy**:
- **Social proof** — testimonials, reviews, customer stories transformed into narrative
- **Authority** — expert perspective, doctor or practitioner endorsement, third-party credibility
- **Comparison framing** — why other approaches fail, what competitors hope customers never figure out
- **Story-driven angle** — founder story, customer transformation story, market narrative
- **Objection handling** — address beliefs the audience holds from past failed solutions

Additional escalation elements that also qualify:
- Clinical data or research depth beyond what a peer narrator would credibly deliver
- Broader proof density — multiple people's results, not just one narrator
- Insider information about the industry or the standard of care
- A different emotional angle on the same truth
- Economic motive explanation (why the system fails this audience)

### Law 5: The Product Enters Through the Mechanism
The product is NEVER introduced before the mechanism is established. The mechanism creates the evaluation criteria. The product meets the criteria. Introduction patterns: authority assessment, crisis discovery, research conclusion, comparative winner, or insider revelation.

### Law 6: Social Proof From Multiple Categories
Layer different proof types. Individual stories + professional observation + community aggregation + clinical citation + comment section. Each piece in the funnel adds a DIFFERENT type. The combination creates triangulated belief. See `references/swipe-pattern-library.md` for full social proof architecture.

### Law 7: Formatting Serves the Editorial Frame
Publication masthead and breadcrumbs, scannable headers, bold for mechanism terms (not sales language), comparison tables, images/diagrams, pull quotes. Every formatting choice serves reading momentum and editorial credibility. Keep paragraphs short. Use subheads.

### The funnel-conditional close (shared rule across the copy library)

This is the same rule the long-form ad skill, the listicle skill, and the copy-chief grader all run on. It governs how hard the close pushes, and it keys off ONE input: where this page sends.

**The advertorial is, by default, the soft-close destination of a 2-step funnel.** The upstream ad's only job was the click; this page carries the conviction load. But the advertorial itself then forks the same way:

- **Bridge advertorial (ad → advertorial → dedicated PDP → checkout):** the advertorial's own close is SOFT — the CTA Bridge (Law 8). No "buy now," no hard apparatus here; it primes the dedicated PDP, which carries the hard close (guarantee, scarcity, urgency). The hard push lives one page downstream.
- **Standalone / fused advertorial (ad → advertorial → checkout, no separate PDP):** the advertorial IS the salesletter, so it carries the HARD conversion close itself — guarantee, risk reversal, urgency, repeated CTA. See `references/standalone-mode.md`.

**"Soft" means push intensity, not brand concealment.** A soft close can name the product and leave the reader Product-Aware; what makes it soft is the absence of the hard apparatus (no guarantee-stacking, scarcity, or urgency). There is no rule that the brand must be hidden. Don't over-engineer a brand-withholding rule.

**Why default soft on the bridge:** as native ad formats saturate and market sophistication rises, response to the hard close decays. Withholding the hard apparatus until the PDP keeps the editorial frame intact and makes the advertorial reusable across cold audiences. Match to avatar — colder, more ad-fatigued readers tolerate the hard apparatus least.

### Law 8: The CTA Bridge Is a Continuation, Not a Pitch
The CTA bridge is where most conversion money is lost. A CTA that says "buy now" or "shop here" the moment the argument lands is a hard left turn that reminds the visitor they're being sold to. The frame breaks.

**The bridge that converts sounds like the next paragraph, not an ad.** It continues the narrative voice and connects the argument to the product as a logical next step. It connects the new angle back to the product and the ad's mechanism — referencing the mechanism briefly, never re-explaining it in full. The visitor should feel like clicking is the next step in their research, not a transaction. The CTA itself is direct, urgent, and aligned with the offer.

**Bridge formula:** "We built [Product] specifically because of [mechanism]. Here's what it does and what to expect in the first 30 days." Then the button.

**What kills bridges:**
- "BUY NOW" or "SHOP HERE" after an editorial narrative — jarring tonal shift
- Any language that breaks the editorial frame and reveals the sales intent
- CTAs that appear before the argument has fully landed
- Generic button text that could be on any product page

**What converts:**
- Language that frames the click as a continuation of the discovery ("See what [Product] does differently")
- Specific expectation-setting before the click ("Here's what happens in the first 30 days")
- The button text matches the editorial register, not a commerce register
- The CTA paragraph TELLS the reader what they'll find on the next page — this primes the PDP handoff

### Law 9: The Close Matches the Framework's Voice
Authority closes with clinical language. Crisis narrators close with personal urgency. Whistleblowers close with "I wish someone had told me sooner." Comparison narrators close with editorial recommendation. The close must feel native to whoever's been narrating. See `references/swipe-pattern-library.md` for full close component architecture.

### Law 10: Objections Are Handled Inside the Narrative
The best advertorials dissolve objections WITHIN the story — not in a bolted-on FAQ section. The authority addresses safety while explaining the mechanism. The crisis narrator addresses cost while describing their discovery. Exception: FAQ sections work near the close for logistics questions (sizing, shipping, dosage).

### Law 11: Write With the PDP Handoff in Mind
The advertorial is not a standalone piece. It is stage 2 of a 4-stage chain. Whatever language, mechanism, and emotional frame the advertorial closes on, the dedicated PDP MUST open with.

**This means the advertorial writer must think about what they're priming:**
- If the advertorial closes on bioavailability as the key mechanism, the PDP hero section leads with bioavailability — not "premium greens blend" or "16 superfoods"
- If the advertorial closes on a specific result timeline ("visible changes in 30 days"), the PDP leads with that timeline
- If the advertorial's narrator uses specific language ("clearing the pathway"), the PDP mirrors that exact language

**The visitor arriving at the PDP is warm.** They have been through the advertorial's argument. If the PDP feels like a different brand — different language, different emphasis, different visual tone — the visitor cognitively resets. The belief work you paid for is erased.

**Dedicated PDP requirements:**
- Advertorial traffic goes to a DEDICATED product page, never the main PDP
- The dedicated PDP strips header navigation, removes exit points, mirrors the advertorial's visual tone
- The dedicated PDP leads with whatever the advertorial closed on
- One URL for cold/discovery traffic. One URL for advertorial traffic. Always.

**The diagnostic:** If conversion drops at the PDP step, you have a handoff problem, not a product problem. Not a copy problem. Not a price problem. A handoff problem.

### Law 12: Every Sentence Earns Its Place
Ad-driven advertorials run 800–1,200 words — shorter than the upstream ad, never longer. This audience wants to get to the point; don't pad with unnecessary repetition. Every sentence must build belief, handle an objection, deepen trust, or move toward the sale. If it does none of these, cut it.

### Law 13: The Rule of One
One avatar (specific, not generic). One deep desire. One core message. Every sentence serves that single thread. If a paragraph serves a second avatar, a second desire, or a second big idea, cut it — or save it for a different advertorial (see Anti-Mimicry).

---

## Section Architecture (Ad-Driven)

Every ad-driven advertorial runs on a five-part spine:

- **Hook** — open with curiosity or drama that aligns with the ad's angle but approaches from the new awareness stage. Do NOT repeat the ad's opening.
- **Lead** — 2–3 paragraphs that establish the new angle and pull the reader in.
- **Body** — the complementary layers (proof, authority, comparison, story). Short paragraphs. Subheads.
- **Bridge** — connect the new angle back to the product and the ad's mechanism. Reference it briefly, don't re-explain it in full — assume some readers consumed the ad; others skimmed it.
- **CTA** — direct, urgent, aligned with the offer (soft-register on bridge pages per Law 8).

The eight sections below map onto that spine:

| Section | Spine | Words | Function |
|---------|-------|-------|----------|
| 1. Editorial Frame + Headline | Hook | 40-60 | Publication masthead, breadcrumbs, byline, headline, subhead |
| 2. Opening Hook + Bridge | Hook / Lead | 100-150 | Validates ad promise from the NEW stage, bridges emotional state, establishes new voice |
| 3. Mechanism Confirmation | Lead | 40-80 | Confirms installed beliefs in 2-4 sentences. NOT re-teaching. |
| 4. Escalation / New Value | Body | 250-400 | The main event. The complementary layers the ad couldn't deliver. |
| 5. Product Confidence | Body | 120-200 | Objection handling through product assessment, dosing depth, safety, differentiation |
| 6. Proof Density | Body | 120-200 | Multiple sources, different proof category than ad |
| 7. CTA Bridge | Bridge | 50-100 | Continuation-style transition that connects the argument to the product. NOT "buy now." Primes PDP language. |
| 8. Conversion Close | CTA | 80-200 | Offer, CTA, post-CTA reinforcement (full hard apparatus only in standalone mode) |
| **TOTAL** | | **800-1,200** | Shorter than the ad, never longer. The ad already did the belief work. |

### Section Details

**Section 1 — Editorial Frame:** Publication name (plausible niche outlet, NOT a real publication). Category breadcrumbs. Headline: 10-20 words, makes a claim about the problem or system failure. Subhead: 1-2 sentences with symptom/situation callouts. Byline: name, credential/title, date.

**Section 2 — Opening Hook:** Match the ad's exit state. Establish the new voice within 50 words. Never repeat the ad's opening. Signal what the reader will get from this page that they didn't get from the ad. Authority opens with credential + tension. Crisis opens with discovery + stakes. Whistleblower opens with revelation + personal cost.

**Section 3 — Mechanism Confirmation:** The briefest section. Uses the same metaphor as the ad. Adds the professional stamp ("this is textbook pathophysiology") or the pattern stamp ("I've heard this same story from hundreds of people"). If the mechanism needs deeper treatment, read `references/mechanism-education.md`.

**Section 4 — Escalation:** Every sentence passes the escalation test: "Did the reader already know this from the ad?" If yes, cut it. The new value comes from the narrator's unique vantage point. Authority adds clinical depth. Whistleblower adds system exposure. Crisis narrator adds a different discovery path. Comparison adds competitive context.

**Section 5 — Product Confidence:** NOT a product introduction — the reader knows the product from the ad. Frame every product detail as an answer to a question the reader is already asking. Authority assesses through professional criteria. Crisis narrator confirms through experience. Comparison narrator evaluates against established criteria.

**Section 6 — Proof Density:** Different category than the ad's proof. If the ad used personal story → advertorial uses aggregated proof. If the ad used emotion → advertorial uses clinical data. Three independent sources triangulating the same conclusion.

**Section 7 — CTA Bridge:** This is NOT a CTA button. It is a 2-4 sentence paragraph that connects the argument you just made to the product page the reader is about to visit. It sounds like the next paragraph of the article, not a sales pitch. It tells the reader what they'll find and what to expect. It uses the same language the PDP will use — because the PDP was built to continue this exact conversation. Example: "That's why the team behind [Product] focused entirely on [mechanism]. Here's what it does differently — and what most people notice in the first 30 days." Then the button, with text like "See how it works" or "Learn more about [Product]" — NOT "Buy Now" or "Shop Here."

**Section 8 — Conversion Close:** Direct and urgent, in the framework's voice. On bridge pages, keep it soft-register (Law 8). On standalone pages it is multi-component — see `references/swipe-pattern-library.md` for the full six-component close architecture: value summary, pricing psychology (6 patterns), guarantee/risk reversal, urgency (5 patterns), CTA placement strategy, and post-CTA reinforcement.

### The Post-Reveal Skepticism Run (MANDATORY — locked 2026-07-27)

**Never close the sale immediately after the product reveal.** The reveal answers "what is it?" — it does not answer "why should I believe you?" The reader who was going to click already clicked the first CTA; everything after the reveal exists for the skeptic who kept scrolling. Model: the Blyme Prime Elixir swipe (`brands/motilli/swipe/blyme-prime-elixir/`), which runs a full back half after naming the product.

After the reveal section + first CTA, continue in the SAME narrator voice with (pick 3-5, in roughly this order):
1. **Comparison chart** — the failed-solutions table: each thing the reader owns vs. where it works vs. the product. A table is a different FORMAT than the ad's narrative takedown, so it doesn't echo.
2. **Expectations timeline** — what week one/two/three actually feel like, including the honest "quiet start — don't quit on day four" beat. Kills the silent refund-and-churn objection before purchase.
3. **Reviews block** — 2-4 "Verified Buyer" style reviews spanning demographics, INCLUDING one slow-responder/almost-returned-it review. The imperfect review converts harder than the glowing ones.
4. **Guarantee expansion** — the full no-hoops policy, reframed as "what does it cost me to find out?"
5. **Two-options close** — Option 1 (keep doing what you're doing, painted concretely) vs. Option 2 (try it risk-free), plus the "you didn't read this far for nothing" consistency beat. THEN the final CTA.

CTA placement across the run: reveal CTA → mid-run CTA (varied language, e.g. "See Current Pricing") → final CTA after two-options. Max 4 total. A sticky "Check Availability" button in the page build covers the reader who's ready early.

**Word count interaction:** the 800–1,200 band covers the STORY (hook through reveal). Pages that run the full skepticism run — universal pages especially — land at ~1,800–2,100 total. That is the correct length for a universal/high-skepticism page; do not cut the run to protect the band.

---

## Word Count Targets

**Ad-driven (complementary) default: 800–1,200 words for the story (hook through product reveal) — the story stays shorter than the upstream ad.** The ad already did the belief work; the advertorial complements, it doesn't duplicate. This audience wants to get to the point. Stretch the story above 1,200 only when the pre-flight demands it (a low-selling/curiosity-gap upstream ad that built little belief, or a high-ticket/complex-mechanism product).

**The Post-Reveal Skepticism Run is ON TOP of the band, not inside it.** A page running the full post-reveal run (see Section Architecture) lands at ~1,800–2,100 total — universal pages that receive traffic from multiple ads should always run it. Never close immediately after the reveal to stay inside the band.

| Product Type | Ad-Driven | Standalone |
|-------------|-----------|-----------|
| Simple consumer product (<$50) | 800-1,000 | 1,800-2,500 |
| Supplement / health product ($30-80) | 800-1,200 | 2,200-3,500 |
| Medical device / premium ($80-200) | 1,000-1,500 | 3,000-4,500 |
| High-ticket / surgery alternative ($200+) | 1,200-2,000 | 3,500-5,000+ |

Longer copy correlates with higher price points and more complex mechanisms. But every word earns its place regardless of length.

For standalone word counts and architecture, see `references/standalone-mode.md`.

---

## Pre-Writing Locks

Before writing any advertorial, confirm ALL of the following:

1. **What ad is driving traffic?** Read it. Know its awareness stage, angle/storyline, avatar, narrator, mechanism/USP, metaphor, desire targeted, tone/voice/language patterns, emotional exit state, and installed beliefs. If no ad → read `references/standalone-mode.md`.
2. **Stage shift locked?** Name the ad's awareness stage AND the advertorial's target stage. They must be different (see The Awareness-Stage Shift).
3. **Rule of One locked?** One specific avatar, one deep desire, one core message — written out in one line each. Every sentence will serve that thread.
4. **Framework?** Which of the six? Or a blend — with which center of gravity?
5. **Who is the narrator?** Specific person with specific credentials or experience. What's their inciting incident? What do they know that the reader doesn't?
6. **What does this advertorial ADD?** Name at least two complementary layers NOT in the ad (Law 4 menu: social proof, authority, comparison framing, story-driven angle, objection handling).
7. **What's the primary objection?** The central objection this page exists to dismantle.
8. **Editorial frame?** Publication name, byline, category breadcrumbs.
9. **Core metaphor continuity?** Same metaphor as the ad. Can extend. Cannot replace.
10. **Avatar language sourced?** Pull phrases from the brand's market research files (reviews, VOC, research docs) if available — how the customer actually speaks and thinks, not corporate marketing language.
11. **Social proof format?** Which patterns, and how do they differ from the ad's proof type?
12. **Close architecture?** Pricing pattern, urgency type, guarantee framing. See `references/swipe-pattern-library.md`.
13. **CTA bridge language?** What exact language will the CTA bridge use? This language must match the PDP hero section. If no dedicated PDP exists yet, flag this — the advertorial writer defines what the PDP must open with.
14. **Dedicated PDP?** Does a dedicated PDP exist for this advertorial traffic? If not, flag it as a critical conversion risk. Advertorial traffic should NEVER go to the main product page.
15. **Word target?** 800–1,200 and shorter than the upstream ad (unless standalone).
16. **Anti-mimicry check?** What advertorials already exist for this product? What's been used?

---

## The Handoff Tests

Before finalizing, run these seven tests:

**1. Emotional Bridge Test (Ad → Advertorial):** Read the last 200 words of the upstream ad, then the first 200 words of the advertorial. Does the emotional temperature flow?

**2. Echo Test:** Highlight every sentence that restates something the ad already taught. If highlighted text exceeds 15% of word count, cut it.

**3. Stage-Shift Test:** Name the awareness stage of the ad and the stage the advertorial's body operates at. If they're the same stage, the piece is a rehash — rebuild the body at the deeper stage. Also check the hook: does it approach the ad's angle from the NEW stage, or does it re-run the ad's opening?

**4. Rule of One Test:** State the one avatar, one desire, one message in a single sentence each. Then scan every subhead and paragraph: if any section serves a different avatar, desire, or message, cut it.

**5. Escalation Test:** List everything the advertorial delivers that the ad didn't. If the list is shorter than three items, add value.

**6. CTA Bridge Test:** Read the last paragraph before the primary CTA button. Does it sound like a continuation of the article, or does it sound like a sales pitch? If you can hear the tonal shift from editorial to commerce, rewrite it. The reader should feel like clicking is the next step in their research, not a transaction.

**7. PDP Handoff Test (Advertorial → Dedicated PDP):** Read the last 200 words of the advertorial (including the CTA bridge), then read the PDP hero section. Answer these questions:
- Does the PDP lead with the same mechanism/language the advertorial closed on?
- Would the visitor feel like they're on the same journey, or like they landed on a stranger's page?
- Does the PDP strip navigation and remove exit points for advertorial traffic?
- Is there a SEPARATE URL for advertorial traffic vs. cold/discovery traffic?

If the PDP feels like a different brand than the advertorial, you have a handoff problem. The advertorial copy may be perfect — but if the PDP doesn't continue the conversation, the conversion will still die at checkout.

---

## Anti-Mimicry

When writing multiple advertorials for the same product, each must use:
- A different FRAMEWORK
- A different NARRATOR
- A different AWARENESS STAGE (where the funnel allows)
- A different PRIMARY OBJECTION
- A different PROOF FORMAT
- A different OPENING EVENT
- A different URGENCY TYPE

The test: if someone read two advertorials for the same product and said "these are basically the same page," the copy failed.

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
Complementary Layers: [the 2+ layers NOT in the ad — from the Law 4 menu]
Narrator: [specific person, credential/experience, inciting incident]
Publication Name: [editorial frame]
Byline: [name, credential, date]
Primary Objection Handled: [central objection]
Metaphor Continuity: [same metaphor, extended how]
Proof Format: [which patterns, how they differ from ad]
CTA Bridge Language: [what the bridge paragraph will say — this defines the PDP hero]
Dedicated PDP: [URL if exists / "NEEDED — flag for build" if not]
PDP Hero Must Lead With: [exact language/mechanism the PDP opens on, based on advertorial close]
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

[Audit checklist results]
```

---

## Final Audit Checklist

### Confirm-and-Escalate Compliance
- [ ] Awareness stage shifted? (ad's stage ≠ the stage the advertorial's body operates at)
- [ ] At least 2 complementary layers delivered that are NOT in the ad?
- [ ] Mechanism confirmation is 2-4 sentences maximum? No re-teaching?
- [ ] Same core metaphor as upstream ad?
- [ ] Echo test passed? (<15% restated content)
- [ ] Emotional bridge from ad exit state to advertorial opening?
- [ ] Same pitch/narrative structure NOT re-run? (different room, same house)

### Law Compliance
- [ ] Law 1: Headline sells article, not product?
- [ ] Law 2: Opening validates ad promise from the new stage — without repeating the ad's opening?
- [ ] Law 3: Mechanism confirmed, not re-taught?
- [ ] Law 4: Complementary layers delivered?
- [ ] Law 5: Product enters through the mechanism?
- [ ] Law 6: Social proof from multiple categories?
- [ ] Law 7: Formatting serves editorial frame? Short paragraphs, subheads?
- [ ] Law 8: CTA bridge sounds like a continuation — and the CTA itself is direct, urgent, offer-aligned?
- [ ] Law 9: Close matches framework voice?
- [ ] Law 10: Objections handled inside the narrative?
- [ ] Law 11: Written with PDP handoff in mind? Closing language matches PDP hero?
- [ ] Law 12: Every sentence earns its place? Word count 800-1,200 and shorter than the ad?
- [ ] Law 13: Rule of One — one avatar, one deep desire, one core message throughout?

### Structural Audit
- [ ] Hook → Lead → Body → Bridge → CTA spine intact?
- [ ] Editorial frame is believable and consistent?
- [ ] Narrator voice is distinct from the ad's narrator?
- [ ] Primary objection explicitly addressed?
- [ ] Product differentiation clear?
- [ ] Proof from multiple sources and categories?
- [ ] Pricing justified?
- [ ] Urgency story-driven?
- [ ] Guarantee removes risk?
- [ ] CTA bridge language matches editorial tone? (NOT "buy now")
- [ ] CTA bridge primes the PDP hero section language?
- [ ] Dedicated PDP specified or flagged as needed?

### Language Audit
- [ ] Written in the customer's voice — how they actually speak and think, not corporate marketing language?
- [ ] Language and phrases pulled from the market research files where available?
- [ ] No hallucinated statistics or claims?
- [ ] Bold text for mechanism terms, not sales emphasis?
- [ ] Headers create scannable entry points?
- [ ] Voice consistent throughout?
- [ ] No visual design notes or meta-commentary inside the copy?
