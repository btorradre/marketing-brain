# Reading the link

## The ladder

`ingest_source.py` tries three things and takes the first that resolves a product:

1. **Shopify product JSON** — `<url>.json` then `<url>.js`. Most DTC brands. Gives title,
   full description HTML, price, options, every variant, and every image at full
   resolution. Best case by a wide margin.
2. **JSON-LD** `schema.org/Product` embedded in the page. Marketplaces, BigCommerce,
   WooCommerce, most Next.js storefronts.
3. **OpenGraph plus `<img>` harvest.** Last resort, noisy, but usually gets the hero images.

Thumbnail URLs are rewritten toward the original file (Shopify `_800x.`, Alibaba
`_720x720`, Cloudinary `w_400`), so the downloads are full resolution rather than gallery
crops.

## When it is bot-blocked

The script prints a loud warning when the resolved title looks like `404`, `Not Found`,
`Access Denied` or `Just a moment` (Cloudflare). Do not trust anything after that warning.

Fallback, in order:

1. **Re-check the URL.** Most failures are a wrong or region-redirected path.
2. **Playwright MCP** — `browser_navigate` to the URL, `browser_snapshot` to read the page,
   `browser_evaluate` to pull the image list directly out of the DOM:

   ```js
   () => [...document.querySelectorAll('img')]
     .map(i => i.currentSrc || i.src)
     .filter(u => u && !/sprite|icon|logo|\.svg/i.test(u))
   ```

   Then feed those URLs to `fetch_images.py` with `path` entries pointing into `source/images/`.
3. **Ask Brooks for the photos.** If he is sourcing from a supplier, he usually has a
   better set than the public listing anyway, and supplier photos carry the real hardware.

## What to read off the photos

The JSON gives you the listing. The photos give you the product. Open them with the Read
tool and answer these, because every one of them ends up in a prompt and none of them can
be guessed:

- **Silhouette and proportion.** Wider than tall or taller than wide? Structured or slouchy?
- **Opening mechanism.** How does it actually open? Flap folding all the way over, zip,
  drawstring, magnetic, open top? This is the single most-failed detail in generation and
  it needs prompt-ready language, not a noun.
- **Hardware.** Metal colour, and the exact count and placement of every piece. Engines
  duplicate hardware and invent studs whenever the prompt is vague about what carries what.
- **Handles.** Rolled or flat, and the drop. The drop decides carry truth: short rolled
  handles are hand or forearm only, and if you script a shoulder carry the engine invents a
  strap to bridge the impossible pose.
- **Interior.** Lining material and colour, pockets. Written blocks get this wrong more
  often than any other field, and a wrong lining fails every open-bag frame.
- **Base and corners.** Feet, corner patches, reinforcement.
- **Branding.** Almost always none on our bags. Confirm, then keep the no-lettering negatives.
- **Texture per colorway.** Weave density and leather finish genuinely differ between
  colorways of the same bag.
- **Scale.** Anything in frame that gives real size: a hand, a shoulder, a suitcase.

Write the answers into `PRODUCT-TRUTH.md` as you go, and mark anything you are inferring
rather than seeing as TODO.

## What the source pack is not

Reference. Not assets. The photos are read, measured, and never published, never uploaded
to our store, and never used as the i2i seed for anything that ships. A recolour of a
claimant's photo is still their photo. `laws.md` §5 has the DMCA history and the
legitimate path when the competitor's *composition* is what Brooks wants.
