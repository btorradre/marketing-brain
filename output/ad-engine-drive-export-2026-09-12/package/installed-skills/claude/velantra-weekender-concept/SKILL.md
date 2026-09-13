---
name: velantra-weekender-concept
description: Write a VIDEO AD CONCEPT + creative brief for the Velantra Weekender specifically. Trigger when the user says "video ad concept for the weekender", "write a weekender ad", "new video ad for the weekender/duffel/travel bag", "concept for the weekender", or runs ad concepting/briefing for this product. Pre-loads the Weekender's references, colorways, the existing video asset, the Velantra avatar, and travel-bag sophistication, then runs the ad-concept-builder intent flow tuned for a VIDEO ad and outputs a production-ready concept brief. Pair with the velantra-weekender product-scale skill for generation.
disable-model-invocation: false
---

## GOLDEN NUGGET DOCTRINE (MANDATORY — locked 2026-07-11)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded DEEP FRAME in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: *is this the topic, or is this the motive?* If it's the topic, dig one layer deeper (memory loss → becoming my parent; GLP-1 bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes.** The golden nugget LEADS — very top of the piece, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence BEFORE drafting. When analyzing a reference ad/funnel/swipe instead of writing, state the nugget it's built on and whether it leads with it. If the research hasn't surfaced one, mine reviews/VOC/Reddit until it does — never default to a surface angle.

# Velantra Weekender — Video Ad Concept & Brief

Product-specialized entry point for concepting a **video ad** for the Velantra Weekender (the travel/duffel weekend bag). Thin specialization layer over [ad-concept-builder](../ad-concept-builder/SKILL.md): pre-loads this product's references, colorways, avatar, and sophistication, then steers the 7-slot intent flow toward a **video** ad and hands off a creative brief.

> Generation counterpart: the [velantra-weekender](../velantra-weekender/SKILL.md) product-scale skill.

## When this runs
- "write a video ad concept for the weekender"
- "new weekender / travel bag / duffel ad" · "concept for the weekender"

## Product context — PRE-LOADED, do not re-ask

**Product:** Velantra Weekender (structured weekend/travel duffel)
**Category:** Heritage-look weekender — the "weekend at the coast" bag, classic Velantra silhouette
**Price band:** $50–$150 (Velantra accessible-luxury)
**Colorways:** light chocolate (1–5) + core numbered variants (1–5)

### Reference assets (base: `/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/weekender/`)
- `product-references/weekender/` — `light chocolate 1–5.png` + `1–5.png` multi-angle shots for i2i
- `product-images/weekender/` — generated/edited product shots
- `video/weekender aivo 1/Luxury Bag.mp4` — **existing AI video asset** (reference / iterate on it)

### Avatar — the "Velantra Woman" ("Caroline", 40–48)
Coastal-affluent professional, anti-logo, IYKYK. The Weekender hits her **second-home / coastal-getaway** life — the ferry to Nantucket, the weekend bag that looks expensive on a luggage rack without a logo. She buys "fewer, better things that last." Full ICP: `brands/velantra/research/icp-branding/Ideal_Customer_Profile.md`.

### Market sophistication & awareness (slot pre-fill defaults)
- **Sophistication: 4** — fewer direct dupe-claims than the totes, but travel/weekender is a mature category. Differentiator = **timeless heritage look + durability for travel abuse** at the Velantra price.
- **Awareness: problem-aware → solution-aware** for cold; **product-aware** for retargeting.
- **Angle / wound:** "My weekend bag is either a beat-up gym duffel or a $900 logo bag I'm scared to scuff" — the gap between practical and beautiful. Vindication: the weekender that looks heritage-luxury and survives being thrown in the trunk.

## Flow
1. **Load context above** — never ask for product, colorways, avatar, or references.
2. **Confirm format.** Default: **TikTok UGC** travel vignette (pack-with-me / weekend-trip). Note the existing `video/` asset — offer to iterate on it.
3. **Mine the existing video asset** (`watch` it) and/or borrow a sibling beat skeleton (boat-tote `ugc/ripped ugc/`).
4. **Run the ad-concept-builder 7-slot flow, FRAMED FOR VIDEO** — defaults below, via AskUserQuestion.
5. **Output the Video Ad Concept Brief** (artifact below).
6. **Offer to produce** via [velantra-weekender](../velantra-weekender/SKILL.md) → video-scene-replicator / ugc-forge / higgsfield-replicator.

### Product-tuned slot defaults (weekender)
| Slot | Default | Why |
|------|---------|-----|
| Concept/vehicle | "Pack-with-me / weekend trip" lifestyle vignette | Travel context sells the weekender |
| Lead | Aspiration/relatability ("The bag that makes a 2-night trip feel like a getaway") | Lifestyle pull over problem-poke |
| Mechanism intro | Capacity + travel-durability proof — reinforced base, brass hardware, 2-yr warranty | Earns the "survives the trunk" belief |
| Solution intro | Whisper→Discovery | Quiet-luxury tone |
| Proof | "Threw it in the trunk all summer" durability + airport-compliment beat | Her trust triggers |
| CTA | Soft → PDP | Quiet-luxury tone |
| Length | 20–40s UGC | Channel-appropriate |

## Video Ad Concept Brief (the artifact)
```
# VIDEO AD CONCEPT — Velantra Weekender
Format/destination:  <TikTok UGC vignette | VSL | iterate-on-existing-video>
Avatar:              Velantra Woman (coastal-getaway traveler)
Awareness/Sophist.:  <…> / <4>
Angle (wound):       <practical-vs-beautiful gap>

HOOK (0–3s):         "<exact line>"
BEATS:
  1. <shot — visual + VO/on-screen text + role>
  2. …
PROOF BEAT:          <travel-durability demo / compliment beat>
CTA:                 "<exact words>" → <destination>

PRODUCTION NOTES
  Colorway(s):       <light chocolate / hero>
  Beat source:       video/weekender aivo 1/Luxury Bag.mp4 (or sibling UGC)
  Product refs (internal): product-references/weekender/<files> (i2i)
  Editor-facing refs:      live product links + creator t2i prompt — see "Editor-facing brief rules"
  Voice:             <ElevenLabs clone or UGC creator>
  Build path:        velantra-weekender → <video-scene-replicator | ugc-forge | higgsfield-replicator>
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
- **Generation:** [velantra-weekender](../velantra-weekender/SKILL.md)
- **Copy/concept engine:** [ad-concept-builder](../ad-concept-builder/SKILL.md) · lfc-writer
- **Video build:** video-scene-replicator · ugc-forge · higgsfield-replicator · aiugc-infinite
- **Research:** `brands/velantra/research/icp-branding/`
