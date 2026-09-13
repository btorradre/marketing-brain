# The Delphine — 5 VO ads, v3 (verdict framework)

**Built 2026-08-16.** `final/DEL-FALL-VO-01..05.mp4`, 9:16 1080×1920, 28–31s.
Scripts: `../SCRIPTS-v3.md`. Footage: the reusable library at `../../../broll/`.

## Voice

**Claire — "Ultra Real & Natural", middle-aged American** (`7A85ufQZSEaTbZ5eQ4f4`).
Brooks asked for a woman over 40. Two other 40+ candidates were generated and kept in
`tests/` (Kiora, Eryn); swapping is one line in `gen_vo.py`.

`eleven_v3`, Creative preset (stability 0.0, similarity 0.85). One continuous take per ad,
never per-line renders.

**Brand name:** the TTS input says `Vell-Ahn-Trah`. Plain "Velantra" returns "Volantra"
essentially every time. All five takes were STT-checked and land the "Vel-" onset.
(Only Vel/Vol is real signal — the a/e flips on the same audio and is jitter.)

## Structure

Verdict hook → brand named at ~4s → stacked physical reasons to believe → soft CTA.
No villain, no manufactured problem, no capacity overclaim. Every reason is a specific
physical fact about our bag, which is what stops it reading as a category ad.

| Ad | Hook | Opens on |
|---|---|---|
| VO-01 | "I think I found the perfect fall bag." | bench, autumn leaves |
| VO-02 | "If you're looking for a fall bag, this is the one to get." | walking, wet autumn street |
| VO-03 | "This is the fall bag I'd tell my sister to buy." | held at hip, full length |
| VO-04 | "I've been looking for a bag like this all year." | reaching into the closet |
| VO-05 | "Everyone keeps asking me where this bag is from." | carried on the elbow, out |

## Congruence — every line lands on the thing it names

| Line | Shot |
|---|---|
| "This is the Delphine, from Velantra" | bench hero |
| "structured, so it stands up on its own" | set down on a table, standing |
| "the flap is one piece of leather" | held up, flap readable |
| "rolled handles" | hand gripping the handles |
| "gold buckles on the sides" | macro, side roller buckle |
| "little gold feet on the bottom" | low macro, feet on stone |
| "no logo on it anywhere" | carried close, clean canvas |
| "wallet, cards, keys, a lip color" | flat lay of those items |
| "it closes" | wallet going into the open bag |
| "three colors" | Dark Chocolate |
| "one production run" | Army Green |
| CTA | walking away |

**"Three colors" shows DC and "one run" shows AG on purpose.** Light Chocolate carries the
rest of the ad, so across the spot the viewer actually sees three colorways. Showing LC again
on that line would make the claim visually false.

**Product-only.** No second bag appears in any frame. The closet shot was regenerated to remove
a straw basket from the background and a global no-other-bags clause now sits in every
generation prompt.

## Two bugs caught in build, worth keeping

1. **Hooks containing the word "this" were truncated.** The hook/body boundary was found by
   matching the first "this" after 0.5s, but three hooks contain "this" themselves
   ("…this is the one to get", "…where this bag is from"). VO-05 opened on the wrong shot as a
   result. Fixed by anchoring on "Delphine" and walking BACK to the "This" that introduces it.
   **Caught by contact-sheeting the hook frame of all five side by side** — it is invisible when
   you check one ad.
2. An em dash reached a caption. Removed; captions carry no em dashes.

## Notes

- Cuts land 120ms ahead of their anchor word; a cut on the word reads late.
- Captions are Pillow PNGs, never ffmpeg `drawtext` — this machine's ffmpeg has no libfreetype.
- The CTA names a live sale. **It must actually exist on the PDP before these run**, or swap the
  closing line for "so I'd go get one."
- Product is still a Shopify draft (`8041821143105`) at inventory 0. Nothing runs until it's live.

## 2026-08-16 REBUILD — sunglasses removed from the flatlay, VO-01 continuity fixed

**Why.** Brooks tightened the capacity claim (see PRODUCT-TRUTH.md): the provable load is a
wallet, cards, a lip color and keys. **Phone and sunglasses are banned.** A contact-sheet pass
over all five ads found **tortoiseshell sunglasses sitting in the flatlay in every ad**, on the
exact line "Wallet, cards, keys, a lip color". The visual was naming four items and showing five,
including the banned one. Every flatlay in the library had them, so there was no clean swap.

**How they were removed — NOT generatively.** A GPT Image 2 i2i edit was tried first and redrew
the bag as an all-leather product with no canvas and a rearranged composition: a product-truth
failure, discarded (6 credits). The fix that worked is deterministic and cannot touch the bag:
a clean linen swatch is mirror-tiled over the sunglasses through a feathered mask, exposure-matched
to the ring of pixels around the target. Script: `desunglass.py` in the session scratchpad, boxes
recorded per colorway. Originals kept at `broll/_variants/*-WITH-SUNGLASSES-orig.png`, old clips at
`broll/_retired-clips/`. All three colorways were fixed so the library itself is clean for reuse.

**LAW: to remove one object from an approved product frame, patch it, do not re-generate it.**
i2i on a full frame redraws the product. The bag is the one thing that must not move.

**VO-01 continuity.** Its hook was the bench in Light Chocolate and body slot 0 was the same bench
in Dark Chocolate, back to back, which reads as an error rather than a colorway reveal. Slot 0 now
uses a different shot entirely (`B11-carseat`) via the new `shot_swap` mechanism. The deliberate
three-colorway reveal still happens at slots 9 and 10, where it is doing real work.

**Known, still open:** the doorway shots (DC and AG, used on "Three colors" and "One production
run") have **a phone visible in her hand**. Not a capacity claim, so not a hard fail, but it sits
oddly on a bag whose copy deliberately excludes phones. Regenerating those two clips is the fix if
Brooks wants it.

**Canonical output is `../final-vo/`.** The five live there now; the 8/15 set moved to
`../final-vo/_v3-superseded-0815/`. `vo-v3/final/` holds the same five as the build's own output.

