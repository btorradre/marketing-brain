# Sourcing plan, verdict schema, and QA checklist

Deeper reference material for the tiktok-broll-crawler skill: the full sourcing-plan
structure, the visual-match-gate verdict structure, the contact-sheet audit checklist,
and the deliverable job layout.

## Sourcing plan structure

One record per slot. Recommended fields:

```json
{
  "job": "example-hook-v3",
  "brand": "example-brand",
  "brand_context": "Example brand, celery juice fiber gummies for GLP-1 users. B-roll subjects: real, relatable women 30-55. No competitor supplement products visible.",
  "slots": [
    {
      "slot_id": "S01",
      "script_line": "By 6pm my stomach was so bloated I looked six months pregnant.",
      "emotion": "frustrated, uncomfortable, defeated — physically miserable",
      "action": "woman clutching visibly bloated stomach, wincing, couch/bed, or lifting shirt to show bloat",
      "mode": "search",
      "search_terms": ["bloated stomach end of day", "bloating before bed"],
      "per_term_count": 10,
      "min_duration_s": 4,
      "max_duration_s": 60
    }
  ]
}
```

Field notes:

- `brand_context` — the avatar's age range, vibe, and disqualifiers (e.g. "no competitor
  products visible"). This is what the gate uses to reject off-avatar or competitor
  footage, so write it explicitly rather than assuming it's implied.
- `slot_id` — a short stable ID (`S01`, `S02`, ...) so downloads, verdicts, and delivered
  clips can all be organized under the same key.
- `script_line` — the exact line of the script this B-roll sits under.
- `emotion` — what's on the subject's face/body, not the topic of the line.
- `action` — a concrete, frame-filling physical description ("thumb turning the dose
  dial, close-up"), never an abstract topic ("medication handling").
- `mode` — `search` (keyword, the default), `hashtag`, `sound`, `user`, or an explicit
  list of URLs for hand-picked or already-found links.
- `search_terms` — 2–4 short subject/product nouns or voice-of-customer phrases (1–4
  words each) that triangulate the subject from different angles. Never the full action
  sentence — see the search-term law in SKILL.md.
- `per_term_count` — candidates to pull per search term. Default 10+, since most
  candidates will be rejected by the gate.
- `min_duration_s` / `max_duration_s` — duration bounds for the source video (not the
  extracted segment). Don't set `max_duration_s` low just to filter out talking-head
  videos — the needed moment is often buried inside one.

## Visual-match gate verdict structure

For every downloaded candidate, the vision-language model pass should return a
structured verdict along these lines:

```json
{
  "slot_id": "S01",
  "candidate_id": "<video id or filename>",
  "match": true,
  "confidence": 78,
  "best_segment": { "start_s": 14.2, "end_s": 17.6 },
  "emotion_observed": "visibly uncomfortable, grimacing, hand on stomach",
  "action_observed": "pulls up shirt hem to show bloated stomach, winces",
  "flags": [],
  "reasoning": "Subject stops talking at 14.2s, lifts shirt, grimaces at the bloat for ~3.4s before resuming speech. Clean segment, no watermark or caption overlay in this window."
}
```

Hard-reject flags (evaluated against the **best segment only**, not the whole video):

- `TALKING_TO_CAMERA` — subject is talking directly to camera during the needed segment.
- `BURNED_CAPTIONS` — burned-in captions cover the needed segment.
- `WATERMARK` — a visible watermark is on the needed segment.
- `COMPETITOR_PRODUCT` — a competitor's product is visible.

A soft flag worth keeping separate from a hard reject:

- `VERTICAL_CROP_RISK` — the required action is real but small/off-center in frame; note
  it for salvage-by-cropping rather than rejecting the clip outright.

Passing clips (confidence ≥ threshold, 65/100 is a reasonable default) get their best
segment trimmed out with a small padding buffer (e.g. +0.25s on each side, or 1.5s of
editor handle room) rather than the whole raw file being delivered. Cache verdicts by
candidate ID so re-runs only analyze newly added candidates.

## Contact-sheet audit checklist

Build one contact sheet per surviving clip (a labeled row of frames sampled across the
clip), then grade every sheet against this list before anything is delivered. A clip
fails and gets deleted (with the reason noted) if any of these are true:

1. **Fails the visual subject test** — someone unfamiliar with the brief couldn't
   identify the required action just from the frames.
2. **Off-avatar** — the subject is obviously outside the target avatar's age band, on a
   slot where the person's face is visible.
3. **Watermark/caption violation** — placement violates the plan's rules for that slot.
4. **AI-slop look** — the clip has an obvious AI-generated appearance, on a slot that
   specifically needs real footage.
5. **Displaying vs. performing** — the subject is showing an item to camera when the spec
   calls for a performed action (using it, not displaying it).
6. **Comedy-skit framing** — the clip reads as a scripted bit rather than genuine,
   unstaged footage.

If even the top-ranked clip in a slot fails this personal review, treat it as a signal
that the slot's spec or search terms are leaky — fix the spec and re-run the gate for
that slot rather than delivering a clip you know is wrong.

## Deliverable job layout

A complete sourcing job should contain:

```
<job>/
├── sourcing_plan.json          # the plan (Step 1)
├── source_map.jsonl            # url / author / stats per downloaded candidate
├── candidates/<slot_id>/...    # raw downloads, kept for re-analysis
├── verdicts.json               # gate verdicts (resumable cache)
├── matched/<slot_id>/...       # trimmed, gate-passed, human-audited clips
├── contact_sheets/<slot_id>.png
└── match_report.md             # per-slot table: verdict, confidence, segment, flags, source URL
```

Keep `candidates/` (the full raw downloads) even after trimming — a different segment of
the same video may be needed later, and the source URL/author fields are required if a
creator ever needs to be found and licensed for paid use.
