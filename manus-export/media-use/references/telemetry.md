# Telemetry, usage stats & privacy

If you build or maintain a media pipeline like this over time, it's worth tracking basic usage telemetry to understand what's actually being used and where the gaps are — while keeping that telemetry deliberately coarse and privacy-respecting.

## What to log, and at what granularity

For each significant operation (an asset resolve, a resolve that found nothing, a transcription, an audio-ducking pass, etc.), log only coarse categorical facts — the *type* of media involved, the *source* it came from (cache hit vs. fresh fetch vs. generation), and the *provider* that ultimately served it.

Deliberately **exclude** anything identifying or content-specific: no free-text search/intent strings, no file names, no file paths, and no IP address. This lets you answer aggregate questions ("how much is X used, for what, is reuse working, what can't it satisfy") without building a record of what any individual project actually contains.

## Useful aggregate questions to track over time

If you set up any kind of usage dashboard, these are the tiles worth building:

1. **Invocation volume** — how often each capability gets used, over time.
2. **Breakdown by media type** — which categories (music, SFX, images, icons, logos, voice, grading, LUTs) see the most use.
3. **Resolve/hit rate** — of all attempts, what fraction actually found or produced a usable asset vs. came up empty (`hits / (hits + misses)`). This tells you whether your existing asset library is covering real needs.
4. **Provider mix** — which underlying provider actually served each successful resolve; useful for spotting when a preferred provider silently isn't being reached and a lesser fallback is doing more work than expected.
5. **Top misses by type** — where requests are landing where nothing was found; pair this with a *local*, non-telemetry log of the actual missed request text (kept locally, not sent anywhere) to see the specific gaps.
6. **Dependency/setup health** — if you run any kind of "doctor"/setup-check command, track which dependency checks fail most often, to prioritize documentation or setup fixes.
7. **Adoption** — if you can distinguish a first-ever use of a capability from a repeat use, segment by that to see whether new capabilities are getting picked up.

## Privacy posture

If usage is ever linked to an identity at all (e.g. because a provider account is signed in), that link should be a deliberate, disclosed choice — not hidden. Events should stay coarse (type/source/provider/small counts only) regardless of whether they're linked to an account.

Always provide, and clearly document, an opt-out mechanism (an environment variable such as `DO_NOT_TRACK=1` is a widely-recognized convention) and make sure telemetry never runs in automated/CI contexts by default.

Telemetry of this kind should always be **best-effort and non-blocking** — a logging call should never be able to delay or fail the actual operation it's describing.

## Ownership/scope framing

It's useful to explicitly document, for a system like this, which responsibilities it owns versus which it deliberately leaves to a different layer — for example: "this system owns sourcing/generating/remembering media assets; a separate rendering/compositing system owns actually playing them back." Keeping that boundary explicit and verified (e.g. with a small test that walks the claimed ownership table) prevents the two layers from silently duplicating or contradicting each other as both evolve.

A practical way to keep this honest: maintain a short table of "gap → how this system fills it" (e.g. "no third-party brand logos" → "logo resolution via a marks/icon lookup chain," "no cross-project memory" → "a global content-addressed cache with auto-promotion") and revisit it whenever either layer's responsibilities shift.
