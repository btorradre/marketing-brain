---
name: tiktok-broll-crawler
description: Sources real organic TikTok footage as B-roll for ad creatives, matched to the exact script line and emotion. Takes either a reference ad (analyzes it scene-by-scene to spec the emotion/action needed) or a creative brief + script with sourcing keywords, builds a slot-based sourcing plan, crawls and downloads candidate TikToks (Apify search / TikTokApi / yt-dlp), then runs EVERY candidate through a Gemini visual-match gate that verifies the footage shows the required emotion and action for that specific line before anything reaches the editor. Use when the user wants to "source B-roll from TikTok", "find real footage for this line/scene", "crawl TikTok for clips", or feeds a reference ad and asks for matching action shots.
disable-model-invocation: false
---

# TikTok B-Roll Crawler

Sources **real organic TikTok footage** for specific moments in an ad script. Every clip is visually verified by a Gemini subagent against the exact script line, required emotion, and required action before it counts as sourced. This is the skill that satisfies the "action beats = genuine rips, never AI" law.

**Location:** `~/.claude/skills/tiktok-broll-crawler/` — has its own Python 3.11 venv (`venv/`). Always use `venv/bin/python`, never system python.

---

## The Law

**No clip reaches the editor without passing the Gemini gate.** The gate watches every downloaded video and answers: *does any continuous segment of this footage visually show the emotion and action this script line needs, under a voiceover the viewer will hear instead of the TikTok's audio?* Topic-match is not a match — a person **talking about** bloating is not a person **looking** bloated. Expect a high rejection rate; that is the gate doing its job. Source wide (15–25 candidates per slot), keep few.

---

## Pipeline

```
Input A: reference ad  ──► scene/emotion autopsy ─┐
Input B: brief + script + keywords ───────────────┤
                                                  ▼
                              [1] sourcing_plan.json   (Claude writes this)
                                                  ▼
                              [2] crawl.py  — search + download candidates
                                                  ▼
                              [3] analyze.py — Gemini gate on EVERY candidate
                                                  ▼
                              [4] matched/<slot>/rankNN_*.mp4  + match_report.md
```

### Step 0 — Brand context first (LAW)

Load `brands/<brand>/` research docs before writing the plan. The plan's `brand_context` field is what the Gemini gate uses to reject competitor products and off-avatar subjects — write the avatar's age range, vibe, and disqualifiers into it.

### Step 1 — Build the sourcing plan

**Input A (reference ad):** watch the reference first (use the `watch` or `ad-watcher` skill, or Gemini directly). For each scene that needs sourced B-roll, extract: the script line it sits under, the *emotion on screen* (not the topic), the *physical action*, and the shot vibe. Then derive search terms.

**Input B (creative brief + script):** map each script line/beat that needs B-roll to a slot. When the brief has an exact-action table (e.g. "Every action B-roll clip described exactly": action / framing / line covered), make **one slot per action**, copying the brief's action text verbatim into the `action` field — don't collapse actions into one slot per line.

**Realism audit before sourcing (from Brooks's SOP Loom, 8/18):** read every action beat and ask "would this avatar actually do this?" before you source it. Example from the Loom: "woman scrolling a laptop late at night" — a woman in this avatar's situation researches on her *phone*, not a laptop. Fix the spec (and note the change in the plan) rather than sourcing an unbelievable beat.

**THE SEARCH-TERM LAW (from the same Loom):** search terms find the **subject neighborhood**; the **gate finds the moment**. TikTok search matches how people caption and talk, so:

- Search **short subject/product nouns and VoC phrases, 1–4 words**: `zepbound`, `ozempic close up`, `miralax`, `mounjaro shot`, `metamucil gummy`, `bloated end of day`.
- **NEVER search the brief's action sentence.** Demonstrated failure: searching "Woman fanning 2-3 pens in her hand" returned calligraphy pens and colored pencils. The action phrasing goes in the slot's `action` field for the gate — not in `search_terms`.
- Give every slot 2–4 terms that triangulate the subject from different angles (product name, condition VoC, action-format phrases like "bloat check").

Write `sourcing_plan.json` into the job dir:

```json
{
  "job": "motilli-hook-v3",
  "brand": "motilli",
  "brand_context": "Motilli celery juice fiber gummies for GLP-1 users. B-roll subjects: real, relatable women 30-55. No competitor supplement products visible.",
  "engine": "auto",
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
      "max_duration_s": 60,
      "duration_needs_s": 4
    }
  ]
}
```

Slot fields: `mode` = `search` (keyword, default) | `hashtag` | `sound` | `user` | `urls` (explicit `"urls": [...]` list, downloaded via yt-dlp — use for hand-picked or TrendTrack/Apify-found links). `per_term_count` = candidates per search term — default to 10+; the gate rejects most.

### Step 2 — Crawl

```bash
cd ~/.claude/skills/tiktok-broll-crawler
venv/bin/python crawl.py --plan <job>/sourcing_plan.json --output <job>
```

Engines (`--engine` or `"engine"` in the plan):
- **`auto` (default):** uses TikTokApi when `MS_TOKEN` is set in `marketing brain/.env`, otherwise Apify; TikTokApi failures fall through to Apify automatically.
- **`apify`:** `clockworks/free-tiktok-scraper` via `APIFY_API_TOKEN` (already in `.env`). Supports `search`, `hashtag`, `user`. **This is the verified-working path.**
- **`tiktokapi`:** the vendored DAN3002/Tiktok-Crawler path (`crawler/`, TikTokApi + Playwright). Needs a real `MS_TOKEN` from a logged-in tiktok.com browser cookie (DevTools → Application → Cookies → `msToken`) added to `marketing brain/.env`. `get_ms_token.py` can harvest an anonymous token but TikTok usually still blocks anonymous API calls — logged-in token or Apify. `sound` mode is tiktokapi-only.

Downloads land in `<job>/candidates/<slot_id>/<video_id>.mp4`, metadata in `<job>/candidates_meta.jsonl` (author, url, plays, duration — the source map for attribution/re-finding).

One-off (no plan): `venv/bin/python crawl.py --mode search --keys "girl packing weekender bag" --count 10 --slot S01 --output <job>`

### Step 3 — Gemini gate (mandatory, every candidate)

```bash
venv/bin/python analyze.py --plan <job>/sourcing_plan.json --output <job>
```

- Uploads each candidate to Gemini (`gemini-3-flash-preview`), gets a structured verdict: match, confidence, best usable segment timestamps, emotion/action actually on screen, flags, reasoning.
- **The moment lives inside a longer video.** The usable clip is usually 2–4 seconds inside a 30–90s talking video (the creator pauses talking to inject the pen, pinch their stomach, pour the powder). That's what Brooks does manually — scrub the whole timeline for the moment. So don't pre-filter talking-head candidates out of the crawl, don't set `max_duration_s` low to dodge talkers, and expect matches whose parent video is 90% unusable.
- Hard flags reject outright: `TALKING_TO_CAMERA`, `BURNED_CAPTIONS`, `WATERMARK`, `COMPETITOR_PRODUCT` (`--keep-flagged` demotes −25 confidence instead — only when a slot is desperate). All are judged on the **best segment**, not the whole video — a video that talks or has text overlays elsewhere is fine if the extracted segment is clean.
- Passing clips (default threshold 65, `--threshold N`) get their best segment **trimmed via ffmpeg** (video-only, +0.25s pad) into `<job>/matched/<slot_id>/rankNN_c<conf>_<id>.mp4`. `--no-trim` copies full clips.
- Resumable: verdicts cache in `verdicts.json`; re-runs only analyze new files. `--slot S02` limits to one slot.
- Report: `<job>/match_report.md` — per-slot table with verdict, confidence, segment, flags, and clickable source URLs.

### Step 4 — Contact sheets + Claude's own frame audit (mandatory before delivery)

Laws adopted from the b-roll-finder skill (`~/.claude/skills/b-roll-finder/`): **the agent never picks the final b-roll — the user does**, and **never deliver footage you haven't visually inspected**.

The Gemini gate is necessary but not sufficient — it has passed topic-matches before (a face on a "bloat" clip, a pen *displayed* instead of *used*). After the gate:

1. Build per-slot contact sheets of EVERY surviving clip:
   `venv/bin/python contact_sheet.py --output <job>` → `<job>/contact_sheets/<slot>.png` (one labeled row of frames per clip).
2. **Look at every sheet yourself** and grade each row against the auto-reject list — line by line, not "looks fine": (a) fails the visual subject test (a muted stranger couldn't name the required action from the frames); (b) subject obviously outside the avatar age band on a face-visible people slot; (c) watermark/caption state violates the plan's rules; (d) AI-slop look on a real-footage slot; (e) displaying-to-camera where the spec asks for a performed action; (f) comedy-skit framing. Delete failing clips from `matched/` and note why.
3. If a top rank fails your eyes, the slot spec or prompt is leaky — fix and re-gate that slot; never hand it over anyway.
4. Deliver the contact sheets WITH the clips — the user makes final picks from the sheets; `matched/` is the vetted shortlist, not the final selection.

Spec-writing rules learned the hard way:
- **Never write softeners** like "talking acceptable if the action reads" — the gate uses any exemption to rationalize a topic-match through.
- Faceless age-exemptions must say "only if the face NEVER appears in the best segment".
- The `action` field should describe what fills the frame ("thumb turning the dose dial close-up"), not the topic ("medication handling").
- Deliver **trimmed** best-segments (`--pad 1.5` for editor handles), not full clips — a 45s video with 3 good seconds reads as a miss to whoever opens it. Keep `candidates/` so full versions remain available.

### Step 5 — Deliver

Deliver the `matched/` clips + `match_report.md`. If a slot comes back empty: rewrite that slot's search terms (different VoC phrasing, adjacent hashtags), bump `per_term_count`, and re-run steps 2–3 **for that slot only** — don't loosen the gate first. Search-term strategy when a people-slot underfills: TikTok search skews young and comedic, so anchor terms to the avatar's community and age ("mounjaro over 40", "menopause bloating real") and to the exact action format ("bloat check", "weigh in wednesday") rather than the topic. Report which slots are filled and which are dry; never pad a dry slot with an unverified clip.

**Volume target:** a long-form VSL (~4 min) needs **30–40 sourced clips with room to cut** — size the plan (slot count × survivors per slot) against the ad's length, not against "one clip per slot".

**AI-generation fallback (per the SOP Loom):** if a slot is still dry after a term rewrite + re-crawl, don't keep grinding TikTok — convert that slot's `action` spec into a generation prompt and route it to the AI b-roll library instead (per the b-roll engine rule: Omni for VO-style ads; Seedance only for lipsync/complex passes). Mark those slots `AI-GENERATED` in the report so real-rip and generated footage never get confused — the "action beats = genuine rips" law still applies to action/testimonial beats; the fallback is for mechanism/insert-style visuals a real person plausibly never filmed.

**Salvage by crop:** a clip where the required action is real but small in frame can be zoomed/cropped in the edit — note "zoom in on X" in the report instead of discarding it (this is why `VERTICAL_CROP_RISK` is a soft flag, not a rejection).

---

## Job directory layout

Create jobs under the relevant brand's working area (or wherever the user is working):

```
<job>/
├── sourcing_plan.json
├── candidates_meta.jsonl        # source map: url/author/stats per video_id
├── candidates/<slot_id>/*.mp4   # raw downloads (keep for re-analysis)
├── verdicts.json                # Gemini verdicts (resume cache)
├── matched/<slot_id>/rankNN_c<conf>_<id>.mp4   # trimmed, verified B-roll
└── match_report.md
```

## Setup notes

- Deps live in `venv/` (TikTokApi 7.x, playwright + chromium/webkit, google-genai, yt-dlp). If the venv is ever rebuilt: `python3.11 -m venv venv && venv/bin/pip install -r crawler/requirements.txt --upgrade TikTokApi && venv/bin/pip install google-genai yt-dlp requests && venv/bin/playwright install webkit chromium`.
- Keys: `GEMINI_API_KEY` and `APIFY_API_TOKEN` are read from `marketing brain/.env` automatically. Optional: `MS_TOKEN` (enables tiktokapi engine), `APIFY_TIKTOK_ACTOR`, `GEMINI_VIDEO_MODEL`.
- Sourced clips are organic content by real creators — for ad usage, flag in the report that rights/whitelisting are the user's call; the `candidates_meta.jsonl` URL + author fields exist so creators can be found and licensed.
