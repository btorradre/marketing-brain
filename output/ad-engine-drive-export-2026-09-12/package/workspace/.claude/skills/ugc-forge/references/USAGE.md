# ugc-forge — usage & internals

## Quick start

```bash
cd ".claude/skills/ugc-forge"
pip3 install -r requirements.txt
python3 scripts/ugc_forge.py \
  --script ad.txt --avatar creator.png --voice <eleven_voice_id> \
  --lexicon examples/pron.example.json --aspect 9:16 --reanchor-every 4 --out ad.mp4
```

Keys come from the vault `.env` (`GEMINI_API_KEY`, `ELEVENLABS_API_KEY`). Never pass them
as flags; they are never logged or printed.

## Module map (`scripts/`)

| file | responsibility |
|------|----------------|
| `ugc_forge.py` | CLI + orchestration (the pipeline below) |
| `segmenter.py` | raw text → `<=8s` beats at sentence/breath boundaries; manifest normalize |
| `lexicon.py` | apply pronunciation map (respelling / SSML `<phoneme>`) before synthesis |
| `tts_elevenlabs.py` | ElevenLabs REST synth, one fixed voice, ffprobe duration, backoff |
| `veo.py` | Veo 3 image-to-video (native audio OFF, fixed seed + negative prompt), retry/skip |
| `video_ops.py` | last-frame extract, conform-video-to-audio, mux, concat, aspect, drift |
| `lipsync.py` | pluggable lip-sync registry (omni / wav2lip / none) with mux fallback |
| `prompts.py` | the style-anchor block appended to every prompt |
| `faces.py` | multi-face guard on the reference (opencv, optional) |
| `manifest.py` | run manifest read/write + selective-rerun dependency logic |

## Pipeline (what `ugc_forge.py main()` does)

1. Load env, require both keys.
2. Segment (`--script` raw → `<=8s` beats, or `--manifest` pre-segmented). If a prior run
   manifest exists with a different segment count → stop unless `--resegment`.
3. **Audio pass (shared across all avatars):** apply lexicon → ElevenLabs synth → ffprobe
   duration. Reuse a stem if its text+voice+model hash is unchanged.
4. Compute re-anchor index set from `--reanchor-every` / `--reanchor-on-segment`.
5. Decide which segments to render: auto-changed (text/settings/no prior artifact) ∪
   `--regen`, expanded across frame-chain dependents up to the next anchor.
6. **Video pass per avatar (sequential, frame-chained):** pick start frame (original
   reference at anchors / on drift; otherwise previous segment's last frame) → build prompt
   (visual + style anchor) → Veo image-to-video (seed `777`, native audio off) → conform to
   the audio duration → lip-sync conform (talking head) or mux VO (b-roll) → extract last
   frame for the next segment.
7. Concat → master MP4 (+ labeled MP4 per variation). Optional `--also-aspect` exports.
8. Write `<out>.manifest.json`.

## Run manifest schema (per segment)

```json
{
  "index": 0,
  "line": "I used to bloat up every single afternoon...",
  "applied_text": "I used to bloat up...",          // after lexicon substitution
  "visual": "creator talking directly to camera...",
  "talking_head": true,
  "prompt": "<full Veo prompt incl. style anchor>",
  "seed": 777,
  "veo_model": "veo-3.0-generate-001",
  "start_frame_source": "reference | prev_frame | reanchor",
  "audio_path": ".../audio/seg_000.mp3",
  "audio_duration": 7.84,
  "final_path": ".../avatar_00_creator/seg_000.mp4",
  "last_frame": ".../frames/seg_000_last.png",
  "watermark": "SynthID",
  "text_hash": "...", "settings_key": "..."          // drive selective re-runs
}
```

Skipped (safety-filtered) segments record `{"skipped": true, "reason": ...}` and are
excluded from the concat.

## Wiring a real lip-sync backend

```bash
# wav2lip example — template gets {video} {audio} {out} substituted (already shell-quoted)
export UGC_WAV2LIP_CMD='python /path/Wav2Lip/inference.py --checkpoint_path wav2lip.pth --face {video} --audio {audio} --outfile {out}'
python3 scripts/ugc_forge.py ... --lipsync-backend wav2lip
```

Register a new backend by adding a `fn(video, audio, out) -> out` to `BACKENDS` in
`scripts/lipsync.py`.

## Conform semantics

`conform_video_to_audio` makes the silent Veo clip exactly the audio length: trim if the
video is longer, freeze-pad the last frame (`tpad`) if shorter. The ElevenLabs audio is
then muxed in **as-is** (AAC copy, `-shortest`) — never time-stretched or pitch-shifted.

## Notes

- Veo 3 clips are ~8s; that is why beats are capped at 8s of spoken audio.
- `seed=777` and the negative prompt in `veo.py` are intentionally fixed for consistency;
  change them only if you want a different look across the whole ad.
- All Veo outputs carry an invisible SynthID watermark (recorded in the manifest).
