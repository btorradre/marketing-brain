---
name: ad-watcher
description: Universal video-ad watcher and psychological breakdown. Takes any ad (URL or local file), downloads it, extracts every visual beat via ffmpeg scene-change detection, pulls a timestamped transcript, sends the full video to a Gemini subagent for a structured per-beat descriptive pass (shot type, composition, on-screen text, motion, audio cues, ad role), and then Claude layers a frame-by-frame psychological/direct-response analysis on top — hook mechanics, pattern interrupts, emotional state mapping, belief-shift architecture, visual/audio craft. Writes the breakdown as a markdown file next to the video. Use whenever the user asks to "break down this ad", "analyze this ad", "watch and dissect this ad", "what's working in this ad", or pastes any video ad URL/path and wants a deep teardown.
argument-hint: "<video-url-or-path> [optional focus question]"
allowed-tools: Bash, Read, Write, AskUserQuestion
user-invocable: true
---

## Current hosted analysis and editing workflow

For the ad engine, use the `video-analysis-edit-handoff` playbook and `get_edit_plan_contract`. It defines source analysis, detailed frame review, a validated edit plan and the internal timeline editor. The local script and publishing steps below are legacy documentation.


## GOLDEN NUGGET DOCTRINE (MANDATORY — locked 2026-07-11)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded DEEP FRAME in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: *is this the topic, or is this the motive?* If it's the topic, dig one layer deeper (memory loss → becoming my parent; GLP-1 bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes.** The golden nugget LEADS — very top of the piece, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence BEFORE drafting. When analyzing a reference ad/funnel/swipe instead of writing, state the nugget it's built on and whether it leads with it. If the research hasn't surfaced one, mine reviews/VOC/Reddit until it does — never default to a surface angle.

# /ad-watcher — universal ad teardown

You receive a video ad and produce a psychological/direct-response teardown of every beat. The mechanical work (downloading, scene-cutting, transcribing, sending to Gemini for descriptive per-beat data) is handled by `pipeline.py`. YOU do the psychology layer.

## Step 0 — Preflight

Verify deps once per session (silent on success):

```bash
command -v ffmpeg >/dev/null && command -v ffprobe >/dev/null && command -v yt-dlp >/dev/null && python3 -c "import google.genai" 2>/dev/null && echo OK || echo MISSING
```

If `MISSING`: install with `brew install ffmpeg yt-dlp && pip install google-genai requests`. The pipeline auto-uses the Gemini API key baked into the script (same one as `video-scene-replicator`); override with `GEMINI_API_KEY` if needed. For Whisper fallback when a video has no captions, set `GROQ_API_KEY` (preferred) or `OPENAI_API_KEY` in your environment — without one, transcripts fall back to "none" and you work from frames + Gemini only.

## Step 1 — Parse input

Separate the source (URL or path) from any focus question. Examples:
- `/ad-watcher https://www.facebook.com/.../videos/...` → analyze the whole ad
- `/ad-watcher ./reference.mp4 why does the hook work?` → analyze with hook focus
- `/ad-watcher https://youtu.be/abc compare this to a typical VSL structure` → analyze with comparison framing

If you cannot tell the source from prose, `AskUserQuestion` for the URL or path before running.

## Step 2 — Run the pipeline

```bash
python3 "${CLAUDE_SKILL_DIR}/pipeline.py" "<source>"
```

Optional flags:
- `--out-dir DIR` — force a working directory (default: `<video-dir>/.ad-watcher-<slug>/` for local files, tmp dir for URLs)
- `--scene-threshold F` — lower = more beats, higher = fewer (default 0.28). Drop to 0.18 for AIUGC where cuts are subtle; raise to 0.4 for hard-cut TikToks
- `--skip-gemini` — frames + transcript only, no Gemini descriptive pass (use when Gemini API is down or the user explicitly asks for raw frames)

The script prints `MANIFEST_PATH=`, `WORK_DIR=`, `VIDEO_PATH=`, `FRAME_COUNT=` on the last lines — capture those.

## Step 3 — Read the manifest + every frame

```
Read MANIFEST_PATH                                # JSON: per-beat Gemini analysis + VO
Read every beat["frame"] in parallel              # so you SEE the ad
```

Read all frames in a single parallel batch. You need both the Gemini descriptive layer AND your own visual perception of each frame to do the psychological analysis well — Gemini catches the literal content, you catch the persuasion craft.

If the manifest has `_raw_gemini` or `_error`, Gemini's structured pass didn't parse. Fall back to reading the raw text or working from frames + transcript alone.

## Step 4 — Write the psychological teardown

Write a markdown file: `<WORK_DIR>/breakdown.md` AND a sibling next to the video (for local files): `<VIDEO_PATH dirname>/<video-stem>.breakdown.md`. For URL sources, just the work-dir copy.

Use this structure:

```markdown
# <Inferred ad name or source> — Ad Watcher Breakdown

**Source:** <url or path>
**Duration:** <seconds>
**Format:** <Gemini "format" — AIUGC talking head / VSL with B-roll / Animated / etc.>
**Core promise:** <Gemini "core_promise">
**Emotion arc:** <Gemini "primary_emotion_arc">

## Top-line read

2-4 paragraphs. What's working psychologically. Who this is for (avatar). Which DR principles are doing the heavy lifting (mechanism, social proof, urgency, etc.). What you'd steal and what you'd fix.

## Beat-by-beat

For EVERY beat in the manifest, write a section:

### Beat <N> — <t MM:SS> · <shot_type> · <ad_role>
![](frames/beat_NNN.jpg)

- **What's on screen:** <one line, drawing on Gemini composition + your own read>
- **On-screen text:** `<exact overlay text or em-dash if none>`
- **VO:** "<transcript text for this beat, or em-dash>"
- **Audio:** <music/SFX/VO delivery cues>
- **Ad function:** what this beat is DOING in the funnel (hook, agitate, mechanism reveal, proof, etc.)
- **Why it works (psychology):**
  - <Belief shift this beat installs — old belief → new belief>
  - <Emotional state the viewer is in by the end of this beat>
  - <Pattern interrupt / curiosity gap / unresolved tension carried into next beat, if any>
  - <Reference to DR principle if applicable: mechanism education, social proof formatting, objection handling, urgency stacking, etc.>
- **Craft notes:** <composition / motion / sound / pacing observation worth stealing>

## Structural map

A short table or bulleted timeline showing how beats group into acts (hook block / agitation block / mechanism block / proof block / offer block / close). Note where the offer drops, where the longest unresolved tension lives, and where retention is most at risk.

## What to steal / what to fix

Two short bulleted lists:
- **Steal:** specific techniques transferable to other ads in this category
- **Fix:** weaknesses, missed beats, or places this ad leaks attention/credibility

## Raw manifest

`<WORK_DIR>/manifest.json` — full JSON for downstream pipelines.
```

## Psychological layer — what to actually evaluate

Cover EVERY dimension below for every beat (the user wants this skill to be universal — don't skip any):

- **Hook mechanics:** What stops the scroll? Curiosity gap? Pattern interrupt? Specificity (numbers, names, places)? Direct callout to avatar? Visual oddity? Sound design hit?
- **Pattern interrupts:** Where does the ad break the viewer's expected rhythm — visually, audibly, or narratively — to keep retention?
- **Emotional state mapping:** Name the dominant emotion the viewer feels at each beat (curiosity, recognition, fear, hope, vindication, urgency, etc.). Note when the state shifts and what causes the shift.
- **Belief-shift architecture:** For every beat that's doing persuasion work, state the OLD belief getting broken and the NEW belief getting installed. This is the spine of DR copy — without belief shifts, beats are just decoration.
- **Mechanism education:** When does the ad explain WHY/HOW the solution works? Is the mechanism literal (apigenin relaxes smooth muscle) or metaphorical (the "gut stall" / "mover-bulk-feed")? Note: metaphor frameworks usually weaken sophisticated avatars — call it out.
- **Social proof formatting:** How is proof delivered — testimonial card, before/after, count ("50,000 women"), specificity, third-party endorsement, celebrity, doctor in white coat? Is the proof concrete or vague?
- **Objection handling:** Which objections does the ad pre-empt, and at which beats? Are they handled with confidence (one-line dismissals) or sophistication (deep proof)? Match to avatar sophistication level.
- **Urgency / scarcity:** Does the offer beat manufacture urgency? Is it genuine (limited supply, sale ends) or manufactured (artificial countdown)? How aggressive vs. casual is the close?
- **CTA architecture:** How does the close stack offer, guarantee, bonuses, price anchor, urgency, and call-to-action button copy?
- **Visual/audio craft:** Composition, motion (camera + subject), color palette, lighting mood, sound design (music drops, whooshes, SFX hits, VO delivery — intimate vs broadcast vs hype). Note when craft amplifies the persuasion vs when it works against it.
- **Pacing / retention risk:** Identify the longest beats and longest gaps without a new hook or pattern interrupt — that's where viewers drop. Identify the unresolved tension/promise carried across beats that keeps them watching.
- **Avatar match:** Does the ad assume the right sophistication level for its target? Where does it talk down to a sophisticated buyer or over the head of a beginner?

If the user passed a focus question (Step 1), lead the **Top-line read** with it and weight the beat-by-beat commentary toward it — but still cover every beat.

## Step 5 — Report back

Reply to the user with:
1. The markdown file path(s) you wrote.
2. A 4-6 sentence headline summary: format, core promise, emotion arc, what's working, what's broken, who it's for.
3. Offer follow-ups: "want me to apply this to Brand X?", "want a version-2 script using these mechanics?", "want me to lift the hook block for a new variant?"

## Cleanup

Do NOT delete the work_dir unless the user asks. The frames + manifest are often reused by downstream pipelines (ad-replicator, video-scene-replicator, claymation, animated-video-replicator, hook-generation).

## Universality

This skill is brand-agnostic and format-agnostic. It works on:
- AIUGC talking heads (single creator, two-cut, long-form VSLs)
- B-roll VSLs (voiceover + cutaways, no on-camera presenter)
- Animated explainers (2D/3D, mechanism-of-action style)
- Claymation / stop-motion / surreal
- Founder UGC, doctor talking heads, podcast clips
- Listicle promos, advertorial promos
- TikTok POVs, Instagram Reels, YouTube Shorts, paid Meta video ads

Do NOT couple analysis to one brand vault — the user might point this at a competitor's ad, a viral organic, or anything else. Cite brand-specific memory only if the user asks for adaptation to their brand.

## When NOT to use

- Pure static image ads → use `ad-replicator` or `cro-agent` instead.
- Landing pages / advertorials → use `cro-agent` or `funnel-analysis` skills.
- Audio-only podcasts → no frames to analyze; not useful here.
- Live-action production teardowns where the user wants shot lists for filming (use `video-editor-brief` or `mbc-pipeline`).

## Security & permissions

- Runs `yt-dlp` locally to download from public URLs.
- Runs `ffmpeg`/`ffprobe` locally for scene extraction + audio strip.
- Uploads the full video file to `generativelanguage.googleapis.com` (Gemini Files API) for the descriptive pass. Deletes the upload immediately after.
- Uploads the extracted audio (mono 16 kHz, ~0.5 MB/min) to Groq or OpenAI Whisper ONLY when native captions are unavailable.
- Writes all working files into the `WORK_DIR` (next to the video for local files, tmp for URLs).
- Does NOT log in to any platform, does NOT post anywhere, does NOT cache API keys.
