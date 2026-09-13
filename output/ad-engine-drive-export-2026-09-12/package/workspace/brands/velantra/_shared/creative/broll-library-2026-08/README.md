# Colette + Margot B-roll Library — 2026-08

200 clips (10s, 720x1280, 9:16, h264 + native ambient audio) + 200 matching keyframe stills. Every clip passed a three-frame drift audit; every still passed photoreal + product-truth QA against the locked references.

## Where the deliverables live
- `brands/velantra/products/margot/broll/library-2026-08/` — 110 clips + 110 stills (90 Margot solo + 20 duo)
- `brands/velantra/products/cashmere-tote/broll/library-2026-08/` — 110 clips + 110 stills (90 Colette solo + the same 20 duo)

## Naming
`VEL-COL-###-<shot>`, `VEL-MAR-###-<shot>`, `VEL-DUO-###-<shot>`. Categories by number range:
- Colette: 001-018 street/carry · 019-030 cafe · 031-038 car · 039-050 home · 051-058 open-bag · 059-070 packing · 071-074 what-fits flat lays · 075-086 macros · 087-090 set-downs
- Margot: 001-016 commute · 017-028 office · 029-036 cafe · 037-044 car · 045-052 home · 053-060 open-bag · 061-072 packing · 073-076 flat lays · 077-086 macros · 087-090 set-downs
- Duo: 20 both-bag scenes (entry bench, bed packing, closet, trunk, cafe, flat lays, handoffs)

## Colorways used
Colette: Caramel (majority) + Espresso. Margot: Burgundy, Midnight Black, Brown. One colorway per frame (colorway-drift law). MAR-032 reads closer to Coffee Brown than Burgundy; acceptable, both are live variants.

## Notes for the edit
- Omni adds native ambient audio; mute it, the VO is the only voice track (SOP).
- Cut from the early-to-mid stretch of each clip when possible.
- 11 clips are slow push-ins rendered from the approved still (macro shots + engraving-prone scenes where i2v mutates hardware): COL-050, 083, 085, 086; MAR-008, 011, 031, 038, 077, 080, 088. They cut like locked-off tripod shots.
- Rejected variants stay in `keyframes/<id>/` beside the pick for auditability.

## Process (for reruns)
`scenes.py` (200 scenes) → `pipeline.py run` (kie GPT Image 2 i2i, 3 variants/scene, photoreal blocks per Velantra-Avatar-BRoll-Production-SOP §3/§3b) → strip QA + picks → `animate_omni.py run` (Omni 10s) → clip drift QA → `kenburns.py` fallback → `distribute.py`. Pinterest shot-language study in `shot-language.md`.
