# Higgsfield Product Photoshoot

Generates brand-quality product images through Higgsfield's product-photoshoot prompt enhancement, running on the GPT Image 2 model. This is the entry point for professional brand/product visuals: product photos, studio shots, lifestyle images, Pinterest pins, hero/banner images, social carousels, ad creative packs, virtual try-on/model shots, closeups with hands, levitating/floating/splash or CGI-style product shots, restyles, and seasonal/aesthetic variations. Use it for any product, brand, or paid-social creative request. This is NOT the right tool for no-product text-to-image generation, branded avatar video, marketplace listing cards (Amazon-style A+ content — use the marketplace-cards tool for that), or training a reusable face/identity model.

This skill wraps the Higgsfield CLI (`higgsfield product-photoshoot create`), which calls a backend prompt enhancer holding mode-specific photography vocabulary and structural templates, then submits to the `gpt_image_2` model and returns image URLs. On Manus, treat this as: call the Higgsfield API/CLI with the mode and short intent below — never hand-write the final image-generation prompt yourself.

## How to use this

1. **Set up access.** If the `higgsfield` CLI isn't installed, install it (`curl -fsSL https://raw.githubusercontent.com/higgsfield-ai/cli/main/install.sh | sh`). If account status shows a session/auth error, the user needs to log in (`higgsfield auth login`) before continuing.
2. **Identify which of the 10 modes** fits the request (table and tie-breakers below).
3. **Run a short pre-generation interview** (3–4 short, labeled-option questions — never open-ended) to fill in the gaps context doesn't already answer. Skip any question whose answer is already obvious.
4. **Submit one generation command** with the mode, a short prompt describing intent, any reference images, and count/aspect ratio if non-default.
5. **Deliver only the resulting image URLs**, as a short bulleted list with brief labels. Never show JSON, job IDs, internal model names, or the enhanced prompt text unless explicitly asked.

### Modes

| Mode | When the user wants... |
|---|---|
| `product_shot` | Product on a neutral / studio / catalog background |
| `lifestyle_scene` | Product in a real-world environment, hands, action, atmosphere |
| `closeup_product_with_person` | Tight crop with hands / partial face — beauty application, holding, demonstrating |
| `moodboard_pin` | Vertical 2:3 Pinterest-native aesthetic, moodboard feel |
| `hero_banner` | Wide-format website / email / campaign header |
| `social_carousel` | 3–10 connected slides for Instagram / LinkedIn / Facebook |
| `ad_creative_pack` | Coordinated pack of static ad variants for Meta / TikTok / Pinterest / Google Ads |
| `virtual_model_tryout` | Product worn or used by an AI-rendered model |
| `conceptual_product` | Surreal / CGI-style / levitating / splash / sculptural product |
| `restyle` | Transform an existing image's aesthetic, mood, or seasonal context |

**Mode selection — pick by intent, not surface keyword; when two modes could apply, prefer the more specific one:**
- Product + neutral/clean/white/studio/catalog/e-commerce → `product_shot`
- Product + scene/in-use/kitchen/outdoor/cafe/gym → `lifestyle_scene`
- Hands holding / face with product / beauty application / demonstrating → `closeup_product_with_person`
- Pinterest, pin, vertical pin → `moodboard_pin`
- Hero, banner, website header, landing page, email header, wide format → `hero_banner`
- Carousel, slide post, multi-slide, swipeable → `social_carousel`
- Ads, ad pack, paid social, Meta/TikTok/Pinterest ads → `ad_creative_pack`
- Model wearing, virtual try-on, on body, fashion shoot, lookbook → `virtual_model_tryout`
- Levitating, floating, splash, frozen motion, surreal, CGI, sculptural → `conceptual_product`
- Modify an EXISTING image's aesthetic, mood, or season without changing the subject → `restyle`

**Tie-breakers:**
- "Pinterest pin of my product on a kitchen counter" → `moodboard_pin` (the platform wins)
- "Hero banner showing my product in use" → `hero_banner` (the format wins)
- "Carousel of my product in different scenes" → `social_carousel` (multi-slide wins)
- "Closeup of person applying my serum" → `closeup_product_with_person` (the specific genre wins)

### Pre-generation interview

Ask 3–4 short questions before submitting, always with labeled options, never open-ended. Skip any question whose answer is obvious from context.

**Type A — uploaded a product photo, general "make me images/photoshoots" request:**
1. How many? [1 / 3 / 5]
2. What style/mood? [Clean studio / Lifestyle / Conceptual / With a model / Other]
3. Where will you use them? [E-commerce listing / Instagram / Pinterest / Paid ads / Website hero]
4. Brand colors to match? (skip if obvious)

**Type B — uploaded a product photo, named a specific use case** (e.g. "make ads for my product," "make a Pinterest pin," "make a hero banner"). Mode is obvious; ask only the gaps:
1. How many? (if a multi-output mode)
2. What's the offer/mood/hook?
3. Anything in particular to emphasize?

**Type C — text only, no product photo:**
1. Can you provide a product photo? (preferred — much higher fidelity)
2. If not, describe the product — category, packaging, color, distinctive features.
3. What style? (same options as Type A)
4. Where will you use it?

**Type D — uploaded an existing image, wants a redo / different vibe** → `restyle`
1. What aesthetic? [Clean girl / Cottagecore / Quiet luxury / Dark academia / Y2K / Other]
2. Seasonal context? [Christmas / Valentine's / Halloween / Black Friday / None]
3. What to preserve vs. change? (only if ambiguous)

**Type E — model wearing a product (fashion, accessories)** → `virtual_model_tryout`
1. Model archetype? (suggest 2–3 based on the brand's audience)
2. Environment? [Studio clean / Outdoor natural / Street style / Editorial / Home cozy]
3. Framing? [Full body / Three-quarter / Waist up / Closeup on product area]

**Type F — vague request, unclear subject** (e.g. "make me something cool for my brand"):
1. What product or topic?
2. Goal? [Sell on a marketplace / Build awareness / Run paid ads / Update website]
3. Reference image available?

After getting answers, route back into the relevant Type A–E flow.

### Generation

Build one command per request:

```
higgsfield product-photoshoot create \
  --mode <mode> \
  --prompt "<short user-intent description from interview answers>" \
  [--image <path-or-upload-id>]... \
  [--count <1-10>] \
  [--aspect_ratio <override>]
```

Examples:
```
higgsfield product-photoshoot create \
  --mode lifestyle_scene \
  --prompt "bottle of cold-brew on a sunlit kitchen counter, IG feed" \
  --image bottle.jpg \
  --count 3
```
```
higgsfield product-photoshoot create \
  --mode moodboard_pin \
  --prompt "vertical pin for my candle brand, cottagecore mood" \
  --image candle.jpg
```
```
higgsfield product-photoshoot create \
  --mode restyle \
  --prompt "Christmas version, quiet-luxury aesthetic" \
  --image existing-shot.jpg
```

`--image` accepts a local file path (auto-uploaded) or an existing upload ID; repeat the flag for multiple references.

## Rules & standards

1. Be concise — print only image URLs in the final reply.
2. Detect the user's language and respond in it; mode names and flags stay in English.
3. Ask at most 4 short questions before submitting, always with labeled options.
4. Skip questions whose answers are obvious from context (an uploaded image, prior conversation, known brand info).
5. Never write the `gpt_image_2` prompt yourself — the backend enhancer assembles it.
6. `--count 3` (or any N) returns N distinct variants — the backend varies preset, lighting, angle, and palette across them; they will not be near-duplicates.
7. For `social_carousel` and `ad_creative_pack`, count = number of slides/variants, and the visual system is locked consistently across the whole set automatically.
8. Resolution: use `2k` for every product-photoshoot job.
9. Aspect ratio: a sensible default is chosen per mode automatically. Only override it if the user explicitly asks for something different. Allowed values: `1:1`, `4:5`, `5:4`, `3:4`, `4:3`, `2:3`, `3:2`, `9:16`, `16:9`.
10. Never bypass the prompt enhancer by calling the underlying image model directly — it produces noticeably worse output than going through `product-photoshoot create`.
11. Never paste the assembled/enhanced prompt back to the user.

### Common mistakes to avoid

- Asking more than 4 interview questions in a single message.
- Picking the wrong mode (e.g. `product_shot` when the user actually wants a Pinterest pin).
- Bypassing the prompt enhancer.
- Pasting the assembled prompt back to the user instead of just the URLs.
- Using a mode value that isn't in the table above.

## Templates & examples

Delivery format:
```
3 lifestyle shots ready:
- https://cdn.higgsfield.ai/.../job_abc.jpg
- https://cdn.higgsfield.ai/.../job_def.jpg
- https://cdn.higgsfield.ai/.../job_ghi.jpg
```
