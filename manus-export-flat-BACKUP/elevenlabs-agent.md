# ElevenLabs Voice Agent

Handles all ElevenLabs voice cloning and text-to-speech work: cloning a voice from a reference audio or video file, keeping a persistent registry of cloned voices so the same voice never gets re-cloned across sessions, breaking a script into segments for scene-by-scene voiceover, and generating the final TTS audio. Use this whenever someone wants to clone a voice, generate voiceover from a script, manage a library of cloned voices, extract audio from a reference video for cloning, or produce TTS audio to feed into a downstream video pipeline (a talking-head generator, a UGC video assembler, etc.). Trigger phrases: "clone this voice," "use this person's voice," "generate voiceover," "make a VO," "extract the voice from this video," "list my voices."

## How to use this

1. **Set up access.** You need an ElevenLabs API key (`xi-api-key` header on every request).

2. **Maintain a voice registry.** Keep a simple persistent record (a JSON file, a spreadsheet, or any structured note) of every cloned voice so it never needs to be re-cloned. For each voice, track: a short name, its ElevenLabs `voice_id`, a description, which source file(s) it was cloned from, when it was cloned, which brand/project it belongs to, and any tags (e.g. "female," "warm," "conversational"). Also keep a small table of default/stock ElevenLabs voice IDs for cases where no custom clone is needed.

3. **Clone a voice from a reference file.**
   - If the reference is a video file (.mp4, .mov, .webm, .mkv), extract the audio track first (any audio-extraction tool, e.g. ffmpeg, works).
   - Supported audio formats for cloning: .mp3, .wav, .m4a, .aac, .ogg, .flac.
   - Upload the audio sample(s) to ElevenLabs' instant voice cloning endpoint. Multiple samples can be passed for better clone quality — ElevenLabs recommends 1-3 minutes of clean speech total.
   - Optionally request background-noise removal during cloning if the source audio is noisy.
   - Store the returned `voice_id` in the registry immediately.

4. **Segment a script when the downstream use needs per-scene audio** (e.g. matching voiceover to individual video scenes). Segmentation options:
   - By line — each line becomes its own segment.
   - By paragraph — split on blank lines.
   - By scene marker — split on explicit markers like "[Scene 1]," "---," or "## Scene."
   - No segmentation — generate one continuous audio file (the default when segmentation isn't needed).
   Save each segment as its own audio file in sequence, plus a small manifest (JSON or similar) recording each segment's text, filename, and duration, along with the voice used and total duration.

5. **Generate the voiceover.** Call ElevenLabs' text-to-speech endpoint with the chosen voice (cloned or stock), the script text, and voice settings (below). Build in retry logic — a few attempts with a short backoff — since API calls occasionally fail transiently. Output as MP3.

6. **Hand off the output.** The generated audio (single file or segment set) is the direct input for any talking-head video generator, any UGC video assembly pipeline, or a video-editor brief that needs to match audio to scenes.

## Rules & standards

### Voice settings (tuned for natural-sounding ad voiceover — override per project as needed)

| Setting | Default value | What it controls |
|---|---|---|
| stability | 0.5 | Higher = more consistent, lower = more expressive |
| similarity_boost | 0.75 | How closely to match the cloned voice |
| style | 0.3 | Style exaggeration (keep low for natural sound) |
| use_speaker_boost | true | Enhances speaker similarity |

### ElevenLabs API reference
- **Clone voice**: `POST https://api.elevenlabs.io/v1/voices/add` (multipart form upload)
- **Text-to-speech**: `POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id}`
- **List voices**: `GET https://api.elevenlabs.io/v1/voices`
- **Auth header**: `xi-api-key: <ELEVENLABS_API_KEY>`
- **Model**: `eleven_multilingual_v2`

### Registry record shape (example)
```json
{
  "voices": {
    "friendly-female-brandx": {
      "voice_id": "abc123xyz",
      "name": "friendly-female-brandx",
      "description": "Cloned from a winning reference ad — warm female narrator",
      "source_files": ["reference-ad.mp4"],
      "cloned_at": "2026-03-27T10:30:00Z",
      "brand": "brandx",
      "tags": ["female", "warm", "conversational"]
    }
  },
  "default_voices": {
    "rachel": "21m00Tcm4TlvDq8ikWAM",
    "drew": "29vD33N1CtxCmqQRPOHJ"
  }
}
```

### Segment manifest shape (example)
```json
{
  "segments": [
    {"index": 1, "text": "Have you ever noticed...", "file": "segment_001.mp3", "duration_ms": 4200},
    {"index": 2, "text": "Well here's the thing...", "file": "segment_002.mp3", "duration_ms": 3800}
  ],
  "total_duration_ms": 8000,
  "voice_id": "abc123xyz",
  "voice_name": "friendly-female-brandx"
}
```
