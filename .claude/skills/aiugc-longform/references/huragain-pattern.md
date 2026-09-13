# HurAgain / Joint Pain Experts 2025 — Pattern Analysis

Distilled from two reference ads in this brand's library:
- Ref #1: "The Best Thing For Hip Pain" — 1:53, kitchen, older creator, blue tee + pink star cap
- Ref #2: "The Real Cause Of Hip Pain" — 2:58, parked car, mid-40s creator, denim jacket

Both ads pitch the same product (HurAgain moringa supplement) with the same narrative spine, executed by two different creators in two different settings. This is a **single-narrator continuous-shot** format.

## Structural skeleton

| % through | Beat | Words spoken (approx) |
|---|---|---|
| 0-5% | **Hook** — promise + curiosity | 15-25 |
| 5-25% | **Problem agitation** — concrete sensory pain (3am wake-ups, can't sleep on side, hips burning, stiffness on standing, "have to think about every chair") | 80-150 |
| 25-40% | **Authority subversion** — "doctors said wear and tear," "anti-inflammatories like that was an answer" | 60-100 |
| 40-60% | **Mechanism** — estrogen → joint lubrication → estrogen drops in menopause → joints dry out → phytoestrogens fix it | 100-180 |
| 60-75% | **Solution** — "moringa is highest-concentration phytoestrogen," product name, dosage, what makes this brand different (potency) | 80-130 |
| 75-95% | **Personal proof** — "felt lubricated within weeks," "rusted hinge to well-oiled machine" | 60-100 |
| 95-100% | **CTA + guarantee** — "link below," "60-day guarantee," "don't wait as long as I did" | 20-40 |

Total ~ 400-700 spoken words for 90-180s VSLs at conversational pace (4-5 words/sec).

## Voice & cadence

- **Conversational rant energy.** "I'm gonna tell you...", "And here's what nobody told me...", "I had a suspicion..."
- **Specific sensory details.** Not "I had pain" — "the ache that wakes you up at 3am," "the way you have to think about every chair before you sit in it."
- **Authority subversion built in.** Always positions doctors as having missed the obvious. The viewer agrees because they've experienced the same brush-off.
- **Mechanism is plain-English.** "Estrogen is what keeps your tendons supple." No jargon stack.
- **Metaphors carry the proof.** "Like someone had sprayed WD-40 on my hips." "Rusted hinge to well-oiled machine." These do more work than data.
- **No hard sell.** CTA is "link below, don't wait as long as I did." Soft pull.

## Visual pattern

- **9:16 vertical phone selfie**, low chin-up angle (phone propped or held below eye level)
- **One creator, one setting**, no cuts, no B-roll, no zoom, no pan
- **Eye-level to upper-third framing** — eyes visible across frame, chest/shoulders typically visible, often with hand gestures coming up into the lower frame
- **Practical/ambient lighting** — kitchen ceiling recessed light, car interior diffused daylight. No softboxes, no ring lights visible.
- **Imperfect framing** — slightly off-center subject, head sometimes near top edge, framing not "professional"
- **Background recognizable but blurred-ish** — shallow depth of field from phone camera; you can read "kitchen" or "car" but can't analyze the contents

## Hook overlay style

- **Red rounded badge**, fully opaque, sharp corners slightly rounded (~14px radius)
- **Bold white sans-serif** (Helvetica/system bold), approximately 50-60px at 1080x1920
- **Centered horizontally**, pinned upper-third (~18% from top)
- **2-3 lines max**, wrapped at natural phrase breaks
- **Pinned ~0-8s**, fades out as the speaker hits the first transition into agitation
- Examples: "After trying 14 supplement for my hip pain", "My hip pain journey (tried everything)"

## Why this format converts

Direct-response philosophy at work:
- **Avatar mirroring**: 50+ female creator, candid setting, sounds like a friend → trust
- **Granular specificity**: 3am wake-ups, WD-40 metaphor → can't be AI-generated, feels real
- **Mechanism education**: viewer learns *why* nothing else worked → vindication of past frustration
- **Soft sell**: low-pressure CTA + 60-day guarantee → frictionless first purchase

Replicate this faithfully — don't compress the agitation, don't skip the mechanism, don't crank the urgency. The format earns trust through length.

## Replication targets for the skill

Defaults that produce HurAgain-faithful output:
- `--duration 120` (2 minutes — sweet spot)
- 9:16, 720p (`std` Seedance)
- Hook overlay style `red_badge` upper-third
- Voice: 50+ female (default `matilda` from ElevenLabs registry)
- Avatar: 50+ female demo, kitchen or parked-car setting per registry brand defaults
- Script generator enforces the 7-beat arc above (hook → agitate → subvert → mechanism → solution → proof → CTA) with word-count guardrails per beat
