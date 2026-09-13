# VEL-MARGOT-PERFECT-VO-01 — "Perfect Work Bag" product-focused VO ad

**Shipped 2026-07-27.** Faceless product-montage VO ad (Weekender aivo format) for The Margot Leather Tote, Burgundy — "the perfect work bag" positioning. Finished cut delivered, edited in-pipeline per Brooks ("you create and edit the video").

## Deliverables

| File | What |
|---|---|
| `VEL-MARGOT-PERFECT-VO-01-final.mp4` | 28.3s, 1080×1920, 24fps, captions burned, VO at −14 LUFS, no music |
| `VEL-MARGOT-PERFECT-VO-01-final-nocaptions.mp4` | Clean plate for re-captioning |
| `VEL-MARGOT-PERFECT-VO-01-voiceover.mp3` | Main VO (comment-MARGOT CTA), one seamless ElevenLabs take |
| `VEL-MARGOT-PERFECT-VO-01-voiceover-alt-link-ending.mp3` | Same read, "I've left the link below if you want it." ending (23.5s) for paid placements |

## Script (as delivered, all Brooks's lines, product-only)

> Okay, I think I found the perfect work bag, and it almost feels illegal. Structured leather with a fine embossed grain, a belt strap and a silver turn lock. It stands up on its own, it fits your laptop and your planner, and it goes with everything you wear to work. Would you believe me if I told you it's under a hundred dollars? This is the Velantra Margot. Comment MARGOT and I will send it straight to your DMs.

## Production

- **Zero new video generation.** All 10 visuals reuse the QA'd 7/27 asset package (`../7:27:26 - tof ugc perfect work bag/assets/`): 5 Google Omni b-roll scenes (var1s) + 4 GPT Image 2 stills, all seeded from the live burgundy PDP.
- **VO:** ElevenLabs `Velantra Quiet-Luxe VO (Eden ref)` — one seamless take. **Pronunciation law: write "Margo" in the TTS input** (plain "Margot" renders a hard t: "mar-GOT"). Do NOT try hyphen-phonetics ("Vel-AHN-tra") — ElevenLabs reads the caps as spelled letters. Verified by Gemini audio QA: veh-LAHN-truh ✓, MAR-go with no t ✓.
- **Edit:** `_production/assemble.py` — beats cut to Gemini phrase timestamps, both face-showing walk clips (scene03/scene11 feature two different women) punched in 0.74x and reframed faceless per the goeswith model-discontinuity law, Ken Burns zoompan on stills, PIL caption cards (Arial Rounded Bold, white + black stroke, 78% height — no drawtext/libass in this ffmpeg), loudnorm mux.
- **Beat map:** office walk → hero push ("feels illegal") → grain macro → turn-lock → standing still ("stands up on its own") → laptop-in → on-model faceless → closeup push (price) → golden-hour walk (name drop) → hero zoom-out (CTA).
