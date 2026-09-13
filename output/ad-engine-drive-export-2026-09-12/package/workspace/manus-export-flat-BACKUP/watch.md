# Watching and Analyzing a Video

This document describes a process for "watching" a video — downloading it, extracting frames, pulling or generating a transcript, and then using both to answer questions about what's in it. Use this whenever you're given a video URL (YouTube, Vimeo, X/Twitter, TikTok, or most other common video sites) or a local video file, and asked to describe, analyze, or answer questions about its content. Since you can't natively watch a video, this process converts it into two things you can actually read: a sequence of extracted still frames, and a timestamped transcript.

## Setup — dependencies and API keys

You'll need the following tools installed and available on the command line:
- **yt-dlp** — for downloading videos from URLs and pulling native captions when available.
- **ffmpeg** and **ffprobe** — for extracting frames as images and, when needed, extracting audio for transcription.

You'll also want at least one speech-to-text API key for the fallback transcription path (used when a video has no native captions, or is a local file):
- **Groq** (preferred: cheaper, faster) — uses the `whisper-large-v3` model. Get a key at console.groq.com/keys.
- **OpenAI** (fallback) — uses the `whisper-1` model. Get a key at platform.openai.com/api-keys.

Store whichever key(s) you have as environment variables (`GROQ_API_KEY` and/or `OPENAI_API_KEY`). If both are present, prefer Groq by default.

If you don't have a Whisper API key at all, you can still proceed frames-only (skip transcription) — just tell whoever you're working with that videos without native captions will come back without a spoken-word transcript.

## Recommended limits

- **Best accuracy: videos under 10 minutes.** Frame coverage (and therefore accuracy) scales inversely with duration — the longer the video, the sparser your frame sampling has to be to stay within a reasonable frame budget.
- **Hard caps: 100 frames total, never more than 2 frames per second.** Recommended frame budget by duration:
  - ≤30 seconds → ~1-2 fps (up to 30 frames)
  - 30 seconds–1 minute → ~40 frames
  - 1–3 minutes → ~60 frames
  - 3–10 minutes → ~80 frames
  - Over 10 minutes → 100 frames, sparsely spaced (flag this to whoever you're working with)
- If handed a long video, consider asking whether there's a specific section of interest before burning a large frame budget on a sparse full-video scan.

## Step-by-step process

**Step 1 — Separate the video source from any specific question.** E.g., given "watch this video and tell me what language it's in, here's the link," separate out the URL from the actual question being asked.

**Step 2 — Download the video and extract everything you need.**
1. Use `yt-dlp` to download the video from the URL (or use the local file path directly if one was given).
2. Use `ffprobe`/`ffmpeg` to extract still frames at an appropriate frame rate for the video's length (per the budget table above), saving them as JPEGs with their timestamps in the filename (e.g. `frame_t=01-23.jpg` for the frame at 1 minute 23 seconds).
3. Get a timestamped transcript, in this priority order:
   a. First, try to pull native captions/subtitles via `yt-dlp` (manual or auto-generated, if the source platform provides them) — this is free and preferred.
   b. If no captions are available (or the source is a local file), extract the audio track (mono, 16kHz, low bitrate is sufficient — roughly 0.5 MB per minute) and send it to whichever Whisper-compatible API you have a key for.

### Focusing on a specific section (denser frame sampling)

When the question is about a specific moment ("what happens around the 2 minute mark?", "the first 10 seconds", "zoom into 0:45 to 1:00"), or the video is long and the question only concerns one part of it, restrict frame extraction and transcript coverage to that time range instead of scanning the whole video. This lets you sample much more densely within the region that actually matters — up to the same 2 fps hard cap, but concentrated:

- ≤5 seconds → 2 fps (up to 10 frames)
- 5–15 seconds → 2 fps (up to 30 frames)
- 15–30 seconds → ~2 fps (up to 60 frames)
- 30–60 seconds → ~1.3 fps (up to 80 frames)
- 60–180 seconds → ~0.6 fps (100 frames, capped)

This focused approach is the right call for: any moment or range named explicitly by whoever's asking; any video longer than roughly 10 minutes where the question concerns only part of it (a focused pass on the relevant section beats a sparse scan of the whole thing); and re-running with denser sampling after an initial full scan didn't have enough detail in some region.

Frame timestamps should always be absolute (positioned on the real video timeline), not relative to the start of your extracted section, and the transcript should be filtered down to the same time range.

**Step 3 — Review every extracted frame as an image**, ideally all together so you can compare them in sequence. Each frame's filename or accompanying metadata should carry its timestamp so you can align it against the transcript.

**Step 4 — Answer the question using both streams of evidence.**
- **Frames** tell you what's visually on screen at each timestamp.
- **Transcript** tells you what's being said at each timestamp (note whether it came from native captions or from Whisper transcription — captions are generally more reliable for exact wording).

If a specific question was asked, answer it directly and cite specific timestamps as evidence. If no specific question was asked, summarize what happens in the video overall: structure, key moments, notable visuals, and spoken content.

**Step 5 — Clean up.** Delete the downloaded video, frames, and audio from your working directory once you're done, unless follow-up questions about the same video are likely — in which case, leave the working files in place so you don't have to re-download and re-process from scratch.

## Failure modes and how to handle them

- **Missing dependencies** → install `ffmpeg` and `yt-dlp` (on macOS, Homebrew handles this: `brew install ffmpeg yt-dlp`; on Linux/Windows, use your platform's package manager).
- **No transcript available** → this means captions were missing AND either no Whisper key is configured or the Whisper API call failed. Proceed frames-only and be explicit that no spoken transcript was available.
- **Long-video warning** → acknowledge the sparse sampling in your answer, and offer to re-run focused on a specific section if more detail is needed there.
- **Download fails** → the error will usually explain why (login-required, region-locked, etc.) — report it plainly rather than retrying repeatedly.
- **Whisper request fails** → likely causes are an invalid key, a rate limit, or exceeding the API's upload size limit on a very long audio file (commonly 25 MB). If one provider fails, retry with the other if you have both keys configured.

## Token/cost efficiency notes

Frames are the primary cost driver, not the transcript:
- Roughly 80 frames at a modest resolution (e.g. 512px wide) is a substantial number of image tokens, depending on aspect ratio.
- The transcript itself is comparatively cheap — even a 10-minute video's transcript is only a few thousand tokens.
- Bumping frame resolution up (e.g. to 1024px wide) roughly quadruples the image-token cost per frame — only do this when you specifically need to read small on-screen text.
- If you already processed a video earlier in the same session and get a follow-up question about it, don't re-download and re-process — just answer from the frames and transcript you already have.

## What this process does and does not do

**Does:**
- Downloads the video locally and pulls native captions when the source platform supports them (this is a request to whatever public host the URL points at).
- Extracts frames and, when needed, a short audio clip locally.
- Sends the extracted audio clip (not the full video) to a speech-to-text API, only when native captions are unavailable and Whisper hasn't been explicitly disabled.
- Writes the downloaded video, frames, audio, and transcript to a temporary local working directory.

**Does not:**
- Upload the full video itself to any API — only the extracted audio ever leaves your machine, and only for transcription.
- Access any platform account, log in, or use session cookies.
- Share your speech-to-text API key(s) between providers.
- Persist any of this outside the working directory — clean it up when you're finished (Step 5).
