# The Colette — Positioning + Pre-Order Email Flow
*Locked by Brooks 2026-07-27 · angle drives ALL Colette creative (email, ads, PDP)*

## LOCKED ANGLE

**"The cashmere-soft everything bag of fall — the one bag that goes with everything you own from September on, and makes all of it look intentional."**

- **Closet slot:** the seasonal handoff from the Sofia. Summer's bag was about where you were going; the Colette is the ONE bag by the door from September to March. The default she stopped choosing.
- **The physics of "goes with everything":** every other bag is leather or canvas and sits ON TOP of a fall outfit. The Colette is brushed wool — it dresses like her clothes do (camel coat, cream cardigan, trench, denim). It doesn't match an outfit; it matches the season.
- **Daily reel (outcome scenes):** Monday laptop + planner, stands upright under the desk → Wednesday passenger seat, coffee run, open-top throw-in → Saturday market, kid's water bottle, her cardigan. One bag, Monday to Sunday. Outcome = she stopped switching bags; out the door faster, one decision lighter.
- **Identity:** the softly put-together woman. No logos, nothing shouting — cashmere-soft texture is the quietest expensive signal there is. Every outfit she already owns looks *finished*.
- **Line discipline:** the Margot owns "the perfect work bag" (leather, turn lock, office armor). The Colette NEVER competes for that slot — work is one scene in her week, not the identity. Soft everything bag that happens to swallow a laptop.

## PRE-ORDER EMAIL FLOW (campaign sequence, standard launch audience)

| # | Send | Subject | Job |
|---|------|---------|-----|
| E1 | Day 0 | Meet the Colette — the first fall bag | Announcement / seasonal handoff (LIVE draft, angle-tuned 7/27) |
| E1b | Day 1 | (booster) | Non-openers of E1, house pattern |
| E2 | Day 2-3 | One bag, Monday to Sunday | The angle deep-dive: week reel + texture physics + interior/capacity |
| E3 | Day 4-5 | Caramel, or Espresso? | Colorway decision helper + "pre-orders decide the run" |
| E4 | Day 6-7 | Last call at the pre-order price | $149.99 → $189.99 deadline + founder note + summer proof |

- Audience: include First-Time Buyers `6a34f290fbb65567455d0485` + Repeat Buyers `6a34f291aad55fe582bba43d`; exclude Purchased Last 5 Days `6a34f28f4978cecb92fcdea5` + **Purchased Colette** segment (line-item title contains "Colette") so buyers drop out of E2-E4.
- All sends GATED on Brooks + supplier ship date ("early October" placeholder).
- Files: `_shared/omnisend/omnisend/colette-preorder-e{1,2,3,4}.html`. Fluid-width rules apply (no fixed widths, literal UTF-8, [[unsubscribe_link]], 600px/24px screenshot verify).

**BUILT 2026-07-27 (all DRAFT, sends gated):**
| Email | Template ID | Campaign ID |
|---|---|---|
| E1 (angle-tuned in place) | 6a67a7a6c31c42f96af098ee | 6a67a7b0e55c140707da1e9c (contentID 6a67a7b036bb799a50b07f88) |
| E2 | 6a67ddf375fad0eeb532730e | 6a67de782a2ab80968020536 |
| E3 | 6a67de1e75fad0eeb5327367 | 6a67de960a1a952a4772a495 |
| E4 | 6a67de57bb78ee810e07f688 | 6a67de970a1a952a4772a496 |

**Purchased Colette (pre-order)** exclusion segment: `6a67ddbe2c5ce05a83b63697` (event placed order, origin shopify, `raw.line_items.[].title` contains "Colette"; self-maintaining). Excluded on E2-E4 only — E1 predates any purchase. All three new emails screenshot-verified in the 600px/24px container.

**LAUNCHED 2026-07-27 ~9pm PT.** Product ACTIVE (URL 200-verified pre-send). E1 SENT (~30s full delivery; subject/h1 changed to "Meet Colette" per Brooks). Booster `6a682afe64c63678baec8276` created as draft-with-delay BEFORE parent send (Flow 1) → auto-scheduled Jul 29 04:08Z (+24h, nonOpeners, subject "Still here: the first fall bag"). E2 scheduled Jul 30 17:00Z · E3 Aug 1 17:00Z · E4 Aug 3 17:00Z. Ship-date placeholder "early October" shipped as-is on Brooks's send order — confirm supplier lead time and honor or correct it before fulfillment.
- Image pool (Shopify CDN, v3 set): editorial bench (E1 hero), caramel front (E2 hero), caramel interior (E2 capacity), caramel side + colorway 2-up (E3), caramel side (E4 hero).

## Copy guardrails (per house rules)

No LP/icon references · "cashmere-feel"/"cashmere-soft" only, never a fiber claim · no origin claims, no "Italian leather" · sign "Brooks, Founder" · no vignettes/personification · simple reading level · Margot's "work bag" phrase never used for the Colette.
