# Shopify deploy — native buy box, standalone page

## Why a theme template, not a content Page

A basic Shopify content Page can't render a product form — its content field isn't Liquid-evaluated, so it can't host the native buy box. To get a WORKING buy box (variant selector + bundle pricing app + add-to-cart) the page must be built as a **theme template made of sections**. Use the theme's native product-details section (which already wires up the merchant's bundle-pricing app, e.g. a quantity-break/bundle app, plus the add-to-cart button) and drop custom advertorial sections above and below it.

## Auth (Admin API, custom app)

The Shopify CLI is often not authorized for a given store. Use the Admin API with a `client_credentials` grant instead. Ask the user for the custom app's **client_id + client_secret**, then mint a short-lived access token:

```bash
curl -s -X POST "https://<shop>.myshopify.com/admin/oauth/access_token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials" -d "client_id=<id>" -d "client_secret=<secret>" \
| python3 -c "import sys,json;open('/tmp/sp_tok','w').write(json.load(sys.stdin)['access_token'])"
```

Never write the token or secret into a committed file. Read it from a temporary location and **delete that token file when finished** (e.g. `shred -u /tmp/sp_tok`). Re-mint a new token whenever needed rather than reusing an old one indefinitely.

## Discover the store (do this before deploying)

- `GET /admin/api/2024-10/themes.json` → find the `role:main` theme id (its ID may change over time if the theme gets republished — don't hardcode it).
- `GET /admin/api/2024-10/products.json` → find the product handle to bind the buy box to. Reuse a product that already has a **bundle deal configured** (the pricing tiers usually come from that bundle app's own configuration, not from Shopify's native variant system) — bind via the section's product-reference setting (commonly called something like `current_product`).
- `GET themes/<id>/assets.json?asset[key]=templates/product.json` → confirm it has a native product-details section with the bundle app block and an add-to-cart button. That's the exact buy box you're going to clone.

## Deployment pipeline

1. **Upload every generated image** to the platform's file/asset storage and record each one's resulting CDN URL, keyed by original filename.
2. **Split the finished page HTML** into "everything above the buy box" and "everything below the buy box" — these become two separate reusable content sections, with the generated-image CDN URLs inlined in. Keep all page CSS scoped under one wrapping container ID (e.g. `#advertorial-wrap`) so it can't collide with the surrounding theme.
3. **Push those two sections to the theme**, then build a new page template that stacks them as: `[top section, native buy box section, bottom section]`. Adjust the buy box's own copy/settings as needed and bind it to your target product. Preview this safely by viewing the target product's URL with a template-override query parameter (e.g. `/products/<handle>?view=<slug>`), without disrupting the product's live default page.
4. **Clone that same three-section template into a standalone page template**, and create a new published-but-unlinked page using it — this becomes your final standalone URL (e.g. `/pages/<handle>`).
5. **Delete the temporary token file.**

## Gotchas (learned the hard way)

- **Full-page caching:** after pushing a content section update, the live storefront can keep serving the old HTML for roughly 10-20 seconds. A cache-busting query string typically does NOT bust this kind of cache. Instead, explicitly touch/re-save the page record itself (e.g. `PUT /pages/<id>.json` with an empty body_html field) to force invalidation, then poll the live URL until your new content actually appears.
- **Verify on the real live URL, not a saved HTML snapshot.** Dynamic widgets (like a bundle-pricing app) are often injected by that app's own JavaScript at page-load time — they'll appear blank in a saved static HTML file but work fine on the actual live page. Check the live HTML for the app's known markers (button text like "ADD TO CART", cart-endpoint calls like `/cart/add`) to confirm the buy box is genuinely functional.
- **File storage may silently rename extensions** (e.g. storing a `.jpeg` upload as `.jpg`) — make sure your CDN-URL lookup is keyed by the same filename your HTML actually references, not by whatever extension the storage system chose.
- **Keep the surrounding theme's header and footer visible** (don't strip out all store chrome) so the shopping cart still actually functions on this page.
- Flipping a product's own default template to point at your new advertorial (e.g. setting its `template_suffix`) makes the advertorial the product's default page at its normal URL — only do this if explicitly asked; it's reversible.
