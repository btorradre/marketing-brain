---
name: ingest-swipes
description: Process queued GetHookd ads — classify by type, transcribe video, tag with metadata, route to correct vault folder, update indexes. Run this after the n8n workflow has pulled new ads into the queue. Triggers include "ingest swipes," "process the queue," "classify new ads," "run swipe intake," or any variation of processing queued ad data from GetHookd.
user_invocable: true
---

## GOLDEN NUGGET DOCTRINE (MANDATORY — locked 2026-07-11)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded DEEP FRAME in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: *is this the topic, or is this the motive?* If it's the topic, dig one layer deeper (memory loss → becoming my parent; GLP-1 bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes.** The golden nugget LEADS — very top of the piece, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence BEFORE drafting. When analyzing a reference ad/funnel/swipe instead of writing, state the nugget it's built on and whether it leads with it. If the research hasn't surfaced one, mine reviews/VOC/Reddit until it does — never default to a surface angle.

# Swipe Intake — Ad Classification & Routing System

This skill processes raw ad JSON files from the GetHookd intake queue, classifies each ad by type, transcribes video content, applies full metadata taxonomy, generates formatted markdown, routes to the correct vault folder, and updates indexes.

## WHEN TO RUN

Run this skill after the n8n workflow "GetHookd Swipe Intake — Daily Ad Puller" has deposited new JSON files into the queue. The n8n workflow runs daily at 7 AM or can be triggered manually. This skill processes whatever is in the queue.

## PATHS

```
QUEUE:      /Users/brooksorradre2/Documents/marketing brain/swipe-intake/queue/
PROCESSED:  /Users/brooksorradre2/Documents/marketing brain/swipe-intake/processed/
FAILED:     /Users/brooksorradre2/Documents/marketing brain/swipe-intake/failed/
VIDEOS:     /Users/brooksorradre2/Documents/marketing brain/swipe-intake/videos/
TRANSCRIPTS:/Users/brooksorradre2/Documents/marketing brain/swipe-intake/transcripts/
LOGS:       /Users/brooksorradre2/Documents/marketing brain/swipe-intake/logs/
MANIFEST:   /Users/brooksorradre2/Documents/marketing brain/swipe-intake/manifest.json
```

**Routing destinations:**
```
LONG_FORM:    /Users/brooksorradre2/Documents/marketing brain/long form copy/references/{brand_slug}/
VIDEO_ADS:    /Users/brooksorradre2/Documents/marketing brain/video ads/references (transcripts)/
HOOKS:        /Users/brooksorradre2/Documents/marketing brain/hook generation/references/
ADVERTORIAL:  /Users/brooksorradre2/Documents/marketing brain/advertorial/references/
LISTICLE:     /Users/brooksorradre2/Documents/marketing brain/listicle/references/
```

**Index files to update:**
```
LONG_FORM_INDEX: /Users/brooksorradre2/Documents/marketing brain/long form copy/references/REFERENCE-AD-INDEX.md
```

## PROCESSING SEQUENCE

For each JSON file in the queue:

### Step 1: Read and Parse
- Read the JSON file from queue/
- Extract: `id`, `body` (Facebook copy text), `title`, `landing_page`, `display_format`, `media` (video URLs), `performance_score`, `days_active`, `start_date`, `_brand_name`, `_brand_slug`
- If the JSON is malformed or missing critical fields (`id`, `body` or `media`), move to `failed/` with error note

### Step 2: Video Transcription (if applicable)
- If `display_format` is "VIDEO" and `media` array contains a video URL:
  1. Download the video to `videos/{gethookd_id}.mp4` using curl
  2. Transcribe using Gemini API:
     - Upload video file to Gemini Files API
     - Prompt: "Transcribe this video ad word for word. Include all spoken text. If there is text on screen, note it in brackets. Return only the transcript, no commentary."
     - Save raw transcript to `transcripts/{gethookd_id}.txt`
  3. If transcription fails (network error, Gemini rate limit, dead URL), log the failure and continue processing based on body text alone. Add `transcription_failed: true` to metadata.
  4. Clean up the video file from `videos/` after transcription

### Step 3: Classify Ad Type
Run the classification decision tree in strict order:

1. **VIDEO AD**: Has video media AND body text word count < 500. The video IS the content; Facebook copy is just a teaser. Route as video-ad.

2. **LONG-FORM COPY**: Body text word count >= 1,000 AND contains narrative indicators. Check for ANY of these: character names or dialogue markers (quotes with attribution), temporal markers ("Week 1", "Three months later", "That morning"), mechanism education (cause-and-effect language, "because", "the reason", "what actually happens"), erosion stacking (multiple scenes of decline). If >= 1,000 words with 2+ indicators, classify as long-form-copy. NOTE: If the ad also has video, still classify as long-form-copy — the video gets transcribed and included but the body text is the primary content.

3. **ADVERTORIAL**: If `landing_page` URL contains patterns suggesting editorial content: `/article`, `/blog`, `/story`, `/health/`, `/wellness/`, `/discover/`, domain names containing "journal", "health", "insider", "daily", "report". Classify as advertorial — the Facebook copy may be short, but the landing page is the content.

4. **LISTICLE**: If `landing_page` URL contains patterns suggesting list format: `/reasons`, `/best-`, `/top-`, `X-things`, numbered slug patterns, or the body text itself is a numbered list format. Classify as listicle.

5. **HOOK**: Body text < 300 words, no mechanism education, no narrative arc, no erosion stacking. This is a standalone hook — pure attention-grabbing opening. Classify as hook.

6. **FALLBACK**: If none of the above match clearly, default to long-form-copy. Better to have a misclassified long-form that gets manually re-sorted than to lose it.

### Step 4: Apply Metadata Tags
Read the body text (and transcript if available) and classify across six dimensions:

**Mechanism Type:**
- LINEAR: Single reframe, one cause → one effect. "Wrong organ." "Wrong metric."
- BRANCHING: One root cause with multiple downstream consequences
- CYCLE: Problem feeds itself — A causes B causes C causes more A
- NONE: No mechanism education present (common in hooks and short video ads)

**Authority Resistance:**
- LOW: Avatar already frustrated with current approach
- MEDIUM: Avatar skeptical but not defending a specific prescriber
- HIGH: Avatar embedded in medical authority (married to prescriber, identity tied to compliance)
- GENERATIONAL: Avatar watched approach fail in family member
- NONE: Not applicable (hooks, short video)

**Solution Complexity:**
- DIRECT: Guide character identifies criteria, narrator finds product
- EXTENSIVE_VILLAIN_CATALOG: Multiple wrong solutions, each torn down
- FAILED_SOLUTION_WITHIN_SOLUTION: Right ingredient, wrong form/concentration
- NONE: Not applicable

**Architecture:**
- STORY_DOMINANT: 55-65% emotional clearing, story IS the conversion mechanism
- MECHANISM_DOMINANT: 60-70% mechanism education, biology creates urgency
- AUTHORITY_DISMANTLING: Multi-scene architecture dismantling trusted authority
- PARALLEL_TIMELINE: Narrator mapped against family member's trajectory
- DISCOVERY_DISAPPOINTMENT_REDISCOVERY: False positive requires second explanation
- NOT_APPLICABLE: Hooks, short video

**Hook Type** (classify the opening 1-5 lines):
- authority-disruption: Opens by questioning a trusted authority
- family-truth: Family member reveals something
- symptom-stacking: Rapid symptom listing with attribution
- lab-results: Opens with specific numbers/metrics
- generational-fear: "My mother/father had this..."
- accidental-discovery: Stumbled onto something unexpected
- timeline-opener: Specific date or time as opening
- confrontation: Direct challenge or dramatic moment
- credential-opener: "I'm a [profession]..."
- list-format: Numbered or bulleted opening

**Narrator Type:**
- expert: Doctor, specialist, professional in the field
- patient: Person with the condition
- witness: Nurse, caregiver, family member who watched
- spouse: Married to either the authority or the sufferer
- parent: Child's condition drives the story
- child: Adult child caring for aging parent
- pharmacist: Pharmacy professional
- institutional: Nurse, hospital worker with systemic perspective
- friend: Peer recommendation
- not-applicable: Hooks without clear narrator

### Step 5: Generate Markdown File
Create a formatted markdown file with YAML frontmatter:

```markdown
---
gethookd_id: {id}
brand: {_brand_name}
brand_slug: {_brand_slug}
platform: {platform}
performance_score: {performance_score}
days_active: {days_active}
start_date: {start_date}
ad_type: {classified_type}
mechanism_type: {mechanism_type}
authority_resistance: {authority_resistance}
solution_complexity: {solution_complexity}
architecture: {architecture}
hook_type: {hook_type}
narrator_type: {narrator_type}
landing_page: {landing_page}
video_length: {video_length if applicable}
date_ingested: {current date YYYY-MM-DD}
source: gethookd
---

# {brand} — {hook_type} ({narrator_type})

## Facebook Copy

{full body text}

## Video Transcript

{transcript if available, otherwise "No video transcript available"}

## Classification Notes

{Brief 2-3 sentence explanation of classification decisions — why this type, why this mechanism, etc.}
```

### Step 6: Route to Destination
Based on classification, route the markdown file:

**Long-Form Copy:**
- Create brand folder if it doesn't exist: `long form copy/references/{brand_slug}/`
- Count existing ads for this brand to determine sequential number
- Name: `{brand_slug}-ad-{NN}-{hook_slug}.md`
- `{hook_slug}` = first 3-5 significant words of the hook, kebab-case (e.g., "cardiologist-wife-lipitor", "thirteen-years-fatigue", "granddaughter-pool")

**Video Ad:**
- Check if `{brand_slug}-direct-response-video-ads.md` exists in `video ads/references (transcripts)/`
- If yes: append new ad section at the end with `## Ad #{N+1}` heading
- If no: create new file with standard header + first ad entry

**Hook:**
- Append to `hook generation/references/Facebook Ad Hooks Swipe File & Narrative Analysis.md`
- Search for existing `## Brand: {BrandName}` section
- If found: append new hook entry
- If not: add new brand section at end of file

**Advertorial:**
- Create: `advertorial/references/{brand_slug}-advertorial-{NN}.md`

**Listicle:**
- Create: `listicle/references/{brand_slug}-listicle-{NN}.md`

### Step 7: Update Index
**For long-form copy only:** Append to REFERENCE-AD-INDEX.md under a section called `## NEW INGESTIONS (Auto-classified — Needs Tiering)`:

```
| {brand_slug}-ad-{NN}-{hook_slug}.md | {hook description} | {narrator_type} | {architecture} | {mechanism_type} |
```

### Step 8: Update Manifest and Clean Up
- Add entry to manifest.json: `"{gethookd_id}": {"type": "{ad_type}", "brand": "{brand}", "destination": "{file_path}", "processed_at": "{timestamp}"}`
- Move the JSON file from `queue/` to `processed/`
- Delete the video file from `videos/` if it exists

### Step 9: Processing Summary
After all queued ads are processed, generate a summary log at `logs/{YYYY-MM-DD}_{HHMMSS}_run.md`:

```markdown
# Swipe Intake Run — {date} {time}

## Summary
- Ads processed: {count}
- Long-form copy: {count}
- Video ads: {count}
- Hooks: {count}
- Advertorials: {count}
- Listicles: {count}
- Failed: {count}

## Processed Ads
| ID | Brand | Type | Destination |
|---|---|---|---|
| {id} | {brand} | {type} | {path} |

## Errors (if any)
{error details}
```

## IDEMPOTENCY RULES

- Before processing any ad, check manifest.json for the gethookd_id. If already processed, skip.
- Before appending to any file (video transcript, hook swipe), search for the gethookd_id in the existing content. If found, skip the append.
- Before creating a new file, check if a file with matching gethookd_id exists in the destination folder. If yes, skip.

## ERROR HANDLING

- **Gemini transcription failure:** Process based on body text alone. Add `transcription_failed: true` to frontmatter. Include "VIDEO TRANSCRIPTION FAILED — classify from body text only" in classification notes.
- **Dead video URL (404/403):** Same as transcription failure.
- **Empty body text AND no video:** Move to `failed/` with note "No content to classify."
- **Malformed JSON:** Move to `failed/` with note "Malformed JSON."
- **Manifest corruption:** If manifest.json can't be parsed, rename to `manifest.json.bak.{timestamp}` and rebuild by scanning `processed/` folder filenames (extract gethookd_id from filename pattern `{id}_{slug}.json`).
- **Gemini rate limiting:** Wait 5s, retry. If still limited, wait 15s. If still limited, wait 30s. After 3 failures, skip transcription for this ad and continue.

## GEMINI TRANSCRIPTION

Use the Gemini API (key from .env: GEMINI_API_KEY) to transcribe video ads:

1. Download video: `curl -L -o videos/{id}.mp4 "{video_url}"`
2. Upload to Gemini Files API: `POST https://generativelanguage.googleapis.com/upload/v1beta/files`
3. Generate transcript: `POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent` with the uploaded file URI and transcription prompt
4. Extract text from response
5. Save to `transcripts/{id}.txt`

The existing pattern is in `tools/gemini_video_analyzer.py` — follow the same upload + generate flow.

## ADDING NEW BRANDS

To track a new brand:
1. Get the brand's GetHookd brand spy ID from the GetHookd platform
2. Open the n8n workflow "GetHookd Swipe Intake — Daily Ad Puller"
3. Edit the "Brand Registry" Code node
4. Add the new brand to the BRANDS array: `{ name: 'Brand Name', brandId: 12345, slug: 'brand-name' }`
5. Save and run the workflow — new ads will be pulled and queued
6. Run `/ingest-swipes` to process them

Brand folders are auto-created on first ad intake. No manual folder setup needed.
