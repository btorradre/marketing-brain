---
name: velantra-meridian-concept
description: Writes a video ad concept and creative brief for the Velantra Meridian, a structured leather-look everyday handbag/tote positioned as durable professional carry. Use when the user asks for a video ad concept for the Meridian, or any ad concepting/briefing request for this specific product. Pair with the velantra-meridian product-scale skill for the actual visual/colorway details when it's time to generate imagery.
---

# Velantra Meridian — Video Ad Concept & Brief

Use this when writing a video ad concept and creative brief for the Velantra Meridian — a structured leather-look everyday handbag/tote positioned as durable professional carry.

## Golden Nugget Doctrine (apply to every piece of creative you write)

Before writing any hook, angle, script, concept, or audit verdict, name the **golden nugget**: the single most emotionally loaded deep frame in the research — the real motive that makes buyers act, never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test:** for every candidate angle ask "is this the topic, or is this the motive?" If it's the topic, dig one layer deeper (memory loss → becoming my parent; GLP-1 bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes:** the golden nugget leads — right at the top, as the hook. Never buried in the body.
- **Deliverable:** state the golden nugget in one explicit sentence before drafting. When analyzing a reference ad/funnel instead of writing fresh copy, state the nugget it's built on and whether it leads with it. If the research hasn't surfaced one, keep digging through reviews/voice-of-customer/forums until it does — never default to a surface angle.

## Product context (use this, don't re-derive it)

- **Product:** Velantra Meridian — structured leather-look everyday handbag/tote.
- **Category:** Structured professional carry — "morning meeting to weekend coast."
- **Price band:** $50–$150 (Velantra accessible-luxury).
- **Colorways:** black, brown, coffee brown, gray, white, green, burgundy, light blue, ultra light blue (40 reference images across these 9+ colorways).
- **Reference material:** multi-angle colorway product shots used as image-to-image seeds, plus generated/edited product shots from prior campaigns. There is no dedicated ripped-UGC library for this product yet — either invent the beat structure from the avatar and sophistication below, or borrow a beat skeleton from a sibling product's UGC (e.g. the Boat Tote line).

### Avatar — the "Velantra Woman" ("Caroline," 40–48)

Coastal-affluent professional, anti-logo, in-the-know. The Meridian is her everyday workhorse — the bag that transitions from a morning meeting to the weekend coast. She's "done chasing trends and tired of bags that break their promises."

### Market sophistication & awareness

- **Sophistication: 4–5** — the "structured everyday luxury tote" claim is saturated. Differentiator = durability proof (multi-year warranty, brass hardware, reinforced stitching) plus the no-logo quiet-luxury frame.
- **Awareness:** problem-aware moving toward solution-aware for cold audiences; product-aware for retargeting.
- **Angle / wound:** "I keep buying everyday bags that look the part for a month then fall apart or look cheap" — durability betrayal. Vindication: the one bag that works as hard as she does and still looks expensive a year in.

## How to use this

1. Start from the product context above — never ask the user to re-supply product, colorways, avatar, or references.
2. Confirm the format with one question. Default: TikTok-style UGC, or a static-to-animated demo.
3. If a proven beat skeleton is needed, mine a sibling product's UGC library for structure.
4. Fill out the seven-slot concept flow below, framed for video.
5. Produce the Video Ad Concept Brief using the template below.
6. Once the concept is approved, hand it off to production using the Meridian product-scale reference material (the companion `velantra-meridian` skill) for accurate product generation.

### Slot defaults tuned for this product

| Slot | Default | Why |
|------|---------|-----|
| Concept/vehicle | "The one bag that lasted" — everyday carry over a season | Matches workhorse positioning |
| Lead | Problem-callout ("Why does every $300 work bag fall apart in a month?") | Durability betrayal is the live wound |
| Mechanism intro | Construction proof — brass hardware, reinforced stitching, multi-year warranty | Earns "quality you can feel" |
| Solution intro | Whisper → Discovery | Avoids hard-sell |
| Proof | "1 year later" durability demo + peer compliment | Her trust triggers |
| CTA | Soft, point to product page | Quiet-luxury tone |
| Length | 20–40s UGC | Channel-appropriate |

## Templates & examples

### Video Ad Concept Brief

```
# VIDEO AD CONCEPT — Velantra Meridian
Format/destination:  <TikTok UGC | longer-form | static→animated>
Avatar:              Velantra Woman (everyday professional workhorse buyer)
Awareness/Sophist.:  <…> / <4–5>
Angle (wound):       <durability betrayal>

HOOK (0–3s):         "<exact line>"
BEATS:
  1. <shot — visual + voiceover/on-screen text + role>
  2. …
PROOF BEAT:          <durability demo / compliment beat>
CTA:                 "<exact words>" → <destination>

PRODUCTION NOTES
  Colorway(s):       <hero colorway>
  Product references: multi-angle colorway images used as generation seeds
  Editor-facing refs: live product links + creator description — see rules below
  Voice:              <cloned voice or UGC creator style>
```

## Rules & standards

### Editor-facing brief rules (hard rule — never include internal file paths)

Any brief that reaches an editor or gets published for production must be fully self-contained. The editor has no access to your internal files, so never put an internal file path, folder name, or local filename in an editor-facing brief.

**Brevity:** briefs should be short — roughly 5–6 pages max. Don't re-explain your internal production process inside every brief; document that once, separately, and link to it. A brief itself should only carry: the product-truth block, the script, the timeline, the generation prompts, and brief-specific guardrails/QA. Cut strategic exposition down to one or two lines — the editor executes, they don't need the reasoning.

1. **Product references → live product page links.** Point the editor at the live product page for the exact colorway/variant, and name the specific gallery photo to reference.
2. **Creator references → a real reference photo plus a written identity block.** Source a candidate creator photo, and write a verbatim description (age range, hair, build, wardrobe, energy) rather than cloning a real identifiable person's face.
3. **Reference ads → public links only** (an ad library URL or a public platform URL), never a downloaded local video file. If an internal clip has no public URL, describe it beat-by-beat instead of pointing to a path.
4. **No companion files** — everything the editor needs (segment prompts, scripts, tables) should live inline in the brief document itself.
5. **Generated B-roll:** use a still-image generation model for keyframes and a motion/video generation model to animate them. The 3D-model/CGI look is banned — if a frame looks like a computer-rendered 3D model, it must be regenerated, no exceptions. Never ship the first attempt: generate three variants of every scene and pick the one that reads as real photography, not a render.

Internal file paths are fine to use for your own internal generation work — this rule only governs what you hand to an editor or external collaborator.
