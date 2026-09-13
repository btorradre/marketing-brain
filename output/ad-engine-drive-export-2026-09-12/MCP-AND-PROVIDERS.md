# MCP and provider inventory

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
