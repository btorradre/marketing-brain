---
type: session-transcript
date: 2026-03-25
session_id: local_5f53ddb0-4466-4aa2-bc05-00ac1c7c4fe2
title: "Analyze viral animated ad for recreation"
tags:
  - session-log
  - transcript
  - creative-production
  - motilli
  - animated-ad
  - storyboard
  - gemini
  - glp-1
---

# Session Transcript: Analyze viral animated ad for recreation

**Date:** 2026-03-25
**Session ID:** local_5f53ddb0-4466-4aa2-bc05-00ac1c7c4fe2
**Status:** idle

---

## Summary of Actions

Brooks shared a viral animated e-commerce ad and asked to recreate the concept for Motilli. Used Gemini API (via direct API call with API key from .env) to analyze the video frame by frame, then built a full storyboard document.

### Concept Developed
"Hi! I'm Your Ozempic Shot!" — The GLP-1 injection itself is the anthropomorphic villain character (cocky syringe with sunglasses and gold chain). It brags about killing food noise and weight loss, then casually dismisses the digestive destruction it caused.

### 4-Act Structure (~90 seconds)
- Act 1 (0:00-0:15): Hook — Shot drops into stomach with swagger, brags, then reveals side effects
- Act 2 (0:15-0:40): Damage — Shot is present during every suffering scene (bathroom, dinner burps, bloating). Delivers mechanism education by being dismissive: "I didn't break your colon. I broke your STOMACH."
- Act 3 (0:40-1:05): Motilli enters — Shot panics seeing celery extract. Accidentally reveals why Motilli works by panicking about stomach targeting. Hero ingredients (Apigenin + Chlorophyll) enter and fix everything.
- Act 4 (1:05-1:30): CTA — "Your shot gave you the weight loss. Motilli gave you your life back." Product shot, social proof, 50% off.

### Output
- Motilli_Animated_Ad_Storyboard.docx — Full storyboard with character profiles, scene-by-scene table, voiceover transcript, production notes, legal/compliance guardrails
- Gemini video analysis saved as reference

### Technical Note
Used Gemini API directly (not MCP) with API key from .env file for multimodal video analysis.
