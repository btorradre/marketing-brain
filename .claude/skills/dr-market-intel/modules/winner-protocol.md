# Winner protocol — make the learning outlive the ad

Most brands find a winner and let it run until it dies, then start the next brief from nothing. A documented winner is the foundation of every brief that comes after it, which is the entire reason this protocol exists.

Run it while the ad is still spending, not after it has died. Fatigue signals are easier to name when you can still see them arriving.

## Operating rules

1. **Diagnose, do not describe.** Anyone can describe what an ad does. Explain why each element works psychologically and strategically.
2. **Separate hook from angle.** The hook is the opening move. The angle is the entire idea the ad is built around. They are not the same thing, and conflating them is why iterations fail: teams rewrite the hook and think they tested a new angle.
3. **Map to one awareness level** and explain why it works there and not elsewhere.
4. **Every finding ends transferable.** "This works because [mechanism]. This means future briefs should [specific action]." A finding that does not produce an instruction is trivia.
5. **Name what could kill it.** The signs this ad is starting to die, and what to test when it does.

## Inputs worth gathering first

- The creative itself. For video, run the `ad-watcher` skill for a beat-by-beat teardown, then layer this strategic pass on top. Do not re-derive what `ad-watcher` already produces.
- Performance from `_engine/creative-tracker/creative-tracker.csv` (spend, cpa, roas, hook_rate, hold_rate, ctr) and `pull_performance.py` for fresh numbers.
- The Meta account itself for frequency and delivery trend. Reads work on `act_1481421530341223`; writes are blocked and the app is in dev mode.
- The angle record this ad came from, if it exists in `angle-bank.md`.

Never estimate a performance number. If the tracker row is empty, say the row is empty.

## Output sections

### SECTION 1 — STRUCTURAL DIAGNOSIS

- **Hook**: what it is, who it speaks to, why it stops the scroll
- **Angle**: the single core idea, one sentence
- **Golden nugget**: the deep frame it is actually built on, and whether the ad leads with it or buries it
- **Awareness level** and why
- **Format**: why this format serves this angle
- **Opening loop**: what question the hook creates, and the timestamp where the ad answers it

### SECTION 2 — PSYCHOLOGICAL MECHANICS

- Which human desire or fear does this speak to at its core?
- The emotional journey from hook to CTA, beat by beat
- What objections it handles, and how
- What trust signals it uses
- What makes it feel native rather than like an ad

### SECTION 3 — LANGUAGE ANALYSIS

- Which specific phrases are doing the most work?
- Is there customer language present? Quote it, and trace it back to the VoC index entry if it is there. An ad whose best line came from a real review is the strongest possible argument for funding more VoC mining.
- The single most powerful line, and why

### SECTION 4 — TRANSFERABLE FRAMEWORK

Minimum five principles, each completing: *"This works because [mechanism]. This means future briefs should [specific action]."*

These are the lines that get copied into the next brief, so write them as instructions rather than observations.

### SECTION 5 — ITERATION ROADMAP

- **Same hook, new format**: which format to test next
- **Same format, new hook**: 3 alternative hooks for the same angle
- **Same angle, new awareness level**: what this ad looks like one step higher in the funnel
- **Fatigue signals**: which metrics say it is dying. Hook rate falling with CTR holding means the opening is worn out and the body still works, so change the first three seconds only. CPM falling alongside flat spend means delivery is decaying rather than the creative failing.
- **The first iteration to test**, named specifically

## Writing back

Write to `brands/<brand>/research/dr-os/winners/<asset_id>.md` (`artifact: winner`).

Then update the angle record in `angle-bank.md`: append this `asset_id` to `tested_assets`, set `verdict: winner`, and set `saturation: tested-by-us`. If the winner came from an angle not yet in the bank, create the record now, because a proven angle with no record is exactly the loss this OS was built to stop.
