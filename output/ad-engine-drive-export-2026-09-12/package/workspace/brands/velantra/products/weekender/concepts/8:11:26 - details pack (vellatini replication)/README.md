# Details Pack — Vellatini replication (Weekender + Colette)

Reference: TrendTrack `vellatini-Uzptt3` (Vellatini, active 57 days, US, "Exclusive Sale Is LIVE: 50% OFF Sitewide").
Copy hook on the reference ad: *"Maturing as a man is realizing you need a bag too..."*

## What the reference actually is

20.0s, 9:16, 30fps. **A spoken voiceover front-loads the whole argument in the first 4.5
seconds, then hands off to music for the remaining 15.5s.** ElevenLabs Scribe with
`diarize=true` separates the two cleanly:

| speaker | span | content |
|---|---|---|
| `speaker_0` (VO) | 0.20–4.54s | "Nothing upgrades a man faster than a good bag. The difference is in the details" |
| `speaker_1` (track) | 4.62–19.18s | Gigi Perez, "Sailor Song" |

The VO itself is two lines with a 0.70s beat between them: L1 0.20–2.64s (2.44s), L2
3.34–4.54s (1.20s).

⚠️ **The on-screen text is a CAPTION OF THE VO, not a substitute for it.** Both lines are
spoken *and* burned in, synchronised, with the text lingering after the voice stops (L1 text
0–3.3s vs voice ending 2.64s; L2 text 3.5s to the end vs voice ending 4.54s). A first pass on
this teardown read the Scribe output as if it were reading the burned-in text and concluded the
ad was music-only. Scribe is audio-only, so anything it returns was *heard*. Always diarize.

Four-act structure (scene scores confirm the cut points):

| act | window | what happens | shots |
|---|---|---|---|
| A — arrival | 0.0–3.3s | model enters a cafe, bag on shoulder, sits | 3 quick beats ~1.1s |
| B — settle | 3.3–7.2s | seated, laptop out, bag beside him | 3 beats ~1.3s |
| **C — THE PACK BLOCK** | **7.2–14.8s** | **locked-off tabletop. Bag centred, mouth to camera. Items in a flatlay in the foreground go in ONE AT A TIME, and the flatlay visibly depletes** | **7–8 inserts, ~0.95s each** |
| D — departure | 14.8–20.0s | lifts the bag, walks out the door, street wide | 4 beats ~1.3s |

**The whole ad is act C.** A and B are the life-wrapper; D is the payoff. Act C is a single
locked camera where only the hand and the flatlay change, which is why this reference is
uniquely cheap for us to clone: it is a stills sequence, not a moving shot.

## Why it works (psychology)

1. **Category permission, then proof.** L1 gives the viewer permission to want the thing;
   L2 ("details") reframes the next 11 seconds so every insert reads as evidence of quality
   rather than as a list of stuff.
2. **The depleting flatlay is the mechanism.** Capacity is not claimed, it is *counted*. The
   viewer watches seven objects leave the table and none of them come back. That is a
   demonstration, and demonstrations do not get argued with.
3. **No face, no pitch, no creator.** The model never addresses camera. It reads as observed
   lifestyle, so it never triggers ad-defences, and it lets trending audio carry the retention.
4. **Luxury claim last.** Nothing about price, brand or status until the departure shot, by
   which point utility is already proven.

## Our adaptation

The reference's hook is a **men's category-permission play** — "should a man own a bag at all".
That tension does not exist for our avatar, so the hook is **re-derived, not translated**.
Both cuts cast women (Brooks, 8/11). The aphorism *shape* of L1 is kept because that shape is
the style being cloned; the *tension* underneath it is replaced.

| | Weekender | Colette |
|---|---|---|
| tension | one bag vs. checked luggage | which bag goes with this outfit |
| L1 | *Nothing changes how you pack faster than the right bag.* | *Nothing pulls an outfit together faster than the right bag.* |
| L2 | *Three days. One bag.* | *The difference is in the details* |
| VO voice | ElevenLabs **Kiora** `hGQkZQUA5RiOXIw7P9iO` | ElevenLabs **Katie** `T720RsqorTx4ZZWohrNN` |
| VO span | L1 0.08–2.82s · L2 3.80–5.36s | L1 0.12–3.82s · L2 4.80–6.68s |
| colorway | Light Chocolate (released) | Caramel |
| pack surface | white quilted duvet, bedroom | white marble bistro table, cafe terrace |
| end card | none | **Pre-order · ships October** |

Both lines are spoken over burned-in captions, exactly as the reference does it. The VO is
**one continuous take per ad** covering both lines (never one render per line), `eleven_v3` at
stability 0.0. Three takes each were generated and transcribed word-level; the pick was made on
whichever take's internal rhythm sat closest to the reference's 2.44s / 0.70s gap / 1.20s
cadence. Caption in and out points are then driven off the picked take's real word timings
rather than guessed, so the text appears with the voice and lingers past it.

Voices are carried over from the 8/10 linear-story ads for the same two products, so a viewer
who sees both cuts hears one consistent voice per bag.

Weekender L2 is a live-PDP-safe claim (holds three days of clothing, overhead bin).
Colette carries no possession or availability language anywhere, so the pre-order end card is
the only stock statement in the cut.

### Pack-block item order (the depletion sequence)

**Weekender** — a three-day pack, so the block *is* the "three days" proof:
sweater → jeans → linen shirt → toiletry pouch → sandals → book → sunglasses

**Colette** — her week, weighted away from work (the Margot owns the work slot):
scarf → book → water bottle → laptop → pouch → sunglasses → market flowers

## Build architecture

Act C is built as **locked GPT Image 2 i2i stills, hard-cut** — never animated. This is forced
by the Weekender open-bag law (motion destroys the flap and front hardware, and keyframe mode
does not rescue it) and by the Omni Colette failure mode (secondary hand actions mutate the
straps and vanish the belt). It is also simply what the reference *is*: a locked camera.

Acts A, B and D come from the existing b-roll libraries rather than new generations:
- Weekender: `broll/lc-travel-S01..S17` (Light Chocolate, one consistent model)
- Colette: `broll/library-2026-08/clips/VEL-COL-*` (caramel-trim clips only; the espresso
  clips are a different colorway and must not be intercut)

Finishing: mandatory ffmpeg degrade pass on every segment (see
`project_linear_story_ugc_ads` memory) — Omni/GPT output denoises to a clean CGI look
otherwise. No vignette.

### Audio

This is a **Meta** ad (the reference ran 57 days in the US Meta library), so the ad carries its
own audio and there is no in-platform trending track to add at upload. The master needs a bed
baked in.

- **VO:** ElevenLabs `eleven_v3`, one continuous take, stems in `audio/VO-*.mp3`.
- **Bed:** ElevenLabs **Music** (`POST /v1/music`, `music_length_ms`) — commercially licensed,
  unlike the reference's Sailor Song. Stems in `audio/music-bed.mp3`. Higgsfield's
  `generate_audio` cannot be used for this: it is speech-only and its own tool contract says to
  decline standalone music rather than substitute a speech model.
- **Mix:** bed ducked to 0.17 under the VO, ramping to full over 1.2s once the VO's last word
  lands, then `loudnorm=I=-14:TP=-1.5:LRA=11`. Every generated bed was transcribed before use to
  confirm it carried no vocals.
- **Verification:** the finished master is re-transcribed and must return the VO text verbatim.
  If Scribe cannot read the VO out of the mix, neither can a viewer with the sound low.

## Props law applied

Reject any prop that is a recognisable branded design. The first scout roll produced
Hermes Oran-style H-cutout sandals on 2 of 3 Weekender frames; the prompt now pins
"one single plain wide band, no cut out shapes, no letter shapes". Laptop lids and book
covers are pinned blank.
