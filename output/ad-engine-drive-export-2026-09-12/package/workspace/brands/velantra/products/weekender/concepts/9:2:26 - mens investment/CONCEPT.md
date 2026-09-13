# VEL-WEEKENDER-INVEST-01 — "The one purchase I tell every guy to make"

**Date:** 2026-09-02
**Product:** The Eleanor Weekender · $159.99 (compare $209.99) · Light Chocolate / Army Green / Dark Chocolate / Black (pre-order) · all live 9/02
**Audience:** MEN. Investment angle: the purchase that pays for itself, the bag you buy once.
**Reference:** `instagram.com/reels/DZOsGdmMppU/` · 21.5s · Poke "10/10 male purchases (luxury edition), but they get increasingly more niche" · local copy `reference/poke-10of10-ref.mp4`
**Format:** AI UGC greenscreen mirroring the reference: 2x2 photo GRID hook with a big centred title, then one still per beat with a short lower-third label, hard cuts every 1.5-3s, creator keyed over the middle-bottom of the frame and cut by the bottom edge. One VO on the gringo clone. 1080x1920, ~28s
**Funnel:** TOF cold
**Angle:** the one purchase (investment) · **Mechanism:** structure (holds its shape packed or empty)

---

## Reference autopsy (watched frame by frame, `_engine/mcp/ad-engine/data/watch/job_d16d7aac2857/`)

| Beat | Time | VO | On screen |
|---|---|---|---|
| Hook | 0:00-0:03 | "10 out of 10 male purchases, but they get increasingly more niche" | **2x2 grid** of four aspiration photos (shopping bags, indoor pool, Soho street, Amex Black), thin dark gutters, big white title "10/10 Male Purchases (Luxury Edition)" centred, creator inset over the middle |
| Items 1-5 | 0:03-0:12 | Equinox membership · Loro Piana Summer Walks · 500ml Le Labo · cashmere sweater · vintage Cartier Tank | One still per item, hard cut every 1.1-3.7s, small white lower-third label repeating the item name |
| Sponsor as item 6 | 0:12-0:16 | "An AI personal assistant like Poke to message you about your daily client meetings" | Screen recording of the app, same label treatment, no change in energy |
| Items 7-8 | 0:16-0:21 | Soho shopping · Amex Black · Chrome Hearts ring "that makes every handshake feel financially irresponsible" | Same grammar, ends on a joke |

What we take: the grid hook, the title, the label-per-beat rhythm, the creator centred over the image. What we change: the list is the hook only; from 0:04 the whole body is our bag (house formula, product intro by 0:07).

---

## Script (locked, Brooks 9/02 · hook 4 of 5 · price removed, sale pushed)

> The one purchase I tell every guy to make before he books another trip. A weekend bag that holds its shape.
> This is the Velantra Weekender.
> Full grain leather over woven canvas, no logo on it, and it stands up on its own, packed or empty.
> I've dragged mine through three airports in two months and it still looks new.
> Three days of clothes, laptop in the slip pocket, straight into the overhead bin.
> Four colors, and they're running a sale on it right now, so this is the time.
> I left the link below.

92 words · take A on the gringo clone = **27.7s, 204 wpm, brand clean** (take B 29.0s, STT "Velentra" = jitter only). Every claim is on the live PDP. No price spoken; the price is visible in the real screen recording at the close.

---

## Storyboard — 13 beats

| # | Lands | Line | On screen | Label |
|---|---|---|---|---|
| 1 | 0:00 | The one purchase I tell every guy to make before he books another trip. | **GRID hook** (three variants in `plates/`, A-travel is the default) | TITLE: *The one purchase / every guy should make* |
| 2 | 0:04 | A weekend bag that holds its shape. | Real footage, closed bag front (R1) | a weekend bag that holds its shape |
| 3 | 0:06.5 | This is the Velantra Weekender. | Bag held up to camera at the gate (B7) | the Velantra Weekender |
| 4 | 0:08.5 | Full grain leather over woven canvas, | Macro, hand on the closure (B4) | full grain leather over woven canvas |
| 5 | 0:10.5 | no logo on it, | Real footage, blank leather front with hand for scale (R2) | no logo on it |
| 6 | 0:11.5 | and it stands up on its own, | Standing on the extended carry-on handle (B3) | stands up on its own |
| 7 | 0:13 | packed or empty. | Real footage, open and empty, still square (R3) | packed or empty |
| 8 | 0:14 | I've dragged mine through three airports in two months and it still looks new. | Walking the terminal, bag riding the carry-on (B2) | three airports, still looks new |
| 9 | 0:18 | Three days of clothes, | Open and packed on the hotel bed (B5) | three days of clothes |
| 10 | 0:19.5 | laptop in the slip pocket, | Laptop sliding into the interior at the gate (B10, the 9/01 K11 pick) | laptop in the slip pocket |
| 11 | 0:21 | straight into the overhead bin. | Hands lifting it into the bin (B6) | straight into the overhead bin |
| 12 | 0:22.5 | Four colors, and they're running a sale on it right now, so this is the time. | **Brooks's real screen recording**: PDP swatches → price → add to cart → cart drawer | four colors, on sale now |
| 13 | 0:26.5 | I left the link below. | Checkout frame | link below |

### Grid hook variants (`plates/`)

| Plate | Tiles (TL, TR, BL, BR) | Read |
|---|---|---|
| **GRID-A-travel** (default) | terminal walk · cab back seat · hotel on carry-on · overhead bin | The trip. Closest to the reference's lifestyle grid |
| GRID-B-product | real closed front · hardware macro · packed on bed · full body hotel | The object. Strongest product read |
| GRID-C-mixed | full body hotel · terminal · macro · packed | Half and half |

All tiles are QA-passed frames from HAALAND-01 / MENSID-01 or Brooks's own 4K footage; the bag is in every tile.

---

## Creator

Same recipe as HAALAND-01: **C1** (`../9:2:26 - erling haaland/casting/C1/v1.png`, HeyGen look `34134762f59286a9a55afbf85193a936`) rendered on Avatar V from take A. Positioned per the reference: **centred**, head 20% of frame width, body running 60px past the bottom edge (no side cut this time, the reference creator sits over the middle of the image). Labels at y1640 across his chest.

## Production

- `_build/build_ad.py bed | C1` (env `VOICE=gringo-A|gringo-B`, `GRID=GRID-A-travel|GRID-B-product|GRID-C-mixed`)
- Zero new product generation. One HeyGen render (~85 api credits for 28s).
- Labels are per beat (the reference's grammar), not word-synced captions.
- Screen recording slowed to fill beats 12-13, ends on Checkout.

## Built (9/02)

- HeyGen Avatar V render on C1 from take A: video `59a3cecf888efdf9b02601e26861f1bf`, 27.7s, green `0x2AA637`. Composite: head 508px on the plate → 459x816 at x=247 y=1164 (centred, cut by the bottom edge), head top y=1289.
- **`final/VEL-WEEKENDER-INVEST-01-C1-gringo-A-A.mp4`** · 28.2s · -14.0 LUFS (VO lifted 1.1 dB on this take) · zero black frames · grid A hook.
- Swap the grid with `GRID=GRID-B-product python3 build_ad.py C1` (no re-render needed); swap the take with `VOICE=gringo-B` (needs a HeyGen re-render).

## Laws checked

Formula intact (hook with verdict → name at 0:06.5 → stack → proof → capacity → variants → offer → link) · materials literal and on the PDP · no gendered word on the bag · no competitor, no price comparison, no origin claim · "they're running a sale" (third person about the brand) · sale visibly true on the live page 9/02 · no em dashes · no season peg.
