# The rubric

Ten points. Above 5.0 gets pinned, 5.0 and below gets archived. The bar is
deliberately set where a merely competent editor lands on the wrong side of it.

Every number you assign needs a sentence of evidence naming what you saw and
where. "Strong hooks" is not evidence. "First 3s of `v02` opens on a static
product shot with a centred title card, no motion until 1.4s" is.

---

## Hard gates: run these first, on text alone

All four are stated in the posting under "Applications missing any of these four
items are deleted unread." Any single failure archives the application at 0.0
and you stop working on it. Do not score, do not download anything.

| Gate | Passes when |
|---|---|
| `filter_word` | The application opens with the brand's filter word. Velantra = **SAFFRON**, Motilli = **JUNIPER**. Case-insensitive, and "opens with" is generous: anywhere in the first line or two counts. A word buried in paragraph four does not: that is a keyword scrape, not instruction compliance. |
| `loom_link` | A Loom URL is present. Another host is fine if it is plainly a screen-recorded walkthrough. A YouTube link that is just their reel again is not a Loom. |
| `portfolio_link` | A reel or portfolio link that is distinct from the Loom. |
| `timezone_hours` | They stated a timezone **and** weekly hours. Both. One without the other fails. |

Two gates that are wrong to enforce, so do not invent them: applicants who
mention a different brand's filter word are usually applying to several of our
posts and that is fine; and a filter word in the subject line rather than the
body still counts.

---

## Scored components

Weighted toward the three things Brooks named: the right visual under the right
line, fast pacing, and a reel that resembles the benchmark. Scripts and briefs
are supplied by us, so writing ability is not scored on its own.

Read `benchmark-balmbare.md` before scoring these. The anchors below are measured
from that pull, not invented.

### `visual_line_match` (max 2.5), the headline criterion

We hand over the script, the brief, and the references. The whole job is knowing
which frame belongs under which line. This is the heaviest single component
because it is the one skill we cannot supply.

Judge it by reading the caption or transcript at a cut, then looking at what is
actually in that frame.

| Band | Pts | Looks like |
|---|---|---|
| Literal and motivated | 2.5 | Named things appear. "Saw palmetto" is a saw palmetto shot. A mechanism line gets a diagram. A comparison line gets the competitor product. Cuts land where the sentence turns. |
| Mostly right, some filler | 1.5 | The important beats are matched but stretches run on generic b-roll that would fit any line. |
| Decorative | 0.75 | Visuals are pretty and roughly on-topic but interchangeable. Cuts land on the music, not the read. |
| Unrelated | 0 | Footage runs independently of what is being said. |

If the reel has no voiceover or captions at all, you cannot score this. Say so in
evidence and score 0 rather than guessing.

### `pacing` (max 2.0)

Measured, not felt. Count the `scene_*.jpg` frames against the duration in
`media.json` for an approximate average shot length, and read `hook_*.jpg` in
order for where the first cut lands.

Benchmark: short-form ads average **2.0 to 3.2s per shot**, and even a 192s VSL
holds 1.76s. First cut lands by **1.5 to 3.2s**.

- **2.0**: average shot at or under 3s, first cut inside 3s, no dead air, and the
  cadence varies rather than being metronomic.
- **1.2**: average 3 to 4s, first cut inside 4s. Competent, a little slack.
- **0.6**: average 4 to 5s, or a strong opener that sags badly in the middle.
- **0**: average over 5s. Apply the `too_slow` cap. The clearest loser in the
  benchmark pull was a 102s ad with two cuts and a first cut at 28.7s.

Cutting so fast that nothing registers is also wrong, but it is rare and it costs
0.4 rather than the whole component. Note it in evidence.

### `benchmark_resemblance` (max 1.5)

Would this reel sit comfortably next to the Balmbare set, or does it belong in a
different business?

- **1.5**: 9:16, phone-native, ungraded or lightly graded, hard cuts, mixed
  sources cut together without apology, burned-in text carrying the argument.
- **0.9**: DR-shaped and platform-native but visibly templated, or one source
  type only.
- **0.4**: polished brand or agency work. Colour-graded, slow pushes, shallow
  depth of field, music-led. Real skill, wrong job.
- **0**: not advertising. Apply `not_direct_response`.

**Do not reward cinematic polish here.** A graded, beautifully lit reel is
further from this benchmark than a scrappy phone-shot one that cuts hard and puts
the right thing under the right line. This is the trap in the whole rubric.

### `category_fit` (max 1.5)

Both postings say the category is "required, not a bonus," so it keeps a cap as
well as points, but craft now outweighs it.

| Band | Pts | Looks like |
|---|---|---|
| Direct evidence in the reel | 1.5 | Velantra: finished paid-social ads for fashion, apparel, handbags, jewellery or accessories. Motilli: finished DR ads for supplement, health, wellness or medical. You watched them. |
| Claimed and partly shown | 0.9 | Adjacent category with one or two real examples: beauty/skincare for Velantra, fitness or food-supplement for Motilli. |
| Claimed only | 0.4 | Says it in the cover letter, nothing in the reel backs it. |
| Absent | 0 | Apply the `wrong_category` cap. |

### `caption_craft` (max 1.0)

Every ad in the benchmark is carried by burned-in text. An unlettered reel is a
real gap, not a stylistic choice.

- **1.0**: captions on effectively every shot, one idea per shot, legible at
  thumbnail size, timed to the read. Bonus signals: a keyword coloured for
  emphasis, or a line stacking under a held line so the reveal lands on the cut.
- **0.6**: captions present and readable but uniform and untimed, or default
  auto-caption styling with no treatment.
- **0.2**: captions on some pieces only, or text that clips the safe area.
- **0**: no burned-in captions anywhere. Apply `no_burned_captions`.

### `ai_tooling` (max 1.0)

The named stack is HeyGen, ElevenLabs, Veo / Google Flow, Google Omni, Seedance
2, GPT Image 2. Motilli additionally wants terminal comfort (pulling a repo,
running a script from a written setup doc).

- **1.0**: names three or more of the stack **and** the Loom shows them working
  in at least one. Watching them drive a tool beats any claim.
- **0.6**: names three or more, Loom shows the workflow but not the tools.
- **0.3**: generic AI claims, or only consumer tools (CapCut AI, Canva, Runway
  alone) with nothing from the stack.
- **0**: no AI generation anywhere. Apply `no_ai_generated_work`.

For Motilli only, subtract 0.3 if they say outright they need a GUI for
everything. The posting warns about this and it is a real failure mode there.

### `throughput` (max 0.5)

Can they hold roughly 5 concepts a day (Velantra) or 3 plus hook variants
(Motilli) without the quality sliding?

- **0.5**: evidence of volume. An in-house or agency role shipping daily, a
  stated weekly output, or a reel with many pieces in one visual system.
- **0.25**: full-time available, no volume evidence either way.
- **0**: part-time only, stacked freelance clients, or a reel of four films that
  clearly took a month each. A beautiful slow editor is a real miss for this
  role and it should show in the number.

---

## Caps

Caps clamp the final total after the weighted sum. They exist so a strong-looking
paper application cannot pin its way past a disqualifying fact.

| Cap key | Ceiling | Use when |
|---|---|---|
| `no_ai_generated_work` | 4.0 | Nothing in the portfolio is AI-generated. |
| `wrong_category` | 5.0 | No work in the required category. |
| `not_direct_response` | 5.0 | Portfolio is brand, event, or personal work. |
| `unverifiable_media` | 5.0 | Nothing playable came back at all. |
| `too_slow` | 4.0 | Average shot length over 5s across the reel. |
| `no_burned_captions` | 5.0 | No burned-in captions anywhere in the reel. |

`unverifiable_media` behaves differently from the others. If the gates passed and
the paper score is above 5.0 but no media opened, the verdict is **review**, not
archive. That pattern is nearly always a permissioned Google Drive folder, and
dropping someone for a sharing setting is a bad screen. `score_ledger.py` handles
this branch; you do not need to special-case it.

---

## Three failure modes to watch for in yourself

**Rewarding polish.** This is the big one, and it now costs points in two places
rather than one. A colour-graded, shallow-depth, music-led reel reads as "high
craft" frame by frame and is further from this benchmark than a scrappy
phone-shot one that cuts hard and puts the right thing under the right line. If
you find yourself impressed, check the shot lengths before you check your
feeling.

**Scoring the reel instead of the match.** `visual_line_match` is the heaviest
component and it is the easiest to skip, because judging it means reading the
caption at a cut and then looking at what is in that exact frame. Do that work
per cut on at least two of their pieces. A summary impression is not a score.

**Believing the cover letter.** Every claim in the text is worth 0 until a frame
or the Loom backs it. Score what you watched.
