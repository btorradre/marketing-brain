# Native Elixir blocks & behaviors (no custom code)

Everything here is edited via `settings`/block settings in `templates/product.json`,
`config/settings_data.json`, or section files — **never** by replacing files or touching the
bundler/buy button.

## Above-the-fold buy box — `shop-product-details` section
Repopulate these native blocks (find them in `templates/product.json` → the
`shop_product_details_*` section's `blocks`). Map copy from the research/`copy.json`:

| block type | what to set |
|---|---|
| `reviews` | `rating_text_content` → "Rated 4.8 'Excellent' \| 2,247+ Reviews" |
| `title` | `custom_title` → product H1; `font_size` ~40 |
| `custom_text` (subtitle) | `text` → 1-sentence promise with †; `text_color` → `MUTED` |
| `bullet_list` | 4 benefit bullets (organ → benefit†) |
| `benefits_grid` | 4 short benefit labels |
| `guarantee_badges` | "90-Day Guarantee"; `text_color` INK, `icon_color` BRAND |
| `add_to_cart` | `button_behavior` → `skip_to_checkout`; `buy_box_button_bg_color` → BRAND; text `#fff` |
| `product_tabs` → swap for `custom_liquid` accordions (Description / The Results / Shipping & Returns) |

**Add `custom_liquid` blocks (allowed — they're not the bundler), ordered:**
`add_to_cart → [checkmarks] → [trust strip] → [guarantee box] → [accordions]`
- Checkmarks: 3 objection-killers from research (zero-X / format / shipping).
- Trust strip: `{% for type in shop.enabled_payment_types %}{{ type | payment_type_svg_tag }}{% endfor %}`.
- All `custom_liquid` blocks use `width:100%` (the wrapper centers/shrink-wraps otherwise).

**Never edit:** the `quantity_break` / bundle app block, or `add_to_cart` logic (only its color + behavior).
Set the section bg white and the buy-column text dark.

## Section order (product template)
`shop_product_details → sticky_add_to_cart → rv_faq(top) → rv_feeling_worse → rv_core →
rv_stages → rv_compare → rv_timeline → rv_results → rv_reviews → rv_faq`

## Global behaviors
- **Home → PDP redirect** (`layout/theme.liquid`, right after `<head>`):
  `{%- if request.page_type == "index" and request.design_mode == false -%}<meta http-equiv="refresh" content="0; url=/products/HANDLE"><script>location.replace("/products/HANDLE")</script>{%- endif -%}`
- **Logo non-clickable**: add to header a scoped `{% style %}` → `.header-wrapper .header__heading-link{pointer-events:none !important;cursor:default !important;}`
- **Cart drawer readability**: override CSS vars on `.gb-cart-drawer-lb,.cart-drawer{--cart-drawer-background-gradient:none!important;--cart-drawer-primary-background-color:OFF!important;--cart-drawer-primary-text-color:INK!important;}`; recolor `.discounts__discount` → BRAND bg + white text; the shipping-protection text inherits white from a parent, so set an **inline** `style="color:INK"` on `.gb-shipping-protection-icontext`. Disable the social-proof banner by emptying `snippets/cart-social_proof_bar.liquid`.

## Footer + policy pages
- Custom `rv-footer` section → point `sections/footer-group.json` at it (logo, `help@DOMAIN`, link columns, **FDA disclaimer**).
- Create pages via `shopify_api.py page`: privacy-policy, refund-policy, shipping-policy, terms-of-service, cancellation-policy.

## Compliance (from research "never say" list)
Use supports/helps, never cures/treats/reverses. Disclose sweeteners openly. Keep the high-risk
emotional claims off the buy box. Always append the FDA disclaimer in the footer + timeline.
