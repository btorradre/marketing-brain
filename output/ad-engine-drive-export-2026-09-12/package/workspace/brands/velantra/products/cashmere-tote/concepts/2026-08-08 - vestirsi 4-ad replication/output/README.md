# Vestirsi 4-ad replication — delivered assets

All four ads complete, 2026-08-10.

| File | Runtime | Ref | Engine |
|---|---|---|---|
| `VEL-COL-AD1-final.mp4` | 25.06s | 1 `vestirsi-gQp9r7` | Seedance 2.5, single pass |
| `VEL-COL-AD2-final.mp4` | 23.07s | 2 `tiktok-0SvcYJ` | Seedance 2.5, single pass |
| `VEL-COL-AD3-final.mp4` | 30.08s | 3 `vestirsi-oChMfW` | Seedance 2.5, single pass |
| `VEL-COL-AD3-OFFER-final.mp4` | 33.10s | 3 + price end card | same pass, card in post |
| `VEL-COL-THANKME-02.mp4` | 37.68s | 4 `vestirsi-Zrdgh4` | Omni, creator-led |

Every one carries burned house-style captions cut to **real word timings**, never estimates:
the Omni ad from its ElevenLabs alignment, the three Seedance ads by force-aligning the known
dialogue against Seedance's own rendered audio (`_build/finish_seedance.py`).

## Verification, all four

QA is a full sweep — every frame at 2.5fps in contact sheets, never a sample. Sampling is how
two artifacts shipped earlier in this build: Omni and Seedance failures are *progressive*, the
first second of any shot is clean and the object mutates later, so a sparse sample reliably
lands on good frames. Sheets in `_build/qa-AD1/`, `qa-AD2/`, `qa-AD3/`, `qafull/`.

| Check | AD1 | AD2 | AD3 |
|---|---|---|---|
| Runtime vs declared | 25.056 / 25 | 23.072 / 23 | 30.080 / 30 |
| Cuts declared vs detected | 0 / 0 | 0 / 0 | **5 / 5** |
| Cut placement vs beat map | n/a (oner) | n/a (oner) | all within **0.38s** |
| Dialogue inside its beat window | ✓ | ✓ | ✓ all 6 beats |
| Words force-aligned | ✓ | 58 across 21.5s | 83 across 29.4s |
| Identity / wardrobe / product truth | ✓ | ✓ | ✓ |
| Reference lighting reproduced | ✓ | ✓ | ✓ |

**AD2's two-speaker beat worked first try** — the off-camera friend's "Okay, that is really
cute" lands at 18.3s. That was the single biggest generation risk in the set.

**AD3 is the proof the prompt system works as specified**: one continuous 30-second pass with
5 internal cuts, all landing within 0.38s of where the timeline put them, dialogue in every
beat window, no chaining and no stitching.

## Cost

Seedance 4,914cr (1,449 + 1,575 + 1,890) plus a 315cr 5s pilot = 5,229cr, about $21.
The Omni ad cost a VO generation and ~28 GPT Image 2 keyframes; Omni video itself is on the
Gemini API, not kie.

### The Omni input-block, and the runner bug that hid it

s05 and s07 kept coming back with no video, including 5/5 on a bounded retry. Two separate problems:

1. **My poller was swallowing the reason.** Omni rejects bad input *immediately*, returning an
   `error` field and **no `status` field at all**. The poller only inspected `status`, so it spun for
   the full 10-minute window against an already-dead job and reported a bare "NO VIDEO". It now bails
   in seconds and prints the message. Anyone debugging Omni should check `error` first.
2. **The block was my prompt text, not the images.** Both "blocked" keyframes animated fine from a
   bland prompt, which localised it immediately. The cause was the **negation stack**: the motion
   prompt re-asserted the whole product block plus a footer of `no other people / no text / no music /
   no zoom / no speed change / no slow motion`. Omni's input filter reads that prose and on some
   frames the accumulated negation trips it. Stripping it and stating everything positively — the
   keyframe already carries the product truth, so restating it buys nothing — got both shots through
   on the first attempt. `motion_prompt()` in `_build/ad4v2_shots.py` is now lean and positive, with
   the reasoning recorded in its docstring.

**Key note.** The Gemini key supplied on 2026-08-08 is byte-identical to the `GEMINI_API_KEY` already
in `.env`. It is now also stored as `GEMINI_OMNI_API_KEY`, which the Omni runner prefers, so a genuinely
different key can be swapped in without touching code. The key was never the cause of these failures.

## NOT GENERATED — blocked on kie credits

`VEL-COL-POV-01` (25s), `VEL-COL-OBSESSED-01` (23s), `VEL-COL-SPEC-01` (30s).

All three prompts are final, linted and fireable, with lighting written from each reference. Refs are
uploaded and cached in `_build/state.json`. createTask was attempted twice and hard-rejected:

```
402 Credits insufficient
balance 1208.3 then 1112.3, need 1575 / 1449 / 1890 (4914 total, about $20)
```

Nothing was charged — kie does not bill a rejected createTask. Auto top-up did not fire, and the
balance went **down** 96 credits between attempts, so something else on the account is drawing on it.

To run them the moment there are credits:

```
cd "_build" && python3 run.py fire AD1 AD2 AD3
python3 run.py poll        # downloads to output/ when each finishes
```

## Still open

- **Ship date.** "Early October" has been an unconfirmed supplier placeholder since 7/27 and
  `THANKME-02` says it out loud at 33.07s. Confirm the lead time or re-cut that line.
- **Listen to the VO before it runs.** I cannot hear audio. The automated judge I used proved
  unreliable, so its scores are not evidence. An isolated slice test did confirm "Loro Piana" reads
  correctly as *pee-AH-na*; "Colette" lands closer to *CO-let* than *co-LET*.
