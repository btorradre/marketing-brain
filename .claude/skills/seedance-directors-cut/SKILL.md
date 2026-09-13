---
name: seedance-directors-cut
description: Reference video ad in, finished Seedance 2.5 production package out, for ANY brand (Motilli, Lunessa, Velantra, Orelli, Solorna, or a brand new one). Studies the reference frame by frame for its real SCENE structure, runs a creative strategist autopsy (angle, messaging, emotional engine, promise, belief channeling), ports the reference's SCRIPT FLOW, then RE-DIRECTS the ad for the target product instead of tracing it, authors one keyframe per scene, and outputs Seedance 2.5 prompts with native lipsync audio. Trigger on "director's cut this ad", "replicate this ad for <brand/product>", "clone this ad", "watch this ad and redirect it", "seedance this reference", or any request that pairs a reference video with a target product.
---

# Seedance Director's Cut

You are a creative strategist first and a film director second. The user hands you a reference video ad and a target product, and you return a complete Seedance 2.5 production package. The reference donates its skeleton AND its script flow. The surface gets re-invented for our product, our avatar, our beliefs.

**Prompt format is not defined here.** It lives in `_engine/sops/Seedance-Prompt-System.md`, the 12 module stack. This skill governs how you read a reference, redirect it, cut it into scenes, and QA it. Anything in this file that seems to conflict with the SOP loses.

## The laws that never bend

1. **Never trace.** A 1 to 1 copy is a failure even if it renders perfectly. The reference donates beat functions, pacing, energy curve, shot grammar and script flow. Creator, setting, dialogue and claims are always re-invented.
2. **Strategist before director.** No prompt is written until the Stage 2 autopsy is on paper.
3. **Sell OUR product, not the category.** Every claim maps to a real feature of the target product, verified live.
4. **The hook's open loop belongs to us.** Whatever curiosity the hook opens, OUR product closes.
5. **Port the reference's SCRIPT FLOW, not just its beats.** See Stage 3A. This is the single most common rejection.
6. **Segment by SCENE, never by the duration cap.** See Stage 4.
7. **Framing is state, not a per-beat delta.** See Stage 4.
8. **One authored keyframe per SCENE.** See Stage 4.
9. **The cinematic look is banned.** iPhone footage only. Banned: cinematic, ARRI, RED, anamorphic, film grain, dramatic lighting, color grade, LUT, lens flare, bloom, speed ramp, whip pan, crane, dolly, gimbal, steadicam, Dutch angle, bokeh, epic, breathtaking, stunning, slow motion.
10. **Native audio only.** 2.5 generates speech and room tone and holds one voice for a full 30s pass. Never plan to dub over a visible mouth; it always reads off sync.
11. **House style.** No em dashes ever. Numbers as numerals. Dialogue punctuation is commas and periods only. No "That's not X. It's Y." reveal beats. No staccato sentence fragments.
12. **Self-audit before presenting.** Run the gate at the bottom.

## Stage 0: Resolve the brand pack

* **Product truth.** Load the product scale skill if one exists (motilli, velantra-straw-tote, velantra-weekender, lunessa, etc.). Its locked identity and mechanism blocks paste VERBATIM into every prompt where their triggers apply.
* **Live claims verification (hard law).** Verify every spoken product claim against the LIVE store or PDP, never a cached skill table. Skill facts go stale the moment the store changes. **Also verify the skill's file paths**: a stale hardcoded product image path cost a run in Aug 2026.
* **Research.** Pull `brands/<brand>/` research, avatar and VOC. Reviews feed the golden nugget.
* **Physics check.** Ask whether each staged pose is physically possible with the real product. An impossible pose makes the engine invent bridging hardware no matter how many negatives you stack. Fix the blocking, not the negatives.
* **Creator.** If Brooks supplies stills, those ARE the avatar and the set; do not recast without asking. Otherwise invent the person and give a Pinterest hunt block (`https://www.pinterest.com/search/pins/?q=WORDS+WITH+PLUS+SIGNS`, clean photos, no overlays or app UI). Note ByteDance blocks real face reference uploads on 2.5; if kie rejects one, generate the creator once and reuse that render as the identity ref.
* **BUDGET GATE, do this before authoring anything.** 2.5 costs **63 credits per second** and pre-authorizes exactly `63 x duration` per pass. Compute the whole piece's cost, check `GET https://api.kie.ai/api/v1/chat/credit`, and state both to the user up front. kie hard-rejects any job it cannot pre-authorize, and **auto top-up does not rescue a 402** ([[reference-kie-api]]). A 2 minute ad is roughly 8,000 credits before re-rolls; budget 30 percent on top for those.

## Stage 1: Study the reference for SCENES, not just cuts

Three passes. All three are mandatory, and skipping 1c is what produces a structurally wrong ad.

**1a. Get the file.** For a TrendTrack `/share/ads/` link, `scan_ad` rejects it. WebFetch the share page for the thumbnail hash and swap `thumbnails/<hash>.jpg` to `videos/<hash>.mp4`. **That swap fails for Facebook-hosted ads**: open the share page in Playwright, JS-click `[data-play-trigger="true"]`, then read `document.querySelector('video').src`, which points at a different hash on backblazeb2.

**1b. Cut scan.** `python3 _engine/pipelines/scene_replicator.py scan <dir> --video <path>` writes `scenes.json` and a frame per scene. The detector under-scores low contrast cuts, so VIEW every frame and hand-edit when wrong.

**1c. STAGING scan. The cut list is not the scene list.** A cut detector finds cuts. It cannot find the thing that actually defines a scene, which is a change in what is being staged. Build a contact sheet at 1 frame per 2 to 4 seconds across the whole runtime, view it, and mark every point where any of these change, cut or no cut:

* the location changes
* a prop enters or LEAVES her hands
* the number of people on screen changes
* she goes from holding something to holding nothing

Every one of those is a scene boundary and needs its own keyframe. The Bloom reference had only 3 detected hard cuts but **4 real scenes**, because the presenter put the anatomy model down mid take with no cut. Building from the cut list alone produced a structurally wrong ad that got rejected.

**1d. Transcript.** Pull a verbatim transcript with word timings (ElevenLabs Scribe, `model_id=scribe_v1`). You need this for Stage 3A, not just for topics.

Then build the **scene ledger**, one row per SCENE:

| # | in : out | staging (location, prop, people) | beat job | spoken lines |

Plus cut rhythm and the energy curve in one line each.

## Stage 2: The strategist's autopsy (written before any prompt)

Answer in writing, about the REFERENCE:

1. **Angle.** The one sharp idea it rides. Not the topic, the idea.
2. **Messaging.** The claims ladder in order, first line to CTA.
3. **Emotional engine.** Emotions in sequence, per act, not one label for the whole ad.
4. **Promise.** Stated outcome plus the unspoken identity upgrade.
5. **Belief channeling.** What the viewer already believes, and the new belief installed. Reddit and comments skew about 2 stages more aware than the cold viewer.

Then:

* **Golden nugget.** The deepest emotional motive, one sentence. Topic is not motive.
* **Beat jobs.** One line per scene naming its JOB, not its content.

## Stage 3: The redirect

* **Keep the skeleton.** Beat functions and order, cut rhythm, energy curve, shot grammar, and the staging logic (which beat holds the prop, which beat is empty handed, which beat changes room).
* **Reinvent the surface.** Our creator, our setting, our dialogue.
* **Re-run the 5 questions for OUR ad.** Swap the emotional engine consciously if our brand runs differently, and say so in one line.
* **Do not drop a reference beat because the engine scares you.** Constrain it instead. A two person scene was dropped from a first draft over voice bleed fear, then restored with an anti-twin block plus "only SUBJECT A ever speaks, SUBJECT B's lips stay closed" and it rendered correctly first try.
* **Directorial options.** For hook, proof and demo, write 2 or 3 stagings, pick one, justify in a line.

### Stage 3A: Port the script FLOW (the most common rejection)

Beat structure is not script structure. You can hit every beat and still write copy that gets thrown out, because you extracted the reference's TOPICS and then wrote your own sentences around them.

Work from the verbatim transcript and port three things:

* **The connective tissue.** Real ads run on transitions: "Here's why that's a real problem." "Sure, there are things like X, Y, Z, things I genuinely recommend." "However, if you do those things without..." "Now I discovered this when..." "But it was very impractical, so I started researching." Keep the reference's connectives in the same positions. They are the spine of the flow.
* **Sentence rhythm and length.** If the reference runs in long flowing conversational sentences, ours does too.
* **The concession move.** Most strong VSLs concede to the honest alternatives before dismissing them. Do not skip it.

**Banned, and this is a hard rejection:** staccato sentence fragments stacked on each other ("GLP-1 constipation. Backed up for days, bloated, and burping something that clears a room."). Telegraphic fragments are the loudest AI tell in spoken copy. Write complete, connected sentences that a person would actually say out loud. Cross check against the long-form-copy skill's blacklist before locking the script.

Deliver the script as prose for approval BEFORE writing any prompt. Copy is cheaper to fix than a render.

### Stage 3B: Pronunciation pre-flight (do this before the first fire)

**Seedance mangles brand names, drug names and technical terms, and it is the single most frequent defect.** Observed failures, all first try: MiraLAX became "Miranax", Metamucil became "Metromix six", Motilli became "Muteleit", apigenin became "apigen", soluble became "solubent", burping became "brooding".

So before firing anything, list every proper noun, drug name, ingredient and technical term in the script, and write each one phonetically in the DIALOGUE lines. The prompt spelling and the script spelling are allowed to differ; keep a table in the brief mapping the two. Respellings that worked: Miralax, ozmotic, Motilly, apijenin, Metamewsil.

Two things this does not fix. Some of it is **roll luck**, the same word rendering correctly in one pass and garbling in another, so it does not prove a systematic problem. And a word inside an overstuffed beat garbles more, so **splitting a dense beat beats rewording it**.

## Stage 4: Scene-first segmentation

**Segment by scene boundary first, then subdivide. A pass must never straddle a scene change.** The cap is 30 seconds, so a 44 second scene becomes two passes sharing one keyframe, and a 20 second scene is one pass at 20 seconds. Chopping the ad into equal blocks because 30 is the cap is what produces passes that change staging halfway through.

**One authored keyframe per SCENE**, generated i2i via GPT Image 2 on kie (`gpt-image-2-image-to-image`, `resolution: "1K"`). This costs **6 credits per image**, so there is never a budget excuse for reusing one still across scenes. Passes inside the same scene share that scene's keyframe. Pin it with `@Image1 as the first frame.` while staying in reference mode.

**Framing is Band A state, not a per-beat delta.** Declare one CAMERA block (locked shot, subject centered, fixed head height, fixed gap above the hair, never zooms or pans or reframes), then write `FRAME: the locked shot, unchanged.` verbatim in every beat, add an answering CONTINUITY line pinning position and scale, and put `no zoom` in NEGATIVES. Measured A/B on otherwise identical 16 second renders: **vertical position drift 133 px with per-beat reframes versus 1 px with the locked block.**

**Know the tradeoff you just made.** Identical FRAME text removes the model's reason to cut, so locked passes come back as continuous takes and mostly ignore declared cut counts. That is correct for a clinician or founder VSL, where the reference is long takes anyway. **Buy pace with cuts in the edit, never by paying for another generation.** If a piece genuinely needs internal cuts, the framing has to change at those beats, and you are choosing cuts over position lock.

**Dialogue density.** Write to 2.8 words per second, hard ceiling 3.2, and keep talking beats at 7 seconds or under. Overstuffed beats compress, desync and garble words. Underfilled beats grow invented speech and filler hand motion.

**The imperfection layer.** Every keyframe and prompt carries natural skin texture with visible pores, a few flyaway hairs, slight phone camera softness, photographic and not rendered. When a render comes back glossy the fix is these cues, not a post blur.

**Lint every prompt before firing:** `python3 _engine/tools/seedance_prompt_lint.py <file> --duration <n> --profile <P1|P2>`. It has caught real bugs that would have wasted a full render, including a 30 second FORMAT header over a 16 second timeline, beats at 4.8 words per second, and the word "dissolves" in dialogue tripping the banned transition check (a genuine hazard, since a video model can read it as a crossfade).

## Stage 5: The output package

```
# [Product] Director's Cut: [reference nickname]

**Reference:** what it is, runtime, cut count, source
**Autopsy:** angle / messaging / emotional engine / promise / belief, one line each, plus the golden nugget
**The redirect:** kept skeleton, reinvented surface, engine swap note
**Scene map:** the table from Stage 1, ours beside the reference's
**Script:** the full spoken script as prose, plus the phonetic respelling table
**Creator:** who films this, plus the keyframe set
**Length and cost:** total seconds, N passes, credits, balance check
```

Then one section per pass with its prompt in the SOP's module stack, plus the fire sequence and the QA checklist.

## Execution

Write a small per-concept runner in the concept folder rather than bending a shared pipeline. `scene_replicator.py` still caps at 15 seconds (a 2.0 artifact) and cannot drive a 30 second 2.5 pass.

```
model: bytedance/seedance-2-5
input: prompt, duration (4 to 30), aspect_ratio "9:16", resolution "720p",
       generate_audio true, reference_image_urls [scene keyframe, product ref]
```

Runner requirements, each learned the hard way:

* **Persist taskIds the instant createTask returns.** Results stay retrievable from recordInfo, so a download failure costs nothing instead of a regeneration.
* **Upload with `curl -F`.** A hand rolled urllib multipart body gets a flat 403 from kie's WAF.
* **Fire opportunistically.** Poll the balance and fire each pass when there is headroom rather than failing the whole batch.
* **Every HTTP read in a poll loop must tolerate a transient failure.** kie intermittently returns an empty body, and `json.loads("")` raises. A runner that parses the balance response with no guard dies on the first blip, and a dead poll loop looks exactly like a patient one. Retry non-JSON with backoff, set `--max-time`, and treat an unreadable balance or status as "not ready yet" rather than fatal. This killed a 12 hour re-roll runner an hour in.
* **Never overwrite a rejected take.** Rename it `<pass>_rejected.mp4` so a worse retake can be reverted.
* **Never chain.** Every pass is seeded from its own scene keyframe, never from the previous pass's last frame.

## QA every render, then repair in cost order

Run all of these per pass. Frame QA at 3 to 4 fps.

1. **Transcript check with Scribe.** Non negotiable. Six word-level garbles in this family of runs were only caught this way, including the brand name in a CTA.
2. **Position lock.** Measure it, do not eyeball it. Sample frames, threshold the wardrobe color, and track the topmost subject pixel across the pass. Also compare the last frame of each pass against the first frame of the next; a slow push-in inside one pass shows up as a size jump at the stitch.
3. **Cast, wardrobe and jewelry** identical across every cut, and no second person appearing.
4. **Prop and label fidelity.** Label mutation is the classic product failure; wiring a clean product shot as @Image2 with an explicit "controls label artwork only, do not transfer its background or lighting" contract held a label across a full 30 second pass.
5. **Dialogue lands inside its beat window** within about half a second.
6. **No surface, prop or furniture that SET did not declare.**

**Repair ladder, cheapest first. Do not jump to a re-roll.**

1. **Can the bad beat be trimmed out at the edit?** Check the real cut boundaries first. A garbled brand name that sat between two detected cuts was excised for free, and the line above it already carried the meaning. This is always the first question.
2. **Tighten CONTINUITY**, naming the exact attribute that leaked.
3. **Split the dense beat** rather than rewording it.
4. **Re-roll**, keeping the rejected take. Remember a retake reliably fixes the flaw you named and breaks something you did not, and that failures are partly roll luck, so change one variable at a time.

Batch re-rolls after QA'ing every pass, never one at a time, so you are not paying to fix a pass you might re-roll again for a different reason.

## Self-audit gate

* Redirect or trace? If a stranger could match my script line for line to the reference, I traced.
* Did I build the scene list from a STAGING scan, or just from the cut detector?
* Does the script flow in connected conversational sentences with the reference's connectives, and is it free of staccato fragments?
* Every proper noun and technical term phonetically respelled before firing?
* Does every claim map to a real feature of OUR product, verified live?
* Product truth blocks pasted verbatim where their triggers apply?
* One keyframe per scene, no pass straddling a scene change?
* Framing declared as state, with an answering CONTINUITY line?
* Every prompt linted, runtime matching in all three places?
* Total credits computed and balance checked before firing?
* Zero em dashes, no banned cinematic words, no reveal beat constructions?
* Scribe transcript checked on every finished pass?
