---
name: velantra-product-launch
description: Historical notes on a superseded Velantra product-launch process — kept only as standing lessons for anyone building or maintaining a similar product-launch pipeline. Not an active workflow. Use only if you need the reasons the old approach was replaced.
---

# Velantra Product Launch (superseded reference)

This document is a thin pointer, not an active skill. The source folder it was converted from contains a note stating that this older product-launch process was superseded by a newer, unified product-launch workflow, and that the old folder is being kept only for a historical launch-state record (a prior bag launch). There is no active process content to preserve here — only the reasons the old approach was replaced, which are useful as standing lessons if you build or maintain a similar product-launch process elsewhere.

## Why the old approach was replaced

- Product image-to-image generation was being run through a different image model than the one standardized on for all product photography — the standing rule is that all product image-to-image generation should go through GPT Image 2 specifically, not a substitute model.
- Editorial/lifestyle image generation was calling out to a command-line tool that was broken/unauthenticated in the environment it ran in — a reminder to avoid hard dependencies on tools that require interactive browser login in an automated pipeline.
- Every script depended on a networking library that had no certificate bundle available in that environment, requiring a manual workaround just to make HTTPS requests work at all — the replacement approach uses a more robust HTTP client throughout.
- Generated images were uploaded without any colorway/variant tagging, which caused product photo galleries to leak images across different colorways on the live product page.
- The page-builder for this process cloned a hardcoded content template that had brand-banned origin claims baked into it (fabricated claims like a specific tannery or country of manufacture, or a fabricated leather-grading certification). The replacement approach clones a live, already-approved template and explicitly strips any inherited claims before publishing.
- Store/theme identifiers were resolved in a way that assumed a specific theme version that had since been replaced by a republish.

## Rules & standards

If rebuilding a product-launch process from scratch, carry these lessons forward:
- Standardize on one image generation model for all product photography and stick to it.
- Don't build automated pipelines around tools that require interactive/browser-based login.
- Use an HTTP client that works out of the box in the target environment, without manual certificate configuration.
- Tag every uploaded product image with its colorway/variant so galleries never mix colorways.
- Never hardcode marketing claims into a page template — clone from an already-approved live page and actively strip any claims that shouldn't carry over, especially unverifiable origin/certification claims.
- Re-verify store/theme identifiers at launch time rather than assuming a previously recorded one is still current.
