---
name: dr-ugc-brief
description: Turn one angle plus its hook into a complete UGC creator brief a creator who has never heard of the brand can shoot without a single follow-up question. Part of the Direct Response OS. Use when the user says "write a creator brief", "brief this for UGC", "brief for the creator", "what do we send the creator", "turn this angle into a shoot brief", or has an approved angle and hook ready for production. Enforces a demo beat on every claim, keeps the creator speaking as a customer rather than as the brand, contains no file paths or internal jargon, and writes brands/<brand>/research/dr-os/briefs/<date>-<angle-id>-<format>.md.
user_invocable: true
---

## GOLDEN NUGGET DOCTRINE (MANDATORY — locked 2026-07-11)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded DEEP FRAME in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: *is this the topic, or is this the motive?* If it's the topic, dig one layer deeper (memory loss → becoming my parent; GLP-1 bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes.** The golden nugget LEADS — very top of the piece, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence BEFORE drafting. When analyzing a reference ad/funnel/swipe instead of writing, state the nugget it's built on and whether it leads with it. If the research hasn't surfaced one, mine reviews/VOC/Reddit until it does — never default to a surface angle.

# DR OS — UGC Creator Brief

A bad brief produces bad footage no matter how good the creator is. These briefs are not shot lists. They are creative strategies written in plain language, and every instruction in them exists to protect the angle from being diluted in production.

Load [`../direct-response-os/modules/laws.md`](../direct-response-os/modules/laws.md) first. Laws 7 and 8 are the ones this skill lives or dies on.

## Operating rules

1. **The brief serves the angle, not the creator.** Every instruction exists because without it the angle degrades on set.
2. **Specificity prevents mistakes.** Write every instruction as if you cannot be reached to clarify it, because you cannot.
3. **The hook is non-negotiable.** The creator has freedom in the body. The opening three seconds are delivered as written. Say this explicitly in the brief.
4. **Tone comes from awareness level.** A solution-aware customer is sceptical. A problem-aware customer is frustrated. The creator's energy has to match, so explain which one they are playing.
5. **Show, do not tell.** Instead of "seem relaxed," write "film in your kitchen like you're telling a friend something you just figured out."
6. **No file paths, no internal jargon.** No angle IDs, no skill names, no vault paths, no awareness-level vocabulary in the creator-facing document. Those live in the internal header only.

## Step 1 — Load everything the brief depends on

Per Law 1, `brands/<brand>/` first, then:

- The angle record from `angle-bank.md` and the hook file from `hooks/`. If either is missing, run [`dr-hook-lab`](../dr-hook-lab/SKILL.md) first rather than improvising a hook here.
- **Product truth, mandatory.** For Velantra, load the product-scale skill for that exact product (`velantra-weekender`, `velantra-straw-tote`, `velantra-meridian`, `velantra-boat-tote`) and carry its locked identity and mechanism blocks. The flap-mechanism block is not optional on the Straw Tote or Weekender.
- Known dimension gaps. The Camille Boat Tote, Margot Leather Tote, and Sofia Woven Tote have no published dimensions, so no brief may state a size for those three.
- `voc-index.md` for the phrases that must appear verbatim.

## Step 2 — Write the brief

Internal header first (never sent to the creator): angle ID, awareness level, persona, golden nugget, source hook file.

Then the creator-facing document:

### OVERVIEW (3 sentences maximum)
What this ad is trying to do and who it speaks to.

### THE HOOK (non-negotiable)
- The exact opening line, word for word
- Visual direction for the first 2 to 3 seconds: setting, framing, body language
- What the creator must NOT do in the opening

On top of funnel, the opening does not lead on the product. If the first frame is a product beauty shot, the brief is wrong.

### THE BODY
- Key points in order, written as talking points rather than a full script
- The emotional journey: what the creator's energy is at each stage
- **Which customer phrases must appear verbatim**
- **Demo beats.** Every claim gets a paired on-screen demonstration. Write them as a two-column list so nothing ships as a bare assertion:

  | Claim she makes | What the camera shows while she says it |
  |---|---|
  | it holds a 16 inch laptop | the laptop sliding in, lid closing over it |
  | the leather softens instead of scuffing | thumb pressed into the grain, releasing |

- What objections to address, and how

### THE CLOSE
- How the ad ends
- Specific CTA language

### PRODUCTION NOTES
- Recommended setting, and why that setting serves this angle
- Wardrobe and styling direction
- What to avoid
- One creator throughout, same person in every shot. If this is an AI-generated build, the creator is locked as the reference element in every prompt.

### WHAT SUCCESS LOOKS LIKE
One paragraph describing the finished ad if the brief was executed correctly. This is what the editor and the reviewer both grade against.

## Step 3 — Run the gates

| Gate | Kill condition |
|---|---|
| **Demo beat** | Any claim in the body with no paired visual. Law 7. |
| **Creator voice** | Any "our," "we," or "my brand." The creator says "they're," "their," "this brand." Law 8. |
| **Product truth** | Any spec, dimension, material, colourway, or capability not in the product files. Law 2. |
| **AI tells** | Em dash, "not X it's Y," parallel stacks, in any line the creator actually speaks. Law 9. |
| **Swap test** | The script would read identically for a competitor's product. Law 5. |
| **Six-month test** | The concept dies with the season or moment. Law 4. |
| **Clean brief** | Any file path, angle ID, skill name, or internal vocabulary in the creator-facing section. |

## Step 4 — Write and hand off

Write `brands/<brand>/research/dr-os/briefs/<YYYY-MM-DD>-<angle-id>-<format>.md` (`artifact: brief`).

Push the concept to the tracker before production starts, per the creative velocity law, and write the returned `asset_id` into the angle record's `tested_assets`:

```bash
python3 "_engine/creative-tracker/push_concept.py" \
  --product "<product>" --concept "<concept name>" --angle "<angle id + name>" \
  --thesis "<one sentence>" --format video --type net-new --source dr-os
```

Close with the two-line self-audit confirming the six-month test and the swap test, then name the production skill: `velantra-ugc` for Velantra creator video, `ugc-forge` or `omni-ugc` for generic UGC, `aiugc-longform` for continuous-VO long form, `seedance-directors-cut` when replicating a reference.
