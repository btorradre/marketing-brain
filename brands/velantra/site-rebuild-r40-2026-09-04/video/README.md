# Vivienne media delivery

HyperFrames is banned. The earlier composition code and render configuration have been retired to an inert archive in `../research/retired-video-framework.zip`.

The approved workflow is GPT Image 2 for image production, Google Omni for video generation, and the user's internal video editor only when editing is needed. Simple hero videos go directly from the approved product keyframe to the provider's requested three-second output; there is no timeline, cut, crossfade, re-timing, crop-render or video re-encoding step.

`generate_studio.py` implements direct Google Omni generation. `direct-omni/` stores original provider video files, request records and technical/visual verification. `exports/` contains the files used by Shopify; the hero MP4s must match the approved provider outputs byte for byte. Duration, dimensions and hashes are recorded in `manifest.json`.

The macro uses the unchanged, previously approved Google Omni file `../../products/vivienne/broll/final/O11.mp4`: 10 seconds, 720 × 1280, silent H.264 at 24 fps. Shopify's normal video container handles its display dimensions. It is not passed through a video editor or composition renderer.

Posters are first-frame extractions for loading and reduced-motion playback. Editorial stills remain approved production assets. The generated footage uses Velantra's product references; no reference-brand imagery or footage is included.

The current project instructions are in `AGENTS.md`, with the persistent workspace policy in the root `AGENTS.md`. Existing provider outputs require no service connection to play. Rerunning the generator submits a new paid Google generation; it reads configured credentials without writing them into this project.
