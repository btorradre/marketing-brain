# Motilli VSL V15 — prepared revision

Selected hook: `deliverables/Visual-Hook-3.233s.mp4` — 1080×1920,30fps,97frames,silent. Original Google Omni output remains under assets/video-v15/toilet-hook.mp4. GPT Image 2 selected keyframe and prompts/provenance retained.

Combined native change: hook0–97; clean TikTok fiber-food1425–1491; cooking7256–7346. All ranges use exclusive end frames. Preserve V12 narration, captions and runtime8327frames. Isolated target timeline: v15 FINAL - visual hook; baseline: v12 FINAL - scale overlay. Existing projects/timelines preserved.

Full ad is NOT exported yet. Resolve MCP returned SCRIPTING_UNAVAILABLE; native GUI console returned no accessible text areas and screen capture could not access a display. Resume after desktop/Resolve are accessible:

`python3 resolve_lua.py resume-and-export-v15.lua`

This idempotent native script checks actual existing target clips before applying missing replacements, asserts native counts and starts MP4/DRP/DRT export. Wait for render completion, run `python3 qa_revision.py`, inspect final frame contact, verify native readback and SRTidentity, then update board/plan/status. Do not call an unverified or partial output the finished ad.

Cut Room: https://cutroom-three.vercel.app/b/mot-ugc-yapper-01
