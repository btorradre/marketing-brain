---
name: velantra-jelly-tote-concept
description: Write a VIDEO AD CONCEPT + creative brief for the Velantra Jelly Tote (jelly Birkin) specifically. Trigger when the user says "video ad concept for the jelly tote", "jelly birkin ad", "new video ad for the jelly bag", "concept for the jelly tote", or runs ad concepting/briefing for this product. Pre-loads the Jelly Tote's references, candy colorways, ripped UGC, the Velantra avatar, and category sophistication, then runs the ad-concept-builder intent flow tuned for a VIDEO ad and outputs a production-ready concept brief.
disable-model-invocation: false
---

## GOLDEN NUGGET DOCTRINE (MANDATORY — locked 2026-07-11)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded DEEP FRAME in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: *is this the topic, or is this the motive?* If it's the topic, dig one layer deeper (memory loss → becoming my parent; GLP-1 bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes.** The golden nugget LEADS — very top of the piece, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence BEFORE drafting. When analyzing a reference ad/funnel/swipe instead of writing, state the nugget it's built on and whether it leads with it. If the research hasn't surfaced one, mine reviews/VOC/Reddit until it does — never default to a surface angle.

# Velantra Jelly Tote — Video Ad Concept & Brief

Product-specialized entry point for concepting a **video ad** for the Velantra Jelly Tote (the translucent "jelly Birkin"). Thin specialization layer over [ad-concept-builder](../ad-concept-builder/SKILL.md): pre-loads this product's references, candy colorways, avatar, ripped UGC, and sophistication, then steers the 7-slot intent flow toward a **video** ad and hands off a creative brief.

## When this runs
- "write a video ad concept for the jelly tote / jelly birkin"
- "new jelly bag ad" · "concept for the jelly tote" · "jelly bag UGC idea"

## Product context — PRE-LOADED, do not re-ask

**Product:** Velantra Jelly Tote (translucent jelly/PVC Birkin-silhouette tote)
**Category:** Playful translucent summer/beach Birkin-silhouette tote — the fun, color-forward sibling of the line
**Price band:** $50–$150 (Velantra accessible-luxury)
**Colorways (candy):** limoncello, peach, baby-pink, baby-blue, tiffany, tangerine, mint, milk, blush, grape, brat-green, watermelon, lilac, aqua, acid

### Reference assets (base: `/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/jelly-tote/`)
- `product-references/jelly tote/` — candy colorway flats (`limoncello.png`, `peach.png`, `tiffany.png`, etc.) for i2i
- `ugc-ripped/jelly firkin ripped/` — **9 ripped UGC clips** → mine for hooks/beats/pacing before writing

### Avatar — note the skew
Core brand avatar is the "Velantra Woman" (Caroline, 40–48, anti-logo, IYKYK — full ICP `brands/velantra/research/icp-branding/Ideal_Customer_Profile.md`). BUT the **jelly tote skews younger / more playful / beach-pool-festival** — color-forward, trend-aware, Gen-Z-to-younger-millennial buyer, lower price-anxiety, higher impulse. Treat this product's avatar as a younger, more expressive cut of the brand: she buys it for the *color* and the *vibe*, not heritage durability. Confirm avatar with the user if the angle hinges on it.

### Market sophistication & awareness (slot pre-fill defaults)
- **Sophistication: 3–4** — jelly/PVC bags are trendy but less claim-saturated than leather totes. You can lead more directly with the *look* and *color*.
- **Awareness: problem-aware → solution-aware** (she wants a fun summer bag) — impulse-friendly.
- **Angle / wound:** "I want a fun, summer-proof bag that pops in photos and won't be ruined by sand/water/spills" — practicality of jelly + color expression. Vindication: the bag everyone asks about at the pool.

## Flow
1. **Load context above** — never ask for product, colorways, or references. *Do* confirm the younger-skew avatar if the angle depends on it.
2. **Confirm format.** Default: **TikTok UGC** (fast, color-forward, trend-audio). Confirm with one question.
3. **Mine the ripped UGC** in `ugc-ripped/jelly firkin ripped/` for proven hooks/beats (run `watch` for transcripts).
4. **Run the ad-concept-builder 7-slot flow, FRAMED FOR VIDEO** — defaults below, via AskUserQuestion.
5. **Output the Video Ad Concept Brief** (artifact below).
6. **Offer to produce** → video-scene-replicator / ugc-forge / higgsfield-replicator (reference paths baked in here; no standalone product-scale skill yet).

### Product-tuned slot defaults (jelly tote)
| Slot | Default | Why |
|------|---------|-----|
| Concept/vehicle | "Color drop / summer haul" trend-audio UGC | Color is the hook for this product |
| Lead | Visual pattern-interrupt ("This bag is jelly — and it's wipe-clean after the beach") | Lead with the look + the practical twist |
| Mechanism intro | Wipe-clean, waterproof, sand/spill-proof | The functional reason-to-believe for jelly |
| Solution intro | Full-court / Discovery — product is the star early | Lower sophistication tolerates earlier product |
| Proof | "Got 12 'where's that from' DMs" social proof beat | Younger social-proof trigger |
| CTA | Color-scarcity ("these colors sell out") → PDP | Honest, color-driven urgency |
| Length | 10–25s trend-audio UGC | Channel-appropriate |

## Video Ad Concept Brief (the artifact)
```
# VIDEO AD CONCEPT — Velantra Jelly Tote
Format/destination:  <TikTok UGC | static→animated>
Avatar:              <younger color-forward cut of the Velantra Woman>
Awareness/Sophist.:  <…> / <3–4>
Angle (wound):       <fun + summer-proof + photogenic>

HOOK (0–3s):         "<exact line>"
BEATS:
  1. <shot — visual + VO/on-screen text + role>
  2. …
PROOF BEAT:          <wipe-clean demo / DM social proof>
CTA:                 "<exact words>" → <destination>

PRODUCTION NOTES
  Colorway(s):       <hero candy colorway>
  Reference clips:   ugc-ripped/jelly firkin ripped/<file(s)>
  Product refs (internal): product-references/jelly tote/<files> (i2i)
  Editor-facing refs:      live product links + creator t2i prompt — see "Editor-facing brief rules"
  Voice/audio:       <trend audio or UGC creator>
  Build path:        video-scene-replicator | ugc-forge | higgsfield-replicator
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
- **Copy/concept engine:** [ad-concept-builder](../ad-concept-builder/SKILL.md) · lfc-writer
- **Video build:** video-scene-replicator · ugc-forge · higgsfield-replicator · aiugc-infinite
- **Research:** `brands/velantra/research/icp-branding/`
