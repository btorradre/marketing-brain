---
brand: velantra
artifact: brief
generated_by: dr-os-mcp
updated: 2026-08-21
sources:
  - http://instagram.com/p/Dbrbo70AAc2/
  - _engine/mcp/ad-engine/data/watch/job_9f6a924f572b/manifest.json
  - brands/velantra/products/weekender/concepts/8-20-26-zede-airport-replication/adaptation-plan.json
  - brands/velantra/products/weekender/concepts/8:10:26 - black preorder greenscreen/CONCEPT.md
  - https://velantrafashion.com/products/velantra-weekender
  - ~/.claude/skills/velantra-weekender/SKILL.md
  - brands/velantra/products/weekender/concepts/8-21-26-birkin-greenscreen/CONCEPT.md
---

VEL-WEEKENDER-GS-BIRKIN-01. Greenscreen AI UGC, Eleanor Weekender Light Chocolate.

The 8/20 Zede airport AI UGC script held word for word and moved into the greenscreen format proven by DC-04 and BLK-01 (creator keyed PiP bottom-left for the full runtime over full-frame b-roll, burned captions, one continuous VO, 1080x1920). Angle broadened off "perfect summer travel bag" to just the perfect travel bag, season-neutral. New mechanism: Birkin-inspired silhouette scaled up to travel size.

Cutroom board: http://localhost:8765/b/vel-weekender-gs-birkin-01 (slug vel-weekender-gs-birkin-01)
Full concept, beat map and production recipe: brands/velantra/products/weekender/concepts/8-21-26-birkin-greenscreen/CONCEPT.md

THREE SCRIPT CHANGES, all forced by facts. Nothing else moved.
1. "It's got that classic structured shape everyone recognizes" reverts to "It's a Birkin-inspired shape, just scaled up to a travel bag." That hedge was the law-forced replacement for exactly this line on the Zede build, so this is a straight reversal back, per Brooks.
2. "three colors" becomes "four colors." Verified live 8/21: Light Chocolate, Army Green, Dark Chocolate, Black.
3. "an end of summer sale" becomes "a sale right now," so the asset survives 9/1.

LOCKED SCRIPT (252 words, spoken):
Okay, if you travel at all, I need to show you something. I used to check a bag for every single trip, because I could never fit everything into something that also looked good. My old duffel held everything, but it looked like a gym bag. And my nice bags held basically nothing. This is the Weekender from Velantra. It's a Birkin-inspired shape, just scaled up to a travel bag. So it holds three days of clothes, plus my laptop, my chargers, all of it, and it keeps its shape whether it's packed full or half empty. The whole inside is this soft caramel leather with a big slip pocket, and the top flap just folds back so I can see everything at once. I packed it for a three day trip and I didn't check a single thing. It slides right into the overhead bin, so I walk straight past the bag drop line every time. I've taken it to three cities in the last two months, and I get stopped about it constantly. People always ask if it's a designer bag. There's no logo anywhere on it, it comes in four colors, and they sell it for about a hundred and sixty dollars. So if you're tired of paying for checked bags, or you just want one bag that actually does everything, go look at Velantra. They're running a sale right now and colors sell out fast, so I'd get yours quickly. I've left the link below.

TTS feeds the brand as Vell-Ahn-Trah. Plain spelling returns Volantra or Velen Trail and kills the take.

MECHANISM RATIONALE. The problem beat states a real bind: capacity and shape have been mutually exclusive for her. "Birkin-inspired shape, scaled up to a travel bag" resolves that bind in one sentence and explains every downstream benefit the script already claims. It never names Hermes, never quotes a Birkin price, never uses dupe, replica, alternative or knockoff, and never ranks the bag against anything. The live PDP already reads "The structured, Birkin-inspired silhouette, sized for a weekend away," so the ad is congruent with the page it clicks to rather than introducing a new claim. The word Birkin must never enter a generation prompt (kie claims-grep blocks it); it lives in the VO and caption layer only, which this format supports because the b-roll is already shot.

RUNTIME, FLAGGED. Roughly 93s at this creator's measured 162wpm, against a 41 to 53 second norm for the format. Never atempo, that produced the robotic take on the men's cut. Recommendation is to ship the full read as a MOF and retargeting asset, and cut four marked lines for a 70s cold TOF version: "and it keeps its shape whether it's packed full or half empty"; "I packed it for a three day trip and I didn't check a single thing"; "I've taken it to three cities in the last two months, and"; "or you just want one bag that actually does everything."

BEAT MAP, 21 beats. Main frame is bag and hands only for the entire runtime so the b-roll model's face never competes with the keyed presenter. 1 door and roller, 2 entry bench with coat, 3 bed flatlay, 4 bed styled, 5 sofa scale, 6 front hero console, 7 MECHANISM bag on top of a full-size carry-on with the silhouette dead front-on and scale unmistakable, 8 laptop going in, 9 open and packed holding structure, 10 hands packing with caramel interior visible, 11 one-piece flap folded fully back, 12 packed beside the roller, 13 overhead bin (the only new generation, no-person still, frame-first with a slow push-in), 14 carry and walk cropped below the chin, 15 macro hardware, 16 macro clean leather no logo, 17 PDP four swatches, 18 PDP price block, 19 entry bench, 20 PDP scroll to buy box, 21 PDP add to cart.

ASSETS. Every beat except the overhead bin pulls from the existing Weekender library (lc-travel and onroute series). Board frames extracted to the concept's board-frames directory. The live PDP was captured headless on 8/21 and cropped into the offer-block and feature/pre-order proof frames.

PRODUCTION, all validated on DC-04 and BLK-01. VO: ElevenLabs Woman Over 40 (NBIPq5xdnIg9kaBH5Ape), eleven_v3, stability 0.0, three takes, STT-gate every one on word timestamps. Avatar: no new avatar, re-drive the existing green creator clip with the new VO through fal sync-lipsync v2 in bounce mode. Chromakey 0x007A28 similarity 0.11 blend 0.02, despill OFF (0.5 renders a cream sweater visibly pink). PiP 44% width bottom-left. Captions capped at 4 words and flushed at terminal punctuation. Offer beat: headless Chrome at window-size 500x3200 with force-device-scale-factor 3, pan started BELOW the gallery because the carousel ignores the variant parameter. VP9 alpha needs -c:v libvpx-vp9 before the webm input or the presenter renders as an opaque green box.

FLAGGED FOR BROOKS.
1. The Birkin line is already live on our own PDP, so the standing house law saying Birkin stays out of Velantra copy entirely now contradicts our storefront. The law text needs resolving.
2. Black is a pre-order shipping mid September 2026; Light Chocolate, Army Green and Dark Chocolate ship now. "Four colors" is true but the ship split should sit in the ad copy, not in her mouth.
3. The live PDP description contains an em dash, in the clause running from "sized for a weekend away" into "and made in limited quantities". Minor, but it breaks the house rule on our own page.

COMPLIANCE. Creator says "they," never "we." No competitor named or ranked. No season in the read, so no calendar death. Swap test fails for a rival at the mechanism, the fold-back flap, the gold turn lock and the no-logo fact. Every claim has its own demo frame. One creator locked, no second face on screen. TOF opens on her situation, not the product. Price and colour count verified live 8/21. No em dashes. One continuous VO, never chained.
