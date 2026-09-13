# Kling 3.0 — Image-to-Video Prompting Reference

Working reference for DR marketers running Kling 3.0 (Kuaishou) via Kling AI API, fal.ai, kie.ai, and Higgsfield's `kling3_0`. Focus: animating static product/lifestyle stills into UGC-feeling motion that converts.

---

## 1. Image-to-video prompt structure

When a start frame is supplied, the still IS the subject. The prompt describes **motion, not subject**. Repeating "woman holding red bottle" burns tokens and pulls the model toward re-imagining what's already locked. Optimal stack, in order:

1. **Camera move** — "slow dolly push, ~5% zoom"
2. **Primary subject motion** — what the human/product actually does
3. **Secondary/ambient motion** — hair, fabric, steam, dust, background bodies
4. **Texture/imperfection cues** — handheld jitter, rolling shutter, focus drift, grain
5. **End-state** (only if the clip stalls) — "settles back to original framing"

The fal.ai and Kling-AI docs converge on a "Camera Movement + Scene Setup + Subject Action + Vibe + Time/Audio" formula; for i2v drop "Scene Setup" because the frame already provides it.

## 2. Motion vocabulary cheatsheet

**Camera verbs Kling 3.0 reliably honors:** `dolly in slow`, `dolly push`, `pull back`, `whip-pan`, `tilt up/down`, `orbit left`, `crane up`, `crash zoom`, `snap focus`, `rack focus`, `shoulder-cam drift`, `static tripod`, `handheld follow`. Compound with `while` or `as`.

**Subject motion verbs that work:** `accelerates`, `weight transfers to left foot`, `exhales`, `tilts head 15° right`, `lifts product to chest height`, `rotates jar 90° clockwise`, `unscrews cap`. Specific over generic.

**Words Kling ignores or muddles:** `moves`, `goes`, `does something`, `interacts`, `looks nice`, `cinematic`. Generic verbs produce mush.

**Texture cues that materially change output:** `subtle handheld jitter`, `rolling shutter wobble`, `eye-focus drift`, `background motion blur`, `fabric ripples in breeze`, `steam rises and curls`, `condensation drip`, `dust motes float`, `lens breathing`, `35mm film grain`, `skin pores visible`, `slight chromatic aberration`. These are the difference between glossy AI-render and "real phone footage."

## 3. Prompt length

**≤2 sentences is the sweet spot for i2v.** Long prompts fight the start frame. fal/Tona docs explicitly: "Kling can work great without the prompt — add small details when you need exact camera or action control." If past 60 words, you're over-cooking it.

## 4. `std` vs `pro` mode

| | std | pro |
|---|---|---|
| Cost (no audio) | ~$0.168/sec | ~$0.224/sec |
| Cost (audio on) | ~$0.252/sec | ~$0.336/sec |
| Strength | Speed, iteration, scale | Motion fidelity, polish, fewer failed runs |
| Use for | Concept exploration, A/B testing hooks, scrappy UGC | Hero ads, product close-ups, character-heavy shots |

Workflow: explore in `std`, finalize hero shots in `pro`. Pro reduces re-rolls.

## 5. Sound `on` vs `off`

Native audio (rolled in via Kling 2.6's audio engine, carried into 3.0) generates **dialogue (lip-synced if face is in frame), SFX synced to motion events, and ambient bed (room tone, wind, traffic) — all in one pass**.

- **Dialogue:** quote the line: `the woman says "I cannot believe this actually worked"`. Lip-sync to source face.
- **SFX:** name the action sound — `the cap clicks open with a soft pop`, `gummies rattle inside the jar`.
- **Ambient:** name the room — `quiet kitchen ambience, refrigerator hum`, `car interior with faint engine idle`.

Turn sound `off` when dubbing ElevenLabs over the top. Turn it `on` for talking-head UGC where Kling-native dialogue beats lipsync-in-post.

## 6. Duration tradeoffs

Kling 3.0 supports 3–15s. Practical sweet spots:
- **5s** — highest frame-to-frame consistency, cheapest, best for product shots, hard cuts in fast UGC. **Default.**
- **6–8s** — medium-complexity (one subject + environment interaction).
- **10s** — only for simple scenes with one subject and a single clean motion arc. Multi-subject 10s clips drift.

Rule: 2+ subjects or rapid action → hard-cap 5–6s and chain in FFmpeg.

## 7. Aspect ratios

9:16, 16:9, 1:1 supported. No documented quality delta — but the start frame's AR drives the clip, so feed Kling the AR you want out.

## 8. Start-frame + end-frame mode

Pass both `--start-image` and `--end-image` for controlled interpolation. Rules:
- **Same aspect ratio on both frames** — mismatch causes stretch/crop.
- **Keep style/lighting/color close** — extreme jumps break the interpolation.
- **Minimal prompt** — start/end already define the arc.
- **Multi-clip sequences:** export last frame of clip N → start frame of clip N+1. Cleanest way to fake 15s+ shots.

Breaks when: faces rotate >45°, products change orientation, or one frame has motion blur and the other doesn't.

## 9. Camera control (API parameter)

Beyond text prompts, Kling exposes numerical sliders in Pro i2v: `horizontal`, `vertical`, `zoom`, `pan`, `tilt`, `roll`. **Keep values 1–3 for cinematic smoothness;** higher values distort. Presets (`pan`, `orbit`, `zoom`, `handheld`, `stationary`) via Prompt Dictionary panel + most third-party APIs.

## 10. Identity consistency

What helps:
- Toggle **"Bind Subject"** / Element Reference.
- Same start-frame-derived character description on every clip in a sequence (exact wording, not paraphrased).
- Negative prompts: `no morphing, no warping, no extra limbs, no face shift`.
- 5s clips, not 10s.

What breaks it:
- Multiple faces in frame.
- 360° head turns at 10s duration.
- Re-describing the face differently from frame to frame.

## 11. Common failure → fix

| Failure | Fix |
|---|---|
| Face morphs mid-clip | 5s only; Bind Subject; remove face descriptors; Pro mode |
| Plastic-skin slow-mo | Add `realistic skin texture, visible pores, natural micro-expression`; avoid `cinematic, dreamy, smooth` |
| AI face wobble (talking head) | Use Kling-native audio (sound on) instead of dub; keep mouth motion implied not described |
| Hands warp | Keep hands out of close-up; if in frame, prompt `hands stay still, fingers steady, no gesturing` |
| Product label gibberish | Don't fight it. Composite logo in post. Add `preserve product shape, maintain proportions` |
| Stuck at 99% / no motion | Add an end-state: `…then settles back into original frame` |
| Over-eager floaty motion | Strip prompt; rely on start frame; lower camera-control numerical values |
| Glossy AI-render feel | Add 4 imperfection cues (§12) |

## 12. The "4 organic imperfection cues" pattern — confirmed

The marketing-brain memory pattern (handheld jitter + rolling shutter + eye-focus drift + background motion) **maps directly to what every credible Kling guide recommends** under different labels. This isn't superstition — it's the documented difference between AI render and phone capture. Use it on every UGC clip.

## 13. UGC / talking-head pattern

```
Handheld iPhone selfie video, slight natural sway, rolling shutter wobble,
shallow depth of field, eye-focus drift. The woman speaks: "[line]". Subtle
breathing, micro-blinks, soft daylight from window behind camera. Background
slightly out of focus, faint refrigerator hum.
```

Open with how it was captured. Specify the device. Quote dialogue. Demand micro-behaviors. Name room sound.

## 14. Product-focused i2v pattern

```
Static tripod with subtle handheld micro-jitter. Steam rises and curls slowly
from the rim. Condensation forms a single drip on the glass. Soft window
light. Background blurred. 35mm grain.
```

Lock camera, give the product ONE motion event, let texture cues lift. Don't ask for camera + product motion + character motion in one 5s clip.

## 15. Ready-to-steal templates

**Car-yapper UGC (sound on, std, 5s, 9:16):**
```
Handheld phone selfie in car driver seat, slight sway with road vibration,
rolling shutter, eye-focus drift. She says: "[hook line]". Subtle blinks,
natural breath. Faint engine idle, soft seatbelt creak.
```

**Kitchen counter product reveal (pro, 5s, 9:16):**
```
Slow dolly push, 5% zoom, handheld micro-jitter. Steam rises from coffee mug
beside the bottle. Soft morning window light, dust motes float. 35mm grain.
```

**Gummy bottle being opened (pro, 5s, sound on, 1:1):**
```
Hands rotate the cap counter-clockwise 90°, soft click, cap lifts. Gummies
rattle gently inside. Static tripod, shallow focus on label. Preserve bottle
shape and proportions.
```

**Before/after pan (std, 5s, 16:9, end-frame mode):**
```
Slow horizontal pan left, steady. Soft daylight, no other motion.
```

**Fashion outfit walking shot (pro, 6s, 9:16):**
```
Tracking shot, shoulder-cam drift, follows subject from waist up. Fabric
ripples in stride, hair sways naturally. Shallow depth of field, golden hour
backlight, lens flare on left edge.
```

---

**Sources:** fal.ai Kling 3.0 prompting guide, Atlabs Kling 3.0 prompt guide 2026, glbgpt Kling 3.0 prompt guide, klingaio Kling 3 best practices, Atlas Cloud Kling 3.0 advanced prompts + character consistency, VideoAI Kling prompt mistakes, flaq.ai Kling 3 std vs pro pricing, Sequencer Kling Pro vs Standard, getimg.ai Kling 2.6 native audio review, Tona.AI Kling 3 start/end frame tutorial, Higgsfield Kling start/end frames, ComfyUI Kling camera controls, kie.ai Kling 3 motion control, glbgpt Kling camera movements 2026, ugcmaker Kling 3.0 UGC video guide, ugccopilot Kling 3.0 complete guide, Cliprise Kling 3.0 production-ready prompts.
