# <BRAND>-VID-<NNN> — <Concept Name> (<Format>)

### PRODUCTION METHODS — HOW WE MAKE ADS
HeyGen Avatar — Single talking-head yapper. One presenter, lip-synced to VO. Use for first-person story concepts and authority presenters.
Google Flow + Google Omni VO — For animation and VO-driven concepts with no person on screen. Google Omni generates the voiceover. Google Flow generates the video animation sequences.
Seedance 2.5 — For complex AI UGC where multiple people are talking in scenes and you need audio and video generated simultaneously. Use for character dramas, multi-person dialogue, scripted scenes with several characters.

---

## <BRAND>-VID-<NNN> — <Concept Name> (<Format>)
Reference: <swipe URL>
Format: <type> — <m:ss>. 1080x1920, 30fps, 9:16.
Production type: <method> + <voice route>. <One sentence on the physical setup.>

> [!note] VOICE CLONE: Extract the speaker voice from the reference below. Clone this exact voice — tone, pace, cadence, register. Do NOT use a generic AI voice. Then generate the WHOLE script as ONE continuous take — never segment and stitch, the stitches are audible. Settings: stability 0.45, similarity 0.8, style 0.25, speaker boost on. Reference: <swipe URL>

> [!note] THE ONE THING: <the single governing creative principle, and the rules it forces>

---

### <N> RULES THAT RUN THE WHOLE EDIT
1. <What is on screen by default, and the named exceptions.>
1. The image lands ON the word. <Cue-word examples.> Never mood footage — the image proves the word.
1. <The visual taxonomy for this ad and the rule that keeps the kinds from mixing.>
1. Real products only. <Name the exact products by trade dress.> Generic bottles kill the ad.
1. No image twice, with these exceptions: <timecodes>. <Which shot appears exactly once, and where.>
Captions: burned in, bottom-center, black text on a white rounded box, 2-5 words per card, changing about every second. There is no caption-free frame in this ad.

---

### STEP 1 — <THE TALENT / THE CHARACTER / THE CAST> (build this first)
<Route: generate one base frame, then build the avatar/character from it and drive it with the VO file. Engine, resolution.>
Before you generate: <the real-world quality bar to sit next to the output>. Generate 3-5 and pick the most ORDINARY one, not the prettiest.
Base-frame prompt (<engine>, 9:16):
```Plain Text
<full base-frame prompt>
```
Reject and regenerate if: <the specific tells that mean it looks generated>.

---

### STEP 2 — THE BUILDING BLOCKS (paste these into the prompts below)
Every prompt in the Visual Schedule is written short. Add the matching block to it. That is the whole system — you never write these out yourself again.

#### LOOK — add to every CARD prompt
```Plain Text
<the candid/real photography grammar>
```

#### SCIENCE — add to every FULL-BLEED you have to generate
```Plain Text
<the render grammar for unphotographable interiors>
```

#### <HER/HIM/CHARACTER> — add to every image they appear in
```Plain Text
Same <person/character> as the base frame attached as image reference — same face, same hair, same wardrobe.
```

#### PRODUCT — the hard law for the reveal
NEVER generate the <product> from imagination. Every product shot is image-to-image with the real product photos attached, so <label / shape / color / hardware> stay exact. Ask Brooks for the product reference pack.

> [!note] Before you generate anything: most of these images are already made and sitting on the Cutroom storyboard for this ad. Ask Brooks for the board link and view passcode, plus the real-footage folders. ALWAYS use real footage before you generate a replacement. The prompts below are only for what is missing.

---

### SCRIPT
Read verbatim, no paraphrasing. Timecodes are from the delivered VO take. The audio is ONE continuous take and never cuts — you are only cutting picture.
[00:00] <script>

---

### VISUAL SCHEDULE
One block per beat. Each block tells you the cue word, what goes on screen, and the prompt if you have to make it. Everything holds until the next beat unless it says otherwise.
Legend — CARD = camera roll, sits full frame. FULL-BLEED = <the generated/animated full-frame kind>. FACE = them, alone, nothing over them. GFX = you build it. PRODUCT = real product footage.

#### [m:ss] "<cue words>" — <TYPE>
<One line of intent. Hold / callback / once-only notes.>
Use: <folder> — <which clip>.
Only if missing — Make: <short prompt>. + LOOK

#### [m:ss] "<cue words>" — <TYPE>
<intent>
Make: <short prompt>. + <BLOCK> + <BLOCK>

---

### BEFORE YOU SEND IT BACK
1. Captions burned in on every single frame — black on white rounded box, bottom-center, 2-5 words a card.
1. <Any built graphics are placed.>
1. <Any fast flash-cut sequences are cut in.>
1. Word-sync pass: scrub the whole ad and check every image lands on its cue word and leaves when the claim ends. This is the pass that makes or breaks it.
1. <The bare-face beats are still bare. Do not let a caption crowd the face there.>
1. Product clips are cropped to fill 1080 with the label fully readable.
1. Listen at <m:ss> — the VO has to say "<brand>" correctly. If the clone mangles it, re-do that word.
1. Export 1080x1920, H.264, audio at -14 LUFS.

---

### PRODUCT LINK
<live product URL>
