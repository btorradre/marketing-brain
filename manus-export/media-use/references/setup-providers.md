# Provider setup & requirements

This captures the general **shape** of provider/credential management for a media pipeline like this — adapt the specific services named to whatever you actually have access to.

## General credential-priority pattern

When multiple ways to authenticate exist for the same capability, resolve them in a fixed priority order and use the first one that's actually configured — e.g., check an explicit environment variable first, then a more general fallback environment variable, then a locally-stored credentials file. Document that order clearly so provider selection is predictable rather than mysterious.

Illustrative priority chain for one capability:

1. A capability-specific environment variable (e.g. `$SERVICE_API_KEY`)
2. A more general fallback environment variable shared across capabilities
3. A locally-stored credentials file written by that service's own CLI/login flow

A sign-in / OAuth-style login is generally the friendliest setup path when available (one sign-in covers every project, no per-project credential files); a raw API key is the alternative when OAuth isn't practical. Be aware some services offer a limited free usage tier for either signed-in or API-key access, with different billing/quota rules for each — know which one you're on before assuming a capability is free.

## Illustrative credential/provider table

The specific services below are examples — substitute your own equivalents for whatever you actually have access to:

| Capability | Provider example | Local dependency, if any |
|---|---|---|
| TTS + BGM/SFX retrieval (best quality, needs an account) | A premium creative-suite API | None — pure API calls |
| TTS fallback | A standard cloud TTS API | An SDK/client library |
| BGM fallback (generative) | A real-time text-to-music model | An API key + SDK |
| TTS, no account needed | A local/offline TTS model (e.g. Kokoro-class) | A local ML runtime |
| BGM, no account needed | A local text-to-music model (e.g. MusicGen-class) | A local ML runtime with a sizeable model download |

## Local model caching

Any locally-run model (a TTS voice model, a text-to-music model, a transcription model, a background-removal segmentation model) will typically download and cache its weights on first use — sizes can range from tens of MB (a small transcription/segmentation model) up to a few GB (a large transcription model or diffusion image model). Plan for that first-run download time and disk usage.

A general-purpose media/video tool (`ffmpeg`) needs to be present on the system path for many of the operations described throughout this skill (transcoding, silence detection, loudness measurement, etc.) — verify it's installed before assuming any of these workflows will work. A one-time "doctor" check (verifying each dependency is present and each credential resolves) is worth running before starting a production pass, so failures surface up front rather than mid-render.

## Deciding when to ask before spending money

As a general rule, an **agent-initiated** call to a paid/metered service should be confirmed with the requester first; a call the requester **explicitly asked for** can just run without an extra confirmation step. This matters most for anything metered per-use (video generation is the clearest example) — flag those as needing confirmation before firing.
