# DR Hook Lab

Writes five genuinely different hook variations for one angle, each aimed at one specific person at one awareness level, in the customer's own recorded language. Use when someone says "write hooks," "give me hook variations," "5 hooks for this angle," "new opening lines," "the hook isn't landing," "rewrite the first 3 seconds," or picks an angle to brief.

A hook is not a headline. It is a decision made in under two seconds. The job is not to make it sound good — it is to make the right person stop because this was obviously made for them.

**Where hooks sit.** One avatar is a campaign, one angle is an ad set, and hooks are the ad variations inside that one ad set. They all argue about the same problem and differ in how they open it. If a candidate line changes the problem rather than the argument, it's a new angle, not a hook. Angle: "menopause wrinkly skin." Hooks: "Progesterone is what makes your skin saggy" and "During menopause your skin loses minerals."

Write 5, ship 1 to 3 per ad set. Each one gets tracked separately with its own performance and verdict, because variations win and lose independently while the angle stays constant.

Hooks are written from customer language, not from a product brief. If the line doesn't exist somewhere in the voice-of-customer research in some form, it's marketing language about the customer rather than the customer's own language.

## Golden Nugget Doctrine

Before writing, name the **golden nugget**: the single most emotionally loaded deep frame in the research — the real motive that makes buyers act — never the surface theme. Topic ≠ motive: "memory loss" is a topic; "I thought I was getting dementia just like my mum did, until I discovered this" is the motive. State it in one sentence before drafting. If the research hasn't surfaced one, keep mining until it does.

## Operating rules

1. **Every hook is written for one specific person.** Name who they are before writing the line. "Women 35 to 65" is not a person.
2. **Hooks must earn the next line.** Every hook creates a question only the next sentence can answer. A hook that resolves itself has nowhere to go.
3. **No generic openers.** No "Are you tired of," no "Did you know," no "Introducing," no "Imagine if." Everyone writes these.
4. **Match the awareness level.** An unaware hook names a problem without naming the product. A solution-aware hook leads with a failed solution. State the level for every hook.
5. **Variation means variation.** Five hooks should feel like five different conversations: different emotional entry points, different opening moves, different people being addressed. Five rewrites of one sentence is one hook.

## How to use this

1. **Load the angle and the language.** Read the brand's existing research first, then find the specific angle record being hooked (if none is specified, pick the highest-priority untested angle serving the currently starved awareness level, and say which one was picked). Read the voice-of-customer research for the emotional language and community-dialect sections — this is the phrase bank. Look for proven structural hook patterns by awareness level from any swipe file or hook bank the brand keeps; pick the *skeleton* from proven patterns, write the *words* from customer research. Also load product-truth documentation so no hook implies a feature the product doesn't have, and house voice/brand rules.

   If the angle has already failed the swap test, or is flagged against a brand law, say so in one line and either rebuild the angle on the brand's own facts first or write to the stated constraint — never quietly write hooks for a failed record.

2. **Write five hooks.** For each:
   - **The hook**, exactly as it appears on screen or as the first line of a script
   - **Who this is for**: the specific person, one sentence
   - **Awareness level**: unaware / problem aware / solution aware / product aware
   - **Hook type**: problem naming / failed solution / curiosity / pattern interrupt / transformation / social proof
   - **Why it works**: one sentence on the mechanism
   - **Source language**: the customer quote it was built from, with where it came from. If a hook has no source quote, say so explicitly rather than hiding it.
   - **Format recommendation**: UGC / static / street interview / podcast / founder-to-camera

3. **Apply craft standards to every line before the gates** (see below).

4. **Run the five gates on every line** (see below). Fix violations before presenting — never present a line with a note asking whether it's acceptable.

5. **Recommend one to test first.** Base this on the size of the available audience at that awareness level, not on which line reads best. The prettiest hook aimed at an exhausted level loses to a plainer one aimed at a fresh one.

6. **Write and hand off.** Save the finished hooks as a standalone document, and record them back against the source angle (status: untested, no assets yet) so the angle record shows it now has variations. A hook file that never lands back in the angle record leaves the angle looking untested when it's actually just unrecorded.

7. **Close with two lines**: the recommended hook, and the next step — for video, a creator brief; for long-form, a full copywriting pass; for statics, an image-ad prompt pass.

## Rules & standards

### Craft standards (apply to every line before the gates)

- **~5-word hooks.** Target 3-7 words, maximum two lines on a phone. A hook that explains is a wall of text; its job is to stop the scroll and open a loop, not to teach. Statics headline cap: 6-8 words.
- **Direct before indirect.** The hook states the angle's outcome plainly ("14+ Hours. No Swelling"). Indirect/clever is an advanced move — earn it.
- **The Four U's, in priority order:** Unique (must be present — it's the scroll-stopper), Useful (a desire they actually have), Urgent, Ultra-specific (real numbers, names, timelines — specific claims are believed, vague ones ignored). Hit at least 3.
- **The Big 4 emotions:** NEW/ONLY, EASY/ANYBODY, SAFE/PREDICTABLE, BIG/FAST. Hit 2-3 powerfully; forcing all four reads like a checklist.
- **Slippery slope.** The hook ends with intrigue, never resolution — each line makes the next one necessary. "Regular sheets trap heat. But that's not the real problem..."
- **Categorization = death.** Never say what the product is "like," never name a competitor category ("the best massage gun"). Position by what it uniquely DOES ("the only bag that..."). A categorized line fails the swap test by definition.
- **Two hook frameworks when stuck:** "biggest thing happening now" (scale/urgency) or "quirky" (one counter-intuitive twist).

House laws still outrank all of it: numbers must be real (no fabricated citations, ever), lines come from customer research not invention, and the voice-tell gate applies to every line.

### The five gates (every line must pass all five)

| Gate | Kill condition |
|---|---|
| **Voice tells** | Em dash. "That's not X, it's Y." Parallel repetition stack. Rhetorical opener. Tidy tricolon. Personified object. |
| **Swap test** | A competitor's product drops in and the line still reads perfectly. Rewrite onto the brand's own physical facts. |
| **Six-month test** | The line dies when the season or moment changes. A seasonal wrapper survives only if deleting the season leaves the reason to believe intact. |
| **Product truth** | The line implies a spec, material, dimension, or capability not actually true of the product. Fix or cut. |
| **Brand law** | Competitor mention outside an explicit-comparison format, a villain or manufactured problem, a product-first opening on top of funnel, a creator speaking as the brand. |

### Where hooks sit in the angle record

Every angle in this system is tracked with this structure:

```yaml
id: <BRAND-PREFIX>-A-<counter>
avatar: "Menopause Skin"            # the campaign this sits under
name: "Sagging skin"                # short internal label, NOT a hook
problem: >                          # the angle — the specific problem, in her words
  My skin started sagging and none of the creams I've tried touch it.
golden_nugget: >
  I look in the mirror and see my mother's face arriving ten years early.
persona: >                          # ONE person, a situation, a feeling — never a demographic
  A 52-year-old who stopped booking the window seat at lunch because of what the light does to her jawline.
awareness: problem                  # unaware | problem | solution | product | most
hooks:                              # the ad variations this angle spawns
  - text: "Progesterone is what makes your skin saggy"
    mechanism: progesterone decline
    status: fresh                   # fresh | active | fatigued
    verdict: ""                     # winner | flat | loser, after 30 days of spend
  - text: "During menopause your skin loses minerals"
    mechanism: mineral loss
    status: fresh
    verdict: ""
```

An angle is a problem, not a claim. "Menopause wrinkly skin" is the angle. "Progesterone is what makes your skin saggy" is a hook that argues about that angle — writing the hook into the angle field is the single most common error.

Naming convention for tracking hooks once shipped: `<AVATAR>_<ANGLE-ID>_<HOOK-N>_<FORMAT>`, e.g. `MENOSKIN_MOT-A-014_H2_UGC`.
