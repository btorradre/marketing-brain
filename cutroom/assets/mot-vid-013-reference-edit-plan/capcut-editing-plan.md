# MOT-VID-013 — CapCut editing plan

**Plan complete; edit and new voice generation have not started.** The latest user instruction selects CapCut. Use the science-v2 selected clips, preserve the exact 291-word script, and keep three interchangeable hooks. The reference breakdown is in `reference-breakdown.md` and the 33-shot map in `reference-cut-map.json`.

## Creative approach

Each shot answers the current sentence. Anatomy carries stomach slowdown, constipation, fullness, burps and ingredient function. Objects carry named remedies, the bathroom and the GLP-1 pen. People appear for waking up, dressing, making plans and feeling like yourself. Preserve the science-heavy revision already accepted.

Borrow the reference’s rhythm: hold the hook; accelerate a list with short inserts; give a complex mechanism enough time; make ingredient-to-action cuts; use a bright product reveal; finish with warm human activity and a clear offer. Its median shot is 1.88 seconds, but it varies from 0.76 to 4.36 seconds. Do not force every Motilli clip to the same length.

## Voiceover first

The current Woman Over 40 take is not established as the reference narrator and will not be passed off as a clone. Two audio analyses describe the reference as a brisk male lower-register American explainer voice. Its measured rough pace is 222 words/minute over the full reference, much faster than the current Motilli draft. Match directness, stress and short contrast pauses while preserving intelligibility of apigenin, soluble fiber and chlorophyllin.

For a reference clone, first establish permission/rights or a licensed existing ElevenLabs voice ID. ElevenLabs explicitly requires permission for Instant Voice Cloning: https://elevenlabs.io/docs/help-center/product/voices/my-voices/what-is-my-voices . A competitor reference URL alone does not establish those rights. Do not attest to rights on the user’s behalf. If an authorized clone or licensed voice is available, use that source. An alternative voice would need to be identified as an alternative.

Production sequence: prepare a clean authorized voice sample; inspect for music contamination; create or select the authorized voice; generate a short pronunciation/pacing test; then a complete exact-script narration with ElevenLabs. Review the whole take for omissions, repeats and unnatural delivery. Obtain fresh word timestamps from the selected final audio. Do not automatically apply the old 1.22× playback rate. The target remains approximately 95 seconds unless the user changes the duration brief; final timings are determined by the approved narration performance.

## CapCut build

CapCut 9.3.0 is installed, the draft folder exists, and plaintext drafts use materials/tracks. The local bridge is `_engine/mcp/capcut-kit/capcut-bridge.py`; its documented UI testing was on 8.9.0, so inspect the current accessibility controls before relying on its open/seek/export selectors. This is a verified route to investigate, not a claim that export on 9.3.0 has already passed.

Create a new isolated MOT-VID-013-science-CapCut project, preserve existing drafts, and back up any registry before file-lane writes. Use the bridge’s normal save/quit sequence, never force-kill an unsaved session. Import the selected native files listed in `capcut-edit-plan.json`; use the revised S12 and S22 sources and retained approved product shots. Build the main variant, then duplicate into A/B/C and replace only the hook imagery and hook banner.

Track layout: V1 for B-roll, V2 for restrained emphasis and ingredient labels, V3 for captions, V4 for CTA/guarantee elements; A1 continuous narration, A2 quiet licensed underscore, A3 sparse transition effects. Mute source clip audio. Use 1080×1920 at 30fps for delivery; source motion is 720×1280/24fps, so inspect scaling/cadence and do not advertise the source as native 1080p.

## Cuts and transitions

Default to hard cuts at complete meaning units or the named object/action. The narration runs continuously across them. Reframe within S06 (remedy list), S16 (upstream/downstream), S20 (ingredient detail) and S28 (gummy count) if needed to avoid long repetitive holds. These are crop/scale edits in CapCut, not new generated people clips. Keep anatomy screen direction consistent and use modest crops so the 720p sources stay clear.

Proposed blur resets: S03 trap, S22 second ingredient, S27 product reveal, S32 imagined morning. Begin around 0.20–0.24 seconds and shorten if text readability suffers. The reference’s approximately 0.24–0.28-second rendered blur is evidence, not a mandate to use eight effects. Keep captions on their own readable track rather than blurring them with the source. Use available clip handles without moving narration or changing total timing.

## Captions, labels and closing card

Body captions: mostly 2–4 words per chunk, up to 5 only where the phrase reads better; bold black sans-serif on compact white rounded backing. Start around 64–68% of frame height, then inspect every organ/hand/product frame and platform UI overlap. The existing 73% caption position is a starting draft setting to revisit. Hook: larger white uppercase on dark green. Trap: one short red-backed emphasis. Ingredient labels: distinct from captions, anchored where they do not cover the named material. Avoid running a second full sentence above the captions.

S37 has three reading priorities: Motilli package/name, 90-DAY MONEY-BACK GUARANTEE, then SHOP MOTILLI / TAP BELOW. Reveal the guarantee near the spoken guarantee; keep the last two seconds stable. Maintain exact Motilli packaging and exactly two heart-shaped gummies. Do not inherit the reference’s 60-day guarantee, capsules, vitamin claims, or customer testimony.

## Audio finish and delivery checks

Keep narration dominant; choose a quiet licensed instrumental texture and duck it where necessary. Small swishes may support the four blur resets. Do not add a sound effect to every hard cut. The reference’s subtle background mix is not fully resolved by audio analysis, so named instruments and beat-perfect sync are not asserted here. Make music changes follow narrative sections rather than overwhelm the voice.

Listen to the complete final edit at normal playback. Check every cut against the spoken noun/action, all 291 words, captions, pronunciation, organ continuity, product labels, end-card reading time, video bounds, audio peaks and source mute state. Inspect the exported MP4 as well as the CapCut timeline. Deliver three hook variants, editable CapCut drafts, final MP4s, caption files and a source/voice manifest.

## Line-by-line cut instructions

Times below are the existing 96.63-second draft for orientation only. They must be rebuilt against the new final narration; every row has its exact native source in the JSON plan.

| Shot | Provisional time | Exact narration | Reference analogy | CapCut edit |
|---|---|---|---|---|
| HA1 | 0.00–1.93s | On a GLP-1, the harder you push your colon | R01–R03 | opening. Open immediately on remedy cabinet; persistent hook banner. Keep bottles identifiable during the short hold. |
| HA2 | 1.93–4.53s | with laxatives and fiber, the more stuck you can feel. | R01/R11 | hard cut. Hard cut from remedies to colon while the line names laxatives, fiber and feeling stuck. Preserve headline across the cut. |
| S03 | 4.53–6.47s | Here’s the trap no one explains. | R02 | horizontal blur, 0.20–0.24s. Short horizontal blur into anatomy; swap persistent headline for red-backed trap cue, then return to normal captions. |
| S04 | 6.47–8.73s | Your GLP-1 slows your stomach down. | R03 | hard cut. Hard cut on GLP-1/stomach slowdown; move eye toward stomach with the native camera action. |
| S05 | 8.73–10.33s | So when you haven’t gone in days, | R11 | hard cut. Hard cut to slow colon transit on not going in days. Keep the lumen legible. |
| S06 | 10.33–14.10s | you reach for MiraLAX, magnesium, stool softeners, or more fiber. | R04/R09/R10 | hard cut. Use the existing remedy clip; make two or three brief crop changes keyed to the named remedies if each crop stays readable. No body reaction insert. |
| S07 | 14.10–17.53s | Those products work downstream. They target the colon— | R14/R15 | hard cut. Hard cut to whole tract and label COLON on that word. Favor lower anatomy without losing the upstream relationship. |
| S08 | 17.53–19.23s | the end of your digestive system. | R14/R15 | hard cut. Tighter colon crop completes the definition; retain the COLON label over this connected beat. |
| S09 | 19.23–22.03s | But if the slowdown begins higher up in your stomach, | R03/R14 | hard cut. Cut back up to the stomach on the contrast. Swap COLON for STOMACH; keep screen direction anatomically consistent. |
| S10 | 22.03–23.90s | food is still sitting at the beginning. | R11/R24 | hard cut. Macro stomach contents on food sitting; use gentle native movement, no emptying transformation. |
| S11 | 23.90–26.13s | That’s why the relief may last a day, | R05 | hard cut. Clock/anatomy image covers temporary relief. A new small time emphasis supplies rhythm without adding a person. |
| S12 | 26.13–28.33s | the fiber can make you feel even fuller, | R06/R11 | hard cut. Selected revised stomach/fiber clip. Keep fibers lying in meal; use the clean opening window. |
| S13 | 28.33–30.60s | and those rotten-egg burps keep coming back. | R12/R24 | hard cut. Cut at burps to gas moving up the stomach/esophagus. No mouth-reaction footage. |
| S14 | 30.60–32.50s | It’s not that your body is broken. | R13 | hard cut. Intact neutral tract for body not broken. Brief visual calm before the explanation pivots. |
| S15 | 32.50–34.53s | And it doesn’t mean you have to quit your shot. | R31 | hard cut. Object-only capped GLP-1 pen on quitting the shot; native clip already has hands but focus stays on the medication object. |
| S16 | 34.53–38.63s | You’ve been trying to solve an upstream slowdown with downstream tools. | R14/R15 | hard cut. Preserve one continuous anatomy view. Add a two-stage emphasis: STOMACH / UPSTREAM, then COLON / DOWNSTREAM, exactly on the terms. A modest crop change may split this 4.1s hold. |
| S17 | 38.63–41.33s | What you need is something designed to wake your stomach back up | R18 | hard cut. Stomach locator identifies the organ; no invented cure pulse, activation claim or before/after reset. |
| S18 | 41.33–43.47s | while supporting everything below it. | R03 | hard cut. Native camera follow toward lower tract as the line says below; continue visual direction from S17. |
| S19 | 43.47–46.27s | And to do that, you need three specific things. | R16/R23 | hard cut. Show the three ingredient dishes while the narrator announces three requirements; small 1 / 2 / 3 editor labels cue the structure. |
| S20 | 46.27–50.13s | First, apigenin—a plant compound concentrated from celery juice— | R23 | hard cut. Tactile celery close-up on apigenin/from celery. Label APIGENIN / FROM CELERY. Use a second crop only if the longer narration hold needs it. |
| S21 | 50.13–52.80s | to support your stomach’s natural wave-like movement. | R24 | hard cut. Hard cut from ingredient to stomach and existing external wave line on wave-like movement. Preserve anatomy. |
| S22 | 52.80–55.27s | Second, a low-viscosity soluble fiber | R19 | horizontal blur, 0.20–0.24s. A short horizontal blur marks the second requirement. Use selected revised fiber-dispersion motion; title LOW-VISCOSITY SOLUBLE FIBER. |
| S23 | 55.27–56.73s | that holds water in the stool | R19 | hard cut. Hard cut on water/stool to colon detail. Keep the material being discussed central and readable. |
| S24 | 56.73–59.27s | without becoming another heavy bulk load. | R11/R19 | hard cut. Open lumen and sparse strands on no heavy bulk load; do not show a fake treated-versus-untreated comparison. |
| S25 | 59.27–62.30s | And third, chlorophyllin to neutralize the sulfur compounds | R23/R25 | hard cut. Straight cut into green chlorophyllin powder on third/ingredient name; title CHLOROPHYLLIN. Do not borrow B12/iron imagery. |
| S26 | 62.30–65.50s | behind those burps instead of merely covering the smell. | R24 | hard cut. Hard cut to stomach/esophageal gas source; the mint remains secondary. No molecule-binding effect added to unsupported illustration. |
| S27 | 65.50–67.77s | That’s why Motilli combines all three | R17 | horizontal blur, 0.20–0.24s. Main product reveal: brief horizontal blur into bright Motilli jar only after all three ingredients. Land the product name as the bottle becomes readable. |
| S28 | 67.77–72.10s | in two heart-shaped gummies made specifically for people on GLP-1s. | R17/R26 | hard cut. Macro gummies on two heart-shaped gummies. Preserve count, shape and package label. One short crop change can emphasize TWO without new footage. |
| S29 | 72.10–73.60s | For women on a GLP-1, | R25 | hard cut. Female anatomical torso on women using GLP-1s; transition context from formula to audience. |
| S30 | 73.60–75.83s | the goal isn’t just another trip to the bathroom. | R16 | hard cut. Empty bathroom gives literal bathroom-trip context; keep this short and move on with the narration. |
| S31 | 75.83–78.87s | It’s feeling regular again—and getting on with your day. | R18/R20 | hard cut. Gentle colon movement on regularity. End before the everyday activities begin; no treatment transformation. |
| S32 | 78.87–81.27s | Imagine waking up, going comfortably, | R20/R28 | horizontal blur, 0.20–0.24s. Short blur into warm waking-up footage at Imagine. First lifestyle payoff after the science sequence. |
| S33 | 81.27–83.83s | and getting dressed without wondering how long it’s been. | R28 | hard cut. Hard cut on getting dressed; show actual dressing action, unchanged body size. |
| S34 | 83.83–87.20s | Making plans without your stomach being the first thing you think about. | R29 | hard cut. Hard cut on making plans; phone action carries the sentence. Keep phone text out of focus and avoid fabricated messages. |
| S35 | 87.20–89.03s | You want to feel like yourself again, | R29 | hard cut. Close face on feel like yourself. Allow the expression to settle without an extra transition. |
| S36 | 89.03–91.27s | without giving up the progress you’ve worked for. | R31 | hard cut. Hard cut to capped pen/planner on keeping progress. Finish with the medication visible. |
| S37 | 91.27–96.63s | Motilli. 90-day money-back guarantee. Tap below. | R32/R33 | hard cut. Final pack shot on Motilli. Build 90-day guarantee as separate CapCut text/shape; show SHOP MOTILLI / TAP BELOW. Hold a stable, uncluttered layout through the two-second tail. |

Hook B uses HB1/HB2 and hook C uses HC1/HC2 from the existing science-v2 source catalog. Retain the shared audio and common-body join after the identical hook narration. Re-evaluate that join time after new voice alignment.
