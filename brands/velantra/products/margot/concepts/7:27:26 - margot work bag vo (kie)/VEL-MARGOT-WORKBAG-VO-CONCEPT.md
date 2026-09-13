# VEL-MARGOT-WORKBAG-VO — Concept Overview

**Source concept:** Weekender AI VO series (`weekender/concepts/7:10:26 - weekender * vo (kie)/` + assembled finals in `aivo - 7:11:26/`) — the AI-voiceover-over-product-action-shots format currently working on the Velantra page.

**Adaptation:** Same format, repositioned for **The Margot Leather Tote** as **"the perfect work bag"** (locked positioning, 7/27). Three variations mirroring the proven Weekender trio.

---

## Anatomy of the source concept (why it works)

1. **Hook = the searching avatar's own query, mirrored back:** "If you're looking for the perfect summer travel bag…" — closes an open loop for a solution-aware shopper, no manufactured pain.
2. **Faceless, hands + product only.** No avatar identity to hold across shots. The bag is the only face.
3. **Every claim is shown while it's said.** "Holds its shape even packed full" plays over hands pressing structured sides. Claims never float.
4. **One AI VO voice** — warm female, early 40s, girlfriend energy — over hard-cut 9:16 iPhone-style clips, burned captions, name-drop of the product in the first 4 seconds, "link below" close.
5. **Three angles, one format:** Build (durability/hardware), Pack (capacity), Fit (colorways/urgency) — a testable mini-batch from one production setup.

## The three Margot variations

| ID | Angle | Length | Mirrors |
|---|---|---|---|
| `VEL-MARGOT-BUILD-VO-01` | Structure, grained leather, silver turn lock, daily-carry durability + ICP wound (heavy/flimsy work bags) | 22s (9+13) | Weekender BUILD |
| `VEL-MARGOT-FIT-VO-01` | Capacity — laptop, planner, charger, still closes; kills the laptop-bag-plus-tote shuffle | 20s (9+11) | Weekender PACK |
| `VEL-MARGOT-NEUTRALS-VO-01` | Six neutrals, one for every office outfit, under $100 close | 14s (single) | Weekender FIT |

## Key adaptation decisions (do not drift)

- **Name:** "the Velantra Margot" in VO, "The Margot Leather Tote" in any on-screen context. NEVER "Meridian" in copy (folder/handle only).
- **Product truth (verified vs live PDP 7/27 — overrides the stale skill description):** structured **OPEN-TOP** tote, **NO FLAP**, embossed swirling grain (never smooth, never generic pebble), slim flat top handles, front belt strap through **silver** keepers, two slotted clasp-plate ends meeting in a shallow V under a small square polished **silver** turn-lock. Soft tan interior, center zip pocket. **Silver hardware, never brass/gold** (the Weekender prompts say brass — that's the #1 swap-miss risk).
- **Scene world swap:** hallway console + car trunk + airport → home entry console + office desk + office lobby/commute.
- **Price truth:** $99.99 live, NO sale. "Under a hundred dollars right now" is approved language (locked 7/27 script). NEVER "they're having a sale" (the Weekender FIT line does — do not carry it over).
- **Colorway cycle (NEUTRALS v3):** six bags in one Seedance flat-lay = colorway-drift roulette. The segment generates burgundy-only; the six-neutral beat is cut in POST from the six live PDP stills (~0.5s each, Ken Burns), exactly like slot 9 of the 7/27 TOF UGC brief. We deliver the segment + the stills; editor drops them in.
- **Hero colorway:** Burgundy (variant 42827787173953).

## Production route (same as the Weekender run + Margot-specific laws)

- kie.ai Seedance 2.0, 9:16, native VO per segment. `@Image1` = creator hands/wardrobe ref, `@Image2` = live PDP burgundy hero (Shopify CDN URL direct).
- **Frame-QA every keyframe/clip vs the live PDP hero:** embossed grain (i2i drifts to generic pebble on first roll), colorway fidelity (coffee-brown shipped taupe-light on 7/27), silver-not-gold hardware, open top with no invented flap.
- **PROPORTION-AUDIT LAW:** measure body W:H against the burgundy PDP hero before shipping — wider than tall, top rim ≈ base width, never stretched tall/pinched.
- **ACTION-READS LAW (FIT v2 laptop beat):** bake the packed end-state into the keyframe, or chain first_frame (laptop above the mouth) → last_frame (settled inside). QA "does the action read?" separately from "is the product correct?" QA a t1.5/t2.0 frame ladder on that beat.
- **KEYFRAME-SEEDED ARTIFACT LAW:** same invented object at t0.2 across regens = regenerate the keyframe, not the video. Pre-audit the turn-lock/strap-plate zone at 8x.
- Captions burned in post (PIL overlay pipeline — local ffmpeg has no libass/drawtext). Captions transcribe VO word-for-word, lowercase, same style as the Weekender finals.
- Deliverables: raw segment clips + stills only. Brooks owns the timeline.

## Hard guardrails (every prompt, every frame)

No origin claims. No "Birkin"/"Hermes" spoken or shown. No other brand's bag in frame. No sale graphics/discount text. No flap, ever. No music in-gen (post only). Dialogue verbatim, commas and periods only.
