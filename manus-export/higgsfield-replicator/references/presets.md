# Higgsfield Marketing Studio — Preset Routing

The 9 presets are the entire creative surface of Marketing Studio Video. Pick exactly one based on the reference ad's format. Hooks/settings only apply to the UGC family.

## Decision Tree

Run through these tests **in order** — first match wins.

1. **Is the reference a CGI / hyperlapse / object-flying-through-effects clip with no person speaking?**
   → `product_showcase` (UI label: "Hyper Motion")

2. **Is it a multi-scene narrative ad with story beats (problem → solution → reveal), 20-60s, polished cinematography?**
   → `TV Spot`

3. **Is the entire ad someone unwrapping/opening a box and revealing the product?**
   → `Unboxing`

4. **Is it a step-by-step "how to use / do this with the product" demo?**
   → `ugc_how_to` (UI label: "Tutorial")

5. **Is it a sit-down "I tried this for X days" / star-rating / pros-and-cons review?**
   → `Product Review`

6. **Is the person trying on clothes/accessories — selfie, casual?**
   → `UGC Virtual Try On`

7. **Is the try-on cinematic / editorial / fashion-runway style?**
   → `Pro Virtual Try On`

8. **Is the reference surreal, weird, stunt-driven, viral-bait, or doesn't fit any preset above?**
   → `Wild Card`

9. **Default fallback: selfie-style talking head, casual delivery, single take.**
   → `UGC`

## Preset Compatibility Matrix

The slug below is what you pass to `higgsfield generate create marketing_studio_video --mode <slug>`. (The Marketing Studio UI surfaces names like "Tutorial" and "Hyper Motion" — the CLI mode enum uses `ugc_how_to` and `product_showcase` for those. Always use the CLI slug.)

| UI label | `--mode` slug | Hook/Setting? | Avatar? | Product Required? | Best Use |
|---|---|---|---|---|---|
| UGC | `ugc` | YES | YES | YES | Talking-head selfie ads (rapid-VSL style) |
| Tutorial | `ugc_how_to` | YES | YES | YES | "How to use" demos, step-by-step |
| Unboxing | `ugc_unboxing` | YES | YES | YES | Box reveals, ASMR unwraps |
| Product Review | `product_review` | YES | YES | YES | Sit-down reviews, rating cards |
| UGC Virtual Try On | `ugc_virtual_try_on` | YES | YES | YES (apparel) | Casual selfie try-ons |
| Hyper Motion | `product_showcase` | NO | NO | YES | CGI, slow-mo, product hero shots |
| TV Spot | `tv_spot` | NO | YES | YES | 30s narrative commercials |
| Pro Virtual Try On | `virtual_try_on` | NO | YES | YES (apparel) | Cinematic editorial try-ons |
| Wild Card | `wild_card` | NO | optional | YES | Surreal, viral-bait, custom ideas |

Get the live enum any time: `higgsfield model get marketing_studio_video --json | jq '.params[] | select(.name=="mode")'`

## Brand → Preset Defaults

When asked for "a Higgsfield ad for <brand>" without a reference, default to:

| Brand | Default Preset | Why |
|---|---|---|
| Motilli (gummies) | `UGC` or `Product Review` | Health-supplement avatars sell with talking-head reviews |
| Lunessa (heart health, 50+ female) | `Product Review` or `UGC` | Avatar credibility wins; story-driven works too |
| Velantra Boat Tote | `UGC Virtual Try On` or `Hyper Motion` | Either casual try-on or hero CGI showcase |
| Velantra Meridian | `Pro Virtual Try On` or `TV Spot` | Premium leather → editorial framing |
| Velantra Weekender | `UGC` | Travel-day-in-the-life selfie POV |
| Avelle | `UGC` or `Product Review` | (Confirm with user — depends on positioning) |
| Solorna | (TBD per category) | (Confirm with user) |

Override these whenever the reference clearly fits a different preset. Add rows here for any new brand you onboard — the pattern is: default preset + one line on why it fits that brand's positioning.

## Reference-Type → Preset Examples

| Reference description | Preset |
|---|---|
| UGC car-yapper ad (talking into phone camera while driving) | `UGC` |
| Animated "inside the body" 3D mechanism ad | `Wild Card` (custom prompt) — Higgsfield doesn't have a native animated-3D preset |
| Talking-head doctor/expert explaining a mechanism | `UGC` (with authority avatar) or `Product Review` |
| 30s broadcast spot with dramatic music | `TV Spot` |
| Slow-mo product splash into water with ingredients flying around | `Hyper Motion` |
| "I tried this for 14 days, here's what happened" before/after | `Product Review` |
| Outfit-of-the-day featuring a bag or accessory | `UGC Virtual Try On` |
| Editorial fashion-magazine-style shoot featuring a premium handbag | `Pro Virtual Try On` |
| Recipe video using a kitchen product | `Tutorial` |
| Box reveal + unwrapping + product discovery | `Unboxing` |
| Surreal "person casually reviewing the product in an absurd location" | `Wild Card` (or `UGC` + an unrealistic setting) |

## Multi-Scene Reference Strategy

If the reference is a multi-scene 30-60s video (narrative ad), do NOT try to recreate every scene in one Marketing Studio call. Either:

- **Option A — `TV Spot` preset, single call**: Adapt the entire script into one prompt and let Marketing Studio's TV Spot template handle multi-scene production. Best for cinematic refs.
- **Option B — chained UGC clips**: Split the reference into 5-second beats, generate each as a separate `UGC` clip, then stitch externally with FFmpeg. Use this when avatar consistency across all clips matters more than cinematic flow. Pin the same Soul Character + setting_id across all clips.

For animated/3D references that don't match any Higgsfield preset, fall back to a general video-generation model (e.g. Veo) outside Marketing Studio — Higgsfield has no native 3D animation preset.
