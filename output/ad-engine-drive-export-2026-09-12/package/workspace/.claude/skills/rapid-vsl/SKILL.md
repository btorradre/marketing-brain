---
name: rapid-vsl
description: Rapid VSL generation for organic talking-head "yapper" ads. Takes a script + avatar image, segments the script into ~5-second clauses, generates lip-synced clips via kie.ai Kling 3.0 image-to-video, and stitches them with FFmpeg into a single VSL mp4. Use this for high-volume organic-feeling video ads (talking head in car, kitchen, bathroom, etc.) where the priority is speed and authenticity, not polished production.
---

## GOLDEN NUGGET DOCTRINE (MANDATORY — locked 2026-07-11)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded DEEP FRAME in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: *is this the topic, or is this the motive?* If it's the topic, dig one layer deeper (memory loss → becoming my parent; GLP-1 bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes.** The golden nugget LEADS — very top of the piece, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence BEFORE drafting. When analyzing a reference ad/funnel/swipe instead of writing, state the nugget it's built on and whether it leads with it. If the research hasn't surfaced one, mine reviews/VOC/Reddit until it does — never default to a surface angle.

# Rapid VSL

End-to-end pipeline for generating organic talking-head VSL ads.

**Use when:** Brooks wants to turn a written VSL script into a finished talking-head video as fast as possible — organic yapper feel, not polished ad production.

**Don't use when:** You need polished AI UGC with broll, transitions, or multi-scene production. Use `aiugc-orchestrator` or `video-scene-replicator` instead.

## How it works

1. **Segment script** — splits the script into ~5s chunks at natural clause breaks (periods → commas → conjunctions). Strips `...` (Kling delivery breaks on triple dots).
2. **Upload avatar once** — uploads the user-provided avatar image to a temp host (0x0.st → catbox fallback) and reuses the URL across all segments.
3. **Generate clips in parallel** — fires kie.ai Kling 3.0 image-to-video jobs (4 concurrent), one per segment, with the prompt template `{setting} says: "{line}".`
4. **Stitch with FFmpeg** — normalizes each clip to 1080x1920/30fps and concatenates with re-encode, preserving Kling's audio. Hard cuts only — no crossfades (preserves the organic yapper feel).
5. **Output** — single stitched mp4 at `~/Documents/marketing brain/b-roll/{brand}/{concept_code}/final/final_output.mp4`.

## Usage

```bash
python pipeline.py \
  --script /path/to/script.txt \
  --avatar /path/to/avatar.jpg \
  --setting "Woman sitting in the car" \
  --brand lunessa \
  --concept-code RVSL_001
```

**Args:**

| Arg | Required | Description |
|---|---|---|
| `--script` | yes | Path to text file containing the VSL script |
| `--avatar` | yes | Path to vertical avatar image (jpg/png) |
| `--setting` | no | Prompt prefix. Default: `"Woman sitting in the car"`. Becomes `"{setting} says: \"{line}\"."` |
| `--brand` | no | Brand slug for output dir. Default: `test` |
| `--concept-code` | no | Output subfolder. Default: auto-generated `RVSL_{timestamp}` |
| `--max-words` | no | Target words per segment (default 14, hard cap 16) |
| `--duration` | no | Seconds per Kling clip (default 5, max 10) |
| `--workers` | no | Parallel kie.ai workers (default 4) |
| `--no-audio` | no | Pass `sound: false` to Kling (default: `true`) |

## Output structure

```
~/Documents/marketing brain/b-roll/{brand}/{concept_code}/
├── segments.json          # parsed script → segments + prompts
├── clips/                 # raw Kling clips (clip_001.mp4, clip_002.mp4, ...)
├── normalized/            # ffmpeg-normalized clips
├── final/
│   ├── concatenated.mp4
│   ├── concat_list.txt
│   └── final_output.mp4   # ← deliverable
├── manifest.json          # kie.ai task IDs, prompts, statuses
└── .progress.json         # resume state
```

## Resume support

Re-running with the same `--concept-code` will skip any segments whose clips already exist on disk. Useful if a few segments fail mid-run — just re-run, only the missing ones regenerate.

## Dependencies

- Python: `requests` (already pinned in marketing brain)
- System: `ffmpeg` (must be on PATH)
- kie.ai API key from `KIE_API_KEY` env var (falls back to embedded key used by `video-scene-replicator`)

## Known limitation: Kling audio

The skill defaults to `sound: True` on the Kling request, which is supposed to make Kling 3.0 generate the spoken dialogue from the `says: "..."` clause in the prompt. If on first run the clips have no audio (or only ambient audio), this needs to fall back to ElevenLabs VO + Sync.so lip-sync — that path is not yet implemented. Verify on first run.
