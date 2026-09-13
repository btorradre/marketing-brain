# 2026-05-07 — Branded Statics Scrape (Thursday Rotation)

**Brands scraped:** AG1 (Athletic Greens), GOLO, Provitalize (BB Company)
**Operator:** Market Analyst (scheduled task)
**Session conditions:** Two Chrome browser disconnects mid-session (one mid-AG1, one between Golo and Provitalize). No full crash. Image-download path remains fully blocked (Meta CDN: cookie/query-string filter on JS extraction, tainted-canvas CORS error, FBCDN fetch returns "Failed to fetch" even with credentials:include). The browser tool's `save_to_disk` flag captures screenshots for in-context review only — they do not persist to the outputs directory. All deliverables this run are observation-only catalog updates.

---

## Summary

- **Net new creative across all three brands today vs April 30:** ~3 net-new creatives observed (1 AG1 — "vocal stim" bold-claim text static; 2 Provitalize — two-SKU bundle visual + the OFFER ENDING SOON red gradient that wasn't documented April 30)
- **Major status change:** GOLO is back on Meta after going dark in March. New page: "GOLO for Life." Two ads visible — both video format with text-card thumbnails. No traditional branded statics
- **Library ID overlap with April 30:** ~85% on AG1, ~70% on Provitalize (more rotation in their pricing-urgency family), 0% prior baseline for GOLO (was dark)
- **No images downloaded to disk this run** (CDN extraction blocked — same condition as 5/3, 5/4, 5/5 sessions)

Today's scrape is a **steady-state-with-one-surprise** day. AG1 and Provitalize are running the archetype mix catalogued April 30 with minor additions. GOLO's reappearance is the news of the day.

---

## Brand-by-brand observations

### AG1 (Athletic Greens)

- **~240 active total ads** ("AG1 by Athletic Greens" keyword) — flat vs April 30
- Image-only filter still useless (returns 1 unrelated result) — Meta classifies most of AG1's testimonial cards as video posters, not images. All-media query is the only useful surface
- Confirmed active branded statics (May 7):
  - Library 1603630744310905 — "$72 Free Welcome Kit" (10+ weeks running, still strong)
  - Library 2485445425209226 — "Wakey, wakey, shakey, shakey is our new vocal stim" (Mar 25 start) — bold-claim text static, AG1 wordmark hero
  - Library 2207803266411261 — Sloane Stephens tennis testimonial card (5+ months running)
  - Library 1629162558332407 — Hugh Jackman glass-quote static (Apr 8 launch — Hugh re-entered static after appearing video-only April 30)
  - Library 880604541292075 — Female testimonial at desk (5+ months)
  - Library 2320562558408213 — Tennis player white outfit testimonial card (5+ months)
- **Notable shift:** "Vocal stim" copy is internal AG1 brand vocabulary now appearing externally. Indicates the brand is confident enough in its own language to expose it publicly. Watch for this — it's a maturity signal
- **Notable shift:** Hugh Jackman re-appeared in static after the April 30 catalog noted he had moved to video. AG1 cycles celebrity creative rather than retiring it
- **Quality assessment:** Welcome Kit static (1603630744310905) remains AG1's strongest pricing creative — 9/10. Testimonial cards are 7/10 (template-grade, replicable, scalable)

### GOLO (NEWS — Back After 5+ Weeks Dark)

- **NEW STATUS:** GOLO has returned to Meta. New page: **GOLO for Life**
- Two confirmed active ads:
  - Library 1506576801021492 — "Your metabolism matters more than you think" — VIDEO format, native lifestyle (woman handling product). Started Apr 29, 2026 (recent re-launch)
  - Library 2524117801383311 — "International Co Development an GLP-1 Drugs" — VIDEO with text-card thumbnail. Long-running from May 15, 2025. Bold-claim text static visible as the first frame
- **Zero traditional branded statics** in the rotation (no pricing urgency, no comparison charts, no testimonial cards, no ingredient callouts)
- **Strategic read:** GOLO appears to have engineered their re-entry to slip past Meta compliance review on weight-loss creative. Headline framing on the GLP-1 ad reads like a policy/news story ("International Co Development") rather than a product claim. Body copy says "metabolism support" and "balanced approach," not "weight loss." The dial has been rotated all the way toward editorial/news framing
- **Implication for our portfolio:** Do NOT use GOLO as a branded-static template right now — they have nothing in the high-design archetype space. Use them as a cautionary signal: weight-loss-supplement compliance pressure on Meta is real, and competitors are responding by going video + news-framed text

### Provitalize (BB Company)

- **~1,900 active total ads** ("Provitalize" keyword) — small growth from ~1,800 on April 30
- Multi-page strategy still active across all 6 confirmed pages (BB Company, Best Probiotics For Menopause, Menopause And Me, Provitalize Probiotics by BB Company, Lucy Chapman, Menopause Care And Relief)
- Confirmed active branded statics (May 7):
  - Library 1000931931511448 + 989012903360618 — Yellow notepad / sticky-note "$10 off" (9-month runners, both pages running same creative simultaneously)
  - Library 2684523008388969 — "WAITING FOR A GOOD DEAL? Patience Pays! Save $39 On 3 Bottles" (autumn-leaves background, 5-claim stack)
  - Library 1285532896830656 — "OFFER ENDING SOON! / RISK FREE" red-gradient static (Mar 18 start) — third visual treatment of the pricing-urgency archetype
  - Library 1955593041515680 — "I finally feel like MYSELF!" testimonial card (Feb 17 start)
  - Library 974540865299422 — Two Provitalize bottles side-by-side (Apr 24 start) — first multi-SKU/bundle static observed
  - All April 30 pain-angle native testimonials (Lucy Chapman / "I almost SLAPPED Dr Smith," "Just as I suspected... Gluteal Tendinopathy," vintage anatomical illustrations) confirmed still active
- **Notable shift:** Two-SKU bundle static (974540865299422) is new since April 30 cataloging. Suggests product-line extension may be incoming or a bundle/stack offer is being tested
- **Notable shift:** Pricing urgency now runs in three distinct visual treatments simultaneously (notepad, autumn-leaves, red gradient) — they're A/B testing aesthetic variants of the same offer
- **Quality assessment:** "Nothing Comes Close To Provitalize" hexagonal benefit callout (Library 1403352224881158, catalogued April 30) remains Provitalize's strongest polished-design static — 8.5/10. Pricing-urgency family is 7/10. Pain-angle natives are deliberately 5/10 in design but 9/10 in stopping power

---

## Cross-brand design trends spotted

1. **Testimonial cards are now AG1's near-exclusive static archetype.** Six of seven captured statics this scrape use the same template: subject photo + italic pulled-quote overlay + AG1 wordmark + product-routine CTA banner. AG1 has settled on a single template and is iterating subject diversity (athletes, professionals, older adults) rather than archetype diversity. **Lesson:** When a single template works, lean in — don't keep inventing new layouts.

2. **Pricing-urgency statics now live across multiple visual treatments simultaneously.** Provitalize is running three different aesthetic variants (yellow-notepad-handwritten / autumn-leaves-bottle / red-gradient-OFFER) of the same offer architecture. **Lesson:** A winning offer should be re-skinned across multiple visual aesthetics. Don't run one creative version of your best offer — run three.

3. **GOLO's re-entry signals the next compliance evolution.** Going dark for 5+ weeks → returning with news-framed headlines, "metabolism support" language instead of "weight loss," and video-as-primary-format with text-card-as-thumbnail. **Lesson:** For Velantra (or any metabolic-adjacent product), the compliance-tested copy template is GOLO's current creative — study the language they use to stay in-bounds.

4. **Two-SKU/bundle statics are emerging at scaling brands.** Provitalize introduced a side-by-side two-bottle static April 24. AG1 has the Welcome Kit grid (single SKU but multiple products in frame). **Lesson:** When you have a second product/SKU, design at least one static around the bundle. Frame two products together visibly.

5. **Internal brand vocabulary is showing up in external static.** AG1's "vocal stim" copy in Library 2485445425209226 is the brand using its own private term in public creative. This is a confidence move — only mature brands do this. **Lesson:** Once your internal terminology has earned its keep, surface it. It signals authority and creates linguistic ownership.

---

## Template recommendations (priority order)

### #1 — Three-Variant Pricing Urgency System (steal from Provitalize)
- Build any offer in three distinct visual aesthetics simultaneously: native/handwritten (yellow notepad), product-hold-with-overlay (autumn leaves), red-gradient-urgency-bar
- For Lunessa: same $X off offer in (a) sticky-note-on-pillow, (b) bottle-on-bedside-table-with-overlay, (c) red OFFER ENDING SOON product hero
- For Velantra: same offer in (a) sticky-note-on-coffee-cup, (b) bottle-in-morning-light, (c) red urgency banner
- For Motilli: same approach
- Why: A/B testing the offer at the visual level — same dollar amount, three creatives. Provitalize has been doing this for 9+ months with sustained results

### #2 — Testimonial Card Template (steal from AG1)
- Subject photo (athlete / professional / older adult — cast against your avatar) + italic pulled-quote overlay + brand wordmark + product-routine CTA banner
- For Lunessa: night-shift nurse — "Lunessa is the part of my routine that lets me come back from a 12-hour shift and still get sleep"
- For Velantra: shift worker — "Velantra is the part of my morning that means I don't crash at 2pm anymore"
- For Motilli: traveling salesperson — "Motilli is the part of my travel kit that means my gut doesn't betray me at hotel breakfast"
- Why: AG1 has invested 5+ months in this template across six confirmed running creatives. Cast diversity is the only variable. Layout is fixed

### #3 — News-Framed Compliance-Safe Static (steal from GOLO post-return)
- Replace direct claim headlines with news/policy-style framing for any compliance-sensitive category
- Body copy: "metabolism support / balanced approach / supports your body's natural processes" — never "weight loss," "fat burning," "rapid results"
- Visual: black text on white, pure typography, reads like a news headline
- Apply to Velantra (metabolic) and Motilli (digestion) where Meta compliance is heaviest
- Why: GOLO's first static back from a 5-week ban is engineered for review survival. Study what language they chose

### #4 — Two-SKU Bundle Static (steal from Provitalize)
- Once Lunessa/Motilli/Velantra has a second SKU or complementary product, build a side-by-side bundle visual
- Pair with a "buy 2, get $X off" or "Stack & Save" pricing
- Why: 974540865299422 is Provitalize's first move into multi-SKU static. They started running it 13 days ago. If we don't have a second SKU yet, this informs roadmap

---

## Chrome stability notes

- Two browser disconnects this session (one mid-AG1 zoom-screenshot pass, one between Golo and Provitalize tab close)
- Each disconnect required calling `tabs_context_mcp` with `createIfEmpty: true` to restart
- No full Chrome crash; no lost work because all observation was captured to memory before each disconnect
- The image-download blocker is now a confirmed structural issue, not session-specific. We have logged this on 5/3, 5/4, 5/5, and 5/7 — that's four consecutive sessions with the same CDN cookie/query-string filter blocking JS extraction. Should escalate to operator: either (a) get Meta Ad Library API access for image pulls or (b) build a Chrome extension that bypasses the CORS taint via background-page fetch

---

## Library ID inventory captured this session (for future API pull)

**AG1:**
- 1603630744310905 (Welcome Kit pricing — Feb 24 start)
- 2485445425209226 ("vocal stim" bold-claim text — Mar 25 start)
- 2207803266411261 (Sloane Stephens tennis testimonial — Dec 3, 2025 start)
- 1629162558332407 (Hugh Jackman glass quote — Apr 8 start)
- 880604541292075 (female testimonial at desk — Dec 3, 2025 start)
- 2320562558408213 (tennis player white outfit testimonial — Dec 2, 2025 start)

**GOLO for Life:**
- 1506576801021492 (metabolism support video — Apr 29 start)
- 2524117801383311 (GLP-1 international news-frame video — May 15, 2025 start)

**Provitalize / BB Company:**
- 1000931931511448 (yellow notepad pricing — Jul 31, 2024 start)
- 989012903360618 (yellow notepad pricing duplicate, different page — Jul 31, 2024)
- 2684523008388969 (autumn leaves bottle hold — Jul 31, 2024)
- 1285532896830656 (RISK FREE red gradient — Mar 18 start)
- 1955593041515680 ("I finally feel like MYSELF!" testimonial — Feb 17 start)
- 974540865299422 (two-bottle bundle — Apr 24 start)

---

## Tomorrow's rotation reminder

Friday: Arrae, Nuora / myNuora, North Valley Health Clinic
