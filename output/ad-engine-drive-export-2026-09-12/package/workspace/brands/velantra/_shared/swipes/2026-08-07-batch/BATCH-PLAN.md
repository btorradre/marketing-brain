# 2026-08-07 swipe batch — 7 references, Colette + Weekender

Assets downloaded to this folder. Cut profiles, contact sheets and audio references are built.
**Nothing has been generated yet — two hard blockers below.**

---

## 🚫 Blockers

**1. Credits.** Balance is **154.3**. Seedance 2.5 costs **63 credits/second** and kie *hard-rejects*
createTask below the full amount, so right now I cannot fire even a 5-second test (315). Rough budget
for this batch at 3 variants per scene:

| | seconds | credits | ≈ USD |
|---|---|---|---|
| One 25s concept, 3 variants | 75 | 4,725 | ~$19 |
| Seven concepts, 3 variants each | 525 | 33,075 | ~$132 |

That is before re-rolls. Auto top-up is on but does not beat the request, so the balance needs to be
sitting there before a run starts.

**2. The creator images never landed as files.** All five came through in the message and I can see them,
but Claude Code did not write them to disk, and kie needs an uploadable file. **Drop the five images into
`brands/velantra/_shared/ugc-creators/2026-08-07/` and I can wire them straight in.**

Everything below is done and waiting on those two.

---

## The five creators (as received)

| # | Read | Best fit |
|---|---|---|
| C1 | Late 20s, long dark wavy hair, pink sweater, bedroom, warm and soft-spoken | Colette fall/cozy |
| C2 | Late 20s, long balayage waves, grey wool coat, car selfie, polished | Colette, travel |
| C3 | Late 30s/40s, blonde-brown lob, white top, bright kitchen, warm and direct | Weekender, "what's in my bag" |
| C4 | Mid 20s, long dark waves, black knit, neutral bedroom, calm | Colette OOTD |
| C5 | Mid 20s, dark hair, cream knit, car selfie, understated | Weekender |

All five read as genuine iPhone selfies with real skin texture and available light, which is exactly the
register the photoreal law wants. Wire each in as `@Image1` and **point at it, never re-describe the face** —
text beats the image and re-describing is how identity gets lost.

---

## The seven references

| # | File | Len | Format | Audio | Assign |
|---|---|---|---|---|---|
| 01 | `01-vestirsi-iDgwls` | 36.0s | "Ask me a question → give me a full review". Talking head + product b-roll inserts, burned captions | voice clone | **Weekender** |
| 02 | `02-ig-DWocMIVEZy3` | 44.0s | "3 BAGS FOR THE PRICE OF 1". Convertible demo + street walking | voice clone | ⚠️ see collision |
| 03 | `03-ig-DWOGHMhkwpJ` | 74.1s | Floating reaction head over brand imagery and IG screenshots | voice clone | ⚠️ not a Seedance job |
| 04 | `04-ig-DZGLFLpytkP` | 38.9s | Mirror OOTD, "get dressed with me", one bag across several outfits | voice/music | **Colette** ← best fit in the batch |
| 05 | `05-ig-DQoIBOhjya8` | 17.9s | "What's in my carry-on?" full-body + packing b-roll | music | **Weekender** |
| 06 | `06-ig-DYmTZEtsjhE` | 8.3s | Hands-only ASMR pack on a chair. No face, no dialogue, 2 cuts | **music clone** | **Colette or Weekender** |
| 07 | `07-ig-DYyoMXppnT0` | 32.1s | Closet talking head, bag worn 3 ways, "comment BAG for 40% off" | voice clone | ⚠️ see collision |

Contact sheets: `_analysis/*-contact.jpg`. Cut counts at two thresholds are in the session log.

---

## ⚠️ Collisions to settle before generating

**1. Three of seven sell a convertible bag we do not make.** References 02, 05 and 07 are all built on
Vestirsi's 3-in-1 (tote → backpack → crossbody). Neither Colette nor the Weekender converts. This is the
same class of problem as the luggage pass-through sleeve in the other Vestirsi film: the swipe's entire
mechanism is hardware we do not have, and inventing it is a hard ban.

- **05 survives** because the convertible angle is secondary; the real engine is "what's in my carry-on",
  which redirects cleanly to the Weekender's *holds three days, fits the overhead bin* claims.
- **02 and 07 do not survive as-is.** Their whole payload is "one bag, three ways." Our honest equivalent
  is *one bag, every outfit* (Colette) or *one bag, the whole trip* (Weekender), which is a different ad.
  Recommend either redirecting them to that, or dropping them for better-fitting swipes.

**2. 07 also has a fabricated-offer problem.** It closes on "comment BAG for the 40% sale details." We do
not run a 40% sale and inventing scarcity is banned. That CTA has to become a real one.

**3. 01 is a review format, and Colette is pre-order.** Review-quote ports are banned on a pre-order
product, so 01 goes to the Weekender (in stock, real reviews) and not to Colette. If you want a Colette
version it has to be a first-look, not a review.

**4. 03 is not a Seedance job.** A floating green-screen head composited over brand imagery and Instagram
profile screenshots is an editing task. Seedance would have to generate the screenshots, and it garbles
text. Recommend: generate the talking head only, composite the rest in post. It is also 74 seconds, so it
would need to be three generations regardless.

**5. Five of seven exceed the 30-second cap** (36, 44, 74, 39, 32). Each needs either a trim to a 25-30s
arc or a split. The adapter's `scaffold --target` retimes the beats proportionally so the timeline still
sums correctly; do not just generate short against a long timeline, that is what desyncs delivery.

---

## Audio — done

Per the brief: 15 seconds pulled from each reference, selected by scanning for the **densest speech-band
window** (300–3400 Hz bandpass) rather than raw loudness, so a loud music bed does not win the window.

Then run through **ElevenLabs audio isolation** to strip the music, because Seedance voice cloning wants a
dry vocal — a reference with music under it clones the mix, not the voice.

`_audio/isolated/`
```
01-vestirsi-iDgwls-voiceref-dry.mp3    (window 0–15s)
02-ig-DWocMIVEZy3-voiceref-dry.mp3     (12–27s)
03-ig-DWOGHMhkwpJ-voiceref-dry.mp3     (48–63s)
04-ig-DZGLFLpytkP-voiceref-dry.mp3     (18–33s)
05-ig-DQoIBOhjya8-voiceref-dry.mp3     (0–15s)
06-ig-DYmTZEtsjhE-MUSICref.wav         (full 8.3s, music — NOT isolated, this is the POV music clone)
07-ig-DYyoMXppnT0-voiceref-dry.mp3     (9–24s)
```
All 44.1kHz mono, ~15.0s, verified distinct.

**How they get used:** `reference_audio_urls` on the 2.5 call. This is the "lip-sync compiler" path —
rather than dubbing over a finished clip, the voice goes in as a reference and Seedance moves the mouth to
it. It is field-reported in two independent source families and **not yet verified on kie**, so the first
run should be a cheap single-scene test before committing a whole concept to it.

Two things that matter if it works: the shot must run on the standard tier (fast plus audio fails
server-side), and for 06 the music reference must be the **only** clock in the prompt — do not also give it
a timestamped timeline, or nothing knows which to follow.

---

## Per-concept build shape

All of them: **P1/P2 profile, 9:16, 720p, iPhone-real LOOK block, no on-screen text** (burned in post — and
mandatory here because Seedance cannot spell "Weekender"). Scenes generated in one Seedance 2.5 pass with
internal cuts, which is validated to land within half a second of the marked timestamps.

Standing gates from the product skills, unchanged:
1. Three variants per scene, pick before animating. Photoreal first, product truth second, composition third.
2. Mandatory frame-QA subagent pass on every pick.
3. Weekender: identity block + photoreal block verbatim; hand/forearm carry only, never shoulder; no
   on-camera opening; both clasp plates pinned gold.
4. Colette: **real-photo-anchor law** — never i2i from our own render, it inherits the CGI fingerprint.
   Anchor on `product-references/colette-canonical-caramel-v3.png`. Body claim is "cashmere-feel brushed
   wool" only. Never position as a work bag.
5. Creator never speaks as the brand: "they're running…", never "our…".
6. Negation discipline: describe what IS in frame; keep literal negation in the closing block only.

---

## What I need to start

1. The five creator images dropped into `brands/velantra/_shared/ugc-creators/2026-08-07/`.
2. Credits topped up — 5,000 covers one concept properly, 35,000 covers the batch.
3. A call on collisions 1 and 2: redirect 02 and 07 to "one bag, every outfit / the whole trip", or swap
   them for better-fitting swipes.
