# Google Ads Creative & Copywriting

## RSA (Responsive Search Ads)

### Character Limits
- Headlines: 30 characters each (max 15 headlines)
- Descriptions: 90 characters each (max 4 descriptions)
- Display URL paths: 15 characters each (2 fields)

### Best Practices
- Provide all 15 headlines and 4 descriptions
- Each headline should stand alone and make sense in any position
- Mix types: benefit-driven, feature-driven, CTA-driven, social proof, urgency
- Include primary keyword in 2-3 headlines (not all)
- Descriptions should expand on headlines, not repeat them
- Include CTA in at least one description

### Headline Formulas
- **Benefit**: "Get [Benefit] in [Timeframe]", "Save [Amount] on [Product]"
- **Question**: "Looking for [Solution]?", "Tired of [Pain Point]?"
- **Urgency**: "Limited Time: [Offer]", "Sale Ends [Date]"
- **Social Proof**: "Trusted by [X]+ Customers", "#1 Rated [Category]"
- **Feature**: "Free Shipping", "No Contract Required"
- **CTA**: "Shop Now", "Get Your Free Quote", "Start Free Trial"
- **Price/Value**: "Starting at $[X]", "Best Price Guaranteed"

### Description Templates
- "[Offer/Benefit]. [Supporting detail]. [CTA] Today!"
- "Shop our [Product Line] — [Key Feature]. [Guarantee]. Order Now."
- "[Pain Point]? Our [Product] [Solves it]. [Social Proof]. Get Started."

---

## Dynamic Features

### Dynamic Keyword Insertion (DKI)
- Syntax: `{KeyWord:Default Text}`
- Inserts triggering keyword into headline/description
- Use in 1-2 headlines max, not all
- Only in tightly themed ad groups where all keywords make grammatical sense
- Don't use with competitor keywords (trademark issues) or misspellings

### Ad Customizers
- **Countdown**: `{COUNTDOWN(yyyy/MM/dd HH:mm:ss)}` → "Sale Ends in 3 days"
- **IF Functions**: `{=IF(device=mobile, Call Now):Shop Online}`
- **Location**: `{LOCATION(City):Your Area}` → "Best Pizza in Chicago"
- **Data Feeds**: `{=FeedName.Attribute}` for massive customization at scale

### Pinning
- Forces headline/description to specific position
- Only pin for: brand consistency, legal disclaimers, critical CTAs
- Pin 2-3 variants to same position for flexibility
- Excessive pinning kills Ad Strength and testing potential

### Ad Strength (Poor → Excellent)
- Directional indicator, not performance metric
- Driven by: number of assets, uniqueness, keyword inclusion, diversity, pinning
- Aim for "Good" or "Excellent" but don't obsess — some "Good" ads outperform "Excellent"

---

## Ad Assets (formerly Extensions)

### Essential (Always Use)
| Asset | Specs | Purpose |
|---|---|---|
| **Sitelinks** | 25 char link text, 35 char descriptions | Additional links to key pages |
| **Callouts** | 25 char each, non-clickable | Highlight benefits: "Free Shipping", "24/7 Support" |
| **Business Name/Logo** | 25 char name, 1200x1200 logo | Brand recognition |

### High Priority
| Asset | Specs | Purpose |
|---|---|---|
| **Image** | 1200x1200 square, 1200x628 landscape | Visual alongside text ads |
| **Structured Snippets** | Header + 3+ values (25 char each) | Showcase types, brands, services |
| **Call** | Phone number, schedule-able | Click-to-call on mobile |
| **Promotion** | 20 char item, discount type, dates | Sales/offers with price tag icon |
| **Price** | Header + price + description per item | Show pricing directly |

### Situational
| Asset | When |
|---|---|
| **Lead Form** | Lead gen (keep forms short) |
| **Location** | Physical store businesses |

---

## Shopping Feed Optimization

### Product Titles (150 char, ~70 visible)
- Formula: Brand + Product Type + Key Attributes (color, size, material)
- Front-load important info
- Include primary search keyword
- No ALL CAPS, no promotional text, no price

### Product Images
- Min 800x800, product on white/transparent background
- Product fills 75-90% of frame
- No watermarks, logos, or promotional text
- Multiple angles via additional_image_link

### Custom Labels (5 fields: custom_label_0-4)
- By margin: high/medium/low
- By performance: best-seller/new/clearance
- By season: spring/summer/fall/winter
- By price range: $0-25, $25-50, etc.
- Use for separate campaigns with different ROAS targets

---

## Writing by Funnel Stage

### Top of Funnel (Awareness)
- Focus on problem/pain point, not product
- Question headlines, educational angle
- CTAs: "Learn More", "Discover How"

### Mid-Funnel (Consideration)
- Compare solutions, highlight differentiators
- Social proof important
- CTAs: "Compare Plans", "Get a Demo"

### Bottom of Funnel (Conversion)
- Direct, action-oriented
- Strong offers, discounts, urgency
- CTAs: "Buy Now", "Sign Up", "Get Your Quote"

---

## Policy Compliance

### Healthcare/Supplement Rules
- CANNOT claim: cure, treat, prevent diseases
- CAN say: "Supports healthy [function]", "May help with [general wellness]"
- FDA disclaimer required
- May need LegitScript certification
- Weight loss claims heavily scrutinized

### Common Disapproval Reasons
1. Destination mismatch (display URL ≠ final URL domain)
2. Misleading content / unsubstantiated claims
3. Trademark violations in ad copy
4. Healthcare claims without certification
5. Punctuation/symbol abuse
6. Phone numbers in ad text (use call extension)
7. Broken landing page (404)

### Appeal Process
1. Understand the specific policy cited
2. Fix if legitimate, then resubmit
3. Appeal via Policy Manager with specific compliance explanation
4. Escalate to Google Ads support if denied
5. Timeline: 1-5 business days typical
