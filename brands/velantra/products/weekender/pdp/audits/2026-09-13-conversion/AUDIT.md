# Weekender: ad-to-PDP conversion audit

September 13, 2026. Campaign `6998265963075` in Meta account `28754886360776091`; Shopify store Velantra. Diagnosis only; no live ad, theme, product, inventory or policy changes.

**There are real inconsistencies. The strongest is product identity: the bag demonstrated in the ads has different construction details from the bag in the current PDP gallery. The offer also promises three sizes that cannot be selected, and the shipping expectations change after the click.** These are plausible reasons for hesitation; their individual conversion effects have not been measured.

The page is not failing to convert entirely. This young campaign has one attributed purchase. A synthetic Cognac add-to-cart succeeded, and following its checkout link loaded the checkout at $159.99. Payment and address-dependent shipping rates were not tested.

## What the numbers establish

Meta data retrieved at approximately 16:46 UTC, September 13. Campaign started September 12 at 21:40 America/Los_Angeles, roughly 12 hours before this snapshot. The supplied September 13–14 range contains only partial September 13 activity; September 14 had not happened.

| Metric | Since campaign launch, Sep 12–13 | Supplied Sep 13–14 window so far |
|---|---:|---:|
| Spend | $119.80 | $100.68 |
| Impressions | 1,096 | 865 |
| All clicks | 69 | 62 |
| Link/outbound clicks | 58 | 51 |
| Landing-page views | 49 | 44 |
| Pixel add-to-cart events | 7 | 6 |
| Pixel checkout initiations | 2 | 2 |
| Pixel purchases | 1 | 1 |
| Attributed purchase value | $159.99 | $159.99 |

Since-launch link CTR is 5.29%, link CPC $2.07, CPM $109.31, and attributed ROAS 1.34. There is click interest, but that does not establish profitable traffic: acquisition is expensive and there is only one purchase. The active revised Haaland ad received that purchase; five attributed landing-page views are much too few to declare it a winner.

Meta uses the ad sets' unified attribution settings: seven-day click, one-day view and one-day engaged-video. Actions and landing-page views are not a strict session funnel; repeated and attributed events must not be treated as unique shoppers.

Shopify provides a separate session-based view of the canonical PDP, across **all traffic**, September 7–13 partial:

**205 landing sessions → 11 sessions with a cart addition → 5 reaching checkout → 3 completing checkout.** Conversion is 1.46%; add-to-cart rate 5.37%. Mobile accounts for 158 sessions, or 77%. Most sessions do not reach the cart, so product recognition, desire and purchase confidence deserve attention before assuming checkout failure. These sessions can include prior page versions and are not a controlled measurement of today's design or this campaign alone.

Sources: [Meta daily totals](meta-daily-30d.json), [selected window](meta-selected-window.json), [Shopify daily sessions](shopify-weekender-daily-30d.json), [device breakdown](shopify-weekender-devices-7d.json). Meta's timezone is Los Angeles; Shopify's is New York. Counts should not be forced into one attribution model.

## Confirmed discrepancies and gaps

### 1. The product looks different after the click — highest priority

The old-money product demonstration at 22.5 seconds shows a **horizontal oval fitting and contoured flap with handle cutouts**. The current Cognac hero shows a **vertical oval fitting, different flap shape, and different side fittings/strap treatment**. The current gallery's interior is cream/fabric-looking; the chic ad describes and demonstrates a caramel interior. The live PDP's own lower craft copy describes a horizontal fitting while its hero shows a vertical one.

The owner's August 8 physical-product photographs support the horizontal fitting, contoured flap and smooth caramel interior. The dedicated Weekender product reference records the older generated gallery's deviations. That dated sample is strong comparison evidence, but it does not certify every unit shipping today or its measured dimensions.

**Likely shopper effect:** uncertainty about which bag will arrive. This is more consequential than a different background or color grade.

**Correction:** establish the current physical SKU as the source of truth, then make the ad, hero, close-ups, interior, color variants and cart thumbnail depict that same construction. Preserve aspirational styling using accurate product imagery.

[Side-by-side evidence](ad-vs-pdp-construction.jpg) · [Current Cognac gallery](cognac-gallery-contact.jpg) · [Ad product frame](ads/old-money-hardware.png) · [Physical interior reference](../../../product-references/real-product-2026-08-08/LC-open-interior-slip-pocket.jpg)

### 2. All eight ad texts promise three sizes; the product has one

The identical primary text across all eight campaign ads says the bag comes in three sizes. Shopify exposes only a Color option with Cognac, Army Green, Espresso and Black. The PDP describes one nominal size, 18 × 14.5 × 7 inches, and has no size selector. Seven ads are active; the eighth is currently disapproved but has historical delivery.

**Likely shopper effect:** visitors looking for a smaller/larger bag cannot find what the ad offered and may suspect missing options or a wrong landing page.

**Correction:** remove the three-size claim from the ad copy. Describe one size and four colors only if that remains the actual offer. Do not manufacture new size options to match erroneous copy.

Sources: [live ad creative metadata](meta-ads.json), [Shopify canonical product](product-7971794747457.json), [visible PDP text](mobile-visible-text.txt).

### 3. Shipping and availability promises conflict

The chic ad says Black ships in mid-September at approximately 43.5–45.6 seconds. European travel ad 2 makes the same promise around 46.9–49.8 seconds. Its closing page recording says the other three colors are in stock and ship now.

The current PDP says ten days before dispatch, including the default Cognac view. Selecting Black adds an explicit preorder message with transit time additional. Meanwhile, the shipping policy gives a general processing period of one to two business days, then seven to ten business days in transit, without clearly reconciling this product's longer lead time.

**Likely shopper effect:** a person buying for an upcoming trip loses confidence that the bag will arrive in time.

**Correction:** use one truthful, color-specific dispatch estimate and a separate delivery estimate. Reconcile the ad, page, policy and any cart messaging. Do not promise mid-September or immediate shipping unless operations can meet it.

[Shipping promise inside the European ad](ads/europe-old-page.png) · [Black selection evidence](color-diagnostic-black.png) · [Shipping policy](https://velantrafashion.com/policies/shipping-policy)

### 4. The ads show an older purchase page and different color names

The chic ad's closing screen recording, around 47 seconds, shows the older title, illustrated color selection, fit/function benefits and purchase reassurance. European travel ad 2 also records that older page. Light Chocolate and Dark Chocolate in those recordings are now Cognac and Espresso. The current title is shortened to Eleanor and the layout/content hierarchy is substantially different.

The sale price is consistent at $159.99 against $209.99 where shown; this is not evidence of a price bait-and-switch. A color rename alone is a smaller issue, but combined with changed bag construction it weakens recognition.

**Correction:** refresh page footage after the product and offer are corrected; use consistent names across creative, landing page and cart.

[Old purchase page in the chic ad](ads/chic-old-page.png) · [Current first mobile screen](mobile-initial.png)

### 5. Premium specifications and selling points are not carried through clearly

Chic and European travel ad 2 assert full-grain leather and solid/real brass, and emphasize three-day packing and overhead-bin use. Chic specifically sells the caramel interior and slip pocket. The current purchase section emphasizes canvas, vegetable-tanned leather, craftsmanship and atmospheric travel prose; its lower hardware description specifies color rather than metal composition.

Full-grain and vegetable-tanned are **not mutually exclusive**: they describe different properties. The finding is a specification/proof gap, not proof of fake leather or non-brass hardware. Material grade, origin, metallurgy, durability and universal airline fit cannot be certified from these photographs.

**Correction:** substantiate each specific claim, carry supported benefits into a concise buying section, and remove or qualify unsupported claims in the ads. For old-money and European styling traffic, lead with how the accurate bag elevates an outfit, supported by useful capacity/fit demonstrations. The page does have on-body photos; they are not missing altogether.

## Additional page friction

At the tested 390 × 844 mobile viewport, the main purchase button begins approximately **1,465 pixels below the page top**. The first screen is dominated by the gallery; facts and a long descriptive paragraph sit before colors and purchase. There is no visible purchase button in the initial viewport. A sticky purchase element exists in the theme, so this is not a claim that no sticky functionality exists anywhere.

The page explicitly presents an empty customer-review section. Its two-year defect replacement warranty exists in the refund policy but is not prominent beside the main purchase action. Lower craft content remains Army Green-specific when another color is selected; it is labeled Army Green, but does not reinforce the chosen variant.

**Recommended test:** shorten the initial mobile gallery/spacing, put title, price, color and purchase action together, and show accurate delivery, returns and warranty reassurance nearby. Lead supporting imagery with desirable outfits and the actual product; add authentic customer evidence when available. Do not invent testimonials or hide a genuine preorder delay.

[Button position and browser measurements](mobile-initial-audit.json) · [Initial mobile view](mobile-initial.png) · [Refund/warranty policy](https://velantrafashion.com/policies/refund-policy)

## Functional checks and limits

- All four color controls changed selection and variant URL. Purchase remained enabled; Black correctly changed the button to Pre-order. Negative Shopify stock quantities do not establish a sold-out blocker because selling past zero is enabled.
- A synthetic Cognac add returned HTTP 200 and displayed one bag at $159.99 in the live cart. Following the cart's actual checkout link loaded the contact/delivery/payment page at the same product amount. No personal information, payment or order was submitted; final shipping/tax and payment processing remain untested.
- A preliminary automation attempt looked for the theme's fallback checkout button, while the visible cart was provided by UpCart. That locator failure was a test assumption, not a demonstrated storefront defect. The subsequent visual and checkout checks succeeded.
- Several isolated browser visits and up to two synthetic cart additions occurred after the analytics snapshot, including a logged add test at 17:01 UTC and checkout navigation at 17:02 UTC. Subsequent live analytics may contain these audit events. The metrics above were collected before the cart tests.
- The page loaded and no page JavaScript exception was captured in the controlled tests. A fast desktop connection emulating mobile is not a real-device field speed study. No claim is made about all browsers, payment methods or destinations.

[Cart screenshot](cart-test-after.png) · [Cart response receipt](cart-observation.json) · [Checkout screenshot](mobile-checkout.png) · [Checkout receipt](checkout-link-test.json) · [All color checks](color-diagnosis.json)

## Campaign coverage and next action

| Ad set | Spend | Landing-page views | Cart events | Checkout events | Purchases |
|---|---:|---:|---:|---:|---:|
| European travel | $11.00 | 3 | 0 | 0 | 0 |
| Chic travel bag | $45.18 | 9 | 1 | 0 | 0 |
| Old money | $45.33 | 24 | 3 | 0 | 0 |
| Haaland | $18.29 | 13 | 3 | 2 | 1 |

Reviewed actual Meta creative metadata for all eight ads and transcribed their downloaded, Meta-served video files. Visual findings use chronological sampled frames and targeted product/CTA frames; this is not an exhaustive frame-by-frame editing audit. Exact ad IDs, media, transcripts and frames are retained in this directory. The disapproved older Haaland ad contains a different celebrity association/material-origin script; do not attribute those claims to the active revised Haaland narration or copy them into the PDP.

All eight CTA links point to the canonical `/products/velantra-weekender` page. A duplicate `/products/the-eleanor-weekender` product exists, but it is not the destination of these eight ads. No explicit creative URL tags were present; adding stable ad-ID UTMs would improve future session analysis, without replacing Meta attribution.

**Fix order:** (1) accurate, matching product imagery; (2) remove the false size offer and reconcile shipping; (3) compact mobile purchasing with supported proof/reassurance; (4) update old page footage and names. Then measure add-to-cart and purchase rates by device/source with versioned landing-page exposure. The present data does not isolate which mismatch caused lost sales, and the current sample cannot establish that the ads are otherwise commercially successful.

These campaign findings are reference observations, not exact-export performance bindings or a formal creative winner/loser decision. No ad launch, store publication or pricing change was performed.
