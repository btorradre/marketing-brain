# Seedance Prompt System

**Scope:** every Seedance generation across every skill. Replaces the three competing prompt formats currently in the repo (the 4-block lean format, the locked 4-part simple format, and the dense timestamped-block format).

**Engine:** `bytedance/seedance-2-5` on kie.ai. Validated live 2026-08-07.

**Version:** v1, 2026-08-07.

---

## 0. Why the old rulebook has to go

Everything we wrote for Seedance 2.0 was a workaround for two engine failures: identity drifts past roughly 6 to 8 seconds, and the model has no memory across an internal cut. Every rule we built followed from those two facts:

| 2.0 rule | The failure it worked around |
|---|---|
| One prompt = one shot | No cross-cut memory |
| Cap talking shots at 6 to 8s | Face drift |
| Re-declare identity and negatives in every prompt | Each gen was independent |
| Cut in ffmpeg, never in the prompt | Multi-shot ate fidelity |
| Chain from the last frame, or re-seed from one keyframe | Only way to carry a person forward |
| Lay one continuous VO over the assembly | Per-clip native audio restarts at every seam |

2.5 holds character and voice for the full runtime in a single pass. All six workarounds are now dead weight, and each one costs us quality: chaining inherits drift, per-shot re-declaration burns tokens on repetition, and ffmpeg cuts can't do a real match cut.

**The unit of authorship moves from the shot to the ad.** One prompt now describes an entire 15 to 30 second creative, cuts included.

What does not change, because these are content laws and not engine laws: product truth blocks, the anti-3D-render law, the no-invented-support-surface law, the creator-never-speaks-as-brand law, no product in the first TOF seconds. Those all survive intact and are wired into the modules below.

The one-take audio law also survives, and 2.5 satisfies it natively. One generation is one continuous recording, so there is no seam to sound like a restart. We no longer need to pre-render a VO and lay it back over an assembly for anything that fits in 30 seconds.

---

## 1. The module stack

Every prompt is the same twelve modules in the same order, across three bands. Content type changes which modules are on and how they're filled. It never changes the order.

Order is load-bearing. Declare-then-delta only works if the declaration comes first, and the model weights early tokens more heavily.

```
BAND A — STATE            declared once, holds for the whole runtime
  1  FORMAT
  2  CAST
  3  WARDROBE
  4  SET
  5  PRODUCT
  6  LOOK
  7  VOICE
  8  SOUND

BAND B — TIMELINE         the deltas
  9  BEATS  (with inline PHASE OVERRIDE where state legitimately changes)

BAND C — GUARDS           closes the loop
  10 CONTINUITY
  11 TEXT
  12 NEGATIVES
```

Band A is the thing 2.0 could never have. Under 2.0 every shot re-declared its own state because every gen was independent. Under 2.5 you state it once and spend the rest of the prompt on what changes.

---

### 1. FORMAT

```
FORMAT: A single continuous 25-second take containing exactly 5 hard cuts, at the
timestamps marked in the timeline below and nowhere else. Real-time pacing throughout.
```

Three laws:

**Declare the cut count.** It gives the model a budget to hold itself to and it costs one clause. Validated: a test declaring "exactly 2 cuts" produced exactly 2, within half a second of the requested timestamps.

**Runtime must match in three places.** The number in FORMAT, the sum of the beat windows, and the `duration` parameter sent to the API all have to be the same integer. Mismatch is the single most common cause of desync: ask for 15 seconds while writing a 21-second timeline and the model compresses everything, so the delivery slides out from under the beats and any captions you cut to it are wrong. Duration is integers only, 4 to 30.

**Do not restate the API parameters in the prompt.** ByteDance's own prompt-engineering guidance is explicit that aspect ratio, resolution, frame rate and the audio on/off switch belong in the request body, not the text, because restating them wastes attention and can contradict the actual call. That is why the block above says "25-second take" and not "25-second vertical 9:16 720p video." The runtime stays in the text because it anchors the timeline; everything else goes in the payload.

---

### 2. CAST

**When a reference image is wired, this is a pointer, not a portrait.**

```
CAST: The woman in @Image1. Do not restyle her, do not change her age or face shape.
She reads late twenties. Roughly 5'6", so the tote sits at mid-thigh when carried.
```

Describe only what the reference can't carry: age read, height relative to the product, build. Re-describing a face that's already in a reference makes the model re-render it from text, and the text version wins over the image. That's the fastest way to lose the ref.

Text-only casting, when there's no reference: 25 to 40 words, durable traits only. Bone structure, hair length and color and texture, skin tone, eye color, distinguishing marks. Expression and pose are beat-level, not cast-level.

Multiple people: number them `SUBJECT A` and `SUBJECT B` and use those exact tokens in every beat. Never write "the other woman," which is where cast swaps come from.

---

### 3. WARDROBE

Its own slot rather than part of CAST, because outfit is the second thing to drift after the face and the first thing a viewer consciously notices.

```
WARDROBE (identical in every beat unless a PHASE OVERRIDE below says otherwise):
cream ribbed knit sweater, sleeves pushed to the elbow, small gold hoop earrings,
thin gold chain, bare hands.
```

Name the jewelry. Earrings and necklaces vanish and reappear across cuts more than any other element, and they're small enough that the model treats them as optional unless you pin them.

15 to 25 words.

---

### 4. SET

```
SET: A bright bedroom corner. Unmade white bed behind her at frame left, one window
camera-right throwing all the light, plain off-white wall. Late morning.
Nothing else in the room. No table, no desk, no visible surfaces.
```

**Hard law, promoted from the existing no-invented-support-surface rule:** never let a beat use a surface, prop, or piece of furniture that SET didn't declare or a reference image doesn't show. If the creator sets the product down anywhere, the surface has to exist in SET first. Otherwise the model invents one, and an invented surface mutates between cuts.

**⚠️ Do not list absent objects here. Naming a thing to forbid it summons it.** This is the best-documented failure in the whole model family: a prompt reading "worker not wearing a hard hat" reliably produces hard hats, because negation is weak grammar wrapped around a strong activation. Our own test wrote `no table, no desk, no visible surfaces` into SET and the output contained a nightstand and a lamp. That is almost certainly cause and effect, not coincidence.

Say the same thing positively instead. Describe the empty surface as a surface:

```
SET: A bright bedroom corner. Unmade white bed behind her at frame left, one window
camera-right throwing all the light, bare off-white wall behind her, clear floor.
Late morning. The room is sparse and uncluttered.
```

"Bare wall, clear floor, sparse and uncluttered" does the work that "no table, no desk" was supposed to do, without putting a table into the model's head. Negation belongs only in the closing NEGATIVES block, where the platform expects it and where it demonstrably works for on-screen text and audio.

25 to 40 words.

---

### 5. PRODUCT

Pointer to the reference plus the product's truth block, pasted verbatim from the product skill.

```
PRODUCT: The bag in @Image2. It is exactly as shown. Do not restyle, recolor, or
re-proportion it. [paste the mandatory mechanism block from the product skill verbatim]
```

**Do not describe the product's appearance when a reference is wired.** Same failure mode as CAST: description overrides the image. Describe only two things: what the reference physically cannot show (how it opens, how it's carried, what's inside), and what must not change.

Two content laws attach here. Product does not appear in the first beat of a TOF creative. And the product's mechanism block is not optional or paraphrasable, it goes in verbatim or the mechanism gets invented.

---

### 6. LOOK

The anti-AI-tell module. Capture medium, lens character, lighting quality, grade.

UGC default:

```
LOOK: Shot on an iPhone front camera, handheld, slightly imperfect framing, mild
sensor noise, natural window light with real falloff. Photographic, not rendered.
No color grading, no cinematic look, no shallow-depth-of-field bokeh, no 3D render
or CGI quality, no plastic skin, no glossy studio product-render sheen.
```

The "photographic, not rendered" sentence and the render negatives are the global anti-3D-render law. They go in every prompt including brand films, where only the first half of the block changes.

LOOK is the one Band A module that can legitimately take a mid-timeline override, and only in the founder profile, where polished b-roll beats cut against phone-shot founder beats on purpose.

---

### 7. VOICE

This module is the whole reason 2.5 matters for us. Under 2.0 we cast a voice in segment 1, saved that audio, and passed it as an anchor to every subsequent segment, and it still shifted. Under 2.5 you describe the voice once and it holds for the full runtime.

```
VOICE: Mid-twenties American woman, light vocal fry, conversational and slightly
rushed, the way you talk when you're telling a friend something. Close phone-mic
sound, a little boomy, no studio polish, no announcer energy.
```

20 to 30 words. One VOICE block per SUBJECT when there's more than one speaker.

ByteDance's documented casting formula is **gender + age range + voice attributes + speaking rate + emotional baseline**, in that order, which is what the example above follows. Two rules from their docs worth obeying: name the language explicitly when the line is not in the model's default (`speaking in English, {...}`), and do **not** invent an accent the brief didn't ask for, because "American woman" and "American woman with a Southern accent" are different castings and the model will take whatever you give it.

If the voice drifts mid-take, their documented fix is to make the timbre description more specific rather than to repeat the instruction.

**Always close VOICE with the no-narrator lock**, verbatim from a team who traced invented narration back to its absence:

```
There is no narrator and no voiceover. Only the person visible on screen speaks,
and her lips move when she does.
```

Without it, clips occasionally grow spontaneous narration, and silent beats grow speech. It costs one sentence.

**Two more voice facts worth knowing before they cost you a run.** The model **infers a voice from the character reference image**, so a creator reference silently dictates accent before your text gets a say. And accent wording is brittle: a documented case had "American English" pull delivery back toward British because the word "English" dragged it there, where plain "American" held. If an accent comes out wrong, change the wording rather than repeating it.

**Multi-speaker warning for P6.** A single audio reference is applied to **every** speaker in the shot; the model does not map voice references to characters. A two-speaker shot with one reference gave both characters the same voice. Either keep one speaker per beat, which the profile already requires, or accept a shared voice.

Dialogue content law, enforced at the beat level but stated here: the creator never speaks as the brand. "They're running a sale," never "our sale." First person plural reads as paid.

---

### 8. SOUND

```
SOUND: Ambient room tone only. No music, no BGM. No narration layered over her
dialogue. <soft fabric rustle> where she handles the bag, nothing else.
```

"No music" is close to always correct. If a trending sound goes on in post, generated music fights it. If the piece needs a bed, it's cheaper and more controllable to add it in the edit.

**Use ByteDance's documented bracket system.** These are real parsed delimiters, not decoration, and they are the most reliable way to keep the three audio layers from bleeding into each other:

| Layer | Delimiter | Example |
|---|---|---|
| Music / BGM | `( )` | `(soft lo-fi piano under the whole take)` |
| Sound effect | `< >` | `<zipper>` · `<footsteps on tile>` |
| Spoken dialogue | `{ }` | `{It's one piece, it folds over.}` |
| Burned subtitle | `【 】` | avoid entirely, we burn text in post |

Two cautions. If you use `< >` for SFX, do not also wrap subject names in angle brackets anywhere in the prompt; the parser collides. And audio is the one area where negatives genuinely work: ByteDance documents that **only subtitles and audio are reliably negatable**, so `no BGM, ambient and action sound only` is a real instruction while `no invented furniture` is only a nudge.

Dialogue may be written either in `{ }` or in plain double quotes. Both are attested in ByteDance's own examples. This spec uses double quotes in the DIALOGUE field because it keeps the timeline readable, and `{ }` when a line needs to be unambiguously separated from surrounding description.

---

### 9. BEATS

The timeline. Every beat is the same five-field block.

```
[00:00–00:04]  SHOT 1. OPEN.
  FRAME: chest-up, front camera held at arm's length, she's centered
  ACTION: she leans in slightly, one hand comes up into frame
  DIALOGUE: "Okay so I figured out why my bag kept doing this."

[00:04–00:09]  SHOT 2. JUMP CUT.
  FRAME: same setup, framing a touch wider
  ACTION: she turns the bag toward the lens and taps the front panel twice
  DIALOGUE: "It's the flap. It folds all the way over, one piece."
```

**Cut execution: VALIDATED 2026-08-07.** A 10-second three-beat test (task `53e9e54d5585a245b77955777ef494c4`) declared "exactly 2 cuts" with beats at 00:04 and 00:07. The output contained **exactly 2 hard cuts, at 3.625s and 6.958s** (scene scores 0.396 and 0.351). Runtime landed at 10.08s against a declared 10s. Beat content executed precisely: chest-up talking, then hands-only tight on the bag with no face, then back to chest-up. Identity, wardrobe, room, light direction and product geometry all held with no drift, and the footage reads as genuinely photographic.

So the timeline controls both *what is on screen when* and *where the cuts land*, to within about half a second.

> **Measurement warning, learned the hard way.** An earlier pass concluded there were zero cuts. That was a broken ffmpeg invocation, not model behavior: `showinfo` logs at INFO level, so pairing it with `-v error` prints nothing and every video looks like one continuous take. Detect cuts with `-vf "select='gt(scene,0.25)',metadata=print:file=-"` and read **stdout**, which is what `_engine/tools/seedance_adapt.py` now does. Never conclude "no cuts" from a `showinfo` command that also passes `-v error`.

Two smaller violations in the same test: a ring appeared despite `no rings` in WARDROBE, and a nightstand and lamp appeared despite SET declaring `no table, no desk, no visible surfaces`. Both are the summoning effect described under SET: naming an object in order to forbid it puts the object in the model's head. ByteDance's docs independently say only **subtitles and audio** negate reliably. So state what *is* in the frame, and keep negation in the closing NEGATIVES block.

**CUT vocabulary, pick exactly one per beat:**

Header format is `[MM:SS–MM:SS] SHOT n. <CUT TYPE>.` This mirrors ByteDance's own documented notation, which numbers shots (`镜头 N` / `Shot N`) and marks cuts with an explicit `硬切` / HARD CUT token. Two things they document that matter here: **2.5 responds to whole-second timestamps and 2.0 does not**, so the timestamped form is a 2.5-only capability; and the timeline must have **no gaps**, which the linter enforces.

| Cut type | Use |
|---|---|
| `OPEN` | First beat only |
| `JUMP CUT` | Same setup, time skips forward. The UGC-native cut, and your default inside a talking sequence |
| `HARD CUT` | Instant change of framing or location, same world. Use for inserts and scene changes |
| `MATCH CUT` | Same composition, contents change. The only genuinely new capability 2.5 offers over ffmpeg |
| `CONTINUOUS` | No cut. Flows from the previous beat. Use to split a long action into directable chunks without spending a cut from the budget |

Do not write "Cut to:". It appears nowhere in ByteDance's documentation and is third-party folklore. Do not write "lens switch" either; it is a mistranslation of 切镜.

> **⚠️ Trap: most Seedance guidance you will find online forbids timestamps, and it is all about 2.0.** ByteDance's 2.0 prompt guide and their `sd2-pe` optimizer skill both state flatly that shot order takes priority over absolute time and that writing `0-3s` is forbidden, because 2.0's support for precise timing is unstable. That is true, and it is 2.0-scoped. Their 2.5 documentation says the opposite in as many words: **2.0 does not respond to timestamps and only responds to shot numbers, while 2.5 responds to whole-second timestamps.** Their own 2.5 examples use the fused form this spec uses, `镜头 1 [0:00–0:03]`. Our validated run was on 2.5 with timestamps and it cut where it was told.
>
> So: **timestamps on 2.5, shot numbers alone on 2.0.** If someone reads a 2.0 guide and "corrects" our headers by stripping the timestamps, they will have removed the mechanism that makes the timeline binding. The one piece of that advice which does carry over is the warning against mixing two competing timing systems: never put a timestamped timeline and an audio-as-clock instruction in the same prompt, because then nothing knows which clock to follow.

Banned: whip pan, zoom transition, crossfade, dissolve, speed ramp. Every one of them reads agency-produced and kills the UGC illusion.

**FRAME:** shot size, camera position, and at most one camera move. Two moves in one beat still produces jitter, that rule survives from 2.0 unchanged. The eight primitives are still the vocabulary: slow dolly in, slow dolly out, pan left/right, tracking on hands, slow orbit, overhead, handheld, locked off. Never orbit a product, it scrambles labels and hardware.

> **⚠️ For a locked-off talking head, framing is STATE, not a per-beat delta. Measured 2026-08-09.** Writing casual reframes into successive beats ("same setup, a touch wider", "slightly tighter") is read as an instruction to recompose at every cut, and the subject visibly jumps around the frame between shots. Brooks rejected a 4-pass ad for exactly this. The fix is a CAMERA block in Band A declaring one locked shot with the subject centered, a fixed head height and a fixed gap above the hair, then `FRAME: the locked shot, unchanged.` verbatim in every beat, an answering CONTINUITY line pinning position and scale, and `no zoom` in NEGATIVES.
>
> A/B on 16s renders differing only in this grammar, measuring the subject's shoulder line across frames: **vertical position spread 133 px with per-beat deltas versus 1 px with the locked block**, horizontal centroid 15.1 px versus 8.0 px. Only vary FRAME across beats when a reframe is a deliberate creative beat, and then say what the new framing is rather than nudging it.

**ACTION:** concrete physical verbs tied to a body part or the product. Picks up, lifts, tilts, unzips, folds back, slides the strap on, sets down, turns, glances, nods. The model still fudges "uses," "showcases," "interacts with," "experiences." Also survives from 2.0 unchanged.

**Describe behavior, not emotion.** This is the same rule one level deeper, and it is the most common reason a performance comes back flat. Emotional labels get rendered as a neutral face: a team documented the model defaulting to a blank expression on "cheerfully arguing" and "playfully bickering." Say what the face is physically doing. Not "she's excited" but "she's grinning, eyebrows up, mouth open mid-laugh." Not "she looks skeptical" but "one eyebrow lifts and her head tilts back slightly."

**One action per beat.** Two verbs in one beat blend into mush. If the beat needs a lift and a turn and a point, it is three beats or it is one beat with one verb.

**DIALOGUE:** verbatim, in quotes. If a beat has no speech, say so explicitly: `DIALOGUE: (none, natural breath)`. An unmarked silent beat gets filled with invented speech.

**Beat length by role:**

| Beat type | Length |
|---|---|
| Hook (beat 1), visual only | 1.5 to 3s |
| Hook (beat 1), spoken | 3 to 5s |
| Talking | 3 to 7s |
| Product or hands insert | 2 to 4s |
| Lifestyle, walking, environment | 3 to 6s |
| Close / CTA | 2 to 4s |

Above 7 seconds on a talking beat the viewer wants a cut whether or not the model can hold it. Below 3 seconds the line clips.

A spoken hook is governed by word density, not by the cut rhythm you want. At the 2.8 words per second target, 3 seconds buys you 8 words and 4 seconds buys you 11. If the hook line won't fit, cut the line, never stretch the beat past 5 seconds.

**Cut budget: one cut per 3.5 to 5 seconds, and treat 6 shots as the working ceiling.**

There is a genuine disagreement in the sources here, so know where the risk sits. ByteDance's own documentation ships a 9-shot, 30-second example and a storyboard guide that goes to 15 panels. Practitioners who have actually run volume report degradation much earlier: one reports 5 shots as the reliable limit with compression and dropped shots beyond it, another caps at 2 or 3 and says subject consistency falls apart past 5. Our own validated run was 3 shots and clean.

So: **5 to 6 shots (4 to 5 cuts) is the safe zone for a 25-second piece.** Go to 7 or more only after you've confirmed it holds for your setup, and check specifically for dropped shots, because the failure mode is the model silently skipping a beat rather than producing anything obviously broken. Under 4 cuts in 25 seconds reads like a webinar.

**A note on the platforms disagreeing with each other.** Several 2.5 hosts now tell you to "plan for one continuous 30-second shot" and to write a continuous action arc rather than cuts, and ByteDance's consumer product teaches the same. That guidance is about what the model is *best* at, not what it *can* do. Our own test cut on command, twice, within half a second of the requested timestamps. Explicit shot labels plus a cut marker produce real cuts. Bare timestamps with no shot labels only pace beats inside one continuous take, which is very likely what the "one continuous shot" advice is really describing.

**Dialogue density: write to 2.8 words per second, hard ceiling 3.2.** The repo's existing `WORDS_PER_SEC = 4.2` constants are far too fast and are listed in the retrofit table in section 5.

**Size the beat to the line. Do not leave slack, and do not overstuff.** Both directions fail, and they fail differently:

- **Over-filled**, the model speed-reads. It does not truncate, it crams, and you get an unnaturally fast delivery that you can hear immediately and reject.
- **Under-filled is the more dangerous one, and it is why the old "underfill on purpose" advice in this document was wrong.** Given empty time, the model invents something to fill it. A production team running roughly ten films on this engine documented a silent render that **grew a spoken line out of a stage direction**, and they now transcribe every silent clip to check. Under-filled beats also invent filler hand motion, which is where warped hands come from.

The mitigation is already in the beat spec and it is not optional: mark every silent beat `DIALOGUE: (none, natural breath)`, and put the no-narrator clause in VOICE.

**Know that there are two different budgets, and lip-sync is the tighter one.** What fits acoustically at a natural speaking pace is roughly 2.5 to 2.8 words per second. What stays reliably *lip-synced* is reported at around 1.1 to 1.3 words per second in English, or 5 to 10 words per line, which would make a 6-second beat hold 7 or 8 words rather than 16. That number comes from two independent source families and is the single most confident figure in the research.

Our own validated run sat at 2.75 words per second and the frames looked right, **but I checked frames, not audio, so that run is not evidence that lip-sync holds at 2.8.** Treat 2.8 as the working target because it is what our timeline math and the acoustic budget support, and treat 1.3 as the number to fall back toward the moment sync looks soft. **The lever is always fewer words, never more duration.** The safest unit is one short sentence, one idea, one breath.

Everything else that helps sync is a framing decision: keep the camera locked to a medium close-up while a line runs, no head turn, no walking, hands still, and no music or SFX competing under the dialogue.

**PHASE OVERRIDE** goes inline in a beat, and only when a Band A value legitimately changes:

```
[00:12–00:18]  SHOT 4. HARD CUT.
  OVERRIDE — WARDROBE: black wool coat over the same cream sweater. Same earrings.
  OVERRIDE — SET: sidewalk outside a coffee shop, overcast daylight.
  Everything in CAST, PRODUCT, LOOK, and VOICE is unchanged.
  FRAME: ...
```

An override must name what changed and assert what didn't. Overrides leak. Change the location and the outfit drifts with it. Change the body and the hair color goes. Every override needs a matching line in CONTINUITY.

---

### 10. CONTINUITY

The module 2.0 never needed, because under 2.0 every shot was independently locked to its own reference. Under 2.5 the model has to hold itself consistent across its own internal cuts, and this is where you make it.

```
CONTINUITY: The same person in every beat. Identical face, hair color, hair length,
skin tone, and eye color from the first frame to the last. Same wardrobe and same
jewelry in every beat except where a PHASE OVERRIDE states otherwise. Same room, same
light direction, same time of day. One voice throughout, one person in one recording
session, no shift in pitch or accent at any cut. The bag is identical in every beat it
appears in, same color, same hardware, same proportions.
```

**The law: every PHASE OVERRIDE gets an answering CONTINUITY line that names what the override must not drag along with it.** Change the body, pin the hair. Change the location, pin the outfit. Change the outfit, pin the face and the jewelry. This is the highest-leverage single line in the whole prompt and it's the one thing a 2.0-trained prompter will forget, because 2.0 never gave you an internal cut to leak across.

---

### 11. TEXT

```
TEXT: No on-screen text, no captions, no subtitles, no watermarks, no rendered logos.
```

Default is off, always. Seedance garbles brand names (it cannot spell "Weekender"), and hooks and captions belong in post where they stay editable and can be A/B tested without a regeneration.

Turn it on only when text is a diegetic prop, a phone screen or a price tag in frame. Keep it under two words even then, and plan to fix it in post.

---

### 12. NEGATIVES

Short and specific. Long negative lists dilute, each additional negative gets less weight.

```
NEGATIVES: no slow motion, no speed ramps, no cinematic color grading, no 3D render or
CGI look, no plastic skin, no extra fingers, no warped hands, no morphing between cuts,
no extra people entering frame, no invented props or furniture.
```

Anything product-specific that must not happen goes in PRODUCT, not here, so it sits next to the thing it governs.

**Which negations actually fire.** The split is principled, and it explains why our SET negatives failed while these work. Negation works for **global render properties and for people**, and backfires for **objects and props**:

| Negate | Works? |
|---|---|
| `no music`, `no on-screen text`, `no subtitles`, `no watermark`, `no logo` | Yes, reliably. ByteDance says so and every source agrees |
| `no slow motion`, `no cuts`, `no zoom` | Yes |
| `no other people, no onlookers` | Yes, tested and confirmed as a fix |
| `no table`, `no rings`, `no extra props` | **No. Summons them.** Describe the space positively instead |
| `no blur`, `no extra fingers`, `no warped hands` | **No.** Lock the positive: "hands rest still and fully in frame" |

**Crowd creep, and the law that generalizes from it.** Dialogue scenes regenerate with extra onlookers unless you say so explicitly. The working line is `the location is otherwise completely empty, no other people, no onlookers`. The part that matters for us is what a production team found next: **a start frame with the people edited out did not stop the model re-adding them. The ban has to live in the video prompt.**

That directly extends our no-invented-support-surface law. Cleaning the reference image is necessary and not sufficient. If a surface, prop or person must not exist, say so in the prompt, and for objects say it by describing what is there instead.

**Keep the list short for a second reason.** Long negation stacks measurably raise the moderation-rejection rate, because the filter reads the prose. One team traced a persistent rejection to the phrase "still no pants," which passed once they deleted it and left only the positive wardrobe description.

---

## 2. Content profiles

A profile is a module configuration. Skills become thin profile selections over this spec rather than carrying their own prompt formats.

| # | Profile | Runtime | Cuts | Modules off | Beat mix | Mandatory guard |
|---|---|---|---|---|---|---|
| P1 | Talking-head UGC | 15 to 30s | 4 to 6, all jump cuts | PRODUCT | hook 2s, then 4 to 6s talking, close 3s | face + wardrobe + room |
| P2 | UGC demo (talk → show → talk) | 20 to 30s | 5 to 7, alternating jump/hard | none | talking 4 to 6s, inserts 2 to 4s | + product fidelity |
| P3 | POV trend | 15 to 25s | 5 to 8, hard | VOICE, and CAST to hands only | 2 to 4s throughout | set-per-beat continuity |
| P4 | Transformation / before-after | 8 to 20s | 1 to 3, hard, on phase boundaries | often VOICE | phase A then phase B | one CONTINUITY line per override, no exceptions |
| P5 | Product film / b-roll, no face | 15 to 30s | 5 to 8, hard | CAST, WARDROBE, VOICE | 2 to 4s throughout | product fidelity + set |
| P6 | Street interview / two-hander | 20 to 30s | 6 to 8, on speaker change | none | one speaker per beat, never both | CAST A/B and VOICE A/B pinned separately |
| P7 | Listicle / ranking | 20 to 30s | one per item | none | repeating template per item | wardrobe + set across all items |
| P8 | Founder-to-camera | 20 to 30s | 4 to 6 | none | 2/3 founder beats, 1/3 b-roll | LOOK override on b-roll beats only |

Notes that matter per profile:

**P3, POV trend.** The old 8-second total cap was a 2.0 artifact, not a format truth. A POV concept can now run 25 seconds with 7 internal scene changes in one generation instead of seven generations plus a stitch.

**P4, transformation.** This is the profile that fails without CONTINUITY, and it's the one the reference article got right by accident: their running-app prompt needed a trailing "keep her hair color consistent in both clips" because the body override leaked into hair. Write that line before you generate, not after you see it fail.

**P5, product film.** The biggest cost win. Six b-roll clips used to be six generations plus a stitch. Now it's one.

**P8, founder-to-camera.** The only profile where LOOK takes a mid-timeline override, because the contrast between phone-shot founder and clean product b-roll is the format.

---

## 3. Engine binding (kie.ai)

```
model: bytedance/seedance-2-5
input:
  prompt:                 the full module stack
  duration:               up to 30, must equal the FORMAT runtime and the beat sum
  aspect_ratio:           "9:16"
  resolution:             "720p"
  generate_audio:         true
  reference_image_urls:   up to 9, order maps to @Image1..@ImageN
  reference_video_urls:   up to 3
  reference_audio_urls:   up to 3
```

**Resolution: 480p and 720p only.** 2.5 dropped the 1080p and 4K tiers that 2.0 offered. 720p is the default and the only sensible choice for feed. If someone asks for a 1080p Seedance master, the answer is that the model does not produce one; upscale after the fact.

**Native limits vs the kie wrapper.** ByteDance's own API allows 2.5 far more references than 2.0 did: **30 images, 10 videos, 10 audio files, 50 assets total**, against 2.0's 9 / 3 / 3. The kie schema we call through was written for 2.0's limits, so treat 9 images as the working ceiling until a run proves otherwise, and test before designing a pipeline that needs more. In any case ByteDance explicitly advises against filling the cap, because too many assets make it hard for the model to rank which features matter. Their recommended production loadout is **4 to 5 assets**: one or two character images, one set image, optionally one motion-reference video and one audio file. That matches what we would have used anyway.

**⚠️ Reference images may not contain real human faces.** ByteDance blocks real-face reference uploads on both 2.5 and 2.0. The sanctioned inputs are their preset virtual-portrait library, licensed portrait assets, or **prior Seedance outputs from your own account within the last 30 days**. This has a direct operational consequence for us: the current practice of handing a Pinterest photo in as the creator reference is not a supported path. The workable pattern is to generate the creator once, then reuse that generated frame as the identity reference for every subsequent run inside the 30-day window. Worth testing on kie specifically, since kie may or may not enforce the same check.

**⚠️ Prompt keywords silently reroute the task.** 2.5 decides between generation, editing and extension from the prompt text, not from a parameter. Words like "add," "remove," "change," "replace" fire the **editing** path, and "extend" or "continue" fires the **extension** path. Editing mode force-locks `duration` to `-1`. So a beat that innocently says "she adds a scarf" can push the whole job into edit mode. Prefer "she puts on a scarf." This is a real authoring hazard the linter should eventually check for.

**Prompt length: target under 600 English words, hard-plan against 4000 characters.** ByteDance's guide says 1000 English words, Replicate's schema enforces 4000 characters on 2.0 and passes along a BytePlus recommendation of 600 words, and Runware allows 10,000 characters. Design to the tightest credible number, which is 600 words. The stated failure mode past the limit is not an error, it is dilution: the model attends to the headline instructions and quietly drops details, so elements go missing from the video. They also warn specifically against pasting a whole script as the prompt.

**Budget carefully, because we are close to the line.** The worked example in section 7 measures 601 words with a placeholder in the PRODUCT slot. A real product mechanism block, pasted verbatim as the law requires, adds 40 to 80 words on top. So a full production prompt lands around 650 to 700 words and is already past the conservative target. The places to buy the words back, in order: trim NEGATIVES to the four that matter for the piece, since long negative lists dilute anyway and only subtitles and audio negate reliably; shorten SET once a reference image carries the room; and cut CONTINUITY down to the attributes an override actually threatens. Do not buy words back by trimming the PRODUCT block or the timeline.

**You can have the first frame AND the references.** `first_frame_url` is mutually exclusive with reference mode at the parameter level; mixing them returns `first/last frame content cannot be mixed with reference media content`. But there is a documented way around it: stay in reference mode and pin the first frame **in the prompt text** instead.

```
@Image1 as the first frame.
```

That buys a start-frame lock without surrendering the reference slots, which removes the tradeoff this section previously said you had to accept. It is documented for 2.0 and unverified on 2.5, so confirm it on the first run that needs it.

**Reference hygiene**, all of it field-reported and cheap to obey:

- **Order is priority.** Put the asset you most need preserved first; that is almost always the face. Their term for it is "important assets go early."
- **Never feed a grid, collage, contact sheet, or character turnaround.** The model reads a collage as a busy scene, and multi-view sheets are a documented cause of identity drift and the twin bug. Use a headshot plus a full-body instead.
- **Never put a verb straight after a reference tag.** Write `the woman in @Image1 walks`, not `@Image1 walks`, because the digit runs into the next token and the binding gets ambiguous.
- **State what each reference does NOT control.** The single best phrasing pattern from the research is a transfer contract: `@Video1 controls side-tracking camera rhythm only; do not transfer performer identity, wardrobe, or background.` Naming what must not transfer is the difference between a reference and a contaminant.
- **A video reference has three sanctioned jobs**: motion, camera movement, and effects. It does not copy an edit. Sources disagree on whether cut cadence transfers at all, and nobody has demonstrated a cut landing at the reference's timecode, so do not plan around it.
- **Don't mix lighting temperatures across a reference pack**, it averages to neutral.

**Doctrine change on references.** For any multi-cut single-pass ad, use reference mode and take the images. A first frame buys you exact control of frame one, which is worth very little in a 25-second piece with six cuts, and it costs you the ability to bind creator, product, and set references at the same time.

Which means: **no keyframes and no chaining for anything that fits in one pass.** The keyframe-first doctrine was correct against chaining under 2.0 and both are now obsolete under 2.5 for pieces at or under 30 seconds. Keyframes stay relevant only for pieces longer than 30 seconds, and for GPT Image 2 product stills that get used as references here.

**⚠️ You cannot dub over a visible mouth, and this constrains the whole VO pipeline.** Practitioner consensus is firm: even speech-to-speech conversion that preserves timing exactly still reads as off-sync on a mouth that is on camera. Post-dubbing works only for faceless shots, off-screen lines, and voiceover over b-roll. For on-camera dialogue the line has to be re-rendered with the right voice, not replaced afterwards.

That is a real limit on the "generate silent, lay ElevenLabs over it" instinct, and it means voices have to be **cast before anything is generated**. One team named retrofitting voices after the clips existed as the single biggest time sink of their first project, and said so twice.

**The inverse path is the highest-value untested lead in this whole document.** Rather than dubbing after, feed the finished ElevenLabs track in as a **reference audio** and let Seedance move the mouth to it, using the model as a lip-sync compiler instead of a voice generator. This is field-reported independently in English and Chinese sources, and the Chinese talking-head recipe is specific: a front half-body character image, a dry vocal track with no music under it, moderate pace, 15 seconds or less, clean mono. If it works on kie it would give us ElevenLabs voice quality with native lip-sync and would reshape how every VO ad gets made.

**Test it before designing around it**, both because kie may not expose an audio reference for 2.5 and because nobody has published a clean result. Related operational note: any shot carrying an audio reference must run on the standard tier, since fast plus audio fails server-side. We ban fast anyway.

**Cost, measured 2026-08-07.** Flat **63 credits per second** at 720p 9:16 with audio, confirmed on three runs: 5s cost 315, 15s cost 945, 25s cost 1575. At roughly $0.004 per credit that is about $0.25 per second, so a 25-second ad costs about $6.30 and a 30-second about $7.56.

**Pre-auth equals the actual cost.** Unlike Seedance 2.0, which demanded roughly 3x the real price up front, 2.5 reserves exactly what it charges: a 25s task was accepted at a 1619 balance (needing 1575) and a 30s task was refused (needing 1890). Budget exactly `63 × duration` clear before firing. Auto top-up is on, but createTask does hard-reject on an insufficient balance, so batch runners should check the balance before each fire rather than assume the refill beats the request.

**Cost against 2.0.** 2.0 ran 41 credits per second, so per finished second 2.5 is about 54% more expensive. The comparison flatters 2.0 more than it should. A 25-second multi-scene piece under 2.0 was two or more generations plus a GPT Image 2 keyframe for each scene, plus the regenerations that drift and seam failures forced, plus a stitch. Single-pass is close to break-even on anything with more than two scenes, and it wins outright once you count the regenerations you no longer run.

`fast` variants remain banned (distortion).

---

## 4. QA and the retry ladder

Frame QA still runs at 3 to 4 fps, not 1 fps. Single-pass adds five checks that per-shot generation never needed:

1. Cut count in the output matches the count declared in FORMAT.
2. No cast swap at any cut. Check the frame immediately before and immediately after every cut.
3. Wardrobe and jewelry consistent across every cut.
4. Dialogue lands inside its declared beat window. More than 0.5s of drift means the timeline was overfull.
5. No surface, prop, or piece of furniture appears that SET didn't declare.

**Before the ladder: fix it with the cheapest tool that works, and know that retakes regress.**

The most useful economic finding in the research is that **a retake reliably fixes the flaw you named and breaks something you didn't** — a voice, a face, the camera, an extra person wandering in. A team running roughly ten films on this engine reverted two native retakes back to dubs on exactly that basis, and their rule is: if a take is 95% there, trim it, patch it, or live with it. A slightly awkward patch of a good take usually beats a native retake.

Their cost ordering, which holds for us too: an edit-side trim is free, an audio patch is trivial, a regenerated still is a few credits, and a full retake is the whole clip. At 63 credits per second a 25-second retake is 1575 credits, so a re-roll is never the first move.

Corollary worth internalizing: **failures are partly roll luck.** One documented prompt failed five times and then passed verbatim on the sixth. Change one variable per retake, and after two or three failed rewordings stop rewording and change what actually happens in the shot.

**Retry ladder, in order. Do not skip to step 4.**

1. Tighten CONTINUITY, naming the exact attribute that leaked. Fixes most drift failures.
2. Drop the cut count by one. Fixes "the model lost the thread."
3. Cut dialogue words, not add duration. Fixes desync.
4. Split into two generations of 15s that share a byte-identical Band A block, then hard cut between them. Last resort, and it costs you the seamless native audio.

---

## 5. Retrofit map

**Do not do this as a blanket find-and-replace.** The caps have to become **per-engine**, not globally raised. `bytedance/seedance-2` still hard-caps at 15 seconds, so raising `MAX_GEN_SECONDS` to 30 in `scene_replicator.py` would send 2.0 jobs a duration the API rejects. The same applies to the word-rate constants: 2.8 words per second is right for 2.5's single-pass timeline and the existing 4.2 was always wrong, but changing it silently re-chunks every script in the older pipelines. Gate both on the engine, and re-run one known-good job per skill before trusting the change.

Hard numeric caps in code that block a 30-second single pass:

| File | Constant | Current | Target |
|---|---|---|---|
| `_engine/pipelines/scene_replicator.py:123-124` | `MIN_GEN_SECONDS` / `MAX_GEN_SECONDS` | 4 / 15 | 4 / 30 |
| `.claude/skills/pov-trend-factory/scripts/pov_factory.py:39` | `POV_MAX_SECONDS` | 8 | 25 |
| `.claude/skills/omni-ugc/scripts/omni_ugc.py:88` | `ENGINE_MAX_SECONDS["seedance"]` | 15 | 30 |
| `.claude/skills/omni-ugc/scripts/omni_ugc.py:93-104` | `WORD_BUDGET` keys | 5 to 15 only, hard-fails outside | extend to 30 at 2.8 wps |
| `.claude/skills/seedance-directors-cut/scripts/segment_script.py:38` | duration clamp | `min(10, …)` | 30 |
| `.claude/skills/seedance-directors-cut/scripts/segment_script.py:16` | `WORDS_PER_SEC` | 4.2 | 2.8 |
| `.claude/skills/aiugc-longform/scripts/chunk_script.py:38,103-105` | clamp + target/min/max | 10, and 8/5/10 | 30, and 25/15/30 |
| `.claude/skills/aiugc-longform/scripts/chunk_script.py` | `WORDS_PER_SEC` | 4.2 | 2.8 |
| `.claude/skills/seedance-prompt-architect/scripts/detect_cuts.py:88` | `--max` | 15.0 | 30.0 |
| `.claude/skills/aiugc-infinite/scripts/cut2_seedance.sh:11` | Cut 2 default duration | 5 | profile-driven |

Prose-only caps to rewrite: `velantra-ugc/SKILL.md:44,47` (15 to 30s total, 4 to 15s per segment, becomes one segment); `_engine/sops/Segment-Brief-SOP.md:42` vs `:50` vs `:61` (three contradictory caps of 10s, 15s, and 12 to 15s, all replaced by this document); `seedance-prompt-architect/references/seedance-prompting.md:25-31,69-72` (the 4 to 15s range and the explicit ban on multi-shot in one generation, both now reversed).

Three prompt formats get retired and replaced by the module stack: the 4-block lean format (`seedance-prompting.md:15-18`), the locked 4-part simple format (`omni_ugc.py:252-265` and `Segment-Brief-SOP.md:42-47`), and the dense timestamped-block format (`seedance-directors-cut/SKILL.md:110-131`, `velantra-ugc/SKILL.md:76`).

Also unify `seedance-directors-cut`, which currently has two conflicting prompt sites: a dense block in SKILL.md that a human generates from, and a lean one-paragraph template in `render_segment.sh:42-47` that the automated path actually uses.

---

## 6. Replication intake

This is what makes replication fast. A reference breakdown is only useful if it lands in a fixed schema, and the schema is the module stack. Watching a reference and writing prose about it produces something you then have to translate. Watching it against the stack produces something you can fire.

**The split: the reference supplies structure, we supply content.**

| Module | Source when replicating |
|---|---|
| FORMAT | Reference. Runtime and cut count, counted off the actual cuts |
| CAST | Ours. Our creator reference, never the reference video's person |
| WARDROBE | Ours, unless the outfit is doing structural work (a uniform, a gym fit) |
| SET | Ours, matched to the reference's *type* of space, not its specific room |
| PRODUCT | Ours. Verbatim from the product skill |
| LOOK | Reference. Capture medium, lighting quality, grade |
| VOICE | Ours. Our avatar's register |
| SOUND | Reference |
| BEATS | Reference for the rhythm (cut points, beat lengths, shot sizes, what's on screen when). Ours for every word of dialogue |
| CONTINUITY | Derived from our own overrides, not from the reference |
| TEXT / NEGATIVES | Always ours, standing defaults |

Two laws carry over from how we handle swipes generally. **Port the structure, re-derive the content from our avatar**, because a swipe imports its awareness stage along with its beats and our avatar is rarely at the same stage. And **every RTB has to be our feature**, so a reference beat that sells a category benefit gets rewritten to sell the thing our product actually does.

**Extraction prompt** for the watcher pass (`ad-watcher`, `watch`, or a Gemini video pass), which returns the reference half of the table above and nothing else:

```
Break this video down into the following schema and return only this, no prose.

FORMAT: total runtime to the nearest 0.5s. Then the exact number of cuts, and the
timestamp of every cut.

For each beat between cuts, in order:
  window     [MM:SS-MM:SS]
  cut type   how the previous beat ends into this one: hard cut, jump cut (same
             setup, time skips), match cut (same composition, contents change), or
             continuous (no cut)
  frame      shot size and camera position, and any camera move (one only)
  action     the physical action, using concrete verbs tied to a body part
  dialogue   verbatim transcript for this window, with the word count
  on-screen  any burned-in text, verbatim

LOOK: capture medium, lens character, lighting direction and quality, color grade.
SOUND: music, room tone, SFX.
PACING: words per second across the whole piece.

Do not describe the person, their clothes, the room, or the product. I am replacing
all of those.
```

That last line matters. A watcher left unconstrained spends most of its output describing a creator and a product we are about to throw away, and worse, that description tends to leak into the generation prompt and fight our own references.

Once the reference half is in the schema, filling our half is mechanical, and the linter tells you whether the result is fireable before you spend a credit.

---

## 7. Worked example

Profile P2, UGC demo, 25 seconds, 6 cuts.

```
FORMAT: One continuous 25-second vertical 9:16 video, real-time pacing throughout.
Contains exactly 5 cuts, at the timestamps marked in the timeline below. No other cuts.

CAST: The woman in @Image1. Do not restyle her, do not change her age or face shape.
She reads late twenties. Roughly 5'6".

WARDROBE (identical in every beat unless a PHASE OVERRIDE says otherwise): cream ribbed
knit sweater, sleeves pushed to the elbow, small gold hoop earrings, bare hands.

SET: A bright bedroom corner. Unmade white bed behind her at frame left, one window
camera-right throwing all the light, bare off-white wall behind her, clear floor.
Late morning. The room is sparse and uncluttered.

PRODUCT: The bag in @Image2. It is exactly as shown. Do not restyle, recolor, or
re-proportion it. [product skill's mandatory mechanism block, verbatim]

LOOK: Shot on an iPhone front camera, handheld, slightly imperfect framing, mild sensor
noise, natural window light with real falloff. Photographic, not rendered. No color
grading, no cinematic look, no shallow-depth-of-field bokeh, no 3D render or CGI quality,
no plastic skin, no glossy studio product-render sheen.

VOICE: Mid-twenties American woman, light vocal fry, conversational and slightly rushed,
the way you talk when you're telling a friend something. Close phone-mic sound, a little
boomy, no studio polish, no announcer energy.
There is no narrator and no voiceover. Only the person visible on screen speaks,
and her lips move when she does.

SOUND: Ambient room tone only. No music. No narration layered over her dialogue. Natural
sound where the action makes it, nothing else.

TIMELINE

[00:00–00:04]  SHOT 1. OPEN.
  FRAME: chest-up, front camera at arm's length, centered
  ACTION: she leans in slightly, one hand comes up into frame
  DIALOGUE: "Okay I need to talk about tote bags for a second."

[00:04–00:09]  SHOT 2. JUMP CUT.
  FRAME: same setup, slightly wider
  ACTION: she gestures with both hands, shoulders loose
  DIALOGUE: "Every one I've owned, the top gapes open and everything falls out."

[00:09–00:12]  SHOT 3. HARD CUT.
  FRAME: hands only, tight, bag on her lap, no face in frame
  ACTION: both hands fold the front flap all the way over in one motion
  DIALOGUE: (none, natural breath)

[00:12–00:17]  SHOT 4. HARD CUT.
  FRAME: back to chest-up, same setup as beat 2
  ACTION: she holds the bag up beside her face, taps the folded flap twice
  DIALOGUE: "This one's one piece. It just folds over and it stays shut."

[00:17–00:21]  SHOT 5. JUMP CUT.
  FRAME: same setup, she's turned slightly toward the window
  ACTION: she slides the strap onto her shoulder, glances down at it, back up
  DIALOGUE: "Three months in and I've stopped thinking about it."

[00:21–00:25]  SHOT 6. JUMP CUT.
  FRAME: chest-up, centered, closer than beat 5
  ACTION: she shrugs once, small smile, holds eye contact with the lens
  DIALOGUE: "They're running a sale right now so go look."

CONTINUITY: The same person in every beat, identical face, hair and skin from first frame
to last. Same sweater and earrings throughout. Same room, same light direction. One voice
throughout, one recording session, no shift in pitch or accent at any cut. The bag is
identical in every beat it appears in.

TEXT: No on-screen text, no captions, no subtitles, no watermarks, no rendered logos.

NEGATIVES: no slow motion, no speed ramps, no cinematic color grading, no 3D render or
CGI look, no plastic skin, no extra fingers, no warped hands, no morphing between cuts,
no extra people entering frame, no invented props or furniture.
```

Check it against the spec: FORMAT says 25 seconds and 5 cuts, the beats sum to exactly 25 seconds and contain 5 cuts after the open, and the API gets `duration: 25`. No beat exceeds 2.8 words per second. The product does not appear until 00:09. The creator says "they're running a sale," not "our sale."

Lint it before firing:

```
python3 _engine/tools/seedance_prompt_lint.py prompt.txt --duration 25 --profile P2
```

The linter enforces the mechanical laws in this document: module presence and order, the three-way runtime match, the declared cut budget against the actual cut count, per-beat word density, banned transitions, abstract verbs, the brand-first-person check, and whether every PHASE OVERRIDE has an answering CONTINUITY carve-out. It also prints the credit pre-auth the run needs. Errors block, warnings don't.

---

## 8. Appendix: the official grammar this maps onto

Researched 2026-08-07 from ByteDance / Volcengine first-party documentation. Recorded so nobody has to re-derive it, and so the choices above can be checked rather than trusted.

**ByteDance ships an installable prompt-engineering skill for 2.5.** Worth pulling down before any deep work:

```
npx --yes skills@latest add "https://arkdocs.tos-cn-beijing.volces.com/skills/" --skill sd25-pe --yes
```

**Their prompt formula for 2.5:** subject + action/event + scene and environment + visual style + camera move/cut + audio. Note that style comes *before* camera and audio is last. Our module stack is that formula expanded and reordered so the persistent state is declared once up front, which is the thing 2.5 makes possible and 2.0 did not.

**Their document skeleton for a structured prompt:** asset references first (numbered by upload order, each with a stated job), then a one-line summary, then the shot-by-shot body, then a closing block of things that run throughout. Bands A, B and C are the same idea.

**Shot notation.** `镜头 N` is the documented shot marker, and `Shot N` is explicitly recognized in English. Cuts are marked with `硬切` / HARD CUT, which appears in their own example prompts. Attested header forms include `镜头 1 [0:00–0:03]`, `镜头 1 (0-3s):` and bare `镜头 1：`. The timeline must be gapless.

**Subject binding.** Their recommended sentence is "define the [2 to 3 stable visual traits] person in image N as subject N," after which you reuse that label everywhere. One subject per line; never compress two subjects and two images into one range sentence. They also recommend an explicit block listing any uploaded assets that are *not* being used, so stray references cannot leak in.

**Their anti-twin constraint**, which is worth appending verbatim whenever more than one person is in frame: no two people identical in appearance, clothing or accessories, no duplicated or twin characters, only one instance of each character in a frame.

**Camera vocabulary** they say you can write directly, no explanation needed: the shot sizes from extreme wide through close-up; push, pull, pan, track, follow, orbit, crane down, pull back, tilt up, handheld shake; low angle, overhead, first person. Named moves like one-take, Hitchcock zoom, aerial, FPV, bullet time also parse directly. Anything more obscure has to be written as term plus a plain description of what changes. Their single most repeated constraint is the one we already had: **one camera move per shot.**

**Where we deliberately diverge.** They allow up to 9 shots in 30 seconds; we cap at 6 because practitioner reports of dropped shots are more consistent than their example. They permit long prompts; we target 600 words. Their guidance increasingly frames 2.5 as a continuous-take model; our own test cut on command, so we use cuts where the creative wants them.

Primary sources: Volcengine docs 2607689 (2.5 prompt guide), 2607688 (2.5 tutorial), 2222480 (2.0 prompt guide), 2168087 (1.5 pro, origin of the audio bracket grammar), 1520757 (video generation API schema).
