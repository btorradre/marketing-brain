# Higgsfield Marketplace Cards

Generates marketplace product image cards through Higgsfield: a compliant main listing image, secondary product images, and A+ style content modules. Use this when the request is for marketplace listing images, product detail cards, secondary product images, product infographics, lifestyle listing shots, A+ style content, marketplace image sets, or sales-ready product visuals for a marketplace (e.g. Amazon-style listings). This is NOT the right tool for generic brand product photography without marketplace/listing context (that's a product photoshoot task), for video generation or UGC-style ads, or for training a reusable face/identity model.

This skill is a thin wrapper around the Higgsfield CLI (`higgsfield marketplace-cards create`), which calls Higgsfield's backend prompt enhancer — the backend privately owns the marketplace compliance rules and prompt templates — then submits jobs on the `nano_banana_2` model and returns result URLs. On Manus, treat this as: call the Higgsfield API/CLI with the parameters below rather than hand-writing image-generation prompts yourself.

## How to use this

1. **Set up access.** If the `higgsfield` CLI isn't installed, install it (official installer: `curl -fsSL https://raw.githubusercontent.com/higgsfield-ai/cli/main/install.sh | sh`). If account status shows an authentication error, the user needs to log in (`higgsfield auth login`) before continuing.
2. **Gather inputs.** Prefer having an actual product image to reference. If only text or a URL is available, proceed only once the product details are clear enough to generate from.
3. **Pick a scope or a custom asset list** (see tables below).
4. **Build and run one command**, then deliver only the resulting image URLs with short labels — never paste the enhanced/internal prompt text, job IDs, or internal model names back to the user unless they explicitly ask.

### Scope selection

Use a scope flag for common bundles:

| Scope | Creates |
|---|---|
| `main` | 1 marketplace main image |
| `product-images` | main image + 5 secondary images |
| `aplus` | main image + 7 A+ modules |
| `full-set` | main image + 5 secondary images + 7 A+ modules |

For a custom subset, specify individual assets instead of a scope:

- `main_image`
- `infographic`
- `multi_angle`
- `detail_shot`
- `lifestyle`
- `whats_in_box`
- `aplus_hero_banner`
- `aplus_pain_points`
- `aplus_features`
- `aplus_ingredients`
- `aplus_efficacy`
- `aplus_how_to_use`
- `aplus_endorsement`

### Command shape

```
higgsfield marketplace-cards create \
  --scope <main|product-images|aplus|full-set> \
  --prompt "<short product and listing intent>" \
  [--image <path-or-upload-id>]... \
  [--product_context "..."] \
  [--brand_context "..."] \
  [--category "..."] \
  [--visual_style "..."]
```

Examples:
- Product images: `higgsfield marketplace-cards create --scope product-images --prompt "sparkling peach lemonade can for marketplace listing" --image ./can.png --category "beverage"`
- Full set: `higgsfield marketplace-cards create --scope full-set --prompt "premium skincare serum, clean clinical marketplace visual system" --image ./serum.jpg --brand_context "minimal white and sage palette"`
- Custom subset: repeat the asset flag, e.g. `--asset main_image --asset infographic --asset lifestyle`.
- To add secondary/A+ assets onto an already-completed main image job, reference that completed job instead of regenerating the main image.

## Rules & standards

1. Respond in the user's language.
2. Ask at most one concise confirmation question before running the job.
3. Prefer working from an actual product image; only proceed on text/URL alone once product details are clear.
4. Never write the final image-generation prompt yourself — that's owned by the backend enhancer; you only supply the short intent/prompt and context flags.
5. The final answer should contain only the ready image URLs and short labels — no JSON, no job IDs, no internal model names, no enhanced prompt text, unless explicitly requested.

## Templates & examples

Delivery format:
```
Marketplace cards ready:
- Main image: https://...
- Infographic: https://...
- Lifestyle: https://...
```
