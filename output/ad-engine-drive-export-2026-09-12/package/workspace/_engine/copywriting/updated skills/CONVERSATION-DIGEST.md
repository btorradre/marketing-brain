# Long-Form Copy — Conversation Digest

A distilled record of the chats where we built, refined, and used the long-form copy system. Each entry has the link, what it covered, and the decisions worth carrying forward. This is context for the agent — the operational rules live in the `skills/` files.

---

## 1. Ceylon Cinnamon Audience Awareness
**Link:** https://claude.ai/chat/8ccc7a85-fa98-445f-aed1-e2ac1c005510
**This is the most important thread for the agent.** It's where the writing system got rebuilt.

What we did:
- Diagnosed that the existing `long-form-copy` skill optimized for the wrong avatar. Its center of gravity was "the story IS the ad — run emotional clearing at 55–65%," which is correct for a **problem-aware / unaware** reader but wrong for what we're actually writing now: **product-aware, Stage-4 sophistication** copy (the nurse-insider-leaking-why-a-format-fails concept).
- Rebuilt the skill around **six locks + three passes**: a pre-draft lock phase (five locks + engine declaration), the draft, then a three-pass audit. Slimmed the skill from ~1,450 lines toward a ~500-line target by stripping superseded laws.
- One audit mechanic worth noting: the mechanical check for personified-inanimate writing — *inanimate noun + human verb = rewrite* — because by ear those lines read as "vivid," which is exactly why AI-pattern lines slip through.
- Wired three skills to reference each other by name: **copy-strategy → concept-databank → long-form-copy**, so there's one source of truth and the brief's fields map one-to-one onto the writing skill's locks.
- Built out the final **copy-strategy** skill as the front end (engine-rotation wiring lives here; it pulls concepts by name from concept-databank rather than re-listing them).

Strategic note captured: the copy can't open with "cinnamon lowers blood sugar" — ~55% have heard it and ~40% think it's a scam. It validates the failure first ("you tried the cheap stuff, here's why it did nothing"), then installs the mechanism almost nobody knows. The whitespace isn't the spice — it's the unclaimed mechanism.

> Note: `concept-databank` is referenced by these skills as the twelve-vehicle library but was not part of this export — if the agent needs it, it should be exported separately.

---

## 2. Improving Hook Generation With Copy Patterns
**Link:** https://claude.ai/chat/40e231bb-4ea0-4bb0-9ba9-bd045e76680e

What we did:
- Read all the long-form swipe files and extracted recurring hook patterns, then folded them into the `hook-generation` skill.
- Added new hook types (14–18), including **The Effort Betrayal** (the avatar's own discipline is the hook — she didn't cut corners), **Observed-Change** (someone else detects the transformation first — smuggles social proof into line one), and the **Exoneration Reframe** (overturns self-blame: "not broken — blocked").
- Added a **Generational Refusal** contrarian subtype ("My father took X for 22 years… I refused… and what I found instead…") — flagged as the most-replicated skeleton in the library, with a terror/grief engine and saturation risk so it doesn't get defaulted into every brief.
- Added two templating axes: **Place/Source Swap** and **Headline-Stack Rotation** (the pipi_tea logic — hold the proven body constant, rotate only the opener; cheapest high-leverage test available).
- Added a sixth pattern-interrupt mechanic (promised indignation / "three things happening right now") plus matching updates to awareness mapping and the Hook Autopsy examples.
- Kept mechanism congruence out of scope (that lives in `hook-congruence`) and folded in light compliance/engine-rotation cautions where patterns lean on terror or fabricated authority.

---

## 3. Market Awareness Stage From Updated Avatar Research
**Link:** https://claude.ai/chat/4b9e76bd-0f36-4f66-9862-fdc009cc73f7

What we did:
- Wrote a set of five long-form ads for **Renavita** (Ceylon Cinnamon Gummies), modeled on the Metabolae structure — same hooks/patterns/structure, rewritten with different numbers, NOT word-for-word (to avoid high CPMs from duplicate copy).
- Locked the **rust** core metaphor (the anti-mimicry swap away from Metabolae's clogged-sink) and the chew/enzyme delivery as the differentiation.
- Anti-mimicry move: each ad gets its **own narrator** — distinct name, distinct credential, internally consistent — rather than one repeated "Sandra." This also fixes Metabolae's credential contradiction across its five ads.
- Held the line on not inventing a clinical ingredient claim: would not write a chromium objection unless chromium is actually in the formula.

---

## 4. Met Forman as Villain Character (Angle / Concept Strategy)
**Link:** https://claude.ai/chat/f864a476-93f4-4991-aad1-db455492ec17

What we did:
- Deconstructed three competitor ads (two nurse-narrator kidney-decline ads, one "why cinnamon fails" ad) to extract each one's **angle**, **desire angle**, **concept**, and **sophistication stage**.
- Reached the core strategic decision: Metabolae's emotional architecture, desire angles, and narrator concepts can be adapted as inspiration, but the **mechanism layer must be rebuilt** — Metabolae's softgel-absorption-superiority argument directly contradicts the gummy format.
- Identified the **inversion play**: for an avatar whose GI tract is compromised by years of harsh oral meds, chewable/buccal delivery bypasses the damaged gut and becomes the *superior* mechanism, not an inferior one.
- Native differentiators: zero-sugar / zero-maltitol (neutralizes the "sugar paradox" objection) and no pill fatigue (avatar is already capsule-overwhelmed).
- Flagged the category-maturity mismatch: gummy format sits at Stage 1–2 maturity despite a Stage 4–5 audience — a mechanism-reset opportunity to re-virginize fatigued claims.
- One correction: the audience's cinnamon skepticism in the reviewed ad is driven primarily by **absorption format and dosing failures**, with Cassia-species mislabeling as secondary support — a weighting distinction that matters for how copy structures its argument.

---

## 5. Document Review and Analysis (System Review + Boundaries)
**Link:** https://claude.ai/chat/da799523-ed55-4dcd-a5e5-a8583a403d2c

What we did:
- Reviewed the full copywriting system and acknowledged the craft — its grounding in the DR canon (Ogilvy, *Scientific Advertising*, *Great Leads*, *Reason Why*) and its structural soundness.
- Recorded the boundaries that apply when *producing* copy: no narrator personas presented as real people, no advertorial formats built to pass as editorial, no disease/condition-treatment claims aimed at vulnerable audiences, no fabricated clinical-pathology imagery. The standing alternative offered: compliant, persuasive copy grounded in real proof assets, consented testimonials, and structure/function claims.

This is included so the agent inherits the same boundaries rather than rediscovering them.

---

## Threads intentionally left out
Two adjacent chats — *Copying competitor product images for new brand* and *Image replication with Higgsfield MCP and GPT* — were about product-image generation, not long-form copy, so they're not part of this export.
