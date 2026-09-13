---
type: session-transcript
date: 2026-03-30
session_id: local_e8fae75e-6c9c-4535-a3b4-5d5708aaaa44
title: "Create product images for Solorna sandals"
tags:
  - session-log
  - transcript
  - creative-production
  - product-photography
  - img2img
  - solorna
---

# Session Transcript: Create product images for Solorna sandals

**Date:** 2026-03-30
**Session ID:** local_e8fae75e-6c9c-4535-a3b4-5d5708aaaa44
**Status:** idle

---

[assistant] Attempted to use native image factory workflow — wrong approach for this task.

[user] You dumb bitch Dont use native image factory. We need to use image to image here

[assistant] You're right — my mistake. Text-to-image won't match the actual product. We need to feed the existing product photos from the TikTok listing into Gemini as reference images and use image-to-image to restyle them in the Tory Burch aesthetic. Two options: modify existing n8n workflow for img2img, or build a new one.

[user] Use gemini api: [API key provided]

[assistant] Got it. Grabbed product image URLs from TikTok page via JavaScript extraction. Attempted to map each color to its product image by clicking through swatches.

[user] Just give me the prompts and I'll create the product images myself

[assistant] Wrote img2img prompts — 6 colors (beige, black, brown, coffee, khaki, sky blue) x 4 Tory Burch perspectives (angle, side, detail, overhead). Saved as single JSON file.

[user] Separate them by color so its easy for me to copy and paste

[assistant] Split into 6 separate files — one per color.

[user] Remove the logo from all of the images

[assistant] Updated all 6 files with logo removal baked into every prompt — replace existing brand logos on chain hardware with clean unbranded polished metal.

[user] Fix the prompts so they generate new images, not old ones

[assistant] Rewrote all prompts: "Using this image as a reference for the product's exact design, materials, shape, and color, generate a brand new..." instead of "Restyle."

[user] make them all json prompts

[assistant] Converted all 6 files to clean JSON arrays with prompt_id, shot, prompt, and aspect_ratio fields. Saved as .json files.
