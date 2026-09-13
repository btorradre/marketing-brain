---
name: nano-banana
description: Generates AI images using the nano-banana command-line tool, which wraps Google's Gemini image models (Gemini 3.1 Flash Image Preview by default, Gemini 3 Pro available). Handles multi-resolution output (512px-4K), aspect ratio control, reference-image-driven editing and style transfer, a green-screen workflow for transparent assets, cost tracking, and exact-dimension control. Use when asked to "generate an image", "create a sprite", "make an asset", "generate artwork", or any image generation task for UI mockups, game assets, video visual elements, or marketing materials.
---

# nano-banana

AI image generation CLI. Default model: Gemini 3.1 Flash Image Preview ("Nano Banana 2"); Gemini 3 Pro is available for higher quality.

## First-Time Setup

Requires Bun (a JavaScript runtime). If Bun isn't installed:
```bash
curl -fsSL https://bun.sh/install | bash
```

Then install the tool:
```bash
# 1. Clone the repo
git clone https://github.com/kingbootoshi/nano-banana-2-skill.git ~/tools/nano-banana-2

# 2. Install dependencies
cd ~/tools/nano-banana-2 && bun install

# 3. Link globally (creates the `nano-banana` command via Bun — no sudo needed)
cd ~/tools/nano-banana-2 && bun link

# 4. Set up the API key
mkdir -p ~/.nano-banana
echo "GEMINI_API_KEY=<your key>" > ~/.nano-banana/.env
```

If `bun link` fails or the command isn't found afterward, fall back to a manual symlink:
```bash
mkdir -p ~/.local/bin
ln -sf ~/tools/nano-banana-2/src/cli.ts ~/.local/bin/nano-banana
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

Get a Gemini API key at https://aistudio.google.com/apikey.

Once set up, images are generated with: `nano-banana "prompt" [options]`. Default behavior: 1K resolution, Flash model, output written to the current directory.

## Core Options

| Option | Default | Description |
|--------|---------|-------------|
| `-o, --output` | `nano-gen-{timestamp}` | Output filename (no extension) |
| `-s, --size` | `1K` | Image size: `512`, `1K`, `2K`, or `4K` |
| `-a, --aspect` | model default | Aspect ratio: `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, etc. |
| `-m, --model` | `flash` | Model: `flash`/`nb2`, `pro`/`nb-pro`, or any raw model ID |
| `-d, --dir` | current directory | Output directory |
| `-r, --ref` | - | Reference image (repeatable — use multiple times for multiple references) |
| `-t, --transparent` | - | Generate on a green screen, then remove the background automatically |
| `--api-key` | - | Gemini API key (overrides env var / config file) |
| `--costs` | - | Show a running cost summary |

## Models

| Alias | Model | Use when |
|-------|-------|----------|
| `flash`, `nb2` | Gemini 3.1 Flash | Default. Fast, cheap (~$0.067 per 1K image) |
| `pro`, `nb-pro` | Gemini 3 Pro | Highest quality is needed (~$0.134 per 1K image) |

## Cost by Size

| Size | Cost (Flash) | Cost (Pro) |
|------|-------------|------------|
| `512` | ~$0.045 | Flash only |
| `1K` | ~$0.067 | ~$0.134 |
| `2K` | ~$0.101 | ~$0.201 |
| `4K` | ~$0.151 | ~$0.302 |

## Supported Aspect Ratios

`1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3`, `4:5`, `5:4`, `21:9` — set with the `-a` flag, e.g. `nano-banana "cinematic scene" -a 16:9`.

## How to Use This

### Basic generation
```bash
nano-banana "minimal dashboard UI with dark theme"
nano-banana "cinematic landscape" -s 2K -a 16:9
nano-banana "quick concept sketch" -s 512
```

### Model selection
```bash
# Default (Flash — fast, cheap)
nano-banana "your prompt"

# Pro (highest quality)
nano-banana "detailed portrait" --model pro -s 2K
```

### Reference images (editing / style transfer)
```bash
# Edit an existing image
nano-banana "change the background to pure white" -r dark-ui.png -o light-ui

# Style transfer with multiple references
nano-banana "combine these two styles" -r style1.png -r style2.png -o combined
```

Reference order matters:
- The **first** reference is the primary style/content source.
- Additional references are secondary influences.
- The **last** reference controls output dimensions, if you're using the blank-image trick below.

### Transparent assets
```bash
nano-banana "robot mascot character" -t -o mascot
nano-banana "pixel art treasure chest" -t -o chest
```
The `-t` flag automatically instructs the model to generate on a green screen, then uses FFmpeg's `colorkey` + `despill` filters to key out the background and clean green spill from edge pixels — producing pixel-perfect transparency with no manual prompt engineering. Requires `ffmpeg` and `imagemagick` to be installed (e.g. `brew install ffmpeg imagemagick` on macOS).

### Exact output dimensions
To force a specific pixel dimension:
1. Pass your style/content reference as the first `-r`.
2. Pass a blank image sized to your target dimensions as the last `-r`.
3. State the target dimensions in the prompt text itself.

```bash
nano-banana "pixel art character in style of first image, 256x256" -r style.png -r blank-256x256.png -o sprite
```

### Cost tracking
Every generation is logged to a local cost file (`~/.nano-banana/costs.json`). View a running summary at any time with:
```bash
nano-banana --costs
```

## API Key Resolution Order

The CLI resolves the Gemini API key by checking, in order:
1. The `--api-key` flag
2. The `GEMINI_API_KEY` environment variable
3. A `.env` file in the current directory
4. A `.env` file next to the CLI script itself
5. `~/.nano-banana/.env`

## Use Cases

- Landing page assets — product mockups, UI previews
- Image editing — transforming existing images via prompt
- Style transfer — combining multiple reference images
- Marketing materials — hero images, feature illustrations
- UI iteration — quickly generating design variations
- Transparent assets — icons, logos, mascots with no background
- Game assets — sprites, backgrounds, characters
- Video production — visual elements for video compositions

## Prompt Examples

```bash
# UI mockups
nano-banana "clean SaaS dashboard with analytics charts, white background"

# Widescreen cinematic
nano-banana "cyberpunk cityscape at sunset" -a 16:9 -s 2K

# Product shots with Pro quality
nano-banana "premium software product hero image" --model pro

# Quick low-res concept
nano-banana "rough sketch of a robot" -s 512

# Dark mode UI
nano-banana "Premium SaaS chat interface, dark mode, minimal, Linear-style aesthetic"

# Game assets with transparency (green screen auto-prompted)
nano-banana "pixel art treasure chest" -t -o chest

# Portrait aspect ratio
nano-banana "mobile app onboarding screen" -a 9:16
```
