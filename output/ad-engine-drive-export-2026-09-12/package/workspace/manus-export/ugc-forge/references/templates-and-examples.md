# Templates & worked examples

Supporting templates for the ugc-forge skill: a pronunciation lexicon, a pre-segmented
script, a style-settings block (the style anchor), and a run-manifest entry.

## Pronunciation lexicon example

A JSON dictionary mapping tricky brand/product words to either a plain phonetic
respelling or a structured phoneme spec (alphabet + phoneme string). Applied to the
script text before every synthesis call, so the fix is deterministic across every
segment and every creator variation.

```json
{
  "Boatkin": "Boat-kin",
  "seagrass": "SEE-grass",
  "Velantra": { "alphabet": "ipa", "ph": "vəˈlæntrə" },
  "Motilli": { "alphabet": "cmu-arpabet", "ph": "M OW T IY L IY" },
  "GLP-1": "G L P one"
}
```

## Pre-segmented script example

When beats are already known (rather than auto-segmenting raw script text), supply them
directly. `talking_head: true` routes a segment through the lip-sync pass; `false` routes
it to a plain voiceover-under-visuals mux.

```json
{
  "segments": [
    {
      "line": "I used to bloat up every single afternoon. It was honestly miserable.",
      "visual": "creator talking directly to camera, intimate handheld selfie framing, kitchen background",
      "talking_head": true
    },
    {
      "line": "Then my sister told me about these seagrass gummies from Velantra.",
      "visual": "creator holds the product jar up to frame, slight rotate to show the label",
      "talking_head": true
    },
    {
      "line": "Two weeks later? The bloat was just gone.",
      "visual": "b-roll: product jar on a sunny windowsill, gummies spilling out, no speaker",
      "talking_head": false
    }
  ]
}
```

## Style-settings example (the style anchor)

A fixed block describing the creator, wardrobe, setting, lighting, and camera feel,
appended to every single generation prompt across every segment. This is what keeps the
"same person, same outfit, same room" reading even where frame chaining alone might
drift.

```json
{
  "style": {
    "creator": "the same woman from the reference: early 30s, freckles, shoulder-length brown hair, same face",
    "wardrobe": "cream ribbed knit sweater (identical every shot)",
    "setting": "bright minimalist kitchen with a window, same angle",
    "lighting": "soft natural morning daylight from camera-left",
    "feel": "shot on an iPhone 15 front camera, vertical 9:16, candid UGC, slight handheld sway, real skin texture, no beautify filter"
  }
}
```

## Run-manifest entry example (per segment)

One entry per segment, recording everything needed to reproduce it exactly and to
compute what a future selective re-render must touch.

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

`start_frame_source` records where segment *i*'s starting frame came from — the original
reference still (segment 0, or a forced/auto re-anchor point), or the previous segment's
extracted last frame (the normal frame-chained case). This field is what the re-run logic
uses to figure out which downstream segments depend on segment *i* and must be
regenerated alongside it.

A segment skipped due to a safety filter should record `{"skipped": true, "reason": "..."}`
and be excluded from the final concatenation.
