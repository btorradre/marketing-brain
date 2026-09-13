# Shopify + Kaching Deploy Playbook

This is the exact mechanics for getting a listicle live as a product page. The reference build targeted the Motilli store (`y9t3s8-ns.myshopify.com`, Shrine theme). Swap the store domain, theme id, OAuth credentials, and product ids for the target brand.

## Prereqs
- Admin API access token with `write_theme_code`, `write_products`, `read_products`. For Motilli, mint one via the OAuth client-credentials flow in the brand's Shopify-admin memory/reference. Tokens expire ~24h — refetch as needed.
- The store's **Shrine** theme id (the `role=main` theme): `GET /admin/api/2025-01/themes.json`.
- Confirm the **Kaching Bundles** app embed is enabled on the theme (it injects `kaching-bundles-config` JSON on product pages). Confirm theme setting `cart_type: drawer` in `config/settings_data.json`.

## Step 1 — Duplicate the product (own URL, original untouched)
Use GraphQL so the copy includes media:
```graphql
mutation Dup($productId: ID!, $newTitle: String!, $newStatus: ProductStatus, $includeImages: Boolean) {
  productDuplicate(productId: $productId, newTitle: $newTitle, newStatus: $newStatus, includeImages: $includeImages) {
    newProduct { id legacyResourceId title handle }
    userErrors { field message }
  }
}
```
Variables: `productId` = the brand's source product gid, `newTitle` = e.g. "<Product> (GLP-1 Listicle)", `newStatus` = `ACTIVE`, `includeImages` = true. Keep the returned `legacyResourceId` (numeric) and `handle` — the listicle lives at `/products/<handle>`.

Never repurpose the brand's main product page by setting a `template_suffix` on it — that replaces the canonical PDP. Always duplicate.

## Step 2 — Build the product JSON template from the brand's base
The buy box must inherit the brand's exact `main-product` block settings, so build the listicle template from a copy of the brand's `templates/product.json`:
1. `GET` the base `templates/product.json`, parse it, take `sections.main`.
2. Repurpose its `custom-liquid` blocks for the listicle right-column content (rating, subtitle, benefits, "FINAL SUPERSAVINGS" label, scarcity). Keep the stock `title` (product_title), `buy_buttons` (product_buy-buttons), and shipping-checkpoints blocks.
3. Curate `block_order` to: `[rating, title, subtitle, benefits, supersavings_label, buy_buttons, shipping, scarcity, (optional) guarantee, payments, faq, reviews]`.
4. To carry over the brand's guarantee box / low-stock warning / payment badges / FAQ accordion / reviews, copy those `custom-liquid` blocks' `custom_liquid` payloads from the base product.json into NEW block ids in the listicle template, and append them to `block_order`.
5. Build the template object:
```json
{ "sections": { "listicle_top": {"type":"listicle-top","settings":{}},
                "main": <the curated main-product section>,
                "listicle_bottom": {"type":"listicle-bottom","settings":{}} },
  "order": ["listicle_top","main","listicle_bottom"] }
```
6. `PUT` it to `templates/product.<suffix>.json`. (Online Store 2.0 product templates must be **JSON**, not `.liquid` — a `.liquid` product template silently falls back to the default.)

## Step 3 — Push the section files
`PUT` `sections/listicle-top.liquid` and `sections/listicle-bottom.liquid`. Each needs a `{% schema %}` block at the end:
```liquid
{% schema %}
{ "name": "Listicle Top", "settings": [], "presets": [{"name":"Listicle Top"}] }
{% endschema %}
```
`listicle-top` holds the full `<style>` block (colors, hero, items, mini-PDP styling for `#shopify-section-main`, hidden-chrome CSS) and the editorial markup through "Recommended For", ending with the `#buybox` anchor. `listicle-bottom` holds press → footer.

## Step 4 — Bind + verify
1. `PUT /products/<dupe_id>.json` with `{"product":{"id":<dupe_id>,"template_suffix":"<suffix>"}}`.
2. To flush the storefront's compiled-section cache, toggle the suffix off then on (`null` → `<suffix>`).
3. Verify on `/products/<handle>?view=<suffix>` (source-of-truth check is the Admin API, since the render lags):
   - `kaching-bundles-config` script present and `"productId": <dupe_id>`
   - a `<form action="/cart/add"` with the `main-product-atc` / `product-form__submit` button class (native ATC)
   - `id="buybox"` present and positioned before the `__main` section
   - `<cart-drawer>` / `#shopify-section-cart-drawer` present (NOT hidden by the chrome CSS)
4. Remind the user to **recreate the Kaching bundles** for the new product id in the Kaching dashboard (1-bottle / B2G1 / B3G2, etc.) — duplicating a product does not copy its Kaching config.

## Uploading images as theme assets
Base64 payloads exceed the shell arg limit — always upload from a Python script (`urllib`), not a `curl -d` one-liner:
```python
import base64, json, urllib.request
b64 = base64.b64encode(open(path,'rb').read()).decode()
urllib.request.urlopen(urllib.request.Request(
  f'https://{SHOP}/admin/api/2025-01/themes/{THEME}/assets.json',
  data=json.dumps({'asset':{'key':f'assets/{key}','attachment':b64}}).encode(),
  method='PUT', headers={'X-Shopify-Access-Token':TOKEN,'Content-Type':'application/json'}))
```
Public URL form: `https://cdn.shopify.com/s/files/<store>/t/<n>/assets/<key>`. In Liquid use `{{ '<key>' | asset_url }}`.

## Hidden-chrome CSS (paste into listicle-top `<style>`)
Hides header/footer/announcement/popups so the listicle reads like a standalone LP — but deliberately leaves the cart drawer alive:
```css
.shopify-section-header,.shopify-section-footer,
[id*='shopify-section-'][id*='__header'],[id*='shopify-section-'][id*='__footer'],
[id*='shopify-section-'][id*='__announcement'],[id*='shopify-section-'][id*='announcement-bar'],
#shopify-section-promo-popup,#shopify-section-scroll-to-top-btn,#shopify-section-global-music-player,
.site-header,.header,header.site-header,.site-footer,.footer,footer.site-footer,
#header-component,#footer-component,.announcement-bar,.promo-popup,
scroll-to-top-btn,global-music-player { display:none !important; }
body{padding-top:0!important;margin-top:0!important;}
main,#MainContent,[role="main"]{margin-top:0!important;padding-top:0!important;}
```
Note: NO `#shopify-section-cart-drawer` and NO bare `cart-drawer` in that list.
