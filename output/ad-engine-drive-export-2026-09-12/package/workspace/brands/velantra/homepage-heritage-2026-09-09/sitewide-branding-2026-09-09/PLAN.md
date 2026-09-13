# Sitewide heritage branding

Source of truth: approved Heritage Homepage draft 151519330369, including the exact 16:9 Vivienne hero. September 9, 2026.

Observed: homepage renders a separate heritage shell only on template-index. Every other page uses old near-white/charcoal settings, a centered desktop wordmark, compact uppercase product titles and small commerce text. Thirteen published product routes use twelve specialized templates. Cart includes the UpCart app; order tracking uses /apps/parcel.

Implementation:
- Share the existing cream/navy header, service strip, navigation, newsletter and footer across all theme-rendered routes.
- Set editable global theme colors to cream #f7f5ef, navy #132039, warm divider #dedad0 and readable muted #5e6269. Keep Cormorant Garamond and Montserrat from the homepage.
- Use one shared commerce/content styling snippet for editorial headings, readable details, navy purchase buttons, warm borders, forms, navigation drawers, card spacing, cart and policy content.
- Product pages: framed original studio photography, larger title-case product names, clearer left-aligned buying panel, consistent options, quantity and accordions. Keep product data, media, price, availability, preorder text and all variant/gallery logic unchanged.
- Extend heading hierarchy and spacing into craft stories, recommendations, value details and reviews. Normalize existing uppercase display settings only, including inactive product templates for future consistency.
- Inspect third-party cart and tracking output and apply styles only where the host DOM supports it. No changes to checkout settings or live publication.

QA: compare before/after screenshots, audit every published product at 1440 and 390 widths, representative tablet and small mobile widths, collection/search/contact/tracking/policy/cart/404 routes. Check shared header/footer colors, no horizontal overflow, title hierarchy, images, menu/search/cart, each accessory color and key bag variant states, quantity/add-to-cart and cart update. Validate changed theme files before draft deployment; verify server readback. Preserve before snapshots and deployment receipt.
