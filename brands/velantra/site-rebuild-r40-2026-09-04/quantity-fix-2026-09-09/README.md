# Quantity selector fix — September 9, 2026

Published to live theme 151389143105 (Detail Film Cleanup · Sep 6).

Root cause: all 18 product templates inherited `show_quantity: false` from the shared main-product section. Changed the default to true, with translated minus/plus controls and native numeric entry above Add to cart / Pre-order. The shared product form submits the selected quantity, including through the existing mobile purchase button. Minimum quantity is one. Only `sections/main-product.liquid` changed on the live theme. The canonical local theme received the same focused patch, preserving its other content.

Shopify Liquid validation passed. All 13 published active product pages render the numeric selector and both buttons. Desktop Vivienne and mobile Bag Scarf passed increment, decrement, minimum, direct entry, zero normalization, quantity preservation through a color change, and adding two units to the cart. No browser errors. Test carts were cleared; no orders were placed.

`before/` contains the original live files; `after/sections/main-product.liquid` contains the deployed patch; `deployment.json`, `catalog-qa.json`, `browser-qa.json` and the screenshots contain verification evidence. Shopify normalized trailing whitespace on save; file content matches after trimming trailing whitespace.

Rollback: restore `before/sections/main-product.liquid` to theme 151389143105 after checking for subsequent edits.
