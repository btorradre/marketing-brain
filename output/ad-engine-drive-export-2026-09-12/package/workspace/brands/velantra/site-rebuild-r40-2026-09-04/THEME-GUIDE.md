Velantra Quiet Luxury is a complete Shopify Online Store 2.0 theme with editable sections, product templates, collection pages, search, cart, articles, pages and contact form.

The working theme is **Velantra — R40 / Vivienne Craftsmanship**, ID **151364960321**, saved as an unpublished theme. The prior R40 theme, ID **151337074753**, was published by the merchant during the craftsmanship update. This working draft was duplicated from that current version, preserving its settings. Open the [theme editor](https://admin.shopify.com/store/uzdgxy-sb/themes/151364960321/editor) or [storefront preview](https://velantrafashion.com/?preview_theme_id=151364960321). Saving editor changes updates this draft; publishing is a separate action and has not been assumed.

**Open or install the theme**

For the installed draft, go to **Online Store → Themes**, find the theme above and open its editor. To install the supplied `velantra-quiet-luxury-theme.zip` as another draft, use **Draft themes → Import theme → Upload zip file → Choose File → Upload**. Upload the theme ZIP itself, not a ZIP of the entire project folder. Preview the resulting draft and use its editor to customize it. Shopify documents the [ZIP upload process here](https://help.shopify.com/en/manual/online-store/themes/adding-themes#upload-a-theme-file-from-your-computer).

**Customize the homepage**

Choose **Home page** in the editor's page selector. Drag sections in the sidebar to reorder them; add, hide or remove sections there. The supplied order is Hero film, Philosophy, Atelier statement, Signature model collection, Detail film, Leather timeline, Value breakdown, and closing statement. The Everyday Collection has been removed; the three model product cards are the homepage’s single shopping collection. Header and footer are separate groups.

| Change | Editor control |
| --- | --- |
| Main hero | **Hero film**: film, heading, text, link, desktop height, overlay, text color and video focal point. |
| Homepage copy | **Editorial statement** sections: eyebrow, heading, text, alignment, width and link. |
| Models carrying the three featured bags | **Featured model collection → Model product** blocks: select Vivienne, Weekender or Meridian; edit the model image, display title, alt text and optional variant ID. Reorder the blocks to change their order. Each image and title opens its product page. Choose **Contain** to preserve the full photograph, or **Cover** for a crop. |
| Leather timeline | **Leather timeline → Stage** blocks: edit each photograph, date or stage label, heading and description. Four columns on desktop become a horizontal scroll strip on mobile. |
| Material and design details | **Value breakdown**: edit the image, three table headings, each detail row and closing copy. |
| Detail video | **Detail film → Video**. The native Shopify-hosted Vivienne multishot film is selected. Change the video, cover, description, or vertical focal point here. Clearing Video displays the cover only. |
| Wordmark and navigation | **Header**: logo or wordmark, logo width and main navigation menu. The assigned **Velantra — Quiet Luxury navigation** menu contains All bags, Accessories, Track your order and Contact. Edit it under **Content → Menus**. All bags opens Handbags; tracking opens the existing tracking form directly. **Footer**: statement and menu blocks. |

The hero uses the first available source in this order: **Shopify video**, **MP4 video URL**, then **Use included Vivienne film**. The included film automatically switches between desktop and mobile versions. A custom Shopify video or MP4 URL uses one source at both sizes; adjust **Video focal point** if needed, for example `center center`.

For a custom MP4 URL, select **Poster / fallback image** as its loading image. For an image-only hero, clear both video fields, turn off **Use included Vivienne film**, and select a poster. The included film uses its bundled poster; a selected Shopify video uses Shopify's video preview image. Keep the video description meaningful for accessibility.

**Fonts, colors and spacing**

Open **Theme settings → Typography**. The supplied design uses bundled **Cormorant Garamond** headings and **Montserrat** body text. To use the font pickers, enable **Use custom fonts**, then choose **Body font** and **Heading font**. Turning this off restores the bundled pair.

**Theme settings → Colors** controls page background, text, dividers, secondary text and the studio image container background. The studio background setting does not recolor the backgrounds inside photographs. **Layout and brand** controls transparent homepage header, page width, section spacing, favicon and social links. Mobile spacing has its own responsive defaults.

**Product pages and preorders**

Choose **Products** and the appropriate template in the editor, then select the product to preview. Active handbag templates are `vivienne`, `delphine`, `juliette`, `colette`, `weekender`, `meridian-tote` and `boat-tote-2`. Both active Eleanor listings share `weekender`. Draft handbag templates are `straw-birkin`, `bow-tote`, `portico-bucket-bag`, `ingrid` and `boat-tote-legacy`. The Ingrid and three older Boat Tote listings have been assigned their dedicated templates and remain draft products. Template edits apply to every product using that template; they do not publish a draft product.

Product media galleries scroll left to right on desktop and mobile. Use the arrows, a horizontal trackpad gesture, keyboard arrow keys while the gallery is focused, or swipe on touchscreens. Each color keeps its own gallery; image zoom and the slide counter remain available.

Under **Product**, edit the display title, description override, subtitle, verified fact overrides, quantity selector, accelerated checkout, policy display and mobile purchase bar. Add or edit **Accordion** blocks for Details and Care, or **Text** and app blocks. An accordion can use rich text, an existing page, or both. A display title override changes the page heading; the underlying product title remains in checkout and search. A blank description override uses the catalog description. Vivienne has a draft-specific override describing its grained body and smoother contrasting trim.

Descriptions, prices, variants, inventory and original media come from **Products** in Shopify Admin. Shipping and return policy content comes from **Settings → Policies**. These are shared store records, so changing them can affect the live theme too. Use this draft's section fields for presentation changes that should remain within the draft.

**Compare-at prices:** In Shopify Admin, open **Products → a product → a variant → Pricing** and edit its **Compare-at price**. The draft shows a crossed-out compare-at price only when it is greater than the selling price. **Theme settings → Product prices → Show compare-at prices** controls display across product pages, product cards and the mobile purchase bar. Variant selection updates both prices. Products with no selling price continue to show Contact for availability.

**Checkout:** Both the cart drawer and cart page submit to Shopify’s native checkout. In the theme editor, checkout opens a new tab so it can load outside the embedded preview. On the storefront, it opens in the same tab. The drawer temporarily disables checkout while cart updates save. Same-origin Ajax cart requests run in order to prevent an app’s late cart-initialization response from replacing an already populated cart. Test with the storefront preview link above.

The authorized Weekender naming update applies to both `velantra-weekender` and `the-eleanor-weekender`: **Cognac** replaces Light Chocolate and **Espresso** replaces Dark Chocolate. Army Green and Black keep their names. The product-page Care accordion uses the same updated names.

**Theme settings → Preorders** has separate switches and editable messages for Vivienne, Colette and Eleanor Black. The supplied wording refers to October, early October, and mid September 2026 respectively; update it when fulfillment changes. Vivienne and Colette apply to all variants, while Eleanor's notice applies to the first option value `Black`. Dates are message text and do not expire automatically. These controls change notices and purchase labels; they do not change inventory availability, fulfillment dates or payment terms. Also update any dates written in catalog descriptions or a template's description override. Vivienne's description override currently includes its October preorder date.

**Studio catalog and future products**

**Theme settings → Studio catalog → Use included white studio product images** turns the theme's replacement images on or off. The complete replacement set contains **152 unique views covering all 185 original gallery positions across 13 product listings and 68 variants**. Every image was regenerated, visually reviewed, uploaded and mapped in this theme. Original product media is preserved. The replacements are used by this theme through an image-ID mapping, including product galleries, product cards, variant thumbnails and cart images.

That review compares each output with its selected source image. It does not certify physical dimensions, capacity, manufacturing specifications or the accuracy of an older catalog source. Product-specific measurement records distinguish nominal catalog or owner-approved dimensions from physically measured evidence. Use the [scale and fidelity protocol](../product-skills/SCALE-AND-FIDELITY.md) before adding size or fit claims. New craft panels and value-panel photographs are separate editorial assets; they do not replace the original gallery mappings.

For new products, upload photographs through Shopify's product Media area and associate variant images as usual. Unmapped media automatically displays the newly uploaded photograph; it is not automatically regenerated. Use a neutral white studio background when preparing new photography to keep the catalog consistent.

If a developer adds a new replacement only to this theme, they should add its reviewed WebP to `theme/assets/` and map the original Shopify image/media IDs in `theme/snippets/studio-image-url.liquid`, plus the variant map in `theme/snippets/studio-variant-map.liquid` for the AJAX cart. The source-to-output records live in `media/production-manifest.json` and `media/studio-image-map.json`. Replacing an original Shopify image can change its ID, so its theme mapping may need updating. The existing batch workflow is `media/build_delivery.py` followed by `scripts/integrate_media.py`; inspect their manifests before rebuilding. See `CATALOG-QA.md` for supplier details that still need confirmation.

When renaming a color, update its gallery alt-tag suffix too: the Weekender uses `#color_cognac`, `#color_army-green`, `#color_espresso` and `#color_black`. The gallery matches those tags to current variant names. A color rename does not require new studio assets or ID mappings. Historical source snapshots and production records retain the original color labels for provenance.

**Video ownership and editable sources**

The studio hero is AI-generated Vivienne footage, built from the September 3 Vivienne master product image with image generation and Google Gemini Omni 1.1 Flash animation. It is not a physical studio shoot. The detail film follows the R40 reference’s cut sequence using supported Vivienne detail views. The reference brand's photography and footage are not included in the delivered theme.

Original hero MP4s are in `video/exports/`; the accepted 21.67-second Vivienne detail film is in `video/detail-followup-2026-09-05/exports/v5/vivienne-detail-stage-3.mp4`. The detail film is hosted in Shopify Files as `velantra-vivienne-detail-film-2026-09-05.mp4`, with its original bytes preserved. The hero is generated directly by Google Omni at three seconds in native desktop and mobile aspect ratios. Its MP4 files are delivered without trimming, crossfades, timeline rendering or re-encoding. The homepage detail film uses a new multi-cut Omni sequence with provider-native extensions; the earlier ten-second macro is retained only as a historical source. First-frame posters support loading and reduced-motion playback. The detail film follows the reference’s wide desktop and narrower mobile crop, plays when visible, and offers a pause/play control. Reduced-motion visitors can start it manually.

Use GPT Image 2 for new image production and the internal video editor only for actual editing. HyperFrames is banned; its former project files are retired and are not part of the active workflow. Direct generation requests, provider outputs and validation are in `video/direct-omni/`, `video/README.md` and `video/manifest.json`. Rerunning `video/generate_studio.py` submits new paid Google generation. Existing exports require no AI service connection.

The timeline uses the owner-requested **Day 1** and **Day 4–8** labels. Finishing and final inspection use stage labels without importing R40’s additional manufacturing dates or certifications. The photographs are generated Vivienne detail studies, with source fidelity documented in `media/craftsmanship-followup-2026-09-05/`.

**Cart and shipping note:** The draft enables the store’s existing UpCart app embed. Header Cart and product additions open UpCart; the native theme cart remains a fallback when the app is unavailable. Product pages display “Free shipping over $75” below the purchase button without a policy link. This text does not change Shopify shipping-rate rules.

**Handbag product pages:** Each active handbag template now follows Product gallery and purchase details → Detail film → Craft / The Rhythm of Making (four cards) → Value breakdown → Complete The Look → Client Perspectives. Each active handbag family has its own selected film: Vivienne runs 21.67 seconds; Weekender, Meridian, Camille, Colette and Delphine run 18 seconds; Juliette uses a 9-second, five-shot film to preserve the referenced construction. Product-specific craft images are editable and show generated studies of visible materials and details, not documentary footage of manufacture. The six non-Vivienne timelines use material or stage labels without claiming manufacturing dates. Draft handbag editorial sections remain hidden until their own media and evidence are ready. The default and accessory templates remain separate.

**Client Perspectives:** Add your installed reviews app's native block in this section to supply real product reviews. No verified review feed has been connected for the active handbag families, so the current section honestly says that customer reviews are not available there yet. It does not contain invented quotes, ratings, counts or verification badges. The empty-state wording and visibility are editable. Historic fallback testimonials from the older theme were not migrated.

**Editor checkout:** UpCart checkout opens in a separate tab when Shopify design mode is active, preserving the editor preview. The standard storefront opens Shopify checkout normally. Verified with the design-mode flag simulated; access to the authenticated editor browser was unavailable.

The Detail film section also provides a Mobile height control (at a 390px viewport width): the homepage uses 340, the Weekender uses 360 so its broad outer panels stay visible, and other handbag pages use 420. The width scales with the viewport. Native Shopify video and cover pickers remain editable.

The longer detail films are stored in Shopify Files because native Shopify videos provide the storefront playback sources. The theme ZIP contains their section settings and cover images. On this same store, those settings resolve the existing video files. To move the theme to a different Shopify store, upload the accepted MP4 originals listed in the video delivery manifests, then select each file in its Detail film section. The three-second homepage hero clips remain bundled theme assets.

All seven installed native detail videos, their exact Shopify filenames, download URLs and approved local originals are listed in [video/shopify-detail-films.json](video/shopify-detail-films.json). Each original CDN file was checked against its unchanged provider output.
