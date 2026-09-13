# Shopify mechanics

## Auth

Client-credentials token exchange from `marketing brain/.env`, minted per process, never
written to disk. `scripts/shop.py` handles it: `shop.context("velantra")` returns
`{store, token, theme_id, api}`.

Brands available: `VELANTRA`, `MOTILLI_1`, `MOTILLI_2`, `LUNESSA`, `SOLORNA`, `WEND`.
Velantra resolves to `uzdgxy-sb.myshopify.com` (velantrafashion.com). Scopes are near-total
including `write_theme_code`, so this path can edit the live theme, which the claude.ai
Shopify connector cannot.

**Everything goes through curl.** `urllib` in this environment has no CA bundle
(`CERTIFICATE_VERIFY_FAILED`) and has been seen to hang on Shopify GraphQL. Do not
reintroduce it, and do not paper over it with `SSL_CERT_FILE` exports.

## Theme

- **Never hardcode a theme id.** Velantra republishes themes; the live one was
  148370161729, then 150684762177. `shop.main_theme_id()` reads the `main`-role theme
  every run. A template pushed to the wrong theme is invisible and looks like a bug
  somewhere else.
- Theme asset reads need the bracket param URL-encoded (`asset%5Bkey%5D=...`) or curl
  rejects the URL as a bad range.
- **Each product has its own template suffix.** `templates/product.weekender.json`,
  `templates/product.straw-birkin.json`, `templates/product.delphine.json`. Editing
  `templates/product.json` does nothing to any of them.
- **The `custom` block sanitises its `code` setting** — `<style>`, `<details>`, `<summary>`
  and unknown tags are stripped. Rich HTML ships as a real theme snippet
  (`{% render 'name' %}`), which is not sanitised and has `product` in scope. The same
  applies to `advanced-content` → `liquid` sub-blocks.
- Block rendering for main-product lives in `snippets/product-template.liquid`, not the
  section file.

## Donor templates

`python3 scripts/build_pdp.py --list-donors` reads the published theme. Current shapes:

| Donor | Use for |
|---|---|
| `weekender` | Structured leather and canvas, flap closure. The most current house layout. |
| `straw-birkin` | Woven and straw bodies. |
| `delphine` | Top-handle leather. |
| `meridian-tote` | Open-top structured tote. |

The donor decides which sections exist. `build_pdp.py` fills what is there and reports
what the donor lacks. It also blanks every `shopify://` and `/cdn/shop/` image reference,
because those are the donor's photos and they will otherwise show on the new PDP.

Section `disabled` flags carry over from the donor. Flip them per product with
`spec.pdp.sections_enabled`.

## Product creation

`productSet` with `synchronous: true`, one `Color` option, one variant per colorway. Never
`productDuplicate` (house law). Always `status: DRAFT`.

`inventoryPolicy: CONTINUE` on every variant: Velantra runs negative oversell counters, and
pre-orders depend on it. It is also why a pre-order colorway is invisible in the buy box
unless the PDP says so in words.

## Media

The sequence, and every step matters:

1. `stagedUploadsCreate` → POST the file to the returned target with curl → use
   `resourceUrl` as `originalSource`.
2. `productCreateMedia` in batches of 10, each with its `alt` already carrying the
   `#color_<handle>` tag.
3. **Wait for every media to reach `READY`.** Reordering before that silently misfires.
4. `productReorderMedia` with a full move list, matching media by alt.
5. `productVariantAppendMedia` to set each variant's featured image.

### The tag

```
"<Title> in <Colorway>, <angle> #color_<handleized-colorway>"
```

Impulse PDP templates filter the gallery on that suffix. Untagged media renders on **every**
colorway at its raw global position. Shared shots are attached once **per colorway**, each
with its own tag. Never share one attachment across colorways.

## Caching

- **Product pages**: Shopify's full-page cache can serve a stale PDP for 10 to 15 minutes,
  and `?cb=` query params do **not** bust it. Verify against the Admin API or the source
  metafield, never against the rendered page.
- **Pages** (`/pages/...`) update instantly. Different cache. Do not generalise from one to
  the other.
- Storefront CDN lags admin media changes by roughly 10 minutes.

## Collections and channels

`assign.py --collections handbags` joins by handle. `--channels` publishes to every sales
channel. The `handbags` collection uses `templates/collection.luxe.json`, whose per-card
sale badge defaults to "End of Summer Sale" and renders on any product where
`compare_at > price` — invisible while compare-at is cleared, back the moment it is
restored. **Re-check the badge after any pricing change.**

## Sanity commands

```bash
python3 scripts/shop.py context velantra                              # store, live theme, token ok
python3 scripts/shop.py templates velantra                            # every product template
python3 scripts/shop.py theme-get velantra templates/product.weekender.json
python3 scripts/build_pdp.py --list-donors
```
