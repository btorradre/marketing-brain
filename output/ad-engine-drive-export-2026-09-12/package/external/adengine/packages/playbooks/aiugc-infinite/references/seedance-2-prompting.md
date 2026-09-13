# Seedance 2.0 — Image-to-Video Prompting Reference

Working reference for DR marketers using Seedance 2.0 (ByteDance Seed) as Cut 2 of a two-cut UGC ad — talking-head (Cut 1) hard-cuts to creator-with-product (Cut 2) seeded from Cut 1's last frame. Identity continuity is non-negotiable.

---

## 1. Prompt structure (image-to-video)

When a start frame is supplied, **stop describing what the image looks like — describe what moves**. Seedance already sees the frame; tokens spent re-describing the creator, the kitchen, or the bottle are wasted.

The canonical 6-block formula (Apiyi/ByteDance docs):
**Subject action → environment motion → camera → lighting cue → style/genre → constraints**

For UGC Cut 2, collapse to a leaner 4-block:
```
[UGC anchor] + [creator action on product] + [single camera move] + [identity lock + negatives]
```

Target length: **60–120 words**. Past ~150 words you start getting conflicting instructions and degraded motion.

UGC anchor (always lead with this — biases the model toward phone footage and away from cinematic gloss):
> `UGC creator, iPhone handheld, harsh midday window light, slightly imperfect framing,`

---

## 2. Multi-shot in one generation

Seedance 2.0 reads explicit shot markers:
- `Shot 1: ... Cut to: Shot 2: ...` (cleanest, recommended)
- `[00:00–00:05] ... [00:05–00:10] ...` (timestamp = hard editorial cut)
- `lens switch` (legacy 1.0 Pro phrase, still parsed)

**For UGC Cut 2 you almost never want multi-shot inside Seedance.** Multi-shot eats fidelity and Seedance's identity-lock works best when animating one continuous beat off your seed frame. Stitch Cut 1 → Cut 2 in FFmpeg instead. Reserve multi-shot for B-roll generators.

---

## 3. The `genre` parameter (Higgsfield)

`auto / action / horror / comedy / noir / drama / epic`. Post-prompt aesthetic bias, not hard switch.

For DR UGC, **always use `auto` or `comedy`**. `action`/`epic` introduce speed-ramps and dramatic push-ins that destroy "girl-in-her-kitchen" believability. `drama` adds a teal-orange cast that screams AI. `noir` and `horror` are useless here.

---

## 4. `std` vs `fast`

| Mode | 720p i2v | Speed | Use when |
|---|---|---|---|
| `std` | ~$0.30/sec | <2 min | Final hero ad, product label has to read clean |
| `fast` | ~$0.24/sec | ~30–50% faster | Concept testing, A/B variants, first-pass batch |

`fast` is good enough for ~80% of UGC Cut 2 work. Same motion model — what you lose is ~10–15% on text-on-product fidelity and fine hand articulation. Run `fast` first, regen winners on `std`.

---

## 5. Resolution sweet spot

- **480p** — prototyping only. Faces drift faster.
- **720p** — production sweet spot for Meta/TikTok feed. **Default.**
- **1080p** — diminishing returns; pricing scales per second; only for top-of-funnel polish.

DR iteration: 720p `fast` → pick winners → 720p `std` final. Skip 1080p unless buyer asks.

---

## 6. Duration

Range: **4–15s**, or `auto`.
- 5s = one beat (lift bottle to mouth, drink, set down). Best identity retention.
- 8–10s = two beats (open jar, scoop, reaction). Drift starts.
- 12–15s = multi-shot territory. Don't run Cut 2 here.

**For UGC Cut 2: 5–6s.** Hard rule.

---

## 7. Audio role

Seedance 2.0 generates **native synchronized audio** — phoneme-level lip-sync, ambient SFX reactive to visuals, optional music bed. Three ways:

1. **Generate from prompt:** describe SFX inline — `soft cap-pop, liquid pour, gentle ice clink`. No music for UGC.
2. **Provide audio reference** (uploaded WAV/MP3 ≤15s): model lip-syncs and beat-matches to it.
3. **Tag the role** as `voiceover` or `ambient` so the model knows whether to lip-sync or just match pacing.

For Cut 2 in two-cut UGC, **default to no dialogue, just ambient SFX**: `no music, only raw room tone and product SFX, no narration`. Keeps Cut 1's voiceover dominant in the final stitch.

---

## 8. Identity consistency from seed frame

This is what Seedance 2.0 is genuinely SOTA at — but it still drifts past 6s, and it drifts faster when the prompt fights the image. Lock-in tactics:

- **Don't re-describe the creator.** Don't say "blonde woman in white t-shirt" if she's already in the seed frame.
- Append the explicit lock phrase: `maintain exact appearance from reference image, consistent character throughout, no deformation, no drift, no face morphing`.
- Keep camera motion *small* — orbit/dolly aggressively and the face re-renders. `slow handheld, minimal camera motion` preserves identity.
- Center the subject. Faces near frame edges warp first.
- If you have both Cut 1 last frame *and* a Cut 2 end-state image, use `end_image_url` (fal/Replicate) — A→B locks both ends.

---

## 9. Motion vocabulary

Verbs Seedance executes literally: **picks up, lifts, tilts, unscrews, twists, pours, scoops, dispenses, snaps, pumps, dabs, rubs, sips, drinks, sets down, spreads, shakes, smiles, glances, nods**.

Verbs it ignores or fudges: "uses", "interacts with", "enjoys", "experiences", "showcases" — too abstract. Replace every abstract verb with one concrete physical verb.

Compared to Kling 3.0: Kling is looser/more interpretive (great for vibes), Seedance more literal (great for product action). If you want a specific physical beat to happen, Seedance.

---

## 10. Camera vocabulary

The 8 primitives (only ever pick **one** per generation — multiple = jitter):

`slow dolly in` · `slow dolly out` · `pan right/left` · `tracking shot following hands` · `slow orbit` · `aerial / overhead` · `handheld` · `locked-off / fixed camera`

For UGC Cut 2, the only two you should ever use are **`handheld, minimal motion`** and **`locked-off, fixed camera`**. Anything else screams agency-produced.

---

## 11. Prompt length

- 5s single-action: 2–4 sentences (~50–80 words)
- 10s two-beat: 4–6 sentences (~120 words)
- Past 150 words, dropped/merged instructions. Past 250, output degrades visibly.

---

## 12. Failure → fix

| Failure | Cause | Fix |
|---|---|---|
| Face morphs/drifts | Camera moving too much; clip too long | `handheld, minimal motion`; cap at 5–6s |
| Hands warp / 6 fingers | Complex hand-product interaction + fast motion | Slow the verb (`slowly lifts`); keep hands fully in frame |
| Product label gibberish | Logo near edge; reflections; rotation | Center logo with margin; clean reflections in source; avoid orbit/rotate; add `keep label perfectly readable, no garbled text, no logo morphing` |
| Product re-rendered as wrong shape | Re-described product in prompt | Stop describing product. Let seed frame define it. Only describe action |
| Video stays static | No concrete verb; abstract motion | Replace abstract verbs with physical (`unscrews cap` not `opens product`) |
| Plasticky AI gloss / slow-mo | Default cinematic bias; 1080p + dramatic camera | Lead with `UGC creator, iPhone handheld, harsh window light`; `genre: auto`; add `no slow motion, real-time pacing, natural imperfect motion` |
| Background hijacks attention | Scene re-rendered each frame | `static background, only [subject/hands] move` |
| Two camera moves blend into jitter | Multiple camera verbs | Pick one. Negate the rest: `no zoom, no pan, only slight handheld jitter` |

---

## 13. UGC Cut 2 templates (copy/paste)

**Template A — Drink/sip a supplement**
```
UGC creator, iPhone handheld, harsh window light, kitchen background.
She unscrews the cap, lifts the bottle, takes a small sip, lowers it,
half-smiles at camera. Locked-off camera, minimal handheld jitter.
Ambient room tone, soft cap-click and liquid sip SFX, no music.
Maintain exact appearance from reference image, no face morphing,
no logo morphing, keep label readable. 5s, 720p, 9:16.
```

**Template B — Pour into hand / scoop**
```
UGC creator, handheld iPhone POV, bathroom counter daylight.
She tilts the jar, taps two gummies into her open palm, looks down at them.
Camera locked, only hands and jar move, static background.
Soft tap and rattle SFX, no music, no narration.
Lock identity to reference image, no drift, no warping hands,
keep label perfectly readable, no garbled text. 5s, 720p, 9:16.
```

**Template C — Unbox / open**
```
UGC creator, handheld phone, bedroom soft daylight.
She slides the lid off the box, peels back tissue paper, lifts the bag
out by the handle, holds it up beside her face, raises eyebrows.
Slow handheld, subtle natural shake, no zoom, no pan.
Soft paper rustle and box-thunk SFX, no music.
Maintain exact appearance and product from reference image,
no deformation, no extra props invented. 6s, 720p, 9:16.
```

**Template D — Wear / try on (fashion)**
```
UGC creator, mirror selfie iPhone handheld, bedroom natural light.
She lifts the strap onto her shoulder, adjusts it, turns slightly side
to side, glances down at the bag, back up to mirror.
Locked-off, only subject moves, no orbit, no zoom.
Fabric rustle and strap-creak SFX, no music.
Lock face and outfit to reference image, no morphing,
keep hardware and stitching detail consistent. 6s, 720p, 9:16.
```

---

## 14. Product fidelity anchoring

- **Source image rules:** 2000+px long edge, sharp, flat lighting, logo centered with margin, reflections cleaned. Garbage seed → garbage Cut 2.
- **Negate explicitly** every gen: `no logo morphing, no garbled text, no warped label, no color shift, no extra products invented`.
- **Avoid rotational moves** on the product (orbit, 360, dolly arc) — the #1 cause of label scramble. Linear lifts/tilts/pours are safe.
- If label still scrambles at 720p `std`, you're asking for too much motion. Cut duration to 4s or freeze product and only animate creator.

---

## 15. The "natural / organic" look

Seedance defaults toward smooth/cinematic — fight that for UGC. Required cues:

`UGC creator · iPhone handheld · harsh window light / harsh midday sun · slightly imperfect framing · real-time pacing, no slow motion · subtle natural handheld jitter · no music, only ambient room tone · no color grading, no cinematic look`

No exact "rolling shutter" toggle, but the phrases above approximate it. Combined with `genre: auto` and 720p (not 1080p), output reads as phone footage ~85% of the time.

---

## 16. When to pick Seedance vs Kling 3.0 vs Veo 3.1

| Use case | Pick |
|---|---|
| UGC Cut 2 with literal product action seeded from last frame | **Seedance 2.0** — best motion literalism, best identity from single seed, native audio |
| Multi-shot mini-story with consistent character (no FFmpeg stitch) | Kling 3.0 — Elements (4 refs) + storyboard beats Seedance for cross-shot identity |
| Cinema-grade hero with native dialogue + broadcast color | Veo 3.1 — cleanest motion + audio, but expensive and over-polished for UGC |
| Fast batch UGC variants for A/B | Seedance 2.0 `fast` 720p — cheapest serviceable motion + native audio in one pass |
| Creator talking while using product (lip-sync to existing VO) | Seedance 2.0 with audio role = voiceover; Veo 3.1 second |

**Production default for two-cut UGC Cut 2:** Seedance 2.0 `fast` at 720p, 5s, `genre: auto`, locked-off or handheld camera, one concrete action verb, aggressive identity-lock negatives.

---

**Sources:** ByteDance Seed Seedance 2.0 docs, fal.ai Seedance 2.0 model page, Replicate Seedance models, Higgsfield Seedance 2.0 page, Apiyi Seedance prompt formula, Atlabs Seedance prompting guide, Reddit r/aivideo + r/StableDiffusion Seedance threads.
