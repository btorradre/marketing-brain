# Field Architecture, Multi-Panel Compositions, Display Format, and Cross-Tests

## The Field Architecture

Every image prompt uses these fields. Prefix the generation request with: "Generate an authentic native advertising photo. No text or typography in this image."

- **subject** — the exact content of the image. Real age, real body type, specific physical details matching the problem (weathered hands, visible age, dark circles). For object shots, describe the object plus the hand/environment holding or surrounding it. Never model-like features. **Anatomical completeness:** explicitly state every limb/body part that should be visible from the described camera angle (e.g. "both feet in worn running shoes visible on the sidewalk," "right hand with all five fingers wrapped around the bottle") — AI generators drop limbs that are implied but not stated.
- **setting** — drawn directly from the avatar world built in Step 2 of the main process. Never generic — not "kitchen," not even "older suburban kitchen," but the specific kitchen THIS person has, given their income, region, life stage, and taste (e.g. "1990s ranch-house kitchen, yellowing laminate countertop with a coffee ring stain near the drip coffee maker, white Kenmore fridge with a grandkid's crayon drawing held by a pizza magnet, window over the sink showing a chain-link fence and a flat Ohio backyard"). Every material and appliance must be consistent with one person's economic reality — granite counters don't belong with 15-year-old white appliances, a Sub-Zero fridge doesn't belong with a 2008 Camry in the driveway.
- **lighting** — real-world sources only, matched to time of day: overhead kitchen fluorescent, morning window light, phone-screen glow in a dark bedroom, hospital fluorescent with green-tinted panels, car dashboard glow at dusk, tungsten bedside lamp. Never rim lights, never studio lighting, nothing that couldn't exist in a real house, car, bathroom, or hospital.
- **props** — 3-5 specific objects from the avatar's world, each something this exact person would actually own. One "wrong detail" that signals real life (a kid's crayon drawing on the fridge, a lipstick-marked glass of water, a TV remote on the counter) — but it must also match the avatar's economic reality; a 62-year-old machinist's wrong detail is a hardware-store receipt, not a Whole Foods bag.
- **emotion** — for images with people: the precise micro-state, not a mood word (e.g. "the flat, unfocused gaze of someone going through a motion they've done a thousand times — not performing anything, just existing in a routine moment, the face you make when no one is supposed to be watching"). For images without people: the emotional atmosphere the scene creates (e.g. "the quiet resignation of a countertop that's been holding the same pill bottle for three years").
- **image_type** — technical specs plus visual quality, e.g. "iPhone 12 rear wide lens, slightly off-center framing, something cropped at the edge of frame, fine luminance noise in shadows, no post-processing, auto-exposure with slight highlight blow, phone-sensor depth of field with harsh bokeh transitions, looks like it came from someone's camera roll and was uploaded to Facebook without editing." For multi-panel compositions, add: "This is panel [N] of a [X]-panel composition. Maintain visual cohesion with the other panels — similar warmth, similar exposure level, similar grain texture — but each panel should look like a different photo from the same person's phone, not four frames from one photoshoot."
- **aspect_ratio** — 1:1 for single square images (most common for Facebook feed), 4:5 for single vertical images. For multi-panel compositions, generate each panel at 1:1 and assemble afterward.
- **prompt_id** — filename format `[campaign_slug]_[descriptor]`, lowercase with underscores, no spaces (e.g. `motilli_bathroom_scale`, `lunessa_pharmacist_counter`).

## Multi-Panel Compositions

Generate each panel as a separate prompt; panels get assembled after generation. Each panel plays one of four narrative roles (not rigid categories — lenses for deciding what each panel contributes):

- **The Anchor** — what identifies the narrator or their world (their profession's setting, their home, their daily environment)?
- **The Villain** — what is the reader currently using/doing that the copy positions as the problem (the medication bottle, the waiting room, the pill organizer)?
- **The Human** — who is involved (the narrator, their spouse, family, the person affected)?
- **The Evidence** — what happened, or what the reader fears (a hospital bed, clinical images, a consequence shot, a grave)?

Not every composition needs all four. A three-panel image might use Anchor + Villain + Evidence; a two-panel might use Villain + Consequence. The copy determines which roles matter.

Visual cohesion rules across panels: similar warmth/color temperature (all slightly warm domestic, or all cool clinical — never mixed); similar grain/noise level (all look like the same phone); similar level of "imperfection" (don't mix a perfectly composed panel with a drastically off-center one); different content but the same quality feel, like four photos from one person's camera roll.

## Display Format

Show every prompt as the exact structured object that will be sent for generation — no translation layer between what gets reviewed and what fires.

Single image:
```json
{
  "image_label": "A",
  "description": "[what this image captures]",
  "role": "[narrative function]",
  "identification_trigger": "[what the reader recognizes as their own life]",
  "prompt": {
    "prompt_id": "brandslug_descriptor",
    "subject": "...",
    "setting": "...",
    "lighting": "...",
    "props": "...",
    "emotion": "...",
    "image_type": "...",
    "aspect_ratio": "..."
  }
}
```

Multi-panel composition:
```json
{
  "composition": "[name]",
  "panel_count": 4,
  "panel_layout": "[describe arrangement]",
  "panels": [
    {
      "panel_number": 1,
      "role": "anchor",
      "prompt": {
        "prompt_id": "brandslug_panel1_descriptor",
        "subject": "...",
        "setting": "...",
        "lighting": "...",
        "props": "...",
        "emotion": "...",
        "image_type": "...",
        "aspect_ratio": "..."
      }
    }
  ]
}
```

The `prompt` object inside each image/panel is exactly what should be sent to the image-generation tool. What gets shown for review is what gets sent.

## Cross-Tests

When setting up cross-tests to isolate which variable is driving performance:

- **Round 1 — test image impact:** pair Image A with Hook B, Image B with Hook C, Image C with Hook A.
- **Round 2 — test headline impact:** pair Image A + Hook A with Headline C, and so on.

Naming convention: `[slug]_[image]_x_[hook]` — e.g. `brandslug_pharmacist_x_hookB`.
