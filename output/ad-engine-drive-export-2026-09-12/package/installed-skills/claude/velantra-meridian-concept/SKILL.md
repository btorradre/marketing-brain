---
name: velantra-meridian-concept
description: Write a VIDEO AD CONCEPT + creative brief for the Velantra Meridian specifically. Trigger when the user says "video ad concept for the meridian", "write a meridian ad", "new video ad for the meridian", "concept for the meridian", or runs ad concepting/briefing for this product. Pre-loads the Meridian's references, colorways, the Velantra avatar, and market sophistication, then runs the ad-concept-builder intent flow tuned for a VIDEO ad and outputs a production-ready concept brief. Pair with the velantra-meridian product-scale skill for generation.
disable-model-invocation: false
---

## GOLDEN NUGGET DOCTRINE (MANDATORY — locked 2026-07-11)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded DEEP FRAME in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: *is this the topic, or is this the motive?* If it's the topic, dig one layer deeper (memory loss → becoming my parent; GLP-1 bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes.** The golden nugget LEADS — very top of the piece, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence BEFORE drafting. When analyzing a reference ad/funnel/swipe instead of writing, state the nugget it's built on and whether it leads with it. If the research hasn't surfaced one, mine reviews/VOC/Reddit until it does — never default to a surface angle.

# Velantra Meridian — Video Ad Concept & Brief

Product-specialized entry point for concepting a **video ad** for the Velantra Meridian. Thin specialization layer over [ad-concept-builder](../ad-concept-builder/SKILL.md): pre-loads this product's references, colorways, avatar, and sophistication, then steers the 7-slot intent flow toward a **video** ad and hands off a creative brief.

> Generation counterpart: the [velantra-meridian](../velantra-meridian/SKILL.md) product-scale skill.

## When this runs
- "write a video ad concept for the meridian"
- "new meridian ad" · "concept for the meridian" · "meridian UGC idea"

## Product context — PRE-LOADED, do not re-ask

**Product:** Velantra Meridian (structured leather-look everyday handbag/tote)
**Category:** Structured professional carry — "morning meeting to weekend coast"
**Price band:** $50–$150 (Velantra accessible-luxury)
**Colorways:** black, brown, coffee brown, gray, white, green, burgundy, light blue, ultra light blue (40 reference images across 9+ colorways)

### Reference assets (base: `/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/meridian/`)
- `product-references/meridian/` — multi-angle colorway shots (`black 1–9`, `brown 1–5`, `coffee brown`, `gray`, `white`, `burgundy`, `light blue`, `ultra light blue`) for i2i
- `product-images/meridian/` — generated/edited product shots

> No ripped-UGC folder for this product yet — invent the beat structure from the avatar + sophistication, or borrow a beat skeleton from a sibling product (boat-tote `ugc/ripped ugc/`).

### Avatar — the "Velantra Woman" ("Caroline", 40–48)
Coastal-affluent professional, anti-logo, IYKYK. The Meridian is her **everyday workhorse** — the bag that transitions from a morning meeting to the weekend coast. She's "done chasing trends and tired of bags that break their promises." Full ICP: `brands/velantra/research/icp-branding/Ideal_Customer_Profile.md`.

### Market sophistication & awareness (slot pre-fill defaults)
- **Sophistication: 4–5** — the "structured everyday luxury tote" claim is saturated. Differentiator = **durability proof** (2-yr warranty, brass hardware, reinforced stitching) + the no-logo quiet-luxury frame.
- **Awareness: problem-aware → solution-aware** for cold; **product-aware** for retargeting.
- **Angle / wound:** "I keep buying everyday bags that look the part for a month then fall apart / look cheap" — durability betrayal. Vindication: the one bag that works as hard as she does and still looks expensive a year in.

## Flow
1. **Load context above** — never ask for product, colorways, avatar, or references.
2. **Confirm format.** Default: **TikTok UGC** (or static→animated demo). Confirm with one question.
3. **Mine sibling UGC** if needed (boat-tote `ugc/ripped ugc/`) for a proven beat skeleton.
4. **Run the ad-concept-builder 7-slot flow, FRAMED FOR VIDEO** — defaults below, via AskUserQuestion.
5. **Output the Video Ad Concept Brief** (artifact below).
6. **Offer to produce** via [velantra-meridian](../velantra-meridian/SKILL.md) → video-scene-replicator / ugc-forge / higgsfield-replicator.

### Product-tuned slot defaults (meridian)
| Slot | Default | Why |
|------|---------|-----|
| Concept/vehicle | "The one bag that lasted" — everyday carry over a season | Matches workhorse positioning |
| Lead | Problem-callout ("Why does every $300 work bag fall apart in a month?") | Durability betrayal is the live wound |
| Mechanism intro | Construction proof — brass hardware, reinforced stitching, 2-yr warranty | Earns "quality you can feel" |
| Solution intro | Whisper→Discovery | Avoids hard-sell |
| Proof | "1 year later" durability demo + peer compliment | Her trust triggers |
| CTA | Soft → PDP | Quiet-luxury tone |
| Length | 20–40s UGC | Channel-appropriate |

## Video Ad Concept Brief (the artifact)
```
# VIDEO AD CONCEPT — Velantra Meridian
Format/destination:  <TikTok UGC | VSL | static→animated>
Avatar:              Velantra Woman (everyday professional workhorse buyer)
Awareness/Sophist.:  <…> / <4–5>
Angle (wound):       <durability betrayal>

HOOK (0–3s):         "<exact line>"
BEATS:
  1. <shot — visual + VO/on-screen text + role>
  2. …
PROOF BEAT:          <durability demo / compliment beat>
CTA:                 "<exact words>" → <destination>

PRODUCTION NOTES
  Colorway(s):       <hero colorway>
  Product refs (internal): product-references/meridian/<files> (i2i)
  Editor-facing refs:      live product links + creator t2i prompt — see "Editor-facing brief rules"
  Voice:             <ElevenLabs clone or UGC creator>
  Build path:        velantra-meridian → <video-scene-replicator | ugc-forge | higgsfield-replicator>
```

## Editor-facing brief rules (HARD — no local file paths, ever)

Any brief sent to the editor (e.g. published to the Velantra Notion Briefs page) must be fully self-contained — the editor has NO access to local files. Never put a `/Users/...` path, vault directory, or local filename in an editor-facing brief.

**Brevity (2026-07-28):** briefs are short — 5-6 pages max. The "how to generate" process (Pinterest→Nano Banana Pro avatars, GPT Image 2→Omni b-roll) lives ONCE in `_engine/sops/Velantra-Avatar-BRoll-Production-SOP.md`, paired with a Loom walkthrough — never re-explain that process inside a brief. A brief carries only: the product-truth block, the script, the timeline, the prompts, and brief-specific guardrails/QA. Cut strategic exposition (why the angle works, why this format) down to one or two lines — the editor executes, they don't need the reasoning.

1. **Product refs → live product links.** Point the editor at the live velantrafashion.com product page — deep-link the exact colorway variant (`?variant=<id>`, pull the ID from the Shopify Admin API at brief time) and name the gallery shot to save from the page.
2. **Creator refs → Pinterest + Nano Banana Pro.** Full process, base prompt template, and the "never clone the real face" rule: `_engine/sops/Velantra-Avatar-BRoll-Production-SOP.md` §1. The brief itself only needs the Pinterest search link + identity block per creator — never restate the process in the brief.
3. **Reference ads → public links** (Facebook Ad Library `https://www.facebook.com/ads/library/?id=<ad-id>`, TrendTrack share link, or platform URL) — never a downloaded `.mp4` path. Internal clips with no public URL get an inline beat-by-beat description instead.
4. **No companion files** — everything the editor needs (segment prompts, scripts, tables) lives inline in the Notion page.
5. **B-roll (generated scenes) → GPT Image 2 (still) + Google Omni (motion).** Full process, QA gate, the photoreal/anti-CGI prompt blocks, and the three-variants-then-pick rule (all apply to macro/product-detail shots too): `_engine/sops/Velantra-Avatar-BRoll-Production-SOP.md` §2–3b. **The 3D-model look is BANNED — if a frame looks like a 3D model it gets regenerated, no exceptions (Brooks, 2026-07-29). Never ship the first roll: generate 3 variants of every scene and pick the one that is not artifacted.** The brief itself only needs the keyframe/motion prompts per scene — never restate the process in the brief.

Local vault refs stay valid for INTERNAL generation runs (i2i, replicators) — this rule governs what the editor sees. Full worked example: [velantra-straw-birkin-concept](../velantra-straw-birkin-concept/SKILL.md).

## Related
- **Generation:** [velantra-meridian](../velantra-meridian/SKILL.md)
- **Copy/concept engine:** [ad-concept-builder](../ad-concept-builder/SKILL.md) · lfc-writer
- **Video build:** video-scene-replicator · ugc-forge · higgsfield-replicator · aiugc-infinite
- **Research:** `brands/velantra/research/icp-branding/`
