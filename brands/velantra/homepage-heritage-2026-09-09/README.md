# Velantra heritage homepage

The first variation is installed and verified as unpublished Shopify theme **151519330369**, “Velantra — Heritage Homepage · Sep 9.”

[Open homepage preview](https://velantrafashion.com/?preview_theme_id=151519330369)

## What is built

A complete replacement homepage within the draft: Vivienne opening campaign, Colette autumn campaign, The World of Velantra with Vivienne and Black Eleanor cards, Horse Charm accessories campaign, closing brand passage, native newsletter and footer. Five GPT Image 2 outputs plus the existing approved Vivienne master. Editable sections, text, images, focal positions and shopping links are in Shopify's theme editor.

Desktop uses a cream header above immersive campaigns. Mobile uses the dedicated portrait opening and separate copy panels for subsequent campaigns. Tablet preserves the full landscape opening and uses separate copy panels. The header stays available on scroll. The source homepage and original shared theme files are retained in `before/`; intermediate layout revisions are in `resumed-before/`.

## Recovered and finished September 9

The previous chat ended during QA. Recovered its saved transcript and draft, corrected tests to follow UpCart's offscreen closed state, waited for product page scripts before quantity interaction, and fixed the header and tablet image crops. Deployed only the two changed layout files to the existing draft and verified their readback.

## Verification

- Theme validation passes for all seven authored files; latest layout revision 6 passes.
- Browser checks pass at 1440 × 1000, 768 × 1024 and 390 × 844.
- One H1, all five page images load, no horizontal overflow and no page JavaScript errors in those checks.
- Desktop search dialog, mobile/tablet navigation, sticky header, and UpCart open/close work.
- Newsletter email and consent fields remain required; no signup submitted.
- All five distinct shopping destinations return HTTP 200 with expected page headings.
- The opening product link selects Chocolate Vivienne variant 44462686830657. Quantity increment to 2 and add-to-cart verified; isolated test cart cleared. No checkout or order placed.
- Brown Horse Charm retains the color-only gallery behavior.
- Final desktop, tablet and mobile screenshots inspected; complete featured products visible in the reviewed campaign frames.

Evidence: `qa/report.json`, `qa/link-checks.json`, `qa/final-*.png`, `research/resumed-theme-validation.txt`, `research/resumed-layout-validation.txt`, `deployment.json`, and `readback/`.

## Remaining reference dependency

This is a functioning heritage-inspired variation, not a verified one-to-one Ralph Lauren reproduction. The original reference's visual layout was blocked by a human-verification challenge; the resumed text fetch redirected to a regional page. A full-page screenshot of the user's intended desktop/mobile reference is needed to match exact layout, dimensions, crops and pacing. No Ralph Lauren photography or logo is used. Product image provenance and unverified physical scale are documented in `media/PROVENANCE.md`.

The draft is unpublished. The live homepage remains the source version.


## Hero revision 2 — Kie.ai GPT Image 2.5

The opening now uses the user's seated-on-stone-steps photo as the scene/style reference, with the Chocolate Vivienne master defining the bag. Desktop and portrait images were generated through Kie.ai's `gpt-image-2-5-sunburst-image-to-image`, as explicitly requested. The initial country-house hero is retained as a prior version. Mobile copy is below the portrait to keep the complete bag visible. Production plan, final prompts, provenance, task receipts, validation and browser checks: `edit/hero-steps-v2/`.

## Sitewide branding — September 9

The homepage's cream/navy header, navigation, newsletter and footer are now shared across the draft storefront. All product templates, collection/search cards, product stories, cart/UpCart, contact, tracking, policies and other theme content use the same typography and styling. Product/variant/gallery logic and the exact 2720×1530 hero are preserved. Verified 13 published products, 65 color selections and 58 page/viewport combinations, plus desktop/mobile purchase flow. Plan, backups, validation, deployment hashes and screenshots: `sitewide-branding-2026-09-09/`. This supersedes the earlier homepage-only scope; the draft remains unpublished.

## Black palette — September 9

Replaced the navy branding color with pure black (#000000) sitewide, including homepage panels, text, footer, buttons and UpCart. Cream and imagery are unchanged. See `black-palette-2026-09-09/` for validation, backups, deployment and browser verification. This supersedes the previous navy palette.

The theme was published externally during the black-palette task. The palette change was applied to the now-live theme 151519330369 after confirming none of the six edited files had changed since backup.

## Navy restored — September 9

Per user request, reverted the black palette to the exact prior navy (#132039) across all six affected files on live theme 151519330369. Readback matches the saved navy versions. Homepage/mobile and product/desktop color checks passed. Evidence: `navy-restored-2026-09-09/`.
