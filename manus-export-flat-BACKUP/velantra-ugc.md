# Velantra UGC — Multi-Shot Ad Factory

Use this to go from a one-line request (e.g. "ad for the Straw Tote, use this creator photo, lead with the structure angle") to a finished, conversational, multi-shot UGC-style video ad for any Velantra product. It's built around a video generation engine capable of native multi-shot camera direction and native audio/dialogue generation within a single clip. Trigger this whenever the request is for a Velantra UGC video ad, multi-shot UGC, or a video ad that wants a creator on camera with multiple camera angles/cuts.

## Golden Nugget Doctrine (apply to every piece of creative you write)

Before writing any hook, angle, script, concept, or audit verdict, name the **golden nugget**: the single most emotionally loaded deep frame in the research — the real motive that makes buyers act, never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test:** for every candidate angle ask "is this the topic, or is this the motive?" If it's the topic, dig one layer deeper.
- **Where it goes:** the golden nugget leads — right at the top, as the hook. Never buried in the body.
- **Deliverable:** state the golden nugget in one explicit sentence before drafting. If the research hasn't surfaced one, keep digging until it does — never default to a surface angle.

## How multi-shot works here

Multi-shot works on two levels:
1. **Cuts inside a single generated segment.** A capable video generation engine can follow multi-shot direction within one continuous generation: change the camera framing across sequential blocks of the timeline (e.g. selfie medium close-up → macro shot of fingers on the material → wide step-back shot) and the engine cuts natively within that one output, in a multi-shot style.
2. **Cuts across separate segments.** Each segment of the ad (roughly 4–15 seconds) is generated independently, then stitched together in order afterward.

## How to use this

### Step 1 — Gather the input slots

Fill these from the user's request; only ask about what's genuinely missing:

1. **Product** — which Velantra product, and colorway if specified.
2. **Creator reference** — a single reference photo of the person who will appear as the on-camera creator for this whole ad. If none is supplied, either ask for one or propose a plausible creator (invent who would plausibly post this content, then search for a matching reference photo — clean photos only, no text overlays or app UI baked into the reference image) and get it approved before proceeding. From the chosen reference photo, write a verbatim creator description: age range, hair, skin, build, wardrobe, and energy — include natural, slightly imperfect human details (not airbrushed-perfect) — plus a matching voice character description. This description becomes the identity lock used identically across the entire ad.
3. **Angle/hook** — if not specified, default to this product's core wound (e.g. for the Straw Tote: floppy/fragile/sold-out straw bags → a structured alternative).
4. **Length** — do not treat this as a default user input. Derive it from the script (see the length doctrine below) unless the user gives an explicit target length.

### Step 2 — Derive the ideal length, then segment

Velantra UGC ads run 15–30 seconds total. The concept sets the exact length — an odd total like 23 or 26 seconds is correct when the script earns it. Never pad the script to hit a round number, and never cut a beat just to hit one.

1. Write the script first, using the beat structure: Hook → Problem → Benefit/Demo → CTA (see script laws below).
2. Time it: conversational delivery runs at roughly 2.7 words per second (about 30–45 spoken words per 15 seconds). Each beat's duration = that beat's word count ÷ 2.7, rounded to the nearest second. Total duration = sum of all beats, and the total should land between 15 and 30 seconds — if it doesn't, adjust the script itself, not the pacing.
3. Segment it: each generated segment should be 4–15 seconds, and splits should only happen at beat boundaries. Prefer the fewest segments possible (every extra segment is another seam where identity/scene consistency can drift): a script under 15s = 1 segment; 16–30s = 2 segments (e.g. a 23s ad might split 12s + 11s, wherever the beat boundary naturally falls). A beat that needs its own distinct visual world (e.g. a macro product demo) may deserve its own segment even if the timing would otherwise allow combining it.
4. A change in camera angle or energy does not by itself require a new segment — direct those changes as camera changes across sequential timeline blocks within a single segment.

## Rules & standards

### Script laws

Write conversational UGC dialogue, as if spoken to one friend:
- Commas and periods only — no ellipses, no em dashes, no hyphens (rephrase instead), numbers written as numerals, and never use the word "cinematic" in the dialogue itself.
- Use contractions, sentence fragments, and natural filler ("honestly," "okay so," "I'm not even kidding"). Aim for roughly 30–45 spoken words per 15 seconds.
- Keep delivery directions positively framed (avoid words like "composed" or "steady" — they tend to read as monotone delivery instructions).
- CTA = a casual nudge plus soft, honest, seasonal scarcity — never hard-sell urgency.

**Claims guardrails (hard rule — treat any violation as an automatic fail):**
- Never use any origin claim — no "Italian leather," "European craftsmanship," "made in the USA," etc. Say "leather detailing," "hand woven," and similar material-only language instead.
- Never say "Birkin" or "Hermes" in spoken or on-screen copy. Say "structured top handle silhouette" instead.
- If a founder character is referenced, always use the name "Jessica" — never a real person's actual name.
- Product-specific claim lists (what's allowed vs. banned for that specific product) always override these general defaults.

### Reference images — the identity mechanism (every segment, no exceptions)

Every generated segment should carry two reference images:
- **The creator reference** — the single reference photo chosen for this run, plus that run's verbatim creator description copied identically into every timeline block of every segment. Consistency across segments depends entirely on repeating this description exactly.
- **The product reference** — the canonical real photo of the product in the colorway the concept calls for. The product must be grounded by a real reference image; never let the generation model invent the product's appearance from text alone.

Optionally, a third reference image can lock a specific setting/room when a beat needs a consistent location.

### Segment prompt structure

Structure each segment's generation prompt as a block covering: overall format/shot style, an identity statement (creator + product both locked to their reference images), a scene lock (the setting), the creator description (verbatim, repeated identically across every segment), a timeline broken into ~5-second blocks each specifying camera framing, what's in each hand, facial expression, what's in frame vs. not in frame, lighting, and background, an audio section (voice description, room tone, delivery style, and the exact dialogue for that block), and a "never" list of things that must not appear.

Notes for this product line specifically:
- The identity statement should explicitly state that the product stays exactly as shown in its reference image — same texture, same shape, same colorway, unchanged.
- For segments with multiple camera angles, change the camera direction between timeline blocks, and drop any "no cuts inside the clip" instruction (keep that instruction only for genuinely single continuous-shot segments).
- A reliable default shot arc: medium-close selfie hook with the product at chest height → macro insert on fingers touching material/stitching → wide step-back shot with the product on the arm → medium-close CTA. Adjust for unboxing, try-on, or review-style variants as the concept calls for.
- Always include in the "never" list: no brand logos, no invented text on the product, never mention where the product or its materials are made.
- **Face law:** always state explicitly which faces/sides of the product carry visible detailing — e.g. "the leather flap and belts exist ONLY on the FRONT face, the back is plain straw" — and add "no duplicated front detailing on any other face" to the "never" list. Video generation engines have a strong tendency to mirror front detailing onto the back of a product whenever it turns or tilts, unless explicitly told not to.
- **Component-count law:** state exact counts for any repeated design element — e.g. "the front flap is exactly 3 leather elements, one wide center panel with 2 squared outer tabs, never 4." Video generation engines tend to multiply repeated elements (tabs, grommets, straps) under motion unless the count is explicitly pinned down.
- **Blocking-escalation law:** if the same visual defect survives two rounds of prompt-level fixes (negative instructions, geometry pinning), stop re-prompting — the composition itself is likely the root cause. Rewrite the blocking (the pose/composition) so the defect becomes physically impossible. For example, if a raised-bag pose keeps wrapping a handle around a model's face, change the pose entirely (e.g. bag resting on a table, hands on the table, "the bag is never lifted, no hands on the bag") rather than continuing to patch the same defect with more negative instructions. Poses that keep hands and faces away from a fragile design element usually cost nothing creatively at normal viewing speed.
- **Pronunciation law:** video generation engines can randomly slur risky product words (e.g. slurring "tote" into something else). Delivery hints and phonetic respelling reduce but don't reliably fix this, and automated transcription tools can "launder" the slur in either direction, so always do a human ear-check on product name pronunciation. If a take is visually perfect but the pronunciation is wrong, the fix is a targeted audio patch rather than re-rolling the whole segment: extract the audio, transcribe it with word-level timestamps to find the slurred word's exact time window, generate a clean replacement of that single word using a cloned version of the same voice (spoken mid-sentence in matching context so the prosody matches), word-timestamp that replacement, cut it to size, gain-match it to the surrounding audio, splice it in with a short crossfade (~20ms) on each side, and re-transcribe the patched region to confirm it reads correctly before archiving the original. This works because a slurred one-syllable word usually has nearly identical mouth shapes to the correct word, so the patch is invisible at normal viewing speed.

### Build workflow

1. Resolve the product and colorway. Confirm or gather the creator reference photo (keep a copy alongside the rest of the concept's files so the run is reproducible). Write the script, derive the length, and segment it per the doctrine above.
2. Write out the full generation plan: which engine mode to use, whether the first segment's voice should be carried forward as the voice reference for later segments (recommended, for one consistent voice across cuts), which reference images go into which segment, and each segment's full prompt, dialogue, and target duration. Default to a vertical 9:16 aspect ratio; use a lower base resolution for drafts and only render a winning concept at full resolution.
3. Show the user the script, the segment plan, and a rough cost/effort estimate before generating anything.
4. Generate segment by segment, in a way that's resumable — if a run fails partway through, re-running should skip any already-finished segments rather than redoing them. After all segments are generated, stitch them into a final video in order.

### Output organization

Organize each finished concept's files together: the human-readable segment-by-segment prompt document, the generation plan/manifest, and the output folder containing each individual segment file plus the final stitched video.

### QA before delivering (non-negotiable)

Watch the finished video end-to-end and confirm all of the following before handing it over:
1. No origin claim or other banned word appears anywhere in the spoken audio.
2. The product matches its canonical reference exactly (correct shape/mechanism, correct material/weave, correct colorway).
3. The same face and the same voice appear consistently across every cut.
4. Energy is held all the way to the last word — no fade-out in delivery.

Any failure on any of these means regenerating that segment — never hand over a video that fails this check.

## Related workflows

This skill produces the segment-by-segment script and generation plan. A separate, more detailed segment-prompt-format reference exists for teams that want the full JSON-style prompt schema in more depth. A separate skill/process exists for other brands using a different underlying video engine — this one is specific to the engine capable of native multi-shot camera direction and native dialogue/audio generation described above. Upstream, the various Velantra per-product "video ad concept" documents are meant to feed their finished briefs into this skill's script-writing step.
