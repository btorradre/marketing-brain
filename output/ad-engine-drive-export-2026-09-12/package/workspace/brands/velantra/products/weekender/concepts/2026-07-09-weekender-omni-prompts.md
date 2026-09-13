# Velantra Weekender — Google Omni Product B-Roll Prompt Pack
2026-07-10 (rev. 5 — competitor-comparison line removed, Velantra-only focus) · Product-only generation prompts, no AI UGC / no talking / no dialogue performance

**Scope:** Omni generates **product B-roll only** — clean shots of the bag, hands optional, face never. The AI UGC talking head itself (Blair, continuous footage + voice) is a separate asset produced through the normal talking-head pipeline, not Omni. These B-roll clips/stills cut in behind/over her continuous audio track, and double as the swappable backgrounds for the green screen version.

**Finalized script (9 lines — no competitor comparison, Velantra-only per standing rule):**
> "If you're looking for the perfect summer travel bag, I have the one for you. This is the Velantra Weekender. It's a structured top-handle silhouette, real brass hardware, but actually built for a weekend trip. This one holds its shape even packed full. I've thrown it in the trunk every weekend this summer, and it still looks brand new. It actually fits everything, two outfits, shoes, your toiletries. It comes in two different colors and three different sizes. They're having a summer sale right now and colorways go fast. I left the link below."

**Rule: one new visual per line. Never compare to other brands/products** — no wound beat built on "other bags," no price comparisons, no competitor mentions of any kind. Velantra-only focus throughout. 9 lines total, 2 stay on Blair's talking-head footage (name reveal, close), 7 are B-roll generated here — including the hook line, which opens on a product close-up before she's ever seen. Exception: the "fits everything" line (packed capacity, the strongest proof beat) gets two companion clips instead of one, for editor's choice or an A/B cut.

**Image input:** canonical Weekender product reference (light chocolate colorway) for every prompt, i2i seeded — never generated from scratch. **Open-bag shots must also wire in `light chocolate 4.webp` (open-interior reference)** — see opening mechanism below. No face, no invented logos or on-bag text, never mention where the bag is made. **Attach the actual reference image(s) in Flow/Omni for every generation** — text description alone is not enough to hold product fidelity; without the image input the model will invent a generic bag.

**PRODUCT TRUTH (per the `velantra-weekender` skill — verbatim, do not paraphrase):** structured two-tone weekend bag, wider than tall, rich cognac brown leather upper flap section and two rolled cognac leather top handles over a cream ivory woven canvas (or army green twill canvas) body, a small gold oval turn lock on the front, two flat gold clasp plates with cognac leather belt straps threaded through them, a small cognac leather key bell tied to the handle base, cognac leather corner patches at the bottom, visible stitching, gold hardware, no logos anywhere on the bag, natural cream cotton canvas interior lining with a cognac leather slip pocket on the back wall. **No zipper anywhere.**

**OPENING MECHANISM (MANDATORY on any open-bag shot):** the entire cognac leather flap, one single piece, folds backward over the top rear edge and hangs down flat against the outside of the **back** of the bag, mostly hidden. The front of the open bag is almost entirely canvas — only a thin leather binding at the mouth, the small gold turn-lock post, and the two hanging belt straps with their gold clasp plates. **No leather panel, no flap, no pocket shape ever appears on the front of an open bag** — that is the exact defect that hit Pack's packing shot. Wire `light chocolate 4.webp` in as a reference on every open-bag prompt.

**SIZE (2026-07-10):** every prompt below depicts the **Medium** (16in W x 13in H x 6.5in D — an overnight trip or an oversized everyday carry, slides under an airline seat, per the live PDP). B-Roll 6 (colors + sizes flat lay) is the one exception — it deliberately shows all three sizes (Medium 16x13x6.5in, Medium Large 18x14.5x7in, Large 20x15.5x8in) side by side.

---

## Full timeline

| # | Time | Line | Visual |
|---|------|------|--------|
| 1 | 0:00–0:05 | "If you're looking for the perfect summer travel bag, I have the one for you." | B-Roll 1 — close-up on the Weekender, before she's revealed |
| 2 | 0:05–0:06.7 | "This is the Velantra Weekender." | **Talking head** (not Omni) — bag revealed in her hands |
| 3 | 0:06.7–0:11 | "It's a structured top-handle silhouette, real brass hardware, but actually built for a weekend trip." | B-Roll 2 |
| 4 | 0:11–0:13.7 | "This one holds its shape even packed full." | B-Roll 3 |
| 5 | 0:13.7–0:19 | "I've thrown it in the trunk every weekend this summer, and it still looks brand new." | B-Roll 4 |
| 6 | 0:19–0:22 | "It actually fits everything, two outfits, shoes, your toiletries." | B-Roll 5 + 5b (two clips, editor's choice or A/B) |
| 7 | 0:22–0:25.3 | "It comes in two different colors and three different sizes." | B-Roll 6 |
| 8 | 0:25.3–0:29 | "They're having a summer sale right now and colorways go fast." | B-Roll 7 |
| 9 | 0:29–0:31 | "I left the link below." | **Talking head** (not Omni) — bag in hand, warm close |

---

## B-Roll prompts

**1. [VIDEO] — pairs with: "If you're looking for the perfect summer travel bag, I have the one for you."**
```
Handheld macro close-up, phone drifting slowly over a console table or entryway bench, the Velantra Weekender (light chocolate) fills the frame, warm soft daylight from one side. No face, no hands yet — just the bag sitting in frame before she's revealed. Vertical 9:16. No invented text or logos on the bag.
```

**2. [VIDEO] — pairs with: "It's a structured top-handle silhouette, real brass hardware, but actually built for a weekend trip."**
```
The Velantra Weekender (natural canvas body, cognac leather trim) sits upright on an airport bench or a car trunk ledge, implying a travel context. Camera slowly drifts in to end on a macro close-up of the small gold oval turn-lock and the gold clasp plates with cognac leather belt straps, warm natural light catching the metal. No face, no hands. Vertical 9:16. No invented text or logos on the bag.
```

**3. [VIDEO] — pairs with: "This one holds its shape even packed full."**
```
Close-up, both hands press flat against the base of the Velantra Weekender (light chocolate) to show it holds its structure, natural grip, no visible strain or give in the shape. No face in frame. Vertical 9:16. No invented text or logos.
```

**4. [VIDEO] — pairs with: "I've thrown it in the trunk every weekend this summer, and it still looks brand new."**
```
The Velantra Weekender (light chocolate) sits in the open trunk of a car in natural daylight. Camera slowly drifts closer to end on a tight macro of a bottom corner and base edge, pristine leather and stitching with zero scuffing or wear. No people, no hands, no face. Vertical 9:16.
```

**5. [VIDEO] — pairs with: "It actually fits everything, two outfits, shoes, your toiletries."**
```
Close-up, the Velantra Weekender (light chocolate) open per the opening mechanism above — the leather flap folded back and hidden against the rear, the front showing only canvas, the thin mouth binding, the turn-lock post, and the hanging belt straps — two folded outfits, a pair of shoes, and a toiletry bag visible inside against the cream canvas interior and cognac slip pocket, a hand adjusts one item into place. No face in frame. Warm natural light. Vertical 9:16. No invented text or logos. Reference: light chocolate 4.webp wired in alongside the closed hero shot.
```

**5b. [VIDEO] — companion clip — pairs with: "It actually fits everything, two outfits, shoes, your toiletries."**
```
Close-up, hands fasten the Velantra Weekender (light chocolate) closed after being packed full — buckling the two leather belt straps through the gold clasp plates and turning the gold oval lock shut — the bag closing flush with no strain or gap, the flap already folded to the back and out of view the entire time. No face in frame. Warm natural light. Vertical 9:16. No invented text or logos.
```

**6. [IMAGE] — pairs with: "It comes in two different colors and three different sizes."**
```
Clean flat lay product graphic: the Velantra Weekender shown in its two core colorways (cream ivory canvas and army green twill) side by side, with all three size variants lined up beneath or beside them from smallest to largest (Medium 16in W x 13in H x 6.5in D, Medium Large 18in W x 14.5in H x 7in D, Large 20in W x 15.5in H x 8in D), soft neutral background, even studio lighting, no text, no logos, no people.
```

**7. [IMAGE] — pairs with: "They're having a summer sale right now and colorways go fast."**
```
Clean product graphic, the Velantra Weekender (light chocolate) on a soft neutral background with a simple "Summer Sale" badge or percentage-off callout in the corner, minimal and elegant, no real brand logos, no invented text beyond "Summer Sale."
```

---

## Reuse note

These same 7 assets (pick either 5 or 5b, not both) are the swappable backgrounds for the green screen version (Section B of `2026-07-09-aiugc-talking-head-greenscreen-brief.md`) — generate once, use in both pieces.

## Outro (optional, after the spoken CTA)

**8. [IMAGE] — PDP / shop-now card**
```
Clean e-commerce product page mockup graphic for the Velantra Weekender, light chocolate colorway centered, minimal white background, a subtle "Shop Now" call-to-action button, no real brand logos, no invented text beyond "Shop Now."
```

---

## Notes

- Nothing above includes a person's face, dialogue, or a voice line — that's the talking-head asset's job, generated separately.
- **Never compare to another brand or product, in any form** — no "other bags," no price comparisons, no competitor mentions. See `feedback_velantra_no_competitor_comparisons`.
- Never mention where the bag is made, in any prompt (see `feedback_velantra_origin_claims`).
- No invented logos or on-bag text in any prompt.
- One visual per line — do not sub-split a single line into multiple cuts even if it runs long; let the line's visual hold.
