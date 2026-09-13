# dr-os MCP — the Direct Response OS as a tool surface

Turns the whole reference-to-editor-brief pipeline into an MCP server any
agent can drive — a local Claude Code session, or an external agent (e.g.
Sam) connected over stdio or HTTP.

**Division of labor:** the machinery lives in the server (reference download,
ffmpeg/Gemini frame-by-frame watch, the artifact contract on disk, the
deterministic law-gate, Cutroom board layout, creative-tracker push). The
judgment lives in the playbooks the server serves — the CALLING model reads
them and does the thinking (golden nugget, angles, adaptation calls,
scripts). Nothing is duplicated: playbooks are read live from the skill
files, the watch head is imported from ad-engine, boards go through
`cutroom/board_builder.py`.

## Connect

Local Claude Code: already registered in the repo's `.mcp.json` (stdio).

External agent host (stdio):

```
command: /Users/brooksorradre2/Documents/marketing brain/_engine/mcp/ad-engine/.venv/bin/python
args:    ["/Users/brooksorradre2/Documents/marketing brain/_engine/mcp/dr-os/server.py"]
```

External agent host (streamable HTTP):

```bash
"_engine/mcp/ad-engine/.venv/bin/python" "_engine/mcp/dr-os/server.py" --http 8770
# endpoint: http://127.0.0.1:8770/mcp
```

Binds localhost only. To reach it from another machine, tunnel it (SSH/
tailscale) — do not bind it publicly, it has filesystem write access.

## The 14 tools

| Tool | What it does |
|---|---|
| `dr_pipeline_guide` | Canonical order of operations. **First call, always.** |
| `dr_load_brand` | Brand brief + house/global laws + angle bank + product-truth skill list. |
| `dr_list_playbooks` / `dr_get_playbook` | Serve the SOPs (router, laws, strategize, hook-lab, ugc-brief, cutroom, …) and any product-truth skill (`velantra-weekender`, `motilli`, …). |
| `dr_ingest_reference` | Any URL/path → local video → frame-by-frame watch manifest (via ad-engine). Minutes, not seconds. |
| `dr_lawgate` | Deterministic house-law check (AI-tells, Strato, BNPL, 90-day, Monacolin, creator-as-brand, …). |
| `dr_list/read/save_artifact` | The dr-os artifact contract under `brands/<brand>/research/dr-os/` — frontmatter enforced, law-gate blockers stop saves. |
| `dr_push_brief_board` / `dr_list_boards` / `dr_export_board` | Storyboard spec → Cutroom board URL for the editor (auto-starts the server); export → self-contained HTML. |
| `dr_push_concept` | Registers the agreed concept in the creative tracker; returned asset_id goes into the angle record's `tested_assets`. |
| `dr_status` | Brands, Cutroom health, ad-engine import, kie balance. |

## The canonical run (what Sam should do with a reference)

1. `dr_pipeline_guide` → `dr_load_brand(brand)` → `dr_get_playbook(<product-truth skill>)`
2. `dr_ingest_reference(url, brand, concept)` → manifest = ground truth
3. `dr_get_playbook("strategize")` → reason the manifest into an adaptation
   plan → `dr_save_artifact(brand, "adaptation-plan", …)`
4. `dr_read_artifact(brand, "angle-bank")` → map the concept to an angle
   (angle = the PROBLEM; a claim is a hook)
5. `dr_get_playbook("hook-lab")` / `("ugc-brief")` → script + brief, every
   creator line through `dr_lawgate(…, speaker="creator")` →
   `dr_save_artifact(brand, "brief", …)`
6. `dr_get_playbook("cutroom")` → build the two-lane storyboard spec
   (REFERENCE CREATIVE vs OUR VERSION, per-beat timecode/SCRIPT/frame/
   EMOTION) → `dr_push_brief_board(spec, project=brand)` → hand the URL to
   the editor
7. `dr_push_concept(…)` → write the asset_id back into the angle record

Generation (Seedance/Kling/HeyGen/ElevenLabs) is deliberately NOT here — that
is the sibling `ad-engine` MCP. This server ends at the brief, the board, and
the tracker entry.

## Notes

- Reuses ad-engine's venv (`_engine/mcp/ad-engine/.venv`) — no second venv.
- `cutroom/` was `briefboard/` until 2026-08-17; `paths.py` resolves either.
- The law-gate is a heuristic pre-filter. The judgment laws (golden nugget,
  swap test, six-month shelf life, demonstrate-never-describe) can only be
  enforced by the model reading `dr_get_playbook("laws")`.
