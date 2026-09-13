# Universal Script Naturalizer

Full pass for the naturalizer step summarized in SKILL.md's spoken-copy section. Mandatory for any deliverable that gets spoken: video ad scripts, VSLs, UGC scripts, VO tracks, podcast reads, founder-to-camera pieces. This is not optional polish — it is part of the self-audit for any spoken copy, in the same way the pre-writing checklist and audit in references/output-format-checklist-and-commandments.md are mandatory for written copy.

Takes any ad script that is strategically correct but sounds written, and makes it sound spoken. Works on any format (two-person podcast, single talking head, VO over B-roll, founder to camera, street interview, duet reaction), any runtime, any voice engine (a TTS/AI voice tool or a human creator reading off a phone).

This pass runs on top of the anti-choppiness rules in references/voice-engineering.md — it does not replace them. Those rules kill patterns that read as AI on a page. This kills patterns that read as WRITTEN when spoken out loud. A script can pass the anti-choppiness rules clean and still sound like a copywriter performing.

---

## Role

Think of this as script-doctoring for spoken performance, not rewriting the argument. The strategy, mechanism, proof, and close are already decided and correct. The only job is to make a real person sound like they're saying this out loud for the first time, instead of reciting something someone else built. Nothing changed here may alter what the script claims, proves, or asks for.

---

## Config to Fill Before Running a Naturalizer Pass

If a field is blank, infer from the script and state the inference in one line at the top of the output, then proceed.

```
FORMAT:            (2-person podcast / single talking head UGC / VO over b-roll /
                    founder to camera / street interview / duet reaction / other)
RUNTIME:           (seconds, approximate)
SPEAKERS:          (who, and their relationship to the product: user, host, founder,
                    friend of a user, expert)
ENGINE:            (which video/voice generation tool or human creator will deliver this)
MODE:              (LOCK or REWRITE. Default REWRITE.)
AWARENESS STAGE:   (problem aware / solution aware / product aware, etc.)
BRAND LAWS:        (any brand-specific bans, e.g. no competitor comparisons,
                    no origin claims, banned words)
LOCKED ELEMENTS:   (any claim, number, study, dosage, price, guarantee, product name,
                    URL, or placeholder that must survive verbatim)
```

---

## Mode

### Mode A: LOCK

The spoken words are frozen. Do not change, rewrite, paraphrase, shorten, expand, reorder, correct, or remove a single word any speaker says. Do not add filler, interjections, acknowledgments, or new lines. All naturalness comes from the performance annotation layer only (Parts 4–5 below).

Use LOCK when the script is legally approved, when it's a proven winner being reshot, or when explicitly instructed to.

### Mode B: REWRITE (default)

The words may change, under the hard locks below — this is the mode that fixes a script that sounds like a direct response copywriter wrote it, because that problem lives in the words, not the camera.

REWRITE produces two versions:
1. **Copy of record** — the clean written script with changes applied, filed and approved.
2. **Spoken delivery version** — the same script formatted for the delivery engine or creator, with performance annotations attached.

They differ only in punctuation and annotation, never in content.

---

## Hard Locks (both modes) — these survive untouched no matter what

1. Every claim — no claim softened, strengthened, added, or removed. If the script says a study found roughly fifty to sixty percent, it still says roughly fifty to sixty percent.
2. Every number, study name, ingredient, dosage, price, timeframe, and guarantee term.
3. The product name, brand name, and URL, spelled and said exactly as given.
4. The CTA — same ask, same place in the script.
5. The beat order — hook, problem, mechanism, redirect, product, proof, close stay in the order written; this is not a re-architecting pass.
6. Runtime — the naturalized version must still fit. Naturalness that adds fifteen seconds to a thirty-second ad is a failure, not an improvement.
7. All user-editable placeholders in brackets or braces, verbatim.
8. Any brand law given in CONFIG.
9. Compliance posture — if the script hedges deliberately (association is not causation, results vary), the hedge stays. Naturalizing is not a license to make a claim harder.

---

## Part 1: Diagnose — the tells that make a script sound like a copywriter performing

Read the script out loud in your head at performance speed and mark every instance of:

1. **The announced transition.** The script says out loud that a new beat is starting. "And here's the part that should make you angry." "So here's why the obvious fix makes it worse." "And this is the part almost nobody gets told." Nobody announces their own paragraph breaks in speech. One is a device; three is a formula the audience feels even if they can't name it.
2. **Every beat lands.** Every paragraph closes on a crafted punch line. Real speech doesn't land every thought — some die mid-sentence, some end on the least interesting word, some run straight into the next idea. A script where all eight beats stick the landing is a script that was built, not said.
3. **Symmetry.** Balanced clause pairs, tricolons, matched sentence lengths, setup-turn-payoff every time. Speech is lopsided — one thought gets nine words, the next gets thirty-one.
4. **No backing up.** Nobody restarts a sentence, corrects a word, or approximates before getting specific. Written copy is right the first time; speech arrives at precision.
5. **Page vocabulary.** Words the speaker doesn't own: "Moreover." "The mechanism." "Crucially." "What's actually happening here." "The reality is." Also house-style tells: "here's the kicker," "let that sink in," "that's the part nobody tells you."
6. **Reaction after information.** The script states the fact, then delivers a crafted emotional line about it. People do the opposite — the feeling comes first, the fact follows.
7. **Unspeakable punctuation.** Em dashes, semicolons, colons, ellipses, parentheticals. If it can't be said out loud, it was written for an eye.
8. **Zero waste.** Every word load-bearing. Real speech carries about one wasted cluster per thirty seconds, and that waste is what makes the load-bearing parts sound thought of rather than drafted.
9. **Brand voice leaking into the speaker.** A creator who's not the brand saying "our sale," "we formulated," "we stand behind it," instead of "they're running a sale," "the company that makes it," "they do ninety days instead of thirty." Founders speaking as themselves are the only exception.
10. **Uniform energy.** No section is throwaway. In speech, some information gets tossed off and some gets leaned into, and the contrast is what makes the leaned-in parts hit.

---

## Part 2: The Rewrite Moves (Mode B only)

Apply selectively — the target is a script that sounds spoken, not a script covered in tics. Fix the worst offenders, leave clean lines alone.

- **Cut the announcement, keep the beat.** Delete the sentence that announces the next section; start the section on its own content. Keep at most one announced transition in the whole script, at the single most important turn.
- **Un-land one beat in three.** Move a crafted closing line earlier so the thought continues past it, or replace it with the plain version of itself.
- **Break the symmetry.** In any tricolon, give one item twice the words and blow through another in four. In any balanced pair, make one side longer and rougher.
- **Let one thought arrive instead of starting correct.** One self-correction per sixty seconds, landing on the same meaning it started toward: "It's a signal. It's a nerve, really, but think of it as a signal." Never on a number, ingredient, dosage, product name, or CTA — those deliver clean, always.
- **Front-load the reaction.** Move the emotional line ahead of the fact it's reacting to, and shorten it: "That one made me mad when I found it. The slowdown isn't what's making you lose the weight."
- **Start sentences with and, so, but, because.** Repeat a word instead of reaching for a synonym.
- **Contractions everywhere,** except where the uncontracted form is doing audible emphasis work.
- **Trade one category noun for a concrete one.** "Symptoms" becomes "the burps." "Digestive discomfort" becomes "a brick in your stomach." Never trade the other direction.
- **Add one wasted cluster per thirty seconds.** "Honestly." "I mean." "The weird part is." Comma-framed, never trailing off. Roughly one per two segments in a segmented shoot.
- **Vary the energy.** Mark one stretch to be tossed off at speed, one to be leaned into — usually the mechanism is leaned into, the setup is tossed.
- **Read the breath test.** Any sentence you can't say in one breath gets a comma or a split. Any sentence that's uncomfortably short next to two other short ones gets absorbed into its neighbor.

### What NOT to do

- Don't dumb it down — named terms stay named (gastroenterologist, apigenin, chlorophyll). Simple means short sentences and one job per term, not a smaller vocabulary. Target a fifth-to-sixth-grade reading level, not a hard fourth.
- Don't add personality, quirk, jokes, hedging, or warmth that wasn't in the strategy.
- Don't add "um," "uh," "like," or "you know." Verbal texture is comma-framed words, not stutter.
- Don't trail off — no sentence ends in a fade.
- Don't lose a proof point, number, or beat to make room for texture.
- Don't make it longer — texture comes out of the word budget freed by cutting announced transitions, not on top of it.
- Don't naturalize the CTA into vagueness — the ask stays specific and confident.

---

## Part 3: Punctuation Law (spoken delivery version)

The spoken delivery version uses commas and periods only. No em dashes, en dashes, ellipses, semicolons, colons, or parentheses inside a spoken line — video and TTS engines render them as literal dead air, and a human reading off a phone renders them as a stall. Every intentional pause is directed in the performance annotation, never punctuated into the dialogue. Question marks are allowed where the line is genuinely a question; exclamation points are not. The copy of record follows normal written punctuation, minus em dashes, which are banned house-wide in every format.

---

## Part 4: Performance Annotation Layer (both modes)

Annotations live outside quotation marks, on their own line or in brackets, never inside the dialogue where an engine could speak them out loud. Realism comes from a few chosen imperfections with a clear purpose, not from annotating every line — it should be obvious in the finished video and nearly invisible on the page.

**Delivery:** brief inhale before a difficult or personal statement; half-beat pause inside a thought, not between thoughts; slight hesitation before one important word; glance away while recalling a detail, then back; pace picks up on the casual part, settles on the important part; a sentence that starts fast and slows into its own point; a soft exhale or self-conscious half-smile after a revealing line; voice drops on the honest line, not the sales line. Never direct a mispronunciation or anything that makes the words hard to hear — numbers, ingredients, the product name, the URL, and the CTA stay clean and clear, no texture.

**Overlap and interruption (multi-speaker only):** next speaker starts during the final fraction of the previous line; listener leans in as if preparing to answer before the other finishes; a quiet nonverbal acknowledgment under the last few words; one speaker's hand starts to rise as if to interject, then settles. Must feel supportive and accidental — never rude, never on top of a claim, number, or CTA. Don't add new spoken interjections to create overlap.

**Listening reaction (multi-speaker only):** reactions build in stages instead of appearing on cue — a nod that begins before the line finishes, eyebrows lifting as significance arrives (not as the sentence starts), a beat of confusion resolving into recognition, a restrained smile (never a grin), a small pause before replying, eye contact then a natural glance down. The listener is listening for the answer, not waiting for their cue.

**Body and behavior:** irregular blinking, visible but quiet breathing, small posture shifts, hands resting imperfectly rather than posed, occasional gestures beginning slightly after the sentence they belong to, brief glances away and natural return. Movements don't land simultaneously and speakers don't mirror each other. No constant gesturing.

**Pacing:** avoid symmetrical back-and-forth. Include one reply that comes a half-beat late, one that comes fast, one breath that delays a phrase, and one cut that lands a fraction off the cleanest possible edit point. Keep the total inside the runtime.

---

## Part 5: Camera and Audio Realism

Professionally captured, not clinically perfect. The camera is present in the room without asking to be noticed.

**Camera:** very subtle handheld drift or tripod micro-movement; minor framing variation between speakers; slight focus breathing on a posture shift; one small autofocus correction that resolves fast; one cut a fraction early or late; natural background depth with small unfocused movement where the location justifies it; mild lighting variation across faces and realistic shadow falloff; normal lens character rather than artificial sharpness. Never: dramatic shake, aggressive rack focus, cinematic swoops, artificial zooms, visual glitches. Never use the word "cinematic" in a generation prompt.

**Audio:** consistent low-level room tone named once; soft breath before selected lines; slight variation in voice intensity; minor mic proximity change on a posture shift; minimal mouth sounds; a faint chair, clothing, or table sound only when a movement in frame justifies it. Never: distracting noise, clipping, distortion, loud background events, exaggerated mic artifacts, or heavily processed studio-perfect sound. Dialogue stays fully intelligible throughout.

**Support surfaces:** never direct a set-down, a lean, or a placement onto a surface that doesn't exist in the reference frame.

---

## Part 6: Annotation Density

Density per unit of time goes DOWN as runtime goes up. A ninety-second script with sixty annotations is over-directed.

| Runtime | Delivery | Overlap | Body | Camera | Audio |
|---|---|---|---|---|---|
| up to 15s | 2 to 4 | 1 | 2 to 4 | 1 | 2 |
| 15 to 30s | 4 to 6 | 1 to 2 | 4 to 6 | 1 to 2 | 2 to 3 |
| 30 to 60s | 1 per ~8s | 2 | 1 per ~10s | 2 to 3 total | room tone once, 3 to 4 breaths |
| 60s and up | annotate per segment, 1 to 2 each | as the cuts allow | 1 to 2 per segment | 3 to 4 total | room tone once, breath as needed |

These are guidelines, not quotas. Don't annotate every sentence, don't repeat the same annotation, and never place a pause, a nod, or a smile after every line. On segmented shoots, one named vocal register is restated verbatim in every segment prompt, with deviations written as small shades of it rather than gear changes. Energy holds through the final word of every segment — no trailing off, no fade to flat.

---

## Part 7: Format Profiles

- **Two-person podcast.** Overlap and listening reaction carry most of the realism. The guest is explaining something they understand or lived, not presenting. The host is curious, not performing curiosity. Neither looks at the camera.
- **Single talking-head UGC.** No overlap available, so realism moves into delivery variation and the self-correction budget. Register: talking to a friend about something that actually happened, voice rising and falling, stressing key words, speeding up and slowing down. Never monotone, never reading. Avoid register words that cue flatness (composed, steady, even, calm) and backward-looking words that cue drift (remembering, wistful, reminiscing). Quiet beats are intense and leaning in, never low energy.
- **VO over B-roll.** No body-language layer — everything rides on pacing, breath, and energy contrast. Deliver as one continuous take rather than assembled per line, so the register can't drift between cuts. Naturalize harder on the words, since the words are all there is.
- **Founder to camera.** Direct address is allowed and expected; the founder can say "we." Lower the disfluency budget, raise the pause budget. Authority reads as unhurried, not polished.
- **Street interview or reaction.** Highest disfluency tolerance, lowest production polish — framing imperfection is the point. Still never on numbers or the product name.
- **Any format where the speaker is not the brand.** They never say "our," "we," or "us" about the company. Sale, guarantee, and shipping all belong to "they."

---

## Part 8: Engine Notes

- **Annotations must sit outside quotation marks.** Several generation tools will read a parenthetical inside a dialogue line out loud. Put performance direction on its own line or in a separate performance block keyed to the line.
- **Dense visual-generation prompts** (for tools that build video from a text description) need timestamped blocks with everything locked explicitly — the tool invents whatever's left undescribed. Use frame-relative spatial language only, never person-relative. These tools generally can't spell reliably, so on-screen text should come from a post-production overlay, not the model.
- **Segmented engines** (where a long video is built from a chain of shorter segments): segment one sets the voice anchor for the whole chain. If segment one sounds read, regenerate it before continuing — never try to fix delivery downstream. Every later segment anchors to segment one, not to the segment before it.
- **Voiceover/TTS tools:** deliver one continuous full-length take, never assembled from per-line renders.
- **Human creator:** deliver the spoken delivery version plus a short performance note per beat. Don't hand a creator a page of annotations — they'll perform the annotations instead of the line.

---

## Final Audit Before Delivering a Naturalized Script

Confirm silently before returning; if any check fails, fix it and re-run the audit:

1. Every claim, number, study, ingredient, dosage, price, guarantee, product name, URL, and placeholder survives exactly.
2. The CTA is unchanged in content and position.
3. The beat order is unchanged.
4. In LOCK mode, not one spoken word changed and no dialogue was added.
5. The script still fits the runtime at performance speed.
6. Zero em dashes anywhere. Zero ellipses, semicolons, colons, or parentheses in the spoken delivery version.
7. No "that's not X, it's Y" construction. No false contrast stack. No parallel repetition stack. No rhetorical section opener. No banned transition phrase.
8. At most one announced transition remains in the entire script.
9. At least one beat now ends without a crafted landing.
10. Sentence lengths are visibly uneven across the script.
11. Disfluency and self-correction appear nowhere near a number, an ingredient, the product name, the dosage, or the CTA.
12. If the speaker is not the brand, they never say we, our, or us about the company.
13. Nothing was dumbed down — named terms are intact, each doing one clearly stated job.
14. Annotations are sparse, non-repeating, outside quotation marks, and within the density table.
15. The result reads as a person talking, not as an ad being performed.

---

## What to Hand Back

Return, in this order, with no commentary before or after and no change log:

1. **Copy of record** (Mode B only) — the clean written script with changes applied.
2. **Spoken delivery version** — commas and periods only, formatted for the delivery engine or creator named in CONFIG, with performance annotations attached outside the dialogue.
3. **Production notes** — camera, audio, and register direction as a short block, not per line.

---

## Standalone Use

This reference also works as a self-contained prompt: fill the CONFIG block above and paste the complete script below it, then run the full pass (diagnose, rewrite, punctuation law, annotation layers, final audit, output) in any context that needs to naturalize a script on its own.

```
CONFIG:
[FILL THE CONFIG BLOCK]

SCRIPT:
[PASTE THE COMPLETE SCRIPT]
```
