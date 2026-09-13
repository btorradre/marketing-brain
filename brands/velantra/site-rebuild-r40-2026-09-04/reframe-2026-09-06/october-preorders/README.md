# October preorders

User confirmed Colette and Vivienne arrive in October. Updated unpublished draft 151389143105 for every color of both products. Customer-facing message: “Pre-order — all colors expected to arrive in October 2026. Orders dispatch after stock arrives; delivery time is additional.” This describes stock arrival without promising a customer delivery date or an early-October date.

Updated the global preorder messages and enabled flags, matching theme-editor defaults and locale fallbacks, and both product templates' lead-time fields and shipping accordions. Conflicting 10-day dispatch copy is removed from those two PDPs. The cart page and native cart drawer use the same global messages. No product inventory or checkout settings changed; detail films remain removed.

All five files passed theme validation and exact semantic Shopify readback. All color selections passed desktop and mobile checks for the October notice, lead-time row, preorder buttons and absence of 10-day wording. Shipping accordion copy and mobile width also passed. Interactive cart verification was blocked by HTTP 429 on the isolated test-cart add request; no checkout was attempted. See qa.json for the validation scope.

The local proposed shipping policy now includes the Colette/Vivienne preorder exception; that policy is not applied because the connector lacks write_legal_policies. Theme remains UNPUBLISHED and needs manual publication under the connector's existing safety restriction.
