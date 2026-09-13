# Weekender women / men PDP build plan

September 13, 2026. User authorizes building two Weekender product pages with Vellatini gallery compositions, Verano Hill section/layout treatment and Velantra's Ralph Lauren-inspired aesthetic. This is product-page development, not an ad timeline or video storyboard.

## Source study

Actual desktop browsers, page markup and all ten Vellatini gallery images were captured in ../references. Vellatini gallery order: coat-and-bag torso crop; clean front packshot; three-quarter packshot; tactile hands/body crop; outdoor coat carry; car-seat everyday context; strap/leather detail; closure macro; open interior; architectural product still. The two isolated PNGs have transparent backgrounds, not black studio backgrounds. Source images are reference only, never Velantra deliverables.

Verano Hill: broad two-column image grid on desktop beside a compact buying column. Product title in spaced sans serif; review stars/count immediately below; price and offer chip together; illustrated color swatches; order/receive line; wide dark add-to-cart button; compact material/service tags; Details / What Fits / Delivery & Returns accordions; offer panel; four service benefits; full review summary/list; recommendations; community/footer. Capture uses Montserrat, 22px title at 1440px. The new pages borrow composition and hierarchy, not their 578 reviews, customer counts, BOGO offer or delivery promises.

## Product and claims

Canonical Shopify product 7971794747457, current handle velantra-weekender. Both pages purchase the existing color variant IDs; no duplicate stock pools. Four colors: Cognac, Army Green, Espresso, Black. One nominal size. Current price/availability must be rendered from Shopify, not baked into image text. Use August 8 physical Cognac construction reference: horizontal oval fitting, single contoured flap, two handle cutouts, two closure straps, rolled handles, canvas body, leather corners, caramel interior/slip pocket. Existing vertical-oval generated gallery is not an input. Nominal dimensions are owner specification, not measured sample certification. No airline, capacity, origin or leather-grade claim inferred from generated images.

## Gallery sequence for each audience

| Position | Asset / action | Reference cue and purpose | Audience distinction |
|---|---|---|---|
| 1 | Close-cropped model holding Cognac by top handles beside coat | Vellatini 1; immediate outfit aspiration and recognizable bag | Woman in oatmeal wool and cream knit; man in navy tailoring and camel knit |
| 2 | Exact Cognac front, light seamless | Vellatini 2; clean construction and color recognition | Shared product evidence |
| 3 | Exact Cognac slight three-quarter angle | Vellatini 3; depth and reinforced corners | Shared product evidence |
| 4 | Hands resting on bag / leather, waist crop | Vellatini 4; tactile desire | Female cream/satin styling; male oxford/knit styling |
| 5 | Tight shoulder-to-thigh crop carrying by hand outdoors | Vellatini 5; styled real-life silhouette | Distinct female and male clothing and hands; face outside frame |
| 6 | Bag on tan leather car seat, closed | Vellatini 6; everyday premium setting without unsupported fit demonstration | Distinct scene and accessories for each audience |
| 7 | Handle base, stitch and canvas macro | Vellatini 7; inspect actual material transitions | Shared product evidence |
| 8 | Horizontal oval fitting / flap macro | Vellatini 8; closure identity; no invented zipper | Shared product evidence |
| 9 | Caramel interior and wide slip pocket | Vellatini 9; show actual interior construction | Shared product evidence |
| 10 | Product alone on textured architectural concrete | Vellatini 10 exact product-only composition and directional daylight | Shared product-only still; no model or face |

Create separate front packshots for Army Green, Espresso and Black. Color selection must show the correct selected bag; Cognac editorial images must remain clearly identified as Cognac and must not masquerade as another color. Add audience-specific color hero coverage as needed for a coherent selector experience.

All new raster imagery uses GPT Image 2. Preserve provider originals, prompts and input provenance. Inspect every selected output against the input, including flap, both straps, horizontal fitting, canvas/leather boundary, handle count and interior. Refine rejected images before use. Physical scale remains unverified. Export web derivatives with preserved proportions and suitable file sizes.

## Page design and behavior

White/ivory background, deep navy actions, refined dark text, quiet lines, restrained serif Velantra wordmark with the reference's compact sans-serif buying hierarchy. Desktop 2-column gallery + sticky buying panel. Mobile swipe gallery, visible pagination/thumbnail access and compact title/reviews/price/colors/action. Provide a sticky mobile purchase action after the primary action scrolls away. Keyboard-accessible gallery zoom, swatches, accordions and focus management; reduced-motion support.

Each avatar gets its own page template and gallery/copy. Retain a shared canonical product/variant cart binding. Render current price and availability. Display authentic review data if recovered; otherwise provide an honest zero-review state and a working review submission path, never fabricated stars or testimonials. Delivery line uses actual lead-time/transit assumptions with separate dispatch and arrival labels and no fake countdown. Add material, return and warranty tags using actual Velantra facts. Offer panel explains the existing sale rather than inventing BOGO. Include all reference section roles: details, what fits/size, delivery/returns, offer, service strip, reviews, recommendations and community/footer.

## Delivery and verification

Prepare and validate local Liquid/CSS/JS and generated assets. Build reviewable Shopify previews in an isolated unpublished theme, preserving the live theme, product stock and ad destinations. Test both audiences at desktop/mobile sizes, every color, gallery/lightbox, accordion, review navigation/submission validation, recommendations and cart routing. Synthetic cart tests must not place orders. Inspect actual rendered images and key screenshot states. Deliver both working preview URLs, screenshots and project directory. A publication decision, if needed, comes only after this concrete result is reviewable.

## Staging adjustment — live evidence

Shopify themeDuplicate returned no new theme; subsequent REST creation explicitly returned 422, "A shop may only have 20 themes." Verified the theme list contains 20 and no new theme. Stage only new, namespaced `wk-editorial` layout/sections/templates/assets in existing unpublished theme 151410507841 (Velantra — Order Status · Sep 7). Do not overwrite its existing files or change its role. New product views provide women/men preview URLs; preserve live theme 151519330369. The custom layout is self-contained for these views and uses the existing canonical product variants.

## User correction — photographic treatment, September 13

User rejected the first generated portraits as visibly AI-generated, especially faces, and requested the same visual style and prompting as the reference. Inspected original Vellatini slots 1, 4, 5 and 10 at full size. Slots 1/4/5 exclude faces; slot 10 is a product-only architectural still. The first full-body outdoor and architectural portraits depart from this treatment and are rejected. Preserve originals as provenance, never use those portraits in the pages.

Regenerate all model hero, tactile and outdoor images using each actual Vellatini slot as the first composition reference, followed by the exact Weekender product master and physical construction reference. Match crop, camera distance, light direction, background depth and tactile detail. Adapt only the bag and appropriate female/male clothing. No full faces, posed smiles, synthetic portrait beauty retouching, excessive warm bloom or perfect polished hands. Maintain realistic cloth folds, subtle natural skin texture and optical falloff. Slot 10 returns to the observed product-only still. Original private source prompts are unavailable; our prompts are documented reconstructions from observed images, not recovered originals.

QA: compare each replacement with its source and physical product. Reject extra feet, handles, shoulder straps, wrong clasp/flap and fake interior details. Keep bag scale plausible without certifying uncalibrated measurements.

Staging locale exception: append the new wk_editorial namespace to the existing en.default.json with an exact backup and concurrency check. Preserve every pre-existing key. The staging theme has no en.default.schema.json (verified 404); its new schema translation file is additive. Fonts are self-hosted on Shopify CDN.

## Delivery receipt

Completed both functioning unpublished Shopify preview views, 23 selected images / 32 placements, source-based photographic correction, all requested section roles and canonical variant cart binding. Final browser functional, mobile, gallery, links and checkout checks passed; see ../README.md and ../qa/. No live theme publication or product media reassignment occurred. Checkout retains the canonical live thumbnail, documented in the delivery notes.

## All-colors expansion — explicit user update

September 13: user explicitly requires the same photographic treatment for every color. Expand Army Green, Espresso and Black from two images to the complete ten-slot sequence for both audiences. Retain existing color-specific heroes/front packshots; create the missing quarter view, female/male tactile crop, female/male outdoor carry, female/male car context, handle detail, clasp detail, lower-corner material detail and architectural still. This requires 33 additional unique images, producing 56 selected images and 80 gallery placements across two pages.

Use the selected Cognac scene as the exact composition edit target and the corresponding approved color front as the material/color reference. Preserve human hands, face-free framing, garments, background, light and bag geometry. Black must remain all leather; Army Green dark olive canvas with chestnut trim; Espresso ivory canvas with deep brown trim. No new feet, buckles, straps or compartments.

Slot 9 for these three colors is a lower-corner material close-up, preserving source-visible exterior construction. Their exact SKU-specific interiors are not established by reliable opening photos, so do not invent an interior recoloring. This preserves a complete ten-image gallery and the reference's tactile detail treatment using supported views. Cognac retains its evidenced interior image.

Inspect every output individually for color, material, silhouette, horizontal oval clasp, flap, two handles/two closure straps and realistic hands. Update both draft templates to forty image blocks, ten per color. Verify all eight audience/color selections have ten correct images and functional gallery controls; preserve existing cart/checkout bindings and unpublished status. Save all new prompts and selected files in the existing delivery folder.

### Inspection corrections

All 33 first outputs were inspected individually. The Espresso clasp macro incorrectly replaced the upper front leather panel with canvas; a targeted correction restores the leather panel. Men’s touch shots showed an artificial polygonal skin texture inherited from the selected Cognac source. Regenerate skin and plain shirt texture in all four colors while preserving pose, bag, composition and lighting; select the corrected files after inspection.

### All-colors completion

Delivered 56 selected web assets in 80 gallery placements, ten per color per audience. Both JSON templates validated and staged in unpublished theme 151410507841. All eight preview combinations passed image loading, lightbox, mobile carousel and variant checks; screenshots in `qa/all-colors/`. Live theme and canonical product template remain unchanged. Follow-up skin retouch alone retained too much patterned forearm texture; full-sleeve revisions were selected after individual viewing, with remaining fine synthetic texture documented in photography notes.
