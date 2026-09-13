# Motilli — Official Brandkit

*Source: live crawl of getmotilli.com via Firecrawl, 2026-04-21*
*Store URL: https://www.getmotilli.com*

---

## 1. Brand at a Glance

| Field | Value |
|---|---|
| **Brand Name** | Motilli |
| **Tagline (functional)** | "The First Gummy Designed for GLP-1 Side Effects" |
| **Category** | Digestive Health Supplement (Gummy) |
| **Target Audience** | GLP-1 users (Ozempic®, Wegovy®, Mounjaro®, Zepbound®) suffering digestive side effects: delayed gastric emptying, sulfur burps, constipation, bloating, nausea |
| **Core Promise** | Wake up the stomach's natural rhythm so GLP-1 users can keep their medication AND their dignity |
| **Authority Anchor** | "Gastroenterologist-Recommended Formula" |
| **Guarantee** | 90-Day Money Back Guarantee |
| **Pricing Signal** | "About a dollar a day" vs. "$400 on Miralax, magnesium, fiber powders and probiotics that didn't work" |
| **Channel** | DTC only — *"Not Available on Amazon or in Stores"* |
| **Shipping** | 1 business day handling, 2–4 day US delivery, free >$45 |

---

## 2. Brand Positioning

### Core Positioning Statement
> **"Stop treating your colon. Start supporting your stomach."**

### The Wedge (vs. Laxatives / Miralax)
Motilli's entire narrative is built on a single mechanism wedge: **laxatives work on the colon — six feet downstream from the actual problem.** GLP-1 drugs slow gastric emptying, so the problem is *upstream* in the stomach. Motilli is the only product designed to treat the correct organ.

### The 4 Pillars of the Brand Story
1. **"Wrong Organ"** — Every other product (laxatives, fiber powders, probiotics) targets the colon. That's the wrong end.
2. **"Upstream Fix"** — Natural prokinetic compounds (apigenin from celery juice) restore stomach motility at the source.
3. **"Stay on Your Meds"** — Users shouldn't have to choose between weight loss and dignity. Motilli manages the side effects.
4. **"Gentle, Not Violent"** — No cramping, no urgency, no emergency bathroom trips. Predictable mornings.

---

## 3. Logo System

**Primary Logo (dark/brand):**
`assets/motilli_logo_primary.png`
Source: https://www.getmotilli.com/cdn/shop/files/motilli_logo-topaz-sharpen-upscale-4x_Medium_07791a67-e530-4d26-b59b-a0ae169e9f63.png

**White Logo (for dark backgrounds):**
`assets/motilli_logo_white.png`
Source: https://www.getmotilli.com/cdn/shop/files/white_logo.png

### Usage Rules
- **Always pair logo with generous whitespace.** The header on the live site uses ~123px of vertical clear space (`--header-height: 123px`).
- **Never tint the logo** with any non-brand color. Use primary on light; white on brand green or dark photography.
- **Do not stretch, rotate, or add drop shadows.**

---

## 4. Color System

Pulled directly from the live Shopify theme's CSS custom properties.

### 4.1 Primary Palette

| Token | Hex | Role | Notes |
|---|---|---|---|
| **Motilli Green** | `#94C218` | Primary brand color — CTA, selected states, bar borders | Signature celery/apigenin green |
| **Hover Green** | `#9ACD32` | Button hover, secondary accent | Slightly yellow-shifted |
| **Deep Green** | `#7DA614` | CTA button base before hover | Darker action state |
| **Leaf Green** | `#4CAF50` | Occasional supporting green (icons, checks) | — |

### 4.2 Accent Palette

| Token | Hex | Role |
|---|---|---|
| **Signal Pink** | `#EF4A65` | Urgency / main accent callouts (`--color-main-accent`) |
| **Light Pink** | `#FFEAEE` | Light accent washes (`--color-light-accent`) |

### 4.3 Neutrals

| Token | Hex | Role |
|---|---|---|
| **Ink Black** | `#000000` | Body text (`--color-text`) |
| **Charcoal** | `#2A2A2A` | Heading alt |
| **Mid Gray** | `#5F6264` | Secondary text / subcopy |
| **Light Mute** | `#555555` | Subtitle gray (`--bar-subtitle-color`) |
| **Line Gray** | `#E5E5E5` | Borders / dividers |
| **Canvas Gray** | `#F5F5F5` | Image/section background (`--image-bg-color`) |
| **White** | `#FFFFFF` | Primary surface, cards |

### 4.4 Product Bundle / Proof Palette

| Token | Value | Role |
|---|---|---|
| Bundle bar bg | `rgba(239, 250, 209, 1)` | Soft celery-tint background |
| Selected bundle bar | `#FFFFFF` | Active state |
| Bundle border | `rgba(148, 195, 14, 0.3)` | Inactive |
| Bundle border selected | `#94C218` | Active |
| "Most Popular" badge bg | `#94C218` | Primary |
| "Most Popular" badge text | `#FFFFFF` | — |
| Label bg | `rgba(233, 247, 194, 1)` | Pale celery |

### 4.5 Payment Proof Colors (for checkout trust badges)

| Hex | Source |
|---|---|
| `#006FCF` | American Express blue |
| `#EB001B` | Mastercard red |
| `#231F20` | Apple Pay / PayPal black |
| `#243044` | Diners Club navy |

### 4.6 Palette Usage Rules
- **60/30/10 ratio:** White 60% / Neutral gray 30% / Motilli Green 10%.
- **Pink is a scalpel, not a brush.** Use `#EF4A65` only for "stop-and-read" urgency elements (sale ribbons, savings %, scarcity, error).
- **Greens don't mix.** Pick one green per surface — never stack `#94C218`, `#4CAF50`, and `#7DA614` side-by-side.

---

## 5. Typography System

### 5.1 Fonts
The Shopify theme runs a single font stack:

```css
--font-body:    'Inter', sans-serif;
--font-heading: 'Inter', sans-serif;
```

**Primary typeface: Inter** (Google Fonts, variable weight 100–900).
Recommended display pairing if expanding for marketing collateral: **Inter Display** (headlines) + **Inter** (body).

### 5.2 Type Scale (fluid, from live site)

| Role | Min | Max | Weight |
|---|---|---|---|
| H1 | 32px | 48px | 700 bold |
| H2 | 28px | 40px | 700 |
| H3 | 24px | 32px | 600–700 |
| H4 | 20px | 24px | 600 |
| H5 | 18px | 20px | 600 |
| H6 | 16px | 18px | 600 |
| Body Large | 18px | — | 400 |
| Body | 16px | — | 400 |
| Body Small | 14px | — | 400 |
| Caption | 12px | — | 400 |

### 5.3 Letter Spacing

```css
--letter-spacing-heading: -0.9px  /* tight, modern */
--letter-spacing-body:    -0.3px  /* slight negative tracking */
```

### 5.4 Weight Tokens
- Regular: 400
- Semibold: 600
- Bold: 700

### 5.5 Button Type
- `text-transform: uppercase`
- `font-size: 13px`
- Color: white on Motilli Green (`#FFFFFF` on `#7DA614` → `#94C218` on hover)
- Border radius: `25px` (fully rounded pills for nav buttons, `nav-btn-border-radius`)

---

## 6. UI Component Tokens

| Element | Token | Value |
|---|---|---|
| Card bg | `--card-bg-color` | `#FFFFFF` |
| Content bg | `--content-bg-color` | `#FFFFFF` |
| Image bg | `--image-bg-color` | `#F5F5F5` |
| Bundle bar radius | `--bar-border-radius` | `16px` |
| Bundle image radius | `--bar-image-border-radius` | `6px` |
| Variant select radius | `--bar-variant-select-border-radius` | `8px` |
| Product image radius | `--kaching-bundle-products-image-border-radius` | `8px` |
| Nav button radius | `--nav-btn-border-radius` | `25px` (pill) |
| Nav button stroke | `--nav-btn-stroke-width` | `2px` |
| Bundle thumb image size | `--bar-image-size` | `48px` |
| FAQ padding | `--question-padding` | `15px 20px` |

---

## 7. Voice & Tone

### 7.1 Voice Attributes
1. **Mechanism-first, not flowery.** Every claim ties to a named compound (apigenin, chlorophyll, FOS) or an anatomy-specific promise (stomach, not colon).
2. **Direct, plainspoken, zero fluff.** No "wellness speak" ("journey", "balance", "holistic"). Instead: "cement stomach", "rotten-egg burps", "emergency bathroom trips."
3. **Empathetic but unapologetic.** The brand validates suffering ("those brutal GI side effects") then immediately redirects to mechanism ("it's a stomach problem, not a colon one").
4. **Comparative.** The brand is always defining itself against laxatives, Miralax, fiber powders, probiotics — never in isolation.
5. **Outcome-specific, timeline-bound.** "Within 1–5 days…", "by week 4…", "90 days to feel the difference."

### 7.2 Tone Dials

| Dial | Motilli Setting |
|---|---|
| Clinical ←→ Casual | **60% clinical / 40% casual** — mechanism-heavy but written plain |
| Emotional ←→ Rational | **55% rational / 45% emotional** — facts first, feel second |
| Serious ←→ Playful | **80% serious** — this is a dignity problem, not a joke |
| Formal ←→ Familiar | **75% familiar** — "you", direct address, user POV |

### 7.3 Do / Don't Language

**DO use:**
- "Wake up your stomach's natural rhythm"
- "Works where the problem actually is"
- "Upstream, not downstream"
- "Stop treating your colon. Start supporting your stomach."
- "Gentle, predictable motility"
- "Keep the results. Ditch the side effects."
- "About a dollar a day"
- "Clockwork mornings"
- "Cement stomach" (for constipation)
- "Rotten-egg burps" (for sulfur burps)
- Specific drug names: Ozempic®, Wegovy®, Mounjaro®, Zepbound®

**DON'T use:**
- "Detox" (unless paired with "natural" and ingredient mechanism)
- "Cure", "heals", "treats" disease (supplement compliance)
- "Cleanse" as a standalone concept
- Medical diagnosis language
- Weight-loss primary benefit (Motilli is adjunct, not substitute)
- Laxative synonyms ("flush", "purge", "clean out")
- Generic wellness words: "holistic", "balance", "wellness journey", "revolutionary"

### 7.4 Signature Headline Patterns

- **The Mechanism Flip:** *"Your GLP-1 side effects aren't a laxative problem."*
- **The Organ Specificity:** *"Stop treating your colon. Start supporting your stomach."*
- **The Promise + Proof:** *"Feel the difference in 90 days or get 100% of your money back."*
- **The Math of Failure:** *"Compare that to the $400 you've already spent on Miralax, magnesium, fiber powders, and probiotics that didn't work."*
- **The Identity Preservation:** *"You shouldn't have to choose between the weight loss and your dignity."*

### 7.5 Tagline Options (distilled from site)

- **Functional:** "The First Gummy Designed for GLP-1 Side Effects"
- **Positioning:** "Stop treating your colon. Start supporting your stomach."
- **Outcome:** "Clockwork mornings for GLP-1 users."
- **Promise:** "Keep your medication. Keep your dignity."

---

## 8. Product & Ingredient Language

### 8.1 Four-Ingredient Story (use this exact naming)

| Ingredient | Mechanism Claim | Compound Named |
|---|---|---|
| **Celery Juice Extract** (Premium Concentrate) | "Natural prokinetic that wakes up stomach muscles and gets digestion moving again." | Apigenin |
| **Chlorophyll Complex** (Natural Source) | "Nature's deep green cleanser — neutralizes hydrogen sulfide gas at the source, not just the smell." | Sodium copper chlorophyllin |
| **Prebiotic Fiber** (5g Per Serving) | "Rebalances gut bacteria for predictable, comfortable mornings." | FOS (fructooligosaccharides) |
| **Vitamins A, C, K, B6 & Folate** | "Replenishes the essential nutrients your body needs for energy, immunity, and overall wellbeing." | — |

### 8.2 Format Descriptors
- "Pectin-based — melts instantly, easy on sensitive stomachs"
- "Vegan, non-GMO, pectin-based gummy"
- "2 gummies daily, 30–60 minutes before your largest meal"

### 8.3 The "What to Expect" Timeline (reuse verbatim)

1. **Week 1:** "Bloating starts to ease. Your first comfortable movement. The 'cement stomach' feeling begins to lift."
2. **Week 2:** "Sulfur burps reduce or stop. Less nausea after meals. You start trusting your stomach again."
3. **Week 3–4:** "Energy levels stabilize. The brain fog lifts. Mornings become more predictable."
4. **Day 90:** "Full digestive balance restored. Clockwork mornings. You forget what it was like before."

---

## 9. Offer Architecture

| Tier | Language | Savings Claim |
|---|---|---|
| 2 bottles | "Buy 2 Get 1 Free" | **SAVE 64%** |
| 3 bottles | "Buy 3 Get 2 Free" | **SAVE 68%** (most popular) |

### Offer Copy Elements
- **Risk reversal:** "90-Day Money Back Guarantee"
- **Shipping anchor:** "Free US Shipping On All Orders Over $45"
- **Scarcity/Exclusivity:** "Not Available on Amazon or in Stores"
- **Seasonal overlay:** "Spring Sale! Try It Risk Free For 90 Days!"
- **Unauthorized-seller warning:** "Beware of unauthorized sellers — only orders from our store include the 90-day money back guarantee."

---

## 10. Social Proof System

### 10.1 Review Anchor
- **Rating:** 4.9 / 5.0
- **Label:** "Excellent"
- **Header:** "From Real GLP-1 Users — Real Reviews"

### 10.2 Canonical Testimonial Headlines (use these exact phrases)
- "Feel like a different person"
- "The only thing that helped"
- "Less bloating within 3 days"
- "Gave me my mornings back"
- "Finally feel normal again"

### 10.3 Review Construction Formula
**[Medication name] + [specific pain metric] + [timeline] + [outcome identity shift]**

*Example:* "I've been on Ozempic for 3 months and the constipation was unbearable — 4 days without going, my stomach felt like cement. After one week of Motilli, I finally feel normal again."

---

## 11. Comparison Framework (always-on device)

The comparison table is a core brand device. Always present Motilli against "Miralax & Laxatives" on these 6 rows:

1. Targets Stomach Motility (The Actual Problem)
2. Stops Sulfur Burps at the Source
3. No Cramping, No Urgency
4. Restores Energy & Mental Clarity
5. Designed Specifically for GLP-1 Users
6. Contains Prebiotic Fiber + Vitamins

**Motilli wins every row.** Competitor column is intentionally empty/negative.

---

## 12. FAQ Voice Template

Every FAQ answer follows: **[Direct answer] → [Timeline or metric] → [Low-risk out]**

Example:
> **When will I see results?**
> Most customers notice improvements within 1–5 days. Bloating and sulfur burps typically improve first, followed by more regular digestion. Full benefits are usually felt by week 4.

---

## 13. Photography & Visual Direction

### 13.1 Hero Composition Rules
- **Product on clean white or pale celery-green (`rgba(239, 250, 209, 1)`) background.**
- Include the gummy-scatter shot alongside the bottle for tactile credibility.
- Lifestyle photography: warm, natural daylight, kitchen/countertop context, NOT gym or weight-loss imagery.

### 13.2 Asset Types in Use on Site
- Bottle hero (3/4 angle on white)
- Exploded gummies (top-down on pale green)
- Label close-up (supplement facts readable)
- Before/after belly illustrations
- Doctor portraits (authority: Dr. Rebecca Marsh, Dr. Sarah Chen, Dr. Langford)
- Hand-held product (scale/lifestyle)
- Mechanism diagrams (stomach anatomy)

### 13.3 Diagram Style
Flat illustrated anatomy, gentle green accents, **NOT photorealistic medical imagery**. The visual brand is consumer-friendly, not clinical.

### 13.4 Iconography
- Rounded 2px stroke (matches `--nav-btn-stroke-width: 2`)
- Pill-radius containers (`25px`)
- Green on white or white on green — never multi-color icons

---

## 14. CTA System

| CTA Position | Copy |
|---|---|
| Primary (product card) | **"Add to Cart"** / **"Get Motilli"** |
| Bundle selector | **"SAVE 64%" / "SAVE 68%"** (percentage, bold, uppercase) |
| Page-top bar | **"Spring Sale! Try It Risk Free For 90 Days!"** |
| Secondary | **"Continue Shopping"** |
| Trust reinforcer (below CTA) | **"90-Day Money Back Guarantee"** + payment icons |

CTA Button spec:
- Bg: `#7DA614` → hover `#94C218`
- Text: `#FFFFFF`, 13px, **UPPERCASE**, weight 700
- Radius: fully rounded (pill)

---

## 15. Compliance & Disclaimers (critical)

Motilli is a **dietary supplement** — every piece of copy must respect:

- No disease claims ("treats", "cures", "prevents").
- Always include: *"Motilli contains vitamins, minerals, and plant-based extracts commonly found in dietary supplements. As with any supplement, we recommend consulting your healthcare provider."*
- GLP-1 trademarks always follow ® on first use: Ozempic®, Wegovy®, Mounjaro®, Zepbound®.
- State clearly the product is a **supplement, not a drug, and not a GLP-1 replacement.**

---

## 16. Hierarchy of Trust Signals (show in this order on every page)

1. **"Gastroenterologist-Recommended Formula"** (authority)
2. **4.9/5 "Excellent"** (social proof)
3. **"90-Day Money Back Guarantee"** (risk reversal)
4. **"Free US Shipping Over $45"** (friction removal)
5. **"Not Available on Amazon or in Stores"** (exclusivity)
6. **Payment icons row** (transaction trust)

---

## 17. Page Inventory (from site crawl)

| URL | Role |
|---|---|
| `/` | Homepage (product-forward) |
| `/products/motilli-digestive-health-gummies` | Primary PDP |
| `/products/motilli-digestive-health-gummies-celery-juicer` | Celery-juicer avatar variant |
| `/products/motilli-digestive-health-gummies-2` | Alt PDP test |
| `/pages/motilli-pdp` | Custom PDP page |
| `/pages/motilli-advertorial` + `/motilli-advertorial-v2` | Advertorial bridge pages |
| `/pages/motilli-listicle` + `/adv-listicle-v1` | Listicle bridge pages |
| `/pages/motilli-glp1-digestive-support`, `/motilli-glp1` | GLP-1 landing pages |
| `/pages/motilli-diarrhea` | Symptom-specific landing |
| `/pages/adv-wrong-organ` | "Wrong Organ" advertorial (flagship angle) |
| `/pages/celery-quit`, `celery-fiber`, `celery-routine`, `celery-juice-method` | Celery-angle advertorial set |
| `/pages/contact`, `/track-your-order`, `/data-sharing-opt-out` | Service pages |

---

## 18. Quick Reference: Design Tokens (copy-paste ready)

```css
:root {
  /* Brand */
  --motilli-green: #94C218;
  --motilli-green-hover: #9ACD32;
  --motilli-green-deep: #7DA614;
  --motilli-green-leaf: #4CAF50;
  --motilli-pink: #EF4A65;
  --motilli-pink-light: #FFEAEE;

  /* Neutrals */
  --ink: #000000;
  --charcoal: #2A2A2A;
  --mid-gray: #5F6264;
  --mute-gray: #555555;
  --line: #E5E5E5;
  --canvas: #F5F5F5;
  --white: #FFFFFF;

  /* Bundle surfaces */
  --bundle-bg: rgba(239, 250, 209, 1);
  --bundle-selected: #FFFFFF;
  --bundle-border: rgba(148, 195, 14, 0.3);
  --bundle-border-selected: #94C218;

  /* Type */
  --font-body: 'Inter', sans-serif;
  --font-heading: 'Inter', sans-serif;
  --tracking-heading: -0.9px;
  --tracking-body: -0.3px;

  /* Radius */
  --radius-pill: 25px;
  --radius-card: 16px;
  --radius-thumb: 8px;
  --radius-image: 6px;

  /* Button */
  --btn-bg: #7DA614;
  --btn-bg-hover: #94C218;
  --btn-text: #FFFFFF;
  --btn-size: 13px;
  --btn-transform: uppercase;
}
```

---

## 19. Brandkit Asset Inventory (this folder)

```
/brandkit
├── Motilli_Brandkit.md               ← this file
├── assets/
│   ├── motilli_logo_primary.png      (header logo, dark/green on transparent)
│   ├── motilli_logo_white.png        (reverse/dark-background logo)
│   └── product_hero.png              (canonical bottle hero)
└── scraped/                          (raw Firecrawl JSON for the 7 most important pages)
    ├── homepage.json
    ├── pdp-main.json
    ├── pdp-page.json
    ├── advertorial.json
    ├── listicle.json
    ├── glp1-support.json
    └── contact.json
```

---

*Generated from live site crawl of getmotilli.com (Firecrawl API) — 2026-04-21. Update this kit any time the live theme changes; CSS tokens and tagline copy will drift.*
