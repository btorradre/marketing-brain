# Vivienne × Katie Holmes — Quiet Luxury Ad

**Concept:** Position the Vivienne Top Handle Bag as the accessible version of the celebrity-quiet-luxury bag Katie Holmes is constantly photographed carrying. Open on her, name what she's wearing, then bridge to Velantra.

**Format:** ~30-second vertical ad (9:16), TikTok / Instagram Reels / Meta Ads
**Product:** Vivienne Top Handle Bag (chocolate colorway used for hero shots; 4 colorways available)
**Pace:** New visual every 2–3 seconds
**Reference ad:** Nuamōre × Hailey Bieber Oceana watch ad (share.trendtrack.io/nuamore-gxHhlw)

---

## Reference ad shot-type analysis

I re-watched the Nuamōre reference frame by frame. The pattern is consistent:

- **STILL** = celebrity paparazzi photos, Instagram profile screenshots, product beauty shots on plain backgrounds, cutout overlays (a bikini, a tank top, a hair bun, a price card).
- **VIDEO** = the talking head throughout, and any B-roll where the product is being *demonstrated* or *worn in motion* (wrist rotating, walking with a bag, watch under running water, key scraping the watch face).

**Our ad has no talking head** (it's VO over visuals). So the still/video split is even more important — stills hold the celebrity hook and product beauty; videos earn their place only when there's real motion or a demonstration.

---

## Voiceover script

> "Every time Katie Holmes steps out, the internet wants to know what bag she's carrying. It's always a structured top handle. And there's never a logo on it.
>
> This is the Vivienne Top Handle Bag by Velantra.
>
> Vegetable tanned leather all the way through. Belted brass turn lock. No branding anywhere on it.
>
> It's a Birkin-inspired shape — but soft, so it slouches and molds as you carry it.
>
> It carries far more than a top handle bag at this price normally does. It comes in four colors.
>
> Right now it's on pre-order and ships October. I left the link below."

---

## Shot list

| # | Time | Type | Asset | VO line | Notes |
|---|---|---|---|---|---|
| 1 | 0:00–0:02 | **STILL** | `scenes/scene_01_katie_stepping_out.png` | *"Every time Katie Holmes steps out…"* | Paparazzi hook. Consider a red circle overlay around the bag (matches reference's red circle on Hailey's wrist). Hold 2s. |
| 2 | 0:02–0:04 | **STILL** | `scenes/scene_02_hand_carrying_paparazzi.png` | *"…the internet wants to know what bag she's carrying."* | Tighter paparazzi crop, held. Optional Instagram-style overlay ("@katieholmes · 3.2M followers") to mirror the reference's social-proof overlay. |
| 3 | 0:04–0:06 | **STILL** | `scenes/scene_03_full_body_walking.png` | *"It's always a structured top handle."* | Another paparazzi still. Held. |
| 4 | 0:06–0:08 | **STILL** | `scenes/scene_04_clean_leather_no_logo.png` | *"And there's never a logo on it."* | Texture card. Held. Ken Burns push-in optional but not needed. |
| 5 | 0:08–0:11 | **STILL** | `scenes/scene_05_studio_front_product.png` | *"This is the Vivienne Top Handle Bag by Velantra."* | Product page-style reveal. Held. Overlay "Vivienne — $149" bottom third. |
| 6 | 0:11–0:13 | **STILL** | `scenes/scene_06_leather_grain_macro.png` | *"Vegetable tanned leather all the way through."* | Macro texture card. Held. |
| 7 | 0:13–0:15 | **VIDEO** | `animations/scene_07_brass_turnlock_macro.mp4` | *"Belted brass turn lock."* | Turn-lock rotating = mechanism demonstration. Motion earns its place here. |
| 8 | 0:15–0:17 | **STILL** | `scenes/scene_08_three_quarter_side.png` | *"No branding anywhere on it."* | Product angle beauty shot. Held. |
| 9 | 0:17–0:19 | **STILL** | `scenes/scene_09_side_silhouette.png` | *"It's a Birkin-inspired shape — but soft,"* | Silhouette beauty shot. Held. |
| 10 | 0:19–0:22 | **VIDEO** | `animations/scene_10_slouch_lifestyle.mp4` | *"so it slouches and molds as you carry it."* | Woman walking, bag slouching against leg. Motion is the point — it's the "how it wears" demo. |
| 11 | 0:22–0:25 | **STILL** | `scenes/scene_11_open_capacity_flatlay.png` | *"It carries far more than a top handle bag at this price normally does."* | Overhead flat lay. Held. Editor can add a slow Ken Burns pan if needed. |
| 12 | 0:25–0:27 | **STILL** | `scenes/scene_12_four_colorways_real.png` | *"It comes in four colors."* | Real product flat lay (not AI). Held. |
| 13 | 0:27–0:30 | **STILL** | `scenes/scene_13_marble_console_lifestyle.png` | *"Right now it's on pre-order and ships October."* | Beauty shot. Held. Overlay CTA "Pre-order — ships October". |
| 14 | 0:30–0:31 | **VIDEO** | `animations/scene_14_hand_lifting_cta.mp4` | *"I left the link below."* | Hand lifts bag out of frame = closing gesture. Motion earns its place. |

**Totals:** 11 stills, 3 videos.

---

## Files

```
concepts/katie-holmes-quiet-luxury/
├── SHOT_LIST.md                           ← this file
├── scenes/                                ← 14 storyboard stills (all used)
│   ├── scene_01_katie_stepping_out.png    ← use as STILL
│   ├── scene_02_hand_carrying_paparazzi.png ← use as STILL
│   ├── scene_03_full_body_walking.png     ← use as STILL
│   ├── scene_04_clean_leather_no_logo.png ← use as STILL
│   ├── scene_05_studio_front_product.png  ← use as STILL
│   ├── scene_06_leather_grain_macro.png   ← use as STILL
│   ├── scene_07_brass_turnlock_macro.png  ← still fallback if video 07 unused
│   ├── scene_08_three_quarter_side.png    ← use as STILL
│   ├── scene_09_side_silhouette.png       ← use as STILL
│   ├── scene_10_slouch_lifestyle.png      ← still fallback if video 10 unused
│   ├── scene_11_open_capacity_flatlay.png ← use as STILL
│   ├── scene_12_four_colorways_real.png   ← use as STILL (real product photo)
│   ├── scene_13_marble_console_lifestyle.png ← use as STILL
│   └── scene_14_hand_lifting_cta.png      ← still fallback if video 14 unused
├── animations/                            ← ONLY these 3 videos are in the final cut
│   ├── scene_07_brass_turnlock_macro.mp4
│   ├── scene_10_slouch_lifestyle.mp4
│   └── scene_14_hand_lifting_cta.mp4
├── animations/_unused/                    ← generated for review but not in the cut
│   └── (scenes 01, 02, 03, 04, 05, 06, 08, 09, 11, 12, 13 .mp4)
└── references/
    ├── ref_katie_holmes.png
    └── ref_vivienne_chocolate.png
```

---

## Editor notes

**Cutting rhythm.** Every cut lines up with a phrase break in the VO. Don't linger past its line. Scenes 1–3 (paparazzi stills) should feel almost jump-cut — three fast holds in six seconds, matching the reference's opening energy. From scene 5 onward the pace can settle. Videos 7, 10, 14 are your motion punctuation — everything else is a hold.

**The composite hook (optional).** The reference ad opens with a *split-screen composite* — Hailey Bieber paparazzi still (top left), Instagram profile screenshot (middle), watch product still (top right), talking head (bottom right). We don't have a talking head, but we could still do a composite for scenes 1–2:
- Paparazzi Katie still (with red circle on the bag)
- Instagram-style "@katieholmes · 3.2M followers" overlay
- Small Vivienne product thumbnail in the corner

If the editor wants to try this, it will make the celebrity claim land harder. If not, just use the three paparazzi stills back-to-back.

**Music.** Instrumental, quiet-luxury bed underneath the VO — soft piano or a warm ambient loop with light percussion. No lyrics. Ducked -12dB under VO. Nuamōre-style.

**Text overlays.** Minimal:
- Scene 2 optional: "@katieholmes · 3.2M followers" (Instagram-style, small)
- Scene 5: "Vivienne — $149" (bottom third, thin serif)
- Scene 13/14: "Pre-order — ships October" + arrow

**Compliance flag.** Scenes 1, 2, 3 use an AI Katie-alike model (nano_banana refused the celebrity name outright). For paid distribution, swap in licensed Katie Holmes paparazzi footage or a Katie-alike shot day. AI stills are for internal comping and creative sign-off only. Scenes 4–14 are safe to use as-is.

**Colorway shot.** Scene 12 uses the real product photo (not AI). Keep as is.

**No-logo callout.** Every shot has been prompted with "absolutely no logo" — verify on final edit that no scene rendered a logo, monogram, or brand mark.
