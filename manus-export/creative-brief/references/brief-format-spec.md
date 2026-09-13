# Annotated field-by-field spec

### Title

```
# <Concept ID> | <Concept Name>
```

The concept ID should follow a stable per-brand numbering convention. Never guess or reuse an ID. The name is what the team will actually say out loud when referring to this concept — e.g. "The Drawer Full of Started Routines." Name the **moment**, not the benefit: "The $300 Cabinet" is a good name; "Better Digestion" is not.

### Header block

Six bold-label lines. No table — each is one line, two at most.

| Line | What goes in it |
|---|---|
| **Sub-avatar** | Who specifically, in one sentence, ending in the state they're in right now. Not a demographic. |
| **The One Angle** | The problem, stated as the thing she should do or notice. One sentence. This is the whole ad in a line. |
| **Format** | The shape: length class, who's on camera, what the visual journey is, where the product lands. |
| **Product** | Brand + SKU + colorway/variant. Load verified product truth before writing a single Visual line. |
| **Landing Page** | Page name + awareness tag (HOT / WARM / COLD), then the URL on the next line. |
| **Inspiration** | The reference ad's URL, if adapting one. One link. |

Add a seventh line naming a specific persona/page only when the concept is running under one.

The One Angle is the field that does the actual work — everything below it has to serve that one line, and anything that doesn't gets cut. An angle is always the **problem**, never the claim; the claim is the hook.

### 1. Concept

Four sub-headings, written as prose, no bullets. This section is the strategist explaining the reasoning once, so the editor can make judgment calls without having to ask follow-up questions.

- **WHY** — why this person, right now. The state she's in. What wears her down. Not the mechanism, not the product. This is the golden nugget, stated plainly.
- **WHAT** — what the ad literally is, in three or four sentences, including what it deliberately is *not* (e.g. no named competitors, no doctor-authority framing, never claims to be an actual customer if it isn't). These negatives are just as load-bearing as the positive description.
- **HOW** — the shape of the execution, beat by beat, in one paragraph: where it opens, what sequence it moves through, what it teaches exactly once, and **the exact timecode the product is withheld until.** Close with a note on the overall cutting rhythm.
- **Runtime** — one line: total seconds, and what's variable (the hook/bridge choice) versus shared (everything after).

### 2. Ad Structure

The spine of the brief. Every beat is exactly two lines, no more:

```
### <Beat name> | <m:ss>-<m:ss>

**Spoken:** "verbatim VO, in quotes"

**Visual:** One to three sentences. What is on screen. Never a mood description.
```

**Beat order:**

1. `Hook 1 | 0:00-0:08` → `Bridge 1 | 0:08-0:17`
2. `Hook 2 | 0:00-0:08` → `Bridge 2 | 0:08-0:17`
3. `Hook 3 | 0:00-0:08` → `Bridge 3 | 0:08-0:17`
4. `Shared Body | 0:17-<end>` — a header, then timecode-only sub-beats: `**0:17-0:31**`, `**0:31-0:48**`, and so on.
5. `CTA | <m:ss>-<m:ss>`

Hooks and bridges are matched, swappable pairs sharing the same timecode — one ad, three different openings, three finished creative variants out of a single edit. Pick one Hook plus its matching Bridge; the shared body and CTA run identically no matter which pair was chosen. This is the entire reason the format exists. Never write a Hook 2 that only makes sense paired with Bridge 1.

Sub-beats inside the Shared Body get only a timecode, no beat name — the Spoken line itself tells the reader where they are.

**Visual line rules:**
- Concrete nouns. "Overhead shot of the kitchen table, phone and notepad spread out" — never "establish the research mood."
- On-screen text goes verbatim in backticks, so it can be copied character-for-character and never paraphrased.
- State clearly whether real existing footage should be used (and roughly what/where) before falling back to a generation instruction as a last resort. Refer to footage by content description, never by a specific local file path.
- The product's first appearance names its exact timecode, both in the Visual line and again in the HOW paragraph.

### 3. Editing Notes

Bullets only — and only constraints that could actually be checked by looking at the finished timeline. Each one is either a hard *never* or a hard *always*, ideally with a specific number attached.

Good: "Do not show the product or a readable label before 1:28." "New B-roll every 1 to 4 seconds."
Bad: "Keep it feeling authentic."

Always include whichever of these apply:
- Any disclosure that must stay on screen throughout.
- The cut rhythm, stated as a number.
- The product-reveal timecode.
- Whether competitor products shown should look generic/unreadable, or use real recognizable trade dress.
- What the ad may never show (an implied physical result, a before/after comparison, clinical imagery).
- A reminder to verify the live offer and guarantee on the destination page on the day of launch/export, before final delivery.

Roughly six bullets is a healthy brief. Twelve usually means strategy has leaked in from Section 1.

### Media Buyer Only — ad copy

Clearly walled off (e.g. with a warning marker) so an editor knows to stop reading at this point. Opens with one line:

> Media buyer: verify the live offer and destination before launch.

Then: **Primary Text #1**, **Primary Text #2**, **Headline #1**, **Headline #2**.

Each Primary Text is written as short paragraphs separated by blank lines, ends with a soft call to action ("Check the formula at the link below."), then the bare destination URL on its own line. Headlines are four to six words, no punctuation, consistently sentence-cased or title-cased.

Always provide two of each — the media buyer picks which to run, the strategist doesn't decide that.

### What is deliberately left out of this format

No asset checklist. No delivery specs. No production-method preamble. No separate psychographic-reasoning section. No named prompt blocks. No shot tables.

Those things belong elsewhere: psychographic reasoning stays in working/scratch notes, delivery specs live in a standing production SOP, generation prompts live in whatever product-specific reference material exists. The brief is the strategist's decisions plus the editor's instructions, and nothing else. If it grows past roughly two screens of scrolling, something has leaked in that belongs in a different document.
