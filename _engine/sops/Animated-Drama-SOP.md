# Animated Drama SOP — long-form story ads on Seedance 2.5

**Status:** canonical 2026-08-16. Profile **P6-DRAMA**, an extension of `Seedance-Prompt-System.md`. Read that first; this document only covers what changes when the piece is a 2-3 minute multi-character animated story instead of a 25-second UGC clip.

**Worked build:** `brands/wend/creative/WEND-DOOR-ANIM-01/`
**Reference class:** `brands/wend/swipe/resilia-shame-drama/ANATOMY.md`

---

## 0. Why not Kling 3

Kling is the right tool for a 5-second animated beat. It is the wrong tool for this format, and the reason is arithmetic, not taste.

| | Kling 3 | Seedance 2.5 |
|---|---|---|
| A 160s ad with ~35 cuts | 32+ generations (5s reliable ceiling, per CONF-ANIM-01) | **7 generations** |
| Keyframes to author | one per clip, 32+ | one cast sheet, reused |
| Dialogue | silent → ElevenLabs → **you cannot dub a visible mouth** | native, lip-synced, per character |
| Two people talking to each other | not a thing it does | one speaker per beat, turn-taking |
| Continuity across a cut | none, every clip is independent | Band A state holds across the pass |
| Assembly | 32-clip stitch, drift at every seam | 7 hard cuts |

The killer is the third row. A drama is 100% dialogue, and post-dubbing an on-camera mouth reads off-sync no matter how good the voice is. Seedance 2.5 generates the performance and the audio in the same pass, which is why the whole format is only affordable on this model.

**What Seedance 2.5 costs you in exchange:** 30-second hard cap per pass, 720p ceiling, and continuity between passes becomes your job instead of the model's. That is what sections 2 and 3 exist for.

---

## 1. The unit of work is the ACT, not the shot

This is the mistake to fix first. An editor who has been cutting Kling clips will open the reference and start listing 35 shots. Wrong altitude.

**One act = one dramatic situation, one location, one turn = one Seedance pass, 16-30 seconds, 4-6 shots, 3-5 internal cuts.**

Watch the reference and write down only the acts. A 150-second ad is six or seven of them. Then, and only then, write the beats inside each act.

Never plan a pass longer than 30 seconds — it is the hard `duration` cap. Never plan more than 6 shots in a pass; past that the model silently drops beats.

---

## 2. Lock the cast before you generate a single second

Every character appears in multiple passes, and the model has no memory between passes. The cast sheet is the only thing holding the ad together.

1. Generate each character **once** with GPT Image 2 (10cr each): a clean front-facing 3/4 bust on a plain background, in the animated register, no props, neutral expression.
2. Generate a second full-body frame per character from that first image, so you have height and build.
3. Every subsequent pass wires those same files as `@Image1..@ImageN` in the same order. **Most important character first.**
4. Never feed a turnaround sheet, a grid, or a contact sheet. It causes identity drift and the twin bug.
5. Once Pass 1 renders clean, you may swap in a frame **from your own Seedance output** as the identity reference — it is the highest-fidelity ref available and it is a sanctioned input inside 30 days.

The reference ad skipped this and its lead is visibly two different women by the third act. It still converts. Do it anyway — it costs 20 credits.

**Ban list for the cast sheet:** no logos, no readable text on clothing, no real-person likeness, no branded medical devices.

---

## 3. Band A is written once and pasted verbatim into all seven passes

CAST, WARDROBE, LOOK, VOICE, SOUND and CONTINUITY change **only** where the story genuinely changes them. Everything else is copy-paste. This is what stops the ad from looking like seven different ads.

- **SET** is the module that legitimately changes per pass. Rewrite it per location, positively — describe the surfaces that exist, never list the furniture you don't want. Naming a thing to forbid it summons it.
- **VOICE blocks are per character and never edited between passes.** One character's voice drifting between acts is the single most noticeable seam in this format. If it drifts anyway, make the timbre description *more specific*; do not repeat the instruction.
- **WARDROBE changes on a time jump only**, and every change needs an answering CONTINUITY line naming what the change must not drag with it.

### The look block for this profile

```
LOOK: 3D animated family-film style. Stylized human characters with large
expressive eyes, soft rounded features and subsurface-scattering skin.
Physically based rendering, soft global illumination, gentle depth of field on
close-ups, warm domestic palette. Consistent character modelling, proportion and
shading in every beat.
```

> ⚠️ **This is the one profile where the standing no-3D-render law is inverted.** That law exists to stop photoreal b-roll from reading as CGI. Here the animated register *is* the deliverable — it is what makes a bathroom shame scene shootable and what disarms the "paid actress" filter. Do not paste the photoreal block into an animated pass, and do not reject a frame for looking rendered. Reject it for looking *cheap*: plastic hair, dead eyes, mismatched proportions between beats.
>
> Describe the register. **Never name a studio or a franchise in the prompt** — it is an IP-filter rejection and it does not improve the render.

---

## 3b. Two stages: draw every shot, then animate it

**This is the production path. Text-only passes are the fallback, not the default.**

Stage one: every shot in the script gets a keyframe generated in GPT Image 2, image-to-image off the cast sheet. Composition, staging, wardrobe, set and light are decided as stills, where a bad frame costs 10 credits instead of a whole pass. Stage two: the keyframes for one act go into that act's generation together, wired as `@Image1..@ImageN` in shot order, and the prompt opens with `Use @Image1 through @ImageN in order as the keyframes for the N shots below. Each shot opens on its keyframe and holds that framing.`

Validated end to end (VEL-ELEANOR-ASKME25-01): a 25s / 5-shot / 4-cut pass built this way landed at 25.06s with cuts at 5.00 / 8.92 / 14.08 / 19.38 against 5 / 9 / 14 / 19 requested, and all five lines transcribed back word for word.

**Never chain.** Every keyframe is authored independently from the same cast sheet. Feeding the last frame of one shot as the start of the next drifts identity within ~3 hops, in a direction nobody notices until act four.

**Three variants per shot, then pick.** Judge in order: identity match, staging, proportion consistency across the act, light direction. Light direction is declared per act and repeated in every shot line of that act — it is the continuity error nobody catches in stills and everybody sees in the cut.

**File naming is load-bearing.** `P1-S1`, `P1-S2`, and upload in that order. Upload order *is* `@Image` order.

### The keyframe prompt is four blocks

Three are verbatim boilerplate (STYLE, IDENTITY, GUARDS); only the shot line changes. Full text and a 37-shot worked set: `brands/wend/creative/WEND-DOOR-ANIM-01/01-keyframe-prompts.md`.

The load-bearing sentence lives in the IDENTITY block: *"The attachment supplies identity and wardrobe only. Take the framing, the staging, the set and the lighting from this prompt, not from the attachment."* Without it, i2i inherits the cast sheet's lighting and background and every keyframe comes back looking like the cast sheet.

### Once keyframes are wired, half of Band A collapses

| Module | Text-only | Keyframe mode |
|---|---|---|
| CAST | 25-40 words of durable traits | One line. A pointer. |
| WARDROBE | 15-25 words, jewellery named | "Exactly as shown in the keyframes." |
| SET | 25-40 words, positively described | "Exactly as shown in the keyframes." |
| LOOK | Full render description | "Match the keyframes exactly." |
| VOICE | Full | **Full.** A still cannot carry a voice — this module keeps all its weight. |
| FRAME | Shot size, position, one move | "The keyframe framing, held." Name a move only where you want one. |
| ACTION | What happens in the shot | **What *changes* from the still.** The keyframe is the opening state. |

**Do not re-describe anything a keyframe already shows.** Description of a face or set already in an attached image makes the model re-render it from text, and the text wins — that is how you lose a frame you already paid for. The collapse buys back ~200 words, which is the room the timeline needs.

**Keep FRAME "held" on every beat but one.** One slow move per act, on the beat that matters most. A move on every shot reads agency-produced and it jitters.

Seven worked animation prompts: `brands/wend/creative/WEND-DOOR-ANIM-01/02-animation-prompts.md`.

---

## 4. Writing the beats

Straight from the prompt system, with three additions that only bite on drama:

- **One speaker per beat, always.** Two characters talking inside one beat produces overlap and a shared voice. Turn-taking is a cut.
- **Drama runs slower than UGC.** Target **1.5-2.2 words per second**, not 2.8. The pauses are the performance. But an under-filled beat invents speech, so every quiet beat needs a named physical action to spend the time on and an explicit `DIALOGUE: (none, natural breath)`.
- **Describe behavior, never emotion.** "Devastated" renders as a blank face. "Eyes wet, jaw set, she does not sob" renders as devastated.

Cut types: `HARD CUT` is the default here, not `JUMP CUT` — a drama changes angle and staging at every line. Never write "Cut to:", never write a crossfade or a whip pan.

### Worked example — Pass 1 of WEND-DOOR-ANIM-01, **text-only mode**

*This is the fallback shape, shown so the full module stack is legible in one place. The production version of this same pass, in keyframe mode, is in `02-animation-prompts.md` and is about 200 words shorter.*

```
FORMAT: A single continuous 24-second take containing exactly 5 hard cuts, at the
timestamps marked in the timeline below and nowhere else. Real-time pacing throughout.

CAST: SUBJECT A is the woman in @Image1, called ERIN. SUBJECT B is the man in
@Image2, called MARK. Use these exact tokens in every beat. Do not restyle either
character and do not change face shape, hair or age. Erin reads early forties.
Mark reads mid forties and stands a head taller.

WARDROBE (identical in every beat): ERIN — grey cotton pyjama set, sleeves to the
wrist, hair loose and unbrushed, bare feet. MARK — navy t-shirt, grey sweatpants,
bare feet.

SET: An upstairs hallway with a plain closed bathroom door centred in frame, bare
cream walls, a landing window off-frame right throwing early morning light along
the wall. Beyond the door a small pale bathroom: a white sink with a wide flat
edge, a bathtub behind it, one folded towel on a rail. Both spaces are sparse and tidy.

LOOK: 3D animated family-film style. Stylized human characters with large
expressive eyes, soft rounded features and subsurface-scattering skin. Physically
based rendering, soft global illumination, gentle depth of field on close-ups,
warm domestic palette. Consistent character modelling, proportion and shading in
every beat.

VOICE: SUBJECT A (Erin) — American woman, early forties, low and slightly hoarse,
speaking slowly, tired and holding something back. SUBJECT B (Mark) — American man,
mid forties, warm mid-range, speaking gently and evenly, worried rather than angry.
Both speaking in English. There is no narrator and no voiceover. Only the person
visible on screen speaks, and their lips move when they do.

SOUND: Ambient house tone only. No music, no BGM. <two knuckle knocks on a wood
door> in beat 1, <a tap dripping once> in beat 4. Nothing else.

[00:00–00:04]  SHOT 1. OPEN.
  FRAME: medium, from behind Mark's shoulder, the closed door filling frame right
  ACTION: he knocks twice and leaves his hand on the door frame
  DIALOGUE: "Erin. You've been in there since six."

[00:04–00:08]  SHOT 2. HARD CUT.
  FRAME: medium wide inside the bathroom, low, Erin seated on the closed lid
  ACTION: both her hands grip the flat edge of the sink and her forehead drops
  DIALOGUE: "I'm fine. Just give me a minute."

[00:08–00:12]  SHOT 3. HARD CUT.
  FRAME: medium close on Mark in the hallway, the door edge frame right
  ACTION: his open palm settles flat against the door
  DIALOGUE: "You said that Sunday. And Tuesday."

[00:12–00:17]  SHOT 4. HARD CUT.
  FRAME: close on Erin's face, slightly low
  ACTION: her eyes fill and her jaw sets; she does not sob
  DIALOGUE: "It's been nine days, Mark. Nine."

[00:17–00:21]  SHOT 5. HARD CUT.
  FRAME: close on Mark, profile against the door
  ACTION: he rests his forehead on the wood and closes his eyes
  DIALOGUE: "Then let me in."

[00:21–00:24]  SHOT 6. HARD CUT.
  FRAME: close on Erin, she turns her head toward the door
  ACTION: she looks at the door and does not stand up
  DIALOGUE: "Not like this."

CONTINUITY: The same two people in every beat. Identical faces, hair, skin tone and
eye colour from the first frame to the last. Same wardrobe throughout. Same hallway,
same bathroom, same early-morning light direction, same time of day. The door stays
closed in every beat and neither character opens it. One voice per character with no
shift in pitch or accent at any cut.

TEXT: No on-screen text, no captions, no subtitles, no watermarks, no rendered logos.

NEGATIVES: no music, no slow motion, no zoom, no other people, no onlookers, no
photorealistic live-action look, no morphing between cuts.
```

Payload: `duration: 24`, `aspect_ratio: "9:16"`, `resolution: "720p"`, `generate_audio: true`, `reference_image_urls: [erin_bust, mark_bust]`.

**The three-way runtime match is not optional.** FORMAT says 24, the beats sum to 24, `duration` is 24. Break it and the model compresses the whole performance and every caption you cut to it lands wrong.

---

## 5. Firing and cost

```
model: bytedance/seedance-2-5
duration: 16-30 (integers only)   aspect_ratio: 9:16   resolution: 720p
generate_audio: true              reference_image_urls: 2-4, most important first
```

- urllib SSL fails on this machine. **Shell out to curl** in every kie runner.
- Check `kie_balance` before a batch. Auto top-up is broken; a low balance is a hard stop mid-run, after you have already paid for cast sheets.
- **Budget:** a validated 25s / 5-shot pass ran **1,625cr (~$6.50)**. A 7-pass ad is **~$46**, plus ~$0.40 of cast sheets and **~$4.44 of keyframes** (37 shots × 3 variants × 10cr) = **~$50 clean**; budget **$75-95** with retries. Note where the money is: **stage one is 9% of the budget and it decides 80% of the film.** Spend the variants there, not on retrying passes.
- Fire passes **sequentially with a retry loop**, never in a burst. Failed `createTask` calls are not charged.
- Words that silently reroute the job: "add", "remove", "change", "replace" fire EDIT mode and force `duration: -1`. Write "she puts on", never "she adds".

### Retry ladder — cheapest tool first

1. **Trim** the pass in the edit (free). If a take is 95% there, trim it.
2. **Regenerate one pass**, changing exactly **one** variable.
3. After two failed rewordings, **change what physically happens in the shot** — do not reword a third time.
4. Retakes regress randomly: a retake reliably fixes the named flaw and breaks something else. Keep every take on disk and compare before you ship.

---

## 6. Assembly

- **Hard-cut concat between passes. No crossfades.** Characters animate through a dissolve and you get ghosting.
- Act transitions and time jumps are **title cards in post**, black frame, white type, ~3s. The reference does exactly this ("A FEW WEEKS LATER") and it is free continuity insurance across a wardrobe change.
- **Captions last, and never from the script.** Re-transcribe the assembled audio with ElevenLabs Scribe (`scribe_v1`, word timestamps, `diarize=true`), then build the cards off those timings. Word-highlight style, one keyword per card. This machine's ffmpeg has no libass and no drawtext — render Pillow PNGs and composite with one `overlay` per card gated by `enable='between(t,start,end)'`. Never use the concat demuxer for the caption track; it drifts and rots toward the end of the reel.
- End card: wordmark and domain, in post. Seedance cannot spell a brand name — never ask it to.

---

## 7. QA gate

### Stage one — every keyframe, before anything is animated

| # | Check | Fail = |
|---|---|---|
| K1 | Identity matches the cast sheet — face shape, hair, build | take another variant, never "close enough" |
| K2 | Light direction identical across every shot in the act | regenerate the outlier |
| K3 | Head size and body proportion consistent shot to shot | regenerate; this is what reads as cheap in motion |
| K4 | No text, signage or readable writing in frame | regenerate |
| K5 | Hands whole and in frame, five fingers | take another variant |
| K6 | Any product shot matches the real label file | regenerate against the label attachment |

### Stage two — every animated pass

| # | Check | Fail = |
|---|---|---|
| 0 | Each shot opens on its own keyframe, in the right order | check the upload order before blaming the model |
| 0b | No drift away from the keyframe *inside* a shot — compare the last frame of each beat to its still | shorten the beat, or hold the camera |
| 1 | Runtime within ±0.5s of the declared duration | regenerate |
| 2 | Cut count matches FORMAT, cuts within ~0.5s of the timeline (`select='gt(scene,0.25)',metadata=print:file=-`, read **stdout**) | regenerate |
| 3 | Every scripted line present, word for word, on a Scribe read-back | regenerate |
| 4 | Lip-sync holds on every line — check the audio, not the frames | cut words, never add duration |
| 5 | No invented speech in a silent beat | add the action, re-mark `(none, natural breath)` |
| 6 | Face, hair and wardrobe identical across every internal cut **and against the previous pass** | regenerate against the cast sheet |
| 7 | Voice identical to the same character's previous pass | make the timbre line more specific |
| 8 | No extra people, no invented furniture, no readable text | regenerate |
| 9 | Compliance sheet for the concept, line by line | stop, do not ship |

> **Measurement trap:** `showinfo` logs at INFO level, so `-v error` plus `showinfo` prints nothing and every video looks like one continuous take. Never conclude "no cuts" from that command.

---

## 8. What kills this format

1. Treating shots as the unit instead of acts. Seven generations becomes thirty-five and the budget dies.
2. No cast sheet. The ad becomes seven ads.
2b. Chaining keyframes off each other instead of authoring each from the cast sheet.
2c. Re-describing a face or a set in the animation prompt that the keyframe already shows. The text wins and you lose the frame.
3. Cramming a 30-second act into a 20-second pass. The model speed-reads and you can hear it.
4. Pasting the photoreal anti-CGI block into an animated prompt.
5. Building captions from the script instead of a re-transcription.
6. Naming a studio, a franchise, or a real drug brand anywhere in the prompt.
