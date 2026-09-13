---
type: session-transcript
date: 2026-05-15
session_id: local_4f06fac5-30de-4414-901e-8e0184c86baf
title: "Analyze Meta ad funnel performance"
tags:
  - session-log
  - transcript
  - funnel-analysis
  - motilli
  - glp1
  - pdp-diagnosis
  - listicle
  - congruence
---

# Session Transcript: Analyze Meta ad funnel performance

**Date:** 2026-05-15
**Session ID:** local_4f06fac5-30de-4414-901e-8e0184c86baf
**Status:** idle

---

[assistant] Now I have everything. Let me give you the actual diagnosis.

---

## FUNNEL MAP

Native Image Ad (Long-Form Copy, Authority Voice) → Product Detail Page → Checkout

(The listicle ad sets route through a listicle bridge first, but I'll diagnose the direct path since that's where most of the spend and data lives.)

---

## DATA SUMMARY — Final

**Layer 1 — Delivery:** HEALTHY ($31-66 CPM)
**Layer 2 — Thumb-Stop:** HEALTHY-to-STRONG (2.4-5.65% UO CTR)
**Layer 3 — Click-to-Page:** Can't measure, but no reason to suspect technical issues
**Layer 4 — On-Page (ATC):** STRONG cost per ATC across most ad sets
**Layer 5 — Checkout (ATC-to-Purchase):** **THIS IS WHERE THE FUNNEL BREAKS**

---

## PRIMARY BOTTLENECK

**The PDP is your primary bottleneck. Not the creative.**

Here's the cleanest read I can give you:

The ads are doing the harder job. A 5% UO CTR on a $44 CPM, getting ATCs at $3-12 — that's a top-of-funnel that's working. The Fiber - NO METAPHORS ad converted 5.00% of impressions into outbound clicks and 6 of those clicks into ATCs. That ad is selling. People are believing it enough to start the buying process.

Then 5 of those 6 ATCs don't convert. Same on Nurse v2: 6 ATCs, 2 purchases. Same on Fiber (old): 15 ATCs, 6 purchases.

**Your average ATC-to-Purchase rate across the campaign is somewhere around 17-40%.** General DTC supplement benchmark is 50-70%. You're well below that.

The leak is post-ATC. Which means it's the PDP and/or the checkout itself.

---

## ROOT CAUSE ANALYSIS — The PDP Breaks the Story

This is where I have to be direct with you. Your ads are arguably some of the best long-form supplement copy I've read in months. They build a complete worldview: three causes, wrong protocol, wrong organ, fiber-makes-it-worse, here's the mechanism, here's the patient story, here's the product. The reader who clicks has been through 15 minutes of structured belief-building. They arrive at the PDP **emotionally invested, mechanistically educated, and ready to be sold.**

Then they hit your PDP. Let me walk you through what they see, in order, with my reactions as the reader the ad just created:

### Above the fold

**Headline: "End GLP-1 Constipation, Sulfur Burps, and Bloating in 2 Weeks — Without Miralax, Fiber, or Quitting Your Medication"**

This is actually good. It honors the ad's claims.

**Sub-headline: "Gets your stomach moving again so food doesn't sit and ferment — where every other product is aimed at your colon, six feet downstream from the problem."**

Also good. Same vocabulary as the ad. Same mechanism.

**Four bullets:** Stomach / Sulfur Gas / Constipation & Bloating / Side Effects.

Fine.

**Then the pricing block hits immediately:**
- Buy One — $23.99 (1 month supply)
- Buy 2 Get 1 Free — $47.98 (3 month supply, SAVE 64%) [Most Popular]
- Buy 3 Get 2 Free — $71.97 (5 month supply, SAVE 68%) [Best Value]
- Subscribe & Save 20%

**This is the first leak. The Buy 2 Get 1 Free pricing is mathematically incoherent and it triggers an immediate trust break.**

Three bottles for $47.98 means $15.99/bottle. The single bottle is $23.99. So "Buy 2 Get 1 Free" is actually "buy 2 at $24 each and get a third free" = $48 for 3 = $16/bottle. That math works. But the comparison strikethrough says "$134.97" — that implies three bottles at full price would be $44.99 each, which is nowhere on the page. The "SAVE 64%" math is fictional from a price that doesn't exist.

Sophisticated GLP-1 buyers — 30-65 year old women, often with medical training, often spending $100+/month on supplements they're skeptical about — will notice this in under five seconds. They've just spent 15 minutes reading a doctor's letter about how the supplement industry deceives them with fake green-labeled products. Now they're looking at fake savings math.

The ad's villain is the laxative-and-fiber aisle that profits from confusion. The PDP introduces a small dose of the same confusion at the moment of decision. That's a tonal break.

### What's missing above the fold

Here's the bigger issue. **The ad set up specific objections that the PDP doesn't answer above the fold:**

- *"Is this going to undo what the medication is doing for me?"* (Linda's question in the ad. The PDP never addresses this where the buyer is looking — only buried in an FAQ.)
- *"How is this different from the green-labeled supplement aisle products you just told me are scams?"* (The ad spent paragraphs distinguishing Motilli from imitators. The PDP doesn't reinforce that distinction near the price.)
- *"The window matters — am I past month 6 or 12?"* (The ad created urgency around timing. PDP doesn't reflect that.)
- *"My patients recover in 4-8 weeks if they start early."* (The ad's specific timeline promise. PDP says "Feel the difference in 90 days." That's a different, weaker promise.)

### Promise-Delivery Break #2

The ad ends with Dr. Marsh saying her patients recover in **4-8 weeks** if within the first 6 months of GLP-1 use, **3-4 months** if past month 12. That's a specific, mechanism-backed promise.

The PDP guarantee says **"Feel the difference in 90 days. Or get 100% of your money back."**

90 days is the *guarantee window* — but the way it's framed, it reads like "wait 90 days to feel something." The ad promised 4-8 weeks of relief. The PDP guarantee accidentally signals "this might take 90 days to work." That's not the same message. It softens the urgency the ad built.

### Credibility Source Downgrade

The ad's credibility is Dr. Rebecca Marsh — board-certified gastroenterologist, 18 years, 3,200 patients, named, with a story. Specific. Authoritative. Personal.

The PDP's credibility is **"10,000+ Happy Customers Nationwide"** and **"4.9/5.0 | 10,247 Verified GLP-1 Reviews."** Volume-based social proof.

This is a credibility *downgrade*. The reader was just walked through medical authority and patient narrative. Now they're being asked to trust an aggregate review count. The 10,247 number doesn't reinforce Dr. Marsh — it replaces her. Dr. Marsh isn't anywhere on the PDP I can see.

The reviews themselves (Sarah K., Jennifer L., Diana R.) are well-written and on-narrative. But they're peer voices, not the authority voice the ad ended on. The reader has been demoted from "consulting a gastroenterologist" to "reading Amazon reviews."

### Mechanism Continuity — Mostly Good, But Buried

The PDP DOES reinforce the three-cause mechanism (Motility / Fermentation / Transit) further down, with the ingredient breakdown and the "Days 1-3 / Days 3-5 / Weeks 2-3 / Week 4+" timeline cards. This is great content. **But it's below the pricing decision.** The reader has to scroll past the buy box to find the proof.

The ad-to-PDP transition should hand the reader confirmation, mechanism reinforcement, and then the offer. Your PDP gives them the offer first, then the proof. That's PDP architecture written for low-consideration impulse buys. Your traffic is high-consideration, story-led.

---

## CONGRUENCE REPORT — Ad → PDP

1. **Angle Continuity: CONGRUENT.** Same problem, same wound, same vocabulary.
2. **Mechanism Continuity: CONGRUENT but DELAYED.** The three-cause framework is present on the PDP but lives below the pricing decision.
3. **Emotional Temperature: MISMATCH.** The ad ends warm, personal, slightly conspiratorial — "I'd rather you find this through an ad than an exam room visit." The PDP opens transactional with a pricing block.
4. **Credibility Source: DOWNGRADE.** From named gastroenterologist to aggregate review count. Dr. Marsh disappears.
5. **Promise-Delivery: DELAYED AND DOWNGRADED.** "4-8 weeks" in the ad becomes "feel the difference in 90 days" on the PDP. The fake "$134.97" strikethrough breaks trust at the decision moment.

**Verdict:** The PDP is converting traffic as if it were generic e-commerce traffic — pricing-forward, social-proof-volume, decision-first. Your traffic is not generic. It's been pre-sold by an authority figure with a specific story. The PDP doesn't pick up where the ad left off. It restarts the sales conversation in a different voice.

---

## Why "NO METAPHORS" Has a Worse Close Rate Than "Fiber (old)"

This is worth a beat. Looking at both ads side by side, the NO METAPHORS version reads slightly faster and cleaner — fewer extended explanations, more rhythm, more direct claim. The "Fiber (old)" version (with metaphors like "hydrating an empty pipe," "operating like a fermentation tank") slows the reader down and forces them to absorb the mechanism more deeply.

The cleaner, faster ad probably attracts more *clickers* and more *impulse ATCs* because it builds belief efficiently. But the slower, metaphor-rich ad probably attracts *deeper believers* — people who have actually internalized the mechanism and walk into the PDP already committed.

A weak PDP punishes the second group less because they've done the closing work themselves before they arrive. The first group needs the PDP to finish closing them, and the PDP isn't.

**This tells you something important: your ad copy quality is currently *masking* PDP weakness in the metaphor version. When you "improve" the ad by stripping friction, the PDP weakness becomes visible.**

---

## RECOMMENDED ACTION

**The first fix is the PDP, not the ads. Specifically the top of the PDP.**

What I'd test, in order of priority:

1. **Above the fold: Restore Dr. Marsh.** Add a 2-3 line authority callout near the buy box: "Formulated based on the protocol Dr. Rebecca Marsh developed for her 47 GLP-1 patients (43 reported significant improvement in 4 weeks)." This carries the credibility source from the ad into the decision moment.

2. **Fix the pricing math.** Either drop the strikethrough comparison or make it accurate. The fake "$134.97" is a trust hit at the exact moment of decision. If you want to keep value framing, use "$23.99/bottle x 3 = $71.97. With the bundle: $47.98. You save $23.99." Honest math.

3. **Move the timeline cards above the fold (or directly under the buy box).** "Days 1-3 / Days 3-5 / Weeks 2-3 / Week 4+" is your strongest mechanism-to-relief bridge. Right now it's buried below the FAQ. It should be the first thing the reader sees after the headline and bullets — before the pricing.

4. **Match the guarantee language to the ad's promise.** Change "Feel the difference in 90 days" to something like "Most users feel the difference in 2-4 weeks. 90-day full refund if you don't." This honors the ad's specific timeline AND keeps the long guarantee window.

5. **Address the "will this undo my medication" objection above the fold.** This is the #1 objection of the avatar. The ad explicitly raised it. The PDP doesn't answer it where the buyer is making the decision.

After those PDP fixes ship, re-run for another 2-3 weeks at current spend. **If ATC-to-purchase moves from 17-40% to 50%+, the diagnosis was right.** If it doesn't move, the next thing to look at is the checkout flow itself (shipping costs, trust badges at checkout, subscribe-and-save defaulting).

---

## What I'm Less Confident About

A few honest caveats:

**Sample sizes are still small.** Fiber (old) at $185 spend / 15 ATCs / 6 purchases is your most stable signal. Everything else is between $0 and $63 spend. I'm drawing patterns from thin data — the PDP diagnosis would be more confident at 50+ purchases per ad set.

**I can't test the actual checkout.** The leak from "Checkouts Initiated = 6" to "Purchases = 1" on Fiber - NO METAPHORS could be the checkout page itself (shipping reveal, trust friction, form length), not just the PDP. The 100% checkout-to-purchase on Nurse_Listicle and Fiber (old) suggests checkout is probably fine, but I can't see it.

**The listicle data is too thin to call.** Nurse_Listicle at 3-of-3 purchases looks magical but it's three data points. I would not bet money on the listicle being a winner yet. Keep testing.

The PDP is the highest-confidence finding. Fix that first.

[user] I think we need something to happen between the native and the PDP. I think this listicle will outperform the PDP. This is the listicle I've been testing at relatively low spend, but here it is.

https://l7.guthealthblog.org/

[assistant] Let me pull up the listicle and compare it to the ad and the PDP. This is the right strategic instinct — but I want to look at the actual page before I confirm it.

[assistant] (called mcp__workspace__web_fetch)

[assistant] Okay. I've read it carefully. Let me give you a real assessment — and I want to push back on the assumption first, then tell you where I land.

---

## Your Premise: "I think this listicle will outperform the PDP"

You may be right. But the data you have doesn't prove it yet, and your reasoning for the prediction matters more than the prediction itself.

**The argument FOR the listicle outperforming:**

The PDP, as I diagnosed in the last message, fails as a closer for high-consideration, story-led traffic. The listicle gives those readers a soft landing — a continuation of the ad's narrative voice instead of a transactional pricing slap. It carries Dr. Marsh forward (more on this in a second), reinforces the three-cause mechanism, restates the timeline promise in the same vocabulary as the ad, and routes to the PDP only after the reader is fully closed. That's textbook good bridge architecture for this kind of traffic.

**The argument AGAINST relying on the current data:**

Nurse_Listicle had 3 ATCs and 3 purchases on $34.76 spend. That's a 100% close rate on a sample of 3. That isn't a signal. That's a coin flip that landed heads three times. Fiber_Listicle had 1 ATC and 0 purchases on $32.06 — also nothing.

You believe the listicle will win. You also have a 100% close rate from Nurse_Listicle and a 0% close rate from Fiber_Listicle. Both are noise. You're pattern-matching on the favorable data point and discounting the unfavorable one. **I'd want to see Nurse_Listicle and Fiber_Listicle both spend at least $150-200 and produce 10+ ATCs each before I'd call the listicle a winner.**

That said — I think your strategic instinct is correct even though the data hasn't proven it. Let me walk through why the listicle is structurally better-suited to your ad traffic than the PDP, and then flag the things in the listicle itself that I'd fix before scaling spend behind it.

---

## Why The Listicle Architecture Matches Your Traffic

Looking at the listicle against the ad, the congruence is dramatically better than ad-to-PDP.

**1. Voice continuity — Dr. Marsh survives.**

The listicle opens with "You're treating the wrong organ. Dr. Marsh said it almost casually." This is a critical move. The reader who clicked the ad just spent 15 minutes inside Dr. Marsh's letter. The PDP makes Dr. Marsh disappear. The listicle hands her to the reader again — except now she's appearing as a character inside someone else's story. The reader gets to be the patient instead of the audience. That's the right vibrational shift between an authority ad and the page after it.

**2. Mechanism reinforcement without echo.**

The "on-ramp/off-ramp" highway metaphor on the listicle is the SAME mechanism as the ad, but said differently. This is what good page-after-ad copy does — it doesn't re-teach, it re-confirms in a fresh frame. The reader thinks "I just learned this AND now I'm hearing it again from a different angle, which means it's real." That's belief escalation, not redundancy.

**3. Emotional temperature match.**

The ad ends warm and personal — Dr. Marsh saying "I'd rather you find this through an ad on your phone." The listicle opens with a first-person patient narrator who's "8 days away from quitting the shot" and "had already typed the message to my endocrinologist." That's the same emotional register. The reader doesn't get jolted. They get sustained.

**4. Promise-delivery alignment.**

The listicle includes a "Your 90-Day Timeline" section: "Days 1-7: bloating starts to ease... Weeks 2-3: sulfur burps reduce... Weeks 4-6: predictable mornings... Day 90: full balance restored." This matches the ad's "4-8 weeks if early, 3-4 months if later" framing far better than the PDP's "Feel the difference in 90 days" guarantee.

**5. The villain stack stays consistent.**

Both the ad and the listicle name the same enemies in the same order: Miralax, magnesium, fiber gummies, probiotics, Dulcolax. The "what most solutions get wrong vs what Motilli does right" table reinforces the exact villains the ad set up. The PDP doesn't do this.

So yes — **structurally, the listicle is the right page for this ad to land on.** Better than the PDP. Without question.

But the listicle has its own problems I'd address before scaling spend.

---

## What I'd Fix In The Listicle

### 1. The reader's identity slips in the first scene

The ad's narrator is Dr. Marsh. The PDP is voice-less. The listicle's narrator is "a patient" — never named, never given an identity beyond "5 months on Mounjaro, $400 spent, missed niece's birthday." That works for the first 3 paragraphs, but then in section 1 ("Wakes Up Your Slowed Stomach...") the voice silently shifts to direct-to-reader marketing copy ("Motilli uses apigenin from premium celery juice extract"). And then there's a testimonial from "Erin H." which is a third voice. And then section 4 opens "I used to dread mealtimes" — back to first-person, but now is this the original narrator or someone new?

The reader can't quite track who's talking. The ad had ONE voice. The PDP had no voice. The listicle has three voices alternating without smooth handoffs. This isn't fatal, but it's a small friction drag through the page.

**Fix:** Either commit fully to the first-person patient narrator (let her introduce the ingredients in her own voice, then quote testimonials), OR make the transitions explicit ("Here's what Dr. Marsh told me about each piece..."). Pick a frame and stay inside it.

### 2. Dr. Marsh is borrowed, not earned

The listicle opens with "Dr. Marsh said it almost casually." But it never establishes that this is the SAME Dr. Marsh from the ad. Most readers will connect the dots subconsciously, but for the reader who's seen multiple ads in your account (Nurse, Daughter's_Gastroenterologist, Jevawell), the "Dr. Marsh" callout is going to feel disconnected unless they specifically clicked the Fiber ad.

**Fix:** If you're going to use Dr. Marsh on the listicle, either name her fully ("Dr. Rebecca Marsh, the gastroenterologist who wrote about this for many of us...") OR consider creating a listicle variant per ad angle so the authority figure on the page matches the authority figure in the ad. The Nurse ad presumably has a nurse character. The Daughter's_Gastroenterologist ad has a different framing entirely. Routing all of them to a Dr. Marsh listicle creates congruence breaks for the non-Marsh ads.

This is a bigger strategic point: **you're running multiple ad concepts but you only have one listicle.** That's an ad-page congruence problem at the campaign level. Long-term, you need a listicle variant per major creative angle.

### 3. The pricing math problem hasn't been solved — you've just pushed it downstream

Every CTA on the listicle ("Get Motilli Now") routes to the PDP. So the same pricing math break I flagged on the PDP — "Buy 2 Get 1 Free for $47.98, was $134.97" — still hits the reader at the moment of decision. The listicle does a better job of pre-closing them, which means more people will make it to that pricing moment, which means the broken math hits MORE people, not fewer.

**Fix:** Fix the pricing math on the PDP regardless of whether you scale the listicle. The listicle architecture doesn't save you from a trust break on the page that holds the buy button.

### 4. "Gastroenterologist-Recommended Formula" is unsupported

The hero image alt text and the bullets near the bottom say "Gastroenterologist-Recommended Formula." The ad has Dr. Marsh recommending it. ONE gastroenterologist. The plural "Gastroenterologist-Recommended" implies more than one. This is a small claim, but the avatar (medically literate women 30-65) will notice it. If it's just Dr. Marsh, say so explicitly. If it's actually multiple gastroenterologists, name two and let the rest be implied.

### 5. The "Imagine in just 90 days" section is the weakest closer

Right before the final CTA you have a bulleted "Imagine, in just 90 days" list. This is generic benefit-stacking ("waking up without bracing for what your stomach's going to do") that doesn't match the texture of the rest of the page. The page has been built around specific, named patients with specific stories. The final imagination section is faceless. It also reverses the timeline expectation — the previous "Your 90-Day Timeline" promised relief in days 1-7. Now you're asking the reader to imagine 90 days from now. That's a temporal whiplash.

**Fix:** Either remove this section or anchor it to the timeline you already established ("In 7 days you'll feel the bloating start to ease. In 3 weeks the burps will be gone. In 90 days...").

### 6. You're not using Dr. Marsh's patient stats

The ad ends with one of the strongest authority claims in the entire piece: "47 patients on Motilli, 43 reported significant improvement in 4 weeks, 2 needed an extra month, 2 didn't respond." That's the kind of specific, falsifiable, doctor-grade proof that converts skeptics. The listicle doesn't carry this forward. It uses "38,000+ GLP-1 users" and "10,000+ verified reviews" as social proof instead. Volume-based proof is weaker than physician-grade proof for this avatar.

**Fix:** Either lift the 47-patient stat directly into the listicle (probably near section 1 or the timeline section), or weave it into the testimonials section as a third-person callout from Dr. Marsh.

---

## Strategic Read: Do The Listicle Test, But Do It Right

Here's what I'd actually recommend:

**1. Run the listicle test at meaningful spend.** Currently Nurse_Listicle has $34 and Fiber_Listicle has $32. That's not a test. That's a sneeze. Push each to at least $300-500 in spend before you call the result, so you have 20+ ATCs per ad set to evaluate ATC-to-Purchase rate against.

**2. Fix the listicle's voice issues and the unsupported "Gastroenterologist-Recommended" claim first.** These are small but they cost trust. 30 minutes of edits.

**3. Fix the PDP's pricing math regardless.** Whether the listicle wins or loses, that PDP problem leaks money on every funnel path you run. It's the highest-leverage single fix in the whole account.

**4. Plan a listicle variant per ad angle.** If you keep running Nurse, Daughter's_Gastroenterologist, and Jevawell creative, you need three listicles — not one. The current listicle is built off the Fiber ad's authority figure. Routing the Nurse ad through it creates a credibility-source congruence break.

**5. Don't kill the direct-to-PDP path yet.** Even if the listicle wins, the Fiber (old) ad converted 6 purchases at $30.94 CPA directly to PDP. That's a working funnel. The question isn't "listicle or PDP" — it's "which ads should route through a listicle, and which should go direct." That's an answer you'll have after the spend-up test.

---

## Bottom Line

Your instinct is right: the listicle is structurally a much better landing for your ad traffic than the PDP. The voice continuity is intact, the mechanism reinforces without echoing, the emotional temperature matches, and the promise-delivery is aligned.

But the listicle has its own problems (voice slippage, single Dr. Marsh framing across multi-angle campaigns, the unfixed PDP pricing math waiting at the end of every CTA, weak closing section). And you don't have nearly enough spend behind it yet to claim it's working. The 100% close rate on Nurse_Listicle is statistical theater.

If I were running this account, I'd do three things in this order:

1. Fix the PDP pricing math TODAY. It bleeds trust regardless of which funnel path the user takes.
2. Spend 30 minutes patching the listicle voice issues and the unsupported plural claim.
3. Push $300-500 behind each listicle ad set and the direct-to-PDP ad sets in parallel, then evaluate ATC-to-Purchase rate at 20+ ATCs per cohort.

After that, you'll have an actual answer instead of a hypothesis with three data points.

[user] I actually think the problem is the offer.

---

*Note: Transcript captured at idle. The conversation ended with the user's reframing — "I actually think the problem is the offer" — which the assistant had not yet responded to at the time of logging.*
