# Colette Pre-Order Statics — Vestirsi swipe pack (2026-08-05)

6 static ads for The Colette Wool Tote pre-order, each adapted from a Vestirsi reference.
Angle: pre-order announcement ("our most anticipated fall essential"), fall aesthetic.
References scanned from TrendTrack (saved in scratchpad as ref_*.jpg/png).

## Avatar read

**Vestirsi's avatar:** "the woman with somewhere to be." 30-55, busy, polished, quiet
luxury taste. Buys $250 Italian leather as the smart alternative to $3k designer. Their
palette: warm cream, chocolate, mauve. Type: wide-tracked light sans + occasional Didone
serif, tiny brand mark anchor.

**Our avatar shift:** same woman through the Velantra discernment lens. She could buy
designer, chooses not to. Fall is texture season for her; the Colette is the cashmere-soft
everything bag of fall. Mood she responds to hardest: deep cozy fall warmth. Espresso and
chestnut grounds that make the pale oatmeal wool glow, late-afternoon window light, plush
knits. Every backdrop in this pack runs warmer and darker than Vestirsi's summer refs.

## Honesty adaptations (locked)

- Refs 3 (FuER7l) and 5 (0KS5N1) are review-quote statics. The Colette is pre-order with
  zero delivered buyers, so NO fabricated "Verified Buyer" quotes. Those slots convert to
  craftsmanship and capacity claims.
- No Loro Piana or unnamed-icon reference anywhere (locked 7/27).
- Body claim = "cashmere-feel brushed wool" ONLY. No fiber claims, no Italian leather.
- Offer truth: $149.99 pre-order, $189.99 after launch ($40 off before it ships),
  ships early October. No BNPL.

## The 6 ads

| # | Ref | Format kept | Our adaptation |
|---|-----|-------------|----------------|
| A | bZ27Fi "BACK IN STOCK" | Studio still, 2 bags, tracked sans announcement top | Both colorways on warm deep-greige drape. "NOW ON PRE-ORDER" / "Our Most Anticipated Fall Essential" |
| B | lh5lTB VESTIRSI manifesto | Model from behind, bag on shoulder, centered wordmark + line | Camel coat, caramel Colette. VELANTRA wordmark + "The first bag of fall. Now on pre-order." |
| C | FuER7l review quote | Dark chocolate backdrop, hero bag, centered white stack | Craftsmanship swap: "THE TOTE THAT FEELS LIKE A COAT" / "Cashmere-soft brushed wool. Now on pre-order." |
| D | 4sG2ve split lifestyle + lineup | Top lifestyle crop w/ manifesto, bottom colorway band | "One bag, Monday to Sunday." top; Caramel + Espresso lineup band from existing v3 fronts |
| E | 0KS5N1 what's-inside | Open bag with contents, proof headline | Capacity swap: "THE EVERYTHING BAG OF FALL" / "Holds your whole day. Keeps its shape." |
| F | 5QA0c0 flat-lay serif | Top-down on draped fabric, Didone serif announcement | Chocolate wool blanket, caramel Colette. "The First Bag of Fall" serif / "Pre-order now. Ships early October." |

## Primary text (Ads Manager body copy)

- **A:** Our first fall bag is officially on pre-order. The Colette Wool Tote, in
  cashmere-feel brushed wool with leather trim, in Caramel or Espresso. Reserve yours for
  $40 off before it ships in early October.
- **B:** Summer had its bag. This is fall's. The Colette Wool Tote is now on pre-order,
  $40 off before it ships in early October.
- **C:** The difference is in the fabric. The Colette's body is brushed wool with a
  cashmere-soft hand, so it dresses like your fall coats and holds its shape on its own.
  Now on pre-order, $40 off before it ships in early October.
- **D:** Your week doesn't slow down in the fall. The Colette carries the laptop, the
  book, the sweater, all of it, and still looks put together at dinner. One bag, Monday
  to Sunday. Pre-order in Caramel or Espresso.
- **E:** Twenty inches across, and the shape barely moves when it's full. The Colette
  Wool Tote is the bag your whole fall fits inside. Pre-order now and save $40 before it
  ships in early October.
- **F:** The first bag of fall is here. The Colette Wool Tote, now on pre-order in
  Caramel and Espresso. $40 off until it ships in early October.

## Pipeline

1. `gen_plates.py` — text-free plates via kie.ai GPT Image 2 i2i, anchored on the
   approved v3 canonicals (real-photo-anchor law). 9:16 + 4:5 per concept.
2. `compose_ads.py` — Pillow overlays. Didot.ttc idx 0 (serif heads), HelveticaNeue.ttc
   idx 7 Light (tracked sans + subheads), real VELANTRA wordmark inverted white.
3. QA every plate against the no-3D-render law + Colette construction (belt ends curve
   outward with gold disc caps, both handles, brushed wool not knit). Regen failures.
4. Finals → `products/cashmere-tote/concepts/2026-08-05-preorder-statics/`.
