# Ad Engine Productization Plan

Working name: TBD (referred to below as "the product"). Written 2026-09-02 from a full inventory of `_engine/mcp/`, `cutroom/`, `_engine/pipelines/`, `_engine/tools/`, `brands/`, and both skill roots.


## Build status

**Phase 0 complete, 2026-09-02.** Repo at `~/Documents/marketing-apps/adengine/`. The exit gate is a script, not a judgment call: `scripts/phase0_check.sh` greps the engine for home-directory, vault, env-file, brand-literal, localhost, and API-key leaks, boots both MCP servers with an empty HOME and no vault mounted, and runs the test suite. It passes.

| Piece | State |
|---|---|
| Core: settings from env only, Store interface with local and Postgres backends, workspace auth context | Built, tested |
| Laws as data: 5 global rules, 4 brand example files, judgment laws | Built, tested |
| Playbooks as data: 69 playbooks extracted, section index, leak lint | Built, tested. 512 leak findings logged for the de-localization pass |
| Product truth: schema, renderer, 8 seed records | Built, tested. 4 records low confidence, those skills never had verbatim blocks |
| SQL schema: 23 tables, RLS policies, PostgresStore | Written, not yet applied to a database |
| dr server: 18 tools, per-card approval records, stale-on-swap, agent role cannot approve | Built, tested, boots |
| gen server: 24 tools, animate gate verifies board approval server-side, watcher ported with Gemini 3.7 Flash and Whisper, generic analyze-video | Built, tested, boots |
| Workers: store-backed queue, all provider polling inside workers | Built, tested |
| Docker image and compose | Written, unverified, daemon would not start |
| Timeline package: document, 48 typed ops, reducer, event log with per-author undo, inverse ops, assemble-from-board, JSON schema | Built, 110 tests, typechecks, builds. Tick rate 6000/s |
| Tenant zero: our 4 brands and 8 products seeded into a local workspace | Done |

## 1. Thesis

The local engine already splits along one clean seam, stated in the dr-os README: **machinery lives in the server, judgment lives in playbooks the calling model reads.** That seam is the product.

- **Machinery we host:** brand memory, reference ingest and frame-by-frame watch, the artifact contract, the law gate, the storyboard board with a real approval gate, generation jobs against every provider, a cost ledger, a video editor, and the performance loop.
- **Judgment the customer brings:** their own Claude (Claude Code, Claude Desktop, or an API key we run an agent on), reading our playbooks and doing the thinking.
- **Keys the customer brings:** kie.ai, ElevenLabs, HeyGen, Gemini, Higgsfield, fal, Anthropic, Meta, Shopify, Triple Whale. We meter, we never resell by default.

The customer gets the thing that took us a year to earn: a pipeline where nothing renders before a human approves a storyboard, laws are enforced at the write boundary, and every run compounds into a brand's angle bank instead of starting from a blank page.

Two laws from the current engine become product primitives, not features:

1. **Storyboard first.** Script → board → keyframes on the board → human approval on the board → animate. Animation refuses without a server-verified approved board.
2. **Our own editor: a full web CapCut.** The CapCut bridge is macOS accessibility-tree automation and can never be hosted. The product ships a browser editor at CapCut feature parity where the agent edits fully on the timeline using our editing SOPs as executable workflows, and the human steps in to intervene and quality-check at will.

## 2. What exists today

| Component | Where | State | Hosted verdict |
|---|---|---|---|
| dr-os MCP (14 tools) | `_engine/mcp/dr-os/` 750 LOC | Works over stdio and localhost HTTP | Re-host. Playbook-as-data pattern is inherently portable. |
| ad-engine MCP (24 tools) | `_engine/mcp/ad-engine/` 1,613 LOC | stdio only, SQLite registry, cost ledger | Re-host as job workers. Provider adapters (kie, ElevenLabs, HeyGen) reuse as-is. |
| Cutroom | `cutroom/` + Vercel `cutroom-three` | Vanilla JS canvas, JSON boards, Supabase Storage sync, no auth, whole-file last-writer-wins | Rebuild on Postgres with real approval state. Keep the layout engine (`board_builder.py`) and the card model. |
| Approval gate | `plan_runner.py:224` | Non-empty-string check on a slug | Rebuild as a state machine with approver identity. |
| UGC factory / scene replicator | `_engine/pipelines/` 1,460 LOC | Resumable SQLite job runners, parallel implementation of the MCP path | Fold into the worker fleet. One implementation, not two. |
| CapCut kit | `_engine/mcp/capcut-kit/` 1,346 LOC | macOS-only GUI automation | Not portable. Replaced by the editor. |
| Skills (108 unique) | `.claude/skills/` + `~/.claude/skills/` | ~50 generic, 20 brand-specific, ~15 ops, rest generation | Generic ones become versioned playbooks. Brand ones become a product-truth record type. Ops excluded. |
| Frameworks / SOPs / copywriting | `_engine/frameworks/`, `_engine/sops/`, `_engine/copywriting/` | ~1 MB of doctrine, plus ~30 third-party PDFs | Doctrine ships as playbooks. PDFs cannot ship. |
| Creative tracker | `_engine/creative-tracker/` | One Google Sheet, one OAuth user token, Triple Whale pull | Rebuild as tables plus connectors. |
| Launchpad | `_engine/launchpad/` :8787 | Reads local `~/.claude` session logs | Not portable. Replace with in-app cost and job dashboards. |
| Prior attempts | `~/Documents/marketing-apps/specialist`, `marketing-brain-cloud` | Specialist is a Next.js 15 + Supabase RLS + Stripe + Inngest skeleton | Reuse Specialist's auth, RLS, billing, and job scaffolding. |

### What breaks the moment it is hosted

- One shared `.env` with 48 keys; brand is a string column, not a security boundary.
- Absolute paths to one Mac in `.mcp.json`, `scene_replicator.py`, most production skills, and the board URLs returned to users (`http://localhost:8765/b/...`).
- ad-engine imports `~/.claude/skills/ad-watcher/pipeline.py` and `elevenlabs-agent/pipeline.py` at import time. The server does not boot without one user's home directory.
- 8 of 13 law-gate rules name our brands as Python literals.
- Product truth is 20 brand skills (47 KB for the Weekender alone) instead of data.
- No queue, no workers. Every provider is polled in-process by the calling model.
- Cutroom has `role() { return "admin" }`, RLS with zero policies, and no user model.
- 1.6 GB of board assets and 800 MB of job artifacts on a local filesystem. SQLite as system of record with local paths in `assets.path`.
- Two API keys hard-coded in source (GetHookd puller, ad-watcher Gemini fallback).
- Zero live brands have a `00-brief.md`. The onboarding artifact the loader expects does not exist in practice.
- Broken handoffs: `lfc-writer` is empty, `ad-concept-builder` references a missing decision table, `swipe-intake` routes to pre-reorg paths.

## 3. Product definition

**Who it is for.** DTC operators and small creative teams who already run Claude and want an ad factory, not a prompt library. Same profile as us a year ago.

**How they connect.** Three modes, one backend:

| Mode | Customer runs | We provide |
|---|---|---|
| Claude Code / Desktop | Their Claude with their Anthropic plan | Remote MCP server (streamable HTTP + OAuth) and an installable skills pack (plugin) |
| Any MCP host | Cursor, Sam, custom agents | Same remote MCP |
| In-app | Nothing local | Our web app runs an agent on their Anthropic key using the Claude Agent SDK, same tools |

**What they bring.** Provider keys, stored encrypted per workspace. Optional managed keys with markup is a later decision, not v1.

**What we provide.** Brand memory that compounds, the pipeline, the laws, the storyboard and approval gate, the editor, generation orchestration with a truthful cost ledger, and the performance loop.

**What they own.** Everything under their workspace: brand records, artifacts, boards, assets, renders. Export at any time.

## 4. Architecture

Three layers.

```
CUSTOMER'S CLAUDE ──── remote MCP (OAuth) ────┐
IN-APP AGENT (Agent SDK, their key) ──────────┤
BROWSER (web app) ────────────────────────────┤
                                              ▼
                              ┌─────────────────────────────┐
                              │ CONTROL PLANE               │
                              │ Postgres (RLS) · object     │
                              │ storage · credential vault  │
                              │ · job queue · realtime      │
                              └──────────────┬──────────────┘
                                             ▼
                              ┌─────────────────────────────┐
                              │ WORKER FLEET                │
                              │ ffmpeg/yt-dlp · provider    │
                              │ adapters · render · QA      │
                              └─────────────────────────────┘
```

**Stack decisions (recommended, change only with a reason):**

- **Web app:** Next.js + TypeScript on Vercel. Matches Specialist and the Cutroom web functions already deployed.
- **Database and auth:** Supabase Postgres with RLS, Supabase Auth, Supabase Storage with signed URLs, Realtime for board and editor presence. Specialist already has the RLS and billing scaffold.
- **Remote MCP:** Python, reusing the existing FastMCP servers, run as a service behind an OAuth gateway. Every tool takes a workspace from the token, never from an argument. The 2,363 lines of existing tool code carry over; the filesystem calls get replaced with DB and storage calls.
- **Queue and workers:** Postgres-backed queue (pgmq or graphile-worker style) feeding Python workers on Fly.io or Railway with ffmpeg, ffprobe, yt-dlp, curl baked into the image. Provider polling moves off the model and onto workers with webhooks back to the app.
- **Credential vault:** per-workspace envelope encryption (KMS-managed key), keys never returned to clients, only used by workers.
- **Render:** ffmpeg on workers. Browser preview via a lightweight canvas player over signed proxies, not a browser-side render.
- **Observability and billing:** Sentry, PostHog, Stripe usage-based metering from the cost ledger.

## 5. Data model

Tenant boundary is `workspace_id` on every row, enforced by RLS.

```
workspace ─┬─ member (role: owner | editor | viewer | agent)
           ├─ credential (provider, ciphertext, last_verified, balance_cache)
           ├─ brand ─┬─ brand_brief (the 00-brief the loader expects, as fields)
           │         ├─ house_law (rule, severity, regex | judgment, source)
           │         ├─ product ─┬─ product_truth (identity block, mechanism block,
           │         │           │   banned terms, colorways, dimensions, claims)
           │         │           ├─ product_asset (reference images, master seed)
           │         │           └─ concept
           │         ├─ artifact (kind: voc-index | angle-bank | angle | hook |
           │         │   brief | adaptation-plan | mechanism-doc | winner | survey;
           │         │   body, frontmatter, version, generated_by)
           │         ├─ reference (source url, resolved media, watch manifest, beats)
           │         └─ swipe
           ├─ board ─┬─ lane ── card (type, position, size, content, asset_ref)
           │         ├─ card_approval (card, approver, state, at, note)
           │         ├─ board_version
           │         └─ comment
           ├─ job (kind, provider, status, input, output, cost, parent_job)
           ├─ asset (storage key, kind, mime, duration, dims, provenance job)
           ├─ timeline (editor project: tracks, clips, captions, overlays; versioned)
           ├─ render (timeline version, preset, output asset, cost)
           ├─ ad (tracker row: naming convention id, concept family, axis, status)
           └─ ad_metric (source: meta | triplewhale, spend, roas, cpa, hook, hold)
```

The `artifact` table is the current `brands/<brand>/research/dr-os/` contract lifted into rows, frontmatter preserved as columns. The angle bank stays the durable asset with its fresh → active → fatigued → retired lifecycle and `tested_assets` links to `ad` rows.

## 6. The pipeline as a state machine

This is the current "Factory Loop" and pipeline guide A2, made mechanical.

| Stage | State | Who moves it | Server enforces |
|---|---|---|---|
| 1 | Concept logged | Claude via `push_concept` | Naming convention id minted |
| 2 | Reference ingested and watched | Worker job | Manifest with beats, frames, transcript |
| 3 | Strategy and script written | Customer's Claude with playbooks | Law gate on every artifact save |
| 4 | Storyboard built | Claude via `push_board` | Two lanes, one card per beat with timecode, script, visual, emotion |
| 5 | Keyframes generated onto the board | Worker jobs | Anchors before keyframes, no chaining, cost preflight |
| 6 | **Approval** | Human on the board | Every keyframe card has an approval row by a member with editor rights |
| 7 | Animated and voiced | Worker jobs | `animate` verifies board state server-side, refuses otherwise |
| 8 | Assembled in the editor | Human or Claude via editor tools | Timeline versioned, render metered |
| 9 | Launched and measured | Connectors | Metrics attach to the `ad` row, verdicts write back to the angle |

Approval is per card, with approve, reject with note, and re-roll. A board is "approved" only when every card in the our-version lane is approved. Approvals are events with identity and timestamp, visible on the card.

## 7. MCP tool surface, v1

Grouped by stage. Names carry over from today where they exist.

**Context.** `pipeline_guide`, `load_brand`, `load_product` (returns the verbatim identity and mechanism blocks), `list_playbooks`, `get_playbook`, `status`.

**Research and copy.** `ingest_reference`, `get_watch_manifest`, `lawgate`, `list_artifacts`, `read_artifact`, `save_artifact`, `push_concept`.

**Storyboard.** `push_board` (semantic spec in, board out, same layout engine), `get_board` (with approval state), `update_card`, `place_keyframe`, `export_board`.

**Generation.** `preflight`, `generate_anchors`, `generate_keyframes`, `animate_scenes` (gated), `generate_vo`, `clone_voice`, `list_voices`, `generate_avatar`, `generate_image`, `generate_video`, `get_job`, `list_jobs`, `get_asset`, `list_assets`, `cost_summary`, `provider_balance`.

**Editor.** `create_timeline`, `get_timeline`, `apply_edit` (one typed operation per panel action in the feature map: clips, tracks, keyframes, masks, text, captions, audio, effects, transitions, filters, export settings), `run_edit_workflow` (one of the named workflows in section 8.4), `qa_pass` (two-pass review, returns the review card), `get_style` and `update_style` (the brand editing style record), `frame_grab`, `get_waveform`, `get_markers`, `add_marker`, `import_capcut_draft`, `render`, `get_render`.

**Loop.** `record_ad`, `get_performance`, `apply_verdict`.

All tools are workspace-scoped from the OAuth token. No tool accepts a filesystem path. Media in and out is by asset id or signed URL.

## 8. The editor

A full web version of CapCut, feature for feature, with two operators on the same timeline: the agent, which edits fully on its own, and the human, who steps in to intervene and quality-check whenever they want. Nothing is agent-only or human-only. Every action the UI can take, the agent can take, and the reverse.

### 8.1 Two operators, one timeline

- The timeline is a versioned, event-sourced JSON document. Every UI gesture and every agent tool call is the same typed operation appended to the same log. Undo, version history, diffing, and blame come free.
- Concurrent editing by the agent and the human on one project uses a CRDT document so neither clobbers the other. The agent's edits appear live in the human's session, and the human's corrections appear in the agent's next read.
- The agent sees the project three ways: the timeline JSON, rendered frame grabs at any timecode, and audio waveform and transcript data. It never guesses what is on screen.
- Human QC surface: timecoded markers and comments, pinned frames, approve or reject the cut, side-by-side version compare, and "send back to agent with notes," which becomes a workflow run with the notes as instructions.

### 8.2 Architecture

- **Client:** React with a canvas-based timeline. Media plays through WebCodecs with proxy media generated on ingest, so scrubbing is instant at any project size. WebGL compositor for layers, effects, masks, keyframed transforms, and text.
- **One compositor, two homes.** The same TypeScript compositor that draws the preview runs headless on render workers to produce the export. Preview and export are pixel-identical by construction. ffmpeg handles ingest, transcode, proxies, audio, and muxing, never the picture.
- **Media pipeline:** upload or asset-library pull → probe → proxy and thumbnail strip and waveform → original to object storage. Frame-accurate seeking via a keyframe index built on ingest.
- **Project format:** our own JSON document with a CapCut draft importer. The CapCut kit already reverse-engineered the draft schema, so existing CapCut projects and templates open in the product. Draft export back to CapCut is a later nice-to-have.
- **Render:** headless compositor on GPU workers, ffmpeg mux, presets per platform, background queue with progress, review link on completion.

### 8.3 Feature map at CapCut parity

Organized by CapCut's own panels. Tier 1 is what our ads need every week and ships first. Tier 2 is CapCut's core. Tier 3 is the long tail that makes it a 1:1 copy.

| Panel | Tier 1 | Tier 2 | Tier 3 |
|---|---|---|---|
| **Media** | Import, asset library, proxies, folders, search, favorites | Stock library, record screen or webcam, AI-generated media from the product's own jobs | Cloud drives, batch import, media tags |
| **Timeline** | Unlimited tracks, magnetic snapping, trim, split, ripple, roll, slip, slide, delete-and-close-gap, speed, reverse, freeze frame, link and unlink audio, group, lock and mute tracks, markers | Speed curves, compound clips, nested sequences, track heights, clip colors, replace clip, detach audio, multi-select ops | Multicam, time remap by graph, auto-reframe of whole sequence |
| **Player** | Frame-accurate scrub, JKL, loop, safe zones, quality toggle, aspect switch | Full screen, dual view for compare, overlay grid, snapshot | Proxy quality selection, external monitor |
| **Inspector** | Position, scale, rotation, opacity, blend mode, crop, keyframes with easing on every property | Mask shapes with feather and invert, motion tracking, stabilization, chroma key with despill and edge, background removal | Lens correction, 3D rotation, retouch |
| **Audio** | Waveforms, gain, fade, ducking, VO recording, music library, beat markers | Noise reduction, voice isolation, EQ presets, voice changer, auto-ducking by VO | Auto-beat sync, audio-to-text alignment for any clip |
| **Text** | Text layers with fonts, styles, shadows, outlines, backgrounds, animations in and out, presets | Text templates, bubble and callout styles, text-to-speech, text on path | Rich text, kinetic typography templates |
| **Captions** | Auto captions from VO alignment, word-level styles, karaoke highlight, per-brand presets, scrim-aware placement, ASR audit cards | Bilingual captions, caption templates, emoji and keyword emphasis | Caption translation, speaker labels |
| **Stickers and effects** | Image and video overlays, shapes, arrows, blur and pixelate regions | Sticker library, body and face effects, glitch and retro effect packs, particle effects | Full effect library parity, effect keyframing |
| **Transitions** | Cut, dissolve, dip to color, push, slide, zoom | Full CapCut transition set | Custom transition import |
| **Filters and adjust** | Exposure, contrast, saturation, temperature, tint, sharpen, LUT import | Filter library, curves, HSL, vignette, grain | Scopes, match color |
| **Templates** | Brand templates saved from any project, hook-swap families | Community templates, template editing with locked slots | Template marketplace |
| **AI tools** | Everything in section 8.4, plus auto-cut silence, auto-reframe, remove background | Auto-highlights, script-to-video, relight, upscale | Style transfer, lip sync, dubbing |
| **Export** | 9:16, 4:5, 1:1, 16:9, bitrate and codec presets, frame rate, GIF and image sequence, review link | Export ranges, batch export of variant families, direct publish to Meta and TikTok | Cloud render queue prioritization, watermark rules |

### 8.4 The agent's editing workflows

Our editing SOPs ship as executable playbooks the agent runs against the timeline, each followed by a QA pass:

| Workflow | What it does | Laws it carries |
|---|---|---|
| `assemble_from_board` | Approved board → timeline, one clip per beat, VO placed on the beat's timecode | Storyboard first. Product on screen the entire ad. B-roll in-point shows the action, never the aftermath. |
| `sync_vo` | One continuous VO take aligned word-level from the alignment JSON; segments trimmed to the words | VO is one seamless cut. Fixed 6-second segments where the format demands it. |
| `captions` | Word-synced burned captions from the VO alignment, brand style preset, scrim-aware placement | ASR audit: every caption line checked against the script before burn, mismatches surfaced as audit cards. |
| `greenscreen_pip` | Chroma key, despill, PiP framing that cuts the creator at the frame edge, wardrobe check | Edge-cut framing. Despill neutral garment. Dark wardrobe kills the key. |
| `beat_labels` | Title cards and per-beat labels from the storyboard, listicle numbering | Label per beat. Question is the title card for interview formats. |
| `broll_fill` | Fill a gap from the asset library or a sourcing request, never a pan-and-zoom on a still | No Ken Burns fill. B-roll must advance the story. Real footage for action. |
| `hook_family` | Duplicate the timeline, swap the hook segment, render the variant set | Four assets per concept family. |
| `reframe` | 9:16, 4:5, 1:1 with subject tracking and caption re-placement | |
| `two_pass_review` | Pass one: structural defects (missing product, wrong colorway, frame defects), each a FAIL. Pass two: pacing, caption timing, audio levels. Produces a review card the human approves before render. | Self-audit before presenting. A structural defect is a fail, not a note. |

Beyond the named workflows, the agent has a tool for every panel action in the feature map, so it can do anything the human can, including the long tail. It works from the same brand editing style record the human's corrections write to, so style absorbs corrections and the next cut starts from them.

### 8.5 What "1:1" means and does not mean

We copy CapCut's feature set, panel structure, and workflow so a CapCut editor is productive in minutes. We do not copy CapCut's code, assets, effect packs, fonts, sticker libraries, name, or visual design. Feature sets are not protectable; assets and trade dress are. Effects, transitions, stickers, and music are ours or licensed.

## 9. Packaging the IP

**Playbooks.** Every generic skill becomes a versioned playbook record: name, version, stage, body, references. Served by `get_playbook` in chunks, with a section index, so a 193 KB doctrine file can be loaded by section. Playbooks carry a license and a workspace-level entitlement tier.

**Product truth as data.** The 20 brand skills become the `product_truth` record: identity block, mechanism block, banned terms, colorways, dimensions, verified claims, reference images, the one approved master seed. `load_product` returns it in the verbatim block format prompts expect. This is the onboarding wizard's main output.

**Laws as data.** The law gate reads global rules plus per-brand `house_law` rows. The current 13 regexes become seed data, 5 global and 8 as examples for the brand-law editor. Judgment laws stay markdown and stay with the model.

**Leak lint.** The Manus export audit (absolute paths, vault paths, `python3 x.py`, MCP names, `.env`) becomes the CI check for every playbook.

**Excluded.** Finance, Shopify financials, restock, applicant screener, n8n skills, HyperFrames, the third-party PDFs in `_engine/copywriting/copywriting docs/`, and all brand-specific skills.

**Skills pack.** A Claude Code plugin that installs the router skill, the pipeline guide, and MCP registration. Playbook bodies come from the server, so the plugin is thin and updates without reinstall.

## 10. BYO keys and metering

- Per-workspace credential vault, one row per provider, verified on save by a balance or list call.
- Workers fetch keys at job start, never log them, never return them.
- Cost ledger per job from actual provider responses (kie `creditsConsumed`, ElevenLabs characters, HeyGen credits, Gemini tokens), dollarized by a provider rate table we maintain.
- Preflight shows estimated cost and current balance before any spend. Low balance is a hard stop, as it is today.
- Platform fee is a subscription plus render minutes; provider spend passes through at cost because it is their key.

## 11. Phases

Two tracks run in parallel from week 9: the platform track and the editor track. Assumes Brooks plus Claude Code full time, one full-stack engineer on the platform track, and two engineers on the editor track (one media-engine, one frontend) from week 9. Weeks are calendar.

### Platform track

| Phase | Weeks | Deliverable | Exit criterion |
|---|---|---|---|
| 0. Extract and de-localize | 1–2 | Law gate to data. Product truth schema. Artifact contract as SQL. Playbook registry with section index. Leak lint in CI. Pinned dependencies. Copyrighted material out. Hard-coded keys out. | Both MCP servers boot in a container with no home directory and no vault. |
| 1. Multi-tenant core | 3–8 | Supabase schema with RLS, auth, workspaces, roles. Credential vault. Object storage. Queue and Python workers with ffmpeg and yt-dlp. Remote MCP behind OAuth exposing context, research, artifact, and generation tools. Reference ingest and watch as jobs. | A second workspace runs reference → script → keyframes end to end from Claude Code with its own keys and cannot see ours. |
| 2. Storyboard and approval gate | 9–14 | Board on Postgres with lanes, cards, per-card approval, versions, comments, realtime. Layout engine ported. Keyframes land on cards. `animate_scenes` verifies board state server-side. | Animation is impossible without a board approved by a member. Two people can edit one board without lost updates. |
| 4. Onboarding, loop, billing | 15–22 | Brand intake wizard producing brief and product truth. Skills pack plugin. In-app agent mode. Meta and Triple Whale connectors, ad records, verdicts to angles. Stripe metering. Cost and job dashboards. | A new customer goes from signup to first keyframes on a board in one session without us. |

### Editor track

| Phase | Weeks | Deliverable | Exit criterion |
|---|---|---|---|
| E1. Engine | 9–16 | Timeline document and event model. CRDT sync. Media pipeline with proxies, thumbnails, waveforms, keyframe index. WebCodecs playback. WebGL compositor with layers, transforms, keyframes, text. Headless compositor on render workers with ffmpeg mux. | A 30-second multi-track sequence with text and keyframes plays in the browser and exports pixel-identical from a worker. |
| E2. Tier 1 parity | 17–28 | Every Tier 1 cell in the feature map. Captions engine with word-level styles and ASR audit. Chroma key with despill and edge. Markers, comments, version compare, send-back-to-agent. `apply_edit` covering every Tier 1 action. The nine editing workflows and `qa_pass`. Style record with correction write-back. CapCut draft import. | The agent assembles a 30-second UGC ad from an approved board, passes two-pass review, and renders it with VO sync, captions, and a greenscreen PiP. The human intervenes mid-edit and the agent continues from the corrected state. A CapCut draft opens and plays. |
| E3. Tier 2 parity | 29–44 | Every Tier 2 cell: masks, tracking, stabilization, background removal, speed curves, compound clips, audio cleanup, text templates, filter and transition libraries, batch export, direct publish. | A CapCut editor completes a typical ad edit in the product without missing a tool they reach for. |
| E4. Tier 3 parity | 45+ | Long tail: multicam, time remap graphs, full effect library, translation, dubbing, marketplace. Ongoing after GA. | Feature-for-feature audit against current CapCut passes. |

### Beta and GA

| Phase | Weeks | Deliverable | Exit criterion |
|---|---|---|---|
| 5. Beta | 29–36 | Five outside operators on platform plus Tier 1 editor. Weekly fixes, playbook tiering, pricing test. | Retention after the first month and at least one customer running the Sunday loop unassisted. |
| 6. GA | 45 | Tier 2 editor, billing live, docs. | Public signup. |

Migrate our own five brands in Phase 1 as tenant zero. We dogfood every phase on real weekly output. The local vault and CapCut lane stay the fallback until E2 ships.

## 12. Risks

- **Playbook exposure.** Serving doctrine to the customer's Claude means it can be copied. Mitigate with chunked serving, entitlement tiers, a license in every playbook, and accepting that the compounding brand memory and the pipeline are the moat, not the text.
- **Editor scale.** A CapCut-parity editor is the largest single piece of software here, larger than the rest of the product combined. The tier map is the contract for sequencing. Tier 1 ships before anything in Tier 2 starts, and beta runs on Tier 1.
- **Preview and export drift.** Two renderers means two sets of bugs. One compositor running in both browser and worker is the architectural bet that prevents it. Do not let ffmpeg draw pixels.
- **Browser media support.** WebCodecs is in Chromium and Safari; Firefox lags. Beta targets Chromium, and the render path never depends on the browser.
- **Copying CapCut.** Feature parity and panel layout are fair game. Code, assets, effect packs, fonts, stickers, music, name, and visual design are not. Every library asset is ours or licensed.
- **Provider fragility.** kie needs `curl -F` for uploads, HeyGen needs curl for SSL, auto top-up is broken. Adapter tests per provider run nightly against real accounts.
- **BYO key terms.** Confirm each provider allows third-party orchestration on customer keys before beta.
- **Copyright.** The PDFs and scraped competitor ad libraries stay internal. Playbooks that quote them get rewritten.
- **Two implementations today.** The MCP path and the batch pipelines share laws but not code. Phase 1 picks the MCP path and retires the scripts.
- **Concurrency.** Whole-board JSON and SQLite do not survive two users. Phase 2 fixes boards; Phase 1 fixes jobs.

## 13. Decisions needed from Brooks

1. Product name.
2. BYO keys only in v1, or managed keys with markup from the start.
3. Playbook exposure: serve full doctrine to customer Claudes, or serve summaries and keep the full text for in-app agent mode only.
4. Editor tiers: confirm the Tier 1, 2, 3 split in section 8.3 and that beta ships on Tier 1.
5. Compositor strategy: one TypeScript compositor for both preview and render (recommended), or ffmpeg-only render with a browser preview that approximates it.
6. CapCut draft import in Tier 1 (recommended, the kit already knows the schema) or later.
7. Build the remote MCP in Python (reuse 2,363 lines today) or rewrite in TypeScript alongside the app.
8. Whether Specialist's codebase is the starting repo or a reference.
9. Pricing shape: subscription plus render minutes, or seat-based.

## 14. What we leave out on purpose

Finance agent, margin dashboard, Shopify financials, restock watch, applicant screening, n8n workflows, Launchpad, HyperFrames, CapCut bridge, Google Sheets tracker, brand-specific skills, third-party reference PDFs, and the 29 GB archive.
