---
type: session-transcript
date: 2026-04-25
session_id: local_a73be7ba-127e-47e7-ba89-b3378bee83fa
title: "Market analyst meta scraper"
tags:
  - session-log
  - transcript
  - market-analyst
  - meta-scraper
  - weight-loss
  - glp1
  - amanda-reeves
  - eddie-abbew
  - betterthanbefore
  - haven
---

# Session Transcript: Market analyst meta scraper (2026-04-25 weight-loss/GLP-1 rotation)

**Date:** 2026-04-25
**Session ID:** local_a73be7ba-127e-47e7-ba89-b3378bee83fa
**Status:** idle

---

[NOTE: This is a condensed transcript of the most recent activity. The full session involved chunked extraction of 4 long-form ads from Meta Ad Library via JS injection.]

[assistant] Let me try to expand each ad and capture the full text. I'll go more aggressive on the "See more" buttons, including aria-labels.
[assistant] Only 1 visible "See more" — the rest may already be loaded but I cap'd at 5000 chars in my scan. Let me look at the full bodies for each target ad.
[assistant] All three priority ads have their full content already loaded.
[assistant] Lengths look weird (11k for two, 1k for Betterthanbefore). Lengths include trailing UI cruft. Let me extract each individually and tighten the boundary cut.
[assistant] Excellent. Full ad copy of 9-10k chars. Let me extract all three ads cleanly.
[assistant] My boundaries cut off Amanda's ad too late (still has UI noise) and Betterthanbefore is short — it's a shorter ad to begin with.
[assistant] Betterthanbefore's actual ad is shorter — that IS the full body (~900 words is normal for a punchy GLP-1 angle). It cuts at "Link is below." then goes into CTA card.
[assistant] Amanda is 23k chars — that's likely Amanda's ad + the SECOND Amanda Reeves ad merged because the boundary "TRYHAVENHAIRCARE" appears later in the page.
[assistant] Amanda's ad is 11,368 chars / ~11.3k chars. The "TRYHAVENHAIRCARE.COM" CTA card is the actual ad boundary.
[assistant] Eddie now at 11,585 chars (clean). Let me retrieve each one in chunks and write to disk.
[assistant] The browser tool truncates output. Let me try a different approach — use JSON.stringify and check whether shorter slices work, or write to clipboard.
[assistant] Good — stored in window. Now let me retrieve in chunks. The truncation seems to happen around 1000 chars.
[assistant] BTB ad has "Low impression count" trailing. Let me strip that and store cleanly. Need to deliver text in chunks under ~1000 chars per call.
[assistant] JS returns ~990 chars then truncates. Let me chunk in 950-char slices for retrieval.
[assistant] Got 950 cleanly. Amanda is 11,367 chars = ~12 chunks. Eddie is 11,585 chars = ~13 chunks. Plus BTB at 932 (1 chunk). Total ~26 calls — too many. Let me try a different approach: write the text to clipboard or post via fetch.
[assistant] Let me try using batch tool to grab chunks with multiple calls in one round trip.
[assistant] Got chunks 1-6 (covers chars 950-6650). Let me get the rest.
[assistant] Amanda Reeves ad fully captured. Now Eddie.
[assistant] Continuing — got Eddie chunks 1-6 (0-5700). Need chunks 7-13.
[assistant] The Eddie ad ends at "Just watch it. / It's free. / And it might be the most important thing you watch this year. / 👉🏿 https://abbewcrew.co.uk/video-g-us / Eddie". The text after "Eddie\nLow impression count" is the SECOND Eddie Abbew ad — that's actually a different valuable ad ("£250 a month — pharma business model"). Let me grab that as a 4th swipe since it's clearly running.
[assistant] Eddie #2 captured at 1284 chars.
[assistant] All four ads fully captured:
1. Amanda Reeves — Haven Red Root Complex (~11.4k chars) — GLP-1 hair loss / Korean red root mechanism
2. Eddie Abbew #1 — abbewcrew.co.uk free training (~11.6k chars) — menopause "one hormone" angle
3. Eddie Abbew #2 — abbewcrew (~1.3k chars) — Ozempic business model contrarian short-form
4. Betterthanbefore — Multi Collagen (~932 chars) — Ozempic Face / collagen depletion

[assistant] (called Write × 4 — saved each ad to the brand reference folders)
[assistant] (called Write — intel drop)
[assistant] All files filed cleanly. Run summary:

**Meta Ad Library Scrape — 2026-04-25 (Saturday → weight loss / metabolism / GLP-1)**

- Keywords searched: "weight loss supplement" (~6,400 results)
- New brands found: 3 — Amanda Reeves (Haven Red Root Complex), Eddie Abbew (abbewcrew.co.uk), Betterthanbefore (Multi Collagen)
- Ads swiped and filed: 4
- Top insight: The GLP-1 side-effect category is moving from generic "Ozempic Face → collagen" plays into specific sub-mechanism + compatibility positioning fast. Amanda Reeves's "I'm still on my GLP-1 because I don't have to choose" reframes the entire GLP-1-recovery category — instead of fix-the-side-effect-by-quitting, the product stacks compatibly with the drug.
- Issues: None — Chrome ran one tab cleanly and closed without crashes.
