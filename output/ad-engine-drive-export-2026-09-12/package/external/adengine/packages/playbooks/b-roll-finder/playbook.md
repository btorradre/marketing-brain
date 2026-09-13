---
name: b-roll-finder
description: DR-ad b-roll orchestrator (forked for Brooks from louisedesadeleer/b-roll-finder). Takes an ad script / shot list / creative brief, classifies every beat, routes each to the right sourcing lane (Action/Emotion UGC via tiktok-broll-crawler, Institutional stock, Concept/Mechanism animation, real-artifact Receipts, brand-asset Product, built Graphics), returns vetted candidates on contact sheets for Brooks's final pick, and places cutaways on the VO word. Use when the user says "source b-roll for this ad/script", "build the cutaway bank", "fill this shot list", "find footage for every line", or hands over a sourcing plan / editor shot list for a video ad.
---

# B-Roll Finder — DR ads fork

> Forked 2026-08-17 from louisedesadeleer/b-roll-finder for Brooks's direct-response ad
> production. The original targets YouTube talking-head videos; this fork targets **DR video
> ads** (UGC/VSL/native, continuous VO, 9:16). Methodology laws survive; genre, routes, and
> taste are rebuilt. Load [TASTE.md](TASTE.md) before sourcing anything.

## ⛔ USER OVERRIDES ARE LAW — and they persist

A preference or ban stated mid-run ("no skits", "captions are fine here", "that slot needs
competitor products visible") applies IMMEDIATELY, for the rest of the session, AND gets
written into TASTE.md's Guardrails right then. A banned category is never sourced again.
Violating a stated ban is the worst failure this skill can make.

## STEP 0 — load the profile

Open [TASTE.md](TASTE.md). It is Brooks's confirmed profile — no onboarding interview. "Redo
my profile" re-triggers onboarding at any time. Then **load `brands/<brand>/` research (LAW)**:
the avatar sheet sets the age band, the VoC sets search language, the brief sets villains.

## The rules that govern everything

1. **The agent NEVER picks the final b-roll. Brooks does** — from per-slot contact sheets.
   This skill narrows the funnel: classify, route, source wide, gate hard, frame-audit, then
   hand over a vetted shortlist.
2. **Footage OF the action, never footage ABOUT the topic** — the visual subject test: a
   stranger watching the muted clip must be able to name the required action. A person
   talking about bloating is not a person visibly bloated. Topic-match = reject.
3. **Never deliver footage you haven't visually inspected yourself.** Text verdicts from any
   model are input, not proof — frames on a contact sheet, graded by your own eyes, are proof.
4. **Accuracy over volume; drop, don't pad.** No b-roll is better than wrong b-roll. A dry
   slot ships dry with a note.

## Understand the AD first, then source the MEANING

1. Read the whole script + brief before sourcing. The emotional arc decides what each beat
   needs — the same words need different footage in the agitation vs the resolution section.
2. **B-roll illustrates the POINT, not the words.** "I stopped saying yes to dinner plans" →
   the empty chair, the phone set face-down — not a dinner.
3. **Aftermath, not symptom** — show the defeated posture in the recliner, not the medical
   event.
4. **Mandatory reference sweep per beat:** is there a REAL ARTIFACT behind this line? "She
   showed me the studies", "one thread said", a named product being villainized — real
   headlines/posts/reviews are default candidates (see Receipts route + fabrication guardrail).

## Routing — every beat classified before anything is searched

| Route | Trigger | Source | Who executes |
|---|---|---|---|
| **Action/Emotion** | A person doing/feeling something — the dominant DR route (~25% of a native ad) | TikTok organic, avatar-community VoC search terms | the **`tiktok-broll-crawler` skill** — sourcing plan → crawl → Gemini gate → contact sheets. This fork is the strategist; that skill is the engine. |
| **Institutional** | Authority beats — doctor, lab, clinic | Stock libraries (Envato/Artgrid/Videvo/Pexels) or scoped yt-dlp; polished is CORRECT here | this skill directly |
| **Concept/Mechanism** | "How it works" — organs, nerves, molecules, diagrams | Stock 3D animation, or the brand's science-broll i2i pipeline (never text-to-image) | this skill / science-broll pipeline |
| **Receipts** | A claim, discourse, "people are saying", a cited artifact | REAL posts/headlines/reviews only, captured via `scripts/cdp_capture.py`. **Never fabricate a citation, study, N, %, or doctor (LAW).** Brief-specified mockups are a Graphics BUILD, not a sourced receipt. | this skill directly |
| **Product** | The product on screen | Brand asset library + product-scale skill ONLY. **NEVER sourced from strangers' footage, never generated fresh.** In native-style ads there may be NO packshot at all — follow the brief. | brand assets |
| **Graphics [GFX]** | Text cards, ingredient callouts, counters, mockups | BUILT from the brief's exact spec (GPT Image 2 / HTML / editor), never sourced | graphics pipeline |

**Litmus (in order):** *A person doing/feeling?* → Action/Emotion. *An authority figure?* →
Institutional. *Inside the body / abstract?* → Concept. *A checkable claim/artifact?* →
Receipts. *The product?* → brand assets. *Text/numbers on screen?* → Graphics build list.

## ⚡ Lean path — the funnel is for people-footage, not everything

- **Bank-mode (a full shot list): source by SOURCE, not beat-by-beat.** Cluster beats into
  slots by footage type (the Part-3-style category bank), one crawler slot per category, one
  stock sweep per institutional/concept group. Never fetch serially per line.
- **Objective routes (Receipts, Institutional, Concept): ONE best candidate per beat** once
  the plan is agreed. Contact-sheet options are for the Action/Emotion route, where volume +
  gate + human pick is the mechanism.
- **Per-beat time box ~5 min** on objective routes: place best-available or flag and move on.
- **NO RETRIES — first failure switches method, second failure drops the beat.** Never a
  third attempt; the edit ships without it.
- Cache raw downloads in the job dir (`candidates/`); re-renders never re-fetch.

## Action/Emotion route — the crawler contract

Hand `tiktok-broll-crawler` a sourcing plan where every slot spec obeys:

- `action` describes **what fills the frame** ("thumb turning the dose dial close-up"), never
  the topic ("medication handling").
- **No softeners.** Never write "talking acceptable if…" — the gate uses any exemption to
  rationalize a topic-match through. Faceless age-exemptions must say "only if the face NEVER
  appears in the best segment".
- Search terms in the avatar community's own phrasing, age-anchored ("mounjaro over 40",
  "menopause bloating real") and action-format-anchored ("bloat check", "weigh in wednesday").
- Expect 60–80% rejection; source 3–5× the target count. Underfilled slot → rewrite terms,
  never loosen the gate.

## Eval rubric — score every candidate before showing it

1. **Visual subject test** — the muted-stranger test, decisive.
2. **Avatar fit** — age band on face-visible clips; faceless clips exempt only if the face
   truly never appears.
3. **Credibility texture** — amateur phone-shot for UGC slots; polished for Institutional.
4. **Emotional register** — matches the beat's required emotion, not just its topic. Comedy
   skits and performed reactions about the topic are auto-fails.
5. **Format fit** — 9:16-croppable, ≥720p, ≥duration_needs, silent-able.

## Contact sheets + frame audit (mandatory before Brooks sees anything)

After gating: `tiktok-broll-crawler/contact_sheet.py` tiles every surviving clip into one
labeled grid per slot. LOOK at every sheet and grade line-by-line against the auto-reject
list — (a) fails the visual subject test; (b) off-age face on a people slot; (c)
caption/watermark state violates the brief's rules; (d) AI-slop on a real-footage slot;
(e) displaying-to-camera where the spec asks for a performed action; (f) skit framing;
(g) letterboxing/tiny-source upscales. Delete failures from `matched/` with a noted reason.
"Looks fine" without the list is how a face-filling-the-frame clip ships as "bloat b-roll".

## Placement — land ON or just after the VO word

- The VO is a single continuous track (one-take law) — anchor cutaways to **word-level
  timestamps of the VO** (ElevenLabs output transcribed with Whisper `--word-timestamps True`,
  or the known script text force-matched). Cut lands as/just after the keyword (+0.2–0.5s);
  bias LATER when unsure — late reads as intentional, early reads as a mistake.
- Pacing from TASTE.md: cut every 2.5–4s; no cutaway past 7s; avatar never uncovered >10s;
  connect adjacent cutaways when <half-sentence apart (extend the first — a <2s flash of
  avatar between them reads as an error).
- Word-sync audit before delivery of any placed edit (standing law).

## Composition & formatting

- 9:16 1080×1920, cover-crop (`scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920`),
  never letterbox; blurred-fill only for odd-aspect sources. No agent-built split-screens.
- All cutaways silent (`-an`). Trimmed best-segment + ~1.5s handles; raw stays in `candidates/`.
- Stills: sub-pixel zoom-in only (`scripts/zoom_still.py`, ~1.5%/s) — ffmpeg `zoompan` is
  banned at any speed (integer-stepped = shaky).
- Don't upscale a tiny source — find a better one.

## Iteration discipline — the manifest

Keep `BROLL-MANIFEST.md` next to the deliverable: one row per beat (in/out · beat · asset ·
status · which version approved it) + a "Removed (do not re-add)" list. Before every
re-render: verify every approved beat survives. Approved b-roll never silently disappears.

## Workflow summary

1. Load TASTE.md + `brands/<brand>/` research (avatar, VoC, brief).
2. Read the full script/shot list; classify every beat into routes; cluster Action/Emotion
   beats into category slots (the bank).
3. Propose the routed plan (per-beat interpretation + route + search language). In an
   interactive session, wait for the go; on an explicit "source everything now" instruction,
   the instruction is the go.
4. Execute: crawler for Action/Emotion (plan → crawl → gate); batched stock/receipt sweeps
   for the objective routes; Graphics beats → build list, never sourced.
5. Contact sheets → frame audit (delete failures) → deliver sheets + vetted shortlist +
   match report + dry-slot flags. Brooks picks.
6. (Optional) place on the VO word, render, self-verify the joint grid, update the manifest.

## Tools

- `tiktok-broll-crawler` skill — Action/Emotion engine (crawl, Gemini gate, contact sheets).
- `yt-dlp` — stock/institutional sweeps + any direct URL download.
- `scripts/cdp_capture.py` — headless receipt/page captures (consent-wall aware); verify
  every capture visually.
- `scripts/zoom_still.py` — sub-pixel stills motion. `scripts/render_cutaways.py` —
  cutaway assembly over a base video, audio untouched.
- `ffmpeg` + Pillow — trims, crops, contact sheets, joint grids.
