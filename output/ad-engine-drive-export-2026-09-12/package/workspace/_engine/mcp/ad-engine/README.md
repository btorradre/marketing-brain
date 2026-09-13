# ad-engine MCP

Internal video-ad generation engine, exposed to Claude Code as MCP tools.
Local-only, stdio transport. Registered in `marketing brain/.mcp.json`.

Replaces the per-skill copy-paste of kie.ai auth, polling loops, progress.json
and cost guessing with one shared layer: a job/asset registry, a truthful cost
ledger, and a mandatory watch-first pipeline order.

## Mandatory editing plan before production

For every ad, create and save a concrete editing plan automatically before generating images, video or voice, assembling a timeline, or exporting. Follow [Ad-Editing-Plan-First-SOP.md](../../sops/Ad-Editing-Plan-First-SOP.md). Verify reference cut boundaries/transition spans against actual frames; map every proposed line to B-roll/action, source or gap, timing, transitions, captions, audio and purpose. Save under the concept's `edit/` folder, surface it proactively and update on revisions/new voice alignment. This is a calling-agent workflow requirement, not a claim that the legacy runner validates creative completeness. No extra approval gate is introduced. Current workspace/user instructions govern providers and editor selection over historical defaults below.

## Pipeline order (this is the point)

```
resolve_reference_tool     any input -> local video, registered as an asset
        |                  (GetHookd URL/ID, TikTok/IG/YouTube URL, local path)
        v
watch_reference_tool       MANDATORY. ffmpeg scene-change detection finds every
        |                  real cut; transcript; Gemini per-beat pass ->
        |                  shot_type, composition, subject, action, motion,
        |                  on_screen_text, audio_cues, ad_role
        v
strategize-ad-adaptation   SKILL, not a tool. Opus reasoning pass over the
        |                  manifest. Decides PER BEAT what it is, what honestly
        |                  replicating it requires, and which beats must share
        |                  an asset. Outputs a plan with continuity_groups.
        v
editing_plan              MANDATORY saved line-by-line edit + reference analysis
        |                  before any image/video/voice production
        v
plan_preflight             what would be generated, what defers to sourcing,
        |                  estimated credits, is the balance sufficient
        v
plan_generate_anchors      ONE still per continuity group (the shared avatar /
        |                  location), so identity holds across its beats
        v
plan_generate_keyframes    one still per scene, anchor prepended for group
        |                  members. QA every still here — stills are cheap.
        v
plan_animate_scenes        each approved still animated INDEPENDENTLY
        |
        v
ChatCut                    final assembly (separate, already-working MCP)
```

Voiceover runs alongside: `eleven_generate_vo` produces one continuous take,
`heygen_upload_audio` + `heygen_generate` lip-sync an avatar to that exact file.

**Never generate against a reference that has not been through
`watch_reference_tool`.** Every downstream decision is grounded in that
manifest; skipping it means the strategist is guessing at the reference.

## Laws encoded in the code (not in prompts)

- **No chaining.** No clip is ever seeded from another clip's last frame.
  Chaining compounds errors across segments. Independent stills conditioned on
  shared references cannot. The trade is that continuity must be restated per
  prompt, which is what continuity groups exist for.
- **Real footage stays real.** Scenes the plan marks `real_footage_required`
  are never sent to a generator; they come back as sourcing tasks.
- **One take VO.** `engines/elevenlabs.py` has no per-line render path. Over
  v3's 5,000-char cap it splits at a paragraph boundary into large takes.
- **v3 Creative, not multilingual_v2.** The latter was blind-judged 2.5/10 as
  robotic; v3 Creative scored 9.5/10. Defaults live in `CREATIVE`.
- **Stills before video credit.** Keyframes are auditable before animation spend.

## Provider gotchas handled once, here

| Provider | Gotcha | Where |
|---|---|---|
| kie.ai | Auto top-up is **broken** — low balance is a hard stop, not a warning | `kie.balance()`, `plan_preflight` |
| kie.ai | `seedance-2` pre-auths ~3x actual charge | `cost_ledger.KNOWN_RATES_PER_SECOND` |
| kie.ai | Upload must use `curl -F`; hand-rolled urllib multipart gets a 403 from the WAF | `kie.upload()` |
| kie.ai | recordInfo echoes prompts with raw control chars | `json.loads(..., strict=False)` |
| kie.ai | macOS python.org builds lack system CAs | `SSL_CTX` via certifi |
| HeyGen | `api` credits ≠ `generative_credit`; **only `api` renders** | `heygen.check_quota()` |
| HeyGen | Credit failure surfaces at **poll** time, not submit | `heygen.status()` sets `should_refire` |
| HeyGen | Auto top-up fires on a rejected render, never a quota read → re-fire | `refire_note` |
| HeyGen | Python SSL cannot verify their hosts | every call via `curl` |
| ElevenLabs | v3 caps text at 5,000 chars | `_split_at_paragraph` |
| ElevenLabs | "Velantra" reads as "Volantra" | `PRONUNCIATION_FIXES` (TTS input only) |
| ElevenLabs | v3 has no speed control | pace with ffmpeg `atempo` after generation |

## Layout

```
server.py                 MCP entrypoint, 24 tools
db.py                     SQLite registry: jobs, assets, costs
cost_ledger.py            credit -> USD, per-model rate table, preflight estimates
engines/kie.py            Seedance / Kling / GPT Image 2 / Nano Banana
engines/elevenlabs.py     v3 Creative VO, shared voice registry
engines/heygen.py         v3 Avatar V driven by our own audio
workflows/resolve_reference.py
workflows/watch_reference.py
workflows/plan_runner.py  preflight / anchors / keyframes / animate
data/                     registry.sqlite3 + downloads + watch manifests + vo
```

Reuses rather than forks: `_engine/tools/tools/gethookd_resolver.py`,
`~/.claude/skills/ad-watcher/pipeline.py`, and the elevenlabs-agent voice
registry at `marketing brain/voice-registry.json`.

## Verified live (2026-08-16)

resolve → watch (7 beats, correct ad_role classification) → registry;
kie upload → GPT Image 2 i2i → poll → download → asset + cost row
(6.0 credits logged, balance delta matched exactly); ElevenLabs v3 one-take VO
(19.76s + character alignment); HeyGen quota read (api 754 vs
generative_credit 33 — the split-pool case, live).

## Not built yet

- ffmpeg helper tools (concat / caption burn) — assembly is ChatCut's job by design
- `qa_pass` as a tool (frame QA currently runs as a subagent pass per product skill)
- Google Drive delivery + `push_concept.py` trigger
- VPS hosting for the background agent team
