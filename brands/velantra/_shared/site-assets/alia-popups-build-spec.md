# Velantra — Alia Product Popups · Build Spec

**Goal:** Email/SMS capture with a **10% off first order** welcome offer, one tailored popup per product page.
**Store:** velantrafashion.com · 13 active products · Currency USD
**Build in:** Alia dashboard → *Experiences* (Alia has no API, so these are built by hand using the specs below).

> **How to read this:** Part 1–3 are GLOBAL — set them once and reuse on every popup. Part 4 is the per‑product variable copy (the only thing that changes between popups). Build the Boat Tote first as your master, then **duplicate it** in Alia and swap in each product's Part‑4 row.

---

## PART 1 — Brand Kit (matches velantrafashion.com)

| Token | Value |
|---|---|
| Display font (headlines) | **Abel** (fallback: Arial Narrow / Helvetica) |
| Body font | **Assistant** (fallback: Helvetica, Arial) |
| Background / card | `#ffffff` |
| Primary text | `#000000` |
| Accent panel / highlight | `#f6f1eb` (warm cream — the store's announcement-bar color) |
| Buttons | Fill `#000000`, text `#ffffff`, **square corners** (no radius) |
| Hairlines / borders | `#e0dfdf` |
| Logo | Wordmark **VELANTRA**, uppercase, wide letter‑spacing, black |
| Voice | Quiet luxury, warm, honest, confident — never hypey |

**Layout feel:** generous whitespace, product photo on one side, copy on the other (stacked on mobile). Match the email we built (`straw-tote-delay-email.html`).

---

## PART 2 — Global Popup Settings (apply to ALL 13)

**Experience type:** Multi‑step capture ("offer") — email primary, SMS optional/skippable.

**Step flow (same skeleton on every popup):**
1. **Hook** — product image + headline + subhead + button. *(copy per product, Part 4)*
2. **Engage** — one tappable question with 2–4 answer chips. *(Alia's signature step; gives zero‑party data + lifts conversion. Question per product, Part 4.)*
3. **Email capture** — "Where should we send your 10% off?" → email field → button **Get my 10% off**.
4. **SMS (skippable)** — "Want launch + restock alerts by text too?" → phone field + consent line → **Skip** link.
5. **Success** — reveal the code + button **Apply & shop**. *(success line per product, Part 4.)*

**Trigger:**
- Desktop: **5s delay OR 35% scroll** (whichever first) + **exit‑intent** as a backup catch.
- Mobile: **6s delay OR 35% scroll** (no exit‑intent on mobile).

**Frequency / audience:**
- Show to **non‑subscribed visitors only**; suppress for anyone already on the list.
- If dismissed, **re‑show after 7 days**. After they subscribe, **never show again**.
- Devices: desktop + mobile (mobile = bottom sheet/drawer).

**Consent (required):**
- Email step: marketing‑consent microcopy — "By signing up you agree to receive Velantra emails. Unsubscribe anytime."
- SMS step (TCPA): "By entering your number you agree to receive recurring marketing texts from Velantra. Msg & data rates may apply. Reply STOP to opt out." Phone must be **explicitly opted in**, never pre‑checked.

---

## PART 3 — The 10% Discount (set up before launch)

**Two ways to deliver the code — pick one:**

- **A. Single code `WELCOME10` (simplest, launch‑ready):** one Shopify discount, 10% off, **limit one use per customer**. Success‑step button auto‑applies via:
  `https://velantrafashion.com/discount/WELCOME10?redirect=/products/<product-handle>`
  (drops the customer back on the product with the code live in cart.)
- **B. Unique codes per subscriber (better, anti‑abuse):** connect Alia ↔ Shopify discounts so each subscriber gets a one‑time code. No static link — Alia shows the code + a copy/apply button.

**Recommended discount rules (Shopify → Discounts):**
- 10% off entire order · **one use per customer** · **new email subscribers**
- Optional: minimum order (e.g. $40) so it doesn't wipe margin on a $7.99 charm
- Optional: exclude already‑discounted/sale items
- Set an expiry on the customer's code (e.g. 14 days) to create urgency

*(I can create code `WELCOME10` for you via the Shopify connection in ~10 seconds — just confirm the rules.)*

---

## PART 4 — Per‑Product Copy (the only thing that changes)

Each popup targets **URL path contains `/products/<handle>`**. Use the product's own hero image (URLs below).

### Hero Bags

**1. Velantra Boat Tote** — `velantra-boat-tote-2` · $54.99 *(flagship — build this one first as the master)*
- **Hook H1:** The tote that started it all.
- **Subhead:** Join the Velantra list for 10% off your Boat Tote — plus first dibs on new colorways.
- **Engage Q:** Which color are you eyeing? → *Navy · Emerald · A solid shade · Still deciding*
- **Success:** Here's 10% off — your Boat Tote's waiting.
- *Image:* `…/01_9646591c-8d25-4eb1-b49d-2e477a5534e9.jpg`

**2. Velantra Weekender** — `velantra-weekender` · from $124.99
- **Hook H1:** Made for the long weekend.
- **Subhead:** Take 10% off the Weekender — premium canvas, leather trim, built to travel.
- **Engage Q:** What's it for? → *A weekend away · Carry‑on travel · Everyday/gym · A gift*
- **Success:** 10% off — packed and ready.
- *Image:* `…/light_chocolate_1.png`

**3. Velantra Meridian Tote** — `velantra-meridian-tote` · $99.99
- **Hook H1:** Structure meets softness.
- **Subhead:** 10% off the Meridian — grained leather that works as hard as you do.
- **Engage Q:** Which Meridian suits you? → *Black · Brown/Coffee · Cream/Taupe · Show me all*
- **Success:** 10% off your Meridian — enjoy.
- *Image:* `…/brown_1.webp`

**4. Velantra Portico Bucket Bag** — `velantra-portico-bucket-bag` · $99.99
- **Hook H1:** The bucket bag, elevated.
- **Subhead:** 10% off the Portico — soft leather, room for everything that matters.
- **Engage Q:** How will you carry it? → *Everyday · Work · Going out · A bit of everything*
- **Success:** 10% off the Portico is yours.
- *Image:* `…/portico_black_hero.png`

**5. Velantra Evening Bag** — `velantra-evening-bag` · $49.99
- **Hook H1:** Quiet luxury, after dark.
- **Subhead:** 10% off the Evening Bag — a statement that whispers.
- **Engage Q:** What's the occasion? → *Date night · Wedding/event · Everyday elegance · Treating myself*
- **Success:** 10% off — see you at golden hour.
- *Image:* `…/image_W2r.png`

**6. Velantra Straw Tote** — `velantra-straw-tote` · $119.99 · ⚠️ **DELAYED / restock pending**
- **Hook H1:** Summer's most‑wanted tote.
- **Subhead:** Join the list for 10% off — and be **first to know the moment it's back in stock**.
- **Engage Q:** When will you carry it? → *Beach days · City summer · Vacation · Gifting*
- **Success:** You're on the list — 10% off + first access when it ships.
- *Special:* This one doubles as a **back‑in‑stock waitlist** (it's the delayed product). Lean on "first access," not "buy now." Ties directly to the delay email.
- *Image:* `…/shot1_handheld_front.png`

**7. Velantra Jelly Tote** — `velantra-jelly-tote` · $79.99
- **Hook H1:** Translucent. Playful. Yours.
- **Subhead:** 10% off the Jelly Tote — 15 colors that catch the light.
- **Engage Q:** Pick your shade → *Brights · Pastels · Clear/Neutral · All of them*
- **Success:** 10% off your Jelly Tote — go bold.
- *Image:* `…/jelly-tote-aqua….png`

**8. Velantra Leather Handbag** — `velantra-leather-handbag` · $109.99
- **Hook H1:** The look you've been saving for — for less.
- **Subhead:** 10% off the Leather Handbag — elevated craftsmanship, sized and colored your way.
- **Engage Q:** Which size calls you? → *Mini · Classic · Larger · Help me choose*
- **Success:** 10% off your handbag — quiet luxury, unlocked.
- *Image:* `…/leather-handbag-black….jpg`

### Accessories (lighter, impulse tone)

**9. Bag Scarf** — `bag-scarf` · $9.99
- **Hook H1:** The finishing touch.
- **Subhead:** 10% off your first order — tie on a Bag Scarf and make any bag yours.
- **Engage Q:** Styling it on → *My Boat Tote · A leather bag · A gift · Just browsing*
- **Success:** 10% off — go add the perfect scarf.

**10. Velantra Horse Charm** — `velantra-horse-charm` · $7.99
- **Hook H1:** A little equestrian elegance.
- **Subhead:** 10% off your first order — the Horse Charm that finishes the look.
- **Engage Q:** Where's it going? → *On my tote · On a handbag · A gift · Collecting them*
- **Success:** 10% off — pick your charm.

**11. Velantra Cherry Charm** — `velantra-cherry-charm` · $9.99
- **Hook H1:** Sweet little statement.
- **Subhead:** 10% off your first order — add a Cherry Charm and stand out.
- **Engage Q:** Your vibe → *Cherry Red · Black · Pink · One of each*
- **Success:** 10% off — treat your bag.

**12. Boat Tote Keychain** — `boat-tote-keychain` · $9.99
- **Hook H1:** The Boat Tote, in miniature.
- **Subhead:** 10% off your first order — the collectible keychain everyone's clipping on.
- **Engage Q:** Clipping it to → *My keys · My bag · A gift · Collecting*
- **Success:** 10% off — grab your mini.

**13. Velantra Bag Organizer** — `bag-organizer` · $19.99
- **Hook H1:** Everything in its place.
- **Subhead:** 10% off your first order — the felt insert that keeps your bag flawless.
- **Engage Q:** Organizing which bag? → *Tote · Handbag · Multiple bags · Not sure yet*
- **Success:** 10% off — get organized.

---

## PART 5 — Build Order in Alia

1. **Set up the discount** (Part 3) so the code exists first.
2. In Alia, build the **Boat Tote** popup fully (Parts 1+2+4) — this is your master/brand template.
3. **Duplicate** it 12×; for each copy, change only: **targeting URL**, **hero image**, **hook H1**, **subhead**, **engage question/chips**, **success line** (Part 4).
4. Set each one's **page targeting** to its product handle.
5. **QA:** preview each on desktop + mobile; submit a test email and confirm the code applies via the success button.
6. Turn them live in batches (heroes first), watch Alia's conversion rate, then refine the weakest hooks.

---

## PART 6 — Strategy Notes (worth knowing)

- **Per‑product is the advanced play.** Most stores run ONE site‑wide welcome popup. Doing it per product wins on relevance (the hook names the exact bag) + the engagement question gives you zero‑party data to segment future emails. Worth it on the 8 hero bags; on the 5 cheap accessories it's lower‑leverage — totally fine to point those pages at a single shared accessory popup if 13 becomes a lot to maintain.
- **Don't double‑pop.** If you also run a global welcome popup, exclude product pages that have their own, or visitors get two popups.
- **Straw Tote popup = your delay safety net.** Because it's out of stock, that popup captures demand as a waitlist and pairs with the delay email — nobody who wants it slips away.
- **Suppress for buyers.** Exclude existing customers/subscribers so you're not flashing "10% off your first order" at people who already bought.
