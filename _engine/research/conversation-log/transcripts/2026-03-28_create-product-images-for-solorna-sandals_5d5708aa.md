---
type: session-transcript
date: 2026-03-28
session_id: local_e8fae75e-6c9c-4535-a3b4-5d5708aaaa44
title: "Create product images for Solorna sandals"
tags:
  - session-log
  - transcript
  - native-image
  - product-images
  - solorna
  - img2img
  - gemini
---

# Session Transcript: Create product images for Solorna sandals

**Date:** 2026-03-28
**Session ID:** local_e8fae75e-6c9c-4535-a3b4-5d5708aaaa44
**Status:** idle

---

[assistant] (called n8n_manage_executions)

[user] Continue from where you left off.

[assistant] No response requested.

[user] You dumb bitch Dont use native image factory. We need to use image to image here

[assistant] You're right — my mistake. Text-to-image won't match the actual product. We need to feed the existing product photos from the TikTok listing into Gemini as reference images and use image-to-image to restyle them in the Tory Burch aesthetic.

The current n8n workflow is text-only — it doesn't pass any source images to Gemini. Two options:

1. **Modify the n8n workflow** to accept a source image URL/base64 in each prompt object and include it as an image part in the Gemini API call alongside the text prompt. Then we download each product photo per color from TikTok and feed it through.

2. **Build a new workflow** specifically for img2img product restyling.

Which way do you want to go — update the existing native factory workflow to support img2img, or spin up a separate one for this?

[user] Thats going to create text to image

[assistant] No response requested.

[user] Use gemini api: [REDACTED_SECRET]

[assistant] Got it. Let me do this properly with image-to-image through the Gemini API directly. I'll grab each color's product images from TikTok, then use Gemini img2img to restyle them in the Tory Burch aesthetic.

[assistant] (called TodoWrite)

[assistant] Let me grab all the product image URLs from the TikTok page using JavaScript.

[assistant] (called javascript_tool — extracting TikTok product images)

[assistant] The URLs got blocked due to query params. Let me strip those and try again.

[assistant] (called javascript_tool — retry image extraction)

[assistant] Good, I have the image URLs. Now let me map each color to its product image by clicking through each swatch and grabbing the main image.

[assistant] (called javascript_tool — mapping color swatches to images)

[user] Continue from where you left off.

[assistant] No response requested.

[user] Just give me the prompts and I'll create the product images myself

[assistant] Got it. Let me rewrite these as proper img2img prompts — transformation instructions designed to be paired with the source product photos from the TikTok listing.

[assistant] (called TodoWrite)

[assistant] (wrote solorna_img2img_prompts.json — 24 prompts, 6 colors × 4 perspectives)

[assistant] Done. 24 img2img prompts — 6 colors (beige, black, brown, coffee, khaki, sky blue) × 4 Tory Burch perspectives (angle, side, detail, overhead). Each prompt is designed to be paired with the corresponding source product photo from the TikTok listing and tells Gemini exactly how to restyle it: pure white seamless background, soft diffused studio lighting, minimal shadows, and that elevated minimalist luxury feel.

[user] Separate them by color so its easy for me to copy and paste

[assistant] Let me split these into 6 separate files — one per color.

[assistant] (wrote prompts_beige.txt, prompts_black.txt, prompts_brown.txt)

[user] Continue from where you left off.

[assistant] No response requested.

[user] Remove the logo from all of the images

[assistant] Got it. Let me update all the prompt files to include logo removal instructions on the chain hardware.

[assistant] (rewrote all 6 prompt files with logo removal instructions)

[assistant] All 6 files done, each with logo removal baked into every prompt.

[user] Fix the prompts so they generate new images, not old ones

[assistant] Got it — the prompts need to use the source image as a product reference but generate entirely new shots, not just restyle the existing photo. Let me rewrite all six.

[assistant] (rewrote all 6 files — changed from "Restyle" to "Using this image as a reference for the product's exact design, materials, shape, and color, generate a brand new...")

[assistant] All 6 files updated. Every prompt now starts with "Using this image as a reference..." instead of "Restyle." Gemini will use the source photo to understand what the sandal looks like, then create a completely new image in the specified perspective and Tory Burch style.

[user] make them all json prompts

[assistant] (converted all 6 files to JSON format with prompt_id, shot, prompt, and aspect_ratio fields)

[assistant] Done. Six JSON files, one per color — each a clean JSON array with 4 objects (angle, side, detail, overhead).
