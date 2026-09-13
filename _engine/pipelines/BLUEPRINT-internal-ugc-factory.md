# INTERNAL UGC FACTORY — build blueprint

**Goal:** our own localized InfiniteUGC. Script in → finished, captioned, multi-scene ad out, one command, resumable, no dashboard theater. Their product is orchestration around public models we already call (teardown 2026-08-03: Next.js/Supabase/Railway/Whop wrapper; "no stitching" is a UX claim). The gap is middleware, not models — so we build exactly the middleware and skip the SaaS chrome.

**Prime directive carried over from production runs (2026-08-05/06):**
1. **One-Take Audio Law** — audio is ONE ElevenLabs take for the whole ad, split at sentence boundaries, laid back over the assembled video. The video is assembled; the audio never is.
2. **Keyframe-first, never chain** — every scene's keyframe is authored from the same reference set; no clip ever seeds from the previous clip's last frame. (`reference_multishot_vs_firstframe_fork`: competitors batch-author keyframes from one ref; chaining inherits drift. Measured: background sim 0.53 chained/declining vs 0.86 unchained/flat; race change by ~seg 10.)
3. **Extend `scene_replicator.py`, don't fork it.** It is THE universal runner and already keyframe-first. Skills stay thin profiles over the engine.

---

## Layer map — what exists vs what gets built

| Layer | Their version | Ours | Status |
|---|---|---|---|
| 1. Scene parse | "Nebula agent" LLM scene map | Claude writes `job.json` scene map (talking / broll / product per scene) | **exists** — this is what we already do by hand; formalize the schema |
| 2. VO | ElevenLabs + timestamps | ElevenLabs `with-timestamps`, one call, whole script | **exists** (`aiugc-longform` 3a, key in .env) |
| 3. Audio chunking | server-side | `chunk_vo_beats.py` sentence-safe mode, cutting the AUDIO at word timestamps | **small build**: today it chunks text; add `--timestamps vo_timestamps.json` to emit chunk WAVs |
| 4. Keyframes | Nano Banana / Seedream | GPT Image 2 i2i via kie (house law for product), batch-authored from one ref set | **exists** (`scene_replicator.py`) |
| 5. Video render | Kling 31/s · Seedance 31/s · Omni 20/s · HeyGen 16/s, per-scene routing | Same models minus HeyGen: **Seedance 2.0 (kie)** for dialogue scenes, **Omni** for b-roll/scenes ≤10s, **Kling 3.0** where its look wins | **exists** as separate runners; **build**: one `render_scene(scene, engine)` abstraction so engines swap per scene |
| 6. Lip-sync | HeyGen for avatars | **Tier 1:** Seedance generation-time via `reference_audio_urls` (dialogue scenes). **Tier 2:** fal sync.so post-pass for Omni-rendered talking shots | Tier 1 **exists**; Tier 2 **build** (~a day: fal API, FAL_API_KEY on hand) |
| 7. Assembly | server concat + caption burn | `trim_deadspots.py` (fine trim, re-encoded concat) + lay full VO + caption burn from EL timestamps (Pillow → ffmpeg, per `reference_burned_caption_overlays`) | trim/concat **exists**; **build**: VO-overlay step + caption burner integration |
| 8. QA | none visible | `pick_take.py` accuracy gate (word-level, numeral/proper-noun tolerant) + `scan_consistency.py` (identity/background outliers) | **exists** — wire in as automatic post-render gates |
| 9. Queue/resume | Railway job queue, idempotency | SQLite state file + per-scene status (`pending/rendering/syncing/done/failed`), idempotent re-runs, resumable after any crash | **build** — the core of the project. `run_unchained.sh` proved the pattern; formalize in Python inside scene_replicator |
| 10. Billing/dashboard | Whop, Supabase, editor | **skip** — internal tool. Progress = tail the state file; Launchpad (localhost:8787) can read it later | not needed |

## The build list, in order

1. **`factory.py` job runner** (Layer 9, ~2 days) — takes `job.json`, drives layers 2→8 with SQLite state, per-scene idempotency keys, retry with backoff (transient Omni 400s, kie polling), `--resume`. This is 80% of what makes it "a product" instead of a session.
2. **Audio-chunk mode for `chunk_vo_beats.py`** (Layer 3, ~half day) — split the real WAV at sentence-boundary timestamps; emit `chunk_NN.wav` + manifest. Silence-pad short chunks to each engine's container.
3. **`render_scene()` engine abstraction** (Layer 5, ~1 day) — one interface: `(keyframe, audio_chunk|None, prompt, engine) → mp4`. Backends: kie Seedance (dialogue), Omni Interactions (b-roll), Kling via kie. Certifi/curl transport per `reference_omni_interactions_api`.
4. **fal lip-sync backend** (Layer 6 tier 2, ~1 day) — `lipsync(video, wav) → mp4` so Omni shots can carry dialogue. Gate output through `pick_take.py` accuracy.
5. **Assembly upgrade** (Layer 7, ~half day) — concat video-only, mux `vo_full.wav`, then caption burn from the EL timestamps we already have.
6. **QA gates wired in** (Layer 8, ~half day) — accuracy ≥0.97 per dialogue scene, consistency scan across scenes, hard-fail into the retry loop instead of into the finished cut.

Total: **~5-6 build days**, all local, no infra. Every generation call is an API we already pay for; the whole margin InfiniteUGC charges is for layers 9 and 10, one of which we build in Python and one of which we don't need.

## Scene-routing doctrine (the part that makes ads, not clips)

- Dialogue on camera → Seedance + audio chunk (tier-1 sync)
- B-roll / product-in-use / cutaway → Omni ≤10s (cheap, no audio needed, VO carries over it)
- Product close-ups → keyframe from canonical product refs (product-scale skills), Ken Burns if the engine mutates labels (`feedback_omni_macro_mutation`)
- Podcast format = two alternating talking-head scene chains over one VO — falls out of the same architecture free
- Captions burned from the SAME timestamps the VO produced — sync by construction

## What we deliberately do NOT copy

- HeyGen (their avatar crutch; Seedance tier-1 covers it)
- Chaining in any form
- Credit metering, auth, dashboard, editor — internal tool, the vault is the UI
