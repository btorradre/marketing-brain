# Landing-Page Build Protocol — Mechanics Detail

This reference gives the exact mechanics of the Secondary Protocol described in SKILL.md: turning finished advertorial copy into an importable landing-page file for a page builder (the original implementation targets PageFly on Shopify; the same approach generalizes to any slot-based page builder or static template).

The core idea: a master advertorial page template is a **layout shell with a fixed inventory of editorial slots** — not a script to be re-derived every time. You never hand-build HTML/page-JSON. You write a small **role-keyed content map**, then run a short program that resolves each role name to its slot in the template and overwrites that slot's content. This keeps copy and layout mechanics fully separate: the copywriting engine (frameworks, laws, section architecture) decides what the words say; this protocol only decides where they go.

---

## The slot inventory (example, from the reference "Health Insider Kids" master template)

A typical master template exposes roughly 30-45 named slots, grouped into three kinds:

**Text slots** (write HTML string content) — examples of role names: `brand_header`, `headline` (this one is special — see below), `date_line`, `lede`, `setup_h2` / `setup_para`, `problem_reveal_h2` / `problem_reveal_para`, `hidden_truth_h2` / `hidden_truth_para`, `myth_h2` / `myth_para`, `solution_cat_h2` / `solution_cat_para`, `mechanism_h2` / `mechanism_para`, `transformation_h2` / `transformation_para`, `results_h2` / `results_para`, `why_hidden_h2` / `why_hidden_para`, `math_h2` / `math_para`, `offer_h2` / `offer_para`, `two_futures_h2` / `two_futures_para`, `testimonial_1` / `testimonial_2` / `testimonial_3`, `cta_subtext_1`, `closing_h2` / `closing_subhead`, `footer_legal`, `disclaimer`.

These role names come from one example page's beat structure — they are generic "headline + body" containers, not a required sequence for every advertorial. Map your framework's actual beats onto whichever slots fit, in reading order; consolidate lightly-needed beats, skip slots you don't need (they simply keep the template's placeholder content), and don't force a narrative into an order it doesn't want just because a slot is named `myth_h2`.

**Button slots** (write a label + a destination URL): typically two CTA buttons, `cta_button_1` and `cta_button_2`.

**Image slots** (write a source URL + alt text): typically three — `hero_image`, `product_image`, `closing_image`.

**Special case — `headline`:** in the reference template, the visible headline actually renders from **two synced slots** (e.g. a masthead headline and an SEO/meta headline). Write the headline text once in your content map under the single role name `headline`; the build step fans it out to both underlying slots so they always match.

---

## The content map (what you actually write)

Write a small structured document — a role-keyed JSON object is the simplest shape — with three top-level groups matching the three slot kinds:

```json
{
  "brand": "BrandName",
  "text": {
    "brand_header": "<p>...</p>",
    "headline": "...",
    "lede": "<p>...</p>",
    "setup_h2": "...",
    "setup_para": "<p>...</p>"
    /* ...only the roles you're filling... */
  },
  "buttons": {
    "cta_button_1": { "value": "CHECK AVAILABILITY", "href": "https://product-page-url" },
    "cta_button_2": { "value": "CHECK AVAILABILITY", "href": "https://product-page-url" }
  },
  "images": {
    "hero_image":    { "src": "https://hosted-image-url", "alt": "..." },
    "product_image": { "src": "https://hosted-image-url", "alt": "..." },
    "closing_image": { "src": "https://hosted-image-url", "alt": "..." }
  }
}
```

Rules:
- Text values are HTML strings — wrap body copy in `<p>…</p>` since paragraph slots render HTML directly.
- **Only include the roles you're actually filling.** Any text slot left out of the map keeps whatever placeholder or example copy the master template shipped with — so fill every content slot you intend to use, or that slot will leak the template's original example content into your finished page.
- Image `src` values must be hosted URLs, not local file paths. If hosted URLs for the hero, product, or closing images aren't available yet, leave the `images` block out entirely and tell whoever is finishing the build that those three images need to be swapped in the page builder's own editor after import. The hero-image generation prompt (produced in the Primary Protocol) is what feeds the hero slot once an image exists.

---

## Applying the map and the residue check

Applying the content map to the template is a straightforward find-and-replace / templating operation: for each role in the content map, look up its slot ID(s) in the slot inventory, and overwrite that slot's stored content (its `value`, or `src`/`alt` for images, or `value`/`href` for buttons) with the mapped content. This can be done with a short, generic script — nothing framework-specific, no external dependencies required.

After applying the map, run a **residue check**: search the resulting output for a fixed list of tokens known to belong to the master template's original example content (names, brand references, example phrases — e.g. a placeholder brand name, a placeholder testimonial's first name, a placeholder doctor's name, a placeholder product noun). Any hit means that content is still sitting in the finished page.

- If residue turns up in a **text slot you intended to fill**, you left a role out of the content map — add it and reapply.
- If residue turns up **only in image `src`/`alt` fields** and you deliberately deferred images (no hosted URLs yet), that's expected — confirm every flagged hit traces back to an image slot, then plan to swap those three images in the page builder's editor after import.
- Once every text slot is filled and images are either supplied or explicitly deferred and confirmed, the residue check should come back clean.

The output is a single importable page file (for a PageFly/Shopify target, this is a zip archive containing the page's JSON at its root, given a `.pagefly` extension) — hand that file to whoever manages the storefront to import and publish.

---

## Ship the side assets alongside the build

- **Hero-image generation prompt:** a single, vivid image-gen prompt for the hero slot — subject, scene, emotion, composition, editorial/photographic style, aspect ratio — matched to the avatar and the advertorial's opening. No text-in-image instructions unless specifically requested.
- **Headline variations:** the 3-4 length-varied, open-loop headlines from the Primary Protocol, listed out so there's material for A/B testing beyond the single headline shipped in the build.

---

## When the template genuinely doesn't fit

The slot inventory is fixed by whatever master template is in use. If a narrative genuinely won't fit the available slots — too many distinct beats, or an order the template can't express — say so rather than forcing it, and propose either consolidating beats into fewer, denser slots, or flag that a custom template is needed (building a new template from scratch is out of scope for this slot-swap approach).
