# VEL-ELEANOR-ASKME25 — Seedance 2.5 single-pass ads

## ✅ SHIP: `final/VEL-ELEANOR-ASKME25-05-FINAL.mp4` — 13.04s

Hybrid build. Two Seedance shots that passed frame-QA + one shot rebuilt as a locked i2i still with a
Ken Burns push, with the ElevenLabs VO laid over the whole thing as one continuous track.

| Shot | Source | Status |
|---|---|---|
| 1 (0-3.96s) she holds the bag, talking | Seedance 2.5 | Passed QA clean, zero morphing across 8 sampled frames |
| 2 (3.96-8.71s) bag alone, hardware macro | **GPT Image 2 i2i still + Ken Burns** | Rebuilt. Failed on Seedance twice |
| 3 (8.71-13.04s) macro, hand resting | Seedance 2.5 | Passed. One non-blocking defect below |

**Pronunciation is fixed.** Both "Velantra" and "Weekender" now read correctly and sound natural,
verified by word-level transcription of the finished file. The fix was to stop letting Seedance
synthesize speech at all: the VO is generated in ElevenLabs (`eleven_v3`, Creative, stability 0.0,
similarity 0.85 — three takes, take 3 picked) and fed in as `reference_audio_urls`. Writing the name
phonetically as `WEEK-ender` also worked but sounded forced, which is why it was dropped.

**Known non-blocking defect:** in shot 3 the right clasp plate renders a dull olive-brass rather than
warm gold (measured left RGB 179,151,117 vs right 127,103,78 with brighter surrounding canvas, so it
is the plate and not the light). It is static, not drifting. Editor fix: tracked warm tint.

**Not in this cut:** the closing CTA line ("It's that structured shape, and it fits the overhead bin.
Linked below.") was trimmed to fit the credit budget. The full VO with it is in `vo/vo_take3.mp3`;
extending to ~17s needs one more Seedance shot.

### The law this run produced (now in the skill)
Three adversarial audits converged on it, and the third corrected the second:
**the gate is the FIRST FRAME and how large/well-lit the hardware is — not motion.** v4's shot 2 was
the most static shot in the ad (bounding box measured locked-off, no people, no hands) and failed
worst, with the plates already deformed in frame one. Shots where the hardware is large, sharp and
high-contrast held perfectly. Corollary that would have saved two failed runs:
**a shot with no person in it should never go to Seedance at all** — it gains nothing and risks
everything. Build it as an i2i still.

## ❌ v3 FAILED FRAME-QA (audit: `qa3/`)

v3 closed the bag in all five shots, fixed scale, and fixed the "Weekender" pronunciation. It still
failed 3 of 5 shots — and the two audits together produced **the finding that matters**:

> **Motion destroys the front hardware, not just the flap.** Shots where the bag is held STILL and
> front-on with no hand contact (shots 1 and 4) passed clean on every criterion. Every shot where
> hands touch the bag or the camera moves around it (2, 3, 5) produced invented or destroyed hardware:
> a clasp plate vanishing entirely, both plates elongating into gold spears, **both rolled handles
> disappearing**, an invented arched saddle under the turn lock, an orange grafted panel, a U-shaped
> grab loop, a seam splitting the canvas, long dangling straps.

The keyframes were all correct. i2i holds this bag perfectly. Only the motion breaks it.

**Production doctrine that follows (now written into the skill):**
- Seedance gets: talking-head beats, bag held still and front-on, hand resting motionless.
- GPT Image 2 i2i stills + Ken Burns get: any handling, lifting, carrying, or camera arc.

Pronunciation status: `WEEK-ender` phonetic spelling **worked** — the product name now reads correctly.
The brand name still comes back "Volanta", so it needs the same phonetic treatment (`Vel-AN-tra`).

Usable from v3: shot 1 (0-5.4s) and shot 4 (14.8-19.6s), roughly 10 of the 25 seconds.

## ❌ v2 FAILED FRAME-QA. DO NOT SHIP.

Full audit in `qa2/frames/` (open-bag segment sampled at 4fps). Verdict FAIL, 9 defects.

**Blocking, open-bag packing shot (5-10s):** the fold-back flap degrades to a plain featureless slab
with zero fittings by `pack_11` and stays that way; the turn lock morphs through three geometries by
`pack_06`; the front handle stretches into an invented long dangling strap from `pack_07`; the
leather/canvas split goes diagonal and collapses on the left. **The keyframe was correct — Seedance
destroyed it in five seconds of motion.**

**Blocking, door-exit shot (20-25s):** invented hardware — the right clasp plate becomes an angled
gold spear-bar with its belt strap gone, a U-shaped leather grab loop appears on the front-right that
is not on the reference, the right gusset splits open, and an extra gold post sits below the two-tone
split line.

**Non-blocking:** both clasp plates render pale champagne rather than warm brass in the opening shot
(editor warm-tint territory). Product name pronounced "Weekener", D dropped.

Clean shots: 10-15s and 15-20s pass fully.

### The fix
1. Packing shot comes OUT of the Seedance pass. Build it as locked GPT Image 2 i2i stills, hard-cut or
   Ken Burns. Never hand an open bag to Seedance — now re-confirmed on 2.5 even with a validated keyframe.
2. Door-exit shot is closed-bag, so a Seedance re-roll is legitimate. Three variants, then pick.
3. Write the product name phonetically in the dialogue (`WEEK-ender`), and re-transcribe with
   **word-level** STT to verify.

## Superseded pick: `final/VEL-ELEANOR-ASKME25-02.mp4` (v2)

v2 fixes two things Brooks caught on v1: **the bag rendered far too small**, and **shot 2 is now the
packing scene**. She also names the product on camera.

**The scale fix is the transferable lesson.** v1 gave no scale anchor, so the model defaulted to
handbag proportions. v2 states the real dimensions AND a per-shot relational check:

> SCALE IS CRITICAL. This is a LARGE TRAVEL BAG, 18 inches wide by 14.5 inches tall by 7 inches deep,
> big enough to pack two to three days of clothes. It is NOT a handbag, NOT a purse, NOT a medium
> tote. Roughly the size of a carry-on duffel. Render it noticeably oversized rather than too small.

plus, per shot, e.g. *"the bag is WIDER THAN HER TORSO and its top edge reaches her collarbone"* /
*"as WIDE AS HER SHOULDERS"* / *"hanging at her side it reaches from her hip toward her knee"*.
Dimensions alone are not enough; the relational check against the body is what actually lands.

v2 cuts: requested 5/10/15/20, landed **5.08 / 9.83 / 14.83 / 19.71**.

⚠️ **Open item:** two ElevenLabs transcription passes disagree on the brand name at 3.58-4.22s. The
full-text pass heard "Volantra", the word-level pass heard "Velantra". Needs one listen to settle. If
it is wrong, write it phonetically in the dialogue line rather than re-rolling blind.

⚠️ **Angle note:** Brooks wants the Birkin-inspired travel-bag angle. Per the standing product rule
the word "Birkin" can never appear in a generation prompt or in customer-facing copy, so the angle is
carried by the silhouette itself plus the line "it's that structured shape".

---

## v1 (superseded) — first Seedance 2.5 single-pass ad

**Shipped 2026-08-07.** Swipe: Vestirsi "ask me a question" review (`_shared/swipes/2026-08-07-batch/01-vestirsi-iDgwls.mp4`).
Product: The Eleanor Weekender, Light Chocolate. Creator: C3.

`final/VEL-ELEANOR-ASKME25-01.mp4` — 25.06s, 720x1280, 24fps, native audio. **One generation. No stitching.**

## The workflow that worked (keyframe mode)

1. Generate one still per scene with **GPT Image 2 i2i** on kie (`gpt-image-2-image-to-image`), each
   anchored on the creator selfie + the closed-bag hero, carrying the identity block, the
   reference-anchoring preamble and the photoreal footer. **10 credits per image.**
2. Upload all five stills. They become `@Image1..@Image5` in upload order.
3. Open the prompt with `Use @Image1 through @Image5 in order as the keyframes for the five shots below.`
4. Give Seedance 2.5 the full module stack plus a timestamped timeline, one shot per keyframe.
5. Pass the cloned voice as `reference_audio_urls`.

## Verified results

| Check | Result |
|---|---|
| Runtime | 25.06s against 25 requested |
| Cuts | 4 requested at 5/9/14/19s, landed at **5.00 / 8.92 / 14.08 / 19.38** |
| Dialogue | Transcribed back **word-for-word exact**, all five lines |
| Voice | Cloned from the swipe creator via `reference_audio_urls` |
| Identity | Holds across all five shots, no drift |
| Product truth | Two-tone body, gold turn lock, both clasp plates gold (no silver drift), key bell, corner patches, closed throughout, hand/forearm carry |
| Photoreal | Real rooms, real light, no render look |
| On-screen text | None (post overlay, since Seedance cannot spell "Weekender") |

## Costs

Five keyframes 50cr + one 25s generation 1575cr = **1,625 credits (~$6.50)** for a finished ad.

## Engine facts learned

- `reference_audio_urls` **is supported** on `bytedance/seedance-2-5` via kie.
- Audio references must be **2 to 30 seconds**. A 29.977s file was rejected; trim to 29s.
- Failed createTask is not charged.

## Still to do

Caption overlay in post: "Give me a full review of the Eleanor Weekender" sticker on shot 1,
Pillow PNG + ffmpeg (this machine's ffmpeg has no drawtext).
