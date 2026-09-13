

## V9 speech captions over scientific B-roll — September 10, 2026

Observed cause: v5 caption builder skipped every Science card; v6 additionally removed S10-1 and S12-1 captions under the earlier no-text direction. The current user correction supersedes that caption exclusion: retain normal speech captions across scientific inserts, with no additional explanatory diagram labels. Screenshot shows an intermediate v8 master; deliver and select the final pause-tightened revision.

Preserve v8 final picture/audio, 4882 frames at 30fps, existing 1.1× pace, 75 silence cuts, headline at top, avatars, exact narration and all selected inserts. Duplicate Motilli v8 No Dead Space Final into an isolated v9 timeline. Add only the missing phrase captions on a video track above all picture layers; use existing Arial Bold 57px white with 4px black outline, centered at y1540, maximum two lines and four seconds per phrase. Existing burned-in captions stay untouched.

Schedule: missing phrases in Science cards and S10-1/S12-1 follow the existing per-word v8 alignment and final card windows. Save exact phrase/frame rows in production/v9/added-caption-cues.json before timeline assembly. Clip additions to uncaptioned windows so no duplicate captions overlap. Direct phrase changes, no text animation. Audio, cuts, camera movement, hook/product/CTA timing and end hold are unchanged; no generation or new narration required.

QA: confirm every affected science card has narration captions and no overlap with existing captions; review rendered samples across all affected cards and consecutive frames at scientific insert boundaries; verify final duration and unchanged dialogue timing, full decode and editable export integrity. Update Cut Room with selected final frames and speech-caption treatment, preserving exact script and separate reference lane.
