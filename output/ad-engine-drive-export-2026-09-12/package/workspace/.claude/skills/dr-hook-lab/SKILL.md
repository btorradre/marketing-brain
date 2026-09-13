---
name: dr-hook-lab
description: Write five genuinely different hook variations for one angle, each aimed at one specific person at one awareness level, in the customer's own recorded language. Part of the Direct Response OS. Use when the user says "write hooks", "give me hook variations", "5 hooks for this angle", "new opening lines", "the hook isn't landing", "rewrite the first 3 seconds", or picks an angle from the bank to brief. Reads the angle record and the VoC index so hooks are built from real quotes rather than invented phrasing, runs the AI-tell blacklist and the swap test on every line, and writes brands/<brand>/research/dr-os/hooks/<angle-id>-<slug>.md.
user_invocable: true
---

## GOLDEN NUGGET DOCTRINE (MANDATORY — locked 2026-07-11)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded DEEP FRAME in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: *is this the topic, or is this the motive?* If it's the topic, dig one layer deeper (memory loss → becoming my parent; GLP-1 bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes.** The golden nugget LEADS — very top of the piece, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence BEFORE drafting. When analyzing a reference ad/funnel/swipe instead of writing, state the nugget it's built on and whether it leads with it. If the research hasn't surfaced one, mine reviews/VOC/Reddit until it does — never default to a surface angle.

# DR OS — Hook Lab

A hook is not a headline. It is a decision made in under two seconds. The job is not to make it sound good, it is to make the right person stop because this was obviously made for them.

**Where hooks sit.** One avatar is a campaign, one angle is an ad set, and the hooks written here are the **ad variations inside that one ad set**. They all argue about the same problem and differ in how they open it. If a candidate line changes the problem rather than the argument, it is a new angle and belongs in the bank, not in this file. Angle: "menopause wrinkly skin." Hooks: "Progesterone is what makes your skin saggy" and "During menopause your skin loses minerals."

Write 5, ship 1 to 3 per ad set. Each one gets its own row under `hooks` in the angle record, with its own `asset_ids` and `verdict`, because variations win and lose independently while the angle stays constant.

Hooks are written from customer language, not from a product brief. If the line does not exist somewhere in the VoC index in some form, you are writing marketing language about the avatar rather than the avatar's own language.

Load [`../direct-response-os/modules/laws.md`](../direct-response-os/modules/laws.md) first. Law 9 is enforced line by line here.

## Operating rules

1. **Every hook is written for one specific person.** Name who they are before writing the line. "Women 35 to 65" is not a person.
2. **Hooks must earn the next line.** Every hook creates a question only the next sentence can answer. A hook that resolves itself has nowhere to go.
3. **No generic openers.** No "Are you tired of," no "Did you know," no "Introducing," no "Imagine if." These are the hooks everyone writes.
4. **Match the awareness level.** An unaware hook names a problem without naming the product. A solution-aware hook leads with a failed solution. State the level for every hook.
5. **Variation means variation.** Five hooks should feel like five different conversations: different emotional entry points, different opening moves, different people being addressed. Five rewrites of one sentence is one hook.

## Step 1 — Load the angle and the language

Per Law 1, `brands/<brand>/` first, then:

- The angle record from `brands/<brand>/research/dr-os/angle-bank.md`. Work from **one** record. If the user has not named one, take the highest-priority `fresh` record serving the starved awareness level from `awareness-map.md`, and say which you picked.
- `voc-index.md`, specifically the emotional language extraction and community dialect sections. These are the phrase bank.
- `_engine/swipe-library/hook-bank/` — the proven structural patterns by awareness level: `HOOK-BANK.md` (written long-form/native copy hooks + the governing law of hooks) and `VIDEO-HOOK-BANK.md` (video ad skeletons from ~90 longest-running ads across 6 scaling health-DR brands). Pick the SKELETON from the bank, write the WORDS from VoC. Run the video bank's house-law filter on every line.
- The product truth. For Velantra products this means the matching product-scale skill (`velantra-weekender`, `velantra-straw-tote`, `velantra-meridian`, `velantra-boat-tote`) so no hook implies a feature the product does not have.
- `brands/<brand>/ops/` house laws.

If the angle record has `swap_test: fail` or `brand_law_check: flagged:*`, say so in one line and either rebuild the angle on our own facts first or write to the stated constraint. Do not quietly write hooks for a failed record.

## Step 2 — Write five hooks

For each:

**HOOK [N]**
- **The hook**, exactly as it appears on screen or as the first line of a script
- **Who this is for**: the specific person, one sentence
- **Awareness level**: unaware / problem aware / solution aware / product aware
- **Hook type**: problem naming / failed solution / curiosity / pattern interrupt / transformation / social proof
- **Why it works**: one sentence on the mechanism
- **Source language**: the VoC quote it was built from, with its path. If a hook has no source quote, say so explicitly rather than hiding it.
- **Format recommendation**: UGC / static / street interview / podcast / founder

## Step 2b — Craft standards (EVOLVE layer, added 2026-08-18)

Absorbed from the EVOLVE video and static prompts ([`07-video-ad-script-prompt.md`](../../../_engine/frameworks/fundamentals/evolve-prompt-vault/07-video-ad-script-prompt.md), [`06-static-image-ads-prompt.md`](../../../_engine/frameworks/fundamentals/evolve-prompt-vault/06-static-image-ads-prompt.md)). Apply to every line before the gates:

- **~5-word hooks.** Target 3-7 words, maximum two lines on a phone. A hook that explains is a wall of text; its job is to stop the scroll and open a loop, not to teach. Statics headline cap: 6-8 words.
- **Direct before indirect.** The hook states the angle's outcome plainly ("14+ Hours. No Swelling"). Indirect/clever is an advanced move — earn it.
- **The Four U's, in priority order:** Unique (must be present — it's the scroll-stopper), Useful (a desire they actually have), Urgent, Ultra-specific (real numbers, names, timelines — specific claims are believed, vague ones ignored). Hit at least 3.
- **The Big 4 emotions:** NEW/ONLY, EASY/ANYBODY, SAFE/PREDICTABLE, BIG/FAST. Hit 2-3 powerfully; forcing all four reads like a checklist.
- **Slippery slope.** The hook ends with intrigue, never resolution — each line makes the next one necessary. "Regular sheets trap heat. But that's not the real problem..."
- **Categorization = death.** Never say what the product is "like," never name a competitor category ("the best massage gun"). Position by what it uniquely DOES ("the only bag that..."). This compounds our swap test: a categorized line fails swap by definition.
- **Two hook frameworks** when stuck: "biggest thing happening now" (scale/urgency) or "quirky" (one counter-intuitive twist).

House laws still outrank all of it: numbers must be real (no fabricated citations, ever), lines come from VoC not invention, and the AI-tell blacklist applies to EVOLVE-styled lines too.

## Step 3 — Run the gates on every line

No hook leaves this skill without passing all five.

| Gate | Kill condition |
|---|---|
| **AI tells** | Em dash. "That's not X, it's Y." Parallel repetition stack. Rhetorical opener. Tidy tricolon. Personified object. |
| **Swap test** | A competitor's product drops in and the line still reads perfectly. Rewrite onto our own physical facts. |
| **Six-month test** | The line dies when the season or moment changes. A seasonal wrapper survives only if deleting the season leaves the reason to believe intact. |
| **Product truth** | The line implies a spec, material, dimension, or capability not in the product files. Fix or cut. Law 2. |
| **Brand law** | Competitor mention outside the roundup carve-out, a villain or manufactured problem, a product-first opening on top of funnel, a creator speaking as the brand. |

Fix violations before presenting. Do not present a line with a note asking whether it is acceptable.

## Step 4 — Recommend and write

**RECOMMENDED HOOK TO TEST FIRST**, with reasoning based on the size of the available audience at that awareness level, not on which line reads best. The prettiest hook aimed at an exhausted level loses to a plainer one aimed at a fresh one.

Write `brands/<brand>/research/dr-os/hooks/<angle-id>-<slug>.md` (`artifact: hooks`), then **append the shipped hooks to that angle's `hooks` list** in `angle-bank.md` with `status: fresh` and empty `asset_ids`. A hook file that never lands back in the record leaves the bank showing an angle with no variations, which reads as untested when it is actually unrecorded.

Close with two lines: the recommended hook, and the next skill. Video goes to [`dr-ugc-brief`](../dr-ugc-brief/SKILL.md), long-form goes to [`ad-concept-builder`](../ad-concept-builder/SKILL.md), statics go to the `native-image-factory` skill.
