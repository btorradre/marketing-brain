# Ad Watcher — Universal Ad Teardown

This document describes how to produce a deep psychological / direct-response teardown of any video ad. Use it whenever someone asks to "break down this ad," "analyze this ad," "watch and dissect this ad," "what's working in this ad," or pastes any video ad URL/path and wants a full teardown. It works on AIUGC talking heads, B-roll VSLs, animated explainers, claymation/stop-motion, founder UGC, doctor talking heads, podcast clips, listicle/advertorial promos, TikTok POVs, Instagram Reels, YouTube Shorts, and paid Meta video ads — brand-agnostic and format-agnostic. It is NOT for pure static image ads, landing pages/advertorials, audio-only podcasts, or live-action production shot-lists for filming.

## GOLDEN NUGGET DOCTRINE (apply first)

Before producing any breakdown, name the golden nugget: the single most emotionally loaded deep frame the ad is built on — the real motive that makes buyers act, never the surface theme. Topic is not motive. For every candidate angle ask: is this the topic, or is this the motive? State the golden nugget in one explicit sentence, and note explicitly whether the ad leads with it or buries it.

## How to use this

**Step 1 — Get the video.** If given a URL, download the video (a tool like yt-dlp works for most public URLs). If given a local file, use it directly.

**Step 2 — Extract every visual beat.** Use scene-change detection (ffmpeg's scene-detection filter, or an equivalent) to split the video into beats/shots. Lower the sensitivity threshold for subtle-cut content like AIUGC talking heads (more beats detected); raise it for hard-cut TikToks (fewer, larger beats). Save a representative frame image for each beat.

**Step 3 — Get a timestamped transcript.** Pull captions if the source provides them; otherwise transcribe the audio (Whisper or an equivalent speech-to-text model) with timestamps.

**Step 4 — Run a structured descriptive pass.** Using a vision-capable model, send the full video (or the extracted frames + transcript) and get a structured, factual, per-beat description covering: shot type, composition, on-screen text, motion, audio cues, and what role each beat plays in the ad (hook, agitate, mechanism reveal, proof, offer, close, etc.). Also get: overall format (AIUGC talking head / VSL with B-roll / animated / etc.), core promise, and primary emotion arc across the whole ad. This is the literal, descriptive layer — capture what is objectively on screen and said, not yet the persuasion analysis.

**Step 5 — Look at every frame yourself and add the psychological/persuasion layer.** The descriptive pass catches literal content; you need to independently look at each frame and add the craft/persuasion analysis on top — this is the actual point of the exercise. Cover every dimension listed below for every beat; don't skip any.

**Step 6 — Write the breakdown as a single markdown document** (structure below), and save it as a file for reference.

**Step 7 — Report back** with: the file path, a 4-6 sentence headline summary (format, core promise, emotion arc, what's working, what's broken, who it's for), and offer natural follow-ups (e.g. "want me to apply this to a specific brand?", "want a version-2 script using these mechanics?", "want the hook block lifted for a new variant?").

If a specific focus question was asked (e.g. "why does the hook work?" or "compare this to a typical VSL structure"), lead the top-line read with that focus and weight the beat-by-beat commentary toward it — but still cover every beat.

## The breakdown document structure

```markdown
# <Inferred ad name or source> — Ad Watcher Breakdown

**Source:** <url or path>
**Duration:** <seconds>
**Format:** <AIUGC talking head / VSL with B-roll / Animated / etc.>
**Core promise:** <one line>
**Emotion arc:** <one line>

## Top-line read

2-4 paragraphs. What's working psychologically. Who this is for (avatar). Which
direct-response principles are doing the heavy lifting (mechanism, social proof,
urgency, etc.). What you'd steal and what you'd fix.

## Beat-by-beat

For EVERY beat:

### Beat <N> — <t MM:SS> · <shot_type> · <ad_role>
[reference the frame image for this beat]

- **What's on screen:** <one line>
- **On-screen text:** `<exact overlay text or "—" if none>`
- **VO:** "<transcript text for this beat, or "—">"
- **Audio:** <music/SFX/VO delivery cues>
- **Ad function:** what this beat is DOING in the funnel (hook, agitate, mechanism
  reveal, proof, etc.)
- **Why it works (psychology):**
  - <Belief shift this beat installs — old belief → new belief>
  - <Emotional state the viewer is in by the end of this beat>
  - <Pattern interrupt / curiosity gap / unresolved tension carried into next beat, if any>
  - <Reference to the DR principle at work if applicable: mechanism education,
    social proof formatting, objection handling, urgency stacking, etc.>
- **Craft notes:** <composition / motion / sound / pacing observation worth stealing>

## Structural map

A short table or bulleted timeline showing how beats group into acts (hook block /
agitation block / mechanism block / proof block / offer block / close). Note where
the offer drops, where the longest unresolved tension lives, and where retention is
most at risk.

## What to steal / what to fix

- **Steal:** specific techniques transferable to other ads in this category
- **Fix:** weaknesses, missed beats, or places this ad leaks attention/credibility
```

## The psychological layer — what to evaluate for every beat

Cover every one of these dimensions across the whole ad — this skill is meant to be universal, so don't skip any:

- **Hook mechanics:** What stops the scroll? Curiosity gap? Pattern interrupt? Specificity (numbers, names, places)? Direct callout to the avatar? Visual oddity? Sound design hit?
- **Pattern interrupts:** Where does the ad break the viewer's expected rhythm — visually, audibly, or narratively — to keep retention?
- **Emotional state mapping:** Name the dominant emotion the viewer feels at each beat (curiosity, recognition, fear, hope, vindication, urgency, etc.). Note when the state shifts and what causes the shift.
- **Belief-shift architecture:** For every beat doing persuasion work, state the OLD belief getting broken and the NEW belief getting installed. This is the spine of direct-response copy — without belief shifts, beats are just decoration.
- **Mechanism education:** When does the ad explain WHY/HOW the solution works? Is the mechanism literal (e.g. "apigenin relaxes smooth muscle") or metaphorical (e.g. a "gut stall" framework)? Metaphor frameworks usually weaken sophisticated avatars — call it out when this happens.
- **Social proof formatting:** How is proof delivered — testimonial card, before/after, count ("50,000 women"), specificity, third-party endorsement, celebrity, doctor in a white coat? Is the proof concrete or vague?
- **Objection handling:** Which objections does the ad pre-empt, and at which beats? Are they handled with confidence (one-line dismissals) or sophistication (deep proof)? Match this to the implied avatar sophistication level.
- **Urgency / scarcity:** Does the offer beat manufacture urgency? Is it genuine (limited supply, sale ends) or manufactured (artificial countdown)? How aggressive vs. casual is the close?
- **CTA architecture:** How does the close stack offer, guarantee, bonuses, price anchor, urgency, and call-to-action language?
- **Visual/audio craft:** Composition, motion (camera + subject), color palette, lighting mood, sound design (music drops, whooshes, SFX hits, VO delivery — intimate vs. broadcast vs. hype). Note when craft amplifies persuasion vs. when it works against it.
- **Pacing / retention risk:** Identify the longest beats and longest gaps without a new hook or pattern interrupt — that's where viewers drop off. Identify the unresolved tension/promise carried across beats that keeps them watching.
- **Avatar match:** Does the ad assume the right sophistication level for its target? Where does it talk down to a sophisticated buyer or over the head of a beginner?

## Rules & standards

- Cover every beat — don't skip beats to save time.
- Don't couple the analysis to one specific brand's voice or products unless the user explicitly asks for adaptation to their brand — this teardown should work equally well on a competitor's ad, a viral organic post, or anything else.
- Keep the frames and transcript/manifest around after finishing — they're often reused for downstream work (adapting the ad for a brand, sourcing B-roll, scripting a new version).
- Don't apply this process to pure static images, text-only landing pages, or audio-only content — those need a different kind of analysis (image ad breakdown, or a page/funnel audit).
