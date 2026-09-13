# VEL-TRIAL-GEN-01 · "The Weekender Build" Generation Trial, Worked Edition

## 1. Header

**Concept one-liner:** the completed reference edition of the generation trial, the teaching copy for the walkthrough Loom. One visual per script line: ten frames, ten clips, one finished 32 to 36 second faceless VO ad for the Eleanor Weekender. Script, product truth and claim logic are the VEL-TRIAL-02 ones; read that document first.

**Reference ad (watch it here):** https://app.trendtrack.io/share/ads/sarah-and-stone-nvIyig
37.5 seconds, vertical, one female voiceover over silent footage, no talking head. 31 cuts from roughly 7 physical setups, average shot length 1.2 seconds, persistent black lower third naming the product for the entire runtime. Watch it twice before generating anything: once as a viewer, once counting cuts.

**Format:** 32 to 36s, 9:16, faceless female VO, hard cuts, persistent lower third, static price card close.

**Pipeline:** GPT Image 2 generates each scene still (i2i, product photo wired in) → QA the still → Google Omni animates the approved still with a motion-only prompt, 10s, 9:16 → ElevenLabs renders the VO. Stills first, clips second, always. Three variants per still, pick one, keep rejects beside the pick.

**Deliverables:** ten picked frames (`VEL-GEN-S<scene>_pick.jpg`, rejects kept beside them, plus the pin used for each), ten clips (same naming, `_clip.mp4`), the finished ad cut to the VEL-TRIAL-02 script and spec, and a one-page note listing every regenerate you called and why, and every clip where you used partial clean seconds. The note is the part we read twice.

**Product references (save these before you start):**
Light Chocolate: https://velantrafashion.com/products/velantra-weekender?variant=44165996544065
Army Green: https://velantrafashion.com/products/velantra-weekender?variant=44165996642369
Open-bag scenes also use the open-bag and interior photos from the same page.

---

## 2. Beat map (reference → ours)

| Reference beat | Our beat | What changed and why |
|---|---|---|
| Faceless female VO over silent b-roll, no talking head | Same | The format is the winner, keep it |
| 31 cuts from 7 setups, the same scenes re-entered across the edit | ~24 to 28 cuts from 10 frames plus re-entries | Same trick: fast cadence from a small pool |
| Persistent black lower third naming product and brand | Same: THE ELEANOR WEEKENDER BY VELANTRA | Proven retention device |
| VO names five colours while one pink bag stays on screen | Line 8 cuts to the army green actually on screen (S08) | The beat the reference fumbled; we fix it |
| Opens on a hold | The cut moves inside the first second | Retention law |

---

## 3. Final script (VO, ONE seamless track, warm American female, late 20s to mid 30s, conversational)

9 lines · 99 words · locked, do not rewrite · render as one continuous file, never line by line

> This is the Eleanor Weekender.
>
> It's the only bag I pack for a weekend trip.
>
> The whole top is one piece of leather that folds over the front.
>
> Cognac leather, woven canvas, gold hardware, and no logo anywhere on it.
>
> It holds three days of clothes and still slides into the overhead bin.
>
> Packed full or nearly empty, it keeps its shape.
>
> The handles are rolled and reinforced so they don't dig into your arm.
>
> It comes in light chocolate and army green, one size, a hundred and fifty nine dollars.
>
> Both colors are on the site right now.

VO notes: talking to a friend, never an announcer. Natural pauses. Cut picture to the actual rendered voiceover, not to estimated timings.

---

## 4. Visual system + product lock

**Style bible (pasted into every image prompt):**

> This is a real photograph casually taken handheld on an iPhone by an ordinary person, one dominant available light source, mixed colour temperature, uneven exposure, real shadows with ambient bounce. NOT a 3D render, NOT CGI, NOT a product visualisation, NOT a catalogue or studio product photo, never retouched or airbrushed. Visible sensor noise through the shadows, highlights slightly blown where the light hits, mild chromatic aberration on contrast edges, nothing tack sharp, a trace of handheld blur, framing slightly crooked and off centre. The leather is creased and faintly scuffed, the canvas shows individual woven fibres, ordinary dust and fingerprints are present, the setting is a real lived-in place with ordinary clutter. Any skin shows real texture and any face stays fully outside the frame. No on-screen text, lettering, signage or graphics anywhere. Vertical 9:16.

**Bag identity block (pasted into every image prompt):**

> The bag is a structured two tone weekend bag, wider than tall: rich cognac brown leather upper flap section, two rolled cognac leather top handles that are smooth simple tubes with no braiding or wrapping, a cream ivory woven canvas body, a small gold oval turn lock on the front, two flat gold clasp plates with cognac leather belt straps threaded through them, both plates the same warm brass gold, a small cognac leather key bell at the handle base, cognac leather corner patches, visible stitching, gold hardware only, no logo anywhere on the bag, no zipper anywhere on the bag. The bag keeps exactly these proportions and details everywhere in the frame, even when small or out of focus.

S08 only: swap "cream ivory woven canvas body" for "deep army green twill canvas body."

**Open-bag block (added for S03b and S05):**

> The entire cognac leather flap, one single piece, is folded backward over the top rear edge and leans back behind the open mouth, its inside face showing two round handle holes, strap slots and a small gold plate. The line where the leather ends and the canvas begins sits in exactly the same place as on the closed bag; folding the flap back never moves it. Both rolled handles stand clearly upright, anchored into the wide leather band, never into the canvas; never omit the front handle. The mouth is a clean open oval showing the cream cotton canvas interior lining and the cognac leather slip pocket on the back wall, with no zipper anywhere along it. The belt straps hang loose and unfastened down the front.

**Reference wiring:** attach the product photo first, then your ONE picked pin. Open every image prompt with: the attached product photo supplies the bag only (shape, proportions, materials, colours, stitching, hardware), never its studio lighting, white background or polished catalogue look; any other attached photo is a composition reference only (camera angle, framing, setting, light), any bag in it replaced completely by ours, any person contributing pose only with the face out of frame. S03b and S05 attach the open-bag photo, then the interior photo, then the pin.

**Prompt assembly:** every image prompt = reference wiring opener + the Scene cell below + the bag identity block (+ the open-bag block where marked) + the style bible. Every video prompt = the Motion cell below + this fixed footer:

> Every detail of the bag stays exactly as in the image, nothing on the bag moves or changes shape. No people speaking, natural ambient sound only. Vertical 9:16.

**Product truth (auto-fail, no exceptions):** hand or forearm carry only, never a shoulder or long strap · gold hardware only, both clasp plates matching · no logo, no lettering, no zipper · the flap is one single piece · the leather-canvas split never moves between shots · the bag is never opened, closed or fastened on camera, state changes happen across hard cuts · never state where the bag is made · never name or compare another brand.

---

## 5. Scene map

Ten frames, ten clips. Judge each pick photoreal first, product truth second, composition third.

| # | VO line | Scene | Motion | References |
|---|---------|-------|--------|------------|
| S01 | Hook, "This is the Eleanor Weekender" (also closes L9) | Closed light chocolate bag on a worn entryway bench, morning window light from the left, keys and a folded denim jacket beside it, white sneakers half cut at the frame edge | Very slow handheld sideways drift with slight focus breathing. Nothing in the scene moves. | Setting [entryway bench morning light](https://www.pinterest.com/search/pins/?q=entryway%20bench%20morning%20light%20apartment) · light chocolate |
| S02 | "only bag I pack for a weekend trip" | From behind: woman in jeans and a loose white shirt walking down her hallway toward an open front door, bag in her right hand, rolling suitcase in her left, head fully out of frame, daylight flaring from the doorway | She keeps walking away at a relaxed pace, the bag swaying gently in her hand. Handheld follow with natural footstep bounce. | Pose [woman walking away carrying bag](https://www.pinterest.com/search/pins/?q=woman%20walking%20away%20carrying%20bag%20back%20view) · setting [hallway front door daylight](https://www.pinterest.com/search/pins/?q=apartment%20hallway%20front%20door%20daylight) · light chocolate |
| S03a | "one piece of leather that folds over the front" | Closed bag straight on at mattress height on a wrinkled white linen duvet, flap and turn lock reading clearly, an open paperback and a phone beside it | Slow handheld push in toward the bag with slight focus breathing. | Setting [linen bedding morning light](https://www.pinterest.com/search/pins/?q=linen%20bedding%20bedroom%20morning%20light) · light chocolate |
| S03b | Second half of the L3 cut | OPEN-BAG BLOCK. Same bed, slightly higher angle, the bag already open, one-piece flap leaning back behind the mouth, nothing inside yet. The hard cut from S03a proves the line | Slow push toward the open mouth. The flap stays folded back in one piece. | Same pin as S03a · open-bag + interior photos |
| S04 | "cognac leather, woven canvas, gold hardware, no logo" | Extreme close-up in raking window light where the cognac band meets the cream canvas: one gold clasp plate with the belt strap threaded through, tiny scratches and a fingerprint on the metal, plain unbranded leather around it | Extremely slow macro drift with shallow focus breathing. Omni mutates macro hardware: one re-roll on failure, then a slow push on the still in the edit. | Setting [handbag hardware macro raking light](https://www.pinterest.com/search/pins/?q=handbag%20hardware%20macro%20raking%20light) · light chocolate |
| S05 | "holds three days of clothes... overhead bin" | OPEN-BAG BLOCK. Two hands lowering a folded cream cable-knit sweater into the open bag on the bed, a packing pile of rolled jeans, a toiletry pouch and a paperback waiting beside it. The only zipper in the scene belongs to the pouch. Cut against a one-second re-entry of S02 for the travel half | Her hands press the sweater down gently and let go. Camera holds steady. | Pose [hands packing weekend bag](https://www.pinterest.com/search/pins/?q=hands%20packing%20weekend%20bag%20folded%20clothes) · open-bag + interior photos |
| S06a | "packed full... it keeps its shape" | Closed bag on the floor against a bedroom wall, visibly full, sides taut, low straight angle, a rolling suitcase and shoes beside it, evening lamp light from the right | Very slow sideways drift. The bag stays perfectly upright. | Setting [bedroom corner suitcase lamp light](https://www.pinterest.com/search/pins/?q=bedroom%20corner%20suitcase%20lamp%20light) · light chocolate |
| S06b | "...or nearly empty", second half of the cut | The identical corner, angle and lamp light, the bag nearly empty and holding the exact same upright silhouette. The hard cut carries the comparison | Same drift as S06a so the two clips cut as a match. | Same pin as S06a · light chocolate |
| S07 | "handles are rolled and reinforced" | Chest-down crop: the bag hanging in the crook of a woman's bare forearm at hip height on a sidewalk, linen trousers and sandals, street clutter softly blurred behind, face fully out of frame, no shoulder strap anywhere in the scene | She shifts her weight slightly and the bag moves with her arm in tiny natural motions. Soft handheld sway. | Pose [bag in crook of elbow street crop](https://www.pinterest.com/search/pins/?q=bag%20in%20crook%20of%20elbow%20street%20style%20crop) · light chocolate |
| S08 | "light chocolate and army green, one size, $159" | Closed army green bag upright on a car passenger seat, seat belt crossing behind it, golden light through the side glass, an iced coffee in the cup holder. Cut against a one-second re-entry of any clean light chocolate frame | Very slow drift across the seat with slight focus breathing. | Setting [bag on car passenger seat golden hour](https://www.pinterest.com/search/pins/?q=bag%20on%20car%20passenger%20seat%20golden%20hour) · army green |
| S09 | "both colors are on the site right now" | No new frame. Re-enter S01 as the last clean image and hold it under the price and CTA card | Reuse the S01 clip. | None |

---

## 6. Post / captions

- All on-screen text added in the edit, never generated, and no engine is ever asked to render the word "Weekender."
- Persistent lower third across the entire runtime, black on light, reference style: `THE ELEANOR WEEKENDER BY VELANTRA`
- Hook card over the first 2.5 seconds, five words or fewer: `ONE BAG. THREE DAYS.`
- Price and CTA card over line 9.
- Cadence: a new visual every 1 to 2.5 seconds, 24 to 28 cuts, the cut moving inside the first second. Re-enter setups rather than letting a shot sit; trim, never stretch.
- Audio: one continuous VO track, soft music bed well under the voice, light ambient under the b-roll.
- Spelling authority is the script in section 3. A typo in burned text is an auto-fail.
- Export: 1080 x 1920, H.264, MP4, AAC, 32 to 36 seconds.

## 7. QA before delivery

1. Photoreal check, regenerate on sight: uniform polished leather, clean even lighting with no blown highlights or noise, perfect centred framing, tack-sharp everywhere, spotless surfaces, a background that reads as a set. The 3D render look never ships, no matter how good the bag looks.
2. Product check, regenerate on sight: shoulder carry or any long strap · silver, chrome or mismatched hardware · a zipper · a logo or lettering on the bag · the flap split into pieces, or a flap-shaped panel on the front of an open bag · handles anchored into canvas · the leather-canvas split moving between shots · a missing front handle on an open bag · text rendered into the frame · a recognisable face.
3. Three variants per still were generated and the rejects are kept beside the pick.
4. Every clip checked at three frames, start, middle, end: engines grow hardware, sprout straps and engrave plates mid-motion. Use the clean seconds or reject the clip.
5. S06a vs S06b side by side: same corner, same light, same silhouette.
6. The bag is never opened, closed or fastened on camera anywhere in the cut.
7. Caption spell-check against the script; VO is one continuous track.
8. Runtime 32 to 36s, export spec exact, file naming exact.

## 8. Compliance rules

- Never state where the bag is made: not in VO, not in text, not implied by a visual.
- Never name or compare to another brand, in text or in the visuals.
- No claim on screen or in audio that is not in the locked script.
- No faces anywhere in frame, in any scene.
- One size, two colourways, $159.99: nothing in the ad may suggest otherwise.
