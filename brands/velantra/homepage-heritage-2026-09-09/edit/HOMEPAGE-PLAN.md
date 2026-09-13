# Velantra heritage homepage — working design and visual plan

## Brief and reference evidence

Replace the prior homepage composition with a new Velantra variation closely following the Ralph Lauren homepage's hierarchy, editorial pacing and heritage fashion character. Preserve the original homepage and shared theme files in `before/`. Build as a reviewable variation before the final live replacement.

Reference: https://www.ralphlauren.com/, September 9, 2026. The accessible official page text establishes this order: Heritage Icons campaign, Fall campaign, The World of Luxury introduction, Collection Fall 2026 and Purple Label Fall 2026, Saddlebrook home campaign, Double RL New Arrivals. Navigation includes account, region, shopping and shipping messaging. Automated visual access is blocked by a human-verification challenge. A full-page reference screenshot has been requested. Exact image proportions, hero/video behavior, typography metrics, transition timing, crop positions and mobile rearrangement are **not observed**. The choices below are provisional original layout direction; do not describe this version as a verified pixel-for-pixel match.

## Brand direction

Warm, assured, concise and place-led. The imagery supplies the aspiration; headlines name a mood or chapter, with one clear shopping action. Dark navy, cream, chocolate leather, muted woodland greens, natural wool and warm stone. Use the Velantra wordmark and original copy. Avoid fictional founding dates, artisan/manufacturing scenes, unsupported durability/warranty claims or a suggestion of affiliation with the reference brand. New campaigns use GPT Image 2; photography rather than invented video behavior for the first variation.

## Page and asset map

| Beat / reference role | Velantra copy | Visual / source | Composition and flow | Action and purpose |
|---|---|---|---|---|
| Header | Velantra; Handbags; The Autumn Edit; Travel; Accessories | Text and accessible SVG interface controls | Navy service strip, editorial wordmark, restrained navigation; white over hero then solid on scroll. Exact reference dimensions provisional. | Native search, menu and cart remain functional; links use current published collections/products. |
| Opening campaign / Heritage Icons | A Life Well Carried | NEW: adult woman in tweed and cream tailoring outside a weathered stone country house, hand-carrying Chocolate Vivienne | Wide photograph, person/bag at center-right, atmospheric left space. Full-height mobile crop preserves complete bag and handles. Hard section boundary; no automatic animation. | Shop Handbags and Discover the Vivienne. Establish the desired heritage world immediately. |
| Seasonal campaign / Fall | The Autumn Edit | NEW: Caramel Colette on an old dark wooden chair beside a folded cream knit, warm country-house window | Contrasting quiet interior still life, wide frame with bag prominent and undistorted. Heading below or overlay at bottom with adequate contrast. | Discover the Colette. Texture-led seasonal entry. |
| World introduction | The World of Velantra | Cream field with centered serif heading and one short supporting line | Generous but concise breathing space between immersive campaigns. | Introduce two product worlds. |
| Two collection panels | The Signature / The Weekend Away | Existing approved Chocolate Vivienne master, plus NEW Black Eleanor closed-front travel still life near a country-house departure doorway | Two distinct portrait cards, dark leather close-up versus wider travel scene. Stack on mobile. No repeated image from the campaigns. | Variant-specific Vivienne and Eleanor links. |
| Lifestyle/accessory campaign | The Finishing Touch | NEW Brown loop Horse Charm on warm checked wool and walnut, exact existing source | Intimate close-up, visible long pale loop and cut-strip tail; no invented hardware, no sewn-on logo. Low-overlay copy. | Shop Accessories. Expand from bags to personal details. |
| Closing brand passage | Collected for the Everyday | Editorial typography on warm cream | Short original paragraph; no fabricated founder history. Leads naturally into signup and services. | Shop the Collection; working native email signup. |
| Footer | Client services, Collection, About Velantra | Current navigation and policy links | Refined navy/cream, accessible grouped links, compact mobile accordions if useful. | Working contact, returns, shipping, search and tracking. |

## Product provenance and fidelity

- Vivienne Chocolate: owner-selected September 3 master plus current approved on-body derivative as relationship reference. Preserve soft grained dark body, warmer smooth trim, braided edge, upright rolled handles, horizontal oval gold center, parallel bar fittings, inward belt tails and key bell. Master is an approved design, not a measured finished sample.
- Colette Caramel: current v3 front/hero master; pale felt-like body, leather upper handle arcs, felt lower handle strips, narrow belt and two independently hanging gold-capped ends. No V side connection. Recorded dimensions are catalog-only.
- Eleanor Black: closed-front current source retaining horizontal oval hardware. Black exterior is leather, not canvas. Preserve source view; do not invent opening/inside details. Current physical scale unverified.
- Horse Charm Brown: assigned pale-loop brown horse, with pale saddle and brown cut-strip tail. No gold clasp. Never use the unassigned teal horse as Brown.

All image outputs require whole-frame and product-detail inspection before integration. Do not certify physical dimensions from these uncalibrated campaign scenes. Do not generate an alternate angle when it requires unknown product construction.

## Editorial implementation and QA

No narration, timed cuts, audio mix, captions or video export applies to this static homepage. Copy is real HTML, never baked into images. Text and actions remain legible with mobile crops and 200% zoom. CSS transitions only for hover/navigation, respecting reduced-motion preferences. Use responsive WebP/JPEG images, reserve dimensions, eager-load only the hero and lazy-load lower panels.

Build editable Shopify sections and a replacement `index.json`, preserving the recent quantity and accessory-gallery fixes. Validate all theme edits, inspect desktop/mobile screenshots, test navigation/search/menu/cart and variant links, and ensure there is no horizontal overflow or broken media. Keep deployment/readback receipts and a rollback copy. Exact visual comparison to Ralph Lauren remains pending the requested screenshot; ship the first variation as a draft preview if that evidence is still unavailable.

## Recovered session — September 9

The interrupted session installed draft theme `151519330369` and verified seven theme files by readback. The portrait opening and separate mobile copy panels are already installed. Resume from functional and rendered QA; preserve the existing approved campaign outputs. Cart checks must follow the installed UpCart drawer and its viewport position: closing translates the drawer offscreen rather than removing its content from layout. Validate desktop (1440), tablet (768) and mobile (390), then record the remaining reference screenshot dependency and deliver the preview.

Resumed visual QA found that the overlay header can obscure the model's face, while tablet landscape crops cut the Colette's left edge. Keep the initial header in normal flow with a cream background; retain the sticky header on scroll. Use the full landscape opening followed by its copy on tablet, and extend separate campaign image/copy panels through 1100 px. Keep the portrait mobile opening. These are original responsive decisions, pending the reference screenshot.


## Hero revision 2 — user seated-steps reference

The user rejected the opening as too AI-looking. Replace its country-house walk with the supplied seated model on stone steps, matching the subdued daylight, clothing and relaxed pose while using the Chocolate Vivienne master. Detailed observed reference and production/placement plan: `hero-steps-v2/EDITING-PLAN.md`. The new brief supersedes the opening row above; other homepage campaigns retain their existing direction.
