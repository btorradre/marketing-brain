# Motilli campaign bottleneck audit — September 12, 2026

The observed break is between landing-page arrival and campaign-attributed add-to-cart. The exact customer-level cause is not identifiable from this sample. The clearest creative weakness is delayed useful explanation/product connection; the strongest next diagnostic is reconciled cart attribution plus controlled testing of an earlier mechanism-to-product bridge. A completely unrelated landing page or universally broken cart is not supported by the inspected evidence.

## Source and reporting scope

Read-only Meta Graph API v23.0, account 1752609235887283, campaign 52622637303560 (mot vids 2). Retrieved around 16:31–16:35 UTC / 11:31–11:35 Chicago / 12:31–12:35 New York, September 12. Account currency USD, timezone America/New_York. Campaign created September 11 at 23:38 EDT, scheduled September 12 at midnight. September 11 insights empty. User URL requested September 12–13; a separate September 12-only ad-set/account query confirmed the totals. This is a partial-day snapshot, not two completed days. Campaign was already PAUSED. No campaign settings, budgets, creative or pages were changed.

All ad sets optimize offsite conversions for PURCHASE using pixel 1536431777433131, with 7-day click, 1-day view and 1-day engaged-video-view attribution. Broad US Advantage audience. This is not a traffic-optimized campaign.

| Ad set | Spend | Unique outbound clicks | Unique outbound CTR | Cost / unique outbound click | LPV | Campaign-reported website ATC |
|---|---:|---:|---:|---:|---:|---:|
| AI UGC VSL | $48.70 | 21 | 4.67% | $2.32 | 22 | 0 |
| Podcast | $42.32 | 21 | 6.54% | $2.02 | 21 | 0 |
| AI voiceover | $7.65 | 2 | 2.41% | $3.83 | 1 | 0 |

Campaign totals: $98.67, 900 impressions, 46 outbound clicks, 44 LPV, 44 reported ViewContent events, no campaign-reported website ATC/checkout/purchase. Missing website action types are interpreted as zero reported in this response, not independent proof that no customer acted. Do not sum per-ad-set unique people into a deduplicated campaign audience. LPV are event counts, not 44 verified distinct visitors. The roughly 96% LPV/outbound-click count ratio does not suggest a large pre-load loss but is not a matched visitor funnel; one ad has more LPV than clicks.

Sample context: under an illustrative 5% true ATC probability and 44 independent visitors, zero ATC occurs about 10.5% of the time; with 22 it occurs about 32.4%. Five percent is an example, not a Motilli benchmark, and the LPV counts do not establish independence. AI voiceover has only one LPV and cannot meaningfully be judged. Cost per click is not profitable performance without acquisition economics.

## Live creative identity and timing

Meta object_story_spec video IDs and uploaded titles identify the live files. Two Meta-served video copies were downloaded and visually sampled. Local matching caption/plan artifacts supplied cue times. This is not an exhaustive frame/audio editing audit and does not certify subjective choppiness or an immutable database export binding.

| Ad ID | Ad-set / ad name | Uploaded video |
|---|---|---|
| 52622637303360 | AI UGC / 1 | V31 H3 ACTUAL-PACKAGING, 211.199s |
| 52622638719760 | AI UGC / 2 | V31 H2 ACTUAL-PACKAGING, 209.322s |
| 52622638750760 | AI UGC / 3 | V31 H1 ACTUAL-PACKAGING, 204.735s |
| 52622638771360 | Podcast / 1 | Motilli-Podcast-Complete-Captions, 162.772s |
| 52622639089160 | AI voiceover / 1 | MOT-VID-013 Hook C R3, 95.968s |
| 52622639777760 | AI voiceover / 2 | MOT-VID-013 Hook B R3, 95.968s |
| 52622639922560 | AI voiceover / 3 | MOT-VID-013 Hook A R3, 95.968s |

UGC H1 begins the actual stomach-muscle explanation around 71.6 seconds. It names Motilli around 161.6 seconds; product insertion is planned at frame 4849/30fps and visible in the Meta-served sample at 161.7 seconds. H2/H3 packaging begins around 166.2/168.1 seconds. The preceding minute includes agitation, social discomfort, fiber, MiraLAX and a research story. Its opening promises to explain the slowdown, then delays that payoff. The script already has open loops, but several repeat that something was missing rather than providing a specific bounded payoff.

Podcast mechanism education starts around 8 seconds, three-ingredient explanation around 79 seconds and Motilli around 111.8 seconds. Product is visible in the downloaded sample at 112 seconds. It therefore supports testing an authority/education format, but early attention is not proof of product persuasion.

Hold defined here as ThruPlays / three-second views: UGC 74/214 = 34.6%; podcast 79/159 = 49.7%; AI voiceover 9/30 = 30.0%. With these long videos, the ThruPlay milestone is 15 seconds. Average watch time is 16s UGC, 18s podcast, 8s AI voiceover. Podcast has 29 views at 50%, 10 at 75%, 3 at 95%. UGC H1 has 15 at 50%, 9 at 75%, 5 at 95%. These are video milestone events, not identified unique buyers or an exact measurement of who heard the brand. They reveal why early hold cannot establish exposure to a late product argument. Click timing relative to narration is unavailable.

## Exact destination and purchase test

All seven ads link to https://getmotilli.com/products/motilli-3-bottle-90day-reset . Mobile Chromium page returned HTTP 200 and rendered. The hero uses the same Motilli bottle, GLP-1 audience and stomach/top-versus-bottom mechanism. Initial 390x844 viewport shows the hero and message, with price/CTA below the first screen. Product-specific supporting explanation is largely beneath the buying block or in accordions.

Despite the URL, a single bottle is available for $29.99. Default selected offer is buy two/get one free: three bottles for $59.98. Five bottles are $89.97. Clicking the default Add to Cart produced three items, $59.98 subtotal and a visible checkout button. No checkout or purchase was performed. The default three-month commitment is an offer-friction hypothesis; it is not a mandatory $59.98 minimum or a demonstrated cause of abandonment.

Confirmed copy inconsistency: V31 UGC says two gummies before breakfast; landing page says before bed and particularly the night before the shot. Podcast says the fiber does not form a thick bulky gel; page says it forms a soft gel and makes stronger generalizations about alternatives. Align the instructions and the degree of claim qualification to approved, substantiated product information. Do not solve congruence by repeating unsupported claims across both surfaces.

Interpretation: the education-to-store transition may ask for more product trust than the ad has created. Clinical-sounding badges and efficacy percentages on the page need accessible genuine substantiation; their presence alone does not prove the product mechanism. No clinical efficacy review was performed in this funnel audit. The page also emphasizes an 8–12-week/90-day commitment while testimonials mention much earlier experiences; clear expectations merit testing, but variable results are not automatically contradictory.

## Tracking findings and limits

Pixel source configuration names 1536431777433131, matching ad sets. Meta pixel event stats show three AddToCart and three InitiateCheckout events in the September 12 15:00 UTC bucket, before the first audit cart at 16:33 UTC. They are not attributed to this campaign in the retrieved insights. Their origin could be other traffic, user tests or duplicated events; do not count them as three unique shoppers or campaign conversions. The pixel-stats response is paginated and partial; this is a positive observation of that bucket, not a complete site total. The basic last_fired_time field is stale relative to the returned event buckets, so it cannot establish an outage.

Mobile test: cart succeeds and Shopify product_added_to_cart plus an AddToCart request to the site's tracking endpoint were observed. Facebook /tr POST requests returned HTTP 200 in a further test, but the inspection did not decode their event/pixel payloads. Some tracking-endpoint requests were aborted in the automated environment. This does not prove production attribution or CAPI correctness, nor establish an outage for real visitors. Need Events Manager Test Events and first-party cart/session reconciliation to fully clear attribution. No server-event deduplication validation or Safari/Meta in-app-browser test was completed.

Test carts are synthetic, unpurchased and had no ad click IDs. Baseline campaign snapshot preceded them. Keep later site activity separate from this snapshot. First simple network listener only checked query parameters and missed POST event data; its empty event array is not a tracking-failure finding. An intermediate listener failed on compressed payload; the corrected network capture supersedes it.

## Next decisions

1. Reconcile campaign-attributed events with first-party cart/session data; validate browser/CAPI AddToCart and correct pixel in Test Events. Reporting is the first uncertainty to close.
2. Correct the substantiated ad/page usage inconsistency and make price, serving and proof easy to find. If testing the offer, compare one-bottle versus three-bottle default with creative fixed; measure ATC/session, purchase conversion, revenue and margin, not ATC alone.
3. Retain podcast as a control. Test a shorter authority-led explanation with a specific early educational payoff and earlier product bridge. Separate the structural test from visual polish and landing-page tests; do not simultaneously change everything and claim a cause. The goal is qualified buying intent, not only more hold/CTR. Credentials, endorsements and mechanism claims must be truthful.
4. Treat choppy AI coverage as user feedback needing a separate playback/boundary audit. Stable presenter continuity and complete explanatory actions are sensible test directions; no causal conversion claim is established here.

No ads, landing pages or storyboards were revised/generated. Findings saved to shared ad memory as observations/hypotheses with insufficient evidence for a winner/loser verdict. Raw API files, uploaded-video metadata, Meta-served samples, browser screenshots and test receipts are adjacent to this report.
