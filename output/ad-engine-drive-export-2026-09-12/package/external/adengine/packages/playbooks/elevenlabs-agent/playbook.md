---
name: elevenlabs-agent
description: >
  Dedicated ElevenLabs voice cloning and TTS agent. Handles voice cloning from reference audio/video files,
  manages a persistent voice registry so cloned voices are reused across sessions, breaks scripts into segments,
  and generates voiceover audio via ElevenLabs TTS. Use this skill whenever the user wants to clone a voice,
  generate voiceover from a script, manage cloned voices, extract audio from a reference video for voice cloning,
  or produce TTS audio for any downstream pipeline (fabric-talking-head, aiugc-replicator, aiugc-orchestrator, etc.).
  Also trigger when the user says "clone this voice," "use this person's voice," "generate voiceover," "make a VO,"
  "extract the voice from this video," "list my voices," or any variation of voice cloning or text-to-speech work.
  This is the single source of truth for all ElevenLabs operations — other skills should delegate voice work here.
---

# ElevenLabs Agent

The dedicated voice handler for the marketing brain pipeline. This skill owns all ElevenLabs API interactions:
voice cloning, voice registry management, script segmentation, and TTS generation.

## Setup

- **API Key**: `ELEVENLABS_API_KEY` in `~/Documents/marketing brain/.env`
- **Voice Registry**: `~/Documents/marketing brain/voice-registry.json` — persistent JSON store of cloned voices
- **Pipeline Script**: Run `pipeline.py` in this skill's directory for automated operations

## Core Capabilities

### 1. Voice Cloning from References

Clone a voice from audio or video reference files. The pipeline:

1. If the reference is a **video file** (.mp4, .mov, .webm, .mkv), extract audio using FFmpeg
2. Upload the audio sample(s) to ElevenLabs instant voice cloning (IVC) endpoint
3. Receive back a `voice_id` and store it in the voice registry
4. Optionally remove background noise during cloning (`--remove-noise` flag)

**Supported input formats:**
- Audio: .mp3, .wav, .m4a, .aac, .ogg, .flac
- Video: .mp4, .mov, .webm, .mkv (audio extracted automatically via FFmpeg)

**Multiple samples**: You can pass multiple reference files for better clone quality. ElevenLabs recommends 1-3 minutes of clean speech.

### 2. Voice Registry

The voice registry (`voice-registry.json`) persists cloned voice IDs so you never re-clone the same voice. Structure:

```json
{
  "voices": {
    "friendly-female-motilli": {
      "voice_id": "abc123xyz",
      "name": "friendly-female-motilli",
      "description": "Cloned from Motilli reference ad - warm female narrator",
      "source_files": ["reference-ad-motilli.mp4"],
      "cloned_at": "2026-03-27T10:30:00Z",
      "brand": "motilli",
      "tags": ["female", "warm", "conversational"]
    }
  },
  "default_voices": {
    "rachel": "21m00Tcm4TlvDq8ikWAM",
    "drew": "29vD33N1CtxCmqQRPOHJ",
    "clyde": "2EiwWnXFnvU5JabPnv8n",
    "domi": "AZnzlk1XvdvUeBnXmlld"
  }
}
```

**Registry commands:**
- `--list-voices` — Show all registered voices
- `--delete-voice <name>` — Remove a voice from registry (and optionally from ElevenLabs)
- `--sync-voices` — Sync registry with ElevenLabs account (pull remote voices)

### 3. Script Segmentation

When generating voiceover for long scripts, the pipeline can break them into segments. This is useful when downstream tools (like the video-scene-replicator or aiugc-replicator) need per-scene audio.

**Segmentation modes:**
- `--segment-by lines` — Each line becomes a segment
- `--segment-by paragraphs` — Double-newline splits
- `--segment-by scenes` — Split on scene markers like `[Scene 1]`, `---`, or `## Scene`
- `--no-segment` — Generate one continuous audio file (default)

Each segment is saved as `segment_001.mp3`, `segment_002.mp3`, etc. alongside a `segments.json` manifest:

```json
{
  "segments": [
    {"index": 1, "text": "Have you ever noticed...", "file": "segment_001.mp3", "duration_ms": 4200},
    {"index": 2, "text": "Well here's the thing...", "file": "segment_002.mp3", "duration_ms": 3800}
  ],
  "total_duration_ms": 8000,
  "voice_id": "abc123xyz",
  "voice_name": "friendly-female-motilli"
}
```

### 4. TTS Generation

Generate voiceover audio using any voice (cloned or default). The pipeline handles:
- Retry logic (3 attempts with 5-second backoff)
- Voice settings (stability, similarity boost, style, speaker boost)
- Output as MP3

## Pipeline Usage

```bash
# Clone a voice from a reference video
python3 pipeline.py clone \
    --reference ./reference-ad.mp4 \
    --name "warm-female-narrator" \
    --brand motilli \
    --description "Cloned from winning Motilli ad" \
    --remove-noise

# Clone from multiple audio samples
python3 pipeline.py clone \
    --reference ./sample1.mp3 ./sample2.mp3 \
    --name "doctor-voice" \
    --description "Professional male doctor voice"

# Generate voiceover from script using a cloned voice
python3 pipeline.py generate \
    --script "Your ad script text here..." \
    --voice "warm-female-narrator" \
    --output-dir ./vo-output

# Generate with segmentation
python3 pipeline.py generate \
    --script-file ./script.txt \
    --voice "warm-female-narrator" \
    --segment-by lines \
    --output-dir ./vo-output

# Generate using a default ElevenLabs voice
python3 pipeline.py generate \
    --script "Your script..." \
    --voice-id "21m00Tcm4TlvDq8ikWAM" \
    --output-dir ./vo-output

# List all registered voices
python3 pipeline.py list

# Sync registry with ElevenLabs account
python3 pipeline.py sync
```

## Integration with Other Skills

This skill produces outputs consumed by:
- **fabric-talking-head**: Takes the generated MP3 + avatar image → lip-synced video
- **aiugc-replicator**: Takes per-segment MP3s for scene-by-scene lip-sync
- **aiugc-orchestrator**: Can delegate its Stage 1 (TTS) to this skill for cloned voices
- **video-editor-brief**: Uses segment manifest to match audio to scenes

## Voice Settings

Default voice settings (tuned for natural-sounding ad voiceover):

| Setting | Value | What it controls |
|---------|-------|-----------------|
| stability | 0.5 | Higher = more consistent, lower = more expressive |
| similarity_boost | 0.75 | How closely to match the cloned voice |
| style | 0.3 | Style exaggeration (keep low for natural sound) |
| use_speaker_boost | true | Enhances speaker similarity |

Override with `--stability`, `--similarity`, `--style` flags.

## ElevenLabs API Reference

- **Clone voice**: `POST https://api.elevenlabs.io/v1/voices/add` (multipart form)
- **TTS**: `POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id}`
- **List voices**: `GET https://api.elevenlabs.io/v1/voices`
- **Auth header**: `xi-api-key: <ELEVENLABS_API_KEY>`
- **Model**: `eleven_multilingual_v2`
