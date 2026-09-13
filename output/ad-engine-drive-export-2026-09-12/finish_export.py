from pathlib import Path
import json,csv,hashlib,zipfile,collections,re,shutil,datetime
OUT=Path(__file__).resolve().parent;P=OUT/'package';D=json.loads((OUT/'inventory.json').read_text());M=D['files']; I=P/'00-index';I.mkdir(exist_ok=True)
shutil.copy2(OUT/'session-tool-inventory.json',P/'integrations/session-tool-inventory.json')
for p in ['integrations/session-tool-inventory.json']:
 b=(P/p).read_bytes();M.append({'path':p,'source':'tools exposed in this session on 2026-09-12','resolved_source':'runtime tool catalog','bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'source_sha256':hashlib.sha256(b).hexdigest(),'method':'runtime-inventory'})
md=[m for m in M if Path(m['path']).suffix in {'.md','.mdx','.markdown'}];skills=[m for m in M if Path(m['path']).name=='SKILL.md']
unique=len({m['sha256'] for m in skills})
readme=f'''# Ad Engine — Complete Documentation & Skills

Prepared September 12, 2026 for Brooks Orradre. This is a portable documentation and source snapshot of the ad production system, with original source paths preserved.

## Included

- **{len(M):,} source files**, including **{len(md):,} Markdown documents** and **{len(skills):,} SKILL.md copies** ({unique:,} distinct contents across installed locations and historical copies).
- Marketing brain: research, ideation, copywriting, scripts, SOPs, references, brand/product instructions, editing plans, shared Obsidian memory, work packets, and production records.
- The separate `marketing-apps/adengine` repository: engine services, capabilities, laws, workflows, playbooks, rubrics, schemas and source code.
- Workspace, Codex, Claude and Agents skills, including references and supporting text/code resources. Skill directory symlinks were materialized so their contents travel with the export.
- Cut Room application source, board builder, saved board JSON, project registry, Supabase migration/configuration templates and documentation.
- HeyGen and ElevenLabs adapter source, voice registries, Google Flow production guidance, Seedance 2.5 briefs and playbooks, GPT Image 2 / Omni instructions, DaVinci Resolve MCP source/docs, and installed ChatCut documentation.
- Consistent SQLite snapshots of the selected Ad Studio and ad-engine registries, with snapshot integrity verified.

## How to use this folder

Download BOTH `AD-ENGINE-COMPLETE-PART-1-SYSTEM.zip` and `AD-ENGINE-COMPLETE-PART-2-BRANDS-RESEARCH.zip` for everything included in this export. These are independent standard ZIP files: extract both into the same fresh directory. No special split-archive software is needed. The Drive transfer path enforces a 100 MiB per-file limit, which requires this two-file delivery. The smaller numbered ZIPs contain subsets of the same snapshot and preserve the same paths. This export does not replace your working vault.

Start with `WORKFLOW-MAP.md`, `MCP-AND-PROVIDERS.md`, `SKILL-CATALOG.md`, and `FILE-MANIFEST.csv`. `01-CORE-DOCUMENTS.zip` contains all Markdown and supporting source from the core engine documentation directories; `02-ALL-SKILLS.zip` includes current skills and older packaged skills. The manifest is the authoritative per-file inventory.

Inside the complete archive:

| Path | Contents |
|---|---|
| `workspace/` | Marketing brain vault documents and source |
| `external/adengine/` | Separate adengine repository |
| `installed-skills/` | Codex, Claude and Agents skill trees |
| `integrations/` | Resolve/ChatCut/Drive/browser documentation, sanitized MCP configuration and session tool inventory |
| `00-index/` | This guide, workflow map, catalogs, manifests and scope audit |

## Current authority and historical material

Read `workspace/AGENTS.md` before using an archived skill or playbook. Your current instructions govern: editing plan first; GPT Image 2 for images; Google Omni for video; Cut Room for complete visual storyboards; DaVinci Resolve for editing; product fidelity; scene-specific B-roll reasons and variety; persistent Obsidian memory. Fashion creative leads with aspiration.

Older copies mention ChatCut, CapCut, HyperFrames, Remotion, Nano Banana or other generation routes. They are retained as historical source material, not new authorization. HyperFrames remains banned and was not invoked for this export. No generation or editor action was performed. Seedance/Flow documentation is included as requested; inclusion does not alter your current production routing.

## Scope and restoration limits

This upload covers documentation, source code, structured boards/records and skill text resources. Raw/generated video, audio, raster images, PDFs, other binary media, dependency installations, caches, browser sessions, credentials and unrelated private financial/recruiting datasets are excluded. See `EXCLUSIONS.csv` for exact exclusions. Large rendered HTML exports containing embedded media are excluded alongside raw media; board JSON, Markdown plans and application source remain included. Media URLs and local references inside boards and records remain references; the archive is not a full media-library backup or a hosted Cut Room deployment.

Credential values discovered in included text were replaced with `[REDACTED_SECRET]`; local originals were not edited. Sanitized source/configuration requires your own credentials to run. `SANITIZATION.json` records affected file paths and replacement counts without secret values.

SQLite snapshots use the backup API and are point-in-time snapshots, not an ongoing sync. Existing memory sync-state and record revisions travel as captured; uploading them does not establish a fresh live remote memory mirror. The overall file snapshot is collected sequentially rather than atomically across all applications.

All downloadable source files have SHA-256 entries in `FILE-MANIFEST.csv`. ZIP integrity and staged file checksums were verified before upload. Drive file metadata and byte sizes are checked after upload. This is an export and packaging check, not a production test of every provider or script.
'''
(I/'START-HERE.md').write_text(readme);(OUT/'START-HERE.md').write_text(readme)
workflow='''# Production workflow map

This map is an index to existing source documents, not a rewrite of approved scripts or a new approval gate. Paths below are relative to the complete archive root. Current `workspace/AGENTS.md` resolves conflicts with older documents.

| Stage | Read first | Work/output |
|---|---|---|
| Current context | `workspace/AGENTS.md`; `workspace/_engine/ad-system/README.md`; `workspace/_engine/ad-system/data/memory/INDEX.md`; `installed-skills/codex/ad-system/SKILL.md` | Retrieve existing creative revision, brand note, separate agent notes, approved decisions, sources and selected narration. |
| Research and ideation | `workspace/_engine/frameworks/`; `workspace/_engine/copywriting/`; `workspace/.claude/skills/direct-response-os/`; `workspace/.claude/skills/dr-voc-mining/`; `workspace/.claude/skills/ad-concept-builder/` | Evidence, customer language, awareness, angle/mechanism hypotheses, creative concept and hook tests. |
| Script writing | `installed-skills/codex/ai-ugc-vsl-scripting/`; `workspace/.claude/skills/long-form-copy/`; `workspace/.claude/skills/dr-hook-lab/`; `workspace/hermes-migration/ai-ugc-vsl-swipe-copywriting/` | Spoken script and hook options grounded in the brief, with exact approved narration preserved. |
| Reference and editing analysis | `workspace/_engine/sops/Ad-Editing-Plan-First-SOP.md`; `installed-skills/codex/ad-editing-style/`; `installed-skills/codex/broll-storytelling/` | Actual-media inspection, consecutive-frame cut checks, observed editing language and a saved line-to-visual editing plan with why each cut and scene belongs. |
| B-roll and hook direction | `installed-skills/codex/broll-heygen-vsl/`; `broll-podcast/`; `broll-skeleton-ads/`; `broll-animated-ads/`; `broll-ai-voiceover-vsl/`; `tiktok-broll-sourcing/` under the same root | Match the concept treatment, exact spoken cue, visual action, viewer response and sequence position. Ensure variety; apply EV5/no-text rules where TikTok sourcing is assigned. |
| Product and presenter identity | `workspace/brands/velantra/product-skills/registry.json`; `workspace/brands/velantra/product-skills/SCALE-AND-FIDELITY.md`; dedicated `installed-skills/codex/velantra-*-product/` | Resolve product/color/size, current approved references and identity constraints before generating. |
| Storyboard | `workspace/.claude/skills/cutroom/SKILL.md`; `workspace/cutroom/README.md`; `workspace/cutroom/board_builder.py` | Build cards in the correct brand project with exact narration, scene/edit reasons, actual selected GPT Image 2 images, first frames and separate reference lane. Verify saved board and URL. |
| Voice and presenter | `workspace/_engine/mcp/ad-engine/engines/elevenlabs.py`; `engines/heygen.py` under the same root; `installed-skills/claude/elevenlabs-agent/`; `workspace/voice-registry.json` | Use the selected voice and pronunciation direction; preserve approved speed/word alignment; drive the avatar with the selected narration; retain provider handles and original outputs. |
| Image and video production | `workspace/AGENTS.md`; `installed-skills/agents/higgsfield-generate/`; `external/adengine/services/engine/adengine/gen/server.py`; `workspace/_engine/sops/Seedance-Prompt-System.md` | Follow current GPT Image 2 / Google Omni routing. Historical Seedance/Flow resources explain existing production routes. Inspect actual outputs; report provider format/duration limitations. |
| Editing | `integrations/davinci-resolve-mcp/README.md`; current workspace rules; the creative's `edit/` plan | Verify current Resolve connection, use an isolated project/timeline, align cuts and captions to selected narration, mix audio, preserve existing projects. |
| QA and delivery | `workspace/_engine/ad-system/README.md`; `SCHEMA.md` under the same root; creative editing plan and review files | Inspect actual finished media, product accuracy, exact source reuse and visual similarity; register immutable export hash and exact creative revision. |
| Performance and next iteration | `workspace/_engine/ad-system/data/memory/Performance.md`; Ad Studio README and schema | Bind exact platform ad IDs to exact exports; import actual metrics with measurement definitions; record evidence, alternatives, next tests and memory. |

The archived applications reference services and asset locations on the original Mac or providers. Opening this Drive folder alone does not start those services, reconnect MCPs or republish boards.
'''
(I/'WORKFLOW-MAP.md').write_text(workflow)
providers='''# MCP and provider inventory

This inventory separates installed/documented integration evidence from live connection verification. Only Google Drive was exercised for this upload. No paid generation, provider credit test or editor operation was performed.

| Integration | Evidence included | Snapshot status |
|---|---|---|
| Ad Engine MCP | `workspace/.mcp.json`, `workspace/_engine/mcp/ad-engine/`, `external/adengine/services/engine/` | Local registration and adapter/service source found. |
| DR OS MCP | `workspace/_engine/mcp/dr-os/`, sanitized local registration | Local research/copywriting integration found. |
| HeyGen | `workspace/_engine/mcp/ad-engine/engines/heygen.py`; external engine adapters; relevant UGC and presenter docs | Source supports avatar/audio workflow. No dedicated HeyGen MCP was exposed in this export session; adapter exists locally. |
| ElevenLabs | `workspace/_engine/mcp/ad-engine/engines/elevenlabs.py`; `installed-skills/claude/elevenlabs-agent/`; voice registries | MCP configured and tools exposed in this session. No speech job submitted. |
| Google Flow | `workspace/_engine/sops/Video-Brief-Format-SOP.md` and its template/example copies; inherited playbooks | Existing production-method guidance found. No dedicated Flow MCP registration or callable Flow tool was found in the inspected configurations/session. This does not prove none exists elsewhere. |
| Google Omni | Workspace instructions; production skills and creative plans | Current user-authorized video route. Not called during export. |
| Seedance 2.5 | `external/adengine/services/engine/adengine/gen/server.py`; `workspace/_engine/sops/Animated-Drama-SOP.md`; Seedance prompt/director/brief skills and playbooks | Historical/current local documentation and generation adapter references found. Current workspace model instructions govern execution. |
| GPT Image 2 | Current instructions, image-production skills and engine adapters | Current image route. Not called during export. |
| Higgsfield | `installed-skills/agents/higgsfield-*` and materialized skill copies | Installed generation/product-photography/identity skill resources found. |
| Cut Room / Supabase | `workspace/cutroom/`, `workspace/.claude/skills/cutroom/` | Local application, board JSON, project list, migrations and sync source included. Credentials and media binaries excluded. |
| DaVinci Resolve MCP | `integrations/davinci-resolve-mcp/`; sanitized Codex MCP configuration; session tool inventory | Installed, registered and tools exposed. Resolve itself was not launched or tested. Current editor route. |
| ChatCut | `integrations/chatcut-plugin/` | Installed plugin skill and MCP documentation retained. Historical editing instructions are superseded by Resolve. |
| Browser automation | Installed browser skill, sanitized Playwright registrations | Available setup/documentation retained; no provider browser session exported. |
| Google Drive | `integrations/google-drive-skills/`; relevant runtime tool descriptions | Connected to Brooks Orradre's Drive; folder and uploads verified by metadata readback. |

`mcp-configurations.sanitized.json` records only selected MCP configuration fields. `session-tool-inventory.json` captures exposed tool names/descriptions for ElevenLabs, Resolve and the relevant Drive operations. Tool exposure is not a successful connectivity test.

No new integrations, model support, current prices or provider quotas are inferred from historical documentation. Source dates and original claims remain in the copied files.
'''
(I/'MCP-AND-PROVIDERS.md').write_text(providers)
cat=['# Skill catalog','',f'{len(skills)} SKILL.md files; {unique} distinct file contents. Multiple installed locations and historical export copies are preserved. Current workspace AGENTS.md governs execution.','', '| Skill | Location | Classification |','|---|---|---|']
for m in sorted(skills,key=lambda m:m['path']):
 p=m['path'];name=Path(p).parent.name
 status='Historical export' if any(x in p for x in ['/manus-export','/hermes-migration','/skill-before/']) else 'Source/installed copy'
 if 'hyperframes' in p.lower():status='BANNED / inert archive only'
 cat.append('| '+name.replace('|','\\|')+' | `'+p.replace('|','\\|')+'` | '+status+' |')
(I/'SKILL-CATALOG.md').write_text('\n'.join(cat)+'\n')
with (I/'FILE-MANIFEST.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['path','source','resolved_source','bytes','sha256','source_sha256','method']);w.writeheader();w.writerows(M)
with (I/'EXCLUSIONS.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['path','reason']);w.writeheader();w.writerows(D['excluded'])
(I/'SANITIZATION.json').write_text(json.dumps(D['redactions'],indent=2));(I/'SYMLINKS.json').write_text(json.dumps(D['symlinks'],indent=2))
summary={'source_files':len(M),'markdowns':len(md),'skill_files':len(skills),'distinct_skill_contents':unique,'source_bytes':sum(m['bytes'] for m in M),'sanitized_files':len(D['redactions']),'excluded_entries':len(D['excluded']),'created':datetime.datetime.now(datetime.timezone.utc).isoformat()};(I/'SNAPSHOT.json').write_text(json.dumps(summary,indent=2))
for p in I.iterdir():shutil.copy2(p,OUT/p.name)
for m in M:
 if hashlib.sha256((P/m['path']).read_bytes()).hexdigest()!=m['sha256']:raise RuntimeError('hash mismatch '+m['path'])
files=sorted(p for p in P.rglob('*') if p.is_file())
groups={
'AD-ENGINE-COMPLETE-PART-1-SYSTEM.zip':lambda s:not s.startswith(('workspace/brands/','workspace/_engine/research/','workspace/_engine/creative-research/','workspace/_engine/swipe-library/','workspace/swipe-intake/')),
'AD-ENGINE-COMPLETE-PART-2-BRANDS-RESEARCH.zip':lambda s:s.startswith(('workspace/brands/','workspace/_engine/research/','workspace/_engine/creative-research/','workspace/_engine/swipe-library/','workspace/swipe-intake/')),
'01-CORE-DOCUMENTS.zip':lambda s:s.startswith('00-index/') or any(s.startswith('workspace/_engine/'+x+'/') for x in ['frameworks','copywriting','sops','harness','product','pipelines','standalone-skills']) or s=='workspace/AGENTS.md',
'02-ALL-SKILLS.zip':lambda s:s.startswith('installed-skills/') or '/skills/' in s or s.startswith('workspace/manus-export') or s.startswith('workspace/hermes-migration'),
'03-MCPS-AND-ADENGINE-SOURCE.zip':lambda s:s.startswith(('integrations/','external/adengine/','workspace/_engine/mcp/','workspace/_engine/tools/')) or s=='workspace/.mcp.json',
'04-CUT-ROOM-SOURCE-AND-BOARDS.zip':lambda s:s.startswith('workspace/cutroom/'),
'05-AD-STUDIO-AND-OBSIDIAN-MEMORY.zip':lambda s:s.startswith(('workspace/_engine/ad-system/','workspace/_engine/creative-tracker/')),

}
archives=[]
for name,choose in groups.items():
 target=OUT/name
 with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for p in files:
   rel=p.relative_to(P).as_posix()
   if choose(rel):z.write(p,rel)
 with zipfile.ZipFile(target) as z:
  bad=z.testzip()
  if bad:raise RuntimeError('ZIP CRC failed '+bad)
  count=len(z.namelist())
 b=target.read_bytes();archives.append({'name':name,'files':count,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'md5':hashlib.md5(b).hexdigest()})
part_sets=[]
for name in list(groups)[:2]:
 with zipfile.ZipFile(OUT/name) as z:part_sets.append(set(z.namelist()))
expected={p.relative_to(P).as_posix() for p in files}
assert not part_sets[0].intersection(part_sets[1]), 'Overlapping complete parts'
assert part_sets[0]|part_sets[1]==expected, 'Incomplete two-part coverage'
(OUT/'ARCHIVE-CHECKSUMS.json').write_text(json.dumps(archives,indent=2));print(json.dumps({'summary':summary,'archives':archives},indent=2))
