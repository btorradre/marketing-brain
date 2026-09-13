---
name: velantra-boat-tote-concept
description: Write a VIDEO AD CONCEPT + creative brief for the Velantra Boat Tote specifically. Trigger when the user says "video ad concept for the boat tote", "write a boat tote ad", "new video ad for the boat tote", "concept for the Boatkin", or runs ad concepting/briefing for this product. Pre-loads the Boat Tote's reference images, colorways, winning UGC, the Velantra avatar, and market sophistication, then runs the ad-concept-builder intent flow tuned for a VIDEO ad and outputs a production-ready concept brief. Pair with the velantra-boat-tote product-scale skill for generation.
disable-model-invocation: false
---

## GOLDEN NUGGET DOCTRINE (MANDATORY — locked 2026-07-11)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded DEEP FRAME in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: *is this the topic, or is this the motive?* If it's the topic, dig one layer deeper (memory loss → becoming my parent; GLP-1 bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes.** The golden nugget LEADS — very top of the piece, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence BEFORE drafting. When analyzing a reference ad/funnel/swipe instead of writing, state the nugget it's built on and whether it leads with it. If the research hasn't surfaced one, mine reviews/VOC/Reddit until it does — never default to a surface angle.

# Velantra Boat Tote — Video Ad Concept & Brief

Product-specialized entry point for concepting a **video ad** for the Velantra Boat Tote (the "Boatkin"). It is a thin specialization layer over [ad-concept-builder](../ad-concept-builder/SKILL.md): it pre-loads everything specific to THIS product — references, colorways, avatar, market sophistication, winning UGC — so the concept is grounded in the real product and the real buyer, then steers the 7-slot intent flow toward a **video** ad (UGC / VSL / TikTok) and hands off a creative brief.

> Generation counterpart: the [velantra-boat-tote](../velantra-boat-tote/SKILL.md) product-scale skill. This skill decides *what* the ad says; that skill helps *render* it.

## When this runs
- "write a video ad concept for the boat tote" / "Boatkin"
- "new boat tote ad" · "concept for the boat tote" · "boat tote UGC idea"
- The user runs ad concepting/briefing and names the Boat Tote.

## Product context — PRE-LOADED, do not re-ask

**Product:** Velantra Boat Tote (canvas-and-leather "Boatkin")
**Category:** Structured Birkin-silhouette tote — natural cream canvas body + contrast leather trim, gold turn-lock clasp, gold feet
**Price band:** $50–$150 (Velantra accessible-luxury) vs. the $1,200–$1,600 Hathaway Hutton "Boatkin" it echoes
**Colorways:** Two-tone (cream canvas + colored leather trim): navy, red, pink, dark green, olive green, orange, sunny yellow, yellow, emerald, lady pink, light grey, lineman. Solid: green, navy, olive, orange, pink, red, yellow.

### Reference assets (base: `/Users/brooksorradre2/Documents/marketing brain/brands/velantra/products/boat-tote/`)
- `product-references/boat tote/` — canonical colorway flats + `01.jpg`–`06.jpg` multi-angle studio shots (use for i2i)
- `product-images/boat tote/` — generated/edited product shots
- `statics/boat tote/` — static ad creatives (mine for proven visual angles)
- `ugc/ripped ugc/` — **10 ripped UGC clips** → mine these for hook lines, beat structure, and pacing before writing

### Avatar — the "Velantra Woman" ("Caroline", 40–48)
Coastal-affluent professional, $150K+ HHI, Newport Beach / Hamptons / Nantucket energy. Owns the Birkin *silhouette* obsession but **rejects the logo, the price, the artificial scarcity**. Buys quiet luxury on the IYKYK principle — wants peer recognition, not stranger recognition. Discovers via peer word-of-mouth + trusted micro-creators; shares a find as an identity act ("look what I found" = "look how good my taste is"). Full ICP: `brands/velantra/research/icp-branding/Ideal_Customer_Profile.md`.

### Market sophistication & awareness (slot pre-fill defaults)
- **Sophistication: 4–5** — the "Birkin alternative / Boatkin dupe" claim is crowded. Don't lead with "luxury for less"; lead with a *mechanism* or *new identity* (the discovery story, the craftsmanship proof, the place-name anchor).
- **Awareness: problem-aware → solution-aware** for cold TikTok; **product-aware** for retargeting.
- **Angle / wound:** "I want the Birkin shape without being the woman who paid $12k for a logo" — taste-anxiety + new-money fear. Vindication: the bag that gets the "where did you get that?" without the markup.

## Flow
1. **Load context above** — never ask for product, colorways, avatar, or reference paths; they're here.
2. **Confirm format.** Default destination: **TikTok UGC** (most ripped UGC lives here). Other options: VSL landing, static→animated, talking-head. Confirm with one question.
3. **Mine the winning UGC** in `ugc/ripped ugc/` — pull the actual hooks/beats that already work for this product before inventing new ones (run the `watch` skill on a clip if you need the transcript).
4. **Run the ad-concept-builder 7-slot intent flow, FRAMED FOR VIDEO.** Present the product-tuned defaults below via AskUserQuestion; user confirms/overrides.
5. **Output the Video Ad Concept Brief** (artifact below).
6. **Offer to produce** via the [velantra-boat-tote](../velantra-boat-tote/SKILL.md) product-scale skill → video-scene-replicator / ugc-forge / higgsfield-replicator.

### Product-tuned slot defaults (boat tote)
| Slot | Default | Why |
|------|---------|-----|
| Concept/vehicle | "The discovery" — creator finds the Boatkin at a coastal pop-up | Matches place-name-anchored word-of-mouth behavior |
| Lead | Curiosity / authority-subversion ("Everyone on the Nantucket ferry has this bag — it's not Hermès") | Sophistication 4–5 needs a fresh frame, not a price claim |
| Mechanism intro | Craftsmanship reveal — solid brass turn-lock, reinforced canvas, 2-yr warranty | Earns the "quality you can feel" belief |
| Solution intro | Discovery position (Whisper→Discovery) — product enters as the answer she stumbled onto | Avoids hard-sell that triggers her "manufactured small-brand" suspicion |
| Proof | Peer/UGC social proof + "where did you get that?" testimonial beat | Her #1 trust trigger is peer recommendation |
| CTA | Soft, scarcity-light ("colors sell out each season") → PDP | Hard scarcity reads as the artificial-scarcity she rejects |
| Length | 20–40s UGC (or 60–90s VSL) | Channel-appropriate |

## Video Ad Concept Brief (the artifact)
```
# VIDEO AD CONCEPT — Velantra Boat Tote
Format/destination:  <TikTok UGC | VSL | static→animated>
Avatar:              Velantra Woman (Caroline, coastal-affluent, anti-logo)
Awareness/Sophist.:  <…> / <4–5>
Angle (wound):       <…>

HOOK (0–3s):         "<exact spoken/on-screen line>"
BEATS:
  1. <shot — visual + VO/on-screen text + role>
  2. …
PROOF BEAT:          <UGC testimonial / craftsmanship demo>
CTA:                 "<exact words>" → <destination>

PRODUCTION NOTES
  Colorway(s):       <hero colorway>
  Reference clips:   ugc/ripped ugc/<file(s)> (beat/pacing source)
  Product refs (internal): product-references/boat tote/<files> (for i2i)
  Editor-facing refs:      live product links + creator t2i prompt — see "Editor-facing brief rules"
  Voice:             <ElevenLabs clone or UGC creator>
  Build path:        velantra-boat-tote → <video-scene-replicator | ugc-forge | higgsfield-replicator>
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
- **Generation:** [velantra-boat-tote](../velantra-boat-tote/SKILL.md)
- **Copy/concept engine:** [ad-concept-builder](../ad-concept-builder/SKILL.md) · lfc-writer
- **Video build:** video-scene-replicator · ugc-forge · higgsfield-replicator · aiugc-infinite
- **Research:** `brands/velantra/research/icp-branding/`
