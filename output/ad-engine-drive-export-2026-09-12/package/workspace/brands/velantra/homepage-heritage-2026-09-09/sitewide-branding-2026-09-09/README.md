# Sitewide heritage branding — September 9, 2026

Installed in unpublished theme 151519330369, matching the approved homepage.

Preview: https://velantrafashion.com/?preview_theme_id=151519330369

The cream/navy service strip, navigation, wordmark position, newsletter and footer now render across the storefront. Editable theme colors are cream #f7f5ef, navy #132039, warm divider #dedad0 and muted #5e6269. Typography keeps the existing Cormorant Garamond/Montserrat fonts.

Product pages share framed original photography, larger title-case names, a left-aligned buying panel, navy purchase buttons, clearer details and matching variant/quantity/accordion treatments. The craft stories, value details, recommendations and review sections use the same editorial heading scale. Collection and search cards, filters, cart, forms, policies, blog/article/listing headings and 404 styling share the same system. UpCart's open shadow root receives a theme-local style adapter; ParcelPanel tracking receives scoped form/heading styles and places help information below tracking.

All thirteen published products passed at desktop and mobile sizes. The combined audit covers 58 distinct page/viewport combinations and 65 color selections, with additional Vivienne checks at 768px and 320px. Desktop/mobile purchase tests confirmed color changes preserve quantity, add-to-cart sends quantity 2, the full cart updates to 3, and UpCart opens/closes correctly. Isolated test carts were cleared. No order, contact request or newsletter signup was submitted.

Evidence:
- `PLAN.md`: observations, scope and implementation plan.
- `before/`: complete snapshot of 79 theme text files before changes.
- `after/` and `readback/`: authored files and verified Shopify readback.
- `deployment.json`: theme role, changed files and final SHA-256 hashes.
- `validation-1.txt` through `validation-4.txt`: successful Shopify theme validation.
- `final-qa.json`: consolidated 58 passing page/viewport checks and purchase results.
- `browser-qa.json`, `browser-recheck.json`, `interaction-qa.json`: detailed browser evidence.
- `qa/`: screenshots of products, buying panels, editorial sections, collections, contact, tracking, navigation, cart and policies.

Initial test corrections: app proxy routes need a preview cookie seeded by the homepage; empty hidden recommendation containers should not be screenshot targets; UpCart content must finish loading before testing close. All affected checks passed on recheck.

Core product forms, variant/gallery scripts, product media, availability/preorder text and the exact 16:9 homepage hero remain unchanged. Existing product template edits only normalize display heading capitalization. Changes are draft-only; publishing and Shopify-hosted checkout branding were not part of this deployment. The root `theme/` contains all authored changes. `build.py` here prepares the first sitewide revision; later refinements are in `after/`, which is the final source for this revision.

Final controls check: availability filter application, price sorting and the final cart checkout typography passed at 1440px and 390px. Shopify preview-toolbar chrome was hidden for the mobile filter interaction. See `final-controls-qa.json`.
