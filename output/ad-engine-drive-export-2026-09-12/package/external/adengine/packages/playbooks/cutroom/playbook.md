---
name: cutroom
description: Visual creative briefs on Cutroom, the internal cloud-backed Milanote-style whiteboard (projects → boards → assets, synced to Supabase). Breaks a reference ad down into a visual storyboard board — script beats, frame screenshots, and emotion/direction notes laid out as parallel timelines (reference creative vs our version) — for editors and the team. Trigger on "break down this reference into a board", "map this reference visually", "brief board", "storyboard brief", "make a visual brief", "put this on the board", or any request to turn a reference video / creative concept into a visual editor-facing brief. Also handles Cutroom project management (create a project, move boards, sync to cloud).
---

# Cutroom — visual creative briefs

Cutroom lives at `~/Documents/marketing brain/cutroom/`. It is a local Milanote-style
whiteboard: boards are plain JSON files, images are plain files, and a small server renders
an editable canvas at **http://localhost:8765**. You never touch pixels — `board_builder.py`
does all layout from a semantic spec.

## 0. Make sure the server is running

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:8765/api/boards || true
```

If that is not `200`, start it (background, survives the session):

```bash
cd ~/Documents/marketing\ brain/briefboard && nohup python3 server.py > /tmp/cutroom.log 2>&1 &
```

## 1. Reference breakdown workflow (the main job)

Given a reference video (URL or local file):

1. **Watch it properly.** Use the `watch` skill (or ad-watcher) to download, extract
   scene-change frames via ffmpeg, and pull the timestamped transcript. Never brief a
   reference you haven't seen frame-by-frame.
2. **Segment into beats.** A beat = one visual idea (usually one scene/shot, 1–5s).
   For each beat capture:
   - `t` — timecode range ("0:00-0:03")
   - `script` — the exact spoken line / VO / on-screen text during that beat
   - `frame` — absolute path to the best frame for that beat (pick the clearest, not the first)
   - `visual` — one line: what is literally on screen (shot type, subject, motion)
   - `emotion` — the emotion conveyed AND its DR function: hook / pattern interrupt /
     problem agitation / proof / demonstration / CTA. This is what the editor reads.
   - `note` — optional direction ("hold 0.5s longer than feels right", "hard cut, no transition")
3. **If adapting for a brand, load `brands/<brand>/` FIRST** (brand-context law), then add a
   second timeline `OUR VERSION` with the adapted beats. Its beats can omit `frame` and use
   `visual` text, or point at generated keyframes if they exist.
4. **Write the spec** to the scratchpad and build:

```bash
python3 ~/Documents/marketing\ brain/cutroom/board_builder.py /path/to/spec.json
```

5. **Deliver the board URL** (`http://localhost:8765/b/<slug>`). That IS the deliverable.

### Spec format

```json
{
  "title": "Meridian — 'That Bag' storyboard",
  "summary": "One paragraph the editor reads first: concept, angle, target emotion arc.",
  "timelines": [
    {
      "label": "REFERENCE CREATIVE",
      "source": "TikTok @creator · 1.2M views",
      "beats": [
        {"t": "0:00-0:03",
         "script": "I found the bag everyone keeps asking me about",
         "frame": "/abs/path/frames/f001.jpg",
         "visual": "Handheld selfie shot, creator walking, bag on shoulder",
         "emotion": "curiosity — hook; open loop on 'the bag'",
         "note": "Hard cut in mid-sentence, no intro"}
      ]
    },
    {"label": "OUR VERSION", "beats": [ ... ]}
  ],
  "notes": [
    {"title": "DO", "text": "…", "color": "#dff2e1"},
    {"title": "DON'T", "text": "…", "color": "#f9d9d4"}
  ],
  "moodboard": [{"image": "/abs/path.jpg", "caption": "grade / texture ref"}]
}
```

Every section except `title` is optional — the builder skips what's missing. Add
`"project": "<project-slug>"` to file the board in a Cutroom project (create one first via
`POST /api/projects {"name": "..."}` — GET the same path to list existing slugs; default
"general"). The builder auto-pushes the board + frames to Supabase after writing. Rebuilding with
the same title overwrites the same board (stable slug), so iterate freely.

## 2. Editor-brief laws (non-negotiable)

- **No file paths on the board.** Frames live ON the board as images; the editor never sees
  a path. Notes reference beats by timecode, not by filename.
- **Emotion notes are the brief.** Each beat's emotion card must say what the viewer should
  FEEL and what the beat is DOING in the ad (hook/proof/demo/CTA) — not restate the visual.
- **Script cards carry the exact words**, not a paraphrase.
- Segment-brief and brief-brevity standards from memory apply to any prose notes.

## 3. Freeform board edits (whiteboard mode)

Boards are JSON at `cutroom/boards/<slug>.json` — edit directly for anything the builder
doesn't cover, then just reload the page (no server restart needed). Card schema:

```json
{"id":"c1","type":"note|image|label|lane","x":0,"y":0,"w":260,"h":160,
 "title":"","text":"","src":"/assets/<board>/f.jpg","color":"#fdf3c9","size":22}
```

- `note` — sticky card (`title` bold, `text` body, `color` background)
- `image` — `src` under `/assets/` (copy files into `cutroom/assets/<board>/`), `text` = caption
- `label` — floating headline text (`size` px)
- `lane` — dashed container rectangle with an uppercase `title` tab
- `edges`: `[{"from":"c1","to":"c2"}]` draws dashed connectors between card centers

The team edits the same boards live in the browser (drag, dblclick-edit, drop images);
saves are instant and file-based, so re-read the JSON before scripted edits to a board a
human may have touched.

## 4. Built-in AI (✨ button)

The board UI has an ✨ AI button (bottom prompt bar) that POSTs to `/api/ai`. The server calls
the Anthropic API directly (`claude-opus-5`, key from `marketing brain/.env`,
`ANTHROPIC_API_KEY`) with the full board JSON and returns new note/label/lane cards, which are
appended and saved. This is for the TEAM's in-browser edits (add a lane, summarize, critique).
It cannot add images or run the watch pipeline — full reference breakdowns still go through
this skill and `board_builder.py`. Endpoint shape:
`POST /api/ai {"board": "<slug>", "prompt": "..."}` → `{"reply": str, "added": int}`.

## 5. Sharing / export

One self-contained read-only HTML (images inlined — Slack/email/artifact-ready):

```bash
python3 ~/Documents/marketing\ brain/cutroom/export_board.py <slug>
# → cutroom/exports/<slug>.html
```

For team access beyond this machine, publish the export as an artifact, or serve
`server.py` on the VPS / Tailscale.

## 6. Projects & cloud backend (Supabase)

Boards belong to projects (sidebar on the home page). API: GET/POST `/api/projects`,
DELETE `/api/projects/<slug>` (boards fall back to General). Board JSON carries
`"project": "<slug>"`.

Everything write-through syncs to Supabase Storage (private bucket `cutroom`,
keys in `marketing brain/.env` as SUPABASE_URL / SUPABASE_SECRET_KEY) via
`cutroom/supabase_store.py`. Server startup runs a two-way sync (pull missing, push all);
force one anytime with `POST /api/sync` or `python3 supabase_store.py push|pull|status`.
Local files always win on conflict — the cloud is backup + portability, not the editor.

## 7. Web app (Vercel) + editor access

Team-facing deployment: **https://cutroom-three.vercel.app** (Vercel project `cutroom`,
source in `cutroom/web/` — static pages + serverless functions reading the same Supabase
bucket; deploy with `cd cutroom/web && vercel deploy --prod --yes`).

Access is passcode-gated (cookie), two roles from `.env`:
- `CUTROOM_ADMIN_KEY` — Brooks: full edit + AI.
- `CUTROOM_VIEW_KEY` — editors: view-only (boards + screenshots render, all editing/AI/API
  writes are 401-blocked server-side).

Workflow: Brooks builds briefs (locally via this skill or on the web as admin), then sends
editors the URL + the view passcode. Web edits sync back through Supabase; the local server
picks them up on startup (newer-wins two-way sync).

## 8. Optional relational layer

`cutroom/supabase_schema.sql` creates cutroom_projects / cutroom_boards / cutroom_comments
(RLS locked, secret-key only). Brooks must paste it into the Supabase dashboard SQL editor
once; then `python3 cutroom/supabase_store.py migrate` populates the tables and every
subsequent board push auto-mirrors a row. Until then everything runs on Storage alone.
