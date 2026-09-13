---
name: seedance-directors-cut
description: Takes a reference video ad and a target product and produces a complete AI-video production package for a different product — studying the reference frame by frame for its real scene structure, running a creative-strategist autopsy (angle, messaging, emotional engine, promise, belief channeling), porting the reference's script FLOW (not just its topics), then re-directing the ad for the target product instead of tracing it, authoring one keyframe image per scene, and producing per-scene AI video generation prompts with native lip-synced audio. Works for any brand or product. Use whenever you have a reference video ad and a target product and want a genuinely redirected (not copied) ad built from it. Trigger on "director's cut this ad", "replicate this ad for <brand/product>", "clone this ad", "watch this ad and redirect it", or any request that pairs a reference video with a target product.
---

# Director's Cut: Reference Ad to Redirected AI Video Ad

This skill describes how to take a reference video ad and a target product and produce a complete AI-video production package for a different product — studying the reference frame by frame for its real scene structure, running a creative-strategist autopsy on it (angle, messaging, emotional engine, promise, belief channeling), porting the reference's script FLOW (not just its topics), then re-directing the ad for the target product instead of tracing it, authoring one keyframe image per scene, and producing per-scene AI video generation prompts with native lip-synced audio. Works for any brand or product. Use whenever you have a reference video ad and a target product and want a genuinely redirected (not copied) ad built from it.

Act as a creative strategist first and a film director second. The reference donates its skeleton AND its script flow. The surface — creator, setting, dialogue, specific claims — gets re-invented entirely for the target product, its own avatar, and its own beliefs.

This skill does not define exact prompt syntax for any specific video model — that's a separate, model-specific concern. This skill governs how to read a reference, redirect it, cut it into scenes, and QA it.

## The laws that never bend

1. **Never trace.** A shot-for-shot copy is a failure even if it renders perfectly. The reference donates beat functions, pacing, energy curve, shot grammar, and script flow. Creator, setting, dialogue, and claims are always re-invented.
2. **Strategist before director.** No prompt gets written until the creative autopsy (below) is on paper.
3. **Sell the target product, not the category.** Every claim maps to a real, verified feature of the target product.
4. **The hook's open loop belongs to the new product.** Whatever curiosity the hook opens, the target product closes.
5. **Port the reference's SCRIPT FLOW, not just its beats.** This is the single most common way a redirect gets rejected — see the script-flow section below.
6. **Segment by SCENE, never by an arbitrary duration cap.** See the segmentation section below.
7. **Framing is a fixed state, not something that shifts beat to beat.** See the segmentation section below.
8. **One authored keyframe per SCENE.**
9. **The cinematic look is banned.** Aim for iPhone-style footage only. Banned vocabulary: cinematic, ARRI, RED, anamorphic, film grain, dramatic lighting, color grade, LUT, lens flare, bloom, speed ramp, whip pan, crane, dolly, gimbal, steadicam, Dutch angle, bokeh, epic, breathtaking, stunning, slow motion.
10. **Native audio only.** Modern AI video models can generate speech and room tone together and hold one consistent voice for a full ~30-second pass. Never plan to dub separately recorded audio over a visible speaking mouth — it will always read as out of sync.
11. **House style.** No em dashes ever. Numbers as numerals. Dialogue punctuation is commas and periods only. Avoid "That's not X. It's Y." style reveal constructions. Avoid staccato sentence fragments.
12. **Self-audit before presenting.** Run the self-audit checklist at the end of this document before delivering anything.

## Stage 0: Resolve the brand pack

- **Product truth.** If a locked identity/mechanism reference document exists for this product, its verbatim identity and mechanism language must be pasted into every prompt where it applies.
- **Live claims verification (hard rule).** Verify every spoken product claim against the CURRENT live store/product page, never a cached or previously-written reference — facts go stale the moment the store changes. Also double-check any file paths or reference images you're relying on are still current — a stale hardcoded product image reference has caused a wasted run before.
- **Research.** Pull whatever audience/avatar/voice-of-customer research exists for this brand. Real reviews and testimonials are where the golden nugget usually surfaces.
- **Physics check.** For every staged pose you're about to script, ask whether it's actually physically possible with the real product. An impossible pose (e.g. a carry style the product's handles can't physically support) makes the video model invent bridging elements that shouldn't exist, no matter how many negative instructions you stack against it. Fix the blocking/staging, not the negative-prompt list.
- **Creator.** If real reference photos of a specific creator are supplied, those ARE the avatar and the setting — don't recast without asking. Otherwise, invent the person and describe exactly what kind of reference photo to search for (age, look, vibe, setting) — clean photos only, no text overlays or app UI visible in the reference. Be aware some video models block uploading real face photos as an identity reference directly; if that happens, generate the creator once as an image, then reuse that generated image as the identity reference for every subsequent step.
- **Budget gate — do this before authoring anything.** Compute the full piece's total video-generation cost (seconds × your platform's per-second rate) and check your actual account balance before starting. Video generation platforms typically pre-authorize the full cost of a request and will hard-reject any job they can't fully pre-authorize — don't assume an auto-top-up feature will rescue an insufficient-balance rejection; verify that assumption for your specific platform. Budget roughly 30% extra on top of the base cost for expected re-rolls/retakes.

## Stage 1: Study the reference for SCENES, not just cuts

Three passes, all mandatory — skipping the third is what produces a structurally wrong ad.

**1a. Get the file.** Download the reference video by whatever means works for its source (direct file, a video downloader tool for a social platform link, or — if a link resolves to a share page rather than the file directly — a browser automation tool to load the page and read the actual video element's source URL out of the page).

**1b. Cut scan.** Run scene-change detection on the video (frame-difference-based cut detection) to get an initial scene table plus one representative frame per detected scene. The detector under-scores low-contrast cuts, so VIEW every extracted frame yourself and hand-correct the scene table where it's wrong.

**1c. STAGING scan — the cut list is not the scene list.** A cut detector finds hard visual cuts. It cannot find the thing that actually defines a scene, which is a change in what's being staged. Build a contact sheet by extracting one frame every 2-4 seconds across the entire runtime, view all of them together, and mark every point where ANY of these change, whether or not there's a detected cut at that point:

- the location changes
- a prop enters or LEAVES the person's hands
- the number of people on screen changes
- the person goes from holding something to holding nothing

Every one of those is a scene boundary and needs its own keyframe, even with no hard cut. (Real example: a reference had only 3 detected hard cuts but 4 real scenes, because the presenter put down a prop mid-take with no cut — building the scene list from cuts alone produced a structurally wrong ad that got rejected.)

**1d. Transcript.** Pull a verbatim transcript with word-level timing (a speech-to-text tool with word timestamps and speaker diarization is ideal). You need this for the script-flow work in Stage 3, not just to know the topics covered.

Then build a **scene ledger**, one row per SCENE: scene number, in/out timestamps, staging description (location, prop, people), the beat's JOB (not its content), and the spoken lines in that scene. Also note the overall cut rhythm and energy curve in one line each.

## Stage 2: The strategist's autopsy (written before any prompt)

Answer in writing, about the REFERENCE:

1. **Angle.** The one sharp idea it rides. Not the topic — the idea.
2. **Messaging.** The claims ladder in order, from the first line to the call-to-action.
3. **Emotional engine.** The sequence of emotions, act by act — not one label for the whole ad.
4. **Promise.** The stated outcome, plus the unspoken identity upgrade underneath it.
5. **Belief channeling.** What the viewer already believes going in, and the new belief the ad installs. Note that comment sections and forum discussion tend to skew noticeably more aware/informed than the average cold viewer — calibrate down from what engaged commenters already know.

Then write:
- **Golden nugget.** The deepest emotional motive, one sentence. Topic is not motive.
- **Beat jobs.** One line per scene naming its JOB, not its content.

## Stage 3: The redirect

- **Keep the skeleton.** Beat functions and order, cut rhythm, energy curve, shot grammar, and the staging logic (which beat holds the prop, which beat is empty-handed, which beat changes rooms).
- **Reinvent the surface.** Your own creator, your own setting, your own dialogue.
- **Re-run the five autopsy questions for YOUR ad.** If your brand's emotional engine genuinely needs to run differently than the reference's, swap it consciously and say so in one line — don't swap it accidentally.
- **Don't drop a reference beat just because a video model scares you.** Constrain the staging instead of cutting the beat. (Real example: a two-person scene was initially dropped from a first draft out of fear of voice bleed between the two people, then successfully restored by adding an "anti-twin" instruction plus an explicit "only Subject A ever speaks, Subject B's lips stay closed" rule — it rendered correctly on the first try.)
- **Directorial options.** For the hook, the proof beat, and the demo beat specifically, sketch 2-3 different staging options, pick one, and justify the pick in one line.

### Stage 3A: Port the script FLOW (the most common source of rejection)

Beat structure is not the same thing as script structure. You can hit every beat correctly and still write copy that gets rejected, because you extracted the reference's TOPICS and then wrote entirely your own sentences around them, losing the actual flow.

Work from the verbatim transcript and specifically port three things:

- **The connective tissue.** Real ad scripts run on transitional phrases: "Here's why that's a real problem." "Sure, there are things like X, Y, Z, things I genuinely recommend." "However, if you do those things without..." "Now I discovered this when..." "But it was very impractical, so I started researching." Keep the reference's connective phrases in roughly the same structural positions — they're the actual spine of the flow, not decoration.
- **Sentence rhythm and length.** If the reference runs in long, flowing, conversational sentences, your redirected version should too.
- **The concession move.** Most strong long-form video sales copy concedes honestly to legitimate alternative solutions before explaining why they fall short. Don't skip this move.

**Banned, and this is a hard rejection:** staccato sentence fragments stacked on top of each other (e.g. "GLP-1 constipation. Backed up for days, bloated, and burping something that clears a room."). Telegraphic sentence fragments are one of the most obvious signs that copy was AI-generated. Write complete, connected sentences that a real person would actually say out loud.

Deliver the full script as prose for approval BEFORE writing a single generation prompt. Copy is far cheaper to fix than a finished render.

### Stage 3B: Pronunciation pre-flight (do this before the first generation)

AI video models frequently mangle brand names, drug/ingredient names, and technical terms — this is one of the single most common defects in this kind of production. So before generating anything, list every proper noun, brand name, ingredient name, and technical term in the script, and write out a phonetic respelling for each one specifically for the DIALOGUE text (the prompt's own descriptive text and the dialogue's spelling are allowed to differ — keep a small mapping table of "real spelling → dialogue respelling" in your brief).

Two caveats: some of this comes down to roll luck (the same word can render correctly once and garble the next time — that's not proof the fix failed), and a word embedded in an overstuffed, too-dense beat tends to garble more often regardless of spelling — so splitting a dense beat into two often beats trying to reword the problem word.

## Stage 4: Scene-first segmentation

**Segment by scene boundary first, then subdivide only if a scene is longer than your video model's max clip length. A single generation pass must never straddle a scene change.** If your platform caps generations at, say, 30 seconds, a 44-second scene becomes two passes sharing one keyframe, while a 20-second scene is just one pass at 20 seconds. Chopping the whole ad into equal-length blocks purely because that's the technical cap is what produces passes that awkwardly change staging halfway through — don't do it.

**One authored keyframe per SCENE**, generated via image-to-image from your product/creator reference photos. Multiple generation passes within the same scene should all share that one scene's keyframe as their starting image. Whatever mechanism your image model offers for pinning to a specific reference image, use it explicitly (e.g. "use this as the first frame").

**Framing is a fixed state, not a per-beat delta.** Declare one fixed camera description up front (locked shot, subject centered, fixed head height, fixed gap above the hair, never zooms or pans or reframes), then repeat a line like "the locked shot, unchanged" verbatim in every beat's camera description, add a matching continuity instruction pinning the subject's position and scale, and explicitly add "no zoom" to your negative-instructions list. This matters a lot in practice — one measured comparison found roughly 133 pixels of vertical position drift across an otherwise-identical 16-second render when each beat got its own slightly-reworded framing description, versus about 1 pixel of drift when the exact same locked framing text was repeated verbatim in every beat.

**Know the tradeoff this creates.** Using identical framing text in every beat removes the model's own internal signal that it should cut to something new, so locked-framing passes tend to render as one continuous take and mostly ignore any cut count you tried to specify. That's actually correct for something like a single-person, single-setting talking-head piece, where the reference itself is mostly long continuous takes anyway. If a piece genuinely needs internal cuts, buy that pace in the video EDIT afterward, not by paying for another separate generation — and if you truly need a mid-clip cut baked into one generation pass, the framing description has to actually change at that beat, which means you're deliberately choosing cuts over position-lock for that specific pass.

**Dialogue density.** Write to roughly 2.8 words per second, hard ceiling around 3.2, and keep any single talking beat to 7 seconds or under. Overstuffed beats compress, desync, and garble words. Underfilled beats tend to grow invented extra speech and filler hand motion to fill the time.

**The imperfection layer.** Every keyframe and every prompt should carry natural skin texture with visible pores, a few flyaway hairs, slight phone-camera softness — photographic, not rendered. When a render comes back looking glossy/CGI, the fix is adding these specific descriptive cues to the prompt, not trying to blur it in post-production.

**Lint every prompt before generating.** Whether by hand or with a small script you write yourself, check every prompt for: does the stated duration actually match the described timeline (a mismatched header duration versus content is a real, easy-to-make mistake); is the words-per-second density within the target range; and does the dialogue contain any word that could be misread as a transition/edit instruction by the model (e.g. the literal word "dissolves" in spoken dialogue has been observed to trigger an unwanted crossfade-style visual artifact in some models, since it reads it as an edit instruction rather than as spoken text).

## Stage 5: The output package

Structure the finished deliverable as:

```
# [Product] Director's Cut: [reference nickname]

**Reference:** what it is, runtime, cut count, source
**Autopsy:** angle / messaging / emotional engine / promise / belief, one line each, plus the golden nugget
**The redirect:** kept skeleton, reinvented surface, engine swap note
**Scene map:** the scene ledger table, ours beside the reference's
**Script:** the full spoken script as prose, plus the phonetic respelling table
**Creator:** who films this, plus the keyframe set
**Length and cost:** total seconds, number of generation passes, estimated cost, balance check
```

Then one section per generation pass, with its full prompt, plus the generation order/sequence and the QA checklist below.

## Execution notes

Whatever your generation pipeline looks like, build these behaviors in regardless of the specific video platform:

- **Persist every generation job ID the instant a request is submitted**, before waiting for the result — most platforms keep results retrievable for a while after generation, so a download failure afterward costs nothing extra as long as you kept the ID; without it, a download hiccup forces an expensive full regeneration.
- **Upload reference files using a standard multipart form upload**, not a hand-rolled minimal HTTP client — some platforms' bot-protection will reject an unusual-looking upload request outright.
- **Fire generations opportunistically against your remaining balance** rather than trying to validate the whole batch's cost up front and failing the entire run if one estimate is off.
- **Every network call inside a polling loop must tolerate a transient failure or an empty/malformed response** rather than crashing — some APIs intermittently return an empty body, and a naive JSON parser will throw on that. Retry with backoff, set a reasonable timeout, and treat an unreadable response as "not ready yet," not as a fatal error. A polling loop that dies on the first transient blip looks exactly like a healthy, still-running loop from the outside, which can silently waste hours.
- **Never overwrite a rejected take.** Rename it clearly (e.g. append "_rejected") so a worse retake can be reverted to the previous one if needed.
- **Never chain passes together.** Every generation pass should be seeded from its own scene's keyframe image, never from the previous pass's last frame.

## QA every render, then repair in cost order

Run all of these checks per generated pass, viewing frames closely (a few frames per second) rather than just watching at normal speed:

1. **Transcript check.** Non-negotiable — run the finished audio back through a speech-to-text tool and read the transcript. Word-level garbles (including in something as important as a brand name inside a call-to-action) have repeatedly only been caught this way, not by ear.
2. **Position lock.** Measure it, don't eyeball it — sample frames and track a subject's position/scale numerically if you can. Also explicitly compare the LAST frame of one pass against the FIRST frame of the next pass in sequence — a subtle push-in that happened smoothly within one pass can show up as a jarring size jump at the stitch point between passes.
3. **Cast, wardrobe, and jewelry identical across every cut**, and no unintended second person appearing.
4. **Prop and label fidelity.** Label/text mutation on a product is one of the most common failure modes — wiring in a clean, explicit product reference image with an instruction like "controls label artwork only, do not transfer its background or lighting" has successfully held a label correct across a full-length pass.
5. **Dialogue timing lands inside its intended beat window**, within roughly half a second.
6. **No surface, prop, or furniture appears that wasn't explicitly specified** in the staging description.

**Repair ladder — always try the cheapest fix first, don't jump straight to a full re-roll:**
1. **Can the bad beat just be trimmed out in the final edit?** Check the real cut boundaries first — a garbled brand name that happened to sit between two natural cut points has been successfully removed for free in editing, when the line right before it already carried the necessary meaning. Always ask this question first.
2. **Tighten the continuity instruction**, naming the exact attribute that leaked/drifted.
3. **Split a dense beat into two** rather than trying to reword it.
4. **Re-roll**, but keep the original rejected take on disk. Remember that a retake reliably fixes the specific flaw you named while sometimes introducing a different, new problem — and that some of this is genuinely roll luck — so change only one variable at a time between attempts.

Batch up your re-rolls after QA-ing every pass in the whole piece, rather than fixing one pass at a time — otherwise you risk paying to fix a pass you might need to re-roll again anyway for an unrelated reason discovered later.

## Self-audit gate — run before delivering anything

- Redirect or trace? If a stranger could match your script line-for-line against the reference, you traced it.
- Did you build the scene list from a full STAGING scan, or just from the automatic cut detector?
- Does the script flow in connected, conversational sentences using the reference's own connective phrases, and is it free of staccato sentence fragments?
- Has every proper noun and technical term been phonetically respelled before generating?
- Does every claim map to a real, currently-verified feature of the target product?
- Have any product-truth reference blocks been pasted in verbatim wherever they apply?
- One keyframe per scene, with no generation pass straddling a scene change?
- Is framing declared as a fixed state, with a matching continuity instruction?
- Has every prompt been checked for duration mismatch and other lint issues, with runtime matching everywhere it's stated?
- Has the total cost been computed and the account balance checked before generating?
- Zero em dashes, no banned cinematic vocabulary, no "that's not X, it's Y" reveal constructions?
- Has the finished audio of every completed pass been run back through a transcript check?
