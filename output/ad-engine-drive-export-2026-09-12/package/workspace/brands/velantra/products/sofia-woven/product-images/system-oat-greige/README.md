# The Sofia Woven Tote — oat-greige product-image system

**v4, 2026-08-05.** 32 images: **8 colorways × 4 shots**, all **1:1 / 2048×2048 PNG**,
GPT Image 2 image-to-image on kie.ai. Matches the Margot (Meridian) system so the
collection grid reads as one shoot.

## ⚠️ Source provenance — read before regenerating anything

The luxboattote DMCA compositions must **never be published** on any surface, and that
includes every recolor of them: `product-images/straw birkin/caramel 1.png`, `caramel 2.png`,
`straw tote 1-3.webp`, `black-colorway/black-tote-*.jpeg`, `concepts/…/assets/sofia/colorways/*.jpg`
and `concepts/…/plates/*.png`.

**One deliberate exception, per Brooks (8/05, reaffirmed twice): `_REF-product.jpg`** (a copy of
the colorways caramel.jpg) is used as the i2i SHAPE reference in every generation, because it is
the only photo showing the exact bag construction he wants on all colourways. Using it as an input
to author brand-new studio compositions republishes nothing — the outputs share zero composition
with the claimant's photo. The file itself stays reference-only, never uploaded to any storefront
or ad. All other sources feeding the system are clean: `statics/straw birkin/cream.webp` (on-model
pose) and `product-images/straw birkin/straw birkin opened.png` (open-bag composition + contents).

Colour is introduced by TEXT for every colourway (see the geometry-leak rule below), so no
per-colorway photo — clean or not — enters any job.

## The shots — LIVE GALLERY IS 3 PER COLOUR (Brooks, 8/05)

1. **hero** — 3/4 front, bag standing on the oat-greige `#E7E3DB` seamless sweep
2. **interior** — overhead, flap folded fully back, packed (laptop / bottle / tan wallet)
3. **onmodel** — neutral mid-grey studio, one model, oatmeal linen shirt + cream linen
   trousers, bag held by both handles at hip height

A fourth shot type, **straight** (front elevation), exists on disk but was PULLED from the
live gallery: at PDP scale it reads as a duplicate of the hero at a different size, and
Brooks cut it ("we really only need three product images per product... get rid of all
images like the second one"). Don't re-upload it; don't generate it for future colourways.

## ⛔ REFERENCE LAW + PRODUCT TRUTH (v4, Brooks 8/05)

**`_REF-product.jpg` is THE product reference and is wired into EVERY generation** ("use this as
the reference in every single one"). Do not derive product truth from any other photo — belt
geometry differs per colourway across the source photos and Brooks wants THIS arrangement on all
of them. Never publish the file itself (it is one of the retired compositions — reference-only).

What it shows, pinned in `_v3_blocks.py` (import the blocks, don't re-write them from memory):

- **Body is soft and unstructured.** Hand woven straw that slouches under its own weight; side
  walls flare into soft woven WINGS at the top outer corners; the base is a soft rounded
  rectangle. Pliable basketry, NOT structured leather goods.
- **Weave is coarse and chunky** — thick twisted cord in visible horizontal rows, with a wide
  braided lacing showing a criss-cross X pattern up each side edge. Never a fine machine grid.
- **Flap is one DEEP band across the whole top.** The handles pass through narrow SLOTS cut into
  it. Its lower edge is cut — same single sheet, square corners — into a squared tab stepping down
  at the far left, a wide flat-bottomed centre panel between the handle slots, and a squared tab
  at the far right. Never separate patches, never rounded pillows.
- **Belts: one horizontal + one diagonal**, never a symmetric X and never a V. One narrow strap
  runs nearly horizontally below the flap; a second crosses it diagonally from upper right to
  lower left ending in a rounded tip; a short pointed tab hangs from the flap centre behind them.

## The failure that produced v3 — read before rewriting any prompt

**v2's canon step described the bag so thoroughly that GPT Image 2 stopped copying the reference
and started building one from the text.** What it built was structured leather goods: rigid box
body, hard corners, fat rounded flap tabs reading as applied patches, a fat symmetric X of belts.
All 32 downstream images inherited it, because they all descended from that canon.

**The rule: the canon comes from MINIMAL intervention on a clean static** — restage the background,
change the stitching colour, nothing else. Detailed shape language belongs in *downstream* prompts
as a guard against drift, never as a substitute for the reference. When prompt and reference image
disagree, this model follows the prompt, so an over-specified prompt is a redesign instruction.

Corollaries: every downstream prompt must say image 1 is the ONLY authority on the bag and image 2
supplies composition ONLY. And **never use a previous generation's render as a composition
reference** — it carries its own bag shape in with it. Use clean statics.

## How congruence is enforced

v1 recoloured **four different masters**, each sourced from a different colourway photo. Every shot
therefore carried its own bag geometry and its own hue landing point, which produced three defects
Brooks caught: white contrast stitching, hue drift between shots of the same colourway (yellow was
the obvious one), and a broken asymmetric flap on some on-model frames.

v4 collapses everything to **one bag, rooted in the real product photo**:

```
_REF-product.jpg                     <- the real product. In the refs of EVERY job.
   ├─ _v4-canon-v3.png = sofia-caramel-hero.png      (restage of REF, 3/4)
   ├─ _v4-canon-v2.png = sofia-caramel-straight.png  (restage of REF, front-on)
   ├─ _m4-interior-v1.png            <- REF + open-bag composition ref
   ├─ _m4-onmodel-v2.png             <- REF + on-model composition ref
   │
   └─ sofia-<color>-hero.png         <- recolour of canon-v3, colour by TEXT, REF as ref 2
         └─ sofia-<color>-{straight,interior,onmodel}.png
                                     <- refs = [shot master, that colour's hero, REF]
```

Rules that must survive any future edit:

- **`_REF-product.jpg` appears in every job's refs** as the construction authority.
- **Every shot master descends from a restage of REF**, so silhouette, flap cut, strap
  arrangement and weave scale are identical across all 32 images.
- **The hero is the colour authority** for its colourway's other shots — but colour is always
  *introduced* by text, never by a colourway photo: **a colour-reference image leaks its geometry**
  (proven on Lady Pink in v3, whose handles grew ~12% until its colour ref was dropped).

**Stitching is TONAL everywhere** — thread matches the leather it sits on. No white or
contrast stitching anywhere on the bag. Note this deliberately differs from the poolside
reference photos, which do show white contrast stitching.

## Gallery alt text — REQUIRED for per-color filtering

The Impulse-based theme filters PDP media per selected colour by an alt-text suffix.
**Untagged media leaks onto every colour.** Every image must carry exactly one tag:

```
Velantra Sofia Woven Tote - <Option Label> <Shot> #color_<handle>
```

| File stem | Option label | Alt suffix |
|-----------|--------------|-----------|
| `sofia-caramel-*` | Caramel | `#color_caramel` |
| `sofia-cream-*` | Cream | `#color_cream` |
| `sofia-light-chocolate-*` | Light Chocolate | `#color_light-chocolate` |
| `sofia-caban-black-*` | Caban Black | `#color_caban-black` |
| `sofia-sky-blue-*` | Sky Blue | `#color_sky-blue` |
| `sofia-lady-pink-*` | Lady Pink | `#color_lady-pink` |
| `sofia-lightning-orange-*` | Lightning Orange | `#color_lightning-orange` |
| `sofia-sunny-yellow-*` | Sunny Yellow | `#color_sunny-yellow` |

e.g. `Velantra Sofia Woven Tote - Sky Blue Hero #color_sky-blue`

Group media per colour, hero first within each group, and put the default variant's
hero at **position 0** (that becomes the collection tile / featured image).

## Regenerating

The canons are direct restages of `_REF-product.jpg`: `_v4-canon-v3` IS `sofia-caramel-hero`,
`_v4-canon-v2` IS `sofia-caramel-straight`. To rebuild them, restage REF with the minimal
"only change the setting" prompt (`_jobs_canon.json` pattern) — do NOT write a longer prompt,
see the failure note above.

```bash
python3 _build_jobs.py masters                                      # interior + onmodel from REF
python3 _runner.py _jobs_masters.json
python3 _build_jobs.py heroes                                       # 7 heroes, colour by text
python3 _runner.py _jobs_heroes.json
python3 _build_jobs.py rest '{"interior":"v1","onmodel":"v2"}'
python3 _runner.py _jobs_rest.json
```

Runner notes:

- **kie drops connections under batch load.** Uploads, createTask and downloads all retry with
  backoff. Task IDs are persisted to `_tasks_inflight.json` as they are created, so a failed
  *download* resumes rather than paying for a regeneration. Delete that file only once the run
  is clean. If a job reports a bare task ID as its error it merely out-waited the poll timeout —
  check `recordInfo` before regenerating, the result is usually sitting there ready.
- **kie's result CDN has two hosts.** `tempfile.redpandaai.co` is fine; `tempfile.aiquickdraw.com`
  is intermittently blocked on this network (TLS reset / curl 35; port 80 returns a filter page
  reading "Access to this site is blocked"). When that happens, relay: pass the kie result URL to
  the Pixa MCP `upload {method:"url"}`, which fetches server-side and returns a reachable
  `assets.pixelcut.app` URL. Full resolution is preserved.
- **A colour-reference image leaks GEOMETRY, not just hue.** Passing a colourway static as ref 2
  dragged that photo's taller handles into the render and overrode an explicit "match the handle
  height of image 1" instruction. Lady Pink only locked once its colour ref was dropped and the
  hue driven from text alone. If a colourway's silhouette won't match, drop the colour ref first.
- **TRUE CARAMEL is the muted greige taupe of REF's leather (~RGB 172,135,110), never a saturated
  orange tan (Brooks, 8/05).** The v4 canon restages silently warmed it; only the on-model kept the
  truth. After ANY canon restage, patch-sample the leather against REF numerically before building
  downstream. The caramel wording in `_build_jobs.py` COLORS is pinned accordingly.
- QA the set numerically AND at full resolution: measure the bag's bounding box per image (all 8
  heroes should land within ~1.5%, currently w=453-457 h=385-394), then eyeball flap tabs, belts
  and handle roots at 100% on a few images. Downsampled contact sheets hide both kinds of defect —
  the v3 belt/tab artifacts passed a contact-sheet review and Brooks caught them at full size.
- Known failure mode on `interior`: the recolor leaks onto the tan zip-wallet prop. The prompt
  pins the laptop, bottle, wallet and lining explicitly; if it recurs, re-roll with `"force": true`.
- `_v1-white-stitch/`, `_v2-rigid-rejected/` and `_v3-wrong-belts/` hold superseded sets.
  Delete once v4 is signed off.

Cost: ~95 generations across v1-v4 ≈ $4.
