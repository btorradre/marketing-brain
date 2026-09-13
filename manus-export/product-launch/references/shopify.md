# Shopify mechanics

## Auth

Use a client-credentials token exchange (custom-app client ID/secret → short-lived access token), minted per session, never written to disk long-term. If you have multiple brands/stores, keep a small per-brand config mapping store domain to its credentials.

**Everything should go through curl or an equivalent HTTP client with a proper CA bundle.** Some scripting environments' default HTTP libraries lack a working CA bundle out of the box and will fail with a certificate verification error, or hang on GraphQL calls — don't paper over that with a workaround; use a client that has TLS working correctly.

## Theme

- **Never hardcode a theme id.** Stores republish themes periodically, and the "live" theme's ID changes each time. Look up whichever theme currently has the `main` role at generation/deploy time, every run. A template pushed to the wrong theme is invisible and looks like a bug somewhere else.
- Theme asset reads need the bracket param URL-encoded (`asset%5Bkey%5D=...`) or some HTTP clients will reject the URL as a bad range.
- **Each product should have its own template suffix** (e.g. `templates/product.<slug>.json`). Editing the shared default `templates/product.json` does nothing to a product that already has its own override, and editing it directly affects every product that doesn't have one.
- **Some theme block types sanitize their HTML content setting** — tags like `<style>`, `<details>`, `<summary>`, and unknown tags get stripped. Rich custom HTML should ship as a real theme snippet (rendered via an include/render tag) instead, which isn't sanitized and has the product object in scope.
- Block rendering for the main product section often lives in a separate snippet file, not the section file itself — check both when debugging a rendering issue.

## Donor templates

Read whichever theme is currently published to see what donor page templates already exist. Pick a donor whose structure most resembles the new product:

| Donor shape | Use for |
|---|---|
| Structured, flap closure | Structured leather/canvas bags with a fold-over flap |
| Woven/straw body | Woven or straw-bodied items |
| Top-handle | Top-handle bags |
| Open-top structured tote | Open-top structured totes |

The donor decides which sections exist. Fill what's there and report what the donor lacks. Also blank every image reference pointing at the donor's own CDN-hosted photos, because those are the donor product's photos and they will otherwise show on the new page.

Section `disabled` flags carry over from the donor — flip them per product as your copy specification requires.

## Product creation

Use a bulk/set-style product mutation with synchronous execution, one `Color` option, one variant per colorway. Never use a "duplicate product" mutation or admin button (house law — see `laws.md` §8). Always create with `status: DRAFT`.

Set `inventoryPolicy: CONTINUE` (allow overselling) on every variant if your fulfillment model depends on it — e.g. the store runs negative oversell counters, or pre-orders need to stay purchasable. This is also why a pre-order colorway is invisible in the buy box unless the page itself says so in words.

## Media

The sequence, and every step matters:

1. Create a staged upload, POST the file to the returned target URL, then use the resulting resource URL as the media's original source.
2. Attach the media to the product in reasonable batches (e.g. 10 at a time), each with its `alt` text already carrying the `#color_<handle>` tag.
3. **Wait for every media item to reach a "ready" state.** Reordering before that silently misfires.
4. Reorder the media with a full move list, matching items by their alt text.
5. Set each variant's featured image via a variant-media-append call.

### The tag

```
"<Title> in <Colorway>, <angle> #color_<handleized-colorway>"
```

A page template that filters its gallery by colorway relies on this suffix. Untagged media renders on **every** colorway at its raw global position. Shared shots are attached once **per colorway**, each with its own tag. Never share one attachment across colorways.

## Caching

- **Product pages**: full-page caching can serve a stale page for 10 to 15 minutes after an edit, and cache-busting query parameters typically do **not** bust it. Verify against the Admin API or a source-of-truth field, never against the rendered page.
- **Standalone content pages** (as opposed to product pages) tend to update instantly — a different cache path. Don't generalize caching behavior from one page type to the other.
- The storefront CDN can lag admin media changes by roughly 10 minutes.

## Collections and channels

Join the new product to its collection(s) by handle, and publish it to whichever sales channels it needs. If a collection template has a sale-badge feature that triggers automatically whenever a "compare at" price is set higher than the actual price, re-check what the badge says any time you touch pricing on a product in that collection — a leftover seasonal badge label can resurface unexpectedly when compare-at is restored.

## Sanity checks worth running before and after a deploy

- Confirm the store/token/live-theme resolution is correct before making any write calls.
- List every product template currently on the theme, to confirm you're not colliding with an existing slug.
- Fetch the specific donor template's JSON to confirm it has the section you expect to clone.

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| A generic SSL/certificate verification error | An HTTP client without a proper CA bundle. Switch to one that has TLS working (e.g. curl). |
| GraphQL calls hang indefinitely | Same underlying cause as above. |
| Colors leak across the gallery | An untagged media item. Re-tag its alt text with the colorway suffix. |
| Page shows the generic/default layout | The template was never explicitly assigned, or the suffix has no matching template on the *published* theme. |
| Page looks stale right after a push | Full-page cache (10-15 minutes on product pages); verify via the Admin API, not the rendered page. |
| Custom HTML vanished from a block | The block type sanitizes `<style>`, `<details>`, `<summary>`. Ship rich HTML as a theme snippet instead. |
| "Donor template not found" | The theme was republished. Always resolve the live theme at generation time; never hardcode a theme id. |
| Image generation "rate limit reached" | You've exceeded the platform's concurrency cap. Fire generation jobs in smaller waves. |
