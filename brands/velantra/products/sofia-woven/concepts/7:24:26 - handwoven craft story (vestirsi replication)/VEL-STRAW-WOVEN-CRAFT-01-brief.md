# VEL-STRAW-WOVEN-CRAFT-01 — "Made The Slowest"

**Concept:** Silent-atelier craft film. Twenty-two seconds of macro hands weaving straw, no faces, no model, no lifestyle. A calm narrator explains why the bag takes so long to make. The finished Straw Tote is withheld until the final three seconds.

**Reference:** Vestirsi "Woven Collection" (Meta, AU) — `https://app.trendtrack.io/share/ads/vestirsi-Sdk1ue`

**Product:** Velantra Straw Tote — `https://velantrafashion.com/products/velantra-straw-tote`
**Colorway:** Caramel (hero). Single colorway only — this ad is about the weave, not the range.
**Format:** 9:16, 720p, VO over macro b-roll, progressive word captions.
**Pipeline:** GPT Image 2 i2i keyframes → **Kling 3.0** i2v (6s each) → trim + stitch → ElevenLabs VO (one seamless track) → caption overlay.
**Clips:** 14 → **18 cuts**. **Runtime: 21.3s** (reference is 20.9s).

> **STATUS: BUILT AND SHIPPED 2026-07-24.** Finished files in `final/`. See the production log at the end for what changed during the build.

---

## 1. Reference teardown

Vestirsi, 20.9s, 19 cuts, zero faces, zero models, zero lifestyle. Every shot is a macro of hands working leather. The finished bag does not appear until 0:20.

| # | ~t | Reference shot | VO |
|---|-----|----------------|-----|
| 1 | 0.0 | Wooden mallet tapping a woven leather panel flat on a white table | "The pieces you'll" |
| 2 | 1.3 | Industrial machine stitching edge trim onto the woven panel, gold hardware | "carry the longest are made the slowest." |
| 3 | 2.6 | Artisan lifts a steel cutting die over a black hide on a wood bench | "In Italy," |
| 4 | 3.9 | Hands in white sleeves press the panel flat on the bench | "woven leather is more than" |
| 5 | 5.2 | Red clicker press, hand pulling the lever, scissors on the deck | "more than a technique," |
| 6 | 6.5 | Woven panel settled onto a wooden weaving board with metal comb | "it's a tradition." |
| 7 | 7.3 | Hand lifts the woven panel off the board | "Every panel" |
| 8 | 8.6 | **Top-down: hide slit into strips, metal rods threaded through, hand pushing a strip** | "is woven entirely by" |
| 9 | 9.9 | Top-down tighter, weave nearly complete, hand smoothing it | "hand before it's assembled," |
| 10 | 11.2 | Cylinder-arm machine, ringed hands feeding the woven edge under the needle | "preserving a craft" |
| 11 | 13.2 | Second machine, older weathered hands, stitching the panel edge | "that has been passed down through generations." |
| 12 | 15.2 | Metal setting tool fixing a strap keeper | "It's a slower way of making things," |
| 13 | 16.5 | Machine stitching a rolled leather strap | "but that's exactly" |
| 14 | 17.8 | Macro of the finished bag, hands closing the gold zip | "what makes these pieces" |
| 15 | 18.5 | Hands folding white tissue over the bag | "so special." |
| 16 | 19.2 | Hands lift the bag out of the tissue | "The" |
| 17 | 19.8 | **Hero: finished bag held up against a white coat** | "Woven Collection by Vestirsi." |
| 18 | 20.3 | Bag swings down onto the surface | "Discover yours." |
| 19 | 20.6 | Locked hero of the bag settled on the surface | — |
| 20 | 20.9 | Black end card, wordmark + origin line | — |

### Why it works

1. **The hook is a proverb, not a claim.** "The pieces you'll carry the longest are made the slowest" reads as received wisdom, so ad-defenses never fire. And it inverts the liability (slow) into the proof (longevity).
2. **Price is justified by labor, never by comparison.** Nobody says "worth it." Twenty seconds of a hand doing what a machine can't, and the viewer computes the value themselves. That arithmetic is more durable than any stated one.
3. **The reveal is withheld.** You watch twenty seconds of parts. The brain is trying to assemble the object the whole time, so the payoff at 0:20 lands on tension that's already built.
4. **Hands are the trust device.** A face reads as an actor. A hand reads as a fact.
5. **The mechanism IS the product's most visible feature.** The weave is what you see on the shelf, and the ad spends its whole runtime teaching you to read that weave as expensive.
6. **Craft restraint sells craft.** Locked camera, no music bed, no push-ins, no transitions. The stillness is itself an argument that nobody was in a hurry.

---

## 2. Adaptation deltas

| Reference move | Our move | Why |
|---|---|---|
| "In Italy" + "MADE IN ITALY" end card | **Cut entirely.** No country named anywhere, on screen or spoken. | Locked brand law: Velantra never makes an origin claim. |
| Geography as the authority beat | **Mechanism as the authority beat** — straw has to be worked damp or it splits | A reason-why is stronger than a postcode, and it's ours to own |
| Woven *leather* | Woven *straw* | Our weave is more visibly hand-made than theirs, so the mechanism shot is actually better |
| Machine beats (clicker press, 4 sewing machines) | **Rebalanced to hand beats** | Brooks's ask is "every single bit is handwoven" — machines only appear where leather trim genuinely gets stitched |
| "so special" (generic turn) | **"why it holds its shape"** | Trades a hollow adjective for a locked product claim |
| "Woven Collection" | "The Straw Tote" | Single hero product, not a range |
| Face-free | Face-free (kept) | Also removes all avatar-consistency risk from the build |

**Not doing:** no competitor or category comparison of any kind, no "unlike other straw bags," no designer-inflation angle. This ad is pure craft. It runs cold-audience top-of-funnel next to the existing UGC.

---

## 3. Script

**AS PRODUCED** — 62 words, 20.2s spoken. Passed the origin-claim and competitor-comparison audits.

> The bags you'll carry the longest are made the slowest.
>
> Straw has to be worked by hand while it's damp, so every strand is placed one at a time.
>
> Hours of work, in hands that have done it a thousand times.
>
> A slower way to make a bag, and exactly why it holds its shape.
>
> The Straw Tote by Velantra. Discover yours.

The first draft ran 74 words. Every voice read it at 26-28s against the reference's 21s, so the two mechanism lines were merged into one and the concession line was tightened. Every structural beat survived: proverb hook, reason-why, craft-lineage, concession-and-turn, brand close. Landed at 62 words against the reference's 63.

**Line 2 alternate** (if you'd rather not assert the damp-working detail): *"Hand woven straw is more than a texture, it's a craft."* The damp line is stronger because it gives a reason-why, and it's true of natural straw basketry generally, but it is a manufacturing statement so it's your call. Swapping it means regenerating the VO and rerunning the edit builder, nothing else.

### VO spec

One seamless full-length track, generated in a single pass. Never per-segment files.

- **Voice:** female, 30s, warm and low, unhurried. Neutral accent, no regional marker.
- **Register:** quiet and certain. Someone explaining something they respect, not selling it. No upward inflection, no lift on the CTA.
- **Pace:** slow. ~3.1 words/sec. Real breath between sentences.
- **Never:** brightness, enthusiasm, "excited announcer," any smile in the voice.
- **Direction line:** `Read this slowly and quietly, like you are explaining something you care about to one person standing next to you. Let the sentences land. Do not sell.`

---

## 4. Shot list

Nineteen cuts from fourteen generated clips. Clips marked **2 cuts** get two different sections pulled from the same 6s generation.

| Cut | In | Out | Clip | Shot |
|-----|-----|-----|------|------|
| 1 | 0.0 | 1.3 | A | Flat wooden beater tapping a woven straw panel flat |
| 2 | 1.3 | 2.6 | B | Machine stitching the seam where the taupe leather meets the straw body |
| 3 | 2.6 | 3.9 | C | Hands lifting a hank of raw straw fiber onto the bench |
| 4 | 3.9 | 5.2 | D | Hands drawing straw strands through a damp cloth, water sheen |
| 5 | 5.2 | 6.5 | D *(2 cuts)* | Tighter: damp strands laid out in a row, hand smoothing |
| 6 | 6.5 | 7.3 | E | Part-woven straw panel settled onto the wooden weaving frame |
| 7 | 7.3 | 8.6 | E *(2 cuts)* | Hand lifting the panel edge, loose strand ends fanned out |
| 8 | 8.6 | 9.9 | **F** | **Top-down hero: fingers threading one strand over-under through the warp** |
| 9 | 9.9 | 11.2 | G | Top-down, weave now dense and complete, hand smoothing it flat |
| 10 | 11.2 | 13.2 | H | Macro: braided cross-stitch trim worked along the panel edge by hand with a needle |
| 11 | 13.2 | 15.2 | I | Machine stitching the taupe leather flap panel, white contrast stitch |
| 12 | 15.2 | 16.5 | J | Hands burnishing the edge of a rolled taupe leather handle |
| 13 | 16.5 | 17.8 | K | Macro: the rolled handle running under the needle, white contrast stitch |
| 14 | 17.8 | 18.5 | L | Slow macro glide across the finished caramel weave, crossed belts in frame |
| 15 | 18.5 | 19.2 | M | Hands folding cream tissue paper over the finished tote |
| 16 | 19.2 | 19.8 | M *(2 cuts)* | Hands lifting the tote by both handles out of the tissue |
| 17 | 19.8 | 20.4 | N | Hero: tote held up by the handles against a cream apron |
| 18 | 20.4 | 21.0 | N *(2 cuts)* | Tote lowered onto the worktable, slight settle |
| 19 | 21.0 | 21.6 | N *(freeze)* | Locked hero, tote at rest |
| — | 21.6 | 22.0 | — | Black end card, VELANTRA wordmark |

**Cadence:** 1.3s per cut through the first two thirds, stretching to 2s for the machine beats, then 0.6-0.7s for the reveal run. Hard cuts only. No dissolves, no transitions, ever.

---

## 5. Locked blocks

Paste verbatim into every prompt. Do not paraphrase.

### SET
> a quiet craft workshop, pale cream plaster wall behind, a worn pale wood worktable, soft diffused daylight falling from the left of frame, warm neutral color grade, slightly desaturated. No faces, no heads, no shoulders. Only hands and forearms in a plain cream linen rolled sleeve are ever visible. No windows, no signage, no text, no logos anywhere in frame.

### CAMERA
> shot on a macro lens, shallow depth of field, the camera is locked off on a tripod and does not move at all, no pan, no tilt, no zoom, no push in. All motion in the frame comes from the hands.

### MATERIAL
> natural seagrass straw fiber in warm sandy caramel, fine tightly twisted strands with a matte surface and a faint natural sheen, slightly irregular the way real plant fiber is, never plastic, never shiny, never dyed.

### PRODUCT IDENTITY (clips L, M, N only)
> a structured hand woven straw tote in warm sandy caramel, tightly woven straw body with braided cross stitch trim along the edges, a smooth taupe leather flap folded over the top of the bag from the back: the flap is ONE single seamless piece of leather, its front lower edge cut into the silhouette of a wide center panel with 2 squared outer tabs, the leather fully continuous and unbroken between and above these shapes, with exactly 2 narrow slots through which the handles pass, two rolled taupe leather top handles, two taupe leather belt straps crossed on the front, white contrast stitching on all leather edges, no metal hardware, no logos. The leather flap, tabs and belt straps exist ONLY on the FRONT face of the bag, the back face is plain woven straw, no duplicated front detailing on any other face.

### FLAP MECHANISM (clips L, M, N only — mandatory)
> Flap and opening construction: the taupe leather flap is ONE single seamless sheet of leather attached along the top rear edge of the tote and folded all the way forward over the front, lying completely flat. Its front lower edge is cut into the shape of a wide center panel and 2 squared outer tabs, but these are shapes cut into the SAME single sheet, never separate pieces. The leather is continuous and unbroken between the shapes and across the entire top of the bag, including between the two handle slots. The only openings anywhere in the flap are the 2 narrow handle slots. No gap, no seam, no split, no opening exists anywhere else in the flap, and nothing behind or inside the bag is ever visible through the flap. The flap never splits into pieces, never lifts, never stands up, always folded all the way over. The 2 taupe leather belt straps lie crossed in an X over the front below the flap with rounded ends and white contrast stitching, never threaded through the flap. No metal hardware anywhere on the bag.

### FLAP MECHANISM, VIDEO PIN (append to motion prompts on L, M, N)
> The leather flap stays ONE single seamless sheet folded all the way over, lying completely flat the entire clip: no gap, seam, or split ever opens anywhere in it, nothing behind it ever shows through it, and its cut edge shapes never separate into pieces.

### MOTION FOOTER (append to every motion prompt)
> Ambient workshop room tone. No cuts. No zooms. No transitions. No camera movement. No faces. Vertical 9:16. ONE CONTINUOUS SHOT.

---

## 6. Generation prompts

Each clip = one keyframe (GPT Image 2 i2i, 9:16) then one 6s Seedance 2.0 i2v pass. Generate every clip at 6 seconds regardless of how short the cut is, so the edit has trim headroom on both ends.

Clips L, M and N are seeded from the canonical caramel Straw Tote product reference as a pure i2i composite. Clips A through K carry no finished bag, so they generate from the material and set blocks alone.

---

**CLIP A — beating the panel flat** *(cut 1)*

*Keyframe:* Two hands hold a flat wooden beater over a rectangular hand woven straw panel lying on the worktable. One hand grips the beater handle, the other rests flat on the panel holding it still. The panel is dense caramel straw weave, its edges still raw and unfinished with loose strand ends. Close macro, the panel fills the lower two thirds of frame. `[SET]` `[CAMERA]` `[MATERIAL]`

*Motion:* `the beater taps down onto the straw panel twice with a small firm motion, the flat hand stays pressed on the panel and does not move, the panel settles slightly flatter with each tap` `[MOTION FOOTER]`

---

**CLIP B — joining the leather to the straw** *(cut 2)*

*Keyframe:* Extreme macro of an industrial sewing machine needle and presser foot. The top edge of a caramel straw woven panel is being joined to a piece of smooth taupe leather, white contrast stitching already laid down behind the needle along the seam where the two materials meet. Two hands guide the work from the right of frame, fingers close to the foot. The straw weave fills the lower left of frame, the taupe leather the upper right. `[SET]` `[CAMERA]` `[MATERIAL]`

*Motion:* `the needle rises and falls quickly, the straw panel and the taupe leather feed steadily to the left under the presser foot, a line of white stitching grows behind the needle along the seam between them, the two hands guide with small steady adjustments` `[MOTION FOOTER]`

---

**CLIP C — the raw material** *(cut 3)*

*Keyframe:* Two hands lift a thick loose hank of raw natural straw fiber and lower it onto the worktable. The strands are long, fine and unruly, spilling over the hands. Cream linen sleeves rolled to the forearm. Mid macro, the hank fills the center of frame, the pale wall soft behind. `[SET]` `[CAMERA]` `[MATERIAL]`

*Motion:* `the hands lower the hank of straw onto the table, the loose strands fan out and settle, one hand releases and the fibers spread slightly across the wood` `[MOTION FOOTER]`

---

**CLIP D — working it damp** *(cuts 4 and 5)*

*Keyframe:* Macro of two hands drawing a bundle of straw strands through a folded damp cloth. The strands emerging on the near side are visibly darker and have a wet sheen. A shallow tray of water sits soft and out of focus at the top of frame. Fingers pinch the strands firmly. `[SET]` `[CAMERA]` `[MATERIAL]`

*Motion:* `the hands draw the bundle of straw strands slowly through the damp cloth toward the camera, the strands darken and take on a wet sheen as they emerge, the second hand smooths them straight as they clear the cloth` `[MOTION FOOTER]`

*Editor:* pull cut 4 from the first half of this clip, cut 5 from the second half.

---

**CLIP E — onto the weaving frame** *(cuts 6 and 7)*

*Keyframe:* A part woven caramel straw panel resting on a flat wooden weaving frame with fine metal pins running along one edge. Roughly two thirds of the panel is tightly woven, the remaining third is loose parallel strands waiting to be worked. Two hands settle the panel down onto the frame. Shot at a low angle across the table. `[SET]` `[CAMERA]` `[MATERIAL]`

*Motion:* `the hands settle the part woven panel down flat onto the wooden frame, then one hand lifts the unfinished edge slightly so the loose strand ends fan apart, and lowers it again` `[MOTION FOOTER]`

*Editor:* cut 6 is the settle, cut 7 is the lift.

---

**CLIP F — the hero mechanism shot** *(cut 8)*

This is the single most important frame in the ad. It is the shot that does the persuading. Give it extra generations if needed.

*Keyframe:* Directly top down over the wooden weaving frame. A grid of caramel straw warp strands runs vertically. A single straw strand is being threaded horizontally across them, passing over one strand and under the next in a clear visible over under rhythm. Two fingers pinch the working strand mid weave. Half the panel behind the working row is already tight and finished, the half in front is open warp. Filling the frame edge to edge. `[SET]` `[CAMERA]` `[MATERIAL]`

*Motion:* `the fingers push the single working strand across the warp from left to right, weaving over one strand and under the next in a clear steady rhythm, the second hand holds the finished weave flat below, the strand advances about a third of the way across the panel` `[MOTION FOOTER]`

---

**CLIP G — the weave closes up** *(cut 9)*

*Keyframe:* Top down, tighter than clip F. The straw weave is now dense, complete and even across the whole frame, the pattern tight with no gaps. One open hand rests flat on the surface, palm down, smoothing it. `[SET]` `[CAMERA]` `[MATERIAL]`

*Motion:* `the open hand sweeps slowly across the finished straw weave from left to right, pressing it flat, the weave stays perfectly even and does not shift` `[MOTION FOOTER]`

---

**CLIP H — the braided edge, by hand** *(cut 10)*

*Keyframe:* Extreme macro of the braided cross stitch trim being worked by hand along the raw edge of the caramel straw panel. A large blunt needle carrying a strand of straw is mid stitch, pulled through the edge. The finished braided cross stitch runs away behind it, the unfinished raw edge ahead. Two hands, one pulling the needle, one holding the panel. `[SET]` `[CAMERA]` `[MATERIAL]`

*Motion:* `the hand pulls the needle and its straw strand fully through the edge of the panel and draws it tight, then sets the needle for the next stitch, the braided trim gains one more cross stitch` `[MOTION FOOTER]`

---

**CLIP I — stitching the flap panel** *(cut 11)*

*Keyframe:* Extreme macro of a cylinder arm sewing machine. A flat piece of smooth taupe leather runs under the needle, a line of white contrast stitching being laid along its edge. Two weathered hands guide the leather, one on each side of the foot. No straw in this frame. `[SET]` `[CAMERA]`

*Motion:* `the needle rises and falls, the taupe leather feeds steadily under the presser foot, a clean line of white stitching grows behind the needle, the hands make small steady corrections to keep the edge true` `[MOTION FOOTER]`

---

**CLIP J — finishing the handle edge** *(cut 12)*

*Keyframe:* Macro of two hands working the edge of a rolled taupe leather handle with a small wooden burnishing tool. The handle is held taut between the hands over the pale worktable. White contrast stitching visible along the handle. `[SET]` `[CAMERA]`

*Motion:* `one hand runs the burnishing tool back and forth along the edge of the rolled leather handle in short firm strokes, the other hand holds the handle taut and still, the edge takes on a smooth finish` `[MOTION FOOTER]`

---

**CLIP K — the handle under the needle** *(cut 13)*

*Keyframe:* Extreme macro of a sewing machine needle running along a rolled taupe leather handle, white contrast stitching laid down its length. Fingertips guide the handle from the right of frame. Shallow focus, the machine body soft behind. `[SET]` `[CAMERA]`

*Motion:* `the rolled leather handle feeds steadily under the needle, white stitching runs down its length behind the foot, the fingertips guide it forward with small steady pressure` `[MOTION FOOTER]`

---

**CLIP L — the finished weave** *(cut 14)* — **product clip, i2i from the canonical caramel reference**

*Keyframe:* Macro of the finished Straw Tote standing on the pale worktable, shot close and slightly across the front face so the caramel weave fills most of the frame. The braided cross stitch trim runs along the visible edge. The two crossed taupe leather belt straps sit in the lower part of frame. No hands in this frame. `[PRODUCT IDENTITY]` `[FLAP MECHANISM]` `[SET]` `[CAMERA]`

*Motion:* `nothing in the scene moves except the light, which shifts very slightly across the straw weave. The bag is completely still and does not rotate, tilt or deform. No hands enter the frame` `[FLAP MECHANISM, VIDEO PIN]` `[MOTION FOOTER]`

---

**CLIP M — tissue** *(cuts 15 and 16)* — **product clip, i2i from the canonical caramel reference**

*Keyframe:* Two hands folding a sheet of soft cream tissue paper over the finished Straw Tote on the worktable. The tissue covers most of the bag, one corner of the caramel weave and one rolled taupe handle still visible. Cream linen sleeves. `[PRODUCT IDENTITY]` `[FLAP MECHANISM]` `[SET]` `[CAMERA]`

*Motion:* `the hands fold the cream tissue over the bag, then take hold of both rolled leather handles and lift the tote up and clear of the tissue, the tissue falling away below. The bag holds its shape completely and does not deform, sag or bend as it lifts` `[FLAP MECHANISM, VIDEO PIN]` `[MOTION FOOTER]`

*Editor:* cut 15 is the fold, cut 16 is the lift.

---

**CLIP N — the reveal** *(cuts 17, 18 and 19)* — **product clip, i2i from the canonical caramel reference**

*Keyframe:* The finished caramel Straw Tote held up by both rolled taupe handles, filling the center of frame, against a plain cream linen apron and the soft pale wall behind. Straight on to the front face, so the flap, the crossed belts and the full weave all read clearly. Shot from slightly below table height so the bag sits high in frame. `[PRODUCT IDENTITY]` `[FLAP MECHANISM]` `[SET]` `[CAMERA]`

*Motion:* `the hands lower the tote slowly and set it down onto the pale worktable, the bag settles and comes completely to rest, then the hands release the handles and withdraw out of frame, leaving the bag still and centered. The bag holds its structured shape throughout and never sags, folds or deforms` `[FLAP MECHANISM, VIDEO PIN]` `[MOTION FOOTER]`

*Editor:* cut 17 is the held hero, cut 18 is the lower and settle, cut 19 is a hold on the final still frame after the hands leave.

---

## 7. Captions

Word by word progressive build, matching the reference exactly.

- **Font:** clean grotesque, medium weight. Helvetica Now Medium or SF Pro Text Medium.
- **Color:** pure white. **No** drop shadow, **no** stroke, **no** background plate.
- **Size:** cap height ~3.5% of frame height. Small. It is a subtitle, not a headline.
- **Position:** left aligned, ~10% in from the left edge, vertical center of frame (~50% height). Not lower third, not centered.
- **Behavior:** words appear one at a time in sync with the VO, accumulating across the sentence, then the line clears at the sentence break and the next sentence begins building.
- **Wrapping:** max two lines. Break at natural phrase boundaries.

Overlay in post. Do not attempt to generate on-screen text in Seedance.

## 8. End card

Black frame, 0.4s. Centered `VELANTRA` wordmark in white.

**No tagline. No origin line. No URL.** The reference's end card reads "MADE IN ITALY" underneath — ours carries the wordmark alone. This is the single most important delta in the whole build.

## 9. Audio

- One continuous VO track under the entire cut, generated in a single pass.
- Low workshop room tone underneath: soft machine hum, faint fabric handling. Barely present.
- **No music bed.** The reference has none. Silence is doing work here.
- Cut sound effects are optional and should be almost inaudible if used at all.

---

## 10. QA gates

Nothing ships past a gate.

1. **Pre-animation frame QA.** Every keyframe on clips L, M and N goes to a fresh-context audit subagent against the canonical caramel reference and the campaign QA checklist, before it is animated. Audit the exact crop that feeds the engine. FAIL means regenerate with the mechanism block pasted, cap 3 attempts, then change the blocking.
2. **Video frame QA.** Extract at least 3 frames from each generated L, M and N clip at start, middle and end, and audit each. Seedance breaks the flap mid-motion from a clean first frame.
3. **Invented-design check.** Seedance grows braided buckles, metal hardware, saddle flaps and wrap-around straps on this bag mid-clip. Any geometry not on the canonical reference means regenerate.
4. **Closure interaction.** No clip may show hands unfastening the belts, lifting the flap or opening the bag. Closure state never changes in motion. This build is designed so it never has to.
5. **Face check.** Scrub every clip. If a face, a head or a pair of shoulders appears in any frame, regenerate. The face-free rule is what makes this ad read as documentary.
6. **Origin scan.** Watch the finished cut with captions on and confirm no country, flag, language, or place name appears in any frame, in the VO, in the captions, or on the end card.
7. **Weave continuity.** The straw color and strand gauge must read as the same material from clip A through clip N. Mismatched straw across cuts breaks the whole premise.

---

## 11. Ad copy

**Primary text:**

> The pieces you carry the longest are the ones nobody rushed.
>
> Every Velantra Straw Tote is woven by hand, one strand at a time, before the bag is ever assembled. It is a slower way to make a bag. It is also exactly why it holds its shape.
>
> The Straw Tote. Woven by hand, in limited quantities.

**Headline:** Woven By Hand, One Strand At A Time
**Description:** The Velantra Straw Tote
**CTA:** Shop Now
**Destination:** `https://velantrafashion.com/products/velantra-straw-tote`

---

## 12. Build order

1. Generate keyframes A through K. No product identity at stake, so these move fast.
2. Generate keyframes L, M, N as pure i2i composites from the canonical caramel reference. **Gate 1** before animating any of them.
3. Animate all 14 at 6s. **Gate 2 and 3** on L, M, N.
4. Render the VO as one seamless track.
5. Cut to the shot list against the VO. Hard cuts only.
6. Overlay captions, add the end card.
7. **Gates 4 through 7** on the finished cut.

---

## 13. Production log (2026-07-24)

**Deliverables in `final/`:**
- `VEL-STRAW-WOVEN-CRAFT-01_amaya.mp4` — 21.29s, primary
- `VEL-STRAW-WOVEN-CRAFT-01_lily.mp4` — 20.88s, alt voice

Both are 720x1280 h264 + AAC, captions burned in, end card attached.

### Deviations from the plan

**Engine: Kling 3.0, not Seedance 2.0.** The adjacent Vestirsi replication on this exact product used Kling successfully at 6s; there is no dialogue here so Seedance's native-audio advantage is irrelevant; and the Straw Tote has a documented history of Seedance mutating its flap and growing hardware mid-motion. Kling held the bag geometry across all three product clips with zero regenerations.

**18 cuts, not 19.** The tightened 62-word VO left slightly less runway. The dropped cut was a duplicate pull, not a distinct shot. All 14 clips appear.

**Captions rendered as a PNG sequence, not ASS.** The local ffmpeg is built without libass *and* without libfreetype, so it has no `ass`, `subtitles`, or `drawtext` filter. The caption layer is now rendered with PIL (Helvetica Neue Medium, face index 10) into 496 transparent frames and composited with a single `overlay`. Typographically identical to the spec and fully deterministic. `build_edit.py` owns this.

**End card wordmark had to be recolored.** The shared `velantra_logo.png` is pure black on transparent, so it rendered invisible on the black card. The builder now inverts it to white at build time, preserving alpha.

### QA results

| Gate | Result |
|---|---|
| 1. Pre-animation keyframe QA (L, M, N) | **M FAILED v1** — bag rendered collapsed on its side with the flap bunched, which directly contradicts the "holds its shape" payoff. Regenerated with an explicit upright/structured pin. v2 passed. L and N passed first time. |
| 2. Video frame QA (L, M, N, start/mid/end) | PASS. Flap stayed one seamless sheet in every frame. |
| 3. Invented-design check | PASS. No shoulder strap, no metal hardware, no braided buckles, no added geometry. |
| 4. Closure interaction | PASS by construction. No clip shows hands working the flap or belts. |
| 5. Face check | PASS. Scrubbed 30 frames across the finished cut plus per-clip frames. Hands and torso only, never a head. |
| 6. Origin scan | PASS. No country, flag, place name or language anywhere in frame, VO, captions or end card. End card is the wordmark alone. |
| 7. Weave continuity | PASS. Consistent caramel straw across all cuts. |

### Sync notes worth keeping

The cut list is generated from the VO's real word-level timings (ElevenLabs `/with-timestamps`), not from estimated durations. Cuts are distributed across sentence spans, which lands the payoff beats automatically:
- Clip F (top-down hero weave) sits under *"every strand is placed one at a time"*
- Clip L (finished weave) sits under *"exactly why it holds its shape"*
- Clip N (hero reveal) sits under *"The Straw Tote by Velantra"*

Swapping the voice re-derives every cut boundary against that voice's own timings. `build_edit.py <voice>` is the whole operation.

### Cost

- 15 keyframes at 6cr (14 + one M regeneration) = 90cr
- 14 clips at 84cr = 1,176cr
- **Total 1,266 kie.ai credits.** ElevenLabs VO: 3 casting takes plus 3 final, negligible.
