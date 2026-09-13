# Motilli Product Image Prompts — v3

8 images. Each one solves a specific conversion problem identified in the CRO audit. The design system is derived from Alevia's image architecture but adapted for Motilli's product (glass jar of heart-shaped gummies, not a capsule bottle), Motilli's brand color (#95C537), and Motilli's GLP-1 positioning.

## Product Reference (applies to ALL images that include the jar)

**JAR SHAPE & PROPORTIONS:** Standard wide-mouth supplement jar. The body is taller than it is wide — width-to-height ratio of the body (excluding lid) is approximately 1:1.4. The jar has a cylindrical body that narrows slightly at the neck/mouth area. Visible screw threads at the neck where the lid attaches. The mouth opening is slightly narrower than the body diameter. This is NOT a mason jar, NOT a tall skinny pill bottle — it's a medium-width, medium-height glass supplement jar. Think of a peanut butter jar shape but slightly taller and narrower.

**GLASS:** Clear glass — you can see the dark green gummies packed inside above the label line. However, the glass is NOT invisibly clear. It has a subtle warm/olive cast because the dark gummies show through it. The glass looks like real glass — you can see its thickness, slight reflections, and the way it slightly distorts what's behind it. Do NOT make the glass look frosted, heavily tinted, or opaque.

**LID:** White plastic screw-top lid, CLOSED and ON the jar. Flat top, smooth matte finish. The lid height is approximately 18-20% of the total jar height (including lid). Normal proportioned — not ultra-low-profile and not tall. The lid must be on and closed in every image unless explicitly stated otherwise.

**LABEL:** Bright, saturated lime-chartreuse green (#94C218 — a yellow-leaning vibrant green). The label wraps around the jar and covers approximately the lower 55-60% of the jar body. Above the label, you see bare glass with dark gummies visible inside. The label is the brightest, most saturated element on the entire jar.

**GUMMIES INSIDE:** Dark green, almost olive-black, heart-shaped gummies densely packed inside the jar. Clearly visible through the glass above the label line.

**LABEL TEXT (top to bottom):** 'motilli' in large bold lowercase white sans-serif → 'CELERY JUICE FIBER GUMMIES' in white uppercase → 'supports natural detoxification & a daily green boost' in small white text → 'Clinically Tested Actives' in a small yellow-green pill badge → 'VERIFIED CLEAN' with ingredient names → '5g FIBER' circle badge on right side → Bottom: '60 VEGAN GUMMIES DIETARY SUPPLEMENT' left, green heart + 'GREEN APPLE' right.

Any image referencing "Same Motilli jar" or "Motilli jar" must use these exact physical characteristics.

---

## Design System Notes

**Why Alevia's images work at the design level:**

Alevia uses a three-tier typography hierarchy across every image: (1) an oversized anchor number or word that creates visual weight and stops the scroll, (2) a medium-weight descriptor that contextualizes the anchor, and (3) body-level supporting text that delivers the detail. This hierarchy means you can read every image at three speeds — glance, skim, and read — and each speed delivers a complete message. They also repeat their product bottle in 5 of 7 images, always at the same angle and scale, which creates visual consistency across the carousel. The bottle is never the hero — it's always the supporting character to a text-driven message.

**How Motilli adapts this:**

Motilli's product is a clear glass jar with a bright green label and visible dark green heart-shaped gummies inside. This is actually a visual advantage over Alevia's plain white capsule bottle — the gummies are more interesting, more textured, more scroll-stopping. Motilli's brand green (#95C537) is lighter than Alevia's dark forest green, which means white text on Motilli green has lower contrast. To compensate: all text-on-green images use bold or semi-bold weights minimum, with larger type sizes than Alevia uses. No thin or light weight text on #95C537 backgrounds.

**Carousel sequencing rationale:**

1. Hero (what is this product?) → 2. Social proof (do people like it?) → 3. What it does (why would I take it?) → 4. Timeline (when will it work?) → 5. Comparison (why this over alternatives?) → 6. Guarantee (what's my risk?) → 7. Ingredients (what's in it?) → 8. Supplement facts (proof of the claims)

This sequence mirrors the buyer's decision process: identify → trust → understand → compare → de-risk → verify.

---

## Image 1 — Hero: Product + Benefit Cards

**CRO problem this solves:** The original Motilli hero used feature callouts ("5g Prebiotic Fiber Per Serving," "Daily Green Boost") that told shoppers what's in the product, not what happens to their body. Visitors bouncing from the first image never learned what the product DOES.

**What Alevia does right here:** Their hero puts the product at ~60% frame with three stacked benefit cards on the right. Each card has ONE benefit, large enough to read at thumbnail size. Two trust badges float on the product side (TikTok Viral, Made in USA) creating instant credibility without taking space from the benefit messaging. The product bottle is shot at a 3/4 angle with the label clearly readable — it's a product shot AND a brand shot simultaneously.

```json
{
  "image_number": 1,
  "image_name": "Hero — Product + Outcome Benefit Cards",
  "cro_purpose": "First impression. Must answer 'what does this do for my body?' within 2 seconds. Outcome-driven callouts replace the original feature-driven ones.",
  "aspect_ratio": "1:1",
  "layout": {
    "composition": "Asymmetric split. Product occupies left 58% of frame. Three stacked rectangular cards occupy right 38% with 4% margin between product zone and cards. Cards have ~10px vertical gaps between them.",
    "background": "Clean warm white (#FAFAF5) for the left/product zone. The three cards on the right provide their own solid color backgrounds.",
    "product_shot": {
      "description": "Motilli jar exactly as described in the Product Reference section above. Standard wide-mouth supplement jar — body taller than wide (1:1.4 ratio), visible screw threads at the neck, clear glass with subtle warm/olive cast from dark gummies inside, bright lime-chartreuse (#94C218) label covering lower 55-60% of jar body, flat white screw-top lid. Dark green heart-shaped gummies densely packed inside, visible above the label line.",
      "loose_gummies": "3-5 loose dark green heart-shaped gummies scattered at the base of the jar on the white surface.",
      "angle": "Straight-on front view — the jar faces the camera directly. The label is perfectly centered and fully readable. No rotation, no 3/4 turn. Think standard e-commerce product photo facing the viewer head-on.",
      "scale": "Jar fills ~75% of the product zone height. It should feel large, prominent, but not crowded.",
      "lighting": "Soft studio light from upper-left, creating a gentle shadow behind and to the right of the jar. No harsh reflections on the glass. Warm, slightly golden light temperature."
    },
    "trust_badges": "NONE. No badges on this image. The product jar and benefit cards are the only elements.",
    "benefit_cards": {
      "what": "Three solid-color rounded rectangles stacked vertically in the right 38% of the frame. Each card occupies roughly 31% of the frame height with 10px gaps between them. Rounded corners (~12px radius).",
      "card_background": "Motilli green (#95C537). Solid fill, fully opaque, no gradient.",
      "card_1": {
        "icon": "White thin-line icon: a simplified torso/waist silhouette with a small downward arrow below the stomach area. ~28px height. Centered horizontally in the card, positioned in the upper 35% of the card.",
        "headline": "Stops\nGLP-1 Bloating†",
        "text_style": "White (#FFFFFF), bold serif, 20pt, centered. Line break between 'Flattens' and 'Bloating Fast†'. The dagger is a superscript 10pt."
      },
      "card_2": {
        "icon": "White thin-line icon: a smooth curved arrow forming a gentle loop/cycle shape, indicating regularity. ~28px height. Same positioning as card 1.",
        "headline": "Gets You\nRegular Again†",
        "text_style": "Same as card 1"
      },
      "card_3": {
        "icon": "White thin-line icon: a leaf inside a shield outline. ~28px height. Same positioning.",
        "headline": "Celery Juice\nDetox in a Gummy",
        "text_style": "Same as card 1, no dagger on this one"
      }
    }
  },
  "color_palette": {
    "background": "#FAFAF5",
    "card_fill": "#95C537",
    "card_text": "#FFFFFF",
    "badge_fill": "#95C537",
    "badge_text": "#FFFFFF",
    "label_green": "#94C218"
  }
}
```

---

## Image 2 — Customer Reviews Collage

**CRO problem this solves:** The original Motilli images claimed "Trusted by 30,000+ Happy Customers" but the website showed only one testimonial. This image builds the visual DENSITY of social proof that Alevia achieves with their reviews collage — scattered cards, profile photos, star ratings — so the claim feels substantiated before the visitor even reaches the product page reviews section.

**What Alevia does right here:** Their reviews image creates visual ABUNDANCE — 8+ review cards scattered at angles, partially overlapping, extending past frame edges. This creates the impression of overwhelming positive feedback, not curated cherry-picking. The profile photos clustered in the center humanize the reviews. The "Hear from customers who trust Alevia" headline is the only large text, and it's positioned in the visual quiet zone between the scattered cards above and below.

```json
{
  "image_number": 2,
  "image_name": "Customer Reviews Collage — Social Proof Density",
  "cro_purpose": "Substantiates the 30,000+ customer claim. Creates visual abundance of social proof. The scattered card layout signals 'there are so many reviews we can't fit them all' — which is the opposite of the current page's single testimonial.",
  "aspect_ratio": "1:1",
  "layout": {
    "composition": "A central headline area (~30% of frame height, centered vertically) surrounded by scattered review cards filling the rest of the frame. Cards overlap, extend beyond frame edges, and are rotated at slight angles.",
    "background": "Light warm cream (#F5F0E8).",
    "review_cards": {
      "quantity": "10-12 white rectangular cards. Cards are ~150px wide × ~100px tall with 8px rounded corners and a subtle drop shadow (2px Y offset, 8px blur, 10% black opacity). Each card is rotated between -12° and +12° randomly. Cards in the top and bottom thirds overlap each other and extend past the frame edges so they appear cropped. Only 4-5 cards in the middle zone are fully readable — the rest are partially hidden, reinforcing visual abundance.",
      "card_content_per_card": "Each card contains: (1) a star rating line — five small gold (#D4A017) stars + a rating number like '4.7' or '5.0' in small text, (2) 2-3 lines of review text in dark text, 10-11pt, (3) a reviewer name + '· Verified Customer' in small muted green text at the bottom.",
      "review_texts_for_visible_cards": {
        "card_a": "★★★★★ 5.0\n'The bloating is finally gone. I feel lighter than I have in months.'\n— Sarah K. · Verified Customer",
        "card_b": "★★★★★ 5.0\n'I was skeptical but this actually works. Sulfur burps gone in 3 days.'\n— Margaret P. · Verified Customer",
        "card_c": "★★★★☆ 4.7\n'Best supplement I've tried since starting Ozempic. Game changer.'\n— Jennifer L. · Verified Customer",
        "card_d": "★★★★★ 5.0\n'My digestion has never been better. Taking these every morning.'\n— Diana R. · Verified Customer",
        "card_e": "★★★★★ 5.0\n'Finally something that addresses the GI side effects. Two gummies and done.'\n— Alicia M. · Verified Customer"
      }
    },
    "profile_photos": {
      "what": "4 circular profile photos (~50px diameter each) in a horizontal row at center of frame, overlapping each other by ~15px. Each has a 3px white border. Photos are real-looking women ages 30-50 — natural skin, natural lighting, casual selfie or portrait quality. Diverse appearances. Not models.",
      "position": "Centered horizontally, positioned in the upper portion of the central headline zone."
    },
    "headline_zone": {
      "star_rating": "★★★★★ in gold (#D4A017), 20pt, centered, directly below the profile photos",
      "rating_text": "Rated 4.9 / 5.0 | 'Excellent'",
      "rating_text_style": "Dark green (#2D4A2D), bold, 14pt, centered",
      "headline": "Hear from customers\nwho trust Motilli",
      "headline_style": "Dark green (#2D4A2D), bold serif, 30pt, centered, two lines"
    }
  },
  "color_palette": {
    "background": "#F5F0E8",
    "cards": "#FFFFFF",
    "card_shadow": "rgba(0,0,0,0.10)",
    "star_gold": "#D4A017",
    "headline_text": "#2D4A2D",
    "review_text": "#2D4A2D",
    "verified_badge_text": "#95C537"
  },
  "design_note": "The headline text uses dark green (#2D4A2D) rather than Motilli green (#95C537) for readability on the cream background. Motilli green works great as a fill color but is too light for body text on light backgrounds."
}
```

---

## Image 3 — Benefits Grid (2x2)

**CRO problem this solves:** The original Motilli images had benefit callouts scattered across multiple images with inconsistent language — some were features ("5g Prebiotic Fiber"), some were incomplete ("Stops Bloating & Supports"), some were meaningless ("Daily Green Boost"). This image consolidates the four core outcomes into a single, scannable grid where each benefit answers "what happens to MY body?"

**What Alevia does right here:** Their 2x2 grid is the simplest image in their carousel — and that's the point. After the visually complex hero and the dense reviews collage, the eye needs a rest. Four icons, four headlines, dark background. It reads in under 2 seconds. Each icon is visually distinct (lightning bolt vs. brain vs. molecules vs. person silhouette) so the eye can differentiate the four benefits without reading the text.

```json
{
  "image_number": 3,
  "image_name": "Benefits Grid — 4 Core Outcomes",
  "cro_purpose": "Consolidates the four specific outcomes Motilli delivers for GLP-1 users into a single scannable image. Replaces the vague 'Natural Detoxification / Daily Green Boost' language with specific GLP-1 symptom relief.",
  "aspect_ratio": "1:1",
  "layout": {
    "composition": "Full-bleed Motilli green background. Frame divided into four equal quadrants by very subtle white lines (1px, 15% opacity — barely visible, more felt than seen). Each quadrant has a white icon in its upper 40% and white text in its lower 60%.",
    "background": "Solid Motilli green (#95C537). Flat, no gradient, no texture."
  },
  "quadrants": {
    "top_left": {
      "icon": "White outline icon: a stomach/gut silhouette with a small downward arrow, indicating deflating/flattening. ~40px height.",
      "headline": "Stops GLP-1\nBloating†",
      "subtext": "Most feel it in 48 hours",
      "headline_style": "White, bold serif, 22pt, centered",
      "subtext_style": "White, regular weight, 12pt, centered, 70% opacity"
    },
    "top_right": {
      "icon": "White outline icon: a speech bubble with an X through it, indicating elimination of sulfur burps. ~40px height.",
      "headline": "Stops Sulfur\nBurps†",
      "subtext": "Chlorophyll neutralizes gas",
      "headline_style": "Same",
      "subtext_style": "Same"
    },
    "bottom_left": {
      "icon": "White outline icon: a smooth curved arrow forming a gentle loop/cycle shape, indicating regularity and bowel movement. ~40px height.",
      "headline": "Ends\nConstipation†",
      "subtext": "Gentle daily regularity",
      "headline_style": "Same",
      "subtext_style": "Same"
    },
    "bottom_right": {
      "icon": "White outline icon: a gut/intestine with small sparkle marks, indicating healthy digestion. ~40px height.",
      "headline": "Supports\nDigestion†",
      "subtext": "Prebiotic fiber rebalances your gut",
      "headline_style": "Same",
      "subtext_style": "Same"
    }
  },
  "color_palette": {
    "background": "#95C537",
    "icons_and_headlines": "#FFFFFF",
    "subtext": "rgba(255,255,255,0.70)",
    "grid_lines": "rgba(255,255,255,0.15)"
  },
  "design_note": "Each quadrant maps to a specific GLP-1 side effect: bloating, sulfur burps, constipation, and digestive disruption. These are the four symptoms the Motilli website lists as primary. The subtexts add a second layer of specificity ('Most feel it in 48 hours') that the original Motilli images completely lacked. Headlines are bold enough to read at thumbnail size. Subtext is for the full-size viewer."
}
```

---

## Image 4 — Results Timeline

**CRO problem this solves:** The original Motilli product page hid the results timeline inside a collapsed accordion that most mobile users never opened. This was the single most persuasive piece of content on the site (specific day-by-day expectations) and it was invisible. This image makes it permanently visible in the carousel — every shopper sees it regardless of whether they read the product page.

**What Alevia does right here:** Their timeline uses a clear vertical progression (Week 1-2 → Week 3-4 → Week 5-8 → Week 9-12+) with the time range in a smaller accent color above each bold white milestone name. The product bottle on the right provides brand reinforcement without competing with the timeline content. The milestones each have a checkmark icon creating a visual "completion" cue.

```json
{
  "image_number": 4,
  "image_name": "Results Timeline — When You'll Feel It",
  "cro_purpose": "Surfaces the results timeline that was hidden in a collapsed accordion. Sets specific expectations (Days 1-3, Days 3-5, Weeks 2-3, Week 4+) that reduce purchase anxiety and give the shopper a mental model for how the product works over time.",
  "aspect_ratio": "1:1",
  "layout": {
    "composition": "Motilli green background. Left 55% is the timeline content zone. Right 45% is the product jar, large, partially cropped by the right edge of the frame.",
    "background": "Solid Motilli green (#95C537)."
  },
  "timeline": {
    "structure": "Four milestone entries stacked vertically with equal spacing. Each entry consists of three elements: (1) time range label in small text, (2) a white circle with a checkmark to its left, (3) the milestone headline in large bold white text to the right of the checkmark.",
    "milestone_1": {
      "time_label": "Days 1-3",
      "time_label_style": "White, regular weight, 13pt. Positioned above the headline, left-aligned with the headline text.",
      "checkmark": "White filled circle (~20px diameter) with a Motilli green (#95C537) checkmark stroke inside.",
      "headline": "Bloating Relief*",
      "headline_style": "White, bold serif, 24pt"
    },
    "milestone_2": {
      "time_label": "Days 3-5",
      "headline": "Sulfur Burp Reduction*"
    },
    "milestone_3": {
      "time_label": "Weeks 2-3",
      "headline": "Daily Regularity Restored*"
    },
    "milestone_4": {
      "time_label": "Week 4+",
      "headline": "Full Digestive Balance*"
    },
    "disclaimer": {
      "text": "†These statements have not been evaluated by the FDA.\n*Individual results may vary.",
      "style": "White, 9pt, 60% opacity, centered at very bottom of frame"
    }
  },
  "product_zone": {
    "jar": "Same Motilli jar as Image 1, fully visible — NOT cropped by the frame edge. The entire jar including the full label must be inside the frame. Positioned on the right side, vertically centered. The jar fills ~65% of the right zone height. There should be a small margin (~5%) between the jar and the right edge of the frame so nothing gets cut off.",
    "lighting": "Jar has a subtle bright edge/rim where it meets the green background, giving it dimension against the flat color."
  },
  "color_palette": {
    "background": "#95C537",
    "time_labels": "#FFFFFF",
    "checkmark_circle_fill": "#FFFFFF",
    "checkmark_stroke": "#95C537",
    "headline_text": "#FFFFFF",
    "disclaimer": "rgba(255,255,255,0.60)"
  }
}
```

---

## Image 5 — Comparison Chart: WHY MOTILLI?

**CRO problem this solves:** The original Motilli comparison chart only had spec-based rows (Clinically Tested Actives, Clean Label Certified, etc.) that don't create emotional differentiation. A shopper who doesn't know what "Clean Label Project Certified" means gets nothing from that row. This version leads with an outcome row ("Stops Bloating in 48 Hours") and includes a guarantee row — both create real competitive contrast that matters to the buyer.

**What Alevia does right here:** Their comparison chart uses a clean white background (visual rest after the dark green images), positions their branded bottle against a plain BLACK generic bottle (the black signals "cheap/unknown"), and keeps the claim text centered between the two columns. The checkmarks are green circles, the X marks are dark squares — the shape difference (circle vs square) creates instant visual differentiation beyond just color.

```json
{
  "image_number": 5,
  "image_name": "WHY MOTILLI? — Comparison Chart",
  "cro_purpose": "Creates competitive differentiation by leading with an OUTCOME row and a GUARANTEE row before the spec rows. Also uses a dark/black competitor bottle (not white) to create a stronger visual 'us vs. them' contrast.",
  "aspect_ratio": "1:1",
  "layout": {
    "composition": "White background. 'WHY MOTILLI?' headline at top. Two product images below the headline — Motilli jar upper-left, generic black bottle upper-right. Five comparison rows stacked below the products.",
    "background": "Clean white (#FFFFFF)."
  },
  "header": {
    "headline": "WHY MOTILLI?",
    "style": "Motilli green (#95C537), bold serif, 30pt, centered at top of frame with ~20px top padding"
  },
  "products": {
    "motilli_jar": "Small Motilli jar (same as Image 1), ~18% of frame height. Upper-left area, below headline. Angled slightly.",
    "competitor_bottle": "A plain matte BLACK supplement bottle with a black cap. No label, no text, no branding. Same approximate size as the Motilli jar. Upper-right area, mirroring the Motilli jar's position. The black color signals 'generic/unknown/cheap.'"
  },
  "comparison_rows": {
    "structure": "Five horizontal rows below the two product images. Rows alternate between white and very light gray (#F8F8F8) backgrounds. Each row has: a Motilli green (#95C537) filled circle with white checkmark on the left, centered claim text in the middle, and a dark gray (#4A4A4A) filled square with white X on the right. Rows separated by 1px light gray (#E8E8E8) lines.",
    "row_1": {
      "claim": "Stops Bloating\nin 48 Hours†",
      "claim_style": "Dark (#2D4A2D), bold, 15pt, centered",
      "why_first": "This is the OUTCOME row. It leads the chart because it's the only row that tells the shopper what happens to their body. The original chart had this nowhere."
    },
    "row_2": {
      "claim": "90-Day Money-Back\nGuarantee",
      "why_second": "Risk reversal as a competitive advantage. Most competitors don't offer this."
    },
    "row_3": {
      "claim": "Celery Juice\nExtract"
    },
    "row_4": {
      "claim": "5g Prebiotic Fiber\nPer Serving"
    },
    "row_5": {
      "claim": "Clean Label Project\nCertified"
    }
  },
  "color_palette": {
    "background": "#FFFFFF",
    "headline": "#95C537",
    "checkmark_circle": "#95C537",
    "checkmark_inner": "#FFFFFF",
    "x_square": "#4A4A4A",
    "x_inner": "#FFFFFF",
    "claim_text": "#2D4A2D",
    "row_alt_background": "#F8F8F8",
    "row_divider": "#E8E8E8"
  }
}
```

---

## Image 6 — 90-Day Guarantee + Product

**CRO problem this solves:** The original guarantee image ("Feel Clean Guarantee") used a generic name and didn't include the product. Alevia's "Empty Bottle" framing is viscerally stronger — it tells the shopper they can use the ENTIRE product and still get a refund. The product jar needs to be visible so the shopper mentally connects the guarantee to the physical thing they're buying.

**What Alevia does right here:** Their guarantee image uses a massive "90 Day" as the visual anchor — it's the largest text element on the entire image, creating immediate visual weight. The shield icon above it signals "protection." The guarantee copy below is specific and conversational ("If you're not completely satisfied..."). The product on the right reinforces what the guarantee covers.

```json
{
  "image_number": 6,
  "image_name": "90-Day Empty Bottle Promise + Product",
  "cro_purpose": "Reframes the guarantee from 'Feel Clean Guarantee' to 'The Empty Bottle Promise' — more visceral, more memorable. The 'Use the entire bottle' framing eliminates the 'what if I only use half?' hesitation that weaker guarantees leave open.",
  "aspect_ratio": "1:1",
  "layout": {
    "composition": "Motilli green background. Copy zone on left 55%. Product jar on right 45%, large, partially cropped at right edge.",
    "background": "Solid Motilli green (#95C537)."
  },
  "copy_zone": {
    "shield_icon": {
      "what": "A white (#FFFFFF) shield outline icon with a heart inside. ~55px height. Positioned at top-left of copy zone.",
      "style": "White outline, 2px stroke weight"
    },
    "anchor_text": {
      "text": "90 Day",
      "style": "White, ultra-bold serif, 52pt. This is the LARGEST text element on the image — it's the visual anchor that creates scroll-stopping weight.",
      "position": "Below the shield icon, left-aligned"
    },
    "guarantee_name": {
      "text": "The Empty Bottle\nPromise",
      "style": "White, bold serif, 24pt, left-aligned. Two lines.",
      "position": "Directly below the anchor text, tight spacing"
    },
    "body": {
      "text": "Use the entire bottle. If the bloating,\nburps, and constipation aren't\nnoticeably better within 90 days,\nwe'll refund every penny.",
      "style": "White, regular weight, 14pt, left-aligned, line-height 1.6x",
      "position": "Below guarantee name with ~16px spacing"
    }
  },
  "product_zone": {
    "jar": "Same Motilli jar, fully visible — NOT cropped by the frame edge. The entire jar including the full label must be inside the frame. Vertically centered in the right zone with a small margin (~5%) from the right edge.",
    "lighting": "Subtle rim light on the right edge of the jar."
  },
  "color_palette": {
    "background": "#95C537",
    "all_text_and_icons": "#FFFFFF"
  }
}
```

---

## Image 7 — Ingredients Wheel

**CRO problem this solves:** The original ingredients image used vague descriptors ("Natural Detoxification," "Deep Green Cleanse," "Natural Flavor") that wasted every slot. This version makes each ingredient slot do conversion work — every parenthetical answers "what does this ingredient do for me?" with specific mechanism language tied to the GLP-1 symptoms from the CRO audit.

**What Alevia doesn't have:** Alevia has a single ingredient (amla) so they don't need an ingredients image. Motilli has four active ingredients and a flavor ingredient — the circular wheel format is unique to Motilli and works because it shows the real food sources through photography, which signals "natural" better than any badge can.

```json
{
  "image_number": 7,
  "image_name": "Ingredients Wheel — Mechanism Descriptors",
  "cro_purpose": "Every ingredient slot now does conversion work. Chlorophyll doesn't say 'Deep Green Cleanse' (meaningless) — it says 'Neutralizes Sulfur Gas & Odor' (addresses the #1 embarrassing GLP-1 side effect). Green Apple doesn't say 'Natural Flavor' (wasted slot) — it says 'Tastes Like Candy, Not Medicine' (kills the taste objection).",
  "aspect_ratio": "1:1",
  "layout": {
    "composition": "Warm cream background. Center cluster of heart-shaped gummies. Four circular ingredient photo insets arranged in a clock pattern around the center. Subtle connecting arrows between the circles.",
    "background": "Warm cream (#F5F0E8)."
  },
  "center_cluster": {
    "what": "8-10 dark green heart-shaped gummies arranged in a loose organic cluster at the center of the frame. They cast soft, warm shadows on the cream surface. These are the same gummies visible inside the jar in Image 1.",
    "scale": "The cluster occupies roughly 20% of the frame in both width and height."
  },
  "ingredient_circles": {
    "size": "Each circle is ~22% of frame width. Thin light gray (#E0DCD4) border, 2px. Circles positioned at 12, 3, 6, and 9 o'clock with their edges roughly 10% from the frame edges.",
    "arrows": "Subtle curved gray (#C8C4BC) arrows connecting circles clockwise, passing behind the center gummies. 1px weight.",
    "position_12": {
      "photo": "Close-up of fresh bright green celery stalks, some chopped into small segments, arranged on a clean light surface. Bright, fresh food photography.",
      "name": "Celery Juice Extract",
      "descriptor": "(Restarts Sluggish Digestion)",
      "name_style": "Bold dark green (#2D4A2D) serif, 16pt, centered below circle",
      "descriptor_style": "Italic dark green (#2D4A2D), 13pt, centered below name"
    },
    "position_3": {
      "photo": "A clear glass filled with vibrant bright green chlorophyll liquid, shot from slightly above. Rich, saturated green color.",
      "name": "Chlorophyll",
      "descriptor": "(Neutralizes Sulfur Gas & Odor)"
    },
    "position_6": {
      "photo": "A green apple sliced in half showing white flesh and seeds, with a whole green apple behind it. Fresh, clean food photography.",
      "name": "Green Apple",
      "descriptor": "(Tastes Like Candy, Not Medicine)"
    },
    "position_9": {
      "photo": "A small white ceramic bowl of fine white prebiotic fiber powder, shot from slightly above. Clean, minimal.",
      "name": "Prebiotic Fiber",
      "descriptor": "(Feeds Beneficial Gut Bacteria)"
    }
  },
  "color_palette": {
    "background": "#F5F0E8",
    "text": "#2D4A2D",
    "circle_border": "#E0DCD4",
    "arrows": "#C8C4BC"
  },
  "design_note": "Text on this image uses dark green (#2D4A2D) instead of Motilli green (#95C537) because it sits on a cream background. The dark green provides much better readability than the lighter brand green would."
}
```

---

## Image 8 — Supplement Facts + Dosage

**CRO problem this solves:** The original supplement facts image had DUPLICATE INGREDIENTS listed (Chlorophyll and Sodium Copper Chlorophyllin each appeared twice), typos in the footnotes ('calorins' instead of 'calorie'), and 'Like Inulin' instead of proper formatting. These errors undermined credibility for any shopper who reads labels closely. This version is corrected AND adds the guarantee header and dosage icons from Alevia's format — packing three trust signals (guarantee, facts, dosage) into one image.

**What Alevia does right here:** They put their guarantee header AT THE TOP of the supplement facts image — so even this compliance image starts with a conversion message. The three dosage icons at the bottom ("Get 2 Capsules / Grab your favourite drink / Consume once per day") make usage feel effortless. The dark background makes the white text pop and gives the image a premium, clinical feel.

```json
{
  "image_number": 8,
  "image_name": "Supplement Facts + Dosage + Guarantee Header",
  "cro_purpose": "Three jobs in one image: (1) Corrected supplement facts with zero errors, (2) Simple dosage instructions that make usage feel effortless, (3) Guarantee header reinforcement. Fixes the duplicate ingredient and typo issues from the original.",
  "aspect_ratio": "1:1",
  "layout": {
    "composition": "Motilli green background. Guarantee header text at top. Supplement facts in a white-bordered panel occupying the center ~50% of frame height. Three dosage instruction icons below the panel. FDA disclaimer at very bottom.",
    "background": "Solid Motilli green (#95C537)."
  },
  "guarantee_header": {
    "text": "90-DAY MONEY BACK GUARANTEE",
    "style": "White, bold, all-caps, 18pt, centered, letter-spacing 1.5px. Positioned at the top with ~20px padding."
  },
  "facts_panel": {
    "border": "Thin white (#FFFFFF) border, 1.5px, around the entire panel. Panel fill matches the background green.",
    "header": {
      "text": "SUPPLEMENT FACTS",
      "style": "White, ultra-bold serif, 22pt, all-caps"
    },
    "serving_info": "Serving Size: 2 Vegan Gummies | Serving Per Container: 30",
    "serving_style": "White, regular, 12pt",
    "column_header_bar": {
      "left": "AMOUNT PER SERVING",
      "right": "%DAILY VALUE",
      "style": "White text on a slightly lighter green bar, bold, 10pt, all-caps"
    },
    "rows": [
      {"name": "Celery Juice Extract", "amount": "200mg", "dv": "†"},
      {"name": "Chlorophyll", "amount": "300mg", "dv": "†"},
      {"name": "Prebiotic Fiber Blend (Inulin)", "amount": "300mg", "dv": "†"},
      {"name": "Sodium Copper Chlorophyllin", "amount": "2.5mg", "dv": "†"}
    ],
    "row_style": "White text, 12pt. Name left-aligned, amount+DV right-aligned. Thin white lines (40% opacity) between rows.",
    "footnote": "† Daily Value not established.",
    "other_ingredients": "Other Ingredients: Celery Juice, Chlorophyll, Sodium Copper Chlorophyllin, Inulin (Prebiotic Fiber), Sugar, Pectin, Citric Acid, Natural Green Apple Flavor, Coconut Oil.",
    "other_ingredients_style": "White, 9pt",
    "IMPORTANT": "VERIFY THIS INGREDIENT LIST AGAINST YOUR ACTUAL PRODUCT LABEL BEFORE GENERATING. This is a corrected version of your original — the original had duplicate ingredients and typos."
  },
  "dosage_icons": {
    "layout": "Three icons in a horizontal row below the facts panel, separated by thin white vertical divider lines (1px, 40% opacity). Each icon has a white thin-line illustration above and white text below.",
    "icon_1": {
      "icon": "Two gummy shapes side by side",
      "text": "Take 2\ngummies daily"
    },
    "icon_2": {
      "icon": "A glass with water",
      "text": "With a full\nglass of water"
    },
    "icon_3": {
      "icon": "A clock with a checkmark",
      "text": "Anytime — with\nor without food"
    },
    "text_style": "White, 11pt, centered under each icon"
  },
  "disclaimer": {
    "text": "These statements have not been evaluated by the Food and Drug Administration. This product is not intended to diagnose, treat, cure, or prevent any disease.",
    "style": "White, 8pt, 60% opacity, centered at very bottom"
  },
  "color_palette": {
    "background": "#95C537",
    "all_text": "#FFFFFF",
    "panel_border": "#FFFFFF",
    "row_dividers": "rgba(255,255,255,0.40)",
    "disclaimer": "rgba(255,255,255,0.60)"
  }
}
```
