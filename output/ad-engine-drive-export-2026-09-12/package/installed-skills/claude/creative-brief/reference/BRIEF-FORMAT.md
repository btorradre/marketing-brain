# The creative brief format — annotated spec

Five parts, in this order, nothing else. If a thing you want to say does not fit one of
these five, it does not go in the brief.

```
Title
Header block          6 lines
1. Concept            WHY / WHAT / HOW / Runtime
2. Ad Structure       Hooks + Bridges → Shared Body → CTA
3. Editing Notes      bullets
⛔ MEDIA BUYER ONLY   ad copy
```

---

## Title

```markdown
# <BRAND>-VID-NNN | <Concept Name>
```

The ID comes from `publish_brief.py --brand <Brand> --next-id`. Never guess it.
The name is what the team will say out loud: "The Drawer Full of Started Routines."
Name the **moment**, not the benefit. "The $300 Cabinet" is a name. "Better Digestion" is not.

---

## Header block

Six bold-label lines. No table. Each one line, two at most.

| Line | What goes in it |
|---|---|
| **Sub-avatar** | Who specifically, in one sentence, ending in the state they're in right now. Not a demographic. |
| **The One Angle** | The problem, stated as the thing she should do or notice. One sentence. This is the whole ad in a line. |
| **Format** | The shape: length class, who's on camera, what the visual journey is, where the product lands. |
| **Product** | Brand + SKU + colorway/variant. Load the product-scale skill for it before writing a single Visual line. |
| **Landing Page** | Page name + awareness tag `(HOT / WARM / COLD)`, then the URL on the next line. |
| **Inspiration** | The reference ad URL. One link. |

Add **Facebook Page** as a seventh line only when the concept ships to a persona page.

The One Angle is the field that does the work. Everything below it has to serve that
one line, and anything that doesn't gets cut. Per house law: an angle is the **problem**,
not the claim. The claim is the hook.

---

## 1. Concept

Four sub-headings. Prose, no bullets. This section is the strategist explaining himself
to the editor once, so the editor can make judgment calls without asking.

- **WHY** — why this person, right now. The state she's in. What wears her down.
  Not the mechanism, not the product. This is the golden nugget stated plainly.
- **WHAT** — what the ad literally is, in three or four sentences, including what it
  deliberately is *not* (no named competitors, no doctor authority, never claims to be
  a customer). The negatives here are as load-bearing as the positives.
- **HOW** — the shape of the execution beat to beat, in one paragraph. Where it opens,
  what sequence it moves through, what it teaches once, **and the timecode the product
  is withheld until.** Close with the cutting rhythm.
- **Runtime** — one line. Total seconds, and what's variable vs shared.

---

## 2. Ad Structure

The spine. Every beat is exactly two lines and no more:

```markdown
### <Beat name> | <m:ss>-<m:ss>

**Spoken:** "verbatim VO, in quotes"

**Visual:** One to three sentences. What is on screen. Never a mood description.
```

**Beat order:**

1. `Hook 1 | 0:00-0:08` → `Bridge 1 | 0:08-0:17`
2. `Hook 2 | 0:00-0:08` → `Bridge 2 | 0:08-0:17`
3. `Hook 3 | 0:00-0:08` → `Bridge 3 | 0:08-0:17`
4. `Shared Body | 0:17-1:55` — a header, then timecode-only sub-beats: `**0:17-0:31**`, `**0:31-0:48**`, …
5. `CTA | 1:55-2:00`

Hooks and bridges are **matched swappable pairs** on the same timecode — one ad, three
openings, three creatives out of one edit. Pick one Hook + its matching Bridge, then the
shared body and CTA run identically. This is the whole reason the format exists: it turns
one brief into three ad variants without three edits. Never write a Hook 2 that only works
with Bridge 1.

Sub-beats in the Shared Body get a timecode and nothing else — no beat names. The Spoken
line tells the editor where he is.

**Visual line rules:**
- Concrete nouns. "Overhead shot of the kitchen table, phone and notepad spread out" — not
  "establish the research mood."
- Name the **on-screen text verbatim in backticks**. Anything the editor must burn in
  is inline code, so it can be copied character for character and never paraphrased.
- Carry the real-footage law inline. When footage exists: `Use: <folder name> — <which clip>.`
  and only then `Only if missing — Make: <one short prompt sentence>.` Folder names only,
  never a local file path — the editor is external.
- The product's first appearance names its exact timecode, in the Visual line and again in HOW.

---

## 3. Editing Notes

Bullets. Only constraints the editor can be held to by looking at the timeline. Each one
is either a hard *never* or a hard *always* with a number attached.

Good: "Do not show the pouch or a readable label before 1:28." "New B-roll every 1 to 4 seconds."
Bad: "Keep it feeling authentic."

Always carry in whichever of these apply:
- The disclosure that must stay on screen throughout.
- The cut rhythm, as a number.
- The product-reveal timecode.
- What competitor products may look like (generic + unreadable, or real trade dress — brand law decides).
- What the ad may never show (implied physical result, before/after, clinical imagery).
- **Verify the live offer and guarantee on the destination page on launch day before export.**

Six bullets is a healthy brief. Twelve means strategy leaked in here from section 1.

---

## ⛔ MEDIA BUYER ONLY - Facebook Ad Copy

Walled off with the ⛔ so the editor knows to stop reading. Opens with one line:

> Media buyer: verify the live offer and destination before launch.

Then: **Primary Text #1**, **Primary Text #2**, **Headline #1**, **Headline #2**.

Each Primary Text is short paragraphs separated by blank lines, ends with a soft direction
("Check the formula at the link below.") and then the bare destination URL on its own line.
Headlines are four to six words, no punctuation, sentence-cased or title-cased consistently.

Two of each, always. The buyer picks; the strategist does not.

---

## What is deliberately not in this format

No asset checklist. No delivery specs. No production-method preamble. No psychographic
section. No named prompt blocks. No shot tables.

Those live elsewhere — psychographic reasoning in the working file, delivery specs in the
standing editor SOP, generation prompts in the product-scale skill. The brief is the
strategist's decisions and the editor's instructions, and nothing else. When it grows past
two screens of scrolling, something has leaked in that belongs in another document.
