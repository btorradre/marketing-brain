# Swipe Intake — Ad Classification & Routing System

This document describes a process for turning a queue of raw competitor/reference ad data (exported from an ad-spy tool as JSON records — one per ad, containing body copy, title, landing page URL, display format, media/video URLs, performance score, days active, start date, and brand tags) into a well-organized reference library: each ad gets classified by type, video content gets transcribed, each ad gets tagged with a full metadata taxonomy, a formatted record is written, it's filed into the correct reference collection, and an index is updated. Use this whenever there's a new batch of exported ad data to process into a research/swipe library ("process the queue," "classify these ads," "ingest these swipes").

Before drafting any classification notes or downstream copy work built from this material, apply the golden nugget doctrine: identify the single most emotionally loaded deep frame the ad is built on — the real motive that makes the buyer act, never just the surface topic. "Memory loss" is a topic; "I thought I was getting dementia just like my mother did, until I discovered this" is the frame. Surface angles buy mild hope or curiosity; deep frames trigger identification so strong the reader feels caught. When analyzing a reference ad instead of writing new copy, state the nugget it's built on and whether the ad actually leads with it.

## How to use this

Maintain a small set of reference collections, organized by content type (e.g., long-form copy, video ad transcripts, standalone hooks, advertorials, listicles), each broken down by brand. Maintain one running index file for the long-form copy collection so newly ingested ads can be found and triaged later. Maintain a manifest recording which source ads have already been processed, to avoid reprocessing.

For each ad record in the queue, work through these steps in order:

### 1. Read and parse

Extract: id, body copy text, title, landing page URL, display format, media (video URLs), performance score, days active, start date, brand name, brand slug. If the record is malformed or missing critical fields (id, body, or media), set it aside as failed with a note explaining why, and move on to the next record.

### 2. Transcribe video, if applicable

If the ad's display format is video and it has a video URL:
1. Download the video.
2. Transcribe it word-for-word using a video-understanding or transcription capability, with an instruction like: "Transcribe this video ad word for word. Include all spoken text. If there is text on screen, note it in brackets. Return only the transcript, no commentary."
3. If transcription fails (dead link, rate limit, network error), don't block the whole record — classify from the body text alone and flag the record as having a failed transcription.
4. Discard the downloaded video file once transcription is done (or once it's failed) — no need to keep raw video around after ingestion.

### 3. Classify ad type

Run this decision tree in strict order, taking the first branch that matches:

1. **Video ad**: has video media AND body text under 500 words. The video IS the content; any accompanying text is just a teaser.
2. **Long-form copy**: body text is 1,000+ words AND shows 2 or more narrative indicators from this list: character names or attributed dialogue/quotes; temporal markers ("Week 1," "Three months later," "That morning"); mechanism education (cause-and-effect language — "because," "the reason," "what actually happens"); erosion stacking (multiple scenes depicting decline). If the ad also has video, still classify it as long-form copy — transcribe and include the video, but treat the body text as primary.
3. **Advertorial**: the landing page URL looks editorial (path segments like `/article`, `/blog`, `/story`, `/health/`, `/wellness/`, `/discover/`, or a domain suggesting a publication — "journal," "health," "insider," "daily," "report"). The Facebook/ad copy itself may be short; the landing page is the real content.
4. **Listicle**: the landing page URL or the body copy itself shows list-format patterns (`/reasons`, `/best-`, `/top-`, "X things," numbered slug patterns, or a numbered-list body).
5. **Hook**: body text under 300 words, no mechanism education, no narrative arc, no erosion stacking — a standalone attention-grabbing opening.
6. **Fallback**: if nothing matches clearly, default to long-form copy — a misclassified long-form entry that gets manually re-sorted later is better than losing the ad entirely.

### 4. Apply metadata tags

Read the body text (and transcript, if any) and classify the ad across six dimensions:

**Mechanism type**
- Linear — a single reframe, one cause leading to one effect ("wrong organ," "wrong metric").
- Branching — one root cause with multiple downstream consequences.
- Cycle — the problem feeds itself (A causes B causes C causes more A).
- None — no mechanism education present (common in hooks and short video ads).

**Authority resistance**
- Low — the avatar is already frustrated with their current approach.
- Medium — the avatar is skeptical but not defending a specific prescriber/authority.
- High — the avatar is embedded in medical/professional authority (e.g. married to a prescriber, identity tied to compliance with an expert's advice).
- Generational — the avatar watched this approach fail in a family member.
- None — not applicable (hooks, short video).

**Solution complexity**
- Direct — a guide character identifies the criteria, the narrator finds the product.
- Extensive villain catalog — multiple wrong solutions, each torn down in turn.
- Failed solution within solution — right ingredient, but the wrong form or concentration.
- None — not applicable.

**Architecture**
- Story-dominant — 55-65% emotional clearing; the story itself is the conversion mechanism.
- Mechanism-dominant — 60-70% mechanism education; the biology creates the urgency.
- Authority-dismantling — a multi-scene structure that dismantles a trusted authority.
- Parallel timeline — the narrator's trajectory is mapped against a family member's.
- Discovery-disappointment-rediscovery — a false positive requires a second explanation.
- Not applicable — hooks, short video.

**Hook type** (classify the opening 1-5 lines)
- Authority-disruption — opens by questioning a trusted authority.
- Family-truth — a family member reveals something.
- Symptom-stacking — rapid symptom listing with attribution.
- Lab-results — opens with specific numbers/metrics.
- Generational-fear — "my mother/father had this…"
- Accidental-discovery — stumbled onto something unexpected.
- Timeline-opener — a specific date or time as the opening.
- Confrontation — a direct challenge or dramatic moment.
- Credential-opener — "I'm a [profession]…"
- List-format — numbered or bulleted opening.

**Narrator type**
- Expert — doctor, specialist, professional in the field.
- Patient — the person with the condition.
- Witness — nurse, caregiver, family member who watched it happen.
- Spouse — married to either the authority figure or the sufferer.
- Parent — the story is driven by a child's condition.
- Child — an adult child caring for an aging parent.
- Pharmacist — pharmacy professional.
- Institutional — a nurse or hospital worker with a systemic perspective.
- Friend — peer recommendation.
- Not applicable — hooks without a clear narrator.

### 5. Write the formatted record

Produce a markdown file with frontmatter capturing all the extracted fields and classification tags, structured like this:

```markdown
---
source_id: {id}
brand: {brand_name}
brand_slug: {brand_slug}
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
---

# {brand} — {hook_type} ({narrator_type})

## Ad Copy

{full body text}

## Video Transcript

{transcript if available, otherwise "No video transcript available"}

## Classification Notes

{Brief 2-3 sentence explanation of classification decisions — why this type, why this mechanism, etc.}
```

### 6. File the record

Route the finished markdown file into the right reference collection based on its classified type:

- **Long-form copy**: file under that brand's long-form folder, named with a sequential number and a short kebab-case slug drawn from the hook's first few significant words (e.g. `brand-ad-04-cardiologist-wife-lipitor.md`).
- **Video ad**: append to (or create) a single running "direct response video ads" file per brand, adding each new ad as its own numbered section.
- **Hook**: append to a running swipe file of hooks, filed under a section for that brand (create the brand section if it doesn't exist yet).
- **Advertorial**: file under that brand's advertorial folder with a sequential number.
- **Listicle**: file under that brand's listicle folder with a sequential number.

### 7. Update the index (long-form copy only)

Append a row to the running index under a section for newly ingested, not-yet-manually-reviewed entries:

```
| filename | hook description | narrator_type | architecture | mechanism_type |
```

### 8. Update the manifest and clean up

Record the source ad's id, classified type, brand, destination file, and processing timestamp in the manifest so it's never reprocessed. Discard any downloaded video file once transcription is complete.

### 9. Write a run summary

After the whole queue is processed, write a short summary log: counts by type (long-form, video, hooks, advertorials, listicles, failed), a table of every processed ad (id, brand, type, destination), and any error details.

## Rules & standards

**Idempotency** — before processing any record, check whether its id is already in the manifest; skip if so. Before appending to any running file (a video-ad transcript file, a hook swipe file), search for that id in the file's existing content first and skip the append if it's already there. Before creating a new file, check whether a file for that id already exists in the destination folder.

**Error handling**
- Transcription failure or a dead video link: fall back to classifying from body text alone, and flag the record clearly as having a failed/missing transcript.
- Empty body text AND no video: set the record aside as failed, with the note "no content to classify."
- Malformed source JSON: set the record aside as failed, with the note "malformed JSON."
- A corrupted manifest: back it up under a timestamped filename and rebuild it by scanning the already-processed folder for filenames matching the known id pattern.
- Rate limiting on the transcription service: retry with increasing backoff (e.g. wait 5s, then 15s, then 30s); after repeated failures, skip transcription for that ad and continue processing the rest of the queue from body text alone.

**Adding a new brand to track**: register the brand's identifier with whatever ad-spy source is being used, and make sure that brand is included in future queue pulls. Brand folders in the reference library should be created automatically the first time an ad for that brand is ingested — no manual folder setup should be required.
</content>
