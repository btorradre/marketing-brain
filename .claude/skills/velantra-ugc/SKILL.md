---
name: velantra-ugc
description: Multi-shot UGC video ads for any Velantra product via kie.ai Seedance 2.0, using a Brooks-supplied Pinterest image as the creator reference (the 5-avatar roster is RETIRED for new runs as of 2026-08-05 — Blair/Sloane/Marin/Tessa/Camille only fire if Brooks explicitly names one). Derives the ideal ad length (15-30s, awkward lengths welcome) from the concept, segments the script to fit, generates every segment with the creator + product images wired in as references, and stitches the finished ad. Trigger on "make a UGC ad for the Strato", "Velantra UGC ad", "multi-shot UGC for the boat tote", or any Velantra video-ad production request that wants a creator on camera or multiple camera angles/cuts.
disable-model-invocation: false
---

## GOLDEN NUGGET DOCTRINE (MANDATORY — locked 2026-07-11)

Before any hook, angle, script, concept, or audit verdict is produced, name the **golden nugget**: the single most emotionally loaded DEEP FRAME in the research — the real motive that makes buyers act — never the surface theme.

- **Topic ≠ motive.** "Memory loss" is a topic (surface hook: "my memory feels as young as when I was 25"). The frame is: "I thought I was getting dementia just like my mum did, until I discovered this." Surface angles buy mild hope/curiosity; deep frames trigger identification so strong the reader feels caught.
- **The test.** For every candidate angle ask: *is this the topic, or is this the motive?* If it's the topic, dig one layer deeper (memory loss → becoming my parent; GLP-1 bloat/constipation → exiled from my own dinner table; weight loss → the stolen victory).
- **Where it goes.** The golden nugget LEADS — very top of the piece, as the hook. Never buried in the body.
- **Deliverable.** State the golden nugget in one explicit sentence BEFORE drafting. When analyzing a reference ad/funnel/swipe instead of writing, state the nugget it's built on and whether it leads with it. If the research hasn't surfaced one, mine reviews/VOC/Reddit until it does — never default to a surface angle.

# Velantra UGC — Multi-Shot Ad Factory (kie.ai Seedance 2.0)

One command in ("ad for the Strato, use Blair, lead with the structure angle"), one finished conversational multi-shot UGC ad out. **Engine: Seedance 2.0 through the kie.ai API** (`bytedance/seedance-2` — the std model only; `seedance-2-fast` is BANNED, distortion). Higgsfield is retired from this pipeline (2026-07-07) — do not fall back to the `higgsfield` CLI or MCP.

Multi-shot works on two levels:
1. **Cuts inside a segment** — Seedance 2.0 follows multi-shot prompts: change the `camera` per timeline block (selfie medium close → macro fingers on the weave → wide step back) and it cuts natively, MS-style.
2. **Cuts across segments** — each segment is its own generation (4-15s); the runner stitches them.

Registries (this folder): [products.json](products.json) — canonical product refs, PDP links, claims; [avatars.json](avatars.json) — LEGACY roster (retired for new runs 2026-08-05, kept for explicit-name requests and old-run resumes). Legacy avatar identity files: `brands/velantra/_shared/ugc-creators/<Name>/`. Runner: [scripts/kie_seedance.py](scripts/kie_seedance.py).

## Preflight (every session)

```bash
KEY=$(grep KIE_API_KEY "/Users/brooksorradre2/Documents/marketing brain/.env" | cut -d= -f2)
curl -s -H "Authorization: Bearer $KEY" "https://api.kie.ai/api/v1/chat/credit"   # {"data": <credits>}
command -v ffmpeg && command -v ffprobe
```
Observed cost: **actual charge ≈ 41 credits/sec at 720p** (5s = 205cr, matches kie's public $0.165/s at 1cr ≈ $0.004). BUT task creation is **rejected unless balance ≥ ~130 credits × duration** (a 12s task was refused at 1,298 balance on 2026-07-07 — kie pre-authorizes ~3x actual). Rule: before running, require balance ≥ longest_segment_seconds × 130 + already_planned_spend. A 25s two-segment ad needs ~2,200+ free credits to start even though it only charges ~1,025. Failed/rejected tasks are not charged. If balance is short: STOP and ask for a top-up — NEVER downgrade to `seedance-2-fast` or `seedance-2-0-mini` to fit budget (distortion risk, same principle as the banned Higgsfield fast mode).

## Input slots (fill from the user's sentence; ask only what's missing)

1. **Product** — key or alias from products.json ("Strato" = straw tote). Colorway if named → pick the matching canonical ref image.
2. **Creator** — a Pinterest image Brooks supplies (POLICY 2026-08-05: this replaces the roster — never auto-pick from avatars.json). If the request arrives without one, either ask for the image or hand Brooks a Pinterest hunt block (invent the exact person who would post this, then `https://www.pinterest.com/search/pins/?q=WORDS+WITH+PLUS+SIGNS`, clean photos only, no overlays/stickers/app UI) and wait for his pick. From the chosen image, write a verbatim creator block (age range, hair, skin, build, wardrobe, energy — imperfection cues per `feedback_avatar_imperfection_cues`, never tack-sharp) and a matching voice character; that block is the identity lock for the whole run. Roster avatars fire ONLY if Brooks explicitly names one.
3. **Angle/hook** — if absent, default to the product's wound in products.json (Strato: floppy/fragile/sold-out → structured).
4. **Length** — NOT a user input by default. Derive it (below). Only obey an explicit "make it Xs".

## Length doctrine — derive the ideal duration, then segment

Velantra UGC runs **15-30s total**. The concept sets the exact length — awkward totals (23s, 26s) are correct when the script earns them; never pad to a round number, never cut a beat to hit one.

1. Write the script first (beats: Hook → Problem → Benefit/Demo → CTA, laws below).
2. Time it: conversational delivery ≈ **2.7 words/sec** (UGC DIRECTOR's 30-45 words per 15s). Beat duration = beat words ÷ 2.7, rounded to the nearest second. Total = sum of beats, clamped to 15-30s — if outside, cut or grow the *script*, not the pacing.
3. Segment it: each segment 4-15s, split ONLY at beat boundaries. Prefer the fewest segments (fewer identity/scene seams): ≤15s → 1 segment; 16-30s → 2 segments (e.g. 23s → 12s + 11s or 15s + 8s, wherever the beat seam falls). A beat that needs its own visual world (product macro demo) may take its own segment.
4. Angle changes do NOT require a new segment — write them as camera changes across the 5s timeline blocks inside a segment.

## Script laws

Conversational UGC, spoken to one friend. Per `feedback_ugc_dialogue_naturalness` + UGC DIRECTOR house style:
- Commas and periods ONLY. No ellipses, no em dashes, no hyphens (rephrase), numbers as numerals, the word "cinematic" never.
- Contractions, fragments, filler ("honestly", "okay so", "I'm not even kidding"). ~30-45 spoken words per 15s.
- Positive character framing in delivery directions (never "composed/steady" — reads monotone).
- CTA = casual nudge + soft seasonal scarcity.

**CLAIMS GUARDRAILS (HARD — the runner also greps dialogue and hard-fails):**
- **NEVER any origin claim** — no "Italian leather", "European craftsmanship", "made in the USA". Say "leather detailing", "hand woven". (The 7/7 Higgsfield reference ad said "Italian leather" — compliance bug, not a template.)
- Never "Birkin" or "Hermes" in spoken/on-screen copy. Say "structured top handle silhouette".
- Founder, if referenced, is "Jessica" — never Brooks.
- products.json `claims_ok` / `claims_banned` win over everything.

## Reference images — the identity mechanism (every segment, no exceptions)

Every segment uploads and carries **both**:
- **@Image1 = the creator ref** — the Pinterest image Brooks supplied for this run (legacy roster runs: `avatars.json → ref_image`) + the run's verbatim creator block copied IDENTICALLY into every timeline block of every segment.
- **@Image2 = the product canonical ref** (`products.json → canonical_refs`, colorway the concept calls for). The product is grounded by its real image — Seedance never invents it.

The runner uploads local files to kie temp storage per run (`file-stream-upload`, URLs expire ~24h — never reuse old URLs across days) and passes them as `reference_image_urls` in @Image order. Optional @Image3 = setting ref when a beat needs a locked room.

## Segment prompt format

JSON blocks in the MOT-ELLEN / UGC DIRECTOR style (see the pack at `brands/motilli/creative/MOT-ELLEN-RUPTURE-UGC-01/` for the reference implementation): `format` / `identity` / `scene_lock` / `creator` (verbatim) / `timeline` of 5s blocks (camera, right_hand, left_hand, face, in_frame, not_in_frame, light, background) / `audio` (voice from profile.md, room tone, delivery, dialogue) / `never`. The serialized JSON is the segment's `prompt` string, passed verbatim.

Deltas from the Motilli pack for this skill:
- `identity` line adds: "the bag stays exactly as shown in @Image2, weave texture, flap shape, and colorway unchanged".
- Multi-angle segments: change `camera` between timeline blocks and drop the "no cuts inside the clip" clause from `format` (keep it only for continuous-shot segments).
- Default shot arc (matches the winning 7/7 reference): medium close selfie hook with bag at chest → macro insert, fingers on weave/stitching → wide step back, bag on arm → medium close CTA. Unboxing/try-on/review variants per the concept.
- `never` always includes: "no brand logos, no invented text on the bag, never mention where the bag or leather is made".
- **Face law (2026-07-07, Blair 01 defect):** always state which faces of the product carry detailing — e.g. "the leather flap and belts exist ONLY on the FRONT face, the back is plain straw" — and add "no duplicated front detailing on any other face" to `never`. Seedance mirrors front detailing onto the back whenever the bag turns or tilts unless told not to.
- **Component-count law (2026-07-07, Marin 03 defect):** state exact counts for repeated design elements — "the front flap is exactly 3 leather elements, one wide center panel with 2 squared outer tabs, never 4" — Seedance multiplies repeated elements (tabs, grommets, straps) under motion unless the count is pinned.
- **Blocking-escalation law (2026-07-07, Blair 05 face-in-handle x3):** when the same defect survives 2 prompt-level fixes (negatives, geometry pins), STOP re-prompting — the composition itself is the attractor. Rewrite the blocking so the defect is physically impossible (raised-bag verdict pose kept wrapping a handle around the face → final pose became bag standing on the table, hands ON THE TABLE, "the bag is never lifted, no hands on the bag"). Poses that keep hands and face away from the fragile element cost nothing creatively at feed speed.
- **Pronunciation law (2026-07-07, "tote"→"tuck" slur):** Seedance slurs risky product words STOCHASTICALLY — delivery hints and phonetic respelling ("toat") reduce but do NOT reliably fix it, and Whisper launders the slur both directions ("Tote" written over an audible "tuck" and vice versa). Human ear check on product names is mandatory. **The deterministic fix is the ElevenLabs word punch-in — never re-roll a visually clean take for pronunciation alone:**
  1. `ffmpeg -i final.mp4 -vn -ac 1 -ar 16000 take.wav` → OpenAI whisper with `timestamp_granularities[]=word` → find the slurred word's window.
  2. Clone the take's own voice via elevenlabs-agent (`pipeline.py clone --reference take.wav --name velantra-<avatar>-seedance`) — Blair and Tessa clones already exist in voice-registry.json.
  3. Generate the word mid-sentence in matching context (`"My Velantra straw tote finally came. Straw tote. Tote."`), word-timestamp the TTS, cut the mid-sentence instance sized to the hole.
  4. Gain-match (volumedetect diff), splice with 20ms acrossfades, mux `-c:v copy`, re-transcribe the region to verify, archive the pre-patch file.
  Works because the slurred word is one syllable with near-identical lip shapes — invisible at feed speed.

## Build + run

1. Resolve product from products.json; creator = the Pinterest image Brooks supplied (save a copy into the concept folder so the run is reproducible). Write script → derive length → segment (doctrine above).
2. Write the manifest (shape documented at the top of [scripts/kie_seedance.py](scripts/kie_seedance.py)): `mode: "ref"`, `voice_anchor: true` (segment 1's audio becomes the voice reference for segments 2+ — one voice across cuts), `reference_images: [creator_ref, product_ref]`, per-segment `prompt` + `dialogue` + `duration`, 9:16, 720p (1080p only on winners).
3. Show the user the script + segment plan + cost estimate BEFORE generating.
4. `python3 scripts/kie_seedance.py run <manifest.json>` — uploads refs, creates tasks, polls, downloads `seg_NN.mp4`s, voice-anchors, stitches `final.mp4`. Resumable — re-run after a failure, finished segments skip.
5. API cheatsheet: create `POST https://api.kie.ai/api/v1/jobs/createTask` `{model: "bytedance/seedance-2", input: {prompt, reference_image_urls, reference_audio_urls?, aspect_ratio: "9:16", resolution: "720p", duration: 4-15, generate_audio: true}}` → poll `GET /api/v1/jobs/recordInfo?taskId=` (`state: waiting|queuing|generating|success|fail`, `resultJson.resultUrls`). Note: `first_frame_url` chaining (mode "chain") is mutually exclusive with reference images/audio — use it only for keyframe-locked product beats.

## Output convention

Save to `brands/velantra/products/<product-folder>/concepts/<M:D:YY> - <slug>/`:
```
<concept>/
├── <CONCEPT-ID>-prompts.md   # the human-readable segment pack (MOT-ELLEN style)
├── manifest.json             # runner input
└── output/                   # seg_NN.mp4, voice_anchor.mp3, final.mp4, upload_cache.json
```

**QA before delivering (non-negotiable):** `/watch` the final — (1) no origin claim or banned word in the spoken audio, (2) product fidelity vs the canonical ref (flap shape, weave, colorway), (3) same face and voice across every cut, (4) energy held to the last word (no fade). Any failure → regenerate that segment, don't hand it over.

## Roster ops (LEGACY — retired for new runs 2026-08-05)

The roster (avatars.json, `brands/velantra/_shared/ugc-creators/`) and every ad already produced with it stay in place — do NOT delete any of it. New runs take a Pinterest image from Brooks instead (Input slot 2). Only touch the roster when Brooks explicitly names an avatar or resumes an old roster run. Historical add-an-avatar procedure lives in `brands/velantra/_shared/ugc-creators/README.md`.

## Related skills
- **seedanceugcdirector** — the canonical segment prompt format this skill compiles
- **seedance-brief-runner** — Higgsfield-CLI-based sibling for Motilli/Lunessa briefs (kept as is; this skill's runner is the kie.ai equivalent)
- **velantra-*-concept** — upstream concepting; their briefs feed this skill's script step
