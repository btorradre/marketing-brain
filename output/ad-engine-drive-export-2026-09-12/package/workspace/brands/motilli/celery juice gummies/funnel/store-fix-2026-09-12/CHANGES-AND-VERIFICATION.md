# Motilli live store repair — September 12, 2026

Live URL: https://getmotilli.com/products/motilli-3-bottle-90day-reset

Scope: user authorized fixing the store to align with the ads after requesting the concise Nuora-flow script. The new PDP follows that revised script: GLP-1 context, potentially lower fiber intake, FOS prebiotic fiber and daily regularity support, celery juice powder/chlorophyllin identification, two gummies daily with water, and 90-day refund protection. Older video files were not rewritten, produced or relaunched in this store task. Existing stronger stomach-restoration claims are not substantiated by this work.

## Confirmed issues repaired

- The old mobile ATC was approximately 1,074 px down at 390×844. The new primary ATC is approximately 873 px down, and a working sticky ATC with the selected total is accessible immediately and while reading. It hides when the cart opens.
- The floating Microsoft Brand Agents assistant covered bundle choices and displayed old “90-day reset” copy and a savings prompt. Disabled only the Brand Agents embed. The separate Clarity analytics embed remains enabled.
- Clicking the already-selected three-bottle option reset it to one bottle on both the original page and the preview. The new template prevents that unintended deselection; choosing other offers still works.
- The PDP mixed upper-stomach restoration, fiber-gel, ingredient synergy and fixed week-by-week results with conflicting dosing instructions. Replaced those sections with the revised FOS explanation, daily routine and clear expectations. Removed unsubstantiated review/stat blocks from this PDP; this is not a finding that the underlying customers/reviews are fabricated.
- “90 days” now describes refund protection and bundle supply, not a required physiological reset. The one-bottle option also has the guarantee.
- The shipping policy said all US shipping was free; the actual Shopify profile charges $4.99 below $45 and offers free standard shipping at $45+. Updated the policy and buying-section disclosure to match that configuration. Preserved rates, prices, taxes and discount logic.
- Support links on the new PDP use support@trymotilli.co, the customer-facing address configured in Shopify and used by its policies. No messages were sent. An API-returned privacy-policy template contained placeholders, but browser inspection confirmed Shopify renders them correctly; it was not rewritten.
- The homepage routes to the same PDP and preserves query-string attribution parameters. Header guarantee/shipping copy and footer policy links are consistent.
- Featured product/cart/social image now uses the same existing plain bottle source as the new PDP, without the former surrounding promotional claim graphics. Original media remain attached and recoverable; no product images were generated or physically relabeled.

## Verification

Theme checks passed for the new section/template files. Shopify accepted and read back the deployed files. Native bundle mechanics were retained and tested using isolated guest carts:

| View | Selection | Cart quantity | Cart total before shipping/tax | Result |
|---|---|---:|---:|---|
| Mobile 390 px | One bottle | 1 | $29.99 | Passed; checkout loaded |
| Mobile 390 px | Buy 2, get 1 free | 3 | $59.98 | Passed through sticky ATC |
| Desktop 1440 px | Buy 3, get 2 free | 5 | $89.97 | Passed |

All tested lines use variant 53033648750959, with no selling-plan allocation. No orders or payments were submitted. No horizontal overflow or JavaScript page errors were observed in those cases. Free bottles remain separate discounted cart lines, as in the existing bundle integration.

Shopify product_added_to_cart telemetry was observed for each case. A separate live browser test verified Facebook ViewContent, PageView and AddToCart requests with HTTP 200 for pixel 1536431777433131, matching the campaign's configured pixel. Facebook's POST body is multipart form data; earlier test parsers incorrectly returned empty event fields. No duplicate/manual pixel was added, and no visitor consent settings were changed. These tests establish browser event delivery, not Ads Manager attribution, server-side deduplication, or conversion lift. The recorded AddToCart value is $29.99; complete bundle-value reporting was not certified.

The original cart also worked in the baseline test. These are confirmed friction and consistency fixes, not proof of a single cause of zero reported campaign add-to-carts. Multiple synthetic carts/checkout starts were generated during QA and must be excluded from organic performance interpretation.

## One unresolved product fact

The existing bottle artwork says 5 g fiber; the existing Supplement Facts say 3.3 g total fiber, including 3 g FOS per two gummies. Asked the user which matches the shipped product. No answer was available at publication. Retained the existing label imagery and facts, and did not invent a corrected amount or relabel packaging. This prevents calling the entire store factually reconciled until the actual label is confirmed.

## Deployment and rollback evidence

Shop: y9t3s8-ns.myshopify.com. Existing main theme: 188158148975. Product: 14972162933103. New product template suffix: motilli-regularity. The previous default product template remains untouched; other product-specific templates were not replaced.

- before/: original theme files touched or inspected; products-before.json, policies-before.json and product-immediately-before-publish.json preserve prior product/policy data.
- published-file-hashes.json and publish/stage receipt JSON files identify writes. product-after.json and product-image receipts identify the new featured image and preserved originals.
- theme-validation-v2.txt / theme-validation-v3.txt and GraphQL validation receipts record checks.
- preview-verification.json / live-verification.json contain functional results; meta-delivery-final.json contains the parsed Meta delivery evidence; final-content-and-images.json verifies the final featured image and copy.
- live-final-mobile.png and live-final-cart.png show the final shopper-facing result.

To roll back, first compare the current live values against the deployment receipts so later edits are not overwritten. Restore the product's prior template suffix and description from product-immediately-before-publish.json; restore homepage/header/footer from before/; restore only the Brand Agents disabled flag in a freshly fetched settings_data.json; restore the shipping policy body from policies-before.json; reorder original product media using products-before.json. New unused sections/assets can remain without affecting the restored template. The pre-publication HTML in preview-page-source.html preserves the prior visible SEO title/description; the product's original SEO metafield override state was not separately exported. Do not blindly execute the initial build script against the final theme files.
