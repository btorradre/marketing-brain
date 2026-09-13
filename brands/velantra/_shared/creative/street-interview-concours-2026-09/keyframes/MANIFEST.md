# Keyframe manifest, VEL-STREET-CONCOURS-01 (2026-09-02)
Engine: GPT Image 2 on Higgsfield (gpt_image_2, 9:16, 1k, high). Scene seed = a full-res frame from the reference reel (place/light/grain only, woman explicitly not copied). Product seed = real product photo. 3 variants per frame, picks in picks/.

| Pick | Source variant | Scene seed | Product seeds |
|---|---|---|---|
| W1-WEEKENDER-K1-start | W1-K1-v3 (v1 failed QA: crest on plate, horsebit loafers) | ref_t4 | wk-closed |
| W1-WEEKENDER-K2-lift | W1-K2-v2 | ref_t15 | wk-closed + wk-macro |
| W1-WEEKENDER-K3-arm | W1-K3-r1 (re-roll anchored on the K2 pick; v1-v3 failed QA: flap ears elongated, staples on the ears) | ref_t31 | wk-closed + wk-macro |
| W2-MERIDIAN-K1-start | W2-K1-v1 | ref_t40 | meridian-brown-1 |
| W2-MERIDIAN-K2-lift | W2-K2-v3 | ref_t15 | meridian-brown-1 |
| W2-MERIDIAN-K3-rings | W2-K3-r3 (re-roll; v2 failed QA: black strip inside the handle) | ref_t31 | meridian-brown-1 |
| W3-VIVIENNE-K1-start | W3-K1-v2 | ref_t8 | viv-bag + viv-hardware |
| W3-VIVIENNE-K2-lift | W3-K2-r1 (re-roll seeded on K2-v1 + K1 pick; v2 failed QA: different woman, oval on the band) | ref_t15 | viv-bag + viv-hardware |
| W3-VIVIENNE-K3-watch | W3-K3-r1 (re-roll seeded on K2-v1; v2 failed QA: empty handle holes, diagonal straps) | ref_t31 | viv-bag + viv-hardware |

Rejected on sight: W2-K1-v3 (letter-like mark on the turn-lock), W1-K3-v2 (stray dark croc object bottom-left), W1-K3-v3 (blue jeans, continuity), W3-K1-v3 (bag cropped by the frame edge), W3-K2-v3 (too structured), W3-K3-v1 (square plate, flap state wrong), W3-K3-v3 (staple and strap geometry off).

## Seedance 2.5 passes (Higgsfield, 2026-09-02 late)
Model `seedance_2_5`, mode omni_reference, start_image = the K1 pick, audio_references = a 4s ElevenLabs pronunciation line ("This is the X from Velantra"), duration 26, 720p, 9:16, native audio. 169cr per pass.
Gotcha: Higgsfield refuses the submission and "recommends a preset" whenever the prompt contains render-y negatives ("3D render", "CGI"). Strip those words and pass `declined_preset_id` for whatever it recommends next ("IN THE DARK" the second time). Third submission went through.
Pronunciation refs: W1 Woman Over 55 (FZmr35ewm9E7gnProxwf), W2 Woman Aged 40-65 (SkQqPDmEiASWjGhFSNZ3), W3 velantra-zede-v5-blonde (cNPPZjuwhkbvKJLwd0e3). Files in vo/.

## FINAL CUTS (2026-09-02 late)
- final/VEL-STREET-CONCOURS-01-W1-WEEKENDER.mp4  25.8s  = Seedance take 2 (0-19.6s) + take 1's last beat (19.95s to end), spliced at the scripted jump cut because take 2 grew a phone in the bottom of the final beat. Take 1 had "Birkin" as "Burly"; take 2 fixed it with the word in the pronunciation reference.
- final/VEL-STREET-CONCOURS-01-W2-MERIDIAN.mp4   26.0s  = take 1, clean on both checks.
- final/VEL-STREET-CONCOURS-01-W3-VIVIENNE.mp4   26.0s  = take 2 (take 1 said "Banky" for Birkin and "Carrier" for Cartier; the v2 reference with all four names fixed both).
- final/VEL-STREET-CONCOURS-01-MONTAGE-78s.mp4   77.9s  = hard-cut concat W1 > W2 > W3.
Post: post/build.py (Georgia serif cards top 7%, Helvetica Neue captions at 80% with black halo, phrases max 4 words split at pauses and sentence ends, caption text aligned to the SCRIPT via difflib over whisper word timings so brand spellings are exact). Raw takes and word JSONs in seedance/. QA sheets in post/qa/.
Pronunciation QA: whisper-1 word-level for timings + Gemini 2.5 Flash audio for phonetics (curl, not urllib). Whisper spells the brand "Volantra" even when Gemini confirms vel-AN-truh, so whisper alone cannot judge the brand name.

## v2 FINAL CUTS (2026-09-02, after Brooks's copy note: complete sentences, collection page, offer after)
- final/VEL-STREET-CONCOURS-01-MONTAGE-93s.mp4  93.1s = W1 (30s) > W2 (30s) > W3 (30s) > 3s offer end card ("Every bag in this video is on sale right now. Link below.")
- final/VEL-STREET-CONCOURS-01-W1-WEEKENDER.mp4 / W2-MERIDIAN / W3-VIVIENNE  33.0s each = 30s take + the same end card, so each runs alone.
- Takes: seedance/W1.mp4 (v2, clean), seedance/W2.mp4 (v2 with "Velantra" spliced in from her v1 take at 5.74-6.48s; raw at W2-v2-raw.mp4), seedance/W3.mp4 (v2 with "Birkin" spliced in from her v1 take-2 at 7.92-8.52s; raw at W3-v2-raw.mp4). v1 26s cuts archived in final/v1-26s and seedance/v1-26s.
- Word-swap recipe: whisper word timings on the full file drift ~0.5s; cut a 3.5s window around the rough time and re-run whisper on the clip (with a prompt) to get the real boundaries, then atrim/acrossfade 30ms both sides, video stream copied. Gemini rated both splices 10/10 natural. Only works because donor and target are the same woman from the same start frame.

## v3 (2026-09-03) Brooks's review of v2: restoryboard
Misses: bag scale wrong on all three (true dims: Weekender 18x14.5x7 in; Meridian 14.6x9.4x5.9 in / 37x24x15 cm; Vivienne 38x27x20 cm); W1 "Veronica Beer", "hat has no brand" (should be "label"), cuff named but not shown, Rolex upside down; W2 "no logo" while a Velantra label showed inside the tote, "Janessa Leorne", "Aquazilla", rings not David Yurman and grandmother's ring identical to the others; W3 straps wrong on the bag, "knit is Vince" while pointing at trousers, Cartier upside down. Framing: whole body in every shot, camera tilts down to the bag during the review.
v3 keyframes in keyframes/v3/: K1 full-body start seeded on the v2 K1 pick (identity + place) + product photo, with body-relative scale anchors from the true dims, jewelry specs and watch orientation pinned. K2 (full body, bag lifted) and K3 (full body, wrist raised) seed on the approved v3 K1.

### v3 render-ready IDs (Higgsfield media_ids, for the Seedance step after board approval)
- W1 start_image = keyframes/v3/picks/W1-WEEKENDER-K1-full.png -> 889a57b5-4a34-457a-bf96-52ebb4de9f5c ; audio ref vo/W1-pron-ref-v3.mp3 -> 880f71a4-4e4a-4d89-a82d-98a0b90dd276
- W2 start_image = keyframes/v3/picks/W2-MERIDIAN-K1-full.png -> fd59609b-a818-4ddd-a97a-9a578a0de851 ; audio ref vo/W2-pron-ref-v3.mp3 -> 7117903e-2b47-43ff-91a1-a95307bf1c38
- W3 start_image = keyframes/v3/picks/W3-VIVIENNE-K1-full.png (= W3-K1-r2, re-roll after QA: straps + size) -> see import below ; audio ref vo/W3-pron-ref-v3.mp3 -> f454aa5b-47fa-48bb-b111-10e0e5100540
- All refs verified by Gemini per name (Aquazzura only landed when spelled "Aqua Zoo Ra" in the ElevenLabs script).
- Higgsfield balance after v3 keyframes: ~420cr. Each 30s Seedance 2.5 pass is ~195cr, so two passes fit; the third needs a ~200cr top-up (or run it at 26s / 169cr).

### v3 QA outcome (three fresh-context auditors)
- W1: K1-v1 PASS, K2-v1 PASS, K3 swapped to v1 (v2 fused the cuff and watch into one cuff-watch; v3 had no cuff). Prop lesson: spell the cuff and the watch as TWO separate objects with skin between them.
- W2: K1 swapped to v3 and K3 swapped to v3 (v1 picks rendered background through the open top where the back wall should be; v1 K3 rings were plain bands with no heirloom). K2-v2 PASS (a stray wire loop under the turn-lock, cosmetic). Lesson: "the tote is opaque; a band of lining shows between front and back rim across the whole width".
- W3: K1 re-rolled seeded on the passing K2 (all three first variants ran the straps horizontally through the staples, Birkin-style, and oversized the bag); r2 passes. K2-v2 PASS (best hardware in the run), K3-v1 PASS (bag ~25% large; acceptable on a board frame).
### v3 FINAL render IDs (post-QA picks; use these for the Seedance step)
- W1 start = W1-WEEKENDER-K1-full.png (W1-K1-v1) -> 889a57b5-4a34-457a-bf96-52ebb4de9f5c ; audio 880f71a4-4e4a-4d89-a82d-98a0b90dd276
- W2 start = W2-MERIDIAN-K1-full.png (W2-K1-v3) -> e926f616-657d-4a05-8d45-501e7632ca27 ; audio 7117903e-2b47-43ff-91a1-a95307bf1c38
- W3 start = W3-VIVIENNE-K1-full.png (W3-K1-m3, seeded on the MASTER product image; straps through the staple falling to the middle, handles upright) -> aaaae5e3-7e4e-4279-ad0c-df30749217a5 ; audio f454aa5b-47fa-48bb-b111-10e0e5100540
- Vivienne strap re-roll 9/03: K1 s3, K2 s1, K3 s1 (from W3-K*-s1..s3), each seeded on its own previous pick + hardware macro with the strap ruling spelled out. Straps thread down through the staple and the tails drape inward toward the centre.

## v3 SEEDANCE (2026-09-03/04)
- W3 Vivienne: Higgsfield job f0ec8c04, 30s, from the master-seeded start frame. Visual PASS (full body every beat, tilt-down review, straps through staples, handles up). Audio: brand came out "Volant Antra" plus stutter repeats "Manolo Manolo" / "Cartier Cartier". Fixed by splicing "Velantra" from v1-26s/W3.mp4 (Gemini-verified vel-AN-tra) into the raw at 5.58-6.32 and cutting the repeat spans (video and audio, 18.68-19.22 and 20.08-20.38). Gemini: one continuous natural take, 9/9/7. Raw kept as seedance/W3-v3-raw.mp4; final at final/v3/VEL-STREET-CONCOURS-01-W3-VIVIENNE-v3.mp4 (29.2s + 3s end card).
- W1 / W2: NOT RENDERED. Higgsfield 324cr covered one 30s pass (~195); kie 1,352cr cannot cover a 30s pass (1,890) or 26s (1,638). Needs ~400cr Higgsfield top-up for both, then fire with the v3 prompt deltas in the brief (start frames 889a57b5 / e926f616, audio 880f71a4 / 7117903e).
- Lesson: isolated single words in the pronunciation reference ("Manolo. Cartier.") make Seedance echo the word twice in the take. Next reference = full natural sentences containing the names, never a bare word list.

## v3 MONTAGE RE-EDIT (2026-09-04)
- W1 Weekender: Higgsfield job 9390aca6 (30s). All names correct natively, no repeats. Used as-is.
- W2 Meridian: five 30s passes rolled (798bbf6d raw, f844f7fc = take A, 9b30517a = take B, 0e9817d3 = take C with substitute hat/shoe names). Seedance could not say "Velantra" correctly on any W2 pass (Volanta / Valanta / vuh-LAN-tuh); Leone and Aquazzura came right only on take A. Final = take A + ONE dubbed word: "Velantra" from an ElevenLabs IVC clone of her own take (voice velantra-concours-meridian-diane, b8baTBNNQ8k2CWypDbNU), level-matched, ambience-bedded, NO tone filtering (a lowpass at 7.5k made the T read as D). Gemini: vel-AN-tra, clear T, 10/10 natural, one continuous take. Raw takes kept as seedance/W2-v3-{raw,A,B,C}.mp4.
- W3 Vivienne: job f0ec8c04 + brand word from her v1 take + two stutter cuts (see above).
- Finals: final/VEL-STREET-CONCOURS-01-MONTAGE-93s.mp4 (92.3s = 3 x 30s + 3s offer card), W1/W2/W3 solos 33s each with the card.
- Lessons: (1) single-word dubs from an IVC clone of the same take pass at 10/10 when level-matched with the take's own ambience under them and no EQ; phrase-length dubs and any reverb/EQ read as edits. (2) Seedance says "Velantra" right in roughly 1 of 3 takes per woman; budget for it. (3) Bare-word pronunciation references cause echoes; full sentences do not.
