# Accessory color galleries — September 9, 2026

Deployed and read back on live theme **151389143105**, Velantra — Detail Film Cleanup · Sep 6.

The Horse Charm's unassigned teal loop image (media 27691808260161) appeared in every color gallery, including Brown. The Cherry Charm's unassigned red spherical image (media 27716584243265) likewise appeared under all colors. The shared gallery intentionally treated unassigned media as common to every variant, which was inappropriate for these product-specific packshots.

Added the product-section setting `hide_unassigned_media`, enabled for Horse Charm, Cherry Charm, Bag Scarf and Boat Tote Keychain. For those templates, Liquid excludes unassigned media when the product has a Color/Colour option. Color switching also avoids falling back to other colors when a matching image is absent. Existing variant image assignments and catalog media are preserved. Other templates retain their existing treatment of shared images, including handbag diagrams and the size-only Bag Organizer.

The current Verdant variant is assigned a brown horse with a gold clasp; the teal loop horse is unassigned. The current Cherry Red variant is assigned padded stitched cherries; the spherical red cherry is unassigned. These pre-existing construction/name discrepancies are documented in the dedicated product skills. This repair excludes orphan media without guessing different SKU bindings, renaming variants, or altering photographs.

The quantity-selector fix from `../quantity-fix-2026-09-09/` was already live at intake. It remains enabled and was rechecked here. The main-product patch preserves its controls and cart behavior.

Validation and live QA:

- All seven changed theme files passed Shopify Liquid/theme validation and Shopify readback comparison. JSON was compared structurally because Shopify reformats JSON on save.
- All 13 published products passed desktop (1440px) and mobile (390px) checks for visible quantity input, default quantity one and no horizontal overflow: 26 page checks.
- All 25 accessory colors passed at both widths: 50 gallery checks. Each selected variant's assigned image loaded; no orphan horse/cherry image was present. Horse and Cherry image zoom opened and closed correctly.
- Quantity increase/decrease, minimum one, direct numeric input, zero normalization and preservation through color changes passed at both widths. Adding two Dark Brown Horse Charms produced the correct variant and quantity two in the cart. Test carts were cleared; no orders were placed. No JavaScript page errors occurred.
- Desktop and mobile Horse screenshots were visually reviewed against the approved variant-reference mappings. No physical scale claim is made.

Files: `before/` is the original live backup, `after/` is the proposed/deployed source, `readback/` contains Shopify's saved files, and `deployment.json` records hashes. `browser-qa.json`, `qa.py`, `validation.txt` and screenshots contain verification evidence. The canonical `../theme/` received the same focused changes, preserving its other content; its originals are in `local-before/`.

Rollback: after checking for subsequent edits, restore the seven affected files from `before/` to the recorded theme. That backup includes the working quantity selector, so rolling back this gallery repair will not remove it. Alternatively turn off “Show only color-assigned gallery media” in the four accessory product templates to restore their prior gallery behavior.
