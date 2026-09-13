# TikTok B-Roll Crawler

This document describes a process for sourcing **real, organic TikTok footage** to use as B-roll in an ad, matched to a specific script line and the exact emotion/action that line needs — as opposed to generating fake footage. Every candidate clip must be visually verified against the exact script line, required emotion, and required action before it's allowed to reach an editor. Use this whenever someone wants to source B-roll from TikTok, find real footage for a specific line or scene, crawl TikTok for clips, or hands over a reference ad and asks for matching action shots. This is the process that satisfies the rule that action beats in an ad must be genuine filmed footage, never an AI-generated fake.

## The law

**No clip reaches the editor without passing a rigorous visual-match check.** The check must watch every downloaded candidate video and answer: does any continuous segment of this footage visually show the emotion and action this script line needs, imagining a voiceover playing over it instead of the TikTok's own audio? Topic-match is not a match — a person **talking about** bloating is not a person **looking** bloated. Expect a high rejection rate; a high rejection rate means the check is doing its job. Source wide (15-25 candidates per slot) and keep few.

## How to use this

### Pipeline overview

1. Build a sourcing plan — one "slot" per script line/beat that needs real B-roll, each slot specifying the emotion, action, and search terms needed.
2. Crawl/search TikTok and download candidate videos per slot.
3. Run a visual-match gate (using a capable vision-language model) on every single downloaded candidate.
4. Build contact sheets (a grid of labeled frames per surviving clip) and personally review every one against a strict checklist before delivery.
5. Deliver the vetted, trimmed clips plus a match report for final human selection.

### Step 0 — Load brand context first

Before writing the sourcing plan, gather what's known about the brand and its target avatar (age range, vibe, disqualifying traits — e.g. "no competitor products visible," "avatar is women 30-55"). This context is what the visual-match gate uses to reject competitor products and off-avatar subjects, so write it explicitly into the plan.

### Step 1 — Build the sourcing plan

**If starting from a reference ad**: watch the reference closely first, scene by scene. For each scene that needs sourced B-roll, extract: the script line it sits under, the *emotion on screen* (not the topic), the *physical action*, and the shot vibe. Then derive search terms from that.

**If starting from a creative brief + script**: map each script line/beat that needs B-roll to its own slot. If the brief already specifies an exact action for each beat (e.g. a table of "action / framing / line covered"), make **one slot per action** and copy the brief's action text into the slot verbatim — don't collapse multiple distinct actions into a single slot per line.

**Realism audit before sourcing**: read every action beat and ask "would this avatar actually do this?" before sourcing it. Example: a spec calling for "woman scrolling a laptop late at night" is wrong if this avatar, in this situation, would realistically be on her phone, not a laptop. Fix the spec (and note the change) rather than sourcing an unbelievable beat.

**The search-term law**: search terms find the **subject neighborhood**; the visual-match gate finds the **moment**. TikTok (and social search generally) matches how people caption and talk, so:
- Search short subject/product nouns and voice-of-customer phrases, 1-4 words: e.g. `zepbound`, `ozempic close up`, `miralax`, `bloated end of day`.
- **Never search the brief's full action sentence.** A search like "woman fanning 2-3 pens in her hand" will return irrelevant results (e.g. calligraphy pens, colored pencils) because that's not how anyone captions a video. The action phrasing belongs in the slot's `action` field for the visual gate to check — not in the search terms.
- Give every slot 2-4 search terms that triangulate the subject from different angles: product name, condition-specific voice-of-customer phrasing, and action-format phrases people actually use as captions (e.g. "bloat check").

Structure the sourcing plan as a record per slot, something like:

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

Slot `mode` can be: `search` (keyword search, the default), `hashtag`, `sound`, `user`, or a fixed list of explicit URLs for hand-picked or already-found links. `per_term_count` = number of candidates to pull per search term; default to 10+ since most will be rejected by the gate.

### Step 2 — Crawl and download candidates

Search and download candidate clips per slot, using whatever scraping/search tooling is available (social-media scraping services, a direct video-download tool, or manual search-and-save if no automated tool is available). Save each downloaded clip under its slot, and keep a small metadata record per clip (source URL, author, view count, duration) — this is the source map needed later for attribution or for re-finding a clip, and is also required if the clip's creator ever needs to be found and licensed for paid use.

### Step 3 — Run the visual-match gate on every candidate (mandatory)

For each downloaded candidate, use a capable vision-language model to produce a structured verdict: does it match, what's the confidence, what are the best usable segment's timestamps, what emotion/action is actually on screen, any disqualifying flags, and the reasoning.

- **The needed moment usually lives inside a longer video.** The usable clip is often only 2-4 seconds inside a 30-90 second talking-head video (the creator pauses talking to do the exact gesture/action needed). Don't pre-filter out talking-head-style candidates from the crawl, and don't set a low max-duration to dodge talkers — expect that most of a matched video will be unusable and that's fine, only the extracted segment matters.
- Hard-reject flags: the subject is talking directly to camera during the needed segment, burned-in captions are covering the needed segment, a visible watermark is on the needed segment, or a competitor's product is visible. These should all be judged against the **best segment only**, not the whole video — a video that has talking or text elsewhere is fine if the specific segment being extracted is clean. (A "demote confidence but don't auto-reject" option can make sense for a desperately underfilled slot, used sparingly.)
- Passing clips (above some confidence threshold — 65 out of 100 is a reasonable default) should have their best segment trimmed out (with a small padding buffer, e.g. +0.25s) rather than delivering the whole raw file.
- Cache verdicts so re-runs only need to analyze newly added candidates, not everything again.
- Produce a report: a per-slot table showing verdict, confidence, segment timestamps, flags, and the clickable source URL for each candidate.

### Step 4 — Contact sheets and a personal frame-by-frame audit (mandatory before delivery)

Two standing rules apply here: **the agent never makes the final B-roll pick — the human does**, and **never deliver footage that hasn't been visually inspected by a human/agent, not just algorithmically scored**.

The automated visual-match gate is necessary but not sufficient — it can still pass a false match (e.g. a face appearing on a "bloat" clip, or a prop being displayed to camera instead of actually used). After the gate:

1. Build a contact sheet for every surviving clip in every slot — a single image showing a labeled row of frames sampled across that clip.
2. Look at every contact sheet personally and grade each clip against a strict checklist, line by line, not a vague "looks fine":
   - Fails the visual subject test — a person unfamiliar with the brief couldn't identify the required action just from the frames.
   - The subject is obviously outside the target avatar's age band, on a slot where the person's face is visible.
   - Watermark or caption placement violates the plan's rules.
   - The clip has an obvious AI-generated look, on a slot that specifically needs real footage.
   - The subject is displaying an item to camera when the spec calls for a performed action (using it, not showing it).
   - The clip reads as a comedy skit rather than genuine footage.
   Delete any clip that fails, and note why.
3. If even the top-ranked clip for a slot fails this personal review, the slot's spec (or its search terms) is leaky — go back and fix the spec, then re-run the gate for that slot. Never hand over a clip you know is wrong just because it scored well.
4. Deliver the contact sheets alongside the clips — final selection is made by the person reviewing the sheets. The surviving, gate-passed clips are a vetted shortlist, not the final answer.

**Spec-writing rules, learned from real failures:**
- Never write softening exemptions into a slot's spec, like "talking is acceptable if the action reads" — a gate given any exemption will use it to rationalize a topic-match through.
- If a slot allows the subject's face to be visible only under certain conditions, be explicit: "only if the face NEVER appears in the best segment."
- The `action` field should describe what physically fills the frame ("thumb turning the dose dial, close-up"), not the abstract topic ("medication handling").
- Deliver **trimmed** best-segments (with a little padding for an editor's handles, e.g. 1.5 seconds), not full raw clips — handing over a 45-second video with only 3 good seconds in it reads as a miss to whoever opens it next. Keep the full raw downloads archived separately in case a different segment is needed later.

### Step 5 — Deliver

Deliver the vetted, trimmed clips plus the match report. If a slot comes back empty: rewrite that slot's search terms (different voice-of-customer phrasing, adjacent hashtags/community terms), increase the candidate count per term, and re-crawl and re-gate **that slot only** — don't loosen the gate's standards as the fix. When a "people" slot is chronically underfilled, remember that general social search tends to skew young and comedic — anchor search terms to the specific avatar's community and age (e.g. "over 40," "real," a specific medical/lifestyle context) and to the exact action-format phrase people actually caption with (e.g. "bloat check," "weigh-in Wednesday") rather than the abstract topic. Clearly report which slots are filled and which are still dry; never pad a dry slot with a clip that didn't actually pass the check.

**Volume target**: a long-form video ad (~4 minutes) typically needs 30-40 sourced clips with room to cut freely — size the sourcing plan (number of slots × survivors needed per slot) against the ad's actual runtime, not against a flat "one clip per slot" assumption.

**Fallback when real footage genuinely can't be found**: if a slot is still dry after rewriting search terms and re-crawling, don't keep grinding indefinitely — convert that slot's action spec into a generation prompt and produce it with an image/video generation tool instead. Clearly mark any such slot as AI-generated in the final report so real footage and generated footage are never confused with each other. The rule that action/testimonial beats must be genuine footage still holds — this fallback is only appropriate for mechanism/insert-style visuals that a real creator plausibly never filmed in the first place (e.g. an internal-anatomy illustration), not for a person performing an action that should look authentically human.

**Salvage by cropping**: a clip where the required action is real but small/off-center in frame doesn't have to be discarded — note "zoom in on X" in the report so the editor can crop in, rather than throwing away a clip that's otherwise correct just because the framing is imperfect.

## Rules & standards

- Deliverable job structure per sourcing job: the sourcing plan, a source-map file (URL/author/stats per downloaded video), the raw downloaded candidates organized by slot (kept for re-analysis), a cache of gate verdicts (so re-runs are incremental), the final matched/trimmed clips organized by slot, and the match report.
- Sourced clips are organic content made by real third-party creators. For any use in a paid ad, rights and licensing/whitelisting of the creator is a decision for the brand owner to make explicitly — always keep the source URL and author name attached to every clip so the creator can be found and licensed if needed. Never assume a sourced clip is automatically clear to use in a paid campaign.
</content>
