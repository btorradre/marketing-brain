---
name: media-use
description: Covers every step of turning a script, raw footage, or a creative brief into a finished video/audio deliverable — voiceover/TTS, background music, sound effects, transcription, caption authoring and animation, background removal, color grading and LUTs, and structural editing operations (cutting, reframing, ducking, loudness normalization, image/video generation). States the required production order, the concrete quality bars (LUFS targets, volume levels, word-error-rate expectations), the judgment calls a human editor would make, and the asset-reuse discipline that avoids regenerating the same music/SFX/image/logo twice. Use whenever producing or assembling a video or audio asset and you need to know what standard to hit, what order to do things in, and what the format/quality rules are.
---

# Media production standards & workflow

This skill is a production reference, not a single tool's command syntax. It covers the underlying *operation*, its required inputs/outputs, and the judgment calls involved — you supply or find the actual execution mechanism (an API, a media library, `ffmpeg`, a video editor, or code you write) for whatever environment you're in.

## What this covers

- **Audio production** — TTS/voiceover, background music (BGM), sound effects (SFX), and how the three layer together
- **Transcription** — turning spoken audio into word-level timestamps, and the mandatory quality gate on the result
- **Captions** — style detection, per-word emphasis, motion/animation technique, and transcript cleanup
- **Background removal** — subject cutouts, compositing patterns, and where a cutout is the wrong tool
- **Color grading & LUTs** — parametric grades, `.cube` files, and "smart grade" correction of real footage
- **Operations** — cutting, reframing, stitching, transcript-driven editing, audio ducking, loudness normalization, image/video generation, HEVC handling
- **Asset resolution & reuse** — checking for a reusable asset before generating fresh, and what to remember across projects
- **Provider setup** — the shape of credential/provider decisions or local-model tradeoffs
- **Telemetry** — what's worth logging about usage, and how to keep it privacy-respecting

## Core production sequence

Work a piece of video/audio content in this order. Skipping or reordering these steps is the single most common source of rework (captions built off script text instead of real timing, a grade that undoes an intentional color cast, a render that never got loudness-normalized).

1. **Check for a reusable asset first.** Before sourcing or generating any music, sound effect, image, icon, brand logo, voice, or color grade, check whatever asset library or prior-project archive you have access to for something that already fits. Only fetch or generate fresh when nothing reusable fits. See `references/resolve-and-reuse.md`.
2. **Decide the provider path before generating anything paid or account-linked.** If a step depends on a credentialed service (TTS, music, image API), check whether credentials/access are configured. If not, stop and get an explicit choice from the requester: configure the paid/higher-quality path, or proceed with a free/local/offline fallback. Never silently downgrade without surfacing the choice — this applies even to a single one-off request. See `references/setup-providers.md`.
3. **Produce the audio bed first if the piece has narration.** Generate or record the voiceover, then layer sound effects, then background music, in that order — each layer sits under the previous one in the mix (voice > SFX > BGM in terms of what must stay intelligible). See `references/audio-tts-bgm-sfx.md`.
4. **Generate captions from the real word-level transcript, not the script text.** Timing must come from the actual audio, and the transcript must pass a quality check before it's trusted. See `references/transcription.md` and `references/captions.md`.
5. **Apply color grading as a deliberate creative choice** — analyzed against the actual footage, previewed before committing, never a blind "auto-correct" that could undo an intentional look (a warm sunset, a neon color cast). See `references/grading-and-luts.md`.
6. **Do structural edits (cutting, reframing, trimming silence, stitching) non-destructively** inside a composition/timeline tool where possible; only re-encode a physical file when exporting or handing off outside that tool. See `references/operations.md`.
7. **Normalize final loudness** for the target platform as the last step before delivery. See `references/operations.md`.
8. **Register every asset you generate or bring in** — a short description, duration/dimensions, and provenance — so it can be found and reused later. This is what makes step 1 possible on the next project. See `references/resolve-and-reuse.md`.

## Quick task → reference map

| Need | Read |
|---|---|
| Music under a piece | `references/audio-tts-bgm-sfx.md` |
| A whoosh, click, riser, impact, etc. | `references/audio-tts-bgm-sfx.md` |
| A voiceover from a script | `references/audio-tts-bgm-sfx.md` |
| Spoken audio → word-timed transcript | `references/transcription.md` |
| Style and animate on-screen captions | `references/captions.md` |
| Transcript looks garbled or wrong | `references/captions.md` (Transcript Handling) |
| Isolate a talking subject from its background | `references/background-removal.md` |
| Color-correct or stylize footage | `references/grading-and-luts.md` |
| Trim, reframe, stitch, duck audio, normalize loudness, generate images/video | `references/operations.md` |
| Which service/API to use, how to authenticate | `references/setup-providers.md` |
| What to log about usage/reuse | `references/telemetry.md` |
| Not regenerating the same asset twice, remembered preferences | `references/resolve-and-reuse.md` |

## Be proactive — run a media opportunity pass

The person you're producing for usually can't tell which media would lift the piece. You can. When you build or review a composition, do **one** grounded scan and then **ask once** — don't silently add media, and don't nag per asset.

Surface an opportunity only when a concrete signal is present:

| Signal detected | Offer |
|---|---|
| On-screen text or a script with no voiceover | TTS voiceover |
| An emoji or a styled placeholder standing in for an icon | a real icon asset |
| An image that's a placeholder, tiny, or looks upscaled | a better image (or an upscale pass) |
| Hard scene cuts / transitions with no sound | transition SFX |
| A piece over ~10s with no music bed | BGM |
| Footage that reads under/over-exposed or color-cast | a corrective grade (analyze the real footage, preview before committing) |

Rules that keep this a help, not nagware: **grounded, not generic** (no signal, no suggestion); **opinionated and concrete** (propose the specific fix with defaults chosen — the requester approves all/some/none); **once per project** (one consolidated ask, respect "leave it"); **surface, never silently mutate** (this matters most for color grades — a gray-world "correction" ruins an intentional sunset or neon look).

## Non-negotiable rules

These recur across sections and are easy to violate by default behavior:

- **Never generate a sound effect.** SFX is always retrieved from a catalog or matched against a small bundled/local library — there is no "generate an SFX" step.
- **Never load a `.cube` LUT file's raw contents into context.** A 3D LUT is tens of thousands of lines of pure numeric data. Validate it structurally (does it parse, what size) or render a visual preview — never read the body as text.
- **English-only transcription models will translate, not transcribe, non-English audio.** This silently destroys original-language content. Always set language explicitly.
- **A transcript with >20% garbage/music-note tokens is a failed transcription**, not something to build captions from — retry with a larger model, or fall back to manual/external transcription.
- **Color/exposure correction on real footage is a proposal, not an auto-fix.** Present the measured evidence and a bounded suggestion; never silently neutralize footage that may be intentionally warm, cool, or color-cast.
- **A background-removal "hole-cut" plate is not a clean background plate.** The subject's former position is transparent, not filled in — reconstructing what should be there requires an inpainting model, a different technique entirely.
- **Every caption group needs a hard, explicit exit** (fully hidden and non-interactive, not just faded), and only one caption group should ever be visible at once.
- **Audio-reactive treatment is mandatory when the source audio is music** — captions over music that don't respond to it read as disconnected, even subtly.
- **BGM and SFX failures never block a render; voice failure does** (it's the primary content).
- **An agent-initiated call to a paid/metered service gets confirmed first;** a call the requester explicitly asked for just runs. This matters most for anything metered per-use.

## How to use the reference files

Each `references/*.md` file is a deep dive on one topic — load only the one your current task needs. They assume the core sequence and non-negotiable rules above; don't duplicate that context, just execute against the file's specifics. Where a reference gives a concrete `ffmpeg`/CLI command, it's directly runnable and safe to copy; where it describes a "provider," substitute whatever credentialed service or local model you actually have configured for that capability.
