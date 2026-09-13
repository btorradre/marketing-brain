# Image generation for the sales page

All imagery on the page is generated with an AI image tool that gives strong label/text fidelity and clean illustration output, and accepts a reference image for image-to-image generation. Aim for roughly 2K resolution. Check your available credit/balance before starting a full run.

## The product reference (do this once, first)

The hero/lifestyle/UGC shots must show the REAL product, so feed the brand's product photo as a reference image on every generation call that needs to show the product:

1. Upload the product photo to your image tool as a reference image.
2. Pass that reference on every product/UGC generation call.

Pick the product photo that shows the **brand wordmark and key label text** most clearly. In every product prompt say: "Reproduce the jar/bottle and its label EXACTLY and legibly. IGNORE any badges or marketing text around the product in the reference — render ONLY the clean product."

## Polling / retrieving results

If your generation tool is asynchronous, submit the job, poll until it reports completed, then download the result image to your working folder using the exact filename your page template expects. Don't trust local screenshot tools for verifying product labels — open the actual downloaded image file (or its raw URL) directly to verify legibility.

## The shot list (16 images, file names the template expects)

Product shots (WITH the product reference attached):
- `lp-hero-jar.png` — HERO. Product on a warm brand-gradient backdrop, props at base, soft morning light, square 1:1.
- `lp-formula-jar.png` — product on a low pedestal/plinth, soft studio lighting, square 1:1.
- (`lp-buy-jar.png` optional — the native buy box usually has its own gallery, so this is often unnecessary.)

Emotional portraits (NO product reference — pure lifestyle, text-to-image, 4:3):
- `lp-women-serene.png` — woman ~55, eyes closed, serene expression, soft window light, blush background.
- `lp-women-laughing.png` — woman ~50, laughing outdoors, golden-hour light.
- `lp-women-smiling.png` — woman ~60, warm genuine smile, indoors. **Vary age/ethnicity across all three portraits.**

UGC-style testimonial shots (WITH the product reference, candid amateur-selfie look, square 1:1):
- `lp-ba-1.png` / `lp-ba-2.png` / `lp-ba-3.png` — "before/after / real stories" — 3 distinct women holding the product in a home/kitchen/bathroom setting.
- `lp-rev-1.png` through `lp-rev-5.png` — 5 "review" images — distinct women/settings holding the product. **Vary hair, age, room, and ethnicity across all five** so they don't read as one repeated person. Prompt direction: "authentic user-generated smartphone selfie ... holding the [product] jar, label legible ... candid imperfect amateur photo."
- `lp-research-woman.png` — a warm ~55-year-old woman holding the product up toward the camera, with visual room left in the composition for a stat-callout text overlay (3:4).

Mechanism illustrations (NO product reference — editorial medical/scientific infographic style, 16:9). Always generate these as images rather than hand-drawn vector graphics — hand-drawn SVGs tend to look cheap by comparison. Produce two visually matched panels in the brand's color palette, with NO text/labels/logos baked into the image itself:
- `lp-mech-open.png` — the "working" state panel (e.g. a healthy cell, open channels, fuel flowing in) — calm, optimistic visual tone.
- `lp-mech-locked.png` — the "broken" state panel (e.g. a dim/starved cell, closed or rusted channels, fuel stuck outside) — subdued, somber visual tone. Prompt it to be "visually consistent with the companion diagram" so the two panels read as a matched pair.

Adapt the *subjects* of the mechanism illustrations to whatever mechanism metaphor your brand's angle actually uses — keep the same file-naming convention and functional roles.

## Press logos (NOT generated)

Never AI-generate a news outlet's logo — it will come out garbled or wrong. Use the real official vector marks instead. To source or refresh a logo: download the official SVG from a public logo repository (e.g. Wikimedia Commons) and normalize it — ink it to the page's neutral text color, strip hardcoded width/height, ensure it has a proper viewBox, and namespace any internal IDs so multiple inlined SVGs don't collide when they render together in the press bar. Only claim outlets the brand actually has real placements or licensed mentions for.
