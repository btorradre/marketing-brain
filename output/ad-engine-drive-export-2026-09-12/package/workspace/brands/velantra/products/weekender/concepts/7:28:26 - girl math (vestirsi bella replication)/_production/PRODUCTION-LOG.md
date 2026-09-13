# Production log — "Girl Math" · The Eleanor Weekender

Built 2026-07-28, **fully rebuilt 2026-07-29** after Brooks: *"all of the b-roll you generated
looks like it was 3D. It all looks like a 3D render."* Everything in `final/` is from the rebuild.

## Delivered

| File | Hook | Runtime |
|---|---|---|
| `eleanor-girl-math-v1.mp4` | Girl math is buying one bag… | 38.9s |
| `eleanor-girl-math-hookb.mp4` | The math on this one is easy… | 37.6s |
| `eleanor-girl-math-hookc.mp4` | I stopped travelling with three bags… | 35.5s |

1080×1920, H.264 ~17.7 Mbps, AAC 48kHz. Same body script and 13-slot timeline across all three,
each cut to its own VO's word timings.

## The rebuild — why every slot is new

Two causes of the render look, and the second was the bigger one:

1. **The negative was too weak.** "Raw unedited iPhone photo, available light only, no studio
   lighting" never tells the model not to produce CGI. Replaced with a footer that names what to
   refuse (3D render, CGI, product visualisation, Blender/Octane/Unreal/Keyshot, ray tracing,
   catalogue photography, retouching) and what photographic evidence to require (sensor noise,
   blown highlights, chromatic aberration, JPEG artefacts, imperfect focus, handheld motion blur,
   crooked framing, creased and scuffed leather, visible canvas fibres, dust and fingerprints).
2. **The i2i reference was doing the damage.** `light chocolate 1.webp` is a clean catalogue
   cutout on white and GPT Image 2 inherited its *rendering aesthetic* along with its geometry.
   Every prompt now opens by refusing the attachment's lighting, background, clean edges and
   polished look while keeping its geometry and materials.

Both blocks are now in the `velantra-weekender` skill, the Avatar/B-Roll SOP §3, all seven
`velantra-*-concept` skills, the Segment-Brief-SOP, and this brief's Section 5.

**The five slots that reused the 2026-07-10/11 library clips were also replaced** (new scenes
G, H, I, J, K). Those clips have the same render look, and eleven photographic slots beside five
CGI ones looks worse than either alone. Nothing is reused now.

## Three variants, then pick (standing rule, Brooks 2026-07-29)

32 variants across 12 scenes. Picks and reasons in `picks.json`; every reject is kept in
`keyframes/` beside its pick. **Ten scenes got the full 3 variants; D and E2 got 2** before kie's
error rate ate the rest — picked from what existed rather than block the run.

Two things the rule caught that a single roll would have shipped:

- **I-v1 had a ghost-handle artifact** — a translucent second handle arcing above the real one.
  Invisible unless compared side by side.
- **H and I only had v1/v3 and v2/v3**, so the tile positions I picked from did not map to the
  variant numbers. Worth checking filenames rather than assuming v1/v2/v3 exist.

## Clip QA — 2 of 12 regenerated

- **E2 FAILED.** Omni built the restaurant interior as a **handbag boutique** with lit display
  cases and other bags on the shelves. Wrong location, and it put competitor-looking bags on
  screen. Fixed by naming the interior explicitly (dining tables, napkins, wine glasses, seated
  diners) and banning retail outright. The rejected clip is in `clips/_v1_rejected/`.
- **K FAILED to render** on the first Omni pass (API error, not a quality fail) and passed on
  retry.
- **C's camera tilt runs past the three-bag read by ~7s.** Not a defect in the used range, but
  slot 6's in-point was pulled from 4.4s to 3.4s. Do not cut this clip later than ~6.5s.
- **B holds** through the used range; the older note about proportion drift no longer applies to
  the v3 pick.
- A, D, F, G, H, I, J, E1 held construction across start/mid/end with no mutation.

**Scene K, the open bag, rendered correctly first time** — one-piece flap folded back with the
handle holes, strap slots and gold plate visible on the inner face, both handles standing, wide
leather band constant, no zipper. Given the history on this shot, the planned fallback to the
approved library clip was not needed.

## Engines

| Stage | Engine | Notes |
|---|---|---|
| Keyframes | GPT Image 2 i2i on kie.ai (`gpt-image-2-image-to-image`, 9:16, 2K) | Light Chocolate closed hero. Scene C is text-to-image (no product). Scene K uses the validated pair: a still from the approved fold-back clip + `light chocolate 4.webp`, closed hero deliberately NOT wired. |
| Motion | Google Omni (`gemini-omni-flash-preview`, Interactions API) | 10s / 720×1280, cut ~2–3.5s from the early stretch. Native audio discarded. |
| Voice | ElevenLabs cloned **"Woman Over 40"** on **eleven_v3**, Creative preset (`stability: 0.0`) | One seamless take per version. 3 takes rolled per version, picked on pace. |
| Edit | ffmpeg | 720×1280 → 1080×1920 lanczos, hard cuts, PNG caption overlays. |

## Deviations from the brief

1. **Runtimes are 35.5–38.9s**, set by the read rather than a target. eleven_v3 has no `speed`
   parameter, so pace is controlled only by rolling takes and picking.
2. **Captions carry a soft dark halo.** §6 specced bare white with no outline. Our footage is far
   brighter than Vestirsi's and bare white was illegible on about a third of the slots. The halo
   is a blurred shadow, not an outline, and it disappears on darker frames.
3. **No music bed.** There is no licensed Velantra music in the vault. The cuts ship VO-only.
   **Drop a bed in at ≈ −24 LUFS before this runs.** Everything else is final.

## Gotchas worth keeping

- Omni's Interactions API returns the job handle as **`id`**, not `name`. The request echo lives
  in `steps[0]`, so match `type == "video"` rather than taking the last step.
- **Do not build caption tracks with the ffmpeg concat demuxer.** Per-image `duration` directives
  drifted ~1s late by the end of a 36s reel and floated captions onto the wrong shots. Overlay
  each card with its own `enable='between(t,s,e)'`.
- **Clamp each caption's tail to the next card's start.** Words run almost continuously, so an
  unclamped `end + 0.18` hold double-exposes two cards on top of each other.
- **kie errors on a large fraction of calls** ("Internal Error, Please try again later")
  regardless of pacing, and bursting makes it worse. Fire sequentially with a retry loop. Failed
  tasks are not charged. Never run two generation processes at once — they clobber each other's
  log and drive the error rate up.

## Truth gate

Verified via Shopify Admin API on build day: **The Eleanor Weekender**, handle
`velantra-weekender`, ACTIVE, **$209.99 → $159.99**, Light Chocolate and Army Green both
available, one generous size. PDP still carries "holds three days," "slide into the overhead
bin," "full-grain leather over tightly woven canvas," and "keeps its shape whether it's packed
full or barely at all" — the four claims the script leans on. Recheck before spend.
