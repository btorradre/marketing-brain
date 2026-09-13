---
type: session-transcript
date: 2026-04-10
session_id: local_7f859d88-9aa5-43fa-96c1-c0a8289c2b93
title: "Market analyst branded statics scraper"
tags:
  - session-log
  - transcript
  - competitor-analysis
  - branded-statics
  - meta-ad-library
  - market-analyst
  - arrae
  - mynuora
  - north-valley-health
---

# Session Transcript: Market analyst branded statics scraper

**Date:** 2026-04-10
**Session ID:** local_7f859d88-9aa5-43fa-96c1-c0a8289c2b93
**Status:** idle

---

[Friday rotation — branded statics scrape for Arrae, Nuora (myNuora), and North Valley Health Clinic.]

[assistant] Used Claude in Chrome to navigate Meta Ad Library, ran JS extraction across each brand's active image ads, captured library IDs and ad metadata, then attempted image downloads.

**Findings:**

**Arrae:** No branded statics. Only surfaced 1 third-party keyword match. Nothing fitting the 8 branded-static archetypes.

**Nuora (myNuora):** 5+ active image ads, but all are native-UGC style "Alicia Darling" hooks cloned from their video formula — not the branded-static archetypes the catalog tracks. Worth noting that the brand is exclusively running personality/UGC creative even in the static format.

**North Valley Health Clinic — KEY FINDING:** ~460 results in the library, 3 fresh image ads launched Apr 9-10 using a **paired-contrast clinical narrative hook**:
- "Patient A does everything wrong"
- "Patient B does everything right"
- Same bad outcome
- Routes to shop.getamalahealth.com for PrimeCell H2

Qualifies as **Archetype #7 (Medical/Clinical Proof)**.

**Images downloaded:** 0 — the browser→sandbox bridge strips base64 blobs and signed fbcdn URLs, preventing extraction. Same blocker hit on previous sessions.

**Files updated:**
- Intel drop: `/Users/brooksorradre2/Documents/marketing brain/agents/market-analyst/intel-drops/2026-04-10_statics-scrape.md`
- Catalog populated: `/Users/brooksorradre2/Documents/marketing brain/statics/branded_statics/north_valley_health/catalog.md` — brand identity, design DNA, hook templates, Library IDs

**Top recommendation:** Re-scrape NVH Monday to see which variants scaled past "Low impression count." The paired-contrast narrative hook is a high-potential template for Lunessa.

**Chrome:** One extension disconnect during NVH load (recovered). No hard crashes. All tabs closed.
