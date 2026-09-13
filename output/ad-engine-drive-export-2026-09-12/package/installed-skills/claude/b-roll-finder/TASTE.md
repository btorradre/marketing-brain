# TASTE.md — DR ad b-roll taste profile (Brooks)

Confirmed-by: Brooks (2026-08-17) — derived from standing laws in the marketing-brain memory and the MOT-GLP-SHUTDOWN reference teardown; say "redo my profile" to re-run onboarding.

> The curation layer [SKILL.md](SKILL.md) loads before sourcing anything. This fork is for
> **direct-response video ads** (UGC/VSL/native style) across Brooks's brands — not YouTube
> talking-head videos. The original Louise profile is gone; everything below is revealed from
> real winning-ad teardowns and Brooks's standing laws.

## Where this taste comes from

1. **Revealed fingerprint** — frame-sampled teardowns of winning reference ads (e.g. the Zafira
   GLP-1 ad: 80 sampled frames, every cutaway cataloged and typed). What scales beats what
   anyone says they like.
2. **Standing laws** — Brooks's documented rules in the marketing-brain memory (real-footage
   law, avatar age-matching, product-truth laws, no fabricated citations).

## The fingerprint (revealed from the reference teardown)

**Layer mix of a winning 4-min native VSL-style ad:**

| Layer | Share | Sourcing route |
|---|---|---|
| Talking-head avatar | ~57% | not sourced — the avatar side |
| Action B-roll (real people doing things) | ~25% | **Action/Emotion route** (TikTok organic) |
| Graphic overlays | ~14% | **Graphics** — BUILT, never sourced |
| Institutional stock (doctor/lab) | ~4% | **Institutional route** (stock library) |

- ~20–24 distinct action clips per 4-minute ad; clips recur (several used twice); source 30–40+
  verified clips to cut from — and 3–5× that many candidates, because the gate rejects most.
- **Every clip is an ACTION, not a pose** — sweeping, scrolling, pinching, walking away, forking
  food. Even "doing nothing" clips have a physical anchor (leaning on an elbow, holding a mug).
- **Shoot the aftermath, never the symptom** — the feeling is carried by posture and context
  (slumped in the recliner having given up), not the medical event.
- **Faces often absent or obscured** — behind, waist-down, hands-only. Universal; the viewer
  projects herself in. The most reusable clips in the bank.
- **Badly shot IS the credibility mechanism** — phone footage, ceiling fans in frame, bad white
  balance, a Christmas tree still up. A ring-lit creator clip breaks the ad.
- **Age-matched, always** — every on-camera subject matches the brand avatar's age band
  (e.g. Motilli: women 45–70). One off-age clip breaks the whole ad.

**Pacing (from the reference edit rules):** cut every **2.5–4s**; no cutaway holds past **7s**;
the avatar never runs past **~10s** without a cutaway; captions phrase-by-phrase pop-on,
white bold condensed all-caps on solid box. Audio NEVER stops for a visual — all cutaways
are silent under the continuous VO.

## Trusted sources (by route, not by channel)

- **Action/Emotion (dominant)** → TikTok organic via the `tiktok-broll-crawler` skill
  (Apify search + yt-dlp download + Gemini visual gate + contact sheets). Search language =
  the avatar community's own VoC ("mounjaro over 40", "bloat check"), never stock-librarian
  phrasing. TikTok search skews young and comedic — anchor terms to the avatar's age and
  community every time.
- **Institutional (doctor/lab)** → stock libraries (Envato, Artgrid, Videvo, Pexels) or scoped
  yt-dlp searches; polished footage is CORRECT here (the one exception to the amateur rule).
- **Concept/Mechanism (3D medical, diagrams)** → stock animation libraries, or generated via
  the brand's science-broll pipeline (image-to-image from reference frames per the
  broll-sourcer law — never text-to-image).
- **Receipts (posts, headlines, reviews)** → REAL artifacts only, captured with
  `scripts/cdp_capture.py`. See guardrails.
- **Product** → the brand's own asset library ONLY (`brands/<brand>/` + product-scale skills).

## Guardrails (these are LAWS from the memory — not preferences)

- **Action b-roll = REAL footage, never AI-generated.** A beat with no real footage gets
  dropped or flagged, never AI-filled. (3D mechanism animation is the explicit exception —
  that route WANTS renders.)
- **Product shots are never sourced or generated from strangers' footage** — brand assets
  only, and product truth comes from the brand's product-scale skill (flap mechanism,
  colorways, packaging truth).
- **No fabricated citations in receipts** — never invent a study, statistic, N, %, or doctor.
  A real post/headline/review gets screenshotted; a *mockup* (e.g. a Reddit-thread mockup
  the brief calls for) is a GRAPHICS BUILD executed from the brief's exact spec, clearly a
  build, never presented as a sourced artifact.
- **Audio: always silent** — one continuous VO carries every ad; strip all clip audio.
- **Native burned captions/watermarks on sourced TikTok clips: acceptable by default** in
  raw-UGC-style ads (they read as authenticity) — the ad brief's Part-4-style sourcing rules
  win per job.
- **Competitor branding visible only when the brief intends it** (villain shots); otherwise
  crop or reject.
- **Format:** 9:16 1080×1920 vertical; grab 8–15s even when 2s are needed (editor handles);
  trimmed best-segment delivery with ~1.5s pad.
- **The Gemini gate + the visual subject test are non-negotiable** — footage OF the action,
  never footage ABOUT the topic; Claude frame-audits contact sheets before Brooks sees
  anything; Brooks makes the final picks.

## Defaults

- **Default genre:** DR video ad (UGC/VSL/native), 60s–4min, continuous VO
- **Default output:** silent · 9:16 1080×1920 · trimmed best segment +1.5s handles ·
  organized per script-beat slot with contact sheets + match report
- **Brand context:** ALWAYS load `brands/<brand>/` research first (LAW) — the avatar sheet
  defines the age band, the VoC defines the search language, the brief defines the villains.
