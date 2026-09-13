# Velantra <> ecomflow — SKU List (built 2026-08-06)

Target sheet: `Velantra <> ecomflow | SKU List`
https://docs.google.com/spreadsheets/d/1kqszUVpM63CbWQimaHvFIdMf1mYxyKZ6XktUkwy9ydU/edit?gid=0

## How to load it

Header is row 5. Data starts at **B6**, where the two `ecomflow` placeholder rows sit.

1. Open the sheet, click cell **B6**
2. Paste the contents of `velantra_sku_list.PASTE-AT-B6.tsv` (headerless, tab-separated, so it lands one value per cell)
3. The two placeholder rows are overwritten by rows 1-2 of the paste

`Total Stock` (F3) and `Total SKUs` (G3) are formulas — `=SUM(F6:F1026)` and `=COUNTA(D6:D1026)` — so they update themselves. After paste they read **0** and **62**.

The paste file has no header line; the sheet already has one at row 5.

## What is in it

62 variant rows across 11 products, pulled live from Shopify (`uzdgxy-sb`) on 2026-08-06.

| Hero SKU | Product | Variants | Status |
|---|---|---|---|
| VEL-CAM | The Camille Boat Tote | 13 | Active |
| VEL-SOF | The Sofia Woven Tote | 8 | Active |
| VEL-MAR | The Margot Leather Tote | 6 | Active |
| VEL-ELE | The Eleanor Weekender | 2 | Active |
| VEL-COL | The Colette Wool Tote | 2 | Active (pre-order, ships Oct) |
| VEL-ING | The Ingrid Top Handle Tote | 3 | Draft, launching |
| VEL-ORG | Velantra Bag Organizer | 3 | Active |
| VEL-SCF | Velantra Bag Scarf | 11 | Active |
| VEL-CHM-HRS | Velantra Horse Charm | 5 | Active |
| VEL-CHM-CHY | Velantra Cherry Charm | 3 | Active |
| VEL-KEY | Boat Tote Keychain | 6 | Active |

### Deliberately excluded
- 3 dead duplicate Boat Tote products (`velantra-boat-tote`, `boat-tote`, `velantra-boat-tote-1`) — superseded by The Camille
- 2 dead duplicate Sofia products (`copy-of-velantra-straw-tote`, `the-sofia-woven-tote`) — superseded by `sofia-woven-tote`
- `velantra-straw-tote` — superseded by The Sofia
- The Rosalie Bow Tote — discontinued 2026-07-25
- Velantra Portico Bucket Bag — draft, never launched
- `__Customized-Items` — system placeholder, not a real product

## SKU convention

`VEL-<PRODUCT>-<COLORWAY>` — e.g. `VEL-CAM-NVY`, `VEL-SOF-CBK`, `VEL-ING-BDX`.
Limited-edition Camille colorways carry a `-LE` suffix (`VEL-CAM-SNVY-LE`).
Verified: 62 SKUs, zero collisions.

**These SKUs do not yet exist in Shopify.** Only The Rosalie Bow Tote ever had SKUs
(`velantra-bow-tote-sand` style), and it is discontinued. Everything else has a null SKU
on every variant. Once ecomflow signs off on this scheme, write it back to Shopify so the
two systems match — otherwise order routing has nothing to key on.

## Open gaps

**Weight — 15 of 62 rows filled from the manufacturer's agent (2026-08-07):**
Camille Boat Tote = 600 g (agent quoted 500-600 g, upper bound used) and Eleanor
Weekender = 1300 g (agent's 46 cm weekender figure; Eleanor is the 46×18×37 bag).
The agent's other weekender sizes (25 cm 700 g / 30 cm 900 g / 35 cm 1.1 kg) don't map
to any live Velantra product. Remaining 47 rows still TBC: Sofia, Margot, Colette,
Ingrid, Organizer, and all accessories need either agent estimates or a scale.

**Dimensions — 31 of 62 rows are TBC:**
- The Margot Leather Tote (6 rows) — no dimensions published on the PDP either, which is
  its own gap worth closing
- Bag Scarf (11), Horse Charm (5), Cherry Charm (3), Boat Tote Keychain (6) — accessories,
  never spec'd

Dimensions that ARE filled came from the live PDPs, converted to cm in L×W×H order:
Camille 51×20×36 · Sofia 30.5×15×24 · Eleanor 46×18×37 · Colette 50×18×26 ·
Ingrid 38×16×31 · Organizer 22×11.5×13.5 / 23.5×13×15 / 29×14×18

**Quantity — all zeros.** Shopify inventory is untracked (every variant reads negative,
Camille Navy is at -1005), so there was no real on-hand number to carry over. Fill in the
units actually being sent inbound to ecomflow's warehouse.

## Files
- `velantra_sku_list.PASTE-AT-B6.tsv` — headerless, paste this into B6
- `velantra_sku_list.tsv` / `velantra_sku_list.csv` — same data with header
- `push_to_sheet.py` — writes the 62 rows to B6 via the Sheets API. Blocked until the
  sheet is shared as Editor with btorradre@btoecventures.com (verified 403 on 2026-08-07).
