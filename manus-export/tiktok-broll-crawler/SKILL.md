---
name: tiktok-broll-crawler
description: Sources real, organic TikTok footage as verified B-roll for ad scripts, matched to the exact emotion and action each line needs. Builds a slot-based sourcing plan (search terms plus required emotion/action per script line), searches and downloads candidate clips, then runs every candidate through a mandatory vision-model visual-match gate before trimming and delivering only clips that actually show the required moment. Use when sourcing B-roll from TikTok, finding real footage for a specific script line or scene, crawling TikTok for clips, or turning a reference ad's action beats into genuine (non-AI) footage.
---

# TikTok B-Roll Crawler

Sources **real, organic TikTok footage** for specific moments in an ad script — the alternative to generating fake AI footage for action beats. Every candidate clip is visually verified against the exact script line, required emotion, and required action before it is allowed to reach an editor.

This is the process that satisfies the rule: **action and testimonial beats in an ad must be genuine filmed footage, not an AI-generated fake.**

## The law

**No clip reaches the editor without passing a rigorous visual-match check.** The check must watch every downloaded candidate and answer one question: does any continuous segment of this footage visually show the emotion and action this script line needs, imagining a voiceover playing over it instead of the TikTok's own audio?

- **Topic-match is not a match.** A person *talking about* bloating is not a person *looking* bloated. A person holding a product up to camera is not the same as a person *using* it.
- **Expect a high rejection rate.** A high rejection rate means the gate is doing its job, not that something is broken.
- **Source wide, keep few.** Pull 15–25 candidates per slot; expect most to fail.

## Pipeline overview

1. Build a sourcing plan — one "slot" per script line/beat that needs real B-roll, each slot specifying the emotion, action, and search terms needed.
2. Search TikTok and download candidate videos per slot.
3. Run a visual-match gate (a capable vision-language model) on every single downloaded candidate.
4. Build contact sheets (a grid of labeled frames per surviving clip) and personally review every one against a strict checklist before delivery.
5. Deliver the vetted, trimmed clips plus a match report for final human selection.

## Step 0 — Load brand context first

Before writing the sourcing plan, gather what's known about the brand and its target avatar: age range, vibe, and disqualifying traits (e.g. "no competitor products visible," "avatar is women 30–55"). This context is what the visual-match gate uses to reject competitor products and off-avatar subjects, so write it explicitly into the plan as a `brand_context` field.

## Step 1 — Build the sourcing plan

**If starting from a reference ad:** watch the reference closely, scene by scene. For each scene that needs sourced B-roll, extract: the script line it sits under, the *emotion on screen* (not the topic), the *physical action*, and the shot vibe. Derive search terms from that.

**If starting from a creative brief + script:** map each script line/beat that needs B-roll to its own slot. If the brief already specifies an exact action per beat (e.g. a table of "action / framing / line covered"), make **one slot per action** and copy the brief's action text into the slot verbatim — don't collapse multiple distinct actions into a single slot per line.

**Realism audit before sourcing.** Read every action beat and ask "would this avatar actually do this?" before sourcing it. Example: a spec calling for "woman scrolling a laptop late at night" is wrong if this avatar, in this situation, would realistically be on her phone, not a laptop. Fix the spec (and note the change) rather than sourcing an unbelievable beat.

**The search-term law.** Search terms find the **subject neighborhood**; the visual-match gate finds the **moment**. Social search matches how people caption and talk, not how a script describes an action, so:

- Search short subject/product nouns and voice-of-customer phrases, 1–4 words: e.g. `zepbound`, `ozempic close up`, `miralax`, `bloated end of day`.
- **Never search the brief's full action sentence.** A search like "woman fanning 2–3 pens in her hand" returns irrelevant results (calligraphy pens, colored pencils) because that's not how anyone captions a video. The action phrasing belongs in the slot's `action` field for the visual gate to check — not in the search terms.
- Give every slot 2–4 search terms that triangulate the subject from different angles: product name, condition-specific voice-of-customer phrasing, and action-format phrases people actually use as captions (e.g. "bloat check").

The full sourcing-plan JSON structure (one record per slot, with all fields and a worked example) is in `references/sourcing-plan-and-gate-schema.md`. In short, each slot needs: an ID, the script line, the required emotion, the required action (concrete, frame-filling description — not an abstract topic), a sourcing mode (`search` / `hashtag` / `sound` / `user` / an explicit list of URLs for hand-picked clips), the search terms, how many candidates to pull per term (default 10+, since most will be rejected), and min/max duration bounds.

## Step 2 — Crawl and download candidates

Search and download candidate clips per slot using whatever TikTok search/download tooling is available — a social-media scraping service for keyword/hashtag/sound/user search, or a direct video-download tool for explicit URLs (hand-picked links or links already found through other research). Save each downloaded clip under its slot, and keep a small metadata record per clip: source URL, author, view count, duration. This source map is needed later for attribution, for re-finding a clip, and is required if the clip's creator ever needs to be found and licensed for paid use.

## Step 3 — Run the visual-match gate on every candidate (mandatory)

For each downloaded candidate, use a capable vision-language model to produce a structured verdict: does it match, what's the confidence, what are the best usable segment's timestamps, what emotion/action is actually on screen, any disqualifying flags, and the reasoning. The full verdict schema is in `references/sourcing-plan-and-gate-schema.md`.

- **The needed moment usually lives inside a longer video.** The usable clip is often only 2–4 seconds inside a 30–90 second talking-head video (the creator pauses talking to do the exact gesture/action needed). Don't pre-filter out talking-head-style candidates from the crawl, and don't set a low max-duration to dodge talkers — expect that most of a matched video will be unusable, and that's fine; only the extracted segment matters.
- **Hard-reject flags**, judged against the *best segment only* (not the whole video): the subject is talking directly to camera during the needed segment, burned-in captions cover the needed segment, a visible watermark is on the needed segment, or a competitor's product is visible. A video that talks or has text elsewhere is fine if the specific segment being extracted is clean. (A "demote confidence but don't auto-reject" option can make sense for a desperately underfilled slot, used sparingly.)
- Passing clips (above a confidence threshold — 65/100 is a reasonable default) should have their best segment trimmed out, with a small padding buffer (e.g. +0.25s), rather than delivering the whole raw file.
- Cache verdicts so re-runs only need to analyze newly added candidates, not everything again.
- Produce a report: a per-slot table showing verdict, confidence, segment timestamps, flags, and the clickable source URL for each candidate.

## Step 4 — Contact sheets and a personal frame-by-frame audit (mandatory before delivery)

Two standing rules apply: **the agent never makes the final B-roll pick — the human does**, and **never deliver footage that hasn't been visually inspected by a human, not just algorithmically scored.**

The automated visual-match gate is necessary but not sufficient — it can still pass a false match (e.g. a face appearing on a "bloat" clip, or a prop being displayed to camera instead of actually used). After the gate:

1. Build a contact sheet for every surviving clip in every slot — a single image showing a labeled row of frames sampled across that clip.
2. Look at every contact sheet personally and grade each clip against a strict checklist, line by line, not a vague "looks fine." The full checklist is in `references/sourcing-plan-and-gate-schema.md`; the core failure modes are: the required action isn't identifiable from the frames alone, the subject is obviously outside the avatar's age band (on a face-visible slot), watermark/caption placement violates the plan's rules, the clip has an obvious AI-generated look (on a slot that specifically needs real footage), the subject is displaying an item to camera rather than performing the action, or the clip reads as a comedy skit rather than genuine footage. Delete any clip that fails, and note why.
3. If even the top-ranked clip for a slot fails this personal review, the slot's spec (or its search terms) is leaky — go back and fix the spec, then re-run the gate for that slot. Never hand over a clip you know is wrong just because it scored well.
4. Deliver the contact sheets alongside the clips — final selection is made by the person reviewing the sheets. The surviving, gate-passed clips are a vetted shortlist, not the final answer.

**Spec-writing rules, learned from real failures:**

- Never write softening exemptions into a slot's spec, like "talking is acceptable if the action reads" — a gate given any exemption will use it to rationalize a topic-match through.
- If a slot allows the subject's face to be visible only under certain conditions, be explicit: "only if the face NEVER appears in the best segment."
- The `action` field should describe what physically fills the frame ("thumb turning the dose dial, close-up"), not the abstract topic ("medication handling").
- Deliver **trimmed** best-segments (with a little padding for an editor's handles, e.g. 1.5 seconds), not full raw clips — handing over a 45-second video with only 3 good seconds in it reads as a miss to whoever opens it next. Keep the full raw downloads archived separately in case a different segment is needed later.

## Step 5 — Deliver

Deliver the vetted, trimmed clips plus the match report. If a slot comes back empty: rewrite that slot's search terms (different voice-of-customer phrasing, adjacent hashtags/community terms), increase the candidate count per term, and re-crawl and re-gate **that slot only** — don't loosen the gate's standards as the fix.

When a "people" slot is chronically underfilled, remember that general social search tends to skew young and comedic — anchor search terms to the specific avatar's community and age (e.g. "over 40," "real," a specific medical/lifestyle context) and to the exact action-format phrase people actually caption with (e.g. "bloat check," "weigh-in Wednesday") rather than the abstract topic. Clearly report which slots are filled and which are still dry; never pad a dry slot with a clip that didn't actually pass the check.

**Volume target:** a long-form video ad (~4 minutes) typically needs 30–40 sourced clips with room to cut freely — size the sourcing plan (number of slots × survivors needed per slot) against the ad's actual runtime, not against a flat "one clip per slot" assumption.

**Fallback when real footage genuinely can't be found:** if a slot is still dry after rewriting search terms and re-crawling, don't keep grinding indefinitely — convert that slot's action spec into a generation prompt and produce it with an image/video generation tool instead. Clearly mark any such slot as AI-generated in the final report so real footage and generated footage are never confused with each other. The rule that action/testimonial beats must be genuine footage still holds — this fallback is only appropriate for mechanism/insert-style visuals a real creator plausibly never filmed in the first place (e.g. an internal-anatomy illustration), not for a person performing an action that should look authentically human.

**Salvage by cropping:** a clip where the required action is real but small/off-center in frame doesn't have to be discarded — note "zoom in on X" in the report so the editor can crop in, rather than throwing away a clip that's otherwise correct just because the framing is imperfect.

## Rules & standards

- A deliverable sourcing job includes: the sourcing plan, a source-map file (URL/author/stats per downloaded video), the raw downloaded candidates organized by slot (kept for re-analysis), a cache of gate verdicts (so re-runs are incremental), the final matched/trimmed clips organized by slot, and the match report. Full layout in `references/sourcing-plan-and-gate-schema.md`.
- Sourced clips are organic content made by real third-party creators. For any use in a paid ad, rights and licensing/whitelisting of the creator is a decision for the brand owner to make explicitly — always keep the source URL and author name attached to every clip so the creator can be found and licensed if needed. Never assume a sourced clip is automatically clear to use in a paid campaign.
