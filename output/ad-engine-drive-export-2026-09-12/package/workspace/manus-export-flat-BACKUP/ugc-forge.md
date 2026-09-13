# UGC Forge — Consistent, Correctly-Voiced UGC Video Ads

This document describes a method for turning one ad script into a single consistent, correctly-voiced UGC-style video ad, built by chaining several short generated video segments together seamlessly. It solves two specific failure modes that plague clip-by-clip AI video workflows: the creator's face/wardrobe/lighting/setting visibly drifting between clips, and generated speech mangling brand or product names. Use this approach whenever building a UGC ad from a script where segments need to look like one continuous take, or when previous attempts at stitching AI-generated clips together have drifted visually or mispronounced brand terms.

Before drafting the script itself, apply the golden nugget doctrine: identify the single most emotionally loaded deep frame in the research — the real motive that makes the buyer act, not the surface topic. State it in one sentence before writing, and make sure the script actually leads with it as the hook rather than burying it.

## The two core problems this solves

**Problem 1 — visual drift.** Generating each ~8-second clip independently lets the person, wardrobe, lighting, and setting wander between clips, forcing endless re-rolls to get a usable sequence.

**Fix — frame chaining.** Generate segments *sequentially*, not in parallel. Segment 1 is an image-to-video generation starting from a single reference still of the creator. Extract that segment's **final frame**, and use it as the **starting frame** for segment 2. Repeat all the way down the script. Every segment begins exactly where the previous one ended, so identity, wardrobe, lighting, and setting all carry forward and the cuts read as seamless. Reinforce this further with: a fixed "style anchor" phrase appended to every single generation prompt, a fixed negative prompt used on every call, and a fixed random seed used on every call — consistency comes from holding everything constant except the script line itself.

**Problem 2 — mispronunciation.** AI-generated speech frequently mangles brand names and unusual product terms.

**Fix — one cloned/fixed voice plus a pronunciation lexicon, decoupled from the video model's own audio.** Generate all speech from a single fixed voice (the same exact voice ID/clone across every segment, and across every creator variation if running multiple creators through the same script). Maintain a small pronunciation lexicon (a JSON dictionary) that rewrites tricky words to a phonetic respelling or a phoneme markup before synthesis — so the pronunciation fix is deterministic and reusable rather than a lucky roll. Never use a video-generation model's own native/built-in audio track for dialogue — always mute or discard it and treat the independently-synthesized voice track as the only speech source. The synthesized audio's exact duration (measured precisely, e.g. via a media-inspection tool) becomes the target length for its video segment — conform the silent video to that duration; never stretch, pitch-shift, or re-encode the audio to match the video instead.

## How to use this

### Pipeline

1. Parse the inputs: the script (or a pre-segmented list of beats), a reference still of the creator, the voice to use, a pronunciation lexicon, target aspect ratio, and any style settings.
2. Segment the script into beats of roughly 8 seconds or less each, breaking only at natural sentence/breath boundaries (never mid-clause) — this length ceiling exists because many video-generation models cap out around 8 seconds per clip.
3. Synthesize audio for every beat with the one fixed voice, applying the pronunciation lexicon first, and measure each beat's resulting audio duration precisely.
4. Generate video segments **sequentially, frame-chained**: segment 1 starts from the reference still; extract its last frame and use it as the starting frame for segment 2; and so on down the script. Disable the video model's native audio on every call. Use a fixed seed and fixed negative prompt across all calls. Conform each generated clip's length to its corresponding audio segment's duration.
5. For talking-head segments, run a lip-sync pass so the mouth movement matches the synthesized voice track (see lip-sync section below). For pure b-roll segments (no face talking), simply mux the voiceover audio under the visuals — no lip-sync needed.
6. Concatenate all segments into one continuous final video.
7. Output: the final video (vertical 9:16 as the default format, with optional additional exports at other aspect ratios such as 4:5 or 16:9), the individual segment clips, the individual audio stems, and a run record (a manifest) capturing every decision made — this is what makes selective re-runs possible later (see "re-run economy" below).

### Multiple creators from one script (variations)

The identical script and identical synthesized audio can be run across several different creator reference stills, producing one labeled finished video per creator, all speaking exactly the same words with exactly the same voice — useful for testing which creator performs best without re-writing or re-voicing anything.

### Bringing your own pre-recorded voiceover

If a voiceover has already been recorded/produced elsewhere, it can be fed in directly instead of being synthesized fresh — either as one separate audio file per script beat (in order, with the count matching the number of segmented beats), or as a single full-ad voiceover file that gets automatically split into beats at the silence gaps between sentences. In this mode, the supplied audio is treated as authoritative and is never re-synthesized or re-encoded — the video is conformed to it, and lip-sync (for talking-head segments) is driven by it. If the number of supplied audio pieces doesn't match the number of script beats, stop and report the mismatch rather than guessing how to reconcile them.

### Drift control

Even with frame chaining, color and exposure can slowly drift across many segments in a row. Counter this by periodically "re-anchoring" — every N segments (a reasonable default is every 4), start the next segment from the *original* reference still again instead of the previous segment's last frame, pulling the creator's identity back to true. Re-anchoring can also be forced at specific points where a hard scene change is planned, or triggered automatically when a measured color/brightness drift from the original reference crosses a threshold.

### Lip-sync (pluggable, with guardrails)

Talking-head segments need the mouth to match the independently-synthesized voice track, not whatever speech (if any) the video model itself generated. Treat lip-sync as a swappable component — several different lip-sync services/models can serve this role interchangeably; whichever is used, the same guardrail applies:

- If the chosen lip-sync backend is unavailable, or a call to it fails mid-run, fall back to a plain audio mux (video + correct audio, no lip-sync) rather than failing the whole segment — but log clearly that the mouth wasn't actually driven to match, so this is never silently passed off as a properly lip-synced result.
- After any lip-sync pass, re-mux in the exact original synthesized audio stem for final output, so audio quality is never degraded by round-tripping through the lip-sync service.
- B-roll segments (no face talking to camera) skip lip-sync entirely and just mux the voiceover under the visuals.

### Re-run economy (avoid regenerating everything for one fix)

Keep a manifest of every segment's script line, applied (post-lexicon) text, visual prompt, seed, model, source of its starting frame, audio path and duration, output path, and content hashes of the text/settings that produced it. On a re-run:
- Automatically detect which lines actually changed (by comparing text/lexicon hashes) and only re-synthesize audio for those; reuse unchanged stems as-is.
- When forcing a re-render of specific segments, remember that because of frame chaining, regenerating segment *i* invalidates every segment after it *up to the next re-anchor point* (since they all inherit their starting frame from the previous segment). Automatically include those dependent segments in the re-render so the chain stays visually seamless — everything before segment *i*, and everything after the next re-anchor point, can be reused untouched. This means fixing one bad line doesn't require re-rendering the entire ad.
- If re-segmenting the script produces a different number of beats than a prior run's manifest recorded, stop and report the mismatch rather than silently guessing how to map old segments to new ones — require an explicit confirmation to accept the new segmentation.

## Rules & standards

- The independently-synthesized voice is the **only** speech source in the finished video — a video-generation model's own native/built-in speech or audio track is never used for dialogue.
- Don't bake on-screen text or captions into the generated video itself — add those in a later editing pass, not during generation.
- If the number of audio segments doesn't match the number of script segments, stop and report — never guess at how to line them up.
- If a video-generation call is rejected by a safety filter or returns empty, retry once with a reworded prompt; if it still fails, log the failure and exclude that segment from the final cut rather than crashing the whole batch.
- If a creator reference still contains more than one face, stop and ask which face should be locked as the subject before generating anything — don't guess which face is the intended creator.
- Be aware that many video-generation models embed an invisible provenance watermark (e.g. SynthID) in their outputs; note this in the run manifest so it's not a surprise later.
- Handle rate limits on both the voice-synthesis and video-generation services with exponential backoff rather than failing immediately.
- API keys and credentials should never be passed as visible command-line arguments or logged anywhere in run output.

## Templates & examples

### Example run-manifest entry (per segment)

```json
{
  "index": 0,
  "line": "I used to bloat up every single afternoon...",
  "applied_text": "I used to bloat up...",
  "visual": "creator talking directly to camera...",
  "talking_head": true,
  "prompt": "<full video-generation prompt including the fixed style anchor>",
  "seed": 777,
  "start_frame_source": "reference | prev_frame | reanchor",
  "audio_path": ".../audio/seg_000.mp3",
  "audio_duration": 7.84,
  "final_path": ".../avatar_00_creator/seg_000.mp4",
  "last_frame": ".../frames/seg_000_last.png",
  "watermark": "SynthID",
  "text_hash": "...",
  "settings_key": "..."
}
```

A segment skipped due to a safety filter should record `{"skipped": true, "reason": "..."}` and be excluded from the final concatenation.

### Conform semantics (video-to-audio length matching)

Make the silent generated clip exactly match its audio's length: trim the tail if the video is longer than the audio, or freeze-pad on the last frame if the video is shorter. Mux the synthesized audio in as-is afterward — never time-stretch or pitch-shift it to fit; the video always adapts to the audio, never the reverse.
</content>
