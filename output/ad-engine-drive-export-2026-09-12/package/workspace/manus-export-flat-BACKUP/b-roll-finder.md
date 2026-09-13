# B-Roll Finder

This document describes a methodology for sourcing accurate, on-brand B-roll footage for a video edit and placing each cutaway precisely on the word it illustrates. It reads a script or transcript, works out what each line is *actually about* (not just its keywords), routes each moment to the right kind of footage source, and returns a tight set of vetted candidates for a human to make the final pick from — never picking automatically. Use this whenever a video edit needs supporting cutaway footage sourced or organized: podcast/interview intros, tutorial/explainer intros, direct-response video ads (UGC/VSL/native style), competitor or drama-style videos, or storytelling/listicle videos. It is best suited to reference-rich talking-head video where the speaker names concrete things (people, products, companies) or makes checkable claims — the more proper nouns and provable claims in the script, the better this works. It is not well suited to pure vibe/mood montages or non-verbal music-only video, where footage choice is a pure taste call that should stay with the human editor.

There are two related lineages of this methodology below: a general-purpose version (for talking-head YouTube-style content) and a direct-response ad-specific fork with its own taste profile and stricter laws. Use the general version's principles for any video; use the direct-response section's specific rules when the deliverable is a DR video ad (UGC/VSL/native style).

## Core rules that govern everything, in every context

1. **A human makes the final pick, never the AI.** This methodology's job is to narrow the funnel down to a short, vetted, well-organized set of candidates — never to make the final creative call unsupervised.
2. **Footage of the action, never footage about the topic.** The test: could a stranger, watching the muted clip with no context, correctly name the specific action or emotion required? A person talking *about* being bloated is not the same as a person visibly bloated. If the footage only relates to the topic in the abstract, it's a mismatch and gets rejected.
3. **Never treat an AI text verdict as proof by itself.** Any automated "this clip matches" judgment is an input to be checked, not proof on its own — the actual frames should be visually reviewed by a human (or at minimum tiled into a contact sheet and looked at) before anything ships.
4. **Accuracy over volume; drop rather than pad.** No B-roll for a slot is better than wrong B-roll for that slot. A slot that can't be filled accurately should ship empty with a note, rather than filled with a mediocre-but-technically-on-topic clip.
5. **A user's stated preference or ban is law, and it persists.** If a preference is stated mid-project ("no skits," "captions are fine here," "that slot needs competitor products visible"), it applies immediately, for the rest of the project, and should be written down somewhere durable (a running "guardrails" note) so it's never violated again, even in a later session. Violating a stated ban is the single worst failure mode.

## Understanding the video before sourcing anything

1. Read or watch the whole script/video first, before sourcing a single clip. The emotional arc of the piece determines what each beat actually needs — the same words can need completely different footage depending on whether they land during an agitation section or a resolution section.
2. **B-roll illustrates the point being made, not the literal words used.** Example: the line "I stopped saying yes to dinner plans" calls for the empty chair, or the phone left face-down — not literal footage of a dinner.
3. Prefer footage of **aftermath over symptom**. For an emotional or medical beat, show the defeated posture in the recliner afterward, rather than the acute medical event itself.
4. For any line that references a real, checkable claim, discourse, or artifact ("she showed me the studies," "one thread said," a named product being criticized), the default is to try to source the *real* underlying artifact (a real post, real headline, real review) rather than fabricate a mockup — see the Receipts route below, and the fabrication rule under Guardrails.

## The routing model — classify every beat before sourcing anything

| Route | Trigger | Source | Notes |
|---|---|---|---|
| **Action/Emotion** | A person doing or feeling something — usually the largest single category in a native-style ad (roughly a quarter of total runtime) | Organic short-form social video (e.g. searched via a platform's own search, downloaded via a tool like yt-dlp), matched to the avatar community's own language | This is the route that most needs high sourcing volume + a hard visual quality gate, since rejection rates run 60-80%. |
| **Institutional** | Authority beats — doctor, lab, clinic | Licensed stock footage libraries, or scoped video search of official/authoritative channels | Polished, professional-looking footage is *correct* here — this is the one route where amateur/rough footage is wrong. |
| **Concept/Mechanism** | "How it works" — organs, nerves, molecules, diagrams | Stock 3D/medical animation libraries, or AI image-to-image generation seeded from a real reference diagram/frame (never generate this kind of visual from a blank text prompt) | |
| **Receipts** | A claim, a piece of discourse, "people are saying," a cited artifact | Real posts/headlines/reviews only, captured as clean screenshots. Never fabricate a citation, study, sample size, percentage, or named doctor/expert. A brief-specified *mockup* (e.g. a deliberately fictional forum-thread graphic the brief explicitly calls for) is a graphics build, clearly presented as such — never presented as a sourced real artifact. | |
| **Product** | The product itself on screen | The brand's own real product photos/footage only. Never sourced from strangers' footage, never AI-generated from scratch. In some native-style ads there may be no product shot at all — follow the brief. | |
| **Graphics** | Text cards, ingredient callouts, on-screen counters, mockups | Built directly from the brief's exact spec (image generation tools, HTML/motion graphics, or manual editor work) — never sourced from found footage | |

**Quick decision order:** Is it a person doing or feeling something? → Action/Emotion. Is it an authority figure? → Institutional. Is it something happening inside the body or otherwise abstract? → Concept. Is it a checkable claim or artifact? → Receipts. Is it the product itself? → use real product assets only. Is it text/numbers on screen? → Graphics build list.

## Working efficiently — the funnel is mainly for people-footage

- For a full shot list, source by *category/slot*, not beat-by-beat serially. Cluster similar beats into shared sourcing slots (e.g. all "frustration at the mirror" beats become one slot), and run one sourcing pass per category rather than fetching one clip at a time per line.
- For the more objective routes (Receipts, Institutional, Concept) — once the plan is agreed, source just **one best candidate** per beat. The multi-candidate, human-graded contact-sheet approach is specifically for the Action/Emotion route, where volume + a hard gate + a final human pick is the actual mechanism that makes it work.
- Time-box each objective-route beat to a few minutes: place the best available candidate, or flag it and move on. Don't retry indefinitely — one retry with a different search approach, and if that also fails, drop the beat and flag it rather than trying a third time.
- Cache raw downloads so re-renders of an edit don't have to re-fetch the same source material.

## The Action/Emotion route in detail — sourcing organic social footage

When building a sourcing plan for this route, every slot's search spec should:

- Describe **what literally fills the frame** ("thumb turning a dose dial, close-up"), never the abstract topic ("medication handling"). This distinction matters enormously for search-term quality and for grading candidates later.
- Avoid any softening language like "talking is acceptable if..." in the spec — any such exemption tends to get used by whatever gate/reviewer is checking candidates to rationalize a topic-match through as a pass, when it should be a fail. If there's a genuine exemption for faces not being visible, phrase it strictly: "only if the face never appears in the best segment."
- Use search terms phrased the way the actual target audience talks about this, not generic stock-footage language — and anchor them to the right age group and to the specific format/genre that community actually posts in (e.g. "bloat check" or "weigh-in Wednesday" style phrasing, not "abdominal discomfort").
- Expect a 60-80% rejection rate on candidates — plan to source 3-5x the number of clips actually needed. If a slot comes up short, rewrite the search terms and try again; never loosen the quality gate to make the numbers work.

## Grading candidates — score every clip before it's shown to anyone

1. **Visual subject test** — the decisive test: would a stranger watching muted correctly identify the required action/emotion from the footage alone?
2. **Avatar fit** — does the on-camera person's apparent age match the target avatar, for any face-visible clip? A faceless clip is only exempt from this check if the face genuinely never appears anywhere in the usable segment.
3. **Credibility texture** — for organic/UGC-style slots, rough amateur phone footage (imperfect lighting, handheld, everyday setting) reads as authentic; for Institutional slots, the opposite is true — polished footage is correct there.
4. **Emotional register** — does the footage match the beat's *required emotion*, not just its topic? A performed reaction, a comedy skit, or an obviously staged bit about the topic should auto-fail even if it's topically on-target.
5. **Format fit** — is it croppable to the target aspect ratio, high enough resolution, long enough, and usable with audio stripped out?

## Contact sheets and a mandatory visual audit before anyone else sees the footage

After the automated gate has run, tile every surviving candidate clip into one labeled contact-sheet grid per slot, and *actually look at every sheet*, grading line by line against an explicit reject checklist:
(a) fails the visual subject test; (b) visibly wrong age for a people-facing slot; (c) caption/watermark state violates the project's rules; (d) obviously AI-generated content shown on a slot that's supposed to be real footage; (e) subject displaying something to camera when the spec calls for a performed, non-camera-aware action; (f) reads as a comedy skit/performance; (g) letterboxed or upscaled from too small a source.

Delete anything that fails, with a noted reason. A vague "looks fine" pass without running this checklist is exactly how a wrong clip (e.g. a face-filling-the-frame reaction shot standing in for genuine bloat B-roll) slips through.

## Placement — landing the cutaway on the word

- Voiceover should be treated as one continuous, unbroken audio take — cutaways are visual only and never interrupt the audio. Anchor every cutaway's timing to word-level timestamps of the actual voiceover (most modern transcription tools can output word-level timestamps; if not, force-match the known script text to the audio).
- The cutaway should land as, or just slightly after, the relevant keyword is spoken (roughly 0.2-0.5 seconds after) — bias toward landing slightly late rather than early when in doubt. Late reads as an intentional, considered cut; early reads as a mistake or a technical glitch.
- General pacing guidance for a DR-style ad: a new cutaway roughly every 2.5-4 seconds; no single cutaway holds longer than about 7 seconds; the talking-head/avatar is never left uncovered by a cutaway for more than about 10 seconds at a stretch; when two cutaways would otherwise be separated by less than half a sentence's worth of avatar footage, extend the first cutaway across the gap instead — a very brief flash back to the avatar between two cutaways reads as an editing error.
- Always do a final word-sync audit pass over the whole timeline before delivering any placed edit — literally step through and confirm every cutaway lands where it should relative to the audio.

## Composition and formatting

- For vertical/social formats: crop to fill the frame edge-to-edge (never letterbox); use a blurred-fill background only for genuinely odd-aspect source material. Avoid building split-screen compositions manually.
- All cutaways should be silent — strip clip audio entirely; the continuous voiceover carries all audio.
- For any still-image cutaway, use only a very subtle, smooth, sub-pixel zoom motion (roughly 1.5% scale per second, rendered with proper interpolation) — a naive integer-pixel-stepped zoom looks visibly shaky/jittery at any speed and should never be used.
- Don't upscale a low-resolution source clip to fit — find a better-quality source instead.

## Keeping track across iterations — the manifest

Maintain a running manifest document alongside the deliverable: one row per beat, recording the in/out timecodes, the beat description, which asset is used, its approval status, and which version of the edit approved it — plus a running "removed, do not re-add" list. Before every re-render of the edit, check the manifest to verify every previously-approved beat has survived the new cut. Approved B-roll should never silently disappear between versions of an edit.

## Workflow summary

1. Establish or load the relevant taste/preference profile and any brand research (target avatar, their language, any narrative "villain" or angle framing).
2. Read the full script/shot list; classify every beat into one of the routes above; cluster Action/Emotion beats into shared category slots.
3. Propose the routed sourcing plan (per-beat interpretation, route, and search language) and get it approved before sourcing anything — unless explicitly told to source everything immediately, in which case that instruction is the approval.
4. Execute: run the sourcing process for Action/Emotion beats (search → download candidates → automated visual gate → contact sheets); do batched single-candidate sourcing for the objective routes; compile a build list for Graphics beats (these are never sourced, only built).
5. Deliver contact sheets, a vetted shortlist, a match report, and flags for any beat that had to ship dry. The human makes the final picks.
6. Optionally: place the picked clips on the word, render, do a final self-check by tiling frames at every cut point and every joint and visually reviewing them, and update the manifest.

---

## Direct-response ad fork — additional profile, rules, and specifics

This section describes a more specialized version of the above, tuned specifically for direct-response video ads (UGC/VSL/native style, continuous voiceover, vertical 9:16 format) rather than general talking-head YouTube content. It layers a specific "taste profile" — a set of empirically-derived defaults about what a winning direct-response ad's B-roll actually looks like — on top of the general methodology above.

### The taste profile, and where it came from

This profile was derived two ways: (1) frame-sampling actual winning direct-response reference ads and cataloguing every single cutaway shown, and (2) documented standing brand rules (always use real footage for action B-roll, always match the on-camera talent's age to the actual target avatar, never fabricate a citation, and other product-truth rules specific to the brand in question).

**Layer mix observed in one winning 4-minute native-VSL-style reference ad:**

| Layer | Share of runtime | Sourcing route |
|---|---|---|
| Talking-head avatar/presenter | ~57% | not sourced — this is the on-camera talent |
| Action B-roll (real people doing things) | ~25% | Action/Emotion route (organic social footage) |
| Graphic overlays | ~14% | Graphics — always built, never sourced |
| Institutional stock (doctor/lab) | ~4% | Institutional route (licensed stock) |

- Roughly 20-24 distinct action clips were used across that 4-minute ad, with several clips reused more than once — so plan to source 30-40+ verified usable clips per ad of similar length, and expect to review 3-5x that many raw candidates given typical rejection rates.
- **Every clip shows an action, never a static pose** — sweeping, scrolling, pinching, walking away, eating. Even a "doing nothing" moment has a physical anchor (leaning on an elbow, holding a mug).
- **Shoot the aftermath, never the acute symptom itself** — the feeling should be carried by posture and context (slumped in a recliner having given up) rather than by depicting the actual medical/painful event.
- **Faces are often absent or obscured** — shot from behind, waist-down, or hands-only. This reads as universal and lets the viewer project themselves into the footage; these are also the most reusable clips in a library since they're not tied to one specific face.
- **Deliberately rough, amateur-looking footage is itself part of what makes it credible** — genuine phone footage, imperfect lighting, ordinary cluttered rooms. Highly polished, ring-light-lit creator footage actively undermines a native-style ad's credibility.
- **Age-matching is non-negotiable** — every on-camera subject should match the target avatar's actual age range. A single visibly off-age clip can undermine the credibility of the whole ad.

**Pacing guidance (from studying reference ads):** a new cutaway every 2.5-4 seconds; no cutaway held longer than ~7 seconds; the avatar/presenter never left uncovered for more than ~10 seconds; captions (if used) appear phrase-by-phrase, bold condensed all-caps on a solid background box. Audio should never stop for a visual beat — every cutaway stays silent under the one continuous voiceover.

### Trusted sourcing routes by category

- **Action/Emotion (the dominant category)** → organic short-form social video, sourced via a structured plan: search using the target avatar community's own actual language (their real phrasing, not marketing-speak or stock-footage language), download candidates, run them through a visual matching gate, present as contact sheets. General short-form platforms skew toward younger, comedic content by default, so search terms need to be explicitly anchored to the target age group and the specific community/genre in question every time.
- **Institutional (doctor/lab)** → licensed stock footage libraries, or scoped search of official/authoritative channels. Polished footage is *correct* here — the one exception to the "rough footage reads as authentic" rule.
- **Concept/Mechanism (3D medical visuals, diagrams)** → stock animation libraries, or image-to-image generation seeded from a real reference diagram (never generate this kind of visual from a blank text prompt with no reference).
- **Receipts (posts, headlines, reviews)** → real artifacts only, captured as clean screenshots. See guardrails below.
- **Product** → the brand's own real asset library only — this is never sourced from anyone else's footage.

### Guardrails (these are hard laws, not style preferences)

- **Action B-roll is always real footage, never AI-generated.** A beat with no available real footage gets dropped or flagged — it is never filled with AI-generated video. (The one explicit exception is 3D mechanism/concept animation, which genuinely wants a rendered/animated look.)
- **Product shots are never sourced from strangers' footage and never AI-generated** — brand assets only, and product accuracy (correct materials, colorways, packaging) always takes priority.
- **No fabricated citations in Receipts.** Never invent a study, statistic, sample size, percentage, or named doctor. A real post/headline/review gets screenshotted as-is. A deliberate mockup that the brief explicitly calls for is a Graphics build, executed exactly to the brief's spec, and is never presented as though it were a sourced real artifact.
- **Audio is always silent on sourced clips** — the one continuous voiceover carries all audio; every clip's own audio is stripped.
- **Native burned-in captions/watermarks on sourced organic clips are acceptable by default** in raw-UGC-style ads — they read as authenticity. A specific project's sourcing rules always take precedence when they say otherwise.
- **Competitor branding is shown on screen only when the concept explicitly calls for it** (e.g. a deliberate "villain" comparison shot); otherwise it should be cropped out or the clip rejected.
- **Format defaults:** vertical 9:16, download longer segments than strictly needed (8-15 seconds even for a 2-second need) so the editor has room to choose the exact in/out point; deliver the trimmed best segment with roughly 1.5 seconds of handle padding on each side.
- **A hard visual-matching gate plus the visual-subject test are non-negotiable** — footage of the action, never footage about the topic; every contact sheet gets a human visual audit before the client/stakeholder sees anything; the human makes the final picks, always.

### Defaults for this fork

- **Default genre:** direct-response video ad (UGC/VSL/native), 60 seconds to 4 minutes, one continuous voiceover track.
- **Default output:** silent clips, vertical 9:16, trimmed to the best segment plus ~1.5-second handles, organized per script-beat slot with contact sheets and a match report.
- **Always load brand/avatar research first** — the avatar profile sets the required age band, the voice-of-customer research sets the search language, and the creative brief sets any "villain" framing.
