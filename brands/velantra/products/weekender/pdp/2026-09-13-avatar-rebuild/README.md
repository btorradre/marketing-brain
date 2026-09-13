# Eleanor Weekender — women and men PDP previews

Built September 13, 2026. Updated following the user's rejection of AI-looking portrait faces.

- [Women's Shopify preview](https://velantrafashion.com/products/velantra-weekender?view=wk-editorial-women&preview_theme_id=151410507841)
- [Men's Shopify preview](https://velantrafashion.com/products/velantra-weekender?view=wk-editorial-men&preview_theme_id=151410507841)
- [Selected images](delivery/images/)
- [Selected generation prompts and inputs](delivery/PROMPTS.json)
- [Gallery order, captions and CDN URLs](delivery/gallery-manifest.json)
- [Photographic treatment and source notes](delivery/PHOTOGRAPHY-NOTES.md)
- [Build plan and user correction](edit/BUILD-PLAN.md)

## Delivered

Two functioning Shopify product views, with distinct female/male styling. Vellatini's actual reference photographs were used directly for face-free crops, tactile detail, outdoor carry, car-seat context and the architectural product still. Full-body portraits were rejected and excluded. Original private reference prompts were unavailable; prompts are documented reconstructions of the observed treatment.

56 selected generated images serve 80 gallery placements: ten images for each of Cognac, Army Green, Espresso and Black, in both women’s and men’s views. All colors include styled hero, front and three-quarter product views, hands/touch, outdoor carry, car setting, handle and clasp macros, a detail view and an architectural still. Cognac retains its evidenced interior; the other three colors use an exterior corner detail instead of an unsupported interior. The selected color controls the gallery, price, variant, material copy and Black pre-order button.

The page structure follows Verano Hill's gallery/buying-column hierarchy, title, review link, price/offer, visual swatches, order/receive line, material/service tags, accordions, offer section, service strip, reviews, recommendations and newsletter/footer. Current Velantra facts replace competitor claims. There are no fabricated reviews, customer counts, BOGO promises or scarcity timers.

## Verification

All-colors expansion: both updated JSON templates passed Shopify validation (artifact `weekender-all-colors-20260913`, revision 1). All eight audience/color combinations passed actual preview checks: ten unique images loaded, correct variant IDs, all ten lightbox images and mobile carousel positions, and no horizontal overflow or page errors. Desktop/mobile and complete gallery screenshots were captured; selected screenshots were visually inspected. See [all-colors results](qa/all-colors/results.json), [validator](qa/all-colors-validator.txt), and [current Shopify state](qa/all-colors-shopify-state.json). The broader cart/checkout checks below were completed before this gallery expansion; purchasing code was unchanged.

- Liquid, JSON templates, schema and translations passed the bundled Shopify validator. Final component change passed revision 5; full files passed revision 3, with the cart integration passing revision 4.
- Both pages tested at desktop 1440×1000 and mobile 390×844 / 375×812. No horizontal overflow. Main purchase button fully visible at those mobile sizes: approximately y764–814 and y751–801.
- All four variants select correctly on each page, with matching gallery images and Black pre-order labeling.
- Gallery lightbox, keyboard arrows/Escape, mobile carousel, accordions and sticky purchase action passed.
- Actual add/remove cart operations passed. Women/Cognac and men/Black reached Shopify checkout with one matching item at $159.99. No order was placed and no personal checkout information was entered.
- Review and newsletter required-field validation passed. No review/newsletter messages were submitted. Reviews use a Shopify contact form for moderation; no authentic published reviews were found.
- Four recommendation images display square and load. Header, footer, audience and recommendation destinations returned successful responses.
- No JavaScript errors or broken selected gallery images in the functional checks.

Evidence: [functional results](qa/functional-summary.json), [final visual/link checks](qa/final-visual-check.json), [Shopify state](qa/final-shopify-state.json). Final desktop/mobile/full-page/cart/checkout screenshots are in `qa/`.

## Staging and remaining publication boundary

These are drafts in existing unpublished theme 151410507841, using new namespaced files and an additive translation namespace. The store had reached its 20-theme limit. Existing theme files were preserved except the backed-up addition of `wk_editorial` translations. Live theme 151519330369 remains the main theme. The canonical product still uses its original `weekender` template and the same inventory variants.

The new pages and their cart drawer use the replacement imagery. Shopify checkout still uses the canonical live product's existing thumbnail; changing that thumbnail requires assigning the approved imagery to the live product. No live product media, ad destinations or theme publication was changed.

The existing UpCart app intercepted the new form and displayed the old thumbnail. The custom layout now sets its inspected skip-interceptor flag for these views and preserves native fetch for the scoped cart implementation. App configuration outside these views is unchanged. This behavior was verified in the actual previews; see the functional receipts.

The arrival line is an estimate based on the current 10-day dispatch allowance followed by 7–10 business days in transit for the US. It is separate from transit, not an accelerated shipping promise. General store shipping policy still contains the pre-existing timing inconsistency documented in the conversion audit.

Full-resolution source files remain in `media/` and the provider directory, with selected/rejected records in `edit/`. The `delivery/images/` directory contains only the selected web images.
