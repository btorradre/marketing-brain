---
type: session-transcript
date: 2026-03-25
session_id: local_59de03ed-fcfa-47ac-980a-ddabf7330915
title: "Analyze product images for CRO"
tags:
  - session-log
  - transcript
  - creative-production
  - product-photography
  - sora-scripting
  - UGC
  - motilli
---

# Session Transcript: Analyze product images for CRO

**Date:** 2026-03-25
**Session ID:** local_59de03ed-fcfa-47ac-980a-ddabf7330915
**Status:** idle

---

[assistant] Corrected jar description errors:
- Previous: "1:1.2 ratio, mason jar, crystal clear, low profile lid" — all wrong
- Actual: Standard wide-mouth supplement jar, 1:1.4 ratio, visible neck threading, warm/olive tone from dark gummies, normal-height white screw cap (~18-20% of total height)

[assistant] Updated Product Reference section and Image 1 product shot to match real jar.

[user] Okay, better. The product dimensions are right, but the perspective is wrong. It should just be a front shot of the bottle, if that makes sense.

[assistant] Fixed angle to direct front-facing centered view. Also made lid-ON explicit.

[user] Ok, say "stops GLP-1 bloating".

[assistant] Changed hero card and benefits grid from "Flattens Bloating Fast" to "Stops GLP-1 Bloating" — stronger targeting signal.

[user] The product isn't fully in the shot. Can you fix that?

[assistant] Found the problem: prompt said to crop 15% of jar off right edge. Removed cropping from Images 4 and 6 — full jar now visible.

[user] Okay, now I want to create AI UGC testimonials of women over 50 on GLP-1s reviewing the product. Give me five prompts that I can feed into Sora 2 Pro to create this.

[assistant] Used sora-scripting skill. Built 5 UGC testimonial prompts, each ~12 seconds:
1. "The Bloating Is Gone" — car yapper, blonde, Ozempic
2. "Sulfur Burps Finally Stopped" — kitchen table, dark-haired, Mounjaro
3. "I'm Finally Regular Again" — couch, silver-haired, Wegovy
4. "I Almost Quit My Medication" — bedroom, ponytail, Ozempic
5. "My Doctor Asked What I Changed" — car yapper, auburn pixie, Mounjaro

[user] But turn all these prompts into JSON.

[assistant] Converted to JSON format.

[user] Wait, no, I actually want audio. Sora too will actually handle the audio. Can you fix that?

[assistant] Merged audio into prompt with "She says:" framing — Sora generates video and audio together.

[user] None of the UGC testimonials that were generated have my product in it. Can you fix that?

[assistant] Added Motilli jar into each prompt — each woman now holds or interacts with the jar. Jar description matches real product: wide-mouth glass jar, bright lime-green label, white lid, dark green heart-shaped gummies visible.

[user] Can you go generate this for me using Key.ai, please?

[assistant] No Key.ai integration available. Computer use needed — suggested enabling it in Settings.
