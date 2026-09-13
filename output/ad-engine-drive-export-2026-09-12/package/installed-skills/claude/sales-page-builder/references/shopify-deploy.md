# Shopify deploy — native buy box, standalone page

## Why a theme template, not a content Page
A Shopify content Page can't render a product form — `{{ page.content }}` isn't Liquid-
evaluated, so it can't host the native buy box. To get a WORKING buy box (variant +
bundle app + add-to-cart) the page must be a **theme template made of sections**. This
skill uses the Elixir theme's native `shop-product-details` section (which already wires
the merchant's bundle app, e.g. Kaching, + `add_to_cart`) and drops the custom advertorial
sections above and below it.

## Auth (Admin API, custom app)
The Shopify CLI is usually NOT authorized for these stores. Use the Admin API with a
`client_credentials` grant. Ask the user for the custom app's **client_id + client_secret**,
then mint a short-lived `shpat_` token:

```bash
curl -s -X POST "https://<shop>.myshopify.com/admin/oauth/access_token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials" -d "client_id=<id>" -d "client_secret=<secret>" \
| python3 -c "import sys,json;open('/tmp/sp_tok','w').write(json.load(sys.stdin)['access_token'])"
```

Never write the token or secret into a committed file. Read it from `/tmp/sp_tok` and
**delete `/tmp/sp_tok` when finished** (`shred -u /tmp/sp_tok`). Re-mint when needed.

## Discover the store (do this before deploying)
- `GET /admin/api/2024-10/themes.json` → the `role:main` theme id (THEME_ID).
- `GET /admin/api/2024-10/products.json` → the product handle to bind the buy box to.
  Reuse a product that already has a **bundle deal configured** (the tiers come from the
  app, not from Shopify variants) — bind via the section's `current_product`.
- `GET themes/<id>/assets.json?asset[key]=templates/product.json` → confirm it has a
  `shop-product-details` section with the bundle app block + `add_to_cart`. That's the buy
  box you clone.

## Pipeline (the scripts do this; edit each script's CONFIG block first)
1. `upload_files.py` — images → Shopify Files → `/tmp/sp_cdn.json` (keyed by local filename).
2. `generate_sections.py` — split the page at the buy-box slot → `sp-<slug>-top/bottom.liquid`,
   inline the CDN urls. CSS is scoped under `#rv-adv` so it can't collide with the theme.
3. `deploy_theme.py` — PUT the two sections + build `templates/product.<slug>.json`
   = `[ top, native buy box, bottom ]`, retune buy-box copy, bind `current_product`.
   Preview safely (no disruption to the live product page) at
   `/products/<handle>?view=<slug>`.
4. `deploy_page.py` — clone that into `templates/page.<slug>.json` + create a published,
   **unlinked** Page → `/pages/<handle>`. This is the standalone URL.

## Gotchas (learned the hard way)
- **Full-page cache lag:** after a section PUT, the storefront serves the old HTML for
  ~10-20s. A cache-buster query string does NOT bust it. Touch the page record
  (`PUT /pages/<id>.json` with `body_html:""`) to invalidate, then poll the live URL until
  your new marker appears.
- **Verify on the live URL, not a saved snapshot.** The bundle widget is injected by the
  app's JS — it renders blank in a saved-HTML file but fine on the real URL. Grep the live
  HTML for `kaching` / `ADD TO CART` / `/cart/add` to confirm the buy box is intact.
- **Files keeps the local filename you key by** even if it stores a `.jpeg` as `.jpg`
  (`upload_files.py` already keys the map by the name your HTML references, so inlined
  URLs stay correct).
- **Keep the theme header + footer** (don't hide store chrome) so the cart actually works.
- Flipping the product's own template (`template_suffix=<slug>`) makes the page the
  product's default at `/products/<handle>` — only do that if the user asks; it's reversible.
