---
name: creative-brief
description: Writes the creative strategist's brief for a video ad concept — the simple five-part format (header block, Concept WHY/WHAT/HOW/Runtime, Ad Structure as swappable Hook+Bridge pairs into a Shared Body and CTA, Editing Notes, and a walled-off MEDIA BUYER ONLY ad-copy block) — and publishes it to Notion. Trigger on "creative brief", "brief this concept", "write the brief for <concept>", "turn this reference into a brief", "adapt this ad for <brand>", "give my editor a brief", or any moment a concept has been agreed and needs to reach an editor and a media buyer. Also use to reformat an older brief into this format.
---

# /creative-brief — the strategist's brief

One page an editor can execute and a media buyer can launch from. Five parts, nothing else.

**Read `reference/EXEMPLAR-NOVEXA-DCT-402.md` before writing anything.** It is the gold
standard, transcribed from the source. `reference/BRIEF-FORMAT.md` is the annotated spec;
`reference/TEMPLATE-brief.md` is the blank.

## The two ideas the format is built on

1. **One brief, three ads.** Hooks and Bridges are matched swappable pairs on the same
   timecode. Pick Hook 2, you get Bridge 2, then the shared body and CTA run identically.
   Three creatives out of one edit. Never write a hook that only works with one bridge.
2. **Every beat is two lines.** `Spoken:` and `Visual:`. If a thought doesn't fit in those
   two lines it is strategy, and strategy lives in section 1 where the editor reads it once.

## Structure

```
# <BRAND>-VID-NNN | <Concept Name>

Sub-avatar / The One Angle / Format / Product / Landing Page / Inspiration

💡 1. Concept          WHY · WHAT · HOW · Runtime
🎬 2. Ad Structure     Hook 1+Bridge 1 · Hook 2+Bridge 2 · Hook 3+Bridge 3
                       Shared Body (timecode-only sub-beats) · CTA
🎬 3. Editing Notes    hard constraints, bullets
⛔ MEDIA BUYER ONLY    Primary Text #1/#2 · Headline #1/#2
```

Full field-by-field rules in `reference/BRIEF-FORMAT.md`. Do not add sections. Do not rename them.

## Input contract

Required:
- **Concept** — either agreed in conversation, or a reference ad (URL/path) to adapt.
- **Brand + product** — load `brands/<brand>/` and the product-scale skill (velantra-weekender,
  velantra-straw-tote, motilli, …) **first**. Product truth and brand law beat everything below.
- **Landing page** — name, awareness tag, live URL.
- **Live offer + guarantee** — verify on the page. Never carry an offer forward from memory.

Ask for anything missing. Never guess a landing page, an offer, or a concept ID.

Optional: Facebook/persona page · runtime target (defaults to the reference minus its offer
block) · a focus the user wants weighted.

## Workflow

**1 — Load.** Brand folder, product skill, house laws from `MEMORY.md`. Read the exemplar.

**2 — If adapting a reference, watch it.** `/ad-watcher` or the `watch` skill for the beat
breakdown and verbatim transcript. Do the psychographic reasoning in a scratch file —
**it does not go in the brief.** What survives into the brief is one line of WHY and the
One Angle. Sophistication check: `reference/sophistication-mapping.md`. If the target avatar
is further along the awareness scale than the reference's, compress the discovery block and
open on the verdict.

**3 — Name the golden nugget in one sentence before you draft.** The motive, not the topic.
"Memory loss" is a topic; "I thought I was becoming my mother" is the motive. It becomes WHY,
and the hooks are written off it. If research hasn't surfaced one, mine VoC until it does.

**4 — Get the ID.**

```bash
python3 "/Users/brooksorradre2/Documents/marketing brain/.claude/skills/video-brief/publish_brief.py" --brand <Brand> --next-id
```

**5 — Write** to `brands/<brand>/creative/<CONCEPT-ID>/<CONCEPT-ID>-brief.md`.
Write the One Angle first, then the three hooks, then the body. Everything that doesn't
serve the One Angle gets cut.

**6 — Self-audit** against the checklist below. Fix before showing Brooks anything.

**7 — Publish and push.**

```bash
python3 ".../video-brief/publish_brief.py" --brand <Brand> --file <path>
```

Then push the storyboard to Cutroom the same turn — keyframes on the board, Brooks approves
there, then render. Never wait to be asked.

## Hard rules

- **Runtime is arithmetic, not a wish.** Natural delivery is ~190 wpm, so
  `runtime = words ÷ 190 × 60`. Count the spoken words and print the math. Targets: short
  mechanism ad 270-300 words (~1:35), authority VSL 500-520 words (~2:40). Over 700 words needs
  a written reason; "the reference was long" is not one.
- **Skepticism sets the SHAPE, never the length.** A cold market or an unfamiliar ingredient
  means MORE objections handled inside the SAME short runtime — a criterion line before any
  ingredient is named, and one designated killer per failed solution. Full model in
  `dr-video-ads` → LENGTH, DENSITY & SKEPTICISM.
- **An angle is the PROBLEM.** The One Angle names what she should notice or do. The claim
  is the hook, never the angle.
- **The Visual line is concrete nouns.** What is on screen. Never "establish the mood."
- **On-screen text goes in `backticks`, verbatim.** The editor copies it character for
  character. Never paraphrase a disclosure or a compliance super.
- **`Use:` before `Make:`.** Real footage folder first, generation only for what's missing.
  Folder names only — **no local file paths**, the editor is external.
- **No fabricated citations.** A study on screen is a real paper with a real finding, or it
  does not exist. Same for N, %, and any doctor.
- **Real trade dress** where brand law calls for it; generic-and-unreadable where it doesn't.
  The brief says which, explicitly, in Editing Notes.
- **Product on screen** wherever the concept allows. Name the reveal timecode in HOW *and*
  in the Visual line *and* in Editing Notes.
- **Verify the offer live.** Every brief's last Editing Note is the launch-day re-check.
- **No AI-tells.** No em dashes, no "it's not X, it's Y", no tricolons in spoken lines.
- Brand-specific script law wins over this format's defaults — e.g. Velantra scripts follow
  `velantra-ad-script` (verdict in the hook, "This is the [Name] from Velantra" by 0:06).

## Self-audit before showing Brooks

1. Every Hook works with every Bridge on its number, and all three pairs hand off cleanly to
   the same Shared Body first line.
2. Every beat has exactly `Spoken:` and `Visual:` — no third line, no missing one.
3. Timecodes run in order and the totals match the Runtime line.
4. The product-reveal timecode is identical in HOW, in the Visual line, and in Editing Notes.
5. Every burned super is in backticks and reads exactly as it should appear.
6. No local file paths. No invented studies. Offer and guarantee match the live page today.
7. Editing Notes are all checkable against a timeline. Anything unfalsifiable moves to WHAT.
8. Two Primary Texts, two Headlines, each ending in the destination URL.
9. The whole brief fits in about two screens of scrolling. Longer means strategy leaked in.
10. Print the spoken word count and the arithmetic runtime. Over target = cut before showing Brooks.
11. Every idea appears exactly once. A repeated idea is a cut, not a rewrite.

## When NOT to use this skill

- **Analysis only, no editor handoff** → `/ad-watcher`, stop after the breakdown.
- **Static / native image ads** → `ad-replicator` or `native-image-factory`.
- **Landing page or advertorial copy** → `advertorial`, `shopify-listicle-builder`.
- **Actual asset generation** → hand the finished brief to `video-scene-replicator`,
  `seedance-directors-cut`, or `omni-ugc`.
- **The long-form MOT-VID-009 house brief** (production-methods preamble, named prompt
  blocks, full visual schedule, QC pass) → `video-brief`. That format is for a concept the
  external editor builds from scratch. This one is for a strategist handing an editor a
  script with pictures. Ask Brooks which lane a concept is in when it isn't obvious.
