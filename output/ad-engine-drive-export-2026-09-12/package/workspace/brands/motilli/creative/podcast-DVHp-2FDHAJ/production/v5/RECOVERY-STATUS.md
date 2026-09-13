CURRENT: Production is complete. See DELIVERY.md and delivery-manifest.json. The prior run conflict is resolved; no further generation is pending.

# Motilli podcast recovery status

Recovered session: 01a088d8-a409-7e11-9b1f-c872576eb836. This source session was discovered still executing, with file writes continuing after the new recovery session started. User has been asked to stop that old run before this session resumes shared editor/board changes. No more paid generation submitted after the conflict was discovered.

Completed here:
- Exact v7 script split into 18 turns; no wording changes.
- Woman Over 30 host audio and separately cloned Parker guest audio. Clone permission is preserved in authorization.json. New clone ID addQhAUgyvMLhmX89T8F.
- Raw and 1.1x prepared voice masters with exact character timing. Final mapped spoken sequence including .7s end hold is 197.4 seconds. Sixty-one spoken coverage cards; the empty 0.08s S13-3 presenter flash is merged into the neighboring cut, without removing words.
- Both approved presenter images registered; both look records explicitly support avatar_v.
- Host Avatar V render ae89a13217be5e2d751db57ac5d6f1b9 completed; downloaded host-avatar-master.mp4 and inspected sampled frames.
- Guest Avatar V render de7f0144a61fa6bd716d9f9ef3fba74b submitted; collect.py monitors existing job and downloads when ready. Never resubmit to recover it.
- One Omni stomach-open take completed, 720x1280, 24fps, 10.005 seconds. Original preserved; first four seconds are suitable as a short anatomical insert. It begins already open, so it does not implement a wall-peeling entrance.

Resolve evidence:
- External MCP reports SCRIPTING_UNAVAILABLE.
- In-app Lua fu:GetResolve() returns the live Resolve object. bmd.scriptapp and Resolve() did not.
- Original unnamed project was saved as Recovered Before Motilli Podcast 20260909.
- A create_project.lua command was sent but completion was not verified; no timeline assembly or export is claimed. Re-check actual current project and project list before executing or creating anything. Another agent is also manipulating the app.

Remaining:
- Stop the old conflicting run; consolidate its edit/production-v5 assets with this folder, selecting one voice take per role and avoiding duplicate renders.
- Collect and inspect guest master; full audiovisual lip-sync review still required for both.
- Remove source concept footer in Resolve framing, preserving face/mic. Ingredient images must overlay live guest footage.
- Generate remaining unique Omni inserts and silent listener coverage, replace product proxies using actual approved packaging/gummy references, align captions, assemble in isolated Resolve project, inspect and export.
- Update the current Cut Room board with selected production outputs and final timing; no board changes made from this recovery folder yet.
