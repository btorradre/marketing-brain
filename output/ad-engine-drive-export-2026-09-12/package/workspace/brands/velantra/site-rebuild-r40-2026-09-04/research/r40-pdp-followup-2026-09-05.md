# R40 product-page structure — September 5, 2026

Source: [ARFORTI ALIR](https://arforti.com/products/alir-gray-taupe), inspected through a fresh desktop browser session at 1440 × 1000. HTML, computed dimensions and screenshots are saved alongside this report as `r40-pdp-followup-2026-09-05-{source.json,source.html,top.png,full.png}`.

## Exact page order

1. Main product gallery and centered purchase panel: approximately 1,389 px tall at the inspected viewport.
2. Craft section: detail film first, then centered introduction and four craft cards; approximately 1,756 px combined.
3. Split image/comparison table: approximately 1,008 px.
4. Two-item complementary collection: approximately 600 px.
5. Customer perspectives: approximately 1,511 px with current review content.
6. Three-part service strip: approximately 198 px.
7. Footer: approximately 376 px. No newsletter block on this PDP.

The section boundaries and sizes include content present at inspection; dynamic review content and font rendering can change total height.

## Film and craft geometry

The PDP reuses the homepage's 21.632-second, 1920 × 1080, 30 fps film, with 13 cuts. [Source MP4](https://arforti.com/cdn/shop/videos/c/vp/b0fc145331de40bfaecb0cc68e0acc99/b0fc145331de40bfaecb0cc68e0acc99.HD-1080p-7.2Mbps-91857694.mp4?v=0). The saved local film and shot analysis are `r40-detail-reference-2026-09-05.mp4` and `r40-detail-shot-analysis-2026-09-05.json`.

PDP display crops differ from the homepage: desktop ratio 1434/750; mobile 390/420. Both use object-fit cover. Keep the complete product within the narrower mobile window when selecting clips.

The centered craft introduction has a small kicker, serif heading, restrained sans-serif copy, and generous vertical spacing. Heading is approximately 31.68 px desktop and 22 px mobile in Cormorant Garamond. Body is Montserrat, approximately 13 px desktop and 11 px mobile, with 1.5 line height. Intro copy is capped at 672 px. Outer horizontal padding is 48 px desktop and 20 px mobile; intro-to-cards spacing ranges roughly 48–76 px.

Cards form four equal desktop columns at 1024 px and above. Mobile uses horizontal scroll/snap, each card at min(78vw, 310px), with 12 px gaps. Images are square; image-to-copy spacing is 32 px desktop and 24 px mobile. Each card uses a small stage label, a heading, then compact left-aligned prose. R40 labels four periods: days 01–03, 04–08, 09–13 and 14–15+. Those dates describe R40 and do not establish Velantra production times.

## Reviews and Velantra integration

The reference has a custom wrapper around Judge.me, including photo reviews, progressive loading and a review-submission dialog. Its shop/product identifiers and review data belong to R40 and were not reused.

Read-only Velantra discovery found no review or testimonial fields on the seven active handbag families. Only draft Portico has legacy Loox and standard rating fields. The old Impulse theme contains manually written fallback testimonials; these were excluded because no genuine customer provenance was established. No currently active review app block was recovered. The new `client-perspectives` section supports native Shopify app blocks and displays a merchant-editable honest empty state until a real feed is connected. It creates no ratings, counts, customer identities or verification badges.

## Handbag template coverage

The Handbags collection contains 14 listings: seven active families and seven draft listings. An additional active Eleanor duplicate and three draft Boat Tote aliases exist outside that collection. The 12 handbag templates cover these 18 listings without modifying accessory or default templates. Four draft listings currently using the default template require coordinated template assignments; exact IDs and proposed suffixes are in `pdp-template-integration-2026-09-05.json`.

The new order is main product → detail film → craft timeline → visual-details table → recommendations → client perspectives. Vivienne uses its approved film and four craft images. The other six active timelines use their own final macro images; each unfinished film remains disabled. Draft editorial sections remain configurable and disabled until their own media and evidence are ready.
