# VEL-ELEANOR-VERA25 — Vestirsi "Vera" film, rebuilt on Seedance 2.5

**Date:** 2026-08-07
**Swipe:** https://app.trendtrack.io/share/ads/vestirsi-QsaRUK — 13.16s, 9:16, 720x1280, 30fps, music only, no VO. Local: `_ref/reference.mp4`
**Product:** The Eleanor Weekender, Light Chocolate (cream ivory canvas + cognac leather), $159.99
**System:** `_engine/sops/Seedance-Prompt-System.md`

---

## ⚠️ Read first: this swipe is already replicated

The reference file is **byte-identical** (md5 `fc08c7b2e2fa0f1c2a1b3bc9567c242b`) to the one in
`8:1:26 - on route nyc (vestirsi replication)`, which shipped a finished 5-scene film on the
GPT Image 2 → Google Omni → stitch pipeline.

This run is not a new concept. It is **the same swipe rebuilt on the new single-pass system**, which is
worth doing on its own terms (it is the first real test of the 2.5 prompt stack against a product with
hard mechanism laws), but it should not be presented to anyone as a new angle. The prior run's redirect
table was correct and is carried forward below with two additions.

---

## 1. The cut map (ground truth)

ffmpeg scene detection at threshold 0.2, verified against extracted frames. **10 shots, 9 cuts, 13.16s.**

| # | Window | Len | What is actually on screen |
|---|---|---|---|
| S1 | 0.00–0.63 | 0.63s | Hand extends the telescopic handle of a silver aluminium carry-on. Black bag on the floor beside it |
| S2 | 0.63–1.20 | 0.57s | Bag lifted and held by its **long shoulder straps** beside the suitcase |
| S3 | 1.20–1.83 | 0.63s | Bag seated **on top of** the standing suitcase, handle rising behind it |
| S4 | 1.83–2.70 | 0.87s | Side profile, hands on the straps, bag riding the suitcase |
| S5 | 2.70–3.47 | 0.77s | **Macro: the luggage pass-through sleeve sliding down over the telescopic handle** |
| S6 | 3.47–4.60 | 1.13s | Open bag on a white surface, a **laptop** slides into the padded sleeve |
| S7 | 4.60–7.53 | 2.93s | Headphones lowered in |
| S8 | 7.53–9.30 | 1.77s | A soft folded cream item tucked in |
| S9 | 9.30–11.67 | 2.37s | Closed bag standing in front of the suitcase, hand holding the long straps |
| S10 | 11.67–13.16 | 1.49s | Woman in a cream trench walks past and exits frame, luggage left standing |

**Rhythm:** five shots in the first 3.5 seconds (0.6 to 0.9s each), then it slows to 1.5 to 3s. The fast
front end is the hook; the slow back half is the satisfaction. Nobody's face appears at any point.

**Why it works:** it is a silent product demo. No VO, no claims, no price. The composition asserts
"this bag is part of your luggage system" and the packing beats deliver ASMR satisfaction. One text line
("On route: / for NYC") carries the whole open loop. Faceless staging means there is no casting mismatch
to reject, so the viewer projects herself in.

> **Tooling note for the SOP.** Gemini's per-beat descriptions drifted out of alignment with the
> ground-truth windows even though the windows were supplied explicitly, calling the laptop insert shot 3
> when the frames put it at shot 6. **Always verify the adapter's beat descriptions against extracted
> frames before writing to them.** Also: the default 1.5s merge floor collapsed this ad's entire
> five-shot opening into one beat. Dropped to 0.8s and exposed as `--min-beat`.

---

## 2. Product-truth collision

**Five of the ten shots are built on hardware the Eleanor does not have.** This is the whole job.

| Vestirsi Vera | The Eleanor Weekender |
|---|---|
| Long shoulder straps that reach the shoulder | **Short rolled top handles. Hand or forearm carry only.** Staging a shoulder carry makes Seedance invent a long buckled strap |
| Luggage pass-through sleeve (the S5 hero shot) | **No sleeve, no trolley pass-through.** Never invent hardware |
| Gold zipper along the top | **No zipper anywhere.** Zipper is on the regenerate-on-sight FAIL list |
| Padded laptop sleeve | Not a claim we hold |
| Single-tone black pebbled leather | **Two-tone:** cognac leather upper band over cream ivory woven canvas, gold turn lock, clasp plates, key bell |

Two further conflicts that are not about hardware:

**The open bag.** Shots S6 to S8 all show the bag open. Per the Weekender skill this is a hard block:
Seedance reference mode **cannot** hold the open-bag mechanism (it splits the one-piece flap and paints a
phantom three-tab panel on the front, confirmed across roughly twenty rolls), and the closure-interaction
law says the bag is never opened or manipulated on camera at all. Open-bag frames must come from
GPT Image 2 i2i and then be animated from the locked still.

**The set.** The swipe is a clean seamless-white studio with a silver Rimowa. Copying that look would
violate our photoreal block, which requires "a real lived-in place with ordinary clutter, not a set" and
fails frames on "a background that reads as a set." Redirect to a real entryway or bedroom in window
light. This is also better for our avatar: it reads as her home and her trip rather than a catalogue.

---

## 3. The congruent redirect

Our avatar's nugget, carried from the carry-on brief: **the bag is the first thing they see when you
arrive.** Travel is the highest-visibility stretch of her week.

The swipe's mechanism is "it mates with your suitcase." That is not our mechanism and we cannot fake the
hardware. **Ours is: it holds three days, it goes in the overhead bin, and it keeps its shape.** All three
are live PDP claims. Every beat below sells one of ours, not theirs.

The one element we keep verbatim in intent is **the stack** — the bag sitting on top of the rolling
carry-on with the handle rising behind it. The carry-on brief correctly calls this the highest-leverage
element in the swipe and the one a lazy replication drops. We keep it, executed legitimately: the bag
**rests flat on top** of the suitcase. No sleeve, no strap, nothing threaded.

---

## 4. Scene inventory

**Recommended build: 8 shots, 15 seconds, closed bag throughout, one Seedance 2.5 pass.**

Dropping the open-bag packing beats is not a compromise forced by the engine alone. "Keeps its shape
packed full or barely at all" is a live claim we can show with the bag closed, and it is a better beat
than watching a laptop go in, because it is *our* differentiator rather than a category feature.

| # | Window | Cut | Scene | Sells |
|---|---|---|---|---|
| 1 | 00:00–00:02 | OPEN | Hand extends the telescopic handle of a silver carry-on in a real entryway, morning window light. The Eleanor sits closed on the floor beside it | Hook, travel-system frame |
| 2 | 00:02–00:04 | HARD CUT | Both hands lift the Eleanor by its two rolled top handles, forearm height, bag stays closed | Carry truth, hand carry |
| 3 | 00:04–00:06 | HARD CUT | The Eleanor settles flat onto the top of the standing carry-on, telescopic handle rising behind it. **The stack** | Silent demo: it works with your luggage |
| 4 | 00:06–00:08 | HARD CUT | Macro on the gold turn lock, clasp plates and the little cognac key bell, a hand resting on the leather band. Nothing is manipulated | Hardware, craft, price category |
| 5 | 00:08–00:10 | HARD CUT | The closed bag packed full beside a folded stack of clothes on the bed, holding its rectangular shape | Holds three days |
| 6 | 00:10–00:12 | JUMP CUT | Same bed, the bag now barely filled, still holding exactly the same shape | Keeps its shape either way |
| 7 | 00:12–00:14 | HARD CUT | The Eleanor riding the carry-on at the front door, hand closing around both handles | Departure, the stack again |
| 8 | 00:14–00:15 | HARD CUT | She walks out of frame in a cream trench, luggage left standing in the light | Arrival aspiration, open loop |

Shots 5 and 6 are a **match cut** pair if you want the shape claim to land harder: identical framing,
only the fill changes. That is the one capability 2.5 gives us that ffmpeg cannot.

**Optional hybrid.** If Brooks wants the packing ASMR back, shots 5 and 6 become three open-bag beats
(laptop, knit, pouch) built on the separate path: GPT Image 2 i2i from `light chocolate 4.webp` plus a
still from the validated open-bag broll, mechanism block pasted verbatim, then image-to-video from the
locked still, then cut in. That is a second pipeline running alongside the 2.5 pass, not part of it.

---

## 5. Engine routing and module notes

- **Profile:** P5 (product film, no face) with a partial cast. The reference is faceless — hands, forearms
  and a cream trench only. P5 as written turns CAST off entirely, so this run needs a **hands-and-wardrobe
  cast variant**: no face in frame at any point, but wardrobe and hands are pinned. Worth folding back
  into the SOP as a profile note.
- **VOICE: off.** No dialogue anywhere. SOUND carries it.
- **SOUND:** `no music, no BGM` in the prompt, ambient room tone and real handling sound only. The track
  goes on in the edit as one bed, per the one-take audio law. Generated music would fight it.
- **TEXT: off.** The overlay is post-only via Pillow PNG plus ffmpeg. Mandatory here for two reasons:
  the photoreal block bans on-screen text, and Seedance **cannot spell "Weekender"** (missed 2 of 2).
- **Colorway:** Light Chocolate. The cream-and-cognac palette sits in the swipe's oatmeal quiet-luxury
  register; army green does not.
- **Hardware pin:** state both clasp plates are the same warm brass gold, right identical to left. The
  silver-right-plate attractor hit 3 of 5 rolls on this product.
- **Blocks that must be pasted verbatim:** the identity block, and the photoreal block as the footer.
  The opening-mechanism block is **not** needed in the recommended build because the bag never opens.
- **Negation discipline:** per the updated SOP, do not write "no zipper" or "no shoulder strap" into SET
  or PRODUCT, where naming absent hardware summons it. Pin the positives instead — "two short rolled
  leather top handles carried in the hand", "a smooth unbroken leather upper band across the mouth" — and
  keep the literal no-zipper negation only in the closing NEGATIVES block, where negation actually fires.

## 6. Text overlay options

Reference used "On route: / for NYC" split left and right. Straight lifts of a competitor's line are not
worth the exposure. Congruent alternatives drawn from our own positioning:

1. `Three days. / One bag.` — the capacity claim, plainest read
2. `On route: / for the weekend` — closest to the swipe's rhythm without naming their city
3. `Packed full. / Same shape.` — leads with the differentiator shots 5 and 6 deliver

## 7. Gates before anything ships

1. Three variants of every scene, pick before animating. Photoreal first, product truth second, composition third.
2. Mandatory frame-QA subagent pass on every pick, against the closed-bag calibration.
3. Video QA at three or more frames per clip; engines break the mechanism mid-motion even from a clean first frame.
4. Lint the prompt before firing: `python3 _engine/tools/seedance_prompt_lint.py <prompt> --duration 15 --profile P5`
5. Credit check: 15s at 63 credits per second needs **945 credits** clear, and kie hard-rejects below it.
