# Delphine b-roll library rebuild — 2026-08-20 (round 4)

## 📦 PACKING EXPANSION (same day, Brooks: "too many scenes of the women walking… i want scenes of the bag being packed. go look at the colette library")
10 new scenes (059-068) built to the Colette packing-bank format (12-scene bank at
`_shared/creative/broll-library-2026-08/scenes.py` section F: hands mid-action, item halfway
into the mouth, waiting pile beside the bag, varied rooms) with the v4 real-seed recipe.
Delphine-legal items only (wallet/cards/keys/lip colour/slim pouch — capacity law); open bag =
LC/DC only. Seeds: carry-on bed-packing swipe (05-ig-DQoIBOhjya8, frames t8.5-17.5, new
extraction at `seeds/tiktok/../pack-mine`→ scratchpad), kitchen-counter TikTok (existing
home_7649 frames), bench swipe (ob-hands-open-bench). Renders in `renders/packing/`; rejects in
`renders/packing/_rejected/`.
QA: 065 re-rolled (turn-lock artifact — TURN-LOCK BLOCK now pasted verbatim in every prompt at
medium distance, not just macros) · 066 re-rolled (DAMIER-PATTERNED POUCH — second competitor
trade-dress catch on a prop; "completely plain, no checkerboard, no embossing" now mandatory
for any pouch/wallet prop) · 067 re-rolled (phantom ring hanging from lock + second interior
zip). 066 still carries a strap-knot oddity inherited from the seed after 2 rolls — FLAGGED on
board. Board: http://localhost:8765/b/delphine-broll-packing-expansion — AWAITING BROOKS.
**v2 (same day): Brooks approved the visual style but caught the OPEN-STATE MECHANISM wrong on
every open frame ("triple flap mechanism"). All 8 open frames re-generated with
IMG_4190-open-front.jpg (real bag, open) as a dedicated MECHANISM REFERENCE + the observed
open-state block (now PRODUCT-TRUTH §4). All 8 corrected first try; 064's mid-air keys refused
to render twice → moment renamed to a bench reach. Closed frames 063/068 untouched. Packing
spend total: 22 renders ≈ 139cr, Higgsfield ~686 left.**
On approval: install as VEL-DEL-059..068 in stills/, extend animate_v4.py MOTIONS (061
OVERHEAD, 063 HOLD, rest HANDS), run animate. Spend: 13 imgs ≈ 82cr (Higgsfield ~743 left).

## ✅✅ STATUS: LIBRARY COMPLETE — 49 stills + 49 Omni clips live in stills/ and clips/
Brooks approved via "animate all the scenes with omni" (2026-08-20). v3 archived to
`_superseded-2026-08-20/`. Animation: all 49 landed first pass, 0 failures. Drift QA: one
push-in caught (053 canvas macro, +9.34) and re-fired with a hardened locked-distance motion
(re-landed at +1.45). Omni cost: Gemini API, no Higgsfield/kie credits consumed for animation.

## (superseded) STILLS COMPLETE — 49 picks on the Cutroom board awaiting Brooks
Board: http://localhost:8765/b/delphine-broll-v4-rebuild (slug `delphine-broll-v4-rebuild`)
Picks: `_rebuild-2026-08-20/picks/` (49 files: 23 LC / 14 DC / 12 AG)
ON APPROVAL: archive current stills/+clips/ to `_superseded-2026-08-20/`, move picks into
`stills/` with VEL-DEL-v4-### names, then Omni-animate with the HOLD-family motions from
`scenes_delphine.py` using approved_board_slug=delphine-broll-v4-rebuild.
Total run: 56 images generated (49 kept, 7 superseded by their re-rolls) = 266 Higgsfield
credits exactly (1091.38 → 825.38). kie reserve untouched at 318.3.

Brooks: the 58-shot library still reads as "3D model". This rebuild applies the new house SOP
(feedback_hyperreal_broll_real_ugc_seed): **every scene is seeded from a REAL reference frame**
(Mode A pixel seed), judged by the situational-awareness test (name the moment or don't generate).
Round 3 fixed the scene premises but still generated from written prose — the model defaulted to
editorial/CGI. Round 4 inherits realism from real pixels.

## Diagnosis of round 3 (what "3D look" is, concretely)
- Waxy uniform leather sheen, no real grain/wear
- Perfect bilateral symmetry, bag always display-oriented to camera
- Dramatic editorial light (golden rim light, sculpted shadows) instead of flat phone light
- Professional-lens bokeh
- Art-directed prop spacing (flatlay grid)

## Method
GPT Image 2 (Higgsfield MCP, `gpt_image_2`, resolution 1k, quality high, 9:16).
Per scene: [real scene frame] + [real product ref(s)] →
"output = the next frame from the same phone in the same place; product refs are GEOMETRY AND
MATERIALS ONLY" + verbatim identity block (PRODUCT-TRUTH 2b: 25×22×14, horizontal straps to side
roller buckles, domed flap, clochette, gold feet, turn-lock block) + moment line + anti-CGI footer.

## Seeds
- `seeds/local/` — 26 frames from real assets on disk:
  - street/ (swipe 02: park walkaway, curb crouch, coffee crossing, brick crossing, cars walkaway)
  - outdoor-bench/ (swipe 04: white bench setdown, coffee-by-car carry, hands-open, brick drive)
  - chair-pack/ (swipe 05: boucle chair items, hands lip, pouch in, chair arm, chair wide)
  - home-mirror/ (swipe 04: mirror room)
  - macro-couch/ (swipe 01: suede macro, interior open, couch)
  - real-bag-table/ (Brooks's real iPhone photos/videos of the AG 25cm on the farmhouse table)
- `seeds/tiktok/` — agent-sourced real TikTok frames (cafe-interior, car, home, flatlay,
  street-extra, checkout) — see manifest.md there.

## Higgsfield media IDs (uploaded 2026-08-20, 24h URL TTL but media persists)
- LC-01.png → 6cc48e58-dea5-4bd4-a434-ff891b736244
- LC-02.png → 61484bf8-cf3a-4adf-a721-6bd9d38fb7cb
- DC-01.png → 6b823bc3-b2bb-4118-b456-837ab0b3f492
- AG-01.png → 0600c1de-f2f0-4a1d-ba2f-8574d9a48544
- rt-front-table.jpg → 6c932a6c-48e1-4172-9ea3-1dac145e0190
- st-walkaway-park.jpg → b62477f7-eeb6-469d-a922-33145b2cbd74
- cp-hang-chairarm.jpg → c0b9ccc6-eb73-4700-8599-f15874264948
- ob-bag-on-bench.jpg → 1157df4b-b049-4f6b-bc7f-7b49cc203a84
- cp-hands-lip.jpg → 80d49252-917d-49d7-bde4-aa40484fbbfc
- hm-mirror-room.jpg → a0a041f3-3a94-4898-949d-f4d11f579a94

## Pilot (fired 2026-08-20)
| # | scene | seed | colorway | job_id |
|---|-------|------|----------|--------|
| 1 | street walkaway park | st-walkaway-park | LC | a26cadd1-481b-4429-aabe-d4008dc11587 |
| 2 | bag on boucle chair seat | cp-hang-chairarm | DC | 52e08db6-e6c5-41cb-acd4-7e906de99e08 |
| 3 | bench setdown + coffee cup | ob-bag-on-bench | LC | 1fbecd71-9e26-482e-83b2-cf334dc6adc1 |
| 4 | AG farmhouse table (control/passthrough) | rt-front-table | AG | 4a00b533-8d4b-4936-aa72-a94fb69049fe |
| 5 | hand grabbing bag off chair | cp-hands-lip | LC | faff483e-008c-459e-8538-fd627193996f |
| 6 | mirror outfit check | hm-mirror-room | DC | 23c13d22-22d9-4026-8470-1b03149e3c64 |

Situational fix applied at spec time: seed 2's hobo HANGS from the chrome chair arm by its
shoulder strap; the Delphine has no shoulder strap, so the moment was rewritten to "set on the
seat cushion" (a top-handle bag gets set down, not hung).

## QA gates before board push
1. 3D-tell check (sheen, symmetry, editorial light, fake bokeh)
2. Product truth vs real refs (straps→side buckles, turn-lock block, domed flap, feet, trim)
3. No competitor logos in props (incl. background)
4. Capacity law: NO phone/sunglasses in flatlay/what-fits scenes
5. Situational awareness: the moment is nameable
6. Leather warmth numeric across set (R−G / G−B on flap patch, set range 21-24)

## Gate
Stills → contact sheets → Cutroom board → Brooks approves → only then animate (Omni,
constant-distance motions from scenes_delphine.py — HOLD family, never push-in).

Budget: Higgsfield 1091.38cr at pilot start (Ultra). kie 318.3 reserve.
Pilot verdict: ALL 6 PASS the 3D-tell check. Cost 38cr for 6 (≈6.3cr/img at 1k high).
Pilot notes: P1 wardrobe drifted from seed (white set instead of cardigan+jeans) — acceptable
but prompts hardened with "SAME clothing". P4 control preserved the real photo's realism while
correcting strap architecture — method confirmed.

## Batch A (fired, scene ids from SCENE-MAP)
| scene | job_id |
|-------|--------|
| 002 coffee-crossing DC | a2d11bf9-358c-493b-9c87-06374d68f838 |
| 003 crossing-brick LC | 0747f6a8-d46b-4ad2-9fe3-0fff3cd18076 |
| 004 walkaway-cars DC | 871eb25f-4054-437d-8648-7afed56166da |
| 005 crouch-curb LC | 7476c80e-534f-4c31-ad19-e3c377b457f0 |
| 006 brickdrive AG | 258b5351-0365-47a8-9429-40a814c3fd3e |
| 007 coffee-car LC | 71b632ee-f785-4d2a-90ab-1191193469f4 |
| 030 bag-couch LC | e3686515-f957-48c6-9379-6b9ef9e746bb |
| 031 chair-wide LC | 734ad7ce-184e-40cc-8ab0-b05ebfff9efd |

## Second media-ID registry (imported via kie URL relay)
st-coffee-crossing d185244c · st-crossing-brick 0fb03ec5 · st-walkaway-cars 0c5d903b ·
st-crouch-curb 154922a6 · ob-crossing-brickdrive 2c435a2d · ob-carry-coffee-car b4ae1c5e ·
ob-hands-open-bench 9f673445 · cp-chair-items 2bf7ae35 · cp-pouch-in b1ed468c ·
cp-chair-wide 415492be · mc-bag-couch c24b5db2 · mc-interior-open c86cfbc1 ·
mc-suede-macro 0e5e0727 · rt-standing c4d46fbe · rt-hand-turnlock 97de5860 ·
rt-topdown-open 13ff9c9b · rt-macro-pan c89f2378 · rt-side-1 af805128 ·
ref-LC-open-interior 9603df55 · turnlock-correct c20e0169

## QA ledger (updated live)
PASS: P1-P6 pilots · 003 (relabel DC — flap rendered espresso) · 004 · 005 · 031 · 027(flag:
canvas slightly suede, keep) · 028 · 038 · 040 · 042 · 043 · 058 · 002r · 006r · 007r · 030r ·
049 · 052 · 053 · 056
FAIL→re-rolled: 002 (kept old shoulder bag + face) · 006/007 (faces in frame; library law
faceless) · 030 (strap crossed over flap) · 039 (interior rendered caramel; INTERIOR LAW added:
black fabric lining, never caramel/tan leather — now in every open-bag prompt)
TT batch media IDs: cafe f8dab7c3/3d99f597/d2ce6a51 · car f73d103b/2136e288/c9427d27/e2278e84 ·
home 6f6c2cfb/dac9275c/7d399d2e/93537e78 · flatlay 0e8f9999/f6b7a3fc ·
street 5aaa1b47(t13 friends)/6f01134b(t32 trench)/b35353da(t17 shopfront)/e5d160ed(cafe door) ·
checkout 8b9785a0(counter)/e90d30db(interior wide)

## Brooks mid-run flag (2026-08-20): "text on it"
Checked all 6 pilot frames in thirds at crop level — zero burned text/captions/watermarks.
Standing rule hardened in every prompt: ABSOLUTELY NO text/lettering/captions/watermarks/logos.
Rule added: any seed frame carrying burned creator captions is DISQUALIFIED as a seed
(text in seeds risks bleeding into renders). Awaiting Brooks to point at the specific file
if he saw text somewhere else.
