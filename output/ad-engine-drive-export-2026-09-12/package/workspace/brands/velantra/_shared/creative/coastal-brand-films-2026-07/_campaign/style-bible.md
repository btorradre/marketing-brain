# Coastal Brand Films — Campaign Style Bible

**Campaign:** VEL coastal brand films (Son of a Tailor documentary format)
**Applies to:** VEL-NOLOGO-FILM-01, VEL-SCAM-FILM-02, and any later film in this family
**Reference look:** `../reference-teardowns/son-of-a-tailor-portugal/` — study frames beat_001 (landscape hook), beat_004–007 (portrait grammar), beat_009/012 (macro craft), beat_013/020 (faded archival), beat_022 (artifact money shot)

## The look (high production, SoaT register)

Premium documentary commercial. Natural available light only. Static or near-static confident frames — the camera never begs for attention. Muted coastal palette: warm sand, taupe, navy, sea glass, weathered gray shingle, terracotta accent. Real skin texture, real fabric texture. Filmic highlight rolloff, gentle contrast. NOTHING glossy, HDR, oversaturated, or influencer-lit.

### VERBATIM GLOBAL STYLE BLOCK — paste into every keyframe prompt (marker: {{STYLE}})

> premium documentary commercial photograph, shot on a cinema camera with a 50mm prime lens, shallow depth of field, natural available light only, muted coastal color palette of warm sand, taupe, navy and sea glass, soft filmic highlight rolloff, true to life skin and fabric texture, quiet confident composition, vertical 9:16 full frame, photorealistic, no oversaturation, no HDR glow, no plastic skin, no studio lighting, no text or lettering anywhere in the image

### VERBATIM FADED-FILM BLOCK — flashback/archival shots only (marker: {{FADED}})

> sun faded 1990s film photograph look, desaturated cool blue cast, soft focus edges, fine grain, subtle light leak at frame edge, nostalgic archival quality, slightly overexposed highlights

Snap-back rule (from the reference): flashback shots carry {{FADED}}; the very next present-tense shot returns to full {{STYLE}} crispness. The grade change IS the time-travel — never mix the two looks in one shot.

### VERBATIM VIDEO MOTION FOOTER — paste into every Seedance prompt (marker: {{MOTION}})

> slow deliberate movement only, camera locked on a tripod with subtle natural drift, natural ambient sound, no cuts, no zooms, no transitions, no camera shake, premium documentary commercial aesthetic, vertical 9:16, ONE CONTINUOUS SHOT

Per-shot motion lines go BEFORE the footer and stay minimal: one subject action or one slow camera move per clip, never both stacked.

## Hard production laws

1. **Engines/modes:** GPT Image 2 i2i keyframes (kie.ai, never Nano Banana) → Seedance 2.0 `std`, 720p, 9:16. Fast mode banned. EVERY i2v clip generated at 6s; edit trims to the 2–5s cadence targets in the brief.
2. **Frame-first, always:** keyframe generated and QA-passed BEFORE animation (pre-animation gate). Never animate an unaudited frame.
3. **Frame-QA subagent pass** on every frame containing a Velantra bag (fresh-context agent, checklist at `../claymation-brand-films-2026-07/_campaign/qa-checklists.md` + canonical ref + frame). Video clips: audit ≥3 extracted frames (start/mid/end). FAIL → regenerate with blocks pasted, cap 3, then change blocking.
4. **Closure-interaction law:** never animate hands opening/closing/working a flap or strap. Closure-state changes happen across HARD CUTS between two separately audited stills. In-motion shots keep the closure state frozen.
5. **Product truth blocks:** each product's verbatim identity block (and flap/mechanism block when the bag is open, carrying, or the flap is in motion) pasted into every prompt containing that bag — pulled from `velantra-straw-tote`, `velantra-weekender`, `velantra-boat-tote`, `velantra-meridian` skills. No paraphrasing.
6. **No text in generated frames.** All lettering — location super, captions, end card, the embossed VELANTRA on the inner tag — is composited in post. Generate blank surfaces (plain debossed leather tag, blank signage) and comp the type.
7. **Prompt hygiene:** no em dashes or ellipses inside prompts, never the word "Birkin", no origin words (kie runner claims-grep hard-fails), no real brand names or recognizable branded products ("anonymous status bag" prompts must specify a fictional logo free luxury bag).
8. **Late-clip drift law:** Seedance drifts in the back half — trim targets sit inside the first 4s of each 6s clip. Any clip that mutates product geometry or identity: regenerate once, then fall back to audited-still Ken Burns for that beat.
9. **No logos on bag exteriors, ever.** The only brand mark that exists anywhere is the comped inner-tag emboss and post-comp supers.

## Sound

- **VO:** ONE seamless full-length ElevenLabs track, premium brand "we" voice — calm, unhurried, quietly confident, low-register warmth, never announcer. Generate one male and one female read of the full script; pick per film. ~2.3–2.4 words/sec pacing with real breath pauses at act turns.
- **Music:** minimal warm ambient (felt piano / soft strings), starts under beat 1, almost disappears during the mechanism block, gentle swell into the ring close. Licensed (Artlist), mixed −18 to −14 LUFS under VO.
- **Diegetic layer:** low ambient bed per scene (gull + rope + water for harbor, room tone + cutlery for patio, fabric/paper for macros). Seedance native ambience kept where clean; replaced in the mix where not.

## Type & post

- **Location super (hook only):** NEWPORT BEACH, CALIFORNIA — small caps, tracked wide, white, top third, fades by 0:04. This replaces the reference's founder title card as the documentary-authority device.
- **Captions:** reference grammar — small white bottom-center sentence fragments, cut-synced to the VO clause, sentence case, no emphasis colors, no word-by-word pop.
- **End card:** hero bag packshot (audited still) + VELANTRA wordmark + velantrafashion.com, 2s, silence-then-music-button.
- **Grade:** single warm-neutral grade pass across present-tense shots so multi-engine output reads as one film; faded shots graded separately per {{FADED}}.

## Cast

Portrait-gallery women from the locked 5-avatar roster (Blair, Sloane, Marin, Tessa, Camille) — assignment per brief. Ages read 35–55, coastal-affluent wardrobe (linen, cashmere, canvas — no logos anywhere on wardrobe either).
