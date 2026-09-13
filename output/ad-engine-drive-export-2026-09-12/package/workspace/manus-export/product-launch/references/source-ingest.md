# Reading the link

## The ladder

Try, in order, and take the first that resolves a product:

1. **Shopify product JSON** — `<url>.json` then `<url>.js`. Most DTC brands. Gives title, full description HTML, price, options, every variant, and every image at full resolution. Best case by a wide margin.
2. **JSON-LD** `schema.org/Product` embedded in the page. Marketplaces, BigCommerce, WooCommerce, most modern Next.js-style storefronts.
3. **OpenGraph plus `<img>` harvest.** Last resort, noisy, but usually gets the hero images.

Thumbnail URLs should be rewritten toward the original file (e.g. Shopify `_800x.`, a marketplace's `_720x720`, Cloudinary `w_400`), so the downloads are full resolution rather than gallery crops.

## When it is bot-blocked

Watch for a loud warning sign: the resolved page title looks like `404`, `Not Found`, `Access Denied`, or `Just a moment` (a Cloudflare challenge page). Do not trust anything scraped after that.

Fallback, in order:

1. **Re-check the URL.** Most failures are a wrong or region-redirected path.
2. **Browser automation.** Load the page with a browser-automation tool, take a snapshot to read the page, and evaluate a script to pull the image list directly out of the DOM:

   ```js
   () => [...document.querySelectorAll('img')]
     .map(i => i.currentSrc || i.src)
     .filter(u => u && !/sprite|icon|logo|\.svg/i.test(u))
   ```

   Then download those URLs into your source images folder.
3. **Ask the supplier for the photos.** If you're sourcing from a supplier, they usually have a better set than the public listing anyway, and supplier photos carry the real hardware more accurately.

## What to read off the photos

The JSON gives you the listing. The photos give you the product. Open them and answer these, because every one of them ends up in a prompt and none of them can be guessed:

- **Silhouette and proportion.** Wider than tall or taller than wide? Structured or slouchy?
- **Opening mechanism.** How does it actually open? Flap folding all the way over, zip, drawstring, magnetic, open top? This is the single most-failed detail in generation and it needs prompt-ready language, not a noun.
- **Hardware.** Metal colour, and the exact count and placement of every piece. Image generation models duplicate hardware and invent studs whenever the prompt is vague about what carries what.
- **Handles.** Rolled or flat, and the drop. The drop decides carry truth: short rolled handles are hand or forearm only, and if you script a shoulder carry the engine invents a strap to bridge the impossible pose.
- **Interior.** Lining material and colour, pockets. Written descriptions get this wrong more often than any other field, and a wrong lining fails every open-bag frame.
- **Base and corners.** Feet, corner patches, reinforcement.
- **Branding.** Confirm whether there's any visible branding/logo. If not, keep the no-lettering negative instruction in prompts.
- **Texture per colorway.** Weave density and material finish genuinely differ between colorways of the same product.
- **Scale.** Anything in frame that gives real size context: a hand, a shoulder, another object of known size.

Write the answers into a running product-truth document as you go, and mark anything you're inferring rather than seeing directly as TODO.

## What the source pack is not

Reference. Not assets. The photos are read, measured, and never published, never uploaded to your own store, and never used as the image-to-image seed for anything that ships. A recolour of a claimant's photo is still their photo. See `laws.md` §5 for the DMCA risk and the legitimate path when a competitor's *composition* is what you actually want.
