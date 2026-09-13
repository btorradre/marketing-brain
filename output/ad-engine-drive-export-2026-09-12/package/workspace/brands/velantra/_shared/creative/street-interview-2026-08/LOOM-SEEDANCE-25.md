# Loom: "How to use Seedance 2.5" — recording script

**For Brooks to record once. Target 13 to 15 minutes. Editors watch this instead of reading process notes in every brief.**

Screen setup before you hit record: this brief open in one tab, the prompts doc in a second, the kie dashboard in a third, and one finished 25-second single-pass ad ready to scrub. Have a prompt that failed on hand too — the failure is the most useful thing in the video.

Each section below has what to show on the left of your attention and what to say on the right. The spoken lines are a script to talk from, not to read.

---

## 0:00 — Cold open (45s)

**Show:** the finished 25-second ad, playing.

> "This is one generation. Not five clips stitched together, not a voiceover laid on top. One prompt, one pass, twenty five seconds, five cuts, and the audio came out of the same generation as the picture. That's what changed, and it's why everything you learned about making these last month is now the slow way to do it."

Scrub to a cut. Point at it.

> "The model cut there because I told it to cut there, at that second. That's the whole trick. You are not writing a shot any more. You are writing an ad."

---

## 0:45 — What actually changed (90s)

**Show:** nothing, or a two-column slide.

> "Old way: every shot was its own generation, because the model lost the person's face after about six seconds and had no memory across a cut. So we generated a still for every scene, animated each one, and stitched. Every seam was a place it could go wrong, and the voice shifted every time."
>
> "2.5 holds the face, the outfit, the room and the voice for a full thirty seconds, across its own internal cuts. So one prompt describes the whole thing. No stills per scene. No stitching. No laying a voiceover over the top, because there's no seam to hide."
>
> "Three numbers to hold on to. Thirty seconds is the ceiling. Seven twenty p is the ceiling, there is no ten eighty. And it's sixty three credits a second, flat, so a twenty five second ad is about six dollars fifty."

---

## 2:15 — The stack (3 min)

**Show:** a full prompt from the prompts doc, scrolling slowly.

> "Every prompt is the same twelve blocks in the same order, every time. The order is not cosmetic. The model weights what it reads first, so everything that has to stay true for the whole ad goes at the top, and the stuff that changes goes underneath it."

Point at each band as you scroll.

> "Top band is state. Format, cast, wardrobe, set, product, look, camera, voice, sound. You declare each of those once and they hold for the whole runtime. That's the thing 2.0 could never do."
>
> "Middle band is the timeline. That's the beats, with a timestamp on each one."
>
> "Bottom band is the guards. Continuity, text, negatives. Continuity is the one people skip and it's the one that saves you. Every time you change something mid-ad, continuity is where you say what must *not* change with it. Change the location and the outfit drifts. Change the outfit and the earrings vanish. Earrings always go first."

Pause on the CAST block.

> "One thing that trips everyone. When you've wired a photo of her as a reference, cast is a pointer, not a description. Don't describe her face. If you describe a face that's already in the picture, the model re-renders it from your words and your words win. You've just thrown the reference away. Only describe what the photo can't tell it: how old she reads, how tall she is next to the bag."

---

## 5:15 — The three numbers that must match (90s)

**Show:** the FORMAT line, then the last beat's end timestamp, then the API duration field.

> "This is the single most common way to waste six dollars. The runtime in the format line, the sum of your beat windows, and the duration you send to the API all have to be the same integer."
>
> "If you write a twenty one second timeline and send fifteen, it doesn't error. It compresses. Everything speeds up, the delivery slides out from under your beats, and every caption you cut to it is wrong. It'll look almost right, which is worse."
>
> "Also: declare the cut count in the format line. 'Exactly five hard cuts.' Leave it out and the model either ignores the timeline completely or cuts every two seconds."

---

## 6:45 — Writing the lines (3 min)

**Show:** the beat table in the brief.

> "Every line in the brief is sized to its beat. Roughly two point three words a second. That's not a style preference, it's load bearing, and it fails in both directions."
>
> "Too many words and it doesn't cut the line, it crams it. You get an auctioneer. You'll hear it immediately."
>
> "Too few words is the one that surprises people. Give the model empty time and it invents something to fill it. It will grow a spoken line out of a stage direction. It'll invent filler hand motions, and that's where warped hands come from. So if a beat has no dialogue, you write, in the beat, 'none, natural breath.' Say it out loud in the prompt."

Point at the VOICE block.

> "And at the bottom of voice, this sentence, every single time: 'There is no narrator and no voiceover. Only the person visible on screen speaks, and her lips move when she does.' Without it, clips grow narration out of nowhere."
>
> "If lip sync comes back soft, the fix is always fewer words. Never a longer beat. Cut the line."

**Show:** the cut vocabulary table.

> "Five cut types and you pick exactly one per beat. Open is the first beat. Jump cut is same setup, time skips, and that's your default inside somebody talking. Hard cut is a real change of framing. Match cut is same composition, different contents. Continuous means no cut at all, which is how you break a long action into pieces you can direct without spending a cut."
>
> "Banned: whip pan, zoom transition, crossfade, dissolve, speed ramp. Every one of those reads like an agency made it, and the whole point of this format is that nobody made it."

---

## 9:45 — The two ways prompts silently break (2 min)

**Show:** the failed generation.

> "Two things that don't throw an error, they just quietly ruin it."
>
> "One. Never say 'add', 'remove', 'change' or 'replace' anywhere in the prompt. Those words reroute the whole job into edit mode and force-lock the duration. A beat that innocently says 'she adds a scarf' just broke your timeline. Say 'she puts on a scarf.'"
>
> "Two, and this is the good one. Negation summons. If you write 'no table', you get a table. We tested it. The set block said no table, no desk, no visible surfaces, and the output had a nightstand and a lamp. It said no rings and she had a ring on."

Pause.

> "The reason is that 'no table' is a weak word wrapped around a strong word, and the model hears the strong word. So you never forbid an object. You describe the space positively instead. 'Bare wall, clear floor, sparse and uncluttered.' That does the job that 'no table' was supposed to do without putting a table in its head."
>
> "Negatives only work reliably for three things: on-screen text, audio, and extra people. 'No music' works. 'No subtitles' works. 'No other people, no onlookers' works. Everything else, describe what's actually there."

---

## 11:45 — References (2 min)

**Show:** the reference slots in the call.

> "Up to nine images, but don't fill it. Four or five assets is the sweet spot. Too many and the model can't tell which features matter."
>
> "Order is priority. Whatever you most need preserved goes first, and that's almost always her face."
>
> "Never feed it a collage, a contact sheet, or a character turnaround. It reads a collage as a busy scene, and turnarounds cause identity drift and give you twins."
>
> "Never put a verb right after a reference tag. Write 'the woman in @Image1 walks', not '@Image1 walks'. The digit runs into the next word and the binding goes ambiguous."
>
> "And this is the best line in the whole system: say what each reference does *not* control. 'This supplies geometry, materials and hardware only. Do not transfer its background or its polished product-photo look.' Naming what must not transfer is the difference between a reference and a contaminant. Our product photos are clean cutouts on white, and if you don't refuse the look, every frame you make inherits the catalogue render aesthetic and it looks like CGI."

---

## 13:45 — Firing it and checking it (90s)

**Show:** the kie call, then the balance.

> "Model is bytedance dash seedance dash two dash five. Hyphens, and only the hyphen version resolves. Nine sixteen, seven twenty p, generate audio true, and duration matching your timeline."
>
> "Check the balance before every fire. Sixty three credits a second, and the create call hard-rejects if you're short, it does not wait for a top-up. Failed calls aren't charged, so a rejection costs nothing but time."
>
> "When it comes back, pull frames at three or four a second, not one. Five things to check every time. Did it cut the number of times you asked. Is it the same face on both sides of every single cut. Is the wardrobe and the jewellery the same across every cut. Does the dialogue land inside its window, more than half a second of drift means the beat was overfull. And transcribe it, because if it invented a line you will not catch it by watching."
>
> "Last one and it's the one I care about most. If it looks clean, evenly lit, tack sharp and perfectly centred, it's a render and it's a reject. I want sensor noise, blown highlights, imperfect focus and crooked framing. Regenerate it. Don't ship it because the bag looks right."

---

## 15:15 — Close (30s)

> "Three variants of every still, always. The first roll is never the one. And when a pass is ninety five percent there, patch it rather than rerolling, because a retake reliably fixes the thing you named and breaks something else. Change one variable at a time."
>
> "Prompts are all in the brief. Any question, send me the frame."

---
---

# One-page cheat card

Keep this open while you build.

### The stack, in order — never reorder it
`FORMAT · CAST · WARDROBE · SET · PRODUCT · LOOK · CAMERA · VOICE · SOUND` → `BEATS` → `CONTINUITY · TEXT · NEGATIVES`

### Non-negotiables
- **Three runtimes match**: the number in FORMAT = the sum of the beat windows = the `duration` parameter. Integers only, 4 to 30.
- **Declare the cut count** in FORMAT, or it cuts every two seconds.
- **2.3 to 2.8 words per second.** Size the beat to the line. Both over and under fail.
- **Mark silent beats** `DIALOGUE: (none, natural breath)`.
- **The no-narrator lock** closes every VOICE block, verbatim.
- **Every override gets an answering CONTINUITY line** naming what it must not drag along.

### Words that break the job
`add` · `remove` · `change` · `replace` → reroutes into edit mode and force-locks duration
`extend` · `continue` → reroutes into extension mode
Say `puts on`, `lifts`, `turns`, `hooks` instead.

### Slop that actively hurts
`cinematic` · `epic` · `stunning` · `dynamic` · `8K` · `masterpiece` · `award-winning` · `Unreal Engine` · **`fast`** (the most dangerous single word in a Seedance prompt)

### Negation: what fires, what backfires
| Works | Backfires |
|---|---|
| no music, no BGM | no table, no chair, no props |
| no on-screen text, no subtitles, no watermark | no rings, no jewellery |
| no slow motion, no zoom, no speed ramps | no blur, no extra fingers, no warped hands |
| no other people, no onlookers | |

For anything in the right column, describe what *is* there instead.

### Cut types — one per beat
`OPEN` first beat only · `JUMP CUT` same setup, time skips, your default · `HARD CUT` real change of framing · `MATCH CUT` same composition, different contents · `CONTINUOUS` no cut

Banned: whip pan, zoom transition, crossfade, dissolve, speed ramp. Never write "Cut to:".

### Beat lengths
Spoken hook 3–5s · talking 3–7s · product or hands insert 2–4s · lifestyle 3–6s · close 2–4s
5 to 6 shots and 4 to 5 cuts is the safe zone for 25 seconds. Past 6 shots it starts silently dropping beats.

### References
Face first. 4 to 5 assets, not nine. No collages, no contact sheets, no turnarounds. No verb straight after a tag. State what each reference does **not** control.

### The call
```
model: bytedance/seedance-2-5
aspect_ratio: 9:16 · resolution: 720p · generate_audio: true
duration: matches the timeline exactly
reference_image_urls: face first
```
**63 credits per second, flat.** Check the balance before every fire — create hard-rejects when short and does not wait for a top-up. Failed calls are not charged.

### QA, every pass, frames at 3–4 fps
1. Cut count matches what you declared
2. Same face either side of every cut
3. Wardrobe and jewellery consistent across every cut
4. Dialogue inside its window, under half a second of drift
5. Transcribe it — under-filled beats grow invented speech
6. Product truth: colorway, hardware colour, no logos, no invented strap
7. **Photoreal.** Clean, even, tack-sharp and centred means it's a render. Regenerate.

### When it's wrong
Trim in post < patch the audio < regenerate the still < rerun the pass. If it's 95% there, patch it. Change one variable per retake. After two or three failed rewordings, change what actually happens in the shot.
