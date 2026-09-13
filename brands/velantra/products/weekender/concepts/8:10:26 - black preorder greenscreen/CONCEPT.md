# UGC-BLK-01 — "The One I Won't Be Careful With"

**Date:** 2026-08-10
**Product:** The Eleanor Weekender in **Black** · $159.99 (compare $209.99) · pre-order, ships mid September 2026
**Format:** ~53s greenscreen talking head, creator PiP bottom-left over full-frame b-roll, burned captions, 1080x1920
**Funnel:** MOF / warm. Same slot as the Dark Chocolate announcement it forks.
**Delivered:** `VEL-WEEKENDER-UGC-BLK-01-wont-be-careful.mp4` — in `ugc-blk-01-production/` and
copied into the product's `video/` library. Rebuild end to end with `python3 build.py`.

---

## What this is a variation of

The live Facebook ad `facebook.com/reel/2872770126402572` (posted 8/09, "Summer sale live now!!")
is `VEL-WEEKENDER-UGC-DC-04-they-finally-did-it-v2.mp4` — the Dark Chocolate announcement from
`concepts/8:8:26 - dark chocolate announcement`. Same creator, same greenscreen-over-b-roll
grammar, same one-take VO, same caption treatment. This is that ad rebuilt for Black.

**Everything structural is held:** the creator (identical avatar, re-lip-synced, not re-cast), the
PiP position and scale, the every-2-to-3-second cut rhythm, the offer beat landing on a website
scroll, one continuous ElevenLabs VO with no chaining.

---

## The one thing that could not be ported, and what replaced it

DC-04's spine is **"they finally did it, look at this color."** That works when the bag is in
stock, in hand, and the creator can say she has carried it.

Black is a **pre-order**. Zero units exist. She cannot have carried one, and a novelty-of-the-color
read on an unshippable product is the weakest possible version of this ad. So the angle moves off
novelty and onto the mechanism the noir concept already identified:

> **Cream canvas is the reason the bag stays home.** Rain, a cab, a trip that isn't a clean one.
> All-leather deletes the hesitation. That is a product reason for the variant to exist, it belongs
> to us, and it survives a ship date six weeks out.

The creator's ownership claim also moves. In DC-04 she owns the bag being advertised. Here she owns
**a canvas colorway** — which is true of the actual delivered product line — and the black one is
the thing she just ordered. Nothing in the read requires a black bag to have shipped.

**The structural payoff:** the copy turn and the visual turn are the same cut. Beats 1 through 7 are
cream-canvas b-roll. On "They finally fixed that" at 18.42s it hard-cuts to black and never goes
back. DC-04 had no equivalent moment.

---

## Script (spoken, take 1)

> Okay, I have to admit something about this bag. I've had the Velantra Weekender for months, and
> there are trips I just don't bring it on. It's cream canvas. So if it's raining, or I'm getting in
> a cab, or it's not a clean trip, it stays by the door. They finally fixed that. It's up in all
> black now. No canvas anywhere, it's leather the whole way through. Same size, same shape, same
> gold hardware. And the inside is still that caramel, which against black looks so much better
> than it should. Three days of clothes, still fits the overhead bin. It's a pre-order, so it ships
> mid September, and they size the run off what gets ordered. Same one sixty. I already put mine in,
> because this is the one I actually won't be careful with.

**TTS input differs in one place:** the brand is fed as `Vell-Ahn-Trah`. Plain spelling returns
"Volantra" / "Velen Trail" — take 3 died on exactly that and was discarded.

---

## Beat map

| # | In | Line | Visual |
|---|---|---|---|
| 1 | 0.00 | "Okay, I have to admit something about this bag." | cream bag on the entryway bench |
| 2 | 2.42 | "I've had the Velantra Weekender for months," | cream bag, airport bench |
| 3 | 6.20 | "and there are trips I just don't bring it on." | cream bag styled on a bed, untouched |
| 4 | 9.55 | "It's cream canvas." | macro, canvas weave |
| 5 | 11.30 | "So if it's raining, or I'm getting in a cab," | cream bag in a car trunk |
| 6 | 14.75 | "or it's not a clean trip," | cream bag on a car seat |
| 7 | 16.20 | "it stays by the door." | cream bag by the door under the coats |
| 8 | **18.42** | **"They finally fixed that."** | **HARD CUT** — black, entryway floor |
| 9 | 20.00 | "It's up in all black now." | black, hotel luggage rack |
| 10 | 22.30 | "No canvas anywhere, it's leather the whole way through." | black, tight three-quarter on the body |
| 11 | 25.70 | "Same size, same shape," | black, carried down the hallway |
| 12 | 28.30 | "same gold hardware." | macro, turn lock |
| 13 | 30.10 | "And the inside is still that caramel," | macro, caramel interior |
| 14 | 32.50 | "which against black looks so much better than it should." | black, open and packed on the bed |
| 15 | 36.90 | "Three days of clothes," | hands packing a sweater in |
| 16 | 38.80 | "still fits the overhead bin." | black, airport bench |
| 17 | 40.50 | "It's a pre-order, ships mid September... Same one sixty." | live PDP scroll, Black selected |
| 18 | 47.70 | "I already put mine in," | black, picked up in the doorway |
| 19 | 50.20 | "because this is the one I actually won't be careful with." | black, carried down the stairs |

19 beats over 53.3s. Nothing repeats.

---

## Compliance

| Law | How it is held |
|---|---|
| Creator never speaks as the brand | "they finally fixed that", "they size the run". First person singular only for her own decision ("I already put mine in") |
| No fabricated scarcity | "they size the run off what gets ordered" is literally what a pre-order does. No countdown, no stock number, no "selling fast" |
| No fabricated social proof | She never claims to have used a black bag. Her ownership claim is the canvas colorway, which ships today |
| Ship date matches the PDP | "mid September" — the live description says "expected to ship mid September 2026" |
| Price matches the PDP | "same one sixty" — $159.99 on both, unchanged from the other colorways |
| No competitor comparison, no origin claim, no Birkin/Hermes | Nothing in the read names another brand or a country |
| No em dashes | Commas and periods only |
| One-take audio | One continuous ElevenLabs render. The lip-sync is driven by that file, never chained |
| No generated humans in action beats | The only person on screen is the deliberate synthetic presenter, same carve-out as DC-04 |

**Product truth held:** all smooth black leather with no canvas anywhere, caramel leather interior,
warm brass gold hardware, one size, 18 x 14.5 x 7. The VO says "no canvas anywhere" and the b-roll
has none.

---

## Production

| Stage | What ran |
|---|---|
| VO | ElevenLabs `Woman Over 40` (`NBIPq5xdnIg9kaBH5Ape`), `eleven_v3`, stability 0.0. 3 takes, all three STT-gated on word timestamps. **Take 3 failed on "Velen Trail" and was discarded.** Take 1 shipped (53.04s) over take 2 (51.38s) for the 1.0s pause before "They finally fixed that" — that pause is where the cream-to-black cut lands |
| Avatar | **No new avatar generated.** The DC-04 green clip was re-driven with the new VO through fal `fal-ai/sync-lipsync/v2`, `sync_mode: bounce`, which stretched 40.9s of source across 53.1s of audio. Same face as the ad running on Facebook, which is the point |
| B-roll | 15 black clips already on disk from the noir pre-order run (`broll/NB-01..15`) + 6 cream-canvas clips from the general and DC libraries. **Nothing new was generated** |
| Offer beat | Headless Chrome capture of the live PDP at `?variant=44355431596097`, panned in ffmpeg |
| Composite | ffmpeg. Beats cut to 1080x1920 → concat → chroma key the avatar to VP9 alpha → PiP at 44% width, bottom-left → one-take VO → Pillow caption cards cut on STT word timestamps |

### Two gotchas that carried over, three new ones

- **VP9 alpha must be force-decoded.** `-c:v libvpx-vp9` before the webm input or ffmpeg silently
  drops the alpha plane and the creator renders as an opaque green box.
- **The PDP gallery ignores the variant.** Capturing `?variant=<black>` still opens the carousel on
  the shared cream-canvas feature diagram, exactly as it did on the DC run. Fixed by starting the
  pan **below** the gallery, at the title, so the offer beat only ever shows the pre-order notice,
  the price, the Black swatch and the buy button. Never fight the carousel.
- **New: the chromakey has a hard cliff, and despill turns her sweater pink.** The fal round-trip
  re-encodes the green, so it is no longer the uniform `0x00882F` that keyed at similarity 0.08.
  Sampled range here is `0x006F21` to `0x00842C`. Swept on a single frame by reading the alpha
  plane directly (`format=yuva420p,chromakey=...,alphaextract`): **0.09 through 0.12 give a clean
  binary alpha; 0.16 collapses the whole subject to ~alpha 110** and everything downstream ghosts.
  Shipped at `0x007A28` / 0.11 / 0.02.

  The first pass also ran `despill=type=green:mix=0.5`, which is what the DC recipe used. On a
  **neutral cream sweater** that crushes the green channel and she renders visibly **pink**
  (measured 188 → 152 on G with R and B untouched). Despill is off entirely here; the measured
  green fringe from the key alone is **0.16% of subject pixels**. Any presenter in a neutral or
  warm garment needs despill checked, not inherited.
- **New: caption cards break on sentence boundaries, not every 4 words.** Fixed 4-word grouping
  produced cards like "it on. It's cream" and "the door. They finally". Cards are now capped at 4
  words *and* flushed at any word ending in terminal punctuation, so "They finally fixed that."
  gets its own card, which is the beat the hard cut lands on.

---

## Flagged, not acted on

- **The Facebook caption on the ad this forks is wrong on one fact.** It reads "It comes in three
  sizes." The Weekender is one size, 18 x 14.5 x 7. The same error is indexed publicly in the PDP's
  `global.description_tag`, which has been flagged on two previous runs and is still live. The new
  ad's copy does not repeat it.
- **No sale claim in this read.** The PDP is showing $209.99 struck through to $159.99, and the DC
  ad's Facebook copy ran a sale line. This VO says "same one sixty" and nothing about a sale, so it
  will not go false when the promo ends. If it runs against a live sale, put that in the ad copy,
  not in her mouth.
