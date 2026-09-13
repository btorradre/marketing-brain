# Image generation — Higgsfield MCP

All imagery on the page is generated with the **Higgsfield MCP** (tools prefixed
`mcp__<higgsfield-server>__*`). Use `nano_banana_pro` — it gives the best label/text
fidelity and clean illustration, and accepts a reference image for image-to-image.
2k resolution, ~2 credits/image. Check `balance` first.

## The product reference (do this once, first)
The hero/lifestyle/UGC shots must show the REAL product, so feed the brand's product
photo as a reference:
1. `media_upload` → returns a presigned PUT url + `media_id`.
2. `curl -X PUT -H "Content-Type: image/png" --data-binary @<product.png> '<upload_url>'`
3. `media_confirm` with that `media_id`.
4. Pass it on every product/UGC generation: `medias:[{value:"<media_id>", role:"image"}]`.

Pick the product photo that shows the **brand wordmark + key label text** most clearly.
In every product prompt say: *"Reproduce the jar/bottle and its label EXACTLY and
legibly. IGNORE any badges or marketing text around the product in the reference —
render ONLY the clean product."*

## Polling (text/CLI clients)
`generate_image` returns a job id with `status:pending`. Poll `job_display` with that id
until `status:completed`, then read `results.rawUrl` and `curl` it to
`<brand>/generated-images/<name>.png`. (Don't trust local screenshot tools for product
labels — open the rawUrl or Read the downloaded PNG to verify.)

## The shot list (16 images, file names the template expects)
Product (with product ref):
- `lp-hero-jar.png` — HERO. Product on a warm brand-gradient backdrop, props at base, soft morning light, 1:1.
- `lp-formula-jar.png` — product on a low pedestal/plinth, soft studio, 1:1.
- (`lp-buy-jar.png` optional — the native buy box has its own gallery, usually not needed.)

Emotional portraits (NO product ref — pure lifestyle, text-to-image, 4:3):
- `lp-women-serene.png` — ~55, eyes closed, serene, soft window light, blush bg.
- `lp-women-laughing.png` — ~50, laughing outdoors, golden hour.
- `lp-women-smiling.png` — ~60, warm genuine smile indoors. **Vary age/ethnicity across the three.**

UGC testimonials (WITH product ref, candid amateur-selfie look, 1:1):
- `lp-ba-1/2/3.png` — "before/after / real stories" — distinct women holding the jar in a home/kitchen/bathroom.
- `lp-rev-1..5.png` — reviews — distinct women/settings holding the jar. **Vary hair, age, room, ethnicity** so they don't look like one person. Prompt: *"authentic user-generated smartphone selfie … holding the <product> jar, label legible … candid imperfect amateur photo."*
- `lp-research-woman.png` — warm ~55 woman holding the jar up to camera, room left for an overlay stat (3:4).

Mechanism illustrations (NO product ref — editorial medical infographic, 16:9). Always
generate these instead of hand-drawn SVG (the SVGs look cheap). Two matched panels in the
brand palette, **no text/labels/logos**:
- `lp-mech-open.png` — the "working" state (e.g. healthy cell, open gold channels, fuel flowing IN). Calm/optimistic.
- `lp-mech-locked.png` — the "broken" state (e.g. dim starved cell, rusted/closed channels, fuel stuck OUTSIDE). Subdued/somber. Say "visually consistent with the companion diagram."

Adapt the *subjects* to the brand's mechanism metaphor — the file names and roles stay the same.

## Press logos (NOT generated)
Do NOT AI-generate news logos — they come out garbled. Use the official vector marks.
`assets/press-logos/*.norm.svg` are pre-inked ("USA Today, Fox, Cosmopolitan, Forbes,
Women's Health"). To refresh or add outlets: download the official SVG from Wikimedia
Commons (`https://commons.wikimedia.org/wiki/Special:FilePath/<File>.svg`) and run
`assets/press-logos/normalize_logos.py` to ink them to the page color, strip width/height,
ensure a viewBox, and namespace ids so they inline together. Only claim outlets the brand
actually has placements/licensed mentions for.
