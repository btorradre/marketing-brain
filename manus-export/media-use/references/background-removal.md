# Background removal

Goal: produce a transparent-background cutout of a subject (typically a talking-head) so it can be composited over arbitrary background content. The general technique is a human/subject segmentation model (e.g. `u2net_human_seg`, an MIT-licensed segmentation model) run per-frame (for video) or once (for a still image).

## Output format choices

| Format | Use case |
|---|---|
| VP9 video with alpha channel (e.g. `.webm`) | **Default.** Plugs straight into web `<video>` playback with native transparency support; small file size (~1MB per 4 seconds at 1080p) |
| ProRes 4444 (e.g. `.mov`) | Round-tripping through professional editors (Premiere, Resolve, DaVinci); much larger (~50MB per 4 seconds) |
| PNG | Single-image cutout |

## Quality setting

Controls the video encoder's compression quality only — the underlying segmentation quality is fixed regardless. Higher quality keeps the cutout's colors closer to the source, which matters most when compositing the cutout back over its own original footage:

| Preset | Roughly equivalent CRF | When to use |
|---|---|---|
| Fast | ~30 | Iterating quickly, smaller files, looser color match acceptable |
| Balanced | ~18 | Default — visually indistinguishable from source for most uses |
| Best | ~12 | Final master/delivery, tightest possible color match |

## Device/hardware

Prefer whatever hardware acceleration is available (Apple Silicon's Core ML, or CUDA on an NVIDIA GPU) and fall back to CPU. Peak inference memory for a segmentation pass like this is on the order of ~1.5GB.

## Compositing patterns — pick the right one for what's behind the cutout

| Pattern | What sits behind the cutout | Result |
|---|---|---|
| Cutout over a *different* scene (most common case) | Static image, gradient, or unrelated video | Works cleanly — single RGB source for the subject |
| Cutout over its **own original source video** (a "text behind the subject" effect) | The same video the cutout came from | At high/balanced quality, the double-layering is barely visible; at low quality you'll see a visible color shift or edge halo. Use the highest quality setting for anything that will be delivered as a final master |
| Cutout over **a different take of the same person** | Different footage of the same subject | **Produces two overlapping copies of the person visually. Don't do this.** |

## Text-behind-subject technique

A headline or graphic appears to sit behind the presenter. Two non-obvious rules that are easy to get wrong:

1. **Wrap the cutout video in its own container, and animate that container's opacity — not the video element's opacity directly.** Many video-composition frameworks force any actively-playing video clip to full opacity, silently overriding a direct opacity animation on the video element itself. Animating a wrapping element instead avoids this conflict.
2. **Start both the background video and the cutout video decoding from the same zero point in time**, even if the cutout doesn't become visible until later — mounting/decoding a video late introduces a seek-and-warm-up delay that can land a frame or two out of sync with the base footage, visible as a momentary misalignment at the cut point. Reveal the cutout via the wrapper's opacity (rule 1) rather than by delaying when the video itself starts playing.

## Layer separation ("hole-cut plate")

In addition to the subject cutout, you can also produce a second transparent layer — the *inverse* of the cutout — where the surrounding scene is opaque and the subject's silhouette is a transparent hole. This is useful when you want text or graphics to appear to sit *between* the subject and the background (in front of the background, but behind the subject). Both layers can be produced from a single segmentation pass, at roughly double the encoding cost.

| Layer | What's opaque | Use it for |
|---|---|---|
| Subject cutout | The subject; background is transparent | The foreground/top layer |
| "Hole-cut" plate | The surroundings; the subject's silhouette is a transparent hole | The bottom layer — place text/graphics between this and the subject cutout on top |

**This hole-cut plate is not a clean background plate** — the subject's former position is transparent, not filled in.

A single test for whether you need this layer-separation technique at all: *will anything ever need to be visible through the subject's silhouette, in the spot where the subject used to be?* If no, you don't need the hole-cut plate — the subject cutout alone, composited over a different background, is enough.

## Canonical three-layer composite

Plate + arbitrary content + cutout: stack the hole-cut plate at the back, your text/graphics content in the middle, and the subject cutout on top — this lets you ship just the two transparent layers as a reusable pair of assets without needing to also ship the original source video.

## When background removal is the wrong tool

If what's actually wanted is "show the room *without* the person, on its own, with nothing composited on top of the hole" — that's not achievable with a segmentation-based hole-cut, because the hole is transparent, not filled in. That requires a different technique entirely: a video **inpainting** model (e.g. LaMa, ProPainter, E2FGVI) that actually reconstructs what should be behind the removed subject. Don't try to force a segmentation/cutout tool to do this — it can't.
