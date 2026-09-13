# Order status — September 7, 2026

The previous draft, 151389143105, was found published as MAIN. Duplicated it using Shopify themeDuplicate into **151410507841**, **Velantra — Order Status · Sep 7**, UNPUBLISHED. Waited for processing to complete and verified copied theme text before mutation. Live theme was not changed.

Preview: https://velantrafashion.com/?preview_theme_id=151410507841

The shared PDP section now shows “Orders open · 10 days before dispatch” beneath the subtitle for purchasable standard variants. Colette and Vivienne retain their October 2026 preorder notices. Black Weekender displays its existing preorder notice; switching back to another purchasable color restores Orders open. Unavailable or zero-price variants do not claim orders are open. The theme editor has a Show order status and lead time checkbox, enabled by default.

Existing batch-number/final-orders controls remain available, but no invented batch number, fake deadline or unsupported final-orders claim was enabled. No actual Velantra production batch or cutoff has been supplied. The implemented message is order availability and confirmed lead time, not manufactured scarcity.

Three files changed: sections/main-product.liquid, snippets/commerce-script.liquid, locales/en.default.json. All passed theme validation and Shopify readback. All 26 PDP desktop/mobile cases passed, including applicable color transitions, October dates, Meridian Pebbled leather, one-paragraph descriptions, no detail films and no horizontal overflow. qa.py and qa.json record the checks.

Publication must be performed manually in Shopify admin under the connector's previously established safety restriction. No attempt was made to bypass it. This draft supersedes older draft preview links for this pending update.
