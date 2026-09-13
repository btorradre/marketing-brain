# Direct-response ad fork — taste profile, guardrails, and defaults

This reference tunes the general B-roll Finder methodology specifically for direct-response video ads (UGC/VSL/native style, continuous voiceover, vertical 9:16 format) rather than general talking-head YouTube content. It layers a specific "taste profile" — a set of empirically-derived defaults about what a winning direct-response ad's B-roll actually looks like — on top of the general methodology.

## Where this profile comes from

Two sources: (1) frame-sampling actual winning direct-response reference ads and cataloguing every single cutaway shown, and (2) documented standing brand rules (always use real footage for action B-roll, always match the on-camera talent's age to the actual target avatar, never fabricate a citation, and other product-truth rules specific to the brand in question).

## Layer mix observed in one winning 4-minute native-VSL-style reference ad

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

## Trusted sourcing routes by category

- **Action/Emotion (the dominant category)** → organic short-form social video, sourced via a structured plan: search using the target avatar community's own actual language (their real phrasing, not marketing-speak or stock-footage language), download candidates, run them through a visual matching gate, present as contact sheets. General short-form platforms skew toward younger, comedic content by default, so search terms need to be explicitly anchored to the target age group and the specific community/genre in question every time.
- **Institutional (doctor/lab)** → licensed stock footage libraries, or scoped search of official/authoritative channels. Polished footage is *correct* here — the one exception to the "rough footage reads as authentic" rule.
- **Concept/Mechanism (3D medical visuals, diagrams)** → stock animation libraries, or image-to-image generation seeded from a real reference diagram (never generate this kind of visual from a blank text prompt with no reference).
- **Receipts (posts, headlines, reviews)** → real artifacts only, captured as clean screenshots. See guardrails below.
- **Product** → the brand's own real asset library only — this is never sourced from anyone else's footage.

## Guardrails (these are hard laws, not style preferences)

- **Action B-roll is always real footage, never AI-generated.** A beat with no available real footage gets dropped or flagged — it is never filled with AI-generated video. (The one explicit exception is 3D mechanism/concept animation, which genuinely wants a rendered/animated look.)
- **Product shots are never sourced from strangers' footage and never AI-generated** — brand assets only, and product accuracy (correct materials, colorways, packaging) always takes priority.
- **No fabricated citations in Receipts.** Never invent a study, statistic, sample size, percentage, or named doctor. A real post/headline/review gets screenshotted as-is. A deliberate mockup that the brief explicitly calls for is a Graphics build, executed exactly to the brief's spec, and is never presented as though it were a sourced real artifact.
- **Audio is always silent on sourced clips** — the one continuous voiceover carries all audio; every clip's own audio is stripped.
- **Native burned-in captions/watermarks on sourced organic clips are acceptable by default** in raw-UGC-style ads — they read as authenticity. A specific project's sourcing rules always take precedence when they say otherwise.
- **Competitor branding is shown on screen only when the concept explicitly calls for it** (e.g. a deliberate "villain" comparison shot); otherwise it should be cropped out or the clip rejected.
- **Format defaults:** vertical 9:16, download longer segments than strictly needed (8-15 seconds even for a 2-second need) so the editor has room to choose the exact in/out point; deliver the trimmed best segment with roughly 1.5 seconds of handle padding on each side.
- **A hard visual-matching gate plus the visual-subject test are non-negotiable** — footage of the action, never footage about the topic; every contact sheet gets a human visual audit before the client/stakeholder sees anything; the human makes the final picks, always.

## Defaults for this fork

- **Default genre:** direct-response video ad (UGC/VSL/native), 60 seconds to 4 minutes, one continuous voiceover track.
- **Default output:** silent clips, vertical 9:16, trimmed to the best segment plus ~1.5-second handles, organized per script-beat slot with contact sheets and a match report.
- **Always load brand/avatar research first** — the avatar profile sets the required age band, the voice-of-customer research sets the search language, and the creative brief sets any "villain" framing.
