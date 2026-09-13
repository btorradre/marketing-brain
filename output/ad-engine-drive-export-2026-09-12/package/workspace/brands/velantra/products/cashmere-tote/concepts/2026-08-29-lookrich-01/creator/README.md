# VEL-COLETTE-LOOKRICH-01 · Talking-head greenscreen creator

Generated 2026-08-29 · Nano Banana Pro image-to-image · 1536×2752 (9:16) · 4 candidates, 1 pick.

## Identity

Anchored on **Dana**, the established Colette creator (`_identity-anchor-Dana.jpg`, from the 8/16 linear-story run). No new casting for this product. The anchor supplied face, bone structure, skin tone and hair colour only; everything else (wardrobe, mic, lighting, green) came from the prompt.

## Wardrobe and prop, mirrored from the reference

White ribbed cotton tank, thin gold chain, small gold hoops, hair pulled back into a low loose bun with strands at the temples, and a **small black handheld content mic with a grey furry windscreen held up near the chin**. The mic is the format signature. It is what makes the ad read as a creator recording a voiceover rather than a commercial.

## Candidates

| File | Verdict | Notes |
|---|---|---|
| **`v1-white-a.png`** | **PICK** | Chest-up with headroom, eyes straight to lens, mouth open mid-sentence, mic at chin in the right hand. Best framing for a quarter-frame cutout. Identity match is clean. Skin reads real: pores, fine lines, a little forehead shine. |
| `v4-oatmeal.png` | ALTERNATE | Same framing, oatmeal ribbed tank instead of white. **Flattest green of the four** (G stdev 10.0) and the warm garment is the safer despill. Mic sits lower, at the chest rather than the chin, so it loses a little of the reference's grammar. Use this one if the white tank keys pink. |
| `v2-white-b.png` | HOLD | Too tight. Face fills the frame, so there is not enough body left for a small cutout, and the eyes drift camera-right. |
| `v3-white-c.png` | REJECT | Eyes off-lens, a second hand enters bottom-centre with broken anatomy, and the green carries a visible gradient in the upper left. |

## Key notes

Background measurements, sampled off-subject:

| File | Mean RGB | Green stdev |
|---|---|---|
| v1 | 38, 158, 84 | 23.5 |
| v2 | 25, 164, 78 | 27.1 |
| v3 | 25, 126, 68 | 20.4 |
| v4 | 39, 130, 72 | 10.0 |

All four are keyable, but none is a perfectly flat plate. **Key with a tolerance, not a single-colour hard key**, and pull the matte before judging the edge.

**Despill stays low.** At 0.5 a neutral garment against green renders pink, and v1 is a white tank. Check the tank in pixels, not on the read.

## Next step, gated

This is SOP step 2 of 4. Step 3 is animating the approved still on the finished VO track in HeyGen, and the VO does not exist yet. Per the storyboard-first law the still gets approved before anything renders, so: pick v1 or v4, then the order is VO (voice `NBIPq5xdnIg9kaBH5Ape` "Woman Over 40", respelled `Vell-Ahn-Trah`, STT gate, tighten, normalize to -14 LUFS) → HeyGen animation → key → comp per the shot map in `../2026-08-29-VEL-COLETTE-LOOKRICH-01.md`.
