# Long-Form Copy Export

Everything tied to long-form direct-response copy, packaged for a copywriting agent. Two parts: the **skills** (operational rules the agent executes) and the **conversation digest** (context for how the system was built and used).

## How the skills fit together

The writing pipeline runs in this order:

```
avatar-research  →  desire-angle-concept  →  copy-strategy  →  hook-generation  →  long-form-copy
   (who + VOC)        (angle/concept matrix)    (the brief)      (first 1–5 lines)   (the full ad)
                                                                       │
                                              hook-congruence ─────────┘  (hook→lead→mechanism chain)
                                              ai-copy-blacklist ──────────►  (applied to ALL copy, always)
                                              swipe-adaptation ───────────►  (decompose/adapt references)
                                              ad-assessment ──────────────►  (score/audit finished copy)
```

## Files

**Core writing system (the three you named + the two mandatory layers they run with):**
- `skills/long-form-copy.md` — the writing engine. Executes a brief; does not decide one.
- `skills/copy-strategy.md` — produces the brief (awareness, sophistication, concept, belief set, proportion, discovery mode, engine, push intensity). Run FIRST.
- `skills/hook-generation.md` — the first 1–5 lines. Hook mechanics, taxonomy, awareness matching, templating.
- `skills/hook-congruence.md` — the congruence layer: how hooks connect to leads, leads to mechanism. Used alongside hook-generation.
- `skills/ai-copy-blacklist.md` — mandatory negative-constraint layer. Strips AI-authorship patterns. Applied during the self-audit of every copy skill.

**Adjacent skills that feed / support long-form copy:**
- `skills/desire-angle-concept.md` — the desire→angle→concept matrix that feeds hooks and copy.
- `skills/avatar-research.md` — upstream consumer intelligence / VOC that feeds everything.
- `skills/swipe-adaptation.md` — decompose external copy and adapt it for a new brand/avatar.
- `skills/ad-assessment.md` — score and audit finished long-form copy.

**Context:**
- `CONVERSATION-DIGEST.md` — the chats where this system was built and used, with links and key decisions.

## Note on dependencies

The skills reference a `concept-databank` (the twelve-vehicle library) that copy-strategy and long-form-copy pull from by name. It wasn't part of this request, so it's not bundled here — export it separately if the agent needs the concept library.

## Not included (different deliverables — ask if you want them)

Advertorial, listicle, video-ad-scripts, sora-scripting, the page-builders, native-image-factory, ad-watcher, and the funnel-analysis/congruence/advisory skills. These are separate funnel pieces or production/diagnostic tools rather than long-form copy itself.
