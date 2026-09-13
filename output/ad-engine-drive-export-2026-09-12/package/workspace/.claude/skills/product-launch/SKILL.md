---
name: product-launch
description: End-to-end product launch from a single URL. Takes any product link (competitor DTC page, supplier listing, marketplace), pulls the source pack, locks product truth, generates the full multi-angle AI image set per colorway plus editorial scenes with GPT Image 2 i2i, writes the PDP copy against brand law, builds the product on Shopify with per-colorway gallery tagging, clones a live PDP template for it, and scaffolds the product folder and product-scale skill. Trigger on "launch this product", "here's a link, build the PDP", "new product launch", "generate the angles for this bag", "duplicate the template for the new product", "build out the product page", or any pasted product URL that Brooks wants turned into a live listing.
disable-model-invocation: false
---

# Product Launch

One link in, a complete draft listing out: source pack, product truth, full generated
image set, PDP copy, Shopify product with a per-colorway gallery, its own PDP template,
and the product-scale skill that keeps every later ad on-model.

**Default brand: Velantra.** Other brands work if `SHOPIFY_<BRAND>_*` is in `.env`
(Motilli_1, Motilli_2, Lunessa, Solorna, Wend), but only Velantra has donor PDP templates.

## Read first, every time

1. `references/laws.md` — the gate. Read it before writing a word of copy or firing a
   generation. Several of these laws exist because breaking them cost real money.
2. `brands/<brand>/` — brand context before copy. Never write from the source listing's voice.
3. The product-scale skill for the closest existing product (`velantra-weekender`,
   `velantra-straw-tote`, `velantra-meridian`), for house prompt structure.

## Three standing rules for this skill

- **Draft only.** Every product is created DRAFT and stays DRAFT. Publishing is Brooks's
  call, made after he has seen the page. `--activate` is never yours to pass.
- **Nothing gets invented.** Dimensions, materials, hardware, lining, certifications,
  review counts, warranty terms, ship dates. If it is not in the source pack, on a real
  photo, or from Brooks, it is a TODO, not a sentence.
- **The competitor's photos never ship.** They are read, measured and thrown away. Every
  published pixel is ours, generated from our own reference. See laws.md (DMCA).

---

## Phase 0 — Scope the launch

Before anything runs, get four answers. Ask them in one pass, do not drip-feed:

| | |
|---|---|
| **Colorways** | Which ones we are actually manufacturing. Not the source listing's list. A colorway on the PDP that does not exist as a SKU is a returns problem. |
| **Price** | And whether there is a compare-at. |
| **Donor template** | Which live PDP this one should look like. `python3 scripts/build_pdp.py --list-donors`. Structured leather → `weekender`. Woven → `straw-birkin`. Top-handle → `delphine`. |
| **Pre-order?** | If any colorway is made-to-order, we need the supplier-confirmed ship month before the page is written. See laws.md. |

Write `spec.json` from the answers (`assets/spec.example.json` is the shape, annotated).
The spec is the single input to every script downstream.

## Phase 1 — Ingest the link

```bash
python3 scripts/ingest_source.py --url "<the link>" \
  --out "brands/velantra/products/<slug>/source"
```

Lands `source/images/` at full resolution plus `source.json` and `listing-text.md`.
Handles Shopify, JSON-LD and plain OG scraping automatically. If it prints the
did-not-resolve warning, the site is bot-blocking: fall back to the Playwright MCP
(`references/source-ingest.md`).

Then **look at the images**. Read them with the Read tool. Construction, closure,
hardware count, handle drop, lining, stitching, proportion. You cannot write a truthful
identity block or a truthful prompt from a JSON blob.

## Phase 2 — Lock product truth

Fill `PRODUCT-TRUTH.md` (scaffolded next phase) from what you saw plus what Brooks
confirms. Everything unconfirmed stays marked TODO. The opening mechanism, the carry
truth and the scale anchor are the three that break generations later, so they get
written in prompt-ready language, not spec-sheet language.

Present the colorway list, the dimensions and any claim you intend to make on the page
back to Brooks before Phase 4. This is the cheapest possible moment to catch a wrong fact.

## Phase 3 — Scaffold

```bash
python3 scripts/scaffold.py --spec spec.json
```

Creates `brands/<brand>/products/<slug>/` with the house subfolder layout, writes
`PRODUCT-TRUTH.md`, and stubs `~/.claude/skills/<brand>-<slug>/SKILL.md` — the
product-scale skill. Fill its identity block before any ad work touches this product.

## Phase 4 — Generate the imagery

**This is the phase you run yourself, through the Higgsfield MCP.** There is no working
image CLI. Full mechanics, prompt templates and the QA loop: `references/imagery.md`.

The shape of it:

- **GPT Image 2 (`gpt_image_2`), pure i2i, always.** Never Nano Banana for product shots.
- Generate the **hero colorway's angles first** from the source reference, QA them, then
  derive every other colorway by recolouring the approved hero angle. Geometry is decided
  once; colour is the only thing that varies.
- **Three variants per slot. Pick one.** Never ship the first roll.
- **Frame-QA every pick** against real photos: silhouette, closure, hardware count and
  placement, lining, no logos, correct colour, and the 3D-render tell. A frame that nails
  the product but reads as CGI is a reject, not a compromise.
- Land results with `scripts/fetch_images.py --manifest m.json --out <product-images>`,
  which writes `colors/<Colorway>/<angle>.png` — exactly what Phase 6 reads.

Default angle set per colorway (4 gallery slots, and the order they appear in):

```
front  →  interior  →  lifestyle  →  detail
```

Plus editorial scenes for the PDP tiles. Override with `spec.angle_order` when the
product needs it.

## Phase 5 — Write the PDP copy

`references/pdp-copy.md` has the block-by-block brief, the voice, and the worked example.
Copy goes into `spec.pdp` and nowhere else.

The short version: brand context first, avatar language over adjectives, claims only from
product truth, no em dashes, no origin claims, no invented proof. Read the finished copy
back to Brooks in the chat before it goes near the theme.

## Phase 6 — Build the product

```bash
python3 scripts/create_product.py --spec spec.json \
  --images "brands/velantra/products/<slug>/product-images"
```

Builds it field by field with `productSet` (never `productDuplicate`), staged-uploads
every image, and attaches each with a `#color_<handle>` alt tag, in colorway blocks, with
each colorway's front shot set as its variant featured image.

**The tag is not optional.** An untagged image appears on *every* colorway at its raw
global position. That is the bug that put an interior shot at position 1 across eight
Straw Tote colorways. Shared shots get attached once per colorway, each with its own tag.

## Phase 7 — Build and assign the PDP template

```bash
python3 scripts/build_pdp.py --spec spec.json --donor weekender          # dry
python3 scripts/build_pdp.py --spec spec.json --donor weekender --push   # to the live theme
python3 scripts/assign.py --state <slug>/launch-state.json --collections handbags
```

`build_pdp.py` clones the donor's live template, swaps in the spec's copy, blanks the
donor's image references and normalises em dashes. Every product gets its **own** template
suffix. Editing `templates/product.json` does nothing to a bag.

`assign.py` sets `templateSuffix` and joins collections. Without it the product renders
the generic template and all of Phase 7 is invisible. It stays DRAFT unless Brooks says
otherwise.

## Phase 8 — Hand it back

Deliver, in the chat:

- Admin link and preview link.
- The full generated image set as attachments, not paths (house law: deliver assets).
- The PDP copy read out in full, block by block.
- Every remaining TODO in `PRODUCT-TRUTH.md`, named.
- The launch checklist from `references/laws.md` §Ship gate, with each line answered.

Then ask whether to publish. Do not publish.

---

## Running it end to end

```bash
cd .claude/skills/product-launch/scripts
python3 launch.py --spec spec.json --steps ingest,scaffold
#   ... Phase 4 imagery + Phase 5 copy happen here, by hand ...
python3 launch.py --spec spec.json --steps product,pdp,assign --donor weekender --push
```

Any step is resumable; state lives in `brands/<brand>/products/<slug>/launch-state.json`.

## When something breaks

| Symptom | Cause |
|---|---|
| `CERTIFICATE_VERIFY_FAILED` | An old script using `urllib`. Everything here goes through curl. Do not add urllib. |
| Shopify GraphQL hangs | Same. curl only. |
| Colours leak across the gallery | An untagged media. Re-alt it with `#color_<handle>`. |
| PDP shows the generic layout | `assign.py` never ran, or the suffix has no matching template on the *published* theme. |
| PDP looks stale after a push | Shopify's full-page cache, 10 to 15 minutes, and query params do not bust it. Verify via the Admin API. Pages update instantly; products do not. |
| Custom HTML vanished from a block | The `custom` block sanitises `<style>`, `<details>`, `<summary>`. Ship rich HTML as a theme snippet instead. |
| Donor template not found | The theme was republished. `--list-donors` reads the live one. Never hardcode a theme id. |
| Higgsfield "Rate limit reached" | 8 concurrent jobs max on Ultra. Fire in waves. |

## Files

```
SKILL.md                     this
references/laws.md           the gate: house laws, DMCA, ship checklist
references/source-ingest.md  URL ladder, bot-blocked fallbacks, what to read off the photos
references/imagery.md        the full image system: angles, prompts, MCP calls, frame QA
references/pdp-copy.md       block-by-block copy brief, voice, worked example
references/shopify.md        API mechanics, gallery tagging, template and theme structure
scripts/shop.py              curl-backed multi-brand Admin API
scripts/ingest_source.py     URL -> source pack
scripts/scaffold.py          vault folder + PRODUCT-TRUTH.md + product-scale skill stub
scripts/fetch_images.py      generated URLs -> colors/<Colorway>/<angle>.png
scripts/create_product.py    productSet + staged media + colour tags + reorder
scripts/build_pdp.py         donor template clone + content swap + push
scripts/assign.py            templateSuffix, collections, channels, publish
scripts/launch.py            resumable orchestrator
assets/spec.example.json     annotated spec
```
