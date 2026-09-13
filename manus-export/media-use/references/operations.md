# Operations: cutting, reframing, ducking, loudness, generation

General guidance for structural media edits: cutting, reframing, stitching, silence-trimming, ducking, loudness normalization, and generation of images/video. The underlying tool for most of these is a general-purpose media-processing tool like **ffmpeg** (assumed available) — the commands below are illustrative and directly runnable; adapt to whatever tool you actually have.

## Cut / trim — keep a slice of a file

```bash
ffmpeg -i in.mp4 -ss 00:00:12 -to 00:00:20 -c copy out.mp4   # keep 0:12-0:20, no re-encode
```

Prefer trimming *inside* your composition/timeline tool (playing only a sub-window of a clip, non-destructively) over cutting a physical file whenever possible — only cut a physical file when you need to export or hand the result off outside that tool.

## Reframe / crop — change aspect ratio

```bash
# 16:9 -> 9:16, centered crop
ffmpeg -i in.mp4 -vf "crop=ih*9/16:ih,scale=1080:1920" out.mp4
```

For a non-destructive crop within a composition/timeline tool, prefer a render-time crop/mask (e.g. a CSS `clip-path` if your renderer is web-based) over re-encoding — it leaves the source file untouched.

## Montage / stitch — join clips together

```bash
printf "file '%s'\n" a.mp4 b.mp4 c.mp4 > list.txt
ffmpeg -f concat -safe 0 -i list.txt -c copy out.mp4
```

## Silence-cut / highlight extraction — trim dead air or find the best moment

```bash
auto-editor in.mp4 --edit audio:threshold=4% -o tight.mp4   # remove silence automatically
scenedetect -i in.mp4 detect-adaptive list-scenes            # detect scene/shot boundaries
```

## Quality-tiered transforms

Some operations have both a free/local option and a higher-quality paid/API option; when both exist, it's honest practice to offer a **side-by-side comparison** so the requester can choose rather than silently picking one for them:

| Operation | Free/local option | Higher-quality paid option |
|---|---|---|
| Background removal | A local segmentation model (see `references/background-removal.md`) | A premium API-based background-removal service |
| Upscaling | A local super-resolution model (e.g. Real-ESRGAN) | — |
| Lip-sync / dubbing | — | A premium video-dubbing/lipsync API |
| Translation | — | A premium video-translation API |

After running any operation like this, log the derived output into your asset manifest (with its provenance — what it was derived from and how) so it's discoverable for future reuse (see `references/resolve-and-reuse.md`).

## Text-based editing via transcript

Rather than manually scrubbing through footage to find cut points, you can compile an edit decision list directly from a word-level transcript plus a set of cut instructions: specific time ranges to remove, filler words to strip (e.g. "um", "uh", "like"), and/or a minimum silence-gap threshold to auto-cut. This turns "edit out these words/pauses" into an exact list of kept segments that a rendering step then encodes.

It's good practice to generate and review the *planned* kept-segments list before committing to the final encode.

## Audio ducking (lowering music/background under narration)

Two approaches depending on context:

- **Declare it inside your composition/timeline tool** (preferred when your final output stays inside that tool) — express ducking as a set of volume keyframes (e.g. music drops to ~0.15 at the moment narration starts, and returns to its base ~0.6 level after narration ends) applied directly on the timeline, leaving the source audio file itself untouched.
- **Bake it into an exported/standalone audio file** (only needed when the asset is leaving your composition pipeline as a final rendered file) — a sidechain-compression technique automatically ducks one track based on the level of another:

```bash
ffmpeg -i bgm.mp3 -i voice.wav \
  -filter_complex "[0][1]sidechaincompress=threshold=0.03:ratio=8:attack=200:release=400[ducked]" \
  -map "[ducked]" bgm.ducked.wav
```

Prefer declaring ducking inside the composition; only bake it into an exported file when the asset is truly leaving the pipeline as a standalone deliverable.

## Publish loudness normalization

A two-pass approach: first measure the actual loudness of your final mix, then apply a normalization pass using those measured values plus your target loudness.

```bash
# pass 1: measure
ffmpeg -i mix.wav -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null -

# pass 2: apply, using the measured_* values reported by pass 1
ffmpeg -i mix.wav \
  -af loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=<input_i>:measured_TP=<input_tp>:measured_LRA=<input_lra>:measured_thresh=<input_thresh>:offset=<target_offset>:linear=true:print_format=summary \
  mix.social.wav
```

**Loudness targets:**
- **Social media platforms:** target integrated loudness **-14 LUFS**, true-peak ceiling -1.5 dB, loudness range 11.
- **Podcasts:** target integrated loudness **-16 LUFS**, same true-peak ceiling and loudness range settings.

(Same two-pass structure for podcasts — just swap `I=-14` for `I=-16` in both passes.)

## Generating images

When nothing suitable exists to reuse or retrieve from a stock/catalog source, generate. Prefer a local, private, offline-capable image model (a FLUX-class diffusion model, sized to whatever RAM you actually have) as the default; fall back to a cloud image-generation service for higher quality when needed (an explicit "make it better" request, or when no local model fits your hardware).

Illustrative RAM tiers for a FLUX-class local model:

| Tier | Model class | Approx. RAM needed | Notes |
|---|---|---|---|
| Medium | A 4-bit-quantized "schnell"/fast FLUX variant | ~8GB | Fast (~20s at 512px on a 24GB machine in testing); a low-RAM/memory-conscious mode is close to mandatory at this tier — without it, a modest-resolution run was observed swap-thrashing to ~90 minutes on 24GB, vs. ~20 seconds with it enabled |
| Large | A larger, still-quantized FLUX-class model | ~32GB | Higher quality, fully resident in memory |
| X-large | A top-tier open image model (e.g. Qwen-Image class) | ~64GB+ | Top quality, only practical on high-RAM machines |

Pick the largest tier that comfortably fits your available RAM; a cloud fallback should engage automatically only when no local tier fits (or explicitly on request for better quality).

## Generating video

For a script-driven talking-presenter video, a premium avatar-video API (which handles lip-sync and voice generation from a script directly) is generally the default/best-quality path when available; a local text-to-video generative model (e.g. an LTX-class model) is the fallback when the premium path is unavailable/uncredentialed, or when explicitly working offline-only.

Treat these as **non-substitutable outputs, not a quality ladder** — a real synthesized presenter and a generic generative video clip are different kinds of asset, so falling back should be understood as "the premium service wasn't reachable," not "a slightly worse version of the same thing."

For image-to-video (animating a still photo of a person into a lip-synced talking clip), a premium avatar-video API can typically take any photo of a person plus a script (or pre-recorded audio) directly — no separate "avatar creation" step required for a one-off use, though creating a persistent reusable avatar first is worth it if you'll reuse the same likeness across many scripts.

Common fields such an API typically exposes: `title`, `resolution` (`4k`/`1080p`/`720p`), `aspect_ratio`, `remove_background`, `background`, `voice_settings`, `motion_prompt` + `expressiveness` (for photo-avatar animation), and a webhook callback for async completion. Read the current API schema rather than trusting a remembered field list — these change.

## HEVC/H.265 source footage

Modern rendering pipelines typically pre-decode all input video regardless of codec, so HEVC sources generally don't need conversion just to render. Some preview tooling may auto-generate and cache an H.264 proxy on first use for smoother scrubbing; if you need a proxy manually (e.g. auto-proxying isn't available in your environment), transcode explicitly:

```bash
ffmpeg -i in.mp4 -c:v libx264 -crf 18 proxy.mp4
```
