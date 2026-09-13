# B-roll storytelling skill — qualitative review

Reviewed September 10, 2026. Read `SKILL.md`, all four reference files, the planning template and `agents/openai.yaml` at `/Users/brooksorradre2/.codex/skills/broll-storytelling/`. This is a qualitative walkthrough of three hypothetical cases, not a benchmark or empirical model evaluation. No assets were generated, ads changed or external services used. The skill was not edited.

## Assessment

The skill supports all three requested cases. Its strongest protections are choosing the sentence's purpose before the image, allowing a deliberate stay-on-presenter decision, specifying an observable action, preserving speaker turns, separating source appearance from actual provenance and refusing to treat attractive science illustrations as evidence. The non-health example demonstrates transfer beyond the four health references. No major logic contradiction found.

### Case 1 — personal UGC agitation

Hypothetical line: “I had barely started dinner and I was already pushing the plate away.”

**Decision:** brief full-frame insert of the approved protagonist at her ordinary dining table, captured by a propped phone at seated chest height. One dominant action: she pushes the partly eaten plate a short distance away and pauses, looking at the meal. Available room/window light, normal depth of field, no cinematic move or exaggerated pain. Enter on the first mention of dinner; remain until the plate movement is readable, provisionally around 2–3 seconds if final narration permits. Return to her face for the personal interpretation. Exact duration stays pending voice alignment.

**Why the skill succeeds:** it produces an executable phone-style behavior rather than a generic belly-clutch, stock sad face or anatomy shot. Capture origin remains labeled generated reenactment if generated. A separate insert is unnecessary when the original storyteller's gesture already conveys the moment. One caution for execution: do not automatically select “dinner discomfort” footage that actually shows distaste for food; inspect the action and neighboring context.

### Case 2 — podcast explanation

Hypothetical structure: host asks why a process slows; guest orients the answer, explains movement and then a barrier; host reacts and asks a follow-up. Scientific claims are assumed to require appropriate factual support before illustration.

**Decision:** preserve the host's question and guest's first answer sentence on their existing cameras. For the supported transport sentence, use a longitudinal process view with a visible direction of movement. Return to the guest for the qualification. If a separately supported barrier sentence follows, use a distinct wall cross-section showing the relevant sides and crossing behavior; do not recolor/reuse the transport tunnel. Keep the host visible for the reaction and follow-up. Each insert enters on its causal referent and exits after the stated interaction becomes understandable, respecting final word alignment.

**Why the skill succeeds:** its structure table and question → explanation → reaction rule protect the conversation, while its location/scale/action framework distinguishes two scientific ideas. One template improvement would make this more reliable: add an explicit speaker/turn field to each beat row, rather than relying on the writer to embed speaker IDs in narration text.

### Case 3 — non-health tote ad

Hypothetical sequence: searching frustration → useful construction detail → real packing → convenient retrieval. Exact tote features, dimensions and demonstrated contents must come from verified references; none are assumed here.

**Decision sequence:**

1. **Search frustration:** candid over-shoulder phone view of the owner searching among visible contents at a doorway. One readable action: move items aside while looking for keys. Avoid anatomy, generic stress imagery and implausibly chaotic props.
2. **Construction:** distinct close view of the actual relevant opening/pocket/closure, with a hand tracing or operating it. Select the construction feature that actually exists and supports the line; otherwise record the missing product evidence as an asset gap. A real detail demonstration is the appropriate mechanism view.
3. **Packing:** stable overhead hands-and-product view showing verified items being placed in the bag at true scale. Give the demonstration enough time; do not claim capacity from an uncalibrated generated image or cram a multi-item packing sequence into a tiny insert.
4. **Payoff:** new scene outside the original doorway, showing the owner retrieving the keys directly and continuing her trip. It answers the original search problem through changed behavior and a fresh composition.

**Why the skill succeeds:** the matrix already has an explicit tote example and supports object mechanisms, truthful product use and specific regained activity. A small main-table wording change would reduce remaining health bias: “Problem mechanism → scientifically appropriate diagram/process view” should include real product-mechanics demonstrations explicitly.

## Recommended fixes before final delivery

1. **Correct exact FPS:** `references/reference-lessons.md` lists 99jcKo as `30000/1001fps`. Saved source metadata reports both `r_frame_rate` and `avg_frame_rate` as `2997/100` (29.97 exactly). The shot map used the latter. This is a small but concrete evidence error.
2. **Resolve reference atlas:** the reference file states that `reference-atlas.jpg` exists in the research root, but it was absent at review time. Generate it as planned or remove/change the reference. All other tested local Markdown links and named analysis/shot-map files resolve.
3. **Make speaker turns explicit in template:** add `speaker / turn` to the beat schedule or require it within each narration cell. This preserves podcast handoffs when rows are handed to production.
4. **Broaden main mechanism default:** use a relevant causal/process demonstration for non-health products and scientifically appropriate process imagery for biology. The supporting non-health example already does this; aligning the main summary prevents overfitting.
5. **Clarify Cut Room wording:** template pipeline currently says “Cut Room storyboard delivery when requested.” Main skill correctly says “If delivering a storyboard.” Prefer “whenever the delivery includes a storyboard” in the template so an implicitly authorized storyboard is not accidentally delivered as Markdown alone.

## Process and path checks

The skill appropriately separates analysis, selection, storyboard, generation and editing authorization. It does not introduce a fresh approval gate and correctly keeps research outputs separate from production boards. The full template is detailed but reasonable for an ad; use its existing-plan integration and omit nonapplicable sections for a compact selection task instead of creating a duplicate process.

No missing local Markdown targets were found. The workspace Cut Room skill, Velantra registry and scale/fidelity file exist. All four analysis files and CSV/JSON shot maps exist. The atlas was the only referenced artifact found absent. Source-specific performance and medical claims remain qualified, and music/SFX assessment is accurately identified as unaudited.

## Fixes applied after review

Corrected the exact 99jcKo FPS to 2997/100. Generated and visually inspected reference-atlas.jpg. Added speaker-turn to the schedule template. Expanded mechanism choices to include real product/task demonstrations. Clarified that every storyboard delivery goes to Cut Room. The skill-creator validator passes and all linked support files resolve.
