# Transcription

Goal: normalized, word-level timestamps, in the shape:

```json
[
  { "id": "w0", "text": "Hello", "start": 0.0, "end": 0.5 },
  { "id": "w1", "text": "world.", "start": 0.6, "end": 1.2 }
]
```

## Language rule (non-negotiable)

English-only transcription models (the class of models often labeled `.en`, e.g. `tiny.en`/`base.en`/`small.en`/`medium.en` in the Whisper family) will **translate** non-English audio into English rather than transcribing it in the original language. This silently destroys the original-language content.

Always set the model/language explicitly rather than relying on a tool's default:

1. **Known English audio** → use an English-only model (a larger one, e.g. a "medium" tier, for music or noisy audio).
2. **Known non-English audio** → use a general (non-English-only) model plus an explicit language code.
3. **Unknown language** → use a general multilingual model and let it auto-detect.

An explicit language setting also helps filter out non-target-language segments from mixed-language audio.

## Model size tradeoffs

Illustrative, using Whisper-class model sizes as the reference point:

| Size class | Approx. size | Speed | When to use |
|---|---|---|---|
| tiny | ~75 MB | Fastest | Quick previews, smoke tests |
| base | ~142 MB | Fast | Short clips, clear audio |
| small | ~466 MB | Moderate | Default for most multilingual content |
| medium | ~1.5 GB | Slow | Music with vocals, noisy audio |
| large | ~3.1 GB | Slowest | Production quality |

## Picking a model by content type

1. Speech over silence / light background → a small English-only model
2. Speech over music, or music with vocals → start with a medium-tier English-only model
3. A fully produced music track (vocals + full instrumentation) → start with a medium-tier model; expect you may still need manually-sourced lyrics or an external transcription API (see below)
4. Multilingual content → a medium or large multilingual model, paired with an explicit language code

## A faster, more accurate alternative for supported languages

If available, a modern non-Whisper ASR model (e.g. NVIDIA's Parakeet-TDT family) can substantially outperform Whisper-class models — in one benchmark, ~6.05% average word-error-rate vs ~7.44%, and 5-10x faster, with a bigger gap on noisy audio (~4.73% vs ~5.96%, where a large Whisper-class model was observed hallucinating up to 300%+ WER on meeting-style audio).

Such models typically cover English plus a couple dozen other languages; fall back to a Whisper-class model for anything outside that language coverage, or if the faster model isn't available in your environment.

## Using an external transcription API for best accuracy

Two production-grade options, both callable directly:

```bash
# OpenAI Whisper API — request word-level timestamps
curl https://api.openai.com/v1/audio/transcriptions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F file=@audio.mp3 -F model=whisper-1 \
  -F response_format=verbose_json \
  -F "timestamp_granularities[]=word" \
  -o transcript-openai.json
```

```bash
# Groq Whisper API — fast, has a free tier
curl https://api.groq.com/openai/v1/audio/transcriptions \
  -H "Authorization: Bearer $GROQ_API_KEY" \
  -F file=@audio.mp3 -F model=whisper-large-v3 \
  -F response_format=verbose_json \
  -F "timestamp_granularities[]=word" \
  -o transcript-groq.json
```

Import either result and normalize it into the flat `[{ id, text, start, end }]` word-array shape used throughout the pipeline.

## If no transcript exists yet

1. Check for an existing transcript, SRT, or VTT file first.
2. If none exists, run a transcription pass, picking the model by content type (above).
3. Run the mandatory transcript quality check before trusting the result — see `references/captions.md` → Transcript Handling.
