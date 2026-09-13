# Motilli — "GLP-1 Health Insider" Listicle Advertorial

10-point listicle advertorial (wrong-organ / upstream angle) for women on GLP-1s.
Built from the user-supplied HTML, recolored to a **single brand-green accent (#95c219)**
like the NoraLife reference uses one orange, with all 15 images generated/sourced and wired in.

## Files
- **`index.html`** — the finished standalone page (self-contained; relative `images/` refs).
- `images/` — all 15 assets (4 fresh Higgsfield gens, 8 reused brand assets, 3 hand-built SVGs).
- `gen_fresh.sh` / `gen_fresh.log` — the Higgsfield gpt_image_2 batch for the 4 net-new images.

## Accent color — one green hue, tonal steps (for legibility)
Pure `#95c219` is a light lime: illegible for small text on cream and for white-on-button.
So, exactly like NoraLife's one orange (lighter highlight vs. deeper button), it's used as **one hue in steps**:
| Token | Hex | Used for |
|-------|-----|----------|
| `--green` | `#95c219` | headline highlight, borders, note/offer-card borders, SVG fills, badges |
| `--green-dk` | `#5f8310` | CTA button + hover (white text stays legible) |
| `--green-ink` | `#4c6a0d` | small links, verified badges, "Note:"/emphasis on light |
| `--green-lt` | `#eff7dd` | note-box tint, soft fills |

Kept (true in the NoraLife reference too): review **stars gold** `#f5a623`, **"HIGH" red** `#d63c2f`.
Removed inconsistencies from the source HTML: peach note-box → green tint; teal byline gradient → real photo.

## Image map — each congruent to its item's argument
| Slot | File | Source | Shows |
|------|------|--------|-------|
| Byline | `byline-sarah.png` | fresh | Sarah Mitchell, RN headshot |
| 1 Stomach vs colon | `item01-diagram.svg` | SVG | on-ramp (stomach) vs off-ramp (colon) diagram |
| 2 Failed remedies | `item02-failed-remedy.png` | reuse | laxative/mag/fiber/stool-softener, X-marked |
| 3 Prokinetic mechanism | `item03-mechanism.svg` | SVG | apigenin → vagus nerve → stomach contracts |
| 4 Routine returns | `item04-relief.png` | fresh | relaxed, at-ease woman at home |
| 5 Bloating deflates | `item05-bloating.png` | reuse | before/after midsection |
| 6 Sulfur burps stop | `item06-dinner.png` | reuse | woman confident with friends at dinner |
| 7 One vs cabinet | `item07-one-vs-stack.png` | fresh | single Motilli jar vs 5-product clutter |
| 8 Formulated for GLP-1 | `item08-formulation.png` | fresh | Motilli + celery + chlorophyll, lab/science |
| 9 Guarantee | `item09-guarantee.svg` | SVG | 60-day money-back seal + reassurances |
| 10 Community | `item10-community.png` | reuse | 3×3 grid of women 50–70 with jars |
| Offer card | `offer-trio.png` | fresh | three Motilli jars (Buy-2-Get-1) on soft sage/cream — NoraLife-style 2-col, stacks on mobile |
| Reviews | `rev-linda/diane/barbara/carol.png` | reuse | verified-customer headshots |

Fresh + product-ref images were generated via Higgsfield `gpt_image_2` image-to-image off the
real jar (`brand/website-assets/motilli product reference.png`), matching the existing pipeline.

## v2 — all images 1:1, NoraLife-inspired (current)
The whole image set was rebuilt to **1:1 squares** in a cohesive celery-green/cream palette
(NoraLife's one-warm-world → our one-green-world). Changes from v1:
- `item01` diagram → **product-in-celery-ring hero** (`item01-hero.png`, NoraLife #1 look)
- `item02` failed-remedy photo → **Motilli-vs-The-Old-Stack comparison table** (`item02-table.svg`, NoraLife #2)
- `item03`/`item09` infographics → redesigned as **squares**
- `item06` dinner → **two-women-laughing-close** (`item06-social.png`)
- `item07` → square jar-vs-stack (`item07-stack.png`); `item08` formulation → **gloved-hand lab shot** (`item08-lab.png`, NoraLife #8)
- `item04` relief, plus kept-1:1 `item05`/`item10`/`offer-trio`/`byline`/reviews
Re-deployed via `deploy.py` (now does the unpublish/republish **cache-bust toggle** on update; flipped in ~18s).
`gen_1x1.sh` = the 1:1 regeneration batch.

## v3 — hero/collage restyle + product-holding reviews (current)
- `item01-hero.png` → **product hero with two circular ingredient callout bubbles** ("Real Celery Juice",
  "Organic Chlorophyll") + a "NATURAL INGREDIENTS / CLEAN & PURE / THIRD-PARTY TESTED" badge row (NoraLife img #1).
- `item07-stack.png` → **green-✓ Motilli vs red-✗ failed-cabinet collage** (Osmotic Laxative + Fiber Powder;
  Magnesium Citrate + Stool Softener + Probiotic), styled after NoraLife img #2.
- 4 review avatars (`rev-*.png`) regenerated as **customers holding the jar** (UGC selfie), and `.rcard-photo`
  switched to `aspect-ratio:1/1` so the product is fully visible. Byline (Sarah) left as an author headshot —
  it's a 52px face crop where a held jar wouldn't read.
- `gen_composites.sh` (item1/item7) and `gen_reviews.sh` = the regeneration batches.

## ✅ DEPLOYED — live on getmotilli.com (y9t3s8-ns)
- **Live:** https://getmotilli.com/pages/glp1-wrong-organ-insider
- **Admin:** https://y9t3s8-ns.myshopify.com/admin/pages/705161167215  (page id `705161167215`)
- **Handle:** `glp1-wrong-organ-insider` · **template_suffix:** `adv-wo-v3` (chrome-suppressed) · **published**
- Deployed with `deploy.py` (mirrors `creatives/MOT-ADV-WO-04/deploy.py`): 13 rasters → Shopify Files
  CDN, 3 SVGs inlined into the body, CDN `width=` resize params added (Item 10: 10.8MB PNG → 292KB WebP;
  total page images ~110MB → ~2MB). Verified live: HTTP 200, no theme chrome, styles/fonts/scripts intact,
  all 13 CDN images load as WebP, 3 infographics inlined.
- Re-deploy: re-run `deploy.py` (uses `.cdn_cache.json` to skip unchanged uploads). NOTE: the edge cache
  staleness-traps body updates on an existing handle — bust with an unpublish/republish toggle
  (see `creatives/MOT-ADV-WO-04/poll_bust.py`), per [[advertorial-template-binding]].

## Notes for review
- **CTA target:** every button + the inline "Motilli" link point to `https://getmotilli.com/` — the same
  target the other live Motilli advertorials use. If you want it to land on a specific PDP/checkout, change
  the href and re-deploy (with the cache-bust toggle).
- Footer claims are standard advertorial/FDA boilerplate — keep your medical/regulatory review.

## Notes
- Faces are AI-generated representative customers; footer carries the "names and photographs
  shown are representative" disclaimer.
- Preview locally: `python3 -m http.server 8101 --directory landing-pages/motilli-glp1-insider-listicle`
  (also wired as the `insider-listicle` config in `.claude/launch.json`).
