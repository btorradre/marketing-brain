# Claude Code Prompt — Motilli Website CRO Fixes

Copy everything below the line and paste it into Claude Code as a single prompt. It assumes you're working in the Shopify theme files for trymotilli.co.

---

## THE PROMPT

```
I need you to make the following CRO changes to my Shopify store (trymotilli.co). The store runs on a Shopify theme. Work through the theme's Liquid templates, sections, and settings files to implement each fix. If a fix requires custom CSS or JavaScript, add it cleanly within the existing theme architecture. Do not install apps — all changes should be code-level.

Here are the changes, in priority order:

---

### 1. FIX THE PRODUCT TITLE

The product title currently reads "Motilli Digestive Health Gummies – Motilli v2". Remove "– Motilli v2" from the product title. This appears to be an internal SKU label that leaked into the storefront. Check both the product listing in Shopify admin AND the theme template to make sure it's not being appended by the theme.

---

### 2. ADD A BENEFIT-DRIVEN SUBHEADLINE ABOVE THE FOLD

Directly below the product title on the product page, add a subheadline that reads:

"The Celery Juice Gummy That Stops GLP-1 Bloating, Sulfur Burps & Constipation — In Days, Not Weeks."

Style it as a secondary heading — smaller than the product title, dark green (#2D4A2D) color, normal weight (not bold). Add 8px of margin between the product title and this subheadline. This should appear on both desktop and mobile, above the price.

---

### 3. ADD A "DESIGNED FOR GLP-1 USERS" BADGE

Above the product title, add a small badge/pill that reads "Designed for Ozempic®, Wegovy®, Mounjaro® & Zepbound® Users". Style it as a rounded pill shape — light green (#E8F5E0) background, dark green (#2D4A2D) text, 12px font size, 4px 12px padding, border-radius 20px. This creates instant ad-to-page congruence for visitors coming from Facebook ads about GLP-1 side effects.

---

### 4. UNCOLLAPSE THE KEY CONTENT SECTIONS

The product page currently hides the most persuasive content behind collapsible accordions. Change the following sections from collapsed accordions to always-visible, full-width sections:

- "How Does It Work?" — Make this always visible. Display the four ingredient mechanisms (celery juice extract as natural prokinetic, chlorophyll neutralizes hydrogen sulfide gas, prebiotic fiber rebalances gut bacteria, vitamins replenish depleted nutrients) as a 2x2 grid with icons on desktop, stacking to single column on mobile.

- "What Motilli Helps With" — Make this always visible. Display the 7 symptoms (Constipation & cement stomach, Sulphur burps & gas, Nausea & indigestion, Fatigue & low energy, Brain fog, Bloating) as a visual list with small icons next to each. Add a header: "What Motilli Helps With" in a styled section heading.

- "When Will I See Results?" — Make this always visible. Display the 4-phase timeline (Days 1-3: Bloating relief, Days 3-5: Sulphur reduction, Weeks 2-3: Energy stabilization, Week 4+: Full benefits) as a horizontal timeline on desktop and vertical timeline on mobile, with milestone dots/circles and connecting lines.

Keep these as accordion/collapsible:
- "Who Can Use It?"
- "How Long Until I Get It?"

---

### 5. ADD A TESTIMONIAL CAROUSEL SECTION

Below the product details and above the uncollapsed mechanism sections, add a testimonial carousel. Create a new section that displays customer testimonials in a horizontally scrollable carousel format.

Include these testimonials (add them as section settings so they can be edited from the Shopify theme customizer):

Testimonial 1:
- Quote: "I've been on Ozempic for 3 months and the constipation was unbearable. After one week of Motilli, I finally feel normal again. The sulfur burps are gone too."
- Name: "Margaret P."
- Badge: "Verified Buyer"
- Rating: 5 stars

Testimonial 2:
- Quote: "The only gummy that actually gave me my mornings back. After just a week, the bloating was gone. I actually feel lighter — not just in my stomach, but my whole body."
- Name: "Sarah K."
- Age: "42"
- Rating: 5 stars

Testimonial 3:
- Quote: "I was skeptical about another supplement, but this actually works. The celery juice taste is great and I noticed less bloating within 3 days."
- Name: "Jennifer L."
- Badge: "Verified Buyer"
- Rating: 5 stars

Testimonial 4:
- Quote: "My doctor put me on Mounjaro and the GI side effects were brutal. Motilli was the only thing that helped. I tell everyone about it now."
- Name: "Diana R."
- Age: "38"
- Rating: 5 stars

Testimonial 5:
- Quote: "Finally something that actually addresses the side effects of these weight loss meds. Two gummies a day and I feel like a different person."
- Name: "Alicia M."
- Badge: "Verified Buyer"
- Rating: 5 stars

Display format: Each testimonial card shows 5 gold stars at top, the quote in italic, and the name/badge below. Cards should be ~300px wide on desktop, full-width on mobile. Auto-scroll with manual swipe/arrow navigation. Add an aggregate line above the carousel: "★★★★★ Rated 4.9/5 | Trusted by 30,000+ Happy Customers" in centered text.

---

### 6. REFRAME THE SUBSCRIPTION OPTION

Find where the subscription option is displayed (likely managed by Recharge or a subscription app). If the subscription text is editable in the theme, change:

FROM: "$24.39/month with subscription"
TO: "Subscribe & Save 20% — Cancel Anytime, No Commitment"

If this text comes from an app and can't be changed in the theme, add a small helper line below the subscription radio button that reads: "Cancel anytime. No commitment. No questions asked." Style it as 12px text, muted green color.

---

### 7. ENABLE THE STICKY ADD-TO-CART BAR

The theme appears to have a sticky add-to-cart feature that is currently disabled. Find the sticky ATC setting in the theme configuration and enable it. If the theme doesn't have one built-in, add a sticky bottom bar for mobile that appears when the user scrolls past the main Add to Cart button. The sticky bar should contain:

- Product name (truncated if needed)
- Current selected price
- "Add to Cart" button (same green as the main CTA)

The bar should be fixed to the bottom of the viewport on mobile, with a subtle top shadow, white background, and ~60px height. It should only appear after the user has scrolled past the main product form.

---

### 8. ADD A SHIPPING THRESHOLD NUDGE

Near the Add to Cart button (or in the cart drawer), add a dynamic line that calculates distance to free shipping:

- If cart total < $45: Show "Add $X.XX more for FREE shipping!" in green text
- If cart total >= $45: Show "You've unlocked FREE shipping! ✓" in green text

This encourages the single-bottle buyer ($29.99) to add another item or upgrade to a bundle.

---

### 9. ADD A RESULTS TIMELINE SECTION (VISUAL)

Create a dedicated section (separate from the uncollapsed accordion content) that visualizes the results timeline as an engaging visual component. Header: "What to Expect"

Timeline:
- Day 1-3: "Bloating starts to ease" — icon: stomach with down arrow
- Day 3-5: "Sulfur burps fade" — icon: speech bubble with X
- Week 2-3: "Energy levels stabilize" — icon: battery charging
- Week 4+: "Full digestive balance restored" — icon: sparkle/star

On desktop: horizontal timeline with dots connected by a green line, content below each dot.
On mobile: vertical timeline with dots on the left, content to the right.

Place this section AFTER the testimonials and BEFORE the FAQ accordions.

---

### 10. ADD AN EMAIL CAPTURE POPUP

Add a simple popup that triggers on exit-intent (desktop) or after 15 seconds on page (mobile). Content:

- Headline: "Wait — Get 15% Off Your First Order"
- Subheadline: "Join 30,000+ customers who finally found relief from GLP-1 side effects."
- Email input field
- Button: "Claim My 15% Off" (green button)
- Dismiss link: "No thanks, I'll pay full price"

If you can integrate with Klaviyo (check if the Klaviyo script is already loaded on the site), submit the email to a Klaviyo list. If Klaviyo isn't available, store the emails in a simple format that can be exported. Use localStorage to ensure the popup only shows once per visitor session.

---

### IMPORTANT NOTES:

- Make all changes within the Shopify theme architecture (Liquid, CSS, JS). Do not install third-party apps.
- Ensure all changes are mobile-responsive. Test at 375px (iPhone) and 768px (tablet) widths.
- Preserve all existing functionality — subscription options, bundle selectors, cart behavior.
- Use the existing theme's color palette: primary green (#94c218 or similar), dark green for text, cream/white backgrounds.
- Add comments in the code (<!-- CRO FIX: [description] -->) so changes can be easily identified and reverted if needed.
- If any change requires modifying a section schema to allow theme customizer editing, do so — this makes it easy to update content without code changes later.
```
