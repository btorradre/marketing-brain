# Ad Replicator

This document describes a process for taking a reference ad image (static, native, or branded) and producing a brand-adapted version of it: analyze why the reference works, adapt the concept for a specific brand using that brand's research/voice documents, write an image-to-image generation prompt, and generate the adapted image. Use this whenever someone wants to replicate, adapt, or riff on a reference ad creative for a specific brand and product.

## GOLDEN NUGGET DOCTRINE (apply first)

Before any hook, angle, or adaptation is produced, name the golden nugget: the single most emotionally loaded deep frame in the reference — the real motive that makes buyers act, never the surface theme. Topic is not motive: "memory loss" is a topic; "I thought I was getting dementia just like my mum did" is the frame. Surface angles buy mild curiosity; deep frames trigger identification so strong the viewer feels caught. For every candidate angle ask: is this the topic, or is this the motive? If it's the topic, dig one layer deeper. State the golden nugget in one explicit sentence before adapting the ad — including when only analyzing a reference rather than writing new copy.

## Pipeline overview

```
Reference Ad Image(s)
    |
    v
[Stage 1] Ad analysis (why it works, elements, angle, composition, visual style)
    |
    v
[Stage 2] Brand adaptation strategy (uses brand research/voice documents)
    |
    v
[Stage 3] Image-to-image generation (reference image + product reference photos + adaptation prompt -> branded image)
    |
    v
[Output] Generated adapted ad image(s)
```

## Required inputs

Before starting, collect:

1. **Reference ad image(s)** — one or more images to replicate/adapt (PNG, JPG, JPEG, or WEBP).
2. **Brand name** — which brand this is for. You need that brand's research documents (avatar research, voice guidelines, product descriptions) and reference photos of the actual product to work from.
3. **"Why it works" analysis (optional)** — if the user already has their own breakdown of why the reference works, use it. Otherwise generate the analysis yourself in Stage 1.
4. **Adaptation notes (optional)** — extra direction on how to adapt (e.g. "keep the same composition but swap for our product and avatar," "make it more native/less branded," "change the setting to a kitchen").
5. **Product reference images (optional)** — actual photos of the product being advertised, so the image generator can render it accurately. Without these, a generated product will not match the real thing.
6. **Number of variations (optional)** — how many adapted versions to generate per reference. Default to 1 unless told otherwise.

## How to use this

### Stage 1 — Ad analysis

Look closely at the reference ad image and produce a structured breakdown covering:
- **Why it works** — the persuasion mechanics that make this ad effective.
- **Visual elements** — every visual element catalogued (layout, colors, typography, imagery, props).
- **Composition** — how the image is structured (split layout, centered, grid, etc.).
- **Angle** — the persuasion angle (authority, social proof, curiosity gap, fear, aspiration, etc.).
- **Audience** — who this ad targets (demographics, psychographics, awareness level).
- **Product presence** — whether the reference contains a product, and what kind.
- **Text content** — any text/copy visible in the image.
- **Style** — visual style (native/UGC, branded/polished, editorial, clinical, lifestyle).
- **Color palette** — dominant colors and their psychological function.
- **Mood** — the emotional tone of the image.

### Stage 2 — Brand adaptation strategy

Using the Stage 1 analysis plus the target brand's research documents (avatar, mechanism, voice, visual identity) and product context, write a detailed adaptation plan that preserves what works while adapting it for the target brand. Then write the actual image-generation prompt for Stage 3.

The prompt should **preserve**:
- Composition and layout (1:1 structural match to the reference)
- Visual style and mood
- Persuasion mechanics and angle

The prompt should **adapt**:
- The product to the target brand's actual product (if a product is present)
- Avatar demographics to the target brand's audience
- Colors/branding to the target brand's palette (if the reference is a branded style)
- Setting/environment to match the target brand's avatar's world
- Any text/copy elements to the target brand's messaging

Pull enough brand knowledge into this step that the adaptation reflects the real avatar, mechanism, voice, and visual identity — not a generic guess.

### Stage 3 — Image-to-image generation

Use an image-to-image capable image generation model (a model that can take a reference image plus a text prompt and produce an edited/transformed version, e.g. Gemini's image model or an equivalent image-editing model). For each reference image:

- Send the **reference image** itself plus the brand adaptation prompt from Stage 2, so the model transforms the reference directly rather than generating from scratch.
- **Smart product inclusion**: only include a photo of the actual product when the reference image actually contains a product (as detected in Stage 1). If the reference has no product, instruct the model explicitly: "Do NOT add any product to this image."
- If real product reference photos are available and the reference contains a product, include those images so the generator can replicate the exact product appearance rather than inventing one.
- If the reference shows a competitor or "villain" product in a negative context, replace it with a generic version — never the brand's own product.
- Enforce 1:1 composition replication in the prompt: "Replicate the composition 1:1 — do not invent or add elements that are not in the original."
- If the image-to-image call fails, fall back to a text-only generation using the adaptation prompt alone.

### Output

Organize outputs as:
- An analysis file per reference (the full Stage 1 + Stage 2 output, in JSON or plain text)
- The generated adapted image(s) per reference (multiple files if variations were requested)
- A short summary noting which references succeeded/failed and why

## Rules & standards

- **Smart product inclusion is mandatory** — never blindly inject a product image into every generation; check first whether the reference actually shows a product.
- **1:1 composition replication** — do not invent or add elements not present in the original reference.
- **Competitor/villain products are never replaced with the brand's own product** — use a generic substitute instead, to avoid implying the brand endorses or resembles a specific competitor's imagery inappropriately.
- **Brand knowledge must come from real research documents**, not assumptions — read the brand's actual avatar research, voice guide, and product descriptions before adapting.
- Retry failed generations a few times before giving up on that reference; save progress incrementally so a rerun doesn't have to start over.
