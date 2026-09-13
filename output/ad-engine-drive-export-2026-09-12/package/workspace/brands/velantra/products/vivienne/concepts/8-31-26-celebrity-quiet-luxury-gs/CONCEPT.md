# VEL-VIV-CELEB-GS-01 — "The bag they all carry, without the ten thousand"

**Date:** 2026-08-31
**Product:** The Vivienne Top Handle Bag · $149.99 from $199.99 (Save $50.00 = 25%) · pre-order, first run ships October · Chocolate / Cognac / Black / Olive
**Format:** greenscreen AI UGC. Creator keyed as a PiP for the full runtime over full-frame b-roll, burned word-synced captions, one continuous VO, 1080x1920, 24fps
**Runtime:** **58.3s** (v2 build). 147 words at ~153 wpm — she read slower than the 180 wpm estimate, and the whole bed re-timed off her alignment. The read ships as-is. No atempo, ever.
**Funnel:** TOF
**Reference:** the celebrity-identity ad Brooks sent (`instagram.com/p/DcJd0Y5AGgb`) — a brand tying itself to Brad Pitt: *get that look, without paying for that name.*

---

## What this is

The first Vivienne ad where **the celebrity is the mechanism, not the decoration.**

The reference's whole engine is a borrowed identity: it never claims Brad Pitt uses the product,
it claims the *look* is his, and then sells the affordable route to that look. We run the same
engine with the two women our buyer already screenshots — **Katie Holmes and Sofia Richie** — and
the affordable route is the Vivienne.

That is exactly the Birkin-inspired mechanism the live PDP already runs (laws.md §4, the
2026-08-21 reversal). It stays in the VO and the caption layer. **It never enters a generation
prompt.**

Format is the greenscreen AI UGC bed proven by DC-04 / BLK-01 / GS-BIRKIN-01 / GS-EVERYTHING-01.

---

## The combo hook

Brooks directed it: **a fast two-still combo, Katie then Sofia, before anything else.**

| | Still | What it shows | Hold |
|---|---|---|---|
| c01 | Katie Holmes | denim shirt, flares, **chocolate top-handle** in hand, second bag on the shoulder | 2.2s |
| c02 | Sofia Richie | tweed cape, cream knit, **oxblood top-handle** in hand, rain | 1.6s |

Both are real press photographs, held as **hard stills with zero camera move** — the
no-Ken-Burns law kills a push-in on a still, and the reference holds its celebrity frames dead
still too. The combo runs **3.8s total**, then the ad is on our bag and stays there.

Katie's bag is chocolate, which is our hero colorway. The ad pays that off at c03 and never
says so. Sofia's is oxblood, which we do not make — it is doing the *price* job, not the
*colorway* job, which is why she comes back at c05 carrying the $10,000 caption.

**Frames prepped:** cropped to true 9:16 and upscaled to 1080x1920 in `board-frames/`.
Source crops in `references/`.

---

## Script

Brooks's script, held word for word except for the three edits tabled below.

> Okay, so if you love that Katie Holmes, Sofia Richie clean girl energy, always in a Birkin
> shape bag, never a logo, quiet luxury written all over it, you already know the problem.
> Every bag that gives you that look starts around ten thousand dollars.
> So I hunted down the affordable version.
> It's called the Vivienne by Velantra.
> Same silhouette, no logo, actually accessible.
> It's vegetable tanned leather all the way through, with an aged brass belted turn lock,
> braided leather trim, and zero branding anywhere on it.
> It's soft, so instead of sitting stiff on your arm like most bags in this shape,
> it slouches and molds to you as you carry it.
> And right now they've actually just opened pre orders on it.
> Twenty five percent off, one forty nine instead of one ninety nine, and the first run ships
> in October.
> I've left the link below.

149 words. TTS input feeds `Viv-ee-EN` and `Vell-Ahn-Trah`; plain spelling stays in the captions
via the respell map.

### The three edits, and why

| # | Brooks wrote | Ships as | Why |
|---|---|---|---|
| 1 | "there's already a fifty thousand person waitlist and every batch before this has sold out seven times in a row" | "Twenty five percent off, one forty nine instead of one ninety nine, and the first run ships in October" | 🚨 **Both numbers are fabricated.** They are the Nuamore reference's numbers. The Vivienne has **never shipped** — there are no previous batches to have sold out, and there is no waitlist anywhere in the product tree. The no-fabricated-claims law is absolute, and the same swap was already made once on VEL-VIV-KATIE-01. The replacement carries the real offer, which is genuinely strong and was **verified live today**. |
| 2 | "full grain vegetable tanned leather" | "vegetable tanned leather" | "Full grain" is not a cleared claim. PRODUCT-TRUTH §11 clears "vegetable-tanned leather throughout, no canvas" and nothing more about the hide. One word. |
| 3 | "It's soft structured" | "It's soft" | **"Structured" is a banned word on this product** (PRODUCT-TRUTH §1). The 2026-08-22 correction killed it because the engine and the copy were both rendering a rigid box. The rest of the sentence already does the work. |

**If you want the pressure back**, the honest version of it is one line and it is yours to approve
because it is a promise you have to keep, not a fact I can verify:
> "It's a first run, so it's a limited number of bags, and when they're gone the price goes back to one ninety nine."

### Claim check, run 2026-08-31 against the live PDP

| Line | Live PDP | Verdict |
|---|---|---|
| "always in a Birkin shape bag" | laws.md §4 mechanism reversal, copy only | holds |
| "starts around ten thousand dollars" | category statement about the shape, not about a named house's SKU | holds |
| "vegetable tanned leather all the way through" | "Vegetable-tanned leather, no canvas" | holds |
| "aged brass belted turn lock" | PRODUCT-TRUTH §11 cleared | holds |
| "braided leather trim" | PRODUCT-TRUTH §6 cleared | holds |
| "zero branding anywhere on it" | "The leather, not the logo" | holds |
| "soft… slouches and molds to you" | PRODUCT-TRUTH §11 cleared | holds |
| "twenty five percent off, one forty nine instead of one ninety nine" | `compare_at_price: 19999`, price `$149.99`, Save $50.00 = exactly 25% | **verified live 2026-08-31** |
| "the first run ships in October" | "Expected to ship October. Nothing on this page ships from stock." | **verified live 2026-08-31** |

---

## The bed — 18 cuts over ~46.5s, b-roll on every beat

Every cut is a real clip from the animated Vivienne organic library (`broll/final/`), except the
two hook stills, one new generation, and the PDP recording. **No beat is uncovered.**

| Cut | In → Out | Source | PiP | Spoken over it |
|---|---|---|---|---|
| c01 | 0.00 – 2.20 | **Katie Holmes still** (hard hold) | L | Okay, so if you love that Katie Holmes, |
| c02 | 2.20 – 3.80 | **Sofia Richie still** (hard hold) | L | Sofia Richie clean girl energy, |
| c03 | 3.80 – 6.40 | O8 unmade bed — full trapezoid, clean front | L | always in a Birkin shape bag, never a logo, |
| c04 | 6.40 – 9.70 | O9 on the hip, hallway, walking away | R | quiet luxury written all over it, you already know the problem. |
| c05 | 9.70 – 11.70 | **Sofia still, back** + `$10,000+` card | R | Every bag that gives you that look |
| c06 | 11.70 – 13.40 | O1 kitchen counter, keys + mug + receipt | L | starts around ten thousand dollars. |
| c07 | 13.40 – 15.50 | O2 grab off the bench | L | So I hunted down the affordable version. |
| c08 | 15.50 – 17.60 | O12 over the chair back, lamp light | R | It's called the Vivienne by Velantra. |
| c09 | 17.60 – 19.80 | O3 passenger seat | R | Same silhouette, no logo, actually accessible. |
| c10 | 19.80 – 22.20 | O4 fingers press the leather | L | It's vegetable tanned leather all the way through, |
| c11 | 22.20 – 24.30 | O5 fingers turning the brass lock | L | with an aged brass belted turn lock, |
| c12 | 24.30 – 25.50 | O11 braided trim macro | L | braided leather trim, |
| c13 | 25.50 – 27.50 | **GAP-02 (to generate)** bare band, nothing stamped | L | and zero branding anywhere on it. |
| c14 | 27.50 – 30.40 | O4 late in-point, hand on the panel | R | It's soft, so instead of sitting stiff on your arm |
| c15 | 30.40 – 32.20 | O10 handles released, it settles and slumps | R | like most bags in this shape, |
| c16 | 32.20 – 35.00 | O9 late in-point, moulding against her | R | it slouches and molds to you as you carry it. |
| c17 | 35.00 – 38.30 | O7 walking out the front door | L | And right now they've actually just opened pre orders on it. |
| c18 | 38.30 – 46.50 | **live PDP screen recording, continuous** | L | Twenty five percent off, one forty nine instead of one ninety nine, and the first run ships in October. I've left the link below. |

Average cut 2.58s. Machine-readable: `beat-map.json`. Board frames: `board-frames/`.
Contact sheet: `_qa-storyboard.jpg`.

### The `$10,000+` card at c05

The price gut-punch is a **caption card over Sofia's still**, then a hard cut to O1 — a
ten-thousand-dollar object, then our bag lying on a kitchen counter next to keys and a receipt.
The cut is the argument. Scrim the card over the type's own span, never the whole frame.

### The close is one unbroken screen recording

c18 runs 8.2s and carries the whole offer and CTA. **The ad ends on the website — it never cuts
back to the bag.** One slow continuous downward scroll, no cuts inside it:

| ~t | On screen |
|---|---|
| 38.3s | title, $199.99 struck to $149.99, Save $50.00, four swatches |
| ~42s | Add to Cart, free shipping / returns line, icon bar |
| ~44.5s | the pre-order paragraph — "Expected to ship October" — settles and HOLDS to the last frame |

Captured at 500px CSS window width the day the ad ships. 390 and 430 clip the theme's title.

### Coverage audit — every beat, no holes

| Beat | Line | Frame | Status |
|---|---|---|---|
| HOOK A | Katie Holmes | Katie still | ✅ prepped, needs upscale |
| HOOK B | Sofia Richie | Sofia still | ✅ prepped |
| SHAPE + NO LOGO | Birkin shape, never a logo | O8 | ✅ animated |
| QUIET LUXURY | you already know the problem | O9 | ✅ animated |
| PRICE PROBLEM | ten thousand dollars | Sofia + card → O1 | ✅ animated |
| DISCOVERY | the affordable version | O2 | ✅ animated |
| PRODUCT INTRO | the Vivienne by Velantra | O12 | ✅ animated |
| POSITIONING | same silhouette, accessible | O3 | ✅ animated |
| LEATHER | vegetable tanned | O4 | ✅ animated |
| HARDWARE | brass belted turn lock | O5 | ✅ animated |
| TRIM | braided leather trim | O11 | ✅ animated |
| NO LOGO | zero branding anywhere | GAP-02 | ⚠️ **one generation open** |
| SOFTNESS | not stiff | O4 late | ✅ animated |
| SOFTNESS | most bags in this shape | O10 | ✅ animated |
| SOFTNESS | slouches and molds | O9 late | ✅ animated |
| OFFER OPEN | pre-orders just opened | O7 | ✅ animated |
| OFFER + CTA | price, October, link | PDP scroll | 📹 capture day of ship |

**GAP-02 is the only missing asset.** The house rule is that every claim owns its own frame, and
"zero branding anywhere on it" currently has no dedicated one — O11 is the braid macro and sits
immediately before it, so reusing it would be two near-identical cuts back to back.

> **GAP-02 spec.** Table-level macro, raking window light across the bare front panel and the
> closure band. Natural pore grain, matte-to-satin, nothing stamped, embossed or plated anywhere
> in frame. Flap CLOSED, cutouts occluded. Chocolate body, contrast cognac straps, Weekender
> hardware. Seed i2i from `source/tiktok/SEED-real-bag.jpg`, the supreme real reference — never
> from a previous generation. Still to Omni for a ~1.3s live move before assembly. No Ken Burns.
>
> **Approved fallback if you don't want to spend:** O2 at a late in-point (5.5s) — the clean front
> panel, hand out of frame. Cuts today, weaker claim ownership.

### Why O6 is not in the bed

O6 is the bag on a cafe floor. She would not set a leather bag on a cafe floor. The
situational-plausibility law kills it, same as it did on GS-EVERYTHING-01.

---

## The three creators

Reused from GS-EVERYTHING-01 — same three greenscreen keyframes, already rendered, zero new
generation cost. One shared VO drives all three, so the bed, the captions and every timing are
identical and only the creator changes. A clean creator-only A/B/C.

| | Who | Look | Register |
|---|---|---|---|
| **A** | Diane, 58 | silver-blonde to the shoulders, freckles and sun lines, cream chunky knit | warm, the neighbour everybody trusts |
| **B** | Bridget, 53 | dark brown to the collarbone, grey at the temples, rust fine knit | warm, practical, no-nonsense |
| **C** | Marguerite, 62 | sharp silver bob to the jaw, thin gold chain, black turtleneck | cool, precise, the friend with taste |

Keyframes: `../8-31-26-greenscreen-everything/creators/{A-diane,B-bridget,C-marguerite}-green.png`

> ⚠️ **One casting flag.** Your 50+ direction was given for the "everything bag" script, and it
> fits that script perfectly. This script says *"clean girl energy"* and names a 27-year-old.
> A 62-year-old reading that line is a register mismatch the viewer will hear. Two ways to close
> it, your call: **(a)** ship these three as-is and cut "clean girl" to *"that Katie Holmes, Sofia
> Richie energy"* — one word out, mismatch gone; **(b)** say the word and I'll generate a fresh
> trio at 35–45 on the same greenscreen recipe. Default while you decide is **(a)**.

---

## Production recipe

| Step | How |
|---|---|
| Hook stills | Katie's source is **398x768 — too small for a 1080x1920 frame.** Run it through a real upscaler (Higgsfield `upscale_image` to 2K) before it touches the timeline; the LANCZOS board frame is for approval only. Sofia at 1166x1749 is fine, 1.1x. |
| VO | ElevenLabs **Woman Over 40** (`NBIPq5xdnIg9kaBH5Ape`), eleven_v3 Creative, one continuous take. STT-gate every word. Ship the natural read. **No atempo, ever** — that is what made the men's greenscreen cut sound robotic. |
| Creator render | HeyGen: keyframe → photo avatar → `engine.type: avatar_v`, 1080p. ~330 api credits per 46s render × 3. Check `GET /v3/users/me` `wallet.remaining_balance` first. |
| Key | Sweep the green per creator — HeyGen's green differs per source. Start `chromakey=<measured>:0.10:0.02` + `despill=type=green:mix=0.15`. **Never 0.5 mix: it goes pink.** |
| PiP | 32% of frame width, bottom-anchored, side alternating per the table. |
| Captions | Build from the alignment JSON with the card builder in `../8:22:26 - vivienne launch VO x3/build_ads.py`. Respell `Viv-ee-EN` → Vivienne, `Vell-Ahn-Trah` → Velantra. Cards at y=1500. Scribe spells the brand by ear — audit every card. |
| Assembly | One ffmpeg pass, 1080x1920, 24fps CFR, VO at -14 LUFS, all b-roll audio muted. |

⚠️ This machine's ffmpeg has no libass and no drawtext — caption cards are Pillow-rendered and
overlaid.

---

## Editor notes

- **c01 and c02 are hard holds with no camera move.** No push-in, no drift. The combo is a
  flash-flash, then we're gone. If it feels slow in the cut, trim c01 to 1.8s before you trim c02.
- **c10 and c14 pull from the same clip.** Take c14 from the tail where her hand lifts off, so the
  two reads differ. If they still twin, swap c14 to O10 and give c15 the O4 press.
- **No face appears in any b-roll cut.** O9 and O7 are shot from behind. The keyed creator is the
  only person on screen for the whole runtime (one-creator element lock).
- **Every cut lands on a phrase break.** Don't linger past the line.

---

## Gate

Storyboard-first. Nothing renders until Brooks approves the board. Open:

1. **The scarcity swap** — confirm the real offer ships, or approve the honest first-run line.
2. **Casting** — (a) these three + drop "clean girl", or (b) a fresh 35–45 trio.
3. **GAP-02** — generate it, or ship the O2-late fallback.
4. **Celebrity likeness** — both stills are unlicensed press photography of real people. The ad
   never claims either of them carries ours; they are named as a *look*, which is the reference's
   own mechanic. Still worth your eyes before it goes to Meta review.


---

# PRODUCTION LOG — built 2026-08-31

Three finished ads, one shared VO, creator-only A/B/C. Everything below is what actually
shipped, and where it differs from the approved storyboard it says so and why.

## What was built

| Asset | Detail |
|---|---|
| **VO** | ElevenLabs Woman Over 40 (`NBIPq5xdnIg9kaBH5Ape`), eleven_v3 Creative, **one continuous take**, `job_d81b9c285925`. **58.08s, all 147 words present, nothing dropped.** No atempo. |
| **Bed** | 18 cuts, `production/bed.mp4`, 58.83s. Every cut boundary is a real word boundary from the alignment, not an estimate — `retime.py` asserts each cut's fragment against the alignment and fails loudly if a word drifts. |
| **Captions** | 34 word-synced cards, `production/captions.webm` (alpha VP9), cards at y=1500, overlaid LAST so type always sits above the creator. |
| **Creators** | HeyGen Avatar V, 1080p, the same three greenscreen keyframes as GS-EVERYTHING-01. Green **measured off each render's own backdrop** and the similarity **swept**, never inherited. Despill 0.15. |
| **Assembly** | One ffmpeg pass per creator. PiP sized on the HEAD and **cut by the frame edge** (see the PiP section below), side alternating per cut off the beat map. VO at -14 LUFS, all b-roll audio muted. 1080x1920, 24fps CFR. |

Machine-readable final timings: **`beat-map-final.json`** (the approved `beat-map.json` holds the
storyboard estimate). Scripts: `retime.py`, `build_bed.py`, `build_captions.py`, `assemble.py`,
`creator-renders/{render_heygen,matte}.py`, `broll-new/capture_pdp_scroll.py`.

## Four changes made during the build

1. **Runtime 46.5s → 58.5s.** The estimate assumed 180 wpm off GS-EVERYTHING-01's render. This
   read came back at ~152 wpm. Nothing was cut and nothing was sped up — the one-take audio law
   and the no-atempo law both say the read ships as-is, so the bed stretched to fit her.
   Average cut is now 3.25s against the storyboard's 2.58s, which is inside the range
   GS-BIRKIN-01 shipped at.

2. **c14 moved off O4.** The storyboard had c10 and c14 both pulling the fingers-press clip at
   different in-points, with an editor note to take c14 from the tail. Built and checked, **they
   twinned badly** — the clip barely moves, so both in-points render the same picture. c14 is now
   **O8 at 6.5s**, the bag collapsed into the duvet, which is a better frame for
   *"It's soft, so instead of sitting stiff on your arm"* than a second copy of the press anyway.
   Repeats now: O8 (c03/c14), O9 (c04/c16), O2 (c07/c13). None adjacent, all 17s+ apart.

3. **GAP-02 was not generated. The approved fallback shipped.** The seed the spec called for —
   `source/tiktok/SEED-real-bag.jpg`, the supreme real reference — carries **an ATORIE hang tag
   and the source listing's hardware, not ours.** Seeding a *"zero branding anywhere on it"* macro
   from a frame with a brand tag in it is the wrong move, and the only other real frames have the
   same problem. c13 is **O2 at 5.5s**: the whole clean front panel lifted into the light, bare
   leather, hand clear of frame. If you want the dedicated macro, it needs a clean-room generation
   off the identity block rather than an i2i, which is a separate job.

4. **PDP scroll retuned twice.** Inherited settings (cubic ease, 335px of travel) parked the
   scroll less than half way through a 9s clip and then sat dead for 5s. Now 640→1085 CSS px on a
   quadratic ease over 88% of the clip: it opens on **$199.99 struck to $149.99, Save $50.00,
   four swatches, Add to Cart**, keeps moving through the pre-order paragraph, and settles on
   *"Expected to ship October"* for the final hold. One continuous move, no cuts inside it.

## One defect found and fixed in the caption builder

The inherited card builder merges any card of two words or fewer into its neighbour. On this
script that rule glued **`It's called the Vivienne by Velantra.`** onto **`Same silhouette, no
logo, actually accessible`** and produced a single **8-second** caption card spanning two cuts,
and did the same across `and zero branding anywhere on it.` / `It's soft`.

`build_captions.py` now segments sentence → phrase → card, **never merges across a sentence end**,
and caps a card at 2.9s however few words it holds. 27 bad cards became 34 clean ones.

## Casting

Shipped on **option (a)** as flagged: the three 50+ creators, with the words *"clean girl"* cut
from the hook line. It now reads *"if you love that Katie Holmes, Sofia Richie energy"* — same
mechanic, no register mismatch. Say the word and the fresh 35-45 trio is a re-render on the same
VO, since the VO is creator-independent.

## Still open for you

- **The first-run scarcity line.** Still not in the ad. If it is true that the price returns to
  $199.99 after the first run, that line goes in and the VO re-renders.
- **Celebrity likeness.** Two unlicensed press photographs. Worth your eyes before Meta review.
- **GAP-02**, if you want the dedicated no-logo macro instead of the fallback.


---

## PiP geometry — REBUILT 2026-08-31 after Brooks rejected v1

**v1 was wrong and the rejection was right.** The creator floated in the corner as a complete
cutout with transparent air around her whole silhouette. She read as a sticker pasted onto the
b-roll, not as a person standing in the shot.

**The bug was sizing on the PLATE instead of on the HEAD.** The inherited rule is "PiP = 32% of
frame width", which works for the shipped ads because those HeyGen plates are tight head-and-
shoulders framing. Our Vivienne creator keyframes were generated wide, waist-up, with 10-15%
headroom — so scaling that whole plate to 32% made her head tiny and left the frame showing her
entire outline.

**Measured off the shipped house ads** (`GS-BIRKIN-01-whitney`, `UGC-BLK-01`) at full resolution,
the real house treatment is:

| | Shipped range | Ours now |
|---|---|---|
| Head width | 0.16 - 0.23 of frame width | **0.20** (216px) |
| Head top | y ≈ 1220 - 1340 | **1276 - 1346** |
| Body past the bottom edge | cut | **cut, 60px** |
| Body past the near side edge | cut | **cut, 64 - 73px** |

So `pip_geometry.py` measures each keyed plate's own alpha channel — head width, head centre,
head top — and solves an overlay x/y that is **deliberately negative**: her body runs 60px below
the frame and 64-73px past the near side, so the frame crops her on two edges. A PiP that fits
entirely inside the frame is the defect, not the goal.

Per-creator numbers are in `pip-geometry.json`. They differ because the three plates frame her
differently: A 474x714, B 498x750, C 513x772.

**Captions moved again as a consequence.** At the new scale her head top sits at ~1276, so the
cards moved from y=1330 to **y=1120**. They now clear her head instead of sitting across her face.


---

## v2 — two rejections fixed, 2026-08-31

### 1. The price beat: reused still + cheap card, both gone

Brooks, on the v1 cut: *"you reused the same image twice here and the $10,000+ caption looks
cheap. remove it."* Both were right.

The v1 price beat was **two** cuts: a **second pass of the Sofia still** carrying a burned
`$10,000+` graphic, then O1. The still had already played 8 seconds earlier as the hook, so it
read as a reuse, and the card was a graphic doing work the voiceover already does.

**Both are deleted.** The whole line — *"Every bag that gives you that look starts around ten
thousand dollars"* — now plays over **one continuous cut of our bag on the kitchen counter**
(O1, 4.8s). The number still lands on screen, in the ordinary word-synced caption style, not as
a graphic. `price_card()` is gone from `build_bed.py` entirely.

**Each celebrity still now appears exactly once.** The ad is **17 cuts**, not 18.

### 2. The voiceover: "Vivian", and the pause is gone

Brooks: *"The pronunciation is fucked up. It should say 'the Vivian by Velantra.' It's like she
pauses for a second, and the audio just sounds awkward."*

Diagnosed, not guessed. The rest of the read sits at a **0.060s median gap** between words. The
brand phrase did not:

| | v1 | v2 |
|---|---|---|
| `Viv-ee-EN` / `Vivian` | 0.84s, gap 0.12 | **0.42s, gap 0.06** |
| `by` | 0.37s, gap **0.19** | 0.27s, gap 0.13 |
| `Vell-Ahn-Trah.` / `Vehlantra.` | 1.08s, gap **0.20** | **0.96s, gap 0.08** |

**The cause was my own TTS respellings.** eleven_v3 reads a hyphen as a syllable break, so
`Viv-ee-EN` and `Vell-Ahn-Trah` were each stretched AND given a pause on both sides — three times
the median gap. The hyphens were there to stop the engine saying "Volantra".

**Fix: plain spellings.** `Vivian` and `Vehlantra` go to the engine; the caption respell map maps
them back, so the cards still read **"It's called the Vivienne by Velantra."** New VO is
`job_f97a185c38d2`, 57.84s, one take, all 147 words STT-gated.

> ⚠️ **One thing I could not verify by machine, so ear-check it.** ElevenLabs Scribe transcribes
> **"Volantra" for every spelling tested** — the plain ones AND the hyphenated one that has been
> shipping. It cannot discriminate between them, so it is useless as a judge of that one word.
> What the test does prove is that going plain causes **no regression** (identical STT) and is
> measurably tighter. If the brand word sounds wrong to you, the fix is one token in the TTS
> input, not a rewrite.

### Everything downstream re-timed

The creator plates are lipsynced to the audio, so a new VO means a full rebuild: all three HeyGen
renders redone on the new take, re-keyed, new bed, new captions, new PDP scroll (9.65s), and the
PiP geometry re-measured against the new plates and checked for drift before assembly.
