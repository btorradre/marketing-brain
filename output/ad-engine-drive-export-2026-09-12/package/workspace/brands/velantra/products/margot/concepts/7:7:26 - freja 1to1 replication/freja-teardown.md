# Freja New York → Velantra Meridian — 1:1 Replication Pack (2026-07-07)

Three scaling Freja NYC ads (217 live ads, 1.83M total reach) torn down frame by frame and replicated 1:1 for the **Velantra Meridian**. Freja = same positioning lane as Velantra (NYC quiet-luxury leather bags, anti-logo) so beats transfer with zero adaptation, only product + wordmark swaps.

Reference videos archived in `refs/`. Ad Library links:
- Ad 1 Paloma: https://www.facebook.com/ads/library/?view_all_page_id=384196329160725&id=1519528139646128
- Ad 2 Sylvie: https://www.facebook.com/ads/library/?view_all_page_id=384196329160725&id=997595719920231
- Ad 3 Caroline: https://www.facebook.com/ads/library/?view_all_page_id=384196329160725&id=1319820196990956

---

## Ad 1 — Paloma Tote "work bag stills" (4s, 720x1280, active, launched Jul 3)

**Format:** 4 photos from ONE café photoshoot, hard cut every 1.0s (cuts at exactly 1s/2s/3s). Camera-roll realism, zero motion. Static caption persists all 4s, top-center, small white sans-serif, two lines: `A work bag designed` / `for more than the office.`
Body copy: "Meet the Paloma Tote, our bestselling work bag for the life you're building." CTA SHOP NOW → collection page.

| Still | Beat |
|---|---|
| 1 (0–1s) | High angle down at black tote OPEN on dark wood café window counter. Woman's hands (rings, bracelet, watch) hold iPhone above interior pocket. Two lattes w/ art + spoons foreground. Street through glass behind. |
| 2 (1–2s) | Same scene ~identical angle, phone sliding INTO interior slip pocket. Micro angle change (feels like next camera-roll shot). |
| 3 (2–3s) | Slightly wider/further back, hand reaching into open bag, laptop edge visible inside, more window + street visible. |
| 4 (3–4s) | No hands. Bag styled OPEN showing laptop + slim wallet inside, both coffees repositioned foreground. Product-as-still-life close. |

**Psychology:** photo-dump native format = zero ad-scent; "more than the office" reframes work bag → life bag; interior organization is the silent demo (phone pocket, laptop). Caption does all the selling.

**Replication (VEL-MERIDIAN-FREJA-01):** GPT Image 2 pure i2i from `black 1.webp` + `black 5.webp` canonical refs, 4 stills, café windowsill scene. **Product truth override: Meridian interior is DARK CHARCOAL (not Paloma tan); silver belt-lock hardware + twin rolled handles must survive every still.** Caption identical (generic, no Freja language). Stitch 4×1s @ 720x1280 + ffmpeg drawtext caption. Music added at upload.

## Ad 2 — Sylvie "closer look" POV close-up (10.7s, 720x900 4:5, active, launched Jul 3)

**Format:** one continuous handheld studio close-up (single soft cut at 1.8s). Model = torso only (white boxy tee, black skirt), face never in frame, behind grey concrete plinth, warm white wall. Bag fills frame the whole time. Static caption bottom-center small white sans: `A closer look at the Sylvie`. At ~8s a thin serif white `FREJA` wordmark fades in centered over the bag.
Body copy: "The bag we keep coming back to, Sylvie. Back in stock now."

Beat map: 0–2s bag held to camera by handles, gentle sway → 2–3.5s side profile set on plinth, straps arc → 3.5–5.5s hands open top wide, interior + slip pocket shown → 5.5–7s tilt toward lens holding interior visible → 7–8s grip handles, bag stood upright → 8–10.7s lifted to shoulder, clean silhouette, wordmark on.

**Psychology:** pure product-porn retargeting unit; "closer look" = PDP-in-a-video; facelessness keeps 100% attention on leather/hardware; wordmark late = brand stamp after desire.

**Replication (VEL-MERIDIAN-FREJA-02):** Seedance 2.0, ONE 11s segment, 3:4 (closest supported to 4:5), refs `black 1` + `black 5`. **On-screen text generated natively by Seedance** (per Brooks): caption `A closer look at the Meridian` full-length + `VELANTRA` serif wordmark from 8s. Interior shown = dark charcoal.

## Ad 3 — Caroline "1 bag 3 looks" outfit-switch (11s, 720x1280, wound down Jul 2 — fresh test)

**Format:** static-camera white-studio lookbook. Same model, burgundy shoulder bag constant, THREE all-black outfits, cuts on motion (~3.7s, ~7.3s). Persistent centered white sans text `1 bag 3 looks` + persistent bottom `FREJA` letterspaced wordmark. Model poses/adjusts hair/turns; hair-toss motion masks the outfit cuts.
Body copy: "The Caroline Bag completes any look." CTA LEARN MORE → PDP.

| Look | Outfit | Action |
|---|---|---|
| 1 (0–3.7s) | Black oversized crewneck sweater + chocolate leather midi skirt | adjusts hair, bag on arm |
| 2 (3.7–7.3s) | Black structured cinched-waist jacket + black trousers | hand on hip, chin up, editorial |
| 3 (7.3–11s) | Black oversized sweater + black mini skirt, bare legs | turns to camera, hair toss |

**Psychology:** versatility proof = cost-per-wear math done visually; all-black styling makes the burgundy bag the only color in frame; "completes any look" = the bag is the outfit.

**Replication (VEL-MERIDIAN-FREJA-03):** Seedance 2.0, 3 segments × 4s, 9:16, refs = Sloane (`@Image1`, identity lock) + `burgundy 1.webp` (`@Image2`). Native text both lines (`1 bag 3 looks` + `VELANTRA`) in every segment so the overlay survives the stitch. Bag carried by top handles (product truth: Meridian is a handle-carry tote). Stitch → final.

---

## Production ledger (run of 2026-07-07)
- Engine: kie.ai Seedance 2.0 (`bytedance/seedance-2`) via `velantra-ugc/scripts/kie_seedance.py`, GPT Image 2 (Higgsfield MCP) for the 4 stills (product i2i doctrine)
- Voice anchor: off (no dialogue, music-driven formats; trending audio added at upload)
- **Ad 1** ✅ 4 GPT Image 2 i2i stills (jobs a3be9738/26c7dce1/e2d8717f/2e238ada) + Pillow caption PNG + ffmpeg stitch (this machine's default ffmpeg has NO drawtext — use caption.png overlay). Final: `VEL-MERIDIAN-FREJA-01/final.mp4` → `video/VEL-MERIDIAN-FREJA-01-workbag-stills.mp4`
- **Ad 2** ✅ one 11s 3:4 Seedance task (kie task bcda744b…) — 3:4 aspect accepted, native on-screen text worked: caption renders 0–2s center frame (reference had it persistent bottom — acceptable deviation), VELANTRA serif wordmark 7s→end exactly like reference. Product fidelity strong incl. detachable shoulder strap (real Meridian feature). Final → `video/VEL-MERIDIAN-FREJA-02-closer-look.mp4`
- **Ad 3** ✅ 3×4s 9:16 segments (Sloane @Image1 + burgundy 1 @Image2), 164cr each = 492cr, stitched to 12.3s. All 3 looks + Sloane identity held; both text lines rendered in every segment (note: Seedance native text font drifts slightly between segments — if pixel-identical type matters, strip and re-overlay in post). Final → `video/VEL-MERIDIAN-FREJA-03-1bag3looks.mp4`
- kie balance read 2,761 after Ad 2 (top-up landed mid-run; started 1,581)
- Music: none baked in — add trending audio at upload for all three
