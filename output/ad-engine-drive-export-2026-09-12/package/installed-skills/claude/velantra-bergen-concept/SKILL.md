---
name: velantra-bergen-concept
description: Write a VIDEO AD CONCEPT + creative brief for the Velantra Bergen specifically. Trigger when the user says "video ad concept for the bergen", "write a bergen ad", "new video ad for the bergen", or "concept for the bergen". NOTE this product is a PLACEHOLDER — references are not loaded yet; the skill will ask for the silhouette/colorways/refs before concepting, then run the ad-concept-builder intent flow tuned for a VIDEO ad.
disable-model-invocation: false
---

## GOLDEN NUGGET DOCTRINE (MANDATORY — locked 2026-07-11)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded DEEP FRAME in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: *is this the topic, or is this the motive?* If it's the topic, dig one layer deeper (memory loss → becoming my parent; GLP-1 bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes.** The golden nugget LEADS — very top of the piece, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence BEFORE drafting. When analyzing a reference ad/funnel/swipe instead of writing, state the nugget it's built on and whether it leads with it. If the research hasn't surfaced one, mine reviews/VOC/Reddit until it does — never default to a surface angle.

# Velantra Bergen — Video Ad Concept & Brief  ⚠️ PLACEHOLDER

Product-specialized entry point for concepting a **video ad** for the Velantra Bergen. Thin specialization layer over [ad-concept-builder](../ad-concept-builder/SKILL.md).

> **⚠️ This product is a placeholder.** As of skill creation, `brands/velantra/products/bergen/` has no reference images, colorways, or UGC. Unlike the other Velantra concept skills, this one CANNOT pre-load product specifics — it must collect them first. Once the product folder is populated, update the "Product context" block below to match the sibling skills (e.g. boat-tote) and remove this warning.

## When this runs
- "write a video ad concept for the bergen" · "new bergen ad" · "concept for the bergen"

## Product context — PARTIALLY KNOWN
**Product:** Velantra Bergen
**Brand band:** $50–$150 (Velantra accessible-luxury), no-logo quiet-luxury positioning
**Silhouette / category:** ❓ unknown — **ask the user**
**Colorways:** ❓ unknown — **ask the user**
**Reference assets:** `brands/velantra/products/bergen/` is empty/placeholder — **ask the user for product references** (or where to find them) before any i2i / production handoff.

### Avatar — the "Velantra Woman" ("Caroline", 40–48)
Coastal-affluent professional, anti-logo, IYKYK, buys "fewer, better things that last." Full ICP: `brands/velantra/research/icp-branding/Ideal_Customer_Profile.md`. This applies to the Bergen by default; refine once the silhouette is known.

### Market sophistication & awareness (brand defaults)
- **Sophistication: 4–5** (Velantra category default). **Awareness:** problem→solution-aware cold; product-aware retargeting. Angle depends on the silhouette — set once known.

## Flow
1. **Collect the missing product context FIRST** — ask the user (AskUserQuestion): silhouette/category, colorways, and where the reference images live. Do not invent product details.
2. **Confirm format.** Default: TikTok UGC.
3. **Run the ad-concept-builder 7-slot flow, FRAMED FOR VIDEO**, using the brand avatar + the silhouette-specific angle you just gathered.
4. **Output the Video Ad Concept Brief** (same artifact shape as the [boat-tote concept skill](../velantra-boat-tote-concept/SKILL.md)).
5. **Offer to produce** → video-scene-replicator / ugc-forge / higgsfield-replicator once refs exist.
6. **Backfill this skill:** once the Bergen folder is populated, copy the structure of `velantra-boat-tote-concept/SKILL.md`, fill in real colorways/paths/UGC, and delete the placeholder warnings.

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
- **Pattern to copy when populating:** [velantra-boat-tote-concept](../velantra-boat-tote-concept/SKILL.md)
- **Copy/concept engine:** [ad-concept-builder](../ad-concept-builder/SKILL.md) · lfc-writer
- **Video build:** video-scene-replicator · ugc-forge · higgsfield-replicator
- **Research:** `brands/velantra/research/icp-branding/`
