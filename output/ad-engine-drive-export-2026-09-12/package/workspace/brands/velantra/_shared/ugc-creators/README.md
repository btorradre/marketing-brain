# UGC Creators — Velantra

The pickable avatar roster for the `velantra-ugc` skill (multi-shot UGC ads via kie.ai Seedance 2.0, any Velantra bag). The `<name>-ref.png` IS the avatar — it rides as @Image1 on every generated segment; no platform registration needed.

## AI roster (generated 2026-07-07 — interchangeable across all products, no bag in refs)
| Avatar | Age | Look |
|---|---|---|
| Blair | 42 | golden blonde waves, linen shirt jacket, hallway |
| Sloane | 38 | dark brunette, tan, black tank + ivory cardigan, kitchen |
| Marin | 52 | brown w/ gray streaks, breton stripe, living room |
| Tessa | 35 | strawberry blonde curls, freckles, sage henley, bedroom |
| Camille | 47 | dark bob, pearl studs, ivory crewneck, entryway |

Each folder: `<name>-ref.png` (canonical identity ref, Seedance @Image1) + `profile.md` (verbatim Seedance creator block, voice character). Legacy Higgsfield/MS IDs in profile.md are dead — ignore them.

## Real creators
- **Caroline Nutt** — real UGC footage + `caroline-ref-still.jpg`. Usable as a Seedance @Image1.

## Adding an avatar
1. Generate a photoreal chest-up ref with any t2i engine on kie.ai: 9:16, candid iPhone realism, natural window light, visible skin texture, no bag in hand, no logos, coastal-affluent wardrobe per the Velantra ICP.
2. Save to `<Name>/<name>-ref.png`, write `profile.md` (copy an existing one — the verbatim creator block + voice character are the parts that matter).
3. Add to `.claude/skills/velantra-ugc/avatars.json`.
