# VEL-VIV-BIRKIN-COUCH-01 — "The Birkin is your dream bag, and that's the problem"

**Date:** 2026-09-01 (v4; v1 and v2 were top-5 rankings, v3 had no agitation beat, all superseded, see the bottom)
**Product:** The Vivienne Top Handle Bag · $149.99 from $199.99 (Save $50.00 = 25%) · pre-order, first run ships October · Chocolate / Cognac / Black / Olive
**Format:** the reference's LOOK with the house script. Creator seated on a navy couch behind a podcast mic (HeyGen Avatar V from an approved keyframe), split-screen hook, Didot serif cards, hard cuts to full-frame bag footage with one small serif caption per shot, unbroken PDP close. One continuous VO. 1080x1920, 24fps.
**Runtime:** 33.15s (Woman Over 40 read, dead space removed, no atempo). 122 words. Product name at 0:10.9 (Brooks asked for one sentence of agitation before the pivot, which moves the intro past 0:06; his call).
**Angle:** the Birkin icon. She wants the Birkin shape; the Birkin itself is the problem (you cannot just buy one, and most of what you pay is the name); if it is the shape she loves, we have the perfect one.
**Funnel:** MOF (solution-aware)
**Board:** `http://localhost:8765/b/vel-viv-top5-01-top-5-luxury-bags-no-logo-ranked-round-up` (same slug as v1/v2, overwritten)
**Reference:** `instagram.com/reels/Dcl0MfxMwts/` — man on a couch with a mic, "Top 5 luxury bags (no Hermès)", 47s. **The ranking is not carried over.** Brooks, 9/1: "just position our version as it looks... 'Birkin is your dream bag, and that's the problem, but I have a perfect one for you.' Then 'This is the x from Velantra.'"

---

## What this is

The reference donates its staging and its grammar: a person on a couch behind a mic, a split-screen hook with Birkin street footage over the creator, big white serif cards, quick full-frame cutaways with a lowercase serif phrase on each. The script is the Velantra formula: hook with the verdict inside it, `This is the Vivienne from Velantra` by 0:06, the attribute stack, softness, colors, the live offer, the link.

No competitors are named. No ranking. The Birkin is in the hook and nowhere else; the Vivienne carries the rest.

---

## Script (v4, 122 words, 33.15s tight)

> The Birkin is your dream bag, and that's the problem.
> You can't just walk in and buy one, and when they finally let you, most of what you pay is the name.
> But if it's the shape you love, I found the perfect one.
> This is the Vivienne from Velantra.
> Same silhouette, a belted brass turn lock, vegetable-tanned leather all the way through, braided leather trim, and no logo anywhere.
> It's soft, so it slouches and molds to you instead of sitting stiff on your arm, and it comes in four colors.
> It's twenty five percent off on pre-order right now, one forty nine instead of one ninety nine, and the first run ships in October.
> I left the link below.

Formula check: HOOK (0:00–0:03) → AGITATION, one sentence (0:03–0:08) → PIVOT keyed to the shape, not the bag (0:08–0:10.5) → PRODUCT INTRO (0:10.5–0:12) → ATTRIBUTE STACK (0:12–0:20, five physical facts incl. no-logo) → PROOF-as-demo (softness shown, 0:20–0:24) → VARIANTS (0:24–0:26) → OFFER (0:26–0:32) → CTA (0:32).

Why the pivot changed: "But I have the perfect one for you" straight after the hook read as "here is a Birkin" (Brooks). "If it's the shape you love" makes the promise about the silhouette, and the agitation sentence gives the problem a reason (access and price-for-name) in the discernment register: she is not priced out, she is choosing not to pay for a name. No lived-proof time stamp because the product has not shipped; softness is demonstrated on screen instead of claimed.

### TTS respell map (plain spellings, no hyphens)

| Fed to eleven_v3 | Caption reads |
|---|---|
| Vivian | Vivienne |
| Vehlantra | Velantra |

Gap audit: median inter-word gap 0.048s; Birkin 0.08s after, Vivian 0.03s, Vehlantra 0.14s. No audible pause. Scribe gate: all 122 words present ("Volantra" is Scribe's ear for the brand on every build).

### Claim check, run 2026-09-01

| Line | Source | Verdict |
|---|---|---|
| "You can't just walk in and buy one" / "most of what you pay is the name" | the Birkin's appointment-only sales practice is public record; "pay for the name" is the house value thesis (price-to-quality gap) at category level, no Hermès price quoted, no scam register, she is not framed as priced out | holds |
| "The Birkin" / "Same silhouette" | laws.md §4, the 2026-08-21 reversal: Birkin-inspired is the stated mechanism, VO and caption layer only, never a generation prompt, no Hermès price, no dupe/replica wording | holds |
| belted brass turn lock · vegetable-tanned leather all the way through · braided leather trim · no logo anywhere | PRODUCT-TRUTH §11 cleared; live PDP "Vegetable-tanned leather all the way through" | holds |
| soft, slouches and molds | PRODUCT-TRUTH §1/§11 ("structured" is banned and not said) | holds |
| four colors | live variants Chocolate / Cognac / Black / Olive | holds |
| 25% off, $149 from $199 | live `price 149.99, compare_at 199.99` on all four variants | **verified live 2026-09-01** |
| first run ships in October | live PDP "Expected to ship October" | **verified live 2026-09-01** |

Not said: Hermès, any competitor, capacity, laptop, lining, dimensions, origin, "structured".

---

## The creator

Diane (58, silver-blonde, the approved creator A from GS-EVERYTHING-01 and CELEB-GS-01), re-staged to mirror the reference: seated on a navy couch, plain wall, black podcast mic on a desk stand on the coffee table, hands in frame so Avatar V has something to move. Three keyframes generated i2i from her approved green plate (kie `gpt-image-2-image-to-image`, 2:3, 2K, 10 credits each):

| | File | Look | Note |
|---|---|---|---|
| A | `creator/A-knit-gesture.png` | cream knit, one hand mid-gesture | her established Vivienne look |
| B | `creator/B-knit-relaxed.png` | cream knit, hands on knee | calmest read |
| **C** | `creator/C-blue-shirt.png` | light blue button-up, gesturing | **board default: mirrors the reference's wardrobe** |

Pick one. The board is rendered on C; swapping is a one-line change in `build_board_frames.py`.

---

## The bed — 15 cuts over 33.15s

TH = talking head, full frame. Every Vivienne cutaway is a real clip from the organic library (`broll/final/`), never a still. Timecodes are the tightened VO's own phrase boundaries (`vo/words-tight.json`).

| Cut | In → Out | On screen | Overlay | Spoken over it |
|---|---|---|---|---|
| c01 | 0.00 – 1.94 | **Split:** top = sourced street footage of a Birkin being carried, bottom = TH | caption "the Birkin" | The Birkin is your dream bag, |
| c02 | 1.94 – 2.98 | **Split:** top = second Birkin street shot, bottom = TH | caption "and that's the problem" | and that's the problem. |
| c03 | 2.98 – 4.58 | TH, full frame | caption "you can't just walk in and buy one" | You can't just walk in and buy one, |
| c04 | 4.58 – 7.90 | TH, full frame | caption "most of what you pay is the name" | and when they finally let you, most of what you pay is the name. |
| c05 | 7.90 – 10.51 | TH, full frame | card **The perfect one / if it's the shape you love** | But if it's the shape you love, I found the perfect one. |
| c06 | 10.51 – 12.34 | **O8** unmade bed, full clean front | card **The Vivienne / Velantra** | This is the Vivienne from Velantra. |
| c07 | 12.34 – 13.40 | O2 grab off the bench, clean front (the silhouette) | "same silhouette" | Same silhouette, |
| c08 | 13.40 – 14.74 | O5 fingers turn the brass lock | "a belted brass turn lock" | a belted brass turn lock, |
| c09 | 14.74 – 16.94 | O4 fingers press the leather, it gives | "vegetable-tanned leather" | vegetable-tanned leather all the way through, |
| c10 | 16.94 – 18.00 | O11 braided trim macro | "braided leather trim" | braided leather trim, |
| c11 | 18.00 – 19.67 | O12 over the chair back, lamp light, bare front | "no logo anywhere" | and no logo anywhere. |
| c12 | 19.67 – 21.40 | O10 handles released, it settles (1.73s of its 2.2s) | "it's soft" | It's soft, so it slouches |
| c13 | 21.40 – 23.97 | O9 on the hip, moulding | "molds to you" | and molds to you instead of sitting stiff on your arm, |
| c14 | 23.97 – 25.69 | colorway four-up (real per-colorway renders) | "four colors" | and it comes in four colors. |
| c15 | 25.69 – 33.15 | **live PDP screen recording, unbroken** | "25% off on pre-order" | It's twenty five percent off on pre-order right now, one forty nine instead of one ninety nine, and the first run ships in October. I left the link below. |

Average cut 2.2s (reference 1.5s). Machine-readable: `beat-map.json`. Board frames: `board-frames/c01..c15.jpg`. Contact sheet: `_qa-storyboard.jpg`.

### The hook is the only place the reference's footage is mirrored

c01 and c02 are the reference's own split-screen: Birkin street footage top, creator bottom, phrase caption between. The editor sources two short street clips of a Birkin being carried (the frames on the board are the reference's own, placeholders only, they never ship). c03–c05 are the creator full frame carrying the agitation and the pivot, the way the reference holds on its creator for its longer lines. Everything after 0:10.5 is the bag.

### Overlay spec (mirrors the reference)

- Typeface **Didot** (system), white, soft dark drop shadow, no box, no scrim.
- Cards: 120px Didot main line, 56px sub line, centred at y≈980 so the card sits across her chest, never her face. c05 holds "The perfect one / if it's the shape you love"; c06 holds "The Vivienne / Velantra" over the bag, the way the reference puts its n°4 card over the Margaux. c03–c04 carry lowercase phrase captions on the talking head.
- Phrase captions: 58px Didot, lowercase, centred at y≈1200, 2 to 5 words, one per cutaway. Not word-synced; one phrase per shot, like the reference.

### The close is one unbroken screen recording

c15 runs 7.5s and carries the entire offer and CTA. The ad ends on the website and never cuts back to the bag. One slow continuous downward scroll: title and $199.99 struck to $149.99 → Add to Cart → the "Expected to ship October" paragraph settles and holds. Captured at 500px CSS window width the day the ad ships.

---

## Production recipe

| Step | How |
|---|---|
| VO | `vo/VO-tight.mp3` (33.15s) from `vo/VO-raw.mp3` (36.72s), Woman Over 40 `NBIPq5xdnIg9kaBH5Ape`, eleven_v3 Creative, one take, ad-engine job `job_71b8bf93dfe9`. 3.57s of silence removed by `vo/tighten_vo.py`, no sample stretched. Ship as is, no atempo. |
| Creator | HeyGen: upload the approved keyframe → `POST /v3/avatars` photo → poll until `completed` → `POST /v3/videos` `type: avatar`, `engine: avatar_v`, `audio_asset_id` = VO-tight, 1080p. ~235 api credits for 33s; check `wallet.remaining_balance` first. Full frame, no key: she is on screen for c01–c05 (0:00–0:10.5), the bottom half of the split and then the whole frame. |
| Cutaways | `broll/final/O*.mp4` at the in-points in `beat-map.json`. Two sourced Birkin street clips for the split hook. |
| Overlays | `build_board_frames.py` already renders the cards and captions; the same functions draw them onto the final at the same coordinates. This machine's ffmpeg has no drawtext, so overlays are Pillow PNGs composited per cut. |
| Assembly | one ffmpeg pass, 1080x1920, 24fps CFR, VO at -14 LUFS, cutaway audio muted, hard cuts only. |
| QA | Scribe on the finished audio (brand card spelled "Velantra"); frame QA on every Vivienne cut for hardware and softness; overlay never crosses a face. |

**Gate:** nothing renders until the keyframe and the board are approved on Cutroom. HeyGen has not been fired.

---

## Superseded versions (kept for the record)

| | What | Why it died |
|---|---|---|
| v1 | Top-5 ranking, Birkin neutralized to "the one everybody recognizes on sight" | Brooks: keep the Birkin angle, we target people who want a Birkin-inspired bag. VO in `vo/v1-no-birkin-rejected/` |
| v2 | Top-5 ranking with the Birkin restored (Bottega, The Row, Valextra, Delvaux, Vivienne at #1), 70.49s | Brooks: drop the ranking, mirror the look only, house script. VO in `vo/v2-top5-birkin-superseded/`. Competitor facts verified 9/1 live in the project memory if a ranking ever comes back |
| v3 | House script, hook straight into "But I have the perfect one for you", 28.91s | Brooks: reads as "this is a Birkin"; needs one sentence of agitation and a pivot keyed to the shape. VO in `vo/v3-no-agitation-superseded/` |

---

## Self-audit

- Product intro reads exactly `This is the Vivienne from Velantra.` and lands at 0:10.9 (later than the 0:06 law because Brooks added the agitation sentence).
- The hook resolves inside itself: the Birkin is the problem, the shape is what she loves, the perfect one is here.
- Six-month test: nothing seasonal. Swap test: same silhouette, belted brass turn lock, vegetable-tanned leather, braided trim, no logo, soft; another bag breaks the stack.
- No em dashes, no not-X-it's-Y, no fragment stacks in spoken lines, no personification, no Hermès, no competitor, no invented fact, no origin claim, no capacity claim, no "structured". Birkin in VO and captions only, never in a generation prompt.
