---
name: velantra-boat-tote
description: Product scale for the Velantra Boat Tote. Trained on 14+ colorways including canvas-and-leather two-tone variants (navy, red, pink, dark green, olive green, orange, sunny yellow, yellow, emerald green, lady pink, light grey, lineman) and fully solid-color variants (solid green, solid navy, solid olive green, solid orange, solid pink, solid red, solid yellow). Use this skill whenever generating images, video, or ad creative (ad replication, video scene replication, B-roll sourcing) for the Velantra Boat Tote specifically, so every generation is anchored on the real, current product rather than an outdated or invented one.
---

# Velantra Boat Tote — Product Scale

This skill is the product-specific reference for the Velantra Boat Tote (internally also called the "Boatkin"), a premium canvas tote bag. It exists to keep every downstream generation — ad replication, video scene replication, B-roll sourcing, static or video ad production — anchored on the real, current product identity instead of an outdated or hallucinated one.

**Why this matters:** a real ad previously shipped showing a design of this bag that doesn't actually exist. The mistake happened because an old (retired) reference image got mixed in with current ones and the generation leaned on a text description instead of a verified photo. The rules below exist specifically to stop that from happening again.

## MANDATORY: paste the identity block verbatim into every generation prompt

The "Locked Product Identity" section below is copied character-for-character from the source spec. Do not paraphrase it, summarize it, "clean it up," or reword it when using it in an image/video generation prompt — copy it verbatim. It is written the way it is (short fragments, ALL-CAPS emphasis, explicit negatives) specifically to stop a generation model from inventing wrong colorways, hardware, or construction details. Any rewording risks losing the exact constraint that prevents the hallucination.

---

## Locked Product Identity (verbatim — paste into generation prompts)

**Category:** Premium canvas tote bag, Birkin-inspired silhouette.

### Visual Description (⚠️ CORRECTED 2026-07-24 — Brooks caught a shipped ad with a nonexistent design; anchor EVERY generation on a verified current colorway reference image, never on this text alone)

- **Silhouette:** soft structured tote, Birkin-inspired outline, SOFT slouchy canvas body with gentle pleats at the lower corners — NOT stiff/boxy
- **Body:** natural cream/ivory canvas INCLUDING the fold-over top edge — the top of the bag is ALWAYS cream. There is NO wide colored top section, NO colored yoke, NO colored leather upper band. A colored top yoke = invented product, regenerate on sight.
- **Trim (THIN straps only):** two slim colored top handles, ONE thin colored belt strap high across the front with a small gold turn lock at its center (plus two small gold keeper bars), TWO colored vertical straps running from the belt down the front to the base, colored trimmed bottom edge. White contrast stitching on all trim.
- **Hardware:** ONLY the small gold turn lock + the two small gold belt keepers. No Kelly-style clasp plates, no big V-straps with silver/gold plate tips, no corner patches, no feet visible in most shots.
- **Construction:** cream canvas + thin colored trim two-tone (Solid colorways are the exception: fully colored body).

### Available Colorways

**Two-tone (cream canvas body + thin colored trim):**

| Colorway | Notes |
|----------|-------|
| Navy | Very dark navy trim, near-black |
| Red | Deep red trim |
| Sunny Yellow | Warm mustard-yellow trim |
| Emerald Green | Rich emerald trim |
| Lady Pink | Soft coral-pink trim |
| Light Grey | Light grey trim |
| Lineman | Lineman colorway |

Note: this skill's own description also names pink, dark green, olive green, orange, and yellow as additional two-tone colorways beyond the seven above — carried over as-is from the source spec, which does not give them their own reference-image row in this table. Treat those five as existing colorways to confirm against a verified current photo before generating, the same as any other colorway; don't invent trim details for them from the text alone.

**Solid (fully colored body, no two-tone canvas):**

| Colorway |
|----------|
| Solid Green |
| Solid Navy |
| Solid Olive Green |
| Solid Orange |
| Solid Pink |
| Solid Red |
| Solid Yellow |

---

## The reference-image law (the most important rule in this document)

When generating any image or video of this product, always anchor the generation on a real, verified-current photo of the specific colorway — never on the text description alone, and never on an outdated reference photo.

This product previously existed in an earlier, now-retired design (chunky leather trim, wide colored top sections, fully-colored bodies) that has since been replaced by the current design described above (thin trim, cream top, gold turn-lock only). A real ad shipped showing the *retired* design because an old reference image was mixed in with the current ones — an expensive, avoidable error.

Before starting any generation work on this product:

1. **Confirm which reference images represent the current, live product versus the retired design — don't assume, verify.** If you're pulling from a shared product-image library, retired-design images (chunky trim, wide colored top, all-colored bodies) may still be sitting alongside current ones.
2. **Always generate from the current, verified reference photo for the specific colorway being used** — never rely on the written Visual Description above as a substitute for an actual reference image. The text description is a checklist to QA against, not a generation source on its own.
3. **If a pipeline or tool auto-loads reference images from a shared library, double-check it isn't silently pulling in retired-design images alongside current ones.** When in doubt, specify the exact current reference image explicitly rather than trusting an automatic selection.
4. **Each colorway should have multiple reference angles/shots available** — ideally at least one straight-on/front view and one detail/hardware shot. Use the most direct, unambiguous angle as the primary anchor for any new generation, and cross-check the result against a second angle if the first result looks uncertain.
5. **A model-worn/carrying reference shot per colorway is also valuable** for lifestyle or UGC-style generations, since it shows scale and drape on a body.

## QA standard before delivering any generated asset

Before delivering any generated image or video containing this product, compare it side-by-side against the verified current reference photo for that exact colorway and confirm every element in the Locked Product Identity above is correctly represented:

- Cream top with no colored yoke
- Thin trim only (no chunky leather trim)
- Small gold turn-lock only (no Kelly-style clasp plate, no big V-straps)
- Soft, slouchy silhouette (not stiff/boxy)

Any deviation from the locked identity is a **defect, not a stylistic choice** — regenerate rather than accepting it. If a generated frame shows a colored top yoke, wrong hardware, or a stiff/boxy body, that is an invented, incorrect product.

## Using this with downstream generation work

When running ad replication, video scene replication, or B-roll sourcing for the Velantra Boat Tote:

1. Load the correct colorway's verified current reference photo(s) — never the retired-design flats.
2. Paste the Locked Product Identity block above verbatim into the generation prompt alongside the reference image(s).
3. Apply the reference-image law and QA standard above to every output before it ships.
4. To force a specific colorway, explicitly name that colorway's verified current reference image(s) rather than letting an automatic/registry-driven selection choose for you.

## Related

- **Concept/brief companion:** velantra-boat-tote-concept — decides *what* the ad says (angle, hook, script, brief); this skill helps *render* it accurately.
