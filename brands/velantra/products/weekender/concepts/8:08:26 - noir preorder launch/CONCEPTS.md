# Weekender in Black — Pre-Order Launch Concepts

**Date:** 2026-08-08
**Product:** The Eleanor Weekender in Black. All leather, no canvas. Same silhouette, same
opening mechanism, same caramel leather interior, same gold hardware.
**Mechanic:** Pre-order test. Ships mid-September.

---

## ⚠️ Assumptions I built on — confirm before anything sends

| Decision | What I used | Why / what to check |
|---|---|---|
| **Colorway name** | **"Black"** | Consistent with Light Chocolate / Army Green / Dark Chocolate, which are all plainly descriptive. "Noir" is the internal build code only, it does not appear in any customer-facing copy |
| **Price** | **$159.99**, same as the other colorways | Keeps the pre-order test measuring demand for the colorway rather than price elasticity. All-leather almost certainly costs more per unit than canvas-and-leather, so this may not survive contact with the agent's quote. One-line change in every asset if it moves |
| **Ship date** | **"Ships mid-September"** | Your "about a month" from 8/08, with buffer. **This has to be confirmed with the agent before send.** The Colette pre-order went out with an unconfirmed placeholder and we were then locked into honoring it |
| **Social proof** | **None used** | Zero delivered units means any review quote or "verified buyer" line would be fabricated. Same rule that reshaped the Colette pre-order statics |
| **Scarcity** | Only "the run gets sized from pre-orders" | Literally true of a pre-order. No countdown, no "selling fast", no invented stock number |

Everything below is built on generated imagery. **No physical black bag exists yet**, so there is
no real photography, no real UGC, and nothing in this campaign can claim anyone has used one.

---

## The angle both concepts share

The canvas colorways have one real, honest weakness: **cream canvas shows everything.** People
who love the bag still leave it at home when it is raining, when they are getting into a cab, when
the trip is not a clean one. All-leather removes that hesitation, and it is the actual reason this
variant should exist.

So the campaign is not "new color, it's pretty." It is **"this is the one you don't have to be
careful with."** That is a product mechanism, it belongs to us, and it gives a pre-order a reason
to exist beyond novelty.

Secondary beat in both: the **caramel leather interior**, which on the canvas colorways is a nice
detail and against black becomes the reveal.

---

## Concept A — VO-NOIR-01 · "Nothing To Be Careful About"

**Format:** Voiceover over b-roll. No creator on camera. ElevenLabs v3 Creative, one continuous
track, cut to Omni b-roll.
**Length:** ~34s
**Awareness:** Product-aware warm traffic and solution-aware cold. They know the silhouette.
**Placement:** Meta feed + reels, 9:16.

### Script (spoken)

> You know the bag you keep meaning to bring, and then you don't.
>
> Because it's cream, and it's raining, and you're getting into a cab.
>
> So it stays by the door.
>
> This is the same bag. Same size, same shape, same everything.
>
> Only there's no canvas on it anywhere. It's leather the whole way through.
>
> Inside is the same caramel lining, which against black looks better than it has any right to.
>
> Eighteen inches wide. Three days of clothes. Fits the overhead bin.
>
> It's on pre-order now, and it ships mid September.
>
> The Velantra Weekender, in black.

**TTS note:** feed the brand as `Vell-Ahn-Trah` in the ElevenLabs input and keep the plain
spelling in the human script. Plain "Velantra" returns "Volantra" reliably.

### Beat map

| # | Line | B-roll |
|---|---|---|
| 1 | "You know the bag you keep meaning to bring" | NB-01 entryway floor, coat above |
| 2 | "Because it's cream, and it's raining" | NB-05 car passenger seat, light moving |
| 3 | "So it stays by the door" | NB-01 hold / NB-10 closet shelf |
| 4 | "This is the same bag" | NB-03 hotel rack, slow orbit |
| 5 | "no canvas on it anywhere" | NB-15 macro gusset + eyelet (Ken Burns) |
| 6 | "the same caramel lining" | NB-14 macro interior (Ken Burns) → NB-02 open on bed |
| 7 | "Eighteen inches wide" | NB-04 carry hallway, scale reads |
| 8 | "on pre-order now, ships mid September" | NB-09 airport bench |
| 9 | "The Velantra Weekender, in black" | NB-11 nightstand lamp, gold catching light |

Opening two seconds are deliberately not the product, per the TOF rule. The bag does not appear
until beat 3.

---

## Concept B — UGC-NOIR-02 · "They Finally Made It In Black"

**Format:** AIUGC green screen talking head, keyed over full-frame b-roll. Creator on camera the
whole way, product b-roll behind her, new visual every 2 to 3 seconds.
**Length:** ~40s
**Placement:** Meta reels + TikTok, 9:16.

### Script (spoken)

> Okay so Velantra just dropped the Weekender in all black, and I need to talk about it for a
> second.
>
> This is the bag that's normally cream canvas with the leather. Really pretty. Also really easy
> to get dirty.
>
> This one has no canvas on it. None. It's black leather the whole way through. Same size, same
> shape, same everything else.
>
> The inside is still that caramel leather, which against the black looks so much better than it
> should.
>
> And it's eighteen inches wide, so it's an actual two to three day bag. Not a big purse.
>
> Here's the thing though. It's a pre-order. It ships mid September.
>
> So you're getting in line now, you're not buying it today and having it Thursday.
>
> I'd go look before they size the run.

**Voice rules applied:** she says "they" and "Velantra", never "we" or "our" — the creator never
speaks as the brand. She never claims to own one or to have used one, because none exist. No
review quotes.

### Production recipe (the DC greenscreen path, validated 8/08)

1. **VO:** ElevenLabs voice "Woman Over 40" `NBIPq5xdnIg9kaBH5Ape`, `eleven_v3`, stability 0.0,
   similarity 0.85. Generate 3 takes, gate with word-level STT, keep only a take that says the
   brand correctly.
2. **Avatar:** GPT Image 2 text-to-image keyframe (mid-40s woman, solid chroma green background,
   selfie framing, imperfection cues so she is never tack sharp) → Kling 3.0 i2v 15s "talking to
   camera", sound off → fal `fal-ai/sync-lipsync/v2` with `sync_mode: "bounce"` to stretch the
   15s clip across the full VO.
3. **Key + composite in ffmpeg, not ChatCut.** ChatCut has no chroma key and its cloud renderer
   drops VP9 alpha. Key to VP9-alpha webm, force `-c:v libvpx-vp9` on decode or the alpha is
   silently ignored, overlay onto the b-roll bed.
4. **Captions:** Pillow cards from STT word timings, 4-word cards.

### Beat map

| Time | Line | Behind her |
|---|---|---|
| 0-4s | "just dropped the Weekender in all black" | NB-03 hotel rack |
| 4-9s | "normally cream canvas… easy to get dirty" | NB-06 kitchen counter |
| 9-16s | "no canvas on it. None." | NB-15 macro gusset (KB) → NB-01 entryway |
| 16-22s | "same size, same shape" | NB-03 orbit / NB-10 closet shelf |
| 22-27s | "the inside is still that caramel leather" | NB-14 macro interior (KB) → NB-02 open |
| 27-32s | "eighteen inches wide, an actual two to three day bag" | NB-04 carry hallway |
| 32-37s | "it's a pre-order, ships mid September" | NB-07 packing hands |
| 37-40s | "before they size the run" | NB-09 airport bench → site scroll |

Website only appears at the offer push at the end, per the v2 rebuild note on the DC ad.

---

## B-roll library (15 clips, Omni)

Generated as GPT Image 2 i2i keyframes off the QA-passed NOIR picks, 3 variants each, then
animated. **Macros go to Ken Burns push-in, never to an i2v engine** — Omni re-synthesizes
hardware at high magnification and grows garbled engraving on gold plates.

| ID | Scene | Engine |
|---|---|---|
| NB-01 | Entryway floor, coat above, morning light | Omni |
| NB-02 | Open on unmade bed, packed, caramel interior | Omni |
| NB-03 | Hotel luggage rack, low three-quarter, lamp light | Omni |
| NB-04 | Carried at hip down an apartment hallway | Omni |
| NB-05 | Car passenger seat, late sun moving across leather | Omni |
| NB-06 | Kitchen counter with coffee and keys | Omni |
| NB-07 | Hands lowering a folded knit into the open bag | Omni |
| NB-08 | Hand lifting the bag off the floor by the handles | Omni |
| NB-09 | Airport departure bench beside her legs | Omni |
| NB-10 | Closet shelf beside folded clothes | Omni |
| NB-11 | Beside the bed under a warm lamp, gold catching | Omni |
| NB-12 | Carried down apartment stairs, low angle | Omni |
| NB-13 | Macro, front closure hardware | Ken Burns |
| NB-14 | Macro, caramel interior and slip pocket | Ken Burns |
| NB-15 | Macro, side gusset and gold eyelet | Ken Burns |

Motion prompts keep every hand on the rolled handles only. Nothing presses the flap, unfastens a
strap, or orbits the front clasp architecture, because that is what destroys this bag's hardware
in motion.
