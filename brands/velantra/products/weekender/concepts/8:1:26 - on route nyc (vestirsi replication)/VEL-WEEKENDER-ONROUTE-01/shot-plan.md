# VEL-WEEKENDER-ONROUTE-01 — "On route: NYC" (Vestirsi replication)

**Swipe:** https://app.trendtrack.io/share/ads/vestirsi-QsaRUK (13.2s, 9:16, music only, on-screen text "On route: / for NYC")
**Pipeline:** GPT Image 2 i2i (kie.ai) keyframes → Google Omni i2v → trim/stitch + Pillow text overlays
**Colorway:** light chocolate (cream ivory woven canvas)

## Why the swipe works
Faceless "airport quiet luxury" identity the viewer projects herself into. The bag is staged as the working centerpiece of a travel system (slides onto the suitcase, swallows a laptop), with ASMR-packing satisfaction and a single open-loop text line. No VO, no claims, pure aspiration.

## Redirects (their mechanism is not ours)
| Vestirsi beat | Our redirect | Why |
|---|---|---|
| Slides bag onto trolley handle (trolley sleeve) | Bag RESTS flat on top of the suitcase, no sleeve, no strap | Weekender has no trolley sleeve; never invent hardware |
| Shoulder carry side profile | Hand carry / hand resting on handles | Short rolled handles = hand or forearm only |
| Gold zipper macro | Gold turn lock + clasp plate macro, hand resting, nothing manipulated | Bag has NO zipper; closure-interaction law = no on-camera opening |
| Black leather bag | Light chocolate two-tone per identity block | Our product truth |

## Shot list (5 scenes, each Omni clip trimmed to ~2.6s, total ~13s)
1. **S1 Departure stance** (closed, hand carry) — faceless model, cream trench, silver aluminum carry-on, bag held at her side. Text overlay lives here + S2.
2. **S2 Packing: laptop** (open, mechanism block) — laptop slides into the open mouth on a bedroom bench.
3. **S3 Packing: knit** (open, mechanism block) — folded cream cable knit lowered in next to charcoal jeans.
4. **S4 Hardware macro** (closed) — turn lock + clasp plates + key bell, hand resting on handle.
5. **S5 Travel-system hero** (closed) — bag resting on top of the suitcase by the front door, hand steadying handles.

## Text overlays (post only, Pillow PNG + ffmpeg)
- S1+S2: "On route:" (left) / "for NYC" (right), small white sans, matching swipe placement.
- No native text in any generated frame (photoreal footer bans it).

## QA gates
- 3 variants per scene, pick before animating (photoreal first, product truth second, composition third).
- Mandatory frame-QA subagent pass on every pick BEFORE Omni (pre-animation gate).
- Video QA: 3+ frames per clip against open/closed calibrations; open-bag FAIL list incl. missing front handle, zipper, flap-shaped front panel, plain featureless flap inner face.
