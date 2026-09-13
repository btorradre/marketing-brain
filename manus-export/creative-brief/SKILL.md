---
name: creative-brief
description: Writes the creative strategist's brief for a video ad concept — a compact five-part format (header block, Concept WHY/WHAT/HOW/Runtime, Ad Structure as swappable Hook+Bridge pairs into a Shared Body and CTA, Editing Notes, and a walled-off MEDIA BUYER ONLY ad-copy block) that an editor can execute from and a media buyer can launch from directly. Use whenever a video ad concept has been agreed on and needs to be turned into a brief that reaches both an editor and a media buyer — including adapting a reference ad into a new brief, or reformatting an older, messier brief into this tighter format.
---

# The Creative Strategist's Brief

One page an editor can execute and a media buyer can launch from. Five parts, nothing else.

## The two ideas the format is built on

1. **One brief, three ads.** The Hooks and Bridges in the structure below are matched, swappable pairs sharing the same timecodes. Pick Hook 2, and you use Bridge 2 — then the shared body and the CTA run identically regardless of which hook/bridge pair was picked. This turns one brief into three finished creative variants without three separate edits. Never write a hook that only works with one specific bridge.
2. **Every beat is exactly two lines.** A `Spoken:` line and a `Visual:` line. If an idea doesn't fit into those two lines, it's strategy — and strategy lives in the Concept section (read once), not repeated at every beat.

## Structure

```
# <Concept ID> | <Concept Name>

Header block: Sub-avatar / The One Angle / Format / Product / Landing Page / Inspiration

1. Concept          WHY · WHAT · HOW · Runtime
2. Ad Structure      Hook 1+Bridge 1 · Hook 2+Bridge 2 · Hook 3+Bridge 3
                      Shared Body (timecode-only sub-beats) · CTA
3. Editing Notes     hard constraints, bullets
MEDIA BUYER ONLY     Primary Text #1/#2 · Headline #1/#2
```

Do not add sections. Do not rename them. Everything that doesn't fit one of these five parts doesn't belong in the brief. The full field-by-field spec, a complete worked example, and a blank template to start from are in `references/` — read `references/exemplar-and-template.md` before writing your first brief in this format.

## Input contract — what's needed before writing anything

Required:
- **Concept** — either already agreed on in conversation, or a reference ad to adapt.
- **Brand and product** — load the brand's research/voice documentation and the product's verified visual/factual truth (dimensions, materials, colorways) *first*. Product truth and brand voice rules override everything else below.
- **Landing page** — its name, its awareness-stage tag, and its live URL.
- **The live offer and guarantee** — verify these on the actual current page. Never carry an offer or guarantee forward from memory or from an old brief.

Ask for anything missing rather than guessing. Never guess a landing page, an offer, or a concept name.

Optional: a specific persona/page the ad is running under · a target runtime (if not given, default to the reference ad's runtime minus its offer section) · a particular focus area the requester wants weighted more heavily.

## Workflow

**1 — Load context.** Read the brand's research/voice documentation, the product's verified truth, and any house voice/law documents. Study the worked example in `references/exemplar-and-template.md` before writing.

**2 — If adapting a reference ad, watch it properly first.** Get a full beat-by-beat breakdown and a verbatim transcript before writing anything — never brief a reference you haven't actually reviewed shot by shot. Do the deeper psychographic reasoning (why does this ad work, what's the underlying belief shift) in scratch notes — **none of that reasoning goes into the final brief.** What survives into the brief is one line of WHY, and the One Angle. Also check whether the target audience's awareness level differs from the reference ad's original audience — see `references/sophistication-mapping.md`, and compress the discovery/education portion of the ad accordingly if the new target audience is further along.

**3 — Name the golden nugget in one sentence before drafting anything.** The underlying motive, not the surface topic. "Memory loss" is a topic; "I thought I was becoming my mother" is the motive. This becomes the WHY, and every hook gets written from it. If existing research hasn't surfaced a real motive yet, keep mining voice-of-customer material until it does.

**4 — Assign a concept ID.** Use a consistent naming convention such as `<BRAND>-VID-NNN`, incrementing from whatever the last concept number was for this brand.

**5 — Write the brief.** Write the One Angle first, then the three hooks, then the shared body. Cut anything that doesn't serve the One Angle.

**6 — Self-audit** against the checklist below before showing it to anyone.

**7 — Deliver.** Hand the finished brief to whoever needs to build a storyboard or start production from it, along with any reference frames/screenshots that help ground the visual direction.

## Hard rules

- **Runtime is arithmetic, not a guess.** Natural spoken delivery runs at roughly 190 words per minute, so `runtime = words ÷ 190 × 60`. Count the actual spoken word total and show the math. Reasonable targets: a short mechanism-focused ad around 270-300 words (~1:35); an authority-style long-form ad around 500-520 words (~2:40). Anything over roughly 700 words needs a stated reason — "the reference ad was long" is not a sufficient reason on its own.
- **Skepticism changes the shape of the ad, never its length.** A cold audience or an unfamiliar product/ingredient means handling *more* objections within the *same* short runtime — a stated criterion line before naming any new ingredient/mechanism, and one clearly designated "killer" line addressing each previously-failed alternative solution the audience has likely already tried.
- **An angle is the problem, never the claim.** The One Angle names what the viewer should notice or do. The claim itself is the hook, never the angle.
- **The Visual line is always concrete nouns.** What is literally on screen. Never a vague mood description like "establish the mood."
- **On-screen text goes in backticks, written exactly as it should appear.** Whoever builds the video should be able to copy it character for character. Never paraphrase a disclosure, disclaimer, or compliance line.
- **Real footage before generated footage.** State clearly when real existing footage should be used (and roughly what/where from) before falling back to "generate this if nothing existing fits." Never reference a specific local file path in the brief — describe footage by content/folder name only, since whoever builds the video may not have access to the same file system.
- **No fabricated citations, ever.** A study referenced on screen must be a real paper with a real finding, or it doesn't appear at all. Same standard for any statistic, percentage, or named doctor/expert.
- **Real product/trade dress vs. generic-and-unreadable** — decide explicitly per brief whether competitor products shown on screen should be real recognizable products or deliberately generic and unreadable, based on brand rules, and state that decision explicitly in the Editing Notes.
- **Product on screen wherever the concept allows it.** State the product's first-appearance timecode in three places: in the HOW paragraph, in the relevant Visual line, and again in the Editing Notes.
- **Verify the offer live, every time.** The brief's final Editing Note should always be a reminder to re-check the live offer and guarantee on the destination page on the actual day of launch/export.
- **No AI-sounding copy.** No em dashes, no "it's not X, it's Y" constructions, no three-item parallel-structure lists in spoken lines.
- **Brand-specific script formulas take precedence over this format's defaults** wherever they conflict — e.g. a brand might require a specific opening structure (stating a verdict, then naming the brand by a specific timecode) that overrides the generic hook/bridge structure below.

## Self-audit checklist before presenting a brief

1. Every Hook works correctly with every Bridge at its matching number, and all three hook/bridge pairs hand off cleanly into the same first line of the Shared Body.
2. Every beat has exactly a `Spoken:` and a `Visual:` line — no third line, and neither one missing.
3. Timecodes run in order and the totals add up to match the stated Runtime.
4. The product-reveal timecode is identical across the HOW paragraph, the relevant Visual line, and the Editing Notes.
5. Every burned-in on-screen text element is in backticks and reads exactly as it should appear on screen.
6. No local file paths anywhere. No invented studies. The offer and guarantee match the live page as of today.
7. Every Editing Note is checkable against a timeline (a specific, falsifiable instruction). Anything vague or unfalsifiable moves up into the Concept section instead.
8. Exactly two Primary Texts and two Headlines are provided, each Primary Text ending with the destination URL.
9. The whole brief fits in roughly two screens of scrolling. If it's longer, strategy has leaked into sections where it doesn't belong.
10. Print the spoken word count and the arithmetic runtime calculation. If it's over target, cut before presenting.
11. Every idea appears exactly once. A repeated idea should be cut, not restated.

## When NOT to use this format

- **Analysis only, no handoff to an editor** — just do the ad breakdown/analysis and stop there; no brief needed.
- **Static or native image ads** — this format is for video; use a different process for static ad creative.
- **Landing page or long-form advertorial copy** — this format is for video ad briefs specifically, not page copy.
- **Actual asset generation** — this format produces the brief; a separate production step turns the brief into finished footage/renders.
- **A long-form, fully self-contained production brief** (one that includes a full production-methods preamble, named prompt blocks for every generation step, a complete visual asset schedule, and a formal QC pass) is a different, heavier format intended for an external editor building a concept entirely from scratch with no other context. The five-part format described here is for a strategist handing a *script with pictures* to an editor who already has full context. When it's unclear which is appropriate for a given concept, ask.

## Reference material

- `references/brief-format-spec.md` — the full annotated field-by-field specification: exactly what goes in every line of the header block, the Concept section, the Ad Structure beats, the Editing Notes, and the Media Buyer block.
- `references/sophistication-mapping.md` — how to reshape a hook when the target audience's awareness level differs from the reference ad's original audience.
- `references/exemplar-and-template.md` — a complete, real worked example of a finished brief in this format, plus a blank skeleton template to start a new brief from.
